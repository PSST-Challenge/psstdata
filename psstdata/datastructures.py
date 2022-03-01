import dataclasses
import datetime
import itertools
import numbers
import os
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from typing import Iterable, Iterator, Union, Tuple

from psstdata import WAV_FRAME_RATE
from psstdata._system import read_tsv
from psstdata.versioning import PSSTVersion


class AQSeverity(Enum):
    MILD = 100
    MODERATE = 75
    SEVERE = 50
    VERY_SEVERE = 25
    UNKNOWN = -1

    @classmethod
    def from_score(cls, aq_index: Union[numbers.Number, str]):
        # See this: ________
        try:
            if aq_index is None:
                return cls.UNKNOWN
            aq_index = float(aq_index)
            return next(s for s in (cls.VERY_SEVERE, cls.SEVERE, cls.MODERATE, cls.MILD) if aq_index < s.value)
        except Exception as e:
            raise ValueError(f"Could not classify AQ score into severity: {e}")

    def __str__(self):
        return self.name

    def __gt__(self, other):
        return self.value > other.value

    def __lt__(self, other):
        return self.value < other.value


@dataclass(frozen=True)
class PSSTSessionMetadata:
    session: str
    aq_index: float

    @property
    def severity(self):
        return AQSeverity.from_score(self.aq_index)


@dataclass(frozen=True)
class PSSTUtterance:
    id: str
    session: str
    prompt: str
    transcript_ipa: str
    transcript_arpabet: str
    filename: str
    duration_frames: int
    aq_index: float = None
    is_correct: bool = None

    root_dir: str = dataclasses.field(default=None, repr=False)

    @property
    def filename_absolute(self):
        if not self.root_dir:
            raise NotADirectoryError(self.root_dir)

        if self.filename[:5] in ("train", "valid", "test/"):
            # Fix for pre-release data. Delete once data is officially released.
            return os.path.abspath(os.path.join(os.path.dirname(self.root_dir), self.filename))

        return os.path.abspath(os.path.join(self.root_dir, self.filename))

    @property
    def duration(self) -> datetime.timedelta:
        return datetime.timedelta(seconds=self.duration_seconds)

    @property
    def duration_seconds(self) -> float:
        return self.duration_frames / WAV_FRAME_RATE

    @property
    def session_metadata(self) -> PSSTSessionMetadata:
        return PSSTSessionMetadata(self.session, self.aq_index)


@dataclass(frozen=True)
class PSSTUtteranceCollection(Iterable[PSSTUtterance]):
    utterances: Tuple[PSSTUtterance, ...]

    def __post_init__(self):
        assert isinstance(self.utterances, tuple), "Utterances must be a tuple."

    def __iter__(self) -> Iterator[PSSTUtterance]:
        yield from self.utterances

    def __len__(self):
        return len(self.utterances)

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.utterances[item]
        if isinstance(item, str):
            return next(u for u in self.utterances if u.id == item)
        raise NotImplementedError()

    @lru_cache()
    def sessions(self):
        by_session = itertools.groupby(sorted(self.utterances, key=lambda s: s.session), key=lambda s: s.session_metadata)
        return {
            session: PSSTUtteranceCollection(tuple(session_utterances))
            for session, session_utterances in by_session
        }

    def ids(self):
        return tuple(u.id for u in self.utterances)

    @classmethod
    def from_tsv(cls, tsv_file):
        split_data = read_tsv(tsv_file, PSSTUtterance)
        root_dir = os.path.dirname(tsv_file)
        split_data = (dataclasses.replace(u, root_dir=root_dir) for u in split_data)
        return cls(tuple(split_data))


@dataclass(frozen=True)
class PSSTData:
    train: PSSTUtteranceCollection
    valid: PSSTUtteranceCollection
    test: PSSTUtteranceCollection

    version: PSSTVersion

    test_is_placeholder: bool = False

    def __post_init__(self):
        assert not set(self.train.sessions()).intersection(self.test.sessions()), \
            "train/test have overlapping sessions!"
        assert not set(self.train.sessions()).intersection(self.valid.sessions()), \
            "train/valid have overlapping sessions!"
        assert self.test_is_placeholder or not set(self.valid.sessions()).intersection(self.test.sessions()), \
            "valid/test have overlapping sessions!"

    def __iter__(self):
        return iter((self.train, self.valid, self.test))

    def items(self):
        return zip(("train", "valid", "test"), self)

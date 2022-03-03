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


@dataclass(frozen=True)
class PSSTUtterance:
    """
    A record from utterances.tsv, and a response to an item in the Boston Naming Test (BNT) or Verb Naming Test (VNT).

    utterance_id (str):     a unique identifier for each production, of the form
                            {session}-{test}{item}-{prompt} (e.g. "ACWT02a-BNT01-house")
    session (str):          the name of the AphasiaBank session from which the production was taken
    test (str):             indicates which test each utterance comes from, either `BNT` (Boston
                            Naming Test) or `VNT` (Verb Naming Test)
    prompt (str):           an orthographic rendering of the target word. Silence is marked using
                            `<sil>`. Spoken noise is marked using `<spn>`
    transcript (str):       is the phonemic transcription of the production, in ARPAbet.
    correctness (bool):     marked as `TRUE` if the production is "correct" according to the
                            clinical scoring rules of the BNT/VNT, `FALSE` otherwise
    aq_index (float):       is the participant's Aphasia Quotient (AQ).  AQ is the Western Aphasia
                            Battery - Revised Aphasia Quotient (Kertesz, 2007) and it is a
                            standardized total score that reflects overall aphasia severity. Values
                            can fall between between 0.0 and 100.0. A lower number indicates higher
                            severity.
    duration_frames (int):  the number of audio frames in each recording, or the duration in
                            seconds times 16000
    filename (str):         the relative path within the data pack to the file containing the audio
                            recording for this production
    """

    utterance_id: str
    session: str
    test: str
    prompt: str
    transcript: str
    correctness: bool
    aq_index: float
    duration_frames: int
    filename: str

    root_dir: str = dataclasses.field(default=None, repr=False)

    @property
    def filename_absolute(self):
        if not self.root_dir:
            raise NotADirectoryError(self.root_dir)
        return os.path.abspath(os.path.join(self.root_dir, self.filename))

    @property
    def duration(self) -> datetime.timedelta:
        return datetime.timedelta(seconds=self.duration_seconds)

    @property
    def duration_seconds(self) -> float:
        return self.duration_frames / WAV_FRAME_RATE

    @property
    def session_metadata(self) -> "PSSTSessionMetadata":
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
        if isinstance(item, (int, slice)):
            return self.utterances[item]
        if isinstance(item, str):
            return next(u for u in self.utterances if u.utterance_id == item)
        raise NotImplementedError()

    @lru_cache()
    def sessions(self):
        by_session = itertools.groupby(sorted(self.utterances, key=lambda s: s.session), key=lambda s: s.session_metadata)
        return {
            session: PSSTUtteranceCollection(tuple(session_utterances))
            for session, session_utterances in by_session
        }

    def utterance_ids(self):
        return tuple(u.utterance_id for u in self.utterances)

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


@dataclass(frozen=True)
class PSSTSessionMetadata:
    session: str
    aq_index: float

    @property
    def severity(self) -> "AQSeverity":
        return AQSeverity.from_score(self.aq_index)


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

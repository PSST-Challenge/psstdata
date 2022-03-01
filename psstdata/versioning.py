import dataclasses
import json
import os
from dataclasses import dataclass
from json import JSONDecodeError
from typing import Dict, Tuple

import psstdata
from psstdata import CORRECTNESS_TASK, PHONEME_RECOGNITION_TASK
from psstdata._system import cast_dict


@dataclass
class PSSTVersion:
    version_id: str
    files: Dict[str, str]
    root_dir: str
    comment: str = ""

    def __post_init__(self):
        assert self.root_dir is not None

    def local_dir(self):
        return os.path.join(self.root_dir, f"psst-data-{self.version_id}")

    def files_phoneme_recognition_task(self):
        return self.task_files(task=PHONEME_RECOGNITION_TASK)

    def files_correctness_task(self):
        return self.task_files(task=CORRECTNESS_TASK)

    def task_files(self, task):
        results = {}
        for split_name, file in self.files.items():
            if file is None:
                results[split_name] = None
            else:
                results[split_name] = self._get_path(f"{split_name}/{task}_{split_name}.tsv")
        return results

    def _get_path(self, file):
        if file is None:
            return None
        return os.path.join(self.local_dir(), file)



@dataclass
class PSSTVersionCollection:
    comment: str = "Most recent versions are first in the list."
    versions: Tuple[PSSTVersion] = tuple()

    def __iter__(self):
        return iter(v.version_id for v in self.versions)

    def latest(self):
        if not len(self.versions):
            raise KeyError(f"[latest]")
        return tuple(self.versions)[0]

    def __getitem__(self, version_id):
        version = next((v for v in self.versions if v.version_id==version_id), None)
        if version is None:
            raise KeyError(version_id)
        return version

    def apply_dir(self, dir):
        return PSSTVersionCollection(
            comment=self.comment,
            versions=tuple(dataclasses.replace(v, root_dir=dir) for v in self.versions)
        )

    @classmethod
    def from_object(cls, obj, root_dir, version_filter=lambda v: True):
        versions = (cast_dict({**v, "root_dir": root_dir}, PSSTVersion) for v in obj["versions"])
        return cls(
            comment=obj["comment"],
            versions=tuple([v for v in versions if version_filter(v)])
        )

    @classmethod
    def from_disk(cls, dir):
        def check_version(version: PSSTVersion):
            for task in CORRECTNESS_TASK, PHONEME_RECOGNITION_TASK:
                for split, tsv in version.task_files(task=task).items():
                    if tsv is None:
                        continue
                    if not os.path.exists(tsv):
                        psstdata.logger.warning(f"Missing file {tsv}")
                        return False
            return True

        version_file = os.path.join(dir, "versions.json")
        try:
            with open(version_file) as f:
                return PSSTVersionCollection.from_object(
                    json.load(f),
                    version_filter=check_version,
                    root_dir=dir
                )
        except (FileNotFoundError, JSONDecodeError):
            return PSSTVersionCollection()

    def save(self, dir):
        version_file = os.path.join(dir, "versions.json")
        os.makedirs(dir, exist_ok=True)
        data = dataclasses.asdict(self)
        for version in data["versions"]:
            del version["root_dir"]
        with open(version_file, "w") as f:
            json.dump(data, f, indent=4)

import dataclasses
import json
import os
from dataclasses import dataclass
from functools import lru_cache

from psstdata._system import read_json

CONFIG_DIR = os.path.expanduser("~/.config/psstdata")
CONFIG_FILE_SETTINGS = os.path.expanduser("~/.config/psstdata/settings.json")

AUTH_COMMENT = "Check the README.md at https://github.com/PSST-Challenge/psstdata for help getting access."


@dataclass
class PSSTSettings:
    comment: str = AUTH_COMMENT

    local_dir: str = "~/psst-data"
    base_url: str = "https://media.talkbank.org/aphasia/RaPID"

    parallel_n_jobs: int = 1
    auth_server: str = "https://sla2.talkbank.org:1515"
    download_username: str = ""
    download_password: str = ""

    def save(self):
        os.makedirs(os.path.dirname(CONFIG_FILE_SETTINGS), exist_ok=True)
        with open(CONFIG_FILE_SETTINGS, "w") as f:
            default_settings = dataclasses.asdict(self)
            json.dump(default_settings, f, indent=1)
        self.load.cache_clear()
        return self

    @classmethod
    @lru_cache()
    def load(cls):
        if not os.path.isfile(CONFIG_FILE_SETTINGS):
            return cls().save()
        try:
            return read_json(CONFIG_FILE_SETTINGS, cls)
        except Exception as e:
            raise FileNotFoundError(f"Settings file {CONFIG_FILE_SETTINGS} is possibly corrupt.") from e

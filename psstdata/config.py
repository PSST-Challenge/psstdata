import dataclasses
import json
import os
from dataclasses import dataclass

CONFIG_DIR = os.path.expanduser("~/.config/psstdata")
CONFIG_FILE_SETTINGS = os.path.expanduser("~/.config/psstdata/settings.json")


@dataclass
class PSSTSettings:
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
        return self

    @classmethod
    def load(cls):
        if not os.path.isfile(CONFIG_FILE_SETTINGS):
            return cls().save()
        try:
            with open(CONFIG_FILE_SETTINGS) as f:
                settings_dict = json.load(f)
                return cls(**settings_dict)
        except Exception as e:
            raise FileNotFoundError(f"Settings file {CONFIG_FILE_SETTINGS} is possibly corrupt.") from e

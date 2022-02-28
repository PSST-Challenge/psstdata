import csv
import dataclasses
import logging
import os
from functools import lru_cache
from typing import Type

import psstdata
from psstdata import PHONEME_RECOGNITION_TASK, CORRECTNESS_TASK
from psstdata.config import PSSTSettings
from psstdata.datastructures import PSSTData, PSSTUtteranceCollection
from psstdata.downloading import PSSTDownloader


def load_asr(
        *,
        local_dir: str = None,
        version_id: str = None,
        log_level=logging.INFO,
        artificial: bool = False
) -> PSSTData:
    return _load(
        local_dir=local_dir,
        version_id=version_id,
        task=PHONEME_RECOGNITION_TASK,
        log_level=log_level,
        artificial=artificial
    )


def load_correctness(
        *,
        local_dir: str = None,
        version_id: str = None,
        log_level=logging.INFO,
        artificial: bool = False
) -> PSSTData:
    return _load(
        local_dir=local_dir,
        version_id=version_id,
        task=CORRECTNESS_TASK,
        log_level=log_level,
        artificial=artificial
    )


def _load(
        *,
        local_dir,
        task: str,
        version_id: str = None,
        log_level=logging.INFO,
        artificial: bool = False
) -> PSSTData:
    psstdata.logger.setLevel(log_level)

    if artificial:
        local_dir = os.path.join(os.path.dirname(psstdata.__file__), "artificialdata")
        version_id = "ARTIFICIAL"

    if local_dir is None:
        settings = PSSTSettings.load()
        local_dir = settings.local_dir
    local_dir = os.path.expanduser(local_dir)

    valid_as_test = False

    with PSSTDownloader() as downloader:
        version = downloader.download(local_dir, version_id=version_id)
        psstdata.logger.info(f"Loaded data `{task}` version {version.version_id} from {local_dir}")
        if not os.path.exists(local_dir):
            raise FileNotFoundError(local_dir)

        tsv_files = version.task_files(task=task)

        if version.files["test"] is None:
            psstdata.logger.warning(
                f"The PSST `train` and `valid` sets were downloaded, but `test` is not yet released. "
                f"Using a copy of the `valid` data as a placeholder."
            )
            tsv_files["test"] = tsv_files["valid"]
            valid_as_test = True

        data = {}
        for split, tsv_file in tsv_files.items():
            data[split] = PSSTUtteranceCollection.from_tsv(tsv_file)

        return PSSTData(**data, version=version, test_is_placeholder=valid_as_test)


def _read_tsv(tsv_file: str, t: Type):
    items = []
    row_factory = _read_tsv_row_factory(t)
    with open(tsv_file) as f:
        reader = csv.reader(f, dialect=csv.excel_tab)
        columns = next(reader)
        for row in reader:
            item = row_factory(columns, row)
            items.append(item)
    return items


@lru_cache()
def _read_tsv_row_factory(t: Type):
    fields = {
        field.name: field.type
        for field in dataclasses.fields(t)
    }

    def cast(columns, row):
        return t(**{
            column: fields[column](value)
            for column, value in zip(columns, row)
        })

    return cast

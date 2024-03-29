import logging
import os

import psstdata
from psstdata._system import cast_dict
from psstdata.config import PSSTSettings
from psstdata.datastructures import PSSTData, PSSTUtteranceCollection
from psstdata.downloading import download


def load(
        version_id: str = None,
        *,
        local_dir: str = None,
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

    version = download(local_dir, version_id=version_id)
    if not os.path.exists(local_dir):
        raise FileNotFoundError(local_dir)

    tsv_files = version.tsv_files()

    if version.files["test"] is None:
        # make it yuge
        psstdata.logger.warning(f"")
        psstdata.logger.warning(f"The PSST `train` and `valid` sets were downloaded, but `test` is not yet released.")
        psstdata.logger.warning(f"Once `test` is released, you should only need to re-run this code to retrieve the additional materials.")
        psstdata.logger.warning(f"Meantime, data labeled `test` is a copy of `valid` as a convenient placeholder.")
        psstdata.logger.warning(f"")

        tsv_files["test"] = tsv_files["valid"]
        valid_as_test = True

    data = {}
    for split, tsv_file in tsv_files.items():
        data[split] = PSSTUtteranceCollection.from_tsv(tsv_file)

    psstdata.logger.info(f"Loaded data version {version.version_id} at {local_dir}")

    return cast_dict({**data, "version": version, "test_is_placeholder": valid_as_test}, PSSTData)


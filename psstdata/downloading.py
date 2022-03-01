import os
import shutil
import tarfile

import requests

import psstdata
import psstdata.networking
from psstdata.config import PSSTSettings
from psstdata.versioning import PSSTVersionCollection


def download(destination, version_id=None):
    local_versions = PSSTVersionCollection.from_disk(destination)
    if version_id in local_versions and local_versions[version_id].files["test"] is not None:
        return local_versions[version_id]
    else:
        try:
            result = psstdata.networking.request("GET", _url("versions.json")).json()
            remote_versions = PSSTVersionCollection.from_object(result, root_dir=destination).apply_dir(destination)
            if version_id != "ARTIFICIAL":
                remote_versions.save(destination)
            version = remote_versions.latest() if version_id is None else remote_versions[version_id]

            if version_id is None and version.version_id in local_versions:
                if version == local_versions[version.version_id]:
                    return version
        except (requests.exceptions.ConnectionError, requests.HTTPError) as e:
            if version_id in local_versions:
                # Reachable only when .files["test"] is None. Past due for some unit testing here.
                return local_versions[version_id]
            if version_id is not None or not any(local_versions):
                message = f"Couldn't connect to data server, and no data found in {os.path.abspath(destination)}"
                raise PSSTDownloadError(message, e) from e
            latest_local_version = local_versions.latest()
            psstdata.logger.warning(f"Unable to connect to TalkBank. Using latest local version {latest_local_version.version_id}")
            return latest_local_version

    psstdata.logger.info(f"Downloading a new data version: {version.version_id}")

    for split, path in version.files.items():
        if path is None:
            continue
        url = _url(path)
        try:
            _download_split(version.local_dir(), split=split, url=url)
            psstdata.logger.info(f"Downloaded `{split}` to {version.local_dir()}.")
        except FileExistsError as e:
            psstdata.logger.info(f"Already `{split}` data in directory: {version.local_dir()}, skipping.")
            continue
        except Exception as e:
            raise PSSTDownloadError(split, e) from e

    local_versions = PSSTVersionCollection.from_disk(destination)
    return local_versions[version.version_id]


def _download_split(destination_folder, split: str, url: str):
    split_destination = os.path.join(destination_folder, split)
    if os.path.exists(split_destination):
        raise FileExistsError(split_destination)

    incomplete = os.path.join(destination_folder, "incomplete")

    with psstdata.networking.request("GET", url, stream=True) as response:
        with tarfile.open(fileobj=response.raw, mode="r:gz") as t:
            def itermembers():
                for tarinfo in t:
                    yield tarinfo
            t.extractall(incomplete, itermembers())

    shutil.move(os.path.join(incomplete, split), destination_folder)
    os.rmdir(incomplete)


def _url(path):
    settings = PSSTSettings.load()
    return f"{settings.base_url.rstrip('/')}/{path}"


class PSSTDownloadError(Exception):
    def __init__(self, message, inner_error):
        self.message = message
        self.inner_error = inner_error

    def __str__(self):
        if self.inner_error:
            return f"{self.message}. {type(self.inner_error).__name__}: {self.inner_error}"
        return self.message


class PSSTDataUnavailableError(Exception):
    def __init__(self, split):
        self.split = split

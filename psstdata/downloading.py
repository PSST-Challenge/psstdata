import os
import shutil
import tarfile

import requests
from requests import HTTPError

import psstdata
import psstdata.networking
from psstdata.config import PSSTSettings
from psstdata.networking import PSSTAuthToken
from psstdata.versioning import PSSTVersionCollection


class PSSTDownloader:
    def __init__(self, auth_token: PSSTAuthToken = None, base_url: str = None):
        self._auth = auth_token
        self._base_url = base_url

    def __enter__(self):
        settings = PSSTSettings.load()
        self._base_url = settings.base_url
        self._auth = psstdata.networking.PSSTAuthToken()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def url(self, path):
        return f"{self._base_url.rstrip('/')}/{path}"

    def version(self, version_id=None):
        if version_id is None:
            return self.versions()[0]
        else:
            version = next((v for v in self.versions() if v.version_id == version_id), None)
            if version is None:
                message = f"No version \"{version_id}\". Provide one of: {set(v.version_id for v in self.versions())}"
                raise ValueError(message)
            return version

    def download(
            self,
            destination,
            version_id=None,
    ):
        local_versions = PSSTVersionCollection.from_disk(destination)
        if version_id in local_versions:
            version = local_versions[version_id]
            return version
        else:
            try:
                result = psstdata.networking.request("GET", self.url("versions.json")).json()
                remote_versions = PSSTVersionCollection.from_object(result, root_dir=destination).apply_dir(destination)
                if version_id != "ARTIFICIAL":
                    remote_versions.save(destination)
                version = remote_versions.latest() if version_id is None else remote_versions[version_id]
                if version_id is None and version.version_id in local_versions:
                    return local_versions[version.version_id]
            except (requests.exceptions.ConnectionError, HTTPError) as e:
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
            url = self.url(path)
            try:
                self._download_split(version.local_dir(), split=split, url=url)
            except FileExistsError as e:
                psstdata.logger.info(f"Directory already exists: {e.filename}, skipping.")
                continue
            except Exception as e:
                raise PSSTDownloadError(split, e) from e

        local_versions = PSSTVersionCollection.from_disk(destination)
        return local_versions[version.version_id]

    def _download_split(
            self,
            destination_folder,
            split: str,
            url: str
    ):
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

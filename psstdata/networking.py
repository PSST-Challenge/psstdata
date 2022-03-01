import dataclasses
import time
from getpass import getpass

import requests
from requests.auth import HTTPBasicAuth

import psstdata
from psstdata.config import PSSTSettings, AUTH_COMMENT, CONFIG_FILE_SETTINGS


def request(method, url, *, data=None, stream=False, **kwargs):
    auth = get_auth()
    while True:
        try:
            response = requests.request(method, url, data=data, stream=stream, auth=auth, **kwargs)
            response.raise_for_status()
            return response
        except requests.HTTPError as e:
            if e.response.status_code == 401:
                psstdata.logger.warning(f"Could not authenticate with TalkBank. {AUTH_COMMENT}")
                time.sleep(0.1)  # HACK: cosmetic, gets around PyCharm's asynchronized output streams
                auth = get_auth(reset=True)
                continue
            else:
                raise



def get_auth(reset=False) -> HTTPBasicAuth:
    settings = PSSTSettings.load()
    if not settings.download_username or reset:
        username = input(f"The credentials in {CONFIG_FILE_SETTINGS} were missing or incorrect.\n"
                         f"Please enter the PSST username: ")
        password = getpass(f"Please enter the PSST password: ")
        settings = dataclasses.replace(settings, download_username=username, download_password=password)
        settings.save()
    return HTTPBasicAuth(settings.download_username, settings.download_password)



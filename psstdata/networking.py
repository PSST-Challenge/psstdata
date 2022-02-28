import dataclasses
import time
from dataclasses import dataclass
from getpass import getpass
from typing import Dict

import requests
from requests.cookies import RequestsCookieJar

from psstdata.config import PSSTSettings


@dataclass
class PSSTCredentials:
    userID: str
    pswd: str


class PSSTAuthToken:
    _cookie_cache: RequestsCookieJar = None

    @property
    def cookies(self):
        if self.expired:
            settings = PSSTSettings.load()
            credentials = get_credentials()
            response = request("POST", f"{settings.auth_server}/authorizeUser", data=credentials, is_auth_request=True)
            PSSTAuthToken._cookie_cache = response.cookies
        return PSSTAuthToken._cookie_cache

    @property
    def expired(self):
        if not PSSTAuthToken._cookie_cache:
            return True
        now = time.time()
        return any(c.expires < now for c in PSSTAuthToken._cookie_cache)


def request(method, url, *, data=None, stream=False, is_auth_request=False, **kwargs):
    cookies = None
    if not is_auth_request:
        cookies = PSSTAuthToken().cookies
    response = requests.request(method, url, data=data, cookies=cookies, stream=stream,  **kwargs)
    response.raise_for_status()
    return response


def get_credentials() -> Dict[str, str]:
    settings = PSSTSettings.load()
    if not settings.download_username:
        username = input(f"Please enter the PSST username: ")
        password = getpass(f"Please enter the PSST password: ")
        settings = dataclasses.replace(settings, download_username=username, download_password=password)
        settings.save()
    return {"userID": settings.download_username, "pswd": settings.download_password}



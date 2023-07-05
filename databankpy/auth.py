from __future__ import annotations

import requests

from databankpy import BASE_URL

def get_access_token(email: str, password: str) -> str:
    """ Return an access token for the API """
    response = requests.post(f'{BASE_URL}/v1/auth/login', data={
        'email': email,
        'password': password
    })
    if not response.ok:
        raise RuntimeError(f'Login request failed with status code {response.status_code}')
    data: dict[str, str] = response.json()
    return data['accessToken']
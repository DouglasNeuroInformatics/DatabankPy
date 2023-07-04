import requests

from databankpy import BASE_URL

""" return an access token for the API """
def get_access_token(email: str, password: str) -> str:
    response = requests.post(f'{BASE_URL}/v1/auth/login', data={
        'email': email,
        'password': password
    })
    if not response.ok:
        raise RuntimeError(f'Login request failed with status code {response.status_code}')
    data: dict[str, str] = response.json()
    return data['accessToken']
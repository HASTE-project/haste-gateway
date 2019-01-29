import aiohttp
import hashlib

_SALT = bytes([37, 17, 48, 89])


def creds_to_digest(username, password):
    auth_header = aiohttp.BasicAuth(login=username, password=password).encode()
    digest = hashlib.sha224(_SALT + bytes(auth_header, 'utf-8')).hexdigest()
    print(auth_header)  # Basic XXXXXXXX==
    print(digest)


def is_valid_login(auth_header, secret):
    digest = hashlib.sha224(_SALT + bytes(auth_header, 'utf-8')).hexdigest()
    return digest == secret


if __name__ == '__main__':
    creds_to_digest('???', '???')

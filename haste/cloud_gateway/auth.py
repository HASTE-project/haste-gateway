import aiohttp
import hashlib

_SALT = bytes([37, 17, 48, 89])

def is_valid_login(auth_header, secret):
    digest = hashlib.sha224(_SALT + bytes(str(auth_header), 'utf-8')).hexdigest()
    return digest == secret


if __name__ == '__main__':
    def print_header(username, password):
        auth_header = aiohttp.BasicAuth(login=username, password=password).encode()
        digest = hashlib.sha224(_SALT + bytes(auth_header, 'utf-8')).hexdigest()
        print('this is what your auth header needs to look like')
        print(auth_header)  # Basic XXXXXXXX==
        print('this is the digest to use as a parameter for the web application')
        print(digest)

    print_header('???', '???')

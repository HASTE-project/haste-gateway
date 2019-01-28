import aiohttp

from aiohttp import web
import sys

_username = sys.argv[1]
_password = sys.argv[2]
_auth_header = aiohttp.BasicAuth(login=_username, password=_password).encode()


async def handle(request):
    if not request.headers.get('Authorization') == _auth_header:
        return await _401_unauthorized()

    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


async def handle_blob(request):
    if not request.headers.get('Authorization') == _auth_header:
        return await _401_unauthorized()

    stream_id = request.match_info.get('stream_id')
    # text = "Hello, " + stream_id

    # TODO: send to HarmonicIO

    return web.json_response({'result': 'OK!'})


async def _401_unauthorized():
    return web.Response(status=401,  # Unauthorized
                        body='The request has not been applied because it lacks valid authentication credentials for the target resource.',
                        headers={'WWW-Authenticate': 'Basic realm="HASTE Cloud"'})


app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/{name}', handle),
                web.post('/stream/{stream_id}', handle_blob)
                ])

web.run_app(app)

import aiohttp

from aiohttp import web
import sys


from harmonicIO.stream_connector.stream_connector import StreamConnector

_username = sys.argv[1]
_password = sys.argv[2]
_auth_header = aiohttp.BasicAuth(login=_username, password=_password).encode()

# std_idle_time is in seconds
config = {'master_host': '192.168.0.84',
          'master_port': 8080,
          'container_name': 'benblamey/hio-example:latest',
          'container_os': 'ubuntu'}
sc = StreamConnector(config['master_host'], config['master_port'], max_try=1, std_idle_time=1)

async def handle(request):
    # TODO: for security, this should be constant-time equlity compare
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





    message_bytes = bytearray('test data', encoding='utf-8')

    sc.send_data(config['container_name'],
                 config['container_os'],
                 message_bytes)

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

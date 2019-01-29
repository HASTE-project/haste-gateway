import asyncio
import logging
import pickle

import aiohttp

from aiohttp import web
import sys

from harmonicIO.stream_connector.stream_connector import StreamConnector

_username = sys.argv[1]
_password = sys.argv[2]
_auth_header = aiohttp.BasicAuth(login=_username, password=_password).encode()

# std_idle_time is in seconds
config = {'master_host': '192.168.1.24',
          'master_port': 8080,
          'container_name': 'benblamey/hio-example:latest',
          'container_os': 'ubuntu'}

sc = StreamConnector(config['master_host'], config['master_port'], max_try=1, std_idle_time=1)


async def handle(request):
    # TODO: for security, this should be constant-time equlity compare
    if not request.headers.get('Authorization') == _auth_header:
        return await _401_unauthorized()

    text = "Hello!"
    return web.Response(text=text)


async def handle_blob(request):
    if not request.headers.get('Authorization') == _auth_header:
        return await _401_unauthorized()

    logging.info('blob received')

    original_filename = 'X-HASTE-original_filename'
    tag = 'X-HASTE-tag'
    original_timestamp = 'X-HASTE-unixtime'

    stream_id = request.match_info.get('stream_id')

    logging.info({'original_filename': original_filename,
                  'tag': tag,
                  'original_timestamp': original_timestamp,
                  'stream_id': stream_id,
                  })

    metadata = {}

    # The format of this binary blob is specific to the image analysis code.
    # TODO: add link!
    pickled_metadata = bytearray(pickle.dumps(metadata))

    result = await request.content.read()

    sc.send_data(config['container_name'],
                 config['container_os'],
                 bytearray(b'These are some bytes'))

    return web.json_response({'result': 'OK!'})


async def _401_unauthorized():
    # TODO: this could be an exception?
    return web.Response(status=401,  # Unauthorized
                        body='The request has not been applied because it lacks valid authentication credentials for the target resource.',
                        headers={'WWW-Authenticate': 'Basic realm="HASTE Cloud"'})


app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/{name}', handle),
                web.post('/stream/{stream_id}', handle_blob)
                ])

web.run_app(app,
            port=8080,
            host='0.0.0.0')

import asyncio
import logging
import pickle

import aiohttp

from aiohttp import web
import sys

from harmonicIO.stream_connector.stream_connector import StreamConnector

from haste.cloud_gateway.auth import is_valid_login


_secret = None

# std_idle_time is in seconds

HIO_MASTER_HOST = '192.168.1.24'
HIO_MASTER_PORT = 8080

# Looks like max_try is broken -- 0 => never try!
sc = StreamConnector(HIO_MASTER_HOST, HIO_MASTER_PORT, max_try=2, std_idle_time=1)


async def handle(request):
    # TODO: for security, this should be constant-time equlity compare
    if not is_valid_login(request.headers.get('Authorization'), _secret):
        return await _401_unauthorized()

    text = "Hello!"
    return web.Response(text=text)


async def handle_blob(request):
    if not is_valid_login(request.headers.get('Authorization'), _secret):
        return await _401_unauthorized()

    logging.info('blob received!')

    original_filename = request.headers['X-HASTE-original_filename']
    tag = request.headers['X-HASTE-tag']
    original_timestamp = request.headers['X-HASTE-unixtime']

    stream_id = request.match_info.get('stream_id')

    file = await request.content.read()

    metadata = {
        'timestamp': original_timestamp,
        'original_filename': original_filename,
        'tag': tag,
        'stream_id': stream_id,
        'image_length_bytes': len(file)}

    logging.info(metadata)

    if tag == 'vironova':
        config = {
            'container_name': 'benblamey/haste-image-proc:latest',
            'container_os': 'ubuntu'}
        logging.info(f'accepted tag:{tag}, config:{config}')

        # The format of this binary blob is specific to the image analysis code.
        # TODO: add link!
        pickled_metadata = bytearray(pickle.dumps(metadata))
        message_bytes = pickled_metadata + file

        logging.info('sending data to HIO...')
        sc.send_data(config['container_name'],
                     config['container_os'],
                     message_bytes)
    elif tag == 'discard':
        # This tag simply discards on the server-side. For benchmarking.
        logging.info(f'tag {tag} -- discarding blob.')
        pass
    else:
        logging.info(f'rejected tag:{tag}')
        return await _412_tag_unknown()


    return web.json_response({'result': 'OK!'})


async def _401_unauthorized():
    # TODO: this could be an exception?
    return web.Response(status=401,  # Unauthorized
                        body='The request has not been applied because it lacks valid authentication credentials for the target resource.',
                        headers={'WWW-Authenticate': 'Basic realm="HASTE Cloud"'})


async def _412_tag_unknown():
    # TODO: this could be an exception?
    return web.Response(status=412,  # Precondition Failed
                        body='The request has not been applied because it lacks valid X-HASTE-tag.')


if __name__ == '__main__':
    _secret = sys.argv[1]

    app = web.Application()
    app.add_routes([web.get('/', handle),
                    web.get('/{name}', handle),
                    web.post('/stream/{stream_id}', handle_blob)
                    ])

    web.run_app(app,
                port=8080,
                host='0.0.0.0')
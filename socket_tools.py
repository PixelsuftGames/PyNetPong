import json
import gzip
import zlib
import socket
from threading import Thread
from utils import *


def logme(nn) -> None:
    return
    print(', '.join([str(nn) for _x in range(10)]))


conf_: dict = get_var('conf')
use_gzip: bool = conf_.get('use_gzip')
info = [
    {
        'w': conf_.get('width'),
        'h': conf_.get('height'),
        'y': 0,
        'l_': False,
        's1': 0,
        's2': 0,
        'bx': round(conf_.get('width') / 2),
        'by': round(conf_.get('height') / 2)
    }, {
        'w': conf_.get('width'),
        'h': conf_.get('height'),
        'y': 0,
        'l_': False,
        's1': 0,
        's2': 0,
        'bx': round(conf_.get('width') / 2),
        'by': round(conf_.get('height') / 2)
    }
]
sock = [False, socket.socket(), None, socket.socket()]


def decode_msg(message: bytes) -> dict:
    return json.loads(message.decode(encoding_))


def encode_msg(message: dict) -> bytes:
    return json.dumps(message).encode(encoding_)


def decode_msg_(message: bytes) -> dict:
    return json.loads(message.decode(encoding_))


def encode_msg_(message: dict) -> bytes:
    return gzip.compress(json.dumps(message).encode(encoding_))


def wait_sock_accept() -> None:
    logme(4)
    sock[3].listen()
    logme(5)
    conn, addr = sock[3].accept()
    logme(6)
    sock[0] = True
    logme(7)
    sock[1] = conn
    logme(8)
    sock[2] = addr
    logme(9)
    server()


def server() -> None:
    logme(10)
    while sock[1]:
        size = int(sock[1].recv(10).decode(encoding_).strip())
        msg = decode_msg(sock[1].recv(size))
        info[0] = msg
        result = info[1]
        result_bytes = encode_msg(result)
        sock[1].send((str(len(result_bytes)) + '          ')[:10].encode(encoding_) + result_bytes)


def client() -> None:
    while sock[1]:
        result = info[1]
        result_bytes = encode_msg(result)
        sock[1].send((str(len(result_bytes)) + '          ')[:10].encode(encoding_) + result_bytes)
        size = int(sock[1].recv(10).decode(encoding_).strip())
        msg = decode_msg(sock[1].recv(size))
        info[0] = msg


def run_server(host: str, port: int) -> None:
    logme(1)
    sock[3] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logme(2)
    sock[3].bind((host, port))
    logme(3)
    Thread(target=wait_sock_accept).start()
    logme(3.5)


def connect_server(host: str, port: int) -> None:
    sock[1] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock[1].connect((host, port))
    Thread(target=client).start()


def kill_all() -> None:
    sock[1] = None


if use_gzip:
    decode_msg = decode_msg_
    encode_msg = encode_msg_

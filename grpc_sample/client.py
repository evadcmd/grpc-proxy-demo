import os
import logging

import grpc

from grpc_sample.grpclib.test_pb2 import Param
from grpc_sample.grpclib.test_pb2_grpc import FIOTStub

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s %(levelname)s] %(message)s',
    datefmt='%Y%m%d %H:%M:%S',
)

URL = f'{"server" if os.environ.get("IN_CONTAINER", False) else "localhost"}:8090'


params = [
    Param(x=1, y=3, z=5),
    Param(x=2, y=4, z=6),
    Param(x=-1, y=-3, z=-5),
    Param(x=-2, y=-4, z=-6)
]


def test_simple():
    """ single req -> single resp
    """
    with grpc.insecure_channel(URL) as channel:
        stub = FIOTStub(channel)
        res = stub.Simple(Param(x=1, y=3, z=5))
        logging.info(f'[simple] resp:{res.value}')
        logging.info(f'[simple] resp tags:{res.tags}')


def test_stream_resp():
    """ single req -> stream resp
    """
    with grpc.insecure_channel(URL) as channel:
        stub = FIOTStub(channel)
        for res in stub.StreamResp(Param(x=0, y=0, z=0)):
            logging.info(f'[stream-resp] resp:{res.value}')


def test_stream_req():
    """ stream req -> single resp
    """
    with grpc.insecure_channel(URL) as channel:
        stub = FIOTStub(channel)
        res = stub.StreamReq(iter(params))
        logging.info(f'[stream-req] resp:{res.value}')


def test_bistream():
    """ stream req -> stream resp
    """
    with grpc.insecure_channel(URL) as channel:
        stub = FIOTStub(channel)
        for res in stub.BiStream(iter(params)):
            logging.info(f'[bistream] resp:{res.value}')


def test_all():
    """ test all functions in a single connection
    """
    with grpc.insecure_channel(URL) as channel:
        stub = FIOTStub(channel)
        # single request -> single response
        res = stub.Simple(Param(x=1, y=3, z=5))
        logging.info(f'[simple] resp:{res.value}')
        # single request -> stream response
        for res in stub.StreamResp(Param(x=0, y=0, z=0)):
            logging.info(f'[stream-resp] resp:{res.value}')
        # stream request -> single response
        res = stub.StreamReq(iter(params))
        logging.info(f'[stream-req] resp:{res.value}')
        # stream request -> stream response
        for r in stub.BiStream(iter(params)):
            logging.info(f'[bistream] resp:{r.value}')


if __name__ == '__main__':
    test_simple()
    test_stream_req()
    test_stream_resp()
    test_bistream()
    test_all()

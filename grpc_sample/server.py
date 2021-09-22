from concurrent.futures import ThreadPoolExecutor

import grpc
from grpc_sample.grpclib.test_pb2 import Param, Res
from grpc_sample.grpclib.test_pb2_grpc import FIOTServicer, add_FIOTServicer_to_server

class FIOT(FIOTServicer):
    # single req -> single resp
    # def Simple(self, param, ctx):
        # val = param.x + param.y + param.z
        # return Res(value=val)

    def Simple(self, param, ctx):
        val = param.x + param.y + param.z
        res = Res(value=val)
        # res.tags.extend([Res.SUCCESS, Res.FAILED, Res.WARNING])
        return res

    # stream req -> single resp
    def StreamReq(self, params, ctx):
        val = 0
        for req in params:
            val += (req.x + req.y + req.z)
        return Res(value=val)

    # single req -> stream resp
    def StreamResp(self, param, ctx):
        for i in range(10):
            yield Res(value=i)

    # stream req -> stream resp
    def BiStream(self, params, ctx):
        for i, param in enumerate(params):
            s = param.x + param.y + param.z
            # response only on odd requests
            if i & 0b1:
                yield Res(value=s)


def serve():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    add_FIOTServicer_to_server(FIOT(), server)
    server.add_insecure_port('[::]:50050')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

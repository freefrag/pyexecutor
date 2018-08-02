from concurrent import futures
import grpc
import time

import generated.pyexecutor_pb2 as pyexecutor_pb2
import generated.pyexecutor_pb2_grpc as pyexecutor_pb2_grpc

import grpc_reflection.v1alpha.reflection as reflection

from jupyter_client import BlockingKernelClient, MultiKernelManager

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class PyExecutor(pyexecutor_pb2_grpc.PyExecutorServicer):

    def __init__(self):
        self.manager = MultiKernelManager()
        kernel_id = self.manager.start_kernel()
        self.kernel = self.manager.get_kernel(kernel_id)
        self.client = BlockingKernelClient()
        self.client.load_connection_file(self.kernel.connection_file)

    def Execute(self, request, context):
        response = self.client.execute_interactive(
            code=request.command,
            user_expressions={
                'test': request.expression
            }
        )
        expression = response['content']['user_expressions']['test']['data']
        result = expression['text/html'] if 'text/html' in expression else expression['text/plain']
        return pyexecutor_pb2.ExecuteResponse(result = result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pyexecutor_pb2_grpc.add_PyExecutorServicer_to_server(PyExecutor(), server)

    reflection.enable_server_reflection('pyexecutor.PyExecutor', server)
    server.add_insecure_port('[::]:8443')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()

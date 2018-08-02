from grpc_tools import protoc

protoc.main((
    '',
    '-I./protos',
    '--python_out=./generated',
    '--grpc_python_out=./generated',
    './protos/pyexecutor.proto',
))

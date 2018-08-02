from grpc_tools import protoc

protoc.main((
    '',
    '-I./src/protos',
    '--python_out=./src/',
    '--grpc_python_out=./src/',
    './src/protos/generated/pyexecutor.proto',
))

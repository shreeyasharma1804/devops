import grpc

from protos import service_pb2
from protos import service_pb2_grpc

def run():
    # Connect to the server
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.GreeterStub(channel)
        
        # Send a request
        response = stub.SayHello(service_pb2.HelloRequest(name='Alice'))
        
    print(f"Client received: {response.message}")

if __name__ == '__main__':
    run()
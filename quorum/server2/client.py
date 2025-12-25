import grpc

from protos import healthcheck_pb2
from protos import healthcheck_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = healthcheck_pb2_grpc.HealthCheckStub(channel)
        response = stub.SendHealthCheck(healthcheck_pb2.HealthCheckMessage(message="I'm Alive", server="Server2"))
        
    print(f"Client received: {response.message}")

if __name__ == '__main__':
    run()
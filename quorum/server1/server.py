import grpc
from concurrent import futures
import time

from protos import healthcheck_pb2
from protos import healthcheck_pb2_grpc

class HealthCheck(healthcheck_pb2_grpc.HealthCheckServicer):
    def SendHealthCheck(self, request, context):
        print(f"Received heartbeat from: {request.server}")
        return healthcheck_pb2.HealthCheckMessage(message="Registered", server="Server1")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    healthcheck_pb2_grpc.add_HealthCheckServicer_to_server(HealthCheck(), server)
    server.add_insecure_port('[::]:50051')
    print("Server started on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
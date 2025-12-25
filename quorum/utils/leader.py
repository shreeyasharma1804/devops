import grpc
from concurrent import futures
import time
from protos import healthcheck_pb2
from protos import healthcheck_pb2_grpc
import asyncio

class HealthCheck(healthcheck_pb2_grpc.HealthCheckServicer):

    def SendHealthCheck(self, request, context):
        print(f"{request.message}: {request.server}")
        return healthcheck_pb2.HealthCheckMessage(
            message="Registered", server="Server1"
        )

class Leader:

    def __init__(self, cache_instance: dict):
        self.cache_instance: dict = cache_instance
        self.total_quorum: dict = {"2": 0, "3": 0, "4": 0, "5": 0}
        self.healthy_brokers: dict = {"2": 0, "3": 0, "4": 0, "5": 0}
        self.unhealthy_count: dict = {"2": 0, "3": 0, "4": 0, "5": 0}
        # {"Broker2": 0, "Broker3": 0, "Broker4": 0, "Broker5": 0}

    def _reset_counters(self):
        for key in self.total_quorum.keys():
            if(self.total_quorum[key] > 0):
                self.total_quorum[key] = 0

    def _increment_counter(self, broker_id):
        self.total_quorum[broker_id] += 1

    async def inspect_healthchecks(self):
        await asyncio.sleep(int(self.cache_instance["InitialWaitTime"]))
        while True:
            for broker, count in self.total_quorum.items():
                if count > 0:
                    print(f"{broker} is healthy with {count} healthchecks.")
                else:
                    self.total_quorum[id] += 1
                    if(self.unhealthy_count[id] > self.cache_instance["FailureThreshold"]):
                        del self.healthy_brokers[id]
            self._reset_counters()
            print(f"Healthy brokers: {self.healthy_brokers}")

    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        healthcheck_pb2_grpc.add_HealthCheckServicer_to_server(HealthCheck(), server)
        server.add_insecure_port("[::]:50051")
        print("Server started on port 50051...")
        server.start()
        server.wait_for_termination()

    def run(self):
        self.serve()
import grpc
from concurrent import futures
import time
from protos import healthcheck_pb2
from protos import healthcheck_pb2_grpc
import asyncio

class HealthCheck(healthcheck_pb2_grpc.HealthCheckServicer):

    def __init__(self, cache_instance: dict) -> None:
        super().__init__()
        self.cache_instance: dict = cache_instance
        self.total_quorum: dict = {"2": 0, "3": 0, "4": 0, "5": 0}
        self.healthy_brokers: dict = self.total_quorum.copy()
        self.unhealthy_brokers: dict = self.total_quorum.copy()
        asyncio.run(self.inspect_healthchecks())

    def _reset_counters(self):
        for broker_id in self.total_quorum.keys():
            self.total_quorum[broker_id] = 0

    def _increment_counter(self, broker_id):
        self.total_quorum[broker_id] += 1

    async def inspect_healthchecks(self):
        await asyncio.sleep(int(self.cache_instance["initialwaittime"]))
        print("Starting healthcheck inspection...")
        while True:
            for broker_id, count in self.total_quorum.items():
                if count > 0:
                    if(broker_id not in self.healthy_brokers):
                        self.healthy_brokers[broker_id] = 1
                else:
                    self.unhealthy_brokers[broker_id] += 1
                    if(self.unhealthy_brokers[broker_id] > self.cache_instance["FailureThreshold"]):
                        del self.healthy_brokers[broker_id]
            self._reset_counters()
            print(f"Healthy brokers: {self.healthy_brokers}")
            await asyncio.sleep(int(self.cache_instance["CheckHeartbeatInterval"]))

    def SendHealthCheck(self, request, context):
        self._increment_counter(request.server)

        print(f"{request.message}: {request.server}")
        return healthcheck_pb2.HealthCheckMessage(
            message="Registered", server="Server1"
        )

class Leader:

    def __init__(self, cache_instance: dict) -> None:
        self.cache_instance: dict = cache_instance

    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        healthcheck_pb2_grpc.add_HealthCheckServicer_to_server(HealthCheck(self.cache_instance), server)
        server.add_insecure_port("[::]:50051")
        print("Server started on port 50051...")
        server.start()
        server.wait_for_termination()

    def run(self):
        self.serve()
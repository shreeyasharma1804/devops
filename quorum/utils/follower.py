import grpc
from protos import healthcheck_pb2
from protos import healthcheck_pb2_grpc
import time

class Follower:
    def __init__(self, cache_instance: dict) -> None:
        self.cache_instance: dict = cache_instance

    def run(self):
        with grpc.insecure_channel(self.cache_instance["send_heartbeat_to"]) as channel:
            stub = healthcheck_pb2_grpc.HealthCheckStub(channel)
            while True:
                stub.SendHealthCheck(
                    healthcheck_pb2.HealthCheckMessage(
                        message="I'm Alive", server=self.cache_instance["broker_id"]
                    )
                )
                time.sleep(int(self.cache_instance["send_heartbeat_after"]))

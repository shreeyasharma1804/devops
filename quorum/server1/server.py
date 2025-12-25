import grpc
from concurrent import futures
import time
from protos import healthcheck_pb2
from protos import healthcheck_pb2_grpc
from utils import cache, leader
import os

cache_instance = cache.Cache(os.path.join(os.path.dirname(__file__), "config.ini"), "LEADER")
cache_instance.set()

process = leader.Leader(cache_instance.get())

if __name__ == '__main__':
    process.run()
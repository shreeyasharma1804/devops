import grpc
from protos import healthcheck_pb2
from protos import healthcheck_pb2_grpc
from utils import cache, follower
import os
import time


cache_instance = cache.Cache(config_file=os.path.join(os.path.dirname(__file__), "config.ini"))
cache_instance.set()

process = follower.Follower(cache_instance.get())

if __name__ == '__main__':
    process.run()
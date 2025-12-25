import os
import configparser

class Cache:
    def __init__(self, server: str, config_file: os.PathLike):
        self.server: str = server
        self.config_file: os.PathLike = config_file
        self.config_parser: configparser.ConfigParser = configparser.ConfigParser()
        self.cache_state: dict = {}

    def set_config(self):
        self.config_parser.read(self.config_file)
        self.cache_state["heartbeat_reciever"] = self.config_parser["heartbeat_reciever"]

    def get_config(self):
        return self.cache_state
import os
import configparser


class Cache:
    def __init__(self, config_file: str, role: str = "FOLLOWER") -> None:
        self.config_file: str = config_file
        self.role: str = role
        self.config_parser: configparser.ConfigParser = configparser.ConfigParser()
        self.cache_state: dict = {}

    def set(self) -> None:
        self.config_parser.read(self.config_file)
        self.cache_state = dict(self.config_parser[self.role])

    def get(self):
        return self.cache_state

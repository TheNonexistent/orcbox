import yaml
import sys

from lib.printformat import Print

class Parser:
    @staticmethod
    def parse(config_file):
        Print.info("Loading configuration file: " + config_file + " ...")
        with open(config_file, "r") as stream:
            try:
                config = yaml.safe_load(stream)
                Print.success("Configuration file successfully loaded.")
                return config
            except yaml.YAMLError as exc:
                Print.error(exc)
                sys.exit(1)
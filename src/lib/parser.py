import yaml
import sys
import json

from lib.system.printformat import Print, Color

class Parser:
    @staticmethod
    def parse_config(config_file):
        Print.info("Loading configuration file: " + Color.paint('purple',config_file) + " ...")
        with open(config_file, "r") as stream:
            try:
                config = yaml.safe_load(stream)
                Print.success("Configuration file successfully loaded.")
                return config
            except yaml.YAMLError as exc:
                Print.error(exc)
                sys.exit(1)
    
    @staticmethod
    def parse_session(session_file):
        Print.info("Loading session file: " + Color.paint('purple',session_file) + " ...")
        with open(session_file, "r") as stream:
            try:
                data = stream.readline()
                config = json.loads(data)
                return config
            except json.JSONDecodeError as exc:
                Print.error(exc)
                sys.exit(1)
#!/usr/bin/env python3
import argparse

from pprint import pprint

from lib.printformat import Colors, Color, Print
from lib.parser import Parser
from lib.manager import OrcManager


ORC_VERSION = "0.1 Alpha"
ORC_YAML_VERSION = "1.2.2"
ORC_AVAILABLE_COMMANDS = ["up", "down", "status"] ## + ["netstat", "ssh", ...]

##Argparse Configuration
orc_parser = argparse.ArgumentParser(description="Orchestrate infrastructure for development and testing on virtualbox")

orc_parser.add_argument("Command", metavar="command", type=str, choices=ORC_AVAILABLE_COMMANDS)
orc_parser.add_argument("-f", "--file", type=str, default="orcbox.yaml", help="orcbox configuration yaml file")

args = orc_parser.parse_args()
##

command = args.command

Print.success("OrcBox Started.")

config_file = args.file
config = Parser.parse(config_file)




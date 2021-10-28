#!/usr/bin/env python3
import argparse
import sys, os
import json

from pprint import pprint

from lib.parser import Parser
from lib.manager import OrcManager

from lib.system.printformat import Colors, Color, Print
from lib.system.utils import uprint_status, uprint_line


ORC_VERSION = "0.1 Alpha"
ORC_YAML_VERSION = "1.2.2"
ORC_AVAILABLE_COMMANDS = ["up", "down", "status"] ## + ["start", "stop", "netstat", "ssh", "monitor"(eg.: docker stats),  "log"(cast vbox log), "inspect"...]
ORC_DEFAULT_SESSION_DIRECTORY = ".orcbox"

##Argparse Configuration
orc_parser = argparse.ArgumentParser(description="Orchestrate infrastructure for development and testing on virtualbox")

orc_parser.add_argument("Command", metavar="command", type=str, choices=ORC_AVAILABLE_COMMANDS)
orc_parser.add_argument("-f", "--file", type=str, default="orcbox.yaml", help="orcbox configuration yaml file")

args = orc_parser.parse_args()
##

session_id = None
session_name = None
##Creating Session Directory Structure
if not os.path.exists(ORC_DEFAULT_SESSION_DIRECTORY):
    open_session = False
    os.mkdir(ORC_DEFAULT_SESSION_DIRECTORY)
    os.mkdir(ORC_DEFAULT_SESSION_DIRECTORY+"/data")
else:
    open_session = True
    with open(ORC_DEFAULT_SESSION_DIRECTORY+"/.id", 'r') as id_file:
        session_id = id_file.read().replace('\n', '')
    with open(ORC_DEFAULT_SESSION_DIRECTORY+"/.name", 'r') as name_file:
        session_name = name_file.read().replace('\n', '')


command = args.Command

Print.success("OrcBox Started.")

if not open_session:
    config_file = args.file
    config = Parser.parse_config(config_file)
else:
    session_file = ORC_DEFAULT_SESSION_DIRECTORY+"/.session"
    config = Parser.parse_session(session_file)

if command == "up":
    if open_session:
        print()
        Print.info("Session already running.")
        sys.exit(0) #TODO: bring up downed machines here.
    Print.info("Following machines detected: ")
    uprint_line(15)
    pprint(config)
    uprint_line(15)
    Print.info("Bringin up detected machines...")
    Print.info("Setting up Session Manager...")
    session_name = os.getcwd().split('/')[-1]
    base_folder = os.getcwd() + "/" + ORC_DEFAULT_SESSION_DIRECTORY + "/data/"
    manager = OrcManager(session_name, config, base_folder)
    session_id = manager.session_id
    with open(ORC_DEFAULT_SESSION_DIRECTORY+"/.id", 'w') as id_file, open(ORC_DEFAULT_SESSION_DIRECTORY+"/.name", 'w') as name_file:
        id_file.write(session_id)
        name_file.write(session_name)
    Print.success("Session created.")
    print("Session:", Color.paint('purple', session_name))
    print("Session ID:", Color.paint('purple', session_id))
    print()
    Print.info("Starting up machines...")
    session_machines = manager.up()
    print()
    Print.success("Successfully stared all machines.")
    with open(ORC_DEFAULT_SESSION_DIRECTORY+"/.session", 'w') as session_file:
        session_file.write(json.dumps(session_machines))
    Print.success("Session saved.")
elif command == "down":
    pass
elif command == "status":
    base_folder = os.getcwd() + "/" + ORC_DEFAULT_SESSION_DIRECTORY + "/data/"
    manager = OrcManager(session_name, config, base_folder,session_id, open_session=True)
    machines_stats = manager.status()
    print()

    uprint_line(20)
    uprint_status(machines_stats)
    uprint_line(20)


    
from tabulate import tabulate

from lib.system.printformat import Color

ORC_DEFAULT_LINE_CHARACTR = "="

def uprint_line(count):
    print(ORC_DEFAULT_LINE_CHARACTR*count)

def uprint_status(machines_stats):
    headers = ["Name", "uuid", "VirtualBox Name", "OS", "CPU Cores", "Memory", "Network", "Disk Name", "Boot Name"]
    table = []
    for machine_stat in machines_stats:
        table.append([
            Color.paint("green", machine_stat['name']+"(running)") if machine_stat['running'] else Color.paint("red", machine_stat['name']+"(stopped)"),
            machine_stat['uuid'],
            machine_stat['vbox_name'],
            machine_stat['os'],
            str(machine_stat['cpu']),
            str(machine_stat['memory']),
            machine_stat['network'],
            machine_stat['disk']['name'] if machine_stat['disk']['initialized'] else "None",
            machine_stat['boot']['name'] if machine_stat['boot']['using'] else "None"
        ])
    print("\n",tabulate(table, headers=headers),"\n")
    # print(machine_stat['boot']['name'] if machine_stat['boot']['using'] else "Noone")
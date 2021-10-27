import sys, os

from lib.printformat import Print
from lib.interface import VboxInterface as interface

class Machine:
    def __init__(self, name, vbox_name, base_folder, data, create):
        #network, status -> up or down, ip_address, mac_address, disk_status, ram_status, [created], [started]
        self.name = name
        self.vbox_name = vbox_name
        self.base_folder = base_folder
        try:
            self.os = data['os']
            self.cpu = data.get('cpu', 1)
            self.memory = data['memory']
            self.vram = data.get('vram', "128")
            self.network = data.get('network', "nat")
            self.groups = data.get('groups', None)
            self.boot = {"name": None, "location": None, "using": False}
            if isinstance(data['disk'], str):
                self.explicit_disk = True
                self.disk = {"name": data['disk'].split('/')[-1], "location": data['disk'], "size": None, "initialized": True}
                ## TODO: disk probably needs to be it's own object with data such as size and status and so on.
                ## TODO: find a way to figure out the size of the specified disk
            elif isinstance(data["disk"], dict):
                self.explicit_disk = False
                self.disk = {"name": None, "location": None, "size": data['disk']['size'], "initialized": False}
                self.boot['location'] = data['boot']
                self.boot['name'] = self.boot["location"].split('/')[-1]
                self.boot['using'] = True
            else:
                Print.error("Disk Configuration on machine '" + self.name + "' invalid.")
                Print.warning("Aborting...")
                sys.exit(5)## TODO: Graceful exit
        except KeyError as ke:
            Print.error(f"Machine '{self.name}' Configuration Missing Required Value: " + ke.args[0])
            sys.exit(5)## TODO: Graceful exit

        if create:
            self._create_machine()
        else:
            # _get_status()
            pass

    @classmethod
    def create(cls, *args, **kwargs):
        return cls(*args, **kwargs, create=True)

    @classmethod
    def load(cls, *args, **kwargs):
        return cls(**args, **kwargs, create=False)

    def _create_machine(self):
        machine = {
            "machine_name": self.vbox_name,
            "os_type": self.os,
            "base_folder": self.base_folder,
            "memory": self.memory,
            "cpu": self.cpu,
            "vram": self.vram,
            "network": self.network,
            "groups": self.groups
        }
        interface.createvm(**machine)
        boot_order = [None]*4
        if self.explicit_disk:
            boot_order[0] = "disk"
        else:
            boot_order[0] = "dvd"
            boot_order[1] = "disk"
            self.disk['location'] = self.base_folder + "/disk.vdi"
            interface.createdisk(self.disk['location'], self.disk['size'])
            self.disk['initialized'] = True
            interface.connectboot(self.vbox_name, self.boot['location'])

        boot_order = filter(None, boot_order)
        
        interface.connectdisk(self.vbox_name, self.disk['location'])
        interface.setbootorder(self.vbox_name, *boot_order)

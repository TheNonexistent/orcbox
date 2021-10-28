import sys, os
import uuid
import multiprocessing
import time

from lib.system.printformat import Print, Color
from lib.interface import VboxInterface as interface

ORC_DEFAULT_ACPI_TIMEOUT = 25

class Machine:
    def __init__(self, name, vbox_name, base_folder, data, create):
        #network, status -> up or down, ip_address, mac_address, disk_status, ram_status, [created], [started]
        self.name = name
        self.vbox_name = vbox_name
        self.uuid = data.get('uuid', None)
        self.boot_order = data.get('boot_order', None)
        self.explicit_disk = data.get('explicit_disk', None)
        self.base_folder = base_folder
        try:
            self.os = data['os']
            self.cpu = data.get('cpu', 1)
            self.memory = data['memory']
            self.vram = data.get('vram', "128")
            self.network = data.get('network', "nat")
            self.groups = data.get('groups', None)
            self.boot = {"name": None, "location": None, "using": False}
            if create:
                if isinstance(data['disk'], str):
                    self.explicit_disk = True
                    self.disk = {"name": data['disk'].split('/')[-1], "location": data['disk'], "size": None, "initialized": True}
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
            else:
                self.disk = data['disk']
                self.boot = data['boot']
        except KeyError as ke:
            Print.error(f"Machine '{self.name}' Configuration Missing Required Value: " + ke.args[0])
            sys.exit(5)## TODO: Graceful exit

        if create:
            self.uuid = str(uuid.uuid4())
            self._create_machine()
        else:
            # _get_status()
            pass

    @classmethod
    def create(cls, name, vbox_name, base_folder, data):
        return cls(name, vbox_name, base_folder, data, create=True)

    @classmethod
    def load(cls, session_entry):
        try:
            name = session_entry.pop('name')
            vbox_name = session_entry.pop('vbox_name')
            base_folder = session_entry.pop('base_folder')
        except KeyError:
            Print.warning("Session file is missing and/or having damaged entries. This may result in undefined behavior.")
            pass
        return cls(name, vbox_name, base_folder, session_entry, create=False)

    @property
    def running(self):
        return interface.getvmrunning(self.uuid)

    @property
    def stats(self):
        return {"name": self.name,
             "vbox_name": self.vbox_name,
             "uuid": self.uuid,
             "running": self.running,
             "base_folder": self.base_folder,
             "os": self.os,
             "cpu": self.cpu,
             "memory": self.memory,
             "vram": self.vram,
             "disk": self.disk,
             "boot": self.boot,
             "boot_order": self.boot_order,
             "network": self.network,
             "groups": self.groups
              }

    def _create_machine(self):
        machine = {
            "machine_name": self.vbox_name,
            "uuid": self.uuid,
            "os_type": self.os,
            "base_folder": self.base_folder,
            "memory": self.memory,
            "cpu": self.cpu,
            "vram": self.vram,
            "network": self.network,
            "groups": "/"+self.groups if self.groups is not None else self.groups
        }
        interface.createvm(**machine)
        self.boot_order = [None]*4
        if self.explicit_disk:
            self.boot_order[0] = "disk"
        else:
            self.boot_order[0] = "dvd"
            self.boot_order[1] = "disk"
            self.disk['location'] = self.base_folder + "/disk.vdi"
            interface.createdisk(self.disk['location'], self.disk['size'])
            self.disk['initialized'] = True
            interface.connectboot(self.uuid, self.boot['location'])

        self.boot_order = filter(None, self.boot_order)
        self.boot_order = list(self.boot_order)
        
        interface.connectdisk(self.uuid, self.disk['location'])
        interface.setbootorder(self.uuid, *self.boot_order)

    def start_machine(self):
        interface.startvm(self.uuid)

    def stop_machine(self, soft=False):
        if self.running:
            if soft:
                pacpi = multiprocessing.process(target=Machine._acpipoweroff, args=(self.uuid,))
                pacpi.start()

                pacpi.join(ORC_DEFAULT_ACPI_TIMEOUT)
                if pacpi.is_alive():
                    Print.warning(f"ACPI Shutdown on '{self.name}' vbox_name:{self.vbox_name}:{self.uuid} Timed out. Skipping...")
                    pacpi.kill()
                    #p.terminate() will probably be a better choice but it has a chance of stucking which is problematic...

                    pacpi.join()
            else:
                interface.poweroffvm(self.uuid)

    def remove_machine(self):
        if not self.running:
            interface.removevm(self.uuid, delete=not self.explicit_disk)

    @staticmethod
    def _acpipoweroff(uuid):
        interface.acpipoweroffvm(uuid)
        

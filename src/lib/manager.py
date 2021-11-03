import string
import random

from lib.machine import Machine
from lib.system.decorators import singleton
from lib.system.printformat import Print, Color


_SESSION_ID_LENGTH = 10

def _id_generator(length=_SESSION_ID_LENGTH, chars=string.ascii_lowercase + string.digits):
    return  ''.join(random.choices(chars, k=length))

@singleton
class OrcManager:
    def __init__(self, session_name, session_config, base_folder, session_id=None, open_session=False):
        if session_id == None:
            self._session_id = _id_generator()
        else:
            self._session_id = session_id
        self.session_name = session_name
        self._machine_list = []

        if not open_session:
            for name,data in session_config.items():
                vbox_name = self._session_id+"_"+name
                self._machine_list.append(Machine.create(name, vbox_name, base_folder+vbox_name, data))
                Print.success("# Created machine '" + name + "' as: " + vbox_name)
            Print.success("\nSession Manager has been successfully set up.")
        else:
            for machine in session_config:
                self._machine_list.append(Machine.load(machine))
            


    def up(self):
        ##TODO: implement functionallity so that if one machine is down the up command just brings up that one
        for machine in self._machine_list:
            machine.start_machine()
            print("+ Started: " + Color.paint("lblue", machine.name))
        return [machine.__dict__ for machine in self._machine_list]

    def down(self, soft=False):
        softstring = 'soft ' if soft else ''

        for index, machine in enumerate(self._machine_list):
            Print.info(f"Attempting {softstring}poweroff on '{machine.vbox_name}'...")
            machine.stop_machine(soft=soft)
            print("+ Stopped: " + Color.paint("lblue", machine.name))
        return [machine.__dict__ for machine in self._machine_list]

    def purge(self):
        for index, machine in enumerate(self._machine_list):
            Print.info(f"Removing '{machine.vbox_name}'...")
            machine.remove_machine()
            print("+ Removed: " + Color.paint("lblue", machine.name))
            del machine

    def status(self):
        machines_stats = []
        for machine in self._machine_list:
            machines_stats.append(machine.stats)
        return machines_stats

    def pass_input(self,machine_name, input):
        pass

    @property
    def machine_list(self):
        return self._machine_list

    @property
    def session_id(self):
        return self._session_id

    


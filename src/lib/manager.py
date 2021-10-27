import string
import random

from lib.machine import Machine
from lib.printformat import Print


_SESSION_ID_LENGTH = 10

def _id_generator(length=_SESSION_ID_LENGTH, chars=string.ascii_lowercase + string.digits):
    return  ''.join(random.choices(chars, k=length))


class OrcManager:
    def __init__(self, session_name, config, base_folder, session_id=None, open_session=False):
        if session_id == None:
            self._session_id = _id_generator()
        else:
            self._session_id = session_id
        self.session_name = session_name
        self._machine_list = []

        for name,data in config.items():
            vbox_name = self._session_id+"_"+name
            if not open_session:
                self._machine_list.append(Machine.create(name, vbox_name, base_folder+vbox_name, data))
                Print.success("# Created machine '" + name + "' as: " + vbox_name)
            else:
                self._machine_list.append(Machine.load(name, vbox_name, base_folder+vbox_name, data))
        
        if not open_session:
            Print.success("\nSession Manager has been successfully set up.")


    def up(self,):
        pass

    def down(self,):
        pass

    def status(self,):
        pass

    def pass_input(self,machine_name, input):
        pass

    @property
    def machine_list(self):
        return self._machine_list

    @property
    def session_id(self):
        return self._session_id

    


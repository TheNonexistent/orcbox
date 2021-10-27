import string

from lib.interface import VboxInterface

_SESSION_ID_LENGTH = 10

def _id_generator(length=_SESSION_ID_LENGTH, chars=string.ascii_lowercase + string.digits):
    return  ''.join(random.choices(chars, k=length))


class OrcManager:
    def __init__(self, session_name, config):
        self._session_id = _id_generator()
        self.session_name = session_name
        self._interface = VboxInterface()
        self._machine_list = []

    def up():
        pass

    def down():
        pass

    def status():
        pass

    def pass_input(machine_name, input):
        pass

    @property
    def machine_list():
        return self._machine_list

    @property
    def session_id():
        return self._session_id

    


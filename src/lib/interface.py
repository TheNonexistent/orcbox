import subprocess
import sys

from lib.system.printformat import Print

# TODO: These Should be piped to a log later...
STDOUT = subprocess.DEVNULL
STDERR = subprocess.DEVNULL

def _run(cmd, name):
    ret = subprocess.run(cmd, capture_output=True)
    if ret.returncode != 0:
        Print.error("Error during " + name)
        Print.error("VirtualBox Manager command did not complete successfully.")
        Print.error("Info:")
        print(cmd)
        print("status: " + str(ret.returncode), "o: " + ret.stdout.decode('utf-8'), "\n", "e: " + ret.stderr.decode('utf-8'))
        Print.error("Aborting.")
        sys.exit(6) #TODO: Exit Gracefully
    return ret

class VboxInterface:
    @staticmethod
    def createvm(machine_name, uuid, os_type, base_folder, memory, cpu, vram, network, groups):
        try:
            cmd = ["VBoxManage", "createvm",
            "--name", machine_name,
            "--uuid", uuid,
            "--ostype", os_type,
            "--register",
            "--basefolder", base_folder]
            if groups != None:
                cmd += ["--groups", groups]
            # Debug Print: print("++", cmd)
            _run(cmd, "VM CREATION")
            cmd = ["VBoxManage", "modifyvm", uuid,
            "--ioapic", "on",
            "--cpus", str(cpu),
            "--memory", str(memory),
            "--vram", str(vram),
            "--nic1", network]
            # Debug Print: print("++", cmd)
            _run(cmd, "VM CREATION")
            Print.info(f"-- Created vm: {machine_name}:{uuid}, os_type: {os_type}, base_folder: {base_folder}, memory: {memory}, cpu: {cpu}, vram: {vram}, network: {network}, groups: {groups}")
        except Exception as e:
            Print.error("Error during VM CREATION")
            Print.error("Info:")
            print(e)
            sys.exit(6) #TODO: Exit Gracefully

    @staticmethod
    def createdisk(disk_location, size):
        try:
            cmd = ["VBoxManage", "createhd",
            "--filename", disk_location,
            "--size", str(size),
            "--format", "VDI"]
            # Debug Print: print("++", cmd)
            response = _run(cmd, "DISK CREATION") # TODO: return uuid of the created disk to be unregistered at purge
            Print.info(f"-- Created disk '{disk_location}' size: {size}")
        except Exception as e:
            Print.error("Error during DISK CREATION")
            Print.error("Info:")
            print(e)
            sys.exit(6) #TODO: Exit Gracefully


    @staticmethod
    def connectdisk(uuid, disk_location):
        try:
            cmd = ["VBoxManage", "storagectl", uuid,
            "--name", "\"SATA Controller\"",
            "--add", "sata",
            "--controller", "IntelAhci"]
            # Debug Print: print("++", cmd)
            _run(cmd, "DISK CONNECTION")
            cmd = ["VBoxManage", "storageattach", uuid,
            "--storagectl", "\"SATA Controller\"",
            "--port", "0",
            "--device", "0",
            "--type", "hdd",
            "--medium", disk_location]
            # Debug Print: print("++", cmd)
            response = _run(cmd, "DISK CONNECTION")# TODO: return uuid of the created disk to be unregistered at purge
        except Exception as e:
            Print.error("Error during DISK CONNECTION")
            Print.error("Info:")
            print(e)
            sys.exit(6) #TODO: Exit Gracefully
        Print.info(f"-- Connected disk to '{uuid}' location: {disk_location}")


    @staticmethod
    def connectboot(uuid, boot_location):
        try:
            cmd = ["VBoxManage", "storagectl", uuid,
            "--name", "\"IDE Controller\"",
            "--add", "ide",
            "--controller", "PIIX4"]
            # Debug Print: print("++", cmd)
            _run(cmd, "BOOT IMAGE CONNECTION")
            cmd = ["VBoxManage", "storageattach", uuid,
            "--storagectl", "\"IDE Controller\"",
            "--port", "1",
            "--device", "0",
            "--type", "dvddrive",
            "--medium", boot_location]
            # Debug Print: print("++", cmd)
            _run(cmd, "BOOT IMAGE CONNECTION")
        except Exception as e:
            Print.error("Error during BOOT IMAGE CONNECTION")
            Print.error("Info:")
            print(e)
            sys.exit(6) #TODO: Exit Gracefully
        Print.info(f"-- Connected boot image to '{uuid}' location: {boot_location}")


    @staticmethod
    def setbootorder(uuid, boot1="none", boot2="none", boot3="none", boot4="none"):
        try:
            cmd = ["VBoxManage", "modifyvm", uuid,
            "--boot1", boot1,
            "--boot2", boot2,
            "--boot3", boot3,
            "--boot4", boot4]
            # Debug Print: print("++", cmd)
            _run(cmd, "BOOT ORDER SETUP")
        except Exception as e:
            Print.error("Error during BOOT ORDER SETUP")
            Print.error("Info:")
            print(e)
            sys.exit(6) #TODO: Exit Gracefully
        Print.info(f"-- Set boot order on '{uuid}' order: 1-{boot1}, 2-{boot2}, 3-{boot3}, 4-{boot4}")

    @staticmethod
    def startvm(uuid):
        try:
            cmd = ["VBoxManage", "startvm", uuid,
            "--type", "headless"]
            # Debug Print: print("++", cmd)
            _run(cmd, "VM STARTUP")
        except Exception as e:
            Print.error("Error during VM STARTUP")
            Print.error("Info:")
            print(e)
            sys.exit(6) #TODO: Exit Gracefully

    @staticmethod
    def getvmrunning(uuid):
        running = VboxInterface._get_running_vms()
        if uuid in running:
            return True
        else:
            return False

    @staticmethod
    def poweroffvm(uuid):
        try:
            cmd = ["VBoxManage", "controlvm", uuid,
            "poweroff"]
            # Debug Print: print("++", cmd)
            _run(cmd, "VM POWEROFF")
        except Exception as e:
            Print.error("Error during VM POWEROFF")
            Print.error("Info:")
            print(e)
            sys.exit(6) #TODO: Exit Gracefully

    @staticmethod
    def acpipoweroffvm(uuid):
        try:
            cmd = ["VBoxManage", "controlvm", uuid,
            "acpipowerbutton"]
            # Debug Print: print("++", cmd)
            _run(cmd, "VM ACPI POWEROFF")
        except Exception as e:
            Print.error("Error during ACPI VM POWEROFF")
            Print.error("Info:")
            print(e)
            sys.exit(6) #TODO: Exit Gracefully

    @staticmethod
    def removevm(uuid, delete=False):## TODO: get the uuid of attached disk to unregister here
        try:
            cmd = ["VBoxManage", "unregistervm", uuid]
            if delete:
                cmd += ["--delete"]
            # Debug Print: print("++", cmd)
            _run(cmd, "VM REMOVE") 
        except Exception as e:
            Print.error("Error during VM REMOVE")
            Print.error("Info:")
            print(e)
            sys.exit(6) #TODO: Exit Gracefully

    @staticmethod
    def _get_running_vms():
        try:
            cmd = ["VBoxManage", "list", "runningvms"]
            response = _run(cmd, "GET RUNNING VMS")
            machines = response.stdout.decode('utf-8').split('\n')[:-1]
            uuids = [entry[entry.find('{')+1:entry.find('}')] for entry in machines]
            return uuids
        except:
            Print.error("Error during GET RUNNING VMS")
            Print.error("Info:")
            print(e)
            sys.exit(6) #TODO: Exit Gracefully




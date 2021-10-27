import subprocess
import sys

from lib.printformat import Print

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
    def createvm(machine_name, os_type, base_folder, memory, cpu, vram, network, groups):
        try:
            cmd = ["VBoxManage", "createvm",
            "--name", machine_name,
            "--ostype", os_type,
            "--register",
            "--basefolder", base_folder]
            if groups != None:
                cmd += ["--groups", groups]
            # Debug Print: print("++", cmd)
            _run(cmd, "VM CREATION")
            cmd = ["VBoxManage", "modifyvm", machine_name,
            "--ioapic", "on",
            "--cpus", str(cpu),
            "--memory", str(memory),
            "--vram", str(vram),
            "--nic1", network]
            # Debug Print: print("++", cmd)
            _run(cmd, "VM CREATION")
            Print.info(f"-- Created vm: {machine_name}, os_type: {os_type}, base_folder: {base_folder}, memory: {memory}, cpu: {cpu}, vram: {vram}, network: {network}, groups: {groups}")
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
            _run(cmd, "DISK CREATION")
            Print.info(f"-- Created disk '{disk_location}' size: {size}")
        except Exception as e:
            Print.error("Error during DISK CREATION")
            Print.error("Info:")
            print(e)
            sys.exit(6) #TODO: Exit Gracefully


    @staticmethod
    def connectdisk(machine_name, disk_location):
        try:
            cmd = ["VBoxManage", "storagectl", machine_name,
            "--name", "\"SATA Controller\"",
            "--add", "sata",
            "--controller", "IntelAhci"]
            # Debug Print: print("++", cmd)
            _run(cmd, "DISK CONNECTION")
            cmd = ["VBoxManage", "storageattach", machine_name,
            "--storagectl", "\"SATA Controller\"",
            "--port", "0",
            "--device", "0",
            "--type", "hdd",
            "--medium", disk_location]
            # Debug Print: print("++", cmd)
            _run(cmd, "DISK CONNECTION")
        except Exception as e:
            Print.error("Error during DISK CONNECTION")
            Print.error("Info:")
            print(e)
            sys.exit(6) #TODO: Exit Gracefully
        Print.info(f"-- Connected disk to '{machine_name}' location: {disk_location}")


    @staticmethod
    def connectboot(machine_name, boot_location):
        try:
            cmd = ["VBoxManage", "storagectl", machine_name,
            "--name", "\"IDE Controller\"",
            "--add", "ide",
            "--controller", "PIIX4"]
            # Debug Print: print("++", cmd)
            _run(cmd, "BOOT IMAGE CONNECTION")
            cmd = ["VBoxManage", "storageattach", machine_name,
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
        Print.info(f"-- Connected boot image to '{machine_name}' location: {boot_location}")


    @staticmethod
    def setbootorder(machine_name, boot1="none", boot2="none", boot3="none", boot4="none"):
        try:
            cmd = ["VBoxManage", "modifyvm", machine_name,
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
        Print.info(f"-- Set boot order on '{machine_name}' order: 1-{boot1}, 2-{boot2}, 3-{boot3}, 4-{boot4}")

    @staticmethod
    def startvm(machine_name):
        try:
            cmd = ["VBoxManage", "startvm", machine_name,
            "--type", "headless"]
            # Debug Print: print("++", cmd)
            _run(cmd, "VM STARTUP")
        except Exception as e:
            Print.error("Error during VM STARTUP")
            Print.error("Info:")
            print(e)
            sys.exit(6) #TODO: Exit Gracefully

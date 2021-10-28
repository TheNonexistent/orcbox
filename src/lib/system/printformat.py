from sys import stderr
Colors = {
   "LBLUE" : '\033[94m',
   "LGREEN" : '\033[92m',
   "LYELLOW" : '\033[93m',
   "LRED" : '\033[91m',
   "BLUE" : '\033[34m',
   "YELLOW" : '\033[33m',
   "RED" : '\033[31m',
   "GREEN" : '\033[32m',
   "PURPLE" : '\033[35m',
   "ENDC" : '\033[0m'
        }

class Color:
    @classmethod
    def paint(cls, color, text):
        color = color.upper()
        try:
            return Colors[color] + text + Colors["ENDC"]
        except KeyError:
            print("No such color: " + color)
            print("Please select from :")
            print(list(Colors.keys()))
            return

    @classmethod
    def catalog(cls):
        print(Colors)

class Print():
    @classmethod
    def success(cls, msg):
        print(Color.paint("green", msg))
    
    @classmethod
    def info(cls, msg):
        print(msg)

    @classmethod
    def warning(cls, msg):
        print("Warning: " + Color.paint("yellow", msg))

    @classmethod
    def error(cls, msg):
        print("Error: " + Color.paint("red", msg), file=stderr)
    
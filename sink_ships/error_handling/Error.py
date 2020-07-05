from classes.Color import Color

class Error:
    @classmethod
    def print_error(cls, msg):
        print(Color.BOLD + Color.RED + '[ERROR] ' + msg + Color.WHITE)
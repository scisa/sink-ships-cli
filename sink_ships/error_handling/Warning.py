from classes.Color import Color

class Warning:
    @classmethod
    def print_warning(cls, msg):
	    print(Color.BOLD + Color.YELLOW + '[WARNING] ' + msg + Color.WHITE)
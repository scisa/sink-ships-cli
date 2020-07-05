from classes.Color import Color

class Winning:
    @classmethod
    def winning(cls):
        print('\n' + Color.RED + 'Herzlichen Glückwunsch alle Schiffe wurden versenkt!' + Color.WHITE + '\n')
        exit(0)
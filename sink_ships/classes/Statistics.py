from classes.Color import Color
from util.GlobalVariables import GlobalVariables

class Statistics:
    @classmethod
    def print_statistics(cls):
        print("Gesamtanzahl Schüsse:", Color.BOLD, GlobalVariables.STONES_COUNT, Color.WHITE)
        print("Gesamtanzahl Wasser:", Color.BOLD, Color.BLUE, GlobalVariables.WATER_COUNT, Color.WHITE)
        print("Geamtanzahl Treffer:", Color.BOLD, Color.RED, GlobalVariables.HIT_COUNT, Color.WHITE, end='\n\n')
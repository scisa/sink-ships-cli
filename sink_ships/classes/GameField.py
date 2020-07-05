import re
import random

from classes.Color import Color
from util.GlobalConstants import GlobalConstants

class GameField:
	def __init__(self):
		self.field = [
						[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
						[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
						[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
						[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
						[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
						[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
						[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
						[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
						[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
						[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
					]

		self.ships = []


	def __calc_coordinates(self, row, col, direction, length):
		coordinates = []

		for ship in range(length):
			coordinates.append((row, col))
			if direction == 0: #N
				col = (int(col) + 1) %10
			elif direction == 1: #E
				row = (int(row) + 1) %10
			elif direction == 2: #S
				col = (int(col) - 1) %10
			else: #W
				row = (int(row) - 1) %10
			
		return coordinates

	def __draw_ship(self, coordinates, length):
		for coordinate in coordinates:
			if re.match('[1-5]', self.field[coordinate[0]][coordinate[1]]):
				return False
		
		self.ships.append(coordinates)
		for coordinate in coordinates:			
			self.field[coordinate[0]][coordinate[1]] = GlobalConstants.SHIP
		return True

	def __construct_ship(self, length):
		while True:
			col = random.randrange(0, 10, 1)
			row = random.randrange(0, 10, 1)
			direction = random.randrange(0, 4, 1)
			coordinates = self.__calc_coordinates(row, col, direction, length)
			if self.__draw_ship(coordinates, length):
				break

	def hide_ships(self):
		ships = [5, 4, 3, 3, 2]
		
		for ship_len in ships:
			self.__construct_ship(ship_len)
			GlobalConstants.SHIP = str(int(GlobalConstants.SHIP) + 1)
		
	def __print_col_numbers(self):
		print(' '*GlobalConstants.FLF, end='')
		for index, row in enumerate(self.get_field()):
			print(Color.WHITE + Color.BOLD + str(index) + Color.WHITE, end=' '*(GlobalConstants.FLF - 1))
		print('')

	def __print_row_separator(self):
		print('-'*GlobalConstants.SEP_FAC)

	def __print_rows(self):
		for index, row in enumerate(self.get_field()):
			print(Color.BOLD + GlobalConstants.number_to_letter[index] + Color.WHITE, end='')
			for i in range(10):
				if re.match('[1-5]',row[i]):
					stone = Color.GREEN + row[i] + Color.WHITE
				elif re.match('w', row[i]):
					stone = Color.BLUE + row[i] + Color.WHITE
				elif re.match('x', row[i]):
					stone = Color.RED + row[i] + Color.WHITE
				else:
					stone = Color.WHITE + row[i]
				print(' | ' + stone, end='')
			print(' | ')
			self.__print_row_separator()
		print("")

	def print_game_field(self):
		self.__print_col_numbers() # 1.Zeile Zahlen
		self.__print_row_separator() # 2.Zeile Abtrennung oben
		self.__print_rows() # restliche Zeilen rows

	def set_field(self, row, col, char):
		self.field[row][col] = char

	def get_field(self):
		return self.field

	def get_ships(self):
		return self.ships

	def delete_ship(self, index):
		self.ships.pop(index)

	def delete_coordinate(self, index, row, col):
		tuple_index = self.ships[index].index((row, col))
		self.ships[index].pop(tuple_index)
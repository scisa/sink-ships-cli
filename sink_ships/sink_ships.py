#!/usr/bin/env python3

#10x10 -> 1-10; A-J


import collections
import random
import re
import argparse

FLF = 4 #field length factor
SEP_FAC = 43 #row separator factor

GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
WHITE = '\033[0m'
BOLD = '\033[1m'

SHIP = '1'
HIT = 'x'
WATER = 'w'
TRYS = 3
STONES_COUNT = 0
HIT_COUNT = 0
WATER_COUNT = 0


number_to_letter = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E',
                    5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J'}

letter_to_number = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4,
                    'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9}
 

def print_error(msg):
	print(BOLD + RED + '[ERROR] ' + msg + WHITE)


def print_warning(msg):
	print(BOLD + YELLOW + '[WARNING] ' + msg + WHITE)


def wrong_location_error(game_try):
	print_error('That\'s not a valid input. Please try again.')
	print_warning("Only " + str(game_try) + " trys left before exiting!")


def trys_exceeded_error():
	print_error('You exceeded your number of trys. Exiting...')
	exit(1)


def doubled_shot_warning():
	print_warning('You have already shot at this place.')


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
			self.field[coordinate[0]][coordinate[1]] = SHIP
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
		global SHIP
		ships = [5, 4, 3, 3, 2]
		
		for ship_len in ships:
			self.__construct_ship(ship_len)
			SHIP = str(int(SHIP) + 1)
		
	def __print_col_numbers(self):
		print(' '*FLF, end='')
		for index, row in enumerate(self.get_field()):
			print(BOLD + str(index) + WHITE, end=' '*(FLF - 1))
		print('')

	def __print_row_separator(self):
		print('-'*SEP_FAC)

	def __print_rows(self):
		for index, row in enumerate(self.get_field()):
			print(BOLD + number_to_letter[index] + WHITE, end='')
			for i in range(10):
				if re.match('[1-5]',row[i]):
					stone = GREEN + row[i] + WHITE
				elif re.match('w', row[i]):
					stone = BLUE + row[i] + WHITE
				elif re.match('x', row[i]):
					stone = RED + row[i] + WHITE
				else:
					stone = WHITE + row[i]
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



def check_location(loc):
	if re.match('^[A-J][0-9]$', loc):
		return True
	return False


def shoot():
	game_try = TRYS
	while game_try > 0:
		location = input("Geben Sie eine Position ein, auf die Sie schiessen wollen (Bsp.: A0): ")
		if check_location(location):
			break
		game_try = game_try - 1
		wrong_location_error(game_try)
	else:
		trys_exceeded_error()
	return location
	

def calc_location_from_string(location):
	row = int(letter_to_number[list(location)[0]])
	col = int(list(location)[1])
	return row, col
	

def try_shooting(op_field, row, col):
	result = 0 # water
	if re.match('[1-5]', op_field.get_field()[row][col]):
		result = 1 # ship
	elif re.match(WATER, op_field.get_field()[row][col]) or re.match(HIT, op_field.get_field()[row][col]):
		result = 2 # bereits genommener Zug
	return result
	

def hit_water(op_field, your_field, row, col):
	global WATER_COUNT
	op_field.set_field(row, col, WATER)
	WATER_COUNT += 1
	your_field.set_field(row, col, WATER)

	return op_field, your_field


def winning():
	print('\n' + RED + 'Herzlichen Glückwunsch alle Schiffe wurden versenkt!' + WHITE + '\n')
	exit(0)


def check_if_ship_down(op_field, row, col):
	for index, ship in enumerate(op_field.get_ships()):
		if (row, col) in ship:
			op_field.delete_coordinate(index, row, col)
		if not ship:
			print('\n' + RED + 'Schiff versenkt!' + WHITE +'\n')
			op_field.delete_ship(index)
	if not op_field.get_ships():
		op_field.print_game_field()
		print_statistics()
		winning()
	return op_field


def hit_ship(op_field, your_field, row, col):
	global HIT_COUNT
	op_field.set_field(row, col, HIT)
	your_field.set_field(row, col, HIT)
	HIT_COUNT += 1
	op_field = check_if_ship_down(op_field, row, col)
	
	return op_field, your_field


def print_game_fields(your_field, op_field):
	if DEBUG:
		op_field.print_game_field()
	your_field.print_game_field()
	

def print_statistics():
	print("Gesamtanzahl Schüsse:", BOLD, STONES_COUNT, WHITE)
	print("Gesamtanzahl Wasser:", BOLD, BLUE, WATER_COUNT, WHITE)
	print("Geamtanzahl Treffer:", BOLD, RED, HIT_COUNT, WHITE, end='\n\n')


def play(op_field, your_field):
	global STONES_COUNT
	while True:
		print_game_fields(your_field, op_field)
		print_statistics()
		location = shoot()
		row, col = calc_location_from_string(location)
		result = try_shooting(op_field, row, col)
		if result == 0: # water
			STONES_COUNT += 1
			op_field, your_field = hit_water(op_field, your_field, row, col)
		elif result == 1:# ship
			STONES_COUNT += 1
			op_field, your_field = hit_ship(op_field, your_field, row, col)
		else:
			doubled_shot_warning()
		

def define_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="debug output", action="store_true")
    arguments = parser.parse_args()
    return arguments


if __name__ == "__main__":
	args = define_argument_parser()
	DEBUG = args.debug

	op_field = GameField()
	op_field.hide_ships()
	your_field = GameField()
	play(op_field, your_field)

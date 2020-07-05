#!/usr/bin/env python3

#10x10 -> 1-10; A-J


import collections
import random
import re
import argparse

from classes.Color import Color
from classes.Statistics import Statistics
from classes.GameField import GameField
from classes.Winning import Winning
from util.GlobalConstants import GlobalConstants
from util.GlobalVariables import GlobalVariables
from error_handling.Error import Error
from error_handling.Warning import Warning


def wrong_location_error(game_try):
	Error.print_error('That\'s not a valid input. Please try again.')
	Warning.print_warning("Only " + str(game_try) + " trys left before exiting!")


def trys_exceeded_error():
	Error.print_error('You exceeded your number of trys. Exiting...')
	exit(1)


def doubled_shot_warning():
	Warning.print_warning('You have already shot at this place.')


def check_location(loc):
	if re.match('^[A-J][0-9]$', loc):
		return True
	return False


def shoot():
	game_try = GlobalConstants.TRYS
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
	row = int(GlobalConstants.letter_to_number[list(location)[0]])
	col = int(list(location)[1])
	return row, col
	

def try_shooting(op_field, row, col):
	result = 0 # water
	if re.match('[1-5]', op_field.get_field()[row][col]):
		result = 1 # ship
	elif re.match(GlobalConstants.WATER, op_field.get_field()[row][col]) or re.match(GlobalConstants.HIT, op_field.get_field()[row][col]):
		result = 2 # bereits genommener Zug
	return result
	

def hit_water(op_field, your_field, row, col):
	op_field.set_field(row, col, GlobalConstants.WATER)
	GlobalVariables.WATER_COUNT += 1
	your_field.set_field(row, col, GlobalConstants.WATER)

	return op_field, your_field


def check_if_ship_down(op_field, row, col):
	for index, ship in enumerate(op_field.get_ships()):
		if (row, col) in ship:
			op_field.delete_coordinate(index, row, col)
		if not ship:
			print('\n' + Color.RED + 'Schiff versenkt!' + Color.WHITE +'\n')
			op_field.delete_ship(index)
	if not op_field.get_ships():
		op_field.print_game_field()
		Statistics.print_statistics()
		Winning.winning()
	return op_field


def hit_ship(op_field, your_field, row, col):
	op_field.set_field(row, col, GlobalConstants.HIT)
	your_field.set_field(row, col, GlobalConstants.HIT)
	GlobalVariables.HIT_COUNT += 1
	op_field = check_if_ship_down(op_field, row, col)
	
	return op_field, your_field


def print_game_fields(your_field, op_field):
	if DEBUG:
		op_field.print_game_field()
	your_field.print_game_field()
	

def play(op_field, your_field):
	while True:
		print_game_fields(your_field, op_field)
		Statistics.print_statistics()
		location = shoot()
		row, col = calc_location_from_string(location)
		result = try_shooting(op_field, row, col)
		if result == 0: # water
			GlobalVariables.STONES_COUNT += 1
			op_field, your_field = hit_water(op_field, your_field, row, col)
		elif result == 1:# ship
			GlobalVariables.STONES_COUNT += 1
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

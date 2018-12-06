import random
import sys
import pdb
import re
from enum import Enum
from custom_lib import *

class Cell_State(Enum):
	EXPLORED = 'X'
	UNEXPLORED = 'O'
	FLAGGED = 'F'

class MS_Grid():
	"""docstring for MS_Grid"""
	def __init__(self, n, debug=False, density=0.2):
		self.debug = debug
		self.density = density
		self.grid  = [[0 for _ in range(n)] for _ in range(n)]
		self.fog = [[Cell_State.UNEXPLORED for _ in range(n)] for _ in range(n)]
		self.populate()
		
	def populate(self):
		# Insert mines(-1) randomly
		for row in self.grid:
			for i in range(len(row)):
				row[i] = -1 if random.randint(0,101) < self.density*100 else 0

		for i in range(len(self.grid)):
			for j in range(len(self.grid[i])):
				if self.grid[i][j] == 0:
					count = 0
					for i_p in range(max(0,i-1), min(len(self.grid), i+2)):
						for j_p in range(max(0,j-1), min(len(self.grid[i]), j+2)):
							if self.grid[i_p][j_p] == -1:
								count += 1

					self.grid[i][j] = count


	def sweep_cell(self, x,y):
		# Marks the swept cell
		# Returns True if a mine was swept, otherwise False
		def _sweep_cell(x,y):
			if self.grid[x][y] >= 0 and self.fog[x][y] == Cell_State.UNEXPLORED:
				self.fog[x][y] = Cell_State.EXPLORED
				if self.grid[x][y] == 0:
					for i in range(max(0,x-1), min(len(self.grid), x+2)):
						for j in range(max(0,y-1), min(len(self.grid[i]), y+2)):
							_sweep_cell(i,j)

		_sweep_cell(x,y)
		self.fog[x][y] = Cell_State.EXPLORED
		if self.grid[x][y] == -1:
			return True
		return False

	def flag_cell(self, x, y):
		'''
			Toggles the flag on a cell.
		'''
		if self.is_swept(self.fog[x][y]):
			return
		if self.fog[x][y] == Cell_State.FLAGGED:
			self.fog[x][y] = Cell_State.UNEXPLORED
		else:
			self.fog[x][y] = Cell_State.FLAGGED

	def is_win(self):
		for i in range(len(self.grid)):
			for j in range(len(self.grid[i])):
				if self.grid[i][j] == -1 and self.fog[i][j] != Cell_State.FLAGGED:
					return False
		return True



	def __repr__(self):
		string = ''
		for i in range(len(self.grid)):
			for j in range(len(self.grid[i])):
				if self.fog[i][j] == Cell_State.EXPLORED or self.debug:
					if self.grid[i][j] < 0:
						string += f'* '
					else:
						string += f'{self.grid[i][j]} '
				else:
					string += f'{self.fog[i][j].value} '
			string +='\n'

		return string

	def play(self):
		print('Choose which cell to sweep.')
		print('How To:\t action x y\naction = s or f.\n ex. s 0 1')
		while not self.is_win():
			print(self)
			action = input('>>> ')
			if not re.match('[sfSF] [0-9]+ [0-9]+', action):
				print('Invalid action.')
				continue
			action,x,y = action.strip().split(' ')
			if not check_int(x) or not check_int(y):
				continue
			x = int(x)
			y = int(y)
			if action.lower() == 's':
				if self.sweep_cell(x,y):
					return False
			elif action.lower() == 'f':
				self.flag_cell(x,y)
			else:
				print(f'Invalid action: {action}')

		return True



if __name__ == '__main__':
	debug = False
	density = 0.2
	if len(sys.argv) > 0:
		for i in range(len(sys.argv)):
			if sys.argv[i] == '--debug':
				debug = True
			if sys.argv[i] == '--density':
				density = float(sys.argv[i+1])


	grid = MS_Grid(int(input('Grid Size: ')), debug, density)

	if grid.play():
		print(f'Congradulations Winner!\n{grid}')
	else:
		print(f'BOOOOOOMM!!!!\n{grid}')


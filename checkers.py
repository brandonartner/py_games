from math import copysign

class Piece():
	def __init__(self,color,direction):
		self.color = color.lower()
		self.direction = direction

	def king(self):
		self.color = self.color.upper()
		self.direction = 0

	def __repr__(self):
		return self.color


class CheckerBoard():
	def __init__(self,size=8):

		self.board = [['_' for _ in range(size)] for _ in range(size)]
		self.populate()

	def populate(self):
		'''
			Populates the board with initial conditions.
		'''
		for i in range(3):
			for j in range(i%2,len(self.board[i]),2):
				self.board[i][j%len(self.board[i])] = Piece('r',1)

		for i in range(3):
			for j in range(i-1%2,len(self.board[i]),2):
				self.board[i-3][j%len(self.board[i])] = Piece('b',-1)

	def move(self,x,y,nx,ny):
		'''
			Moves a piece. Returns True if move succesful, otherwise False.

			Valid move checks: 	- If there is a piece in the cell,
									return False
								- If move is not a diagonal, move in the correct direction,
									return False
								- If there is a piece in the new cell,
									- If it is a team piece,
										return False
									- If it is an enemy piece,
										- If the cell behind it is filled
											return False
										- otherwise,
											return True and captured piece

		'''
		# Cell will contain a string if not a piece.
		if not isinstance(self.board[x][y],Piece):
			print(f'No piece in the cell.')
			return False, None

		# Any move has to be +/- 1 in the column and + or - 1 in the row,
		#	depending on it's movement direction, unless it has been kinged
		#		(kinged represended by setting direction to zero)
		######## Doing this part wrong ###########
		#if not (abs(x-nx) == 1 and y-ny == copysign(1, self.board[x][y].direction)):
		#	return False, None

		# If there is a piece in the new cell
		if isinstance(self.board[nx][ny],Piece):
			if self.board[nx][ny].color == self.board[x][y].color:
				return False, None
			else:
				# Get the cell behind the new cell
				behind_nx = x + (nx - x)*2
				behind_ny = y + (ny - y)*2
				if isinstance(self.board[behind_nx][behind_ny], Piece):
					return False, None
				else:
					captured = self.board[nx][ny]
					self.board[nx][ny] = '_'
					self.board[behind_nx][behind_ny] = self.board[x][y]
					self.board[x][y] = '_'
					return True, captured

		self.board[nx][ny] = self.board[x][y]
		self.board[x][y] = '_'
		return True, None

	def win_condition(self):
		'''
			Checks if there are any win conditions. Returns player color
			that won. Returns None if no player has a winning condition.

			Win Conditions: - Opponent has no valid moves.
							- Opponent has no pieces left.
			Maybe implement draws.
			Draw conditions: - Both players concede to draw.
		'''
		return 

	def play(self,players=['r','b'],starting_player=0):
		'''
			Runs the main play loop.

			Loop Steps: - Print board
						- Get user move.
						- Attempt to perform move.
						- If invalid,
							return to top of loop.
						(- If can still move,
							return to top of loop.)
						- Otherwise,
							change player.
		'''
		curr_player = starting_player
		while not self.win_condition():
			print(f'----------------------------------------------\n{self}')
			print(f'It is player {players[curr_player]} turn.')
			command = input('Enter a piece\'s address and the address to move it to.\n')
			x,y,nx,ny = map(int,command.split(' '))

			result,captured = self.move(x,y,nx,ny)
			if not result:
				print(f'Invalid Move. Retry.')
				continue
			elif captured:
				print(f'Captured a {captured} piece. It remains your turn.')
				continue

			# Switch player.
			curr_player ^= 1




	def __repr__(self):
		'''
			Prints the checkers board.
		'''
		result = '  ' + ' '.join([str(i) for i in range(len(self.board))]) + '\n'
		for i,row in enumerate(self.board):
			result += f'{i} '
			for j,elem in enumerate(row):
				result += elem.__str__() + '|'
			result = result[:-1] + '\n'

		return result

if __name__ == '__main__':
	checkers = CheckerBoard()
	checkers.play()
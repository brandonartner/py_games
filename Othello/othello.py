class OthelloBoard():
	'''
		Othello board class.
	'''
	def __init__(self,size=8, players=('b','w')):
		'''
			Default size is 8x8.
			Initialize board to have the middle 4 filled.

			Args: 
					int : Size of the board. Default: 8
					(str,str) : Players on the board. Default: w and b.

			Todo: Implement a scoreboard. Update how the win checking works.
		'''
		self.EMPTY = '_'
		self.size = size
		self.board = [[self.EMPTY for _ in range(self.size)] for _ in range(self.size)]
		self.players = players
		self.scoreboard = {}

		for player in self.players:
			self.scoreboard[player] = 0

		init=True
		self.place('w',int(size/2)-1, int(size/2)-1, init=init)
		self.place('w',int(size/2), int(size/2), init=init)
		self.place('b',int(size/2)-1, int(size/2), init=init)
		self.place('b',int(size/2), int(size/2)-1, init=init)

	def set(self,color,x,y):
		'''
			Sets a cell to a desired color. No validity checking occures.
			Adjusts the score.

			Args:
					char : The color of the tile being placed.
					int : The row of the tile being placed.
					int : The column of the tile being placed.
		'''
		if  self.board[x][y] != self.EMPTY:
			self.scoreboard[self.board[x][y]] -= 1

		self.board[x][y] = color
		self.scoreboard[color] += 1

	def place(self,color,x,y,init=False):
		'''
			Place the tile on the board at x,y.

			Args:
					char : The color of the tile being placed.
					int : The row of the tile being placed.
					int : The column of the tile being placed.

			Returns:
						boolean : True, if valid placement; 
								  False, otherwise

			Valid Moves: 	- Cell has to be on the board.
							- Cell has to be empty.
							- Cell has to 'flank' other players pieces.
								Vertically, Horizontally, Diagonally
		'''
		# Is x and y in bounds?
		if (0 > x or  x >= self.size) or (0 > y or  y >= self.size):
			return False
		# Is there already a piece in that cell?
		if self.board[x][y] != self.EMPTY:
			return False

		# 1. Loop through all of the new spots neighbors
		# 2. 	If a neighbor is the opposite color, 
		# 3.		add it to the potential flip stack
		# 4.		Loop through cells in-line behind the different neighbor
		# 5. 			if cell has a tile the same color as the placed tile
		# 6.				Flip all cells in stack and return True
		# 7.			if cell is empty
		# 8.				return False
		flipped_cells = []
		if not init:
			for i in [-1,0,1]:
				for j in [-1,0,1]:
					potential_flips = []
					# Ensure neighbor is inbounds
					if (0 > x+i or  x+i >= self.size) or (0 > y+j or  y+j >= self.size):
						continue

					opponent = self.players[self.players.index(color)^1]

					if self.board[x+i][y+j] == opponent:
						# An opposing neighbor was found
						potential_flips.append((x+i,y+j))
						n = 2
						while 0 <= x+i*n < self.size and 0 <= y+j*n < self.size:

							if self.board[x+i*n][y+j*n] == opponent:
								potential_flips.append((x+i*n,y+j*n))
								n+=1
							elif self.board[x+i*n][y+j*n] == color:
								# Was a flank, flip flanked tiles
								# Leave loop
								for pos in potential_flips:
									self.set(color,pos[0],pos[1])
									flipped_cells.append(pos)
								break
							else:
								# Wasn't a flank, break out of loop
								break
			if not flipped_cells:
				return False

		self.set(color,x,y)
		return True

	def is_full(self):
		'''
			Checks if the board is full.

			Returns:
						boolean : True, if board is full;
								  False, otherwise
		'''
		for row in self.board:
			for elem in row:
				if elem == self.EMPTY:
					return False
		return True

	def winner(self):
		'''
			Counts the number of pieces for each color and returns the winner. 
			Winner is who had more.
			
			Returns:
					char : the winner, w or b. If there is a tie, None.
					dict : The scoreboard for the game as a dictionary.
		'''
		if self.scoreboard[self.players[0]] > self.scoreboard[self.players[1]]:
			return self.players[0], self.scoreboard
		elif self.scoreboard[self.players[0]] < self.scoreboard[self.players[1]]:
			return self.players[1], self.scoreboard
		else:
			return None, self.scoreboard

	def play(self):
		'''
			Main play loop for the game.
			User either enters coordinates.
						enters skip, to forfeit turn.
						enters q or concede, to forfeit game.

			Returns:
					char : the winner, w or b. If there is a tie, None.
					dict : The scoreboard for the game as a dictionary.
		'''
		curr_player = 0
		previous_player_forfeited_turn = False

		print(f'*************************** Welcome to Othello ***************************\n' 
				'The game ends when the board is full or no valid moves still exist.\n'
				'Note: The latter occures when both players forfeit their turns in a row.')
		while not self.is_full():
			print(f'-------------------------------------------------------------------------\n{self}')
			command = input(f'Player {self.players[curr_player]}\'s turn.\n'
								'Enter your next move. Example: a1\n'
								'If no valid moves exist enter: \'skip\'\n'
								'To concede game enter: \'concede\'\n'
								'>>> ')

			# Exit game loop. Current player forfeit
			if command == 'concede' or command == 'q':
				print(f'Player {self.players[curr_player]} forfeited the game.')
				return self.players[curr_player^1], {}
			if command == 'skip':
				print(f'Turn forfeited.')
				if previous_player_forfeited_turn:
					print('Both players forfeited.')
					return None, {}
				curr_player ^= 1
				previous_player_forfeited_turn = True
				continue

			previous_player_forfeited_turn = False
			try:
				# Split the entered command
				y,x = command.strip()

				# If invalid move, allow player to enter another move.
				if not self.place(self.players[curr_player],int(x)-1,ord(y)-97):
					print(f'({x},{y}) is an invalid placement. Try again.')
					continue
			except ValueError as e:
				print(f'Invalid input: {command}')
				continue

			# Switch players
			curr_player ^= 1

		return self.winner()

	def get_scoreboard(self):
		'''
			Get a string representation of the scoreboard.

			Returns:
						string : A string represetation of the scoreboard.
		'''
		result = 'Scoreboard:\n'

		for player in self.scoreboard.items():
			result += f'\t Player {player[0]}: {player[1]} |'

		return result[:-1] + '\n\n'

	def __repr__(self):
		'''
			Overridden __repr__ funtion.
			Return string representation of the board.

			Todo: Print the current scores for each player.
		'''
		result = self.get_scoreboard()

		result += '  ' + ' '.join([chr(i+97) for i in range(self.size)]) + '\n'

		for i in range(self.size):
			result += f'{i+1} '
			for j in range(len(self.board[i])):
				result += f'{self.board[i][j]}|'
			result = f'{result[:-1]}{i+1}\n'

		result += '  ' + ' '.join([chr(i+97) for i in range(self.size)]) + '\n'
		return result

if __name__ == '__main__':
	# Create a board
	board = OthelloBoard()

	# Start the main game loop.
	winner,player_counts = board.play()
	# Print the winner if there is one.
	print('*************************************************************************')
	if winner:
		print(f'Player {winner} wins!\n')
	else:
		print(f'Draw!\n')

	# Print the scores.
	print(board.get_scoreboard())

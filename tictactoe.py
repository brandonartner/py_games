import sys
import re

class FullBoardException(Exception):
	"""docstring for FullBoardException"""
	def __init__(self):
		super(FullBoardException, self).__init__()
		

class TicTacToe():
	"""docstring for TicTacToe"""
	def __init__(self):
		self.size = 3
		self.board = [['-' for _ in range(self.size)] for _ in range(self.size)]

	def is_full(self):
		for row in self.board:
			for elem in row:
				if elem == '-':
					return False
		return True

	def ai_move(self, letter='O'):
		for i in range(len(self.board)):
			for j in range(len(self.board[i])):
				if self.board[i][j] == '-':
					return self.make_move(i,j,letter)

		raise Exception('Out of room.')


	def make_move(self,x,y,player):
		if self.board[x][y] == '-':
			self.board[x][y] = player
			return True
		else:
			return False

	def __repr__(self):
		string = ''
		
		for row in self.board:
			for elem in row:
				string += f'{elem}|'
			string = string[:-1]
			string += '\n'
		return string


if __name__ == '__main__':
	board = TicTacToe()
	'''print(f'{board}')
				board.make_move(0,0,'X')
				print(f'{board}')
				print(f'{board.is_full()}')
			
				while board.ai_move():
					print(f'{board}')'''
	
	player_letter = 'X'
	while not board.is_full():
		print(f'{board}')
		player_move = input('Enter next move: ')
		if not re.match('[1-3],[1-3]', player_move):
			print('Invlaid Move.')
			continue
		x,y = map(int, player_move.split(','))
		if not board.make_move(x-1,y-1,player_letter):
			print('Invlaid Move.')
			continue

		try:
			board.ai_move()
		except Exception as e:
			pass

	print(f'Game Over!\n{board}')



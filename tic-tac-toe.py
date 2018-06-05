import random
from time import sleep
import sys
sys.setrecursionlimit(4000)

def getHumanInput(player):
	move = ' '

	while not tictactoe.isValidMove(move):
		print('Enter a move (1 - 9) for ' + player)
		move = input()
		
	return int(move)


def getComputerInput(player):
	sleep(1)
	
	if len(tictactoe.getValidMoves()) == 9:
		return random.choice(tictactoe.getValidMoves())

	# Impossible
	maxplayer = True if player == 'X' else False
	print('Calculating...')
	result = alphabeta(State(0, 0), -1, 1, maxplayer)
	print('Done!')
	print(result.action)
	return result.action


class State:
	def __init__(self, action, score):
		self.action = action
		self.score = score


def alphabeta(state, alpha, beta, maxplayer):

	# Stop search if the game is over
	winner = tictactoe.checkWin()
	score = 0

	if winner != ' ':
		if winner == 'X':
			score = 1
		if winner == 'O':
			score = -1
		return State(state.action, score)
	

	if maxplayer:
		highestScore = -1
		bestAction = -1

		for action in tictactoe.getValidMoves():
			tictactoe.performTurn(action)
			nextState = alphabeta(State(action, 0), alpha, beta, False)
			tictactoe.undoTurn(action)

			if bestAction == -1 or nextState.score > highestScore:
				bestAction = action
				highestScore = nextState.score

			alpha = max(alpha, highestScore)

			if beta <= alpha:
				return State(bestAction, highestScore)

		return State(bestAction, highestScore)


	if not maxplayer:
		smallestScore = 1
		bestAction = -1

		for action in tictactoe.getValidMoves():
			tictactoe.performTurn(action)
			nextState = alphabeta(State(action, 0), alpha, beta, True)
			tictactoe.undoTurn(action)

			if bestAction == -1 or nextState.score < smallestScore:
				bestAction = action
				smallestScore = nextState.score

			beat = min(beta, smallestScore)

			if beta <= alpha:
				return State(bestAction, smallestScore)

		return State(bestAction, smallestScore)


def drawBoard(board):
	
	print('   |   |   ')
	print(' 1 | 2 | 3 ')
	print('   |   |   ')
	print('---+---+---')
	print('   |   |   ')
	print(' 4 | 5 | 6 ')
	print('   |   |   ')
	print('---+---+---')
	print('   |   |   ')
	print(' 7 | 8 | 9 ')
	print('   |   |   ')
	
	print('\n' * 3)

	print('   |   |   ')
	print(' ' + board[0] + ' | ' + board[1] + ' | ' + board[2])
	print('   |   |   ')
	print('---+---+---')
	print('   |   |   ')
	print(' ' + board[3] + ' | ' + board[4] + ' | ' + board[5])
	print('   |   |   ')
	print('---+---+---')
	print('   |   |   ')
	print(' ' + board[6] + ' | ' + board[7] + ' | ' + board[8])
	print('   |   |   ')








class TicTacToe:

	def __init__(self):
		self.EMPTY = ' '
		self.winningCombinations = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
		self.gameOver = False
		self.board = [' '] * 9
		self.currentPlayer = 'X'


	# Resets the board to an empty state
	def reset(self):
		self.gameOver = False
		self.board = [' '] * 9
		self.currentPlayer = 'X'
		

	# Checks if a given move is valid
	def isValidMove(self, move):

		if(move not in '1 2 3 4 5 6 7 8 9'.split()):
			return False
		
		if self.board[int(move) - 1] != self.EMPTY:
			return False

		# Input is valid
		return True


	# Places a player's piece on a tile
	def performTurn(self, tile):
		self.board[tile - 1] = self.currentPlayer
		self.swapTurns()
		if self.checkWin() != self.EMPTY:
			self.gameOver = True


	# Clears a tile on the board
	def clearTile(self, tile):
		self.board[tile - 1] = self.EMPTY


	# Undoes a turn
	def undoTurn(self, tile):
		self.clearTile(tile)
		self.swapTurns()
		self.gameOver = False


	# Checks if a player has won
	def checkWin(self):
		
		# Check for win
		for combo in self.winningCombinations:
			tile1 = self.board[combo[0]]
			tile2 = self.board[combo[1]]
			tile3 = self.board[combo[2]]

			if tile1 == tile2 and tile2 == tile3 and tile1 != self.EMPTY:
				self.gameOver = True
				return tile1

		# Check if board is full
		if self.boardIsFull(self.board):
			self.gameOver = True
			return 'T'

		# No winners yet
		return self.EMPTY


	def swapTurns(self):
		if self.currentPlayer == 'X':
			self.currentPlayer = 'O'
		else:
			self.currentPlayer = 'X'


	def boardIsFull(self, board):
		for tile in self.board:
			if tile == self.EMPTY:
				return False

		return True


	def getValidMoves(self):
		validMoves = []
		for index, tile in enumerate(self.board):
			if tile == ' ':
				validMoves.append(index + 1)

		return validMoves





print('\n' * 100)
tictactoe = TicTacToe()
drawBoard(tictactoe.board)

while True:
	
	# Perform player turn
	if tictactoe.currentPlayer == 'X' and False:
		tictactoe.performTurn(getHumanInput(tictactoe.currentPlayer))
	else:
		tictactoe.performTurn(getComputerInput(tictactoe.currentPlayer))

	print('\n' * 100)
	drawBoard(tictactoe.board)


	# Check for game over
	if tictactoe.gameOver:
		winner = tictactoe.checkWin()
		if(winner == 'X' or winner == 'O'):
			print('Game over! ' + winner + ' wins!')
		if(winner == 'T'):
			print('Game over! It\'s a tie!\n')

		print('Press ENTER to play again')
		test = input()
		tictactoe.reset()
		print('\n' * 100)
		drawBoard(tictactoe.board)

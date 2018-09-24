#!/usr/bin/env/python
# -*- coding: utf-8 -*

import random
import network
import numpy as np
import copy

INFINITY = 100000000

class board(object):
	def __init__(self,evaluateClassA,evaluateClassB):
		"""In the chess, 0---empty, 1---black, -1---white, in the later, 1 and -1 respectively
		represents players who use 'black' and 'white' """

		self.evaluateA = evaluateClassA
		self.evaluateB = evaluateClassB
		self.chess = [[0,0,0,0,0,0,0,0],
		 	     [0,0,0,0,0,0,0,0],
	        	     [0,0,0,0,0,0,0,0],
		 	     [0,0,0,1,-1,0,0,0],
		 	     [0,0,0,-1,1,0,0,0],
		 	     [0,0,0,0,0,0,0,0],
		             [0,0,0,0,0,0,0,0],
		 	     [0,0,0,0,0,0,0,0]]

	def isGameOver(self,board):
		"""given a board, check if the game is over, 1---game over, 0---continue"""
		if(self.canMove(board,1) == False):
			if(self.canMove(board,-1) == False):
				return True
		return False
		
		

	def whoWins(self):
		"""decide which player wins the game, 1--Black win, -1--White win, 0--draw"""
		countBlack = 0
		countWhite = 0
		for i in range(8):
			for j in range(8):
				if(self.chess[i][j] == 1):
					countBlack = countBlack + 1
				elif(self.chess[i][j] == -1):
					countWhite = countWhite + 1

		if(countBlack > countWhite):
			return 1
		elif(countBlack == countWhite):
			return 0
		else:
			return -1


	def isLegal(self,row,column):
		"""check the move is on the board"""
		if( row<0 or row>=8 or column<0 or column>=8):
			return False
		return True

	def isLegalMove(self,board,move):
		"""a move is a three-dimension tuple (x,y,player)"""
		row,col,chessColor = move
		if( self.isLegal(row,col) == False or board[ row ][ col ] != 0):
			return False

		for dirx in range(-1,2):
			for diry in range(-1,2):
				if(dirx == 0 and diry == 0):
					continue
				x,y = row+dirx,col+diry
				if( self.isLegal(x,y)==True and board[x][y] == (-chessColor) ):
					i,j = row+2*dirx,col+2*diry
					while(self.isLegal(i,j) == True):
						if(board[i][j] == (-chessColor)):
							i,j = i+dirx,j+diry
							continue
						elif(board[i][j] == chessColor):
							return True
						else:
							break
						
		return False

	def getMoves(self,board,player):
		"""get all the legal moves in the current board for the player"""
		legalMove = []
		for i in range(8):
			for j in range(8):
				move = tuple([i,j,player])
				if(self.isLegalMove(board,move) == True):
					legalMove.append(move)

		return legalMove



	def canMove(self,board,player):
		"""check whether or not the player can move in this step"""
		legalMove = self.getMoves(board,player)
		if (legalMove):
			return True
		else:
			return False

	def makeMove(self,board,move):
		"""given a current board and move, return a new board based on the game rule"""
		row,col,chessColor = move
		newBoard = copy.deepcopy(board)
		for dirx in range(-1,2):
			for diry in range(-1,2):
				if(dirx == 0 and diry ==0):
					continue
				temp = 0
				x,y = row+dirx,col+diry
				if(self.isLegal(x,y) == True and board[x][y] == (-chessColor)):
					temp = temp + 1
					i,j = row+2*dirx,col+2*diry
					while(self.isLegal(i,j) == True):
						if(board[i][j] == (-chessColor)):
							i,j = i+dirx,j+diry
							temp = temp + 1
							continue
						elif(board[i][j] == chessColor):
							m,n = row+dirx,col+diry
							while(temp > 0):
								newBoard[m][n] = chessColor
								m,n = m+dirx,n+diry
								temp = temp - 1
							break
						else:
							break

		newBoard[row][col] = chessColor
		return newBoard
						

	def changeBoard(self,move):
		"""revise the board of current class, its implementation is based on makeMove() method """
		self.chess = self.makeMove(self.chess,move)


	def abNegaMax(self, board, evaluateClass, player, depth, maxDepth, alpha, beta):
		if( self.isGameOver(board) or depth == maxDepth ):
			score = evaluateClass.evaluate(board)
			return -score,None
		
		#if current player can't move, the other player take the turn, the depth remains unchanged
		if( self.canMove(board,player) == False ):
			score,temp = self.abNegaMax(board,evaluateClass,-player,depth,maxDepth,-beta,-alpha)
			return score,temp

		bestMove = None
		bestScore = -INFINITY
		validMoves = self.getMoves(board,player)
		for move in validMoves:
			newBoard = self.makeMove(board,move)
			score,tmep = self.abNegaMax(newBoard, evaluateClass, -player, depth+1, maxDepth, -beta, -max(alpha,bestScore))
			score = - score
			if(score > bestScore):
				bestScore = score
				bestMove = move
				if(bestScore >= beta):
					return bestScore,bestMove
		return bestScore,bestMove




def simulate(playerA,playerB):
	"""simulate two players compete, assume playerA uses black. return 1 if playerA wins, -1 if playerA loses, 
	0 if two players draw"""
	Board = board(playerA,playerB)

	while( Board.isGameOver(Board.chess) == False ):
		if( Board.canMove(Board.chess,1) == True ):
			#if playerA can move
			score,move = Board.abNegaMax(Board.chess, Board.evaluateA, 1, 0, 3, -INFINITY, INFINITY)
			Board.changeBoard(move)

		if( Board.isGameOver(Board.chess) == True ):
			break

		if( Board.canMove(Board.chess,-1) == True ):
			#if playerB can move
			score,move = Board.abNegaMax(Board.chess, Board.evaluateB, -1, 0, 3, -INFINITY, INFINITY)
			Board.changeBoard(move)
	flag = Board.whoWins()
	return flag

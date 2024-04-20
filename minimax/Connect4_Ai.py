import math
import random
import numpy as np  

#constants to make code more readable
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

ROW_COUNT = 6
COLUMN_COUNT = 7

GET_VALID_MOVES = [3,4,2,6,0,5,1]

WINDOW_LENGTH = 4

#scoreing constants
WIN_SCORE = 1000000000
LOSE_SCORE = -100000000000000000000000

FOURINROW = 10000
THREEINROW = 10
TWOINROW = 3
MIDDLE_COLUMN =2

AGING_PENALTY = 3

OPP_FOURINROW = -100000000000000000000000
OPP_THREEINROW = -12
OPP_TWOINROW = -4

#Win/loss counting variables

##################### min max algorithm ################################

def minimax (grid, depth, alpha, beta, isMaximisingPlayer, heuristic):
    validLocations = getValidMoves(grid)

    #depth = 0 game won or no valid moves left
    if isTerminal(grid) or depth == 0: 
        if isTerminal(grid):
            if PieceWinCheck(grid, AI_PIECE):
                score = WIN_SCORE+depth*AGING_PENALTY #score is greater for wins in fewer moves
                return(None, score) 
            
            elif PieceWinCheck(grid, PLAYER_PIECE):
                score = LOSE_SCORE-depth*AGING_PENALTY #score is less when player can win in few moves
                return(None, score)
            
            else: #game over no more valid moves
                return (None, 0)
        else: #depth is 0 so leaf node reached
            return (None, heuristic(grid,AI_PIECE)) #return score for game output
      
    if isMaximisingPlayer:
        value = -math.inf
        column = random.choice(validLocations)
        for col in validLocations:
            tempGrid = np.copy(grid)
            Drop(tempGrid, col, AI_PIECE)
            newScore = minimax(tempGrid, depth-1, alpha, beta, False, heuristic)[1]
            if newScore > value:
                value = newScore
                column = col

            #alpha pruning
            alpha = max (alpha, value)
            if alpha >= beta:
                break

        return column, value
    
    else: #minimising player
        value = math.inf
        column = random.choice(validLocations)
        for col in validLocations:
            tempGrid = np.copy(grid)
            Drop(tempGrid, col, PLAYER_PIECE)
            newScore = minimax(tempGrid, depth-1, alpha, beta, True, heuristic)[1]
            if newScore < value:
                value = newScore
                column = col
            
            #beta pruning
            beta = min(beta, value)
            if alpha >= beta:
                break
        
        return column, value

#################### making moves ##########################

def Drop(grid, column, num):
        i = 0
        for i in range(6):
           if grid[column][i] != 0:
                grid[column][i-1] = num
                break
           elif i == 5:
                grid[column][i] = num
        return grid


################### finding valid moves ############################

def getValidMoves(grid):
    validLocaions=[]
    for column in GET_VALID_MOVES: #ordered so that rows closest to middle are at the start
        if IsValid(grid, column) == True:
            validLocaions.append(column)
    return validLocaions

def IsValid(grid, columnIndex):
     #checks column isnt full
        if grid[columnIndex][0] == 0: #if top empty turn is valid
            return True
        else: #else column is full and move not valid
            return False

################# evaluating board ###################

def score_position(board, piece):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[COLUMN_COUNT//2,:])]
	center_count = center_array.count(piece)
	score += center_count * MIDDLE_COLUMN

	## Score Horizontal
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[:,r])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score Vertical
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[c,:])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score postive sloped diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[c+i][r+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[c+3-i][r+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score


def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	if window.count(piece) == 4:
		score += FOURINROW
		return score
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += THREEINROW
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += TWOINROW

	if window.count(opp_piece) == 4:
		score -= FOURINROW
		return score
	elif window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= THREEINROW
	elif window.count(opp_piece) == 2 and window.count(EMPTY) == 2:
		score -= TWOINROW
	return score

########################### Game End Conditions ##################

def isTerminal(grid): #is grid full
    return PieceWinCheck(grid, PLAYER_PIECE) or PieceWinCheck(grid, AI_PIECE) or len(getValidMoves(grid)) == 0

def PieceWinCheck(board, piece): # has someone won
	# Check vert? locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT -3):
			if board[c][r] == piece and board[c][r+1] == piece and board[c][r+2] == piece and board[c][r+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT -3):
		for r in range(ROW_COUNT):
			if board[c][r] == piece and board[c+1][r] == piece and board[c+2][r] == piece and board[c+3][r] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[c][r] == piece and board[c+1][r-1] == piece and board[c+2][r-2] == piece and board[c+3][r-3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT -3):
			if board[c][r] == piece and board[c+1][r+1] == piece and board[c+2][r+2] == piece and board[c+3][r+3] == piece:
				return True
	return False

#################### Zobrist Hashing #######################

# generates a zorbist table filled with random numbers which remin constant throuhgt a game
numBoardCells, numPieces = ROW_COUNT * COLUMN_COUNT, 2 
zobristMatrix = [[random.randint(1,2**64 - 1) for x in range(numPieces)] for y in range(numBoardCells)]


def FindHash (grid): # returns zobrist hash key for current board config
	zobHashVal = 0 
	for row in range(ROW_COUNT-1):
		for col in range(COLUMN_COUNT-1):
			if grid[col][row] != 0:
				piece = grid[col][row]

				gridPosition = (row * COLUMN_COUNT) + col

				zobHashVal ^= zobristMatrix[gridPosition][piece] #XOR Operation on all piece position and types to create unique hash
				print("Zobrist hash value is: "+zobHashVal)

	return hash

def evaluate_board2(grid, piece):
      values = [
		[3, 4, 5, 5, 4, 3],
		[4, 6, 8, 8, 6, 4],
		[5, 8, 11, 11, 8, 5],
		[7, 10, 13, 13, 10, 7],
		[5, 8, 11, 11, 8, 5],
		[4, 6, 8, 8, 6, 4],
		[3, 4, 5, 5, 4, 3]
	]
      score = 0
      for row in range(len(grid)):
           for col in range(len(grid[row])):
                if grid[row][col] == piece:
                      score += values[row][col]
      return score


#### Evaluate 1

# Constants for feature values
WIN2_SCORE = float('inf')
THREE_CONNECTED_SCORE = 900000
TWO_CONNECTED_SCORE = {
    5: 40000,
    4: 30000,
    3: 20000,
    2: 10000
}

SINGLE_SCORE = {
     'a': 40,
     'b': 90,
     'c': 200,
     'd': 200,
	 'e': 90,
	 'f': 40,
}

def evaluate_board1(grid, piece):
    score = 0

    # Evaluate Feature 1: Absolute win
    if PieceWinCheck(grid, piece):
        score += WIN2_SCORE

    # Evaluate Feature 2: Three connected chessmen
    three_connected_score = evaluate_three_connected(grid, piece)
    score += three_connected_score

    # # Evaluate Feature 3: Two connected chessmen
    two_connected_score = evaluate_two_connected(grid, piece)
    score += two_connected_score

    # Evaluate Feature 4: Single chessman
    single_score = evaluate_single(grid, piece)
    score += single_score

    return score


def evaluate_three_connected(grid, piece):
    score = 0
    directions = [(0, 1), (1, 1), (1, 0), (1, -1)]
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == piece:
                for dr, dc in directions:
                    count = 1
                    r, c = row + dr, col + dc
                    while 0 <= r < len(grid) and 0 <= c < len(grid[0]) and grid[r][c] == piece:
                        count += 1
                        r += dr
                        c += dc
                    if count >= 3:
                        if is_move_possible_both_sides(grid, row, col) == 2:
                              score += WIN2_SCORE
                        elif is_move_possible_both_sides(grid, row, col) == 1:
                              score += THREE_CONNECTED_SCORE
                        else:
                              score += 0      
    return score

def is_move_possible_both_sides(grid, row, col):
    piece = grid[row][col]
    # Check if moves are possible on both sides horizontally
    if col > 0 and col < len(grid[0]) - 1:
        if grid[row][col - 1] == EMPTY and grid[row][col + 1] == EMPTY:
            return 2
        elif grid[row][col - 1] == EMPTY or grid[row][col + 1] == EMPTY:
            return 1
    return 0


def evaluate_two_connected(grid, piece):
    score = 0
    directions = [(0, 1), (1, 1), (1, 0), (1, -1)]
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == piece:
                for dr, dc in directions:
                    count = 1
                    r, c = row + dr, col + dc
                    while 0 <= r < len(grid) and 0 <= c < len(grid[0]) and grid[r][c] == piece:
                        count += 1
                        r += dr
                        c += dc
                    if count == 2:
                        score += TWO_CONNECTED_SCORE[count]
    return score

def evaluate_single(grid, piece):
    score = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == piece:
                # Check if the piece is one square away from two connected men
                if is_one_square_away_from_two_connected(grid, row, col):
                    score += 900000
                else:
                    # Check if the piece is in a special position
                    position = get_position(row, col)
                    if position in SINGLE_SCORE:
                        score += SINGLE_SCORE[position]
    return score

def is_one_square_away_from_two_connected(grid, row, col):
    piece = grid[row][col]
    directions = [(0, 1), (1, 1), (1, 0), (1, -1)]
    for dr, dc in directions:
        next_row, next_col = row + dr, col + dc
        if 0 <= next_row < len(grid) and 0 <= next_col < len(grid[0]) and grid[next_row][next_col] == piece:
            next_next_row, next_next_col = next_row + dr, next_col + dc
            if 0 <= next_next_row < len(grid) and 0 <= next_next_col < len(grid[0]) and grid[next_next_row][next_next_col] == EMPTY:
                return True
    return False

def get_position(row, col):
    columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    return columns[col]

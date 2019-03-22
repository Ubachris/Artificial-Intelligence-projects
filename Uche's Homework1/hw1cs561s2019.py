
OPPONENT_EMITTER= 2
MY_EMITTER= 1
JOINT_EMISSION= 6
FREE= 0
BLOCK= 3
SIZE= 0
value_and_positions= {}

with open('input2.txt', "r") as file:
	SIZE= file.readline()
	SIZE= int(SIZE)
	input_board= []

	for line in range(int(SIZE)):
		row= file.readline().split()
		input_board.append(row)

boardx= []
for line in input_board:
	int_line= []
	for value in line:
		for letter in value:
			int_line.append(int(letter))
	boardx.append(int_line)


def print_board(board_to_print):
	"""Converts board to a string representation"""
	for row in board_to_print:
		str_row=[]
		for col in row:
			col= str(col)
			str_row.append(col)
		print " ".join(str_row)

def not_out_of_bounds(row,col):
	if (row >= 0 and row < SIZE and col >= 0 and col < SIZE):
		return True
	else:
		return False


def emittLaser(board,row,col, emitter):

	#temp_new_board = [list(x) for x in board]

	if emitter== 1:  #checks what emitter positons are being expanded 
		current_emitt= 4
		enemy_emitt= 5
	else:
		current_emitt= 5
		enemy_emitt= 4

	for i in range(-3,4):

		if i > 0:
			if (row >= 0 and row < SIZE and col+i >= 0 and col+i < SIZE):    #Check to see if position is out of bounds
				if (board[row][col+i] != BLOCK): #checks the WEST to see if there's either a block or emitter in said position 
					if board[row][col+i] == FREE:
						if (not_out_of_bounds(row,col+i-1) and not_out_of_bounds(row,col+i-2)) and (board[row][col+i-1] != BLOCK and board[row][col+i-2] != BLOCK) or board[row][col+i-1] == emitter:
							"""checks the positions to the left to see if it's being blocked off"""
							board[row][col+i]= current_emitt
							
					elif board[row][col+i]== enemy_emitt:
						if (not_out_of_bounds(row,col+i-1) and not_out_of_bounds(row,col+i-2)) and  (board[row][col+i-1] != BLOCK and  board[row][col+i-2] != BLOCK) or board[row][col+i-1] == emitter:
							"""checks if there's already a laser covering said position and it is legal to also cover it"""
							board[row][col+i]= JOINT_EMISSION

			if (row+i >= 0 and row+i < SIZE and col >= 0 and col <SIZE):    #Check to see if position is within of bounds
				if (board[row+i][col] != BLOCK): #checks the SOUTH for the same conditions 
					if board[row+i][col] == FREE:
						if (not_out_of_bounds(row+i-1,col) and not_out_of_bounds(row+i-2,col)) and (board[row+i-1][col] != BLOCK and board[row+i-2][col] != BLOCK) or board[row+i-1][col] == emitter:
							board[row+i][col]= current_emitt

					elif board[row+i][col]== enemy_emitt:
						if (not_out_of_bounds(row+i-1,col) and not_out_of_bounds(row+i-2,col)) and (board[row+i-1][col] != BLOCK and board[row+i-2][col] != BLOCK) or board[row+i-1][col] == emitter:
							"""checks if there's already a laser covering said position and it is legal to also cover it"""
							board[row+i][col]= JOINT_EMISSION

			if (row+i >= 0 and row+i < SIZE and col+i >= 0 and col+i <SIZE):    #Check to see if position is within of bounds
				if (board[row+i][col+i] != BLOCK): #checks the SOUTH-WEST for the same conditions 
					if board[row+i][col+i] == FREE:
						if (not_out_of_bounds(row+i-1,col+i-1) and not_out_of_bounds(row+i-2,col+i-2)) and (board[row+i-1][col+i-1] != BLOCK and board[row+i-2][col+i-2] != BLOCK) or board[row+i-1][col+i-1] == emitter:
							board[row+i][col+i]= current_emitt

					elif board[row+i][col+i]== enemy_emitt:
						if (not_out_of_bounds(row+i-1,col+i-1) and not_out_of_bounds(row+i-2,col+i-2)) and (board[row+i-1][col+i-1] != BLOCK and board[row+i-2][col+i-2] != BLOCK) or board[row+i-1][col+i-1] == emitter:
							"""checks if there's already a laser covering said position and it is legal to also cover it"""
							board[row+i][col+i]= JOINT_EMISSION

			if (row-i >= 0 and row-i < SIZE and col+i >= 0 and col+i <SIZE):    #Check to see if position is within of bounds
				if (board[row-i][col+i] != BLOCK): #checks the NORTH-EAST for the same conditions 
					if board[row-i][col+i] == FREE:
						if (not_out_of_bounds(row-i+1,col+i-1) and not_out_of_bounds(row-i+2,col+i-2)) and (board[row-i+1][col+i-1] != BLOCK and board[row-i+2][col+i-2] != BLOCK) or board[row-i+1][col+i-1] == emitter:
							board[row-i][col+i]= current_emitt

					elif board[row-i][col+i]== enemy_emitt:
						if (not_out_of_bounds(row-i+1,col+i-1) and not_out_of_bounds(row-i+2,col+i-2)) and (board[row-i+1][col+i-1] != BLOCK and board[row-i+2][col+i-2] != BLOCK) or board[row-i+1][col+i-1] == emitter:
							"""checks if there's already a laser covering said position and it is legal to also cover it"""
							board[row-i][col+i]= JOINT_EMISSION


		elif i < 0:
			if (row >= 0 and row < SIZE and col+i >= 0 and col+i <SIZE):    #Check to see if position is within of bounds
				if (board[row][col+i] != BLOCK): #checks the EAST to see if there's either a block or emitter in said position
					if board[row][col+i] == FREE:
						if (not_out_of_bounds(row,col+i+1) and not_out_of_bounds(row,col+i+2)) and (board[row][col+i+1] != BLOCK and board[row][col+i+2] != BLOCK) or board[row][col+i+1] == emitter:
							"""checks the positions to the left to see if it's being blocked off"""
							board[row][col+i]= current_emitt

					elif board[row][col+i]== enemy_emitt:
						if (not_out_of_bounds(row,col+i+1) and not_out_of_bounds(row,col+i+2)) and (board[row][col+i+1] != BLOCK and board[row][col+i+2] != BLOCK) or board[row][col+i+1] == emitter:
							board[row][col+i]= JOINT_EMISSION

			if (row+i >= 0 and row+i < SIZE and col >= 0 and col <SIZE):    #Check to see if position is within of bounds
				if (board[row+i][col] != BLOCK): #checks the NORTH for the same conditions 
					if board[row+i][col] == FREE:
						if (not_out_of_bounds(row+i+1,col) and not_out_of_bounds(row+i+2,col)) and (board[row+i+1][col] != BLOCK and board[row+i+2][col] != BLOCK) or board[row+i+1][col] == emitter:
							board[row+i][col]= current_emitt

					elif board[row+i][col]== enemy_emitt:
						if (not_out_of_bounds(row+i+1,col) and not_out_of_bounds(row+i+2,col)) and (board[row+i+1][col] != BLOCK and board[row+i+2][col] != BLOCK) or board[row+i+1][col] == emitter:
							"""checks if there's already a laser covering said position and it is legal to also cover it"""
							board[row+i][col]= JOINT_EMISSION

			if (row+i >= 0 and row+i < SIZE and col+i >= 0 and col+i <SIZE):    #Check to see if position is within of bounds
				if (board[row+i][col+i] != BLOCK): #checks the SOUTH-EAST for the same conditions 
					if board[row+i][col+i] == FREE:
						if (not_out_of_bounds(row+i+1,col+i+1) and not_out_of_bounds(row+i+2,col+i+2)) and (board[row+i+1][col+i+1] != BLOCK and board[row+i+2][col+i+2] != BLOCK) or board[row+i+1][col+i+1] == emitter:
							board[row+i][col+i]= current_emitt

					elif board[row+i][col+i]== enemy_emitt:
						if (not_out_of_bounds(row+i+1,col+i+1) and not_out_of_bounds(row+i+2,col+i+2)) and (board[row+i+1][col+i+1] != BLOCK and board[row+i+2][col+i+2] != BLOCK) or board[row+i+1][col+i+1] == emitter:
							"""checks if there's already a laser covering said position and it is legal to also cover it"""
							board[row+i][col+i]= JOINT_EMISSION

			if (row-i >= 0 and row-i < SIZE and col+i >= 0 and col+i <SIZE):    #Check to see if position is within bounds
				if (board[row-i][col+i] != BLOCK): #checks the SOUTH-WEST for the same conditions 
					if board[row-i][col+i] == FREE:
						if (not_out_of_bounds(row-i-1,col+i+1) and not_out_of_bounds(row-i-2,col+i+2)) and (board[row-i-1][col+i+1] != BLOCK and board[row-i-2][col+i+2] != BLOCK) or board[row-i-1][col+i+1] == emitter:
							board[row-i][col+i]= current_emitt

					elif board[row-i][col+i]== enemy_emitt:
						if (not_out_of_bounds(row-i-1,col+i+1) and not_out_of_bounds(row-i-2,col+i+2)) and (board[row-i-1][col+i+1] != BLOCK and board[row-i-2][col+i+2] != BLOCK) or board[row-i-1][col+i+1] == emitter:
							"""checks if there's already a laser covering said position and it is legal to also cover it"""
							board[row-i][col+i]= JOINT_EMISSION

	return board

def processBoard(board_to_process):
	my_board = [list(x) for x in board_to_process]
	initial_board= board_to_process
	i=0
	for row in board_to_process:
		j=0 
		for col in row:
			if initial_board[i][j] == OPPONENT_EMITTER or initial_board[i][j] == MY_EMITTER:
				emitter= initial_board[i][j]
				my_board = emittLaser(initial_board,i,j,emitter)
			j+=1

		i+=1 
	return my_board

def is_terminal_position(board):
	i=0
	for row in board:
		j=0
		for col in row:
			if board[i][j] == FREE:
				return False
			j+=1
		i+=1
	return True 


def utility(board_state,isFinal):
	
	my_points=0
	opponent_points=0
	my_laser= 4
	opponent_laser= 5
	i= 0

	for row in board_state:
		j=0
		for col in row:
			if board_state[i][j] == OPPONENT_EMITTER or board_state[i][j] == opponent_laser:
				opponent_points += 1
			elif board_state[i][j] == MY_EMITTER or board_state[i][j] == my_laser:
				my_points +=1
			j+=1
		i+=1

	result= my_points - opponent_points
	if isFinal:
		if result > 0:
			return float("inf")
		elif result < 0:
			return float("-inf")
		else:
			return 0
	else:
		return result 



def minimax(board_state, depth, maximizingPlayer, firstLayer,alpha,beta):
	#print_board(board_state)
	
	new_board= processBoard(board_state)
	#print(new_board)
	#print("-----")
	if is_terminal_position(new_board):
		#print("????")
		return utility(new_board,True)
	if depth == 0:
		return utility(new_board,False)

	temp_board = [ list(x) for x in new_board]
	if maximizingPlayer == True:
		maxEval= float('-inf')
		i=0
		for row in board_state:
			j=0
			for col in row:
				#if depth == 3:
					#print_board(new_board)
					#print("----------")
				if new_board[i][j] == FREE:
					#if depth == 3:
						#print("lol")
					temp_board[i][j]= MY_EMITTER
					#print(str(i)+" "+str(j))
					#print("mine---"+str(depth))
					once = True
					if once:
						once = False
						evaluate= minimax(temp_board, depth-1, False, firstLayer,alpha,beta)
					#if depth == 3:
					#	print(evaluate)
					#print(evaluate)
					if depth == firstLayer:
						#print(value_and_positions)
						coord= [i,j]
						value_and_positions[evaluate]= coord

					maxEval= max(maxEval, evaluate)
					if evaluate >= beta:
						return evaluate
					alpha = max(alpha,evaluate)
				j+=1
			i+=1
		return maxEval

	else:
		minEval= float('inf')
		i=0
		for row in board_state:
			j=0
			for col in row:
				if new_board[i][j] == FREE:
					temp_board[i][j] = OPPONENT_EMITTER
					#print(str(i)+" "+str(j))
					#print("op---")
					once = True
					if once:
						once = False
						evaluate= minimax(temp_board, depth-1, True, firstLayer,alpha,beta)
					minEval= min(minEval, evaluate)
					if evaluate <= alpha:
						return evaluate
					beta = min(beta,evaluate)
				j+=1
			i+=1
		return minEval


#print_board(processBoard(boardx))
best_move= minimax(boardx, 10, True, 10,float("-inf"),float("inf"))
#print value_and_positions
final_move= value_and_positions[best_move]
print final_move
output= open('output.txt', "w")
output.write(str(final_move[0])+ " "+ str(final_move[1]))









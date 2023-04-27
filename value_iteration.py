#import modules
import pygame
from pygame.locals import *
import random
import numpy as np

pygame.init()

#define colours
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

#define font
font = pygame.font.SysFont(None, 40)

#define variables
clicked = False
player = 1
pos = (0,0)
markers = []
game_over = False
winner = 0


n = int(input('Enter n = '))
# n = 2
#create empty 3 x 3 list to represent the grid
for x in range (n):
	row = [0] * n
	markers.append(row)

screen_height = 100 * n
screen_width = 100 * n
line_width = 6
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tic Tac Toe')

#setup a rectangle for "Play Again" Option
again_rect = Rect(screen_width // 2 - 80, screen_height // 2, 160, 50)

def draw_board():
	bg = (255, 255, 210)
	grid = (50, 50, 50)
	screen.fill(bg)
	for x in range(1,n):
		pygame.draw.line(screen, grid, (0, 100 * x), (screen_width,100 * x), line_width)
		pygame.draw.line(screen, grid, (100 * x, 0), (100 * x, screen_height), line_width)

def draw_markers(): 
	x_pos = 0
	for x in markers:
		y_pos = 0
		for y in x:
			if y == 1:
				pygame.draw.line(screen, red, (x_pos * 100 + 15, y_pos * 100 + 15), (x_pos * 100 + 85, y_pos * 100 + 85), line_width)
				pygame.draw.line(screen, red, (x_pos * 100 + 85, y_pos * 100 + 15), (x_pos * 100 + 15, y_pos * 100 + 85), line_width)
			if y == -1:
				pygame.draw.circle(screen, green, (x_pos * 100 + 50, y_pos * 100 + 50), 38, line_width)
			y_pos += 1
		x_pos += 1	


def check_game_over():
	global game_over
	global winner

	x_pos = 0
	for x in markers:
		#check columns
		if sum(x) == n:
			winner = 1
			game_over = True
		if sum(x) == -n:
			winner = 2
			game_over = True
		#check rows
		row_sum = sum([markers[i][x_pos] for i in range(n)])
		if row_sum == n:
			winner = 1
			game_over = True
		if row_sum == -n:
			winner = 2
			game_over = True
		x_pos += 1

	#check cross
	lcross_sum = sum([markers[i][i] for i in range(n)])
	if lcross_sum == n:
		winner = 1
		game_over = True
	if lcross_sum == -n:
		winner = 2
		game_over = True

	rcross_sum = sum([markers[i][n-i-1] for i in range(n)])
	if rcross_sum == n:
		winner = 1
		game_over = True
	if rcross_sum == -n:
		winner = 2
		game_over = True

	#check for tie
	if game_over == False:
		tie = True
		for row in markers:
			for i in row:
				if i == 0:
					tie = False
		#if it is a tie, then call game over and set winner to 0 (no one)
		if tie == True:
			game_over = True
			winner = 0

def draw_game_over(winner):

	if winner != 0:
		end_text = "Player " + str(winner) + " wins!"
	elif winner == 0:
		end_text = "You have tied!"

	end_img = font.render(end_text, True, blue)
	pygame.draw.rect(screen, green, (screen_width // 2 - 100, screen_height // 2 - 60, 200, 50))
	screen.blit(end_img, (screen_width // 2 - 100, screen_height // 2 - 50))

	again_text = 'Play Again?'
	again_img = font.render(again_text, True, blue)
	pygame.draw.rect(screen, green, again_rect)
	screen.blit(again_img, (screen_width // 2 - 80, screen_height // 2 + 10))

def isGameOver(state, n):
	matrix = []
	k=0
	for i in range(n):
		row = []
		for j in range(n):
			row.append(int(state[k]) if int(state[k]) != 2 else -1)
			k += 1
		matrix.append(row)

	x_pos = 0
	isOver = 0
	win = 0
	for x in matrix:
		#check columns
		if sum(x) == n:
			win = 1
			isOver = 1
		if sum(x) == -n:
			win = 2
			isOver = 2
		#check rows
		row_sum = sum([matrix[i][x_pos] for i in range(n)])
		if row_sum == n:
			win = 1
			isOver = 1
		if row_sum == -n:
			win = 2
			isOver = 2
		x_pos += 1

	#check cross
	lcross_sum = sum([matrix[i][i] for i in range(n)])
	if lcross_sum == n:
		win = 1
		isOver = 1
	if lcross_sum == -n:
		win = 2
		isOver = 2

	rcross_sum = sum([matrix[i][n-i-1] for i in range(n)])
	if rcross_sum == n:
		win = 1
		isOver = 1
	if rcross_sum == -n:
		win = 2
		isOver = 2

	#check for tie
	if isOver == 0:
		tie = 1
		for row in matrix:
			for i in row:
				if i == 0:
					tie = 0
		#if it is a tie, then call game over and set win to 0 (no one)
		if tie == 1:
			isOver = 1
			win = 0
		if tie == 1:
			return 3
		
	# print(state, matrix, isOver)
	return isOver

def isPlayerWon(state,n,plyr):
	p_1=0
	p_2=0
	matrix = []
	k=0
	for i in range(n):
		row = []
		for j in range(n):
			row.append(int(state[k]) if int(state[k]) != 2 else -1)
			k += 1
		matrix.append(row)

	p1=0
	p2=0

	for x in matrix:
		if sum(x) == n:
			p1 += 1
		if sum(x) == -n:
			p2 += 1
	if p1 > 1 and plyr == 1:
		return False
	if p2 > 1 and plyr == 2:
		return False
	if p1 > 0 and p2 > 0:
		return False
	
	p_1+=p1
	p_2+=p2
	
	p1=0
	p2=0
	for j in range(n):
		colsum = sum([matrix[i][j] for i in range(n)])
		if colsum == n:
			p1 += 1
		if colsum == -n:
			p2 += 1
	if p1 > 1 and plyr == 1:
		return False
	if p2 > 1 and plyr == 2:
		return False
	if p1 > 0 and p2 > 0:
		return False
	
	p_1+=p1
	p_2+=p2

	lcross_sum = sum([matrix[i][i] for i in range(n)])
	if lcross_sum == n:
		p_1 += 1
	if lcross_sum == -n:
		p_2 += 1
	
	rcross_sum = sum([matrix[i][n-i-1] for i in range(n)])
	if rcross_sum == n:
		p_1 += 1
	if rcross_sum == -n:
		p_2 += 1

	if plyr == 1 and p_2 > 0:
		return False
	if plyr == 2 and p_1 > 0:
		return False
	
	if plyr == 1 and p_1 > 0:
		return True
	if plyr == 2 and p_2 > 0:
		return True
	
	return False

# 112
# 211
# 122


def basek(num, k):
    if num == 0:
        return '0'.rjust(k*k, '0')
    nums = []
    while num:
        num, r = divmod(num, 3)
        nums.append(str(r))
    ret = ''.join(reversed(nums))
    return ret.rjust(k*k, '0')

def decimal(base_k, k):
	ans = 0
	for i in base_k:
		ans = ans * k + int(i)
	return ans

def getValidStates(n):
	valid_states = []
	for i in range(3**(n*n)):
		base_n = basek(i,n)
		# print(i, base_n)
		num_1s = base_n.count('1')
		num_2s = base_n.count('2')

		if num_1s == num_2s and isGameOver(base_n, n) == 0:
			# if isGameOver(basek(i,n), n) == 0: 
			valid_states.append(base_n)
		elif num_1s == num_2s+1 and isGameOver(base_n, n) == 3:
			valid_states.append(base_n)
		elif num_1s == num_2s and isPlayerWon(base_n,n,2):
			valid_states.append(base_n)
		elif num_1s == num_2s+1 and isPlayerWon(base_n,n,1):
			valid_states.append(base_n)
		

	return valid_states

# valid_states = getValidStates(n)

def transition_func(state, action, n):
	# index = action[0]*n + action[1]
	index = action
	next_states = []

	if(state[index] == '0' and (isGameOver(state,n) == 0)):
		st = state[:index] + '1' + state[index+1:]
		# state[index] = '1'
		if isGameOver(st,n):
			next_states.append(st)
			return next_states
		
		remaining_pos = st.count('0')
		for i in range(len(st)):
			if st[i] == '0':
				s = st[:i] + '2' + st[i+1:]
				# s[i] = '2'
				next_states.append(s)
	
	return next_states

def rewardVec(state, action, n):
	reward_vec = np.zeros((3**(n*n), 1))
	state_prob = transition_func(state,action,n)

	for i in range(len(state_prob)):
		if state_prob[i] != 0:
			if isGameOver(basek(i,n)) == 2:
				reward_vec[i] = -3
			elif isGameOver(basek(i,n)) == 3:
				reward_vec[i] = 1
		elif state_prob[i] == 1:
			reward_vec[i] = 2
			
	return reward_vec


# print(len(getValidStates(3)))

gamma = 1
policy = {}
def ValueIteration(n):
	global policy
	validStates = getValidStates(n)
	numValStates = len(validStates)
	# print(numValStates)

	indexOfState = {validStates[i]:i for i in range(numValStates)}
	policy = {x:0 for x in validStates}
	
	w = np.zeros((numValStates,1))
	
	while True:
		# print(1)
		w_old = w.copy()
		for i in range(numValStates):
			state = validStates[i]
			maxa = -100
			max_a = 0
			for a in range(n*n):
				w_i0 = 0
				if state[a] == '0' and state.count('1') == state.count('2') and (isGameOver(state,n) == 0):
					next_states = transition_func(validStates[i], a, n)
					
					for ns in next_states:
						rwd = 0
						igo = isGameOver(ns,n)
						if igo == 1:
							rwd = 2
						elif igo == 2:
							rwd = -2
						elif igo == 3:
							rwd = 1

						w_i0 += rwd + gamma*w_old[indexOfState[ns]]
					w_i0 /= len(next_states)
				# maxa = max(maxa, w_i0)
				if w_i0 > maxa:
					maxa = w_i0
					max_a = a

			w[i][0] = maxa
			policy[state] = max_a
					# reward_vec = rewardVec(state, a, n)
					# w[i][0] = max(w[i][0], np.matmul(trans_func.T, reward_vec + gamma*w_old))
		
		max_diff = 0
		for i in range(numValStates):
			max_diff = max(max_diff,abs(w[i][0] - w_old[i][0]))
		
		# print(max_diff)
		if max_diff == 0:
			print('Value Iteration Completed')
			# for x in w:
			# 	if x>0:
			# 		print(x)
			break
	# print(policy)			
	
ValueIteration(n)

#main loop
run = True
choices = [i for i in range(n*n)]
num_games = 1000

results = {0:0, 1:0, 2:0}

# '''
current_game = 0
while current_game < num_games:

    # if current_game % 100 == 0:
    #     print(f"{current_game=}")

    
    #draw board and markers first
    draw_board()
    draw_markers()

    while not game_over:

        #run new game
        if game_over == False and player == 1:
            st = ''
            # print(markers)
            for r in markers:
                for c in r:
                    st += str(c) if c != -1 else str(2)
            
            pos = policy[st]
            cell_x = int(pos / n)
            cell_y = int(pos % n)
            if markers[cell_x][cell_y] == 0:
                markers[cell_x][cell_y] = player
                choices.remove(n*cell_y + cell_x)
                player *= -1
                check_game_over()

        if game_over == False and player == -1:
            index = random.randint(0,len(choices)-1)
            pos = [int(choices[index]%n), int(choices[index]/n)]
            cell_x = pos[0]
            cell_y = pos[1]
            # print('o', cell_x, cell_y)
            if markers[cell_x][cell_y] == 0:
                markers[cell_x][cell_y] = player
                choices.remove(n*cell_y + cell_x)
                player *= -1
                check_game_over()

    #check if game has been won
    if game_over == True:
        current_game += 1
        # results.append(winner)
        results[winner] += 1
        choices = [i for i in range(n*n)]
        draw_game_over(winner)
        #reset variables
        game_over = False
        player = 1
        pos = (0,0)
        markers = []
        winner = 0
        #create empty 3 x 3 list to represent the grid
        for x in range (n):
            row = [0] * n
            markers.append(row)

    #update display
    pygame.display.update()
pygame.quit()
print('Won =', results[1])
print('Draw=', results[0])
print('Loss=', results[2])
# '''

			

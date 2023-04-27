#import modules
import pygame
from pygame.locals import *
import random

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
	cross_sum = sum([markers[i][i] for i in range(n)])
	if cross_sum == n or cross_sum == n:
		winner = 1
		game_over = True
	if cross_sum == -n or cross_sum == -n:
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


#main loop
run = True
opponent_choices = [i for i in range(n*n)]
# print(opponent_choices)

while run:

	#draw board and markers first
	draw_board()
	draw_markers()

	#handle events
	for event in pygame.event.get():
		#handle game exit
		if event.type == pygame.QUIT:
			run = False
		#run new game
		if game_over == False and player == 1:
			#check for mouseclick
			if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
				clicked = True
			if event.type == pygame.MOUSEBUTTONUP and clicked == True:
				clicked = False
				pos = pygame.mouse.get_pos()
				cell_x = pos[0] // 100
				cell_y = pos[1] // 100
				if markers[cell_x][cell_y] == 0:
					# print('p', cell_x, cell_y, n*cell_y + cell_x, opponent_choices)
					markers[cell_x][cell_y] = player
					opponent_choices.remove(n*cell_y + cell_x)
					player *= -1
					check_game_over()

		# print('p', game_over)
		if game_over == False and player == -1:
			index = random.randint(0,len(opponent_choices)-1)
			pos = [int(opponent_choices[index]%n), int(opponent_choices[index]/n)]
			cell_x = pos[0]
			cell_y = pos[1]
			# print('o', cell_x, cell_y)
			if markers[cell_x][cell_y] == 0:
				markers[cell_x][cell_y] = player
				opponent_choices.remove(n*cell_y + cell_x)
				player *= -1
				check_game_over()
		# print('o', game_over)

	#check if game has been won
	if game_over == True:
		opponent_choices = [i for i in range(n*n)]
		draw_game_over(winner)
		#check for mouseclick to see if we clicked on Play Again
		if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
			clicked = True
		if event.type == pygame.MOUSEBUTTONUP and clicked == True:
			clicked = False
			pos = pygame.mouse.get_pos()
			if again_rect.collidepoint(pos):
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
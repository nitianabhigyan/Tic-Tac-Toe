from time import sleep
import random
import pygame 
import names
from os import system


"""
	Create a simple 3x3 grid visually which matches to a 3x3 matrix (2d array)
	Create a function which checks if the grid is completed ( a player has 3 continuous characters marked.
	Create a user a and b (Multiplayer mode) 
	Create a versus Computer mode. (Computer will be 0 always.
	Create a check function i.e. veriefies if the move is legal or not. (empty place)
	0|1|2
	3|4|5
	6|7|8
	A Cross will be donated by 1 Programatically and Zero by 0.
"""

#Global variables initialization.
#colors
black = (0,0,0)
white = (255,255,255)
red = (230,0,0)
green = (124,252,0)
blue = (0,0,135)
yellow = (255,251,66)
hotpink = (255,105,180)
dark_red = (150,0,0)
dark_green = (0,102,0)
dark_orange = (255,140,0)
orange = (255, 102, 0)
x = 600
y = 600
dis_x = x+300
dis_y = y
pygame.init()
pygame.display.set_caption("Tic Tac Toe")
# font = pygame.font.SysFont('gameofthrones', 32) # font to be used.
# font = pygame.font.SysFont('parchment', 55) # font to be used.
# font = pygame.font.SysFont('bookmanoldstyle', 38) # font to be used.
# font = pygame.font.SysFont('gangofthree', 40) # font to be used.
font = pygame.font.SysFont('oldenglishtext',40) # font to be used.
smallfont = pygame.font.SysFont('monotypecorsiva', 24)  # Final
# smallfont = pygame.font.SysFont('blackadderitc', 24)
# smallfont = pygame.font.SysFont('oldenglishtext', 28)
gamescreen = pygame.display.set_mode((x,y))
gamescreen.fill(black)

GRID = [-1,-2,-3,-4,-5,-6,-7,-8,-9]  # Indexing as 0,1,2,3,4,5,6,7,8 Initialized without Cross zero
VALID_PAIRS = [(0,1,2),(0,4,8),(0,3,6),(1,4,7),(2,5,8),(2,4,6),(3,4,5),(6,7,8)]
PLAYERS = None
GAME_MODE = None
# pygame.font.get_fonts()

class Moves():  # Location, value (Player)
	def __init__(self, location, value):
		self.location = location
		self.value = value
		self.is_legal()
		
	def is_legal(self):
		if -1 <self.location < 9:
			if GRID[self.location] < 0:
				self.legal = True
			else:
				self.legal = False
		else:
			self.legal = False


class Player():  # IsComputer, name, assignment
	def __init__(self,iscomputer, name = names.get_full_name(),assign = 0):
		if iscomputer:
			self.auto = True
			self.name = name
			self.assignment = assign
		else:
			self.auto = False
			self.name = name
			self.assignment = assign


class Button():  # Color, dimensions,text,msg,Clicked color
	def __init__(self,color,dimensions,text,msg=None,clicked = None):
		if clicked is None:
			clicked = color

		self.color = color
		self.dimensions = dimensions  # [x,y,w,h]
		self.text = text
		self.clicked = clicked
		if msg is None:
			self.msg = ""
		else:
			self.msg = msg
		self.draw()  # First Draw
		
	def is_clicked(self):
		return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())
	
	def draw(self):
		self.rect = pygame.draw.rect(gamescreen, self.color,(self.dimensions[0],self.dimensions[1],self.dimensions[2],self.dimensions[3]))
		textSurf = smallfont.render(self.msg,True,white)
		gamescreen.blit(textSurf, (self.dimensions[0] + (self.dimensions[2] -smallfont.size(self.msg)[0])/2,self.dimensions[1]))
		# Text will be centrally aligned on the button. 
		# If text size > button size will raise error
		
	def change(self):
		self.rect = pygame.draw.rect(gamescreen, self.clicked,(self.dimensions[0],self.dimensions[1],self.dimensions[2],self.dimensions[3]))
		pygame.display.update()


def get_input(Text):
	pygame.display.set_caption(Text)
	name = ""
	flag = True
	while flag:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit_seq()
			elif event.type == pygame.KEYDOWN:
				if event.unicode.isalnum() or (event.key == pygame.K_SPACE):
					name+= event.unicode
				elif event.key == pygame.K_BACKSPACE:
					name = name[:-1]
				elif event.key == pygame.K_RETURN:
					flag = False
					return name
		pygame.draw.line(gamescreen,white,
		[x/2+font.size(name)[0]/2,y/2],
		[x/2+font.size(name)[0]/2,y/2+font.size(name)[1]],2)
		pygame.display.flip()
		text = font.render(Text,True, yellow)
		block = font.render(name,True, white)
		gamescreen.fill(black)
		gamescreen.blit(text,(x/2-font.size(Text)[0]/2,y/3-font.size(Text)[1]/2))
		gamescreen.blit(block, (x/2-font.size(name)[0]/2,y/2))  # Auto adjust text
		pygame.display.flip()
	

def create_player():
	# print("Entering create_player")
	global PLAYERS
	while PLAYERS is None:
		if GAME_MODE is None:
			print("Attempted to create players without specifying game mode\n Exiting")
			exit_seq()
		elif GAME_MODE == "players":
			name = get_input("Type Player 1's Name (Zero)")
			p_a = Player(False,name,0)
			name = get_input("Type Player 2's Name (Cross)")
			p_b = Player(False,name,1)
			PLAYERS = [p_a, p_b]
		
		elif GAME_MODE == "computer":
			p_a = Player(True)
			name = get_input("Enter your name")
			p_b = Player(False,name,1)
			PLAYERS = [p_a, p_b]


def set_game_mode():
	choose = font.render("Choose your mode",True,white)
	# print(choose)
	gamescreen.blit(choose,(x/2-font.size("Choose Your mode")[0]/2,y/6))  # Center aligned.
	b1 = Button(dark_green,[70,290,165,60],"computer","Versus Computer",green)
	b2 = Button(dark_red,[365,290,165,60],"players","Versus Player",red)
	pygame.display.update()
	global GAME_MODE
	while GAME_MODE is None:
		sleep(.1)
		for event in pygame.event.get():  # Needs to be removed. put in thread TBD
			if event.type == pygame.QUIT:
				exit_seq()
		if b1.is_clicked():
			b1.change()
			GAME_MODE = b1.text
			break
			
		elif b2.is_clicked():
			b2.change()
			GAME_MODE = b2.text
			break


def static_display(text,display_height,color):
    
    surface = font.render(text,True,color)
    rect = surface.get_rect()
    rect.center = ((dis_x/2),(display_height))
    gamescreen.blit(surface,rect)
    pygame.display.update()


def exit_seq():
	gamescreen = pygame.display.set_mode((dis_x,dis_y))  # Expand the screen
	for alph in range (255,0,-1):
		gamescreen.fill((alph,alph,alph))
		static_display(' .:Made By:. ',dis_y/2 - 30,(255-alph,255-alph,255-alph))
		static_display('Abhigyan Kumar',dis_y/2+ 50,(255-alph,255-alph,255-alph))
		sleep(.012)
	sleep(.2)
	pygame.quit()
	exit(0)


def make_move(move):
	if move.legal:
		if move.value == 0:  # Zero
			draw_zero(move.location)
		elif move.value == 1:  # Cross
			draw_cross(move.location)
	else:
		print("Error move is not LEGAL!")
	# In main call is_complete after making the move.


def draw_zero(location):  # Grid location
	GRID[location] = 0
	center = None
	if location == 0:
		center = (int(x/6), int(y/6))
	elif location == 1:
		center = (int(x/6 + x/3), int(y/6))
	elif location == 2:
		center = (int(x/6+ 2*x/3), int(y/6)*1)
	elif location == 3:
		center = (int(x/6), int(y/6 + y/3))
	elif location == 4:
		center = (int(x/6 + x/3), int(y/6 + y/3))
	elif location == 5:
		center = (int(x/6 + 2*x/3), int(y/6 + y/3))
	elif location == 6:
		center = (int(x/6), int(y/6 + 2*y/3))
	elif location == 7:
		center = (int(x/6 + x/3), int(y/6 + 2*y/3))
	elif location == 8:
		center = (int(x/6 + 2*x/3), int(y/6 + 2*y/3))
	
	pygame.draw.circle(gamescreen,hotpink,center,int(x/8))
	pygame.display.update()
	
	
def draw_cross(location,padding=5,color=dark_green):  # Grid location
	GRID[location] = 1
	rectangle = None
	width = x/3 - 2*padding
	height = y/3 - 2*padding
	if location == 0:
		rectangle = [padding, padding, width, height]  # left,top,width,height
	elif location == 1:
		rectangle = [x/3+padding, padding, width, height]
	elif location == 2:
		rectangle = [2*x/3+padding, padding, width, height]
	elif location == 3:
		rectangle = [padding, y/3+padding, width, height]
	elif location == 4:
		rectangle = [x/3+padding, y/3+padding, width, height]
	elif location == 5:
		rectangle = [2*x/3+padding, y/3+padding, width, height]
	elif location == 6:
		rectangle = [0+padding, 2*y/3+padding, width, height]
	elif location == 7:
		rectangle = [x/3+padding, 2*y/3+padding, width, height]
	elif location == 8:
		rectangle = [2*x/3+padding, 2*y/3+padding, width, height]
		
	pygame.draw.rect(gamescreen,color,rectangle,0)  # 0 Denotes Solid square
	pygame.display.update()
	

def draw_grid():
	width = 2
	pygame.draw.line(gamescreen,white,[x/3,0],[x/3,y],width) # khadi wali line
	pygame.draw.line(gamescreen,white,[2*x/3,0],[2*x/3,y],width)
	pygame.draw.line(gamescreen,white,[0,y/3],[x,y/3],width)
	pygame.draw.line(gamescreen,white,[0,2*y/3],[x,2*y/3],width)
	pygame.draw.rect(gamescreen,white,[0,0,x,y],1)
	pygame.display.update()
# Need to go to main screen i.e. welcome->game mode... after this


def refresh_board():
	global GRID
	GRID = [-1,-2,-3,-4,-5,-6,-7,-8,-9]
	pygame.display.set_caption("Tic Tac Toe")
	gamescreen.fill(black)
	try:
		system('cls')  # WILL WORK on windows only
	except:
		system('clear')


# Takes the grid and checks if the game is completed (a player has won).
# Returns False if nobody has won else returns the location of first completed line.
def is_complete(GRID):
	for state in VALID_PAIRS:
		if GRID[state[0]] == GRID[state[1]] == GRID[state[2]]:
			return state  # Return the state where it is found. Immediate return on first match

	flag = True
	for location in range(9):  # if all board places are fill
		if GRID[location] < 0:
			flag = False
			break
	return flag

	
def test():  # Test Bed for testing functions etc.
	move = Moves(0,1)
	# print(move,move.legal,move.location,move.value)  # For testing ONLY.
	refresh_board()
	draw_grid()
	print(GRID)
	for location in range(9):
		move = 	Moves(location,0)
		make_move(move)
		temp = is_complete(GRID)
		if temp:
			print("Won",temp)
		else:
			print("Not Yet")
		sleep(.1)
		
	print(GRID)
	sleep(1)
	refresh_board()
	draw_grid()
	for location in range(9):
		move = 	Moves(location,1)
		make_move(move)
		temp = is_complete(GRID)
		if temp:
			print("Won",temp)
		else:
			print("Not Yet")
		sleep(.1)
		
	sleep(1)
	print(GRID)
	refresh_board()	
	set_game_mode()
	create_player()
	# sleep(3)
	print("GAME_MODE in end:",GAME_MODE)
	exit_seq()
	

def prompt(text):
	width = dis_x - x
	pygame.draw.rect(gamescreen,white,[x,0,width,y],0)
	pygame.display.set_caption(text)
	box = smallfont.render(text,True,hotpink)
	gamescreen.blit(box,((dis_x+x-smallfont.size(text)[0])/2,y/2))  # Center aligned wrt small side.
	pygame.display.update()
	

def game_loop():  # Error
	turn = 0  # Player a starts.
	while not is_complete(GRID):
		location = 13  # Initialization value
		new_move = Moves(location, PLAYERS[turn].assignment)  # Test initialization.
		prompt("%s's Turn"%(PLAYERS[turn].name))
		while(not(new_move.legal)):  # Breaks when a legal move is found.
			if PLAYERS[turn].auto:
				left = [loc for loc in range(len(GRID)) if GRID[loc] <0]
				location = random.choice(left)  # From empty location in grid, pick one
				new_move = Moves(location, PLAYERS[turn].assignment)
				sleep(1)
			else:	# Human needs to make the move.
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						exit_seq()
					elif event.type == pygame.MOUSEBUTTONDOWN:
						loc_x, loc_y = pygame.mouse.get_pos()  # X,Y
						if loc_x < x/3 and loc_y < y/3:
							location = 0
						elif loc_x < 2*x/3 and loc_y < y/3:  # Don't need to check lower than as elif
							location = 1
						elif loc_x < x and loc_y < y/3:
							location = 2
						elif loc_x < x/3 and loc_y < 2*y/3:
							location = 3
						elif loc_x < 2*x/3 and loc_y < 2*y/3:
							location = 4
						elif loc_x < x and loc_y < 2*y/3:
							location = 5
						elif loc_x < x/3 and loc_y < y:
							location = 6
						elif loc_x < 2*x/3 and loc_y < y:
							location = 7
						elif loc_x < x and loc_y < y:
							location = 8
						# else:
							# print("if else :",loc_x,loc_y)
						print("Location value manual: ",location)
						#set move and go on		
					new_move = Moves(location, PLAYERS[turn].assignment)
					if new_move.legal:
						break
	
		make_move(new_move)
		# print("Turn no:",turn,PLAYERS[turn].name,PLAYERS[turn].assignment,GRID)
		turn = int((turn + 1) %2)
	# print("Done with the game. details:",is_complete(GRID),turn, PLAYERS[turn].assignment,PLAYERS[turn].name,GRID)


def declare_winner():
	temp = is_complete(GRID)
	sleep(.5)
	if temp == True:
		# print("No winner :(")
		prompt("No Winner\n Game tied :(")
	else:
		player = None
		for player in PLAYERS:
			if player.assignment == GRID[temp[0]]:
				break
		prompt("The winner is: %s"%player.name)
		temp = [temp[0-t-1] for t in range(len(temp))]  # Reverse a tuple
		for location in temp:
			draw_cross(location,0,yellow)
			sleep(.35)
		# print("The winner is: %s"%player.name,temp)
	sleep(2)

def reset_game():
	global PLAYERS, GAME_MODE
	PLAYERS = None
	GAME_MODE = None
	gamescreen = pygame.display.set_mode((x,y))
	refresh_board()


def post_game():
	choose = font.render("Do you wish to continue?",True,white)
	gamescreen.blit(choose,(x/2-font.size("Do you wish to continue?")[0]/2,y/6))
	b1 = Button(dark_green,[70,290,165,60],"exit","EXIT :(",green)
	b2 = Button(dark_red,[365,290,165,60],"continue","Play another round",red)
	b3 = Button(dark_orange,[250,420,170,60],"replay","Replay match",orange)
	pygame.display.update()
	while True:
		for event in pygame.event.get():  # Needs to be removed. put in thread TBD
			if event.type == pygame.QUIT:
				exit_seq()
	
		if b1.is_clicked():
			b1.change()
			return "exit_seq"
			break
			
		elif b2.is_clicked():
			b2.change()
			return "main"
			break
		
		elif b3.is_clicked():
			b3.change()
			return "replay"
			break


def main():
	print("Welcome")  # Welcome
	set_game_mode()  # Set game mode
	refresh_board()  # refresh the board (clean black)
	create_player()  # Create players
	gamescreen = pygame.display.set_mode((dis_x,dis_y))  # Expand the screen
	static_display(PLAYERS[0].name+" VS "+PLAYERS[1].name,y/3,white)
	sleep(2)
	refresh_board()  # Clear the board
	draw_grid()  # Draw the grid
	
	game_loop()  # The actual game loop as per game mode.
	declare_winner()
	refresh_board()
	return_val = post_game()
	global GAME_MODE
	if return_val == "main":
		reset_game()
		main()
	elif return_val == "replay":
		main()
	else:
		exit_seq()

# test()  # For testing ONLY.
reset_game()
main()
import pygame
import random
import sys
from os import path

img_dir = path.join(path.dirname(__file__), 'img')


WIDTH = 626
HEIGHT = 626
PLAYER_COLOUR = (255, 0, 0)
ENEMY_COLOUR = (0,255,0)
BACKGROUND_COLOUR = (0,0,0)
FONT_COLOUR = (0,0,0)
FPS = 27

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #create a screen
pygame.display.set_caption("Lamar's Game")
clock = pygame.time.Clock()

player_size = 32
player_speed = 15
player_pos = [WIDTH/2, HEIGHT-2*player_size, 3] # x coordinate for starting rectangle
player_x = WIDTH/2
player_y = HEIGHT - (2 * player_size)

# image setup

left = False
right = False
up = False
down = False
walkCount = 0
sheild = False


enemy_speed = 0
enemy_size = 50
enemy_pos = [random.randint(0, WIDTH-enemy_size), 0] #use random.randomint to randomly assign a position for the enemy
enemy_list = [enemy_pos]


trophy_size = 0
trophy_pos = [random.randint(0, WIDTH-trophy_size), random.randint(0, HEIGHT - trophy_size)]
trophy_list = [trophy_pos]
trophy_speed = 5
trophy = 0

score = 0
running = True
gameover = False

font = pygame.font.SysFont("monospace", 35)

#Load game graphics

background = pygame.image.load(path.join(img_dir, "winter-landscape.jpg")).convert()
background_rect = background.get_rect()

player_img = pygame.image.load(path.join(img_dir, "square-penguin-copy.png"))
player_rect = player_img.get_rect()

trophy_img = pygame.image.load(path.join(img_dir, "circle-giraffe-copy.png"))
trophy_rect = player_img.get_rect()

enemy_img = pygame.image.load(path.join(img_dir, "zombie-copy.png"))
enemy_rect = enemy_img.get_rect()


class Trophy(pygame.sprite.Sprite):
    def __init__(self, color, x, y, player = None):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([20, 20])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass


def draw_window():
	global walkCount
	screen.fill(BACKGROUND_COLOUR)
	screen.blit(background, background_rect)

	if walkCount + 1 >= 27:
		walkCount = 0

	if left or right or up or down:
		screen.blit(player_img, (player_pos[0], player_pos[1]))
		#pygame.draw.rect(screen, (255, 255, 255), (player_pos[0], player_pos[1], player_size, player_size))

		walkCount += 1

	else:
		screen.blit(player_img, (player_pos[0], player_pos[1]))

		#screen.blit(player_img, (player_x, player_y))


def show_game_over_screen():
	draw_text(screen, "GAME OVER!", 64, WIDTH /2, HEIGHT / 2)
	pygame.display.flip()
	clock.tick(10)


def set_level(score, enemy_speed):

	if score < 20:
		enemy_speed = 3

	elif score < 30:
		enemy_speed = 5

	elif score < 40:
		enemy_speed = 7

	elif score < 70:
		enemy_speed = 9

	elif score < 100:
		enemy_speed = 11

	elif score < 150:
		enemy_speed = 13

	else:
		enemy_speed = 15
	
	return enemy_speed


def drop_enemies(enemy_list):

	delay = random.random() #generates number from 0 to 1

	if len(enemy_list) < 7 and delay < 0.1: #keep adding enemies until 10 are on screen
		x_pos = random.randrange(0, WIDTH-enemy_size) #generate new enemy position on top of screen
		y_pos = 0
		enemy_list.append([x_pos, y_pos])

def draw_enemies(enemy_list):

	for enemy_pos in enemy_list:
		screen.blit(enemy_img, (enemy_pos[0], enemy_pos[1]))



def update_enemy_pos(enemy_list, score):
	
	for index, enemy_pos in enumerate(enemy_list):
		if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT: #enemy is on screen
				enemy_pos[1] += enemy_speed #drop enemy by speed
		else:
			enemy_list.pop(index)
			score += 1
	return score

def collision_check(enemy_list, player_pos):

	for enemy_pos in enemy_list:
		if detect_collision(player_pos, enemy_pos):
			return True

	return False

def detect_collision(player_pos, enemy_pos):

	p_x = player_pos[0]
	p_y = player_pos[1]


	e_x = enemy_pos[0]
	e_y = enemy_pos[1]

	#x-coordinate of enemy will overlap player x-coordinate

	if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
		if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
			return True


	return False



#will loop while game is in use to run all the code below
while not gameover:

	#loop will track all key events
	for event in pygame.event.get():
		# to allow screen to close when you hit exit button
		if event.type == pygame.QUIT:
			sys.exit()


	x = player_pos[0]
	y = player_pos[1]
	l = player_pos[2]


	keys = pygame.key.get_pressed()

	if keys[pygame.K_LEFT] and x > player_speed:
		x -= player_speed
		left = True
		right = False
		up = False
		down = False
	if keys[pygame.K_RIGHT] and x < WIDTH - player_size - player_speed:
		x += player_speed
		right = True
		left = False
		up = False
		down = False
	# if keys[pygame.K_UP] and y < HEIGHT - player_size - player_speed:
	# 	y -= player_speed
	# 	up = True
	# 	down = False
	# 	left = False
	# 	right = False
	# if keys[pygame.K_DOWN] and y > player_speed:
	# 	y += player_speed
	# 	down = True
	# 	up = False
	# 	left = False
	# 	right = False
	if keys[pygame.K_UP]:#event.key == pygame.K_UP:
		if y - player_size < 0:
			y = 0 
		else:
			y -= player_speed
	if keys[pygame.K_DOWN]:#event.key == pygame.K_DOWN:
		if y + player_size >= HEIGHT:
			y = HEIGHT - player_size
		else:
			y += player_speed
	# else:
	# 	right = False
	# 	left = False
	# 	down = False
	# 	up = False
	# 	walkCount = 0

	player_pos = [x, y, l]


	# this resets the screen background each time the loop runs, allowing a new rectangle to be drawn
	draw_window()
	
	drop_enemies(enemy_list)
	score = update_enemy_pos(enemy_list, score) #score is integer ie. immutable value so must pass it to change
	enemy_speed = set_level(score, enemy_speed)

	# place_trophies(trophy_list, score)
	#update_trophy_pos(trophy_list)

	text = "Score:" + str(score)
	label = font.render(text, 1, FONT_COLOUR)
	screen.blit(label, (WIDTH-200, HEIGHT-40))

	
	# if trophy_check(trophy_list, player_pos):
	# 	trophy += 5

	# text_lives = "Trophy:" + str(trophy)
	# label_lives = font.render(text_lives, 1, FONT_COLOUR)
	# screen.blit(label_lives, (WIDTH-200, HEIGHT-80))

	if collision_check(enemy_list, player_pos):
		gameover = True
		break		

	draw_enemies(enemy_list)
	#draw_trophies(trophy_list)

	#update screen every iteration so you can see the visualizations
	clock.tick(FPS)
	pygame.display.update()


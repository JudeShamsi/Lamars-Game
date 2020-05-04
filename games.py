import pygame
import random
import sys



WIDTH = 800
HEIGHT = 600
PLAYER_COLOUR = (255, 0, 0)
ENEMY_COLOUR = (0,255,0)
BACKGROUND_COLOUR = (0,0,0)
FONT_COLOUR = (255,255,0)
FPS = 40

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #create a screen
pygame.display.set_caption("Toilet Paper Frenzy")
clock = pygame.time.Clock()

player_size = 50
player_speed = 40
player_pos = [WIDTH/2, HEIGHT-2*player_size] # x coordinate for starting rectangle


enemy_speed = 10
enemy_size = 50
enemy_pos = [random.randint(0, WIDTH-enemy_size), 0] #use random.randomint to randomly assign a position for the enemy
enemy_list = [enemy_pos]

score = 0
running = True
gameover = False

font = pygame.font.SysFont("monospace", 35)

class ToiletPaper(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image =  pygame.Surface((50, 40))
		self.image.fill((0, 255, 0))
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH / 2
		self.rect.centery = HEIGHT - 10
		self.speedx = 0

	def update(self):
		self.rect.x += self.speedx

all_sprites = pygame.sprite.Group()
toilet_paper = ToiletPaper()
all_sprites.add(toilet_paper)



def show_game_over_screen():
	draw_text(screen, "GAME OVER!", 64, WIDTH /2, HEIGHT / 2)
	pygame.display.flip()
	clock.tick(10)


def set_level(score, enemy_speed):

	if score < 20:
		enemy_speed = 1

	elif score < 40:
		enemy_speed = 2
	else: 
		enemy_speed = 3
	
	return enemy_speed

def drop_enemies(enemy_list):

	delay = random.random() #generates number from 0 to 1

	if len(enemy_list) < 10 and delay < 0.1: #keep adding enemies until 10 are on screen
		x_pos = random.randint(0, WIDTH-enemy_size) #generate new enemy position on top of screen
		y_pos = 0
		enemy_list.append([x_pos, y_pos])

def draw_enemies(enemy_list):

	for enemy_pos in enemy_list:
		pygame.draw.rect(screen, ENEMY_COLOUR, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))


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
while running:

	#loop will track all key events
	for event in pygame.event.get():
		# to allow screen to close when you hit exit button
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.KEYDOWN:

			x = player_pos[0]
			y = player_pos[1]

			if event.key == pygame.K_LEFT:
				if x - player_size < 0:
					x = 0
				else:
					x -= player_speed					
			if event.key == pygame.K_RIGHT:
				if x + player_size >= WIDTH:
					x = WIDTH - player_size
				else:
					x += player_speed
			if event.key == pygame.K_UP:
				if y - player_size < 0:
					y = 0 
				else:
					y -= player_speed
			if event.key == pygame.K_DOWN:
				if y + player_size >= HEIGHT:
					y = HEIGHT - player_size
				else:
					y += player_speed
			

			player_pos = [x,y]


	# all_sprites.update()

	# this resets the screen background each time the loop runs, allowing a new rectangle to be drawn
	screen.fill(BACKGROUND_COLOUR)
	# all_sprites.draw(screen)
	# pygame.display.flip()



	drop_enemies(enemy_list)
	score = update_enemy_pos(enemy_list, score) #score is integer ie. immutable value so must pass it to change
	enemy_speed = set_level(score, enemy_speed)
	
	text = "Score:" + str(score)
	label = font.render(text, 1, FONT_COLOUR)
	screen.blit(label, (WIDTH-200, HEIGHT-40))

	if collision_check(enemy_list, player_pos):
		gameover = True
		running = False
		break
		

	draw_enemies(enemy_list)

	pygame.draw.rect(screen, PLAYER_COLOUR, (player_pos[0], player_pos[1], player_size, player_size))

	#update screen every iteration so you can see the visualizations

	clock.tick(FPS)


	pygame.display.update()




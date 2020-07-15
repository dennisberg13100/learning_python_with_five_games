import math 
import random 
import pygame 
import tkinter as tk 
from tkinter import messagebox

class cube(object):
	rows = 20
	w = 500

	def __init__(self, start,dirnx=1, dirny=0, color=(255, 0, 0)):
		self.pos = start
		self.dirnx = 1
		self.dirny = 0
		self.color = color

	def move(self, dirnx, dirny):
		self.dirnx = dirnx
		self.dirny = dirny
		self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

	def draw(self, surface, eyes=False):
		dis = self.w // self.rows 
		i = self.pos[0]
		j = self.pos[1]

		pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
		if eyes:
			center = dis // 2
			radius = 3
			CircleMiddle = (i*dis+center-radius, j*dis+8)
			CircleMiddle2 = (i*dis+dis-radius*2, j*dis+8)
			pygame.draw.circle(surface, (0,0,0), CircleMiddle, radius)
			pygame.draw.circle(surface, (0,0,0), CircleMiddle2, radius)

class snake(object):
	body = []
	turns = {}
	def __init__(self, color, pos):
		self.color = color
		self.head = cube(pos)
		self.body.append(self.head)
		# This two values can be 0, 1 or -1, and show the direction in which de snake moves 
		self.dirnx = 0 
		self.dirny = 1

	def move(self):
		for event in pygame.event.get():
			# Just to garanty that we can quit the game 
			if event.type == pygame.QUIT:
				pygame.quit()

			keys = pygame.key.get_pressed()

			# Check if we changed to any direction before we move
			for key in keys:
				if keys[pygame.K_LEFT]:
					self.dirnx = -1 
					self.dirny = 0
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

				elif keys[pygame.K_RIGHT]:
					self.dirnx = 1 
					self.dirny = 0
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

				elif keys[pygame.K_UP]:
					self.dirnx = 0
					self.dirny = -1
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

				elif keys[pygame.K_DOWN]:
					self.dirnx = 0
					self.dirny = 1
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

		for i, c in enumerate(self.body):
			p = c.pos[:]

			# Not even the theacher knows what he is doing here 
			if p in self.turns:
				turn = self.turns[p]
				c.move(turn[0], turn[1])
				if i == len(self.body)-1:
					self.turns.pop(p)
			else:
				# Here we check if the snake went out of the screen on each direction 
				if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows - 1, c.pos[1]) 
				elif c.dirnx == 1 and c.pos[0] >= c.rows - 1: c.pos = (0, c.pos[1])
				elif c.dirny == 1 and c.pos[1] >= c.rows - 1: c.pos = (c.pos[0], 0)
				elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], c.rows - 1)
				else: c.move(c.dirnx, c.dirny)


	def reset(self, pos):
		self.head = cube(pos)
		self.body = []
		self.body.append(self.head)
		self.turns = {}
		self.dirnx = 1
		self.dirny = 0


	def addCube(self):
		tail = self.body[-1] # With a negative one we gat the last number of the list 
		dx, dy = tail.dirnx, tail.dirny

		if dx == 1 and dy == 0:
			self.body.append(cube((tail.pos[0] -1, tail.pos[1])))
		elif dx == -1 and dy == 0:
			self.body.append(cube((tail.pos[0] +1, tail.pos[1])))
		elif dx == 0 and dy == 1:
			self.body.append(cube((tail.pos[0], tail.pos[1] -1)))
		elif dx == 0 and dy == -1:
			self.body.append(cube((tail.pos[0], tail.pos[1] +1)))

		self.body[-1].dirnx = dx
		self.body[-1].dirny = dy

	def draw(self, surface):
		for i, c in enumerate(self.body):
			# If it's the first cube we draw the eyes 
			if i == 0:
				c.draw(surface, True)
			else: 
				c.draw(surface)


def drawGrid(width, rows, surface):
	size_between = width // rows

	x = 0
	y = 0 

	for row in range(rows):
		x += size_between
		y += size_between
		pygame.draw.line(surface, (225, 225, 225), (x, 0), (x, width))
		pygame.draw.line(surface, (225, 225, 225), (0, y), (width, y))

def redrawWindow(surface):
	global rows, width, s, snack
	surface.fill((0, 0, 0))
	s.draw(surface)
	snack.draw(surface)
	drawGrid(width, rows, surface)
	
	pygame.display.update()

def randomSnack(rows, item):
	positions = item.body

	while True: 
		x = random.randrange(rows)
		y = random.randrange(rows)

		# this crazy function goes trough all the snake positions so that we don't put the food on the same place as teh snake 
		if len(list(filter(lambda z:z.pos == (x,y), positions ))) > 0:
			continue
		else:
			break

	return (x,y)

def message_box(subject, conttent):
	root = tk.Tk()
	root.attributes("-topmost", True)
	root.withdraw()
	messagebox.showinfo(subject, conttent)
	try: 
		root.destroy()
	except:
		pass

def main():
	global rows, width, s, snack
	width = 500
	height = width #the screen is square, so height and width are the same. I kept both so that its clear what I'm doing 
	rows = 20
	win = pygame.display.set_mode((width, height))
	s = snake((255, 0, 0), (10, 10)) # First argument is the color of the snake (red) and the second the initial position (center)
	snack = cube(randomSnack(rows, s), color=(0,255,0))
	flag = True
	clock = pygame.time.Clock() # The game runs at max speed of 10 frames per second

	while flag:
		pygame.time.delay(50)
		clock.tick(10)
		s.move()

		# Check if the snake eat the snack
		if s.body[0].pos == snack.pos:
			s.addCube()
			snack = cube(randomSnack(rows, s), color=(0,255,0))

		#Check if the snake toughed his own body
		for x in range(len(s.body)):
			if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
				print("Score: ", len(s.body))
				message_box("You Lost", "Play again...")
				s.reste((10,10))
				break


		redrawWindow(win)


	pass

main()

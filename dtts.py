import pygame
import math

pygame.init()

white = (255,255,255)
black = (0,0,0)
gray = (198, 198, 198)
red = (255,0,0)
cyan = (0,255,255)
res_x = 800
res_y = 600
fps = 60

gameDisplay = pygame.display.set_mode((res_x, res_y))
pygame.display.set_caption('don\'t touch the sides')
clock = pygame.time.Clock()

class Entity(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		
class Ship(Entity):
	def __init__(self, pos_x, pos_y):
		Entity.__init__(self)
		self.ship_size = 16
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.vel_x = 0.0
		self.vel_y = 0.0
		self.accel_x = 0.0
		self.accel_y = 0.0
		self.mass = 3
		self.trail = [[pos_x, pos_y]]
		self.trail_len = 20
		self.hitbox = pygame.Rect(self.pos_x-self.ship_size/2, self.pos_y-self.ship_size/2, self.ship_size, self.ship_size)

	def update(self, lkey, rkey, ukey, dkey):
		self.accel_x = int(rkey) - int(lkey)
		self.accel_y = int(dkey) - int(ukey)
		self.vel_x += self.accel_x/self.mass
		self.vel_y += self.accel_y/self.mass
		self.pos_x += self.vel_x
		self.pos_y += self.vel_y
		self.hitbox.center = (self.pos_x, self.pos_y)
		self.trail.append([self.pos_x, self.pos_y])
		if len(self.trail) > self.trail_len:
			del self.trail[0]
	
	def collide(self, walls):
		for w in walls:
			if w.hitbox.colliderect(self.hitbox):
				gameLoop()
	
	def draw(self):
		pygame.draw.lines(gameDisplay, white, False, self.trail)
		drawShip(self.pos_x, self.pos_y, self.accel_x, self.accel_y, self.ship_size)

class Wall(Entity):
	def __init__(self, x, y, wid, hi):
		Entity.__init__(self)
		self.x = x
		self.y = y
		self.wid = wid
		self.hi = hi
		self.hitbox = pygame.Rect(x, y, wid, hi)
	
	def draw(self):
		pygame.draw.rect(gameDisplay, gray, [self.x, self.y, self.wid, self.hi])

class Door(Entity):
	def __init__(self, x, y, wid, hi, color):
		Entity.__init__(self)
		self.x = x
		self.y = y
		self.wid = wid
		self.hi = hi
		self.hitbox = pygame.Rect(x, y, wid, hi)
		self.color = color
		self.opened = False
		
	def draw(self):
		if not self.opened:
			pygame.draw.rect(gameDisplay, color, [self.x, self.y, self.wid, self.hi])
		else:
			pygame.draw.rect(gameDisplay, color, [self.x, self.y, self.wid, self.hi], 1)
	
class Switch(Entity):
	def __init__(self, x, y, wid, hi, color):
		Entity.__init__(self)
		self.x = x
		self.y = y
		self.wid = wid
		self.hi = hi
		self.hitbox = pygame.Rect(x, y, wid, hi)
		self.color = color
		self.flipped = False

	def draw(self):
		if not self.flipped:
			pygame.draw.rect(gameDisplay, color, [self.x, self.y, self.wid, self.hi])
		else:
			pygame.draw.rect(gameDisplay, color, [self.x, self.y, self.wid, self.hi], 1)
		
class Scene(object):
	def __init__(self):
		pass
		
	def render(self, gameDisplay):
		raise NotImplementedError
		
	def update(self):
		raise NotImplementedError
		
	def handle_events(self, events):
		raise NotImplementedError
		
class Level(object):
	def __init__(self, levelimg):
		self.walls = []
		self.doors = []
		self.switches = []
		self.entities = pygame.sprite.Group()
		self.tiles = loadLevel(levelimg)
		
class GameScene(Scene):
	def __init__(self):
		super(GameScene, self).__init__()
		level = 0
		lkey = False
		rkey = False
		ukey = False
		dkey = False
		
		self.entities = pygame.sprite.Group()
		self.walls = []
		
		x = 0
		y = 8
		
		if level == 0:
			level = [
				"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
				"W                                                W",
				"W                                                W",
				"W                                                W",
				"W                                                W",
				"W                                                W",
				"W                                                W",
				"W               WWWWWWWWWWWWWWWWWWWW             W",
				"W               W                  W             W",
				"W               W                  W             W",
				"W               W                  W             W",
				"W               W                  W             W",
				"W               W                  W             W",
				"W               W                  W             W",
				"W               W                  W             W",
				"WWWWWWWWWWWWWWWWW                  WWWWWWWWWWWWWWW",
				"W                                                W",
				"W                                                W",
				"W     S                                          W",
				"W                                                W",
				"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
				"W                                                W",
				"W                                                W",
				"W                                                W",
				"W                                                W",
				"W                                                W",
				"W                                                W",
				"W                                                W",
				"W                                                W",
				"W                                   W            W",
				"W                                                W",
				"W                                                W",
				"W                                                W",
				"W                                                W",
				"W                                                W",
				"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",]
		level_width = len(level[0])*16
		level_height = len(level)*16
		
		for row in level:
			for col in row:
				if col == "S":
					self.ship = Ship(x, y)
				elif col == "W":
					w = Wall(x, y, 16, 16)
					self.walls.append(w)
					self.entities.add(w)
				x += 16
			y += 16
			x = 0
			
		self.entities.add(self.ship)
	
	def render(self):
		gameDisplay.fill(black)
		for w in self.walls:
			w.draw()
		self.ship.draw()
		
	def update(self):
		pressed = pygame.key.get_pressed()
		lkey, rkey, ukey, dkey = [pressed[key] for key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)]
		self.ship.update(lkey, rkey, ukey, dkey)
		self.ship.collide(self.walls)
		
	def handle_events(self, events):
		for e in events:
			if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
				pass
				
def loadLevel(levelimg):
	pass

def drawShip(pos_x, pos_y, accel_x, accel_y, ship_size):
	if accel_x > 0:
		pos_plume_x_x = pos_x-ship_size/2
	elif accel_x < 0:
		pos_plume_x_x = pos_x+ship_size/2
	else:
		pos_plume_x_x = pos_x
	pos_plume_x_y = pos_y-ship_size/4
	
	if accel_y > 0:
		pos_plume_y_y = pos_y-ship_size/2
	elif accel_y < 0:
		pos_plume_y_y = pos_y+ship_size/2
	else:
		pos_plume_y_y = pos_y
	pos_plume_y_x = pos_x-ship_size/4
	
	l_plume_x = -accel_x*ship_size/2
	w_plume_x = ship_size/2
	l_plume_y = -accel_y*ship_size/2
	w_plume_y = ship_size/2
	
	pygame.draw.rect(gameDisplay, cyan, [pos_plume_x_x, pos_plume_x_y, l_plume_x, w_plume_x])
	pygame.draw.rect(gameDisplay, cyan, [pos_plume_y_x, pos_plume_y_y, w_plume_y, l_plume_y])
	pygame.draw.rect(gameDisplay, white, [pos_x-ship_size/4, pos_y-ship_size/2, ship_size/2, ship_size])
	pygame.draw.rect(gameDisplay, white, [pos_x-ship_size/2, pos_y-ship_size/4, ship_size, ship_size/2])
	
def gameLoop():
	gameExit = False
	
	scene = GameScene()
	
	while not gameExit:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameExit = True
		
		scene.handle_events(pygame.event.get())
		scene.update()
		scene.render()
		pygame.display.update()
		clock.tick(fps)
		
	pygame.quit()
	quit()
	
gameLoop()

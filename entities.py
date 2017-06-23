import pygame
import math
import text
import random
from globals import *

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
		self.max_accel = 1
		self.trail = [[pos_x, pos_y]]
		self.trail_len = 20
		self.hitbox = pygame.Rect(self.pos_x-self.ship_size/2, self.pos_y-self.ship_size/2, self.ship_size, self.ship_size)

	def update(self, lkey, rkey, ukey, dkey, spacebar):
		if not spacebar:
			self.accel_x = self.max_accel*(int(rkey) - int(lkey))
			self.accel_y = self.max_accel*(int(dkey) - int(ukey))
		else:
			self.accel_x = -self.vel_x
			self.accel_y = -self.vel_y
			scale = self.max_accel/2
			if abs(self.accel_x) > self.max_accel:
				scale = abs(self.accel_x)
			elif abs(self.accel_y) > self.max_accel:
				scale = abs(self.accel_y)
			self.accel_x *= self.max_accel/scale
			self.accel_y *= self.max_accel/scale
			# print ('acceleration: ({0},{1}); velocity: ({2},{3})'.format(self.accel_x, self.accel_y, self.vel_x, self.vel_y))
		self.vel_x += self.accel_x/self.mass
		self.vel_y += self.accel_y/self.mass
		if abs(self.vel_x) < 0.05:
			self.vel_x = 0
		if abs(self.vel_y) < 0.05:
			self.vel_y = 0
		
		self.pos_x += self.vel_x
		self.pos_y += self.vel_y
		self.hitbox.center = (self.pos_x, self.pos_y)
		self.trail.append([self.pos_x, self.pos_y])
		if len(self.trail) > self.trail_len:
			del self.trail[0]
	
	def collide(self, walls):
		for w in walls:
			if w.hitbox.colliderect(self.hitbox):
				if w.color == white:
					return True
				elif w.color == red or w.color == blue:
					if w.opened == False:
						return True
	
	def switchCheck(self, switches):
		for s in switches:
			if s.hitbox.colliderect(self.hitbox):
				if s.color == red or s.color == blue:
					s.flipped = True
	
	def draw(self):
		if len(self.trail) > 1:
			pygame.draw.lines(gameDisplay, white, False, self.trail)
		drawShip(self.pos_x, self.pos_y, self.accel_x, self.accel_y, self.ship_size)

class Wall(Entity):
	def __init__(self, x, y, wid, hi):
		Entity.__init__(self)
		self.x = x
		self.y = y
		self.wid = wid
		self.hi = hi
		self.color = white
		self.hitbox = pygame.Rect(x, y, wid, hi)
		self.leftline = False
		self.rightline = False
		self.upline = False
		self.downline = False
		self.upleft = False
		self.upright = False
		self.downleft = False
		self.downright = False
	
	def draw(self, ship_xy):
		#pygame.draw.rect(gameDisplay, self.color, [self.x, self.y, self.wid, self.hi])
		diff_x = ship_xy[0] - self.x
		diff_y = ship_xy[1] - self.y
		diff_x *= diff_x
		diff_y *= diff_y
		#thickness = int(40000/(diff_x+diff_y))
		thickness = 2
		if thickness > 8:
			thickness = 8
		if self.leftline:
			gameDisplay.fill(white, pygame.Rect([self.x, self.y, thickness, self.hi]))
		if self.rightline:
			gameDisplay.fill(white, pygame.Rect([self.x+self.wid-thickness, self.y, thickness, self.hi]))
		if self.upline:
			gameDisplay.fill(white, pygame.Rect([self.x, self.y, self.wid, thickness]))
		if self.downline:
			gameDisplay.fill(white, pygame.Rect([self.x, self.y+self.hi-thickness, self.wid, thickness]))
		if self.upleft:
			gameDisplay.fill(white, pygame.Rect([self.x, self.y, thickness, thickness]))
		if self.upright:
			gameDisplay.fill(white, pygame.Rect([self.x+self.wid-thickness, self.y, thickness, thickness]))
		if self.downleft:
			gameDisplay.fill(white, pygame.Rect([self.x, self.y+self.hi-thickness, thickness, thickness]))
		if self.downright:
			gameDisplay.fill(white, pygame.Rect([self.x+self.wid-thickness, self.y+self.hi-thickness, thickness, thickness]))

		
# doors work as follows:
# - blue doors are tied to blue switches. flip all the blue switches to open all the blue doors
# - red doors work the same as blue doors, except with red switches
# - yellow doors alternate between open and closed on a timer. They can start open or closed, and alternate in turn
# - green doors and magenta doors are paired. Hit a green switch to open all green doors and close all magenta doors. 
#    hit a magenta switch to do the opposite. if you hit a green switch, it disables all green switches and enables 
#    all magenta switches, and vice versa. magenta doors start open, and green doors start closed

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
			pygame.draw.rect(gameDisplay, self.color, [self.x, self.y, self.wid, self.hi])
		else:
			pygame.draw.rect(gameDisplay, self.color, [self.x, self.y, self.wid, self.hi], 1)
	
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
		self.font = pygame.font.SysFont('Arial Black', 14)

	def draw(self):
		if not self.flipped:
			pygame.draw.rect(gameDisplay, self.color, [self.x, self.y, self.wid, self.hi])
		else:
			pygame.draw.rect(gameDisplay, self.color, [self.x, self.y, self.wid, self.hi], 1)
		switchtext = self.font.render('!', True, white)
		gameDisplay.blit(switchtext, (self.x+5+int(self.color == blue), self.y-3))
		
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
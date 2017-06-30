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
		self.is_accel = False

	def update(self, lkey, rkey, ukey, dkey, spacebar):
		if not spacebar:
			self.accel_x = self.max_accel*(int(rkey) - int(lkey))
			self.accel_y = self.max_accel*(int(dkey) - int(ukey))
		else:
			self.accel_x = -self.vel_x
			self.accel_y = -self.vel_y
			scale = self.max_accel
			if abs(self.accel_x) > self.max_accel:
				scale = abs(self.accel_x)
			elif abs(self.accel_y) > self.max_accel:
				scale = abs(self.accel_y)
			self.accel_x *= self.max_accel/scale
			self.accel_y *= self.max_accel/scale
			# print ('acceleration: ({0},{1}); velocity: ({2},{3})'.format(self.accel_x, self.accel_y, self.vel_x, self.vel_y))
		if self.accel_x != 0 or self.accel_y != 0:
			self.is_accel = True
		else:
			self.is_accel = False
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
				if w.color == white or w.color == black:
					return True
				else:
					if w.opened == False:
						return True
	
	def switchCheck(self, switches):
		for s in switches:
			if s.hitbox.colliderect(self.hitbox):
				s.flipped = True
				if s.color == green:
					return [True, True]
				elif s.color == magenta:
					return [True, False]

		return [False, False]
	
	def draw(self, framecount = 16):
		if framecount > 15:
			if len(self.trail) > 1:
				pygame.draw.lines(gameDisplay, white, False, self.trail)
			drawShip(self.pos_x, self.pos_y, self.accel_x, self.accel_y, self.ship_size)
		else:
			drawSpawnShip(self.pos_x, self.pos_y, self.ship_size, framecount)

class Wall(Entity):
	def __init__(self, x, y, wid, hi, color):
		Entity.__init__(self)
		self.x = x
		self.y = y
		self.wid = wid
		self.hi = hi
		self.color = color
		self.ghost = False
		self.rayhit = False
		
		# defines the wall's hitbox. If the wall is on an edge in the x direction,
		# increase its width to prevent clipping out of bounds (it shouldn't be 
		# possible to build up enough speed in the y direction to clip oob, but
		# we'll see
		
		if self.x == tilesize:
			self.hitbox = pygame.Rect(x-3*tilesize, y, wid+2*tilesize, hi)
		elif self.x == res_x-3*tilesize:
			self.hitbox = pygame.Rect(x, y, wid+2*tilesize, hi)
		else:
			self.hitbox = pygame.Rect(x, y, wid, hi)
		self.leftline = False
		self.rightline = False
		self.upline = False
		self.downline = False
		self.upleft = False
		self.upright = False
		self.downleft = False
		self.downright = False
	
	def draw(self, ship):
		# if the wall's color is set to white, it draws the walls with a regular white outline.
		# otherwise, it draws the walls with a "ghost" effect
		if not self.ghost:
			wallcolor = self.color
			if self.rayhit and (ship.accel_x != 0 or ship.accel_y != 0):
				diff_x = ship.pos_x - self.x
				diff_y = ship.pos_y - self.y
				diff_x *= diff_x
				diff_y *= diff_y
				radscale = 20000*math.sqrt(ship.accel_x*ship.accel_x+ship.accel_y*ship.accel_y)
				dist = (diff_x + diff_y)
				if dist < 2*radscale+radscale*dither.bayer8x8[int(self.y/2)%8][int(self.x/2)%8]:
					wallcolor = cyan
			thickness = 2
			if self.leftline:
				gameDisplay.fill(wallcolor, [self.x, self.y, thickness, self.hi])
			if self.rightline:
				gameDisplay.fill(wallcolor, [self.x+self.wid-thickness, self.y, thickness, self.hi])
			if self.upline:
				gameDisplay.fill(wallcolor, [self.x, self.y, self.wid, thickness])
			if self.downline:
				gameDisplay.fill(wallcolor, [self.x, self.y+self.hi-thickness, self.wid, thickness])
			if self.upleft:
				gameDisplay.fill(wallcolor, [self.x, self.y, thickness, thickness])
			if self.upright:
				gameDisplay.fill(wallcolor, [self.x+self.wid-thickness, self.y, thickness, thickness])
			if self.downleft:
				gameDisplay.fill(wallcolor, [self.x, self.y+self.hi-thickness, thickness, thickness])
			if self.downright:
				gameDisplay.fill(wallcolor, [self.x+self.wid-thickness, self.y+self.hi-thickness, thickness, thickness])
		else:
			thickscale = 40000
			diff_x1 = ship_xy[0] - self.x
			diff_y1 = ship_xy[1] - self.y
			diff_x2 = ship_xy[0] - self.x - int(self.wid/2)
			diff_y2 = ship_xy[1] - self.y - int(self.hi/2)
			diff_x1 *= diff_x1
			diff_y1 *= diff_y1
			diff_x2 *= diff_x2
			diff_y2 *= diff_y2
			
			# we don't need to divide if we know it'll be zero, so if/else statements to save CPU load
			if diff_x1 + diff_y1 + 1 > thickscale:
				thickness_ul = 0
			else:
				thickness_ul = int(thickscale/(diff_x1+diff_y1+1))
				
			if diff_x2 + diff_y1 + 1 > thickscale:
				thickness_ur = 0
			else:
				thickness_ur = int(thickscale/(diff_x2+diff_y1+1))
				
			if diff_x1 + diff_y2 + 1 > thickscale:
				thickness_dl = 0
			else:
				thickness_dl = int(thickscale/(diff_x1+diff_y2+1))
				
			if diff_x2 + diff_y2 + 1 > thickscale:
				thickness_dr = 0
			else:
				thickness_dr = int(thickscale/(diff_x2+diff_y2+1))
			
			max_thickness = 15
			if thickness_ul > max_thickness:
				thickness_ul = max_thickness		
			if thickness_ur > max_thickness:
				thickness_ur = max_thickness		
			if thickness_dl > max_thickness:
				thickness_dl = max_thickness		
			if thickness_dr > max_thickness:
				thickness_dr = max_thickness
			
			if self.leftline:
				gameDisplay.fill(white, [self.x, self.y, thickness_ul, self.hi/2])
				gameDisplay.fill(white, [self.x, self.y+self.hi/2, thickness_dl, self.hi/2])
			if self.rightline:
				gameDisplay.fill(white, [self.x+self.wid-thickness_ur, self.y, thickness_ur, self.hi/2])
				gameDisplay.fill(white, [self.x+self.wid-thickness_dr, self.y+self.hi/2, thickness_dr, self.hi/2])
			if self.upline:
				gameDisplay.fill(white, [self.x, self.y, self.wid/2, thickness_ul])
				gameDisplay.fill(white, [self.x+self.wid/2, self.y, self.wid/2, thickness_ur])
			if self.downline:
				gameDisplay.fill(white, [self.x, self.y+self.hi-thickness_dl, self.wid/2, thickness_dl])
				gameDisplay.fill(white, [self.x+self.wid/2, self.y+self.hi-thickness_dr, self.wid/2, thickness_dr])
			if self.upleft:
				gameDisplay.fill(white, [self.x, self.y, thickness_ul, thickness_ul])
			if self.upright:
				gameDisplay.fill(white, [self.x+self.wid-thickness_ur, self.y, thickness_ur, thickness_ur])
			if self.downleft:
				gameDisplay.fill(white, [self.x, self.y+self.hi-thickness_dl, thickness_dl, thickness_dl])
			if self.downright:
				gameDisplay.fill(white, [self.x+self.wid-thickness_dr, self.y+self.hi-thickness_dr, thickness_dr, thickness_dr])

		
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
		if self.x == tilesize:
			self.hitbox = pygame.Rect(x-3*tilesize, y, wid+2*tilesize, hi)
		elif self.x == res_x-3*tilesize:
			self.hitbox = pygame.Rect(x, y, wid+2*tilesize, hi)
		else:
			self.hitbox = pygame.Rect(x, y, wid, hi)
			
		self.color = color
		self.opened = False
		self.startopened = False
		
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
	
def drawSpawnShip(pos_x, pos_y, ship_size, framecount):
	spawnmatrix = [[99,  6,  1, 99],
	               [ 9,  3, 11,  4],
	               [ 2,  8,  0,  7],
	               [99,  5, 10, 99]]
				   
	if framecount > 12:
		plumescale = (18-framecount)*ship_size/2
		pygame.draw.rect(gameDisplay, cyan, [pos_x-plumescale/2, pos_y-ship_size/4, plumescale, ship_size/2])
		pygame.draw.rect(gameDisplay, cyan, [pos_x-ship_size/4, pos_y-plumescale/2, ship_size/2, plumescale])
	
	for y in range(0, 4):
		for x in range(0, 4):
			if spawnmatrix[y][x] < framecount:
				pygame.draw.rect(gameDisplay, white, [pos_x-ship_size/2+x*ship_size/4, pos_y-ship_size/2+y*ship_size/4, ship_size/4, ship_size/4])
	

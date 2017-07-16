from globals import *

class Ship(object):
	def __init__(self, pos_x, pos_y):
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
		self.thrustbox_x = pygame.Rect(self.pos_x-self.ship_size/2, self.pos_y-self.ship_size/2, self.ship_size, self.ship_size/2)
		self.thrustbox_y = pygame.Rect(self.pos_x-self.ship_size/2, self.pos_y-self.ship_size/2, self.ship_size/2, self.ship_size)
		self.pushlist = [False, False, False, False]

	def update(self, lkey, rkey, ukey, dkey, spacebar):
		pushdir = (int(self.pushlist[3])-int(self.pushlist[1]), int(self.pushlist[2])-int(self.pushlist[0]))
		if not spacebar:
			self.accel_x = self.max_accel*(int(rkey) - int(lkey))
			self.accel_y = self.max_accel*(int(dkey) - int(ukey))
		else:
			k = 3
			self.accel_x = -self.vel_x - pushdir[0]*pushforce
			self.accel_y = -self.vel_y - pushdir[1]*pushforce
			scale = self.max_accel
			if abs(self.accel_x) > self.max_accel or abs(self.accel_y) > self.max_accel:
				scale = max(abs(self.accel_x),abs(self.accel_y))
			self.accel_x *= self.max_accel/scale
			self.accel_y *= self.max_accel/scale
		self.vel_x += (self.accel_x + pushdir[0] * pushforce)/self.mass
		self.vel_y += (self.accel_y + pushdir[1] * pushforce)/self.mass
		if abs(self.vel_x) < 0.05:
			self.vel_x = 0
		if abs(self.vel_y) < 0.05:
			self.vel_y = 0
		
		self.pos_x += self.vel_x
		self.pos_y += self.vel_y
		self.hitbox.center = (self.pos_x, self.pos_y)
		self.thrustbox_x.center = (self.pos_x - self.accel_x*self.ship_size/2, self.pos_y)
		self.thrustbox_y.center = (self.pos_x, self.pos_y - self.accel_y*self.ship_size/2)
		self.trail.append([self.pos_x, self.pos_y])
		if len(self.trail) > self.trail_len:
			del self.trail[0]
	
	def collide(self, walls, movers):
		for w in walls:
			if self.hitbox.colliderect(w.hitbox):
				if w.opened == False:
					return True
		for m in movers:
			if self.hitbox.colliderect(m.hitbox):
				return True

	def switchCheck(self, switches):
		for s in switches:
			if s.hitbox.collidelist([self.hitbox, self.thrustbox_x, self.thrustbox_y]) != -1:
				s.flipped = True
				if s.color == green:
					return [True, True]
				elif s.color == magenta:
					return [True, False]

		return [False, False]
		
	def pushCheck(self, pushers):
		self.pushlist = [False, False, False, False]
		for p in pushers:
			if self.hitbox.colliderect(p.hitbox):
				self.pushlist[p.dir] = True
				
	
	def draw(self, framecount = 16):
		if framecount > 15:
			if len(self.trail) > 1:
				pygame.draw.aalines(gameDisplay, white, False, self.trail)
			drawShip(self.pos_x, self.pos_y, self.accel_x, self.accel_y, self.ship_size)
		else:
			drawSpawnShip(self.pos_x, self.pos_y, self.ship_size, framecount)

class Wall(object):
	def __init__(self, x, y, wid, hi, color):
		self.x = x
		self.y = y
		self.wid = wid
		self.hi = hi
		self.color = color
		self.ghost = False
		self.opened = False
		
		# defines the wall's hitbox. If the wall is on an edge in the x direction,
		# increase its width to prevent clipping out of bounds (it shouldn't be 
		# possible to build up enough speed in the y direction to clip oob, but
		# we'll see
		
		if self.x == level_left:
			self.hitbox = pygame.Rect(x-3*tilesize, y, wid+2*tilesize, hi)
		elif self.x == level_right:
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
			diff_x1 = ship.pos_x - self.x
			diff_y1 = ship.pos_y - self.y
			diff_x2 = ship.pos_x - self.x - int(self.wid/2)
			diff_y2 = ship.pos_y - self.y - int(self.hi/2)
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
# - green doors and magenta doors are paired. Hit a green switch to open all green doors and close all magenta doors. 
#    hit a magenta switch to do the opposite. if you hit a green switch, it disables all green switches and enables 
#    all magenta switches, and vice versa. magenta doors start open, and green doors start closed

class Door(object):
	def __init__(self, x, y, wid, hi, color):
		self.x = x
		self.y = y
		self.wid = wid
		self.hi = hi
		if self.x == level_left:
			self.hitbox = pygame.Rect(x-3*tilesize, y, wid+2*tilesize, hi)
		elif self.x == level_right:
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
	
class Switch(object):
	def __init__(self, x, y, wid, hi, color):
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
		
class Mover(object):
	def __init__(self, x, y, wid, hi, color, startdir, id):
		self.x = x
		self.y = y
		self.wid = wid
		self.hi = hi
		self.color = color
		self.dir = startdir
		self.prevdir = self.dir
		self.id = id
		
		# each mover has 3 hitboxes. A main hitbox that is exactly the shape and size of the wall;
		# a leading hitbox the same shape and size, but shifted ahead by the wall speed; and a trailing 
		# hitbox the same shape and size, but shifted behind
		# by checking how each hitbox overlaps when colliding with walls and switches we can determine
		# whether the mover should change direction, stop, hit a switch, etc. very quickly without
		# worrying about counting frames or anything like that.
		self.hitbox = pygame.Rect(x, y, wid, hi)
		if self.color == cyan:
			self.leadbox = pygame.Rect(x, y+wallspeed, wid, hi)
			self.trailbox = pygame.Rect(x, y-wallspeed, wid, hi)
		else:
			self.leadbox = pygame.Rect(x+wallspeed, y, wid, hi)
			self.trailbox = pygame.Rect(x-wallspeed, y, wid, hi)
		self.walls = []
		self.movers = []
		self.pushers = []
		
	def draw(self):
		pygame.draw.rect(gameDisplay, self.color, [self.x, self.y, self.wid, self.hi])
		pygame.draw.rect(gameDisplay, black, [self.x+2, self.y+2, self.wid-4, self.hi-4])
	# Since movers move only along the x- or y- axes, anything outside their respective rows
	# and columns can be safely ignored, with the exception of perpendicular-movers. This
	# function gives a mover object a list of walls, doors, and movers that it may
	# collide with, so when collision is checked the mover only checks these lists.
	# 
	# With this function, there's no discernable CPU difference between a level with 4 movers
	# and a level with 60
	def initCollide(self, walls, movers, pushers):
		for w in walls:
			skip = False
			if self.color == cyan:
				if w.x + w.wid <= self.x or w.x >= self.x + self.wid:
					skip = True
			else:
				if w.y + w.hi <= self.y or w.y >= self.y + self.hi:
					skip = True
			if not skip:
				self.walls.append(w)
				
		for m in movers:
			if m.id != self.id:
				skip = False
				if m.color == self.color:
					if self.color == cyan:
						if m.x + m.wid <= self.x or m.x >= self.x + self.wid:
							skip = True
					else:
						if m.y + m.hi <= self.y or m.y >= self.y + self.hi:
							skip = True
				if not skip:
					self.movers.append(m)
					
		for p in pushers:
			skip = False
			if self.color == cyan:
				if p.x + tilesize <= self.x or p.x >= self.x + self.wid:
					skip = True
			else:
				if p.y + tilesize <= self.y or p.y >= self.y + self.hi:
					skip = True
			if not skip:
				self.pushers.append(p)

	def collide(self, walls, movers, pushers):	
		if self.x % tilesize == 0 and self.y % tilesize == 0:
			pdirlist = []
			for p in self.pushers:
				if self.hitbox.colliderect(p.hitbox):
					pdirlist.append(p.dir)
			if len(pdirlist) > 1:
				pushlist = [False, False, False, False]
				for p in pdirlist:
					pushlist[p] = True
				
				pushdir = {yellow: int(pushlist[3])-int(pushlist[1]), cyan: int(pushlist[2])-int(pushlist[0])}
				if self.color == cyan:
					if pushdir[yellow] != 0:
						self.changeDir(pushdir[yellow], yellow, walls, movers, pushers)
					else:
						self.dir = pushdir[cyan]
						self.prevdir = self.dir
				else:
					if pushdir[cyan] != 0:
						self.changeDir(pushdir[cyan], cyan, walls, movers, pushers)
					else:
						self.dir = pushdir[yellow]
						self.prevdir = self.dir
				
		maincollide = False
		leadcollide = False
		trailcollide = False
		for w in self.walls:
			if maincollide or leadcollide and trailcollide:
				break
			if w.opened == False:
				collides = w.hitbox.collidelistall([self.hitbox, self.leadbox, self.trailbox])
				for c in collides:
					if c == 0:
						maincollide = True
					elif c == 1:
						leadcollide = True
					elif c == 2:
						trailcollide = True
		for m in self.movers:
			if maincollide or leadcollide and trailcollide:
				break
			collides = m.hitbox.collidelistall([self.leadbox, self.trailbox])
			for c in collides:
				if c == 0:
					leadcollide = True
				elif c == 1:
					trailcollide = True
		
		if maincollide or leadcollide and trailcollide:
			self.dir = 0
		elif leadcollide and not trailcollide:
			self.dir = -1
		elif not leadcollide and trailcollide:
			self.dir = 1
		else:
			self.dir = self.prevdir

		if self.dir != 0:
			self.prevdir = self.dir
						
	def changeDir(self, newdir, newcolor, walls, movers, pushers):
		self.color = newcolor
		self.walls = []
		self.movers = []
		self.pushers = []
		self.initCollide(walls, movers, pushers)
		self.dir = newdir
		self.prevdir = self.dir
		if self.color == cyan:
			self.leadbox = pygame.Rect(self.x, self.y+wallspeed, self.wid, self.hi)
			self.trailbox = pygame.Rect(self.x, self.y-wallspeed, self.wid, self.hi)
		else:
			self.leadbox = pygame.Rect(self.x+wallspeed, self.y, self.wid, self.hi)
			self.trailbox = pygame.Rect(self.x-wallspeed, self.y, self.wid, self.hi)

	def move(self):
		if self.dir != 0:
			if self.color == cyan:
				self.y += self.dir*wallspeed
				self.hitbox.y += self.dir*wallspeed
				self.leadbox.y += self.dir*wallspeed
				self.trailbox.y += self.dir*wallspeed
			else:
				self.x += self.dir*wallspeed
				self.hitbox.x += self.dir*wallspeed
				self.leadbox.x += self.dir*wallspeed
				self.trailbox.x += self.dir*wallspeed
		
	def switchCheck(self, switches):
		for s in switches:
			maincollide = False
			leadcollide = False
			trailcollide = False
			collides = s.hitbox.collidelistall([self.hitbox, self.leadbox, self.trailbox])
			for c in collides:
				if c == 0:
					maincollide = True
				elif c == 1:
					leadcollide = True
				elif c == 2:
					trailcollide = True
			# the 3 hitboxes overlap, so this checks for a specific overlap pattern that can only hit the switch
			# on one frame. prevents double-hitting switches, most evident in levels where the ship can hit a green
			# switch and a mover can hit a magenta switch
			if maincollide and leadcollide and not trailcollide and self.dir == 1:
				flip = True
			elif maincollide and trailcollide and not leadcollide and self.dir == -1:
				flip = True
			else:
				flip = False
			if flip:
				s.flipped = True
				if s.color == green:
					return [True, True]
				elif s.color == magenta:
					return [True, False]

		return [False, False]

# these will accelerate the ship in one of 4 directions, depending on their orientation
# this will either be the last feature I add, or I'll scrap it if it's not fun to play.
# but I feel like it'll be fun
class Pusher(object):
	def __init__(self, x, y, dir):
		self.x = x
		self.y = y
		self.dir = dir
		self.hitbox = pygame.Rect(x, y, tilesize, tilesize)
		
	def draw(self, framecount):
		frames = int(framecount/40)
		arrow = pygame.transform.rotate(arrows[(self.dir+frames)%4], 90*self.dir)
		gameDisplay.blit(arrow, (self.x, self.y))

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
	

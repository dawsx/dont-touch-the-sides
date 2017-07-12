from globals import *
from entities import *

class Scene(object):
	def __init__(self):
		pass
		
	def render(self):
		raise NotImplementedError
		
	def update(self):
		raise NotImplementedError

		
class TitleScene(Scene):
	def __init__(self):
		super(TitleScene, self).__init__()
		self.framecount = 0
		self.shipframes = 0
		self.ship = Ship(res_x/2, res_y/2)
	
	def render(self):
		gameDisplay.fill(black)
		self.ship.draw(self.shipframes)
		flashtimer = 40
		if (self.framecount % flashtimer < flashtimer/2):
			entercolor = yellow
		else:
			entercolor = blue
		if (self.framecount) % flashtimer < flashtimer/2:
			wasdcolor = magenta
			arrowcolor = green
			spacebarcolor = blue
		else:
			wasdcolor = green
			arrowcolor = magenta
			spacebarcolor = red			
		
		y_line = 67
		wid_str = text.sizeString("don't touch the sides",8)[0]
		x_start = (res_x - wid_str)/2
		x_next = text.placeString(gameDisplay, "don't touch the sides", white, x_start, y_line, 8)

		
		linespace = 48
		
		y_line = 520
		wid_str = text.sizeString("wasd or <_^> to move")[0]
		x_start = (res_x - wid_str)/2

		x_next = text.placeString(gameDisplay, "wasd", wasdcolor, x_start, y_line)
		x_next = text.placeString(gameDisplay, "or", white, x_next, y_line)
		x_next = text.placeString(gameDisplay, "<_^>", arrowcolor, x_next, y_line)
		x_next = text.placeString(gameDisplay, "to", white, x_next, y_line)
		x_next = text.placeString(gameDisplay, "move", green, x_next, y_line)
		
		y_line += linespace
		wid_str = text.sizeString("spacebar to stop")[0]
		x_start = (res_x - wid_str)/2
		x_next = text.placeString(gameDisplay, "spacebar", spacebarcolor, x_start, y_line)
		x_next = text.placeString(gameDisplay, "to", white, x_next, y_line)
		x_next = text.placeString(gameDisplay, "stop", red, x_next, y_line)

		y_line += linespace
		wid_str = text.sizeString("find the exit in each level")[0]
		x_start = (res_x - wid_str)/2
		x_next = text.placeString(gameDisplay, "find the exit", white, x_start, y_line)
		x_next = text.placeString(gameDisplay, "in each level", white, x_next, y_line)

		y_line += linespace
		wid_str = text.sizeString("press enter/return to begin")[0]
		x_start = (res_x - wid_str)/2
		x_next = text.placeString(gameDisplay, "press", white, x_start, y_line)
		x_next = text.placeString(gameDisplay, "enter/return", entercolor, x_next, y_line)
		x_next = text.placeString(gameDisplay, "to begin", white, x_next, y_line)

	def update(self):
		pressed = pygame.key.get_pressed()
		left, right, up, down, wkey, akey, skey, dkey, spacebar, escape, enter = [pressed[key] for key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_SPACE, pygame.K_ESCAPE, pygame.K_RETURN)]
		if enter:
			self.manager.go_to(GameScene(0))
		if escape and self.shipframes > 15:
			self.ship = Ship(res_x/2, res_y/2)
			self.shipframes = 0
		if self.shipframes > 15:
			self.ship.update(left or akey, right or dkey, up or wkey, down or skey, spacebar)
		self.framecount += 1
		self.shipframes += 1

class GameScene(Scene):
	def __init__(self, levelno):
		super(GameScene, self).__init__()
		self.ispaused = False
		self.pausedelay = 0
		self.framecount = 0
		self.levelno = levelno
		level_tiles = loadLevel(levels[levelno])
		if level_tiles[0][0] == "S":
			self.ghostlevel = True
			level_tiles[0][0] = level_tiles[0][1]
		else:
			self.ghostlevel = False
		self.walls = []
		self.doors = []
		self.switches = []
		self.movers = []
		self.movercount = 0
		for y in range (0, len(level_tiles)):
			for x in range (0, len(level_tiles[0])):
				tile = level_tiles[y][x]
				if tile == "S" and level_tiles[y+1][x] == "S" and level_tiles[y][x+1] == "S":
					self.spawn_x = (x+1)*tilesize + level_left
					self.spawn_y = (y+1)*tilesize + level_top
				elif tile == "W":
					w = Wall(x*tilesize+level_left, y*tilesize+level_top, tilesize, tilesize, white)
					w.ghost = self.ghostlevel
					if x == 0 or level_tiles[y][x-1] != "W":
						w.leftline = True
					if x == len(level_tiles[0])-1 or level_tiles[y][x+1] != "W":
						w.rightline = True
					if y == 0 or level_tiles[y-1][x] != "W":
						w.upline = True
					if y == len(level_tiles)-1 or level_tiles[y+1][x] != "W":
						w.downline = True
					if x != 0 and y != 0 and level_tiles[y][x-1] == "W" and level_tiles[y-1][x] == "W" and level_tiles[y-1][x-1] != "W":
						w.upleft = True
					if x != len(level_tiles[0])-1 and y != 0 and level_tiles[y][x+1] == "W" and level_tiles[y-1][x] == "W" and level_tiles[y-1][x+1] != "W":
						w.upright = True
					if x != 0 and y != len(level_tiles)-1 and level_tiles[y][x-1] == "W" and level_tiles[y+1][x] == "W" and level_tiles[y+1][x-1] != "W":
						w.downleft = True
					if x != len(level_tiles[0])-1 and y != len(level_tiles)-1 and level_tiles[y][x+1] == "W" and level_tiles[y+1][x] == "W" and level_tiles[y+1][x+1] != "W":
						w.downright = True
					self.walls.append(w)
				elif tile == "R" or tile == "B" or tile == "G" or tile == "M":
					d = Door(x*tilesize+level_left, y*tilesize+level_top, tilesize, tilesize, colors[tile])
					if tile == "M":
						d.opened = True
					self.doors.append(d)
				elif tile == "r" or tile == "b" or tile == "g" or tile == "m":
					s = Switch(x*tilesize+level_left, y*tilesize+level_top, 2*tilesize, 2*tilesize, colors[tile])
					if tile == "m":
						s.flipped = True
					self.switches.append(s)
					level_tiles[y][x] = ' '
					level_tiles[y+1][x] = ' '
					level_tiles[y][x+1] = ' '
					level_tiles[y+1][x+1] = ' '
				elif tile == "C" or tile == "c" or tile == "Y" or tile == "y":
					tx = x
					ty = y
					while (level_tiles[ty][tx] == tile):
						tx += 1
						
					while (level_tiles[ty][tx-1] == tile):
						ty += 1
						
					if tile == "c" or tile == "y":
						dir = -1
					else:
						dir = 1
						
					m = Mover(x*tilesize+level_left, y*tilesize+level_top, (tx-x)*tilesize, (ty-y)*tilesize, colors[tile], dir, self.movercount)
					self.movers.append(m)
					
					for qy in range (y, ty):
						for qx in range(x, tx):
							level_tiles[qy][qx] = " "
					
					self.movercount += 1
		self.ship = Ship(self.spawn_x, self.spawn_y)
		self.reddoorsopen = False
		self.bluedoorsopen = False
		self.greendoorsopen = False
		for m in self.movers:
			m.initcollide(self.walls + self.doors, self.movers)
		print (len(self.movers))
	
	def render(self):
		gameDisplay.fill(black)
		for w in self.walls:
			w.draw(self.ship)
		for s in self.switches:
			s.draw()
		for m in self.movers:
			m.draw()
		for d in self.doors:
			d.draw()
		if not self.ispaused:
			self.ship.draw(self.framecount)
		else:
			wid_str, hi_str = text.sizeString("pause",8)
			x_next = (res_x - wid_str)/2
			y_line = (res_y - hi_str)/2
			x_next = text.placeString(gameDisplay, "pause", yellow, x_next, y_line, 8)
			
	def update(self):
		pressed = pygame.key.get_pressed()
		left, right, up, down, wkey, akey, skey, dkey, spacebar, escape, enter, backspace = [pressed[key] for key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_SPACE, pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_BACKSPACE)]
		if self.ispaused:
			if escape and self.pauseframes > 15:
				self.ispaused = False
				self.pausedelay = 15
			self.pauseframes += 1
		else:
			for m in self.movers:
				greencheck = m.switchCheck(self.switches)
				if greencheck[0]:
					self.greendoorsopen = greencheck[1]
					
			greencheck = self.ship.switchCheck(self.switches)
			self.reddoorsopen = True
			self.bluedoorsopen = True
			if greencheck[0]:
				self.greendoorsopen = greencheck[1]
			
			for s in self.switches:
				if s.color == red and s.flipped == False:
					self.reddoorsopen = False
				elif s.color == blue and s.flipped == False:
					self.bluedoorsopen = False
				elif s.color == green:
					s.flipped = self.greendoorsopen
				elif s.color == magenta:
					s.flipped = not self.greendoorsopen
			
			for d in self.doors:
				if d.color == red:
					d.opened = self.reddoorsopen
				elif d.color == blue:
					d.opened = self.bluedoorsopen
				elif d.color == green:
					d.opened = self.greendoorsopen
				elif d.color == magenta:
					d.opened = not self.greendoorsopen
			
			for m in self.movers:
				m.collide()
			for m in self.movers:
				m.move()
			
			dead = self.ship.collide(self.walls + self.doors, self.movers)
			if dead:
				self.manager.go_to(GameScene(self.levelno))
			if escape and self.pausedelay <= 0:
				self.ispaused = True
				self.pauseframes = 0
			if self.framecount > 15:
				self.ship.update(left or akey, right or dkey, up or wkey, down or skey, spacebar)
				
			# level is considered beaten when the ship leaves the window range. If this happens, go to the next level
			if self.ship.pos_x > (res_x + self.ship.ship_size) or self.ship.pos_x < (0 - self.ship.ship_size) or self.ship.pos_y > (res_y + self.ship.ship_size) or self.ship.pos_y < (0 - self.ship.ship_size) or (enter and self.framecount > 10 and skiplevels == True):
				self.manager.go_to(GameScene(self.levelno + 1))
			if backspace and self.framecount > 10 and skiplevels == True:
				if self.levelno == 0:
					self.manager.go_to(TitleScene())
				else:
					self.manager.go_to(GameScene(self.levelno - 1))
			self.framecount += 1
			if self.pausedelay > 0:
				self.pausedelay -= 1
				
class SceneManager(object):
	def __init__(self):
		self.go_to(TitleScene())
		
	def go_to(self, scene):
		self.scene = scene
		self.scene.manager = self
	
def loadLevel(levelimg):
	file = open(levelimg, 'rb')
	file.seek(0x12)
	bwidth = file.read(4)
	bheight = file.read(4)
	width = struct.unpack("<l", bwidth)[0]
	height = struct.unpack("<l", bheight)[0]
	pad = (-width)%4
	
	fileoffset = 0x436
	pixellist = []
	file.seek(fileoffset)
	for x in range (0,height):
		temp = file.read(width)
		pixellist = [temp] + pixellist
		file.seek(pad, 1)
	
	# tile constants for loading a level from bmp
	spawntile = b'\xff'
	bgtile = b'\x00'
	walltile = b'\xa4'
	bluedoortile = b'\xd2'
	blueswitchtile = b'\xec'
	reddoortile = b'\x4f'
	redswitchtile = b'\xef'
	greendoortile = b'\x71'
	greenswitchtile = b'\x3e'
	magentadoortile = b'\xd5'
	magentaswitchtile = b'\x07'
	mwalltile_l = b'\xfb'
	mwalltile_r = b'\x08'
	mwalltile_u	= b'\xe8'
	mwalltile_d = b'\x09'

	level = []
	for row in pixellist:
		str = []
		splitrow = [row[i:i+1] for i in range(0, len(row))]
		for col in splitrow:
			if col == spawntile:
				str += ["S"]
			elif col == walltile:
				str += ["W"]
			elif col == reddoortile:
				str += ["R"]
			elif col == redswitchtile:
				str += ["r"]
			elif col == bluedoortile:
				str += ["B"]
			elif col == blueswitchtile:
				str += ["b"]
			elif col == greendoortile:
				str += ["G"]
			elif col == greenswitchtile:
				str += ["g"]
			elif col == magentadoortile:
				str += ["M"]
			elif col == magentaswitchtile:
				str += ["m"]
			elif col == mwalltile_l:
				str += ["Y"]
			elif col == mwalltile_r:
				str += ["y"]
			elif col == mwalltile_u:
				str += ["C"]
			elif col == mwalltile_d:
				str += ["c"]
			else:
				str += [" "]
		
		level.append(str)
	return level

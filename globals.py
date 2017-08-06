import pygame
import math
import struct
import text

# debug option, skips levels by pressing enter
skiplevels = True

# colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
cyan = (0, 255, 255)
blue = (0, 0, 255)
magenta = (255, 0, 255)

colors = {
        "R": red, 
        "r": red, 
		"B": blue, 
		"b": blue, 
	    "G": green, 
		"g": green, 
		"M": magenta, 
		"m": magenta, 
		"C": cyan, 
		"c": cyan, 
		"Y": yellow, 
		"y": yellow
}

# tile constants for loading a level from bmp

tiledict = {
		b'\xff': "S",
		b'\x00': " ",
		b'\xa4': "W",
		b'\xd2': "B",
		b'\xec': "b",
		b'\x4f': "R",
		b'\xef': "r",
		b'\x71': "G",
		b'\x3e': "g",
		b'\xd5': "M",
		b'\x07': "m",
		b'\x08': "y",
		b'\xfb': "Y",
		b'\x09': "c",
		b'\xe8': "C",
		b'\x37': "<",
		b'\x67': ">",
		b'\x66': "^",
		b'\x01': "v"
}

# display constants
res_x = 1024
res_y = 768
fps = 60
tilesize = 8

level_left = 1*tilesize
level_right = 126*tilesize
level_top = 11*tilesize
level_bottom = 94*tilesize

wallspeed = 2
pushforce = 0.4

# create the list of levels
from os import listdir
from os.path import isfile, join
leveldir = "./levels"
levels = [leveldir + "/" + f for f in listdir(leveldir) if isfile(join(leveldir, f))]

gameDisplay = pygame.display.set_mode((res_x, res_y))
clock = pygame.time.Clock()

arrows = []
arrowcolors = [red, green, blue, yellow]
for c in arrowcolors:
	a = pygame.Surface([tilesize, tilesize])
	pygame.draw.rect(a, c, [tilesize/8, tilesize/2, tilesize/8, tilesize/2])
	pygame.draw.rect(a, c, [tilesize/4, tilesize/4, tilesize/8, tilesize*5/8])
	pygame.draw.rect(a, c, [tilesize*3/8, 0, tilesize/4, tilesize*5/8])
	pygame.draw.rect(a, c, [tilesize*5/8, tilesize/4, tilesize/8, tilesize*5/8])
	pygame.draw.rect(a, c, [tilesize*3/4, tilesize/2, tilesize/8, tilesize/2])
	arrows.append(a)
	
pushdict = {
"^": 0,
"<": 1,
"v": 2,
">": 3
}

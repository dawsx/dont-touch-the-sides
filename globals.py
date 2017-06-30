import pygame
import math
import text
import dither

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


# display constants
res_x = 800
res_y = 576
fps = 60
tilesize = 8
res_x += 2*tilesize
res_y += 2*tilesize

# create the list of levels
from os import listdir
from os.path import isfile, join
leveldir = "./levels"
levels = [leveldir + "/" + f for f in listdir(leveldir) if isfile(join(leveldir, f))]

gameDisplay = pygame.display.set_mode((res_x, res_y))
clock = pygame.time.Clock()

# pre-calculate sin and cos values for ray-tracing
psin = []
pcos = []
numrays = 360
for x in range(0, numrays):
	psin.append(math.sin(x*math.pi*2/numrays))
	pcos.append(math.cos(x*math.pi*2/numrays))
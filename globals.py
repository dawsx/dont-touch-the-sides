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

colors = {"R": red, "r": red, "B": blue, "b": blue, "G": green, "g": green, "M": magenta, "m": magenta, "C": cyan, "c": cyan, "Y": yellow, "y": yellow}

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

# create the list of levels
from os import listdir
from os.path import isfile, join
leveldir = "./levels_test"
levels = [leveldir + "/" + f for f in listdir(leveldir) if isfile(join(leveldir, f))]

gameDisplay = pygame.display.set_mode((res_x, res_y))
clock = pygame.time.Clock()
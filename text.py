import pygame
import math
from globals import *
import struct

file = open('gfx\charmap.bmp', 'rb')
fileoffset = 0x436
file.seek(0x12)
bwidth = file.read(4)
bheight = file.read(4)

width = struct.unpack("<l", bwidth)[0]
height = struct.unpack("<l", bheight)[0]

pixellist = []
file.seek(fileoffset)
for x in range (0,height):
	temp = file.read(width).split(b'\xa4')
	pixellist = [temp] + pixellist

chardict = {}
dictstring = '0123456789abcdefghijklmnopqrstuvwxyz.,!?-+/\'"<>^_ '

for x in range(0, len(dictstring)):
	char = []
	for line in pixellist:
		temp = []
		splitline = [line[x][i:i+1] for i in range(0, len(line[x]))]
		for col in splitline:
			if col == b'\xff':
				temp += [' ']
			else:
				temp += ['#']
		char.append(temp)
	chardict[dictstring[x]] = char

def placeChar(gameDisplay, char, color, x_0, y_0, scale = 4, spacing = 0):
	outchar = chardict[char]
	for y in range(0,len(outchar)):
		for x in range(0,len(outchar[0])):
			if outchar[y][x] == ' ':
				pass
			else:
				xcoord = x*scale + x_0
				ycoord = y*scale + y_0
				pygame.draw.rect(gameDisplay, color, [xcoord, ycoord, scale-spacing, scale-spacing])
	return x_0 + scale*(len(outchar[0])+1)

def placeString(gameDisplay, string, color, x_0, y_0, scale = 4, spacing = 0):
	char_x = x_0
	char_y = y_0
	for c in string:
		char_x = placeChar(gameDisplay, c, color, char_x, char_y, scale, spacing)
	return char_x + 5*scale

def sizeString(string, scale = 4):
	length = 0
	for c in string:
		length += scale*(len(chardict[c][0])+1)
	return (length - scale, scale * len(chardict['0']))
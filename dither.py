from globals import *
	
bayer8x8 = [[ 0, 48, 12, 60,  3, 51, 15, 63],
            [32, 16, 44, 28, 35, 19, 47, 31],
            [ 8, 56,  4, 52, 11, 59,  7, 55],
            [40, 24, 36, 20, 43, 27, 39, 23],
            [ 2, 50, 14, 62,  1, 49, 13, 61],
            [34, 18, 46, 30, 33, 17, 45, 29],
            [10, 58,  6, 54,  9, 57,  5, 53],
            [42, 26, 38, 22, 41, 25, 37, 21]]
		

def dither(color, x, y, use4x4 = True):
	red = color[0]
	green = color[1]
	blue = color[2]
	if use4x4:
		thres = bayer4x4[y%4][x%4]
	else:
		thres = bayer8x8[y%8][x%8]
	
	if red > thres:
		red = 255
	else:
		red = 0
		
	if green > thres:
		green = 255
	else:
		green = 0
		
	if blue > thres:
		blue = 255
	else:
		blue = 0
		
	return (red, green, blue)
	
def gradient(color1, color2, depth = 0, size = 8):
	surflist = []
	numtiles = 4**depth + 1
	pxscale = 2**(3-depth)
	for i in range (0, numtiles):
		temp = pygame.Surface((size, size))
		for y in range(0, int(size/pxscale)):
			for x in range(0, int(size/pxscale)):
				if i < bayer8x8[(y*pxscale) % 8][(x*pxscale) % 8] + 0.5:
					color = color1
				else:
					color = color2
				temp.fill(color, [x*pxscale, y*pxscale, pxscale, pxscale])
		
		surflist.append(temp)
		
	return surflist

	
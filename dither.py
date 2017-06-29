from globals import *

bayer4x4 = [[  0, 128,  32, 160], 
            [192,  64, 224,  96], 
			[ 48, 176,  16, 144], 
			[240, 112, 208,  80]]
			
			

bayer8x8 = [[  0, 192,  48, 240,  12, 204,  60, 252],
            [128,  64, 176, 112, 140,  76, 188, 124],
            [ 32, 224,  16, 208,  44, 236,  28, 220],
            [160,  96, 144,  80, 172, 108, 156,  92],
            [  8, 200,  56, 248,   4, 196,  52, 244],
            [136,  72, 184, 120, 132,  68, 180, 116],
            [ 40, 232,  24, 216,  36, 228,  20, 212],
            [168, 104, 152,  88, 164, 100, 148,  84]]

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
	
def gradient(color1, color2, size = 8, pxscale = 2, use4x4 = True):
	surflist = []
	for i in range (0, 17):
		temp = pygame.Surface((size, size))
		for y in range(0, int(size/pxscale)):
			for x in range(0, int(size/pxscale)):
				if i*16 < bayer4x4[y][x]+8:
					color = color1
				else:
					color = color2
				temp.fill(color, [x*pxscale, y*pxscale, pxscale, pxscale])
		
		surflist.append(temp)
		
	return surflist

	
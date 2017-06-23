import pygame
import math
import text
import random
from globals import *
from entities import *
from scenes import *

def gameLoop():
	gameExit = False
	
	manager = SceneManager()
	
	while not gameExit:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameExit = True
		
		manager.scene.update()
		manager.scene.render()
		pygame.display.update()
		clock.tick(fps)
		
	pygame.quit()
	quit()

pygame.init()
pygame.display.set_caption('don\'t touch the sides')
gameLoop()

#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#H##############################################################################
# FILE:	      game.py
# PROJECT:    Bunny the Defender
# AUTHOR:     David Hás
# START DATE: 2 Sep 2018
# VERSION:    0.3
#
# DESCRIPTION:
# 	Game, where a bunny defends castles againgst an army of badgers.
#
# CHANGES:
#
# VERSION DATE    WHO     DETAIL
# 0.1     02Sep18 DH      Initial implementation
# 0.2     03Sep18 DH      An attempt to refactor using a main class Game()
# 0.3     03Sep18 DH      Refactoring to more objective design using function
#                         main()
#
###

import pygame
from pygame.locals import *
import math

class Window():
	def __init__(self, width, height):
		self.rect = pygame.Rect(0, 0, width, height)
		self.border = 40

class Player():
	image = None

	def __init__(self):
		self.playerPos = [100, 100]
		self.walkSpeed = 5

class Grass():
	image = None

class Castle():
	image = None

class Arrow():
	image = None

def main():
	# Game initialization
	pygame.init()
	window = Window(640, 480)
	player = Player()
	keys = {'w': False,
		'a': False,
		's': False,
		'd': False}
	screen = pygame.display.set_mode(window.rect.size)

	# Load the images
	Player.image = pygame.image.load("resources/images/dude.png")
	Grass.image = pygame.image.load("resources/images/grass.png")
	Castle.image = pygame.image.load("resources/images/castle.png")
	Arrow.image = pygame.image.load("resources/images/arrow.png")

	# Game loop
	while True:
		# Clear the screen before redrawing
		screen.fill(0)
		# Draw the screen elements
		for y in range(0, height, grassImage.get_height()):
			for x in range(0, width, grassImage.get_width()):
				screen.blit(grassImage,(x,y))
		screen.blit(castleImage,(0,30))
		screen.blit(castleImage,(0,135))
		screen.blit(castleImage,(0,240))
		screen.blit(castleImage,(0,345))
		# Set player position and rotation and draw him
		mousepos = pygame.mouse.get_pos()
		angle = math.atan2(mousepos[0]-playerpos[0], mousepos[1]-playerpos[1])
		angle = (angle * 180/math.pi) - 90
		player = pygame.transform.rotate(playerImage, angle)
		playerDrawPos = [playerpos[0] - player.get_rect().width/2, playerpos[1] - player.get_rect().height/2]
		screen.blit(player, playerDrawPos)
		# Update the screen
		pygame.display.flip()
		# Event loop
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit(0)
			if event.type == pygame.KEYDOWN:
				if event.key == K_w:
					keys['w'] = True
				elif event.key == K_a:
					keys['a'] = True
				elif event.key == K_s:
					keys['s'] = True
				elif event.key == K_d:
					keys['d'] = True
			if event.type == pygame.KEYUP:
				if event.key == K_w:
					keys['w'] = False
				elif event.key == K_a:
					keys['a'] = False
				elif event.key == K_s:
					keys['s'] = False
				elif event.key == K_d:
					keys['d'] = False
		# Move the player
		if keys['w']:
			if playerpos[1] >= border:
				playerpos[1] -= walkStep
		elif keys['s']:
			if playerpos[1] <= height - border:
				playerpos[1] += walkStep
		if keys['a']:
			if playerpos[0] >= border:
				playerpos[0] -= walkStep
		elif keys['d']:
			if playerpos[0] <= width - border:
				playerpos[0] += walkStep

if __name__ == "__main__":
	main()


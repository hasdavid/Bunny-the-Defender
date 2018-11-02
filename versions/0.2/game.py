#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#H##############################################################################
# FILE:	      game.py
# PROJECT:    Bunny the Defender
# AUTHOR:     David Hás
# START DATE: 2 Sep 2018
# VERSION:    0.2
#
# DESCRIPTION:
# 	Game, where a bunny defends castles againgst an army of badgers.
#
# CHANGES:
#
# VERSION DATE    WHO     DETAIL
# 0.1     02Sep18 DH      Initial implementation
# 0.2     03Sep18 DH      An attempt to refactor using a main class Game()
#
###

import pygame
from pygame.locals import *
import math

# Load images
playerImage = pygame.image.load("resources/images/dude.png")
grassImage = pygame.image.load("resources/images/grass.png")
castleImage = pygame.image.load("resources/images/castle.png")
arrowImage = pygame.image.load("resources/images/bullet.png")

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

class Game():
	"""Main class"""

	def __init__(self):
		self.width = 640
		self.height = 480

	def run(self):
		"""Initialization and game loop"""
		pygame.init()
		width, height = 640, 480
		playerpos = [100,100]
		walkStep = 5
		border = 40
		keys = {'w': False, 'a': False, 's': False, 'd': False}
		screen = pygame.display.set_mode((width, height))

if __name__ == "__main__":
	app = Game()
	app.run()


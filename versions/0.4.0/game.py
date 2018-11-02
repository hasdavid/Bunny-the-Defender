#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#H##############################################################################
# FILE:	      game.py
# PROJECT:    Bunny the Defender
# AUTHOR:     David Hás
# START DATE: 2 Sep 2018
# VERSION:    0.4.0
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
# 0.4.0   04Sep18 DH      Another try to reimplement using objective programming
#
###

import pygame
from pygame.locals import *
import math

class Entity():
	"""Represents an entity on the game screen.

	Note:
		Do not use 'origImage' or 'pos' attributes to draw the entity.
		Instead, use the 'image' attribute and 'drawPos' property.

	Attributes:
		pos (int, int): Current entity position. Holds coordinates of
			the center of the image. Do not use this to draw the
			entity, as top left corner needs to be used instead.
		origImage (pygame.Surface): Contains an unchanged original entity
			image.

	Properties:
		drawPos (int, int): Returns a top left corner of the entity
			image. Use this to draw the entity.
		image (pygame.Surface): Returns an image edited for drawing.
	"""

	def __init__(self):
		"""Initializes the Entity instance."""

		self.pos = [0, 0]
		self.origImage = pygame.image.load("resources/images/notfound.png")

	@property
	def drawPos(self):
		return (self.pos[0] - self.image.get_width() / 2,
			self.pos[1] - self.image.get_height() / 2)

	@property
	def image(self):
		return self.origImage

class Arrow(Entity):
	"""Represents an arrow projectile."""

	def __init__(self):
		"""Initializes the Arrow instance."""

		super().__init__()
		self.origImage = pygame.image.load("resources/images/arrow.png")

class Player(Entity):
	"""Contains information about player character."""

	def __init__(self):
		"""Initializes the Player instance."""

		super().__init__()
		self.origImage = pygame.image.load("resources/images/bunny.png")
		self.pos = [100, 100]

class Game():
	"""Contains general information about game and window.

	Attributes:
		player (Player): Contains information about the player
			character.
		screen (pygame.Surface): Used to interact with pygame's
			display. Use it to get screen dimensions, to force
			update the screen etc.
		keys ({string: bool}): A dictionary of pressable keys with
			information whether they are pressed or not.
		castleImage (pygame.Surface): Image of the castle.
		grassImage (pygame.Surface): Image of the grass.
		castlePos (tuple of (x,y)): Tuple containing positions of the
			castles.
	"""

	def __init__(self):
		"""Initializes the game instance and sets neccessary
		attributes."""

		pygame.init()
		self.player = Player()
		self.loadImages()
		self.screen = pygame.display.set_mode((640, 480))
		self.keys = {
			'w': False,
			'a': False,
			's': False,
			'd': False}
		self.castlePos = (
			(0, 30),
			(0, 135),
			(0, 240),
			(0, 345))

	def loadImages(self):
		"""Loads images from resources/images."""

		self.castleImage = pygame.image.load("resources/images/castle.png")
		self.grassImage = pygame.image.load("resources/images/grass.png")

	def redrawScreen(self):
		"""Redraws the game screen."""

		self.screen.fill(0)
		yRange = range(0, self.screen.get_height(), self.grassImage.get_height())
		xRange = range(0, self.screen.get_width(), self.grassImage.get_width())
		for y in yRange:
			for x in xRange:
				self.screen.blit(self.grassImage, (x, y))
		for position in self.castlePos:
			self.screen.blit(self.castleImage, position)
		self.screen.blit(self.player.image, self.player.drawPos)
		pygame.display.flip()

	def handleEvents(self):
		"""Processes events and reacts to them."""

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit(0)
			if event.type == pygame.KEYDOWN:
				if event.key == K_w:
					self.keys['w'] = True
				elif event.key == K_a:
					self.keys['a'] = True
				elif event.key == K_s:
					self.keys['s'] = True
				elif event.key == K_d:
					self.keys['d'] = True
			if event.type == pygame.KEYUP:
				if event.key == K_w:
					self.keys['w'] = False
				elif event.key == K_a:
					self.keys['a'] = False
				elif event.key == K_s:
					self.keys['s'] = False
				elif event.key == K_d:
					self.keys['d'] = False

	def run(self):
		"""Main game method. Call it to run the game."""

		while True:
			self.redrawScreen()
			self.handleEvents()

if __name__ == "__main__":
	game = Game()
	game.run()


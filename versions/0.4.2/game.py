#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#H##############################################################################
# FILE:	      game.py
# PROJECT:    Bunny the Defender
# AUTHOR:     David Hás
# START DATE: 2 Sep 2018
# VERSION:    0.4.2
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
# 0.4.1   04Sep18 DH      Making the bunny respond to keystrokes.
# 0.4.2   05Sep18 DH      Making the bunny turn wih mouse.
#
###

import pygame
from pygame.locals import *
import math
from libs import point

class Arrow():
	"""Represents an arrow projectile.

	Note:
		Do not use 'origImage' or 'pos' attributes to draw the entity.
		Instead, use the 'image' attribute and 'drawPos' property.

	Attributes:
		pos (point.Point): Current entity position. Holds coordinates of
			the center of the image. Do not use this to draw the
			entity, as top left corner needs to be used instead.
		origImage (pygame.Surface): This class attribute contains an
			unchanged original entity image.
		speed (int): How many pixels per tick the entity travels.

	Properties:
		drawPos (point.Point): Returns a top left corner of the entity
			image. Use this to draw the entity.
		image (pygame.Surface): Returns an image edited for drawing.
	"""

	origImage = pygame.image.load("resources/images/arrow.png")

	def __init__(self):
		self.pos = point.Point()
		self.speed = 10

	@property
	def drawPos(self):
		return point.Point(self.pos.x - self.image.get_width() / 2,
			self.pos.y - self.image.get_height() / 2)

	@property
	def image(self):
		return Arrow.origImage


class Player():
	"""Represents a player entity.

	Note:
		Do not use 'origImage' or 'pos' attributes to draw the entity.
		Instead, use the 'image' attribute and 'drawPos' property.

	Attributes:
		pos (point.Point): Current entity position. Holds coordinates of
			the center of the image. Do not use this to draw the
			entity, as top left corner needs to be used instead.
		origImage (pygame.Surface): Contains an unchanged original entity
			image.
		speed (int): How many pixels per tick the entity travels.

	Properties:
		drawPos (point.Point): Returns a top left corner of the entity
			image. Use this to draw the entity.
		diagonalSpeed (int): Returns diagonal speed of the entity in
			pixels.
		image (pygame.Surface): Returns an image edited for drawing.
	"""

	def __init__(self):
		self.origImage = pygame.image.load("resources/images/bunny.png")
		self.pos = point.Point(100, 100)
		self.speed = 5

	@property
	def drawPos(self):
		return point.Point(self.pos.x - self.image.get_width() / 2,
			self.pos.y - self.image.get_height() / 2)

	@property
	def diagonalSpeed(self):
		return self.speed / math.sqrt(2)

	@property
	def image(self):
		direction = pygame.mouse.get_pos()
		angle = math.atan2(direction[0] - self.pos.x, direction[1] - self.pos.y)
		angle = (angle * 180/math.pi) - 90
		return pygame.transform.rotate(self.origImage, angle)

class Game():
	"""Contains general information about game and window.

	Attributes:
		player (Player): Contains information about the player
			character.
		screen (pygame.Surface): Used to interact with pygame's
			display. Use it to get screen dimensions, to force
			update the screen etc.
		border (int): A border of the map in pixels which cannot be
			crossed by player.
		keys (dict of string:bool): A dictionary of pressable keys with
			information whether they are pressed or not.
		castleImage (pygame.Surface): Image of the castle.
		grassImage (pygame.Surface): Image of the grass.
		castlePos (tuple of (point.Point)): Tuple containing positions
			of the castles.
	"""

	def __init__(self):
		pygame.init()
		self.player = Player()
		self.loadImages()
		self.screen = pygame.display.set_mode((640, 480))
		self.border = 40
		self.keys = {
			'w': False,
			'a': False,
			's': False,
			'd': False}
		self.castlePos = (
			point.Point(0, 30),
			point.Point(0, 135),
			point.Point(0, 240),
			point.Point(0, 345))

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
			self.screen.blit(self.castleImage, position.as_tuple())
		self.screen.blit(self.player.image, self.player.drawPos.as_tuple())
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

	def movePlayer(self, entity):
		"""Updates the player's position attribute.

		Args:
                        entity (Player): The entity to move.

		Returns:
			point.Point: New position of the entity.
		"""

		vertical = False
		horizontal = False

		if self.keys['w']:
			vertical = not vertical
		if self.keys['s']:
			vertical = not vertical
		if self.keys['a']:
			horizontal = not horizontal
		if self.keys['d']:
			horizontal = not horizontal
		if vertical and horizontal:
			speed = entity.diagonalSpeed
		else
			speed = entity.speed

		if self.keys['w']:
			if self.keys['s']:
				pass
			elif entity.pos.y >= self.border + speed:
				entity.pos.y -= speed
		elif self.keys['s']:
			if entity.pos.y < self.screen.get_height() - self.border - speed:
				entity.pos.y += speed
		if self.keys['a']:
			if self.keys['d']:
				pass
			elif entity.pos.x >= self.border + speed:
				entity.pos.x -= speed
		elif self.keys['d']:
			if entity.pos.x < self.screen.get_width() - self.border - speed:
				entity.pos.x += speed

		return entity.pos

	def moveArrow(self, entity):
		"""Updates the arrow's position attribute.

		Args:
                        entity (Arrow): The entity to move.

		Returns:
			point.Point: New position of the entity.
		"""

		pass # TODO

	def run(self):
		"""Main game method. Call it to run the game."""

		while True:
			self.redrawScreen()
			self.handleEvents()
			self.movePlayer(self.player)

if __name__ == "__main__":
	game = Game()
	game.run()


#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#H##############################################################################
# FILE:	      game.py
# PROJECT:    Bunny the Defender
# AUTHOR:     David Has
# START DATE: 2 Sep 2018
# VERSION:    0.6.0
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
# 0.4.3   05Sep18 DH      Optimizing bunny's movement method using a bitmap.
# 0.4.4   05Sep18 DH      Reverting to original movement method.
# 0.5.0   05Sep18 DH      Implementing arrows.
# 0.6.0   02Nov18 DH      Added badgers, sounds, battle system and statistics.
#
###

import pygame
from pygame.locals import *
import math
from libs import point
import random

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
		angle (float): An angle by which the entity is rotated. Angle is
			in radians.

	Properties:
		drawPos (point.Point): Returns a top left corner of the entity
			image. Use this to draw the entity.
		image (pygame.Surface): Returns an image edited for drawing.
	"""

	origImage = pygame.image.load("resources/images/arrow.png")

	def __init__(self, playerPos, playerAngle):
		"""Initializes an Arrow instance.

		Args:
			playerPos (point.Point): Position of the player when
				fired.
			playerAngle (float): Angle of the player when fired in
				radians.
		"""

		self.pos = playerPos.clone()
		self.angle = -playerAngle 
		self.speed = 10

	def get_rect(self):
		"""Returns a pygame.Rect of the object."""

		return pygame.Rect(
			self.drawPos.x,
			self.drawPos.y,
			self.image.get_width(),
			self.image.get_height())

	@property
	def drawPos(self):
		return point.Point(self.pos.x - self.image.get_width() / 2,
			self.pos.y - self.image.get_height() / 2)

	@property
	def image(self):
		return pygame.transform.rotate(Arrow.origImage, -self.angle * 180/math.pi)

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
		angle (float): Returns an angle by which the entity is rotated.
			Angle is in radians.
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
	def angle(self):
		direction = pygame.mouse.get_pos()
		alpha = math.atan2(direction[0] - self.pos.x, direction[1] - self.pos.y)
		alpha -= math.pi/2 # Angle correction
		return alpha

	@property
	def image(self):
		return pygame.transform.rotate(self.origImage, self.angle * 180/math.pi)

class Badger():
	"""A badger entity.

	These are the enemies the bunny is supposed to shoot.

	Note:
		Do not use 'origImage' or 'pos' attributes to draw the entity.
		Instead, use the 'image' attribute and 'drawPos' property.

	Properties:
		drawPos (point.Point): Returns a top left corner of the entity
			image. Use this to draw the entity.
	"""

	origImage1 = pygame.image.load("resources/images/badguy.png")
	origImage2 = pygame.image.load("resources/images/badguy2.png")
	origImage3 = pygame.image.load("resources/images/badguy3.png")
	origImage4 = pygame.image.load("resources/images/badguy4.png")

	def __init__(self, spawnPos):
		"""Initializes a Badger instance.

		Args:
			spawnPos (point.Point): Spawning position of the badger.
		"""

		self.pos = spawnPos
		self.speed = 5
		self.imageChangeCountdown = 0
		self._image = Badger.origImage1

	def move(self, vector):
		"""Moves the entity by adding the specified vector.

		Args:
			vector (point.Point): A vector to be added.
		"""

		self.pos += vector

	def get_rect(self):
		"""Returns a pygame.Rect of the object."""

		return pygame.Rect(
			self.drawPos.x,
			self.drawPos.y,
			self._image.get_width(),
			self._image.get_height())

	@property
	def drawPos(self):
		return point.Point(self.pos.x - self._image.get_width() / 2,
			self.pos.y - self._image.get_height() / 2)

	@property
	def image(self):
		if self.imageChangeCountdown == 0:
			self.imageChangeCountdown = 5
			if self._image == Badger.origImage1:
				self._image = Badger.origImage2
			elif self._image == Badger.origImage2:
				self._image = Badger.origImage3
			elif self._image == Badger.origImage3:
				self._image = Badger.origImage4
			elif self._image == Badger.origImage4:
				self._image = Badger.origImage1
		else:
			self.imageChangeCountdown -= 1
		return self._image

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
		castlePos (tuple of point.Point): Tuple containing positions
			of the castles.
		arrowList (list of Arrow): List of all arrows currently present
			on the game screen.
	"""

	def __init__(self):
		pygame.init()
		pygame.font.init()
		pygame.mixer.init()
		self.gamefont = pygame.font.SysFont("Arial", 30)
		self.player = Player()
		self.loadImages()
		self.loadAudio()
		self.screen = pygame.display.set_mode((640, 480))
		self.border = 40
		self.running = True
		self.wintime = 90000
		self.badMinDmg = 5
		self.badMaxDmg = 20
		self.badgerBaseTime = 100
		self.nextBadgerTimer = 0
		self.castleHealth = 194
		self.kills = 0
		self.shotArrows = 0
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
		self.arrowList = []
		self.badgerList = []

	def loadImages(self):
		"""Loads images from resources/images."""

		self.castleImage = pygame.image.load("resources/images/castle.png")
		self.grassImage = pygame.image.load("resources/images/grass.png")
		self.healthBarImage = pygame.image.load("resources/images/healthbar.png")
		self.healthImage = pygame.image.load("resources/images/health.png")
		self.gameOverImage = pygame.image.load("resources/images/gameover.png")
		self.youWinImage = pygame.image.load("resources/images/youwin.png")

	def loadAudio(self):
		"""Loads audio files from resources/audio."""

		self.hitSound = pygame.mixer.Sound("resources/audio/explode.wav")
		self.hitSound.set_volume(0.05)
		self.enemySound = pygame.mixer.Sound("resources/audio/enemy.wav")
		self.enemySound.set_volume(0.05)
		self.shootSound = pygame.mixer.Sound("resources/audio/shoot.wav")
		self.shootSound.set_volume(0.05)
		self.music = pygame.mixer.music.load("resources/audio/moonlight.wav")
		pygame.mixer.music.set_volume(0.25)
		pygame.mixer.music.play(-1, 0.0)

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
		for arrow in self.arrowList:
			self.screen.blit(arrow.image, arrow.drawPos.as_tuple())
		for badger in self.badgerList:
			self.screen.blit(badger.image, badger.drawPos.as_tuple())
		self.screen.blit(self.player.image, self.player.drawPos.as_tuple())

		killstext = self.gamefont.render(str(self.kills), False, (0,0,0))
		textrect = killstext.get_rect()
		textrect.topright = (635,35)
		self.screen.blit(killstext, textrect)

		ticks = pygame.time.get_ticks()
		timeLeft = self.wintime - ticks
		if timeLeft < 0:
			timeLeft = 0
		minutes = str(timeLeft // 60000)
		seconds = str(timeLeft // 1000 % 60)
		timetext = self.gamefont.render(minutes+":"+seconds.zfill(2), False, (0,0,0))
		textrect = timetext.get_rect()
		textrect.topright = (635,5)
		self.screen.blit(timetext, textrect)

		self.screen.blit(self.healthBarImage, (5,5))
		for i in range(self.castleHealth):
			self.screen.blit(self.healthImage, (8+i,8))

		pygame.display.flip()

	def handleEvents(self):
		"""Processes events and reacts to them."""

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit(0)
			elif event.type == pygame.KEYDOWN:
				if event.key == K_w:
					self.keys['w'] = True
				elif event.key == K_a:
					self.keys['a'] = True
				elif event.key == K_s:
					self.keys['s'] = True
				elif event.key == K_d:
					self.keys['d'] = True
			elif event.type == pygame.KEYUP:
				if event.key == K_w:
					self.keys['w'] = False
				elif event.key == K_a:
					self.keys['a'] = False
				elif event.key == K_s:
					self.keys['s'] = False
				elif event.key == K_d:
					self.keys['d'] = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				self.arrowList.append(Arrow(self.player.pos, self.player.angle))
				self.shootSound.play()
				self.shotArrows += 1

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
		else:
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

	def handleArrows(self):
		"""Updates the arrow's position attribute."""

		for arrow in self.arrowList:
			arrow.pos.x += arrow.speed * math.cos(arrow.angle)
			arrow.pos.y += arrow.speed * math.sin(arrow.angle)
			if not self.screen.get_rect().contains(pygame.Rect(arrow.pos.x, arrow.pos.y, 0, 0)):
				self.arrowList.remove(arrow)

	def handleBadgers(self):
		"""Updates the badgers' position."""

		for badger in self.badgerList:
			badrect = badger.get_rect()
			for arrow in self.arrowList:
				arrowrect = arrow.get_rect()
				if badrect.colliderect(arrowrect):
					self.badgerList.remove(badger)
					self.arrowList.remove(arrow)
					self.kills += 1
					self.enemySound.play()
					break

		for badger in self.badgerList:
			badger.move(point.Point(-badger.speed, 0))
			if badger.pos.x <= self.castleImage.get_width() + 20:
				self.badgerList.remove(badger)
				self.castleHealth -= random.randint(self.badMinDmg, self.badMaxDmg)
				self.hitSound.play()

	def badgerTimer(self):
		"""Handles the badger timer. Periodically increases the timer for badger
		spawning."""

		self.nextBadgerTimer += 1

		if self.nextBadgerTimer == self.badgerBaseTime:
			self.badgerList.append(Badger(point.Point(self.screen.get_width(), random.randint(50, 430))))
			self.nextBadgerTimer = 0
			if self.badgerBaseTime >= 30:
				self.badgerBaseTime -= 1

	def checkEndGame(self):
		"""Ends the game when the conditions are met."""

		if pygame.time.get_ticks() >= self.wintime:
			self.running = False
			self.win = True
		elif self.castleHealth <= 0:
			self.running = False
			self.win = False

	def run(self):
		"""Main game method. Call it to run the game."""

		while self.running:
			self.redrawScreen()
			self.handleEvents()
			self.movePlayer(self.player)
			self.handleArrows()
			self.handleBadgers()
			self.badgerTimer()
			self.checkEndGame()

		if self.kills < 1:
			accuracy = "{:.2f}".format(0)
		else:
			accuracy = "{:.2f}".format(self.kills/self.shotArrows*100)
		text = self.gamefont.render("Accuracy: "+accuracy+" %", False, (0,0,0))
		textrect = text.get_rect()
		textrect.centerx = self.screen.get_rect().centerx
		textrect.centery = self.screen.get_rect().centery + 24
		if self.win == True:
			self.screen.blit(self.youWinImage, (0,0))
		else:
			self.screen.blit(self.gameOverImage, (0,0))
		self.screen.blit(text, textrect)

		while True:
			pygame.display.flip()
			for event in pygame.event.get():
				if (event.type == pygame.QUIT or
					event.type == pygame.KEYDOWN or
					event.type == pygame.MOUSEBUTTONDOWN):
					pygame.quit()
					exit(0)

if __name__ == "__main__":
	game = Game()
	game.run()


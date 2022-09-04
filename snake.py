#!/usr/bin/env python3
import time
import pgzrun
from enum import Enum 
import pgzero
import pygame
import random
from random import randint

SPEED = 0.2
SEGMENT_SIZE = 40
TITLE = "Snake by Wojciech Kosikowski"
WIDTH = 30 * SEGMENT_SIZE
HEIGHT = 20 * SEGMENT_SIZE 

XGRID = 25
YGRID = 18

class State(Enum):
	MENU = 1
	PLAY = 2
	GAME_OVER = 3
	WIN = 4

class Direction(Enum):
	RIGHT = 1
	UP = 2
	LEFT = 3
	DOWN = 4


class Segment(Actor):
	def __init__(self, image):
		super().__init__(image)


class Snake :
	def __init__(self, posx, posy):
		self.posx = posx
		self.posy = posy
		self.growSnake = False
		self.snake = []
		
		
		for i in range(0,5):
			if i == 0:
				actor = Segment("head")
			else:
				actor = Segment("body")
				
			#actor._surf = pygame.transform.scale(actor._surf, (SEGMENT_SIZE, SEGMENT_SIZE))
			actor.pos = (120 + (posx - i) * SEGMENT_SIZE, 120 + posy * SEGMENT_SIZE)
			self.snake.append(actor)
	
	def len(self):
		return len(self.snake)
	
	def draw(self):
		for segment in self.snake:
			segment.draw()
		
	def move(self, direction):
		
		if direction == Direction.LEFT: self.posx -= 1
		if direction == Direction.RIGHT: self.posx += 1
		if direction == Direction.UP: self.posy -= 1
		if direction == Direction.DOWN: self.posy += 1  
		
		if self.growSnake == True:
			self.growSnake = False
			actor = Actor("body")
			#actor._surf = pygame.transform.scale(actor._surf, (SEGMENT_SIZE, SEGMENT_SIZE))
			self.snake.append(actor)
		
		for i in range(len(self.snake) - 1, 0, -1):
			self.snake[i].pos = self.snake[i - 1].pos
			
		self.snake[0].pos = (120 + self.posx * SEGMENT_SIZE, 120 + self.posy * SEGMENT_SIZE)
	
	
	def grow(self):
		self.growSnake = True
	
	def canEatApple(self, applePosx, applePosy):
		if self.posx == applePosx and self.posy == applePosy:
			return True
		return False
	
	def onItself(self):
		for i in range(1, self.len() - 1):
			if self.snake[0].pos == self.snake[i].pos:
				return True
		return False
		
	

class Game:
	def __init__(self):
		self.snake = Snake(5, 6)
		self.state = State.MENU
		self.applesEaten = 0
		self.gameRegionBox = Rect((98, 98),(44 + 25 * SEGMENT_SIZE, 44 +  15 * SEGMENT_SIZE))
		self.appleGridPosy = 6
		self.appleGridPosx = 10
		self.apple = Actor("apple")
		self.apple.pos = (120 + self.appleGridPosx * SEGMENT_SIZE, 120 + self.appleGridPosy * SEGMENT_SIZE )
		#self.apple._surf = pygame.transform.scale(self.apple._surf, (SEGMENT_SIZE, SEGMENT_SIZE))
		self.speed = 0.3
		self.moveBeep = tone.create("C4", self.speed / 2)
		self.eatBeep1 = tone.create("E3", self.speed / 3)
		self.eatBeep2 = tone.create("G3", self.speed / 2)
		
	
	def draw(self):
			self.snake.draw()
			self.apple.draw()
			
	def newApple(self):
		self.appleGridPosx = random.randint(0,25)
		self.appleGridPosy = random.randint(0,15)
		self.apple.pos = ((120 + self.appleGridPosx * SEGMENT_SIZE, 120 + self.appleGridPosy * SEGMENT_SIZE ))
		for i in self.snake.snake:
			if self.apple.pos == i.pos:
				self.newApple()
				break
		
	def move(self, direction):
		if self.state != State.PLAY:
			return
		self.moveBeep.play()
		self.snake.move(direction)
		if self.snake.canEatApple(self.appleGridPosx, self.appleGridPosy):
			self.snake.grow()
			self.newApple()
			self.speed -= 0.0015
			self.eatBeep1.play()
			self.eatBeep2.play()
			self.applesEaten += 1
		self.updateState()
	
	def updateState(self):
		if self.snake.onItself():
			self.state = State.GAME_OVER
		if self.snake.posy > 15 or self.snake.posy < 0 or self.snake.posx > 25 or self.snake.posx < 0:
			self.state = State.GAME_OVER
		if self.snake.len() >= XGRID * YGRID - 1:
			self.state = State.WIN
			
			

#=======================================================================
#=======================================================================

snakeDirection = Direction.RIGHT
lastDirectionMoved = Direction.RIGHT

def on_key_down(key):
	global snakeDirection, lastDirectionMoved, game
	if key == keys.UP:
		if lastDirectionMoved != Direction.DOWN: 
			snakeDirection = Direction.UP
	if key == keys.DOWN:
		if lastDirectionMoved != Direction.UP: 
			snakeDirection = Direction.DOWN
	if key == keys.RIGHT:
		if lastDirectionMoved != Direction.LEFT: 
			snakeDirection = Direction.RIGHT
	if key == keys.LEFT:
		if lastDirectionMoved != Direction.RIGHT: 
			snakeDirection = Direction.LEFT
	if key == keys.SPACE and game.state != State.PLAY:
		game = Game()
		game.state = State.PLAY
		snakeDirection = Direction.RIGHT
		lastDirectionMoved = Direction.RIGHT


	

def draw():
	global game
	if game.state == State.GAME_OVER:
		screen.draw.text("GAME OVER\nPRESS SPACE TO RESTART" , center=(WIDTH / 2, HEIGHT / 2), owidth=0.5, ocolor=(255,255,255), color=(255,64,0) , fontsize=60)
	if game.state == State.MENU:
		screen.fill((0, 0, 0))
		screen.draw.text("PRESS SPACE\nTO START" , center=(WIDTH / 2, HEIGHT / 2), owidth=0.5, ocolor=(255,255,255), color=(255,64,0) , fontsize=60)
	if game.state == State.PLAY :
		screen.fill((128, 128, 128))
		screen.draw.text( "Score: "+ str(game.applesEaten) , topleft=(10,10), owidth=0.2, ocolor=(0,0,0), fontsize=60)
		screen.draw.rect(game.gameRegionBox, (255, 255, 255))
		game.draw()
	if game.state == State.WIN :
		screen.draw.text("YOU WIN\nPRESS SPACE TO START OVER" , center=(WIDTH / 2, HEIGHT / 2), owidth=0.5, ocolor=(255,255,255), color=(255,64,0) , fontsize=60)
		

lastUpdateTime = time.time()			

def update():
	global lastUpdateTime, lastDirectionMoved
	if game.state == State.PLAY:
		currenTime = time.time()
		if currenTime - lastUpdateTime < game.speed:
			return
		lastUpdateTime = currenTime
		
		game.move(snakeDirection)
		lastDirectionMoved = snakeDirection
	



game = Game()

pgzrun.go()
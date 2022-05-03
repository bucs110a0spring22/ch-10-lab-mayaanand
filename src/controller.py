import sys
import pygame
import random
from src import hero
from src import enemy
import time
import math

pygame.init()

display_width = 600
display_height = 500
screen = pygame.display.set_mode( (display_width, display_height) )
fps = 60
font_ubuntumono = pygame.font.SysFont('ubuntumono', 50, True)
rock = pygame.image.load('assets/cave-painting.png').convert_alpha()
rock_width = rock.get_width()
rock_height = rock.get_height()
player = pygame.image.load('assets/wizard.png').convert_alpha()

def initialize():
    global speed_rock, rocks, playerX, playerY
    speed_rock = 2
    playerX = display_width//2
    playerY = 400
    rocks = []
    rocks.append( RockClass() )

class RockClass:
    def __init__(self):
        self.x = display_width//2
        self.y = 0

    def continueDraw(self, a, b):
        self.x += speed_rock
        self.y += speed_rock
        screen.blit( rock, (self.x, self.y) )

    def collision(self, player, playerX, playerY):
        tolerability = 5
        right_player = playerX + player.get_width() - tolerability
        left_player = playerX + tolerability
        up_player = playerY + tolerability
        right_rock = self.x + rock_width
        left_rock = self.x
        down_rock = self.y + rock_height

        #check collision
        if down_rock > up_player and ( ( left_player < left_rock and left_rock < right_player) or ( right_player > right_rock and right_rock > left_player) ):
            #delete the rock from the screen
            self.x = 5000

initialize()

def update():
    pygame.display.update()
    pygame.time.Clock().tick(fps)

def drawThings():
    #draw background
    screen.fill ( (255, 255, 255) )

    #draw rocks
    for rock2 in rocks:
        rock2.continueDraw(210, 210)

    #draw the player
    screen.blit( player, (playerX, playerY) )

running = True
#main loop
while running:

    #event loop
    for event in pygame.event.get():

        #move player
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX -= 30
            if event.key == pygame.K_RIGHT:
                playerX += 30

        #quit
        if event.type == pygame.QUIT:
            running = False

    #to generate infinite rocks
    if rocks[-1].y > 10:
        rocks.append( RockClass() )

    #check the player-rock collision
    for rock2 in rocks:
        rock2.collision(player, playerX, playerY)

    #bordo alto
    if playerX <= 0:
        playerX = 0
    if playerX >= 600:
        playerX = 600

    #update screen
    drawThings()
    update()

class Controller:
    def __init__(self, width=640, height=480):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((250, 250, 250))  # set the background to white
        pygame.font.init()  # you have to call this at the start, if you want to use this module.
        pygame.key.set_repeat(1, 50)  # initialize a held keey to act as repeated key strikes
        """Load the sprites that we need"""

        self.enemies = pygame.sprite.Group()
        num_enemies = 3
        for i in range(num_enemies):
            x = random.randrange(100, 400)
            y = random.randrange(100, 400)
            self.enemies.add(enemy.Enemy("Boogie", x, y, 'assets/enemy.png'))
        self.hero = hero.Hero("Conan", 50, 80, "assets/hero.png")
        self.all_sprites = pygame.sprite.Group((self.hero,) + tuple(self.enemies))
        self.state = "GAME"

    def mainLoop(self):
        while True:
            if(self.state == "GAME"):
                self.gameLoop()
            elif(self.state == "GAMEOVER"):
                self.gameOver()

    def gameLoop(self):
        while self.state == "GAME":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if(event.key == pygame.K_UP):
                        self.hero.move_up()
                    elif(event.key == pygame.K_DOWN):
                        self.hero.move_down()
                    elif(event.key == pygame.K_LEFT):
                        self.hero.move_left()
                    elif(event.key == pygame.K_RIGHT):
                        self.hero.move_right()

            # check for collisions
            fights = pygame.sprite.spritecollide(self.hero, self.enemies, True)
            if(fights):
                for e in fights:
                    if(self.hero.fight(e)):
                        e.kill()
                        self.background.fill((250, 250, 250))
                    else:
                        self.background.fill((250, 0, 0))
                        self.enemies.add(e)

            # redraw the entire screen
            self.enemies.update()
            self.screen.blit(self.background, (0, 0))
            if(self.hero.health == 0):
                self.state = "GAMEOVER"
            self.all_sprites.draw(self.screen)

            # update the screen
            pygame.display.flip()

    def gameOver(self):
        self.hero.kill()
        myfont = pygame.font.SysFont(None, 30)
        message = myfont.render('Game Over', False, (0, 0, 0))
        self.screen.blit(message, (self.width / 2, self.height / 2))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

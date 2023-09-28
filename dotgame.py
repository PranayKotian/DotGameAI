import pygame
import math
import numpy as np
import random
from sys import exit

class Brain:
    def __init__(self, size):
        self.directions = [0 for i in range(size)]
        self.step = 0
        
        self.randomize()

    def randomize(self):
        for i in range(len(self.directions)):
            randomAngle = 2*math.pi*random.random()
            self.directions[i] = randomAngle 

class Dot(pygame.sprite.Sprite):
    VEL = 5
    
    def __init__(self):
        super().__init__()

        self.brain = Brain(500)
        DOT = 5
        x = WIN_WIDTH/2-DOT/2
        y = WIN_HEIGHT/2-DOT/2
        
        self.move = True
        self.image = pygame.Surface([DOT, DOT])
        self.image.fill('Black')
        self.rect = self.image.get_rect(center=(x,y))
        
    def update(self):
        if self.move:
            if len(self.brain.directions) > self.brain.step:
                angle = self.brain.directions[self.brain.step]
                self.brain.step += 1

                self.rect.centerx += math.cos(angle) * self.VEL
                self.rect.centery += math.sin(angle) * self.VEL

                if not (0<= self.rect.centerx <= WIN_WIDTH and 0<= self.rect.centery <= WIN_HEIGHT):
                    self.image.fill('Red')
                    self.move = False
                    if self.rect.centerx < 0:
                        self.rect.centerx = 0
                    elif self.rect.centerx > WIN_WIDTH:
                        self.rect.centerx = WIN_WIDTH
                    elif self.rect.centery < 0:
                        self.rect.centery = 0
                    elif self.rect.centery > WIN_HEIGHT:
                        self.rect.centery = WIN_HEIGHT

class Population():
    def __init__(self, size):
        self.dots = []
        self.dot_group = pygame.sprite.Group()
        for i in range(size):
            dot = Dot()
            self.dots.append(dot)
            self.dot_group.add(dot)

pygame.init()

#Window Properties
WIN_WIDTH = 1000
WIN_HEIGHT = 1000

GOAL_WIDTH = 20
GOAL_X = WIN_WIDTH/2 - GOAL_WIDTH/2
GOAL_Y = 0
goal_image = pygame.Surface([GOAL_WIDTH, GOAL_WIDTH])
goal_image.fill('Light Green')
goal_rect = goal_image.get_rect(topleft=(GOAL_X,GOAL_Y))

def main():
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    pop = Population(1000)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()
        
        win.fill((94,129,162))


        pop.dot_group.draw(win)
        pop.dot_group.update()
        
        pygame.display.update()
        clock.tick(30)

main()
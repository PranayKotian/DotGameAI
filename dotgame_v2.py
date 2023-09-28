import pygame
import math
import random
from sys import exit

class Brain:
    def __init__(self, size):
        self.directions = [0 for i in range(size)]
        self.step = 0
        
        self.randomize()

    def randomize(self):
        for i in range(len(self.directions)):
            randomAngle = 2 * math.pi * random.random()
            self.directions[i] = randomAngle 

class Dot:
    VEL = 5

    def __init__(self, goal):
        self.brain = Brain(500)
        self.goal = goal

        DOT = 5
        x = WIN_WIDTH/2-DOT/2
        y = 100
        
        self.alive = True
        self.image = pygame.Surface([DOT, DOT])
        self.image.fill('Black')
        self.rect = self.image.get_rect(center=(x,y))

        self.fitness = 0
        self.fitnessSum = 0
        self.reachedGoal = False
    
    def move(self):
        if len(self.brain.directions) > self.brain.step:
            angle = self.brain.directions[self.brain.step]
            self.brain.step += 1
        
            self.rect.centerx += math.cos(angle) * self.VEL
            self.rect.centery += math.sin(angle) * self.VEL
        else:
            self.alive = False

    def update(self):
        if self.alive and not self.reachedGoal:
            self.move()
            if not (0<= self.rect.centerx <= WIN_WIDTH and 0<= self.rect.centery <= WIN_HEIGHT):
                self.alive = False
            elif pygame.Rect.colliderect(self.rect, self.goal.rect):
                self.image.fill('Green')
                self.reachedGoal = True
        elif not self.alive:
            self.image.fill('Red')
    
    def calculateFitness(self, goal):
        dot = [self.rect.centerx, self.rect.centery]
        distanceToGoal = math.dist(dot, goal.center)
        self.fitness = 1.0/(distanceToGoal**2)

class Population:
    def __init__(self, size, goal):
        self.dots = []
        for i in range(size):
            dot = Dot(goal)
            self.dots.append(dot)

    def update(self, win):
        for d in self.dots:
            d.update()
            win.blit(d.image, d.rect)
    
    def calculateFitness(self, goal):
        for d in self.dots:
            d.calculateFitness(goal)
    
    def allDotsDead(self):
        for d in self.dots:
            if d.alive:
                return False
        return True
    
    def naturalSelection(self):
        newDots = []

        for i in range(self.size):
            pass

    def calculateFitnessSum(self):
        self.fitnessSum = sum([d.fitness for d in self.dots])

    def selectParent(self):
        pass

class Goal:
    def __init__(self, size):
        self.image = pygame.Surface([size, size])
        self.image.fill('Light Green')
        self.center = (WIN_WIDTH/2, 50)
        self.rect = self.image.get_rect(center=self.center)

pygame.init()

#Window Properties
WIN_WIDTH = 1000
WIN_HEIGHT = 1000

def main():
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    goal = Goal(20)
    pop = Population(1000, goal)
    
    if pop.allDotsDead():
        #Genetic algorithm
        pop.calculateFitness()
        pop.naturalSelection()
        pop.mutateBabies()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()
        
        win.fill((94,129,162))

        pop.update(win)
        win.blit(goal.image, goal.rect)

        pygame.display.update()
        clock.tick(30)

main()

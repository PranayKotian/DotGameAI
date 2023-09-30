import pygame
import math
import random
#import copy
from sys import exit

class Brain:
    def __init__(self, size):
        self.size = size
        self.directions = [2*math.pi*random.random() for i in range(self.size)]
        self.step = 0

    def clone(self):
        clone = Brain(self.size)
        clone.directions = self.directions.copy()
        return clone
    
    def mutate(self):
        mutationRate = 0.01 #Probability that vector in directions gets changed

        #LIST COMP W/ IF/ELSE: [f(x) if condition else g(x) for x in sequence]
        self.directions = [2*math.pi*random.random() if random.random()<mutationRate else d for d in self.directions]
        
        # for i in range(len(self.directions)):
        #     if random.random() < mutationRate:
        #         #Randomize direction
        #         self.directions[i] = 2*math.pi*random.random()

class Dot:
    VEL = 20

    def __init__(self, goal):
        DOT = 5
        x = WIN_WIDTH/2-DOT/2
        y = WIN_HEIGHT - 100

        self.image = pygame.Surface([DOT, DOT])
        self.image.fill('Black')
        self.rect = self.image.get_rect(center=(x,y))

        self.brain = Brain(1000)
        self.goal = goal
        
        self.alive = True
        self.reachedGoal = False
        self.isBest = False #True if this dot is best dot from previous generation

        self.fitness = 0
        self.fitnessSum = 0
        
    def move(self):
        if len(self.brain.directions) > self.brain.step:
            angle = self.brain.directions[self.brain.step]
            self.rect.centerx += math.cos(angle) * self.VEL
            self.rect.centery += math.sin(angle) * self.VEL 

            self.brain.step += 1
        else:
            self.alive = False

    def update(self):
        if self.alive and not self.reachedGoal:
            self.move()
            if not (0<= self.rect.centerx <= WIN_WIDTH and 0<= self.rect.centery <= WIN_HEIGHT):
                self.alive = False
            elif pygame.Rect.colliderect(self.rect, self.goal.rect):
                self.image.fill('Dark Green')
                self.reachedGoal = True
        elif not self.alive:
            self.image.fill('Red')
    
    def calculateFitness(self, goal):
        if self.reachedGoal:
            self.fitness = 1.0/16.0 + 10000.0/(self.brain.step**2)
        else:
            dot = [self.rect.centerx, self.rect.centery]
            distanceToGoal = math.dist(dot, (WIN_WIDTH/2, 50))
            self.fitness = 1.0/(distanceToGoal**3)

    def createChild(self):
        baby = Dot(self.goal)
        baby.brain = self.brain.clone() #Child has same brain as parent
        return baby

class Population:
    def __init__(self, size, goal):
        self.dots = []
        self.size = size

        self.fitnessSum = 0
        self.gen = 1
        self.bestDot = 0 #Index of best dot in self.dots
        self.minStep = 1000

        for i in range(size):
            dot = Dot(goal)
            self.dots.append(dot)

    def update(self, win):
        for i in range(len(self.dots)):
            if self.dots[i].brain.step > self.minStep:
                self.dots[i].alive = False
            
            self.dots[i].update()
            win.blit(self.dots[i].image, self.dots[i].rect)
    
    def calculateFitness(self, goal):
        for i in range(len(self.dots)):
            self.dots[i].calculateFitness(goal)
    
    def allDotsDead(self):
        for i in range(len(self.dots)):
            if self.dots[i].alive and not self.dots[i].reachedGoal:
                return False
        return True
    
    def naturalSelection(self):
        newDots = [0 for i in range(len(self.dots))]
        self.setBestDot()
        self.calculateFitnessSum()

        newDots[0] = self.dots[self.bestDot].createChild()
        newDots[0].isBest = True

        for i in range(1, len(newDots)):
            #Select parent based on fitness
            parent = self.selectParent()
            #Get baby from parent (i.e. clone parent)
            newDots[i] = parent.createChild()
        
        self.dots = newDots.copy()
        self.gen += 1 
        print(f"generation: {self.gen}")

    def calculateFitnessSum(self):
        self.fitnessSum = sum([d.fitness for d in self.dots])
        print(f"fitness sum: {self.fitnessSum}")

    #Randomly returns dot from population (based on fitness)
    def selectParent(self):
        rand = random.random()*self.fitnessSum
        runningSum = 0

        for i in range(len(self.dots)):
            runningSum += self.dots[i].fitness
            if runningSum > rand:
                return self.dots[i]
    
    def mutateBabies(self):
        for i in range(1, len(self.dots)):
            self.dots[i].brain.mutate()

    def setBestDot(self):
        max = 0.0
        maxIndex = 0
        for i in range(len(self.dots)): 
            if self.dots[i].fitness > max:
                max = self.dots[i].fitness
                maxIndex = i
        
        self.bestDot = maxIndex

        if self.dots[self.bestDot].reachedGoal:
            self.minStep = self.dots[self.bestDot].brain.step

class Goal:
    def __init__(self, size):
        self.image = pygame.Surface([size, size])
        self.image.fill('Green')
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

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()
        
        if pop.allDotsDead():
            #Genetic algorithm
            pop.calculateFitness(goal)
            pop.naturalSelection()
            pop.mutateBabies()

        win.fill("Light Grey")

        pop.update(win)
        win.blit(goal.image, goal.rect)

        pygame.display.update()
        clock.tick(100)

main()

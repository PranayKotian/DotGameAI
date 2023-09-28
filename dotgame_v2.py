import pygame
import math
import random
from sys import exit

class Brain:
    def __init__(self, size):
        self.size = size
        self.directions = [2*math.pi*random.random() for i in range(self.size)]
        self.step = 0
        #self.randomize()

    """def randomize(self):
        self.directions = [2*math.pi*random.random() for i in range(self.size)]

        # for d in self.directions:
        #     randomAngle = 2 * math.pi * random.random()
        #     d = randomAngle """

    def clone(self):
        clone = Brain(self.size)
        clone.directions = self.directions.copy()
        return clone
    
    def mutate(self):
        mutationRate = 0.01 #Probability that vector in directions gets changed

        #LIST COMP W/ IF/ELSE: [f(x) if condition else g(x) for x in sequence]
        #self.directions = [2*math.pi*random.random() if random()<mutationRate else d for d in self.directions]
        
        for d in self.directions:
            rand = random()
            if rand < mutationRate:
                #Randomize direction
                randomAngle = 2 * math.pi * random.random()
                d = randomAngle

class Dot:
    VEL = 5

    def __init__(self, goal):
        DOT = 5
        x = WIN_WIDTH/2-DOT/2
        y = 100

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
        angle = self.brain.directions[self.brain.step]
        self.rect.centerx += math.cos(angle) * self.VEL
        self.rect.centery += math.sin(angle) * self.VEL

        if len(self.brain.directions) > self.brain.step:
            self.brain.step += 1 
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

    def createChild(self):
        baby = Dot(self.goal)
        baby.brain = self.brain.clone() #Child has same brain as parent
        return baby

class Population:
    def __init__(self, size, goal):
        self.dots = []

        self.fitnessSum = 0
        self.gen = 1
        self.bestDot = 0 #Index of best dot in self.dots
        self.minStep = 1000

        for i in range(size):
            dot = Dot(goal)
            self.dots.append(dot)

    def update(self, win):
        for d in self.dots:
            if d.brain.step > self.minStep:
                d.alive = False
            
            d.update()
            win.blit(d.image, d.rect)
    
    def calculateFitness(self, goal):
        for d in self.dots:
            d.calculateFitness(goal)
    
    def allDotsDead(self):
        for d in self.dots:
            if d.alive and not d.reachedGoal:
                return False
        return True
    
    def naturalSelection(self):
        newDots = []
        self.setBestDot()
        self.calculateFitnessSum()

        newDots.append(self.dots[self.bestDot].createChild())
        newDots[0].isBest = True

        for i in range(self.size):
            #Select parent based on fitness
            parent = self.selectParent()
            #Get baby from parent (i.e. clone parent)
            newDots.append(parent.createChild())
        
        self.dots = newDots.copy()
        self.gen += 1 

    def calculateFitnessSum(self):
        self.fitnessSum = sum([d.fitness for d in self.dots])

    #Randomly returns dot from population (based on fitness)
    def selectParent(self):
        rand = random(self.fitnessSum)
        runningSum = 0

        for d in self.dots:
            runningSum += d.fitness
            if runningSum > rand:
                return d
    
    def mutateBabies(self):
        for d in self.dots:
            d.brain.mutate()

    def setBestDot(self):
        max = 0.0
        maxIndex = 0
        for i, d in enumerate(self.dots): 
            if d.fitness > max:
                max = d.fitness
                maxIndex = i
        
        self.bestDot = maxIndex

        if self.dots[self.bestDot].reachedGoal:
            self.minStep = self.dots[self.bestDot].brain.step
            print(f"step: {self.minStep}")

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

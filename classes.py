from shapes import *
from random import *
from math import *
import numpy as np

class Ship:
    def __init__(self, pos, r):
        self.pos = pos
        self.r = r
        self.vel = np.array([.0, .0])
        self.size = 25
        self.maxThrust = 0.5
        self.thrust = 0
        self.maxV = 15
        self.fuel = 50
        self.bulletCost = 3
        self.age = 0
    def think(self, ships, bullets, foods, camera):
        sensor = self.sense(ships, foods, camera)
        enemies = sensor[0]
        foodsDetected = sensor[1]
        self.thrust = 0
        if self.fuel > 10:
            self.thrust = self.maxThrust / 3
        if random() < 0.03:
            self.r += 0.4
        if random() < 0.03:
            self.r -= 0.4
        if sum(enemies) > 0.5:
            self.r += 0.05
            self.thrust = self.maxThrust
        if enemies[0] > 0 and random() < 0.5:
            self.shoot(bullets)
        if sum(foodsDetected) > 0:
            self.thrust = self.maxThrust
    def update(self):
        i.age += 1
        i.fuel -= 0.05
        if self.fuel > self.thrust:
            self.vel -= np.array([sin(self.r), cos(self.r)]) * self.thrust
            self.fuel -= self.thrust
        self.vel *= 0.98
        if hypot(self.vel[0], self.vel[1]) > self.maxV:
            self.vel = self.vel / hypot(self.vel[0], self.vel[1]) * self.maxV
        self.pos += self.vel
    def sense(self, ships, foods, camera):
        enemies = [.0]*12
        foodsDetected = [.0]*12
        for ray in range(12):
            ang = - self.r + pi*2/12 * ray - pi/2
            for segment in range(1, 6):
                dx = cos(ang) * segment * 50
                dy = sin(ang) * segment * 50
                #if segment == 5: text( str(ray), self.pos[0]+dx, self.pos[1]+dy, 20, camera)
                for ship in ships:
                    if id(ship) != id(self):
                        d = sqrt(pow(ship.pos[0]-(self.pos[0]+dx), 2)+pow(ship.pos[1]-(self.pos[1]+dy), 2))
                        if d < ship.size:
                            if enemies[ray] == .0:
                                enemies[ray] = int( (6-segment)/5 * 10)/10
                for food in foods:
                    d = sqrt(pow(food.pos[0]-(self.pos[0]+dx), 2)+pow(food.pos[1]-(self.pos[1]+dy), 2))
                    if d < food.size*5:
                        if foodsDetected[ray] == .0:
                            foodsDetected[ray] = int( (6-segment)/5 * 10)/10
        return [enemies, foodsDetected]
    def shoot(self, bullets):
        if self.fuel > self.bulletCost:
            point = np.array([sin(self.r + pi), cos(self.r + pi)]) * self.size + self.pos
            bullets.append(Bullet(point, point-self.pos, id(self)))
            self.fuel -= self.bulletCost
    def render(self, camera):
        point1 = np.array([sin(self.r + pi), cos(self.r + pi)]) * self.size + self.pos
        point2 = np.array([sin(self.r+pi*2+pi/4), cos(self.r+pi*2+pi/4)]) * self.size + self.pos
        point3 = np.array([sin(self.r+pi*2-pi/4), cos(self.r+pi*2-pi/4)]) * self.size + self.pos
        point4 = np.array([sin(self.r), cos(self.r)]) * 6  + self.pos
        point5 = np.array([sin(self.r), cos(self.r)]) * 10  + self.pos
        line(point1[0], point1[1], point2[0], point2[1], camera)
        line(point2[0], point2[1], self.pos[0], self.pos[1], camera)
        line(point3[0], point3[1], self.pos[0], self.pos[1], camera)
        line(point1[0], point1[1], point3[0], point3[1], camera)
        circle(point4[0], point4[1], (self.thrust/self.maxThrust)*5, camera)
        circle(point5[0], point5[1], (self.thrust/self.maxThrust)*4, camera)
        text( 'fuel: '+str(int(self.fuel*10)/10), self.pos[0]+15, self.pos[1]+15, 15, camera)
        text( 'trust: '+str(int(self.thrust*10)/10), self.pos[0]+15, self.pos[1]+30, 15, camera)
        text( 'age: '+str(self.age), self.pos[0]+15, self.pos[1]+45, 15, camera)

class Bullet:
    def __init__(self, pos, vel, id):
        self.pos = pos
        self.vel = vel
        self.id = id
        self.size = 3
    def update(self):
        self.pos += self.vel
    def render(self, camera):
        circle(self.pos[0], self.pos[1], self.size, camera)

class Food:
    def __init__(self, pos):
        self.pos = pos
        self.size = 6
    def render(self, camera):
        circle(self.pos[0], self.pos[1], self.size, camera)
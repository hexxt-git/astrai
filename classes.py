from shapes import *
from random import *
from math import *
import numpy as np

def sigmoid(x):
    if x > 100: return 1
    if x < -100: return 0
    return 1 / ( 1 + pow(e, -x))

def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y'][magnitude])

class Ship:
    def __init__(self, pos, r, network, color):
        self.pos = pos
        self.vr = 0
        self.r = r
        self.vel = np.array([.0, .0])
        self.size = 25
        self.thrust = 0
        self.maxV = 18
        self.turnSpeed = 0.5
        self.fuel = 50 + random()*30
        self.bulletCost = 25
        self.age = 0
        self.rays = 16
        self.segments = 5
        self.segmentSize = 80
        self.network = network
        self.color = color
        self.kills = 0
        self.eats = 0
        self.traveled = 0
    def think(self, ships, bullets, foods, camera):
        sensors = self.sense(ships, foods, camera)
        inputs = sensors[0] + sensors[1] + [self.thrust, self.fuel, self.r, self.vel[0], self.vel[1], random()*8-4]
        calculated = []
        for layer in range(4):
            calculated.append([])
            if layer <= 2:
                for node in range(16):
                    calc = self.network[1][layer][node]
                    if layer == 0:
                        for inp in range(26):
                            calc += self.network[0][layer][node][inp] * inputs[inp]
                    if layer == 1 or layer == 2:
                        for inp in range(16):
                            calc += self.network[0][layer][node][inp] * calculated[0][inp]
                    calculated[layer].append(sigmoid(calc))
            if layer == 3:
                for node in range(3):
                    calc = self.network[1][layer][node]
                    for inp in range(16):
                        calc += self.network[0][layer][node][inp] * calculated[1][inp]
                    calculated[layer].append(sigmoid(calc))

        self.thrust = calculated[3][0] * 3
        self.vr = ( calculated[3][1]*2 - 1) * self.turnSpeed
        if calculated[3][2] > 0.5: self.shoot(bullets)

    def score(self):
        return pow(self.age, 1) * pow(self.kills+1, 1.3) * pow(self.eats+1, 2) * pow(self.traveled, 1.3)

    def update(self):
        while self.r > pi*2: self.r -= pi*2
        while self.r < 0: self.r += pi*2
        self.age += 1
        self.fuel -= 0.05

        self.r += self.vr
        self.fuel -= abs(self.vr / 2)

        self.vel -= np.array([sin(self.r), cos(self.r)]) * self.thrust
        self.fuel -= self.thrust / 4

        self.vel *= 0.98
        if hypot(self.vel[0], self.vel[1]) > self.maxV:
            self.vel = self.vel / hypot(self.vel[0], self.vel[1]) * self.maxV
        self.pos += self.vel
        self.traveled += hypot(self.vel[0], self.vel[1])
        
    def sense(self, ships, foods, camera):
        enemies = [.0]*self.rays
        foodsDetected = [.0]*self.rays
        for ray in range(self.rays):
            ang = - self.r + pi*2/self.rays * ray - pi/2
            for segment in range(1, self.segments):
                dx = cos(ang) * segment * self.segmentSize
                dy = sin(ang) * segment * self.segmentSize
                #if segment == self.segments-1: text( str(ray), self.pos[0]+dx, self.pos[1]+dy, 20, camera)
                #circle( self.pos[0]+dx, self.pos[1]+dy, 4, camera)
                for ship in ships:
                    if id(ship) != id(self):
                        d = sqrt(pow(ship.pos[0]-(self.pos[0]+dx), 2)+pow(ship.pos[1]-(self.pos[1]+dy), 2))
                        if d < ship.size:
                            if enemies[ray] == .0:
                                enemies[ray] = int( (self.segments-segment)/5 * 10)/10
                for food in foods:
                    d = sqrt(pow(food.pos[0]-(self.pos[0]+dx), 2)+pow(food.pos[1]-(self.pos[1]+dy), 2))
                    if d < 50:
                        if foodsDetected[ray] == .0:
                            foodsDetected[ray] = int( (self.segments-segment)/5 * 10)/10
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
        circle(point4[0], point4[1], self.thrust/3*5, camera)
        circle(point5[0], point5[1], self.thrust/3*4, camera)
        text( 'fuel: '+str(int(self.fuel*10)/10), self.pos[0]+15, self.pos[1]+15, 15, camera)
        text( 'thrust: '+str(int(self.thrust*10)/10), self.pos[0]+15, self.pos[1]+30, 15, camera)
        text( 'age: '+str(self.age), self.pos[0]+15, self.pos[1]+45, 15, camera)
        text( 'eaten: '+str(self.eats), self.pos[0]+15, self.pos[1]+60, 15, camera)
        text( 'kills: '+str(self.kills), self.pos[0]+15, self.pos[1]+75, 15, camera)
        text( 'breeding: '+str(human_format(self.score())), self.pos[0]+15, self.pos[1]+90, 15, camera)

class Bullet:
    def __init__(self, pos, vel, id):
        self.pos = pos
        self.vel = vel
        self.id = id
        self.size = 3
    def update(self):
        self.pos += self.vel * 2
    def render(self, camera):
        circle(self.pos[0], self.pos[1], self.size, camera)

class Food:
    def __init__(self, pos):
        self.pos = pos
        self.size = 6
    def render(self, camera):
        circle(self.pos[0], self.pos[1], self.size, camera)
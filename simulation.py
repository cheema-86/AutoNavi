import pygame
import math
import tracks

# pygame initialization
pygame.init()

class SimAI:

    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 720)) # set screen size
        # car image
        self.IMG = pygame.image.load("assets/car.png").convert_alpha()
        self.IMG = pygame.transform.scale(self.IMG, (50, 25)) # resize image
        self.clock = pygame.time.Clock() # need this to limit FPS
        self.running = True
        self.reset()


    def reset(self):
        # sprite definitions
        self.car = pygame.sprite.GroupSingle(Vehicle(self.IMG))
        self.track = pygame.sprite.Group()
        self.sight = pygame.sprite.Group()
        self.rewards = pygame.sprite.Group()

        self.add_sight(self.car)

        # replace with a make_track function
        for barrier in tracks.maze:
            self.track.add(Barrier(*barrier))   
        
        for gate in tracks.mazeR:
            self.rewards.add(Barrier(*gate, color="green")) 

        self.score = 0

    def add_sight(self,car): 
        # vision dots
        self.sight.add(Vision(car.sprite, 0))
        self.sight.add(Vision(car.sprite, 45))
        self.sight.add(Vision(car.sprite, -45))
        self.sight.add(Vision(car.sprite, 90))
        self.sight.add(Vision(car.sprite, -90))
        self.sight.add(Vision(car.sprite, 180))

    def play_step(self,action):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        self.screen.fill("black") 

        self.car.update(action, self.IMG)
        self.car.draw(self.screen)
        self.sight.update(self.car.sprite, self.track)
        self.sight.draw(self.screen)
        self.track.draw(self.screen)

        # ml parameters
        reward = 0
        game_over = False

        # collision detection
        for barrier in self.track: # this is the collision detection
            if pygame.sprite.collide_rect(self, barrier):
                barrier.image.fill("red")
                game_over = True
                reward = -10
                return reward, game_over, self.score
            
        for gate in self.rewards:
            if pygame.sprite.collide_rect(self, gate):
                self.score += 1
                reward = 10
                gate.kill()

        pygame.display.flip() #render frame
        self.clock.tick(60)  # limits FPS to 60

        return reward, game_over, self.score


#this is our car
class Vehicle(pygame.sprite.Sprite):
    def __init__(self,IMG):
        super().__init__() # initialize Sprite

        self.image = IMG
        self.rect = self.image.get_rect()

        self.max_vel = 20
        self.vel = 0
        self.rotation_vel = 3
        self.angle = 0
        self.x, self.y = (100,100)
        self.acceleration = 0.2

    def input(self, action): # get user input
        # [up, down, left, right]
        if action[0]:
            self.accelerate()
        elif action[1]:
            self.brake()
        if action[2]:
            self.turn_left()
        elif action[3]:
            self.turn_right()

    def accelerate(self):
        self.vel += self.acceleration
        self.vel = max(-self.max_vel, min(self.vel, self.max_vel)) # weird janky way to limit velocity

    def brake(self):
        self.vel -= self.acceleration
        self.vel = max(-self.max_vel, min(self.vel, self.max_vel)) # weird janky way to limit velocity

    def turn_right(self):
        if self.vel > 1:
            self.angle += self.rotation_vel
        elif self.vel < -1: # for some reason I need to reverse the rotation when going backwards
            self.angle -= self.rotation_vel*0.5

    def turn_left(self):
        if self.vel > 1:
            self.angle -= self.rotation_vel
        elif self.vel < -1: # for some reason I need to reverse the rotation when going backwards
            self.angle += self.rotation_vel*0.5

    def update(self, action, IMG): # needed to pass on the barriers for collision detection
        self.input(action)
        self.vel *= 0.95 # friction

        self.x += self.vel * math.cos(math.radians(self.angle)) # big math stuff
        self.y += self.vel * math.sin(math.radians(self.angle))

        self.rect.center = (self.x, self.y) # this sets the location of the car
        self.image = pygame.transform.rotate(IMG, -self.angle) # puts the image, idk why but I needed the negative angle



class Vision(pygame.sprite.Sprite): #wanda ded
    def __init__(self, car, offset):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill("green")
        self.rect = self.image.get_rect()
        self.rect.center = (car.x,car.y)
        self.angle = car.angle
        self.offset = offset

    def update(self, car, barriers):
        self.x = car.x + math.cos(math.radians(car.angle+self.offset)) * 70
        self.y = car.y + math.sin(math.radians(car.angle+self.offset)) * 70
        self.rect.center = (self.x, self.y)

        for barrier in barriers: # this is the collision detection
            if pygame.sprite.collide_rect(self, barrier):
                self.image.fill("red")
                break
        else:
            self.image.fill("green")



# this is our barriers
class Barrier(pygame.sprite.Sprite):
    def __init__(self, x, y, length, rotation, color="white"):
        super().__init__()
        if rotation == 0: # horizontal or vertical
            self.length = length
            self.width = 10
        else:
            self.length = 10
            self.width = length
        self.image = pygame.Surface((self.length, self.width))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

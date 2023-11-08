import pygame
import math
import tracks

# pygame initialization
pygame.init()
screen = pygame.display.set_mode((1280, 720)) # set screen size
clock = pygame.time.Clock() # need this to limit FPS
running = True 

# car image
IMG = pygame.image.load("assets/car.png").convert_alpha()
IMG = pygame.transform.scale(IMG, (50, 25)) # resize image


#this is our car
class Vehicle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() # initialize Sprite

        self.image = IMG
        self.rect = self.image.get_rect()

        self.max_vel = 20
        self.vel = 0
        self.rotation_vel = 3
        self.angle = 0
        self.x, self.y = (100,100)
        self.acceleration = 0.2

    def input(self): # get user input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.accelerate()
        elif keys[pygame.K_DOWN]:
            self.brake()
        if keys[pygame.K_LEFT]:
            self.turn_left()
        elif keys[pygame.K_RIGHT]:
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

    def update(self, barriers): # needed to pass on the barriers for collision detection
        self.input()
        self.vel *= 0.95 # friction

        self.x += self.vel * math.cos(math.radians(self.angle)) # big math stuff
        self.y += self.vel * math.sin(math.radians(self.angle))

        self.rect.center = (self.x, self.y) # this sets the location of the car
        self.image = pygame.transform.rotate(IMG, -self.angle) # puts the image, idk why but I needed the negative angle

        for barrier in barriers: # this is the collision detection
            if pygame.sprite.collide_rect(self, barrier):
                barrier.image.fill("red")
                # This is where you get game over
                break


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
    def __init__(self, x, y, length, rotation):
        super().__init__()
        if rotation == 0: # horizontal or vertical
            self.length = length
            self.width = 10
        else:
            self.length = 10
            self.width = length
        self.image = pygame.Surface((self.length, self.width))
        self.image.fill("white")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)


# sprite definitions
car = pygame.sprite.GroupSingle(Vehicle())
track = pygame.sprite.Group()
sight = pygame.sprite.Group()

# vision dots
sight.add(Vision(car.sprite, 0))
sight.add(Vision(car.sprite, 45))
sight.add(Vision(car.sprite, -45))
sight.add(Vision(car.sprite, 90))
sight.add(Vision(car.sprite, -90))
sight.add(Vision(car.sprite, 180))

# replace with a make_track function
for barrier in tracks.maze:
    track.add(Barrier(*barrier))

#main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("black") 

    car.update(track) # pass on the barriers to the car
    car.draw(screen)
    sight.update(car.sprite, track)
    sight.draw(screen)
    track.draw(screen)


    pygame.display.flip() #render frame
    clock.tick(60)  # limits FPS to 60

pygame.quit()
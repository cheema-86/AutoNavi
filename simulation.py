import pygame
import math
import tracks

# pygame initialization
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True


IMG = pygame.image.load("assets/car.png").convert_alpha()
IMG = pygame.transform.scale(IMG, (50, 25))


class Vehicle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = IMG
        self.rect = self.image.get_rect()

        self.max_vel = 20
        self.vel = 0
        self.rotation_vel = 3
        self.angle = 0
        self.x, self.y = (100,100)
        self.acceleration = 0.2

    def input(self):
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
        self.vel = max(-self.max_vel, min(self.vel, self.max_vel))

    def brake(self):
        self.vel -= self.acceleration
        self.vel = max(-self.max_vel, min(self.vel, self.max_vel))

    def turn_right(self):
        if -1 < self.vel > 1:
            self.angle += self.rotation_vel

    def turn_left(self):
        if -1 < self.vel > 1:
            self.angle -= self.rotation_vel

    def update(self):
        self.input()
        self.vel *= 0.95 # friction


        self.x += self.vel * math.cos(math.radians(self.angle))
        self.y += self.vel * math.sin(math.radians(self.angle))

        self.rect.center = (self.x, self.y)
        self.image = pygame.transform.rotate(IMG, -self.angle)


class Barrier(pygame.sprite.Sprite):
    def __init__(self, x, y, length, rotation):
        super().__init__()
        if rotation == 0:
            self.length = length
            self.width = 10
        else:
            self.length = 10
            self.width = length
        self.image = pygame.Surface((self.length, self.width))
        self.image.fill("white")
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)



car = pygame.sprite.GroupSingle(Vehicle())
track = pygame.sprite.Group()

track.add(Barrier(100, 50, 1000, 0))
track.add(Barrier(50, 100, 1000, 1))
track.add(Barrier(200, 500, 1000, 0))
track.add(Barrier(500, 200, 1000, 1))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("black") 

    car.update()
    car.draw(screen)
    track.draw(screen)

    pygame.display.flip() #render frame
    clock.tick(60)  # limits FPS to 60

pygame.quit()
import pygame

class vehicle:
    def __init__(self):
        self.max_vel = 10
        self.vel = 0
        self.rotation_vel = 5
        self.angle = 0
        self.x, self.y = (100,100)
        self.acceleration = 0.1

# pygame initialization
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("black") 




    pygame.display.flip() #render frame
    clock.tick(60)  # limits FPS to 60

pygame.quit()
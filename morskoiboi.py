import pygame

pygame.init()

screen = pygame.display.set_mode((640, 480))


clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    clock.tick(60)
    
    screen.fill((0, 0, 0))
    
    
    pygame.display.flip()
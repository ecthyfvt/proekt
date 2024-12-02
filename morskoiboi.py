import pygame


field_size = 10

ship_count = {1:4, 2:3, 3:2, 4:1, } # количества n-клеточных кораблей






def init_field(): # создать квадратное поле размера size
  global field, field_size
  field = [[0 for j in range(field_size)] for i in range(field_size)]
  


def place_ships():
  pass


pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()


init_field() # создание игрового поля

place_ships()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    clock.tick(60)
    
    screen.fill((0, 0, 0))
    
    
    pygame.display.flip()
import pygame


field_width = 10
field_height = 10
ship_count = [4,3,2,1] # количества (n+1)-клеточных кораблей

cell_width = 40 # размер клетки




def init_field(): # создать поле заданной ширины и высоты
    global field, field_width, field_height
    field = [['empty' for j in range(field_width)] for i in range(field_height)]
    



def place_all_ships(): # функция чтобы поставить корабли на поле
    # надо разместить сначала самый длинный корабль
    # потом корабль поменьше на свободное место
    # потом еще меньше до самого маленького
    pass
  
  
  
  
  
def place_ship(ship_size): # поставить один корабль
    global field
    available_positions = [] # создаем список возможных позиций
    # в нем будут такие параметры как положение верхней левой клетки корабля и направление корабля (вертикально или горизантально)







def render():
    global field, cell_width
    
    for y, row in enumerate(field):
        for x, cell in enumerate(row):
            pygame.draw.rect(screen, (255,255,255), (20+30*x,20+30*y, cell_width,cell_width))
        








pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()


init_field() # создание игрового поля

place_all_ships()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    clock.tick(60)
    
    render()
    
    pygame.display.flip()
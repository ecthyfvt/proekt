import pygame


field_width = 3
field_height = 3
ship_count = [4,3,2,1] # количества (n+1)-клеточных кораблей

cell_size = 180 # размер клетки
border_size = 100 # толщина границы между клетками
offset = 0 # расстояние от края окна



color = [(40, 138, 138), (255, 255, 255)]
# цвет клетки с нулем будет такой 
# по мере добавления кораблей добавим сюда цвета



def init_field(): # создать поле заданной ширины и высоты
    global field, field_width, field_height
    field = [[0 for j in range(field_width)] for i in range(field_height)]
    # в клетках таблицы ноль если пусто и номер корабля если он там




def place_all_ships(): # функция чтобы поставить корабли на поле
    # надо разместить сначала самый длинный корабль
    # потом корабль поменьше на свободное место
    # потом еще меньше до самого маленького
    pass
  
  
  
  
  
def place_ship(ship_size): # поставить один корабль
    global field
    available_positions = [] # создаем список возможных позиций
    # в нем будут такие параметры как положение верхней левой клетки корабля и направление корабля (вертикально или горизантально)




def get_clicked_cell(pos):
    global cell_size, border_size, offset, field_width, field_height
    # проверка что точка внутри поля
    if offset < pos[0] < offset + field_width * cell_size + (field_width-1) * border_size and offset < pos[1] < offset + field_height * cell_size + (field_height-1) * border_size:
        # проверка что попадает на клетку
        if (pos[0] - offset) % (cell_size + border_size) < cell_size and 0 < (pos[1] - offset) % (cell_size + border_size) < cell_size:
            
            px = (pos[0] - offset) // (cell_size + border_size)
            py = (pos[1] - offset) // (cell_size + border_size)
            
        else:
            px = None
            py = None
    else:
        px = None
        py = None
    return (px, py)






def render():
    global field, cell_size, border_size, offset
    
    for y, row in enumerate(field):
        for x, cell in enumerate(row):
            pygame.draw.rect(screen, color[cell], (offset + x*(cell_size + border_size), offset + y*(cell_size + border_size), cell_size, cell_size))
        






def process_click(cell): # дает ошибку list index out of range
    global field
    
    # если нажали на клетку
    if cell[0] != None and cell[1] != None:
        
        # переключить состояние клетки 0 <-> 1
        field[cell[1]][cell[0]] = 1 - field[cell[1]][cell[0]]






pygame.init()


#
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
my_font = pygame.font.SysFont('Comic Sans MS', 40)


#




screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()


init_field() # создание игрового поля

place_all_ships()


pos = 0
clicked_cell = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN or True:
            pos = pygame.mouse.get_pos()
            
            clicked_cell = get_clicked_cell(pos)
            # process_click(clicked_cell)
            
    
    clock.tick(60)
    
    screen.fill((0,0,0))
    
    render()
    
    #
    
    
    
    text_surface = my_font.render(str(pos) + '   ' + str(clicked_cell), False, (0, 255, 0))

    screen.blit(text_surface, (0,0))
    
    
    
    
    
    #
    
    
    
    
    pygame.display.flip()
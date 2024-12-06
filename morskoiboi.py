import pygame
import random


field_width = 10
field_height = 10
ship_count = [4,3,2,1] # количества (n+1)-клеточных кораблей

cell_size = 95 # размер клетки
border_size = 10 # толщина границы между клетками
offset = 0 # расстояние от края окна






def init_field(): # создать поле заданной ширины и высоты
    global field, field_width, field_height
    field = [[{'id':0, 'opened':1} for j in range(field_width)] for i in range(field_height)]
    # в клетках таблицы код клетки
    # 0 если пусто и натур. число если корабль, у каждого будет свой номер
    # и статус открытия, чтобы знать что рисовать 




def get_color(cell):
    global colors
    if cell['opened']:
        if cell['id'] == 0:
            return (20, 20, 20)
        else:
            return colors[cell['id']-1]
    else:
        return  (104, 104, 104)





def place_all_ships(): 
    # функция чтобы поставить корабли на поле
    # надо разместить сначала самы#й длинный корабль
    # потом корабль поменьше
    # на свободное место
    # потом еще меньше до самого маленького
    global colors
    colors = []
    for size, count in enumerate(ship_count[::-1]): # для всех размеров кораблей с самого большого
        for i in range(count): # для каждого корабля
            place_ship(len(ship_count)-size)
    pass







def has_empty_nbh(x,y):
    global field, field_width, field_height
    # смещение в стороны
    ds = [(-1,-1), (-1, 0), (-1, 1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    
    for d in ds:
        if in_field(x + d[0], y + d[1]): # если в клетку можно сместиться
            if field[y+d[1]][x+d[0]]['id'] != 0: # и она не пустая
                return False # тест на отсутствие кораблей не пройден
    
    # прошли по всем ds и все ок
    return True
    
    



def in_field(x,y):
    global field_width, field_height
    return (0 <= x <= field_width - 1) and (0 <= y <= field_height - 1)





def place_ship(ship_size): # поставить один корабль
    global field, colors
    
    available_positions = [] # создаем список возможных позиций
    # в нем будут положение верхней левой клетки корабля и направление корабля (вертикально или горизонтально)
    # тут код для вычислений:
    
    # проходим по каждой клетке поля
    for y, row in enumerate(field):
        for x, cell in enumerate(row):
            
            # проверка горизонтального положения
            is_good_position = None
            for dx in range(ship_size): # для смещения на 0, 1 ... клетку от исходной
                if in_field(x + dx, y):
                    if has_empty_nbh(x + dx, y) and field[y][x+dx]['id'] == 0:
                        if is_good_position != False:
                            is_good_position = True
                    else:
                        is_good_position = False
                        
                else:
                    is_good_position = False
                    
            if is_good_position:
                available_positions.append((x,y,'h'))
            
            # проверка вертикального положения
            is_good_position = None
            for dy in range(ship_size):
                if in_field(x, y + dy):
                    if has_empty_nbh(x, y + dy) and field[y+dy][x]['id'] == 0:
                        if is_good_position != False:
                            is_good_position = True
                    else:
                        is_good_position = False
                        
                else:
                    is_good_position = False
                    
            if is_good_position:
                available_positions.append((x,y,'v'))
    
    
    if len(available_positions) > 0:
        colors.append((random.randint(50,255), random.randint(50,255), random.randint(50,255)))
        id = len(colors)
        pos = random.choice(available_positions)
        if pos[2] == 'h':
            for dx in range(ship_size):
                field[pos[1]][pos[0] + dx]['id'] = id
        else:
            for dy in range(ship_size):
                field[pos[1] + dy][pos[0]]['id'] = id
    
    
    
    
def get_clicked_cell(pos):
    global cell_size, border_size, offset, field_width, field_height
    # проверка что точка внутри поля
    if offset < pos[0] < offset + field_width * cell_size + (field_width-1) * border_size and offset < pos[1] < offset + field_height * cell_size + (field_height-1) * border_size:
        # проверка что попадает на клетку а не между ними
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








def render(): # нарисовать клеточки
    global field, cell_size, border_size, offset
    for y, row in enumerate(field):
        for x, cell in enumerate(row):
            pygame.draw.rect(screen, get_color(cell), (offset + x*(cell_size + border_size), offset + y*(cell_size + border_size), cell_size, cell_size))
        








def process_click(coords):
    global field
    # если нажали на клетку
    if coords[0] != None and coords[1] != None:
        # тестовая функция:
        # переключить состояние клетки 0 <-> 1
        field[coords[1]][coords[0]]['opened'] = 1 - field[coords[1]][coords[0]]['opened']
        





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
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            
            clicked_cell = get_clicked_cell(pos)
            process_click(clicked_cell)
            
    
    clock.tick(60)
    screen.fill((0,0,0))
    
    render()
    
    
    
    
    
    pygame.display.flip()
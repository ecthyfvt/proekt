import pygame


field_width = 10
field_height = 10
ship_count = [4,3,2,1] # количества (n+1)-клеточных кораблей

cell_size = 95 # размер клетки
border_size = 10 # толщина границы между клетками
offset = 0 # расстояние от края окна

colors = [] # цвета кораблей




def init_field(): # создать поле заданной ширины и высоты
    global field, field_width, field_height
    field = [[{'id':0, 'opened':0} for j in range(field_width)] for i in range(field_height)]
    # в клетках таблицы код клетки
    # 0 если пусто и натур. число если корабль, у каждого будет свой номер
    # и статус открытия, чтобы знать что рисовать 




def color(cell):
    if cell['opened']:
        if cell['id'] == 0:
            return (45, 205, 227)
        else:
            return colors[cell['id']]
    else:
        return  (104, 104, 104)





def place_all_ships(): # функция чтобы поставить корабли на поле
    # надо разместить сначала самый длинный корабль
    # потом корабль поменьше
    # на свободное место
    # потом еще меньше до самого маленького
    for size, count in enumerate(ship_count[::-1]): # для всех размеров кораблей с самого большого
        for i in range(count): # для каждого корабля
            place_ship(len(ship_count)-size)
    pass







def has_empty_nbh(x,y):
    global field, field_width, field_height
    # смещение в стороны
    ds = [(-1,-1), (-1, 0), (-1, 1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    
    for d in ds:
        if 0 <= x + d[0] <= field_width - 1 and 0 <= y + d[1] <= field_height - 1: # если в клетку можно сместиться
            if field[y+d[1]][x+d[0]]['id'] != 0: # и она не пустая
                return False # тест на отсутствие кораблей не пройден
    
    # прошли по всем ds и все ок
    return True
    
    







def place_ship(ship_size): # поставить один корабль
    global field
    available_positions = [] # создаем список возможных позиций
    # в нем будут положение верхней левой клетки корабля и направление корабля (вертикально или горизонтально)
    # тут код для вычислений:
    
    # проходим по каждой клетке поля
    for y, row in enumerate(field):
        for x, cell in enumerate(row):
            if cell['id'] == 0: # если клетка пустая
                if has_empty_nbh(x,y): # проверяем что вокруг нее нет кораблей в квадрате 3 на 3
                    pass # тут надо зайти в цикл и проверить клетку правее, еще правее и тд
                    # и еще раз, только идем вниз
                    # в каждом цикле надо:
                    # всего проверить ship_size клеток
                    # условия на клетку для проверки: вокруг нет кораблей и клетка находится на поле
                    # если все клетки проверены и все ок, то такое положение корабля возможно
    
    
    
    
    
    # потом выберем случайную и ставим корабль туда
    







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
            pygame.draw.rect(screen, color(cell), (offset + x*(cell_size + border_size), offset + y*(cell_size + border_size), cell_size, cell_size))
        








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
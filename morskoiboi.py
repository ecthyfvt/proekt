import pygame
import random

window_width = 800
window_heigth = 600

field_width = 10 # ширина игрового поля
field_height = 10 # высота поля
ship_count = [3,3,2,1] # количества (n+1)-клеточных кораблей

border_fraction = 0 # толщина границы между клетками

border_radius = 0.03 # толщина клеточек




def init_field(field_width, field_height): # создать поле заданной ширины и высоты 
    field = [[{'id':0, 'opened':1, 'orientation':None, 'type':None, 'size':0} for j in range(field_width)] for i in range(field_height)]
    return field
    # в клетках таблицы код клетки
    # 0 если пусто и натуральное число если корабль, у каждого будет свой номер
    # и статус открытия, направление и край или центр корабля, чтобы знать что рисовать







def get_color(cell):
    global colors
    if cell['opened']:
        if cell['id'] == 0:
            return (20, 20, 20)
        else:


            #return ((cell['type'] == 'DRedge') * 200, 0, 0)
            return colors[cell['id']-1]
    else:
        return  (54, 54, 54)







def place_all_ships(): 
    # функция чтобы поставить корабли на поле
    # надо разместить сначала самый длинный корабль
    # потом корабль поменьше
    # на свободное место
    # потом еще меньше до самого маленького
    global colors
    colors = []
    for size, count in enumerate(ship_count[::-1]): # для всех размеров кораблей с самого большого
        for i in range(count): # для каждого корабля
            place_ship(len(ship_count)-size)






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









def get_dimensions(window_width, window_height):
    global field_width, field_height, border_fraction, border_radius
    
    
    offset_x, offset_y = 0, 0
    
    X = field_width * (1 + border_fraction) + border_fraction
    Y = field_height * (1 + border_fraction) + border_fraction
    
    kx = window_width / X
    ky = window_height / Y
    
    k = min(kx, ky)
    
    cell_size = k
    border_size = k * border_fraction
    
    
    offset_x = (window_width - ((border_size + cell_size) * field_width + border_size)) / 2
    
    offset_y = (window_height - ((border_size + cell_size) * field_height + border_size)) / 2
    
    
    
    thickness = k * border_radius/2
    
    
    
    return cell_size, border_size, offset_x, offset_y, thickness










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
                field[pos[1]][pos[0] + dx]['orientation'] = 'h'
                field[pos[1]][pos[0] + dx]['size'] = ship_size

                if dx == 0:
                    field[pos[1]][pos[0] + dx]['type'] = 'ULedge'

                elif dx == ship_size - 1:
                    field[pos[1]][pos[0] + dx]['type'] = 'DRedge'


                else:
                    field[pos[1]][pos[0] + dx]['type'] = 'center'



        else:
            for dy in range(ship_size):
                field[pos[1] + dy][pos[0]]['id'] = id
                field[pos[1] + dy][pos[0]]['orientation'] = 'v'
                field[pos[1] + dy][pos[0]]['size'] = ship_size

                if dy == 0:
                    field[pos[1] + dy][pos[0]]['type'] = 'ULedge'

                elif dy == ship_size - 1:
                    field[pos[1] + dy][pos[0]]['type'] = 'DRedge'



                else:
                    field[pos[1] + dy][pos[0]]['type'] = 'center'







def get_clicked_cell(pos):
    global cell_size, border_size, field_width, field_height, offset_x, offset_y
    
    
    pos[0], pos[1] = pos[0] - offset_x, pos[1] - offset_y
    
    
    # проверка, что точка внутри поля
    if border_size < pos[0] < border_size + field_width * cell_size + (field_width-1) * border_size and border_size < pos[1] < border_size + field_height * cell_size + (field_height-1) * border_size:
        # проверка что попадает на клетку, а не между ними
        if (pos[0] - border_size) % (cell_size + border_size) < cell_size and 0 < (pos[1] - border_size) % (cell_size + border_size) < cell_size:
            px = int( (pos[0] - border_size) // (cell_size + border_size) )
            py = int( (pos[1] - border_size) // (cell_size + border_size) )
        else:
            px = None
            py = None
    else:
        px = None
        py = None
    return (px, py)







def render(): # нарисовать клеточки
    global field, cell_size, border_size, offset_x, offset_y
    for y, row in enumerate(field):
        for x, cell in enumerate(row):
            # pygame.draw.rect(screen, get_color(cell), (offset_x + border_size + x*(cell_size + border_size), offset_y + border_size + y*(cell_size + border_size), cell_size, cell_size))
            pygame.draw.rect(screen, (155, 214, 51), (offset_x + border_size + x * (cell_size + border_size), offset_y + border_size + y * (cell_size + border_size), cell_size, cell_size), max(1, round(thickness)), border_radius=1)

            if not cell['opened']:
                pygame.draw.rect(screen, (56, 171, 140), (offset_x + border_size + x * (cell_size + border_size),
                                                           offset_y + border_size + y * (cell_size + border_size),
                                                           cell_size, cell_size))
            elif cell['size'] == 1:
                screen.blit(onecell, (offset_x + border_size + x*(cell_size + border_size), offset_y + border_size + y*(cell_size + border_size)))
            elif cell['type'] == 'ULedge':
                
                if cell['orientation'] == 'h':
                    screen.blit(ul, (offset_x + border_size + x*(cell_size + border_size), offset_y + border_size + y*(cell_size + border_size)))
                else:
                    screen.blit(ul_rotated, (offset_x + border_size + x*(cell_size + border_size), offset_y + border_size + y*(cell_size + border_size)))
                
                    
                    
            elif cell['type'] == 'center':
                
                if cell['orientation'] == 'h':
                    screen.blit(center, (offset_x + border_size + x*(cell_size + border_size), offset_y + border_size + y*(cell_size + border_size)))
                else:
                    screen.blit(center_rotated, (offset_x + border_size + x*(cell_size + border_size), offset_y + border_size + y*(cell_size + border_size)))
                
            elif cell['type'] == 'DRedge':
                if cell['orientation'] == 'h':
                    screen.blit(dr, (offset_x + border_size + x*(cell_size + border_size), offset_y + border_size + y*(cell_size + border_size)))
                else:
                    screen.blit(dr_rotated, (offset_x + border_size + x*(cell_size + border_size), offset_y + border_size + y*(cell_size + border_size)))
                
            if not cell['opened']:
                pygame.draw.rect(screen, (155, 214, 51), (offset_x + border_size + x * (cell_size + border_size), offset_y + border_size + y * (cell_size + border_size), cell_size, cell_size), max(1, round(thickness)), border_radius=1)
  



def process_click(coords):
    global field
    # если нажали на клетку
    if coords[0] != None and coords[1] != None:
        # тестовая функция:
        # переключить состояние клетки 0 <-> 1
        if field[coords[1]][coords[0]]['opened'] == 0:
            field[coords[1]][coords[0]]['opened'] = 1
        else:
            field[coords[1]][coords[0]]['opened'] = 0








pygame.init()
screen = pygame.display.set_mode((window_width, window_heigth), pygame.RESIZABLE)
clock = pygame.time.Clock()


current_width, current_height = pygame.display.get_surface().get_size()


cell_size, border_size, offset_x, offset_y, thickness = get_dimensions(current_width, current_height)







bg_orig = pygame.image.load('underwater_bg.jpg')
onecell_orig = pygame.image.load('1cell.png')
ul_orig = pygame.image.load('ul.png')
dr_orig = pygame.image.load('dr.png')
center_orig = pygame.image.load('center.png')







bg = pygame.transform.smoothscale(bg_orig, screen.get_size())
onecell = pygame.transform.smoothscale(onecell_orig, (cell_size, cell_size))
ul = pygame.transform.smoothscale(ul_orig, (cell_size, cell_size))
dr = pygame.transform.smoothscale(dr_orig, (cell_size, cell_size))
center = pygame.transform.smoothscale(center_orig, (cell_size, cell_size))


ul_rotated = pygame.transform.rotate(ul, -90)
dr_rotated = pygame.transform.rotate(dr, -90)
center_rotated = pygame.transform.rotate(center, -90)



field = init_field(field_width, field_height) # создание игрового поля

place_all_ships() 



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = list(pygame.mouse.get_pos())
            
            clicked_cell = get_clicked_cell(pos)
            process_click(clicked_cell)

        if event.type == pygame.VIDEORESIZE:
            current_width, current_height = pygame.display.get_surface().get_size()
            cell_size, border_size, offset_x, offset_y, thickness = get_dimensions(current_width, current_height)
            bg = pygame.transform.smoothscale(bg_orig, screen.get_size())
            onecell = pygame.transform.smoothscale(onecell_orig, (cell_size, cell_size))
            ul = pygame.transform.smoothscale(ul_orig, (cell_size, cell_size))
            dr = pygame.transform.smoothscale(dr_orig, (cell_size, cell_size))
            center = pygame.transform.smoothscale(center_orig, (cell_size, cell_size))

            ul_rotated = pygame.transform.rotate(ul, -90)
            dr_rotated = pygame.transform.rotate(dr, -90)
            center_rotated = pygame.transform.rotate(center, -90)

    clock.tick(60)

    # начало рисования

    screen.fill((0,0,0))
    screen.blit(bg, (0, 0))
    
    # поставить картинку

    render()
    
    
    
    
    
    pygame.display.flip()
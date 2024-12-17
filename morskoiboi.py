import pygame
import random

window_width = 800
window_heigth = 600

field_width = 10 # ширина игрового поля
field_height = 10 # высота поля
ship_count = [3,3,2,1] # количества (n+1)-клеточных кораблей

border_fraction = -0.01 # толщина расстояния между клетками
border_radius = 0.03 # толщина клеточек



def init_field(field_width, field_height): # создать поле заданной ширины и высоты
    field = [[{'id':0, 'opened':0, 'orientation':None, 'type':None, 'size':0} for j in range(field_width)] for i in range(field_height)]
    return field
    # в клетках таблицы код клетки
    # 0 если пусто и натуральное число если корабль, у каждого будет свой номер
    # и статус открытия, направление и край или центр корабля, чтобы знать что рисовать



def get_color(cell):
    # не используется, так как изменена логика выбора текстур
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
    # функция, чтобы поставить корабли на поле
    # надо разместить сначала самый длинный корабль
    # потом корабль поменьше
    # на свободное место
    # потом еще меньше до самого маленького
    global colors
    colors = []
    for size, count in enumerate(ship_count[::-1]): # для всех размеров кораблей с самого большого
        for i in range(count): # для каждого корабля
            place_ship(len(ship_count)-size) # поставить корабль



def has_empty_nbh(x,y):
    # проверка пустоты пространства вокруг клетки
    global field, field_width, field_height
    # смещение в стороны
    ds = [(-1,-1), (-1, 0), (-1, 1), (0,-1), (0,1), (1,-1), (1,0), (1,1)] # стандартный вариант
    # ds = [(-1, 0), (0,-1), (0,1), (1,0)] # корабли могут касаться углами

    for d in ds: # для каждого смещения
        if in_field(x + d[0], y + d[1]): # если в клетку можно сместиться
            if field[y+d[1]][x+d[0]]['id'] != 0: # и она не пустая
                return False # тест на отсутствие кораблей не пройден

    # прошли по всем ds и все ок
    return True



def in_field(x,y):
    # находится ли точка внутри таблицы, чтобы не было ошибки лист индекс оут оф ранге
    global field_width, field_height
    return (0 <= x <= field_width - 1) and (0 <= y <= field_height - 1)



def get_dimensions(window_width, window_height):
    # обновить значения размеров для отрисовки, чтобы поле поместилось в окно

    global field_width, field_height, border_fraction, border_radius

    # получаем маленький прямоугольник
    X = field_width * (1 + border_fraction) + border_fraction
    Y = field_height * (1 + border_fraction) + border_fraction

    # на сколько надо домножить, чтобы растянуть его на ширину или высоту окна
    kx = window_width / X
    ky = window_height / Y

    # берем минимум
    k = min(kx, ky)

    # домножаем
    cell_size = k
    border_size = k * border_fraction
    thickness = k * border_radius / 2

    # поставить по центру
    offset_x = (window_width - ((border_size + cell_size) * field_width + border_size)) / 2
    offset_y = (window_height - ((border_size + cell_size) * field_height + border_size)) / 2

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
            is_good_position = None # место еще неизвестно какое
            for dx in range(ship_size): # для смещения на 0, 1 ... клетку от исходной
                if in_field(x + dx, y): # если она есть
                    if has_empty_nbh(x + dx, y) and field[y][x+dx]['id'] == 0: # если стоит отдельно от кораблей и пустая
                        if is_good_position != False: # это место еще не было плохим
                            is_good_position = True # оно хорошее
                    else:
                        is_good_position = False # оно плохое и больше хорошим не станет (см. выше)
                else:
                    is_good_position = False # клетка за пределами поля, место плохое
            if is_good_position: # если место хорошее
                available_positions.append((x,y,'h')) # добавить это положение в список

            # проверка вертикального положения аналогично
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


    if len(available_positions) > 0: # есть хотя бы одно доступное положение
        colors.append((random.randint(50,255), random.randint(50,255), random.randint(50,255))) # не используется
        id = len(colors) # присвоить номер
        pos = random.choice(available_positions) # выбрать случайное


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
    # получить координаты кликнутой клетки
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



def render():
    # нарисовать клеточки
    global field, cell_size, border_size, offset_x, offset_y, text_to_show, reveal_time, my_font, current_width, current_height
    for y, row in enumerate(field):
        for x, cell in enumerate(row):

            pygame.draw.rect(screen, (155, 214, 51), (offset_x + border_size + x * (cell_size + border_size), offset_y + border_size + y * (cell_size + border_size), cell_size, cell_size), max(1, round(thickness)), border_radius=1)

            if not cell['opened']:
                pygame.draw.rect(screen, (56, 171, 140), (offset_x + border_size + x * (cell_size + border_size), offset_y + border_size + y * (cell_size + border_size), cell_size, cell_size))

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



    if pygame.time.get_ticks() - reveal_time < 700:
        text_surface = my_font.render(text_to_show, True, (117, 92, 27))

        screen.blit(text_surface, (current_width/2.5, lin(0,700**3,current_height*0.8,current_height*1.2,(pygame.time.get_ticks() - reveal_time)**3)))



def lin(a,b,c,d,t):
    # map ab to cd
    # t is in ab
    # return t1 on cd
    return c + (d - c) * ( (t - a) / (b - a) )



def process_click(coords):
    # обработка нажатий
    global field, reveal_time, text_to_show
    if coords[0] != None and coords[1] != None:
        if field[coords[1]][coords[0]]['opened'] == 0:
            field[coords[1]][coords[0]]['opened'] = 1
            reveal_time = pygame.time.get_ticks()
            if field[coords[1]][coords[0]]['id'] == 0:
                text_to_show = 'Вы не попали'
            else:
                text_to_show = 'Вы попали в корабль!!'





reveal_time = 0
text_to_show = ''
pygame.init()
screen = pygame.display.set_mode((window_width, window_heigth), pygame.RESIZABLE)
clock = pygame.time.Clock()



my_font = pygame.font.SysFont('Comic sans MS', 30)






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

    screen.fill((0,0,0))
    screen.blit(bg, (0, 0))
    render()

    pygame.display.flip()
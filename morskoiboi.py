import pygame


field_width = 10
field_height = 10
ship_count = [4,3,2,1] # количества (n+1)-клеточных кораблей

cell_size = 95 # размер клетки
border_size = 10 # толщина границы между клетками
offset = 0 # расстояние от края окна



color = [(40, 138, 138), (210, 230, 100)]
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
    
    # используем функцию place_ship для каждого корабля
    pass
  
  
  
  
  
def place_ship(ship_size): # поставить один корабль
    global field
    available_positions = [] # создаем список возможных позиций
    # в нем будут положение верхней левой клетки корабля и направление корабля (вертикально или горизонтально)
    # тут код для вычислений будет
    #
    #
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
            pygame.draw.rect(screen, color[cell], (offset + x*(cell_size + border_size), offset + y*(cell_size + border_size), cell_size, cell_size))
        








def process_click(cell):
    global field
    # если нажали на клетку
    if cell[0] != None and cell[1] != None:
        # тестовая функция:
        # переключить состояние клетки 0 <-> 1
        field[cell[1]][cell[0]] = 1 - field[cell[1]][cell[0]]






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
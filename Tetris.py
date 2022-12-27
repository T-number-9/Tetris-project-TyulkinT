import pygame
import os
import sys
import random
from copy import deepcopy

figures_pos = [[[-1, 3], [-1, 4], [-1, 5], [-1, 6]],    # линия
               [[-1, 4], [-1, 5], [0, 4], [0, 5]],  # квадрат
               [[0, 3], [0, 4], [-1, 4], [-1, 5]],   # S
               [[-1, 3], [-1, 4], [0, 4], [0, 5]],   # Z
               [[-1, 5], [0, 5], [1, 5], [1, 4]],   # J
               [[-1, 4], [0, 4], [1, 4], [1, 5]],    # L
               [[-1, 4], [0, 3], [0, 4], [0, 5]]]    # T

pygame.init()
pygame.display.set_caption('Tetris') # наименование игры
w_size = window_weight, window_height = 700, 650 # размеры основного окна
c_size = cup_weight, cup_height = 10, 21 # размеры игрового стакана
block = 30 # сторона одной клетки поля
screen = pygame.display.set_mode(w_size) # создание основного окна

# переменные
clock = pygame.time.Clock()
FPS = 60
delta_limit = 20
delta, figure, new_fig, figure_name, new_fig_name = 0, 0, 0, 0, 0
all_sprites = pygame.sprite.Group()

# фоновая музыка
#pygame.mixer.music.load("data/Tetris Theme.mp3")
#pygame.mixer.music.play(-1)


# загрузка изображений
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# загрузка фигур
def figure_load():
    global figure_name, new_fig_name
    figure_name = new_fig_name
    figure_num = random.randint(0, 6)
    figure = deepcopy(figures_pos[figure_num])
    if figure_num == 0:
        new_fig_name = 'линия'
    elif figure_num == 1:
        new_fig_name = 'квадрат'
    elif figure_num == 2:
        new_fig_name = 'S'
    elif figure_num == 3:
        new_fig_name = 'Z'
    elif figure_num == 4:
        new_fig_name = 'J'
    elif figure_num == 5:
        new_fig_name = 'L'
    elif figure_num == 6:
        new_fig_name = 'T'
    return figure


figure = figure_load()
new_fig = figure_load()


# начальное меню и экран паузы
class Menu:
    pass


class New:
    # отображение следующей фигуры
    def __init__(self):
        global new_fig
        self.new_fig_board = [[0] * 7 for _ in range(7)]
        for i in new_fig:
            self.new_fig_board[i[0]+1][i[1]] = 1
        for irow in range(7):
            for icol in range(7):
                x_left = 460 + icol * block
                y_top = 220 + irow * block
                if self.new_fig_board[irow][icol] == 1:
                    pygame.draw.rect(screen, 'Green', (x_left + 2, y_top + 2, block - 2, block - 2))


class Cup:
    # создание стакана
    def __init__(self, c_width, c_height):
        self.width = c_width
        self.height = c_height
        self.board = [[0] * self.width for _ in range(self.height)]
        # значения по умолчанию
        self.left = 190
        self.top = 50
        self.flag = 0
        self.list_coords = []

    # создание сетки
    def render(self, screen):
        for irow in range(self.height):
            for icol in range(self.width):
                x_left = self.left + icol * block
                y_top = self.top + irow * block
                if self.board[irow][icol] == 1:
                    pygame.draw.rect(screen, 'Green', (x_left + 2, y_top + 2, block - 2, block - 2))
                elif self.board[irow][icol] == 2:
                    pygame.draw.rect(screen, 'Red', (x_left + 2, y_top + 2, block - 2, block - 2))
                else:
                    pygame.draw.rect(screen, 'Black', (x_left, y_top, block, block))
        pygame.draw.rect(screen, 'White', (self.left, self.top, self.width * block, 20 * block), 3)

    # проверка на пересечение с границами по х
    def check_borders_x(self, c_figure):
        for i in c_figure:
            if i[1] + 1 > 10 or i[1] - 1 < -1:
                return 'border'
            if i[1] + 1 < 10 and (self.board[i[0]][i[1] + 1] == 2 or self.board[i[0]][i[1] - 1] == 2):
                return 'block'
        return True

    # проверка на пересечение с границами по y
    def check_borders_y(self, c_figure):
        for i in c_figure:
            if i[0] + 1 > 20:
                return 'border'
            if i[0] + 1 <= 19 and self.board[i[0] + 1][i[1]] == 2:
                return 'block'
        return True

    # движение фигуры по оси x
    def move_figure(self, dx, dy):
        global figure
        new_board = deepcopy(self.board)
        m_figure = deepcopy(figure)
        for i in m_figure:
            new_board[i[0]][i[1]] = 0
            i[1] += dx
            i[0] += dy
        if self.check_borders_x(m_figure) == 'border' or self.check_borders_x(m_figure) == 'block':
            pass
        else:
            for i in m_figure:
                new_board[i[0]][i[1]] = (new_board[i[0]][i[1]] + 1) % 2
            figure = m_figure
            self.board = new_board

    # движение фигуры по оси y
    def figure_fall(self, d):
        global delta_limit
        global figure, new_fig
        new_board = deepcopy(self.board)
        m_figure = deepcopy(figure)
        if d % delta_limit == 0:
            for i in m_figure:
                new_board[i[0]][i[1]] = 0
                i[0] += 1
            if self.check_borders_y(m_figure) == 'border':
                for i in m_figure:
                    new_board[i[0]-1][i[1]] = 2
                self.board = new_board
                figure = new_fig
                new_fig = figure_load()
            elif self.check_borders_y(m_figure) == 'block':
                for i in m_figure:
                    new_board[i[0]][i[1]] = 2
                self.board = new_board
                figure = new_fig
                new_fig = figure_load()
            elif self.check_borders_y(m_figure):
                for i in m_figure:
                    new_board[i[0]][i[1]] = (new_board[i[0]][i[1]] + 1) % 2
                figure = m_figure
                self.board = new_board
        delta_limit = 20

    # вращение фигуры
    def rotate(self):
        pass

    # проверка на собранные линии и начисление очков
    def lines_and_points(self):
        pass


cup = Cup(cup_weight, cup_height)


running = True
while running:
    keys = pygame.key.get_pressed()
    delta += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                cup.move_figure(1, 0)
            if event.key == pygame.K_LEFT:
                cup.move_figure(-1, 0)
            if event.key == pygame.K_UP:
                cup.rotate()
    if keys[pygame.K_DOWN]:
        delta_limit = 4
    screen.fill((0, 0, 0))
    cup.figure_fall(delta)
    cup.render(screen)
    New()
    clock.tick(FPS)
    pygame.display.flip()

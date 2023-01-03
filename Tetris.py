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
pygame.display.set_icon(pygame.image.load('data/icon.png')) # иконка
pygame.display.set_caption('Tetris') # наименование игры
w_size = window_weight, window_height = 700, 650 # размеры основного окна
c_size = cup_weight, cup_height = 10, 21 # размеры игрового стакана
block = 30 # сторона одной клетки поля
screen = pygame.display.set_mode(w_size) # создание основного окна

# переменные
clock = pygame.time.Clock()
FPS = 60
delta_limit = 20
score = 0
delta, figure, new_fig, figure_name, new_fig_name = 0, 0, 0, 0, 0

menu_sprite = pygame.sprite.Group()
pause_sprite = pygame.sprite.Group()
over_sprite = pygame.sprite.Group()

shrift = pygame.font.SysFont('Times New Roman', 22) # шрифт основных подписей
small_shrift = pygame.font.SysFont('Times New Roman', 15) # мелкий шрифт
big_shrift = pygame.font.SysFont('Times New Roman', 50) # большой шрифт

tetris = big_shrift.render('TETRIS', True, 'Yellow')
tetris_rect = tetris.get_rect()
tetris_rect.topleft = (258, 0)

next_picture = shrift.render('Следующая фигура', True, 'White')
next_rect = next_picture.get_rect()
next_rect.topleft = (505, 220)

score_picture = shrift.render('СЧЁТ', True, 'White')
score_rect = score_picture.get_rect()
score_rect.topleft = (571, 50)

rule1 = small_shrift.render('ВВЕРХ - вращение фигуры', True, 'White')
rule1_rect = rule1.get_rect()
rule1_rect.topleft = (7, 200)

rule2 = small_shrift.render('ВНИЗ - ускорение', True, 'White')
rule2_rect = rule2.get_rect()
rule2_rect.topleft = (7, 225)

rule3 = small_shrift.render('ВПРАВО - движ. вправо', True, 'White')
rule3_rect = rule3.get_rect()
rule3_rect.topleft = (6, 250)

rule4 = small_shrift.render('ВЛЕВО - движ. влево', True, 'White')
rule4_rect = rule4.get_rect()
rule4_rect.topleft = (7, 275)

rule5 = small_shrift.render('ПРОБЕЛ - пауза', True, 'White')
rule5_rect = rule5.get_rect()
rule5_rect.topleft = (7, 300)

rule6 = small_shrift.render('ESC - выход', True, 'White')
rule6_rect = rule6.get_rect()
rule6_rect.topleft = (7, 325)

rule7 = small_shrift.render('1 - вкл/выкл музыки', True, 'White')
rule7_rect = rule7.get_rect()
rule7_rect.topleft = (7, 350)

key_pic = shrift.render('PRESS ANY KEY TO RESTART', True, 'White')
key_rect = key_pic.get_rect()
key_rect.topleft = (200, 500)

record_pic = shrift.render('РЕКОРД', True, 'White')
record_rect = record_pic.get_rect()
record_rect.topleft = (550, 400)


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


# добавление рисунков
menu = pygame.sprite.Sprite()
menu.image = load_image("menu.png")
menu.rect = menu.image.get_rect()
menu_sprite.add(menu)
pause = pygame.sprite.Sprite()
pause.image = load_image("pause.png")
pause.rect = pause.image.get_rect()
pause_sprite.add(pause)
over = pygame.sprite.Sprite()
over.image = load_image("over.png")
over.rect = pause.image.get_rect()
over_sprite.add(over)


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


def take_record():
    try:
        with open('record') as file:
            return file.readline()
    except FileNotFoundError:
        with open('record', 'w') as file:
            file.write('0')
            return '0'


class New:
    # отображение следующей фигуры
    def __init__(self):
        global new_fig
        self.new_fig_board = [[0] * 7 for _ in range(7)]
        for i in new_fig:
            self.new_fig_board[i[0]+1][i[1]] = 1
        for irow in range(7):
            for icol in range(7):
                x_left = 452 + icol * block
                y_top = 260 + irow * block
                if self.new_fig_board[irow][icol] == 1:
                    pygame.draw.rect(screen, 'White', (x_left + 2, y_top + 2, block - 2, block - 2))


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
                return 'border' # столкновение с бортами
            if i[1] + 1 < 10 and (self.board[i[0]][i[1] + 1] == 2 or self.board[i[0]][i[1] - 1] == 2):
                return 'block' # столкновение с блоками
        return True

    # проверка на пересечение с границами по y
    def check_borders_y(self, c_figure):
        for i in c_figure:
            if i[0] + 1 > 20:
                return 'border' # столкновение с бортами
            if i[0] + 1 <= 19 and self.board[i[0] + 1][i[1]] == 2:
                return 'block' # столкновение с блоками
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
            pass # при столокновении не двигаем
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
                    new_board[i[0]-1][i[1]] = 2 # при столкновении перекрашиваем
                self.board = new_board
                figure = new_fig
                new_fig = figure_load()
                self.lines_and_points()
            elif self.check_borders_y(m_figure) == 'block':
                for i in m_figure:
                    new_board[i[0]][i[1]] = 2 # при столкновении перекрашиваем
                self.board = new_board
                figure = new_fig
                new_fig = figure_load()
                self.lines_and_points()
            elif self.check_borders_y(m_figure):
                for i in m_figure:
                    new_board[i[0]][i[1]] = (new_board[i[0]][i[1]] + 1) % 2
                figure = m_figure
                self.board = new_board
        delta_limit = 20

    # проверка возможности поворота фигуры
    def rotate_check(self, r_figure):
        for elem in r_figure:
            if (elem[1] < 0) or (elem[1] > 9) or (elem[0] < 0) or (self.board[elem[0] + 1][elem[1]] == 2):
                return False
        return True

    # вращение фигуры
    def rotate(self):
        global figure_name, figure
        new_board = deepcopy(self.board)
        r_figure = deepcopy(figure)
        if figure_name == 'линия':
            for i in r_figure:
                new_board[i[0]][i[1]] = 0
            r_figure[0][1] += 1
            r_figure[2][1] -= 1
            r_figure[3][1] -= 2
            r_figure[0][0] += 1
            r_figure[2][0] -= 1
            r_figure[3][0] -= 2
            if self.rotate_check(r_figure):
                self.board = new_board
                figure = r_figure
                figure_name = 'столб'
        elif figure_name == 'столб':
            for i in r_figure:
                new_board[i[0]][i[1]] = 0
            r_figure[0][1] -= 1
            r_figure[2][1] += 1
            r_figure[3][1] += 2
            r_figure[0][0] -= 1
            r_figure[2][0] += 1
            r_figure[3][0] += 2
            if self.rotate_check(r_figure):
                self.board = new_board
                figure = r_figure
                figure_name = 'линия'
        elif figure_name == 'S':
            for i in r_figure:
                new_board[i[0]][i[1]] = 0
            r_figure[0][1] += 2
            r_figure[1][1] += 1
            r_figure[3][1] -= 1
            r_figure[1][0] -= 1
            r_figure[3][0] -= 1
            if self.rotate_check(r_figure):
                self.board = new_board
                figure = r_figure
                figure_name = 'С'
        elif figure_name == 'С':
            for i in r_figure:
                new_board[i[0]][i[1]] = 0
            r_figure[0][1] -= 2
            r_figure[1][1] -= 1
            r_figure[3][1] += 1
            r_figure[1][0] += 1
            r_figure[3][0] += 1
            if self.rotate_check(r_figure):
                self.board = new_board
                figure = r_figure
                figure_name = 'S'
        elif figure_name == 'Z':
            for i in r_figure:
                new_board[i[0]][i[1]] = 0
            r_figure[0][1] += 1
            r_figure[2][1] -= 1
            r_figure[3][1] -= 2
            r_figure[0][0] -= 1
            r_figure[2][0] -= 1
            if self.rotate_check(r_figure):
                self.board = new_board
                figure = r_figure
                figure_name = 'З'
        elif figure_name == 'З':
            for i in r_figure:
                new_board[i[0]][i[1]] = 0
            r_figure[0][1] -= 1
            r_figure[2][1] += 1
            r_figure[3][1] += 2
            r_figure[0][0] += 1
            r_figure[2][0] += 1
            if self.rotate_check(r_figure):
                self.board = new_board
                figure = r_figure
                figure_name = 'Z'
        elif figure_name == 'J':
            for i in r_figure:
                new_board[i[0]][i[1]] = 0
            r_figure[0][0] += 2
            r_figure[0][1] += 2
            r_figure[3][1] += 2
            if self.rotate_check(r_figure):
                self.board = new_board
                figure = r_figure
                figure_name = 'J1'
        elif figure_name == 'J1':
            for i in r_figure:
                new_board[i[0]][i[1]] = 0
            r_figure[0][0] += 2
            r_figure[0][1] -= 2
            r_figure[1][0] += 2
            if self.rotate_check(r_figure):
                self.board = new_board
                figure = r_figure
                figure_name = 'J2'
        elif figure_name == 'J2':
            for i in r_figure:
                new_board[i[0]][i[1]] = 0
            r_figure[0][0] -= 2
            r_figure[0][1] -= 2
            r_figure[3][1] -= 2
            if self.rotate_check(r_figure):
                self.board = new_board
                figure = r_figure
                figure_name = 'J3'
        elif figure_name == 'J3':
            for i in r_figure:
                new_board[i[0]][i[1]] = 0
            r_figure[0][0] -= 2
            r_figure[0][1] += 2
            r_figure[1][0] -= 2
            if self.rotate_check(r_figure):
                self.board = new_board
                figure = r_figure
                figure_name = 'J'
        elif figure_name == 'L':
            for i in r_figure:
                new_board[i[0]][i[1]] = 0
            r_figure[0][0] += 2
            r_figure[0][1] += 2
            r_figure[1][0] += 2
            if self.rotate_check(r_figure):
                self.board = new_board
                figure = r_figure
                figure_name = 'L1'
        elif figure_name == 'L1':
            for i in r_figure:
                new_board[i[0]][i[1]] = 0
            r_figure[0][0] += 2
            r_figure[0][1] -= 2
            r_figure[3][1] -= 2
            if self.rotate_check(r_figure):
                self.board = new_board
                figure = r_figure
                figure_name = 'L2'
        elif figure_name == 'L2':
            for i in r_figure:
                new_board[i[0]][i[1]] = 0
            r_figure[0][0] -= 2
            r_figure[0][1] -= 2
            r_figure[1][0] -= 2
            if self.rotate_check(r_figure):
                self.board = new_board
                figure = r_figure
                figure_name = 'L3'
        elif figure_name == 'L3':
            for i in r_figure:
                new_board[i[0]][i[1]] = 0
            r_figure[0][0] -= 2
            r_figure[0][1] += 2
            r_figure[3][1] += 2
            if self.rotate_check(r_figure):
                self.board = new_board
                figure = r_figure
                figure_name = 'L'
        elif figure_name == 'T':
            for i in r_figure:
                new_board[i[0]][i[1]] = 0
            r_figure[0][0] += 1
            r_figure[0][1] += 1
            r_figure[1][0] -= 1
            r_figure[1][1] += 1
            r_figure[3][0] += 1
            r_figure[3][1] -= 1
            if self.rotate_check(r_figure):
                self.board = new_board
                figure = r_figure
                figure_name = 'T1'
        elif figure_name == 'T1':
            for i in r_figure:
                new_board[i[0]][i[1]] = 0
            r_figure[0][0] += 1
            r_figure[0][1] -= 1
            r_figure[1][0] += 1
            r_figure[1][1] += 1
            r_figure[3][0] -= 1
            r_figure[3][1] -= 1
            if self.rotate_check(r_figure):
                self.board = new_board
                figure = r_figure
                figure_name = 'T2'
        elif figure_name == 'T2':
            for i in r_figure:
                new_board[i[0]][i[1]] = 0
            r_figure[0][0] -= 1
            r_figure[0][1] -= 1
            r_figure[1][0] += 1
            r_figure[1][1] -= 1
            r_figure[3][0] -= 1
            r_figure[3][1] += 1
            if self.rotate_check(r_figure):
                self.board = new_board
                figure = r_figure
                figure_name = 'T3'
        elif figure_name == 'T3':
            for i in r_figure:
                new_board[i[0]][i[1]] = 0
            r_figure[0][0] -= 1
            r_figure[0][1] += 1
            r_figure[1][0] -= 1
            r_figure[1][1] -= 1
            r_figure[3][0] += 1
            r_figure[3][1] += 1
            if self.rotate_check(r_figure):
                self.board = new_board
                figure = r_figure
                figure_name = 'T'

    # проверка на собранные линии и начисление очков
    def lines_and_points(self):
        global game, score, score_points
        j = 0
        if 2 in cup.board[0]: # если стакан заполнен - проигрыш
            game = 'over'
            pygame.mixer.music.load("data/game over.mp3")
            pygame.mixer.music.play()
            if score > int(record):
                with open('record', 'w') as file:
                    file.write(str(score))
        for i in range(21):
            if cup.board[i] == [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]: # если линия заполнена -
                del cup.board[i] # - удаляем её
                cup.board.insert(0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) # добавляем сверху новую
                j += 1
        if j == 1:
            score += 100
        elif j == 2:
            score += 300
        elif j == 3:
            score += 700
        elif j == 4:
            score += 1000


cup = Cup(cup_weight, cup_height)

music = True
game = 'menu'
running = True
while running:
    record = take_record()
    if game == 'play':
        score_points = big_shrift.render(f'{score}', True, 'White')
        score_points_rect = score_points.get_rect()
        score_points_rect.topleft = (540, 100)
        pygame.mixer.music.unpause()
        keys = pygame.key.get_pressed()
        delta += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # закрытие программы
                    running = False
                if event.key == pygame.K_RIGHT: # движение вправо
                    cup.move_figure(1, 0)
                if event.key == pygame.K_LEFT: # движение влево
                    cup.move_figure(-1, 0)
                if event.key == pygame.K_UP: # вращение фигуры
                    cup.rotate()
                if event.key == pygame.K_SPACE: # пауза
                    game = 'pause'
                if event.key == pygame.K_1: # вкл/выкл звука
                    if music:
                        pygame.mixer.music.set_volume(0)
                        music = False
                    else:
                        pygame.mixer.music.set_volume(1)
                        music = True
        if keys[pygame.K_DOWN]:
            delta_limit = 4 # ускорение падения фигуры
        screen.fill((0, 0, 0))
        cup.figure_fall(delta)
        cup.render(screen)
        New() # следующая фигура на экране

        # вывод текста на игровом экране
        screen.blit(tetris, tetris_rect)
        screen.blit(next_picture, next_rect)
        screen.blit(score_picture, score_rect)
        screen.blit(score_points, score_points_rect)
        screen.blit(rule1, rule1_rect)
        screen.blit(rule2, rule2_rect)
        screen.blit(rule3, rule3_rect)
        screen.blit(rule4, rule4_rect)
        screen.blit(rule5, rule5_rect)
        screen.blit(rule6, rule6_rect)
        screen.blit(rule7, rule7_rect)
        screen.blit(record_pic, record_rect)

        record_pic1 = big_shrift.render(record, True, 'White')
        record_rect1 = record_pic1.get_rect()
        record_rect1.topleft = (550, 450)
        screen.blit(record_pic1, record_rect1)

        clock.tick(FPS)
        pygame.display.flip()
    elif game == 'pause':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game = 'play' # продолжение игры
                if event.key == pygame.K_ESCAPE:
                    running = False
        pygame.mixer.music.pause() # остановка музыки
        pause_sprite.draw(screen)
        pygame.display.flip()
    elif game == 'menu':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                game = 'play' # запуск игры
                # фоновая музыка
                pygame.mixer.music.load("data/Tetris Theme.mp3")
                pygame.mixer.music.play(-1)
        menu_sprite.draw(screen)
        pygame.display.flip()
    elif game == 'over':
        score_picture1 = big_shrift.render(f'СЧЁТ: {score}', True, 'White')
        score_rect1 = score_picture.get_rect()
        score_rect1.topleft = (270, 400)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                game = 'play' # запуск игры
                pygame.mixer.music.load("data/Tetris Theme.mp3")
                pygame.mixer.music.play(-1)
                cup.board = [[0] * cup_weight for _ in range(cup_height)]
                score = 0
        over_sprite.draw(screen)
        screen.blit(score_picture1, score_rect1)
        screen.blit(key_pic, key_rect)
        pygame.display.flip()

import pygame
import random

import sys
import os


FPS = 30
WIDTH, HEIGHT = 1600, 900
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('data/images', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


cells = dict()
for cell_id in range(9):
    cells[cell_id] = load_image('kletki/' + str(cell_id) + '.jpg')
cells['bomb'] = load_image('kletki/bomb.jpg')
cells['cell'] = load_image('kletki/kletka.jpg')
cells['flag'] = load_image('kletki/flag.jpg')

difficulty = dict()
difficulty[1] = (9, 9, 10)
difficulty[2] = (16, 16, 40)
difficulty[3] = (16, 30, 99)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 200)
    name = font.render('САПЕР', 1, 'White')

    font2 = pygame.font.Font(None, 50)
    prod = font2.render('Для продолжения нажмите ЛКМ', 1, 'white')

    lenx1 = name.get_rect().size[0]
    lenx2 = prod.get_rect().size[0]
    screen.blit(name, (WIDTH / 2 - (lenx1 / 2), 175))
    screen.blit(prod, (WIDTH / 2 - (lenx2 / 2), 675))

    screen.blit(pygame.transform.scale(cells['bomb'], (256, 256)), (WIDTH / 2 - 128, 350))
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            elif ev.type == pygame.KEYDOWN or \
                    ev.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def level_pick():
    fon = pygame.transform.scale(load_image('fon_game.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    screen.blit(pygame.transform.scale(cells[1], (256, 256)), (WIDTH / 4 - 128, 200))
    screen.blit(pygame.transform.scale(cells[2], (256, 256)), (WIDTH / 2 - 128, 200))
    screen.blit(pygame.transform.scale(cells[3], (256, 256)), (3 * WIDTH / 4 - 128, 200))

    btn1 = (WIDTH / 4 - 128, 200, 256, 256)
    btn2 = (WIDTH / 2 - 128, 200, 256, 256)
    btn3 = (3 * WIDTH / 4 - 128, 200, 256, 256)

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if btn1[0] <= mx <= btn1[0] + 256 and btn1[1] <= my <= btn1[1] + 256:
                    level = 1
                    return level
                elif btn2[0] <= mx <= btn2[0] + 256 and btn2[1] <= my <= btn2[1] + 256:
                    level = 2
                    return level
                elif btn3[0] <= mx <= btn3[0] + 256 and btn3[1] <= my <= btn3[1] + 256:
                    level = 3
                    return level
        pygame.display.flip()
        clock.tick(FPS)


def load_map(size, m):
    cell_size = min((HEIGHT - 200) / size[0], (WIDTH - 200) / size[0])

    #  screen = pygame.display.set_mode((size[1] * cell_size + 200, size[0] * cell_size + 200))

    fon = pygame.transform.scale(load_image('fon_game.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    for a in range(size[0]):
        for b in range(size[1]):
            screen.blit(pygame.transform.scale(cells['cell'], (cell_size, cell_size)),
                        (100 + b * cell_size, 100 + a * cell_size))
    #  return screen
    return cell_size


def cell_number(mx, my, cell_size):
    x = int((mx - 100) // cell_size)
    y = int((my - 100) // cell_size)
    return x, y


def help_for_del(x, y):
    new = []
    for i in range(y - 1, y + 2):
        for j in range(x - 1, x + 2):
            if 0 <= i < len(bombs) and 0 <= j < len(bombs[0]):
                if j == x and i == y:
                    pass
                else:
                    new.append((j, i))
    return new


def change_cell(x, y):
    if number_sosed(bombs, x, y):
        screen.blit(pygame.transform.scale(cells[number_sosed(bombs, x, y)], (cell_size, cell_size)),
                    (x * cell_size + 100, y * cell_size + 100))
    else:
        open_cell = []
        pust = []
        open_cell.append((x, y))
        pust.append((x, y))
        for x1, y1 in pust:
            new = help_for_del(x1, y1)
            for elem in new:
                if number_sosed(bombs, elem[0], elem[1]) == 0:
                    if (elem[0], elem[1]) not in pust:
                        pust.append((elem[0], elem[1]))
                if (elem[0], elem[1]) not in open_cell:
                    open_cell.append((elem[0], elem[1]))

        for o in open_cell:
            n = number_sosed(bombs, o[0], o[1])
            screen.blit(pygame.transform.scale(cells[n], (cell_size, cell_size)),
                        (o[0] * cell_size + 100, o[1] * cell_size + 100))


def generate(size, m, mx, my, cell_size):
    bombs = []
    for row in range(size[0]):
        lst = []
        for col in range(size[1]):
            lst.append('.')
        bombs.append(lst)

    x, y = cell_number(mx, my, cell_size)

    for j in range(m):
        bx = random.randint(0, size[1] - 1)
        by = random.randint(0, size[0] - 1)
        while bombs[by][bx] == 'b' or bx == x and by == y:
            bx = random.randint(0, size[1] - 1)
            by = random.randint(0, size[0] - 1)
        bombs[by][bx] = 'b'
    return bombs


def number_sosed(bombs, x, y):
    if bombs[y][x] != 'b':
        numb = 0
        for c in range(-1, 2):
            for d in range(-1, 2):
                if c == 0 and d == 0:
                    pass
                else:
                    if 0 <= y + c < len(bombs) and 0 <= x + d < len(bombs[0]):
                        if bombs[y + c][x + d] == 'b':
                            numb += 1
        return numb
    else:
        return 'bomb'


def gameover():
    global index
    index = -1

    for r in range(map_size[0]):
        for c in range(map_size[1]):
            change_cell(c, r)

    timer = pygame.USEREVENT + 1
    pygame.time.set_timer(timer, 3000, False)

    t = True
    while t:
        for ev1 in pygame.event.get():
            if ev1.type == timer:
                t = False
        pygame.display.flip()

    fon = pygame.transform.scale(load_image('gameover.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    restart = True
    while restart:
        for ev2 in pygame.event.get():
            if ev2.type == pygame.MOUSEBUTTONDOWN:
                restart = False
        pygame.display.flip()

    fon = pygame.transform.scale(load_image('fon_game.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    cell_size = load_map(map_size, mines)

    return cell_size


def flag(x, y, boom):
    if (x, y) not in check:
        if (x, y) not in flags:
            flags.append((x, y))
            boom -= 1
            screen.blit(pygame.transform.scale(cells['flag'], (cell_size, cell_size)),
                        (x * cell_size + 100, y * cell_size + 100))
        else:
            flags.remove((x, y))
            boom += 1
            screen.blit(pygame.transform.scale(cells['cell'], (cell_size, cell_size)),
                        (x * cell_size + 100, y * cell_size + 100))
        print(boom)
        pygame.draw.rect(screen, 'black', ((4 * WIDTH / 5) - 150, (HEIGHT / 2) - 100, 300, 200))
        screen.blit(pygame.font.Font(None, 100).render(str(boom), 1, 'white'), (4 * WIDTH / 5 - 25, HEIGHT / 2 - 25))
        pygame.display.flip()

    return boom


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Minesweeper!')
    start_screen()
    level = level_pick()
    map_size = (difficulty[level][0], difficulty[level][1])
    mines = difficulty[level][2]
    cell_size = load_map(map_size, mines)
    index = 0

    boom = mines
    flags = []
    check = []
    bombs = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if 100 <= mx <= map_size[1] * cell_size + 100 and 100 <= my <= map_size[0] * cell_size + 100:
                    if index == 0:
                        bombs = generate(map_size, mines, mx, my, cell_size)
                    x, y = cell_number(mx, my, cell_size)
                    if event.button == 1:
                        change_cell(x, y)
                        check.append((x, y))
                        if bombs[y][x] == 'b':
                            cell_size = gameover()
                    else:
                        boom = flag(x, y, boom)
                index += 1
        pygame.display.flip()
    pygame.quit()

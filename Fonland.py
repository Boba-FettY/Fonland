import random as rnd
import pygame
import os
import sys

pygame.init()
size = width, height = 500, 500
scr = pygame.display.set_mode(size)

scr.fill((50, 200, 250))

buts = pygame.sprite.Group()

buttons_new_game = pygame.sprite.Group()

running = True

humus = 1

TYUI = 11
a = False


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


fon = load_image('pixil-frame-0 (74).png')

nazvanie = load_image('pixil-frame-0 (82).png')

pust = load_image('pust.png')

pst = load_image('pst.png')

shir = pygame.font.Font(None, 40)


class But(pygame.sprite.Sprite):
    def __init__(self, group, x, y, img):
        super().__init__(group)
        self.im = load_image(img)
        self.image = self.im

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


aa = But(buts, 175, 190, 'pixil-frame-0 (76).png')

b = But(buts, 175, 260, 'pixil-frame-0 (77).png')

c = But(buttons_new_game, 295, 260, 'pixil-frame-0 (85).png')

d = But(buttons_new_game, 145, 260, 'pixil-frame-0 (90).png')

nazad = But(buttons_new_game, 60, 400, 'pixil-frame-0 (84).png')

sozd = But(buttons_new_game, 280, 400, 'SOZDAT.png')

while running:

    # scr.fill((50, 200, 250))
    scr.blit(fon, (0, 0))

    scr.blit(nazvanie, (155, 90))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if aa.rect.collidepoint(pygame.mouse.get_pos()) and humus == 1:
                    humus = 0
                if b.rect.collidepoint(pygame.mouse.get_pos()) and humus == 1:
                    print('Info')
                if c.rect.collidepoint(pygame.mouse.get_pos()) and humus == 0 and TYUI < 30:
                    TYUI += 1
                if d.rect.collidepoint(pygame.mouse.get_pos()) and humus == 0 and TYUI > 11:
                    TYUI -= 1
                if nazad.rect.collidepoint(pygame.mouse.get_pos()) and humus == 0:
                    humus = 1
                if sozd.rect.collidepoint(pygame.mouse.get_pos()) and humus == 0:
                    a = TYUI
                    running = False

    if humus == 1:
        buts.draw(scr)
    if humus == 0:
        text2 = shir.render('ВЫБЕРИТЕ РАЗМЕР ПОЛЯ', True, 'red')
        text = shir.render(f'{TYUI}', True, 'red')
        buttons_new_game.draw(scr)
        scr.blit(pust, (226, 262))
        scr.blit(pst, (50, 165))
        scr.blit(text, (237, 275))
        scr.blit(text2, (68, 175))

    # scr.blit(text, (120, 120))

    for x in buts:
        if aa.rect.collidepoint(pygame.mouse.get_pos()):
            aa.image = load_image('pixil-frame-0 (79).png')

        elif b.rect.collidepoint(pygame.mouse.get_pos()):
            b.image = load_image('pixil-frame-0 (78).png')

        else:
            x.image = x.im

    for y in buttons_new_game:
        if nazad.rect.collidepoint(pygame.mouse.get_pos()):
            nazad.image = load_image('pixil-frame-0 (86).png')
        if sozd.rect.collidepoint(pygame.mouse.get_pos()):
            sozd.image = load_image('SOZD_REW.png')

        else:
            y.image = y.im

    pygame.display.flip()


# класс, генерирующий поле
class RandomMap:
    def __init__(self, ln):
        self.d = ln

    def random_map(self, x=None):
        if not x:
            x = self.d
        s = [list("0" * x) for _ in range(x)]
        for _ in range(int(x ** 2 * 0.125)):
            i = rnd.randint(0, x - 1)
            j = rnd.randint(0, x - 1)
            s[i][j] = '1'

        for _ in range(int(x ** 2 * 0.35)):
            i = rnd.randint(0, x - 1)
            j = rnd.randint(0, x - 1)
            s[i][j] = '3'

        start_pos = [((2, 1), (x - 3, x - 2)), ((x // 2, 1), (x // 2, x - 2)), ((x - 2, 2), (1, x - 3))]
        a = rnd.choice(start_pos)
        s[a[0][0]][a[0][1]] = '9'
        s = self.town_cell(s, a[0][0], a[0][1])
        s[a[1][0]][a[1][1]] = '9'
        s = self.town_cell(s, a[1][0], a[1][1])
        s = self.create_towns(s)

        twn = 0
        while twn != int(0.02 * self.d * self.d):
            q = rnd.randint(0, x ** 2)
            i = q // self.d
            j = q % self.d
            if s[i][j][-1] != 't' and s[i][j][0] != '2' and s[i][j][0] != '9':
                twn += 1
                s[i][j] = '5'
        return s

    def town_cell(self, s, i, j):
        s[i][j + 1] += "t"
        s[i][j - 1] += "t"
        s[i + 1][j] += "t"
        s[i - 1][j] += "t"
        s[i + 1][j + 1] += "t"
        s[i - 1][j - 1] += "qt"
        s[i - 1][j + 1] += "t"
        s[i + 1][j - 1] += "t"
        return s

    def check_cell(self, s, i, j):
        z = [s[i][j + 1], s[i][j - 1], s[i + 1][j], s[i - 1][j],
             s[i + 1][j + 1], s[i - 1][j - 1], s[i - 1][j + 1], s[i + 1][j - 1]]
        for x in z:
            if x[-1] == 't':
                return False
        return True

    def create_towns(self, s):
        for _ in range(int(len(s) ** 2 * 0.041)):
            a = rnd.randint(1, len(s) - 2)
            b = rnd.randint(1, len(s) - 2)
            h = []
            q = True
            z = 0
            while q:
                a = rnd.randint(1, len(s) - 2)
                b = rnd.randint(1, len(s) - 2)
                if self.check_cell(s, a, b):
                    q = False
                    h.append((a, b))
                z += 1
                if z > 200:
                    return s
            s[a][b] = '2'
            s = self.town_cell(s, a, b)
        return s


locations = pygame.sprite.Group()
terrain = pygame.sprite.Group()
cells = pygame.sprite.Group()
pers = pygame.sprite.Group()
mv_group = pygame.sprite.Group()
buttons = pygame.sprite.Group()
borders = pygame.sprite.Group()


# класс игровой клетки
class Tile(pygame.sprite.Sprite):

    def __init__(self, group, x, y, number, sec_group=0):
        super().__init__(group)
        cl = {'0': 'tile1', '1': f'mountain{rnd.randint(0, 1)}', '2': 'village',
              '3': 'forest', '9': 'castle1', '4': 'nether', '5': 'destruction',
              'q': 'none', 'm': 'move', 'a': 'attack', 'd': 'd', 'h': 'h',
              's': 's', 'l': 'l', 'k': 'k', 'g': f'garden{rnd.randint(1, 3)}'}
        if sec_group != 0:
            sec_group.add(self)
        self.im = load_image(f"{cl[number]}.png")
        self.name = number
        self.image = self.im
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.last_k = 1
        self.m = 40
        if self.name == 'q':
            self.m *= 3
        self.a = x
        self.b = y
        self.cl = 0

    def transform(self, kf, mv=False):
        im = pygame.transform.scale(self.im, (self.m * kf, self.m * kf))
        self.image = im
        if not mv:
            self.rect.x = int(self.rect.x / self.last_k)
            self.rect.y = int(self.rect.y / self.last_k)
            self.rect.x = int(self.rect.x * kf)
            self.rect.y = int(self.rect.y * kf)
        self.last_k = kf
        self.mx()

    def reboot(self):
        self.rect.x = self.a
        self.rect.y = self.b
        self.mx()

    def click(self, kf, town=False):
        if self.cl:
            self.im = load_image('tile1.png')
            self.image = self.im
            self.cl = 0
        else:
            self.im = load_image('tile2.png')
            self.image = self.im
            self.cl = 1
        im = pygame.transform.scale(self.im, (kf * self.m, kf * self.m))
        self.image = im

    def mx(self):
        self.rect.w = self.last_k * self.m
        self.rect.h = self.last_k * self.m


# класс управления полем
class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 40
        self.k = 1

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, mp):
        st = [self.top, self.left]
        brd_list = []
        k = 0
        pr = 0
        for i in range(self.height):
            for j in range(self.width):
                Tile(cells, st[0], st[1], '0', locations)
                if mp[i][j] == '9':
                    Town(pr, cells, st[0], st[1], '9', terrain)
                    Hero(pr, cells, st[0], st[1], 'd', pers)
                    pr += 1
                elif int(mp[i][j][0]):
                    Tile(cells, st[0], st[1], mp[i][j][0], terrain)
                if 'q' in mp[i][j]:
                    brd_list.append((st[0], st[1]))
                st[0] += self.cell_size
                k += 1
            st[1] += self.cell_size
            st[0] = self.top
        for i in range(self.height):
            Tile(cells, st[0], st[1], '4')
            st[0] += self.cell_size
        for x in brd_list:
            Tile(cells, x[0], x[1], 'q', borders)
        for t in terrain:
            if t.name == '9':
                for b in borders:
                    if b.rect.x + 40 == t.rect.x and b.rect.y + 40 == t.rect.y:
                        b.im = load_image('border.png')
                        b.image = b.im

    def new(self, mn, nw=False):
        if mn:
            self.k -= 0.5
        else:
            self.k += 0.5
        if nw:
            self.k = 1
        for el in cells:
            el.transform(self.k)
            if nw:
                el.reboot()


# класс персонажа
class Hero(Tile):
    def __init__(self, n, group, x, y, number, sec_group=0):
        super().__init__(group, x, y, number, sec_group)
        hr = {'d': 'default', 'h': 'horse', 's': 'sword', 'l': 'bow', 'k': 'defender'}
        health = {'d': 10, 'h': 10, 'l': 5, 's': 15, 'k': 20}
        damage = {'d': 5, 'h': 4, 'l': 8, 's': 7, 'k': 3}
        speed = {'d': 1}
        self.damage = damage[number]
        self.health = health[number]
        self.speed = 0
        self.pict = hr[number] + str(n)
        self.im = load_image(hr[number] + str(n) + 'r' + '.png')
        self.image = self.im
        self.n = n
        self.atc = 0

    def move(self):
        if not self.cl:
            if self.speed:
                r = 'm'
            else:
                r = 'a'
            q = 40 * board.k
            Tile(cells, self.rect.x - q, self.rect.y - q, r, mv_group)
            Tile(cells, self.rect.x + q, self.rect.y + q, r, mv_group)
            Tile(cells, self.rect.x - q, self.rect.y + q, r, mv_group)
            Tile(cells, self.rect.x + q, self.rect.y - q, r, mv_group)
            Tile(cells, self.rect.x - q, self.rect.y, r, mv_group)
            Tile(cells, self.rect.x, self.rect.y - q, r, mv_group)
            Tile(cells, self.rect.x + q, self.rect.y, r, mv_group)
            Tile(cells, self.rect.x, self.rect.y + q, r, mv_group)
            for sp in mv_group:
                sp.transform(board.k, True)
            for sp in mv_group:
                for sp1 in locations:
                    x = True
                    if sp.rect == sp1.rect:
                        x = False
                        break
                if x:
                    sp.kill()

            if self.atc and self.speed:
                for sp in mv_group:
                    for sp1 in pers:
                        x = True
                        if sp.rect == sp1.rect:
                            x = False
                            pl = sp1.n == self.n
                            break
                    if not x:
                        sp.kill()
                        if not pl:
                            sp_x, sp_y = sp.rect.x, sp.rect.y
                            q = Tile(cells, sp_x, sp_y, 'a', mv_group)
                            q.transform(board.k, True)
            if self.atc and not self.speed:
                for sp in mv_group:
                    for sp1 in pers:
                        x = False
                        if sp.rect == sp1.rect and sp1.n != self.n:
                            x = True
                            break
                    if not x:
                        sp.kill()
        else:
            for sp in mv_group:
                sp.kill()


# класс города
class Town(Tile):
    def __init__(self, n, group, x, y, number, sec_group=0):
        super().__init__(group, x, y, number, sec_group)
        self.transform(board.k, True)
        self.n = n
        self.level = 1
        self.lvlup = 0
        self.lvllen = 2


# класс картинки хотбара
class Interface(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image('hb.png')
        self.image = pygame.transform.scale(self.image, (500, 500))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 400
        self.drw = 0
        self.cart1 = None
        self.cart = pygame.transform.scale(load_image('tile1.png'), (60, 60))

    def inform(self, img=0):
        if img:
            self.cart1 = pygame.transform.scale(img, (60, 60))
        else:
            self.cart1 = None


# функция для надпсией
def text_pers(mot, hp, dmg, pl, nm):
    font = pygame.font.Font(None, 25)
    qq = str(nm)
    if qq in ['d', 'l', 'k', 'h', 's']:
        text_mv = font.render(f"Количество ходов: {mot}", True, (218, 165, 32))
        text_hp = font.render(f"Жизни: {hp}", True, (255, 0, 0))
        text_dmg = font.render(f"Урон: {dmg}", True, (0, 100, 0))
        screen.blit(text_hp, (85, 430))
        if pl:
            screen.blit(text_mv, (85, 472))
            screen.blit(text_dmg, (85, 451))
        else:
            text_not = font.render(f"Это враг!", True, (139, 0, 0))
            screen.blit(text_not, (85, 451))
    elif qq == '9':
        text_lvl = font.render(f"Уровень: {mot}", True, (218, 165, 32))
        text_lvlup = font.render(f"Ресурсы: {hp}/{dmg}", True, (255, 0, 0))
        text_money = font.render(f"Доход: {mot + 1}", True, (0, 225, 0))
        if pl:
            screen.blit(text_lvl, (85, 430))
            screen.blit(text_lvlup, (85, 451))
            screen.blit(text_money, (85, 472))
        else:
            text_not = font.render(f"Это вражеский город", True, (139, 0, 0))
            screen.blit(text_not, (85, 451))

    else:
        cl = {'0': ['Луг. Удобное место', 'для здания в городе'],
              '1': ['Горы. При желании и', 'деньгах можно сравнять'],
              '2': ['Деревня. При захвате', 'становится городом'],
              '3': ['Лес. При желании и', 'деньгах можно срубить'],
              '5': ['Руины. Захватите,', 'чтобы получить бонус'],
              'g': ['Ферма, приносит одно ', 'очко улучшения городу']}
        text_x = 440
        for text in cl[qq]:
            text_terrain = font.render(text, True, (218, 165, 32))
            screen.blit(text_terrain, (85, text_x))
            text_x += 21


# класс кнопки
class Button(pygame.sprite.Sprite):
    def __init__(self, group, x, y, img, q):
        super().__init__(group)
        self.im = load_image(img)
        self.image = self.im

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = q


if a:
    pygame.init()
    TEXT_PERS = [0, 0, 0, 0, None, None]
    # button_coords = None
    player_money = [3, 5, 0]
    skills = [['d', 'l', 'k', 'h', 's'], ['d', 'l', 'k', 'h', 's']]
    upgrade = 0
    player = 1
    clock = pygame.time.Clock()
    end = False
    fps = 30
    pygame.display.set_caption('Fonland')
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    rd_map = RandomMap(a).random_map()
    board = Board(a, a)
    board.render(rd_map)
    land = False
    kords = [a * 8, a * 8]
    for x in pers:
        x.speed = 1
    # camera = Camera()
    fn = load_image("fn.png")
    money = load_image("money.png")
    hb_group = pygame.sprite.Group()
    hb = Interface(hb_group)
    motion = Button(hb_group, 430, 430, 'motion.png', 'ok')
    running = True
    while running:
        screen.blit(fn, (-200, -200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    if upgrade:
                        upgrade = 0
                    else:
                        upgrade = 1
            if event.type == pygame.MOUSEWHEEL and not upgrade:
                if event.y == 1 and board.k < 2:
                    board.new(False)
                    # camera.set_move(board.k)
                elif event.y == -1 and board.k > 1:
                    board.new(True)
                    # camera.set_move(board.k)
            if event.type == pygame.MOUSEBUTTONDOWN and not upgrade:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if event.button == 1:
                    pict = None
                    cn = {'d': 2, 'l': 4, 'k': 3, 'h': 3, 's': 5}
                    for bt_prs in buttons:
                        if bt_prs.name in ['d', 'l', 'k', 'h', 's'] and bt_prs.rect.collidepoint(mouse_x, mouse_y) \
                                and player_money[player] >= cn[bt_prs.name]:
                            for lc in cells:
                                if lc.cl:
                                    porosya = True
                                    for porosenok in pers:
                                        if porosenok.rect == lc.rect:
                                            porosya = False
                                            break
                                    if porosya:
                                        q = Hero(player, cells, lc.rect.x, lc.rect.y, bt_prs.name, pers)
                                        q.transform(board.k, True)
                                        player_money[player] -= cn[bt_prs.name]
                    fl1, fl2, fl3, fl_hb = (0, 0, 0, 0)
                    for b in buttons:
                        if b.rect.collidepoint(event.pos) and b.name == 'f':
                            for l in locations:
                                if l.cl:
                                    lr = l.rect
                            for t in terrain:
                                if t.rect == lr:
                                    for p in pers:
                                        if p.rect == t.rect:
                                            p.speed = 0
                                            p.atc = 0
                                    if TEXT_PERS[5] == '9' and not TEXT_PERS[4]:
                                        t.n = player
                                    elif TEXT_PERS[5] == '5':
                                        player_money[player] += 10
                                        t.kill()
                                    elif TEXT_PERS[5] == '2':
                                        Town(player, cells, t.rect.x, t.rect.y, '9', terrain)
                                        t.kill()
                                    q = 40 * board.k
                                    for r in terrain:
                                        if r.name == '9':
                                            for b in borders:
                                                if b.rect.x + q == r.rect.x and b.rect.y + q == r.rect.y:
                                                    b.im = load_image('border.png')
                                                    b.image = b.im
                                                    b.transform(board.k)
                                    # break
                        if b.rect.collidepoint(event.pos) and b.name == 'm':
                            for l in locations:
                                if l.cl:
                                    for t in terrain:
                                        if t.rect == l.rect and player_money[player] >= 2:
                                            player_money[player] -= 2
                                            t.kill()
                        if b.rect.collidepoint(event.pos) and b.name == 'g':
                            for loct in locations:
                                if loct.cl and player_money[player] >= 2:
                                    o = Tile(cells, loct.rect.x, loct.rect.y, 'g', terrain)
                                    o.transform(board.k, True)
                                    player_money[player] -= 2
                                    land.lvlup += 1
                                    if land.lvllen == land.lvlup:
                                        land.level += 1
                                        land.lvllen = 3
                                        land.lvlup = 0
                                        land.im = load_image(f'castle{land.level}.png')
                                        land.image = land.im
                                        land.transform(board.k, True)
                    for elem_mv in mv_group:
                        if elem_mv.rect.collidepoint(mouse_x, mouse_y) and \
                                not hb.rect.collidepoint(mouse_x, mouse_y):
                            fl_p = 1
                            for elem2 in pers:
                                if elem2.rect == elem_mv.rect:
                                    fl_p = 0
                                    for elem_pr in pers:
                                        if elem_pr.cl:
                                            elem2.health -= elem_pr.damage
                                            elem_pr.move()
                                            elem_pr.cl = 0
                                            elem_pr.atc = 0
                                            if elem_pr.name[0] != 'h':
                                                elem_pr.speed = 0
                                            if elem2.health <= 0:
                                                elem_pr.rect = elem2.rect
                                                elem2.kill()
                                            else:
                                                elem_pr.health -= elem2.damage
                                                if elem_pr.health <= 0:
                                                    elem_pr.kill()
                                            fl3 = 1
                            if fl_p:
                                for elem2 in pers:
                                    if elem2.cl and player == elem2.n:
                                        elem2.move()
                                        elem2.cl = 0
                                        if elem2.rect.x > elem_mv.rect.x:
                                            elem2.im = load_image(elem2.pict + 'l' + '.png')
                                        elif elem2.rect.x < elem_mv.rect.x:
                                            elem2.im = load_image(elem2.pict + 'r' + '.png')
                                        elem2.image = pygame.transform.scale(elem2.im, (40 * board.k, 40 * board.k))
                                        elem2.rect = elem_mv.rect
                                        elem2.speed -= 1
                                        fl3 = 1
                                        TEXT_PERS[1] -= 1
                    if not fl3:
                        el_x, el_y = (None, None)
                        for elem in locations:
                            if elem.cl:
                                elem.click(board.k)
                                TEXT_PERS[5] = None
                                hb.drw = 0
                                TEXT_PERS[0] = 0
                                el_x, el_y = elem.rect.x, elem.rect.y
                        for elem in locations:
                            if not elem.cl and elem.rect.collidepoint(mouse_x, mouse_y) and \
                                    not hb.rect.collidepoint(mouse_x, mouse_y) and \
                                    not (el_x == elem.rect.x and el_y == elem.rect.y):
                                elem.click(board.k)
                                hb.drw = 1
                                TEXT_PERS[0] = 1
                                TEXT_PERS[5] = elem.name[0]
                                button_coords = elem.rect
                                for elem1 in terrain:
                                    if elem1.rect.collidepoint(mouse_x, mouse_y):
                                        hb.inform(elem1.im)
                                        fl2 = 1
                                        TEXT_PERS[5] = elem1.name[0]
                                        if elem1.name[0] == '9':
                                            TEXT_PERS[1] = elem1.level
                                            TEXT_PERS[2] = elem1.lvlup
                                            TEXT_PERS[3] = elem1.lvllen
                                            TEXT_PERS[4] = (elem1.n == player)
                                if not fl2:
                                    hb.inform()
                        for elem2 in pers:
                            if elem2.cl:
                                elem2.move()
                                elem2.cl = 0
                        for elem in hb_group:
                            if elem != hb and elem.rect.collidepoint(mouse_x, mouse_y):
                                hb.drw = 0
                                TEXT_PERS[0] = 0
                                if player == 1:
                                    player = 0
                                else:
                                    player = 1
                                for elem_pl in pers:
                                    if elem_pl.n == player:
                                        elem_pl.speed = 1
                                        if elem_pl.name == 'h':
                                            elem_pl.speed = 2
                                        elem_pl.atc = 1
                                for elem_twn in terrain:
                                    if elem_twn.name == '9':
                                        if elem_twn.n == player:
                                            player_money[player] += (elem_twn.level + 1)
                                flag_end = True
                                for popug in terrain:
                                    if popug.name == '9':
                                        if popug.n == player:
                                            flag_end = False
                                            break
                                if flag_end:
                                    upgrade = 1

                elif event.button == 3:
                    for elem in locations:
                        if elem.cl:
                            elem.click(board.k)
                            hb.drw = 0
                    el_x, el_y = (None, None)
                    for elem2 in pers:
                        if elem2.cl:
                            elem2.move()
                            elem2.cl = 0
                            hb.drw = 0
                            TEXT_PERS[0] = 0
                            el_x, el_y = (elem2.rect.x, elem2.rect.y)
                    for elem2 in pers:
                        if elem2.rect.collidepoint(mouse_x, mouse_y) and \
                                (elem2.rect.x != el_x and elem2.rect.y != el_y) \
                                and not hb.rect.collidepoint(mouse_x, mouse_y):
                            if (elem2.atc or elem2.speed) and elem2.n == player:
                                elem2.move()
                            elem2.cl = 1
                            hb.drw = 1
                            hb.inform(elem2.im)
                            TEXT_PERS[0] = 1
                            TEXT_PERS[1] = elem2.speed
                            TEXT_PERS[2] = elem2.health
                            TEXT_PERS[3] = elem2.damage
                            TEXT_PERS[4] = (elem2.n == player)
                            TEXT_PERS[5] = elem2.name[0]
            for btn in buttons:
                btn.kill()
            if (TEXT_PERS[5] == '9' and not TEXT_PERS[4]) or TEXT_PERS[5] in ('2', '5') and TEXT_PERS[0]:
                for prs in pers:
                    if prs.n == player:
                        if prs.speed and prs.atc and prs.rect == button_coords:
                            Button(buttons, 300, 430, 'catch.png', 'f')
                            break
            elif TEXT_PERS[4] and TEXT_PERS[5] == '9':
                krd = 195
                for x in skills[player]:
                    if x in ['d', 'l', 'k', 'h', 's']:
                        Button(buttons, krd, 440, f'{x}.png', x)
                        krd += 45
            elif TEXT_PERS[5] in ('1', '3', '0'):
                for zln in locations:
                    if zln.cl:
                        bz = zln
                bk = 40 * board.k
                j = list()
                j.append((bz.rect.x - bk, bz.rect.y - bk))
                j.append((bz.rect.x + bk, bz.rect.y + bk))
                j.append((bz.rect.x + bk, bz.rect.y - bk))
                j.append((bz.rect.x - bk, bz.rect.y + bk))
                j.append((bz.rect.x, bz.rect.y + bk))
                j.append((bz.rect.x, bz.rect.y - bk))
                j.append((bz.rect.x + bk, bz.rect.y))
                j.append((bz.rect.x - bk, bz.rect.y))
                if TEXT_PERS[5] in ('1', '3'):
                    for lnd in terrain:
                        if (lnd.rect.x, lnd.rect.y) in j and lnd.name == '9':
                            if lnd.n == player:
                                Button(buttons, 300, 430, 'get.png', 'm')
                else:
                    for lnd in terrain:
                        if (lnd.rect.x, lnd.rect.y) in j and lnd.name == '9':
                            if lnd.n == player:
                                kaban = True
                                for ter in terrain:
                                    if bz.rect == ter.rect and ter.name == 'g':
                                        kaban = False
                                        break
                                if kaban:
                                    Button(buttons, 300, 430, 'grdn.png', 'g')
                                    land = lnd

        if not upgrade:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            bar = (a + 2) * 20
            # управление камерой
            if 485 < mouse_x < 500 and kords[0] > - bar:
                for x in cells:
                    x.rect.x -= 180 * board.k / fps
                kords[0] -= 180 / fps
            if 485 < mouse_y < 500 and kords[1] > - bar:
                for x in cells:
                    x.rect.y -= 180 * board.k / fps
                kords[1] -= 180 / fps
            if 0 < mouse_x < 15 and kords[0] < bar:
                for x in cells:
                    x.rect.x += 180 * board.k / fps
                kords[0] += 180 / fps
            if 0 < mouse_y < 15 and kords[1] < bar:
                for x in cells:
                    x.rect.y += 180 * board.k / fps
                kords[1] += 180 / fps
            cells.draw(screen)
            # borders.draw(screen)
            pers.draw(screen)
            hb_group.draw(screen)
            font = pygame.font.Font(None, 30)
            text_player_money = font.render(f"x {player_money[player]}", True, (255, 215, 0))
            screen.blit(text_player_money, (445, 20))
            screen.blit(money, (405, 10))
            buttons.draw(screen)

            bt_sl = {}
            if hb.drw:
                screen.blit(hb.cart, (20, 430))
                if hb.cart1:
                    screen.blit(hb.cart1, (20, 430))
            if TEXT_PERS[0]:
                text_pers(TEXT_PERS[1], TEXT_PERS[2], TEXT_PERS[3], TEXT_PERS[4], TEXT_PERS[5])
            clock.tick(fps)
        else:
            font = pygame.font.Font(None, 30)
            kmnd = {0: 'синих', 1: 'красных'}
            color = {0: 'lightblue', 1: 'red'}
            text_end = font.render(f"Выиграла команда {kmnd[player]}!", True, color[player])
            screen.blit(text_end, (115, 250))
        pygame.display.flip()
pygame.quit()

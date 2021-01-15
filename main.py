import sqlite3
import pygame
import os
import sys
from random import shuffle, random, randrange

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Лиса')
clock = pygame.time.Clock()
player = None
all_sprites = pygame.sprite.Group()
a = []

con = sqlite3.connect("play.db")
cur = con.cursor()


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


def terminate():
    pygame.quit()
    sys.exit()


def chot(n):
    res = cur.execute(f"""SELECT * FROM Information
                            WHERE id = 1""").fetchall()
    if n == 1:
        m = res[0][0] - (res[0][1] + 1) * 100
        f = res[0][1] + 1
        if m >= 0:
            cur.execute(f"""UPDATE Information
                        SET fifty_fifty = {f}
                        WHERE id = 1""").fetchall()
            cur.execute(f"""UPDATE Information
                                    SET money = {m}
                                    WHERE id = 1""").fetchall()
            con.commit()
        if m < 0:
            return 1

    if n == 2:
        m = res[0][0] - (res[0][2] + 1) * 100
        f = res[0][2] + 1
        if m >= 0:
            cur.execute(f"""UPDATE Information
                                SET one_mistake = {f}
                                WHERE id = 1""").fetchall()
            cur.execute(f"""UPDATE Information
                                SET money = {m}
                                WHERE id = 1""").fetchall()
            con.commit()
        else:
            return 1

    if n == 3:
        m = res[0][0] - (res[0][3] + 1) * 100
        f = res[0][3] + 1
        if m >= 0:
            cur.execute(f"""UPDATE Information
                                SET money = {m}
                                WHERE id = 1""").fetchall()
            cur.execute(f"""UPDATE Information
                            SET change = {f}
                            WHERE id = 1""").fetchall()
        else:
            return 1


def help_from_liza():
    res = cur.execute(f"""SELECT * FROM Information
                                    WHERE id = 1""").fetchall()
    mn = pygame.font.Font(None, 24)
    text1 = mn.render(str(res[0][0]), True, (0, 0, 0))
    screen.blit(text1, [374, 18])

    ff = pygame.font.Font(None, 24)
    text2 = ff.render(str(res[0][1]), True, (0, 0, 0))
    screen.blit(text2, [137, 150])

    ffc = pygame.font.Font(None, 24)
    text21 = ffc.render(str((res[0][1] + 1) * 100), True, (0, 0, 0))
    screen.blit(text21, [221, 150])

    po = pygame.font.Font(None, 24)
    text3 = po.render(str(res[0][2]), True, (0, 0, 0))
    screen.blit(text3, [137, 228])

    poc = pygame.font.Font(None, 24)
    text31 = poc.render(str((res[0][2] + 1) * 100), True, (0, 0, 0))
    screen.blit(text31, [221, 228])

    pv = pygame.font.Font(None, 24)
    text4 = pv.render(str((res[0][3])), True, (0, 0, 0))
    screen.blit(text4, [137, 310])

    pvc = pygame.font.Font(None, 24)
    text41 = pvc.render(str((res[0][3] + 1) * 100), True, (0, 0, 0))
    screen.blit(text41, [221, 310])


def kpod(a):
    help_from_liza()
    if a == 1:
        osh = pygame.font.Font(None, 24)
        txt = osh.render('НЕДОСТАТОЧНО СРЕДСТВ', True, (0, 0, 0))
        screen.blit(txt, [137, 360])


def podsk():
    dd = pygame.transform.scale(load_image('dob.png'), (width, height))
    screen.blit(dd, (0, 0))
    kpod(0)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and\
                    2 <= event.pos[0] <= 92 and 1 <= event.pos[1] <= 28:
                return 0
            elif event.type == pygame.MOUSEBUTTONDOWN and\
                    (332 - event.pos[0]) ** 2 + (159 - event.pos[1]) ** 2 <= 400:
                a = chot(1)
                screen.blit(dd, (0, 0))
                kpod(a)
            elif event.type == pygame.MOUSEBUTTONDOWN and\
                    (332 - event.pos[0]) ** 2 + (236 - event.pos[1]) ** 2 <= 400:
                a = chot(2)
                screen.blit(dd, (0, 0))
                kpod(a)
            elif event.type == pygame.MOUSEBUTTONDOWN and\
                    (332 - event.pos[0]) ** 2 + (315 - event.pos[1]) ** 2 <= 400:
                a = chot(3)
                screen.blit(dd, (0, 0))
                kpod(a)
        pygame.display.flip()
        clock.tick(50)


class Bomb(pygame.sprite.Sprite):
    image = load_image("ht.jpg")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Bomb.image
        self.rect = self.image.get_rect()
        self.rect.x = randrange(1, 500)
        self.rect.y = randrange(220, 450)

    def update(self):
        self.rect = self.rect.move(randrange(3) - 1,
                                   randrange(3) - 1)


def heart():
    h = pygame.transform.scale(load_image('hart.png'), (width, height))
    screen.blit(h, (0, 0))
    for _ in range(15):
        Bomb(all_sprites)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and\
                    393 <= event.pos[0] <= 497 and 5 <= event.pos[1] <= 30:
                return 0
        screen.blit(h, (0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(100)


def start_screen():
    res = cur.execute(f"""SELECT * FROM Information
                        WHERE id = 1""").fetchall()
    intro_text = [str(res[0][0])]

    fon = pygame.transform.scale(load_image('front.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 25)
    text_coord = 0

    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 15
        intro_rect.top = text_coord
        intro_rect.x = 360
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and 156 <= event.pos[0] <= 334 and 151 <= event.pos[1] <= 181:
                a.append('лёгкий')
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and 156 <= event.pos[0] <= 333 and 197 <= event.pos[1] <= 227:
                a.append('средний')
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and 154 <= event.pos[0] <= 332 and 247 <= event.pos[1] <= 277:
                a.append('hard')
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and 155 <= event.pos[0] <= 333 and 277 <= event.pos[1] <= 327:
                a.append('mix')
            elif event.type == pygame.MOUSEBUTTONDOWN and 422 <= event.pos[0] <= 475 and 60 <= event.pos[1] <= 107:
                g = podsk()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and 14 <= event.pos[0] <= 415 and 85 <= event.pos[1] <= 482:
                g = heart()
                return
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(50)


def play_game(s):
    play = pygame.transform.scale(load_image('game.png'), (width, height))
    screen.blit(play, (0, 0))
    intro_text = s[1:-5]
    font = pygame.font.Font(None, 25)
    text_coord = 170
    if 90 > len(intro_text[0]) > 30:
        k = intro_text[0].split()
        j = [' '.join(k[:3]), ' '.join(k[3:6]), ' '.join(k[6:])]
        for line in j:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 15
            intro_rect.top = text_coord
            intro_rect.x = 100
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
    elif 120 > len(intro_text[0]) > 90:
        k = intro_text[0].split()
        j = [' '.join(k[:4]), ' '.join(k[4:8]), ' '.join(k[8:10]), ' '.join(k[10:])]
        for line in j:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 15
            intro_rect.top = text_coord
            intro_rect.x = 100
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
    elif len(intro_text[0]) > 120:
        k = intro_text[0].split()
        j = [' '.join(k[:3]), ' '.join(k[3:6]), ' '.join(k[6:9]), ' '.join(k[9: 12]), ' '.join(k[12:])]
        for line in j:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 15
            intro_rect.top = text_coord
            intro_rect.x = 100
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
    else:
        string_rendered = font.render(intro_text[0], 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 15
        intro_rect.top = text_coord
        intro_rect.x = 100
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    # 1
    text_coord = 320
    string_rendered = font.render(intro_text[1], 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    text_coord += 15
    intro_rect.top = text_coord
    intro_rect.x = 80
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)
    # 3
    text_coord = 375
    string_rendered = font.render(intro_text[3], 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    text_coord += 15
    intro_rect.top = text_coord
    intro_rect.x = 80
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)
    # 2
    text_coord = 320
    string_rendered = font.render(intro_text[2], 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    text_coord += 15
    intro_rect.top = text_coord
    intro_rect.x = 280
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)
    # 4
    text_coord = 375
    string_rendered = font.render(intro_text[4], 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    text_coord += 15
    intro_rect.top = text_coord
    intro_rect.x = 280
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)


def answer(a, s):
    k = str(s[6])
    if a == k:
        return 1
    return 0


def prompting(a, s=[]):
    if a == 'fifty':
        res = cur.execute(f"""SELECT fifty_fifty FROM Information
                                        WHERE id = 1""").fetchall()[0][0]
        if res > 0:
            s[2] = s[7]
            s[3] = s[8]
            s[4] = s[9]
            s[5] = s[10]
            res -= 1
            cur.execute(f"""UPDATE Information
                            SET fifty_fifty = {res}
                            WHERE id = 1""").fetchall()
            con.commit()
        return s
    elif a == 'pravo':
        res = cur.execute(f"""SELECT one_mistake FROM Information
                                                WHERE id = 1""").fetchall()[0][0]
        if res > 0:
            res -= 1
            cur.execute(f"""UPDATE Information
                                    SET one_mistake = {res}
                                    WHERE id = 1""").fetchall()
            con.commit()
            return 1
        return 0
    elif a == 'change':
        res = cur.execute(f"""SELECT change FROM Information
                                                WHERE id = 1""").fetchall()[0][0]
        if res > 0:
            res -= 1
            cur.execute(f"""UPDATE Information
                                    SET change = {res}
                                    WHERE id = 1""").fetchall()
            con.commit()
            return 1
        return 0


def money(k, a):
    if k < 15 and a == 0:
        ch = cur.execute(f"""SELECT play FROM winning
                                   WHERE id = {k}""").fetchall()[0][0]
        mon = pygame.font.Font(None, 28)
        text5 = mon.render(str(ch), True, (0, 0, 0))
        screen.blit(text5, [129, 34])
        num = pygame.font.Font(None, 35)
        text6 = num.render(str(k + 1), True, (0, 0, 0))
        screen.blit(text6, [70, 112])
    elif a == 1:
        ch = cur.execute(f"""SELECT * FROM winning
                                WHERE id = {k}""").fetchall()[0]
        mon = pygame.font.Font(None, 28)
        text5 = mon.render(str(ch[0]), True, (0, 0, 0))
        screen.blit(text5, [127, 130])
        re = pygame.font.Font(None, 28)
        text6 = re.render(str(ch[1]), True, (0, 0, 0))
        screen.blit(text6, [180, 235])


def resmoney(k):
    ch = cur.execute(f"""SELECT * FROM winning
                                    WHERE id = {k}""").fetchall()[0]
    m = cur.execute(f"""SELECT money FROM Information
                                        WHERE id = 1""").fetchall()[0][0]
    cur.execute(f"""UPDATE Information
                            SET money = {m + ch[1]}
                            WHERE id = 1""").fetchall()
    con.commit()


if __name__ == '__main__':
    while len(a) == 0:
        start_screen()
    if a[0] == 'лёгкий':
        res1 = [item[0] for item in cur.execute(f"""SELECT Ask FROM questions
                                WHERE Type = 'Лёгкий'""").fetchall()]
    elif a[0] == 'средний':
        res1 = [item[0] for item in cur.execute(f"""SELECT Ask FROM questions
                                WHERE Type = 'Средний'""").fetchall()]
    elif a[0] == 'hard':
        res1 = [item[0] for item in cur.execute(f"""SELECT Ask FROM questions
                                WHERE Type = 'Сложный'""").fetchall()]
    elif a[0] == 'mix':
        res1 = [item[0] for item in cur.execute(f"""SELECT Ask FROM questions""").fetchall()]
    shuffle(res1)
    slovar = []
    dop = res1[15:]
    dop1 = 0
    dop_1 = []
    res = res1[:15]
    for i in res:
        d = [x for x in cur.execute(f"""SELECT * FROM questions
                        WHERE Ask = '{i}'""").fetchall()[0]]
        slovar.append(d)
    for i in dop:
        d = [x for x in cur.execute(f"""SELECT * FROM questions
                        WHERE Ask = '{i}'""").fetchall()[0]]
        dop_1.append(d)
    i = 0
    h = -1
    p = 1
    t = 0
    help_1 = 0
    help_2 = 0
    while i <= 15:
        if i < 15:
            play_game(slovar[i])
            money(i, 0)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 16
                    p = 0
                elif event.type == pygame.MOUSEBUTTONDOWN and 58 <= event.pos[0] <= 234 and\
                        325 <= event.pos[1] <= 365:
                    h = answer('1', slovar[i])
                elif event.type == pygame.MOUSEBUTTONDOWN and 268 <= event.pos[0] <= 444 and\
                        325 <= event.pos[1] <= 365:
                    h = answer('2', slovar[i])
                elif event.type == pygame.MOUSEBUTTONDOWN and 58 <= event.pos[0] <= 234 and\
                        384 <= event.pos[1] <= 423:
                    h = answer('3', slovar[i])
                elif event.type == pygame.MOUSEBUTTONDOWN and 268 <= event.pos[0] <= 444 and\
                        384 <= event.pos[1] <= 423:
                    h = answer('4', slovar[i])
                elif event.type == pygame.MOUSEBUTTONDOWN and 165 - 32 <= event.pos[0] <= 165 + 32 and\
                        458 - 32 <= event.pos[1] <= 458 + 32:
                    slovar[i] = prompting('fifty', slovar[i])
                elif event.type == pygame.MOUSEBUTTONDOWN and 248 - 32 <= event.pos[0] <= 248 + 32 and\
                        460 - 32 <= event.pos[1] <= 460 + 32:
                    help_1 = prompting('pravo')
                elif event.type == pygame.MOUSEBUTTONDOWN and 328 - 32 <= event.pos[0] <= 328 + 32 and\
                        464 - 32 <= event.pos[1] <= 464 + 32:
                    help_2 = prompting('change')
                elif event.type == pygame.MOUSEBUTTONDOWN and 406 <= event.pos[0] < 498 and\
                        1 <= event.pos[1] <= 27:
                    t = i
                    p = 2
                    i = 15
                if help_2 == 1:
                    slovar[i] = dop_1[dop1]
                    dop1 += 1
                    help_2 = 0
                if h == 1:
                    i += 1
                    h = -1
                    help_1 = 0
                elif h == 0 and help_1 == 1:
                    help_1 = 0
                    h = -1
                elif h == 0 and help_1 == 0:
                    i = 15
                    p = 0

        elif i == 15:
            play = pygame.transform.scale(load_image('res.png'), (width, height))
            screen.blit(play, (0, 0))
            if p == 0:
                money(16, 1)
            elif p == 1:
                money(i, 1)
            elif p == 2:
                money(t, 1)
                resmoney(t)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 16
                    if p == 1:
                        resmoney(15)
                    elif p == 2:
                        resmoney(t)
                    elif p == 0:
                        pass
        pygame.display.flip()
    pygame.quit()

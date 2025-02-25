import pygame
from random import randint
import sys
import os

def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    intro_text = ["МАРИО ЖДАЛ ВАС", "",
                  "Правила игры",
                  "Ходите стрелками,",
                  "не бейтесь об стены слишком много раз"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def generate_level(level):
    global new_player1
    global new_player2
    global new_player3
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == 'v':
                Tile('empty', x, y)
                new_player1 = Voin(x, y)
            elif level[y][x] == 's':
                Tile('empty', x, y)
                new_player2 = Spearman(x, y)
            elif level[y][x] == 'c':
                Tile('empty', x, y)
                new_player3 = Cavalry(x, y)
            elif level[y][x] == 'e':
                Tile('empty', x, y)
                new_enemy1 = enemy_Cavalry(x, y)
            elif level[y][x] == 'w':
                Tile('empty', x, y)
                new_enemy2 = enemy_Voin(x, y)
            elif level[y][x] == 'q':
                Tile('empty', x, y)
                new_enemy3 = enemy_Spearman(x, y)
    return new_player1, new_player2, new_player3, x, y

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

class enemy_Voin(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y
        super().__init__(player_group, all_sprites)
        self.image = enemy_voin_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def coord(self):
        return self.x, self.y

class enemy_Spearman(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y
        super().__init__(player_group, all_sprites)
        self.image = enemy_spearman_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def coord(self):
        return self.x, self.y

class enemy_Cavalry(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y
        super().__init__(player_group, all_sprites)
        self.image = enemy_cavalry_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def coord(self):
        return self.x, self.y
class Voin(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y
        super().__init__(player_group, all_sprites)
        self.image = voin_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def coord(self):
        return self.x, self.y

class Spearman(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y
        super().__init__(player_group, all_sprites)
        self.image = spearman_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def coord(self):
        return self.x, self.y

class Cavalry(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y
        super().__init__(player_group, all_sprites)
        self.image = cavalry_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def coord(self):
        return self.x, self.y

def fight(unit, direction):
    global mp
    global pvp
    global hp_voin
    global hp_enemy_voin
    global count_voin
    global count_enemy_voin
    global hp_spearman
    global hp_cavalry
    global count_spearman
    global count_cavalry
    global hp_enemy_spearman
    global hp_enemy_cavalry
    global count_enemy_spearmen
    global count_enemy_cavalry
    x, y = unit.coord()
    if direction == 'down':
        pvp = mp[y][x] + mp[y + 1][x]
        if mp[y][x] == 'v':
            cnt = count_voin
            hp = hp_voin
        elif mp[y][x] == 's':
            hp = hp_spearman
            cnt = count_spearman
        else:
            hp = hp_cavalry
            cnt = count_cavalry
        if mp[y + 1][x] == 'w':
            enemy_hp = hp_enemy_voin
            enemy_cnt = count_enemy_voin
        elif mp[y + 1][x] == 'e':
            enemy_hp = hp_enemy_spearman
            enemy_cnt = count_enemy_spearmen
        else:
            enemy_hp = hp_enemy_cavalry
            enemy_cnt = count_enemy_cavalry
        enemy_hp -= fight_damage[pvp][0] * cnt
        hp -= fight_damage[pvp][1] * enemy_cnt
        if hp < 0:
            hp = 0
        if enemy_hp < 0:
            enemy_hp = 0
        cnt = (hp + 9) // 10
        enemy_cnt = (enemy_hp + 9) // 10
        if mp[y][x] == 'v':
            count_voin = cnt
            hp_voin = hp
        elif mp[y][x] == 's':
            hp_spearman = hp
            count_spearman = cnt
        else:
            hp_cavalry = hp
            count_cavalry = cnt
        if mp[y + 1][x] == 'w':
            hp_enemy_voin = enemy_hp
            count_enemy_voin = enemy_cnt
        elif mp[y + 1][x] == 'e':
            hp_enemy_spearman = enemy_hp
            count_enemy_spearmen = enemy_cnt
        else:
            hp_enemy_cavalry = enemy_hp
            count_enemy_cavalry = enemy_cnt
        if cnt == 0:
            mp[y] = mp[y][:x] + '.' + mp[y][x + 1:]
        if enemy_cnt == 0:
            mp[y + 1] = mp[y + 1][:x] + mp[y][x] + mp[y + 1][x + 1:]
            mp[y] = mp[y][:x] + '.' + mp[y][x + 1:]
    if direction == 'up':
        pvp = mp[y][x] + mp[y - 1][x]
        if mp[y][x] == 'v':
            cnt = count_voin
            hp = hp_voin
        elif mp[y][x] == 's':
            hp = hp_spearman
            cnt = count_spearman
        else:
            hp = hp_cavalry
            cnt = count_cavalry
        if mp[y - 1][x] == 'w':
            enemy_hp = hp_enemy_voin
            enemy_cnt = count_enemy_voin
        elif mp[y - 1][x] == 'e':
            enemy_hp = hp_enemy_spearman
            enemy_cnt = count_enemy_spearmen
        else:
            enemy_hp = hp_enemy_cavalry
            enemy_cnt = count_enemy_cavalry
        enemy_hp -= fight_damage[pvp][0] * cnt
        hp -= fight_damage[pvp][1] * enemy_cnt
        if hp < 0:
            hp = 0
        if enemy_hp < 0:
            enemy_hp = 0
        cnt = (hp + 9) // 10
        enemy_cnt = (enemy_hp + 9) // 10

        if mp[y][x] == 'v':
            count_voin = cnt
            hp_voin = hp
        elif mp[y][x] == 's':
            hp_spearman = hp
            count_spearman = cnt
        else:
            hp_cavalry = hp
            count_cavalry = cnt
        if mp[y - 1][x] == 'w':
            hp_enemy_voin = enemy_hp
            count_enemy_voin = enemy_cnt
        elif mp[y - 1][x] == 'e':
            hp_enemy_spearman = enemy_hp
            count_enemy_spearmen = enemy_cnt
        else:
            hp_enemy_cavalry = enemy_hp
            count_enemy_cavalry = enemy_cnt
        if cnt == 0:
            mp[y] = mp[y][:x] + '.' + mp[y][x + 1:]
        if enemy_cnt == 0:
            mp[y - 1] = mp[y - 1][:x] + mp[y][x] + mp[y - 1][x + 1:]
            mp[y] = mp[y][:x] + '.' + mp[y][x + 1:]
    if direction == 'right':
        pvp = mp[y][x] + mp[y][x + 1]
        if mp[y][x] == 'v':
            cnt = count_voin
            hp = hp_voin
        elif mp[y][x] == 's':
            hp = hp_spearman
            cnt = count_spearman
        else:
            hp = hp_cavalry
            cnt = count_cavalry
        if mp[y][x + 1] == 'w':
            enemy_hp = hp_enemy_voin
            enemy_cnt = count_enemy_voin
        elif mp[y][x + 1] == 'e':
            enemy_hp = hp_enemy_spearman
            enemy_cnt = count_enemy_spearmen
        else:
            enemy_hp = hp_enemy_cavalry
            enemy_cnt = count_enemy_cavalry
        enemy_hp -= fight_damage[pvp][0] * cnt
        hp -= fight_damage[pvp][1] * enemy_cnt
        if hp < 0:
            hp = 0
        if enemy_hp < 0:
            enemy_hp = 0
        cnt = (hp + 9) // 10
        enemy_cnt = (enemy_hp + 9) // 10
        if mp[y][x] == 'v':
            count_voin = cnt
            hp_voin = hp
        elif mp[y][x] == 's':
            hp_spearman = hp
            count_spearman = cnt
        else:
            hp_cavalry = hp
            count_cavalry = cnt
        if mp[y][x + 1] == 'w':
            hp_enemy_voin = enemy_hp
            count_enemy_voin = enemy_cnt
        elif mp[y][x + 1] == 'e':
            hp_enemy_spearman = enemy_hp
            count_enemy_spearmen = enemy_cnt
        else:
            hp_enemy_cavalry = enemy_hp
            count_enemy_cavalry = enemy_cnt
        if cnt == 0:
            mp[y] = mp[y][:x] + '.' + mp[y][x + 1:]
        if enemy_cnt == 0:
            mp[y] = mp[y][:x] + '.' + mp[y][x] + mp[y][x + 2:]
    if direction == 'left':
        pvp = mp[y][x] + mp[y][x + 1]
        if mp[y][x] == 'v':
            cnt = count_voin
            hp = hp_voin
        elif mp[y][x] == 's':
            hp = hp_spearman
            cnt = count_spearman
        else:
            hp = hp_cavalry
            cnt = count_cavalry
        if mp[y][x - 1] == 'w':
            enemy_hp = hp_enemy_voin
            enemy_cnt = count_enemy_voin
        elif mp[y][x - 1] == 'e':
            enemy_hp = hp_enemy_spearman
            enemy_cnt = count_enemy_spearmen
        else:
            enemy_hp = hp_enemy_cavalry
            enemy_cnt = count_enemy_cavalry
        enemy_hp -= fight_damage[pvp][0] * cnt
        hp -= fight_damage[pvp][1] * enemy_cnt
        if hp < 0:
            hp = 0
        if enemy_hp < 0:
            enemy_hp = 0
        cnt = (hp + 9) // 10
        enemy_cnt = (enemy_hp + 9) // 10
        if mp[y][x] == 'v':
            count_voin = cnt
            hp_voin = hp
        elif mp[y][x] == 's':
            hp_spearman = hp
            count_spearman = cnt
        else:
            hp_cavalry = hp
            count_cavalry = cnt
        if mp[y][x - 1] == 'w':
            hp_enemy_voin = enemy_hp
            count_enemy_voin = enemy_cnt
        elif mp[y][x - 1] == 'e':
            hp_enemy_spearman = enemy_hp
            count_enemy_spearmen = enemy_cnt
        else:
            hp_enemy_cavalry = enemy_hp
            count_enemy_cavalry = enemy_cnt
        if cnt == 0:
            mp[y] = mp[y][:x] + '.' + mp[y][x + 1:]
        if enemy_cnt == 0:
            mp[y] = mp[y][:x] + '.' + mp[y][x] + mp[y][x + 2:]
def move(unit):
    global mp
    x, y = unit.coord()
    if pygame.K_DOWN == event.key:
        if mp[y + 1][x] == '.':
            mp[y + 1] = mp[y + 1][:x] + mp[y][x] + mp[y + 1][x + 1:]
            mp[y] = mp[y][:x] + '.' + mp[y][x + 1:]
        elif mp[y + 1][x] in 'qwe':
            fight(unit, 'down')

    if pygame.K_UP == event.key:
        if mp[y - 1][x] == '.':
            mp[y - 1] = mp[y - 1][:x] + mp[y][x] + mp[y - 1][x + 1:]
            mp[y] = mp[y][:x] + '.' + mp[y][x + 1:]
        elif mp[y - 1][x] in 'qwe':
            fight(unit, 'up')

    if pygame.K_RIGHT == event.key:
        if mp[y][x + 1] == '.':
            mp[y] = mp[y][:x] + '.' + mp[y][x] + mp[y][x + 2:]

        elif mp[y][x + 1] in 'qwe':
            fight(unit, 'right')

    if pygame.K_LEFT == event.key:
        if mp[y][x - 1] == '.':
            mp[y] = mp[y][:x - 1] + mp[y][x] + '.' + mp[y][x + 1:]

        elif mp[y][x - 1] in 'qwe':
            fight(unit, 'left')


if __name__ == '__main__':

    fight_damage = {'vq': (3, 6), 'sw': (3, 6), 'ce': (3, 6), 'vw': (4, 4),
                    'se': (4, 4), 'cq': (4, 4), 've': (6, 3), 'sq': (6, 3), 'cw': (6, 3)}

    tile_images = {
        'wall': load_image('box.png'),
        'empty': load_image('grass.png')
    }
    voin_image = load_image('voin.png')
    voin_image = pygame.transform.scale(voin_image, (70, 100))

    cavalry_image = load_image('cavalry.png')
    cavalry_image = pygame.transform.scale(cavalry_image, (70, 100))
    spearman_image = load_image('spearman.png')
    spearman_image = pygame.transform.scale(spearman_image, (70, 100))

    enemy_voin_image = load_image('enemy_voin.png')
    enemy_voin_image = pygame.transform.scale(enemy_voin_image, (70, 100))

    enemy_cavalry_image = load_image('enemy_cavalry.png')
    enemy_cavalry_image = pygame.transform.scale(enemy_cavalry_image, (70, 100))
    enemy_spearman_image = load_image('enemy_spearman.png')
    enemy_spearman_image = pygame.transform.scale(enemy_spearman_image, (70, 100))

    tile_width = tile_height = 100
    player = None

    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    count_voin = 100
    count_spearman = 100
    count_cavalry = 100
    hp_voin = count_voin * 10
    hp_spearman = count_spearman * 10
    hp_cavalry = count_cavalry * 10
    count_enemy = randint(250, 350)
    count_enemy_voin = randint(0, count_enemy)
    count_enemy -= count_enemy_voin
    count_enemy_spearmen = randint(0, count_enemy)
    count_enemy_cavalry = count_enemy - count_enemy_spearmen
    hp_enemy_voin = count_enemy_voin * 10
    hp_enemy_spearman = count_enemy_spearmen * 10
    hp_enemy_cavalry = count_enemy_cavalry * 10
    FPS = 50
    clock = pygame.time.Clock()
    pygame.init()
    pygame.display.set_caption('Битва')
    pygame.mouse.set_visible(False)
    size = width, height = 900, 1000
    screen = pygame.display.set_mode(size)
    running = True
    all_sprites = pygame.sprite.Group()
    mp = load_level('level.txt')
    # создадим спрайт
    start_screen()
    fighter, spear, cav, level_x, level_y = generate_level(load_level('level.txt'))
    x, y = fighter.coord()
    choice = False
    unit = fighter
    print(count_voin, count_enemy_voin, count_spearman, count_enemy_spearmen, count_cavalry, count_enemy_cavalry)
    while running:
        for event in pygame.event.get():
            if pygame.KEYDOWN == event.type:
                if choice is True:
                    move(unit)
                    fighter, spear, cav, level_x, level_y = generate_level(mp)
                    x, y = unit.coord()
                    choice = False
                else:
                    if pygame.K_1 == event.key and count_voin != 0:
                        print(count_voin, count_enemy_voin, count_spearman, count_enemy_spearmen, count_cavalry,
                              count_enemy_cavalry)
                        choice = True
                        unit = fighter
                    elif pygame.K_2 == event.key and count_spearman != 0:
                        choice = True
                        unit = spear
                    elif pygame.K_3 == event.key and count_cavalry != 0:
                        choice = True
                        unit = cav
            if event.type == pygame.QUIT:
                running = False

        all_sprites.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
    terminate()

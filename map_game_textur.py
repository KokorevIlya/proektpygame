import pygame
import random
import sqlite3

WIDTH, HEIGHT = 800, 600
TILE_SIZE = 40
LINE_COLOR = (200, 200, 200)
TEXT_COLOR = (255, 255, 255)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Цивилизация на минималках")
font = pygame.font.Font(None, 24)


# База данных
def initialize_database():
    conn = sqlite3.connect("game_data.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY,
            gold INTEGER,
            food INTEGER,
            warriors INTEGER
        )
    ''')

    cursor.execute("SELECT * FROM resources")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO resources (gold, food, warriors) VALUES (0, 0, 0)")
    conn.commit()
    conn.close()


# Загрузки данных из базы
def load_resources():
    conn = sqlite3.connect("game_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT gold, food, warriors FROM resources WHERE id = 1")
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0], result[1], result[2]
    return 0, 0, 0


# Сохранения данных в базу
def save_resources():
    conn = sqlite3.connect("game_data.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE resources SET gold = ?, food = ?, warriors = ? WHERE id = 1",
                   (gold, food, warriors))
    conn.commit()
    conn.close()


def end_game():
    reset_database()
    pygame.quit()
    exit()


# Загрузка текстур
textures = {
    "grass": pygame.image.load("grass3.png"),
    "mine": pygame.image.load("mine.png"),
    "farm": pygame.image.load("farm.png"),
    "castle": pygame.image.load("castle.png"),
    "enemy_castle": pygame.image.load("enemy_castle22.png"),
}


# Масштабирование текстур
for key in textures:
    if key not in ["castle", "enemy_castle"]:
        textures[key] = pygame.transform.scale(textures[key], (TILE_SIZE, TILE_SIZE))


# Текстуры замков
CASTLE_SIZE = 5
CASTLE_PIXEL_SIZE = CASTLE_SIZE * TILE_SIZE
textures["castle"] = pygame.transform.scale(textures["castle"], (CASTLE_PIXEL_SIZE, CASTLE_PIXEL_SIZE))
textures["enemy_castle"] = pygame.transform.scale(textures["enemy_castle"], (CASTLE_PIXEL_SIZE, CASTLE_PIXEL_SIZE))


# Генерация карты (Заполняется всё поле травой)
rows = HEIGHT // TILE_SIZE
cols = WIDTH // TILE_SIZE
terrain_map = [["grass" for _ in range(cols)] for _ in range(rows)]
initialize_database()
gold, food, warriors = load_resources()
enemy_warriors = random.randint(5, 15)
mines = {}
farms = {}
barracks = {}


# Размещаем два замка
player_castle_row, player_castle_col = rows // 2, (cols // 4) - 1
enemy_castle_row, enemy_castle_col = rows // 2, (3 * cols) // 4
for i in range(-2, 3):
    for j in range(-2, 3):
        r1, c1 = player_castle_row + i, player_castle_col + j
        r2, c2 = enemy_castle_row + i, enemy_castle_col + j
        if 0 <= r1 < rows and 0 <= c1 < cols:
            terrain_map[r1][c1] = "grass"
        if 0 <= r2 < rows and 0 <= c2 < cols:
            terrain_map[r2][c2] = "grass"


# Рисуем сетку
def draw_grid(surface):
    for row in range(rows):
        for col in range(cols):
            screen.blit(textures["grass"], (col * TILE_SIZE, row * TILE_SIZE))
            if (row, col) in mines:
                screen.blit(textures["mine"], (col * TILE_SIZE, row * TILE_SIZE))
            elif (row, col) in farms:
                screen.blit(textures["farm"], (col * TILE_SIZE, row * TILE_SIZE))
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(surface, LINE_COLOR, rect, 1)

    screen.blit(textures["castle"], ((player_castle_col - 2) * TILE_SIZE, (player_castle_row - 2) * TILE_SIZE))
    screen.blit(textures["enemy_castle"], ((enemy_castle_col - 2) * TILE_SIZE, (enemy_castle_row - 2) * TILE_SIZE))


# Панель ресурсов
def draw_resource_panel():
    panel_surface = pygame.Surface((200, 80))
    panel_surface.fill((50, 50, 50))

    gold_text = font.render(f"Gold: {gold}", True, TEXT_COLOR)
    food_text = font.render(f"Food: {food}", True, TEXT_COLOR)
    warriors_text = font.render(f"Warriors: {warriors}", True, TEXT_COLOR)

    panel_surface.blit(gold_text, (10, 10))
    panel_surface.blit(food_text, (10, 30))
    panel_surface.blit(warriors_text, (10, 50))

    screen.blit(panel_surface, (10, 10))


# Добыча золота и еды
def generate_resources():
    global gold, food
    gold += len(mines)
    food += len(farms)
    save_resources()


# Найм воинов
def hire_warrior():
    global gold, food, warriors
    if gold >= 5 and food >= 3:
        gold -= 5
        food -= 3
        warriors += 1
        save_resources()

def attack_enemy():
    global warriors, enemy_warriors
    print(f"Ваши воины: {warriors} | Воины противника: {enemy_warriors}")
    if warriors > 0:
        if warriors > enemy_warriors:
            print("Вы победили! Замок врага уничтожен.")
            end_game()
        else:
            print("Вы проиграли! Ваши войска уничтожены.")
            end_game()
    else:
        print("У вас нет воинов для атаки!")


# Сброс базы данных
def reset_database():
    global gold, food, warriors
    conn = sqlite3.connect("game_data.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE resources SET gold = 0, food = 0, warriors = 0 WHERE id = 1")
    conn.commit()
    conn.close()
    gold, food, warriors = 0, 0, 0



running = True
build_mode = None
while running:
    screen.fill((0, 0, 0))
    draw_grid(screen)
    draw_resource_panel()
    pygame.display.flip()
    generate_resources()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                build_mode = "mine"
            elif event.key == pygame.K_2:
                build_mode = "farm"
            elif event.key == pygame.K_3:
                hire_warrior()
            elif event.key == pygame.K_SPACE:
                attack_enemy()
            elif event.key == pygame.K_n:
                reset_database()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            col = x // TILE_SIZE
            row = y // TILE_SIZE
            if build_mode == "mine":
                mines[(row, col)] = "mine"
            elif build_mode == "farm":
                farms[(row, col)] = "farm"

    pygame.time.delay(1000)
pygame.quit()

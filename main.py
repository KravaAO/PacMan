from pygame import *
import math
import random

init()


class Sprite:
    def __init__(self, images, x, y, width, height):
        self.images = [transform.scale(image.load(img), (width, height)) for img in images]
        self.current_image = 0
        self.image = self.images[self.current_image]  # Встановлюємо перше зображення
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = str()
        self.animation_speed = 0.1

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def do_animate(self):
        self.current_image += self.animation_speed
        if self.current_image >= len(self.images):
            self.current_image = 0
        self.image = self.images[int(self.current_image)]


size = 1200, 1000
window = display.set_mode(size)
clock = time.Clock()

bg = transform.scale(image.load('Originalpacmaze.webp'), (1200, 1000))
wall_size = 20
map_list = ['############################################################',
            '############################################################',
            '#----------------------------##----------------------------#',
            '#--+-+-+-+-+-+-+-+-+-+-+-+-+-##----------------------------#',
            '#-+-----------+--------------##----------------------------#',
            '#----#######----#########--+-##----#########----#######----#',
            '#-+--#######--+-#########----##----##------#----#-----#----#',
            '#----#######----#########--+-##----##------#----#-----#----#',
            '#-+--#######--+-#########----##----#########----#######----#',
            '#--------------------------+-------------------------------#',
            '#-+---------+-+-+-+-+-+-+-+-+-+----------------------------#',
            '#----------------------------------------------------------#',
            '#-+--#######--+-##--+--##############-----##----#######----#',
            '#---------------##-----------##-----------##---------------#',
            '#--+-+-+-+-+--+-##--+-+-+-+--##-----------##---------------#',
            '#---------------##-----------##-----------##---------------#',
            '############--+-#########-+--##----#########----############',
            '############----#########----##----#########----############',
            '############--+-##------+-+---------------##----############',
            '############----##------------------------##----############',
            '############--+-##------------------------##----############',
            '############----##----#####------#####----##----############',
            '############--+-##----#--------------#----##----############',
            '#---------------------#--------------#---------------------#',
            '#---------------------#--------------#---------------------#',
            '#---------------------#--------------#---------------------#',
            '############----------#--------------#---------------------#',
            '############----------################---------------------#',
            '############-----------------------------------------------#',
            '############-----------------------------------------------#',
            '############-----------------------------------------------#',
            '############-----------------------------------------------#',
            '############-----------------------------------------------#',
            '#----------------------------------------------------------#',
            '#----------------------------------------------------------#',
            '#----------------------------------------------------------#',
            '#----------------------------------------------------------#',
            '#----------------------------------------------------------#',
            '#----------------------------------------------------------#',
            '#----------------------------------------------------------#',
            '#----------------------------------------------------------#',
            '#----------------------------------------------------------#',
            '#----------------------------------------------------------#',
            '#----------------------------------------------------------#',
            '#----------------------------------------------------------#',
            '#----------------------------------------------------------#',
            '#----------------------------------------------------------#',
            '#----------------------------------------------------------#',
            '#----------------------------------------------------------#',
            '############################################################', ]

walls = list()
coins = list()


# функція для побудови мапи
def make_map(map):
    global walls
    x = 0
    y = 0
    for row in map:
        for block in row:
            if block == '#':
                wall = Rect(x, y, wall_size, wall_size)
                walls.append(wall)
            if block == '+':
                coin = Sprite(['Coin.png'], x, y, 20, 20)
                coins.append(coin)
            x += wall_size
        x = 0
        y += wall_size


def check_collision(new_rect):
    for wall in walls:
        if new_rect.colliderect(wall):
            return True
    return False


def player_update():
    speed = 20
    new_rect = player.rect.copy()

    if player.direction == 'right':
        new_rect.x += speed
    elif player.direction == 'left':
        new_rect.x -= speed
    elif player.direction == 'up':
        new_rect.y -= speed
    elif player.direction == 'down':
        new_rect.y += speed

    # Якщо немає колізії, змінюємо координати гравця
    if not check_collision(new_rect):
        player.rect = new_rect


def green_ghost_update():
    speed = 2
    ghost_new_rect = green_ghost.rect.copy()

    # Поточні координати гравця та привида
    player_x, player_y = player.rect.x, player.rect.y
    ghost_x, ghost_y = green_ghost.rect.x, green_ghost.rect.y

    # Перевірка, чи всі монети зібрані
    is_fleeing = len(coins) == 0

    # Вибираємо напрямок залежно від того, чи привид переслідує, чи втікає від гравця
    possible_directions = {
        'right': (ghost_x + speed, ghost_y),
        'left': (ghost_x - speed, ghost_y),
        'up': (ghost_x, ghost_y - speed),
        'down': (ghost_x, ghost_y + speed)
    }

    # Знайти напрямок із найбільшою (втеча) або найменшою (переслідування) відстанню до гравця
    best_direction = green_ghost.direction  # залишаємо поточний напрямок, якщо інших варіантів немає
    target_distance = -math.inf if is_fleeing else math.inf

    for direction, (new_x, new_y) in possible_directions.items():
        # Створити тимчасовий прямокутник для перевірки колізії
        test_rect = green_ghost.rect.copy()
        test_rect.x, test_rect.y = new_x, new_y

        if not check_collision(test_rect):
            # Обчислити відстань до гравця
            distance = math.sqrt((player_x - new_x) ** 2 + (player_y - new_y) ** 2)
            # Якщо втікаємо, шукаємо напрямок з більшою відстанню, інакше - з меншою
            if (is_fleeing and distance > target_distance) or (not is_fleeing and distance < target_distance):
                target_distance = distance
                best_direction = direction

    # Задати новий напрямок руху привида
    green_ghost.direction = best_direction

    # Оновити положення привида відповідно до вибраного напрямку
    if green_ghost.direction == 'right':
        green_ghost.rect.x += speed
    elif green_ghost.direction == 'left':
        green_ghost.rect.x -= speed
    elif green_ghost.direction == 'up':
        green_ghost.rect.y -= speed
    elif green_ghost.direction == 'down':
        green_ghost.rect.y += speed


def red_ghost_update():
    speed = 5  # Встановлюємо швидкість, яка підходить для кроків Pacman

    # Поточні координати привида
    ghost_x, ghost_y = red_ghost.rect.x, red_ghost.rect.y

    # Вибір напрямку руху залежно від можливих напрямків без зіткнень
    possible_directions = {
        'right': (ghost_x + speed, ghost_y),
        'left': (ghost_x - speed, ghost_y),
        'up': (ghost_x, ghost_y - speed),
        'down': (ghost_x, ghost_y + speed)
    }

    valid_directions = []

    for direction, (new_x, new_y) in possible_directions.items():
        # Створити тимчасовий прямокутник для перевірки колізії
        test_rect = red_ghost.rect.copy()
        test_rect.x, test_rect.y = new_x, new_y

        if not check_collision(test_rect):
            valid_directions.append(direction)

    # Якщо поточний напрямок більше не є допустимим, обираємо новий напрямок
    if red_ghost.direction not in valid_directions:
        red_ghost.direction = random.choice(valid_directions) if valid_directions else None

    # Оновити положення привида відповідно до вибраного напрямку
    if red_ghost.direction == 'right':
        red_ghost.rect.x += speed
    elif red_ghost.direction == 'left':
        red_ghost.rect.x -= speed
    elif red_ghost.direction == 'up':
        red_ghost.rect.y -= speed
    elif red_ghost.direction == 'down':
        red_ghost.rect.y += speed


def draw_cell():
    size_w = 20
    for x in range(0, size[0], size_w):
        for y in range(0, size[1], size_w):
            draw.rect(window, (255, 0, 0), Rect(x, y, size_w, size_w), 2)


font1 = font.Font(None, 40)
player = Sprite(
    ['player.png', 'player1.png', 'player2.png', 'player3.png', 'player4.png', 'player5.png', 'player6.png'], 500, 560,
    50, 50)
make_map(map_list)

green_ghost = Sprite(['green_ghost.png'], 500, 360, 50, 50)
red_ghost = Sprite(['redGhost.png'], 500, 360, 50, 50)
wait = 0
score = 0
finish = False
lvl = 1
destroy_ghost = 0
high_score = 0
while True:
    for e in event.get():
        if e.type == QUIT:
            quit()
        if e.type == KEYDOWN and finish:
            if e.key == K_SPACE:
                finish = False
                lvl = 1
                player = Sprite(
                    ['player.png', 'player1.png', 'player2.png', 'player3.png', 'player4.png', 'player5.png',
                     'player6.png'], 500, 560, 50, 50)
                green_ghost = Sprite(['green_ghost.png'], 500, 360, 50, 50)
                red_ghost = Sprite(['redGhost.png'], 500, 360, 50, 50)
                destroy_ghost = 0
                score = 0

    if not finish:
        window.blit(bg, (0, 0))
        # пересування гравця
        keys = key.get_pressed()
        if keys[K_d]:
            player.direction = 'right'
        elif keys[K_a]:
            player.direction = 'left'
        elif keys[K_w]:
            player.direction = 'up'
        elif keys[K_s]:
            player.direction = 'down'
        if wait == 0:
            player_update()

            wait = 6
        else:
            wait -= 1

        for coin in coins:
            coin.reset()
            if player.rect.colliderect(coin.rect):
                coins.remove(coin)
                score += 10
                if score > high_score:
                    high_score = score
        #
        if player.rect.colliderect(green_ghost.rect):
            if not coins:
                green_ghost = Sprite(['green_ghost.png'], 1500, 360, 50, 50)
                destroy_ghost += 1
            else:
                finish = True

        green_ghost_update()
        green_ghost.reset()
        # логіка відображення граця
        player.do_animate()
        if player.direction == 'right':
            player.image = player.images[int(player.current_image)]
        elif player.direction == 'left':
            player.image = transform.flip(player.images[int(player.current_image)], True, False)
        elif player.direction == 'up':
            player.image = transform.rotate(player.images[int(player.current_image)], 90)
        elif player.direction == 'down':
            player.image = transform.rotate(player.images[int(player.current_image)], -90)
        player.reset()

        text_score = font1.render(f'Score:  {score}', True, (255, 255, 255))
        window.blit(text_score, (20, 5))
        # логіка для другого рівня
        if lvl > 1:  # всі рівні після першого вже будуть мати другого привида
            red_ghost_update()
            red_ghost.reset()
            if player.rect.colliderect(red_ghost.rect):
                if not coins:
                    red_ghost = Sprite(['redGhost.png'], 1500, 360, 50, 50)
                    destroy_ghost += 1
                else:
                    finish = True

        # перевірка чи пройден рівень
        if lvl == 1:
            if destroy_ghost == 1:  # якщо знищили усіх ворогів на перщому рівні
                finish = True
        elif lvl == 2:
            if destroy_ghost == 2:  # якщо знищили усіх ворогів на другому рівні тобто 2
                finish = True
        else:  # обробка невідомого рівня більше запраграмованих
            if destroy_ghost == 2:
                finish = True

    if finish and coins:
        window.fill((255, 0, 0))

        print('рахунок за цю гру', score)  # допрацювати вивід інформації у самій грі
        print('максимальний рахунок за всі ігри', high_score)

    elif finish and not coins:
        print('рахунок за цю гру', score)
        print('максимальний рахунок за всі ігри', high_score)  # допрацювати вивід інформації у самій грі

        make_map(map_list)
        green_ghost = Sprite(['green_ghost.png'], 500, 360, 50, 50)
        red_ghost = Sprite(['redGhost.png'], 560, 360, 50, 50)
        finish = False
        destroy_ghost = 0
        lvl += 1

    draw_cell()
    for wall in walls:
     draw.rect(window, (255, 0, 0), wall)

    display.update()
    clock.tick(60)

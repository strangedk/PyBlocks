import pygame
import sys
import random


""" Initialization of the PyGame """
game_width = 1024
game_height = 1024

pygame.init()
screen = pygame.display.set_mode((game_width, game_height))
clock = pygame.time.Clock()


def rand_color():
    return random.randint(0, 254), random.randint(0, 254), random.randint(0, 254)


def create_bricks(w, h):
    result = []
    matrix = w * h
    x = 0
    y = 0

    for i in range(0, matrix):
        if i % w == 0:
            x = 0
            y = y + 1
        item = pygame.image.load('assets/block.png').convert()
        item.fill(rand_color())
        item = pygame.transform.scale(item, (50, 15))
        rect = item.get_rect()
        rect.x = item.get_width() * x + offset_bricks[0]
        rect.y = item.get_height() * y + offset_bricks[1]
        result.append((item, rect))
        x = x + 1
    return result


""" Ball deltas """
delta_speed = 25
delta_x = 0.1
delta_y = -0.1
delta_pos_x = 0
delta_pos_y = 0
delta_randomizer = 75

""" Offsets """
offset_bricks = (60, 150)
count_bricks_w = 18
count_bricks_h = 18

""" Positions """
player_top = 900
player_pos = 0

""" Items creation """
bg = pygame.image.load('assets/bg.png').convert()
ball = pygame.transform.scale(pygame.image.load('assets/ball.png').convert_alpha(), (20, 20))
player = pygame.image.load('assets/block.png').convert()

""" List of Tuple (Surface, Rect) """
bricks = create_bricks(count_bricks_w, count_bricks_h)

""" Game state """
is_active_game = False

""" Events """
# SPAWNPIPE = pygame.USEREVENT
# pygame.time.set_timer(SPAWNPIPE, 1000)


def reset():
    global delta_pos_x
    global delta_pos_y
    global delta_y
    global is_active_game

    is_active_game = False
    delta_y = -abs(delta_y)
    delta_pos_x = player_pos - ball.get_width() / 2
    delta_pos_y = player_top - ball.get_height() * 2
    screen.blit(ball, (delta_pos_x, delta_pos_y))


def move_ball():
    global delta_x
    global delta_y
    global delta_pos_x
    global delta_pos_y

    if delta_pos_x < 0:
        delta_pos_x = 0
        delta_x *= -1
        delta_x += random.randint(-1, 1) / delta_randomizer
    if delta_pos_x > game_width:
        delta_pos_x = game_width
        delta_x *= -1
        delta_x += random.randint(-1, 1) / delta_randomizer
    if delta_pos_y < 0:
        delta_pos_y = 0
        delta_y *= -1
        delta_y += random.randint(-1, 1) / delta_randomizer
    if delta_pos_y > game_height:
        reset()

    delta_pos_x += delta_x * delta_speed
    delta_pos_y += delta_y * delta_speed
    screen.blit(ball, (delta_pos_x, delta_pos_y))


def bounce_y():
    global delta_y
    delta_y *= -1


def bounce_x():
    global delta_x
    delta_x *= -1


def check_collision():
    global bricks

    ball_rect = ball.get_rect()
    ball_rect.x = delta_pos_x
    ball_rect.y = delta_pos_y

    player_rect = player.get_rect()
    player_rect.x = player_pos - player_rect.width / 2
    player_rect.y = player_top

    ball_collided_with_player = ball_rect.colliderect(player_rect)

    if ball_collided_with_player:
        bounce_y()

    to_remove = []
    for (brick, rect) in bricks:
        if ball_rect.colliderect(rect):
            to_remove.append(rect)
            bounce_y()
            bounce_x()

    def filter_bricks(item):
        result = True
        for brick_f in to_remove:
            if brick_f == item[1]:
                result = False
        return result

    bricks_iterator = filter(filter_bricks, bricks)
    bricks = list(bricks_iterator)


""" Game loop """
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            mp = pygame.mouse.get_pos()
            player_pos = mp[0]
        if event.type == pygame.MOUSEBUTTONUP:
            is_active_game = True

    # Blit all the other stuff
    screen.blit(bg, (0, 0))
    screen.blit(player, (player_pos - player.get_width() / 2, player_top))

    if not is_active_game:
        reset()
    else:
        move_ball()
        check_collision()

    # Blit bricks
    for (brick, rect) in bricks:
        screen.blit(brick, rect)

    pygame.display.update()
    clock.tick(120)

from colors import *
from menu import *
from game_objects import *

import pygame as pg
import pygame.draw as pgd
import pygame.image as pgi
import pygame.transform as pgt
import os.path


def get_level(level: int):
    '''
    gets an info about a level,
    depending on its number from
    a file in game_levels
    '''
    blocks = []
    file = open('game_levels/level_' + str(level) + '.txt', 'r')
    i = 0
    for line in file:
        blocks.append([])
        for elem in line:
            if elem != '\n':
                blocks[i].append(elem)
        i += 1
    return blocks


def define_grid(fullscreen, window_size, full_size, game_resolution, screen):
    '''
    defines game surface depending
    on resolution from get_level()
    '''
    number_x = game_resolution[0]
    number_y = game_resolution[1]
    if fullscreen:
        block_size = min((full_size[0] // number_x), (full_size[1] // number_y))
        start_x = (full_size[0] - block_size * number_x) // 2
        start_y = (full_size[1] - block_size * number_y) // 2
        # return [start_x, start_y], (block_size, block_size)
    else:
        block_size = min((window_size[0] // number_x), (window_size[1] // number_y))
        start_x = (window_size[0] - block_size * number_x) // 2
        start_y = (window_size[1] - block_size * number_y) // 2
    return [start_x, start_y], (block_size, block_size)


def recalculate_rect(obj, fullscreen, window_size, full_size, game_resolution):
    '''
    recalculates game parameters
    when screen mode changes
    '''
    number_x = game_resolution[0]
    number_y = game_resolution[1]
    full_block_size = min((full_size[0] // number_x),
                          (full_size[1] // number_y))
    window_block_size = min((window_size[0] // number_x),
                            (window_size[1] // number_y))
    if fullscreen:
        obj.x = (full_size[0] * obj.x) // window_size[0]
        obj.y = (full_size[1] * obj.y) // window_size[1]
        block_size = (full_block_size, full_block_size)
    else:
        obj.x = (window_size[0] * obj.x) // full_size[0]
        obj.y = (window_size[1] * obj.y) // full_size[1]
        block_size = (window_block_size, window_block_size)
    return [[obj.x, obj.y], block_size]


def recalculate_params(obj):
    '''
    the same as recalculate_rect()
    '''
    params = [int(obj.Rect[1][0] * 1.2 / 2),
              int(obj.Rect[1][0] * 0.2 / 2),
              int(obj.Rect[1][0] * 0.3 / 2),
              int(obj.Rect[1][0] * 0.4 / 2)]
    return params


def change_fullscreen(fullscreen, window_size, full_size, BACKGROUND):
    '''
    check buttons' push to change screen mode
    '''
    fullscreen = not fullscreen
    if fullscreen:
        screen = pg.display.set_mode(full_size, flags)
        screen.fill(BACKGROUND)
    else:
        screen = pg.display.set_mode(window_size)
        screen.fill(BACKGROUND)
    return fullscreen

pg.init()
pg.font.init()

FPS = 30
window_size = (854, 480)
display_info = pg.display.Info()
full_size = (display_info.current_w, display_info.current_h)
game_resolution = (24, 13)
number_x = game_resolution[0]
number_y = game_resolution[1]
window_block_size = min((window_size[0] // number_x), (window_size[1] // number_y))
full_block_size = min((full_size[0] // number_x), (full_size[1] // number_y))
BACKGROUND = GRAY
fullscreen = False
flags = pg.FULLSCREEN
screen = pg.display.set_mode(window_size)
pg.display.set_caption('TANKS')

clock = pg.time.Clock()
finished = False
game = False
tank_is_moving = [False, False, False, False]
screen.fill(BACKGROUND)

tank = Tank([[400, 137], (window_block_size, window_block_size)], LIGHT_GREEN)
tank1 = Enemy([[600, 100], (window_block_size, window_block_size)], BLACK)
objs = [tank, tank1]
level1 = Level(get_level(1))
walls_hp = level1.get_walls_hp()
GROUND_COLOR = DARK_GRASS
bullets = []
enemy_bullets = []
explosions = []
traps = []
enemy_traps = []

while not finished:
    screen.fill(GROUND_COLOR)
    if game:
        pass  # FIXME level's blocks appear
    clock.tick(FPS)
    mouse_pos = pg.mouse.get_pos()
    mouse_pressed = pg.mouse.get_pressed()
    keys = pg.key.get_pressed()
    block_params = define_grid(fullscreen,
                               window_size,
                               full_size,
                               level1.resolution,
                               screen)
    level1.app(screen, block_params, walls_hp)
    walls = Walls(level1, block_params)
    for trap in traps:
        trap.app(screen)
        for obj in objs:
            if obj != tank:
                obj.hp = trap.check_objs(obj)
        if not trap.active:
            trap.explose(explosions,
                         FPS,
                         fullscreen,
                         full_block_size,
                         window_block_size,
                         False)
            traps.remove(trap)
    for trap in enemy_traps:
        trap.app(screen)
        tank.hp = trap.check_objs(tank)
        if not trap.active:
            trap.explose(explosions,
                         FPS,
                         fullscreen,
                         full_block_size,
                         window_block_size,
                         False)
            enemy_traps.remove(trap)
    tank.app(screen, mouse_pos, fullscreen)
    tank1.app(screen, mouse_pos, fullscreen, enemy_bullets, enemy_traps)
    tank1.move(walls, walls_hp, FPS)
    tank.continue_move(walls.walls, walls_hp, tank_is_moving)
    for bullet in enemy_bullets:
        walls_hp = bullet.app(screen, walls.walls, walls_hp, fullscreen)
        tank.hp = bullet.check_hit(tank)
        if not bullet.active:
            bullet.explose(explosions,
                           FPS,
                           fullscreen,
                           full_block_size,
                           window_block_size,
                           True)
            enemy_bullets.remove(bullet)
        if bullet.in_tank:
            bullet.explose(explosions,
                           FPS,
                           fullscreen,
                           full_block_size,
                           window_block_size,
                           False)
            enemy_bullets.remove(bullet)
    for bullet in bullets:
        walls_hp = bullet.app(screen, walls.walls, walls_hp, fullscreen)
        for obj in objs:
            if obj != tank:
                obj.hp = bullet.check_hit(obj)
        if not bullet.active:
            bullet.explose(explosions,
                           FPS,
                           fullscreen,
                           full_block_size,
                           window_block_size,
                           True)
            bullets.remove(bullet)
        if bullet.in_enemy:
            bullet.explose(explosions,
                           FPS,
                           fullscreen,
                           full_block_size,
                           window_block_size,
                           False)
            bullets.remove(bullet)
    for explosion in explosions:
        explosion.app(screen)
        for obj in objs:
            explosion.check_objects(obj)
        if not explosion.active:
            explosions.remove(explosion)
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            controls = [pg.K_RIGHT, pg.K_LEFT, pg.K_UP, pg.K_DOWN]
            if event.key in controls:
                tank_is_moving = tank.move(event, walls.walls, walls_hp, tank_is_moving)
        if event.type == pg.KEYUP:
            controls = [pg.K_RIGHT, pg.K_LEFT, pg.K_UP, pg.K_DOWN]
            if event.key in controls:
                tank_is_moving = tank.stop(event, tank_is_moving)
        if event.type == pg.KEYDOWN and event.key == pg.K_F11:  # FIXME компактность
            # Change window mode
            fullscreen = change_fullscreen(fullscreen,
                                           window_size,
                                           full_size,
                                           BACKGROUND)
            tank.Rect = recalculate_rect(tank,
                                         fullscreen,
                                         window_size,
                                         full_size,
                                         game_resolution)
            tank.params = recalculate_params(tank)
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            traps.append(Trap(tank, 'tank'))
        if event.type == pg.QUIT:
            finished = True
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                bullets.append(Bullet(tank, bullets, mouse_pos))
            elif event.button == 3:
                print(tank.hp)
                print(tank1.hp)
                print(traps)
            else:
                pass
    pg.display.update()

pg.quit()
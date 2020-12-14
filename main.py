import pygame as pg
import pygame.draw as pgd
import pygame.image as pgi
import pygame.transform as pgt
import os.path
from random import randint

from colors import *
from menu import *
from game_objects import *


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


def recalculate_coords(obj, fullscreen, window_size, full_size, game_resolution):
    '''
    recalculates game parameters
    when screen mode changes
    '''
    if fullscreen:
        obj.x = (full_size[0] * obj.x) // window_size[0]
        obj.y = (full_size[1] * obj.y) // window_size[1]
    else:
        obj.x = (window_size[0] * obj.x) // full_size[0]
        obj.y = (window_size[1] * obj.y) // full_size[1]
    return obj.x, obj.y


def recalculate_list(objs, fullscreen, window_size, full_size, game_resolution):
    for obj in objs:
        obj.x, obj.y = recalculate_coords(obj, fullscreen, window_size,
                                          full_size, game_resolution)


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


def spawn_actions(objs, enemies, spawn, window_block_size, full_block_size, fullscreen):
    born = randint(1, 100)
    if born == 100:
        if fullscreen:
            new_enemy = Enemy([spawn, (full_block_size, full_block_size)], BLACK)
        else:
            new_enemy = Enemy([spawn, (window_block_size, window_block_size)], BLACK)
        enemies.append(new_enemy)
        objs.append(new_enemy)


def enemies_live(objs, enemies):
    for enemy in enemies:
        enemy.app(screen, mouse_pos, enemy_bullets, enemy_traps)
        enemy.move(walls, walls_hp, FPS, fullscreen)
        if enemy.hp <= 0:
            enemy.die(bonuses,
                      explosions,
                      FPS,
                      fullscreen,
                      full_block_size,
                      window_block_size,
                      False)
            enemies.remove(enemy)
            objs.remove(enemy)


pg.init()
pg.font.init()

FPS = 30
flags = pg.FULLSCREEN
display_info = pg.display.Info()
full_size = (display_info.current_w, display_info.current_h)
window_size = (854, 480)
screen = pg.display.set_mode(window_size)
pg.display.set_caption('TANKS')
clock = pg.time.Clock()

game_resolution = (24, 13)
number_x = game_resolution[0]
number_y = game_resolution[1]
window_block_size = min((window_size[0] // number_x), (window_size[1] // number_y))
full_block_size = min((full_size[0] // number_x), (full_size[1] // number_y))

fullscreen = False
finished = False
game = False
tank_is_moving = [False, False, False, False]

tank = Tank([[400, 137], (window_block_size, window_block_size)], LIGHT_GREEN)
objs = [tank]
enemies = []
bullets = []
enemy_bullets = []
explosions = []
traps = []
enemy_traps = []
bonuses = []
spawn = None
level1 = Level(get_level(1))
walls_hp = level1.get_walls_hp()
GROUND_COLOR = DARK_GRASS

while not finished:
    screen.fill(GROUND_COLOR)
    if game:
        pass  # FIXME level's blocks appear
    clock.tick(FPS)
    mouse_pos = pg.mouse.get_pos()
    block_params = define_grid(fullscreen, window_size, full_size, 
                               level1.resolution, screen)
    spawn = level1.app(screen, block_params, walls_hp)
    spawn_actions(objs, enemies, spawn, window_block_size, 
                  full_block_size, fullscreen)
    walls = Walls(level1, block_params)
    for bonus in bonuses:
        bonus.app(screen, fullscreen)
        bonus.check_tank(tank, FPS)
        if not bonus.active:
            bonuses.remove(bonus)
    for trap in traps:
        trap.app(screen, fullscreen)
        for obj in objs:
            if obj != tank:
                obj.hp = trap.check_objs(obj)
        if not trap.active:
            trap.explose(explosions, FPS, fullscreen,
                         full_block_size, window_block_size, False)
            traps.remove(trap)
    for trap in enemy_traps:
        trap.app(screen, fullscreen)
        tank.hp = trap.check_objs(tank)
        if not trap.active:
            trap.explose(explosions, FPS, fullscreen,
                         full_block_size, window_block_size, False)
            enemy_traps.remove(trap)
    tank.app(screen, mouse_pos, fullscreen)
    tank.continue_move(walls.walls, walls_hp, tank_is_moving)
    enemies_live(objs, enemies)
    for bullet in enemy_bullets:
        walls_hp = bullet.app(screen, walls.walls, walls_hp, fullscreen)
        tank.hp = bullet.check_hit(tank)
        if not bullet.active:
            bullet.explose(explosions, FPS, fullscreen,
                           full_block_size, window_block_size, True)
            enemy_bullets.remove(bullet)
        if bullet.in_tank:
            bullet.explose(explosions, FPS, fullscreen,
                           full_block_size, window_block_size, False)
            enemy_bullets.remove(bullet)
    for bullet in bullets:
        walls_hp = bullet.app(screen, walls.walls, walls_hp, fullscreen)
        for obj in objs:
            if obj != tank:
                obj.hp = bullet.check_hit(obj)
        if not bullet.active:
            bullet.explose(explosions, FPS, fullscreen,
                           full_block_size, window_block_size, True)
            bullets.remove(bullet)
        if bullet.in_enemy:
            bullet.explose(explosions, FPS, fullscreen,
                           full_block_size, window_block_size, False)
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
            fullscreen = change_fullscreen(fullscreen, window_size,
                                           full_size, GROUND_COLOR)
            for obj in objs:
                obj.Rect = recalculate_rect(obj, fullscreen, window_size,
                                            full_size, game_resolution)
                obj.params = recalculate_params(obj)
            recalculate_list(traps, fullscreen, window_size,
                             full_size, game_resolution)
            recalculate_list(bonuses, fullscreen, window_size,
                             full_size, game_resolution)
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            if tank.traps > 0:
                traps.append(Trap(tank, 'tank'))
                tank.traps -= 1
        if event.type == pg.QUIT:
            finished = True
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if tank.ammo > 0:
                    bullets.append(Bullet(tank, bullets, mouse_pos))
                    tank.ammo -= 1
            elif event.button == 3:
                print(bonuses)
    pg.display.update()

pg.quit()
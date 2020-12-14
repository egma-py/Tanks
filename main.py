import pygame as pg
import pygame.draw as pgd
import pygame.image as pgi
import pygame.transform as pgt
import os.path
from random import randint

from colors import *
from menu import *
from game_objects import *
from tank import *
from enemy import *


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


def level_menu_actions(level_menu, mouse_pos, main_menu):
    level_number = None
    for button in level_menu.buttons:
        if button.check_pos(mouse_pos) and level_menu.active:
            if button.button_text == 'Level 1':
                level_number = 1
                main_menu.active = True
                level_menu.active = False
            if button.button_text == 'Level 2':
                level_number = 2
                main_menu.active = True
                level_menu.active = False
            if button.button_text == 'Level 3':
                level_number = 3
                main_menu.active = True
                level_menu.active = False
            if button.button_text == 'Level 4':
                level_number = 4
                main_menu.active = True
                level_menu.active = False
            if button.button_text == 'Level 5':
                level_number = 5
                main_menu.active = True
                level_menu.active = False
            if button.button_text == '. . . . .':
                main_menu.active = True
                level_menu.active = False
    return level_number


def main_menu_actions(level_menu, mouse_pos, main_menu, level_number, menu_mode):
    level, walls_hp = None, None
    for button in main_menu.buttons:
        if button.check_pos(mouse_pos) and main_menu.active:
            if button.button_text == 'Start game' and level_number != None:
                level = Level(get_level(level_number))
                walls_hp = level.get_walls_hp()
                menu_mode = False
                main_menu.active = False
            elif button.button_text == 'Choose level':
                main_menu.active = False
                level_menu.active = True
    return level, walls_hp, menu_mode


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

menu_mode = True
fullscreen = False
finished = False
show_HUD = False
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
tank_spawn = None
GROUND_COLOR = DARK_GRASS
BACKGROUND = DARK_GRAY

# At first info about level is unknown
level = None
level_number = None
# Making menus
main_menu = Menu((10, 10), (300, 70), True)
level_menu = Menu((400, 10), (300, 200), False)
# Defining buttons
begin = Button(screen, main_menu.x + 10, main_menu.y + 15, 
               main_menu.size_x - 20, 20, [list(RED), list(BLACK)],
               'Start game', 10)
choose_level = Button(screen, main_menu.x + 10, main_menu.y + 40, 
                      main_menu.size_x - 20, 20, [list(RED), list(BLACK)],
                      'Choose level', 10)
return_button = Button(screen, level_menu.x + 10, level_menu.y + 15, 
                       level_menu.size_x - 20, 20, [list(RED), list(BLACK)],
                       '. . . . .', 10)
level1 = Button(screen, level_menu.x + 10, level_menu.y + 40, 
                level_menu.size_x - 20, 20, [list(RED), list(BLACK)],
                'Level 1', 10)
level2 = Button(screen, level_menu.x + 10, level_menu.y + 65, 
                level_menu.size_x - 20, 20, [list(RED), list(BLACK)],
                'Level 2', 10)
level3 = Button(screen, level_menu.x + 10, level_menu.y + 90, 
                level_menu.size_x - 20, 20, [list(RED), list(BLACK)],
                'Level 3', 10)
level4 = Button(screen, level_menu.x + 10, level_menu.y + 115, 
                level_menu.size_x - 20, 20, [list(RED), list(BLACK)],
                'Level 4', 10)
level5 = Button(screen, level_menu.x + 10, level_menu.y + 140, 
                level_menu.size_x - 20, 20, [list(RED), list(BLACK)],
                'Level 5', 10)
# Adding buttons into definite menu
main_menu.add_buttons([begin, choose_level])
level_menu.add_buttons([level1, level2, level3, level4, level5, return_button])
menus = [main_menu, level_menu]

while not finished:
    mouse_pos = pg.mouse.get_pos()
    if menu_mode:
        screen.fill(BACKGROUND)
        for menu in menus:
            if menu.active:
                menu.app(screen, BACKGROUND, mouse_pos)
    else:
        screen.fill(GROUND_COLOR)
        clock.tick(FPS)
        mouse_pos = pg.mouse.get_pos()
        block_params = define_grid(fullscreen, window_size, full_size, 
                                   level.resolution, screen)
        spawn = level.app(screen, block_params, walls_hp)
        spawn_actions(objs, enemies, spawn, window_block_size, 
                      full_block_size, fullscreen)
        walls = Walls(level, block_params)
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
        if show_HUD:
            tank.show_HUD(screen)
        if tank.hp <= 0:
            menu_mode = True
            main_menu.active = True
            tank.hp = 20
            tank.x, tank.y = 400, 137
            objs = [tank]
            enemies = []
            bullets = []
            enemy_bullets = []
            explosions = []
            traps = []
            enemy_traps = []
            bonuses = []
            spawn = None
            level = None
            level_number = None
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if not menu_mode:
                controls = [pg.K_RIGHT, pg.K_LEFT, pg.K_UP, pg.K_DOWN]
                if event.key in controls:
                    tank_is_moving = tank.move(event, walls.walls, walls_hp, tank_is_moving)
        if event.type == pg.KEYUP:
            if not menu_mode:    
                controls = [pg.K_RIGHT, pg.K_LEFT, pg.K_UP, pg.K_DOWN]
                if event.key in controls:
                    tank_is_moving = tank.stop(event, tank_is_moving)
        if event.type == pg.KEYDOWN and event.key == pg.K_F11:
            # Change window mode
            fullscreen = change_fullscreen(fullscreen, window_size,
                                           full_size, GROUND_COLOR)
            for obj in objs:
                obj.Rect = recalculate_rect(obj, fullscreen, window_size,
                                            full_size, game_resolution)
                obj.params = recalculate_params(obj)
            recalculate_list(traps, fullscreen, window_size,
                             full_size, game_resolution)
            recalculate_list(enemy_traps, fullscreen, window_size,
                             full_size, game_resolution)
            recalculate_list(bonuses, fullscreen, window_size,
                             full_size, game_resolution)
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            if not menu_mode:
                if tank.traps > 0:
                    traps.append(Trap(tank, 'tank'))
                    tank.traps -= 1
        if event.type == pg.KEYDOWN and event.key == pg.K_TAB:
            if not menu_mode:
                show_HUD = True
        if event.type == pg.KEYUP and event.key == pg.K_TAB:
            if not menu_mode:
                show_HUD = False
        if event.type == pg.QUIT:
            finished = True
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if not menu_mode:
                if tank.ammo > 0:
                    bullets.append(Bullet(tank, bullets, mouse_pos))
                    tank.ammo -= 1
            else:
                level, walls_hp, menu_mode = main_menu_actions(level_menu, 
                                                               mouse_pos, 
                                                               main_menu, 
                                                               level_number, 
                                                               menu_mode)
                level_number = level_menu_actions(level_menu, 
                                                  mouse_pos, 
                                                  main_menu)
    pg.display.update()

pg.quit()
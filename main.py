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


def get_level(level):
    '''
    This function parses Level blocks from file with level number.

    Parameters
    ----------
    level : int

    Returns
    -------
    blocks : list

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


def define_grid(fullscreen, window_size, full_size, game_resolution):
    '''
    This function defines block parameters depending on
    resolution and fullscreen mode

    Parameters
    ----------
    fullscreen : bool
    window_size : tuple
    full_size : tuple
    game_resolution : tuple

    Returns
    -------
    list
        Returns a list of a list(First block x and y) and a tuple(block size).

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
    return [[start_x, start_y], (block_size, block_size)]


def recalculate_rect(obj, fullscreen, window_size, full_size, game_resolution):
    '''
    This function recalculates object's Rect, if fullscreen 
    mode is changed.

    Parameters
    ----------
    obj : Tank or Enemy object
    fullscreen : int
    window_size : int
    full_size : bool
    game_resolution : tuple

    Returns
    -------
    list
        List of a new object's Rect.

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
    Is ised in recalculate_list function.

    Parameters
    ----------
    obj : simple object(Bullet, Bonus, Trap etc.)
    fullscreen : bool
    window_size : int
    full_size : int
    game_resolution : tuple

    Returns
    -------
    int
    int
        New coords of an object

    '''
    if fullscreen:
        obj.x = (full_size[0] * obj.x) // window_size[0]
        obj.y = (full_size[1] * obj.y) // window_size[1]
    else:
        obj.x = (window_size[0] * obj.x) // full_size[0]
        obj.y = (window_size[1] * obj.y) // full_size[1]
    return obj.x, obj.y


def recalculate_list(objs, fullscreen, window_size, full_size, game_resolution):
    '''
    Simple function to recalculate simple objects'' coords
    such as bonus, trap, bullet etc.

    Parameters
    ----------
    objs : list
    fullscreen : bool
    window_size : int
    full_size : int
    game_resolution : tuple

    Returns
    -------
    None.

    '''
    for obj in objs:
        obj.x, obj.y = recalculate_coords(obj, fullscreen, window_size,
                                          full_size, game_resolution)


def recalculate_params(obj):
    '''
    Simple function to recalculate object's cannon 
    parameters. if fullscreen mode is changed.

    Parameters
    ----------
    obj : Tank or Enemy object

    Returns
    -------
    params : list
        Returns new cannon parameters

    '''
    params = [int(obj.Rect[1][0] * 1.2 / 2),
              int(obj.Rect[1][0] * 0.2 / 2),
              int(obj.Rect[1][0] * 0.3 / 2),
              int(obj.Rect[1][0] * 0.4 / 2)]
    return params


def change_fullscreen(fullscreen, window_size, full_size, BACKGROUND):
    '''
    This function changes current fullscreen mode

    Parameters
    ----------
    fullscreen : bool
    window_size : int
    full_size : int
    BACKGROUND : tuple

    Returns
    -------
    fullscreen : bool
        Returns current fullscreen mode condition

    '''
    fullscreen = not fullscreen
    if fullscreen:
        screen = pg.display.set_mode(full_size, flags)
        screen.fill(BACKGROUND)
    else:
        screen = pg.display.set_mode(window_size)
        screen.fill(BACKGROUND)
    return fullscreen


def spawn_actions(objs, enemies, spawns, window_block_size, full_block_size, fullscreen):
    '''
    This function defines, if an enemy 'wants' to born or not.

    Parameters
    ----------
    objs : list
    enemies : list
    spawn : tuple
    window_block_size : int
    full_block_size : int
    fullscreen : bool
        Is needed to change spawn pos, if fullscreen mode is enabled.

    Returns
    -------
    None.

    '''
    born = randint(1, 100)
    if born == 100 and len(spawns) != 0:
        k = randint(0, len(spawns)-1)
        if fullscreen:
            new_enemy = Enemy([spawns[k], (full_block_size, full_block_size)], BLACK)
        else:
            new_enemy = Enemy([spawns[k], (window_block_size, window_block_size)], BLACK)
        enemies.append(new_enemy)
        objs.append(new_enemy)


def enemies_live(objs, enemies):
    '''
    This function shows all the enemies and changes their conditions.
    Also it checks if an enemy is alive

    Parameters
    ----------
    objs : list
        List with enemies and tank(Mostly used in explosions_live func)
    enemies : list

    Returns
    -------
    None.

    '''
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
    '''
    This funciton checks all the button manipulations in level menu

    Parameters
    ----------
    level_menu : Menu object
    mouse_pos : tuple
    main_menu : Menu object

    Returns
    -------
    level_number : int

    '''
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
    '''
    This function checks all the button manipulations in main menu

    Parameters
    ----------
    level_menu : Menu object
    mouse_pos : tuple
    main_menu : Menu object
    level_number : int
    menu_mode : bool

    Returns
    -------
    level : Level object
    walls_hp : list
    menu_mode : bool
        If level is chosen and Start button is pushed,
        they will be defined by level's number

    '''
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


def bonuses_live(bonuses, screen, fullscreen, tank, FPS):
    '''
    This function shows all the bonuses and checks if they are caught

    Parameters
    ----------
    bonuses : list
        New bonus will be added there
    screen : Surface
    fullscreen : bool
    tank : Tank objects
        Is needed to check if the tank catches a bonus
    FPS : int

    Returns
    -------
    None.

    '''
    for bonus in bonuses:
        bonus.app(screen, fullscreen)
        bonus.check_tank(tank, FPS)
        if not bonus.active:
            bonuses.remove(bonus)


def tank_traps_live(traps, screen, enemies, fullscreen, explosions, FPS, fb, wb):
    '''
    This function shows and checks current conditions of each mine

    Parameters
    ----------
    traps : list
        New traps will be added there
    screen : Surface
    enemies : list
        Is needed for checking if an enemy is harmed
    fullscreen : bool
    explosions : list
        If a trap is activated, a new explosion will be added there
    FPS : int
    fb : TYPE
        Fullscreen block size.
    wb : TYPE
        Window block size.

    Returns
    -------
    None.

    '''
    for trap in traps:
        trap.app(screen, fullscreen)
        for enemy in enemies:
            enemy.hp = trap.check_objs(enemy)
        if not trap.active:
            full_block_size = fb
            window_block_size = wb
            trap.explose(explosions, FPS, fullscreen,
                         full_block_size, window_block_size, False)
            traps.remove(trap)


def enemy_traps_live(enemy_traps, screen, fullscreen, tank, explosions, FPS, fb, wb):
    '''
    This funciton doesn't show, but checking current traps' conditions.

    Parameters
    ----------
    enemy_traps : list
        If an enemy 'wants' to leave a trap, it will be added there
    screen : Surface
    fullscreen : bool
    tank : Tank object
        Checking if traps harm the tank
    explosions : list
        If trap is activated, it causes an explosion(is adding there)
    FPS : int
    fb : int
        Fullscreen block size.
    wb : int
        Window block size.

    Returns
    -------
    None.

    '''
    for trap in enemy_traps:
        trap.app(screen, fullscreen)
        tank.hp = trap.check_objs(tank)
        if not trap.active:
            full_block_size = fb
            window_block_size = wb
            trap.explose(explosions, FPS, fullscreen,
                         full_block_size, window_block_size, False)
            enemy_traps.remove(trap)


def explosions_live(explosions, screen, objs):
    '''
    This function shows us all the explsoions are in the game

    Parameters
    ----------
    explosions : list
        Current list of explosions(always updates).
    screen : Surface
    objs : list
        List of all the objects(is needed for checking
        if an explosion harms an object).

    Returns
    -------
    None.

    '''
    for explosion in explosions:
        explosion.app(screen)
        for obj in objs:
            explosion.check_objects(obj)
        if not explosion.active:
            explosions.remove(explosion)


pg.init()
pg.font.init()

# Defining screen parameters
FPS = 30
flags = pg.FULLSCREEN
display_info = pg.display.Info()
full_size = (display_info.current_w, display_info.current_h)
window_size = (854, 480)
screen = pg.display.set_mode(window_size)
pg.display.set_caption('TANKS')
clock = pg.time.Clock()

# Defining game blocks parameters
game_resolution = (24, 13)
number_x = game_resolution[0]
number_y = game_resolution[1]
window_block_size = min((window_size[0] // number_x), (window_size[1] // number_y))
full_block_size = min((full_size[0] // number_x), (full_size[1] // number_y))

# Defifing all the start parameters
tank = Tank([[0, 0], (window_block_size, window_block_size)], LIGHT_GREEN)
objs = [tank]
enemies, bullets, enemy_bullets, explosions = [], [], [], []
traps, enemy_traps, bonuses = [], [], []
spawns, tank_spawn = None, None
GROUND_COLOR = DARK_GRASS
BACKGROUND = DARK_GRAY

# Default modes
menu_mode = True
fullscreen, finished, show_HUD = False, False, False
tank_is_moving = [False, False, False, False]

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
# Adding buttons into the definite menu
main_menu.add_buttons([begin, choose_level])
level_menu.add_buttons([level1, level2, level3, level4, level5, return_button])
menus = [main_menu, level_menu]

while not finished:
    mouse_pos = pg.mouse.get_pos()
    # If current mode is menu mode, show menus, otherwise - show game field
    if menu_mode:
        screen.fill(BACKGROUND)
        for menu in menus:
            if menu.active:
                menu.app(screen, BACKGROUND, mouse_pos)
    else:
        # Updating main game parameters
        screen.fill(GROUND_COLOR)
        clock.tick(FPS)
        mouse_pos = pg.mouse.get_pos()
        block_params = define_grid(fullscreen, window_size, 
                                   full_size, level.resolution)
        spawns, tank_spawn = level.app(screen, block_params, walls_hp)
        walls = Walls(level, block_params)
        # Spawning the tank if it is not spawned
        if not tank.spawned:
            tank.x, tank.y = tank_spawn[0], tank_spawn[1]
            tank.spawned = True
        # Showing all the game elements on screen
        spawn_actions(objs, enemies, spawns, window_block_size, 
                      full_block_size, fullscreen)
        bonuses_live(bonuses, screen, fullscreen, tank, FPS)
        tank_traps_live(traps, screen, enemies, fullscreen, 
                        explosions, FPS, full_block_size, window_block_size)
        enemy_traps_live(enemy_traps, screen, fullscreen, tank, 
                         explosions, FPS, full_block_size, window_block_size)
        enemies_live(objs, enemies)
        tank.app(screen, mouse_pos, fullscreen)
        tank.continue_move(walls.walls, walls_hp, tank_is_moving)
        explosions_live(explosions, screen, objs)
        # Tank's bullets actions(killing enemies, breaking walls, explosing)
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
        # Enemy bullets actions(killing tank, breaking walls, explosing)
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
        if show_HUD:
            tank.show_HUD(screen)
        # If tank dies, level ends
        if tank.hp <= 0:
            menu_mode, main_menu.active = True, True
            tank.hp = 20
            tank.x, tank.y = 400, 137
            tank.spawned = False
            objs = [tank]
            enemies, bullets, enemy_bullets, explosions = [], [], [], []
            traps, enemy_traps, bonuses = [], [], []
            tank_spawn, spawns, level, level_number = None, None, None, None
            
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            # Enabling tank motion mode
            if not menu_mode:
                controls = [pg.K_RIGHT, pg.K_LEFT, pg.K_UP, pg.K_DOWN]
                if event.key in controls:
                    tank_is_moving = tank.move(event, walls.walls, walls_hp, tank_is_moving)
        if event.type == pg.KEYUP:
            # Stop tank motion
            if not menu_mode:    
                controls = [pg.K_RIGHT, pg.K_LEFT, pg.K_UP, pg.K_DOWN]
                if event.key in controls:
                    tank_is_moving = tank.stop(event, tank_is_moving)
        if event.type == pg.KEYDOWN and event.key == pg.K_F11:
            # Change window mode and recalculating objects' parameters
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
            # Leaving trap
            if not menu_mode:
                if tank.traps > 0:
                    traps.append(Trap(tank, 'tank'))
                    tank.traps -= 1
        if event.type == pg.KEYDOWN and event.key == pg.K_TAB:
            # Enabling HUD mode
            if not menu_mode:
                show_HUD = True
        if event.type == pg.KEYUP and event.key == pg.K_TAB:
            # Disabling HUD mode
            if not menu_mode:
                show_HUD = False
        if event.type == pg.QUIT:
            finished = True
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            # If in game - shoot, if in menu - push a button
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
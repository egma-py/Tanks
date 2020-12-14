import pygame as pg
import pygame.draw as pgd
import math as m
from random import randint

from colors import *
from menu import *
from textures import *
from tank import *
from enemy import *


class EnemyBullet:
    '''ENEMY BULLET
    
    Description: if an enemy shoots, this class
    describes the behaviour of enemy's bullet.
    Functions close_walls and in_wall work the same way
    as other classes' ones.
    '''
    def __init__(self, enemy, enemy_bullets):
        self.active = True
        self.in_tank = False
        self.block_size = enemy.Rect[1][0]
        self.radius = 6
        cannon_pos = [enemy.x + enemy.Rect[1][0] // 2,
                      enemy.y + enemy.Rect[1][1] // 2]
        # Defining start coords depending on enemy's angle
        if enemy.angle == 0:
            self.x = cannon_pos[0]
            self.y = cannon_pos[1] + enemy.cannon_l
            self.speed_x = 0
            self.speed_y = 20
        if enemy.angle == 90:
            self.x = cannon_pos[0] - enemy.cannon_l
            self.y = cannon_pos[1]
            self.speed_x = -20
            self.speed_y = 0
        if enemy.angle == 180:
            self.x = cannon_pos[0]
            self.y = cannon_pos[1] - enemy.cannon_l
            self.speed_x = 0
            self.speed_y = -20
        if enemy.angle == 270:
            self.x = cannon_pos[0] + enemy.cannon_l
            self.y = cannon_pos[1]
            self.speed_x = 20
            self.speed_y = 0

    def check_hit(self, tank):
        '''
        This one checks if a bullet hits the tank.

        Parameters
        ----------
        tank : Tank object

        Returns
        -------
        int
            New tank HP.

        '''
        x, y = self.x, self.y
        left_border = tank.x
        right_border = tank.x + tank.Rect[1][0]
        up_border = tank.y
        down_border = tank.y + tank.Rect[1][0]
        if right_border > x > left_border and down_border > y > up_border:
            self.in_tank = True
            return tank.hp - 2
        else:
            return tank.hp

    def explose(self, explosions, FPS, fullscreen, full_block, window_block, dangerous):
        explosions.append(Explosion(self.x, self.y, FPS, fullscreen,
                                    full_block, window_block, dangerous))

    def close_walls(self, walls, walls_hp):
        block_size = int(self.block_size)
        x, y = self.x, self.y
        close_walls = []
        for i in range(len(walls)):
            # Distances between bullet and wall in each axis
            dx = abs(x - walls[i][0][0][0])
            dy = abs(y - walls[i][0][0][1])
            wall_hp = walls_hp[i][0]
            if dx < 2 * block_size and dy < block_size and wall_hp != 0:
                close_walls.append(walls[i])
        return close_walls

    def in_wall(self, walls, walls_hp):
        '''
        Returning crash_wall is needed in app function.
        '''
        # Defining the closest walls for optimisation
        close_walls = self.close_walls(walls, walls_hp)

        def check_in_wall(pos):
            '''
            Parameters
            ----------
            pos : tuple

            Returns
            -------
            check : bool
            crash_wall : Rect
                It is needed to define explosion's coords.

            '''
            x = pos[0]
            y = pos[1]
            check = False
            crash_wall = None
            for wall in close_walls:
                left_border = wall[0][0][0]
                right_border = wall[0][0][0] + wall[0][1][0]
                top_border = wall[0][0][1]
                down_border = wall[0][0][1] + wall[0][1][1]
                if right_border >= x >= left_border:
                    if down_border >= y >= top_border:
                        check = True
                        crash_wall = wall
            return check, crash_wall

        inwall = False
        current_bullet_pos = (self.x, self.y)
        check, crash_wall = check_in_wall(current_bullet_pos)
        if check:
            inwall = True
            # Explosion pos is in the center of crash wall
            self.x = crash_wall[0][0][0] + crash_wall[0][1][0] // 2
            self.y = crash_wall[0][0][1] + crash_wall[0][1][0] // 2
        return inwall, crash_wall
    
    def app(self, screen, walls, walls_hp, fullscreen):
        '''
        This function draw a bullet.
        In addition this function checks if 
        a bullet collides into a wall.

        Parameters
        ----------
        screen : Surface
        walls : list
        walls_hp : list
        fullscreen : bool

        Returns
        -------
        walls_hp : list
            Return new walls' HP according to bullet moves.

        '''
        # Defining radius depending on window mode
        if fullscreen:
            self.radius = 8
        else:
            self.radius = 6
        # Drawing a bullet
        pgd.circle(screen, BLACK, (self.x, self.y), self.radius)
        # Checking if there is a collide
        inwall, crash_wall = self.in_wall(walls, walls_hp)
        if inwall:
            self.active = False
            index = walls.index(crash_wall)
            if walls_hp[index][0] > 0:
                walls_hp[index][0] -= 1
            if walls_hp[index][0] == 0:
                walls_hp[index][1] = 0
        else:
            self.x += self.speed_x
            self.y += self.speed_y
        return walls_hp


class Bullet:
    '''BULLET
    
    Description: if you shoot, this class
    describes the behaviour of tank's bullet.
    Functions close_walls and in_wall work the same way
    as other classes' ones.
    '''
    Speed = 20
    
    def __init__(self, tank, bullets, mouse_pos):
        self.active = True
        self.in_enemy = False
        self.block_size = tank.Rect[1][0]
        self.radius = 6
        cannon_pos = [tank.x + tank.Rect[1][0] // 2,
                      tank.y + tank.Rect[1][1] // 2]
        # Defining bullet's coords depending on mouse_pos
        if (cannon_pos[1] - mouse_pos[1]) > 0:
            angle = m.atan((mouse_pos[0] - cannon_pos[0]) / (cannon_pos[1] - mouse_pos[1]))
            self.x = cannon_pos[0] + int(tank.cannon_l * m.sin(angle))
            self.y = cannon_pos[1] - int(tank.cannon_l * m.cos(angle))
        elif (cannon_pos[1] - mouse_pos[1]) < 0:
            angle = -m.atan((mouse_pos[0] - cannon_pos[0]) / (cannon_pos[1] - mouse_pos[1]))
            self.x = cannon_pos[0] + int(tank.cannon_l * m.sin(angle))
            self.y = cannon_pos[1] + int(tank.cannon_l * m.cos(angle))
        elif (cannon_pos[1] - mouse_pos[1]) == 0:
            if (cannon_pos[0] - mouse_pos[0]) < 0:
                angle = m.pi / 2
                self.x = cannon_pos[0] + tank.cannon_l
                self.y = cannon_pos[1]
            else:
                angle = -m.pi / 2
                self.x = cannon_pos[0] - tank.cannon_l
                self.y = cannon_pos[1]
        # defining bullet's speed depending on angle
        if cannon_pos[1] - mouse_pos[1] > 0:
            self.speed_x = int(Bullet.Speed * m.sin(angle))
            self.speed_y = -int(Bullet.Speed * m.cos(angle))
        else:
            self.speed_x = int(Bullet.Speed * m.sin(angle))
            self.speed_y = int(Bullet.Speed * m.cos(angle))

    def check_hit(self, enemy):
        '''
        This one checks if a bullet hits an enemy.

        Parameters
        ----------
        enemy : Enenmy object

        Returns
        -------
        int
            New enemy HP.

        '''
        x, y = self.x, self.y
        left_border = enemy.x
        right_border = enemy.x + enemy.Rect[1][0]
        up_border = enemy.y
        down_border = enemy.y + enemy.Rect[1][0]
        if right_border > x > left_border and down_border > y > up_border:
            self.in_enemy = True
            return enemy.hp - 2
        else:
            return enemy.hp

    def explose(self, explosions, FPS, fullscreen, full_block, window_block, dangerous):
        explosions.append(Explosion(self.x, self.y, FPS, fullscreen,
                                    full_block, window_block, dangerous))

    def close_walls(self, walls, walls_hp):
        block_size = int(self.block_size)
        x, y = self.x, self.y
        close_walls = []
        for i in range(len(walls)):
            # Distances between bullet and wall in each axis
            dx = abs(x - walls[i][0][0][0])
            dy = abs(y - walls[i][0][0][1])
            wall_hp = walls_hp[i][0]
            if dx < 2 * block_size and dy < block_size and wall_hp != 0:
                close_walls.append(walls[i])
        return close_walls

    def in_wall(self, walls, walls_hp):
        '''
        Returning crash_wall is needed in app function.
        '''
        # Defining the closest walls for optimisation
        close_walls = self.close_walls(walls, walls_hp)

        def check_in_wall(pos):
            '''
            Parameters
            ----------
            pos : tuple

            Returns
            -------
            check : bool
            crash_wall : Rect
                It is needed to define explosion's coords.

            '''
            x = pos[0]
            y = pos[1]
            check = False
            crash_wall = None
            for wall in close_walls:
                left_border = wall[0][0][0]
                right_border = wall[0][0][0] + wall[0][1][0]
                top_border = wall[0][0][1]
                down_border = wall[0][0][1] + wall[0][1][1]
                if right_border >= x >= left_border:
                    if down_border >= y >= top_border:
                        check = True
                        crash_wall = wall
            return check, crash_wall

        inwall = False
        current_bullet_pos = (self.x, self.y)
        check, crash_wall = check_in_wall(current_bullet_pos)
        if check:
            inwall = True
            # Explosion pos is in the center of crash wall
            self.x = crash_wall[0][0][0] + crash_wall[0][1][0] // 2
            self.y = crash_wall[0][0][1] + crash_wall[0][1][0] // 2
        return inwall, crash_wall
    
    def app(self, screen, walls, walls_hp, fullscreen):
        '''
        This function draw a bullet.
        In addition this function checks if 
        a bullet collides into a wall.

        Parameters
        ----------
        screen : Surface
        walls : list
        walls_hp : list
        fullscreen : bool

        Returns
        -------
        walls_hp : list
            Return new walls' HP according to bullet moves.

        '''
        # Defining radius depending on window mode
        if fullscreen:
            self.radius = 8
        else:
            self.radius = 6
        # Drawing a bullet
        pgd.circle(screen, BLACK, (self.x, self.y), self.radius)
        # Checking if there is a collide
        inwall, crash_wall = self.in_wall(walls, walls_hp)
        if inwall:
            self.active = False
            index = walls.index(crash_wall)
            if walls_hp[index][0] > 0:
                walls_hp[index][0] -= 1
            if walls_hp[index][0] == 0:
                walls_hp[index][1] = 0
        else:
            self.x += self.speed_x
            self.y += self.speed_y
        return walls_hp


class Explosion:
    '''EXPLOSION
    
    Description: if bullet collides, mine exploses or
    enemy dies, this class describes the behaviour of
    each explosion.
    '''

    def __init__(self, x, y, FPS, fullscreen, full_block, window_block, dangerous):
        self.dangerous = dangerous
        self.x = x
        self.y = y
        self.explosion_time = FPS // 6
        if fullscreen:
            self.max_radius = full_block
        else:
            self.max_radius = window_block
        # Start variables
        self.time = self.explosion_time
        self.radius = 0
        self.active = True

    def app(self, screen):
        '''
        This function draws current condition
        of an explose.

        Parameters
        ----------
        screen : Surface

        Returns
        -------
        None.

        '''
        pgd.circle(screen, ORANGE, (self.x, self.y), int(self.radius))
        # Reducing lifetime and increasing radius
        self.time -= 1
        self.radius += self.max_radius / self.explosion_time
        # If lifetime is equal zero
        if self.time == 0:
            self.active = False

    def check_objects(self, sensitive_obj):
        '''
        If an explose is dangerous, it is
        needed to check if an object will 
        get harm or not

        Parameters
        ----------
        sensitive_obj : Tank or Enemy object
            Each object can harm itself and
            each other.

        Returns
        -------
        None.

        '''
        if self.dangerous:
            obj_pos = sensitive_obj.center
            x = obj_pos[0]
            y = obj_pos[1]
            distance = m.sqrt((self.x - x)**2 + (self.y - y)**2)
            if distance <= self.radius:
                sensitive_obj.hp -= 1
                self.active = False


class Trap:
    '''TRAP
    
    Description: Each object can leave a trap
    Your ones are visible, enemies' ones are not.
    '''
    
    def __init__(self, obj, whose):
        self.type = whose
        self.x = obj.center[0]
        self.y = obj.center[1]
        self.active = True
        self.r = 5

    def app(self, screen, fullscreen):  # FIXME мигание
        '''
        Checks, whose the mine is
        if tank's -> visible
        otherwise -> invisible

        Parameters
        ----------
        screen : Surface
        fullscreen : bool

        Returns
        -------
        None

        '''
        if fullscreen:
            self.r = 10
        else:
            self.r = 5
        if self.type == 'tank':
            pgd.circle(screen, BLUE, (self.x, self.y), self.r)
        else:
            pgd.circle(screen, RED, (self.x, self.y), self.r)

    def check_objs(self, obj):
        '''
        Checks if objects get onto the mine.

        Parameters
        ----------
        obj : Tank or Enemy object

        Returns
        -------
        int
            Returns new object's HP1.

        '''
        x = obj.x
        y = obj.y
        if x < self.x < x + obj.Rect[1][0] and y < self.y < y + obj.Rect[1][0]:
            self.active = False
            return obj.hp - 4
        else:
            return obj.hp

    def explose(self, explosions, FPS, fullscreen, full_block, window_block, dangerous):
        explosions.append(Explosion(self.x, self.y, FPS, fullscreen,
                                    full_block, window_block, dangerous))


class Walls:
    '''WALLS
    
    Description: contains only the list of the walls
    in the level. It is useful to work only with 
    walls to control tank's motion.
    '''

    def __init__(self, level, block_params):
        block_size = block_params[1][0]
        start_x = block_params[0][0]
        start_y = block_params[0][1]
        self.walls = []
        self.turns = []
        i, j = 0, 0
        # Making walls list
        for block_line in level.blocks:
            for block in block_line:
                Rect = ((start_x + block_size * j,
                         start_y + block_size * i),
                        (block_size, block_size))
                j += 1
                if block == '-' or block == '^' or block == '|':
                    self.walls.append([Rect, -1])
                elif block == 'V' or block == 'H':
                    self.walls.append([Rect, 3])
            i += 1
            j = 0
        i, j = 0, 0
        # Making turns list
        for block_line in level.blocks:
            for block in block_line:
                Rect = ((start_x + block_size * j,
                         start_y + block_size * i),
                        (block_size, block_size))
                j += 1
                if block == 't':
                    self.turns.append([Rect, -1])
            i += 1
            j = 0


class Bonus:
    '''BONUS
    
    Description: if there is a bonus after
    enemy's death, this class describes it.
    '''
    
    def __init__(self, enemy, bonus_type):
        '''Bonus types:
            - HP
            - Ammo
            - Speed boost
        '''
        self.x = enemy.center[0]
        self.y = enemy.center[1]
        self.type = bonus_type
        self.active = True

    def app(self, screen, fullscreen):
        if fullscreen:
            self.r = 12
        else:
            self.r = 6
        if self.type == 'HP':
            pgd.circle(screen, RED, (self.x, self.y), self.r)
        elif self.type == 'Ammo':
            pgd.circle(screen, YELLOW, (self.x, self.y), self.r)
        elif self.type == 'Speed':
            pgd.circle(screen, BLUE, (self.x, self.y), self.r)

    def check_tank(self, tank, FPS):
        '''
        Checks if tank catches a bonus.

        Parameters
        ----------
        tank : Tank object
        FPS : int

        Returns
        -------
        None.

        '''
        block_size = tank.Rect[1][0] * 0.8
        x = tank.x
        y = tank.y
        if x < self.x < x + block_size and y < self.y < y + block_size:
            self.active = False
            if self.type == 'HP':
                tank.hp += 10
            elif self.type == 'Ammo':
                tank.ammo += 20
            elif self.type == 'Speed':
                tank.boost_time += FPS * 5


class Level:
    '''LEVEL
    
    Description: this class contains all the info about blocks
    and type of blocks in current level. The info about a level
    is read from file.
    '''

    def __init__(self, blocks):
        self.blocks = blocks
        max_block_len = 0
        for block_line in blocks:
            if len(block_line) >= max_block_len:
                max_block_len = len(block_line)
        self.resolution = (max_block_len, len(blocks))

    def get_walls_hp(self):
        walls_hp = []
        i, j = 0, 0
        for block_line in self.blocks:
            for block in block_line:
                j += 1
                if block in '-|^':
                    walls_hp.append([-1, 1])
                if block in 'VH':
                    walls_hp.append([3, 1])
                if block in 'ots':
                    pass  # ground block
            i += 1
            j = 0
        return walls_hp

    def app(self, screen, block_params, walls_hp):
        '''
        This function draws current conditions of each wall in the level.

        Parameters
        ----------
        screen : Surface
        block_params : tuple
            The first elem is start coords in grid.
            The second one is block size.
        walls_hp : list

        Returns
        -------
        spawn : tuple
            Returns enemies' spawn block.

        '''
        block_size = block_params[1][0]
        start_x = block_params[0][0]
        start_y = block_params[0][1]
        index = 0
        # Enumerating block lines
        for m in range(len(self.blocks)):
            # Enumerating blocks in each line
            for k in range(len(self.blocks[m])):
                Rect = ((start_x + block_size * k,
                         start_y + block_size * m),
                        (block_size, block_size))
                # drawing walls
                if self.blocks[m][k] == '-':
                    index += 1
                    draw_wall_horizontal(screen, Rect)
                if self.blocks[m][k] == '|':
                    draw_wall_vertical(screen, Rect)
                    index += 1
                if self.blocks[m][k] == '^':
                    draw_corner(screen, Rect)
                    index += 1
                if self.blocks[m][k] == 'V':
                    if walls_hp[index] != [0, 0]:
                        draw_wall_breakable_vertical(screen, Rect, 0)
                    index += 1
                if self.blocks[m][k] == 'H':
                    if walls_hp[index] != [0, 0]:
                        draw_wall_breakable_horizontal(screen, Rect, 0)
                    index += 1
                if self.blocks[m][k] == 's':
                    spawn = [Rect[0][0] + 5, Rect[0][1] + 5]
        return spawn
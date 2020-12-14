import pygame as pg
import pygame.draw as pgd
import math as m
from random import randint

from colors import *
from menu import *
from textures import *
from tank import *
from game_objects import *


class Enemy:
    '''ENEMY
    
    Description: object Enemy is also one of the main 
    objects in the game. You cannot control it. It
    lives its own life:
        - moves
        - turns
        - leaving mines(they are invisible, for you)
        - shoots
    Some functions there work the same as in class Tank.
    Some special functions are described.
    '''
    def __init__(self, Rect, color):
        '''
        Let me describe some variables, defined
        in this function:
            
        angle - it defines enemy's orientation 
        in the space. This parameter is also
        needed for enemy's shooting
        
        freeze - when an enemy turns, freeze
        becoming equal to 2 seconds. It is 
        necessary, otherwise an enemy will
        be always rotating at the same position.
        
        Shoot and trap factors are created to define, 
        when the enemy "wants" to shoot.
        '''
        # Coordinates and useful parameters
        self.Rect = Rect
        self.x = Rect[0][0]
        self.y = Rect[0][1]
        self.center = [self.x + self.Rect[1][0] // 2,
                       self.y + self.Rect[1][0] // 2]
        # Cannon's parameters (l-lenght, w-width, r-radius)
        self.params = [int(self.Rect[1][0] * 1.2 / 2),
                       int(self.Rect[1][0] * 0.2 / 2),
                       int(self.Rect[1][0] * 0.3 / 2),
                       int(self.Rect[1][0] * 0.4 / 2)]
        self.cannon_l = self.params[0]
        self.cannon_r = self.params[1]
        self.cannon_w = self.params[2]
        self.tower_r = self.params[3]
        # Enemy's game start variables
        self.hp = 10
        self.traps = 1
        self.speed_x = 0
        self.speed_y = 2
        self.angle = 0
        self.freeze = 0
        self.shoot_factor = 0
        self.trap_factor = 0
        self.color = color
        
    def shoot(self, enemy_bullets):
        enemy_bullets.append(EnemyBullet(self, enemy_bullets))

    def make_trap(self, enemy_traps):
        enemy_traps.append(Trap(self, 'enemy'))

    def app(self, screen, mouse_pos, enemy_bullets, enemy_traps):
        '''
        This functions has the same importance, as the tank's one.
        It defines, if the enemy "wants" to shoot or leave a trap or not.

        Parameters
        ----------
        screen : Surface
        mouse_pos : tuple
        enemy_bullets : list
            New bullets will be added there.
        enemy_traps : list
            New traps will be added there.

        Returns
        -------
        None.

        '''
        # If an enemy is alive, continue its life
        if self.hp > 0:
            # Defining if the enemy "wants" to shoot or leave a trap or not.
            self.shoot_factor = randint(1, 100)
            self.trap_factor = randint(1, 200)
            # If "wants"
            if self.shoot_factor == 100:
                self.shoot(enemy_bullets)
            if self.trap_factor == 200 and self.traps > 0:
                self.make_trap(enemy_traps)
                self.traps -= 1
            # Redefining parameters
            self.center = [self.x + self.Rect[1][0] // 2,
                           self.y + self.Rect[1][0] // 2]
            self.cannon_l = self.params[0]
            self.cannon_r = self.params[1]
            self.cannon_w = self.params[2]
            self.tower_r = self.params[3]
            tank_pos = (self.x + int(self.Rect[1][0] * 0.1), 
                        self.y + int(self.Rect[1][1] * 0.1))
            size = (int(self.Rect[1][0] * 0.8), 
                    int(self.Rect[1][1] * 0.8))
            # Drawing the enemy's body
            pgd.rect(screen, self.color, (tank_pos, size))
            pgd.circle(screen, RED, self.center, self.tower_r)
            # Defining the cannon's position
            if self.angle == 0:
                cannon_pos = (self.center[0], 
                              self.center[1] + self.cannon_l)
            if self.angle == 90:
                cannon_pos = (self.center[0] - self.cannon_l, 
                              self.center[1])
            if self.angle == 180:
                cannon_pos = (self.center[0], 
                              self.center[1] - self.cannon_l)
            if self.angle == 270:
                cannon_pos = (self.center[0] + self.cannon_l, 
                              self.center[1])
            # Drawing the enemy's cannon
            pgd.line(screen, RED, self.center, cannon_pos, self.cannon_w)
            pgd.circle(screen, RED, cannon_pos, self.cannon_r)

    def die(self, bonuses, explosions, FPS, fullscreen, 
            full_block, window_block, dangerous):
        '''
        This function is called when you kill an enemy

        Parameters
        ----------
        bonuses : list
            If an enemy dies, there will be a chance
            of bonus appearing on its place.
            If it appears, it will be added there
        explosions : list
            New explosion will be added there.
        FPS : int
            Explosion's time of life depends on it.
            
        fullscreen : bool
        full_block : int
        window_block : int
            Explosion's radius will depend on fullscreen mode
            
        dangerous : bool
            If an explosion is not dangerous, there
            will be no risks to be damaged by it.

        Returns
        -------
        None.

        '''
        explosions.append(Explosion(self.x, self.y, FPS, fullscreen,
                                    full_block, window_block, dangerous))
        bonus_factor = randint(1, 4)
        if bonus_factor == 4:
            bonus_type = randint(1, 3)
            if bonus_type == 1:
                bonuses.append(Bonus(self, 'HP'))
            elif bonus_type == 2:
                bonuses.append(Bonus(self, 'Ammo'))
            elif bonus_type == 3:
                bonuses.append(Bonus(self, 'Speed'))

    def close_walls(self, walls, walls_hp):
        '''
        Works the same way as tank's one.

        Parameters
        ----------
        walls : list
        walls_hp : list

        Returns
        -------
        close_walls : list

        '''
        block_size = int(self.Rect[1][0] * 0.8)
        x, y = self.x, self.y
        close_walls = []
        for i in range(len(walls)):
            # dx and dy are distances in each axis
            dx = abs(x - walls[i][0][0][0])
            dy = abs(y - walls[i][0][0][1])
            wall_hp = walls_hp[i][0]
            if dx < 2 * block_size and dy < 2 * block_size and wall_hp != 0:
                # If a wall is close to the enemy
                close_walls.append(walls[i])
        return close_walls

    def close_turns(self, turns):
        '''
        Works as close_walls, but defines close turns.

        Parameters
        ----------
        turns : list

        Returns
        -------
        close_turns : list

        '''
        block_size = int(self.Rect[1][0] * 0.8)
        x, y = self.x, self.y
        close_turns = []
        for i in range(len(turns)):
            # dx and dy are distances in each axis
            dx = abs(x - turns[i][0][0][0])
            dy = abs(y - turns[i][0][0][1])
            if dx < 2 * block_size and dy < 2 * block_size:
                # If a turn is close to the enemy
                close_turns.append(turns[i])
        return close_turns

    def in_wall(self, walls, walls_hp):
        '''
        The same as tank's one.

        Parameters
        ----------
        walls : list
        walls_hp : list

        Returns
        -------
        inwall : bool

        '''
        # Defining the closest walls for optimisation
        close_walls = self.close_walls(walls, walls_hp)

        def check_in_wall(pos):
            '''
            The same as tank's one.

            Parameters
            ----------
            pos : tuple

            Returns
            -------
            check : bool

            '''
            x = pos[0]
            y = pos[1]
            check = False
            for wall in close_walls:
                left_border = wall[0][0][0]
                right_border = wall[0][0][0] + wall[0][1][0]
                top_border = wall[0][0][1]
                down_border = wall[0][0][1] + wall[0][1][1]
                if right_border >= x >= left_border:
                    if down_border >= y >= top_border:
                        check = True
            return check

        inwall = False
        pos = (self.x + int(self.Rect[1][0] * 0.1), 
               self.y + int(self.Rect[1][1] * 0.1))
        x = pos[0]
        y = pos[1]
        block_size = int(self.Rect[1][0] * 0.8)
        # Enemy's key positions
        right_top = (x + block_size, y)
        left_top = (x, y)
        right_down = (x + block_size, y + block_size)
        left_down = (x, y + block_size)
        for wall in close_walls:
            if check_in_wall(right_top):
                inwall = True
            if check_in_wall(left_top):
                inwall = True
            if check_in_wall(right_down):
                inwall = True
            if check_in_wall(left_down):
                inwall = True
        return inwall

    def in_turn(self, turns):
        '''
        Works the same way as in_wall, but checks if 
        an enemy is in turn or not.

        Parameters
        ----------
        turns : list

        Returns
        -------
        inturn : bool
            Returns true, if ALL the positions are in a turn.

        '''
        close_turns = self.close_turns(turns)

        def check_in_turn(pos):
            x = pos[0]
            y = pos[1]
            check = False
            for turn in close_turns:
                left_border = turn[0][0][0]
                right_border = turn[0][0][0] + turn[0][1][0]
                top_border = turn[0][0][1]
                down_border = turn[0][0][1] + turn[0][1][1]
                if right_border > x > left_border:
                    if down_border > y > top_border:
                        check = True
            return check

        inturn = False
        pos = (self.x + int(self.Rect[1][0] * 0.1), self.y + int(self.Rect[1][1] * 0.1))
        x = pos[0]
        y = pos[1]
        block_size = int(self.Rect[1][0] * 0.8)
        # Enemy's key positions
        right_top = (x + block_size, y)
        left_top = (x, y)
        right_down = (x + block_size, y + block_size)
        left_down = (x, y + block_size)
        for turn in close_turns:
            if check_in_turn(right_top):
                if check_in_turn(left_top):
                    if check_in_turn(right_down):
                        if check_in_turn(left_down):
                            inturn = True
        return inturn

    def rotate(self):
        '''
        This function randomly chooses a new
        directions for enemy's moves.

        Returns
        -------
        None.

        '''
        direction_number = randint(1, 4)
        if direction_number == 1:
            direction = 'right'
        if direction_number == 2:
            direction = 'left'
        if direction_number == 3:
            direction = 'up'
        if direction_number == 4:
            direction = 'down'
        if direction == 'right':
            self.angle = 270
            self.speed_x = 2
            self.speed_y = 0
        if direction == 'left':
            self.angle = 90
            self.speed_x = -2
            self.speed_y = 0
        if direction == 'up':
            self.angle = 180
            self.speed_x = 0
            self.speed_y = -2
        if direction == 'down':
            self.angle = 0
            self.speed_x = 0
            self.speed_y = 2

    def move(self, blocks, walls_hp, FPS, fullscreen):
        '''
        This function defines, where an enemy "wants" 
        to move. If it collides a wall, it turns into 
        the other directon.
        If it is in a turn, it randomly choose: turn or
        not turn.

        Parameters
        ----------
        blocks : Wall object
            It contains the info about turns and walls.
        walls_hp : list
        FPS : int
            This parameter is used to define freeze.
        fullscreen : bool
            If fullscreen mode is enabled, enemy's
            speed will be increased two times more.

        Returns
        -------
        None.

        '''
        if fullscreen:
            increase = 2
        else:
            increase = 1
        # If an enemy is alive, it continues to do its actions
        if self.hp > 0:
            # Close turns are defined for optimisation
            close_turns = self.close_turns(blocks.turns)
            if self.freeze > 0:
                self.freeze -= 1
            if not self.in_wall(blocks.walls, walls_hp):
                self.x += self.speed_x * increase
                self.y += self.speed_y * increase
            elif self.in_wall(blocks.walls, walls_hp):
                self.x -= self.speed_x * increase
                self.y -= self.speed_y * increase
                self.rotate()
            inturn = self.in_turn(close_turns)
            inwall = self.in_wall(blocks.walls, walls_hp)
            # Turn if enemy is not "freezed" and not in wall
            if inturn == True and inwall == False and self.freeze == 0:
                self.rotate()
                self.freeze = 2 * FPS
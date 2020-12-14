import pygame as pg
import pygame.draw as pgd
import math as m
from random import randint

from colors import *
from menu import *
from textures import *
from game_objects import *
from enemy import *

pg.font.init()
font = pg.font.Font(None, 25)


class Tank:
    '''TANK

    Description: object Tank is the main object in the
    game. We can absolutely control it: shooting, lea-
    ving mines, aiming and moving.
    '''

    def __init__(self, Rect, color):
        # Coordinates and useful variables
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
        # Tank's game start parameters
        self.speed = 3
        self.hp = 20
        self.ammo = 100
        self.traps = 3
        self.boost_time = 0
        self.color = color
        # HUD info
        self.HUD_pos = (self.x + int(1.2 * self.Rect[1][0]),
                        self.y)
        self.HUD_size = (self.Rect[1][0] * 3,
                         self.Rect[1][0] * 2.5)

    def show_HUD(self, screen):
        '''
        This function shows us current conditions
        of the tank if show_HUD bool is true

        Parameters
        ----------
        screen : Surface

        Returns
        -------
        None.

        '''
        self.HUD_pos = (self.x + int(1.2 * self.Rect[1][0]),
                        self.y)
        current_HP = font.render(str(self.hp) + '/20', True, RED)
        current_ammo = font.render('Ammo: ' + str(self.ammo), True, RED)
        current_traps = font.render('Traps: ' + str(self.traps), True, RED)
        current_boost = font.render('Boost: +', True, RED)
        pgd.rect(screen, YELLOW, (self.HUD_pos, self.HUD_size))
        screen.blit(current_HP, (self.HUD_pos[0] + 2, self.HUD_pos[1] + 2))
        screen.blit(current_ammo, (self.HUD_pos[0] + 2, self.HUD_pos[1] + 20))
        screen.blit(current_traps, (self.HUD_pos[0] + 2, self.HUD_pos[1] + 40))
        if self.boost_time > 0:
            screen.blit(current_boost, (self.HUD_pos[0] + 2, self.HUD_pos[1] + 60))

    def app(self, screen, mouse_pos, fullscreen):
        '''
        That's the main function in this class. It checks
        current tank's conditions and changes variables,
        depending on these conditions.

        Parameters
        ----------
        screen : Surface
            This parameter is used to show the object
            on screen in main module.
        mouse_pos : tuple
            This parameter is used to orient the can-
            non depending on mouse position.
        fullscreen : bool
            This parameter is used to change tank's
            parameters while the game is running.

        Returns
        -------
        None.

        '''
        # Checking if tank has a boost
        if self.boost_time > 0:
            self.boost_time -= 1
            k = 1.5
        else:
            k = 1
        # Checking if there is a fullscreen mode or not
        if fullscreen:
            self.speed = int(6 * k)
        else:
            self.speed = int(3 * k)
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
        # Drawing tank's body
        pgd.rect(screen, self.color, (tank_pos, size))
        pgd.circle(screen, RED, self.center, self.tower_r)
        # This big part of code draws the cannon, depending on mouse_pos
        if (self.center[1] - mouse_pos[1]) > 0:
            arctg = m.atan((mouse_pos[0] - self.center[0]) / (self.center[1] - mouse_pos[1]))
            new_cannon_x = int(self.center[0] + self.cannon_l * m.sin(arctg))
            new_cannon_y = int(self.center[1] - self.cannon_l * m.cos(arctg))
        elif (self.center[1] - mouse_pos[1]) < 0:
            arctg = m.atan((mouse_pos[0] - self.center[0]) / (self.center[1] - mouse_pos[1]))
            new_cannon_x = int(self.center[0] - self.cannon_l * m.sin(arctg))
            new_cannon_y = int(self.center[1] + self.cannon_l * m.cos(arctg))
        else:
            if (self.center[0] - mouse_pos[0]) > 0:
                new_cannon_x = self.center[0] - self.cannon_l
                new_cannon_y = self.center[1]
            else:
                new_cannon_x = self.center[0] + self.cannon_l
                new_cannon_y = self.center[1]
        # Drawing the cannon after all calculations
        pgd.line(screen, RED, self.center, (new_cannon_x, new_cannon_y), self.cannon_w)
        pgd.circle(screen, RED, (new_cannon_x, new_cannon_y), self.cannon_r)

    def move(self, event, walls, walls_hp, moving):
        '''
        This function moves the tank, depending on our
        pushes on the keyboard.

        Parameters
        ----------
        event : Eventlist
            This is parameter is used to check, what
            key is pressed.
        walls : list
            This parameter is used to check if tank
            collides into a wall.
        walls_hp : list
            If wall is destroyed, its HP is zero. So
            if HP is zero, the tank can move through
            it.
        moving : list
            A list of four bools; each of them can
            tell us, if the tank is moving in definite
            direction.

        Returns
        -------
        moving : list
            Returns the list of four bools after some
            calculations.

        '''
        up = moving[0]
        down = moving[1]
        right = moving[3]
        left = moving[2]
        if event.key == pg.K_RIGHT:
            right = True
            self.x += self.speed
            if self.in_wall(walls, walls_hp):
                self.x -= self.speed
        if event.key == pg.K_LEFT:
            left = True
            self.x -= self.speed
            if self.in_wall(walls, walls_hp):
                self.x += self.speed
        if event.key == pg.K_UP:
            up = True
            self.y -= self.speed
            if self.in_wall(walls, walls_hp):
                self.y += self.speed
        if event.key == pg.K_DOWN:
            down = True
            self.y += self.speed
            if self.in_wall(walls, walls_hp):
                self.y -= self.speed
        self.Rect[0] = [self.x, self.y]
        moving = [up, down, left, right]
        return moving

    def continue_move(self, walls, walls_hp, moving):
        '''
        This function doesn't return anything, because
        this one only checks if definite button  is pu-
        shed. If it is, the function continues to move
        the tank.

        Parameters
        ----------
        event : Eventlist
            This is parameter is used to check, what
            key is pressed.
        walls : list
            This parameter is used to check if tank
            collides into a wall.
        walls_hp : list
            If wall is destroyed, its HP is zero. So
            if HP is zero, the tank can move through
            it.
        moving : list
            A list of four bools; each of them can
            tell us, if the tank is moving in definite
            direction.

        Returns
        -------
        None.

        '''
        right = moving[3]
        left = moving[2]
        down = moving[1]
        up = moving[0]
        if right:
            self.x += self.speed
            if self.in_wall(walls, walls_hp):
                self.x -= self.speed
        if left:
            self.x -= self.speed
            if self.in_wall(walls, walls_hp):
                self.x += self.speed
        if down:
            self.y += self.speed
            if self.in_wall(walls, walls_hp):
                self.y -= self.speed
        if up:
            self.y -= self.speed
            if self.in_wall(walls, walls_hp):
                self.y += self.speed
        self.Rect[0] = [self.x, self.y]

    def stop(self, event, moving):
        '''
        This function checks if a button is
        pushed up or not. And if it is, it will
        stop the tank's movement.

        Parameters
        ----------
        event : list
            This parameter is used to check, what
            key was pushed up.
        moving : list
            This parameter is used to get current
            moving conditons.

        Returns
        -------
        moving : list
            If definite button is pushed up and
            others are not, only pushed up one
            will be changed to a False statement
            and tank's moves in this direction
            will stop.

        '''
        up = moving[0]
        down = moving[1]
        left = moving[2]
        right = moving[3]
        if event.key == pg.K_UP:
            up = False
        if event.key == pg.K_DOWN:
            down = False
        if event.key == pg.K_LEFT:
            left = False
        if event.key == pg.K_RIGHT:
            right = False
        moving = [up, down, left, right]
        return moving

    def close_walls(self, walls, walls_hp):
        '''
        This function is very useful for opti-
        misation. It defines the closest walls
        in relation to the tank

        Parameters
        ----------
        walls : list
        walls_hp : list
            If a wall's HP is zero, the tank
            can move through it.

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
                # If a wall is close to the tank
                close_walls.append(walls[i])
        return close_walls

    def in_wall(self, walls, walls_hp):
        '''
        This function checks if the tank is in a wall.

        Parameters
        ----------
        walls : list
        walls_hp : list
            These two parameters are so useful
            to check collision conditions easily.

        Returns
        -------
        inwall : bool

        '''
        # Defining the closest walls for optimisation
        close_walls = self.close_walls(walls, walls_hp)

        def check_in_wall(pos):
            '''
            This function is created to be the code
            more readable. It is unnecessary, but very
            convenient to use

            Parameters
            ----------
            pos : tuple
                The current position.

            Returns
            -------
            check : bool
                If current position is in wall, return True.
                In other conditions - False.

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
        # Tank's key positions
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
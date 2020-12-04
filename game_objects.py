from colors import *
from menu import *
from textures import *

import pygame.draw as pgd
import pygame as pg
import math as m


class Tank:
    '''
    This class is the object of the tank,
    that can be controlled by us. 
    '''
    speed = 3 #FIXME fit the speed to a window size
    def __init__(self, Rect, color):
        self.Rect = Rect
        self.x = Rect[0][0]
        self.y = Rect[0][1]
        self.color = color
        self.params = [int(self.Rect[1][0]*1.2/2),
                       int(self.Rect[1][0]*0.2/2),
                       int(self.Rect[1][0]*0.3/2),
                       int(self.Rect[1][0]*0.4/2)]
        self.cannon_l = self.params[0]
        self.cannon_r = self.params[1]
        self.cannon_w = self.params[2]
        self.tower_r = self.params[3]
        self.speed = Tank.speed
        
    
    def app(self, screen, pos):
        self.cannon_l = self.params[0]
        self.cannon_r = self.params[1]
        self.cannon_w = self.params[2]
        self.tower_r = self.params[3]
        pos = (self.x + int(self.Rect[1][0]*0.1), self.y + int(self.Rect[1][1]*0.1))
        size = (int(self.Rect[1][0]*0.8), int(self.Rect[1][1]*0.8))
        pgd.rect(screen, self.color, (pos, size))
        cannon_pos = [self.x + self.Rect[1][0]//2, 
                      self.y + self.Rect[1][1]//2]
        pgd.circle(screen, RED, cannon_pos, self.tower_r)
        if (cannon_pos[1] - pos[1]) > 0:
            arctg = m.atan((pos[0] - cannon_pos[0])/(cannon_pos[1] - pos[1]))
            new_cannon_x = int(cannon_pos[0] + self.cannon_l*m.sin(arctg))
            new_cannon_y = int(cannon_pos[1] - self.cannon_l*m.cos(arctg))
            pgd.line(screen, RED, cannon_pos, (new_cannon_x, new_cannon_y), self.cannon_w)
            pgd.circle(screen, RED, (new_cannon_x, new_cannon_y), self.cannon_r)
        elif (cannon_pos[1] - pos[1]) < 0:
            arctg = m.atan((pos[0] - cannon_pos[0])/(cannon_pos[1] - pos[1]))
            new_cannon_x = int(cannon_pos[0] - self.cannon_l*m.sin(arctg))
            new_cannon_y = int(cannon_pos[1] + self.cannon_l*m.cos(arctg))
            pgd.line(screen, RED, cannon_pos, (new_cannon_x, new_cannon_y), self.cannon_w)
            pgd.circle(screen, RED, (new_cannon_x, new_cannon_y), self.cannon_r)
    
    
    def check_keydown(self, event, walls):
        if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
            self.x += self.speed
            if self.in_wall(walls):
                self.x -= self.speed
        if event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
            self.x -= self.speed
            if self.in_wall(walls):
                self.x += self.speed
        if event.type == pg.KEYDOWN and event.key == pg.K_UP:
            self.y -= self.speed
            if self.in_wall(walls):
                self.y += self.speed
        if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
            self.y += self.speed
            if self.in_wall(walls):
                self.y -= self.speed
        self.Rect[0] = [self.x, self.y]
    
    
    def check_key_pressed(self, keys, walls):
        if keys[275] == 1:
            self.x += self.speed
            if self.in_wall(walls):
                self.x -= self.speed
        if keys[276] == 1:
            self.x -= self.speed
            if self.in_wall(walls):
                self.x += self.speed
        if keys[273] == 1:
            self.y -= self.speed
            if self.in_wall(walls):
                self.y += self.speed
        if keys[274] == 1:
            self.y += self.speed
            if self.in_wall(walls):
                self.y -= self.speed
        self.Rect[0] = [self.x, self.y]
        
        
    def in_wall(self, walls):
        def check_in_wall(pos):
            x = pos[0]
            y = pos[1]
            check = False
            for wall in walls:
                if x>=wall[0][0] and x<=(wall[0][0]+wall[1][0]):
                    if y>=(wall[0][1]) and y<=(wall[0][1]+wall[1][1]):
                        check = True
            return check
        inwall = False
        pos = (self.x + int(self.Rect[1][0]*0.1), self.y + int(self.Rect[1][1]*0.1))
        x = pos[0]
        y = pos[1]
        block_size = int(self.Rect[1][0]*0.8)
        right_top = (x + block_size, y)
        left_top = (x, y)
        right_down = (x + block_size, y + block_size)
        left_down = (x, y + block_size)
        for wall in walls:    
            if check_in_wall(right_top):
                inwall = True
            if check_in_wall(left_top):
                inwall = True
            if check_in_wall(right_down):
                inwall = True
            if check_in_wall(left_down):
                inwall = True
        return inwall


class Bullet:
    pass


class Trap:
    pass


class Walls:
    '''
    Contains only the list of the walls
    in the level. It is useful to work
    only with walls to control tank's
    motion/
    '''
    def __init__(self, level, block_params):
        block_size = block_params[1][0]
        start_x = block_params[0][0]
        start_y = block_params[0][1]
        self.walls = []
        i, j = 0, 0
        for block_line in level.blocks:
            for block in block_line:
                Rect = ((start_x + block_size*j,
                         start_y + block_size*i), 
                        (block_size, block_size))
                j += 1
                if block == '-' or block == '^' or block == '|':
                    self.walls.append(Rect)
            i += 1
            j = 0

class Shelter:
    pass


class HUD:
    pass


class Level:
    '''
    This class contains all the info about blocks
    and type of blocks in current level.
    The info about a level is read from file
    '''
    def __init__(self, blocks):
        self.blocks = blocks
        max_block_len = 0
        for block_line in blocks:
            if len(block_line) >= max_block_len:
                max_block_len = len(block_line)
        self.resolution = (max_block_len, len(blocks))
        
        
    def app(self, screen, block_params):
        block_size = block_params[1][0]
        start_x = block_params[0][0]
        start_y = block_params[0][1]
        i, j = 0, 0
        for block_line in self.blocks:
            for block in block_line:
                Rect = ((start_x + block_size*j,
                         start_y + block_size*i), 
                        (block_size, block_size))
                j += 1
                if block == '-':
                    draw_wall_horizontal(screen, Rect)
                if block == '|':
                    draw_wall_vertical(screen, Rect)
                if block == '^':
                    draw_corner(screen, Rect)
                if block == 'o':
                    draw_ground(screen, Rect)
            i += 1
            j = 0
        
        
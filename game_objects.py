from colors import *
from menu import *
from textures import *
from random import randint

import pygame.draw as pgd
import pygame as pg
import math as m


class Tank:
    '''
    This class is the object of the tank,
    that can be controlled by us.
    '''

    def __init__(self, Rect, color):
        self.Rect = Rect
        self.x = Rect[0][0]
        self.y = Rect[0][1]
        self.color = color
        self.params = [int(self.Rect[1][0] * 1.2 / 2),
                       int(self.Rect[1][0] * 0.2 / 2),
                       int(self.Rect[1][0] * 0.3 / 2),
                       int(self.Rect[1][0] * 0.4 / 2)]
        self.cannon_l = self.params[0]
        self.cannon_r = self.params[1]
        self.cannon_w = self.params[2]
        self.tower_r = self.params[3]
        self.speed = 3
        self.hp = 20
        self.center = (self.x + self.Rect[1][0] // 2,
                       self.y + self.Rect[1][0] // 2)

    def app(self, screen, mouse_pos, fullscreen):
        if fullscreen:
            self.speed = 6
        else:
            self.speed = 3
        self.center = [self.x + self.Rect[1][0] // 2,
                       self.y + self.Rect[1][0] // 2]
        self.cannon_l = self.params[0]
        self.cannon_r = self.params[1]
        self.cannon_w = self.params[2]
        self.tower_r = self.params[3]
        tank_pos = (self.x + int(self.Rect[1][0] * 0.1), self.y + int(self.Rect[1][1] * 0.1))
        size = (int(self.Rect[1][0] * 0.8), int(self.Rect[1][1] * 0.8))
        pgd.rect(screen, self.color, (tank_pos, size))
        pgd.circle(screen, RED, self.center, self.tower_r)
        if (self.center[1] - mouse_pos[1]) > 0:
            arctg = m.atan((mouse_pos[0] - self.center[0]) / (self.center[1] - mouse_pos[1]))
            new_cannon_x = int(self.center[0] + self.cannon_l * m.sin(arctg))
            new_cannon_y = int(self.center[1] - self.cannon_l * m.cos(arctg))
            pgd.line(screen, RED, self.center, (new_cannon_x, new_cannon_y), self.cannon_w)
            pgd.circle(screen, RED, (new_cannon_x, new_cannon_y), self.cannon_r)
        elif (self.center[1] - mouse_pos[1]) < 0:
            arctg = m.atan((mouse_pos[0] - self.center[0]) / (self.center[1] - mouse_pos[1]))
            new_cannon_x = int(self.center[0] - self.cannon_l * m.sin(arctg))
            new_cannon_y = int(self.center[1] + self.cannon_l * m.cos(arctg))
            pgd.line(screen, RED, self.center, (new_cannon_x, new_cannon_y), self.cannon_w)
            pgd.circle(screen, RED, (new_cannon_x, new_cannon_y), self.cannon_r)
        else:
            if (self.center[0] - mouse_pos[0]) > 0:
                new_cannon_x = self.center[0] - self.cannon_l
                new_cannon_y = self.center[1]
                pgd.line(screen, RED, self.center, (new_cannon_x, new_cannon_y), self.cannon_w)
                pgd.circle(screen, RED, (new_cannon_x, new_cannon_y), self.cannon_r)
            else:
                new_cannon_x = self.center[0] + self.cannon_l
                new_cannon_y = self.center[1]
                pgd.line(screen, RED, self.center, (new_cannon_x, new_cannon_y), self.cannon_w)
                pgd.circle(screen, RED, (new_cannon_x, new_cannon_y), self.cannon_r)

    def move(self, event, walls, walls_hp, moving):
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

    def in_wall(self, walls, walls_hp):
        close_walls = self.close_walls(walls, walls_hp)

        def check_in_wall(pos):
            x = pos[0]
            y = pos[1]
            check = False
            for wall in close_walls:
                if x >= wall[0][0][0] and x <= (wall[0][0][0] + wall[0][1][0]):
                    if y >= (wall[0][0][1]) and y <= (wall[0][0][1] + wall[0][1][1]):
                        check = True
            return check

        inwall = False
        pos = (self.x + int(self.Rect[1][0] * 0.1), self.y + int(self.Rect[1][1] * 0.1))
        x = pos[0]
        y = pos[1]
        block_size = int(self.Rect[1][0] * 0.8)
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

    def close_walls(self, walls, walls_hp):
        block_size = int(self.Rect[1][0] * 0.8)
        x, y = self.x, self.y
        close_walls = []
        for i in range(len(walls)):
            dx = x - walls[i][0][0][0]
            dy = y - walls[i][0][0][1]
            wall_hp = walls_hp[i][0]
            if abs(dx) < 2 * block_size and abs(dy) < 2 * block_size and wall_hp != 0:
                close_walls.append(walls[i])
        return close_walls


class Enemy:
    def __init__(self, Rect, color):
        self.Rect = Rect
        self.x = Rect[0][0]
        self.y = Rect[0][1]
        self.color = color
        self.params = [int(self.Rect[1][0] * 1.2 / 2),
                       int(self.Rect[1][0] * 0.2 / 2),
                       int(self.Rect[1][0] * 0.3 / 2),
                       int(self.Rect[1][0] * 0.4 / 2)]
        self.cannon_l = self.params[0]
        self.cannon_r = self.params[1]
        self.cannon_w = self.params[2]
        self.tower_r = self.params[3]
        self.speed_x = 0
        self.speed_y = 2
        self.angle = 0
        self.freeze = 0
        self.shoot_factor = 0
        self.trap_factor = 0
        self.hp = 20
        self.center = [self.x + self.Rect[1][0] // 2,
                       self.y + self.Rect[1][0] // 2]

    def app(self, screen, mouse_pos, fullscreen, enemy_bullets, enemy_traps):
        self.shoot_factor = randint(1, 100)
        self.trap_factor = randint(1, 200)
        if self.shoot_factor == 100:
            self.shoot(enemy_bullets)
        if self.trap_factor == 200:
            self.make_trap(enemy_traps)
        if fullscreen:
            self.speed_x = 2 * self.speed_x
            self.speed_y = 2 * self.speed_y
        self.center = [self.x + self.Rect[1][0] // 2,
                       self.y + self.Rect[1][0] // 2]
        self.cannon_l = self.params[0]
        self.cannon_r = self.params[1]
        self.cannon_w = self.params[2]
        self.tower_r = self.params[3]
        tank_pos = (self.x + int(self.Rect[1][0] * 0.1), self.y + int(self.Rect[1][1] * 0.1))
        size = (int(self.Rect[1][0] * 0.8), int(self.Rect[1][1] * 0.8))
        pgd.rect(screen, self.color, (tank_pos, size))
        pgd.circle(screen, RED, self.center, self.tower_r)
        if self.angle == 0:
            cannon_pos = (self.center[0], self.center[1] + self.cannon_l)
            pgd.line(screen, RED, self.center, cannon_pos, self.cannon_w)
            pgd.circle(screen, RED, cannon_pos, self.cannon_r)
        if self.angle == 90:
            cannon_pos = (self.center[0] - self.cannon_l, self.center[1])
            pgd.line(screen, RED, self.center, cannon_pos, self.cannon_w)
            pgd.circle(screen, RED, cannon_pos, self.cannon_r)
        if self.angle == 180:
            cannon_pos = (self.center[0], self.center[1] - self.cannon_l)
            pgd.line(screen, RED, self.center, cannon_pos, self.cannon_w)
            pgd.circle(screen, RED, cannon_pos, self.cannon_r)
        if self.angle == 270:
            cannon_pos = (self.center[0] + self.cannon_l, self.center[1])
            pgd.line(screen, RED, self.center, cannon_pos, self.cannon_w)
            pgd.circle(screen, RED, cannon_pos, self.cannon_r)

    def shoot(self, enemy_bullets):
        enemy_bullets.append(EnemyBullet(self, enemy_bullets))

    def make_trap(self, enemy_traps):
        enemy_traps.append(Trap(self, 'enemy'))

    def move(self, blocks, walls_hp, FPS):
        close_turns = self.close_turns(blocks.turns)
        if self.freeze > 0:
            self.freeze -= 1
        if not self.in_wall(blocks.walls, walls_hp):
            self.x += self.speed_x
            self.y += self.speed_y
        elif self.in_wall(blocks.walls, walls_hp):
            self.x -= self.speed_x
            self.y -= self.speed_y
            self.rotate()
        if self.in_turn(close_turns) == True and self.freeze == 0 and self.in_wall(blocks.walls, walls_hp) == False:
            self.rotate()
            self.freeze = 2 * FPS

    def rotate(self):
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

    def in_turn(self, turns):
        close_turns = self.close_turns(turns)

        # print(close_turns)
        def check_in_turn(pos):
            x = pos[0]
            y = pos[1]
            check = False
            for turn in close_turns:
                if x > turn[0][0][0] and x < (turn[0][0][0] + turn[0][1][0]):
                    if y > (turn[0][0][1]) and y < (turn[0][0][1] + turn[0][1][1]):
                        check = True
            return check

        inturn = False
        pos = (self.x + int(self.Rect[1][0] * 0.1), self.y + int(self.Rect[1][1] * 0.1))
        x = pos[0]
        y = pos[1]
        block_size = int(self.Rect[1][0] * 0.8)
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

    def close_turns(self, turns):
        block_size = int(self.Rect[1][0] * 0.8)
        x, y = self.x, self.y
        close_turns = []
        for i in range(len(turns)):
            dx = x - turns[i][0][0][0]
            dy = y - turns[i][0][0][1]
            if abs(dx) < 2 * block_size and abs(dy) < 2 * block_size:
                close_turns.append(turns[i])
        return close_turns

    def in_wall(self, walls, walls_hp):
        close_walls = self.close_walls(walls, walls_hp)

        def check_in_wall(pos):
            x = pos[0]
            y = pos[1]
            check = False
            for wall in close_walls:
                if x >= wall[0][0][0] and x <= (wall[0][0][0] + wall[0][1][0]):
                    if y >= (wall[0][0][1]) and y <= (wall[0][0][1] + wall[0][1][1]):
                        check = True
            return check

        inwall = False
        pos = (self.x + int(self.Rect[1][0] * 0.1), self.y + int(self.Rect[1][1] * 0.1))
        x = pos[0]
        y = pos[1]
        block_size = int(self.Rect[1][0] * 0.8)
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

    def close_walls(self, walls, walls_hp):
        block_size = int(self.Rect[1][0] * 0.8)
        x, y = self.x, self.y
        close_walls = []
        for i in range(len(walls)):
            dx = x - walls[i][0][0][0]
            dy = y - walls[i][0][0][1]
            wall_hp = walls_hp[i][0]
            if abs(dx) < 2 * block_size and abs(dy) < 2 * block_size and wall_hp != 0:
                close_walls.append(walls[i])
        return close_walls


class EnemyBullet:
    def __init__(self, enemy, enemy_bullets):
        self.block_size = enemy.Rect[1][0]
        self.active = True
        self.in_tank = False
        self.radius = 6
        cannon_pos = [enemy.x + enemy.Rect[1][0] // 2,
                      enemy.y + enemy.Rect[1][1] // 2]
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

    def app(self, screen, walls, walls_hp, fullscreen):
        if fullscreen:
            self.radius = 8
        else:
            self.radius = 6
        pgd.circle(screen, BLACK, (self.x, self.y), self.radius)
        check_params = self.in_wall(walls, walls_hp)
        wall = check_params[1]
        if check_params[0]:
            self.active = False
            index = walls.index(wall)
            if walls_hp[index][0] > 0:
                walls_hp[index][0] -= 1
            if walls_hp[index][0] == 0:
                walls_hp[index][1] = 0
        else:
            self.x += self.speed_x
            self.y += self.speed_y
        return walls_hp

    def check_hit(self, tank):
        left_x = tank.x
        right_x = tank.x + tank.Rect[1][0]
        up_y = tank.y
        down_y = tank.y + tank.Rect[1][0]
        if right_x > self.x > left_x and down_y > self.y > up_y:
            self.in_tank = True
            return tank.hp - 2
        else:
            return tank.hp

    def explose(self, explosions, FPS, fullscreen, full_block, window_block, dangerous):
        explosions.append(Explosion(self.x,
                                    self.y,
                                    FPS,
                                    fullscreen,
                                    full_block,
                                    window_block,
                                    dangerous))

    def close_walls(self, walls, walls_hp):
        block_size = int(self.block_size)
        x, y = self.x, self.y
        close_walls = []
        for i in range(len(walls)):
            dx = x - walls[i][0][0][0]
            dy = y - walls[i][0][0][1]
            wall_hp = walls_hp[i][0]
            if abs(dx) < 2 * block_size and abs(dy) < block_size and wall_hp != 0:
                close_walls.append(walls[i])
        return close_walls

    def in_wall(self, walls, walls_hp):
        close_walls = self.close_walls(walls, walls_hp)

        def check_in_wall(pos):
            x = pos[0]
            y = pos[1]
            check = False
            crash_wall = None
            for wall in close_walls:
                if x >= wall[0][0][0] and x <= (wall[0][0][0] + wall[0][1][0]):
                    if y >= (wall[0][0][1]) and y <= (wall[0][0][1] + wall[0][1][1]):
                        check = True
                        crash_wall = wall
            return (check, crash_wall)

        inwall = False
        current_bullet_pos = (self.x, self.y)
        check_params = check_in_wall(current_bullet_pos)
        if check_params[0]:
            inwall = True
            wall = check_params[1]
            self.x = wall[0][0][0] + wall[0][1][0] // 2
            self.y = wall[0][0][1] + wall[0][1][0] // 2
        return [inwall, check_params[1]]


class Bullet:
    '''
    is created when a user presses left mouse button
    '''
    speed = 20

    def __init__(self, tank, bullets, mouse_pos):
        self.block_size = tank.Rect[1][0]
        self.active = True
        self.in_enemy = False
        self.radius = 6
        cannon_pos = [tank.x + tank.Rect[1][0] // 2,
                      tank.y + tank.Rect[1][1] // 2]
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
        if cannon_pos[1] - mouse_pos[1] > 0:
            self.speed_x = int(Bullet.speed * m.sin(angle))
            self.speed_y = -int(Bullet.speed * m.cos(angle))
        else:
            self.speed_x = int(Bullet.speed * m.sin(angle))
            self.speed_y = int(Bullet.speed * m.cos(angle))

    def app(self, screen, walls, walls_hp, fullscreen):
        if fullscreen:
            self.radius = 8
        else:
            self.radius = 6
        pgd.circle(screen, BLACK, (self.x, self.y), self.radius)
        check_params = self.in_wall(walls, walls_hp)
        wall = check_params[1]
        if check_params[0]:
            self.active = False
            index = walls.index(wall)
            if walls_hp[index][0] > 0:
                walls_hp[index][0] -= 1
            if walls_hp[index][0] == 0:
                walls_hp[index][1] = 0
        else:
            self.x += self.speed_x
            self.y += self.speed_y
        return walls_hp

    def explose(self, explosions, FPS, fullscreen, full_block, window_block, dangerous):
        explosions.append(Explosion(self.x,
                                    self.y,
                                    FPS,
                                    fullscreen,
                                    full_block,
                                    window_block,
                                    dangerous))

    def close_walls(self, walls, walls_hp):
        block_size = int(self.block_size)
        x, y = self.x, self.y
        close_walls = []
        for i in range(len(walls)):
            dx = x - walls[i][0][0][0]
            dy = y - walls[i][0][0][1]
            wall_hp = walls_hp[i][0]
            if abs(dx) < 2 * block_size and abs(dy) < block_size and wall_hp != 0:
                close_walls.append(walls[i])
        return close_walls

    def in_wall(self, walls, walls_hp):
        close_walls = self.close_walls(walls, walls_hp)

        def check_in_wall(pos):
            x = pos[0]
            y = pos[1]
            check = False
            crash_wall = None
            for wall in close_walls:
                if x >= wall[0][0][0] and x <= (wall[0][0][0] + wall[0][1][0]):
                    if y >= (wall[0][0][1]) and y <= (wall[0][0][1] + wall[0][1][1]):
                        check = True
                        crash_wall = wall
            return (check, crash_wall)

        inwall = False
        current_bullet_pos = (self.x, self.y)
        check_params = check_in_wall(current_bullet_pos)
        if check_params[0]:
            inwall = True
            wall = check_params[1]
            self.x = wall[0][0][0] + wall[0][1][0] // 2
            self.y = wall[0][0][1] + wall[0][1][0] // 2
        return [inwall, check_params[1]]

    def check_hit(self, enemy):
        left_x = enemy.x
        right_x = enemy.x + enemy.Rect[1][0]
        up_y = enemy.y
        down_y = enemy.y + enemy.Rect[1][0]
        if right_x > self.x > left_x and down_y > self.y > up_y:
            self.in_enemy = True
            return enemy.hp - 2
        else:
            return enemy.hp


class Explosion:
    '''
    when a bullet crashes into smth,
    it causes an explosion. This is
    an explosion, which can harm all
    the breakable objects
    '''

    def __init__(self, x, y, FPS, fullscreen, full_block, window_block, dangerous):
        self.x = x
        self.y = y
        self.explosion_time = FPS // 6
        self.time = self.explosion_time
        self.radius = 0
        self.active = True
        self.dangerous = dangerous
        if fullscreen:
            self.max_radius = full_block
        else:
            self.max_radius = window_block

    def app(self, screen):
        pgd.circle(screen, ORANGE, (self.x, self.y), int(self.radius))
        self.time -= 1
        self.radius += self.max_radius / self.explosion_time
        if self.time == 0:
            self.active = False

    def check_objects(self, sensitive_obj):
        if self.dangerous:
            obj_pos = sensitive_obj.center
            distance = m.sqrt((self.x - obj_pos[0]) ** 2 + (self.y - obj_pos[1]) ** 2)
            if distance <= self.radius:
                sensitive_obj.hp -= 1
                self.active = False


class Trap:
    def __init__(self, obj, whose):
        self.type = whose
        self.pos = obj.center
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.active = True
        self.r = 5

    def app(self, screen):  # FIXME мигание
        if self.type == 'tank':
            pgd.circle(screen, BLUE, self.pos, self.r)

    def check_objs(self, obj):
        x = obj.x
        y = obj.y
        if x < self.x < x + obj.Rect[1][0] and y < self.y < y + obj.Rect[1][0]:
            self.active = False
            return obj.hp - 4
        else:
            return obj.hp

    def explose(self, explosions, FPS, fullscreen, full_block, window_block, dangerous):
        explosions.append(Explosion(self.x,
                                    self.y,
                                    FPS,
                                    fullscreen,
                                    full_block,
                                    window_block,
                                    dangerous))


class Walls:
    '''
    Contains only the list of the walls
    in the level. It is useful to work
    only with walls to control tank's
    motion
    '''

    def __init__(self, level, block_params):
        block_size = block_params[1][0]
        start_x = block_params[0][0]
        start_y = block_params[0][1]
        self.walls = []
        self.turns = []
        i, j = 0, 0
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
                if block in 'ot':
                    pass  # ground block
            i += 1
            j = 0
        return walls_hp

    def app(self, screen, block_params, walls_hp):
        block_size = block_params[1][0]
        start_x = block_params[0][0]
        start_y = block_params[0][1]
        index = 0
        for m in range(len(self.blocks)):
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


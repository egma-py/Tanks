import pygame as pg
import pygame.draw as pgd
import math as m
from random import randint

from colors import *
from menu import *
from textures import *


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
        self.boost_time = 0
        self.color = color

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
            if self.trap_factor == 200:
                self.make_trap(enemy_traps)
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


class HUD:
    pass


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
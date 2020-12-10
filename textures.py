<<<<<<< HEAD
''' 
A module to draw only textures. 
It is not documented

some textures to be added:
    - tank
    - enemy
    - bullet
    - trap
    - shelter
    - ...
'''

from colors import *
from random import randint
import pygame.draw as pgd


def draw_wall_breakable_horizontal(screen, Rect, hp): #FIXME hp
    pgd.rect(screen, DARK_BLUE, Rect)
    pgd.rect(screen, DARK_BROWN, Rect, 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0], Rect[0][1]), 
                                  (int(Rect[1][0]*0.6), int(Rect[1][1]/3))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0]+int(Rect[1][0]*0.6), Rect[0][1]), 
                                  (int(Rect[1][0]*0.4), int(Rect[1][1]/3))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0], Rect[0][1]+int(Rect[1][1]/3)), 
                                  (int(Rect[1][0]*0.4), int(Rect[1][1]/3))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0]+int(Rect[1][0]*0.4), Rect[0][1]+int(Rect[1][1]/3)), 
                                  (int(Rect[1][0]*0.6), int(Rect[1][1]/3))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0], Rect[0][1]+2*int(Rect[1][1]/3)), 
                                  (int(Rect[1][0]*0.8), (Rect[1][1]-2*int(Rect[1][1]/3)))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0]+int(Rect[1][0]*0.8), Rect[0][1]+2*int(Rect[1][1]/3)), 
                                  (int(Rect[1][0]*0.2), (Rect[1][1]-2*int(Rect[1][1]/3)))), 2)


def draw_wall_breakable_vertical(screen, Rect, hp): #FIXME hp
    pgd.rect(screen, DARK_BLUE, Rect)
    pgd.rect(screen, DARK_BROWN, Rect, 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0], Rect[0][1]), 
                                  (int(Rect[1][0]/3), int(Rect[1][1]*0.6))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0]+int(Rect[1][0]/3), Rect[0][1]), 
                                  (int(Rect[1][0]/3), int(Rect[1][1]*0.4))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0]+2*int(Rect[1][0]/3), Rect[0][1]), 
                                  ((Rect[1][0]-2*int(Rect[1][0]/3)), int(Rect[1][1]*0.8))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0], Rect[0][1]+int(Rect[1][1]*0.6)), 
                                  (int(Rect[1][0]/3), int(Rect[1][1]*0.4))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0]+int(Rect[1][0]/3), Rect[0][1]+int(Rect[1][1]*0.4)), 
                                  (int(Rect[1][0]/3), int(Rect[1][1]*0.6))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0]+2*int(Rect[1][0]/3), Rect[0][1]+int(Rect[1][1]*0.8)), 
                                  ((Rect[1][0]-2*int(Rect[1][0]/3)), int(Rect[1][1]*0.2))), 2)


def draw_wall_horizontal(screen, Rect):
    pgd.rect(screen, DARK_RED, Rect)
    pgd.rect(screen, DARK_BROWN, Rect, 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0], Rect[0][1]), 
                                  (int(Rect[1][0]*0.6), int(Rect[1][1]/3))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0]+int(Rect[1][0]*0.6), Rect[0][1]), 
                                  (int(Rect[1][0]*0.4), int(Rect[1][1]/3))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0], Rect[0][1]+int(Rect[1][1]/3)), 
                                  (int(Rect[1][0]*0.4), int(Rect[1][1]/3))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0]+int(Rect[1][0]*0.4), Rect[0][1]+int(Rect[1][1]/3)), 
                                  (int(Rect[1][0]*0.6), int(Rect[1][1]/3))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0], Rect[0][1]+2*int(Rect[1][1]/3)), 
                                  (int(Rect[1][0]*0.8), (Rect[1][1]-2*int(Rect[1][1]/3)))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0]+int(Rect[1][0]*0.8), Rect[0][1]+2*int(Rect[1][1]/3)), 
                                  (int(Rect[1][0]*0.2), (Rect[1][1]-2*int(Rect[1][1]/3)))), 2)
    
    
def draw_wall_vertical(screen, Rect):
    pgd.rect(screen, DARK_RED, Rect)
    pgd.rect(screen, DARK_BROWN, Rect, 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0], Rect[0][1]), 
                                  (int(Rect[1][0]/3), int(Rect[1][1]*0.6))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0]+int(Rect[1][0]/3), Rect[0][1]), 
                                  (int(Rect[1][0]/3), int(Rect[1][1]*0.4))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0]+2*int(Rect[1][0]/3), Rect[0][1]), 
                                  ((Rect[1][0]-2*int(Rect[1][0]/3)), int(Rect[1][1]*0.8))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0], Rect[0][1]+int(Rect[1][1]*0.6)), 
                                  (int(Rect[1][0]/3), int(Rect[1][1]*0.4))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0]+int(Rect[1][0]/3), Rect[0][1]+int(Rect[1][1]*0.4)), 
                                  (int(Rect[1][0]/3), int(Rect[1][1]*0.6))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0]+2*int(Rect[1][0]/3), Rect[0][1]+int(Rect[1][1]*0.8)), 
                                  ((Rect[1][0]-2*int(Rect[1][0]/3)), int(Rect[1][1]*0.2))), 2)
    
    
def draw_ground(screen, Rect):
    pgd.rect(screen, LIGHT_YELLOW, Rect)
    
    
def draw_corner(screen, Rect):
    pgd.rect(screen, DARK_GRAY, Rect)
=======
''' 
A module to draw only textures. 
It is not documented

some textures to be added:
    - tank
    - enemy
    - bullet
    - trap
    - shelter
    - ...
'''

from colors import *
from random import randint
import pygame.draw as pgd


def draw_wall_breakable_horizontal(screen, Rect): #FIXME hp
    pgd.rect(screen, DARK_RED, Rect)
    pgd.rect(screen, DARK_BROWN, Rect, 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0], Rect[0][1]), 
                                  (int(Rect[1][0]*0.6), int(Rect[1][1]/3))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0]+int(Rect[1][0]*0.6), Rect[0][1]), 
                                  (int(Rect[1][0]*0.4), int(Rect[1][1]/3))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0], Rect[0][1]+int(Rect[1][1]/3)), 
                                  (int(Rect[1][0]*0.4), int(Rect[1][1]/3))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0]+int(Rect[1][0]*0.4), Rect[0][1]+int(Rect[1][1]/3)), 
                                  (int(Rect[1][0]*0.6), int(Rect[1][1]/3))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0], Rect[0][1]+2*int(Rect[1][1]/3)), 
                                  (int(Rect[1][0]*0.8), (Rect[1][1]-2*int(Rect[1][1]/3)))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0]+int(Rect[1][0]*0.8), Rect[0][1]+2*int(Rect[1][1]/3)), 
                                  (int(Rect[1][0]*0.2), (Rect[1][1]-2*int(Rect[1][1]/3)))), 2)
    for i in range(4):
        pgd.line(screen, DARK_BROWN,
                 (Rect[0][0]+int(Rect[1][0]*randint(5, 95)/100), Rect[0][1]+int(Rect[1][1]*randint(5, 95)/100)), 
                 (Rect[0][0]+int(Rect[1][0]*randint(5, 95)/100), Rect[0][1]+int(Rect[1][1]*randint(5, 95)/100)))


def draw_wall_breakable_vertical(screen, Rect): #FIXME hp
    pgd.rect(screen, DARK_RED, Rect)
    pgd.rect(screen, DARK_BROWN, Rect, 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0], Rect[0][1]), 
                                  (int(Rect[1][0]/3), int(Rect[1][1]*0.6))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0]+int(Rect[1][0]/3), Rect[0][1]), 
                                  (int(Rect[1][0]/3), int(Rect[1][1]*0.4))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0]+2*int(Rect[1][0]/3), Rect[0][1]), 
                                  ((Rect[1][0]-2*int(Rect[1][0]/3)), int(Rect[1][1]*0.8))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0], Rect[0][1]+int(Rect[1][1]*0.6)), 
                                  (int(Rect[1][0]/3), int(Rect[1][1]*0.4))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0]+int(Rect[1][0]/3), Rect[0][1]+int(Rect[1][1]*0.4)), 
                                  (int(Rect[1][0]/3), int(Rect[1][1]*0.6))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0]+2*int(Rect[1][0]/3), Rect[0][1]+int(Rect[1][1]*0.8)), 
                                  ((Rect[1][0]-2*int(Rect[1][0]/3)), int(Rect[1][1]*0.2))), 2)
    for i in range(4):
        pgd.line(screen, DARK_BROWN,
                 (Rect[0][0]+int(Rect[1][0]*randint(5, 95)/100), Rect[0][1]+int(Rect[1][1]*randint(5, 95)/100)), 
                 (Rect[0][0]+int(Rect[1][0]*randint(5, 95)/100), Rect[0][1]+int(Rect[1][1]*randint(5, 95)/100)))


def draw_wall_horizontal(screen, Rect):
    pgd.rect(screen, DARK_RED, Rect)
    pgd.rect(screen, DARK_BROWN, Rect, 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0], Rect[0][1]), 
                                  (int(Rect[1][0]*0.6), int(Rect[1][1]/3))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0]+int(Rect[1][0]*0.6), Rect[0][1]), 
                                  (int(Rect[1][0]*0.4), int(Rect[1][1]/3))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0], Rect[0][1]+int(Rect[1][1]/3)), 
                                  (int(Rect[1][0]*0.4), int(Rect[1][1]/3))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0]+int(Rect[1][0]*0.4), Rect[0][1]+int(Rect[1][1]/3)), 
                                  (int(Rect[1][0]*0.6), int(Rect[1][1]/3))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0], Rect[0][1]+2*int(Rect[1][1]/3)), 
                                  (int(Rect[1][0]*0.8), (Rect[1][1]-2*int(Rect[1][1]/3)))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0]+int(Rect[1][0]*0.8), Rect[0][1]+2*int(Rect[1][1]/3)), 
                                  (int(Rect[1][0]*0.2), (Rect[1][1]-2*int(Rect[1][1]/3)))), 2)
    
    
def draw_wall_vertical(screen, Rect):
    pgd.rect(screen, DARK_RED, Rect)
    pgd.rect(screen, DARK_BROWN, Rect, 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0], Rect[0][1]), 
                                  (int(Rect[1][0]/3), int(Rect[1][1]*0.6))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0]+int(Rect[1][0]/3), Rect[0][1]), 
                                  (int(Rect[1][0]/3), int(Rect[1][1]*0.4))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0]+2*int(Rect[1][0]/3), Rect[0][1]), 
                                  ((Rect[1][0]-2*int(Rect[1][0]/3)), int(Rect[1][1]*0.8))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0], Rect[0][1]+int(Rect[1][1]*0.6)), 
                                  (int(Rect[1][0]/3), int(Rect[1][1]*0.4))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0]+int(Rect[1][0]/3), Rect[0][1]+int(Rect[1][1]*0.4)), 
                                  (int(Rect[1][0]/3), int(Rect[1][1]*0.6))), 2)
    pgd.rect(screen, DARK_BROWN, ((Rect[0][0]+2*int(Rect[1][0]/3), Rect[0][1]+int(Rect[1][1]*0.8)), 
                                  ((Rect[1][0]-2*int(Rect[1][0]/3)), int(Rect[1][1]*0.2))), 2)
    
    
def draw_ground(screen, Rect):
    pgd.rect(screen, LIGHT_YELLOW, Rect)
    
    
def draw_corner(screen, Rect):
    pgd.rect(screen, DARK_GRAY, Rect)
>>>>>>> refs/remotes/origin/main
    pgd.rect(screen, BLACK, Rect, 3)
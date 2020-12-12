from colors import *
from textures import *
from math import pi
import pygame
import pygame.draw as pgd
import pygame.transform as pgt

pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
finished = False
screen.fill(GRAY)
rect = pygame.Surface((50, 50))
new_rect = rect
rect.fill(WHITE)
pgd.rect(rect, RED, ((0, 0), (30, 5)))
screen.blit(new_rect, (100, 10))
x = 10
while not finished:
    clock.tick(1)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            finished = True
        if event.type == pygame.KEYDOWN:
            screen.fill(GRAY)
            new_rect = pgt.rotate(rect, x)
            x += 10
    screen.blit(new_rect, (100, 10))
    pygame.display.update()
    
pygame.quit()
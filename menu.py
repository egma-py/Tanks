from colors import *

import pygame as pg
import pygame.draw as pgd
import math as m


def arc(screen, color, Rect, start_angle, stop_angle, width=0):
    '''
    draws an arc which is better than pygame's one
    '''
    start_angle_to_deg = int((start_angle*360)/(2*m.pi))
    stop_angle_to_deg = int((stop_angle*360)/(2*m.pi))
    x = Rect[0][0]
    y = Rect[0][1]
    xr = Rect[1][0]//2
    yr = Rect[1][1]//2
    if width >= 4:    
        while start_angle_to_deg != stop_angle_to_deg:
            dx = int(xr*m.cos(2*m.pi*start_angle_to_deg/360))
            dy = -int(yr*m.sin(2*m.pi*start_angle_to_deg/360))
            pgd.circle(screen, color, (x+xr+dx, y+yr+dy), width//2)
            start_angle_to_deg += 1
    else:     
        while start_angle_to_deg != stop_angle_to_deg:
            dx0 = int(xr*m.cos(2*m.pi*start_angle_to_deg/360)) 
            dy0 = -int(yr*m.sin(2*m.pi*start_angle_to_deg/360))
            dx = int(xr*m.cos(2*m.pi*start_angle_to_deg/360))
            dy = -int(yr*m.sin(2*m.pi*start_angle_to_deg/360))
            pgd.line(screen, color, (x+xr+dx0, y+yr+dy0), (x+xr+dx, y+yr+dy), width)
            start_angle_to_deg += 1


def roundrect(screen, colors, Rect, width=0, radius=0, R=[-1,-1,-1,-1]):
    """
    screen - game surface
    colors[0] - rect color
    colors[1] - background color
    Rect = ((x, y), (length, height))
    width - if 0 -> filled rect; else with borders with width
            if width number isn't even -> +1
    radius - if all corners are rounded similary
    R - if you wanna define the radius of each corner
    """
    x = Rect[0][0]
    y = Rect[0][1]
    l = Rect[1][0]
    h = Rect[1][1]
    if width%2 != 0:
        width += 1
    if l > h:
        maxR = h//2
    else:
        maxR = l//2
    if radius > maxR:
        radius = maxR
    for i in range(4):
        if R[i] > maxR:
            R[i] = maxR
    def with_width0():
        if R == [-1, -1, -1, -1]:
            circle_centers = [(x+radius, y+radius),
                              (x+l-radius, y+radius),
                              (x+l-radius, y+h-radius),
                              (x+radius, y+h-radius)]
            pgd.rect(screen, 
                     colors[0], 
                     ((x, y+radius), (l, h-2*radius)), 
                     width)
            pgd.rect(screen, 
                     colors[0],
                     ((x+radius, y), (l-2*radius, h)),
                     width)
            for center in circle_centers:
                if radius != 0:
                    pgd.circle(screen, colors[0], center, radius)
        else:
            circle_centers = [(x+R[0], y+R[0]),
                              (x+l-R[1], y+R[1]),
                              (x+l-R[2], y+h-R[2]),
                              (x+R[3], y+h-R[3])]
            pgd.rect(screen, colors[0], Rect, width)
            pgd.rect(screen, colors[1], ((x, y), (R[0], R[0])), width)
            pgd.rect(screen, colors[1], ((x+l-R[1], y), (R[1], R[1])), width)
            pgd.rect(screen, colors[1], ((x+l-R[2], y+h-R[2]), (R[2], R[2])), width)
            pgd.rect(screen, colors[1], ((x, y+h-R[3]), (R[3], R[3])), width)
            for i in range(4):
                if R[i] <= 0:
                    pass
                else:
                    pgd.circle(screen, colors[0], circle_centers[i], R[i])
    def with_widthnot0():
        if R == [-1, -1, -1, -1]:
            starts = [(x+radius, y), 
                      (x+l, y+radius),
                      (x+l-radius, y+h),
                      (x, y+h-radius)]
            ends = [(x+l-radius, y),
                    (x+l, y+h-radius),
                    (x+radius, y+h),
                    (x, y+radius)]
            circle_rects = [((x, y), (2*radius, 2*radius)),
                            ((x+l-2*radius, y), (2*radius, 2*radius)),
                            ((x+l-2*radius, y+h-2*radius), (2*radius, 2*radius)),
                            ((x, y+h-2*radius), (2*radius, 2*radius))]
            angles = [(m.pi/2, m.pi),
                      (0, m.pi/2),
                      (-m.pi/2, 0),
                      (m.pi, 3*m.pi/2)]
            for i in range(4):
                pgd.line(screen, colors[0], starts[i], ends[i], width)
                start = angles[i][0]
                stop = angles[i][1]
                arc(screen, colors[0], circle_rects[i], start, stop, width)
        else:
            starts = [(x+R[0], y), 
                      (x+l, y+R[1]),
                      (x+l-R[2], y+h),
                      (x, y+h-R[3])]
            ends = [(x+l-R[1], y),
                    (x+l, y+h-R[2]),
                    (x+R[3], y+h),
                    (x, y+R[0])]
            circle_rects = [((x, y), (2*R[0], 2*R[0])),
                            ((x+l-2*R[1], y), (2*R[1], 2*R[1])),
                            ((x+l-2*R[2], y+h-2*R[2]), (2*R[2], 2*R[2])),
                            ((x, y+h-2*R[3]), (2*R[3], 2*R[3]))]
            angles = [(m.pi/2, m.pi),
                      (0, m.pi/2),
                      (-m.pi/2, 0),
                      (m.pi, 3*m.pi/2)]
            for i in range(4):
                pgd.line(screen, colors[0], starts[i], ends[i], width)
                start = angles[i][0]
                stop = angles[i][1]
                arc(screen, colors[0], circle_rects[i], start, stop, width)
    if width == 0:
        with_width0()
    else:
        with_widthnot0()
        

class Button:
    def __init__(self, screen, x, y, length, height, colors=[list(RED), list(BLACK)],
                                                     text='None',
                                                     radius=0,
                                                     font=None,
                                                     width=0,
                                                     R=[-1, -1, -1, -1],):
        self.screen = screen
        self.x = x
        self.y = y
        self.len = length
        self.height = height
        self.lenmax = int(1.025*length)
        self.proportion = self.height/self.len
        self.lenmin = length
        self.color = colors
        self.width = width
        self.radius = radius
        self.R = R
        self.font_type = font
        self.button_text = text
        self.fontsize = int(0.8*self.height)
        self.font = pg.font.SysFont(font, self.fontsize)
        self.text = self.font.render(self.button_text, True, self.color[1])
        self.ds = 3
        
        
    def show(self, BACKGROUND):
        roundrect(self.screen, 
                  (self.color[0], BACKGROUND),
                  ((self.x, self.y), (self.len, self.height)),
                  self.width,
                  self.radius,
                  self.R)
        self.screen.blit(self.text, (self.x+10, self.y+int(0.2*self.height)))
    
    
    def app(self, BACKGROUND, m_pos):
        if self.check_pos(m_pos):
            self.scale_plus(BACKGROUND)
            self.disapp(BACKGROUND)
        else:
            self.scale_minus(BACKGROUND)
            self.disapp(BACKGROUND)
        self.show(BACKGROUND)
        
    
    def disapp(self, BACKGROUND):
        Rect = ((self.x, self.y), (self.len, self.height))
        roundrect(self.screen, 
                  (self.color[0], BACKGROUND),
                  Rect,
                  self.width,
                  self.radius,
                  self.R)
        self.screen.blit(self.text, (self.x+10, self.y+int(0.2*self.height)))
        
        
    def check_pos(self, m_pos):
        b_left = self.x+self.len
        b_down = self.y+self.height
        if b_left >= m_pos[0] >= self.x and b_down >= m_pos[1] >= self.y:
            return True
        else:
            return False
        
        
    def scale_plus(self, BACKGROUND):
        self.disapp(BACKGROUND)
        if self.len <= self.lenmax:
            self.disapp(BLACK)
            self.x -= self.ds
            self.len += 2*self.ds
        
        
    def scale_minus(self, BACKGROUND):
        self.disapp(BACKGROUND)
        if self.len >= self.lenmin:
            self.disapp(BLACK)
            self.x += self.ds
            self.len -= 2*self.ds
            
            
class Menu: #FIXME to be made
    '''
    class Menu is an object, which contains
    dialogue windows with buttons
    to interact with user.
    '''
    pass
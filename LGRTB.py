#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 11:10:19 2021

@author: up202108717
"""

import pygame as pg

screen_size = (800, 600)
bee_size = 64


pg.init()

screen = pg.display.set_mode(screen_size)
pg.display.set_caption("Let's Get Ready To Bumble")

bee_rest = pg.image.load("bee_rest.png")
#bee_rest.set_colorkey((,,))

bee_x = int(screen_size[0]/2)-32
bee_y = int(screen_size[1]/2)-32

bee_vx = 0
bee_vy = 0

left_key = right_key = up_key = False
in_leaf = False
clock = pg.time.Clock()

running = True
while running:
    #eventos
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            running = False
    #leis
    
    #desenho
    screen.fill(pg.Color('cyan'))
        
    
    screen.blit(bee_rest, (bee_x, bee_y))
    pg.display.flip()

pg.quit()
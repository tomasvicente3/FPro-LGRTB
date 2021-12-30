#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 11:10:19 2021

@author: up202108717
"""

import pygame as pg

pg.init()

screen_size = (800, 600)
screen = pg.display.set_mode(screen_size)
pg.display.set_caption("Let's Get Ready To Bumble")

bee_rest = pg.image.load("Sprites/bee_rest.png")
bee_rest.set_colorkey((255,0,255))
bee_size = 64

leaf = pg.image.load("Sprites/leaf.png")
leaf.set_colorkey((255,0,255))
leaf_size = (128, 32)

bee_ghost = pg.image.load("Sprites/bee_ghost.png")
bee_ghost.set_colorkey((255,0,255))

#bee_lives = pg.image.load("Sprites/bee_rest.png")
#bee_lives.set_colorkey((255,0,255))
#bee_lives.set_alpha(64)
#bee_mask = pg.image.load("Sprites/bee_mask.png")
#bee_mask.set_colorkey((0, 0, 0))
#bee_mask.set_alpha(64)

relogio = pg.image.load("Sprites/clock.png")
relogio.set_colorkey((255,0,255))
relogio.set_alpha(128)

hive = pg.image.load("Sprites/hive.png")
hive.set_colorkey((255,0,255))
hive.set_alpha(128)



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
        elif ev.type == pg.KEYDOWN:
            if ev.key == pg.K_ESCAPE:
                running = False
            elif ev.key == pg.K_LEFT or ev.key == pg.K_a:
                left_key = True
            elif ev.key == pg.K_RIGHT or ev.key == pg.K_d:
                right_key = True
            elif ev.key == pg.K_UP or ev.key == pg.K_w:
                up_key = True
        elif ev.type == pg.KEYUP:
            if ev.key == pg.K_LEFT or ev.key == pg.K_a:
                left_key = False
            elif ev.key == pg.K_RIGHT or ev.key == pg.K_d:
                right_key = False
            elif ev.key == pg.K_UP or ev.key == pg.K_w:
                up_key = False

    #leis

    dt = clock.tick()
    if up_key:
        bee_vy = -0.3
    elif not in_leaf:
        bee_vy = 0.2

    if left_key:
        bee_vx = -0.4
    elif right_key:
        bee_vx = 0.4
    else:
        bee_vx = 0.0


    bee_oldy = bee_y
    bee_x += bee_vx*dt
    bee_y += bee_vy*dt

    if bee_y>screen_size[1]-bee_size: #limite chão (temporário)
        bee_y = screen_size[1]-bee_size
        bee_vy = 0
        in_leaf = True
    else:
        in_leaf = False

    if bee_x < 0: #limites horizontais
        bee_x = 0
    elif bee_x > screen_size[0]-bee_size:
        bee_x = screen_size[0]-bee_size

#    if bee_vy > 0: #voar
#        for row in range(0, len(level)):
#            for col in range(0, len(level[row])):
#                if level[row][col] == 'leaf':
#                    if bee_x + bee_size >= col * leaf_size and bee_x <= (col+1) * leaf_size:
#                        if bee_y + bee_size >= row * leaf_size and bee_oldy < row * bee_size:
#                            in_leaf = True
#                            bee_vy = 0
#                            bee_y = row * leaf_size - bee_size

    #desenho
    screen.fill(pg.Color('cyan'))


#    screen.blit(bee_mask, (screen_size[0]-64, screen_size[1]-96))
#    screen.blit(bee_rest, (screen_size[0]-64, screen_size[1]-96))
    screen.blit(relogio, (screen_size[0]/2-16, screen_size[1]-64))
    screen.blit(hive, (screen_size[0]/2-16, 32))

    screen.blit(bee_rest, (bee_x, bee_y))

    pg.display.flip()

pg.quit()

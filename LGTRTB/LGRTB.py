#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 11:10:19 2021

@author: up202108717
"""

import pygame as pg
import math

pg.init()

#ecrã
screen_size = (800, 600)
screen = pg.display.set_mode(screen_size)
pg.display.set_caption("Let's Get Ready To Bumble")
pot = pg.image.load("Sprites/pot.png")
pot.set_colorkey((255,0,255))
pg.display.set_icon(pot)
grid = 32

#nível
level = [
    "0000000000000000000000000",
    "0000000000000000000000000",
    "0000000000000000000000000",
    "0000000000000000000F00000",
    "0000000000000000leaf00000",
    "0000000000000000000000000",
    "000000000F000000000000000",
    "000000leaf000000000000000",
    "0000000000000000000000000",
    "0000000000000000000000000",
    "0000000000000000000000000",
    "0000000000000000000000000",
    "00000000000000Xxxx0000000",
    "00000000000000xxxx0000000",
    "000000F000000000000000000",
    "000leaf0000000F0000000000",
    "00000000000leaf000000F000",
    "000000000000000000leaf000",
    "XxxxXxxxXxxxXxxxXxxxXxxxX"
    ]

#background
bg = pg.transform.scale2x(pg.image.load("Sprites/bg.png"))
bg_size = 128*2

#abelha
bee_rest = pg.image.load("Sprites/bee_rest.png")
bee_rest.set_colorkey((255,0,255))
bee_fly = pg.image.load("Sprites/bee_fly.png")
bee_fly.set_colorkey((255, 0, 255))
bee_rest.set_colorkey((255,0,255))
bee_size = 64 #(2,2)

#folha
leaf = pg.image.load("Sprites/leaf.png")
leaf.set_colorkey((255,0,255))
leaf_size = (128, 32) #(4,1)

#flor
flower = pg.image.load("Sprites/flower.png")
flower.set_colorkey((255, 0, 255))
flower_size = 32 #(1,1)

#espinhos
spikes = pg.image.load("Sprites/spikes.png")
spikes.set_colorkey((255, 0, 255))
spikes_size = (128, 64) #(4,2)

#abelha morta
bee_ghost = pg.image.load("Sprites/bee_ghost.png")
bee_ghost.set_colorkey((255,0,255))

#bee_lives = pg.image.load("Sprites/bee_rest.png")
#bee_lives.set_colorkey((255,0,255))
#bee_lives.set_alpha(64)
#bee_mask = pg.image.load("Sprites/bee_mask.png")
#bee_mask.set_colorkey((0, 0, 0))
#bee_mask.set_alpha(64)

#relógio
relogio = pg.image.load("Sprites/clock.png")
relogio.set_colorkey((255,0,255))
relogio.set_alpha(128)

#colmeia (pontuação)
hive = pg.image.load("Sprites/hive.png")
hive.set_colorkey((255,0,255))
hive.set_alpha(128)



bee_x = int(screen_size[0]/2)-32
bee_y = int(screen_size[1]/2)-32

bee_vx = 0
bee_vy = 0

k = 4
bee = [bee_rest]*k + [bee_fly]*k + [bee_ghost]
state = 0

alive = True
res = 0
res_time = 500
lives = 3

flower_cont = 7337

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
    if alive:
        if up_key:
            bee_vy = -0.35
            state = (state+1)%(2*k)
        elif not in_leaf:
            bee_vy = 0.05*dt
            state = 0

        if left_key:
            bee_vx = -0.35
        elif right_key:
            bee_vx = 0.35
        else:
            bee_vx = 0.0

    bee_oldx = bee_x
    bee_oldy = bee_y
    bee_x += bee_vx*dt
    bee_y += bee_vy*dt

    if bee_y>screen_size[1]-bee_size: #limite chão (temporário)
        bee_y = screen_size[1]-bee_size
        bee_vy = 0
        in_leaf = True
    else:
        in_leaf = False

    if bee_x < 0: #limites verticais do ecrã
        bee_x = 0
    elif bee_x > screen_size[0]-bee_size:
        bee_x = screen_size[0]-bee_size

    #interações
    for row in range(0, len(level)):
        for col in range(0, len(level[row])):
            #colisão folhas
            if level[row][col] in 'leaf':
                if bee_x + bee_size >= col * grid and bee_x <= (col+1) * grid:
                    #limite superior
                    if bee_y + bee_size >= row * grid and bee_oldy < row * grid and bee_vy > 0:
                        in_leaf = True
                        bee_vy = 0
                        bee_y = row * grid - bee_size
                    #limite inferior
                    if bee_y < (row+1) * grid and bee_oldy >= (row+1) * grid and bee_vy < 0:
                        bee_vy = 0
                        bee_y = (row+1) * grid
                if bee_y + bee_size > row * grid and bee_y < (row+1) * grid:
                    #limite esquerdo
                    if bee_x + bee_size >= (col) * grid and bee_oldx < (col) * grid and bee_vx > 0:
                        bee_vx = 0
                        bee_x = col*grid - bee_size
                    #limite direito
                    if bee_x < (col+1) * grid and bee_oldx >= (col+1) * grid and bee_vx < 0:
                        bee_vx = 0
                        bee_x = (col+1) * grid

            #apanhar flores
            if level[row][col] == 'F':
                if col*grid-bee_size < bee_x < (col+1)*grid and row*grid-bee_size < bee_y < row*grid:
                    level[row] = level[row][:col] + "0" + level[row][col+1:]

            #espinhos
            if level[row][col] in "Xx":
                if col*grid-bee_size < bee_x < (col+1)*grid and row*grid-bee_size < bee_y < row*grid:
                    bee_vy = -0.01
                    bee_vx = 0.01*math.cos(10*pg.time.get_ticks())
                    alive = False

    if not alive:
        if res < res_time:
            state = 2*k
            res +=1
        else:
            alive = True
            lives -= 1
            bee_x = 300
            bee_y = 100
            state = 0
            res = 0

    if lives == 0:
        running = False

    if flower_cont == 0:
        for row in range(0, len(level)):
            for col in range(0, len(level[row])):
                if level[row][col] == 'f':
                    level[row-1] = level[row-1][:col] + "F" + level[row][col+1:]

    #desenho
    for x in range(0, screen_size[0]//bg_size+2):
        for y in range(0, screen_size[1]//bg_size+2):
            screen.blit(bg, (x*bg_size ,y*bg_size))

    flower_cont = 0
    for row in range(0, len(level)):
        for col in range(0, len(level[row])):
            if level[row][col] == 'l':
                screen.blit(leaf, (col*grid, row*grid))
            elif level[row][col] == 'F':
                flower_cont += 1
                screen.blit(flower, (col*grid, row*grid))
            elif level[row][col] == 'X':
                screen.blit(spikes, (col*grid, row*grid))


    screen.blit(bee[state], (bee_x, bee_y))

#    screen.blit(bee_mask, (screen_size[0]-64, screen_size[1]-96))
#    screen.blit(bee_rest, (screen_size[0]-64, screen_size[1]-96))
    screen.blit(relogio, (screen_size[0]/2-16, screen_size[1]-64))
    screen.blit(hive, (screen_size[0]/2-16, 32))


    pg.display.flip()

pg.quit()

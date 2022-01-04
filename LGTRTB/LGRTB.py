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

#fonte
fonte = pg.font.Font("pricedow.ttf", 40)

#nível
level = [
    "XxxxXxxxXxxxXxxxXxxxXxxxX",
    "0000000000000000000000000",
    "0000000000000000000000000",
    "0000000000000000000F00000",
    "0000000000000000leaf00000",
    "0000000000000000000000000",
    "00000000FF000000000000000",
    "00000lleaf000000000000000",
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
bee_start_level = (300, 100)

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

#contador de vidas
bee_lives = pg.image.load("Sprites/bee_rest.png")
bee_lives.set_colorkey((255,0,255))
bee_lives.set_alpha(128)
bee_mask = pg.image.load("Sprites/bee_mask.png")
bee_mask.set_colorkey((0, 0, 0))
bee_mask.set_alpha(128)

#contador flores
flower_counter = pg.image.load("Sprites/flower.png")
flower_counter.set_colorkey((255,0,255))
flower_counter.set_alpha(128)
flower_mask = pg.image.load("Sprites/flower_mask.png")
flower_mask.set_colorkey((0, 0, 0))
flower_mask.set_alpha(128)

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
bee_state = 0

alive = True
res = 0
res_time = 500

#inic. vars HUD
flower_count_raw = 1337
score_raw = 00
time_raw = 120 #segundos
lives_raw = 3

left_key = right_key = up_key = False
in_leaf = False
clock = pg.time.Clock()

#contagem tempo
pg.time.set_timer(pg.USEREVENT, 1000, 9999999)

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
        if ev == pg.USEREVENT:
            time_raw -= 1

    #leis

    dt = clock.tick()
    if alive:
        if up_key:
            bee_vy = -0.3
            bee_state = (bee_state+1)%(2*k)
            in_leaf = False
        elif not in_leaf:
            bee_vy = 0.3
            bee_state = 0

        if left_key:
            bee_vx = -0.3
        elif right_key:
            bee_vx = 0.3
        else:
            bee_vx = 0.0

    bee_oldx = bee_x
    bee_oldy = bee_y
    bee_x += bee_vx*dt
    bee_y += bee_vy*dt

    if bee_x < 0: #limites verticais do ecrã
        bee_x = 0
    elif bee_x > screen_size[0]-bee_size:
        bee_x = screen_size[0]-bee_size

    #interações
    for row in range(0, len(level)):
        for col in range(0, len(level[row])):
            #colisão folhas
            if level[row][col] in 'leaf' and alive:
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
                else:
                    in_leaf = False
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
                if col*grid-bee_size < bee_x < (col+1)*grid and row*grid-bee_size < bee_y < row*grid and alive:
                    level[row] = level[row][:col] + "C" + level[row][col+1:]
                    score_raw += 20

            #espinhos
            if level[row][col] in "Xx":
                if col*grid-bee_size < bee_x < (col+1)*grid and row*grid-bee_size < bee_y < (row+1)*grid:
                    bee_vy = -0.01
                    alive = False


    #sequencia de respawn
    if not alive:
        if res < res_time:
            bee_vx = 0.05*math.sin(pg.time.get_ticks()/200)
            bee_state = 2*k
            res +=1
        else:
            alive = True
            lives_raw -= 1
            time_raw = 120
            bee_x, bee_y = bee_start_level
            bee_state = 0
            res = 0

    #game over por vidas
    if lives_raw == 0:
        running = False

    #morte por tempo
    if time_raw == 0:
        alive = False

    #reset do nivel (temporário)
    if flower_count_raw == 0:
        for row in range(0, len(level)):
            for col in range(0, len(level[row])):
                if level[row][col] == 'C':
                    level[row] = level[row][:col] + "F" + level[row][col+1:]

    #desvio texto pontuação
    score_x_var = 0
    for i in range(0,len(str(score_raw))):
        score_x_var += 5

#desenho

    #papel de fundo
    for x in range(0, screen_size[0]//bg_size+2):
        for y in range(0, screen_size[1]//bg_size+2):
            screen.blit(bg, (x*bg_size ,y*bg_size))

    #criador de nível (c/ contador de flores restantes)
    flower_count_raw = 0
    for row in range(0, len(level)):
        for col in range(0, len(level[row])):
            if level[row][col] == 'l':
                screen.blit(leaf, (col*grid, row*grid))
            elif level[row][col] == 'F':
                flower_count_raw += 1
                screen.blit(flower, (col*grid, row*grid))
            elif level[row][col] == 'X':
                screen.blit(spikes, (col*grid, row*grid))

    #texto
    flower_count = pg.font.Font.render(fonte, str(flower_count_raw), True, (255, 194, 0))
    lives = pg.font.Font.render(fonte, str(lives_raw), True, (255, 194, 0))
    time = pg.font.Font.render(fonte, str(time_raw), True, (255, 194, 0))
    score = pg.font.Font.render(fonte, str(score_raw), True, (255, 194, 0))

    #abelha :D
    screen.blit(bee[bee_state], (bee_x, bee_y))

    #HUD
    screen.blit(bee_mask, (screen_size[0]-96, screen_size[1]-80))
    screen.blit(bee_lives, (screen_size[0]-96, screen_size[1]-80))
    screen.blit(lives, (screen_size[0]-72, screen_size[1]-55))

    screen.blit(flower_mask, (32, screen_size[1]-64))
    screen.blit(flower_counter, (32, screen_size[1]-64))
    screen.blit(flower_count, (40, screen_size[1]-55))

    screen.blit(relogio, (screen_size[0]/2-16, screen_size[1]-64))
    screen.blit(time, (screen_size[0]/2-16, screen_size[1]-55))

    screen.blit(hive, (screen_size[0]/2-16, 32))
    screen.blit(score, (screen_size[0]/2-3-score_x_var, 40))


    pg.display.flip()

pg.quit()

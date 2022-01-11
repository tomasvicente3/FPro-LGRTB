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
screen_size = (1280, 720)
screen = pg.display.set_mode(screen_size)
pg.display.set_caption("Let's Get Ready To Bumble")
pot = pg.image.load("Sprites/pot.png")
pot.set_colorkey((255,0,255))
pg.display.set_icon(pot)
grid = 32

#fonte
fonte = pg.font.Font("pricedow.ttf", 40)

#níveis
#1
level_layouts = [[
    "XxxxXxxxXxxxXxxxXxxxXxxxXxxxXxxxXxxxXxxx",
    "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "0000000000000000000000000000000000000000",
    "0000000000000000000F00000000000000000000",
    "0000000000000000leaf00000000000000000000",
    "0000000000000000000000000000000000000000",
    "00000000FF000000000000000000000000000000",
    "00000lleaf000000000000000000000000000000",
    "0000000000000000000000000000000000000000",
    "0000000000000000000000000000000000000000",
    "0000000000000000000000000000000000000000",
    "0000000000000000000000000000000000000000",
    "0000000000000000000000000000000000000000",
    "0000000000000000000000000000000000000000",
    "0000000000000000000000000000000000000000",
    "00000000000000Xxxx0000000000000000000000",
    "00000000000000xxxx0000000000000000000000",
    "000000F000000000000000000000000000000000",
    "000leaf0000000F0000000000000000000000000",
    "00000000000leaf000000F000000000000000000",
    "000000000000000000leaf000000000000000000",
    "XxxxXxxxXxxxXxxxXxxxXxxxXxxxXxxxXxxxXxxx",
    "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ],
    "XxxxXxxxXxxxXxxxXxxxXxxxXxxxXxxxXxxxXxxx",
    "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "0000000000000000000000000000000000000000",
    "0000000000000000000F00000000000000000000",
    "0000000000000000leaf00000000000000000000",
    "0000000000000000000000000000000000000000",
    "00000000FF000000000000000000000000000000",
    "00000lleaf000000000000000000000000000000",
    "0000000000000000000000000000000000000000",
    "000000000000000000000000Xxxx000000000000",
    "000000000000000000000000xxxx000000000000",
    "0000000000000000000000000000000000000000",
    "0000000000000000000000000000000000000000",
    "0000000000000000000000000000000000000000",
    "0000000000000000000000000000000000000000",
    "00000000000000Xxxx0000000000000000000000",
    "00000000000000xxxx0000000000000000000000",
    "000000F000000000000000000000000000000000",
    "000leaf0000000F0000000000000000000000000",
    "00000000000leaf000000F000000000000000000",
    "000000000000000000leaf000000000000000000",
    "XxxxXxxxXxxxXxxxXxxxXxxxXxxxXxxxXxxxXxxx",
    "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ]
bee_start_levels = [(90, 510), (140, 158)]
time_levels = [120,90]

level = 1
level_layout = level_layouts[level-1]
bee_start_level = bee_start_levels[level-1]
time_level = time_levels[level-1]

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
bee_lives = pg.image.load("Sprites/bee_HUD.png")
bee_lives.set_colorkey((255,0,255))
bee_lives.set_alpha(128)

#contador flores
flower_counter = pg.image.load("Sprites/flower_HUD.png")
flower_counter.set_colorkey((255,0,255))
flower_counter.set_alpha(128)


#relógio
relogio = pg.image.load("Sprites/clock.png")
relogio.set_colorkey((255,0,255))
relogio.set_alpha(128)

#colmeia (pontuação)
hive = pg.image.load("Sprites/hive.png")
hive.set_colorkey((255,0,255))
hive.set_alpha(128)


bee_angle = 0
bee_x = bee_start_level[0]
bee_y = bee_start_level[1]

bee_vx = 0
bee_vy = 0

k = 3
bee = [bee_rest]*k + [bee_fly]*k + [bee_ghost]
bee_state = 0

alive = True
res = 0
res_time = 100

#inic. vars HUD
flower_count = 1337
score = 00
score_temp = 0
lives = 3
time = time_level+1 #segundos
time_var = 0

left_key = right_key = up_key = False
in_leaf = False
clock = pg.time.Clock()

#contagem tempo
pg.time.set_timer(pg.USEREVENT, 1000)

#reset level

def reset_level():
    for row in range(0, len(level_layout)):
        for col in range(0, len(level_layout[row])):
            if level_layout[row][col] == 'C':
                level_layout[row] = level_layout[row][:col] + "F" + level_layout[row][col+1:]

#outline texto
_circle_cache = {}

def _circlepoints(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points

def render(text, font, gfcolor=(255, 194, 0), ocolor=(0, 0, 0), opx=1):
    textsurface = font.render(text, True, gfcolor).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height()

    osurf = pg.Surface((w, h + 2 * opx)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

    for dx, dy in _circlepoints(opx):
        surf.blit(osurf, (dx + opx, dy + opx))

    surf.blit(textsurface, (opx, opx))
    return surf

#rotação
def rot_center(image, angle, x=bee_x, y=bee_y):

    rotated_image = pg.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    return rotated_image, new_rect

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
            time -= 1

    #leis

    dt = clock.tick()

    level_layout = level_layouts[level-1]
    bee_start_level = bee_start_levels[level-1]
    time_level = time_levels[level-1]

    if alive:
        if up_key:
            bee_vy = -0.2
            bee_state = (bee_state+1)%(2*k)
            in_leaf = False
        elif not in_leaf:
            bee_vy = 0.2
            bee_state = 0

        if left_key:
            bee_vx = -0.2
            if bee_angle < 25:
                bee_angle += 2
        elif right_key:
            bee_vx = 0.2
            if bee_angle > -25:
                bee_angle -= 2
        else:
            bee_vx = 0.0
            if bee_angle < 0:
                bee_angle += 1
            elif bee_angle > 0:
                bee_angle -= 1

    bee_oldx = bee_x
    bee_oldy = bee_y
    bee_x += bee_vx*dt
    bee_y += bee_vy*dt

    if bee_x < 0: #limites verticais do ecrã
        bee_x = 0
    elif bee_x > screen_size[0]-bee_size:
        bee_x = screen_size[0]-bee_size


    #interações
    for row in range(0, len(level_layout)):
        for col in range(0, len(level_layout[row])):
            #colisão folhas
            if level_layout[row][col] in 'leaf' and alive:
                if bee_x + bee_size >= col * grid and bee_x <= (col+1) * grid:
                    #limite superior
                    if bee_y + bee_size >= row * grid and bee_oldy < row * grid and bee_vy >= 0:
                        in_leaf = True
                        bee_vy = 0
                        bee_y = row * grid - bee_size
                    #limite inferior
                    elif bee_y < (row+1) * grid and bee_oldy >= (row+1) * grid and bee_vy < 0:
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
            if level_layout[row][col] == 'F':
                if col*grid-bee_size < bee_x < (col+1)*grid and row*grid-bee_size < bee_y < row*grid and alive:
                    level_layout[row] = level_layout[row][:col] + "C" + level_layout[row][col+1:]
                    score_temp += 20

            #espinhos
            if level_layout[row][col] in "Xx":
                if col*grid-bee_size < bee_x < (col+1)*grid and row*grid-bee_size < bee_y < (row+1)*grid:
                    bee_vy = -0.01
                    alive = False

    #correção inclinação na folha
#    if -0.001 < bee_vy < 0.001:
#        bee_y = bee_y - abs(10*math.sin(bee_angle*math.pi/180))

    #sequencia de respawn
    if not alive:
        if res < res_time:
            if bee_angle < -3:
                bee_angle += 3
            elif bee_angle < 0:
                bee_angle += 1
            elif bee_angle > 3:
                bee_angle -= 3
            elif bee_angle > 0:
                bee_angle -= 1
            bee_vx = 0.05*math.sin(pg.time.get_ticks()/200)
            bee_state = 2*k
            res +=1
        else:
            alive = True
            reset_level()
            lives -= 1
            score_temp = 0
            time = time_level
            bee_x, bee_y = bee_start_level
            bee_state = 0
            res = 0

    #game over por vidas
    if lives == 0:
        running = False

    #var tempo
    if alive:
        time -= dt/1000

    #morte por tempo
    if time < 0:
        bee_vy = -0.01
        alive = False

    #reset do nivel (temporário)
    if flower_count == 0:
        score = score + score_temp + int(time)
        score_temp = 0
        level = (level +1)%2
        reset_level()

    #desvio texto pontuação
    score_x_var = 0
    for i in range(0,len(str(score))):
        score_x_var += 8
    time_x_var = 24
    for i in range(0,len(str(time))):
        time_x_var -= 8

#desenho

    #papel de fundo
    for x in range(0, screen_size[0]//bg_size+2):
        for y in range(0, screen_size[1]//bg_size+2):
            screen.blit(bg, (x*bg_size ,y*bg_size))

    #criador de nível (c/ contador de flores restantes)
    flower_count = 0
    for row in range(0, len(level_layout)):
        for col in range(0, len(level_layout[row])):
            if level_layout[row][col] == 'l':
                screen.blit(leaf, (col*grid, row*grid))
            elif level_layout[row][col] == 'F':
                flower_count += 1
                screen.blit(flower, (col*grid, row*grid))
            elif level_layout[row][col] == 'X':
                screen.blit(spikes, (col*grid, row*grid))

    #abelha :D
    bee_rot = rot_center(bee[bee_state], bee_angle)[0]
    bee_rot.set_colorkey((255, 0, 255))
    screen.blit(bee_rot, (bee_x, bee_y))

    #HUD
    screen.blit(bee_lives, (screen_size[0]-97, screen_size[1]-80))
    screen.blit(render(str(lives), fonte), (screen_size[0]-74, screen_size[1]-55))

    screen.blit(flower_counter, (32, screen_size[1]-64))
    screen.blit(render(str(flower_count), fonte), (40, screen_size[1]-55))

    screen.blit(relogio, (screen_size[0]/2-16, screen_size[1]-64))
    screen.blit(render(str(int(time)), fonte), (screen_size[0]/2-16, screen_size[1]-55))

    screen.blit(hive, (screen_size[0]/2-16, 32))
    screen.blit(render(str(score+score_temp), fonte), (screen_size[0]/2-score_x_var, 40))

    print(in_leaf, bee_x, bee_y)
    pg.display.flip()

pg.quit()

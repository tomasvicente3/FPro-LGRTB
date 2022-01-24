#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 11:10:19 2021

@author: up202108717
"""

import pygame as pg
import math
import json
from operator import itemgetter

pg.init()

#ecrã
screen_size = (1280, 720)
screen = pg.display.set_mode(screen_size)
pg.display.set_caption("Let's Get Ready To Bumble")
pot = pg.image.load("Sprites/pot.png")
pot.set_colorkey((255,0,255))
pg.display.set_icon(pot)
grid = 32
menu = "main_menu"

#fonte
fonte = pg.font.Font("pricedow.ttf", 40)

#níveis
level_layouts = [[
    "XxxxXxxxXxxxXxxxXxxxXxxxXxxxXxxxXxxxXxxx",
    "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "0000000000000000000000000000000000000000",
    "0000000000000000000000000000000000000000",
    "0000000Xxxx000000000000000000000F0000000",
    "0000000xxxx000000000000000000leaf0000000",
    "0000000000000000000000000000000000000000",
    "0000000000000000000000000000000000000000",
    "0000000000000000000000000000000000000000",
    "0000000000000000000000F00000000000000000",
    "0000000000000000000leaf00000000000000000",
    "0000000000000000000000000000000000000000",
    "00000000000000F0000000000000000000000000",
    "00000000000leaf0000000000000000000000000",
    "00000000000000Xxxx0000000XxxxXxxx0000000",
    "00000000000000xxxx0000000xxxxxxxx0000000",
    "0000000000000000000000000XxxxXxxx0000000",
    "000000F000000000000000000xxxxxxxx0000000",
    "000leaf000000000000000000000000000000000",
    "0000000000000000000000000000000000000000",
    "0000000000000000000000000000000000000000",
    "XxxxXxxxXxxxXxxxXxxxXxxxXxxxXxxxXxxxXxxx",
    "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ],
    [
    "XxxxXxxxXxxxXxxxXxxxXxxxXxxxXxxxXxxxXxxx",
    "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "0000000000000000000000000000000000000000",
    "0000000000000000000000000000000000000000",
    "0000000000000000000F00000000000000000000",
    "0000000000000000leaf00000000000000000000",
    "00000000FF000000000000000000000000000000",
    "00000lleaf000000000000000000000000000000",
    "0000000000000000000000000000000000000000",
    "000000000000000000000000Xxxx000000000000",
    "000000000000000000000000xxxx000000000000",
    "0000000000000000000000000000000000000000",
    "0000000000000000000000000000000000000000",
    "00000000000000000000000000000000000F0000",
    "00000000000000000000000000000000leaf0000",
    "00000000000000Xxxx0000000000000000000000",
    "00000000000000xxxx0000000000000000000000",
    "000000F000000000000000000000000000000000",
    "000leaf0000000F0000000000000000000000000",
    "00000000000leaf000000F000000000000000000",
    "000000000000000000leaf000000000000000000",
    "XxxxXxxxXxxxXxxxXxxxXxxxXxxxXxxxXxxxXxxx",
    "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ],
    [
     "XxxxXxxxXxxxXxxxXxxxXxxxXxxxXxxxXxxxXxxx",
     "xxxxxxxxxxxxxxxxxxxxxXxxxxxxxxxxxxxxxxxx",
     "000000000000000000000xxxx000000000000000",
     "0000000000000000000000000000000000000000",
     "0000000000000000000000000000000000000000",
     "0000F000000000000000000000000000F0FF0000",
     "0leaf000000000000000000000000lelleaf0000",
     "0000000000000000000000000000000000000000",
     "0000000000000000XxxxXxxxXxxxXxxxXxxxXxxx",
     "0000000000000000xxxxxxxxxxxxxxxxxxxxxxxx",
     "0000000000000000000000000000000000000000",
     "0000000000000000000000000000000000000000",
     "0000000000000000000000000000000000000000",
     "XxxxXxxxXxxx0000000000000000000000000000",
     "xxxxxxxxxxXxxxXxxx000000000000000000F000",
     "0000000000xxxxxxXxxxXxxx000000000leaf000",
     "0000000000000000xxxxxxxx0000000000000000",
     "000000F000000000000000000000000000000000",
     "000leaf000000000000000000000000000000000",
     "0000000000000000000000000000000000000000",
     "0000000000000000000000000000000000000000",
     "XxxxXxxxXxxxXxxxXxxxXxxxXxxxXxxxXxxxXxxx",
     "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
     ]]
bee_start_levels = [(90, 510), (1056, 384), (90, 510)]
time_levels = [120,90,150]

level = 1
level_layout = level_layouts[level-1]
bee_start_level = bee_start_levels[level-1]
time_level = time_levels[level-1]

#title_screen
title_screen = pg.transform.scale2x(pg.image.load("Sprites/title_screen.png"))

#botões
play_sel = pg.transform.scale2x(pg.image.load("Sprites/play_sel.png"))
play_sel.set_colorkey((255,0,255))
play_un = pg.transform.scale2x(pg.image.load("Sprites/play_un.png"))
play_un.set_colorkey((255,0,255))
hs_sel = pg.transform.scale2x(pg.image.load("Sprites/hs_sel.png"))
hs_sel.set_colorkey((255,0,255))
hs_un = pg.transform.scale2x(pg.image.load("Sprites/hs_un.png"))
hs_un.set_colorkey((255,0,255))
exit_sel = pg.transform.scale2x(pg.image.load("Sprites/exit_sel.png"))
exit_sel.set_colorkey((255,0,255))
exit_un = pg.transform.scale2x(pg.image.load("Sprites/exit_un.png"))
exit_un.set_colorkey((255,0,255))

menu_buttons = [(play_sel, hs_un, exit_un),(play_un, hs_sel, exit_un),(play_un, hs_un, exit_sel)]
menu_button = 0

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

q = 30
color = [(255,194,0)]*q + [(255, 255, 255)]*q
color_num = 0

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

left_key = right_key = up_key = down_key = enter_key = escape_key = False
in_leaf = Freeze = False
clock = pg.time.Clock()

#contagem tempo
pg.time.set_timer(pg.USEREVENT, 1000)

#reset level
def reset_level():
    for row in range(0, len(level_layout)):
        for col in range(0, len(level_layout[row])):
            if level_layout[row][col] == 'C':
                level_layout[row] = level_layout[row][:col] + "F" + level_layout[row][col+1:]

def next_level(level, font=fonte, screen_size=screen_size, screen=screen):
    pg.Surface.fill(screen, (0,0,0))
    screen.blit(render("Level "+str(int(level)), fonte), (screen_size[0]/2-55, screen_size[1]/2))
    pg.display.update()
    pg.time.wait(2000)

#game over
def game_over(xs):
    pg.Surface.fill(screen, (0,0,0))
    screen.blit(pg.transform.scale2x(render(xs, fonte)), (screen_size[0]/2-170, screen_size[1]/2-64))
    pg.display.update()
    pg.time.wait(2500)

#escape sair
def escape():
    global menu
    global running
    if menu == "main_menu":
        running = False
    else:
        menu = "main_menu"

#guardar highscores
def save_hs(highscores):
    with open('highscores.json', 'w') as file:
        json.dump(highscores, file)  # Write the list to the json file.

#carregar highscores
def load_hs():
    try:
        with open('highscores.json', 'r') as file:
            highscores = json.load(file)  # Read the json file.
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist.
    # Sorted by the score.
    return highscores

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
                escape_key = True
            elif ev.key == pg.K_LEFT or ev.key == pg.K_a:
                left_key = True
            elif ev.key == pg.K_RIGHT or ev.key == pg.K_d:
                right_key = True
            elif ev.key == pg.K_UP or ev.key == pg.K_w:
                up_key = True
            elif ev.key == pg.K_DOWN or ev.key == pg.K_s:
                down_key = True
            elif ev.key == pg.K_RETURN:
                enter_key = True
        elif ev.type == pg.KEYUP:
            if ev.key == pg.K_LEFT or ev.key == pg.K_a:
                left_key = False
            elif ev.key == pg.K_RIGHT or ev.key == pg.K_d:
                right_key = False
            elif ev.key == pg.K_UP or ev.key == pg.K_w:
                up_key = False
            elif ev.key == pg.K_DOWN or ev.key == pg.K_s:
                down_key = False
            elif ev.key == pg.K_RETURN:
                enter_key = False
        if ev == pg.USEREVENT:
            time -= 1

    #leis

    dt = clock.tick()
    if escape_key:
        escape_key = False
        escape()

    if menu == "main_menu":
        if enter_key:
            if menu_button == 0:
                level = 1
                score = 0
                score_temp = 0
                level_layout = level_layouts[level-1]
                bee_start_level = bee_start_levels[level-1]
                bee_x, bee_y = bee_start_level
                time_level = time_levels[level-1]
                time = time_level + 3
                lives = 3
                menu = "game"
                freeze = True
                reset_level()
                next_level(level)
                freeze = False
            elif menu_button == 1:
                enter_key = False
                menu = "highscore"
                pg.Surface.fill(screen, (0,0,0))
                pg.display.update()
                pg.time.wait(100)
            elif menu_button == 2:
                running  = False
        elif up_key:
            menu_button = (menu_button - 1) % 3
            up_key = False
        elif down_key:
            menu_button = (menu_button + 1) % 3
            down_key = False

    if menu == "highscore" or menu == "game_over":
        if enter_key:
            menu = "main_menu"
            pg.Surface.fill(screen, (0,0,0))
            pg.display.update()
            pg.time.wait(100)
        sorted_hs = sorted(load_hs().items(), key=itemgetter(1), reverse=True)

    if menu == "game":
        if alive and not freeze:
            if up_key:
                bee_vy = -0.15
                bee_state = (bee_state+1)%(2*k)
                in_leaf = False
            elif not in_leaf:
                bee_vy = 0.15
                bee_state = 0

            if left_key:
                bee_vx = -0.15
                if bee_angle < 24:
                    bee_angle += 3
            elif right_key:
                bee_vx = 0.15
                if bee_angle > -24:
                    bee_angle -= 3
            else:
                bee_vx = 0.0
                if bee_angle < -3:
                    bee_angle += 3
                elif bee_angle < 0:
                    bee_angle += 1
                elif bee_angle > 3:
                    bee_angle -= 3
                elif bee_angle > 0:
                    bee_angle -= 1

        bee_oldx = bee_x
        bee_oldy = bee_y
        bee_x += bee_vx*dt
        bee_y += bee_vy*dt

        if bee_x < 0:
            bee_x = 0
        elif bee_x + 64 > screen_size[0]:
            bee_x = screen_size[0] - 64

        #interações
        in_leaf = False
        for row in range(0, len(level_layout)):
            for col in range(0, len(level_layout[row])):
                #colisão folhas
                if level_layout[row][col] in 'leaf' and alive:
                    if bee_x + bee_size > col * grid and bee_x < (col+1) * grid:
                        #limite superior
                        if bee_y + bee_size >= row * grid and bee_oldy < row * grid and bee_vy >= 0:
                            in_leaf = True
                            bee_vy = 0
                            bee_y = row * grid - bee_size
                        #limite inferior
                        elif bee_y < (row+1) * grid and bee_oldy >= (row+1) * grid and bee_vy < 0:
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
                if level_layout[row][col] == 'F':
                    if col*grid-bee_size < bee_x < (col+1)*grid and row*grid-bee_size < bee_y < row*grid and alive:
                        level_layout[row] = level_layout[row][:col] + "C" + level_layout[row][col+1:]
                        score_temp += 20
                #espinhos
                if level_layout[row][col] in "Xx":
                    if col*grid-bee_size < bee_x < (col+1)*grid and row*grid-bee_size < bee_y < (row+1)*grid:
                        bee_vy = -0.01
                        alive = False


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
                time = time_level + 3
                bee_x, bee_y = bee_start_level
                bee_state = 0
                res = 0

        #game over por vidas
        if lives == 0:
            dict_hs = load_hs()
            if dict_hs.get("You", 0) <= score:
                dict_hs["You"] = score
                save_hs(dict_hs)
            game_over("Game Over")
            menu = "game_over"

        #var tempo
        if alive:
            time -= dt/1000

        #morte por tempo
        if time < 0:
            bee_vy = -0.01
            alive = False

        #avançar de nível
        if flower_count == 0:
            score = score + score_temp + 2*int(time)
            score_temp = 0
            level = (level + 1)
            if level <= len(level_layouts):
                level_layout = level_layouts[level-1]
                bee_start_level = bee_start_levels[level-1]
                bee_x, bee_y = bee_start_level
                time_level = time_levels[level-1]
                time = time_level + 4
                freeze = True
                next_level(level)
                reset_level()
                freeze = False
            else:
                score += 50*lives
                dict_hs = load_hs()
                if dict_hs.get("You", 0) < score:
                    dict_hs["You"] = score
                    save_hs(dict_hs)
                game_over("Great Job!")
                menu = "game_over"

        #desvio texto pontuação
        if len(str(score)) == 1:
            score_x_var = 9
        elif len(str(score)) == 2:
            score_x_var = 32
        else:
            score_x_var = 24


#desenho

    #papel de fundo
    for x in range(0, screen_size[0]//bg_size+2):
        for y in range(0, screen_size[1]//bg_size+2):
            screen.blit(bg, (x*bg_size ,y*bg_size))

    if menu == "game":
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

        #abelha
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

    elif menu == "main_menu":
        screen.blit(title_screen, (screen_size[0]/2-256,screen_size[1]-640))
        screen.blit(menu_buttons[menu_button][0], (screen_size[0]/2-122, screen_size[1]/2+64))
        screen.blit(menu_buttons[menu_button][1], (screen_size[0]/2-128, screen_size[1]/2+128))
        screen.blit(menu_buttons[menu_button][2], (screen_size[0]/2-128, screen_size[1]/2+192))

    elif menu == "game_over":
        sorted_hs = sorted(load_hs().items(), key=itemgetter(1), reverse=True)
        screen.blit(pg.transform.scale2x(render("Highscore", fonte)), (screen_size[0]/2-160, 64))
        screen.blit(exit_sel, (screen_size[0]-128, screen_size[1]-64))
        for i in range(10):
            if sorted_hs[i][0] == "You":
                color_num = (color_num + 1) % (2*q)
                screen.blit(render(str(sorted_hs[i][0]), fonte, color[color_num]), (180, 224+32*i))
                screen.blit(render(str(sorted_hs[i][1]), fonte, color[color_num]), (screen_size[0]-256, 224+32*i))
            else:
                screen.blit(render(str(sorted_hs[i][0]), fonte, (255, 255, 255)), (180, 224+32*i))
                screen.blit(render(str(sorted_hs[i][1]), fonte, (255, 255, 255)), (screen_size[0]-256, 224+32*i))

    elif menu == "highscore": #highscore
        screen.blit(pg.transform.scale2x(render("Highscore", fonte)), (screen_size[0]/2-160, 64))
        screen.blit(exit_sel, (screen_size[0]-128, screen_size[1]-64))
        for i in range(10):
            try:
                screen.blit(render(str(sorted_hs[i][0]), fonte, (255, 255, 255)), (180, 224+32*i))
                screen.blit(render(str(sorted_hs[i][1]), fonte, (255, 255, 255)), (screen_size[0]-256, 224+32*i))
            except IndexError:
                break

    pg.display.flip()
pg.quit()

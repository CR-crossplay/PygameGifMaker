#by CR-crossplay

import pygame
from pygame.locals import *
from PIL import Image
import json
import time
from random import randint
pygame.init()
def read_data(url):
    with open(url,"r",encoding='utf-8') as f: return f.readlines()

conf={e.split(":",1)[0]:e.split(":",1)[1] for e in read_data("conf.ini")}
#w_x=int(input("Largeur d'écran ? :"))
#w_y=int(input("Longueur d'écran ? :"))
w_x=512
w_y=512
window=pygame.display.set_mode((w_x,w_y))
pygame.key.set_repeat(3,1) #smooth les controles
main_loop=True
bg_color=(100,100,100)
pos_x=0
pos_y=0
coord=[0,0]
tileMapSize=int(conf["tileMapSize"])
colors=str(conf["Colors"])
colorsList=[(int(color.split(",")[0]),int(color.split(",")[1]),int(color.split(",")[2])) for color in colors.split(";")]
colorAct=0
img_act=1
img_max=int(conf["frames"])
margin=10
keyDelay=int(conf["keyDelay"])
Curseur = pygame.Rect(margin + tileMapSize * 2.5+tileMapSize*10/32, margin*2,tileMapSize*10/32,tileMapSize*10/32)
pygame.display.set_caption("TileGifEditor")
font = pygame.font.Font('Roboto-Regular.ttf', 32)
margin=10
tiles=[[[(0,0,0) for k in range(tileMapSize)] for i in range(tileMapSize)] for e in range(img_max)]
starttime = pygame.time.get_ticks()
inputEnable=True
while main_loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == KEYDOWN and inputEnable:
            if event.key == K_RIGHT and pygame.time.get_ticks()-starttime>keyDelay:
                if coord[0]<31:
                    coord[0]+=1
                    starttime = pygame.time.get_ticks()
                else:
                    coord[0]=0
                    starttime = pygame.time.get_ticks()
            elif event.key == K_LEFT and pygame.time.get_ticks()-starttime>keyDelay:
                if coord[0]>0:
                    coord[0]-=1
                    starttime = pygame.time.get_ticks()
                else:
                    coord[0]=31
                    starttime = pygame.time.get_ticks()
            elif event.key == K_UP and pygame.time.get_ticks()-starttime>keyDelay:
                if coord[1]>0:
                    coord[1]-=1
                    starttime = pygame.time.get_ticks()
                else:
                    coord[1]=31
                    starttime = pygame.time.get_ticks()
            elif event.key == K_DOWN and pygame.time.get_ticks()-starttime>keyDelay:
                if coord[1]<31:
                    coord[1]+=1
                    starttime = pygame.time.get_ticks()
                else:
                    coord[1]=0
                    starttime = pygame.time.get_ticks()
            elif event.key== K_a and pygame.time.get_ticks()-starttime>keyDelay:
                if colorAct>0:colorAct-=1
                else:colorAct=len(colorsList)-1
                starttime=pygame.time.get_ticks()
            elif event.key==K_d and pygame.time.get_ticks()-starttime>keyDelay:
                if colorAct<len(colorsList)-1:colorAct+=1
                else:colorAct=0
                starttime = pygame.time.get_ticks()
            elif event.key==K_z and pygame.time.get_ticks()-starttime>keyDelay:
                if img_act<img_max:img_act+=1
                else:img_act=1
                starttime = pygame.time.get_ticks()
            elif event.key==K_x and pygame.time.get_ticks()-starttime>keyDelay:
                if img_act>1:img_act-=1
                else:img_act=img_max
                starttime = pygame.time.get_ticks()
            elif event.key==K_SPACE and pygame.time.get_ticks()-starttime>keyDelay:
                tiles[img_act-1][coord[0]][coord[1]]=colorsList[colorAct]
                starttime = pygame.time.get_ticks()
            elif event.key == K_e and pygame.time.get_ticks() - starttime > keyDelay:
                images=[]
                for e in range(img_max):
                    im = Image.new(mode="RGB", size=(len(tiles[e]), len(tiles[e][0])))
                    x = 0
                    y = 0
                    print(e)
                    for k in range(tileMapSize * tileMapSize - 1):
                        if k > len(tiles[e]) - 1:
                            y += 1
                            x = 0
                            if y > 31: break
                        im.putpixel((x, y), tiles[e][x][y])
                        x += 1
                    images.append(im)
                images[0].save("gifmaker.gif",
                               save_all=True, append_images=images[1:], optimize=False, duration=40, loop=0)
                starttime = pygame.time.get_ticks()

    info = font.render(f" {img_act} / {img_max} ", True, (255, 255, 255), (120,120,120))
    save = font.render("Save .gif", True, (255, 255, 255), (120, 120, 120))
    infoRect=info.get_rect()
    saveRect=save.get_rect()
    saveRect.center=(w_x-save.get_width()/2,w_y-save.get_height()/2)
    infoRect.center=(w_x/2,w_y-info.get_height()/2)
    btnNextFrame = pygame.Rect(w_x/2+info.get_width()/2+margin, w_y-info.get_height()/2-info.get_height()/2, tileMapSize, info.get_height())
    btnPastFrame = pygame.Rect(w_x/2-info.get_width(), w_y-info.get_height()/2-info.get_height()/2, tileMapSize, info.get_height())
    btnNextColor = pygame.Rect(w_x / 2 + info.get_width() / 2 + margin,
                               w_y - info.get_height() / 2 - info.get_height() / 2, tileMapSize, info.get_height())

    window.fill(bg_color)
    window.blit(info,infoRect)
    window.blit(save, saveRect)
    pygame.draw.rect(window,(80,80,80),btnNextFrame)
    pygame.draw.rect(window, (80, 80, 80), btnPastFrame)

    #Affichage du cadre
    topBorder=pygame.Rect(margin+tileMapSize*2.5,margin,tileMapSize*10+tileMapSize*20/32,margin)
    leftBorder=pygame.Rect(margin+tileMapSize*2.5,margin*2,margin,tileMapSize*10)
    bottomBorder = pygame.Rect(margin + tileMapSize * 2.5, tileMapSize*10+tileMapSize*20/32, tileMapSize * 10++tileMapSize*20/32, margin)
    rightBorder=pygame.Rect(margin*2+tileMapSize*2.5+tileMapSize*10,margin*2,margin,tileMapSize*10)
    pygame.draw.rect(window, (50, 50, 50), topBorder)
    pygame.draw.rect(window, (50, 50, 50), leftBorder)
    pygame.draw.rect(window, (50, 50, 50), bottomBorder)
    pygame.draw.rect(window, (50, 50, 50), rightBorder)
    for i in range(tileMapSize):
        for k in range(tileMapSize):
            tile = pygame.Rect((margin + tileMapSize * 2.5 + tileMapSize * 10 / 32) + i * (tileMapSize * 10 / 32),
                               margin * 2+tileMapSize * (k*10) / 32, tileMapSize * 10 / 32, tileMapSize * 10 / 32)
            pygame.draw.rect(window, tiles[img_act-1][i][k], tile)
            pass
    Curseur.center=(Curseur.width/2+margin+tileMapSize*2.5+tileMapSize*((coord[0]+1)*10)/32,Curseur.height/2+margin+tileMapSize*((coord[1]+1)*10)/32)
    pygame.draw.rect(window,colorsList[colorAct],Curseur)
    pygame.display.flip()
    pygame.display.update()
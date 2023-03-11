# from curses import KEY_SPREVIOUS
# import re
# from termios import VWERASE
from imp import PY_CODERESOURCE
from symbol import power
from tkinter import Y
from turtle import home
import pygame
import os
import random
pygame.font.init() #starts text/font aspect of pygame to dispaly texts
pygame.mixer.init() #starts the sounds aspec tof pygame to use sounds

run_homescreen=True

WIDTH,HEIGHT=(1000,500)
WIN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Neck Twisters")

WHITE  =(255,255,255)
BLACK= (0,0,0)
RED=(255,0,0)
YELLOW=(255,255,0)

BUTTON_WIDTH=300
BUTTON_HEIGHT=50

POWERUP_WIDTH=20
POWERUP_HEIGHT=20


start_button=pygame.Rect(WIDTH//2-BUTTON_WIDTH//2,200,BUTTON_WIDTH,BUTTON_HEIGHT)
quit_button=pygame.Rect(WIDTH//2-BUTTON_WIDTH//2,400,BUTTON_WIDTH,BUTTON_HEIGHT)

HEALTH_FONT=pygame.font.SysFont('comicsans',20) 
WINNER_FONT=pygame.font.SysFont('comicsans',100) 
TITLE_FONT=pygame.font.SysFont('comicsans',50) 
BUTTON_FONT=pygame.font.SysFont('comicsans',20) 

GAME_TITLE="NECK TWISTERS"

BULLET_HIT_SOUND=pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND=pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))

FPS= 60  #define the refresh rate
VELOCITY=7.5
BULLET_VELOCITY=20
MAX_BULLETS=5
POWERUP_VELOCTIY = 5

YELLOW_HIT=pygame.USEREVENT +1# THESE NUMBERS R PUT IN PLACE TO DIFFERENTIATE THE TWO EVENTS HERE
RED_HIT= pygame.USEREVENT +2
RED_BARRIER1_HIT=pygame.USEREVENT +3
RED_BARRIER2_HIT=pygame.USEREVENT +4
YELLOW_BARRIER1_HIT=pygame.USEREVENT + 5
YELLOW_BARRIER2_HIT=pygame.USEREVENT +6
RED_POWERUP_HIT=pygame.USEREVENT +7

SPACESHIP_WIDTH,SPACESHIP_HEIGHT=50,50
BORDER=pygame.Rect((WIDTH//2 -5),0,10,HEIGHT) #dimension for the border)



YELLOW_SHIP_IMAGE=pygame.image.load(os.path.join("Assets","spaceship_yellow.png"))
YELLOW_SHIP=pygame.transform.rotate(pygame.transform.scale(YELLOW_SHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),90)
CURSOR_IMG=pygame.transform.scale(pygame.image.load(os.path.join("Assets","hover cursor.png")),(20,25))
POWERUP_IMAGE=pygame.transform.scale(pygame.image.load(os.path.join("Assets","powerup.png")),(POWERUP_WIDTH,POWERUP_HEIGHT))

##pygame.transform.scale(YELLOW_SHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)) this scales the image down, then we rotate in x degrees
# POWERUP_IMAGE=pygame.image.load(os.path.join("Assets","powerup.jpg")) #loadimage of power upPO
SPACE=pygame.transform.scale( pygame.image.load(os.path.join("ASSETS","space.png")),(WIDTH, HEIGHT) )
HOME_BACKGROUND= pygame.transform.scale( pygame.image.load(os.path.join("Assets","home background.png")),(WIDTH, HEIGHT) )
RED_SHIP_IMAGE=pygame.image.load(os.path.join("Assets","spaceship_red.png"))
RED_SHIP=pygame.transform.rotate(pygame.transform.scale(RED_SHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),-90)



def draw_homescreen(HOME_BACKGROUND,TITLE_FONT,GAME_TITLE):
    WIN.blit(HOME_BACKGROUND,(0,0))
    # print("i got this ffar")
    game_title_text=TITLE_FONT.render(GAME_TITLE,1,WHITE)
    WIN.blit(game_title_text,((WIDTH//2-game_title_text.get_width()//2),50))#-(game_title_text.get_width()//2)

    start_button=pygame.Rect(WIDTH//2-BUTTON_WIDTH//2,200,BUTTON_WIDTH,BUTTON_HEIGHT)
    quit_button=pygame.Rect(WIDTH//2-BUTTON_WIDTH//2,400,BUTTON_WIDTH,BUTTON_HEIGHT)

    pygame.draw.rect(WIN, RED, start_button) 
    pygame.draw.rect(WIN, RED, quit_button) 

    start_button_text=BUTTON_FONT.render("START",1,WHITE)
    quit_button_text=BUTTON_FONT.render("QUIT",1,WHITE)

    WIN.blit(start_button_text, (WIDTH//2-start_button_text.get_width()//2,200+BUTTON_HEIGHT//2-start_button_text.get_height()//2) )
    WIN.blit(quit_button_text, (WIDTH//2-quit_button_text.get_width()//2,400+BUTTON_HEIGHT//2- quit_button_text.get_height()//2) )
    
    

    pygame.display.update()

def homescreen():#tells homescreen wah tto do when to stop
    global run_homescreen
    print (run_homescreen)
    draw_homescreen(HOME_BACKGROUND,TITLE_FONT,GAME_TITLE)
    if handle_homescreen()==True:
        run_homescreen=False
        main()
        
        
    elif handle_homescreen()==False:
        # run_homescreen=False
        pygame.quit()
    else:
        # run_homescreen=False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_homescreen=False
                pygame.quit()

def handle_homescreen():
    # print("im in ")
    if is_over(start_button)==True:
        # print("start but")
        change_cursor()
        if pygame.mouse.get_pressed()[0]==True:
            # main()
            return True
    elif is_over(quit_button)==True:
        change_cursor()
        print('hiii')
        if pygame.mouse.get_pressed()[0]==True:
            # print('byee')
            pygame.quit()
            return False
    else:
        pygame.mouse.set_visible(True)
            

    
            
def is_over(rect):
    # print("is over")
    # for event in pygame.event.get():
    #     if event.type == pygame.MOUSEMOTION:
    #         pos= pygame.mouse.get_pos()
    pos = pygame.mouse.get_pos() 
    # print(pos)
    # if (rect[0]<=pos[0] <= rect[0]+rect[2]) and (rect[1]<=pos[1] <= rect[1]+rect[3]):
    if rect.collidepoint(pos[0], pos[1]):
        # print("mouse is over")
        
        return True
    


def draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health, barrier_list,red_powerup_rect,timer,POWERUP_VELOCTIY):#RBH1/2 = RED BARRIER HEALTH 1/2


    # WIN.blit(HOME_BACKGROUND,(0,0))
    WIN.blit(SPACE,(0,0))
    # WIN.fill((WHITE)) # changes the background colour ( always draw background before drawing the cahracters)
    pygame.draw.rect(WIN, BLACK, BORDER) #DRAWS the borde ron here( what are we drawing it on, colour, shape)
    

    WIN.blit(YELLOW_SHIP, (yellow.x,yellow.y)) #we use blit to draw surfaces on the screen (spacships are considered surfaces)
    WIN.blit(RED_SHIP, (red.x,red.y))

    red_health_text=HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text=HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH-red_health_text.get_width() - 10,10) )
    WIN.blit(yellow_health_text, (10,10) )
    
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)


    
    for i in barrier_list:
        if i !=0:
            draw_barrier(i)

    # hereeee
    
        
    handle_red_powerup(red_powerup_rect,red,timer,red_health)
        
        
    # elif (timer>1000 and yellow_health<5):
    #     draw_powerup(yel_powerup_rect)


    pygame.display.update()

def get_barrier(RBH1,RBH2,YBH1,YBH2,red_health,yellow_health):
    barrier_list=[0,0,0,0]
    if red_health<3:
        if RBH1>0:
            RED_BARRIER_1=pygame.Rect(WIDTH*0.75, HEIGHT*0.25, 10, 50)
            barrier_list[0]=(RED_BARRIER_1)
        if RBH2>0:
            RED_BARRIER_2=pygame.Rect(WIDTH*0.75, HEIGHT*0.75, 10, 50)
            barrier_list[1]=(RED_BARRIER_2)
    if yellow_health<3:
        if YBH1>0:
            YELLOW_BARRIER_1=pygame.Rect(WIDTH*0.25 + 5, HEIGHT*0.25, 10, 50)
            barrier_list[2]=(YELLOW_BARRIER_1)
        if YBH2>0:
            YELLOW_BARRIER_2=pygame.Rect(WIDTH*0.25 + 5, HEIGHT*0.75, 10, 50)
            barrier_list[3]=(YELLOW_BARRIER_2)
    return barrier_list
    




def handle_red_powerup(red_powerup_rect,red,timer,red_health):
    
    global POWERUP_VELOCTIY
    if (timer>1000 and red_health<5): 
        print(red_powerup_rect.y)
        print(POWERUP_VELOCTIY)
        if POWERUP_VELOCTIY<0:
            # print("negative velocity")
            if red_powerup_rect.y - POWERUP_VELOCTIY <= 0:
                print("*=-1")
                POWERUP_VELOCTIY*=-1
            else:
                print("-=1  hdjnfhjdnjfgn")
                red_powerup_rect.y +=POWERUP_VELOCTIY
        elif POWERUP_VELOCTIY>0:
            print(" vel")
            if red_powerup_rect.y + POWERUP_VELOCTIY >= HEIGHT-POWERUP_HEIGHT:
                print("*=-1")
                POWERUP_VELOCTIY*=-1
                
            else:
                # print("+=1")
                red_powerup_rect.y +=POWERUP_VELOCTIY

        if red.colliderect(red_powerup_rect):
            pygame.event.post(pygame.event.Event(RED_POWERUP_HIT))
            pass
        else:
            draw_powerup(red_powerup_rect)
            # print(y)
            # print(POWERUP_VELOCTIY)

    


def yellow_handle_movement(keys,yellow):
    if keys[pygame.K_a] and yellow.x - VELOCITY >0 : # check to see if we press key: A left
        yellow.x-= VELOCITY
    if keys[pygame.K_w] and yellow.y - VELOCITY>0: # check to see if we press key: w up
        yellow.y-= VELOCITY
    if keys[pygame.K_s] and (yellow.y + VELOCITY) < HEIGHT- SPACESHIP_HEIGHT: # check to see if we press key: s down
        yellow.y+= VELOCITY
    if keys[pygame.K_d] and (yellow.x + VELOCITY < BORDER.x-SPACESHIP_WIDTH) : # check to see if we press key: d right
        yellow.x+= VELOCITY
        
def red_handle_movement(keys, red):
    if keys[pygame.K_LEFT] and (red.x - VELOCITY)>(BORDER.x+BORDER.width): # check to see if we press key: A left
        red.x-= VELOCITY
    if keys[pygame.K_UP] and red.y - VELOCITY>0: # check to see if we press key: w up
        red.y-= VELOCITY
    if keys[pygame.K_DOWN] and (red.y + VELOCITY) < HEIGHT- SPACESHIP_HEIGHT: 
        red.y+= VELOCITY
    if keys[pygame.K_RIGHT] and (red.x + VELOCITY < WIDTH-SPACESHIP_WIDTH) :
        red.x+= VELOCITY

def handle_bullets(yellow_bullets, red_bullets, yellow,red,barrier_list):
    # print(barrier_list)mm
    if len(yellow_bullets)>0:
        for bullet in yellow_bullets:
            bullet.x+=BULLET_VELOCITY
            if red.colliderect(bullet):
                pygame.event.post(pygame.event.Event(RED_HIT)) # new event called RED hit has happened
                yellow_bullets.remove(bullet) # deletes bullet
            elif bullet.x>=WIDTH:
                yellow_bullets.remove(bullet)
            # print(barrier_list[0])
            if barrier_list[0]!=0 and barrier_list[0].colliderect(bullet): 
                # print("rb got hit")m
                pygame.event.post(pygame.event.Event(RED_BARRIER1_HIT))
                yellow_bullets.remove(bullet)
            if barrier_list[1]!=0 and barrier_list[1].colliderect(bullet):
                pygame.event.post(pygame.event.Event(RED_BARRIER2_HIT))
                yellow_bullets.remove(bullet)


    if len(red_bullets)>0:##
        for bullet in red_bullets:
            bullet.x-=BULLET_VELOCITY
            print(red_bullets)
            if yellow.colliderect(bullet):
                pygame.event.post(pygame.event.Event(YELLOW_HIT)) # new event called yellow hit has happened
                red_bullets.remove(bullet) # deletes bullet
            elif bullet.x<=0: #this works
                red_bullets.remove(bullet)
            
            if barrier_list[2]!=0 and barrier_list[2].colliderect(bullet): 
                pygame.event.post(pygame.event.Event(YELLOW_BARRIER1_HIT))
                red_bullets.remove(bullet)
            if barrier_list[3]!=0 and barrier_list[3].colliderect(bullet):
                pygame.event.post(pygame.event.Event(YELLOW_BARRIER2_HIT))
                red_bullets.remove(bullet)

def draw_powerup(powerup_rect):
    WIN.blit(POWERUP_IMAGE,(powerup_rect.x,powerup_rect.y))
    pygame.display.update()

def draw_winner(winner_text):

    draw_winner=WINNER_FONT.render(winner_text,1,WHITE)
    WIN.blit(draw_winner,(WIDTH//2 - draw_winner.get_width()//2,HEIGHT//2 - draw_winner.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)# show winning msg for 5 secs and then it dissapears

def draw_barrier(barrier):
    pygame.draw.rect(WIN,WHITE,barrier)
    pygame.display.update()
    
def change_cursor():
    pygame.mouse.set_visible(False)
    cursor_image_rect=CURSOR_IMG.get_rect()
    cursor_image_rect.center = pygame.mouse.get_pos()
    WIN.blit(CURSOR_IMG, cursor_image_rect)
    pygame.display.update()





def main():
    global run_homescreen
    red=pygame.Rect(900,300, SPACESHIP_WIDTH,SPACESHIP_HEIGHT)# (X,y, wdith , height) this defines where we want the red player to be
    yellow=pygame.Rect(100,300, SPACESHIP_WIDTH,SPACESHIP_HEIGHT)


    red_powerup_rect=pygame.Rect(WIDTH//2+10,random.randint(POWERUP_HEIGHT,HEIGHT-POWERUP_HEIGHT),POWERUP_WIDTH,POWERUP_HEIGHT)

    red_bullets=[]
    yellow_bullets=[]
    red_health=10
    yellow_health=10

    yellow_barrier1_health=3
    yellow_barrier2_health=3
    red_barrier1_health=3
    red_barrier2_health=3
    
    while run_homescreen==True:
        homescreen()
    

    clock=pygame.time.Clock()
    run=True
    timer=0
    while run==True:
        timer+=1

        clock.tick(FPS) # controls speed of while loop aka the FPS of the game
        barrier_list=get_barrier(red_barrier1_health, red_barrier2_health,yellow_barrier1_health,yellow_barrier2_health,red_health,yellow_health)


        for event in pygame.event.get():#block below allows to close the window when done
            if event.type == pygame.QUIT:
                run=False
                pygame.quit()
            if event.type== pygame.KEYDOWN:
                if event.key== pygame.K_v and (len(yellow_bullets)<MAX_BULLETS): #red person shooting
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + (yellow.height//2)-2,10,5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key== pygame.K_m and len(red_bullets)<MAX_BULLETS: # yellow shooting
                    bullet = pygame.Rect(red.x, red.y + (red.height//2)-2,10,5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()


            if event.type==RED_HIT:
                red_health-=1
                BULLET_HIT_SOUND.play()

            if event.type==YELLOW_HIT:
                yellow_health-=1
                BULLET_HIT_SOUND.play()
            

            

            if event.type==RED_BARRIER1_HIT:
                red_barrier1_health-=1
            if event.type==RED_BARRIER2_HIT:
                red_barrier2_health-=1
            if event.type==YELLOW_BARRIER1_HIT:
                yellow_barrier1_health-=1
            if event.type==YELLOW_BARRIER2_HIT:
                yellow_barrier2_health-=1

            if event.type==RED_POWERUP_HIT:
                pass
        key_pressed=pygame.key.get_pressed()# this tells us what keys r current being pressed at this second
        
        winner_text=""

        if red_health<=0:
            winner_text="Yellow Wins!"

        if yellow_health<=0:
            winner_text="Red Wins!"

        if winner_text!="":
            draw_winner(winner_text)
            pygame.time.delay(3000)
            run_homescreen=True
            while run_homescreen==True:
                homescreen()
            # break


        yellow_handle_movement(key_pressed,yellow)# movements the yellow ships based on its current postion and keys pressed
        red_handle_movement(key_pressed,red)
        handle_bullets(yellow_bullets,red_bullets, yellow,red,barrier_list)
        draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health,barrier_list,red_powerup_rect,timer,POWERUP_VELOCTIY) #draws something on the screen
        

if __name__=="__main__":
    main()

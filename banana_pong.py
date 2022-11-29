# https://medium.com/geekculture/making-pong-with-pygame-19a632b882d

import pygame
import banana_detection
from threading import Thread
from multiprocessing import Process
import subprocess

banana_pos = 0

# Initialization of the Game
pygame.init()
width = 1500
height = 900
screen = pygame.display.set_mode((width, height)) # Width by Height

# Window Stuff
pygame.display.set_caption('Pong')
icon = pygame.image.load('./images/icon.png')
pygame.display.set_icon(icon)

# Player Stuff
player_img = pygame.image.load('./images/player.png')
player_X = 10
player_Y_default = height/2 - 100
player_Y_dif = 0

# Ball Stuff
ball_img = pygame.image.load('./images/ball.png')
ball_X = width/2 - 15
ball_Y = height/2 - 15
ball_dir_X = -3
ball_dir_Y = 3

# CPU Stuff
cpu_img = pygame.image.load('./images/player.png')
cpu_X = width - 10 - 27
cpu_Y = height/2 - 100

def player(y_val):
    screen.blit(player_img, (player_X, y_val))

def ball():
    screen.blit(ball_img, (ball_X, ball_Y))

def cpu():
    screen.blit(cpu_img, (cpu_X, cpu_Y))

def calc_cpu():
    global cpu_Y
    global ball_Y
    if cpu_Y+100-ball_Y-15 > 0:
        cpu_Y -= 3
    elif cpu_Y+100-ball_Y-15 < 0:
        cpu_Y += 3
    cpu_Y = min(cpu_Y, height-10-200)
    cpu_Y = max(cpu_Y, 10)

def game_over(win):
    global ball_dir_X
    global ball_dir_Y
    global ball_X
    global ball_Y
    print(win)
    ball_X = width/2 - 15
    ball_Y = height/2 - 15
    ball_dir_X = -3
    ball_dir_Y = 3

def calc_ball():
    global ball_dir_X
    global ball_dir_Y
    global ball_X
    global ball_Y
    if ball_Y == 10:
        ball_dir_Y *= -1
    elif ball_Y == height-10-30:
        ball_dir_Y *= -1
    if ball_X <= 37 and ball_Y >= player_Y_default+player_Y_dif-30 and ball_Y <= player_Y_default+player_Y_dif+200 and ball_dir_X < 0:
        ball_dir_X *= -1
    if ball_X >= cpu_X and ball_Y >= cpu_Y-11 and ball_Y <= cpu_Y+200-19 and ball_dir_X > 0:
        ball_dir_X *= -1
    
    ball_X+=ball_dir_X
    ball_Y+=ball_dir_Y
    if (ball_X < 30):
        game_over(False)
    elif (ball_X > cpu_X+10):
        game_over(True)
    ball_Y = min(ball_Y, height-10-30)
    ball_Y = max(ball_Y, 10)

def move_up(y_val):
    global player_Y_dif
    if player_Y_dif-y_val >= -player_Y_default+10:
        player_Y_dif -= y_val

def move_down(y_val):
    global player_Y_dif
    if player_Y_dif+y_val <= player_Y_default-10:
        player_Y_dif += y_val

def pong_game():
    game_on = True

    while game_on:
        screen.fill((255,225,226))

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                game_on=False
        
        key_input = pygame.key.get_pressed()
        if key_input[pygame.K_w]:
            move_up(4)
        elif key_input[pygame.K_s]:
            move_down(4)
        elif key_input[pygame.K_UP]:
            move_up(4)
        elif key_input[pygame.K_DOWN]:
            move_down(4)
        elif banana_detection.banana_pos == 1:
            move_up(4)
        elif banana_detection.banana_pos  == -1:
            move_down(4)
        
        if key_input[pygame.K_5]:
            game_on=False
        player(player_Y_default+player_Y_dif)
        calc_ball()
        calc_cpu()
        ball()
        cpu()
        pygame.display.update()

    return None

# SUBPROCESS
if __name__ == '__main__':
    banana_subprocess = subprocess.call(banana_detection.banana_position())
    pong_subprocess = subprocess.call(pong_game())
    
    banana_subprocess.run()
    pong_subprocess.run()


# # MULTIPROCESSING
# if __name__ == '__main__':
#     process_pong = Process(target=pong_game(), args=())
#     process_banana = Process(target=banana_detection.banana_position(), args=())
#     process_pong.start()
#     process_banana.start()
#     process_banana.join()
#     process_pong.join()


# # THREADING
# # Thread executing the banana detection
# thread_banana = Thread(target=banana_detection.banana_position())
# thread_banana.start()

# # Thread executing the game
# thread_pong = Thread(target=pong_game())
# thread_pong.start()

# thread_banana.join()
# thread_pong.join()
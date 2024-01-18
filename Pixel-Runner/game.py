import pygame
import math
from random import randint, choice
from sprites import *


def displayIntroScreen():
    screen.fill('#9cc2f3')

    welcome_text = header_font.render('Welcome!', False, '#4f719d')
    info_text_instr = normal_font.render('Use SPACE to jump and avoid incoming enemies.', False, '#585858')
    info_text_instr_2 = normal_font.render('Try to stay alive for as long as possible!', False, '#585858')
    info_text_start = halfbold_font.render('Press ENTER to start..', False, '#4f719d')
    info_text_exit = halfbold_font.render('Press ESC to exit..', False, '#4f719d')

    screen.blits([(welcome_text, welcome_text.get_rect(center=(400, 40))),
                  (head, head.get_rect(center=(400, 160))),
                  (info_text_instr, info_text_instr.get_rect(center=(400, 260))),
                  (info_text_instr_2, info_text_instr_2.get_rect(center=(400, 280))),
                  (info_text_start, info_text_start.get_rect(center=(400, 320))),
                  (info_text_exit, info_text_exit.get_rect(center=(400, 350)))])


def displayGameOverScreen():
    screen.fill('#9cc2f3')
    gameover_text = header_font.render('Game Over!', False, '#4f719d')
    info_text_start = halfbold_font.render('Press ENTER to play again', False, '#4f719d')
    score_text = halfbold_font.render(f'Your score was: {score}', False, '#4f719d')

    screen.blits([(gameover_text, gameover_text.get_rect(center=(400, 50))),
                  (dead_head, dead_head.get_rect(center=(400, 180))),
                  (info_text_start, info_text_start.get_rect(center=(400, 300)))])
    if score > 0:
        screen.blit(score_text, score_text.get_rect(center=(400, 340)))


def displayGame():
    # display scrolling background
    global scroll
    for i in range(0, tiles):
        screen.blit(skyBG, (i * bg_width + scroll, 0))
    scroll -= game_speed
    if abs(scroll) > bg_width:
        scroll = 0

    # display ground platform
    screen.blit(groundBG, (0, 300))

    # get score
    global score
    score = displayScore()


def displayScore():
    current_time = (pygame.time.get_ticks() - start_time) // 1000  # time in seconds
    score_text = halfbold_font.render(f'Score: {current_time}', False, '#585858')
    score_rect = score_text.get_rect(center=(400, 20))
    screen.blit(score_text, score_rect)
    return current_time


def collision():
    if pygame.sprite.spritecollide(player.sprite, enemy_group, False):
        enemy_group.empty()
        hit_sound.play()
        return False
    else:
        return True


pygame.init()  # initialize pygame

# scale of the screen
screenWidth = 800
screenHeight = 400

# load and set all the important stuff
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Pixel Runner')

clock = pygame.time.Clock()  # clock object for frame rate
start_time = 0
score = 0  # global variable to store score
game_speed = 1

# sound/music load and settings
background_music = pygame.mixer.Sound('mat/sound/music_background.wav')
background_music.play(loops=-1).set_volume(0.35)

hit_sound = pygame.mixer.Sound('mat/sound/death.mp3')
hit_sound.set_volume(1)

# fonts
header_font = pygame.font.Font('mat/fonts/Symtext.ttf', 60)  # load font for headers
halfbold_font = pygame.font.Font('mat/fonts/DePixelHalbfett.ttf', 20)  # load half-bold font
normal_font = pygame.font.Font('mat/fonts/DePixelSchmal.ttf', 18)  # load font for info texts
pygame.font.Font.set_underline(normal_font, True)  # underlines the chosen font

# load background images
skyBG = pygame.image.load('mat/backgrounds/background_01.png').convert()
groundBG = pygame.image.load('mat/backgrounds/background_02.png').convert()

# load decorative images
head = pygame.transform.scale(pygame.image.load('mat/head.png').convert_alpha(), (200, 175))
dead_head = pygame.transform.scale(pygame.image.load('mat/head_dead.png').convert_alpha(), (200, 175))
empty_heart = pygame.image.load('mat/empty_heart.png').convert_alpha()

# create player group & player
player = pygame.sprite.GroupSingle()
player.add(Player())

# create enemy group
enemy_group = pygame.sprite.Group()

# timers
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1400)  # triggers enemy_timer every 1400 ms

difficulty_timer = pygame.USEREVENT + 2
pygame.time.set_timer(difficulty_timer, 1000)

# boolean variables
intro_screen = True
game_active = False
running = True

bg_width = skyBG.get_width()
scroll = 0
tiles = math.ceil(screenWidth / bg_width) + 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit()
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            running = False
            pygame.quit()
            exit()

        if game_active:
            # enemy mechanics
            if event.type == enemy_timer:
                enemy_group.add(Enemy(choice(['wasp', 'blop', 'blop', 'blop'])))

            if event.type == difficulty_timer:
                game_speed += 0.1
        # game start from game over screen
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_active = True
                game_speed = 1
                start_time = pygame.time.get_ticks()  # help variable to get the proper score
        # game start from intro screen
        if intro_screen:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                intro_screen = False
                game_active = True

    if intro_screen:
        # display intro screen
        displayIntroScreen()
    else:
        if game_active:
            # display game
            displayGame()

            # drawing & animating player
            player.draw(screen)
            player.update()

            # drawing & animating enemies
            enemy_group.draw(screen)
            enemy_group.update()

            # collision
            game_active = collision()
        else:
            displayGameOverScreen()

    pygame.display.update()
    clock.tick(60)  # 60fps (frame rate)

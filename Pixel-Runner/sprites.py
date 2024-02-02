import pygame
from random import randint

game_speed = 1

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  # initialize the sprite class
        self.player_walk = [pygame.image.load('mat/chars/player_walk_01.png').convert_alpha(),
                            pygame.image.load('mat/chars/player_walk_02.png').convert_alpha()]
        self.player_index = 0
        self.player_jump = pygame.image.load('mat/chars/player_jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(100, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('mat/sound/jump.mp3')
        self.jump_sound.set_volume(0.3)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def player_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def player_animation(self):
        if self.rect.bottom < 300:  # jump "animation"
            self.image = self.player_jump
        else:  # walk "animation"
            self.player_index += 0.08  # makes the transition between the two sprites smoother
            self.image = self.player_walk[int(self.player_index) % 2]

    def update(self):
        self.player_input()
        self.player_gravity()
        self.player_animation()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()

        if name == 'wasp':
            self.enemy_move = [pygame.image.load('mat/chars/wasp_01.png').convert_alpha(),
                               pygame.image.load('mat/chars/wasp_02.png').convert_alpha()]
            y_pos = 220
        else:
            self.enemy_move = [pygame.image.load('mat/chars/pinkblop_01.png').convert_alpha(),
                               pygame.image.load('mat/chars/pinkblop_02.png').convert_alpha()]
            y_pos = 300

        self.enemy_index = 0
        self.image = self.enemy_move[self.enemy_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def enemy_animation(self):
        self.enemy_index += 0.07
        self.image = self.enemy_move[int(self.enemy_index) % 2]

    def update(self):
        self.enemy_animation()
        self.rect.x -= (game_speed + 3)
        self.destroy()

    def destroy(self):
        if self.rect.x <= 0 - self.rect.width:
            self.kill()

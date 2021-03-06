import pygame
from pygame.sprite import Sprite

pygame.mixer.init()


class Player(Sprite):
    def __init__(self):
        self.scale = 1
        Sprite.__init__(self)
        # Images
        self.image = pygame.image.load("images/jumpman/jumpman.gif")
        self.image_move_left = pygame.image.load("images/jumpman/jumpman_move_left.gif")
        self.image_move_right = pygame.image.load("images/jumpman/jumpman_move_right.gif")
        self.image_jump_left = pygame.image.load("images/jumpman/jumpman_run_left.gif")
        self.image_jump_right = pygame.image.load("images/jumpman/jumpman_run_right.gif")
        self.image_stairs = pygame.image.load("images/jumpman/jumpman_stairs.gif")
        # Sounds
        self.sound_walk = pygame.mixer.Sound("sounds/walk.wav")
        self.sound_jump = pygame.mixer.Sound("sounds/jump.wav")
        self.sound_stair = pygame.mixer.Sound("sounds/stair.wav")
        self.sound_dead = pygame.mixer.Sound("sounds/dead.wav")
        self.sound_coin = pygame.mixer.Sound("sounds/coin.wav")
        # Rect of image
        self.rect = self.image.get_rect()
        self.rect.x = 105
        self.rect.y = 451
        self.rect.w = 32
        self.rect.h = 32
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
        # Movement values
        self.move_left = False
        self.move_right = False
        self.move_down = False
        self.move_up = False
        self.jumping = False
        self.direction = 0
        self.move_x = 5
        self.move_y = 5
        self.vel_x = 0
        self.vel_y = 11
        self.gravity_force = 5
        self.levelChange = False
        self.level = 1
        self.point = 0
        # Player rect
        self.player_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.w, self.rect.h)

    # Movement Functions
    def functions(self, platformGroup, stairGroup, rampGroupU, rampGroupD, screen, bottomPlatform, coinGroup):
        # Move Left
        if self.move_left:
            if self.rect.x > 0:
                self.rect.x -= self.move_x
                if pygame.sprite.spritecollide(self, platformGroup, False):
                    self.rect.x += self.move_x
                elif pygame.sprite.spritecollide(self, bottomPlatform, False):
                    self.rect.x += self.move_x
                    self.rect.y -= self.move_y + 1
                elif pygame.sprite.spritecollide(self, rampGroupU, False):
                    self.rect.y -= self.move_y - 2
                    self.rect.x += self.move_x - 2
                elif pygame.sprite.spritecollide(self, rampGroupD, False):
                    self.rect.y -= self.move_y - 2
                    self.rect.x -= self.move_x - 2
                else:
                    self.rect.x -= self.move_x
        # Move Right
        if self.move_right:
            if self.rect.x < self.screenwidth - 32:
                self.rect.x += self.move_x
                if pygame.sprite.spritecollide(self, platformGroup, False):
                    self.rect.x -= self.move_x
                elif pygame.sprite.spritecollide(self, bottomPlatform, False):
                    self.rect.x -= self.move_x
                    self.rect.y -= self.move_y
                elif pygame.sprite.spritecollide(self, rampGroupU, False):
                    self.rect.y -= self.move_y
                    self.rect.x += self.move_x - 2
                    if pygame.sprite.spritecollide(self, platformGroup, False):
                        self.rect.x -= self.move_x
                elif pygame.sprite.spritecollide(self, rampGroupU, False):
                    self.rect.y -= self.move_y - 2
                    self.rect.x += self.move_x - 2
                else:
                    self.rect.x += self.move_x
        # Move Right
        if self.move_down:
            if self.rect.y < 473:
                self.rect.y += self.move_y
                if pygame.sprite.spritecollide(self, bottomPlatform, False):
                    self.rect.y -= self.move_y
                elif pygame.sprite.spritecollide(self, stairGroup, False):
                    self.rect.y += self.move_y
                    self.direction = 3
                else:
                    if pygame.sprite.spritecollide(self, platformGroup, False):
                        self.rect.y -= self.move_y
                    elif pygame.sprite.spritecollide(self, rampGroupU, False):
                        self.rect.y -= self.move_y
                    elif pygame.sprite.spritecollide(self, rampGroupD, False):
                        self.rect.y -= self.move_y
                    else:
                        self.rect.y -= self.move_y
        # Move Up
        if self.move_up:
            if self.rect.y > 0:
                self.rect.y -= (self.move_y + 1)
                if pygame.sprite.spritecollide(self, stairGroup, False):
                    self.rect.y -= (self.move_y + 1)
                    self.direction = 3
                else:
                    if pygame.sprite.spritecollide(self, platformGroup, False):
                        self.rect.y += self.move_y
                    elif pygame.sprite.spritecollide(self, rampGroupU, False):
                        self.rect.y += self.move_y
                    else:
                        self.rect.y += self.move_y
        # Jump
        if self.jumping:
            self.direction = 2
            self.rect.y -= (self.vel_y * 2) * 0.5
            self.vel_y -= 1
            if self.vel_y <= -(self.move_y - 2):
                self.vel_y = 11
                self.jumping = False
        # Coin
        if pygame.sprite.spritecollide(self, coinGroup, True):
            self.sound_coin.play(0)
            self.point += 100
            if len(coinGroup) == 0:
                self.levelChange = True
                self.level = 4

    # Movement Keys
    def move(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.move_left = True
                self.direction = -1

            if event.key == pygame.K_RIGHT:
                self.move_right = True
                self.direction = 1

            if not self.jumping and event.key == pygame.K_LSHIFT:
                if self.move_left:
                    self.jumping = True
                    self.sound_jump.play(0)
                if self.move_right:
                    self.jumping = True
                    self.sound_jump.play(0)

            if event.key == pygame.K_DOWN:
                self.move_down = True

            if event.key == pygame.K_UP:
                self.move_up = True

        if not event.type == pygame.KEYDOWN:
            self.direction = 0
            self.move_left = False
            self.move_right = False
            self.jumping = False
            self.move_up = False
            self.move_down = False

    # Gravity
    def gravity(self, platformGroup, rampGroupU, rampGroupD, bottomPlatform):
        self.rect.y += self.gravity_force
        if pygame.sprite.spritecollide(self, platformGroup, False):
            self.rect.y -= self.gravity_force
        elif pygame.sprite.spritecollide(self, rampGroupU, False):
            self.rect.y -= self.gravity_force
        elif pygame.sprite.spritecollide(self, rampGroupD, False):
            self.rect.y -= self.gravity_force
        elif pygame.sprite.spritecollide(self, bottomPlatform, False):
            self.rect.y -= self.gravity_force
        # check collision with bottom floor
        elif self.rect.y > 480:
            self.rect.y -= self.gravity_force

    # Draw animations
    def draw(self, screen):
        if self.direction == 0:
            screen.blit(self.image, self.rect)
        if self.direction == 1:
            screen.blit(self.image_move_right, self.rect)
        if self.direction == -1:
            screen.blit(self.image_move_left, self.rect)
        if self.direction == 2:
            if self.move_left:
                screen.blit(self.image_jump_left, self.rect)
            if self.move_right:
                screen.blit(self.image_jump_right, self.rect)
        if self.direction == 3:
            screen.blit(self.image_stairs, self.rect)

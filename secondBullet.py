import pygame
from pygame.sprite import Sprite


class SecondBullet(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.image.load("images/platform/bullet.png")
        self.rect = self.image.get_rect()
        self.fireSound = pygame.mixer.Sound("sounds/fireSound.wav")
        self.rect.x = 20
        self.rect.y = 25
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
        self.movex = 4
        self.movey = 4
        self.moveOnlyY = False
        self.list = []


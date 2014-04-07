import pygame, sys
pygame.init()
screen = pygame.display.set_mode((800, 600))
street1_img = pygame.image.load('teststreet1.png').convert()
street2_img = pygame.image.load('teststreet2.png').convert()
street3_img = pygame.image.load('teststreet3.png').convert()
player_img = pygame.image.load('persontest.png').convert()
print("loaded images")

while True:
    screen.blit(street1_img, (0, 0))
    pygame.display.update()
    pygame.time.delay(100)

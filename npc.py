import pygame
from player import Player

def load_image(image_name):
    return pygame.image.load(image_name).convert_alpha()

class Npc(pygame.sprite.Sprite):
    def __init__(self, image, x, y, name, screen):
        pygame.sprite.Sprite.__init__(self)
        ##All the lines for the npcs split in to groups
        #Prostitute
        #Prost_Initial
        textB3_P1_2 = (load_image('./text/Background3/textB3_P1_2.png'), True)
        textB3_P1_4 = (load_image('./text/Background3/textB3_P1_4.png'), True)
        textB3_P1_6 = (load_image('./text/Background3/textB3_P1_6.png'), True)
        
        self.prost_initial_lines = [textB3_P1_2, textB3_P1_4, textB3_P1_6]
        #Prost_Final
        textB3_P1_9_AP2 = (load_image('./text/Background3/textB3_P1_9_AP2.png'), True)
        textB3_P1_11_AP2 = (load_image('./text/Background3/textB3_P1_11_AP2.png'), True)

        self.prost_final_lines = [textB3_P1_9_AP2, textB3_P1_11_AP2]        
        #Thug
        #Thug_Initial
        textB4_P2_1 = (load_image('./text/Background4/textB4_P2_1.png'), False)
        textB4_P2_3 = (load_image('./text/Background4/textB4_P2_3.png'), False)
        textB4_P2_8 = (load_image('./text/Background4/textB4_P2_8.png'), False)
        self.thug_initial_lines = [textB4_P2_1, textB4_P2_3, None, None, None, textB4_P2_8]
        #Thug_Secondary
        textB4_P2_10_AC3 = (load_image('./text/Background4/textB4_P2_10_AC3.png'), False)
        textB4_P2_12_AC3 = (load_image('./text/Background4/textB4_P2_12_AC3.png'), False)
        textB4_P2_14_AC3 = (load_image('./text/Background4/textB4_P2_14_AC3.png'), False)
        self.thug_secondary_lines = [textB4_P2_10_AC3, textB4_P2_12_AC3, textB4_P2_14_AC3]
        #Thug_Final
        textB4_P2_16_AC3 = (load_image('./text/Background4/textB4_P2_16_AC4.png'), False)
        textB4_P2_18_AC3 = (load_image('./text/Background4/textB4_P2_18_AC4.png'), False)
        self.thug_final_lines = [textB4_P2_16_AC3, textB4_P2_18_AC3]
        #Crazy Man
        #Crazy_Man_Initial
        textB5_P3_1 = (load_image('./text/Background5/textB5_P3_1.png'), False)
        self.crazy_man_initial_lines = [textB5_P3_1]
        #Crazy_Man_Secondary
        textB5_P3_3_AC4 = (load_image('./text/Background5/textB5_P3_3_AC4.png'), False)
        textB5_P3_5_AC4 = (load_image('./text/Background5/textB5_P3_5_AC4.png'), False)
        textB5_P3_6_AC4 = (load_image('./text/Background5/textB5_P3_6_AC4.png'), False)
        self.crazy_man_secondary_lines = [textB5_P3_3_AC4, textB5_P3_5_AC4, textB5_P3_6_AC4]
        #Crazy_Man_Tertiary
        textB5_P3_9_AC5 = (load_image('./text/Background5/textB5_P3_9_AC5.png'), False)
        textB5_P3_11_AC5 = (load_image('./text/Background5/textB5_P3_11_AC5.png'), False)
        self.crazy_man_tertiary_lines = [textB5_P3_9_AC5, textB5_P3_11_AC5]        
        #Crazy_Man_Final
        textB5_P3_13_AC2 = (load_image('./text/Background5/textB5_P3_13_AC2.png'), False)
        self.crazy_man_final_lines = [textB5_P3_13_AC2]
        
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = name
        self.screen = screen
    def draw(self):
        self.screen.blit(self.image, self.rect)
        
    def talking_pos(self, text_image, left, scene):
        l = self.rect.left
        t = self.rect.top
        w = text_image.get_rect().width
        h = text_image.get_rect().height
        if left:
            l = l - w
            t = t - h
        else:
            l = l + self.rect.width + 20
            t = t - h

        #make sure we don't render off screen
        l = max(0, l)
        l = min(l, 1300 - w)
        t = max(0, t)
        t = min(t, scene.rect.height - h)       
        return (l, t)
    def say(self, line, scene):
        place_to_say = self.talking_pos(line[0], line[1], scene)
        self.screen.blit(line[0], place_to_say)

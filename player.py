import pygame
def load_image(image_name):
    return pygame.image.load(image_name).convert_alpha()



class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.direction = False
        self.current_step = 0
        self.moved = 0
        self.screen = screen
        #walking
        self.rg_images = [load_image("./Richie/RGIdleWalk1.png"),load_image("./Richie/RGWalk2.png"),load_image("./Richie/RGIdleWalk1.png"),load_image("./Richie/RGWalk3.png")]
        self.drg_images = [load_image("./Richie/DRGstandWalk2.png"),load_image("./Richie/DRGWalk1.png"),load_image("./Richie/DRGstandWalk2.png"),load_image("./Richie/DRGWalk3.png")]
        ## Clue Bar Images
        self.default_clue_bar = load_image('./ClueBar/clueBar.png')
        self.cb12345 = load_image('./ClueBar/clueBar12345.png')
        self.cb1234 = load_image('./ClueBar/clueBar1234.png')
        self.cb1345 = load_image('./ClueBar/clueBar1345.png')
        self.cb124 = load_image('./ClueBar/clueBar124.png')
        self.cb134 = load_image('./ClueBar/clueBar134.png')
        self.cb123 = load_image('./ClueBar/clueBar123.png')
        self.cb14 = load_image('./ClueBar/clueBar14.png')
        self.cb13 = load_image('./ClueBar/clueBar13.png')
        self.cb12 = load_image('./ClueBar/clueBar12.png')        
        self.cb1 = load_image('./ClueBar/clueBar1.png')
        ##talking images
        #Self
        textB1_1 = (load_image('./text/Background1/textB1_1.png'), False)
        textB1_2 = (load_image('./text/Background1/textB1_2.png'), False)
        textB1_3 = (load_image('./text/Background1/textB1_3.png'), False)
        textB1_4 = (load_image('./text/Background1/textB1_4.png'), False)
        textB1_5_afterClothes = (load_image('./text/Background1/textB1_5_afterClothes.png'), False)
        textB1_C1_1 = (load_image('./text/Background1/textB1_C1_1.png'), False)
        textB1_Clothes_1 = (load_image('./text/Background1/textB1_Clothes_1.png'), True)
        textB1_Clothes_2 = (load_image('./text/Background1/textB1_Clothes_2.png'), False)
        textB1_Clothes_3 = (load_image('./text/Background1/textB1_Clothes_3.png'), True)
        textB1_Clothes_4 = (load_image('./text/Background1/textB1_Clothes_4.png'), False)
        textB1_Clothes_5 = (load_image('./text/Background1/textB1_Clothes_5.png'), True)
        textB1_Clothes_6 = (load_image('./text/Background1/textB1_Clothes_6.png'), False)

        self.start_lines1 = [textB1_1, textB1_2, textB1_3, textB1_4]
        self.needle_lines = [textB1_C1_1]
        self.clothes_lines = [textB1_Clothes_1, textB1_Clothes_2, textB1_Clothes_3, textB1_Clothes_4, textB1_Clothes_5, textB1_Clothes_6]
        self.find_needle_lines = [textB1_5_afterClothes]
        self.find_clothes_lines = [textB1_3]

        #Racoon
        textB2_C2_1 = (load_image('./text/Background2/textB2_C2_1.png'), False)
        textB2_C2_2 = (load_image('./text/Background2/textB2_C2_2.png'), False)
        
        self.location_lines = [textB2_C2_1]
        self.racoon_lines = [textB2_C2_2]
        #Bottle
        textB5_C4_1 = (load_image('./text/Background5/textB5_C4_1.png'), True)

        self.bottle_lines = [textB5_C4_1]
        #Prost_Initial
        self.met_prostitute = False
        textB3_P1_1 = (load_image('./text/Background3/textB3_P1_1.png'), False)
        textB3_P1_3 = (load_image('./text/Background3/textB3_P1_3.png'), False)
        textB3_P1_5 = (load_image('./text/Background3/textB3_P1_5.png'), False)
        textB3_P1_7 = (load_image('./text/Background3/textB3_P1_7.png'), False)
        
        self.prost_initial_lines = [textB3_P1_1, textB3_P1_3, textB3_P1_5, textB3_P1_7]
        #Prost_Final
        textB3_P1_8_AP2 = (load_image('./text/Background3/textB3_P1_8_AP2.png'), False)
        textB3_P1_10_AP2 = (load_image('./text/Background3/textB3_P1_10_AP2.png'), False)

        self.prost_final_lines = [textB3_P1_8_AP2, textB3_P1_10_AP2]
        #Thug
        self.met_thug = False
        #Thug_Initial
        textB4_P2_2 = (load_image('./text/Background4/textB4_P2_2.png'), True)
        textB4_P2_4 = (load_image('./text/Background4/textB4_P2_4.png'), True)
        textB4_P2_5 = (load_image('./text/Background4/textB4_P2_5.png'), True)
        textB4_P2_6 = (load_image('./text/Background4/textB4_P2_6.png'), True)        
        textB4_P2_7 = (load_image('./text/Background4/textB4_P2_7.png'), True)
        self.thug_initial_lines = [textB4_P2_2, textB4_P2_4, textB4_P2_5, textB4_P2_6, textB4_P2_7]
        #Thug_Secondary
        textB4_P2_9_AC3 = (load_image('./text/Background4/textB4_P2_9_AC3.png'), True)
        textB4_P2_11_AC3 = (load_image('./text/Background4/textB4_P2_11_AC3.png'), True)
        textB4_P2_13_AC3 = (load_image('./text/Background4/textB4_P2_13_AC3.png'), True)
        self.thug_secondary_lines = [textB4_P2_9_AC3, textB4_P2_11_AC3, textB4_P2_13_AC3]
        #Thug_Final
        textB4_P2_15_AC3 = (load_image('./text/Background4/textB4_P2_15_AC4.png'), True)
        textB4_P2_17_AC3 = (load_image('./text/Background4/textB4_P2_17_AC4.png'), True)
        self.thug_final_lines = [textB4_P2_15_AC3, textB4_P2_17_AC3]

        #Crazy_Man
        self.met_crazy_man = False
        #Crazy_Man_Secondary
        self.confronted_crazy_man = False
        textB5_P3_2_AC4 = (load_image('./text/Background5/textB5_P3_2_AC4.png'), True)
        textB5_P3_4_AC4 = (load_image('./text/Background5/textB5_P3_4_AC4.png'), True)
        textB5_P3_7_AC4 = (load_image('./text/Background5/textB5_P3_7_AC4.png'), True)
        self.crazy_man_secondary_lines = [textB5_P3_2_AC4, textB5_P3_4_AC4, None, textB5_P3_7_AC4]
        #Crazy_Man_Tertiary
        self.proved_crazy_man = False
        textB5_P3_8_AC5 = (load_image('./text/Background5/textB5_P3_8_AC5.png'), True)
        textB5_P3_10_AC5 = (load_image('./text/Background5/textB5_P3_10_AC5.png'), True)
        self.crazy_man_tertiary_lines = [textB5_P3_8_AC5, textB5_P3_10_AC5]
        #Crazy_Man_Final
        textB5_P3_12_AC2 = (load_image('./text/Background5/textB5_P3_12_AC2.png'), True)
        self.crazy_man_final_lines = [textB5_P3_12_AC2]
        
        
        self.rect = self.rg_images[0].get_rect()
        self.inventory = set()
    def draw(self, screen):
        if("clothes" in self.inventory):
            if(self.direction):
                screen.blit(pygame.transform.flip(self.drg_images[self.current_step], True, False), self.rect)
            else:
                screen.blit(self.drg_images[self.current_step], self.rect)
        else:
            if(self.direction):
                screen.blit(pygame.transform.flip(self.rg_images[self.current_step], True, False), self.rect)
            else:
                screen.blit(self.rg_images[self.current_step], self.rect)
        if "needle" in self.inventory:
            if "racoon" in self.inventory:
                if "name" in self.inventory:
                    if "bottle" in self.inventory:
                        if "witness" in self.inventory:
                            screen.blit(self.cb12345, (0, 700))
                        else:
                            screen.blit(self.cb1234, (0, 700))
                    else:
                        screen.blit(self.cb123, (0, 700))
                elif "bottle" in self.inventory:
                    screen.blit(self.cb124, (0, 700))
                else:
                    screen.blit(self.cb12, (0, 700))
            elif "name" in self.inventory:
                if "bottle" in self.inventory:
                    if "witness" in self.inventory:
                        screen.blit(self.cb1345, (0, 700))
                    else:
                        screen.blit(self.cb134, (0, 700))
                else:
                    screen.blit(self.cb13, (0, 700))
            elif "bottle" in self.inventory:
                screen.blit(self.cb14, (0, 700))
            else:
                screen.blit(self.cb1, (0, 700))
        else:
            screen.blit(self.default_clue_bar, (0, 700))
                        
    def move(self, x_adj, y_adj, currentBg):
        x = min(self.rect.x + x_adj, currentBg.rect.width - self.rect.width)
        x = max(0, x)
        self.rect.x = x
        self.rect.y = self.rect.y + y_adj
        if x_adj != 0:
            self.moved = self.moved +1
            if self.moved > 5:
                self.current_step = (self.current_step + 1) % 4
                self.moved = 0
    def pickupItem(self, item):
        self.inventory.add(item)
                                 
    def talking_pos(self, text_image, left, scene):
        l = self.rect.left
        t = self.rect.top
        w = text_image.get_rect().width
        h = text_image.get_rect().height
        if self.direction:
            if left:
                l = l + self.rect.width - 100 - w
                t = t + 75 - h
            else:
                l = l + self.rect.width + 100
                t = t + 75 - h

        else:
            if left:
                l = l - 50 - w
                t = t + 75 - h
            else:
                l = l + 150
                t = t + 75 - h

        #make sure we don't render off screen
        l = max(0, l)
        l = min(l, 1300 - w)
        t = max(0, t)
        t = min(t, scene.rect.height - h)       
        return (l, t)
                                 
    def say(self, line, scene):
        place_to_say = self.talking_pos(line[0], line[1], scene)
        self.screen.blit(line[0], place_to_say)
        

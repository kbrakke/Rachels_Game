import pygame, sys
from sets import Set
from player import Player
from npc import Npc

WIN_WIDTH = 1300
WIN_HEIGHT = 1010
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

def load_image(image_name):
    return pygame.image.load(image_name).convert_alpha()

class PythonGame:
    def __init__(self):
        #Dictionary of potential background images
        self.scenes = {}
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.base = pygame.Surface(self.screen.get_size()).convert()
        self.base.fill((255, 255, 255))
        self.player = Player(self.screen)
        self.threshold = 150
        self.timer = 0
        self.rising = False
        self.intro_1 = load_image('./Cutscenes/DRGStartComic1Small.jpg')
        self.intro_2 = load_image('./Cutscenes/DRGStartComic2Small.jpg')
        self.end_1 = load_image('./Cutscenes/DRGEndComic1Small.jpg')
        self.end_2 = load_image('./Cutscenes/DRGEndComic2Small.jpg')
        clothespic = load_image('./Items/detectiveClothes.png')
        needlepic = load_image('./Items/clue1Ons.png')
        racoonpic = load_image('./Items/clue2Ons.png')
        bottlepic = load_image('./Items/clue3Ons.png')
        ppic = load_image('./Npcs/person1.png')
        thugpic = load_image('./Npcs/person2.png')
        crazy_manpic = load_image('./Npcs/person3.png')
        prost = Npc(ppic, 400, 200, "prostitute", self.screen)
        thug = Npc(thugpic, 600, 90, "thug", self.screen)
        crazy_man = Npc(crazy_manpic, 700, 300, "crazy_man", self.screen)
        clothes = Item(clothespic, 450, 200, "clothes")
        needle = Item(needlepic, 700, 600, "needle")
        racoon = Item(racoonpic, 400, 550, "racoon")
        bottle = Item(bottlepic, 150, 250, "bottle")
        scene1 = Scene(load_image('./Backgrounds/background1.png'),
                       {"clothes" : clothes, "needle" : needle},
                       [],
                       self.screen,
                       [Doorway(pygame.Rect(0, 0, 80, 1000), "scene2", load_image("./Interaction/toMainStreet.png"))])
        scene2 = Scene(load_image('./Backgrounds/background2.png'),
                       {"racoon" : racoon},
                       [],
                       self.screen,
                       [Doorway(pygame.Rect(650, 0, 80, 1000), "scene1", load_image("./Interaction/toRichyGAlley.png")),
                        Doorway(pygame.Rect(0, 0, 80, 1000), "scene3", load_image("./Interaction/toMainStreet.png"))])
        scene3 = Scene(load_image('./Backgrounds/background3.png'),
                       {},
                       [prost],
                       self.screen,
                       [Doorway(pygame.Rect(1000, 0, 80, 1000), "scene2", load_image("./Interaction/toMainStreet.png")),
                        Doorway(pygame.Rect(100, 0, 80, 1000), "scene4", load_image("./Interaction/toOtherAlley.png"))])
        scene4 = Scene(load_image('./Backgrounds/background4.png'),
                       {},
                       [thug],
                       self.screen,
                       [Doorway(pygame.Rect(0, 0, 80, 1000), "scene3", load_image("./Interaction/toMainStreet.png")),
                        Doorway(pygame.Rect(1000, 0, 80, 1000), "scene5", load_image("./Interaction/toOtherAlley.png"))])
        scene5 = Scene(load_image('./Backgrounds/background5.png'),
                       {"bottle" : bottle},
                       [crazy_man],
                       self.screen,
                       [Doorway(pygame.Rect(0, 0, 80, 1000), "scene4", load_image("./Interaction/toOtherAlley.png"))])         
        self.drunk_meter = DrunkMeter("med", self.screen)
        self.scenes["scene1"] = scene1
        self.scenes["scene2"] = scene2
        self.scenes["scene3"] = scene3
        self.scenes["scene4"] = scene4
        self.scenes["scene5"] = scene5
        self.current_scene = "scene1"
        self.screen.blit(self.base, (0,0))
        self.drunk_meter.draw()
        self.player.move(200, 160, self.scenes[self.current_scene])

    def update(self, movement):
        if(self.drunk_meter.state == "full"):
            if movement == 7:
                movement = 2
            elif movement == -7:
                movement = -2
        self.player.move(movement, 0, self.scenes[self.current_scene])
        self.screen.blit(self.base, (0,0))       
        self.scenes[self.current_scene].draw(self.player)
        self.drunk_meter.draw()
        self.player.draw(self.screen)
        pygame.display.update()
        self.timer = self.timer + 1
        if(self.timer >= self.threshold):
            self.timer = 0
            self.drunk_meter.next_state()
            self.burp()
        if(self.drunk_meter.state == "empty"):
            self.drink()
            self.drunk_meter.next_state()
        pygame.time.delay(int(1000/30))

    def run(self):
        movement = 0
        game_won = False
        #intial cutscene
        self.screen.blit(self.base, (0,0)) 
        self.screen.blit(self.intro_1, (0,0))
        pygame.display.update()
        go_on = False
        while not go_on:
             for event in pygame.event.get():
                pygame.time.delay(int(1000/30))
                if event.type == pygame.KEYDOWN:
                    go_on = True
        self.screen.blit(self.base, (0,0)) 
        self.screen.blit(self.intro_2, (0,0))
        pygame.display.update()
        go_on = False
        while not go_on:
             for event in pygame.event.get():
                pygame.time.delay(int(1000/30))
                if event.type == pygame.KEYDOWN:
                    go_on = True                    
        #First dialog to start the game
        self.update(movement)
        self.converse(self.player, self.player.start_lines1 , None, [])
        while not game_won:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.quit()
                        sys.exit()
                    if event.key == pygame.K_LEFT:
                        self.player.direction = True
                        movement = -7
                    if event.key == pygame.K_RIGHT:
                        movement = 7
                        self.player.direction = False
                    if event.key == pygame.K_SPACE:
                        ret = self.scenes[self.current_scene].interact(self.player)
                        if ret != None:
                            self.update(0)
                            if ret[0] == "item":
                                if(ret[1] == "clothes"):
                                    self.converse(self.player, self.player.clothes_lines, None, [])
                                if(ret[1] == "needle"):
                                    self.converse(self.player, self.player.needle_lines, None, [])
                                if(ret[1] == "racoon"):
                                    self.converse(self.player, self.player.racoon_lines, None, [])
                                if(ret[1] == "bottle"):
                                    self.converse(self.player, self.player.bottle_lines, None, [])                                    
                            elif ret[0] == "door":
                                self.scenes[ret[1]].enter(self.player, self.current_scene)
                                self.current_scene =  ret[1]
                            elif ret[0] == "npc":
                                if(ret[1] == "prostitute"):
                                    prost = self.scenes[self.current_scene].npcs[0]
                                    if(self.player.met_prostitute):
                                        if(self.player.met_thug):
                                            self.converse(self.player, self.player.prost_final_lines, prost, prost.prost_final_lines)
                                            self.player.pickupItem("name")
                                        else:
                                            self.converse(self.player, self.player.prost_initial_lines, prost, prost.prost_initial_lines)    
                                    else:
                                        self.player.met_prostitute = True
                                        self.converse(self.player, self.player.prost_initial_lines, prost, prost.prost_initial_lines)
                                if(ret[1] == "thug"):
                                    self.player.met_thug = True
                                    thug = self.scenes[self.current_scene].npcs[0]
                                    if("bottle" in self.player.inventory and "name" in self.player.inventory):
                                        self.converse(self.player, self.player.thug_final_lines, thug, thug.thug_final_lines)
                                        self.player.pickupItem("witness")
                                    elif("name" in self.player.inventory):
                                        self.converse(self.player, self.player.thug_secondary_lines, thug, thug.thug_secondary_lines)
                                    else:
                                        self.converse(thug, thug.thug_initial_lines, self.player, self.player.thug_initial_lines)
                                if(ret[1] == "crazy_man"):
                                    crazy_man = self.scenes[self.current_scene].npcs[0]
                                    if(self.player.met_crazy_man):
                                        if(self.player.confronted_crazy_man):
                                            if(self.player.proved_crazy_man):
                                                if("racoon" in self.player.inventory):
                                                    self.converse(self.player, self.player.crazy_man_final_lines, crazy_man, crazy_man.crazy_man_final_lines)
                                                    game_won = True
                                                else:
                                                    self.converse(self.player, self.player.crazy_man_tertiary_lines, crazy_man, crazy_man.crazy_man_tertiary_lines)
                                            elif("witness" in self.player.inventory):
                                                self.player.proved_crazy_man = True
                                                self.converse(self.player, self.player.crazy_man_tertiary_lines, crazy_man, crazy_man.crazy_man_tertiary_lines)
                                            else:
                                                self.converse(self.player, self.player.crazy_man_secondary_lines, crazy_man, crazy_man.crazy_man_secondary_lines)                                                
                                        elif("bottle" in self.player.inventory):
                                            self.player.confronted_crazy_man = True
                                            self.converse(self.player, self.player.crazy_man_secondary_lines, crazy_man, crazy_man.crazy_man_secondary_lines)
                                        else:
                                            self.converse(crazy_man, crazy_man.crazy_man_initial_lines, None, [])
                                    else:
                                        self.player.met_crazy_man = True
                                        self.converse(crazy_man, crazy_man.crazy_man_initial_lines, None, [])
                            elif ret[0] == "event":
                                if (ret[1] == "find_clothes"):
                                    self.converse(self.player, self.player.find_clothes_lines, None, [])
                                if(ret[1] == "find_needle"):
                                    self.converse(self.player, self.player.find_needle_lines, None, [])
                if event.type == pygame.KEYUP:
                    movement = 0
            self.update(movement)
        #final cutscene
        self.screen.blit(self.base, (0,0)) 
        self.screen.blit(self.end_1, (0,0))
        pygame.display.update()
        go_on = False
        while not go_on:
             for event in pygame.event.get():
                pygame.time.delay(int(1000/30))
                if event.type == pygame.KEYDOWN:
                    go_on = True
        self.screen.blit(self.base, (0,0)) 
        self.screen.blit(self.end_2, (0,0))
        pygame.display.update()
        go_on = False
        while not go_on:
             for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    go_on = True
             pygame.time.delay(int(1000/30))
        while 1:
            pygame.time.delay(int(1000/30))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    pygame.display.quit()
                    sys.exit()
            
    def converse(self, subject1, lines1, subject2, lines2):
        lines1_pos = 0
        lines2_pos = 0
        while ((lines1_pos < len(lines1)) or (lines2_pos < len(lines2))):
            if lines1[lines1_pos] != None:
                subject1.say(lines1[lines1_pos], self.scenes[self.current_scene])
                pygame.display.update()
                self.screen.blit(self.base, (0,0))       
                self.scenes[self.current_scene].draw(self.player)
                self.drunk_meter.draw()
                self.player.draw(self.screen)
                wait = True
                while wait:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            wait = False
            lines1_pos += 1
            if(subject2 != None):
                if(lines2_pos < len(lines2)):
                    if lines2[lines2_pos] != None:
                        subject2.say(lines2[lines2_pos], self.scenes[self.current_scene])           
                        pygame.display.update()
                        self.screen.blit(self.base, (0,0))  
                        self.scenes[self.current_scene].draw(self.player)
                        self.drunk_meter.draw()
                        self.player.draw(self.screen)
                        wait = True
                        while wait:
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    wait = False
            lines2_pos += 1
    def drink(self):
        self.screen.blit(self.base, (0,0))       
        self.scenes[self.current_scene].draw(self.player)
        self.drunk_meter.draw()
        self.player.draw(self.screen, True)
        pygame.display.update()
        pygame.time.delay(int(1500))
        self.player.say(self.player.burp, self.scenes[self.current_scene])
        pygame.display.update()
        pygame.time.delay(int(1500) )                
        self.burp()
        
    def burp(self):
        self.screen.blit(self.base, (0,0))       
        self.scenes[self.current_scene].draw(self.player)
        self.drunk_meter.draw()
        self.player.draw(self.screen)
        self.player.say(self.player.burp, self.scenes[self.current_scene])
        pygame.display.update()
        pygame.time.delay(int(500))
        

            


class Scene(object):
    def __init__(self, background, items, npcs, screen, exits):
        self.interaction_images = {"item" : load_image("./Interaction/space.png"),
                                   "npc" : load_image("./Interaction/talk.png")}
        self.background = background
        self.items = items
        self.npcs = npcs
        self.exits = exits
        self.screen = screen
        self.rect = background.get_rect()
    def draw(self, player):
        self.screen.blit(self.background, self.rect)
        for itemName in self.items:
            self.items[itemName].draw(self.screen)
            if(player.rect.colliderect(self.items[itemName].rect)):
                self.showInteraction("item")
        for point in self.exits:
            if(player.rect.colliderect(point.rect)):
                self.showInteraction(point)
        for npc in self.npcs:
            npc.draw()
            if(player.rect.colliderect(npc.rect)):
                self.showInteraction("npc")
                
    def showInteraction(self, subject):
        if subject == "npc":
            i = self.interaction_images["npc"]
        elif subject == "item":
            i = self.interaction_images["item"]
        else:
            i = subject.goto_img
        r = i.get_rect()
        r.x = int(self.rect.width/2) - int(r.width/2)
        r.y = 5
        self.screen.blit(i, r)
    def hideInteraction(self):
        r = self.interact_img.get_rect()
        r.x = int(self.rect.width/2) - int(r.width/2)
        r.y = 50
        self.screen.blit(self.background, r, r)
    def interact(self, player):
        item_to_remove = None
        for itemName in self.items:
            if(player.rect.colliderect(self.items[itemName].rect)):
                if("clothes" in player.inventory or itemName == "clothes"):
                    self.items[itemName].remove(self.screen, self.background)
                    player.pickupItem(itemName)
                    item_to_remove = itemName
                else:
                    return("event", "find_clothes")
        if (item_to_remove != None):
            del self.items[item_to_remove]
            return ("item", item_to_remove)
        scene_to_go_to = None
        for door in self.exits:
            if(player.rect.colliderect(door.rect)):
                if("clothes" in player.inventory):
                    if("needle" in player.inventory):
                        return ("door", door.goto)
                    else:
                        return("event", "find_needle")
                else:
                    return ("event", "find_clothes")
            
        for npc in self.npcs:
            if(player.rect.colliderect(npc.rect)):
                return("npc", npc.name)
        return None
    def enter(self, player, last_scene):
        for door in self.exits:
            if door.goto == last_scene:
                player.rect.x = door.rect.x
                
class DrunkMeter(pygame.sprite.Sprite):
    def __init__(self, state, screen):
        self.full = load_image('./drunkMeter/drunkMeter.png')
        self.med = load_image('./drunkMeter/middleMeter.png')
        self.empty = load_image('./drunkMeter/soberMeter.png')
        self.state = state
        self.past_state = "full"
        self.screen = screen
        self.next_state_dict = {"full" : {"med" : "med"}, "med" : {"full" : "empty", "empty" : "full"}, "empty" : {"med" : "med"}}
    def draw(self):
        if self.state == "full":
            self.screen.blit(self.full, (1060, 0))
        elif self.state == "med":
            self.screen.blit(self.med, (1060, 0))
        elif self.state == "empty":
            self.screen.blit(self.empty, (1060, 0))
    def next_state(self):
        next_state = self.next_state_dict[self.state][self.past_state]
        self.past_state = self.state
        self.state = next_state
            
class Item(pygame.sprite.Sprite):
    def __init__(self, image, x, y, name):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = name
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    def remove(self, screen, image):
        screen.blit(image, self.rect, self.rect)
        

            
        
class Doorway(object):
    def __init__(self, rect, goto, goto_img):
        self.rect = rect
        self.goto = goto
        self.goto_img = goto_img

        
game = PythonGame()
game.run()

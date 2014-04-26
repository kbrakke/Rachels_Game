import pygame, sys
from sets import Set

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
        self.player = Player()
        clothespic = load_image('./Items/detectiveClothes.png')
        needlepic = load_image('./Items/clue1Ons.png')
        ppic = load_image('./Npcs/person1.png')
        #prost = Npc(ppic, 400, 500, "prostitute", npc1generic1, npc1partial1, npc1found1, npc1final1, ["needle",],self.screen)
        clothes = Item(clothespic, 450, 200, "clothes")
        needle = Item(needlepic, 700, 600, "needle")
        scene1 = Scene(load_image('./Backgrounds/background1.png'),
                       {"clothes" : clothes, "needle" : needle},
                       [],
                       self.screen,
                       [Doorway(pygame.Rect(0, 0, 80, 1000), "scene2", load_image("./Interaction/toMainStreet.png"))])
        scene2 = Scene(load_image('./Backgrounds/background2.png'),
                       {},
                       [],
                       self.screen,
                       [Doorway(pygame.Rect(650, 0, 80, 1000), "scene1", load_image("./Interaction/toRichyGAlley.png")),
                        Doorway(pygame.Rect(0, 0, 80, 1000), "scene3", load_image("./Interaction/toMainStreet.png"))])
        scene3 = Scene(load_image('./Backgrounds/background3.png'),
                       {},
                       [],
                       self.screen,
                       [Doorway(pygame.Rect(1000, 0, 80, 1000), "scene2", load_image("./Interaction/toMainStreet.png")),
                        Doorway(pygame.Rect(100, 0, 80, 1000), "scene4", load_image("./Interaction/toOtherAlley.png"))])
        scene4 = Scene(load_image('./Backgrounds/background4.png'),
                       {},
                       [],
                       self.screen,
                       [Doorway(pygame.Rect(0, 0, 80, 1000), "scene3", load_image("./Interaction/toMainStreet.png")),
                        Doorway(pygame.Rect(1000, 0, 80, 1000), "scene5", load_image("./Interaction/toOtherAlley.png"))])
        scene5 = Scene(load_image('./Backgrounds/background5.png'),
                       {},
                       [],
                       self.screen,
                       [Doorway(pygame.Rect(0, 0, 80, 1000), "scene4", load_image("./Interaction/toOtherAlley.png"))])         
        self.drunkMeter = DrunkMeter("full", self.screen)
        self.scenes["scene1"] = scene1
        self.scenes["scene2"] = scene2
        self.scenes["scene3"] = scene3
        self.scenes["scene4"] = scene4
        self.scenes["scene5"] = scene5
        self.current_scene = "scene1"
        self.screen.blit(self.base, (0,0))
        self.drunkMeter.draw()
        self.player.move(10, 160, self.scenes[self.current_scene])

    def update(self, movement): 
        self.player.move(movement, 0, self.scenes[self.current_scene])
        self.screen.blit(self.base, (0,0))       
        self.scenes[self.current_scene].draw(self.player)
        self.drunkMeter.draw()
        self.player.draw(self.screen)
        pygame.display.update()
        pygame.time.delay(int(1000/30))

    def run(self):
        movement = 0
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.quit()
                        sys.exit()
                    if event.key == pygame.K_LEFT:
                        self.player.direction = True
                        movement = -5
                    if event.key == pygame.K_RIGHT:
                        movement = 5
                        self.player.direction = False
                    if event.key == pygame.K_SPACE:
                        ret = self.scenes[self.current_scene].interact(self.player)
                        if ret != None:
                           self.scenes[ret].enter(self.player, self.current_scene)
                           self.current_scene =  ret
                           #print ret
                if event.type == pygame.KEYUP:
                    movement = 0
            self.update(movement)       
            


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
                self.items[itemName].remove(self.screen, self.background)
                player.pickupItem(itemName)
                item_to_remove = itemName
        if (item_to_remove != None):
            del self.items[item_to_remove]
        scene_to_go_to = None
        for door in self.exits:
            if(player.rect.colliderect(door.rect)):
                scene_to_go_to = door.goto
        if scene_to_go_to != None:
            return scene_to_go_to
        for npc in self.npcs:
            if(player.rect.colliderect(npc.rect)):
                self.hideInteraction()
                npc.speak(player)
        return None
    def enter(self, player, last_scene):
        for door in self.exits:
            if door.goto == last_scene:
                player.rect.x = door.rect.x
                
class DrunkMeter(pygame.sprite.Sprite):
    def __init__(self, state, screen):
        self.full = load_image('./DrunkMeter/drunkMeter.png')
        self.med = load_image('./DrunkMeter/middleMeter.png')
        self.empty = load_image('./DrunkMeter/soberMeter.png')
        self.state = state
        self.screen = screen
    def draw(self):
        if self.state == "full":
            self.screen.blit(self.full, (1060, 0))
        elif self.state == "med":
            self.screen.blit(self.med, (1060, 0))
        elif self.state == "empty":
            self.screen.blit(self.empty, (1060, 0))
            
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
        
class Npc(pygame.sprite.Sprite):
    def __init__(self, image, x, y, name, generic_lines, partial_lines, found_line, final_lines, trigger_items, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = name
        self.generic_lines = generic_lines
        self.partial_lines = partial_lines
        self.found_line = found_line
        self.final_lines = final_lines
        self.trigger_items = trigger_items
        self.quest_complete = False
        self.screen = screen
    def draw(self):
        self.screen.blit(self.image, self.rect)
    def speak_line(self, line):
        r = line.get_rect()
        r.x = HALF_WIDTH - int(r.width/2)
        r.y = 50
        self.screen.blit(line, r)
        pygame.display.update()
        pygame.time.delay(700)
    def speak(self, player):
        contains_count = 0
        for item in self.trigger_items:
            if(item in player.inventory.keys()):
                contains_count = contains_count + 1
        if contains_count == len(self.trigger_items):
            if(self.quest_complete):
                self.speak_line(self.final_lines)
            else:
                self.speak_line(self.found_line)
                self.quest_complete = True
        elif contains_count > 0:
            self.speak_line(self.partial_lines)
        else:
            self.speak_line(self.generic_lines)
            
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.direction = False
        self.current_step = 0
        self.moved = 0
        self.rg_images = [load_image("./Richie/RGIdleWalk1.png"),load_image("./Richie/RGWalk2.png"),load_image("./Richie/RGIdleWalk1.png"),load_image("./Richie/RGWalk3.png")]
        self.drg_images = [load_image("./Richie/DRGstandWalk2.png"),load_image("./Richie/DRGWalk1.png"),load_image("./Richie/DRGstandWalk2.png"),load_image("./Richie/DRGWalk3.png")]
        self.default_clue_bar = load_image('./ClueBar/clueBar.png')
        self.cb12345 = load_image('./ClueBar/clueBar12345.png')
        
        self.cb1234 = load_image('./ClueBar/clueBar1234.png')
        self.cb1345 = load_image('./ClueBar/clueBar1345.png')

        self.cb124 = load_image('./ClueBar/clueBar124.png')
        self.cb134 = load_image('./ClueBar/clueBar134.png')
        self.cb123 = load_image('./ClueBar/clueBar123.png')
        
        self.cb14 = load_image('./ClueBar/clueBar14.png')
        self.cb12 = load_image('./ClueBar/clueBar12.png')        

        self.cb1 = load_image('./ClueBar/clueBar1.png')
        
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
                    if "booze" in self.inventory:
                        if "witness" in self.inventory:
                            screen.blit(self.cb12345, (0, 720))
                        else:
                            screen.blit(self.cb1234, (0, 720))
                    else:
                        screen.blit(self.cb123, (0, 720))
                elif "booze" in self.inventory:
                    screen.blit(self.cb124, (0, 720))
                else:
                    screen.blit(self.cb12, (0, 720))
            elif "name" in self.inventory:
                if "booze" in self.inventory:
                    if "witeness" in self.inventory:
                        screen.blit(self.cb1345, (0, 720))
                    else:
                        screen.blit(self.cb124, (0, 720))
            elif "booze" in self.inventory:
                screen.blit(self.cb14, (0, 720))
            else:
                screen.blit(self.cb1, (0, 720))
        else:
            screen.blit(self.default_clue_bar, (0, 720))
                        
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
        
class Doorway(object):
    def __init__(self, rect, goto, goto_img):
        self.rect = rect
        self.goto = goto
        self.goto_img = goto_img

        
game = PythonGame()
game.run()

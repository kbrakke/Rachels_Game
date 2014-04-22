import pygame, sys

WIN_WIDTH = 1280
WIN_HEIGHT = 720
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

def load_image(image_name):
    return pygame.image.load(image_name).convert()

class PythonGame:
    def __init__(self):
        #Dictionary of potential background images
        self.scenes = {}
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT+100))
        self.player = Player(load_image('persontest.png'))
        item1pic = load_image('testitem1.png')
        item2pic = load_image('testitem2.png')
        item3pic = load_image('testitem3.png')
        npc1pic = load_image('npctest1.png')
        npc1final1 = load_image('npc1final1.png')
        npc1generic1 = load_image('npc1generic1.png')
        npc1partial1 = load_image('npc1partial1.png')
        npc1found1 = load_image('npc1found1.png')
        npc2pic = load_image('npctest2.png')
        npc1 = Npc(npc1pic, 400, 600, "npc1",npc1generic1, npc1partial1, npc1found1, npc1final1, ["item1",],self.screen)
        npc2 = Npc(npc2pic, 600, 600, "npc2",npc1generic1, npc1partial1, npc1found1, npc1final1, ["item2",],self.screen)
        item1 = Item(item1pic, 200, 600, "item1")
        item2 = Item(item2pic, 700, 600, "item2")
        item3 = Item(item3pic, 1200, 600, "item3")
        scene1 = Scene(load_image('testbglong1.png'),
                       {"item1" : item1, "item2" : item2},
                       [npc1,],
                       self.screen,
                       [Doorway(pygame.Rect(250, 455, 80, 150), "scene2"),
                        Doorway(pygame.Rect(890, 480, 65, 120), "scene3")])
        scene2 = Scene(load_image('teststreet3.png'),
                       {"item3" : item3},
                       [npc2,],
                       self.screen,
                       [Doorway(pygame.Rect(60, 285, 100, 340), "scene1")])
        
        self.scenes["scene1"] = scene1
        self.scenes["scene2"] = scene2
        self.current_scene = "scene1"
        self.hud = load_image('testhud1.png')
        self.screen.blit(self.hud, pygame.Rect(0, 720, WIN_WIDTH, WIN_HEIGHT))
        self.player.move(100, 520)

    def update(self, movement):
        self.player.move(movement, 0)
        self.scenes[self.current_scene].draw(self.player)
        self.player.draw(self.screen)
        pygame.display.update()
        pygame.time.delay(100)

    def run(self):
        movement = 0
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.quit()
                        sys.exit()
                    if event.key == pygame.K_LEFT:
                        movement = -10
                    if event.key == pygame.K_RIGHT:
                        movement = 10
                    if event.key == pygame.K_SPACE:
                        ret = self.scenes[self.current_scene].interact(self.player)
                        if ret != None:
                           self.scenes[ret].enter(self.player, self.current_scene)
                           self.current_scene =  ret
                if event.type == pygame.KEYUP:
                    movement = 0
            self.update(movement)       
            


class Scene(object):
    def __init__(self, background, items, npcs, screen, exits):
        self.interact_img = pygame.image.load('can_interact.png').convert()
        self.background = background
        self.items = items
        self.npcs = npcs
        self.exits = exits
        self.rect = (0,0, 1280, 720)
        self.screen = screen
    def draw(self, player):
        self.screen.blit(self.background, self.rect)
        for itemName in self.items:
            self.items[itemName].draw(self.screen)
            if(player.rect.colliderect(self.items[itemName].rect)):
                self.showInteraction()
        for point in self.exits:
            if(player.rect.colliderect(point.rect)):
                self.showInteraction()
        for npc in self.npcs:
            npc.draw()
            if(player.rect.colliderect(npc.rect)):
                self.showInteraction()
                
    def showInteraction(self):
        r = self.interact_img.get_rect()
        r.x = HALF_WIDTH - int(r.width/2)
        r.y = 50
        self.screen.blit(self.interact_img, r)
    def hideInteraction(self):
        r = self.interact_img.get_rect()
        r.x = HALF_WIDTH - int(r.width/2)
        r.y = 50
        self.screen.blit(self.background, r, r)
    def interact(self, player):
        item_to_remove = None
        for itemName in self.items:
            if(player.rect.colliderect(self.items[itemName].rect)):
                self.items[itemName].remove(self.screen, self.background)
                player.pickupItem(self.items[itemName])
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
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.inventory = {}
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        ipos = 50
        for itemName in self.inventory:
            i = self.inventory[itemName]
            rect = i.image.get_rect()
            rect.x = ipos
            rect.y = 750
            screen.blit(i.image, rect)
            ipos = ipos + 120
    def move(self, x_adj, y_adj):
        x = min(self.rect.x + x_adj, WIN_WIDTH - self.rect.width)
        x = max(0, x)
        self.rect.x = x
        self.rect.y = self.rect.y + y_adj
    def pickupItem(self, item):
        self.inventory[item.name] = item
class Doorway(object):
    def __init__(self, rect, goto):
        self.rect = rect
        self.goto = goto

        
game = PythonGame()
game.run()

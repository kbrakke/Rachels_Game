import pygame, sys

WIN_WIDTH = 1280
WIN_HEIGHT = 720
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

class PythonGame:
    def __init__(self):
        #Dictionary of potential background images
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT+100))
        self.player = Player(pygame.image.load('persontest.png').convert())
        self.scene = Scene(pygame.image.load('testbglong1.png'), None, None)

    def update(self, movement):
        self.player.move(movement, 0)
        self.scene.draw(self.screen)
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
                if event.type == pygame.KEYUP:
                    movement = 0
            self.update(movement)
            


class Scene(object):
    def __init__(self, background, items, npcs):
        self.background = background
        self.items = items
        self.npcs = npcs
        self.rect = (0,0, 1280, 720)
    def draw(self, screen):
        screen.blit(self.background, self.rect)
##        for item in self.items:
##            item.draw(screen)
##        for npc in self.npcs:
##            pass
            
class Item(pygame.sprite.Sprite):
    def __init__(self, image, width, height, x, y, name):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.width = width
        self.height =  height
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.name = name
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    def move(self, x_adj, y_adj, screen, background):
        screen.blit(background, self.rect, self.rect)
        self.x = self.x + x_adj
        self.y = self.y + y_adj
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)  
        self.draw(screen)
        
class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.inventory = {}
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    def move(self, x_adj, y_adj):
        x = min(self.rect.x + x_adj, WIN_WIDTH - self.rect.width)
        x = max(0, x)
        self.rect.x = x
        self.rect.y = self.rect.y + y_adj
    def pickupItem(item):
        self.inventory[item.name] = item    

        
game = PythonGame()
game.run()

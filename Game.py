import pygame, sys

class PythonGame:
    def __init__(self):
        #Dictionary of potential background images
        self.backgrounds = {}
        self.scenes = {}
        self.interactive = {}
        #TODO: self.npcs{}
        
        pygame.init()
        self.screen = pygame.display.set_mode((800, 700))
        self.player = Item(pygame.image.load('persontest.png').convert(), 40, 60, 400, 540)
        #Give the player his list of images
        #self.player['default'] = pygame.image.load('persontest.png').convert()
        #Initialize the background list
        #self.backgrounds["grey_street"] = pygame.image.load('teststreet1.png').convert()
        #self.backgrounds["red_street"] = pygame.image.load('teststreet2.png').convert()
        #self.screen.blit(self.backgrounds["grey_street"], (0, 0))
        self.scenes["scene1"] = Scene(pygame.image.load('teststreet1.png').convert(),
                                      [Item(pygame.image.load('testitem1.png').convert(),
                                            30,
                                            60,
                                            700,
                                            300),
                                       Item(pygame.image.load('testitem2.png').convert(),
                                            40,
                                            60,
                                            100,
                                            300)],
                                      800,
                                      600)
        self.currentScene = "scene1"
        self.scenes[self.currentScene].draw(self.screen)

    def _update(self, movement):
        #player_rect = pygame.Rect(self.player_pos, self.player_height, 40, 60)
        #self.screen.blit(self.backgrounds["grey_street"], player_rect, player_rect)
        #self.screen.blit(self.player['default'], player_rect.move(movement, 0))
        #self.player_pos += movement
        self.player.move(movement, 0, self.screen, self.scenes[self.currentScene].background)
        pygame.display.update()
        pygame.time.delay(100)

    def _run(self):
        while 1:
            movement = 0
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.quit()
                        sys.exit()
                    if event.key == pygame.K_LEFT:
                        movement = -10
                    if event.key == pygame.K_RIGHT:
                        movement = 10
                #if event.type == pygame.KEYUP:
                #    movement = 0
                #else:
                #    movement = 0
                self._update(movement)        
            #print('EVENT: '+str(event))
            


class Scene:
    def __init__(self, background, items, width, height):
        self.background = background
        self.items = items
        self.width = width
        self.height = height
    def draw(self, screen):
        screen.blit(self.background, (0,0))
        for item in self.items:
            print("draw item")
            item.draw(screen)
        
class Item:
    def __init__(self, image, width, height, x, y):
        self.image = image
        self.width = width
        self.height =  height
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)       
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    def move(self, x_adj, y_adj, screen, background):
        screen.blit(background, self.rect, self.rect)
        self.x = self.x + x_adj
        self.y = self.y + y_adj
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)  
        self.draw(screen)
        
game = PythonGame()
game._run()

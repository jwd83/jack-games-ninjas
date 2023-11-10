import sys
import pygame
from scripts.entities import PhysicsEntity
from scripts.utils import load_image, load_images
from scripts.tilemap import Tilemap

class Game:
    def __init__(self):

        pygame.init()
        pygame.display.set_caption('Jack Ninjas!')

        # our window is 1280x720, but we want to render at a lower resolution
        self.screen = pygame.display.set_mode((1920, 1080))

        # we will render at 320x180 and then scale it up by 4x
        self.display = pygame.Surface((320, 180))

        self.clock = pygame.time.Clock()

        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
        }
        # print our loaded assets
        # print(self.assets)

        self.player = PhysicsEntity(self, 'player', (75,75), (8,15))

        self.tilemap = Tilemap(self, tile_size = 16)


        self.movement = [False, False]

    def perform_quit(self):
        pygame.quit()
        sys.exit()

    def get_events(self):
        # get our events so windows thinks we are responding
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.perform_quit()

            if event.type == pygame.KEYDOWN:
                # if the user presses escape or F5 key, quit the event loop.
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_F5:
                    self.perform_quit()

                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.movement[0] = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.movement[1] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.movement[0] = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.movement[1] = False

    def clear_screen(self):
        # let's go for a sky blue
        self.display.fill((15,220,250))

    def run(self):

        while True:
            self.clear_screen()

            self.tilemap.render(self.display)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display)

            print(self.tilemap.physics_rects_around(self.player.pos))

            # we finished drawing our frame, lets render it to the screen and
            # get our input events ready for the next frame and sleep for a bit
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.get_events()
            self.clock.tick(60) # run at 60 fps

Game().run()

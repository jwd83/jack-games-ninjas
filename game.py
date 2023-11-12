import sys
import pygame
from scripts.entities import PhysicsEntity, Player
from scripts.utils import load_image, load_images, Animation
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds


class Game:
    def __init__(self):

        pygame.init()
        pygame.display.set_caption('Jack Ninjas!')

        # set our output windows size
        self.screen = pygame.display.set_mode((1280, 720))

        # we will render at 320x180 and then scale it up by 4x
        self.display = pygame.Surface((320, 180))

        self.clock = pygame.time.Clock()

        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=8),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump'), img_dur=5),
            'player/fall': Animation(load_images('entities/player/fall')),
            'player/slide': Animation(load_images('entities/player/slide'), img_dur=5),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide'), img_dur=5),

        }
        # print our loaded assets
        print(self.assets)

        self.clouds = Clouds(self.assets['clouds'], count=16)
        self.player = Player(self, (75, 75), (8, 15))

        self.tilemap = Tilemap(self, tile_size=16)

        self.movement = [False, False]

        # setup our pseudo camera
        self.scroll = [0, 0]

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
                if event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_UP:
                    if self.player.velocity[1] >= 0:
                        self.player.velocity[1] = -3

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.movement[0] = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.movement[1] = False

    def draw_background(self):
        # let's go for a sky blue
        # self.display.fill((15,220,250))
        self.display.blit(self.assets['background'], (0, 0))

    def run(self):

        while True:
            self.draw_background()

            # adjust camera position
            self.scroll[0] += (self.player.rect().centerx -
                               self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += ((self.player.rect().centery - 20) -
                               self.display.get_height() / 2 - self.scroll[1]) / 8
            # calculate integer scroll for rendering to fix jitter
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            # draw our clouds
            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            # draw our tilemap
            self.tilemap.render(self.display, offset=render_scroll)

            self.player.update(
                self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)

            # print(self.tilemap.physics_rects_around(self.player.pos))

            # we finished drawing our frame, lets render it to the screen and
            # get our input events ready for the next frame and sleep for a bit
            self.screen.blit(pygame.transform.scale(
                self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.get_events()
            self.clock.tick(60)  # run at 60 fps


Game().run()

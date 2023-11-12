import sys
import pygame

from scripts.utils import load_images
from scripts.tilemap import Tilemap


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Jack Ninja Editor")

        # set our output windows size
        self.screen = pygame.display.set_mode((1280, 720))

        # we will render at 320x180 and then scale it up by 4x
        self.display = pygame.Surface((320, 180))

        self.render_scale = self.screen.get_width() / self.display.get_width()

        self.clock = pygame.time.Clock()

        self.assets = {
            "decor": load_images("tiles/decor"),
            "grass": load_images("tiles/grass"),
            "large_decor": load_images("tiles/large_decor"),
            "stone": load_images("tiles/stone"),
        }
        # print our loaded assets
        print(self.assets)

        self.tilemap = Tilemap(self, tile_size=16)

        self.movement = [False, False, False, False]

        # setup our pseudo camera
        self.scroll = [0, 0]

        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        self.clicking = False
        self.right_clicking = False
        self.shift = False

    def perform_quit(self):
        pygame.quit()
        sys.exit()

    def get_events(self):
        # get our events so windows thinks we are responding
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.perform_quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left mouse button
                    self.clicking = True
                if event.button == 3:  # right mouse button
                    self.right_clicking = True
                if not self.shift:
                    # if we
                    if event.button == 4:  # mouse wheel up
                        self.tile_variant = (self.tile_variant - 1) % len(
                            self.assets[self.tile_list[self.tile_group]]
                        )
                    if event.button == 5:  # mouse wheel down
                        self.tile_variant = (self.tile_variant + 1) % len(
                            self.assets[self.tile_list[self.tile_group]]
                        )
                else:
                    if event.button == 4:  # mouse wheel up
                        self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                        self.tile_variant = 0
                    if event.button == 5:  # mouse wheel down
                        self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                        self.tile_variant = 0

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.clicking = False
                if event.button == 3:
                    self.right_clicking = False

            if event.type == pygame.KEYDOWN:
                # if the user presses escape or F5 key, quit the event loop.
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_F5:
                    self.perform_quit()

                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.movement[0] = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.movement[1] = True
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.movement[2] = True
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.movement[3] = True
                if event.key == pygame.K_LSHIFT:
                    self.shift = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.movement[0] = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.movement[1] = False
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.movement[2] = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.movement[3] = False
                if event.key == pygame.K_LSHIFT:
                    self.shift = False

    def run(self):
        while True:
            self.display.fill((0, 0, 0))

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset=render_scroll)

            current_tile_image = self.assets[self.tile_list[self.tile_group]][
                self.tile_variant
            ].copy()
            current_tile_image.set_alpha(100)

            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / self.render_scale, mpos[1] / self.render_scale)
            tile_pos = (
                int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size),
                int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size),
            )

            self.display.blit(
                current_tile_image,
                (
                    tile_pos[0] * self.tilemap.tile_size - self.scroll[0],
                    tile_pos[1] * self.tilemap.tile_size - self.scroll[1],
                ),
            )

            # create a tile
            if self.clicking:
                self.tilemap.tilemap[str(tile_pos[0]) + ";" + str(tile_pos[1])] = {
                    "type": self.tile_list[self.tile_group],
                    "variant": self.tile_variant,
                    "pos": tile_pos,
                }

            # delete a tile
            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ";" + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]

            self.display.blit(current_tile_image, (5, 5))

            # we finished drawing our frame, lets render it to the screen and
            # get our input events ready for the next frame and sleep for a bit
            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)
            )
            pygame.display.update()
            self.get_events()
            self.clock.tick(60)  # run at 60 fps


Game().run()

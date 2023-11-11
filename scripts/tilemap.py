import pygame

NEIGHBOR_OFFSETS = [
    (-1,  1), (0,  1), (1,  1),
    (-1,  0), (0,  0), (1,  0),
    (-1, -1), (0, -1), (1, -1)
]

# using a set for physics tiles is a good idea because it's faster to check if a tile is in a set than a list
# {} without a colon is a set, not a dictionary
PHYSICS_TILES = {'grass', 'stone'}

class Tilemap:
    def __init__(self, game, tile_size = 16):

        self.game = game

        self.tile_size = tile_size

        # this grid will be used for physics, it's position is based on tile size
        self.tilemap = {}

        # this will be for arbitrary tiles, their position is a raw pixel
        self.offgrid_tiles = []

        for i in range(10_000):
            # horizontal grass
            self.tilemap[str(3 + i) + ';10'] = {'type': 'grass', 'variant': 1, 'pos': (3 + i, 10)}

            # vertical stone
            self.tilemap['10;' + str(5 + i)] = {'type': 'stone', 'variant': 1, 'pos': (10, 5 + i)}

    def tiles_around(self, pos):

        tiles = []

        # // integer divide is better than casting to int after dividing for graphics/grid positions
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])

        return tiles

    def physics_rects_around(self, pos):
        # turning a tile location into a physics rect is easy
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects

    def render(self, surf, offset=(0,0)):

        # draw the offgrid tiles first
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0],tile['pos'][1] - offset[1]))


        # optimzied grid tile renderer
        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))

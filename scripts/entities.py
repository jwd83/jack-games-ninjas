import pygame

GRAVITY = 0.1
MAX_FALL_SPEED = 5

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type

        self.pos = list(pos) # create a new list so we don't modify or share with another entity
        # x position is first element in pos list
        # y position is second element in pos list

        self.size = list(size) # create a new list so we don't modify or share with another entity
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap, movement = (0, 0)):
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

        frame_movement = [movement[0] + self.velocity[0], movement[1] + self.velocity[1]]

        # handle x axis movement
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                # if we are moving right and collided with a tile
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        # handle y axis movement
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                # if we are moving right and collided with a tile
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y




        # apply gravity
        self.velocity[1] = min(MAX_FALL_SPEED, self.velocity[1] + GRAVITY)

        # reset y velocity if collided up or down
        if self.collisions['up'] or self.collisions['down']:
            self.velocity[1] = 0

    def render(self, surface, offset=(0,0)):
        surface.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))

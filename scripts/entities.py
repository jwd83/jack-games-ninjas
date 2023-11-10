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

    def update(self, tilemap, movement = (0, 0)):
        frame_movement = [movement[0] + self.velocity[0], movement[1] + self.velocity[1]]

        # apply gravity
        self.velocity[1] = min(MAX_FALL_SPEED, self.velocity[1] + GRAVITY)

        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]

    def render(self, surface):
        surface.blit(self.game.assets['player'], self.pos)

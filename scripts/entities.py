import pygame

GRAVITY = 0.1
MAX_FALL_SPEED = 5


class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type

        # create a new list so we don't modify or share with another entity
        self.pos = list(pos)
        # x position is first element in pos list
        # y position is second element in pos list

        # create a new list so we don't modify or share with another entity
        self.size = list(size)
        self.velocity = [0, 0]
        self.collisions = {"up": False, "down": False, "left": False, "right": False}
        self.action = ""
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action("idle")

    def set_action(self, action):
        # only change the animation if it's different
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + "/" + self.action].copy()
            self.animation.frame = 0

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {"up": False, "down": False, "left": False, "right": False}

        frame_movement = [
            movement[0] + self.velocity[0],
            movement[1] + self.velocity[1],
        ]

        # handle x axis movement
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                # if we are moving right and collided with a tile
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions["right"] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions["left"] = True
                self.pos[0] = entity_rect.x

        if movement[0] > 0:
            self.flip = False
        elif movement[0] < 0:
            self.flip = True

        # handle y axis movement
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                # if we are moving right and collided with a tile
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions["down"] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions["up"] = True
                self.pos[1] = entity_rect.y

        # apply gravity
        self.velocity[1] = min(MAX_FALL_SPEED, self.velocity[1] + GRAVITY)

        # reset y velocity if collided up or down
        if self.collisions["up"] or self.collisions["down"]:
            self.velocity[1] = 0

        self.animation.update()

    def render(self, surf, offset=(0, 0)):
        surf.blit(
            pygame.transform.flip(self.animation.img(), self.flip, False),
            (
                self.pos[0] - offset[0] + self.anim_offset[0],
                self.pos[1] - offset[1] + self.anim_offset[1],
            ),
        )


class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, "player", pos, size)
        self.air_time = 0

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement)
        self.air_time += 1

        if self.collisions["down"]:
            self.air_time = 0

        if self.air_time > 4:
            if self.velocity[1] < 0:
                self.set_action("jump")
            else:
                self.set_action("fall")
        elif movement[0] != 0:
            self.set_action("run")
        else:
            self.set_action("idle")

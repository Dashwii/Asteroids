from constants import *


class Asteroid:
    def __init__(self, rank):
        self.size_rank = rank
        if self.size_rank == 1:
            self.score_given = 25
            self.image = ASTEROID_SPRITES[2]
        elif self.size_rank == 2:
            self.score_given = 50
            self.image = ASTEROID_SPRITES[1]
        else:
            self.score_given = 100
            self.image = ASTEROID_SPRITES[0]
        self.angle = 0
        self.rotate_speed = random.randint(1, 3)
        self.rotated_image = pygame.transform.rotate(self.image, self.angle)
        self.width = self.rotated_image.get_width()
        self.height = self.rotated_image.get_height()
        self.hitbox_width = self.image.get_width()
        self.hitbox_height = self.image.get_height()
        self.lifespan = 0

        # Choosing random point outside of play area to spawn asteroid in
        self.ranPoint = random.choice([(random.randrange(0, WIDTH - self.width), random.choice([-1 * self.height - 5, HEIGHT + 5])),
                                       (random.choice([-1 * self.width - 5, WIDTH + 5]), random.randrange(0, HEIGHT - self.height))])
        self.x, self.y = self.ranPoint
        self.hitbox = self.rotated_image.get_rect(x=(self.x - self.width), y=(self.y - self.height))

        if self.x < WIDTH // 2:
            self.x_dir = 1
        else:
            self.x_dir = -1
        if self.y < HEIGHT // 2:
            self.y_dir = 1
        else:
            self.y_dir = -1
        self.x_velocity = self.x_dir * random.randrange(1, 3)
        self.y_velocity = self.y_dir * random.randrange(1, 3)

    def draw(self):
        WINDOW.blit(self.rotated_image, (self.x - self.width // 2, self.y - self.height // 2))

    def rotate_asteroid(self):
        self.angle = (self.angle + self.rotate_speed) % 360
        self.rotated_image = pygame.transform.rotate(self.image, self.angle)
        self.width = self.rotated_image.get_width()
        self.height = self.rotated_image.get_height()

    def move_asteroid(self):
        self.x += self.x_velocity
        self.y += self.y_velocity
        self.hitbox = pygame.Rect(self.x - self.hitbox_width // 2, self.y - self.hitbox_height // 2, self.hitbox_width, self.hitbox_height)

















































# class Asteroid:
#     def __init__(self, size, speed, position):
#         self.size = size
#
#         self.sprite_angle = 0
#         self.asteroid_sprite = ASTEROID_SPRITES[size]
#         self.rotated_asteroid_sprite = pygame.transform.rotate(self.asteroid_sprite, self.sprite_angle)
#
#         self.asteroid_rect = self.rotated_asteroid_sprite.get_rect()
#         self.asteroid_rect.x, self.asteroid_rect.y = position
#         self.asteroid_rect_middle = (self.asteroid_rect.x + (self.asteroid_rect.width // 2), self.asteroid_rect.y + (self.asteroid_rect.height // 2))
#
#         self.speed = speed
#         self.movement_angle = 0
#         self.rotation_speed = 2
#
#         self.ran_point = random.choice([(random.randrange(0, WIDTH-self.asteroid_rect.width), random.choice([-1*self.asteroid_rect.height - 5, HEIGHT + 5])),
#                                        (random.choice([-1 * self.asteroid_rect.width - 5, WIDTH + 5]), random.randrange(0, HEIGHT - self.asteroid_rect.height))])
#         self.x, self.y = self.ran_point
#         if self.x < WIDTH // 2:
#             self.xdir = 1
#         else:
#             self.xdir = -1
#         if self.y < HEIGHT // 2:
#             self.ydir = 1
#         else:
#             self.ydir = -1
#
#         self.x_velocity = self.xdir * random.randrange(1, 3)
#         self.y_velocity = self.xdir * random.randrange(1, 3)
#
#     def draw_and_rotate_asteroid(self):
#         self.rotate_asteroid_sprite()
#         WINDOW.blit(self.rotated_asteroid_sprite, (self.asteroid_rect_middle[0] - (self.rotated_asteroid_sprite.get_width() // 2), self.asteroid_rect_middle[1] - (self.rotated_asteroid_sprite.get_height() // 2)))
#
#     def rotate_asteroid_sprite(self):
#         self.sprite_angle = (self.sprite_angle + self.rotation_speed) % 360
#         self.rotated_asteroid_sprite = pygame.transform.rotate(self.asteroid_sprite, self.sprite_angle)
#
#     def move_asteroid(self):
#         self.asteroid_rect.x += self.speed
#         self.asteroid_rect.y += self.speed
#         self.asteroid_rect_middle = (self.asteroid_rect.x + (self.asteroid_rect.width // 2), self.asteroid_rect.y + (self.asteroid_rect.height // 2))
#
#     def split_asteroids(self):
#         if self.size == 2:
#             return False
#         # Larger size = smaller asteroid
#         new_asteroid_sizes = self.size + 1
#         new_asteroid_speed = self.speed + 1
#         new_asteroid_position = (self.asteroid_rect.x, self.asteroid_rect.y)
#
#         return [Asteroid(new_asteroid_sizes, new_asteroid_speed, new_asteroid_position) for _ in range(2)]








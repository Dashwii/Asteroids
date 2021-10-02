from constants import *


class ProjectileBody:
    def __init__(self, image):
        self.image = image
        self.width, self.height = self.image.get_width(), self.image.get_height()
        self.x, self.y = random.choice([(random.randrange(0, WIDTH - self.width), random.choice([-1 * self.height - 5, HEIGHT + self.height])),
                                       (random.choice([-1 * self.width - 5, WIDTH + self.width]), random.randrange(0, HEIGHT - self.height))])
        self.hitbox = self.image.get_rect(x=self.x, y=self.y)

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
        WINDOW.blit(self.image, (self.x, self.y))

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity
        self.hitbox.x, self.hitbox.y = self.x, self.y


class Asteroid(ProjectileBody):
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

        super().__init__(self.image)

    # def draw(self):
    #     WINDOW.blit(self.rotated_image, (self.x - self.width // 2, self.y - self.height // 2))

    def rotate_asteroid(self):
        self.angle = (self.angle + self.rotate_speed) % 360
        self.rotated_image = pygame.transform.rotate(self.image, self.angle)
        self.width = self.rotated_image.get_width()
        self.height = self.rotated_image.get_height()

    # def move_asteroid(self):
    #     self.x += self.x_velocity
    #     self.y += self.y_velocity
    #     self.hitbox = pygame.Rect(self.x - self.hitbox_width // 2, self.y - self.hitbox_height // 2, self.hitbox_width, self.hitbox_height)


class PowerUp(ProjectileBody):
    def __init__(self):
        self.image = STAR_SPRITE
        super().__init__(self.image)

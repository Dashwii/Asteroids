from constants import *


class Spaceship:
    def __init__(self):
        self.lives = 3
        self.angle = 0
        self.image = SPACESHIP_IMAGE
        self.rotated_image = pygame.transform.rotate(self.image, self.angle)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        # Position
        self.x, self.y = WIDTH // 2, HEIGHT // 2
        self.hitbox = self.rotated_image.get_rect(x=self.x - self.width // 2, y=self.y - self.height // 2, height=self.height - 10)

        # Angle
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = ((self.x + self.cosine * self.width // 2) - self.rotated_image.get_width() // 2, self.y - self.sine * self.height // 2)
        self.last_thrust_trajectory = (self.cosine, self.sine)
        self.last_boosted_angle = self.angle

        # Movement
        self.rotate_speed = 6
        self.max_momentum = 3
        self.momentum = 0

        # Boosters
        self.booster_on = False

        # Bullets
        self.current_bullet_frame = 0
        self.bullets = BULLET_SPRITES[1:]

    def draw_ship(self):
        WINDOW.blit(self.rotated_image, (self.x - self.rotated_image.get_width() // 2, self.y - self.rotated_image.get_height() // 2))

    def shoot_bullet(self):
        return Bullet(self.head, -self.sine, self.cosine)

    def rotate_ship_left(self):
        self.angle = (self.angle + self.rotate_speed) % 360
        self.rotated_image = pygame.transform.rotate(self.image, self.angle)

    def rotate_ship_right(self):
        self.angle = (self.angle - self.rotate_speed) % 360
        self.rotated_image = pygame.transform.rotate(self.image, self.angle)

    def calculate_new_angle(self):
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.width // 2, self.y - self.sine * self.height // 2)

    def move_ship(self):
        if self.booster_on:
            self.last_thrust_trajectory = (self.cosine, self.sine)
        self.x += self.last_thrust_trajectory[0] * self.momentum
        self.y -= self.last_thrust_trajectory[1] * self.momentum
        self.hitbox.x, self.hitbox.y = self.x - self.width // 2, (self.y + 5) - self.height // 2
        self.calculate_new_angle()
        # Wrap around
        if self.x < 0 - self.width // 2:
            self.x = WIDTH
        elif self.x - self.width // 2 > WIDTH:
            self.x = 0
        if self.y < 0 - self.height // 2:
            self.y = HEIGHT
        elif self.y - self.height // 2 > HEIGHT:
            self.y = 0

    def add_momentum(self):
        self.last_boosted_angle = self.angle
        if self.momentum <= self.max_momentum:
            self.momentum += 0.1

    def reset_momentum_check(self):
        if abs(self.angle - self.last_boosted_angle) > 6 and abs(self.angle - self.last_boosted_angle) != 354:
            self.momentum = 1


class Bullet:
    def __init__(self, player_head, sine, cosine):
        self.x, self.y = player_head
        self.width = 4
        self.height = 4
        self.sine = sine
        self.cosine = cosine
        self.speed = 10
        self.x_velocity = self.cosine * self.speed
        self.y_velocity = self.sine * self.speed
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity
        self.hitbox.x, self.hitbox.y = self.x, self.y

    def draw(self):
        pygame.draw.rect(WINDOW, WHITE, self.hitbox)


class BoosterSprite:
    pass

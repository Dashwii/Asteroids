from constants import *


class Alien:
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "alien_ship.png")), (65, 30)) # 75 40
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x, self.y = MIDDLE_W, MIDDLE_H
        self.hitbox = self.image.get_rect(x=self.x, y=self.y)
        self.health = 50
        self.speed = 40
        self.bullet_timer = 0
        self.move_timer = 0

        self.target_pos = (random.randint(0, WIDTH - self.width), random.randint(0, HEIGHT - self.height))
        self.angle = math.atan2(self.target_pos[1] - self.y, self.target_pos[0] - self.x)

        self.dx = math.cos(self.angle)*self.speed
        self.dy = math.sin(self.angle)*self.speed

        self.target_x_reached, self.target_y_reached = False, False

        self.list_of_bullets = []

    def draw(self):
        WINDOW.blit(self.image, (self.x, self.y))

    def choose_new_target(self):
        self.target_pos = (random.randint(0, WIDTH - self.width), random.randint(0, HEIGHT - self.height))
        self.angle = math.atan2(self.target_pos[1] - self.y, self.target_pos[0] - self.x)
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed
        self.target_x_reached, self.target_y_reached = False, False

    def check_if_reached(self):
        if self.dx < 0:
            if int(self.x) <= self.target_pos[0]:
                self.target_x_reached = True
            else:
                self.x += self.dx
        elif self.dx > 0:
            if int(self.x) >= self.target_pos[0]:
                self.target_x_reached = True
            else:
                self.x += self.dx
        if self.dy < 0:
            if int(self.y) <= self.target_pos[1]:
                self.target_y_reached = True
            else:
                self.y += self.dy
        elif self.dy > 0:
            if int(self.y) >= self.target_pos[1]:
                self.target_y_reached = True
            else:
                self.y += self.dy
        self.hitbox.x, self.hitbox.y = int(self.x), int(self.y)

    def shoot_bullet(self, player_x, player_y):
        return AlienBullet(self.x + self.width // 2, self.y + self.height // 2, player_x, player_y)

    def move_bullets(self):
        for bullet in self.list_of_bullets:
            bullet.move()


class AlienBullet:
    def __init__(self, x, y, target_x, target_y):
        self.alien_bullet = True
        self.x, self.y = x, y
        self.target_x, self.target_y = target_x, target_y
        self.width, self.height = 4, 4
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed = 10

        self.angle = math.atan2(self.target_y - self.y, self.target_x - self.x)
        self.dx = math.cos(self.angle)*self.speed
        self.dy = math.sin(self.angle)*self.speed

    def draw(self):
        pygame.draw.rect(WINDOW, RED, self.hitbox)

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.hitbox.x, self.hitbox.y = int(self.x), int(self.y)


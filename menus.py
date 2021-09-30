from constants import *
from spaceship_class import Spaceship
from asteroid_class import Asteroid
from alien_class import Alien


class TitleMenu:
    def __init__(self):
        self.playing = True
        self.asteroids_title_rect = pygame.Rect(100, -120, WIDTH // 2, 100)

        self.prev_time = time.time()
        self.dt = 0
        self.play_asteroids = False
        self.options_menu = False

        self.title_screen_text = TITLE_FONT.render("ASTEROIDS", True, WHITE)
        self.play_text, self.highlighted_play_text = TEXT_FONT.render("Play", True, WHITE), ENLARGED_TEXT_FONT.render("Play", True, WHITE)
        self.options_text, self.highlighted_options_text = TEXT_FONT.render("Options", True, WHITE), ENLARGED_TEXT_FONT.render("Options", True, WHITE)

        self.play_text_rect = self.play_text.get_rect()
        self.play_text_rect.x, self.play_text_rect.y = (MIDDLE_W - self.play_text.get_width() // 2, MIDDLE_H - 30)
        self.options_text_rect = self.options_text.get_rect()
        self.options_text_rect.x, self.options_text_rect.y = (MIDDLE_W - self.options_text.get_width() // 2, MIDDLE_H + 60)

        self.is_play_text_highlighted = False
        self.is_options_text_highlighted = False

    def title_screen(self):
        clock = pygame.time.Clock()
        while self.playing:
            now = time.time()
            self.dt = now - self.prev_time
            self.prev_time = now

            clock.tick(FPS)

            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN and self.play_text_rect.collidepoint(mouse_pos):
                    self.playing = False
                    self.play_asteroids = True

            if self.play_text_rect.collidepoint(mouse_pos):
                self.is_play_text_highlighted = True
            if self.options_text_rect.collidepoint(mouse_pos):
                self.is_options_text_highlighted = True

            self.handle_title_rect()
            self.title_draw(self.is_play_text_highlighted, self.is_options_text_highlighted)
            self.is_play_text_highlighted, self.is_options_text_highlighted = False, False
        return False

    def title_draw(self, play_highlighted=False, options_highlighted=False):
        WINDOW.fill(BLACK)
        WINDOW.blit(self.title_screen_text, (MIDDLE_W - self.title_screen_text.get_width() // 2, self.asteroids_title_rect.y))
        if play_highlighted:
            WINDOW.blit(self.highlighted_play_text, (MIDDLE_W - self.highlighted_play_text.get_width() // 2, MIDDLE_H - 30))
        else:
            WINDOW.blit(self.play_text, (MIDDLE_W - self.play_text.get_width() // 2, MIDDLE_H - 30))
        if options_highlighted:
            WINDOW.blit(self.highlighted_options_text, (MIDDLE_W - self.highlighted_options_text.get_width() // 2, MIDDLE_H + 60))
        else:
            WINDOW.blit(self.options_text, (MIDDLE_W - self.options_text.get_width() // 2, MIDDLE_H + 60))
        pygame.display.update()

    def handle_title_rect(self):
        if self.asteroids_title_rect.y < MIDDLE_H - 300:
            self.asteroids_title_rect.y += 115 * self.dt


class AsteroidsGame:
    def __init__(self):
        self.playing = False
        self.prev_time = time.time()
        self.dt = 0
        self.player = Spaceship()
        self.count = 0
        self.list_of_aliens = []
        self.list_of_asteroids = []
        self.list_of_bullets = []
        self.bullet_cooldown = 0.1
        self.last_time_taken_damage = None
        self.invulnerable = False
        self.flick = 0
        self.score = 0
        self.score_text = LIVES_SCORE_FONT.render(f"SCORE: {self.score}", True, WHITE)
        self.lives_text = LIVES_SCORE_FONT.render(f"LIVES: {self.player.lives}x", True, WHITE)
        self.game_over_text = GAME_OVER_FONT.render(f"GAME OVER! PRESS SPACE TO PLAY AGAIN OR ESC TO RETURN TO MENU.", True, WHITE)
        self.score_text_rect = self.score_text.get_rect(x=0, y=0)
        self.lives_text_rect = self.lives_text.get_rect(x=0, y=self.score_text_rect.y + self.score_text_rect.height)
        self.game_over_screen = False

    def game_loop(self):
        clock = pygame.time.Clock()
        last_fire = 0

        while self.playing:
            now = time.time()
            self.dt = now - self.prev_time
            self.prev_time = now

            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    pygame.quit()

                # Bullet Fire
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if now - last_fire >= self.bullet_cooldown:
                        self.list_of_bullets.append(self.player.shoot_bullet())
                        last_fire = time.time()

            self.count += 1
            # After every 50 iterations spawn a new asteroid with a new size_rank
            if self.count % 50 == 0:
                ran = random.choice([1, 1, 1, 2, 2, 3])
                self.list_of_asteroids.append(Asteroid(ran))
            if self.count % 2000 == 0:
                self.list_of_aliens.append(Alien())

            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_ESCAPE]:
                self.playing = False
            if keys_pressed[pygame.K_w]:
                self.player.booster_on = True
                self.player.reset_momentum_check()
                self.player.add_momentum()


            if keys_pressed[pygame.K_d]:
                self.player.rotate_ship_right()
            if keys_pressed[pygame.K_a]:
                self.player.rotate_ship_left()
            if self.player.lives == 0:
                self.game_over_screen = True
                self.game_over_loop()


            self.player.move_ship()
            self.move_bullets()
            self.move_asteroids()
            self.check_asteroid_lifespan()
            self.check_asteroid_bullet_collisions_append_new_asteroids()
            self.move_aliens()
            self.check_alien_collision()
            self.alien_shoot_bullets()
            self.check_alien_bullet_collision()
            self.remove_bullets()

            if self.invulnerable:
                self.flick += 1
                if time.time() - self.last_time_taken_damage > 1.5:
                    self.flick = 0
                    self.invulnerable = False

            self.blit_screen()
            self.give_aliens_target()
            self.player.booster_on = False

    def blit_screen(self):
        WINDOW.fill(BLACK)
        if self.invulnerable:
            if self.flick % 5 == 0:
                self.player.draw_ship()
        else:
            self.player.draw_ship()
        self.draw_bullets()
        self.draw_asteroids()
        self.draw_aliens()
        self.score_text = LIVES_SCORE_FONT.render(f"SCORE: {self.score}", True, WHITE)
        self.lives_text = LIVES_SCORE_FONT.render(f"LIVES: {self.player.lives}x", True, WHITE)
        WINDOW.blit(self.score_text, self.score_text_rect)
        WINDOW.blit(self.lives_text, self.lives_text_rect)
        pygame.display.update()

    def move_asteroids(self):
        for asteroid in self.list_of_asteroids:
            asteroid.move_asteroid()

    def draw_asteroids(self):
        for asteroid in self.list_of_asteroids:
            asteroid.rotate_asteroid()
            asteroid.draw()

    def move_aliens(self):
        for alien in self.list_of_aliens:
            alien.check_if_reached()

    def draw_aliens(self):
        for alien in self.list_of_aliens:
            alien.draw()

    def give_aliens_target(self):
        for alien in self.list_of_aliens:
            alien.move_timer += 1
            if alien.target_x_reached and alien.target_y_reached:
                if alien.move_timer % 500 == 0:
                    alien.choose_new_target()

    def check_alien_collision(self):
        for idx, alien in enumerate(self.list_of_aliens[:]):
            if alien.hitbox.colliderect(self.player.hitbox) and alien.target_x_reached and alien.target_x_reached:
                if not self.invulnerable:
                    alien.health -= 20
                    if alien.health <= 0:
                        del self.list_of_aliens[idx]
                    self.taken_damage()

            for idy, b in enumerate(self.list_of_bullets):
                if hasattr(b, "alien_bullet"):
                    continue
                if alien.hitbox.colliderect(b.hitbox):
                    del self.list_of_bullets[idy]
                    alien.health -= 10
                    if alien.health <= 0:
                        del self.list_of_aliens[idx]

    def check_alien_bullet_collision(self):
        for idx, bullet in enumerate(self.list_of_bullets):
            if hasattr(bullet, "alien_bullet"):
                if bullet.hitbox.colliderect(self.player.hitbox) and not self.invulnerable:
                    del self.list_of_bullets[idx]
                    self.taken_damage()

    def check_asteroid_bullet_collisions_append_new_asteroids(self):
        for idx, asteroid in enumerate(self.list_of_asteroids):
            if asteroid.hitbox.colliderect(self.player.hitbox) and not self.invulnerable:
                self.taken_damage()
                self.asteroid_splitting(asteroid)
                del self.list_of_asteroids[idx]

            for idy, bullet in enumerate(self.list_of_bullets):
                if hasattr(bullet, "alien_bullet"):
                    continue
                if asteroid.hitbox.colliderect(bullet.hitbox):
                    self.score += asteroid.score_given
                    # Give new asteroids same position as old one
                    self.asteroid_splitting(asteroid)
                    del self.list_of_asteroids[idx]
                    del self.list_of_bullets[idy]

    def asteroid_splitting(self, a):
        if a.size_rank == 3:
            new_asteroids = [Asteroid(2) for _ in range(2)]
            new_asteroids[0].x, new_asteroids[0].y = a.x, a.y
            new_asteroids[1].x, new_asteroids[1].y = a.x, a.y
            [self.list_of_asteroids.append(i) for i in new_asteroids]
        if a.size_rank == 2:
            new_asteroids = [Asteroid(1) for _ in range(2)]
            new_asteroids[0].x, new_asteroids[0].y = a.x, a.y
            new_asteroids[1].x, new_asteroids[1].y = a.x, a.y
            [self.list_of_asteroids.append(i) for i in new_asteroids]

    def check_asteroid_lifespan(self):
        for idx, asteroid in enumerate(self.list_of_asteroids[:]):
            asteroid.lifespan += 1
            if asteroid.lifespan % 1500 == 0:
                del self.list_of_asteroids[idx]

    def append_new_asteroids_to_list(self, asteroids_to_append):
        self.list_of_asteroids += asteroids_to_append

    def move_bullets(self):
        for bullet in self.list_of_bullets:
            bullet.move()

    def remove_bullets(self):
        for idx, bullet in enumerate(self.list_of_bullets):
            if bullet.x > WIDTH or bullet.x < 0:
                del self.list_of_bullets[idx]
            elif bullet.y > HEIGHT or bullet.y < 0:
                del self.list_of_bullets[idx]

    def draw_bullets(self):
        for bullet in self.list_of_bullets:
            bullet.draw()

    def taken_damage(self):
        self.player.lives -= 1
        self.invulnerable = True
        self.last_time_taken_damage = time.time()

    def alien_shoot_bullets(self):
        for alien in self.list_of_aliens:
            alien.bullet_timer += 1
            if alien.bullet_timer % 200 == 0:
                self.list_of_bullets.append(alien.shoot_bullet(self.player.hitbox.x + self.player.width // 2, self.player.hitbox.y + self.player.height // 2))

    def game_over_loop(self):
        while self.game_over_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    pygame.quit()
                keys_pressed = pygame.key.get_pressed()
                if keys_pressed[pygame.K_ESCAPE]:
                    self.game_over_screen = False
                    self.playing = False
                    return
                if keys_pressed[pygame.K_SPACE]:
                    self.game_over_screen = False
                    self.reset_game()
            WINDOW.blit(self.game_over_text, (MIDDLE_W - self.game_over_text.get_width() // 2, MIDDLE_H))
            pygame.display.update()

    def reset_game(self):
        self.list_of_asteroids = []
        self.list_of_bullets = []
        self.list_of_aliens = []
        self.score = 0
        self.count = 0
        self.flick = 0
        self.invulnerable = False
        del self.player
        self.player = Spaceship()

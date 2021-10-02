from constants import *
from spaceship_class import Spaceship
from projectile_bodies_class import ProjectileBody
from projectile_bodies_class import Asteroid
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
        self.rapid_fire = False
        self.rapid_fire_activation_time = None
        self.count = 0
        self.list_of_player_bullets = []
        self.list_of_asteroids = []
        self.list_of_rapid_fire_powerups = []
        self.list_of_aliens = []
        self.list_of_alien_bullets = []
        self.list_of_oneups = []
        self.bullet_cooldown = 0.1
        self.last_time_taken_damage = None
        self.invulnerable = False
        self.flick = 0
        self.score = 0
        self.score_text = LIVES_SCORE_FONT.render(f"SCORE: {self.score}", True, WHITE)
        self.lives_text = LIVES_SCORE_FONT.render(f"LIVES: {self.player.lives}x", True, WHITE)
        self.game_over_text = GAME_OVER_FONT.render(f"GAME OVER! CLICK TO PLAY AGAIN OR ESC TO RETURN TO MENU.", True, WHITE)
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
                if not self.rapid_fire:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        if now - last_fire >= self.bullet_cooldown:
                            self.list_of_player_bullets.append(self.player.shoot_bullet())
                            last_fire = time.time()
            self.count += 1

            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_ESCAPE]:
                self.playing = False

            if self.player.lives == 0:
                self.game_over_screen = True
                self.game_over_loop()

            if keys_pressed[pygame.K_w]:
                self.player.booster_on = True
                self.player.reset_momentum_check()
                self.player.add_momentum()

            # After every 50 iterations spawn a new asteroid with a new size_rank
            if self.count % 50 == 0:
                ran = random.choice([1, 1, 1, 2, 2, 3])
                self.list_of_asteroids.append(Asteroid(ran))
            if self.count % 2500 == 0:
                if random.randint(1, 3) == 3:
                    self.list_of_aliens.append(Alien())
            if self.count % 3000 == 0:
                if random.randint(1, 5) == 5:
                    self.list_of_rapid_fire_powerups.append(ProjectileBody(STAR_SPRITE))
            if self.count % 2700 == 0:
                if random.randint(1, 2) == 2:
                    self.list_of_oneups.append(ProjectileBody(HEART_SPRITE))
            if self.rapid_fire:
                if time.time() - self.rapid_fire_activation_time > 5:
                    self.rapid_fire = False
                self.list_of_player_bullets.append(self.player.shoot_bullet())
            if self.invulnerable:
                self.flick += 1
                if time.time() - self.last_time_taken_damage > 1.5:
                    self.flick = 0
                    self.invulnerable = False

            if keys_pressed[pygame.K_d]:
                self.player.rotate_ship_right()
            if keys_pressed[pygame.K_a]:
                self.player.rotate_ship_left()

            self.player.move_ship()
            self.remove_bullets(self.list_of_player_bullets)
            self.remove_bullets(self.list_of_alien_bullets)
            self.move_bullets(self.list_of_player_bullets)
            self.move_bullets(self.list_of_alien_bullets)
            self.move_projectile_bodies(self.list_of_asteroids)
            self.move_projectile_bodies(self.list_of_rapid_fire_powerups)
            self.move_projectile_bodies(self.list_of_oneups)
            self.check_asteroid_collision()
            self.check_asteroid_lifespan()
            self.check_powerup_collisions(self.list_of_rapid_fire_powerups)
            self.check_powerup_collisions(self.list_of_oneups)
            self.move_aliens()
            self.check_alien_collision()
            self.alien_shoot_bullets()
            self.check_alien_bullet_collision()
            self.give_aliens_target()

            self.blit_screen()
            self.player.booster_on = False

    def blit_screen(self):
        WINDOW.blit(BACKGROUND, (0, 0))
        if self.invulnerable:
            if self.flick % 5 == 0:
                self.player.draw_ship()
        else:
            self.player.draw_ship()
        self.draw_projectile_bodies(self.list_of_asteroids)
        self.draw_projectile_bodies(self.list_of_rapid_fire_powerups)
        self.draw_projectile_bodies(self.list_of_oneups)
        self.draw_aliens()
        self.draw_bullets(self.list_of_player_bullets)
        self.draw_bullets(self.list_of_alien_bullets)
        self.score_text = LIVES_SCORE_FONT.render(f"SCORE: {self.score}", True, WHITE)
        self.lives_text = LIVES_SCORE_FONT.render(f"LIVES: {self.player.lives}x", True, WHITE)
        WINDOW.blit(self.score_text, self.score_text_rect)
        WINDOW.blit(self.lives_text, self.lives_text_rect)
        pygame.display.update()

    @staticmethod
    def move_projectile_bodies(projectile_body_list):
        for projectile_body in projectile_body_list:
            projectile_body.move()

    @staticmethod
    def draw_projectile_bodies(projectile_body_list):
        for projectile_body in projectile_body_list:
            projectile_body.draw()

    def check_asteroid_collision(self):
        # For whatever dumbass reason, using del throws IndexErrors left, right, and center. Pop seems to cause less errors.
        # Adding return statements seem to remedy the issue fully. No more crashes, and no more random objects deleting themselves due to index erros. ¯\_(ツ)_/¯

        for idx, asteroid in enumerate(self.list_of_asteroids[:]):
            if asteroid.hitbox.colliderect(self.player.hitbox) and not self.invulnerable:
                self.taken_damage()
                self.asteroid_splitting(asteroid)
                self.list_of_asteroids.pop(idx)
                return
            for idy, bullet in enumerate(self.list_of_player_bullets[:]):
                if bullet.hitbox.colliderect(asteroid.hitbox):
                    self.score += asteroid.score_given
                    self.asteroid_splitting(asteroid)
                    self.list_of_player_bullets.pop(idy)
                    self.list_of_asteroids.pop(idx)
                    return

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
                self.list_of_asteroids.pop(self.list_of_asteroids.index(asteroid))

    def check_powerup_collisions(self, list_of_powerup):
        if list_of_powerup == self.list_of_oneups:
            for idx, powerup in enumerate(list_of_powerup[:]):
                if self.player.hitbox.colliderect(powerup.hitbox):
                    if self.player.lives < 3:
                        self.player.lives += 1
                        self.list_of_oneups.pop(idx)
        elif list_of_powerup == self.list_of_rapid_fire_powerups:
            for idx, powerup in enumerate(list_of_powerup[:]):
                if self.player.hitbox.colliderect(powerup.hitbox):
                    self.rapid_fire_activation_time = time.time()
                    self.rapid_fire = True
                    self.list_of_rapid_fire_powerups.pop(idx)

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
                        self.list_of_aliens.pop(idx)
                    self.taken_damage()
                    return
            for idy, b in enumerate(self.list_of_player_bullets[:]):
                if alien.hitbox.colliderect(b.hitbox):
                    self.list_of_player_bullets.pop(idy)
                    alien.health -= 10
                    if alien.health <= 0:
                        self.score += 125
                        self.list_of_aliens.pop(idx)
                    return


    def check_alien_bullet_collision(self):
        for idx, bullet in enumerate(self.list_of_alien_bullets[:]):
            if hasattr(bullet, "alien_bullet"):
                if bullet.hitbox.colliderect(self.player.hitbox) and not self.invulnerable:
                    self.list_of_alien_bullets.pop(idx)
                    self.taken_damage()

    @staticmethod
    def move_bullets(bullet_list):
        for bullet in bullet_list:
            bullet.move()

    @staticmethod
    def remove_bullets(bullet_list):
        for idx, bullet in enumerate(bullet_list):
            if bullet.x > WIDTH + 100 or bullet.x < -100:
                bullet_list.pop(bullet_list.index(bullet))
            elif bullet.y > HEIGHT + 100 or bullet.y < -100:
                bullet_list.pop(bullet_list.index(bullet))

    @staticmethod
    def draw_bullets(bullet_list):
        for bullet in bullet_list:
            bullet.draw()

    def taken_damage(self):
        self.player.lives -= 1
        self.invulnerable = True
        self.last_time_taken_damage = time.time()

    def alien_shoot_bullets(self):
        for alien in self.list_of_aliens:
            alien.bullet_timer += 1
            if alien.bullet_timer % 200 == 0:
                self.list_of_alien_bullets.append(alien.shoot_bullet(self.player.hitbox.x + self.player.width // 2, self.player.hitbox.y + self.player.height // 2))

    def game_over_loop(self):
        while self.game_over_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.game_over_screen = False
                    self.reset_game()
                keys_pressed = pygame.key.get_pressed()
                if keys_pressed[pygame.K_ESCAPE]:
                    self.game_over_screen = False
                    self.playing = False
                    return
            WINDOW.blit(self.game_over_text, (MIDDLE_W - self.game_over_text.get_width() // 2, MIDDLE_H))
            pygame.display.update()

    def reset_game(self):
        self.list_of_asteroids = []
        self.list_of_rapid_fire_powerups = []
        self.list_of_oneups = []
        self.list_of_player_bullets = []
        self.list_of_alien_bullets = []
        self.list_of_aliens = []
        self.score = 0
        self.count = 1
        self.flick = 0
        self.invulnerable = False
        del self.player
        self.player = Spaceship()

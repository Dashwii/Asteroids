from constants import *
from menus import *


def main():
    running = True
    clock = pygame.time.Clock()
    title = TitleMenu()
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        if title.play_asteroids:
            asteroids_game = AsteroidsGame()
            asteroids_game.playing = True
            while asteroids_game.playing:
                asteroids_game.game_loop()
            if not asteroids_game.playing:
                del asteroids_game
                del title
                title = TitleMenu()
                title.playing = True

        while title.playing:
            title.title_screen()

        WINDOW.fill(BLACK)
        pygame.display.update()


if __name__ == "__main__":
    main()



# Power up ideas:
# Shield - Provides 1 hit of protection from an asteroid
# Drill - Player is able to ram into asteroids and destroy them giving points
# Rapid fire - Self explanatory
# Legion - Alien ships will shoot asteroids to help player gain points
# Piercing bullets - Bullets go through all targets it hits. Only despawns when off screen

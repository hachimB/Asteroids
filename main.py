# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    def reset_game():
        updatable.empty()
        drawable.empty()
        asteroids.empty()
        shots.empty()
        Player.containers = (updatable, drawable)
        Asteroid.containers = (updatable, drawable, asteroids)
        AsteroidField.containers = (updatable,)
        Shot.containers = (updatable, drawable)
        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        asteroid_field = AsteroidField()
        return player, 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    score = 0
    font = pygame.font.SysFont(None, 36)

    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable)
    Shot.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()
    
    game_over = False

    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if not game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        shot = player.shoot()
                        if shot:
                            shots.add(shot)
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    # Reset button
                    if 200 < mx < 400 and 300 < my < 350:
                        player, score = reset_game()
                        game_over = False
                    # Quit button
                    if 200 < mx < 400 and 370 < my < 420:
                        sys.exit()
        
        screen.fill(color="black", rect=None, special_flags=0)
        if not game_over:
            updatable.update(dt)
        
           # Check for collisions between player and any asteroid
            for asteroid in asteroids:
                if player.is_colliding(asteroid):
                    game_over = True
            
        
            for asteroid in asteroids:
                for bullet in shots:
                    if bullet.is_colliding(asteroid):
                        asteroid.split()
                        bullet.kill()
                        score += 10
        
            for draw in drawable:
                draw.draw(screen)

            # Draw the score
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))
    
        else:
             # Draw GAME OVER text
            over_text = font.render("GAME OVER", True, (255, 0, 0))
            screen.blit(over_text, (200, 200))
            # Draw Reset button
            pygame.draw.rect(screen, (100, 100, 255), (200, 300, 200, 50))
            reset_text = font.render("Reset", True, (255, 255, 255))
            screen.blit(reset_text, (270, 310))
            # Draw Quit button
            pygame.draw.rect(screen, (255, 100, 100), (200, 370, 200, 50))
            quit_text = font.render("Quit", True, (255, 255, 255))
            screen.blit(quit_text, (280, 380))

        pygame.display.flip()
        time_passed = clock.tick(60)
        dt = time_passed / 1000


if __name__ == "__main__":
    main()

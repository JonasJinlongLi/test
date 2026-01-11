import pygame
import sys
from Brick_breaker_game import Game, WIDTH, HEIGHT

def manual_game():
    game = Game()
    running = True
    episode = 0
    
    font = pygame.font.Font(None, 24)
    
    while running:
        game.clock.tick(120)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset()
                    episode += 1
                    print(f"Episode {episode} started")
        
        # Manual control with arrow keys
        keys = pygame.key.get_pressed()
        action = 0  # stay
        if keys[pygame.K_LEFT]:
            action = 1  # left
        elif keys[pygame.K_RIGHT]:
            action = 2  # right
        
        # Take step
        reward, done = game.step(action)
        
        # Reset if done
        if done:
            game.reset()
            episode += 1
            print(f"Episode {episode} completed")
        
        # Render
        game.render()
        
        # Display info
        info_text = f"Episode: {episode} | Bricks: {len(game.bricks)} | Reward: {reward}"
        text_surface = font.render(info_text, True, (255, 255, 255))
        game.screen.blit(text_surface, (10, 10))
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    manual_game()
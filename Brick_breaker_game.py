import pygame
import numpy as np

# --- Constants ---
WIDTH, HEIGHT = 600, 400
FPS = 120

WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
RED = (200, 50, 50)
BLACK = (0, 0, 0)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Brick Breaker")
        self.clock = pygame.time.Clock()
        self.reset()
    
    def reset(self):
        """Resetter hele spiltilstanden"""
        self.paddle = pygame.Rect(WIDTH // 2 - 40, HEIGHT - 20, 80, 10)
        self.ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, 10, 10)
        self.ball_speed = [1, 3]
        self.done = False
        
        # Create bricks
        self.bricks = []
        ROWS, COLS = 3, 7
        for row in range(ROWS):
            for col in range(COLS):
                brick = pygame.Rect(col * 80 + 10, row * 30 + 40, 65, 20)
                self.bricks.append(brick)
    
    def step(self, action):
        """
        action:
        0 = stay
        1 = left
        2 = right
        """
        reward = 0
        paddle_speed = 20

        # --- Paddle movement ---
        if action == 1:
            self.paddle.x -= paddle_speed
        elif action == 2:
            self.paddle.x += paddle_speed

        self.paddle.x = max(0, min(WIDTH - self.paddle.width, self.paddle.x))

        # --- Ball movement ---
        self.ball.x += self.ball_speed[0]
        self.ball.y += self.ball_speed[1]

        if self.ball.left <= 0 or self.ball.right >= WIDTH:
            self.ball_speed[0] *= -1
        if self.ball.top <= 0:
            self.ball_speed[1] *= -1

        # Paddle collision
        if self.ball.colliderect(self.paddle) and self.ball_speed[1] > 0:
            self.ball.bottom = self.paddle.top - 1
            self.ball_speed[1] *= -1
            reward += 5
            
            # Adjust ball angle
            relative_intersect = (self.paddle.centerx - self.ball.centerx) / (self.paddle.width / 2)
            self.ball_speed[0] = -relative_intersect * 2

        # Brick collision
        for brick in self.bricks[:]:
            if self.ball.colliderect(brick):
                self.bricks.remove(brick)
                self.ball_speed[1] *= -1
                reward += 10
                break

        # Win condition
        if len(self.bricks) == 0:
            reward += 50
            self.done = True

        # Lose condition
        if self.ball.bottom >= HEIGHT:
            reward -= 20
            self.done = True

        return reward, self.done
    
    def render(self):
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, BLUE, self.paddle)
        pygame.draw.ellipse(self.screen, WHITE, self.ball)
        for brick in self.bricks:
            pygame.draw.rect(self.screen, RED, brick)
        
        pygame.display.flip()
    
    def get_display_info(self):
        return self.screen
    
    def get_clock(self):
        return self.clock
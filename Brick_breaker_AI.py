import numpy as np
import random
from collections import defaultdict
import pygame
import sys
from Brick_breaker_game import Game, WIDTH, HEIGHT

class RLAgent:
    def __init__(self, game):
        self.game = game
        self.ACTIONS = [0, 1, 2]  # left, stay, right
        self.alpha = 0.2
        self.gamma = 0.9
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.1
        
        # Discretization parameters
        self.PADDLE_BINS = 10
        self.BALL_X_BINS = 15
        self.BALL_Y_BINS = 15
        
        # Q-table
        def default_value():
            return [0., 0., 0.]
        self.Q = defaultdict(default_value)
        
        # Statistics
        self.episode = 0
        self.counter = 0
        
        print(f"State space size: {self.PADDLE_BINS * self.BALL_X_BINS * self.BALL_Y_BINS} possible states")
    
    def discretize_value(self, value, max_value, bins):
        normalized = value / max_value
        bin_index = int(normalized * bins)
        return min(bins - 1, max(0, bin_index))
    
    def get_state(self):
        paddle_pos = self.game.paddle.x
        paddle_max = WIDTH - self.game.paddle.width
        paddle_bin = self.discretize_value(paddle_pos, paddle_max, self.PADDLE_BINS)
        
        ball_x_bin = self.discretize_value(self.game.ball.centerx, WIDTH, self.BALL_X_BINS)
        ball_y_bin = self.discretize_value(self.game.ball.centery, HEIGHT, self.BALL_Y_BINS)
        
        return (paddle_bin, ball_x_bin, ball_y_bin)
    
    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.ACTIONS)
        else:
            return np.argmax(self.Q[state])
    
    def update_q(self, state, action, reward, next_state):
        best_next = np.max(self.Q[next_state])
        self.Q[state][action] += self.alpha * (
            reward + self.gamma * best_next - self.Q[state][action]
        )
    
    def decay_epsilon(self):
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
    
    def print_state_info(self):
        state = self.get_state()
        print(f"Paddle x: {self.game.paddle.x}, Ball: ({self.game.ball.centerx}, {self.game.ball.centery})")
        print(f"State tuple: {state}")
        print(f"Q-values for state {state}: {self.Q[state]}")
    
    def run_training(self):
        """Kør RL træningsloop"""
        running = True
        clock = pygame.time.Clock()
        FPS = 120
        
        # Hent skærmen fra game objektet
        screen = self.game.screen
        
        # Farver
        WHITE = (255, 255, 255)
        BLUE = (50, 150, 255)
        RED = (200, 50, 50)
        BLACK = (0, 0, 0)
        
        # Reset spillet først
        self.game.reset()
        
        while running:
            clock.tick(FPS)
            screen.fill(BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.print_state_info()
                    elif event.key == pygame.K_r:
                        self.game.reset()
                        self.episode += 1
                    elif event.key == pygame.K_ESCAPE:
                        running = False

            # Hent nuværende state
            state = self.get_state()
            
            # Vælg action
            action = self.choose_action(state)
            
            # Udfør action og få reward
            reward, done = self.game.step(action)
            
            # Hent næste state
            next_state = self.get_state()
            
            # Opdater Q-værdi
            self.update_q(state, action, reward, next_state)
            
            # Reset hvis spillet er slut
            if done:
                self.decay_epsilon()
                self.counter += 1
                self.game.reset()
                self.episode += 1

            # --- Tegn ---
            pygame.draw.rect(screen, BLUE, self.game.paddle)
            pygame.draw.ellipse(screen, WHITE, self.game.ball)
            for brick in self.game.bricks:
                pygame.draw.rect(screen, RED, brick)
            
            # Vis info
            font = pygame.font.Font(None, 24)
            info_text = f"Episode: {self.episode} | Epsilon: {self.epsilon:.3f} | Bricks: {len(self.game.bricks)}"
            text_surface = font.render(info_text, True, WHITE)
            screen.blit(text_surface, (10, 10))
            
            # Vis nuværende state
            state_text = f"State: {self.get_state()}"
            state_surface = font.render(state_text, True, WHITE)
            screen.blit(state_surface, (10, 40))

            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    # Opret game objekt
    game = Game()
    
    # Opret RL agent
    agent = RLAgent(game)
    
    # Start træning
    agent.run_training()
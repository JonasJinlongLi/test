import pygame
import sys
import random

pygame.init()

# --- Constants ---
WIDTH, HEIGHT = 600, 400
FPS = 60

WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
RED = (200, 50, 50)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")
clock = pygame.time.Clock()

# --- Global game objects ---
paddle = None
ball = None
ball_speed = None
bricks = None
done = False


def reset():

    global paddle, ball, ball_speed, bricks, done

    paddle = pygame.Rect(WIDTH // 2 - 40, HEIGHT - 20, 80, 10)

    ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, 10, 10)
    ball_speed = [random.choice([1,1]), 2]

    bricks = []
    ROWS, COLS = 3, 7
    for row in range(ROWS):
        for col in range(COLS):
            brick = pygame.Rect(col * 80 + 20, row * 30 + 40, 60, 20)
            bricks.append(brick)

    done = False


def step(action):
    global done, ball_speed

    reward = 0
    paddle_speed = 6

    # --- Paddle movement ---
    if action == 0:
        paddle.x -= paddle_speed
    elif action == 2:
        paddle.x += paddle_speed

    paddle.x = max(0, min(WIDTH - paddle.width, paddle.x))

    # --- Ball movement ---
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed[0] *= -1
    if ball.top <= 0:
        ball_speed[1] *= -1

    # Paddle collision
    if ball.colliderect(paddle):
        ball_speed[1] *= -1
        reward += 0.1

    # Brick collision
    for brick in bricks[:]:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_speed[1] *= -1
            reward += 1
            break

    # Lose condition
    if ball.bottom >= HEIGHT:
        reward -= 1
        done = True

    return reward, done


# --- Initialize ---
reset()

# --- Game loop ---
running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Manual control
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        action = 0
    elif keys[pygame.K_RIGHT]:
        action = 2
    else:
        action = 1

    reward, done = step(action)

    if done:
        pygame.time.delay(1000)
        reset()

    # --- Draw ---
    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    for brick in bricks:
        pygame.draw.rect(screen, RED, brick)

    pygame.display.flip()

pygame.quit()
sys.exit()

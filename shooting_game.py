import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Shooting Game")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Set up fonts
font = pygame.font.Font(None, 36)

# Game variables
player_pos = [screen_width // 2, screen_height - 50]
player_size = 50
ball_size = 20
ball_speed = 5
bullet_size = 5
bullet_speed = 10
score = 0
lives = 5
balls = []
bullets = []
player_speed = 15

# Load player image
player_image = pygame.image.load("shooter.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (player_size, player_size))

# Function to create balls
def create_ball():
    x_pos = random.randint(0, screen_width - ball_size)
    y_pos = 0
    color = RED if random.random() < 0.2 else WHITE
    return [x_pos, y_pos, color]

# Function to draw text on the screen
def draw_text(text, color, x, y):
    label = font.render(text, 1, color)
    screen.blit(label, (x, y))

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullets.append([player_pos[0] + player_size // 2 - bullet_size // 2, player_pos[1]])
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < screen_width - player_size:
        player_pos[0] += player_speed
    
    # Add new balls
    if random.randint(1, 20) == 1:
        balls.append(create_ball())
    
    # Move and draw balls
    for ball in balls[:]:
        ball[1] += ball_speed
        if ball[1] > screen_height:
            balls.remove(ball)
            if ball[2] == WHITE:
                score -= 1
            continue
        
        if ball[2] == RED and ball[1] + ball_size > player_pos[1] and player_pos[0] < ball[0] < player_pos[0] + player_size:
            lives -= 1
            balls.remove(ball)
        
        pygame.draw.circle(screen, ball[2], (ball[0], ball[1]), ball_size)
    
    # Move and draw bullets
    for bullet in bullets[:]:
        bullet[1] -= bullet_speed
        if bullet[1] < screen_height * 0.25:
            bullets.remove(bullet)
            continue
        
        # Check for bullet collision with balls
        bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_size, bullet_size)
        for ball in balls[:]:
            ball_rect = pygame.Rect(ball[0] - ball_size // 2, ball[1] - ball_size // 2, ball_size, ball_size)
            if bullet_rect.colliderect(ball_rect):
                if ball[2] == WHITE:
                    score += 1
                balls.remove(ball)
                bullets.remove(bullet)
                break
        
        pygame.draw.rect(screen, WHITE, bullet_rect)
    
    # Draw player
    screen.blit(player_image, (player_pos[0], player_pos[1]))

    # Draw score and lives
    draw_text(f"Score: {score}", WHITE, 10, 10)
    draw_text(f"Lives: {lives}", WHITE, 10, 40)

    # Check for game over
    if lives <= 0:
        draw_text("Game Over", RED, screen_width // 2 - 50, screen_height // 2)
        pygame.display.update()
        pygame.time.wait(3000)
        running = False

    pygame.display.update()
    clock.tick(30)

pygame.quit()

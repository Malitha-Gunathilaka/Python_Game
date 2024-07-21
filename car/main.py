import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Advanced Car Game')

# Set up colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Set up the clock for a decent frame rate
clock = pygame.time.Clock()

# Load car image
car_image = pygame.image.load('car.png')
car_width, car_height = car_image.get_width(), car_image.get_height()
car_x, car_y = width // 2 - car_width // 2, height - car_height - 10

# Load background image
background_image = pygame.image.load('road.png')

# Load background music and sound effects
pygame.mixer.music.load('background.mp3')
pygame.mixer.music.play(-1)  # Play the background music in a loop
collision_sound = pygame.mixer.Sound('collision.wav')
powerup_sound = pygame.mixer.Sound('powerup.wav')

# Load font for score display
font = pygame.font.Font(None, 36)

# Obstacle class
class Obstacle:
    def __init__(self):
        self.image = pygame.image.load('obstacle.png')
        self.x = random.randint(0, width - self.image.get_width())
        self.y = -self.image.get_height()
        self.speed = random.randint(3, 7)

    def update(self):
        self.y += self.speed

    def draw(self):
        window.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

# Power-up class
class PowerUp:
    def __init__(self):
        self.image = pygame.image.load('powerup.png')
        self.x = random.randint(0, width - self.image.get_width())
        self.y = -self.image.get_height()
        self.speed = 5

    def update(self):
        self.y += self.speed

    def draw(self):
        window.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

# Function to check collision
def check_collision(car_rect, obj_rect):
    return car_rect.colliderect(obj_rect)

# Function to display text on the screen
def display_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    window.blit(text_surface, (x, y))

# Function to display the game over screen
def game_over_screen(score, level):
    window.fill(black)
    display_text("Game Over", 64, red, width // 2 - 160, height // 2 - 100)
    display_text(f"Score: {score}", 48, white, width // 2 - 60, height // 2)
    display_text(f"Level: {level}", 48, white, width // 2 - 60, height // 2 + 50)
    display_text("Press R to Restart or Q to Quit", 36, white, width // 2 - 180, height // 2 + 100)
    pygame.display.update()

# Function to display the level complete screen
def level_complete_screen(level):
    window.fill(black)
    display_text(f"Level {level} Complete!", 64, green, width // 2 - 160, height // 2 - 100)
    display_text("Press N for Next Level or Q to Quit", 36, white, width // 2 - 180, height // 2 + 100)
    pygame.display.update()

# Function to display the pause screen
def pause_screen():
    window.fill(black)
    display_text("Paused", 64, blue, width // 2 - 100, height // 2 - 100)
    display_text("Press P to Resume or Q to Quit", 36, white, width // 2 - 180, height // 2 + 100)
    pygame.display.update()

# Main game loop
def game_loop(level=1, score=0):
    car_x, car_y = width // 2 - car_width // 2, height - car_height - 10
    obstacles = [Obstacle() for _ in range(level)]
    powerups = [PowerUp()]
    running = True
    game_over = False
    paused = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    game_loop()  # Restart the game
                elif event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_n and not game_over:
                    level += 1
                    game_loop(level, score)

        if paused:
            pause_screen()
            continue

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and car_x > 0:
            car_x -= 5
        if keys[pygame.K_RIGHT] and car_x < width - car_width:
            car_x += 5

        car_rect = pygame.Rect(car_x, car_y, car_width, car_height)

        if not game_over:
            for obstacle in obstacles:
                obstacle.update()
                obstacle_rect = obstacle.get_rect()
                if check_collision(car_rect, obstacle_rect):
                    pygame.mixer.Sound.play(collision_sound)
                    game_over = True
                if obstacle.y > height:
                    obstacles.remove(obstacle)
                    obstacles.append(Obstacle())

            for powerup in powerups:
                powerup.update()
                powerup_rect = powerup.get_rect()
                if check_collision(car_rect, powerup_rect):
                    pygame.mixer.Sound.play(powerup_sound)
                    powerups.remove(powerup)
                    score += 100  # Increase score for power-up
                if powerup.y > height:
                    powerups.remove(powerup)
                    powerups.append(PowerUp())

            # Increase difficulty over time
            if score % 500 == 0 and len(obstacles) < level * 2:
                obstacles.append(Obstacle())

            window.fill(black)
            window.blit(background_image, (0, 0))
            window.blit(car_image, (car_x, car_y))
            for obstacle in obstacles:
                obstacle.draw()
            for powerup in powerups:
                powerup.draw()
            score += 1
            display_text(f"Score: {score}", 36, white, 10, 10)
            display_text(f"Level: {level}", 36, white, 10, 50)

            pygame.display.update()
            clock.tick(60)
        else:
            game_over_screen(score, level)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()

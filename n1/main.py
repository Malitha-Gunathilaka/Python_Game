import pygame
import sys
import random
import time

pygame.init()

# Screen dimensions
width, height = 1000, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Enhanced Matching Puzzle Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLORS = [RED, GREEN, BLUE]

# Margins
margin = 20

# Levels
levels = [
    {"rows": 2, "cols": 2, "time": 30},
    {"rows": 4, "cols": 4, "time": 60},
    {"rows": 6, "cols": 6, "time": 90},
]
current_level = 0

def calculate_card_size(rows, cols):
    max_width = (width - (cols + 1) * margin) // cols
    max_height = (height - (rows + 1) * margin) // rows
    return min(max_width, max_height), min(max_width, max_height)

def create_board(level_info):
    rows = level_info["rows"]
    cols = level_info["cols"]
    card_width, card_height = calculate_card_size(rows, cols)
    num_pairs = rows * cols // 2
    cards = []
    for _ in range(num_pairs):
        color = random.choice(COLORS)
        cards.extend([color, color])
    random.shuffle(cards)
    revealed = [[False for _ in range(cols)] for _ in range(rows)]
    card_positions = []
    for row in range(rows):
        row_positions = []
        for col in range(cols):
            x = margin + col * (card_width + margin)
            y = margin + row * (card_height + margin)
            row_positions.append((x, y))
        card_positions.append(row_positions)
    return cards, revealed, card_positions, rows, cols, card_width, card_height

# Load sounds
match_sound = pygame.mixer.Sound('match.wav')
mismatch_sound = pygame.mixer.Sound('mismatch.wav')
pygame.mixer.music.load('background.mp3')
pygame.mixer.music.play(-1)  # Loop background music

# Initial setup
level_info = levels[current_level]
cards, revealed, card_positions, rows, cols, card_width, card_height = create_board(level_info)
first_card = None
second_card = None
matches = 0
attempts = 0
hints_left = 3

# Timer
start_time = time.time()
game_time = level_info["time"]

# Define the hint button
hint_button = pygame.Rect(650, 20, 100, 50)

# Main game loop
while True:
    screen.fill(WHITE)

    # Check for game over
    elapsed_time = time.time() - start_time
    remaining_time = game_time - int(elapsed_time)
    if remaining_time <= 0:
        font = pygame.font.SysFont(None, 75)
        game_over_text = font.render("Game Over!", True, BLACK)
        screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - game_over_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            for row in range(rows):
                for col in range(cols):
                    card_x, card_y = card_positions[row][col]
                    if card_x < x < card_x + card_width and card_y < y < card_y + card_height:
                        if not revealed[row][col]:
                            if first_card is None:
                                first_card = (row, col)
                            elif second_card is None:
                                second_card = (row, col)
                            revealed[row][col] = True
            # Check for hint button click
            if hint_button.collidepoint(event.pos):
                if hints_left > 0:
                    hint_cards = random.sample([(r, c) for r in range(rows) for c in range(cols) if not revealed[r][c]], 2)
                    for row, col in hint_cards:
                        revealed[row][col] = True
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    for row, col in hint_cards:
                        revealed[row][col] = False
                    hints_left -= 1

    # Check for match
    if first_card and second_card:
        row1, col1 = first_card
        row2, col2 = second_card
        attempts += 1
        if cards[row1 * cols + col1] == cards[row2 * cols + col2]:
            matches += 1
            pygame.mixer.Sound.play(match_sound)
        else:
            pygame.mixer.Sound.play(mismatch_sound)
            revealed[row1][col1] = False
            revealed[row2][col2] = False
        first_card = None
        second_card = None

    # Draw cards
    for row in range(rows):
        for col in range(cols):
            card_x, card_y = card_positions[row][col]
            if revealed[row][col]:
                pygame.draw.rect(screen, cards[row * cols + col], (card_x, card_y, card_width, card_height))
            else:
                pygame.draw.rect(screen, BLACK, (card_x, card_y, card_width, card_height))

    # Display score, timer, and hints on the right side
    font = pygame.font.SysFont(None, 55)
    score_text = font.render(f"Matches: {matches}", True, BLACK)
    attempts_text = font.render(f"Attempts: {attempts}", True, BLACK)
    timer_text = font.render(f"Time Left: {remaining_time}", True, BLACK)
    hints_left_text = font.render(f"Hints: {hints_left}", True, BLACK)
    screen.blit(score_text, (650, 200))
    screen.blit(attempts_text, (650, 250))
    screen.blit(timer_text, (650, 300))
    screen.blit(hints_left_text, (650, 350))

    # Draw hint button
    pygame.draw.rect(screen, (0, 0, 255), hint_button)
    hint_text = font.render("Hint", True, WHITE)
    screen.blit(hint_text, (hint_button.x + 10, hint_button.y + 10))

    # Check for level completion
    if matches == rows * cols // 2:
        current_level += 1
        if current_level >= len(levels):
            font = pygame.font.SysFont(None, 75)
            win_text = font.render("You Win!", True, BLACK)
            screen.blit(win_text, (width // 2 - win_text.get_width() // 2, height // 2 - win_text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()
        else:
            level_info = levels[current_level]
            cards, revealed, card_positions, rows, cols, card_width, card_height = create_board(level_info)
            first_card = None
            second_card = None
            matches = 0
            attempts = 0
            hints_left = 3
            start_time = time.time()
            game_time = level_info["time"]

    pygame.display.flip()

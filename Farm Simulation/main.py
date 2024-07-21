import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the game window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Farm Simulation")

# Load assets (placeholder for now)
background_color = (135, 206, 235)  # Sky blue

# Game variables
clock = pygame.time.Clock()

# Player class
class Player:
    def __init__(self, name):
        self.name = name
        self.money = 1000
        self.crops = []
        self.animals = []

# Crop class
class Crop:
    def __init__(self, name, growth_time, price):
        self.name = name
        self.growth_time = growth_time
        self.age = 0
        self.price = price

    def grow(self):
        self.age += 1

    def is_harvestable(self):
        return self.age >= self.growth_time

# Animal class
class Animal:
    def __init__(self, name, produce, produce_time, price):
        self.name = name
        self.produce = produce
        self.produce_time = produce_time
        self.time_since_last_produce = 0
        self.price = price

    def care(self):
        self.time_since_last_produce += 1

    def can_produce(self):
        return self.time_since_last_produce >= self.produce_time

# Initialize player, crops, and animals
player = Player("Farmer John")
wheat = Crop("Wheat", 5, 10)
cow = Animal("Cow", "Milk", 3, 150)

player.crops.append(wheat)
player.animals.append(cow)

# Seasons
seasons = ["Spring", "Summer", "Fall", "Winter"]
current_season = random.choice(seasons)
season_duration = 10  # Days
days_passed = 0

# Market
market_prices = {"Wheat": 15, "Milk": 20}

def next_season():
    global current_season, days_passed
    current_season = seasons[(seasons.index(current_season) + 1) % len(seasons)]
    days_passed = 0

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update game state
    days_passed += 1
    if days_passed >= season_duration:
        next_season()

    # Create a list to keep track of harvested crops
    harvested_crops = []

    for crop in player.crops:
        crop.grow()
        if crop.is_harvestable():
            player.money += market_prices[crop.name]
            print(f"{crop.name} harvested! Current money: {player.money}")
            harvested_crops.append(crop)  # Mark crop for removal

    # Remove harvested crops from player's crop list
    for crop in harvested_crops:
        player.crops.remove(crop)

    for animal in player.animals:
        animal.care()
        if animal.can_produce():
            player.money += market_prices[animal.produce]
            print(f"{animal.produce} collected from {animal.name}! Current money: {player.money}")
            animal.time_since_last_produce = 0  # Reset produce timer

    # Render game objects
    screen.fill(background_color)
    
    # Display player money and season
    font = pygame.font.Font(None, 36)
    text = font.render(f"Money: ${player.money} | Season: {current_season}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)  # Run at 60 frames per second

pygame.quit()
sys.exit()

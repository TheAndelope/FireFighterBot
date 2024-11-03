# main.py
import pygame
import sys
from player import Player
from wall import Wall
from candle import Candle  # Import the Candle class
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)

# Initialize the player and walls
player = Player(WIDTH // 2, HEIGHT // 2)
walls = [
    Wall(200, 150, 100, 20),
    Wall(400, 300, 20, 100),
    Wall(600, 150, 150, 20)
]

# Create candles
candles = [
    Candle(250, 160),  # Example candle position
    Candle(500, 250)   # Another example candle position
]

def handle_collisions(player, walls):
    for wall in walls:
        if wall.check_collision(player.rect):
            player.rect.x -= player.movement_speed * math.cos(math.radians(player.angle))
            player.rect.y -= player.movement_speed * math.sin(math.radians(player.angle))
            break

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.act(0)  # Move forward
    if keys[pygame.K_s]:
        player.act(1)  # Move backward
    if keys[pygame.K_a]:
        player.act(2)  # Rotate left
    if keys[pygame.K_d]:
        player.act(3)  # Rotate right
    if keys[pygame.K_LEFT]:
        player.act(4)  # Rotate flame sensor left
    if keys[pygame.K_RIGHT]:
        player.act(5)  # Rotate flame sensor right

    # Handle collisions
    handle_collisions(player, walls)

    # Check for candle detection
    player.check_candles(candles)

    # Cast rays and get distances
    distances = player.cast_rays(walls, screen)
    print(f"Ray distances: {distances}")  # Output the distances for debugging

    # Clear screen
    screen.fill(WHITE)

    # Draw player, walls, and candles
    player.draw(screen)
    for wall in walls:
        wall.draw(screen)
    for candle in candles:
        candle.draw(screen)

    pygame.display.flip()
    clock.tick(60)  # Limit to 60 FPS

pygame.quit()
sys.exit()

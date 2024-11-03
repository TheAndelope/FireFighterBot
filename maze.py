# main.py
import pygame
import sys
import numpy as np  # Make sure to import numpy
from player import Player
from wall import Wall
from candle import Candle  # Import the Candle class
from agent import DQNAgent  # Import the DQNAgent class
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

# Initialize DQN Agent
agent = DQNAgent(state_size=5, action_size=6)  # 5 state variables, 6 actions
batch_size = 32

# Maximum episode time in seconds
max_episode_time = 10  # Set the maximum episode time
episode_start_time = pygame.time.get_ticks()  # Get the current time at the start of the episode

def handle_collisions(player, walls):
    for wall in walls:
        if wall.check_collision(player.rect):
            player.rect.x -= player.movement_speed * math.cos(math.radians(player.angle))
            player.rect.y -= player.movement_speed * math.sin(math.radians(player.angle))
            break

# Main loop
running = True
while running:
    elapsed_time = (pygame.time.get_ticks() - episode_start_time) / 1000.0  # Calculate elapsed time in seconds
    if elapsed_time >= max_episode_time:
        print("Episode finished due to max time reached.")
        agent.save_model("models/bill.pth")  # Save the model after finishing an episode
        break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Cast rays and get distances
    distances = player.cast_rays(walls, screen)
    flame_detected = player.flame_sensor.is_candle_in_range(candles[0], player.rect.center)  # Check for flame detection

    # Create current state representation
    current_state = [
        distances[0],  # Front ray distance
        distances[1],  # Left ray distance
        distances[2],  # Right ray distance
        player.flame_sensor.angle_offset,  # Flame sensor angle (use angle_offset for detection)
        float(flame_detected)  # Flame detected (1.0 if detected, 0.0 otherwise)
    ]

    # Agent decides action based on current state
    action = agent.act(current_state)
    player.act(action)  # Perform action based on agent's decision

    # Handle collisions
    handle_collisions(player, walls)

    # Check for candle detection
    player.check_candles(candles)

    # Store transition in memory for the agent
    next_state = current_state  # The next state is the same for this iteration
    reward = 1.0 if flame_detected else -1.0  # Define reward based on flame detection
    agent.remember(current_state, action, reward, next_state, False)  # Store the experience

    # Train the agent if enough experiences are collected
    if len(agent.memory) > batch_size:
        agent.replay(batch_size)

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

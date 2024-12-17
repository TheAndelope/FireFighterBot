# maze.py
import pygame
import sys
from player import Player
from wall import Wall
from candle import Candle  # Import the Candle class
from agent import DQNAgent  # Import the DQNAgent class
import math

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 729, 729
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
SCALE=3
# Colors
BLACK = (0, 0, 0)

# Initialize the player and walls
player = Player(x=105*SCALE, y=23*SCALE)
walls = [
    Wall(0, 0, 729, 10),
    Wall(0, 0, 10, 729),
    Wall(0, 719, 729, 10),
    Wall(719, 0, 10, 729),
    Wall(72*SCALE, 0, 10, 57*SCALE),
    Wall(72*SCALE-27*SCALE, 57*SCALE, 27*SCALE+10, 10),
    Wall(0 ,729-137*SCALE, 74*SCALE, 10),
    Wall(74*SCALE, 729-137*SCALE, 10, 91*SCALE),
    Wall(719-120*SCALE, 729-45*SCALE, 10, 45*SCALE),
    Wall(719-120*SCALE, 729-(45+46)*SCALE, 120*SCALE, 10),
    Wall(719-121*SCALE, 46*SCALE, 10, 57*SCALE),
    Wall(729-121*SCALE, 46*SCALE, 73*SCALE, 10),
    Wall(719-73*SCALE, 103*SCALE, 27*SCALE+10, 10),
    Wall(719-46*SCALE, 46*SCALE, 10, 57*SCALE)
]

# Create candles
candles = [
    Candle(729-66*SCALE, 83*SCALE),  # Example candle position
]

# Initialize DQN Agent
agent = DQNAgent(state_size=5, action_size=5)  # 5 state variables, 5 actions
#-agent.load_model(file_path="models/bob.pth")
batch_size = 8400

# Maximum episode time in seconds
max_episode_time = 10  # Set the maximum episode time

def handle_collisions(player, walls):
    for wall in walls:
        if wall.check_collision(player.rect):
            player.rect.x -= player.movement_speed * math.cos(math.radians(player.angle))
            player.rect.y -= player.movement_speed * math.sin(math.radians(player.angle))
            break

# Set the number of episodes
max_episodes = 1000  # Increase this value as needed

# Main loop for episodes
for episode in range(max_episodes):
    # Reset the environment for the new episode
    player.rect.topleft = (95*SCALE, 23*SCALE)  # Reset player position
    total_reward = 0  # Initialize total reward for the episode
    elapsed_time = 0  # Track elapsed time for the episode

    # Reset the flame sensor position if needed
    player.flame_sensor.angle_offset = 0  # Reset sensor position

    # Reset all candles to burning state
    for candle in candles:
        candle.reset()  # Reset each candle to burning

    # Store previous state
    previous_state = None

    while True:  # Loop for each time step in the episode
        # Handle events and player controls (if applicable)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Cast rays and get distances for the state
        distances = player.cast_rays(walls, screen)
        flame_detected = player.flame_sensor.is_candle_in_range(candles[0], player.rect.center, player.angle)

        # Get current state
        current_state = [
            distances[0],  # Front ray distance
            distances[1],  # Left ray distance
            distances[2],  # Right ray distance
            player.flame_sensor.angle_offset,  # Sensor angle (use angle_offset)
            float(flame_detected)  # Flame detected (0 or 1)
        ]

        # Choose action using the agent
        action = agent.act(current_state)

        # Perform the action
        player.act(action)

        # Handle collisions
        handle_collisions(player, walls)

        # Reward structure
        reward = 0
        if player.check_candles(candles):
            reward += 1000  # Reward for extinguishing a candle
        elif flame_detected:
            reward += 5  # Reward for detecting a flame but not extinguishing it
        else:
            reward -= 1  # Penalty for not making progress (no flame detected)

        total_reward += reward

        # Store the transition in memory for the agent
        done = elapsed_time >= max_episode_time  # Check if the episode is done
        agent.remember(previous_state, action, reward, current_state, done)  # Store experience

        if len(agent.memory) > batch_size:
            agent.replay(batch_size)

        # Clear the screen and redraw all elements
        screen.fill(BLACK)
        player.draw(screen)
        for wall in walls:
            wall.draw(screen)
        for candle in candles:
            candle.draw(screen)

        pygame.display.flip()
        clock.tick(30)  # Limit to 60 FPS

        elapsed_time += 1 / 60  # Update elapsed time
        previous_state = current_state  # Update the previous state

        # Break if the episode is finished
        if done:
            print(f"Episode {episode + 1} finished with total reward: {total_reward}")
            agent.save_model("models/bob.pth")  # Save model after each episode if needed
            break  # Exit the loop for the current episode

pygame.quit()
sys.exit()

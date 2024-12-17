# flame_sensor.py
import pygame
import math

class FlameSensor:
    def __init__(self):
        self.angle_offset = 0  # Offset angle from the player's angle
        self.range = 100  # Detection range

    def rotate_left(self):
        if self.angle_offset-5>-90:
            self.angle_offset -= 5  # Rotate sensor left by 5 degrees

    def rotate_right(self):
        if self.angle_offset+5<90:
            self.angle_offset += 5  # Rotate sensor right by 5 degrees

    def draw(self, surface, player_position, player_angle):
        # Calculate the sensor's absolute angle based on the player's angle
        sensor_angle = player_angle + self.angle_offset

        # Draw the flame sensor as a line
        sensor_x = player_position[0] + self.range * math.cos(math.radians(sensor_angle))
        sensor_y = player_position[1] + self.range * math.sin(math.radians(sensor_angle))
        pygame.draw.line(surface, (255, 0, 0), player_position, (sensor_x, sensor_y), 2)  # Draw the sensor line

    def is_candle_in_range(self, candle, player_position, player_angle):
        """Check if the flame sensor is in range of a candle."""
        # Use the player's angle combined with the sensor's angle offset
        sensor_angle = player_angle + self.angle_offset
        sensor_x = player_position[0] + self.range * math.cos(math.radians(sensor_angle))
        sensor_y = player_position[1] + self.range * math.sin(math.radians(sensor_angle))

        # Create a point representing the sensor's endpoint
        sensor_point = pygame.Rect(sensor_x, sensor_y, 1, 1)

        # Check for collision with the candle
        return sensor_point.colliderect(candle.rect)

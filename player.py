# player.py
import pygame
import math
from flamesensor import FlameSensor

class Player:
    def __init__(self, x, y, width=54, height=54, rotation_speed=5, movement_speed=5):
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((255, 0, 0))  # Red color
        self.rect = self.image.get_rect(center=(x, y))
        self.rect.x=x
        self.rect.y=y
        self.angle = 90
        self.rotation_speed = rotation_speed
        self.movement_speed = movement_speed
        self.flame_sensor = FlameSensor()  # Initialize the flame sensor

    def act(self, action):
        if action == 0:  # Move forward
            self.move(self.movement_speed)
        #elif action == 1:  # Move backward
        #    self.move(-self.movement_speed)
        elif action == 1:  # Rotate left
            self.rotate(-self.rotation_speed)
        elif action == 2:  # Rotate right
            self.rotate(self.rotation_speed)
        elif action == 3:  # Rotate flame sensor left
            self.flame_sensor.rotate_left()
        elif action == 4:  # Rotate flame sensor right
            self.flame_sensor.rotate_right()

    def rotate(self, degrees):
        self.angle += degrees
        self.angle %= 360

    def move(self, speed):
        dx = speed * math.cos(math.radians(self.angle))
        dy = speed * math.sin(math.radians(self.angle))
        self.rect.x += dx
        self.rect.y += dy

    def get_state(self):
        return (self.rect.x, self.rect.y, self.angle)

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, -self.angle)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, rotated_rect)
        self.flame_sensor.draw(screen, self.rect.center, self.angle)  # Pass player's angle to the sensor

    def cast_rays(self, walls, screen):
        distances = []
        ray_angles = [self.angle, self.angle - 30, self.angle + 30]  # Front, left, right rays
        for ray_angle in ray_angles:
            distance = self._cast_single_ray(ray_angle, walls)
            distances.append(distance)

        # Visualization: Draw the rays
        
            ray_end_x = self.rect.centerx + distance * math.cos(math.radians(ray_angle))
            ray_end_y = self.rect.centery + distance * math.sin(math.radians(ray_angle))

            print(f"Ray at angle {ray_angle} has distance {distance} AT {self.rect.centerx}, {self.rect.centery} to {int(ray_end_x)}, {int(ray_end_y)}")

            # Corrected drawing of the ray from center
            '''
            pygame.draw.line(surface=screen,color= (0, 0, 255), 
                            start_pos=(self.rect.centerx, self.rect.centery), 
                            end_pos=(int(ray_end_x), int(ray_end_y)), 
                            width=5)  # Draw ray
            '''
            

        return distances

    def _cast_single_ray(self, angle, walls):
        ray_dx = math.cos(math.radians(angle))
        ray_dy = math.sin(math.radians(angle))
        
        ray_x, ray_y = self.rect.center
        max_distance = 800  # Maximum distance to check
        for i in range(max_distance):
            ray_x += ray_dx
            ray_y += ray_dy
            
            ray_rect = pygame.Rect(ray_x, ray_y, 1, 1)
            
            for wall in walls:
                if wall.check_collision(ray_rect):
                    return i  # Return distance to wall
        
        return max_distance  # Return max distance if no wall found

    def check_candles(self, candles):
        reward = 0  # Initialize the reward for this action
        for candle in candles:
            if self.rect.colliderect(candle.rect) and candle.is_burning:
                candle.put_out()  # Put out the candle on contact
                reward += 10  # Reward for putting out a candle
                print("Candle put out!")  # Feedback on the action

        # Check if the flame sensor detects the candle
        for candle in candles:
            if self.flame_sensor.is_candle_in_range(candle, self.rect.center, self.angle):
                print("Flame sensor detects candle!")  # Feedback for flame sensor detection
            
        return reward  # Return the total reward

# candle.py
import pygame

class Candle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 40)  # Candle size
        self.is_burning = True  # State of the candle

    def put_out(self):
        if self.is_burning:
            self.is_burning = False  # Mark the candle as put out

    def reset(self):
        self.is_burning = True  # Reset candle to burning state

    def draw(self, surface):
        if self.is_burning:
            pygame.draw.rect(surface, (255, 165, 0), self.rect)  # Draw burning candle
        else:
            pygame.draw.rect(surface, (0, 0, 0), self.rect)  # Draw put-out candle

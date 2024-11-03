import pygame

class Wall:
    def __init__(self, x, y, width, height, color=(0, 255, 0)):
        # Initialize the wall's position, size, and color
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        """Draw the wall on the screen."""
        pygame.draw.rect(screen, self.color, self.rect)
        
    def check_collision(self, player_rect):
        """Check if the player collides with the wall."""
        return self.rect.colliderect(player_rect)

from circleshape import CircleShape
import pygame
from constants import *

class Shot(CircleShape):
    def __init__(self, x, y, radius, velocity):
        super().__init__(x, y, radius)
        self.velocity = velocity
    
    def draw(self, screen):
        pygame.draw.circle(screen, color="white", center=(self.position.x, self.position.y), radius=self.radius, width=0)

    def update(self, dt):
        self.position += self.velocity * dt
    
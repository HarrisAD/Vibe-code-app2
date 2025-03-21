import pygame
import math
import os

class Player:
    def __init__(self, x, y):
        # Position and size
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        
        # Movement
        self.speed = 5
        self.dx = 0  # Horizontal velocity
        self.dy = 0  # Vertical velocity
        
        # Load or create ship image
        self.original_image = self.load_ship_image()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
        # Ship rotation
        self.angle = 0
        self.rotation_speed = 3
        
        # Thruster animation
        self.thruster_active = False
        self.thruster_frames = self.create_thruster_frames()
        self.thruster_frame = 0
        self.thruster_animation_speed = 0.2
        self.thruster_timer = 0
    
    def load_ship_image(self):
        # Try to load image from assets folder
        assets_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')
        ship_path = os.path.join(assets_path, 'player_ship.png')
        
        # If the image file exists, load it
        if os.path.exists(ship_path):
            try:
                image = pygame.image.load(ship_path).convert_alpha()
                return pygame.transform.scale(image, (self.width, self.height))
            except pygame.error:
                print(f"Error loading ship image: {ship_path}")
                # Fall back to creating an image if loading fails
        
        # If file doesn't exist or loading fails, create a ship image
        return self.create_ship_image()
    
    def create_ship_image(self):
        # Create a more detailed triangle ship
        ship_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Ship body (triangle)
        ship_color = (120, 200, 255)  # Light blue
        points = [(self.width//2, 0), (0, self.height), (self.width, self.height)]
        pygame.draw.polygon(ship_surface, ship_color, points)
        
        # Ship outline
        outline_color = (200, 230, 255)  # Lighter blue
        pygame.draw.polygon(ship_surface, outline_color, points, 2)
        
        # Cockpit (small circle near the top)
        cockpit_color = (220, 240, 255)  # Very light blue
        pygame.draw.circle(ship_surface, cockpit_color, 
                          (self.width//2, self.height//3), self.width//10)
        
        # Wings
        wing_color = (80, 140, 240)  # Darker blue
        wing_left = [(0, self.height), (self.width//4, self.height), (0, self.height-10)]
        wing_right = [(self.width, self.height), (self.width*3//4, self.height), (self.width, self.height-10)]
        pygame.draw.polygon(ship_surface, wing_color, wing_left)
        pygame.draw.polygon(ship_surface, wing_color, wing_right)
        
        # Engine
        engine_color = (200, 200, 200)  # Silver
        pygame.draw.rect(ship_surface, engine_color, 
                        (self.width//3, self.height-12, self.width//3, 7))
        
        return ship_surface
    
    def create_thruster_frames(self):
        # Create animation frames for the thruster
        frames = []
        
        # Three frames with different flame sizes
        thruster_colors = [(255, 150, 0), (255, 100, 0), (255, 50, 0)]  # Orange to red
        
        for i in range(3):
            frame = pygame.Surface((self.width, self.height//2), pygame.SRCALPHA)
            
            # Flame height varies by frame
            height = int(self.height//4 * (i+1) / 3)
            
            # Draw the flame as a triangle
            points = [(self.width//3, 0), 
                     (self.width//2, height), 
                     (self.width*2//3, 0)]
            pygame.draw.polygon(frame, thruster_colors[i], points)
            
            frames.append(frame)
        
        return frames
    
    def handle_input(self):
        # Reset movement
        self.dx = 0
        self.dy = 0
        self.thruster_active = False
        
        # Get keyboard state
        keys = pygame.key.get_pressed()
        
        # Move based on arrow keys
        if keys[pygame.K_LEFT]:
            self.dx = -self.speed
        if keys[pygame.K_RIGHT]:
            self.dx = self.speed
        if keys[pygame.K_UP]:
            self.dy = -self.speed
            self.thruster_active = True
        if keys[pygame.K_DOWN]:
            self.dy = self.speed
            
        # Rotate the ship
        if keys[pygame.K_a]:  # Rotate counter-clockwise
            self.angle += self.rotation_speed
        if keys[pygame.K_d]:  # Rotate clockwise
            self.angle -= self.rotation_speed
    
    def update(self, screen_width, screen_height):
        # Apply movement
        self.x += self.dx
        self.y += self.dy
        
        # Enforce screen boundaries
        self.x = max(self.width // 2, min(self.x, screen_width - self.width // 2))
        self.y = max(self.height // 2, min(self.y, screen_height - self.height // 2))
        
        # Update rect position
        self.rect.center = (self.x, self.y)
        
        # Rotate the image
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        
        # Update thruster animation
        if self.thruster_active:
            self.thruster_timer += self.thruster_animation_speed
            if self.thruster_timer >= 1:
                self.thruster_timer = 0
                self.thruster_frame = (self.thruster_frame + 1) % len(self.thruster_frames)
    
    def draw(self, screen):
        # Draw the spaceship to the screen
        screen.blit(self.image, self.rect.topleft)
        
        # Draw thruster effect if active
        if self.thruster_active:
            # Get current thruster frame
            thruster_img = self.thruster_frames[self.thruster_frame]
            
            # Rotate it to match ship angle
            rotated_thruster = pygame.transform.rotate(thruster_img, self.angle)
            
            # Position it at the bottom of the ship
            thruster_pos = self.rect.center
            thruster_offset = pygame.math.Vector2(0, self.height//2)
            thruster_offset.rotate_ip(-self.angle)  # Adjust rotation to match ship angle
            
            # Draw the thruster
            thruster_rect = rotated_thruster.get_rect(center=(
                thruster_pos[0] + thruster_offset.x,
                thruster_pos[1] + thruster_offset.y
            ))
            screen.blit(rotated_thruster, thruster_rect.topleft)
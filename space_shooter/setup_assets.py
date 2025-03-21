import os
import pygame
import math
import random

def create_directories():
    """Create the necessary directories for the game assets."""
    # Get the base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create static directory if it doesn't exist
    static_dir = os.path.join(base_dir, 'static')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
        print(f"Created directory: {static_dir}")
    
    return static_dir

def create_player_ship(static_dir):
    """Create a player ship image and save it to the assets directory."""
    # Initialize Pygame
    pygame.init()
    
    # Set dimensions for the ship image
    width, height = 50, 50
    
    # Create a surface for the ship
    ship_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Ship body (triangle)
    ship_color = (120, 200, 255)  # Light blue
    points = [(width//2, 0), (0, height), (width, height)]
    pygame.draw.polygon(ship_surface, ship_color, points)
    
    # Ship outline
    outline_color = (200, 230, 255)  # Lighter blue
    pygame.draw.polygon(ship_surface, outline_color, points, 2)
    
    # Cockpit (small circle near the top)
    cockpit_color = (220, 240, 255)  # Very light blue
    pygame.draw.circle(ship_surface, cockpit_color, 
                      (width//2, height//3), width//10)
    
    # Wings
    wing_color = (80, 140, 240)  # Darker blue
    wing_left = [(0, height), (width//4, height), (0, height-10)]
    wing_right = [(width, height), (width*3//4, height), (width, height-10)]
    pygame.draw.polygon(ship_surface, wing_color, wing_left)
    pygame.draw.polygon(ship_surface, wing_color, wing_right)
    
    # Engine
    engine_color = (200, 200, 200)  # Silver
    pygame.draw.rect(ship_surface, engine_color, 
                    (width//3, height-12, width//3, 7))
    
    # Save the image
    ship_path = os.path.join(static_dir, 'player_ship.png')
    pygame.image.save(ship_surface, ship_path)
    print(f"Created player ship image: {ship_path}")

def create_asteroid(static_dir):
    """Create an asteroid image and save it to the assets directory."""
    # Set dimensions
    size = 50
    
    # Create a surface for the asteroid
    asteroid_surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Base color
    base_color = (150, 150, 150)  # Grey
    
    # Create an irregular polygon
    points = []
    radius = size // 2
    point_count = 10
    
    for i in range(point_count):
        angle = (i / point_count) * (2 * 3.14159)  # Use radians
        # Add some randomness to the radius
        var_radius = radius * (0.8 + 0.4 * (i / point_count))
        
        x = radius + var_radius * math.cos(angle)
        y = radius + var_radius * math.sin(angle)
        points.append((x, y))
    
    # Draw the asteroid
    pygame.draw.polygon(asteroid_surface, base_color, points)
    
    # Add some texture/craters
    crater_color = (100, 100, 100)  # Darker grey
    import random
    for _ in range(3):
        cx = random.randint(0, size)
        cy = random.randint(0, size)
        crater_radius = random.randint(2, 7)
        pygame.draw.circle(asteroid_surface, crater_color, (cx, cy), crater_radius)
    
    # Save the image
    asteroid_path = os.path.join(static_dir, 'asteroid.png')
    pygame.image.save(asteroid_surface, asteroid_path)
    print(f"Created asteroid image: {asteroid_path}")

def create_bullet(static_dir):
    """Create a bullet image and save it to the assets directory."""
    # Create a surface for the bullet
    bullet_surface = pygame.Surface((6, 6), pygame.SRCALPHA)
    
    # Draw a yellow circle
    pygame.draw.circle(bullet_surface, (255, 255, 100), (3, 3), 3)
    
    # Add a white core for glow effect
    pygame.draw.circle(bullet_surface, (255, 255, 255), (3, 3), 1)
    
    # Save the image
    bullet_path = os.path.join(static_dir, 'bullet.png')
    pygame.image.save(bullet_surface, bullet_path)
    print(f"Created bullet image: {bullet_path}")

def main():
    """Set up all game assets."""
    # Initialize pygame
    pygame.init()
    
    # Create directories
    static_dir = create_directories()
    
    # Create assets
    create_player_ship(static_dir)
    create_asteroid(static_dir)
    create_bullet(static_dir)
    
    # Cleanup
    pygame.quit()
    print("Asset setup complete!")

if __name__ == "__main__":
    main()
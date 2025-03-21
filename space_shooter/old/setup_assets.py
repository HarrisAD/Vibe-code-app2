import os
import pygame

def create_directories():
    """Create the necessary directories for the game assets."""
    # Get the base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create assets directory if it doesn't exist
    assets_dir = os.path.join(base_dir, 'assets')
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
        print(f"Created directory: {assets_dir}")
    
    return assets_dir

def create_player_ship(assets_dir):
    """Create a player ship image and save it to the assets directory."""
    # Set dimensions for the ship image
    width, height = 50, 50
    
    # Create a surface for the ship
    ship_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Ship body (main triangle)
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
    ship_path = os.path.join(assets_dir, 'player_ship.png')
    pygame.image.save(ship_surface, ship_path)
    print(f"Created player ship image: {ship_path}")

def main():
    """Set up all game assets."""
    # Initialize pygame to use its drawing functions
    pygame.init()
    
    # Create directories
    assets_dir = create_directories()
    
    # Create assets
    create_player_ship(assets_dir)
    
    # Cleanup
    pygame.quit()
    print("Asset setup complete!")

if __name__ == "__main__":
    main()
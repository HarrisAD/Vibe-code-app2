import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Game:
    def __init__(self):
        # Set up the display
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Space Shooter")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Add a font for testing text display
        self.font = pygame.font.SysFont(None, 36)

    def handle_events(self):
        # Process all events in the queue
        for event in pygame.event.get():
            # Print event type for debugging
            print(f"Event: {event.type}")
            
            if event.type == pygame.QUIT:
                print("Quit event detected!")
                self.running = False
                return  # Exit the method immediately when quit is detected
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("ESC key pressed - quitting game")
                    self.running = False
                    return  # Exit the method immediately

    def update(self):
        # Update game state here
        pass

    def draw(self):
        # Clear the screen
        self.screen.fill(BLACK)
        
        # Draw game objects here
        # Add a text message showing controls for testing
        controls_text = self.font.render("Press ESC or click X to exit", True, WHITE)
        self.screen.blit(controls_text, (WINDOW_WIDTH//2 - controls_text.get_width()//2, 20))
        
        # Update the display
        pygame.display.flip()

    def run(self):
        print("Game started. Click X or press ESC to exit.")
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        print("Game loop ended. Quitting pygame...")
        pygame.quit()
        print("Exiting program...")
        sys.exit()

if __name__ == "__main__":
    game = Game()
    try:
        game.run()
    except Exception as e:
        print(f"Error occurred: {e}")
        pygame.quit()
        sys.exit(1)
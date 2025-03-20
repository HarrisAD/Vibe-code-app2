import pygame
import sys
import math
import random



# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (20, 20, 20)
CYAN = (0, 255, 255)
ORANGE = (255, 100, 0)
YELLOW = (255, 255, 100)
RED = (255, 50, 50)

# Game States
MENU = 0
PLAYING = 1
GAME_OVER = 2

class Bullet:
    def __init__(self, x, y, angle, speed=10):
        # Position
        self.x = x
        self.y = y
        
        # Size
        self.radius = 3
        
        # Movement
        self.angle = math.radians(angle)
        self.speed = speed
        self.dx = math.sin(self.angle) * self.speed
        self.dy = -math.cos(self.angle) * self.speed
        
        # Create bullet image
        self.image = self.create_bullet_image()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
        # Lifespan in milliseconds (3 seconds)
        self.creation_time = pygame.time.get_ticks()
        self.lifespan = 3000
    
    def create_bullet_image(self):
        # Create a simple circular bullet
        surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, YELLOW, (self.radius, self.radius), self.radius)
        pygame.draw.circle(surface, WHITE, (self.radius, self.radius), self.radius // 2)
        return surface
    
    def update(self, screen_width, screen_height):
        # Move the bullet
        self.x += self.dx
        self.y += self.dy
        
        # Update the rect position
        self.rect.center = (self.x, self.y)
        
        # Check if bullet is out of screen or expired
        current_time = pygame.time.get_ticks()
        if (self.x < -10 or self.x > screen_width + 10 or 
            self.y < -10 or self.y > screen_height + 10 or
            current_time - self.creation_time > self.lifespan):
            return False
        
        # Bullet is still active
        return True
    
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
    
    def get_collision_radius(self):
        return self.radius


class Player:
    def __init__(self, x, y):
        # Position and size
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        
        # Movement
        self.speed = 5
        self.dx = 0
        self.dy = 0
        
        # Create ship image
        self.original_image = self.create_ship_image()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
        # Ship rotation
        self.angle = 0
        self.rotation_speed = 3
        
        # Thruster effect
        self.thruster_active = False
        
        # Shooting mechanics
        self.can_shoot = True
        self.shoot_cooldown = 250  # Milliseconds between shots
        self.last_shot_time = 0
        
        # Lives system
        self.max_lives = 3
        self.lives = self.max_lives
        self.invulnerable = False
        self.invulnerable_time = 0
        self.invulnerable_duration = 3000
        self.visible = True
    
    def create_ship_image(self):
        # Create a triangle ship surface
        ship_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        points = [(self.width//2, 0), (0, self.height), (self.width, self.height)]
        pygame.draw.polygon(ship_surface, CYAN, points)
        pygame.draw.rect(ship_surface, ORANGE, (self.width//4, self.height-10, self.width//3, 5))
        return ship_surface
    
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
        
        # Update shooting cooldown
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shoot_cooldown:
            self.can_shoot = True
        
        # Update invulnerability
        if self.invulnerable:
            if current_time - self.invulnerable_time >= self.invulnerable_duration:
                self.invulnerable = False
                self.visible = True
            else:
                # Flash the ship
                self.visible = ((current_time // 150) % 2 == 0)
    
    def shoot(self):
        if not self.can_shoot:
            return None
        
        # Calculate the bullet position and angle
        angle_rad = math.radians(-self.angle)
        bullet_x = self.x + math.sin(angle_rad) * self.height//2
        bullet_y = self.y - math.cos(angle_rad) * self.height//2
        
        # Create a new bullet
        bullet = Bullet(bullet_x, bullet_y, -self.angle)
        
        # Reset the cooldown
        self.can_shoot = False
        self.last_shot_time = pygame.time.get_ticks()
        
        return bullet
    
    def hit(self):
        # If player is already invulnerable, ignore the hit
        if self.invulnerable:
            return True
        
        # Reduce lives
        self.lives -= 1
        
        # Make player invulnerable temporarily
        self.invulnerable = True
        self.invulnerable_time = pygame.time.get_ticks()
        
        # Return True if the player is still alive, False otherwise
        return self.lives > 0
    
    def draw(self, screen):
        # Only draw the ship if it's visible
        if self.visible:
            # Draw thruster if active
            if self.thruster_active:
                angle_rad = math.radians(self.angle)
                thruster_x = self.x + math.sin(angle_rad) * self.height//2
                thruster_y = self.y + math.cos(angle_rad) * self.height//2
                thruster_size = 10
                points = [
                    (thruster_x, thruster_y),
                    (thruster_x - thruster_size, thruster_y + thruster_size),
                    (thruster_x + thruster_size, thruster_y + thruster_size)
                ]
                pygame.draw.polygon(screen, ORANGE, points)
            
            # Draw the spaceship
            screen.blit(self.image, self.rect.topleft)
    
    def draw_lives(self, screen, x, y, spacing=30):
        # Draw the player's lives as small ships
        for i in range(self.lives):
            # Create a small version of the ship
            mini_ship = pygame.transform.scale(self.original_image, (20, 20))
            screen.blit(mini_ship, (x + i * spacing, y))
    
    def get_collision_radius(self):
        return min(self.width, self.height) // 3
    
    def reset(self, x, y):
        # Reset player position, lives and status for a new game
        self.x = x
        self.y = y
        self.angle = 0
        self.lives = self.max_lives
        self.invulnerable = False
        self.visible = True
        self.rect.center = (self.x, self.y)


class Asteroid:
    def __init__(self, x, y, size):
        # Position
        self.x = x
        self.y = y
        
        # Size categories: 3 = large, 2 = medium, 1 = small
        self.size = size
        
        # Set physical size based on size category
        if self.size == 3:
            self.radius = random.randint(35, 45)
        elif self.size == 2:
            self.radius = random.randint(20, 30)
        else:
            self.radius = random.randint(10, 15)
        
        # Movement
        speed_factor = 4 - self.size  # Smaller asteroids move faster
        self.speed = random.uniform(0.5, 1.5) * speed_factor
        angle = random.uniform(0, math.pi * 2)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed
        
        # Rotation
        self.rotation = 0
        self.rotation_speed = random.uniform(-1, 1)
        
        # Create the asteroid image
        self.original_image = self.create_asteroid_image()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(self.x, self.y))
    
    def create_asteroid_image(self):
        # Create a surface for the asteroid
        size = self.radius * 2
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Choose a color
        color = (150, 150, 150)  # Grey
        
        # Create an irregular shape
        num_points = random.randint(8, 12)
        points = []
        
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            distance = self.radius * random.uniform(0.8, 1.2)
            point_x = self.radius + math.cos(angle) * distance
            point_y = self.radius + math.sin(angle) * distance
            points.append((point_x, point_y))
        
        # Draw the asteroid shape
        pygame.draw.polygon(surface, color, points)
        
        # Add some craters for visual interest
        num_craters = random.randint(2, 5)
        for _ in range(num_craters):
            crater_x = random.randint(int(size * 0.2), int(size * 0.8))
            crater_y = random.randint(int(size * 0.2), int(size * 0.8))
            crater_radius = random.randint(int(size * 0.05), int(size * 0.15))
            crater_color = (100, 100, 100)  # Darker grey
            pygame.draw.circle(surface, crater_color, (crater_x, crater_y), crater_radius)
        
        return surface
    
    def update(self, screen_width, screen_height):
        # Update position
        self.x += self.dx
        self.y += self.dy
        
        # Update rotation
        self.rotation += self.rotation_speed
        
        # Wrap around screen edges
        if self.x < -self.radius:
            self.x = screen_width + self.radius
        elif self.x > screen_width + self.radius:
            self.x = -self.radius
            
        if self.y < -self.radius:
            self.y = screen_height + self.radius
        elif self.y > screen_height + self.radius:
            self.y = -self.radius
        
        # Update rect and rotated image
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=(self.x, self.y))
    
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
    
    def get_collision_radius(self):
        return self.radius * 0.8
    
    def split(self):
        # When an asteroid is hit, it splits into smaller asteroids
        if self.size > 1:
            new_size = self.size - 1
            new_asteroids = []
            
            # Create 2 smaller asteroids
            for _ in range(2):
                offset_x = random.uniform(-10, 10)
                offset_y = random.uniform(-10, 10)
                new_asteroid = Asteroid(self.x + offset_x, self.y + offset_y, new_size)
                new_asteroids.append(new_asteroid)
            
            return new_asteroids
        
        # If it's already the smallest size, return empty list
        return []


class Game:
    def __init__(self):
        # Set up the display
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Space Shooter")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Set up fonts
        self.font_small = pygame.font.SysFont("Arial", 24)
        self.font_medium = pygame.font.SysFont("Arial", 32)
        self.font_large = pygame.font.SysFont("Arial", 64)
        
        # Game state
        self.state = MENU
        
        # Create player spaceship
        self.player = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        
        # Create lists for game objects
        self.asteroids = []
        self.bullets = []
        
        # Asteroid spawning system
        self.asteroid_spawn_timer = 0
        self.asteroid_spawn_delay = 3000  # milliseconds between asteroid spawns
        
        # Score and level
        self.score = 0
        self.high_score = 0
        self.level = 1
        
        # Grid setting
        self.draw_grid = True
    
    def start_new_game(self):
        # Reset game objects and values
        self.asteroids = []
        self.bullets = []
        self.score = 0
        self.level = 1
        
        # Reset player
        self.player.reset(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        
        # Spawn initial asteroids
        self.spawn_initial_asteroids(5)
        
        # Set game state to playing
        self.state = PLAYING
    
    def spawn_initial_asteroids(self, count):
        for _ in range(count):
            self.spawn_asteroid_away_from_player()
    
    def spawn_asteroid_away_from_player(self):
        # Choose a random spawn position at the edge of the screen
        side = random.randint(0, 3)  # 0: top, 1: right, 2: bottom, 3: left
        
        if side == 0:  # Top
            x = random.randint(0, WINDOW_WIDTH)
            y = -50
        elif side == 1:  # Right
            x = WINDOW_WIDTH + 50
            y = random.randint(0, WINDOW_HEIGHT)
        elif side == 2:  # Bottom
            x = random.randint(0, WINDOW_WIDTH)
            y = WINDOW_HEIGHT + 50
        else:  # Left
            x = -50
            y = random.randint(0, WINDOW_HEIGHT)
        
        # Create a new large asteroid
        asteroid = Asteroid(x, y, 3)  # Size 3 = large
        
        # Add to asteroid list
        self.asteroids.append(asteroid)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # In menu, exit. In game or game over, return to menu
                    if self.state == MENU:
                        self.running = False
                    else:  # PLAYING or GAME_OVER
                        self.state = MENU
                
                elif event.key == pygame.K_g:  # Toggle grid with G key
                    self.draw_grid = not self.draw_grid
                
                elif event.key == pygame.K_SPACE:
                    # In menu or game over, start new game. In game, shoot
                    if self.state == MENU or self.state == GAME_OVER:
                        self.start_new_game()
                    elif self.state == PLAYING:
                        self.handle_shooting()
        
    def handle_shooting(self):
        # Handle player shooting
        bullet = self.player.shoot()
        if bullet:
            self.bullets.append(bullet)
    
    def update(self):
        if self.state == PLAYING:
            # Handle player input
            self.player.handle_input()
            
            # Handle continuous shooting with spacebar held down
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.handle_shooting()
            
            # Update player
            self.player.update(WINDOW_WIDTH, WINDOW_HEIGHT)
            
            # Update bullets
            for bullet in self.bullets[:]:
                if not bullet.update(WINDOW_WIDTH, WINDOW_HEIGHT):
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
            
            # Update asteroids
            for asteroid in self.asteroids[:]:
                asteroid.update(WINDOW_WIDTH, WINDOW_HEIGHT)
            
            # Check for collisions
            self.check_collisions()
            
            # Handle asteroid spawning
            current_time = pygame.time.get_ticks()
            if current_time - self.asteroid_spawn_timer > self.asteroid_spawn_delay:
                self.asteroid_spawn_timer = current_time
                max_asteroids = 5 + self.level * 2  # Increase max asteroids with level
                if len(self.asteroids) < max_asteroids:
                    self.spawn_asteroid_away_from_player()
            
            # Level progression - increase level when all asteroids are destroyed
            if len(self.asteroids) == 0:
                self.level += 1
                self.spawn_initial_asteroids(3 + self.level)  # Increase asteroids with level
    
    def check_collisions(self):
        # Check collisions between bullets and asteroids
        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                # Calculate distance between bullet and asteroid centers
                dist_x = bullet.x - asteroid.x
                dist_y = bullet.y - asteroid.y
                distance = math.sqrt(dist_x ** 2 + dist_y ** 2)
                
                # Check if they're colliding
                if distance < bullet.get_collision_radius() + asteroid.get_collision_radius():
                    # Remove the bullet
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    
                    # Add score based on asteroid size
                    self.score += (4 - asteroid.size) * 100
                    
                    # Update high score
                    if self.score > self.high_score:
                        self.high_score = self.score
                    
                    # Split the asteroid
                    new_asteroids = asteroid.split()
                    self.asteroids.extend(new_asteroids)
                    
                    # Remove the hit asteroid
                    if asteroid in self.asteroids:
                        self.asteroids.remove(asteroid)
                    
                    # Break out of the inner loop since the bullet is gone
                    break
        
        # Check collisions between player and asteroids
        if not self.player.invulnerable:  # Only check if player is not invulnerable
            player_radius = self.player.get_collision_radius()
            
            for asteroid in self.asteroids[:]:
                # Calculate distance between player and asteroid centers
                dist_x = self.player.x - asteroid.x
                dist_y = self.player.y - asteroid.y
                distance = math.sqrt(dist_x ** 2 + dist_y ** 2)
                
                # Check if they're colliding
                if distance < player_radius + asteroid.get_collision_radius():
                    # Handle player being hit
                    still_alive = self.player.hit()
                    if not still_alive:
                        # Game over
                        self.state = GAME_OVER
                        return
                    
                    # Break the asteroid
                    new_asteroids = asteroid.split()
                    self.asteroids.extend(new_asteroids)
                    
                    # Remove the hit asteroid
                    if asteroid in self.asteroids:
                        self.asteroids.remove(asteroid)
                    
                    # Only process one collision at a time
                    break

    def draw_background(self):
        # Fill with black background
        self.screen.fill(BLACK)
        
        # Draw a simple grid for reference (if enabled)
        if self.draw_grid:
            grid_spacing = 50
            for x in range(0, WINDOW_WIDTH, grid_spacing):
                pygame.draw.line(self.screen, DARK_GRAY, (x, 0), (x, WINDOW_HEIGHT))
            for y in range(0, WINDOW_HEIGHT, grid_spacing):
                pygame.draw.line(self.screen, DARK_GRAY, (0, y), (WINDOW_WIDTH, y))

    def draw(self):
        # Draw background
        self.draw_background()
        
        if self.state == MENU:
            self.draw_menu()
        elif self.state == PLAYING:
            self.draw_game()
        elif self.state == GAME_OVER:
            self.draw_game_over()
        
        # Update the display
        pygame.display.flip()
    
    def draw_menu(self):
        # Draw title
        title = self.font_large.render("SPACE SHOOTER", True, WHITE)
        self.screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 150))
        
        # Draw high score
        high_score_text = self.font_medium.render(f"High Score: {self.high_score}", True, YELLOW)
        self.screen.blit(high_score_text, (WINDOW_WIDTH//2 - high_score_text.get_width()//2, 250))
        
        # Draw instructions
        start_text = self.font_medium.render("Press SPACE to Start", True, WHITE)
        self.screen.blit(start_text, (WINDOW_WIDTH//2 - start_text.get_width()//2, 350))
        
        quit_text = self.font_medium.render("Press ESC to Quit", True, WHITE)
        self.screen.blit(quit_text, (WINDOW_WIDTH//2 - quit_text.get_width()//2, 400))
        
        # Draw controls
        controls_text = self.font_small.render("Controls: Arrow Keys to Move, A/D to Rotate, SPACE to Shoot", True, CYAN)
        self.screen.blit(controls_text, (WINDOW_WIDTH//2 - controls_text.get_width()//2, 500))
    
    def draw_game(self):
        # Draw asteroids
        for asteroid in self.asteroids:
            asteroid.draw(self.screen)
        
        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(self.screen)
        
        # Draw player
        self.player.draw(self.screen)
        
        # Draw HUD (Heads Up Display)
        self.draw_hud()
    
    def draw_game_over(self):
        # Draw the game objects in the background
        self.draw_game()
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Black with opacity
        self.screen.blit(overlay, (0, 0))
        
        # Draw Game Over text
        gameover_text = self.font_large.render("GAME OVER", True, RED)
        self.screen.blit(gameover_text, (WINDOW_WIDTH//2 - gameover_text.get_width()//2, 150))
        
        # Draw the score
        score_text = self.font_medium.render(f"Your Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (WINDOW_WIDTH//2 - score_text.get_width()//2, 250))
        
        # Draw the high score
        if self.score >= self.high_score:
            high_score_text = self.font_medium.render(f"New High Score!", True, YELLOW)
        else:
            high_score_text = self.font_medium.render(f"High Score: {self.high_score}", True, YELLOW)
        self.screen.blit(high_score_text, (WINDOW_WIDTH//2 - high_score_text.get_width()//2, 300))
        
        # Draw restart instructions
        restart_text = self.font_medium.render("Press SPACE to Restart", True, WHITE)
        self.screen.blit(restart_text, (WINDOW_WIDTH//2 - restart_text.get_width()//2, 400))
        
        menu_text = self.font_medium.render("Press ESC for Main Menu", True, WHITE)
        self.screen.blit(menu_text, (WINDOW_WIDTH//2 - menu_text.get_width()//2, 450))
    
    def draw_hud(self):
        # Draw score
        score_text = self.font_small.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (WINDOW_WIDTH - score_text.get_width() - 20, 20))
        
        # Draw level
        level_text = self.font_small.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(level_text, (WINDOW_WIDTH - level_text.get_width() - 20, 50))
        
        # Draw lives
        lives_text = self.font_small.render("Lives: ", True, WHITE)
        self.screen.blit(lives_text, (20, 20))
        self.player.draw_lives(self.screen, 90, 20)
        
        # Draw controls reminder at the bottom
        controls_text = self.font_small.render("Arrow Keys: Move   A/D: Rotate   SPACE: Shoot   G: Grid   ESC: Menu", True, DARK_GRAY)
        self.screen.blit(controls_text, (WINDOW_WIDTH//2 - controls_text.get_width()//2, WINDOW_HEIGHT - 30))
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

# Run the game
if __name__ == "__main__":
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Error: {e}")
        pygame.quit()
        sys.exit(1)
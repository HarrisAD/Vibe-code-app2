# Space Shooter Game

A simple 2D space shooter game built with Python and Pygame. Control your spaceship, shoot asteroids, and try to survive in space!

## Features (Planned)

- Player-controlled spaceship
- Asteroid obstacles
- Shooting mechanics
- Score tracking
- Simple collision detection
- Game over screen

## Requirements

- Python 3.x
- Pygame library

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install pygame
```

## How to Play

1. Run the game:
```bash
python main.py
```

2. Controls:
- Arrow keys: Move the spaceship
- Spacebar: Shoot
- ESC: Quit game

## Project Structure

```
space_shooter/
├── main.py           # Main game loop and initialization
├── player.py         # Player spaceship class
├── asteroid.py       # Asteroid class
├── bullet.py         # Bullet class
└── assets/          # Game assets (images, sounds)
```

## Development Phases

### Phase 1: Project Setup and Basic Structure
- Set up project directory structure
- Create basic game window
- Implement game loop
- Add basic event handling
- Set up asset loading system

### Phase 2: Player Implementation
- Create player spaceship class
- Implement basic movement controls
- Add ship boundaries
- Create simple ship graphics
- Add ship rotation (optional)

### Phase 3: Asteroid System
- Create asteroid class
- Implement asteroid generation
- Add asteroid movement patterns
- Create asteroid graphics
- Implement asteroid spawning system

### Phase 4: Shooting Mechanics
- Create bullet class
- Implement shooting system
- Add bullet movement
- Create bullet graphics
- Add shooting cooldown

### Phase 5: Collision and Game Logic
- Implement collision detection between:
  - Bullets and asteroids
  - Player and asteroids
- Add asteroid destruction
- Create particle effects (optional)
- Implement basic scoring system

### Phase 6: Game States and UI
- Add main menu
- Implement game over screen
- Create score display
- Add lives system
- Implement restart functionality

### Phase 7: Polish and Enhancement
- Add sound effects
- Implement background music
- Add visual effects
- Create power-ups (optional)
- Add different asteroid types

### Phase 8: Testing and Optimization
- Test all game mechanics
- Optimize performance
- Fix bugs
- Add difficulty levels
- Final polish and cleanup

## Development Roadmap

1. Basic game setup and window creation
2. Player spaceship movement
3. Asteroid generation and movement
4. Shooting mechanics
5. Collision detection
6. Score system
7. Game over screen
8. Polish and additional features

## License

This project is open source and available under the MIT License. 
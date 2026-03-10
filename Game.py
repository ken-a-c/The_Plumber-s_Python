import pygame
import sys

# 1. Initialization
pygame.init()

# 2. Constants and Colors
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Pygame Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Game loop control variable
running = True

# 3. Main Game Loop
while running:
    # 4. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Handle other events like keyboard/mouse input here (e.g., KEYDOWN, MOUSEBUTTONDOWN)

    # 5. Game Logic Updates

    

    # Update positions, check collisions, manage game state, etc. here

    # 6. Drawing
    SCREEN.fill(BLACK)  # Fill the screen with a background color
    # Draw game objects (sprites, shapes, text, etc.) onto the screen here

    # 7. Update the display
    pygame.display.flip()  # or pygame.display.update()

    # 8. Cap the frame rate
    clock.tick(FPS)

# 9. Quit Pygame
pygame.quit()
sys.exit()

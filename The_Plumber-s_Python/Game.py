import pygame
import sys
import time
import random

pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shotgun Side-Scroller: Zombie Phases")

clock = pygame.time.Clock()
font_large = pygame.font.SysFont(None, 72)
font_small = pygame.font.SysFont(None, 40)

# Load images
background = pygame.image.load("background.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

player_img = pygame.image.load("person.png").convert_alpha()
player_width, player_height = 100, 100
player_img = pygame.transform.scale(player_img, (player_width, player_height))

bullet_image = pygame.Surface((10, 5))
bullet_image.fill((255, 0, 0))

ammo_sprite = pygame.image.load("ammo.png").convert_alpha()
ammo_sprite = pygame.transform.scale(ammo_sprite, (30, 30))

zombie_img = pygame.image.load("zombie.png").convert_alpha()
zombie_width, zombie_height = 100, 100
zombie_img = pygame.transform.scale(zombie_img, (zombie_width, zombie_height))

# Player
x = 350
y = 460
speed = 4
facing_right = True
max_health = 30
current_health = max_health

# Bullets
bullets = []
bullet_speed = 15
bullet_range = 200
max_ammo = 10
current_ammo = 3

# Cooldown
shot_cooldown = 0.5
last_shot_time = 0

# Ammo pickups
ammo_pickups = []
ammo_spawn_interval = 5
last_ammo_spawn = time.time()
ammo_amount = 3

# Phases
phase = 1
max_phases = 10
zombies = []

# Music
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)

running = True
game_over = False
game_completed = False

def spawn_wave(phase):
    """Spawn zombies from random sides"""
    new_zombies = []
    num_zombies = phase + 2
    for _ in range(num_zombies):
        side = random.choice(['left', 'right'])
        if side == 'left':
            zombie_x = -random.randint(50, 150)
        else:
            zombie_x = WIDTH + random.randint(50, 150)
        new_zombies.append({
            "x": zombie_x,
            "y": 460,
            "speed": 2,
            "attack_cooldown": 1.5,
            "last_attack": 0,
            "alive": True,
            "facing_right": True
        })
    return new_zombies

# Start first phase
zombies = spawn_wave(phase)

while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    current_time = time.time()

    # Game Over
    if current_health <= 0:
        game_over = True
        screen.fill((0, 0, 0))
        text = font_large.render("GAME OVER", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.update()
        continue

    # Update bullets
    for bullet in bullets[:]:
        bullet["x"] += bullet_speed * bullet["direction"]
        bullet["distance_traveled"] += bullet_speed
        bullet_hit = False
        for z in zombies:
            if z["alive"]:
                z_rect = pygame.Rect(z["x"], z["y"], zombie_width, zombie_height)
                bullet_rect = pygame.Rect(bullet["x"], bullet["y"], 10, 5)
                if bullet_rect.colliderect(z_rect):
                    z["alive"] = False
                    bullet_hit = True
                    break
        if bullet_hit or bullet["distance_traveled"] > bullet_range:
            bullets.remove(bullet)

    # Update zombies
    player_rect = pygame.Rect(x, y, player_width, player_height)
    for z in zombies:
        if z["alive"]:
            dx = x - z["x"]
            if abs(dx) > z["speed"]:
                z["x"] += z["speed"] if dx > 0 else -z["speed"]
            z["facing_right"] = dx > 0

            hit_rect = pygame.Rect(z["x"] + 20, z["y"] + 20, zombie_width - 40, zombie_height - 20)
            if player_rect.colliderect(hit_rect):
                if current_time - z["last_attack"] >= z["attack_cooldown"]:
                    z["last_attack"] = current_time
                    current_health -= 1
                    if current_health < 0:
                        current_health = 0

    # Phase progression & game completion
    all_zombies_dead = all(not z["alive"] for z in zombies)
    if all_zombies_dead and len(bullets) == 0:
        if phase < max_phases:
            phase += 1
            zombies = spawn_wave(phase)
        else:
            game_completed = True  # properly trigger completion

    # Player Movement
    if keys[pygame.K_LEFT]:
        x -= speed
        facing_right = False
    elif keys[pygame.K_RIGHT]:
        x += speed
        facing_right = True

    # Clamp player
    x = max(0, min(WIDTH - player_width, x))
    y = max(0, min(HEIGHT - player_height, y))

    # Shooting
    if keys[pygame.K_SPACE] and current_time - last_shot_time >= shot_cooldown and current_ammo > 0:
        last_shot_time = current_time
        current_ammo -= 1
        offsets = [-5, 0, 5]
        for offset in offsets:
            bullets.append({
                "x": x + player_width // 2 if facing_right else x,
                "y": y + player_height // 2 + offset,
                "direction": 1 if facing_right else -1,
                "distance_traveled": 0
            })

    # Spawn ammo pickups
    if current_time - last_ammo_spawn >= ammo_spawn_interval:
        last_ammo_spawn = current_time
        ammo_x = random.randint(50, WIDTH - 50)
        ammo_y = HEIGHT - 120 + random.randint(0, 20)
        ammo_pickups.append({"x": ammo_x, "y": ammo_y})

    # Collect ammo (stacking)
    for ammo in ammo_pickups[:]:
        ammo_rect = pygame.Rect(ammo["x"], ammo["y"], 30, 30)
        if player_rect.colliderect(ammo_rect):
            current_ammo = min(current_ammo + ammo_amount, max_ammo)
            ammo_pickups.remove(ammo)

    # Draw everything
    screen.blit(background, (0, 0))
    displayed_player = pygame.transform.flip(player_img, not facing_right, False)
    screen.blit(displayed_player, (x, y))

    for bullet in bullets:
        screen.blit(bullet_image, (bullet["x"], bullet["y"]))

    for ammo in ammo_pickups:
        screen.blit(ammo_sprite, (ammo["x"], ammo["y"]))

    for z in zombies:
        if z["alive"]:
            displayed_zombie = pygame.transform.flip(zombie_img, not z["facing_right"], False)
            screen.blit(displayed_zombie, (z["x"], z["y"]))

    # Ammo bar
    for i in range(current_ammo):
        pygame.draw.rect(screen, (255, 255, 0), (10 + i*22, 10, 20, 20))

    # Health bar
    for i in range(current_health):
        pygame.draw.rect(screen, (255, 0, 0), (10 + i*22, 40, 20, 20))

    # Phase display
    phase_text = font_small.render(f"Phase: {phase}", True, (255, 255, 255))
    screen.blit(phase_text, (WIDTH - 140, 10))

    # Display Game Completed if finished
    if game_completed:
        screen.fill((0, 0, 0))
        text = font_large.render("GAME COMPLETED", True, (0, 255, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

    pygame.display.update()

pygame.quit()
sys.exit()
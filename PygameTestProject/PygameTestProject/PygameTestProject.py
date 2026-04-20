import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Player properties
player_pos = [WIDTH // 2, HEIGHT - 50]
player_size = 50

# Enemy properties
enemy_size = 50
enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
enemy_speed = 10

score = 0
game_over = False

# Trail properties
trail = []
trail_length = 10  # Number of trail squares

# Load images and scale to object size
dino_img = pygame.image.load("Dinosaur.png").convert_alpha()
dino_img = pygame.transform.scale(dino_img, (player_size, player_size))
rock_img = pygame.image.load("BigRock.png").convert_alpha()
rock_img = pygame.transform.scale(rock_img, (enemy_size, enemy_size))

while not game_over:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            game_over = True

    # --- BUG 1: Movement Logic ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= 5 + score*1.005  # Should move left
    if keys[pygame.K_RIGHT]:
        player_pos[0] += 5 + score*1.005 # Should move right

    # Update enemy position
    enemy_pos[1] += enemy_speed + score*1.03  # Enemy speed increases with score 

    # --- BUG 2: Resetting the Enemy ---
    if enemy_pos[1] > HEIGHT:
        enemy_pos[1] = 0
        enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
        score += 1
        print(f"Score: {score}")

    # --- BUG 3: Collision Detection --
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
    enemy_rect = pygame.Rect(enemy_pos[0], enemy_pos[1], enemy_size, enemy_size)
    if player_rect.colliderect(enemy_rect):
        print("Game Over!")
        game_over = True

    # Update trail
    trail.append(tuple(player_pos))
    if len(trail) > trail_length:
        trail.pop(0)

    # Drawing
    screen.fill((WHITE))

    # Draw trail with decreasing opacity
    for i, pos in enumerate(trail):
        alpha = int(150 * (i + 1) / trail_length)
        trail_surface = pygame.Surface((player_size, player_size), pygame.SRCALPHA)
        trail_surface.fill((0, 200, 0, alpha))
        screen.blit(trail_surface, pos)

    # Draw enemy and player images
    screen.blit(rock_img, (enemy_pos[0], enemy_pos[1]))
    screen.blit(dino_img, (player_pos[0], player_pos[1]))

    pygame.display.update()
    clock.tick(30)

pygame.quit()

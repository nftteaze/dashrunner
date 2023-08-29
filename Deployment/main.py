import random
import pygame
import os

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
grass_green = (0, 128, 0)
scale_factor = 1.0  # Default scale factor for desktop

# Set maximum screen dimensions for desktop
MAX_WIDTH = 800
MAX_HEIGHT = 600

# Check if the screen size exceeds the maximum dimensions
screen_info = pygame.display.Info()
if screen_info.current_w > MAX_WIDTH or screen_info.current_h > MAX_HEIGHT:
    # Calculate the scale factor based on maximum dimensions
    scale_factor = min(MAX_WIDTH / 450, MAX_HEIGHT / 300)

# Load and resize player and obstacle images
player_image = pygame.image.load('player.png')
obstacle_image = pygame.image.load('obstacle.png')

player_size = int(16 * scale_factor)
player_image = pygame.transform.scale(player_image, (player_size, player_size))
obstacle_size = int(16 * scale_factor)
obstacle_image = pygame.transform.scale(obstacle_image, (obstacle_size, obstacle_size))

# Set up game variables
score = 0
player_x = int(50 * scale_factor)
player_y = int(200 * scale_factor)
y_change = 0
gravity = 1 * scale_factor
x_change = 0
obstacles = [int(300 * scale_factor), int(450 * scale_factor), int(600 * scale_factor)]
obstacle_speed = 2 * scale_factor
active = False

# Create the game screen
screen = pygame.display.set_mode((int(450 * scale_factor), int(300 * scale_factor)))
pygame.display.set_caption('DashRunner')
background = black
fps = 60
font = pygame.font.Font('freesansbold.ttf', int(16 * scale_factor))
timer = pygame.time.Clock()

# Stars initialization
num_stars = 100
stars = [(random.randint(0, int(450 * scale_factor)), random.randint(0, int(220 * scale_factor))) for _ in range(num_stars)]  # Stars won't go below the grass
star_update_counter = 0
star_update_rate = 5

def draw_stars():
    for star in stars:
        pygame.draw.circle(screen, white, star, 2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Handle key events for desktop and touch events for mobile
        if event.type == pygame.KEYDOWN:
            if not active and event.key == pygame.K_SPACE:
                obstacles = [int(300 * scale_factor), int(450 * scale_factor), int(600 * scale_factor)]
                player_x = int(50 * scale_factor)
                score = 0
                active = True
            elif active:
                if event.key == pygame.K_SPACE and y_change == 0:
                    y_change = int(18 * scale_factor)
                if event.key == pygame.K_RIGHT:
                    x_change = int(2 * scale_factor)
                if event.key == pygame.K_LEFT:
                    x_change = int(-2 * scale_factor)
        if event.type == pygame.KEYUP and active:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                x_change = 0

    timer.tick(fps)
    screen.fill(background)

    # Draw grass green color below the floor
    pygame.draw.rect(screen, grass_green, [0, int(220 * scale_factor), int(450 * scale_factor), int(300 * scale_factor) - int(220 * scale_factor)])

    # Create a gradient effect for the mist
    for y in range(int(40 * scale_factor)):
        alpha = int((1 - y / (40 * scale_factor)) * 255)  # Calculate alpha value for gradient
        pygame.draw.rect(screen, (255, 255, 255, alpha), [0, y, int(450 * scale_factor), 1])

    # Update star positions only when the counter reaches the update rate
    if star_update_counter >= star_update_rate:
        star_update_counter = 0
        new_stars = []
        for star in stars:
            new_y = star[1] + 1 if star[1] < int(220 * scale_factor) else random.randint(0, int(220 * scale_factor))
            new_stars.append((star[0], new_y))
        stars = new_stars
        # Move stars down by 1 pixel or wrap them to the top if they go below the grass

    # Increment the star update counter
    star_update_counter += 1

    draw_stars()

    if not active:
        instruction_text = font.render(f'Space Bar to Start', True, white, black)
        screen.blit(instruction_text, (int(140 * scale_factor), int(50 * scale_factor)))
        instruction_text2 = font.render(f'Space Bar Jumps. Left/Right Moves', True, white, black)
        screen.blit(instruction_text2, (int(80 * scale_factor), int(90 * scale_factor)))

    score_text = font.render(f'score: {score}', True, white, black)
    screen.blit(score_text, (int(160 * scale_factor), int(250 * scale_factor)))
    floor = pygame.draw.rect(screen, white, [0, int(220 * scale_factor), int(450 * scale_factor), int(5 * scale_factor)])

    # Draw player and obstacles using images
    screen.blit(player_image, (player_x, player_y))
    screen.blit(obstacle_image, (obstacles[0], int(200 * scale_factor)))
    screen.blit(obstacle_image, (obstacles[1], int(200 * scale_factor)))
    screen.blit(obstacle_image, (obstacles[2], int(200 * scale_factor)))

    for i in range(len(obstacles)):
        if active:
            obstacles[i] -= obstacle_speed
            if obstacles[i] < -obstacle_size:
                obstacles[i] = random.randint(int(470 * scale_factor), int(570 * scale_factor))
                score += 1
            player_rect = player_image.get_rect(topleft=(player_x, player_y))
            obstacle_rect = obstacle_image.get_rect(topleft=(obstacles[i], int(200 * scale_factor)))
            if player_rect.colliderect(obstacle_rect):
                active = False

    if 0 <= player_x <= int(450 * scale_factor) - player_size:
        player_x += x_change
    if player_x < 0:
        player_x = 0
    if player_x > int(450 * scale_factor) - player_size:
        player_x = int(450 * scale_factor) - player_size

    if y_change > 0 or player_y < int(220 * scale_factor):
        player_y -= y_change
        y_change -= gravity
    if player_y > int(200 * scale_factor):
        player_y = int(200 * scale_factor)
    if player_y == int(200 * scale_factor) and y_change < 0:
        y_change = 0

    pygame.display.flip()

pygame.quit()



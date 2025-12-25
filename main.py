import pygame
import random
import sys

# --- Setup ---
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# CHANGE 1: Window ka naam badla
pygame.display.set_caption("JetStorm: Galaxy Defender 🚀")

clock = pygame.time.Clock()
FPS = 60

# --- Colors ---
BLACK = (10, 10, 20)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BRIGHT_RED = (255, 0, 0)
GREEN = (0, 200, 0)
BRIGHT_GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# Fonts
font = pygame.font.SysFont("Verdana", 20, bold=True)
button_font = pygame.font.SysFont("Verdana", 30, bold=True)
title_font = pygame.font.SysFont("Verdana", 60, bold=True)

# --- Global Variables ---
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - 100
player_speed = 7
player_health = 100

bullets = []
enemies = []
particles = []
stars = []

score = 0
game_state = "MENU" # States: MENU, PLAYING, GAMEOVER

# Background Stars
for i in range(50):
    stars.append([random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.randint(1, 3)])

# --- Functions ---

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def draw_button(msg, x, y, w, h, inactive_color, active_color, action=None):
    """Button click check karne ke liye"""
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    clicked = False
    
    # Check if mouse is over button
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h))
        if click[0] == 1 and action != None:
            clicked = True
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))

    draw_text(msg, button_font, WHITE, screen, x + (w/2), y + (h/2))
    return clicked

def reset_game():
    global player_x, player_health, score, enemies, bullets, particles
    player_x = SCREEN_WIDTH // 2
    player_health = 100
    score = 0
    enemies = []
    bullets = []
    particles = []

def draw_player(x, y):
    # Spaceship Design
    pygame.draw.polygon(screen, ORANGE, [(x + 20, y + 60), (x + 30, y + 80 + random.randint(0,5)), (x + 40, y + 60)])
    pygame.draw.polygon(screen, CYAN, [(x, y + 40), (x + 30, y), (x + 60, y + 40)]) 
    pygame.draw.rect(screen, WHITE, (x + 25, y - 10, 10, 60))
    pygame.draw.circle(screen, RED, (x + 30, y + 20), 5)

def create_explosion(x, y):
    for _ in range(15):
        particles.append([[x, y], [random.randint(-5, 5), random.randint(-5, 5)], random.randint(20, 40)])

# --- Main Loop ---
running = True
while running:
    screen.fill(BLACK)
    
    # Stars Animation
    for star in stars:
        star[1] += star[2]
        pygame.draw.circle(screen, WHITE, (star[0], star[1]), 1)
        if star[1] > SCREEN_HEIGHT:
            star[1] = 0
            star[0] = random.randint(0, SCREEN_WIDTH)

    # --- EVENT HANDLING ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Firing Logic
        if game_state == "PLAYING":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append([player_x + 10, player_y])
                    bullets.append([player_x + 50, player_y])

    # --- STATE 1: MENU SCREEN ---
    if game_state == "MENU":
        # CHANGE 2: Screen par naam badla
        draw_text("JETSTORM", title_font, CYAN, screen, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100)
        draw_text("Galaxy Defender Ready", font, WHITE, screen, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40)
        
        if draw_button("START MISSION", 250, 350, 300, 60, GREEN, BRIGHT_GREEN, "play"):
            reset_game()
            game_state = "PLAYING"
            
        if draw_button("EXIT", 250, 430, 300, 60, RED, BRIGHT_RED, "quit"):
            running = False

    # --- STATE 2: PLAYING GAME ---
    elif game_state == "PLAYING":
        
        # Player Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - 60:
            player_x += player_speed

        draw_player(player_x, player_y)

        # Bullets
        for b in bullets[:]:
            b[1] -= 10
            pygame.draw.circle(screen, YELLOW, (b[0], b[1]), 4)
            if b[1] < 0: bullets.remove(b)

        # Enemies
        if random.randint(1, 40) == 1:
            enemies.append([random.randint(0, SCREEN_WIDTH - 50), -50])

        for e in enemies[:]:
            e[1] += 5 
            pygame.draw.rect(screen, RED, (e[0], e[1], 50, 40))
            pygame.draw.circle(screen, GREEN, (e[0] + 25, e[1] + 20), 10)
            
            # Collision: Bullet -> Enemy
            enemy_rect = pygame.Rect(e[0], e[1], 50, 40)
            for b in bullets[:]:
                bullet_rect = pygame.Rect(b[0], b[1], 8, 8)
                if enemy_rect.colliderect(bullet_rect):
                    try:
                        bullets.remove(b)
                        enemies.remove(e)
                        score += 10
                        create_explosion(e[0]+25, e[1]+20)
                    except: pass
            
            # Collision: Enemy -> Player
            player_rect = pygame.Rect(player_x, player_y, 60, 60)
            if player_rect.colliderect(enemy_rect):
                enemies.remove(e)
                player_health -= 25
                create_explosion(player_x+30, player_y+30)
                if player_health <= 0:
                    game_state = "GAMEOVER"

            if e[1] > SCREEN_HEIGHT: enemies.remove(e)

        # Particles
        for p in particles[:]:
            p[0][0] += p[1][0]
            p[0][1] += p[1][1]
            p[2] -= 1
            pygame.draw.circle(screen, ORANGE, (int(p[0][0]), int(p[0][1])), 3)
            if p[2] <= 0: particles.remove(p)

        # UI
        draw_text(f"Score: {score}", font, WHITE, screen, SCREEN_WIDTH - 80, 30)
        pygame.draw.rect(screen, RED, (10, 10, 200, 20))
        if player_health > 0:
            pygame.draw.rect(screen, GREEN, (10, 10, 2 * player_health, 20))
        pygame.draw.rect(screen, WHITE, (10, 10, 200, 20), 2)

    # --- STATE 3: GAME OVER ---
    elif game_state == "GAMEOVER":
        draw_text("MISSION FAILED", title_font, RED, screen, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100)
        draw_text(f"Final Score: {score}", font, YELLOW, screen, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40)

        if draw_button("RETRY MISSION", 250, 350, 300, 60, GREEN, BRIGHT_GREEN, "play"):
            reset_game()
            game_state = "PLAYING"
            
        if draw_button("ABORT (QUIT)", 250, 430, 300, 60, RED, BRIGHT_RED, "quit"):
            running = False

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()
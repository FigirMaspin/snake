import pygame
import random
import pygame.freetype
import time
import os
import sys
import math   # for animations

# ---- init ----
pygame.init()

# ---- colors ----
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
GRAY = (169, 169, 169)
RED = (255, 0, 0)

# For overlays with transparency
OVERLAY_COLOR = (10, 10, 10, 200)

# ---- constants ----
GRID_SIZE = 20
CELL_SIZE = 30
SCREEN_WIDTH = GRID_SIZE * CELL_SIZE
SCREEN_HEIGHT = GRID_SIZE * CELL_SIZE

# ---- window ----
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game - Sprites, Animations & Pause Menu")

# ---- fonts ----
score_font = pygame.freetype.SysFont("Arial", 22)
menu_title_font = pygame.freetype.SysFont("Arial", 44, bold=True)
menu_font = pygame.freetype.SysFont("Arial", 28)

# ---- clock ----
clock = pygame.time.Clock()

# ---- high score file ----
HIGHSCORE_FILE = "highscore.txt"

def load_high_score():
    if not os.path.exists(HIGHSCORE_FILE):
        return 0
    try:
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read().strip() or "0")
    except:
        return 0

def save_high_score(n):
    try:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(int(n)))
    except:
        pass

HIGH_SCORE = load_high_score()

# ---- load sprites ----
apple_img = pygame.image.load("C:\Users\RUDRAKSH\Documents\Hackathon\snakefolder\assets").convert_alpha()
star_img = pygame.image.load("star.png").convert_alpha()
fire_img = pygame.image.load("fire.png").convert_alpha()
hole_img = pygame.image.load("blackhole.png").convert_alpha()
snake_head_img = pygame.image.load("snake_head.png").convert_alpha()
snake_body_img = pygame.image.load("snake_body.png").convert_alpha()

# Scale sprites to cell size
apple_img = pygame.transform.smoothscale(apple_img, (CELL_SIZE, CELL_SIZE))
star_img = pygame.transform.smoothscale(star_img, (CELL_SIZE, CELL_SIZE))
fire_img = pygame.transform.smoothscale(fire_img, (CELL_SIZE, CELL_SIZE))
hole_img = pygame.transform.smoothscale(hole_img, (CELL_SIZE, CELL_SIZE))
snake_head_img = pygame.transform.smoothscale(snake_head_img, (CELL_SIZE, CELL_SIZE))
snake_body_img = pygame.transform.smoothscale(snake_body_img, (CELL_SIZE, CELL_SIZE))

# ---- helper functions ----
def place_black_holes():
    while True:
        b1 = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
        b2 = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
        if abs(b1[0]-b2[0]) + abs(b1[1]-b2[1]) >= 5:
            return b1, b2

def draw_grid():
    grid_color = (200, 200, 200)
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, grid_color, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, grid_color, (0, y), (SCREEN_WIDTH, y))

def draw_snake(snake, direction, boosted):
    for i, segment in enumerate(snake):
        x, y = segment[0]*CELL_SIZE, segment[1]*CELL_SIZE
        if i == 0:  # head
            angle = 0
            if direction == [1,0]: angle = 270
            elif direction == [-1,0]: angle = 90
            elif direction == [0,1]: angle = 0
            elif direction == [0,-1]: angle = 180
            head = pygame.transform.rotate(snake_head_img, angle)
            if boosted:
                glow = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                pygame.draw.circle(glow, (0,255,255,120), (CELL_SIZE//2,CELL_SIZE//2), CELL_SIZE//2)
                screen.blit(glow, (x,y))
            screen.blit(head, (x,y))
        else:  # body
            screen.blit(snake_body_img, (x,y))

def draw_apple(pos, tick):
    scale = CELL_SIZE + int(2 * (1 + math.sin(tick/12)))
    img = pygame.transform.smoothscale(apple_img, (scale, scale))
    rect = img.get_rect(center=(pos[0]*CELL_SIZE+CELL_SIZE//2, pos[1]*CELL_SIZE+CELL_SIZE//2))
    screen.blit(img, rect)

def draw_star(pos, tick):
    scale = CELL_SIZE + int(3 * (1 + math.sin(tick/9)))
    img = pygame.transform.smoothscale(star_img, (scale, scale))
    rect = img.get_rect(center=(pos[0]*CELL_SIZE+CELL_SIZE//2, pos[1]*CELL_SIZE+CELL_SIZE//2))
    screen.blit(img, rect)

def draw_specials(obstacle, star, bh1, bh2, tick):
    screen.blit(fire_img, (obstacle[0]*CELL_SIZE, obstacle[1]*CELL_SIZE))
    draw_star(star, tick)
    if bh1 and bh2:
        screen.blit(hole_img, (bh1[0]*CELL_SIZE, bh1[1]*CELL_SIZE))
        screen.blit(hole_img, (bh2[0]*CELL_SIZE, bh2[1]*CELL_SIZE))

def draw_score(score, high):
    s,_ = score_font.render(f"Score: {score}", BLACK)
    h,_ = score_font.render(f"High Score: {high}", BLACK)
    screen.blit(s, (8,6))
    screen.blit(h, (8,30))

def draw_button(rect,text,hovered=False):
    bg = (40,40,40) if not hovered else (60,60,60)
    border = CYAN if hovered else GRAY
    pygame.draw.rect(screen,bg,rect,border_radius=8)
    pygame.draw.rect(screen,border,rect,2,border_radius=8)
    t,r = menu_font.render(text, WHITE)
    r.center = rect.center
    screen.blit(t,r)

def draw_text_with_shadow(text, font, pos, color, shadow_color=(50,50,50)):
    surf, rect = font.render(text, color)
    shadow, _ = font.render(text, shadow_color)
    screen.blit(shadow, (pos[0]+2, pos[1]+2))
    screen.blit(surf, pos)

def reset_game_state():
    snake = [[10,10],[9,10],[8,10]]
    apple = [random.randint(1,GRID_SIZE-2),random.randint(1,GRID_SIZE-2)]
    obstacle = [random.randint(1,GRID_SIZE-2),random.randint(1,GRID_SIZE-2)]
    star = [random.randint(1,GRID_SIZE-2),random.randint(1,GRID_SIZE-2)]
    direction = [1,0]
    return snake, apple, obstacle, star, direction, 0, False, 0, None, None

# ---- game over screen ----
def game_over_screen(score, high_score):
    screen.fill(WHITE)
    t, r = menu_title_font.render("GAME OVER", RED)
    r.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 60)
    screen.blit(t, r)

    s, sr = menu_font.render(f"Score: {score}", BLACK)
    sr.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
    screen.blit(s, sr)

    h, hr = menu_font.render(f"High Score: {high_score}", BLACK)
    hr.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40)
    screen.blit(h, hr)

    prompt, pr = menu_font.render("Press R to Restart or Q to Quit", GRAY)
    pr.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100)
    screen.blit(prompt, pr)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True   # restart
                elif event.key == pygame.K_q:
                    return False  # quit

# ---- main game ----
def game():
    global HIGH_SCORE

    # ---- difficulty selection ----
    difficulty = None
    while difficulty not in ("E","N","H"):
        screen.fill(WHITE)
        t,r = menu_title_font.render("Select Difficulty: E/N/H",BLACK)
        r.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        
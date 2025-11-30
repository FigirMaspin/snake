import pygame
import random
import pygame.freetype
import time
import os
import sys
import math

# ---- init ----
pygame.init()

# ---- colors ----
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)

# ---- constants ----
GRID_SIZE = 20
CELL_SIZE = 30
SCREEN_WIDTH = GRID_SIZE * CELL_SIZE
SCREEN_HEIGHT = GRID_SIZE * CELL_SIZE

# ---- window ----
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game - Jungle Edition")

# ---- fonts ----
apple_font = pygame.freetype.SysFont("segoeuisymbol", CELL_SIZE)
star_font = pygame.freetype.SysFont("segoeuisymbol", CELL_SIZE)
fire_font = pygame.freetype.SysFont("segoeuisymbol", CELL_SIZE)
hole_font = pygame.freetype.SysFont("segoeuisymbol", CELL_SIZE)
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

# ---- helper functions ----
def get_random_cell(exclude=[]):
    while True:
        cell = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
        if cell not in exclude:
            return cell

def place_black_holes(exclude=[]):
    while True:
        b1 = get_random_cell(exclude)
        temp_exclude = exclude + [b1]
        b2 = get_random_cell(temp_exclude)
        if abs(b1[0]-b2[0]) + abs(b1[1]-b2[1]) >= 5:
            return b1, b2

def draw_snake(snake, direction, boosted):
    snake_color = CYAN if boosted else GREEN
    for segment in snake[1:]:
        pygame.draw.rect(screen, snake_color, pygame.Rect(segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    head = snake[0]
    x = head[0]*CELL_SIZE
    y = head[1]*CELL_SIZE
    radius = CELL_SIZE // 2
    pygame.draw.rect(screen, snake_color, pygame.Rect(x, y, CELL_SIZE, CELL_SIZE))
    if direction == [1,0]:
        pygame.draw.circle(screen, snake_color, (x+CELL_SIZE, y+CELL_SIZE//2), radius)
        eye_y_offsets = [CELL_SIZE//3, 2*CELL_SIZE//3]
        eye_x = x + 3*CELL_SIZE//4
        left_eye = (eye_x, y + eye_y_offsets[0])
        right_eye = (eye_x, y + eye_y_offsets[1])
    elif direction == [-1,0]:
        pygame.draw.circle(screen, snake_color, (x, y+CELL_SIZE//2), radius)
        eye_y_offsets = [CELL_SIZE//3, 2*CELL_SIZE//3]
        eye_x = x + CELL_SIZE//4
        left_eye = (eye_x, y + eye_y_offsets[0])
        right_eye = (eye_x, y + eye_y_offsets[1])
    elif direction == [0,1]:
        pygame.draw.circle(screen, snake_color, (x+CELL_SIZE//2, y+CELL_SIZE), radius)
        eye_x_offsets = [CELL_SIZE//3, 2*CELL_SIZE//3]
        eye_y = y + 3*CELL_SIZE//4
        left_eye = (x + eye_x_offsets[0], eye_y)
        right_eye = (x + eye_x_offsets[1], eye_y)
    else:
        pygame.draw.circle(screen, snake_color, (x+CELL_SIZE//2, y), radius)
        eye_x_offsets = [CELL_SIZE//3, 2*CELL_SIZE//3]
        eye_y = y + CELL_SIZE//4
        left_eye = (x + eye_x_offsets[0], eye_y)
        right_eye = (x + eye_x_offsets[1], eye_y)
    eye_radius = CELL_SIZE//8
    pygame.draw.circle(screen, BLACK, left_eye, eye_radius)
    pygame.draw.circle(screen, BLACK, right_eye, eye_radius)

def draw_apple(pos):
    surf, rect = apple_font.render("🍎", RED)
    rect.topleft = (pos[0]*CELL_SIZE, pos[1]*CELL_SIZE)
    screen.blit(surf, rect)

def draw_specials(obstacle, star, bh1, bh2):
    fire_surf, fire_rect = fire_font.render("🔥", ORANGE)
    fire_rect.center = (obstacle[0]*CELL_SIZE+CELL_SIZE//2, obstacle[1]*CELL_SIZE+CELL_SIZE//2)
    screen.blit(fire_surf, fire_rect)
    star_surf, star_rect = star_font.render("⭐", YELLOW)
    star_surf = pygame.transform.scale(star_surf, (CELL_SIZE, CELL_SIZE))
    star_rect.topleft = (star[0]*CELL_SIZE, star[1]*CELL_SIZE)
    screen.blit(star_surf, star_rect)
    if bh1 and bh2:
        h1,r1 = hole_font.render("⚫", BLACK)
        h1 = pygame.transform.scale(h1,(CELL_SIZE,CELL_SIZE))
        r1.topleft = (bh1[0]*CELL_SIZE, bh1[1]*CELL_SIZE)
        screen.blit(h1,r1)
        h2,r2 = hole_font.render("⚫", BLACK)
        h2 = pygame.transform.scale(h2,(CELL_SIZE,CELL_SIZE))
        r2.topleft = (bh2[0]*CELL_SIZE, bh2[1]*CELL_SIZE)
        screen.blit(h2,r2)

def draw_score(score, high):
    s,_ = score_font.render(f"Score: {score}", WHITE)
    h,_ = score_font.render(f"High Score: {high}", WHITE)
    screen.blit(s, (8,6))
    screen.blit(h, (8,30))

def draw_button(rect,text,hovered=False):
    bg = (40,40,40) if not hovered else (60,60,60)
    border = CYAN if hovered else GREEN
    pygame.draw.rect(screen,bg,rect,border_radius=8)
    pygame.draw.rect(screen,border,rect,2,border_radius=8)
    t,r = menu_font.render(text, WHITE)
    r.center = rect.center
    screen.blit(t,r)

def reset_game_state():
    snake = [[10,10],[9,10],[8,10]]
    exclude = snake.copy()
    apple = get_random_cell(exclude); exclude.append(apple)
    obstacle = get_random_cell(exclude); exclude.append(obstacle)
    star = get_random_cell(exclude); exclude.append(star)
    bh1, bh2 = None, None
    direction = [1,0]
    return snake, apple, obstacle, star, direction, 0, False, 0, bh1, bh2

# ---- jungle effects ----
fog_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
fog_surface.fill((0,0,0,70))
vignette = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
for i in range(300):
    shade = max(0, min(255, int(80 * (i / 300))))
    pygame.draw.rect(vignette, (0,0,0,shade), (i,i,SCREEN_WIDTH-2*i,SCREEN_HEIGHT-2*i), 4)

fireflies = []
for _ in range(25):
    fireflies.append({
        "x": random.randint(0, SCREEN_WIDTH),
        "y": random.randint(0, SCREEN_HEIGHT),
        "dx": random.uniform(-0.5, 0.5),
        "dy": random.uniform(-0.5, 0.5),
        "brightness": random.randint(120, 255),
        "pulse": random.choice([-1, 1])
    })

def update_fireflies():
    for f in fireflies:
        f["x"] += f["dx"]
        f["y"] += f["dy"]
        if random.random() < 0.01:
            f["dx"] = random.uniform(-0.5, 0.5)
            f["dy"] = random.uniform(-0.5, 0.5)
        if f["x"] < 0: f["x"] = SCREEN_WIDTH
        if f["x"] > SCREEN_WIDTH: f["x"] = 0
        if f["y"] < 0: f["y"] = SCREEN_HEIGHT
        if f["y"] > SCREEN_HEIGHT: f["y"] = 0
        f["brightness"] += f["pulse"] * 2
        if f["brightness"] >= 255: f["brightness"]=255; f["pulse"]=-1
        if f["brightness"] <= 80: f["brightness"]=80; f["pulse"]=1

def draw_fireflies():
    for f in fireflies:
        pygame.draw.circle(screen, (255,255,150,f["brightness"]), (int(f["x"]),int(f["y"])), 3)

leaf_images = []
for i in range(3):
    leaf = pygame.Surface((20, 20), pygame.SRCALPHA)
    pygame.draw.polygon(leaf, (40+i*20, 120+i*30, 40), [(10,0),(20,10),(10,20),(0,10)])
    leaf_images.append(leaf)

falling_leaves = []
for _ in range(15):
    falling_leaves.append({
        "x": random.randint(0, SCREEN_WIDTH),
        "y": random.randint(-SCREEN_HEIGHT, 0),
        "speed": random.uniform(1, 2.5),
        "img": random.choice(leaf_images),
        "sway": random.uniform(0.5, 2),
        "angle": random.randint(0, 360)
    })

def update_leaves():
    for leaf in falling_leaves:
        leaf["y"] += leaf["speed"]
        leaf["x"] += math.sin(pygame.time.get_ticks()/300 * leaf["sway"]) * 0.7
        leaf["angle"] += 2
        if leaf["y"] > SCREEN_HEIGHT:
            leaf["y"] = random.randint(-200, -20)
            leaf["x"] = random.randint(0, SCREEN_WIDTH)

def draw_leaves():
    for leaf in falling_leaves:
        rotated = pygame.transform.rotate(leaf["img"], leaf["angle"])
        screen.blit(rotated, (leaf["x"], leaf["y"]))

vines = []
for x in range(0, SCREEN_WIDTH, 150):
    vine_len = random.randint(80, 200)
    vines.append((x, vine_len))

def draw_vines():
    for x,length in vines:
        pygame.draw.line(screen, (20,80,40), (x,0),(x,length),6)
        pygame.draw.circle(screen,(20,80,40),(x,length),8)

# ---- game over screen with Restart/Quit ----
def game_over_screen(score, high_score):
    clock_go = pygame.time.Clock()
    screen.fill(BLACK)
    
    t, r = menu_title_font.render("Game Over", RED)
    r.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-80)
    screen.blit(t, r)
    
    s, r2 = score_font.render(f"Score: {score}", WHITE)
    r2.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-20)
    screen.blit(s, r2)
    
    h, r3 = score_font.render(f"High Score: {high_score}", WHITE)
    r3.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2+20)
    screen.blit(h, r3)

    btn_w, btn_h = 180, 50
    restart_btn = pygame.Rect(SCREEN_WIDTH//2 - btn_w - 20, SCREEN_HEIGHT//2 + 80, btn_w, btn_h)
    quit_btn = pygame.Rect(SCREEN_WIDTH//2 + 20, SCREEN_HEIGHT//2 + 80, btn_w, btn_h)

    while True:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_btn.collidepoint((mx,my)):
                    return "restart"
                elif quit_btn.collidepoint((mx,my)):
                    pygame.quit()
                    sys.exit()

        draw_button(restart_btn, "Restart", restart_btn.collidepoint((mx,my)))
        draw_button(quit_btn, "Quit", quit_btn.collidepoint((mx,my)))

        pygame.display.flip()
        clock_go.tick(30)

# ---- main game ----
def game():
    global HIGH_SCORE

    # ---- difficulty selection ----
    difficulty = None
    while difficulty not in ("E","N","H"):
        screen.fill((200,240,200))
        t,r = menu_title_font.render("Select Difficulty: E/N/H",BLACK)
        r.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        screen.blit(t,r)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e: difficulty="E"
                if event.key == pygame.K_n: difficulty="N"
                if event.key == pygame.K_h: difficulty="H"
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    normal_rate = {"E":5,"N":7,"H":10}[difficulty]
    boost_extra = 5

    snake, apple, obstacle, star, direction, score, boosted, boost_end, bh1, bh2 = reset_game_state()
    running = True
    menu_active = False
    confirm_active = False
    confirm_action = None

    menu_box = pygame.Rect(SCREEN_WIDTH*0.2, SCREEN_HEIGHT*0.2, SCREEN_WIDTH*0.6, SCREEN_HEIGHT*0.6)
    btn_w, btn_h = 240, 54
    resume_btn = pygame.Rect(menu_box.centerx-btn_w//2, menu_box.top+120, btn_w, btn_h)
    restart_btn = pygame.Rect(menu_box.centerx-btn_w//2, menu_box.top+120+74, btn_w, btn_h)
    quit_btn = pygame.Rect(menu_box.centerx-btn_w//2, menu_box.top+120+148, btn_w, btn_h)
    confirm_box = pygame.Rect((SCREEN_WIDTH-420)//2, (SCREEN_HEIGHT-180)//2, 420, 180)
    yes_btn = pygame.Rect(confirm_box.centerx-110, confirm_box.bottom-60,100,42)
    no_btn = pygame.Rect(confirm_box.centerx+10, confirm_box.bottom-60,100,42)

    while running:
        now = time.time()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    menu_active = not menu_active
                elif not menu_active:
                    if event.key in (pygame.K_w, pygame.K_UP) and direction != [0,1]:
                        direction=[0,-1]
                    elif event.key in (pygame.K_s, pygame.K_DOWN) and direction != [0,-1]:
                        direction=[0,1]
                    elif event.key in (pygame.K_a, pygame.K_LEFT) and direction != [1,0]:
                        direction=[-1,0]
                    elif event.key in (pygame.K_d, pygame.K_RIGHT) and direction != [-1,0]:
                        direction=[1,0]
            elif event.type==pygame.MOUSEBUTTONDOWN and event.button==1 and menu_active:
                mx,my=event.pos
                if confirm_active:
                    if yes_btn.collidepoint((mx,my)):
                        if confirm_action=="restart":
                            snake, apple, obstacle, star, direction, score, boosted, boost_end, bh1, bh2 = reset_game_state()
                            menu_active=False
                            confirm_active=False
                        elif confirm_action=="quit":
                            pygame.quit()
                            sys.exit()
                    elif no_btn.collidepoint((mx,my)):
                        confirm_active=False
                        confirm_action=None
                else:
                    if resume_btn.collidepoint((mx,my)):
                        menu_active=False
                    elif restart_btn.collidepoint((mx,my)):
                        confirm_active=True
                        confirm_action="restart"
                    elif quit_btn.collidepoint((mx,my)):
                        confirm_active=True
                        confirm_action="quit"

        if not menu_active:
            new_head = [snake[0][0]+direction[0], snake[0][1]+direction[1]]
            if new_head in snake or new_head[0]<0 or new_head[1]<0 or new_head[0]>=GRID_SIZE or new_head[1]>=GRID_SIZE:
                action = game_over_screen(score, HIGH_SCORE)
                if action=="restart":
                    return game()
                else:
                    pygame.quit()
                    sys.exit()
            snake.insert(0,new_head)
            ate_apple=False

            exclude = snake + [obstacle, star]
            if new_head==apple:
                ate_apple=True
                score+=1
                if score>HIGH_SCORE:
                    HIGH_SCORE=score
                    save_high_score(HIGH_SCORE)
                apple=get_random_cell(exclude)
            elif new_head==star:
                boosted=True
                boost_end=now+1
                star=get_random_cell(exclude)
            elif new_head==obstacle:
                action = game_over_screen(score, HIGH_SCORE)
                if action=="restart":
                    return game()
                else:
                    pygame.quit()
                    sys.exit()

            if score>=2 and bh1 is None:
                bh1,bh2=place_black_holes(snake+[apple,star,obstacle])
            if bh1 and new_head==bh1: snake[0]=bh2.copy()
            elif bh2 and new_head==bh2: snake[0]=bh1.copy()

            if not ate_apple and not boosted:
                snake.pop()
            elif boosted and boost_end<now:
                boosted=False

        # ---- draw jungle ----
        screen.fill((10,30,20))
        draw_vines()
        update_leaves(); draw_leaves()
        update_fireflies(); draw_fireflies()
        screen.blit(fog_surface,(0,0))
        screen.blit(vignette,(0,0))

        draw_snake(snake,direction,boosted)
        draw_apple(apple)
        draw_specials(obstacle,star,bh1,bh2)
        draw_score(score,HIGH_SCORE)

        if menu_active:
            pygame.draw.rect(screen,(60,60,60),menu_box,border_radius=12)
            pygame.draw.rect(screen,GREEN,menu_box,2,border_radius=12)
            t,r=menu_title_font.render("Paused",WHITE)
            r.center=(menu_box.centerx,menu_box.top+50)
            screen.blit(t,r)
            draw_button(resume_btn,"Resume",resume_btn.collidepoint(pygame.mouse.get_pos()))
            draw_button(restart_btn,"Restart",restart_btn.collidepoint(pygame.mouse.get_pos()))
            draw_button(quit_btn,"Quit",quit_btn.collidepoint(pygame.mouse.get_pos()))
            if confirm_active:
                pygame.draw.rect(screen,(50,50,50),confirm_box,border_radius=8)
                pygame.draw.rect(screen,RED,confirm_box,2,border_radius=8)
                t,r=menu_font.render("Are you sure?",WHITE)
                r.center=(confirm_box.centerx,confirm_box.top+40)
                screen.blit(t,r)
                draw_button(yes_btn,"Yes",yes_btn.collidepoint(pygame.mouse.get_pos()))
                draw_button(no_btn,"No",no_btn.collidepoint(pygame.mouse.get_pos()))

        pygame.display.flip()
        clock.tick(normal_rate+ (boost_extra if boosted else 0))

# ---- run game ----
game()




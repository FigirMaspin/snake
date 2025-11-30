import pygame
import random
import pygame.freetype
import time
import os
import sys

# ---- init ----
pygame.init()
pygame.mixer.init()

#putting the sounds 
bg_music = pygame.mixer.Sound('Filo Starquez - Park Vibes (freetouse.com).mp3')
eating_apple = pygame.mixer.Sound('munch-sound-effect.mp3')
# ---- colors ----
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
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
image = pygame.image.load('bg.jpg')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game - With Pause Menu")

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
def place_black_holes():
    while True:
        b1 = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
        b2 = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
        if abs(b1[0]-b2[0]) + abs(b1[1]-b2[1]) >= 5:
            return b1, b2

def draw_grid():
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))

def draw_snake(snake, direction, boosted):
    snake_color = CYAN if boosted else GREEN
    for segment in snake[1:]:
        pygame.draw.rect(screen, snake_color, pygame.Rect(segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    # Draw head with rounded front
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
    else:  # up
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

def reset_game_state():
    snake = [[10,10],[9,10],[8,10]]
    apple = [random.randint(1,GRID_SIZE-2),random.randint(1,GRID_SIZE-2)]
    obstacle = [random.randint(1,GRID_SIZE-2),random.randint(1,GRID_SIZE-2)]
    star = [random.randint(1,GRID_SIZE-2),random.randint(1,GRID_SIZE-2)]
    direction = [1,0]
    return snake, apple, obstacle, star, direction, 0, False, 0, None, None

# ---- main game ----
def game():
    global HIGH_SCORE

    # ---- difficulty selection ----
    difficulty = None
    while difficulty not in ("E","N","H"):
        screen.fill(WHITE)
        screen.blit(image, (0,0))
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

    # ---- menu UI ----
    menu_box = pygame.Rect(SCREEN_WIDTH*0.2, SCREEN_HEIGHT*0.2, SCREEN_WIDTH*0.6, SCREEN_HEIGHT*0.6)
    btn_w, btn_h = 240, 54
    resume_btn = pygame.Rect(menu_box.centerx-btn_w//2, menu_box.top+120, btn_w, btn_h)
    restart_btn = pygame.Rect(menu_box.centerx-btn_w//2, menu_box.top+120+74, btn_w, btn_h)
    quit_btn = pygame.Rect(menu_box.centerx-btn_w//2, menu_box.top+120+148, btn_w, btn_h)
    confirm_box = pygame.Rect((SCREEN_WIDTH-420)//2, (SCREEN_HEIGHT-180)//2, 420, 180)
    yes_btn = pygame.Rect(confirm_box.centerx-110, confirm_box.bottom-60,100,42)
    no_btn = pygame.Rect(confirm_box.centerx+10, confirm_box.bottom-60,100,42)

    bg_music.play()

    while running:
        now = time.time()
        screen.blit(image, (0,0))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
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
            # ---- snake movement ----
            new_head = [snake[0][0]+direction[0], snake[0][1]+direction[1]]
            if new_head in snake or new_head[0]<0 or new_head[1]<0 or new_head[0]>=GRID_SIZE or new_head[1]>=GRID_SIZE:
                break
            snake.insert(0,new_head)
            ate_apple=False

            # ---- collisions ----
            if new_head==apple:
                ate_apple=True
                score+=1
                eating_apple.play()
                if score>HIGH_SCORE:
                    HIGH_SCORE=score
                    save_high_score(HIGH_SCORE)
                while True:
                    cand=[random.randint(1,GRID_SIZE-2),random.randint(1,GRID_SIZE-2)]
                    if cand not in snake and cand!=obstacle and cand!=star:
                        apple=cand
                        break
            elif new_head==star:
                while True:
                    cand=[random.randint(1,GRID_SIZE-2),random.randint(1,GRID_SIZE-2)]
                    if cand not in snake and cand!=apple and cand!=obstacle:
                        star=cand
                        break
                boosted=True
                boost_end=now+1
            elif new_head==obstacle:
                break

            if score>=2 and bh1 is None:
                bh1,bh2=place_black_holes()
            if bh1 and bh2:
                if new_head==bh1:
                    snake[0]=bh2.copy()
                    bh1,bh2=place_black_holes()
                elif new_head==bh2:
                    snake[0]=bh1.copy()
                    bh1,bh2=place_black_holes()

            if not ate_apple:
                snake.pop()
            if boosted and now>boost_end:
                boosted=False

        # ---- draw ----
        screen.fill(WHITE)
        screen.blit(image, (0,0))
        #draw_grid()
        draw_snake(snake,direction,boosted)
        draw_apple(apple)
        draw_specials(obstacle,star,bh1,bh2)
        draw_score(score,HIGH_SCORE)

        if menu_active:
            overlay = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill(OVERLAY_COLOR)
            screen.blit(overlay,(0,0))
            pygame.draw.rect(screen,(30,30,30),menu_box,border_radius=12)
            pygame.draw.rect(screen,(80,80,80),menu_box,2,border_radius=12)
            t,r=menu_title_font.render("PAUSED",CYAN)
            r.center=(menu_box.centerx,menu_box.top+60)
            screen.blit(t,r)
            mx,my=pygame.mouse.get_pos()
            draw_button(resume_btn,"Resume",resume_btn.collidepoint((mx,my)))
            draw_button(restart_btn,"Restart",restart_btn.collidepoint((mx,my)))
            draw_button(quit_btn,"Quit",quit_btn.collidepoint((mx,my)))
            hint,hr=menu_font.render("Use mouse to click  •  Press SPACE to close",GRAY)
            hr.center=(menu_box.centerx,quit_btn.bottom+28)
            screen.blit(hint,hr)
            if confirm_active:
                pygame.draw.rect(screen,(18,18,18),confirm_box,border_radius=10)
                pygame.draw.rect(screen,(90,90,90),confirm_box,2,border_radius=10)
                msg=("Restart game? All progress will be lost." if confirm_action=="restart"
                     else "Quit the game? Your progress will be lost.")
                t,_=menu_font.render(msg,WHITE)
                tr=t.get_rect(center=(confirm_box.centerx,confirm_box.centery-20))
                screen.blit(t,tr)
                draw_button(yes_btn,"Yes",yes_btn.collidepoint((mx,my)))
                draw_button(no_btn,"No",no_btn.collidepoint((mx,my)))

        # ---- speed ----
        clock.tick(normal_rate+(boost_extra if boosted else 0) if not menu_active else 30)
        pygame.display.flip()

    if score>HIGH_SCORE:
        HIGH_SCORE=score
        save_high_score(HIGH_SCORE)
    pygame.quit()

# ---- start ----
if __name__=="__main__":
    game()

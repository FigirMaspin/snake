import pygame
import random
import pygame.freetype
import time
import os
import sys

# ---- init ----
pygame.init()

# ---- colors ----
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
CYAN  = (0, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (169, 169, 169)
RED = (255, 0, 0)
HUD_BG = (20, 20, 20, 200)
OVERLAY_COLOR = (10, 10, 10, 200)

# ---- constants ----
GRID_SIZE = 20
CELL_SIZE = 30
SCREEN_WIDTH = GRID_SIZE * CELL_SIZE
SCREEN_HEIGHT = GRID_SIZE * CELL_SIZE

# ---- window ----
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game - With Pause Menu")

# ---- fonts ----
apple_font = pygame.freetype.SysFont("segoeuisymbol", CELL_SIZE)
star_font  = pygame.freetype.SysFont("segoeuisymbol", CELL_SIZE)
fire_font  = pygame.freetype.SysFont("segoeuisymbol", CELL_SIZE)
hole_font  = pygame.freetype.SysFont("segoeuisymbol", CELL_SIZE)
score_font = pygame.freetype.SysFont("Arial", 22)
menu_title_font = pygame.freetype.SysFont("Arial", 44, bold=True)
menu_font = pygame.freetype.SysFont("Arial", 28)

# ---- NEW FONTS FOR START MENU ----
start_big = pygame.freetype.SysFont("Arial", 52, bold=True)
start_font = pygame.freetype.SysFont("Arial", 32)

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

# =================================================================
#                    🎯 USERNAME INPUT SCREEN (FIXED)
# =================================================================
def ask_username():
    username = ""
    caret_visible = True
    caret_timer = 0
    caret_interval = 0.5  # blink speed

    box = pygame.Rect(SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 20, 400, 50)

    while True:
        screen.fill(BLACK)

        # title
        title, rect = start_big.render("ENTER USERNAME", WHITE)
        rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100)
        screen.blit(title, rect)

        # input box
        pygame.draw.rect(screen, WHITE, box, 2)

        # check mouse focus
        mx, my = pygame.mouse.get_pos()
        focused = box.collidepoint((mx, my))

        # render text
        text_surf, text_rect = start_font.render(username, WHITE)
        text_rect.midleft = (box.left + 10, box.centery)
        screen.blit(text_surf, text_rect)

        # blinking caret
        caret_timer += clock.get_time() / 1000
        if caret_timer >= caret_interval:
            caret_visible = not caret_visible
            caret_timer = 0

        if caret_visible:
            caret_x = text_rect.right + 5
            caret_y1 = box.top + 10
            caret_y2 = box.bottom - 10
            pygame.draw.line(screen, WHITE, (caret_x, caret_y1), (caret_x, caret_y2), 2)

        # hint
        hint, hrect = start_font.render("Press ENTER to continue", GRAY)
        hrect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60)
        screen.blit(hint, hrect)

        pygame.display.update()
        clock.tick(60)

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # ENTER now works even if mouse is outside the input box (as long as username not empty)
                if event.key == pygame.K_RETURN and username.strip():
                    return username

                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    if len(username) < 15:
                        username += event.unicode


# =================================================================
#                     🎯 YES/NO QUIT CONFIRM (FIXED HOVER)
# =================================================================
def quit_confirm():
    selected = 0

    yes_rect = pygame.Rect(SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2, 160, 50)
    no_rect  = pygame.Rect(SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2 + 70, 160, 50)

    while True:
        screen.fill(BLACK)

        title, rect = start_big.render("QUIT GAME?", RED)
        rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 80)
        screen.blit(title, rect)

        mx, my = pygame.mouse.get_pos()
        hover_yes = yes_rect.collidepoint((mx, my))
        hover_no  = no_rect.collidepoint((mx, my))

        yes_color = GREEN if hover_yes or (not hover_yes and not hover_no and selected == 0) else WHITE
        no_color  = GREEN if hover_no  or (not hover_yes and not hover_no and selected == 1) else WHITE

        pygame.draw.rect(screen, (50,50,50), yes_rect, border_radius=10)
        pygame.draw.rect(screen, yes_color, yes_rect, 3, border_radius=10)
        t_yes, r_yes = start_font.render("YES", yes_color)
        r_yes.center = yes_rect.center
        screen.blit(t_yes, r_yes)

        pygame.draw.rect(screen, (50,50,50), no_rect, border_radius=10)
        pygame.draw.rect(screen, no_color, no_rect, 3, border_radius=10)
        t_no, r_no = start_font.render("NO", no_color)
        r_no.center = no_rect.center
        screen.blit(t_no, r_no)

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % 2
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % 2
                elif event.key == pygame.K_RETURN:
                    return selected == 0

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if hover_yes:
                    return True
                if hover_no:
                    return False

# =================================================================
#                     ⭐ START MENU
# =================================================================
def start_menu(username):
    selected = 0
    options = ["START GAME", "QUIT"]

    btn_w, btn_h = 300, 70
    start_btn = pygame.Rect(SCREEN_WIDTH//2 - btn_w//2,
                            SCREEN_HEIGHT//2 - 20,
                            btn_w, btn_h)
    quit_btn = pygame.Rect(SCREEN_WIDTH//2 - btn_w//2,
                           SCREEN_HEIGHT//2 + 80,
                           btn_w, btn_h)

    while True:
        screen.fill(BLACK)

        greet, grect = start_big.render(f"Welcome {username}", YELLOW)
        grect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 140)
        screen.blit(greet, grect)

        # render high score on start menu (above buttons)
        hs_text, hs_rect = start_font.render(f"High Score: {HIGH_SCORE}", WHITE)
        hs_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 60)
        screen.blit(hs_text, hs_rect)

        mx, my = pygame.mouse.get_pos()

        hover_start = start_btn.collidepoint((mx, my))
        hover_quit  = quit_btn.collidepoint((mx, my))

        pygame.draw.rect(screen, (50,50,50), start_btn, border_radius=12)
        pygame.draw.rect(screen, GREEN if hover_start else WHITE, start_btn, 3, border_radius=12)
        t, r = start_font.render("START GAME", GREEN if hover_start else WHITE)
        r.center = start_btn.center
        screen.blit(t, r)

        pygame.draw.rect(screen, (50,50,50), quit_btn, border_radius=12)
        pygame.draw.rect(screen, GREEN if hover_quit else WHITE, quit_btn, 3, border_radius=12)
        t, r = start_font.render("QUIT", GREEN if hover_quit else WHITE)
        r.center = quit_btn.center
        screen.blit(t, r)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % 2
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % 2
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        return "start"
                    else:
                        if quit_confirm():
                            pygame.quit()
                            sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if hover_start:
                    return "start"
                if hover_quit:
                    if quit_confirm():
                        pygame.quit()
                        sys.exit()

# =================================================================
#        ⚠️⚠️⚠️ FULL GAME CODE — UNTOUCHED (except difficulty prompt & fire handling)
# =================================================================
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
    body_color = CYAN if boosted else GREEN
    for segment in snake[1:]:
        pygame.draw.rect(screen, body_color,
                         pygame.Rect(segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    head = snake[0]
    x = head[0] * CELL_SIZE
    y = head[1] * CELL_SIZE
    radius = CELL_SIZE // 2

    pygame.draw.rect(screen, body_color, pygame.Rect(x, y, CELL_SIZE, CELL_SIZE))

    if direction == [1, 0]:
        pygame.draw.circle(screen, body_color, (x + CELL_SIZE, y + CELL_SIZE // 2), radius)
        left_eye = (x + 3 * CELL_SIZE // 4, y + CELL_SIZE // 3)
        right_eye = (x + 3 * CELL_SIZE // 4, y + 2 * CELL_SIZE // 3)
    elif direction == [-1, 0]:
        pygame.draw.circle(screen, body_color, (x, y + CELL_SIZE // 2), radius)
        left_eye = (x + CELL_SIZE // 4, y + CELL_SIZE // 3)
        right_eye = (x + CELL_SIZE // 4, y + 2 * CELL_SIZE // 3)
    elif direction == [0, 1]:
        pygame.draw.circle(screen, body_color, (x + CELL_SIZE // 2, y + CELL_SIZE), radius)
        left_eye = (x + CELL_SIZE // 3, y + 3 * CELL_SIZE // 4)
        right_eye = (x + 2 * CELL_SIZE // 3, y + 3 * CELL_SIZE // 4)
    else:
        pygame.draw.circle(screen, body_color, (x + CELL_SIZE // 2, y), radius)
        left_eye = (x + CELL_SIZE // 3, y + CELL_SIZE // 4)
        right_eye = (x + 2 * CELL_SIZE // 3, y + CELL_SIZE // 4)

    pygame.draw.circle(screen, BLACK, left_eye, CELL_SIZE // 8)
    pygame.draw.circle(screen, BLACK, right_eye, CELL_SIZE // 8)

def draw_apple(pos):
    surf, rect = apple_font.render("🍎", RED)
    rect.topleft = (pos[0] * CELL_SIZE, pos[1] * CELL_SIZE)
    screen.blit(surf, rect)

def draw_specials(obstacles, star_position, bh1, bh2, green_apples):
    # obstacles: list of obstacle positions (each is [x,y]) or empty list
    for obstacle_position in (obstacles or []):
        fire_surf, fire_rect = fire_font.render("🔥", ORANGE)
        fire_rect.center = (obstacle_position[0]*CELL_SIZE + CELL_SIZE//2,
                            obstacle_position[1]*CELL_SIZE + CELL_SIZE//2)
        screen.blit(fire_surf, fire_rect)

    star_surf, star_rect = star_font.render("⭐", YELLOW)
    star_surf = pygame.transform.scale(star_surf, (CELL_SIZE, CELL_SIZE))
    star_rect.topleft = (star_position[0]*CELL_SIZE, star_position[1]*CELL_SIZE)
    screen.blit(star_surf, star_rect)

    # draw green poisonous apples
    for g in (green_apples or []):
        g_surf, g_rect = apple_font.render("🍏", GREEN)
        g_rect.topleft = (g[0]*CELL_SIZE, g[1]*CELL_SIZE)
        screen.blit(g_surf, g_rect)

    if bh1 and bh2:
        h1, r1 = hole_font.render("⚫", BLACK)
        h1 = pygame.transform.scale(h1, (CELL_SIZE, CELL_SIZE))
        r1.topleft = (bh1[0]*CELL_SIZE, bh1[1]*CELL_SIZE)
        screen.blit(h1, r1)

        h2, r2 = hole_font.render("⚫", BLACK)
        h2 = pygame.transform.scale(h2, (CELL_SIZE, CELL_SIZE))
        r2.topleft = (bh2[0]*CELL_SIZE, bh2[1]*CELL_SIZE)
        screen.blit(h2, r2)

def draw_score(score):
    s, _ = score_font.render(f"Score: {score}", BLACK)
    screen.blit(s, (8, 6))

def draw_button(rect, text, hovered=False):
    bg = (40, 40, 40) if not hovered else (60, 60, 60)
    border = CYAN if hovered else GRAY
    pygame.draw.rect(screen, bg, rect, border_radius=8)
    pygame.draw.rect(screen, border, rect, 2, border_radius=8)
    t, r = menu_font.render(text, WHITE)
    r.center = rect.center
    screen.blit(t, r)

def reset_game_state():
    snake = [[10, 10], [9, 10], [8, 10]]
    apple = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
    # set obstacle None at start so fire doesn't appear immediately
    obstacle = None
    star = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
    direction = [1, 0]
    # new: green apples list and red streak counter (consecutive red apples eaten)
    green_apples = []
    red_streak = 0
    return (snake, apple, obstacle, star, direction, 0, False, 0, None, None, green_apples, red_streak)

# =================================================================
#                       GAME OVER SCREEN (UPDATED WITH REASON)
# =================================================================
def game_over_screen(score, high_score, death_reason=None):
    fade = 0
    fading_in = True

    btn_w, btn_h = 220, 58
    restart_btn = pygame.Rect(SCREEN_WIDTH//2 - btn_w//2, SCREEN_HEIGHT//2 + 40, btn_w, btn_h)
    quit_btn = pygame.Rect(SCREEN_WIDTH//2 - btn_w//2, SCREEN_HEIGHT//2 + 120, btn_w, btn_h)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # preserve high score and exit
                save_high_score(high_score)
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                if event.key == pygame.K_q:
                    save_high_score(high_score)
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if restart_btn.collidepoint((mx, my)):
                    return "restart"
                if quit_btn.collidepoint((mx, my)):
                    save_high_score(high_score)
                    pygame.quit()
                    sys.exit()

        # background (NO GRID)
        screen.fill((0,0,0))

        # fade overlay
        if fading_in:
            fade += 8
            if fade >= 180:
                fade = 180
                fading_in = False

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, fade))
        screen.blit(overlay, (0, 0))

        # --- TEXT + EMOJIS ---
        title, rect = menu_title_font.render("Game Over!", RED)
        rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 90)
        screen.blit(title, rect)

        # custom death reason (if provided)
        if death_reason:
            reason_txt, reason_rect = menu_font.render(death_reason, WHITE)
            reason_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50)
            screen.blit(reason_txt, reason_rect)

        score_txt, srect = menu_font.render(f"Score: {score}", WHITE)
        srect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 10)
        screen.blit(score_txt, srect)

        high_txt, hrect = menu_font.render(f"High Score: {high_score}", CYAN)
        hrect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 25)
        screen.blit(high_txt, hrect)

        # buttons
        mx, my = pygame.mouse.get_pos()
        draw_button(restart_btn, "Restart", restart_btn.collidepoint((mx,my)))
        draw_button(quit_btn, "Quit", quit_btn.collidepoint((mx,my)))

        pygame.display.flip()
        clock.tick(30)

# =================================================================
#                           🎮 GAME (UPDATED to accept difficulty)
# =================================================================
def game(existing_difficulty=None):
    global HIGH_SCORE

    (snake, apple_position, obstacle_position, star_position, direction,
     score, boosted, boost_end_time, bh1, bh2, green_apples, red_streak) = reset_game_state()

    # obstacles will be managed as a list (may be empty until spawn)
    obstacles = []

    # --- difficulty selection added --- 
    difficulty = existing_difficulty
    if difficulty not in ("E", "N", "H"):
        while difficulty not in ("E", "N", "H"):
            screen.fill(WHITE)
            t, r = menu_title_font.render("Select Difficulty: E / N / H", BLACK)
            r.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
            screen.blit(t, r)
            hint, hr = menu_font.render("E = Easy, N = Normal, H = Hard", GRAY)
            hr.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50)
            screen.blit(hint, hr)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        difficulty = "E"
                    elif event.key == pygame.K_n:
                        difficulty = "N"
                    elif event.key == pygame.K_h:
                        difficulty = "H"
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    # speeds for modes (lower -> slower)
    normal_rate = {"E": 5, "N": 7.5, "H": 10}[difficulty]
    boost_extra = 5

    # fire counts per difficulty
    fire_count = {"E": 1, "N": 2, "H": 3}[difficulty]

    # green poison apple counts per difficulty
    green_count = {"E": 1, "N": 2, "H": 3}[difficulty]

    # -------------------------
    # spawn fires IMMEDIATELY (once) and keep them for the whole game
    # ensure each fire is at least 5 Manhattan distance from snake head,
    # and doesn't overlap snake body, apple, star, or black holes.
    # -------------------------
    spawned = 0
    attempts = 0
    max_attempts = 1000
    while spawned < fire_count and attempts < max_attempts:
        attempts += 1
        cand = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
        # must not collide with snake body, apple, star, or existing obstacles
        if cand in snake or cand == apple_position or cand == star_position or cand in obstacles:
            continue
        # avoid black holes if they exist
        if bh1 and bh2:
            if cand == bh1 or cand == bh2:
                continue
        # manhattan distance from snake head must be >= 5
        head = snake[0]
        manh = abs(cand[0] - head[0]) + abs(cand[1] - head[1])
        if manh < 5:
            continue
        obstacles.append(cand)
        spawned += 1
    # If not enough spawned within attempts, we keep what we have.

    # helper to spawn / reposition green apples safely
    def spawn_or_reposition_green():
        nonlocal green_apples
        green_apples = []
        tries = 0
        while len(green_apples) < green_count and tries < 2000:
            tries += 1
            cand = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
            # avoid conflicts: snake, apple, star, obstacles, black holes, existing green apples
            if cand in snake or cand == apple_position or cand == star_position or cand in obstacles or cand in green_apples:
                continue
            if bh1 and bh2:
                if cand == bh1 or cand == bh2:
                    continue
            green_apples.append(cand)
        # done (if couldn't place all, keep what we have)

    # helper to spawn a single green apple to maintain count after one is eaten
    def spawn_one_green():
        nonlocal green_apples
        tries = 0
        while len(green_apples) < green_count and tries < 1000:
            tries += 1
            cand = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
            if cand in snake or cand == apple_position or cand == star_position or cand in obstacles or cand in green_apples:
                continue
            if bh1 and bh2:
                if cand == bh1 or cand == bh2:
                    continue
            green_apples.append(cand)

    running = True
    paused = False
    menu_active = False
    confirm_active = False
    confirm_action = None

    menu_box = pygame.Rect(SCREEN_WIDTH*0.2, SCREEN_HEIGHT*0.2,
                           SCREEN_WIDTH*0.6, SCREEN_HEIGHT*0.6)

    btn_w, btn_h = 240, 54
    resume_btn = pygame.Rect(menu_box.centerx - btn_w//2, menu_box.top+120, btn_w, btn_h)
    restart_btn = pygame.Rect(menu_box.centerx - btn_w//2, menu_box.top+120+74, btn_w, btn_h)
    quit_btn = pygame.Rect(menu_box.centerx - btn_w//2, menu_box.top+120+148, btn_w, btn_h)

    confirm_box = pygame.Rect((SCREEN_WIDTH-420)//2, (SCREEN_HEIGHT-180)//2, 420, 180)
    yes_btn = pygame.Rect(confirm_box.centerx - 110, confirm_box.bottom - 60, 100, 42)
    no_btn = pygame.Rect(confirm_box.centerx + 10, confirm_box.bottom - 60, 100, 42)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if not paused and not menu_active:
                    paused = True
                    menu_active = True
                    confirm_active = True
                    confirm_action = "quit"
                else:
                    running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    if not menu_active:
                        paused = True
                        menu_active = True
                        confirm_active = False
                    else:
                        if not confirm_active:
                            paused = False
                            menu_active = False

                elif not menu_active:
                    if event.key in (pygame.K_w, pygame.K_UP) and direction != [0, 1]:
                        direction = [0, -1]
                    elif event.key in (pygame.K_s, pygame.K_DOWN) and direction != [0, -1]:
                        direction = [0, 1]
                    elif event.key in (pygame.K_a, pygame.K_LEFT) and direction != [1, 0]:
                        direction = [-1, 0]
                    elif event.key in (pygame.K_d, pygame.K_RIGHT) and direction != [-1, 0]:
                        direction = [1, 0]

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and menu_active:
                mx, my = event.pos

                if confirm_active:
                    if yes_btn.collidepoint((mx, my)):
                        if confirm_action == "restart":
                            (snake, apple_position, obstacle_position, star_position, direction,
                             score, boosted, boost_end_time, bh1, bh2, green_apples, red_streak) = reset_game_state()
                            obstacles = []
                            paused = False
                            menu_active = False
                            confirm_active = False
                        elif confirm_action == "quit":
                            pygame.quit()
                            sys.exit()

                    elif no_btn.collidepoint((mx, my)):
                        confirm_active = False
                        confirm_action = None

                else:
                    if resume_btn.collidepoint((mx,my)):
                        paused = False
                        menu_active = False
                    elif restart_btn.collidepoint((mx,my)):
                        confirm_active = True
                        confirm_action = "restart"
                    elif quit_btn.collidepoint((mx,my)):
                        confirm_active = True
                        confirm_action = "quit"

        if not menu_active:
            head = snake[0]
            new_head = [head[0] + direction[0], head[1] + direction[1]]

            # death checks split to provide specific message
            # self-collision
            if new_head in snake:
                save_high_score(HIGH_SCORE)
                result = game_over_screen(score, HIGH_SCORE, "You ate yourself!")
                if result == "restart":
                    return game(difficulty)
                else:
                    pygame.quit()
                    sys.exit()

            # wall collision
            if new_head[0] < 0 or new_head[1] < 0 or new_head[0] >= GRID_SIZE or new_head[1] >= GRID_SIZE:
                save_high_score(HIGH_SCORE)
                result = game_over_screen(score, HIGH_SCORE, "You hit the wall")
                if result == "restart":
                    return game(difficulty)
                else:
                    pygame.quit()
                    sys.exit()

            snake.insert(0, new_head)
            ate_apple = False

            if new_head == apple_position:
                ate_apple = True
                score += 1
                # increment red apple streak
                red_streak += 1

                if score > HIGH_SCORE:
                    HIGH_SCORE = score
                    save_high_score(HIGH_SCORE)

                while True:
                    cand = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
                    # ensure not on snake, star, or existing obstacles or green apples
                    if cand not in snake and cand != star_position and cand not in obstacles and cand not in green_apples:
                        apple_position = cand
                        break

                # If red_streak reaches 3, spawn or reposition green apples
                if red_streak >= 3:
                    spawn_or_reposition_green()
                    # reset streak after reposition
                    red_streak = 0

            elif new_head == star_position:
                while True:
                    cand = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
                    if cand not in snake and cand != apple_position and cand not in obstacles and cand not in green_apples:
                        star_position = cand
                        break
                boosted = True
                boost_end_time = time.time() + 3

            else:
                # check collision with any obstacle (fires)
                for obs in list(obstacles):
                    if new_head == obs:
                        # hit fire -> game over (instant death)
                        save_high_score(HIGH_SCORE)
                        result = game_over_screen(score, HIGH_SCORE, "You hit an obstacle")
                        if result == "restart":
                            return game(difficulty)
                        else:
                            pygame.quit()
                            sys.exit()

            # check green apple collision BEFORE pop so snake eats it
            for g in list(green_apples):
                if new_head == g:
                    # NEW RULE: if score is already 0 and snake eats a green apple -> game over
                    if score <= 0:
                        save_high_score(HIGH_SCORE)
                        result = game_over_screen(score, HIGH_SCORE, "You ate poisonous apple")
                        if result == "restart":
                            return game(difficulty)
                        else:
                            pygame.quit()
                            sys.exit()

                    # eat green poisonous apple: lose 1 point (not below 0)
                    score = max(0, score - 1)
                    try:
                        green_apples.remove(g)
                    except:
                        pass
                    # reset red streak because poison apple was eaten
                    red_streak = 0
                    # immediately respawn one to maintain count
                    spawn_one_green()
                    # do not treat this as 'ate_apple' (no growth)

            if new_head == None:
                pass

            # spawn black holes when score >= 2 (as before)
            if score >= 2 and bh1 is None:
                bh1, bh2 = place_black_holes()

            if bh1 and bh2:
                if new_head == bh1:
                    snake[0] = bh2.copy()
                    bh1, bh2 = place_black_holes()
                elif new_head == bh2:
                    snake[0] = bh1.copy()
                    bh1, bh2 = place_black_holes()

            # NOTE: removed later "spawn fires" logic — fires were spawned at start and remain forever.
            # the original block conditioned on score >= 2 is left in the file but since `obstacles` is non-empty, it won't spawn again.

            if not ate_apple:
                snake.pop()

            if boosted and time.time() > boost_end_time:
                boosted = False

        screen.fill(WHITE)
        draw_grid()
        draw_snake(snake, direction, boosted)
        draw_apple(apple_position)
        draw_specials(obstacles, star_position, bh1, bh2, green_apples)

        # draw score at top-left as requested
        draw_score(score)

        if menu_active:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((10,10,10,200))
            screen.blit(overlay, (0,0))

            pygame.draw.rect(screen, (30,30,30), menu_box, border_radius=12)
            pygame.draw.rect(screen, (80,80,80), menu_box, 2, border_radius=12)

            t, r = menu_title_font.render("PAUSED", CYAN)
            r.center = (menu_box.centerx, menu_box.top + 60)
            screen.blit(t, r)

            # render high score near top of pause box (Option A)
            hs_t, hs_r = menu_font.render(f"High Score: {HIGH_SCORE}", WHITE)
            hs_r.center = (menu_box.centerx, menu_box.top + 110)
            screen.blit(hs_t, hs_r)

            mx, my = pygame.mouse.get_pos()
            draw_button(resume_btn, "Resume", resume_btn.collidepoint((mx,my)))
            draw_button(restart_btn, "Restart", restart_btn.collidepoint((mx,my)))
            draw_button(quit_btn, "Quit", quit_btn.collidepoint((mx,my)))

            hint, hr = menu_font.render("Use mouse to click  •  Press SPACE to close", GRAY)
            hr.center = (menu_box.centerx, quit_btn.bottom + 28)
            screen.blit(hint, hr)

            if confirm_active:
                pygame.draw.rect(screen, (18,18,18), confirm_box, border_radius=10)
                pygame.draw.rect(screen, (90,90,90), confirm_box, 2, border_radius=10)

                msg = ("Restart game? All progress will be lost."
                       if confirm_action == "restart"
                       else "Quit the game? Your progress will be lost.")
                t, _ = menu_font.render(msg, WHITE)
                tr = t.get_rect(center=(confirm_box.centerx, confirm_box.centery - 20))
                screen.blit(t, tr)

                draw_button(yes_btn, "Yes", yes_btn.collidepoint((mx,my)))
                draw_button(no_btn, "No", no_btn.collidepoint((mx,my)))

        pygame.display.flip()

        if not menu_active:
            if boosted:
                clock.tick(normal_rate + boost_extra)
            else:
                clock.tick(normal_rate)
        else:
            clock.tick(30)

    # if loop exits unexpectedly, ensure high score saved and quit
    if score > HIGH_SCORE:
        HIGH_SCORE = score
        save_high_score(HIGH_SCORE)

    pygame.quit()

# =================================================================
#                     🎯 PROGRAM START
# =================================================================
if __name__ == "__main__":
    username = ask_username()
    choice = start_menu(username)

    if choice == "start":
        game()

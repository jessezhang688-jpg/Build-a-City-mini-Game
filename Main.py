import pygame
import sys
import json
import base64
import random

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Tile City Builder - Brush Mode")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)
title_font = pygame.font.SysFont(None, 28)

GRID_SIZE = 30
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
current_tool = 1
money = 1000
population = 0
message = "Press R: New World | S: Save | L: Load"

is_loading = False
input_text = ""
last_painted_tile = None  # Tracks the last tile painted during a drag

def generate_world():
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            grid[r][c] = 0

    # Organic Lakes
    num_lakes = random.randint(1, 3)
    for _ in range(num_lakes):
        sr = random.randint(4, GRID_SIZE - 5)
        sc = random.randint(4, GRID_SIZE - 5)
        grid[sr][sc] = 3
        
        lake_tiles = [(sr, sc)]
        lake_size = random.randint(8, 20)
        
        for _ in range(lake_size):
            if not lake_tiles: break
            base_r, base_c = random.choice(lake_tiles)
            dr, dc = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
            nr, nc = base_r + dr, base_c + dc
            
            if 1 <= nr < GRID_SIZE - 1 and 1 <= nc < GRID_SIZE - 1:
                grid[nr][nc] = 3
                if (nr, nc) not in lake_tiles:
                    lake_tiles.append((nr, nc))

    # Winding Rivers
    num_rivers = random.randint(1, 3)
    for _ in range(num_rivers):
        r = random.randint(3, GRID_SIZE - 4)
        c = random.randint(3, GRID_SIZE - 4)
        steps = random.randint(20, 50)
        
        for _ in range(steps):
            grid[r][c] = 3
            if r + 1 < GRID_SIZE: grid[r+1][c] = 3
            if c + 1 < GRID_SIZE: grid[r][c+1] = 3
            
            r += random.choice([-1, 0, 1])
            c += random.choice([-1, 0, 1])
            
            if r < 1 or r >= GRID_SIZE - 1 or c < 1 or c >= GRID_SIZE - 1:
                break

def save_game():
    data = {"grid": grid, "money": money, "pop": population}
    json_str = json.dumps(data)
    code = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
    print(f"\n--- YOUR SAVE CODE ---\n{code}\n----------------------\n")
    return code

def load_game(code):
    global grid, money, population
    try:
        json_str = base64.b64decode(code.strip().encode('utf-8')).decode('utf-8')
        data = json.loads(json_str)
        grid = data["grid"]
        money = data["money"]
        population = data["pop"]
        return True
    except:
        return False

generate_world()

def draw_ui_panels(width, height):
    tile_size = min(width // GRID_SIZE, height // GRID_SIZE)
    grid_px = GRID_SIZE * tile_size
    offset_x = (width - grid_px) // 2

    # Left Panel: City Stats
    left_panel = pygame.Rect(0, 0, offset_x, height)
    pygame.draw.rect(screen, (25, 25, 30), left_panel)
    pygame.draw.line(screen, (70, 70, 80), (offset_x, 0), (offset_x, height), 2)
    
    screen.blit(title_font.render("CITY STATS", True, (255, 255, 255)), (20, 25))
    screen.blit(font.render(f"Money: ${money}", True, (230, 200, 50)), (20, 80))
    screen.blit(font.render(f"Population: {population}", True, (100, 220, 100)), (20, 120))

    screen.blit(title_font.render("CONTROLS", True, (255, 255, 255)), (20, height - 180))
    screen.blit(font.render("R - New World", True, (180, 180, 180)), (20, height - 140))
    screen.blit(font.render("S - Save Game", True, (180, 180, 180)), (20, height - 110))
    screen.blit(font.render("L - Load Game", True, (180, 180, 180)), (20, height - 80))

    # Right Panel: Build Menu
    right_x = offset_x + grid_px
    right_panel = pygame.Rect(right_x, 0, width - right_x, height)
    pygame.draw.rect(screen, (25, 25, 30), right_panel)
    pygame.draw.line(screen, (70, 70, 80), (right_x, 0), (right_x, height), 2)

    screen.blit(title_font.render("BUILD MENU", True, (255, 255, 255)), (right_x + 20, 25))

    tools = [
        (1, "1. Road", "$10", (100, 100, 100)),
        (2, "2. House", "$50", (220, 60, 60)),     # Red house
        (3, "3. Bulldozer", "Free", (200, 70, 70))
    ]

    for idx, (t_id, t_name, t_cost, t_color) in enumerate(tools):
        btn_y = 80 + (idx * 70)
        btn_rect = pygame.Rect(right_x + 20, btn_y, width - right_x - 40, 50)
        
        border_color = (255, 255, 255) if current_tool == t_id else (70, 70, 80)
        bg_color = (45, 45, 55) if current_tool == t_id else (35, 35, 40)
        
        pygame.draw.rect(screen, bg_color, btn_rect, border_radius=6)
        pygame.draw.rect(screen, border_color, btn_rect, 2, border_radius=6)
        pygame.draw.rect(screen, t_color, pygame.Rect(right_x + 35, btn_y + 15, 20, 20))

        screen.blit(font.render(t_name, True, (255, 255, 255)), (right_x + 65, btn_y + 15))
        screen.blit(font.render(t_cost, True, (200, 200, 200)), (btn_rect.right - 60, btn_y + 15))

    screen.blit(font.render(message, True, (150, 200, 255)), (right_x + 20, height - 50))

    if is_loading:
        prompt_box = pygame.Rect(width // 4, height // 2 - 30, width // 2, 60)
        pygame.draw.rect(screen, (40, 40, 50), prompt_box)
        pygame.draw.rect(screen, (200, 200, 255), prompt_box, 2)
        screen.blit(font.render(f"Paste Code (Ctrl+V) & Enter: {input_text}_", True, (255, 255, 255)), (prompt_box.x + 15, prompt_box.y + 20))

def draw_city(width, height):
    tile_size = min(width // GRID_SIZE, height // GRID_SIZE)
    grid_px = GRID_SIZE * tile_size
    offset_x = (width - grid_px) // 2
    offset_y = (height - grid_px) // 2

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            tile = grid[row][col]
            
            if tile == 1: color = (100, 100, 100)       # Road: Gray
            elif tile == 2: color = (220, 60, 60)      # House: Red
            elif tile == 3: color = (30, 144, 255)     # Water: Blue
            else: color = (85, 105, 80)                # Grass: Muted earthy green

            rect = pygame.Rect(offset_x + col * tile_size, offset_y + row * tile_size, tile_size, tile_size)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (60, 75, 55), rect, 1)

while True:
    width, height = screen.get_size()
    tile_size = min(width // GRID_SIZE, height // GRID_SIZE)
    grid_px = GRID_SIZE * tile_size
    offset_x = (width - grid_px) // 2
    offset_y = (height - grid_px) // 2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            last_painted_tile = None  # Reset drag stroke when mouse is released

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not is_loading:
                mx, my = pygame.mouse.get_pos()
                right_x = offset_x + grid_px
                
                # Check build menu clicks
                if mx >= right_x:
                    if 80 <= my <= 130: current_tool = 1
                    elif 150 <= my <= 200: current_tool = 2
                    elif 220 <= my <= 270: current_tool = 3

        elif event.type == pygame.KEYDOWN:
            if is_loading:
                if event.key == pygame.K_RETURN:
                    if load_game(input_text):
                        message = "World Loaded Successfully!"
                    else:
                        message = "Invalid Save Code!"
                    is_loading = False
                    input_text = ""
                elif event.key == pygame.K_ESCAPE:
                    is_loading = False
                    input_text = ""
                    message = "Load canceled"
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_v and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    try:
                        import tkinter as tk
                        input_text += tk.Tk().clipboard_get()
                    except:
                        pass
                elif event.unicode.isprintable():
                    input_text += event.unicode
            else:
                if event.key == pygame.K_1: current_tool = 1
                elif event.key == pygame.K_2: current_tool = 2
                elif event.key == pygame.K_3: current_tool = 3
                elif event.key == pygame.K_r:
                    generate_world()
                    message = "New World Generated!"
                elif event.key == pygame.K_s:
                    save_game()
                    message = "Saved! Code copied to Terminal."
                elif event.key == pygame.K_l:
                    is_loading = True
                    input_text = ""
                    message = "Enter save code & press ENTER"

    # Continuous Mouse Check for Drag-to-Paint (Brush Mode)
    if not is_loading and pygame.mouse.get_pressed()[0]:
        mx, my = pygame.mouse.get_pos()
        right_x = offset_x + grid_px
        if offset_x <= mx < offset_x + grid_px and offset_y <= my < offset_y + grid_px:
            col = (mx - offset_x) // tile_size
            row = (my - offset_y) // tile_size
            
            # Only paint if it's a new tile in the current drag motion
            if (row, col) != last_painted_tile:
                last_painted_tile = (row, col)
                current_tile = grid[row][col]

                if current_tile != 3:
                    if current_tool == 1 and current_tile == 0 and money >= 10:
                        grid[row][col] = 1
                        money -= 10
                    elif current_tool == 2 and current_tile == 0 and money >= 50:
                        grid[row][col] = 2
                        money -= 50
                        population += 5
                    elif current_tool == 3 and current_tile != 0:
                        if current_tile == 2: population -= 5
                        grid[row][col] = 0
                        money += 5

    screen.fill((15, 15, 15))
    draw_city(width, height)
    draw_ui_panels(width, height)
    pygame.display.flip()
    clock.tick(60)
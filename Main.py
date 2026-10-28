import pygame
import sys
import json
import base64
import random

pygame.init()

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 800
GRID_SIZE = 30

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Tile City Builder - Organic Lakes & Save System")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
current_tool = 1
money = 1000
population = 0
message = "Press R to regenerate | S to save | L to load"

# Input box state for loading save codes
is_loading = False
input_text = ""

def generate_world():
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            grid[r][c] = 0

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
    hud_rect = pygame.Rect(0, 0, width, 50)
    pygame.draw.rect(screen, (35, 35, 35), hud_rect)
    pygame.draw.line(screen, (70, 70, 70), (0, 50), (width, 50), 2)

    tool_names = {1: "Road ($10)", 2: "House ($50)", 3: "Bulldozer"}
    text = font.render(f"${money} | Pop: {population} | Tool: {tool_names[current_tool]} | {message}", True, (255, 255, 255))
    screen.blit(text, (20, 15))

    hud_height = 50
    avail_height = height - hud_height
    tile_size = min(width // GRID_SIZE, avail_height // GRID_SIZE)
    grid_px = GRID_SIZE * tile_size
    offset_x = (width - grid_px) // 2

    # Left Panel
    left_panel = pygame.Rect(0, hud_height, offset_x, avail_height)
    pygame.draw.rect(screen, (25, 25, 25), left_panel)
    pygame.draw.line(screen, (70, 70, 70), (offset_x, hud_height), (offset_x, height), 2)
    left_text = font.render("Left UI Panel", True, (120, 120, 120))
    screen.blit(left_text, (20, hud_height + 20))

    # Right Panel
    right_panel = pygame.Rect(offset_x + grid_px, hud_height, width - (offset_x + grid_px), avail_height)
    pygame.draw.rect(screen, (25, 25, 25), right_panel)
    pygame.draw.line(screen, (70, 70, 70), (offset_x + grid_px, hud_height), (offset_x + grid_px, height), 2)
    right_text = font.render("Right UI Panel", True, (120, 120, 120))
    screen.blit(right_text, (offset_x + grid_px + 20, hud_height + 20))

    # Load prompt box overlay when typing a code
    if is_loading:
        prompt_box = pygame.Rect(width // 4, height // 2 - 30, width // 2, 60)
        pygame.draw.rect(screen, (40, 40, 50), prompt_box)
        pygame.draw.rect(screen, (200, 200, 255), prompt_box, 2)
        load_lbl = font.render(f"Paste/Type Code: {input_text}_", True, (255, 255, 255))
        screen.blit(load_lbl, (prompt_box.x + 15, prompt_box.y + 20))

def draw_city(width, height):
    hud_height = 50
    avail_height = height - hud_height
    tile_size = min(width // GRID_SIZE, avail_height // GRID_SIZE)
    grid_px = GRID_SIZE * tile_size
    
    offset_x = (width - grid_px) // 2
    offset_y = hud_height + (avail_height - grid_px) // 2

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            tile = grid[row][col]
            
            if tile == 1: color = (100, 100, 100)
            elif tile == 2: color = (46, 139, 87)
            elif tile == 3: color = (30, 144, 255)
            else: color = (34, 139, 34)

            rect = pygame.Rect(offset_x + col * tile_size, offset_y + row * tile_size, tile_size, tile_size)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (20, 90, 20), rect, 1)

while True:
    width, height = screen.get_size()
    hud_height = 50
    avail_height = height - hud_height
    tile_size = min(width // GRID_SIZE, avail_height // GRID_SIZE)
    grid_px = GRID_SIZE * tile_size
    offset_x = (width - grid_px) // 2
    offset_y = hud_height + (avail_height - grid_px) // 2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not is_loading:
                mx, my = pygame.mouse.get_pos()
                if offset_x <= mx < offset_x + grid_px and offset_y <= my < offset_y + grid_px:
                    col = (mx - offset_x) // tile_size
                    row = (my - offset_y) // tile_size
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

        elif event.type == pygame.KEYDOWN:
            if is_loading:
                # Text input mode handling
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
                # Paste shortcut support (Ctrl+V)
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
                    message = "Enter save code and press ENTER (ESC to cancel)"

    screen.fill((15, 15, 15))
    draw_city(width, height)
    draw_ui_panels(width, height)
    pygame.display.flip()
    clock.tick(60)
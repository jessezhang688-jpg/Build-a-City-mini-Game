import pygame
import sys
import json
import base64
import random

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Tile City Builder - Commuters & Economy")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)
title_font = pygame.font.SysFont(None, 28)

GRID_SIZE = 30
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
house_pop = {}  # Tracks population for house tiles at (row, col)

current_tool = 1
money = 500      # Starting budget
population = 0
message = "Press R: New World | S: Save | L: Load"

# Time System Variables (1 month = 5 real seconds)
months_passed = 0
years_passed = 0

is_loading = False
input_text = ""
last_painted_tile = None

# Worker Commuter Particles
workers = []

# Game Timers
TIME_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIME_EVENT, 5000)

def recalculate_total_population():
    global population
    population = sum(house_pop.values())

def generate_world():
    global house_pop, population, months_passed, years_passed, workers
    house_pop.clear()
    workers.clear()
    population = 0
    months_passed = 0
    years_passed = 0
    
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
    serializable_house_pop = {f"{r},{c}": pop for (r, c), pop in house_pop.items()}
    data = {
        "grid": grid, 
        "money": money, 
        "house_pop": serializable_house_pop,
        "months": months_passed,
        "years": years_passed
    }
    json_str = json.dumps(data)
    code = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
    print(f"\n--- YOUR SAVE CODE ---\n{code}\n----------------------\n")
    return code

def load_game(code):
    global grid, money, house_pop, months_passed, years_passed, workers
    try:
        json_str = base64.b64decode(code.strip().encode('utf-8')).decode('utf-8')
        data = json.loads(json_str)
        grid = data["grid"]
        money = data["money"]
        months_passed = data.get("months", 0)
        years_passed = data.get("years", 0)
        
        house_pop.clear()
        workers.clear()
        if "house_pop" in data:
            for key, val in data["house_pop"].items():
                r, c = map(int, key.split(","))
                house_pop[(r, c)] = val
        else:
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    if grid[r][c] == 2:
                        house_pop[(r, c)] = 2

        recalculate_total_population()
        return True
    except:
        return False

generate_world()

def spawn_commuters():
    houses = list(house_pop.keys())
    workplaces = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if grid[r][c] in (4, 5)]
    
    if not houses or not workplaces:
        return

    for _ in range(min(len(houses), 4)):
        h = random.choice(houses)
        w = random.choice(workplaces)
        workers.append({
            "home": h,
            "start": h,
            "end": w,
            "progress": 0.0,
            "speed": random.uniform(0.015, 0.03),
            "state": "GOING",
            "work_timer": 120
        })

def draw_ui_panels(width, height):
    tile_size = min(width // GRID_SIZE, height // GRID_SIZE)
    grid_px = GRID_SIZE * tile_size
    offset_x = (width - grid_px) // 2

    # Left Panel: City Stats & Time
    left_panel = pygame.Rect(0, 0, offset_x, height)
    pygame.draw.rect(screen, (25, 25, 30), left_panel)
    pygame.draw.line(screen, (70, 70, 80), (offset_x, 0), (offset_x, height), 2)
    
    screen.blit(title_font.render("CITY STATS", True, (255, 255, 255)), (20, 25))
    
    month_names = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    current_month_name = month_names[(months_passed % 12) + 1]
    date_str = f"Date: Year {years_passed + 1}, {current_month_name}"
    screen.blit(font.render(date_str, True, (200, 200, 100)), (20, 70))

    screen.blit(font.render(f"Money: ${money}", True, (230, 200, 50)), (20, 110))
    screen.blit(font.render(f"Population: {population}", True, (100, 220, 100)), (20, 145))

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
        (2, "2. House", "$50", (220, 60, 60)),
        (3, "3. Commercial", "$75", (240, 200, 50)),
        (4, "4. Industrial", "$100", (200, 120, 40)),
        (5, "5. Bulldozer", "Free", (180, 70, 70))
    ]

    for idx, (t_id, t_name, t_cost, t_color) in enumerate(tools):
        btn_y = 80 + (idx * 60)
        btn_rect = pygame.Rect(right_x + 20, btn_y, width - right_x - 40, 48)
        
        border_color = (255, 255, 255) if current_tool == t_id else (70, 70, 80)
        bg_color = (45, 45, 55) if current_tool == t_id else (35, 35, 40)
        
        pygame.draw.rect(screen, bg_color, btn_rect, border_radius=6)
        pygame.draw.rect(screen, border_color, btn_rect, 2, border_radius=6)
        pygame.draw.rect(screen, t_color, pygame.Rect(right_x + 35, btn_y + 14, 20, 20))

        screen.blit(font.render(t_name, True, (255, 255, 255)), (right_x + 65, btn_y + 14))
        screen.blit(font.render(t_cost, True, (200, 200, 200)), (btn_rect.right - 65, btn_y + 14))

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

    absent_workers = {}
    for w in workers:
        h = w["home"]
        absent_workers[h] = absent_workers.get(h, 0) + 1

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            tile = grid[row][col]
            
            if tile == 1: color = (100, 100, 100)       # Road: Gray
            elif tile == 2: color = (220, 60, 60)      # House: Red
            elif tile == 3: color = (30, 144, 255)     # Water: Blue
            elif tile == 4: color = (240, 200, 50)     # Commercial: Yellow
            elif tile == 5: color = (200, 120, 40)     # Industrial: Orange
            else: color = (85, 105, 80)                # Grass: Muted earthy green

            rx = offset_x + col * tile_size
            ry = offset_y + row * tile_size
            rect = pygame.Rect(rx, ry, tile_size, tile_size)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (60, 75, 55), rect, 1)

            # Draw citizen population dots inside houses (minus absent workers)
            if tile == 2 and (row, col) in house_pop:
                pop_count = house_pop[(row, col)]
                absent = absent_workers.get((row, col), 0)
                effective_pop = max(0, pop_count - absent)
                
                dot_radius = max(2, tile_size // 12)
                offsets = [
                    (0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75),
                    (0.50, 0.25), (0.50, 0.75), (0.25, 0.50), (0.75, 0.50)
                ]
                for i in range(min(effective_pop, len(offsets))):
                    ox, oy = offsets[i]
                    dx = rx + int(tile_size * ox)
                    dy = ry + int(tile_size * oy)
                    pygame.draw.circle(screen, (255, 255, 255), (dx, dy), dot_radius)

    # Update and draw worker commuter particles with correct row/column mapping
    for w in workers[:]:
        start_r, start_c = w["start"]
        end_r, end_c = w["end"]
        
        start_x = offset_x + start_c * tile_size + tile_size // 2
        start_y = offset_y + start_r * tile_size + tile_size // 2
        end_x = offset_x + end_c * tile_size + tile_size // 2
        end_y = offset_y + end_r * tile_size + tile_size // 2  # FIXED: using end_r instead of end_c

        if w["state"] == "GOING":
            w["progress"] += w["speed"]
            if w["progress"] >= 1.0:
                w["progress"] = 1.0
                w["state"] = "WORKING"
            curr_x = int(start_x + (end_x - start_x) * w["progress"])
            curr_y = int(start_y + (end_y - start_y) * w["progress"])
            pygame.draw.circle(screen, (255, 255, 255), (curr_x, curr_y), 3)

        elif w["state"] == "WORKING":
            w["work_timer"] -= 1
            curr_x, curr_y = end_x, end_y
            pygame.draw.circle(screen, (255, 255, 255), (curr_x, curr_y), 3)
            if w["work_timer"] <= 0:
                w["state"] = "RETURNING"
                w["start"], w["end"] = w["end"], w["start"]
                w["progress"] = 0.0

        elif w["state"] == "RETURNING":
            w["progress"] += w["speed"]
            if w["progress"] >= 1.0:
                workers.remove(w)
                continue
            curr_x = int(start_x + (end_x - start_x) * w["progress"])
            curr_y = int(start_y + (end_y - start_y) * w["progress"])
            pygame.draw.circle(screen, (255, 255, 255), (curr_x, curr_y), 3)

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

        elif event.type == TIME_EVENT:
            months_passed += 1
            if months_passed >= 12:
                months_passed = 0
                years_passed += 1

            for pos in list(house_pop.keys()):
                if house_pop[pos] < 8 and random.random() < 0.3:
                    house_pop[pos] += 1
            recalculate_total_population()

            spawn_commuters()

            comm_count = sum(1 for r in range(GRID_SIZE) for c in range(GRID_SIZE) if grid[r][c] == 4)
            ind_count = sum(1 for r in range(GRID_SIZE) for c in range(GRID_SIZE) if grid[r][c] == 5)
            
            monthly_tax = (population * 1) + (comm_count * 3) + (ind_count * 5)
            money += monthly_tax
            if monthly_tax > 0:
                message = f"Monthly Tax Collected: ${monthly_tax}"

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            last_painted_tile = None

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not is_loading:
                mx, my = pygame.mouse.get_pos()
                right_x = offset_x + grid_px
                
                if mx >= right_x:
                    if 80 <= my <= 128: current_tool = 1
                    elif 140 <= my <= 188: current_tool = 2
                    elif 200 <= my <= 248: current_tool = 3
                    elif 260 <= my <= 308: current_tool = 4
                    elif 320 <= my <= 368: current_tool = 5

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
                elif event.key == pygame.K_4: current_tool = 4
                elif event.key == pygame.K_5: current_tool = 5
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

    # Drag-to-Paint Brush Handling
    if not is_loading and pygame.mouse.get_pressed()[0]:
        mx, my = pygame.mouse.get_pos()
        right_x = offset_x + grid_px
        if offset_x <= mx < offset_x + grid_px and offset_y <= my < offset_y + grid_px:
            col = (mx - offset_x) // tile_size
            row = (my - offset_y) // tile_size
            
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
                        house_pop[(row, col)] = 2
                        recalculate_total_population()
                    elif current_tool == 3 and current_tile == 0 and money >= 75:
                        grid[row][col] = 4
                        money -= 75
                    elif current_tool == 4 and current_tile == 0 and money >= 100:
                        grid[row][col] = 5
                        money -= 100
                    elif current_tool == 5 and current_tile != 0:
                        if current_tile == 2 and (row, col) in house_pop:
                            del house_pop[(row, col)]
                            recalculate_total_population()
                        grid[row][col] = 0
                        money += 5

    screen.fill((15, 15, 15))
    draw_city(width, height)
    draw_ui_panels(width, height)
    pygame.display.flip()
    clock.tick(60)
import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 850  # Extra space for the HUD bar
GRID_SIZE = 30

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Tile City Builder")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 24)

# Game state
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
current_tool = 1  # 1: Road, 2: House, 3: Bulldozer
money = 1000
population = 0

def draw_hud(width, height):
    hud_rect = pygame.Rect(0, 0, width, 50)
    pygame.draw.rect(screen, (35, 35, 35), hud_rect)
    pygame.draw.line(screen, (70, 70, 70), (0, 50), (width, 50), 2)

    tool_names = {1: "Road ($10)", 2: "House ($50)", 3: "Bulldozer (Free)"}
    text = font.render(f"Money: ${money}  |  Population: {population}  |  Tool: {tool_names[current_tool]}", True, (255, 255, 255))
    screen.blit(text, (20, 15))

def draw_city(width, height):
    hud_height = 50
    avail_height = height - hud_height
    tile_size = min(width // GRID_SIZE, avail_height // GRID_SIZE)
    grid_px = GRID_SIZE * tile_size
    
    offset_x = (width - grid_px) // 2
    offset_y = hud_height + (avail_height - grid_px) // 2

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            tile_type = grid[row][col]
            
            if tile_type == 1:
                color = (100, 100, 100)  # Road
            elif tile_type == 2:
                color = (46, 139, 87)    # House
            else:
                color = (25, 25, 25)     # Empty

            rect = pygame.Rect(offset_x + col * tile_size, offset_y + row * tile_size, tile_size, tile_size)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (45, 45, 45), rect, 1)

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
            mx, my = pygame.mouse.get_pos()
            if offset_x <= mx < offset_x + grid_px and offset_y <= my < offset_y + grid_px:
                col = (mx - offset_x) // tile_size
                row = (my - offset_y) // tile_size
                current_tile = grid[row][col]

                # Place Road
                if current_tool == 1 and current_tile == 0 and money >= 10:
                    grid[row][col] = 1
                    money -= 10
                # Place House
                elif current_tool == 2 and current_tile == 0 and money >= 50:
                    grid[row][col] = 2
                    money -= 50
                    population += 5
                # Bulldozer
                elif current_tool == 3 and current_tile != 0:
                    if current_tile == 2:
                        population -= 5
                    grid[row][col] = 0
                    money += 5

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_tool = 1
            elif event.key == pygame.K_2:
                current_tool = 2
            elif event.key == pygame.K_3:
                current_tool = 3

    screen.fill((15, 15, 15))
    draw_city(width, height)
    draw_hud(width, height)
    pygame.display.flip()
    clock.tick(60)
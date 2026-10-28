import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
GRID_SIZE = 30

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Tile City Builder")
clock = pygame.time.Clock()

# 0: Empty, 1: Road, 2: House
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
current_tool = 1  # Default to road

def draw_city(width, height):
    tile_size = min(width // GRID_SIZE, height // GRID_SIZE)
    grid_px = GRID_SIZE * tile_size
    offset_x = (width - grid_px) // 2
    offset_y = (height - grid_px) // 2

    # Render grid cells and colors based on type
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            tile_type = grid[row][col]
            
            if tile_type == 1:
                color = (100, 100, 100)  # Road: Gray
            elif tile_type == 2:
                color = (46, 139, 87)    # House: Green
            else:
                color = (35, 35, 35)     # Empty: Dark background

            rect = pygame.Rect(offset_x + col * tile_size, offset_y + row * tile_size, tile_size, tile_size)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (50, 50, 50), rect, 1)  # Border

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

        # Place tiles on left click
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            if offset_x <= mx < offset_x + grid_px and offset_y <= my < offset_y + grid_px:
                col = (mx - offset_x) // tile_size
                row = (my - offset_y) // tile_size
                grid[row][col] = current_tool

        # Switch tools with keyboard numbers
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_tool = 1  # Road
            elif event.key == pygame.K_2:
                current_tool = 2  # House

    screen.fill((20, 20, 20))
    draw_city(width, height)
    pygame.display.flip()
    clock.tick(60)
import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 500
ROWS, COLS = 5, 5
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Setup display
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Code Circuitry Prototype")

# Grid position
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
current_pos = (0, 0)

def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(win, WHITE, rect, 1)

def draw_current(pos):
    row, col = pos
    pygame.draw.circle(win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), SQUARE_SIZE//3)

def move_current(direction):
    global current_pos
    row, col = current_pos
    if direction == "UP" and row > 0:
        row -= 1
    elif direction == "DOWN" and row < ROWS - 1:
        row += 1
    elif direction == "LEFT" and col > 0:
        col -= 1
    elif direction == "RIGHT" and col < COLS - 1:
        col += 1
    current_pos = (row, col)

def execute_code(code):
    exec(code, globals())

def main():
    run = True
    clock = pygame.time.Clock()

    # User code to control the current
    user_code = """
# Move right 4 times
for _ in range(4):
    move_current("RIGHT")

# Move down 4 times
for _ in range(4):
    move_current("DOWN")

# Move left 4 times
for _ in range(4):
    move_current("LEFT")

# Move up 4 times
for _ in range(4):
    move_current("UP")
"""
    execute_code(user_code)

    while run:
        clock.tick(60)
        win.fill(BLACK)
        draw_grid()
        draw_current(current_pos)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()


    while run:
        clock.tick(60)
        win.fill(BLACK)
        draw_grid()
        draw_current(current_pos)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()
    sys.exit()

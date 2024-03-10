#this program enables someone to interact with the grid and to try to solve it

import pygame
import sys
from grid import Grid

#creates a random Grid
gride= Grid(3,3)
gride.Shuffle()

#initializing environment
pygame.init()
rows, cols = len(gride.state), len(gride.state[0])
tile_size = 100

background_color = (255, 255, 255)
tile_color = (0, 0, 0)
selected_color = (255, 0, 0)  # Color to indicate the selected tile

window_size = (cols * tile_size, rows * tile_size)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Jeu de Puzzle')

#initializing the counter
swapnb=0

#interface
def draw_grid(grid, selected):
    for i in range(len(grid.state)):
        for j in range(len(grid.state[0])):
            pygame.draw.rect(screen, tile_color, (j * tile_size, i * tile_size, tile_size, tile_size), 2)
            font = pygame.font.Font(None, 36)
            text = font.render(str(grid.state[i][j]), True, tile_color)
            screen.blit(text, (j * tile_size + 30, i * tile_size + 30))

    if selected:
        i, j = selected
        pygame.draw.rect(screen, selected_color, (j * tile_size, i * tile_size, tile_size, tile_size), 2)

#determins on which tile the player clicked
def find_clicked_number(grid, mouse_x, mouse_y):
    for i in range(len(grid.state)):
        for j in range(len(grid.state[0])):
            if j * tile_size <= mouse_x <= (j + 1) * tile_size and i * tile_size <= mouse_y <= (i + 1) * tile_size:
                return (i, j)
    return None

#checks if the move is legit or not
def is_valid_move(selected_tile, clicked_position):
    return(abs(selected_tile[0]-clicked_position[0])+ abs(selected_tile[1]-clicked_position[1])<=1)

#makes the swap
def swap(grid, row1, col1, row2, col2):
    grid.state[row1][col1], grid.state[row2][col2] = grid.state[row2][col2], grid.state[row1][col1]

#default parameters
max_number = rows * cols - 1
puzzle_grid = gride
selected_tile = None

while True:
    screen.fill(background_color)

    for event in pygame.event.get():
        #closing window
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #when the player clicks
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            clicked_position = find_clicked_number(puzzle_grid, mouse_x, mouse_y)

            if clicked_position:
                if selected_tile is None:
                    #selects
                    selected_tile = clicked_position
                else:
                    # exchange cells if the move is legit
                    if is_valid_move(selected_tile, clicked_position):
                        swap(puzzle_grid, selected_tile[0], selected_tile[1], clicked_position[0], clicked_position[1])
                        swapnb+=1
                    selected_tile = None

    # draws the grid
    draw_grid(puzzle_grid, selected_tile)
    pygame.display.flip()

    #checks if grid si sorted
    if gride.is_sorted():
        #will desplay a message for five seconds before quitting
        start_time = pygame.time.get_ticks()
        elapsed_time = 0
        
        #message parameters
        screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Félicitations !")
        
        font = pygame.font.Font(None, 36)
        text = font.render(f"Félicitations ! {swapnb} coups", True, "white")
        text_rect = text.get_rect()
        text_rect.center = (window_size[0] // 2, window_size[1] // 2)
        
        while  elapsed_time - pygame.time.get_ticks() < 5000:
            elapsed_time = pygame.time.get_ticks()
            screen.blit(text, text_rect)
            pygame.display.flip()
        pygame.quit()
        sys.exit()
import pygame
import sys
from grid import Grid
pygame.init()
gride= ride= Grid(2,3 , [[1, 2,5], [4,3,6]])
rows, cols = len(gride.state), len(gride.state[0])
tile_size = 100

background_color = (255, 255, 255)
tile_color = (0, 0, 0)
selected_color = (255, 0, 0)  # Couleur pour indiquer la case sélectionnée

window_size = (cols * tile_size, rows * tile_size)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Jeu de Puzzle')

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

def find_clicked_number(grid, mouse_x, mouse_y):
    for i in range(len(grid.state)):
        for j in range(len(grid.state[0])):
            if j * tile_size <= mouse_x <= (j + 1) * tile_size and i * tile_size <= mouse_y <= (i + 1) * tile_size:
                return (i, j)
    return None
def is_valid_move(selected_tile, clicked_position):
    # Vérifie si le déplacement est horizontal ou vertical
    return selected_tile[0] == clicked_position[0] or selected_tile[1] == clicked_position[1]

def swap(grid, row1, col1, row2, col2):
    grid.state[row1][col1], grid.state[row2][col2] = grid.state[row2][col2], grid.state[row1][col1]

max_number = rows * cols - 1
puzzle_grid = gride
selected_tile = None

while True:
    screen.fill(background_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            clicked_position = find_clicked_number(puzzle_grid, mouse_x, mouse_y)

            if clicked_position:
                if selected_tile is None:
                    # Sélectionne la case si aucune case n'est déjà sélectionnée
                    selected_tile = clicked_position
                else:
                    # Déplace la case sélectionnée vers la case cliquée si le déplacement est valide
                    if is_valid_move(selected_tile, clicked_position):
                        swap(puzzle_grid, selected_tile[0], selected_tile[1], clicked_position[0], clicked_position[1])
                    selected_tile = None

    # Dessine la grille
    draw_grid(puzzle_grid, selected_tile)
    pygame.display.flip()
    if gride.is_sorted():
        print("Félicitations ! Vous avez résolu le puzzle.")
        pygame.quit()
        sys.exit()
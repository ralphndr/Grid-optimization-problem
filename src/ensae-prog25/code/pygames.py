import pygame
import sys
import os
from grid import Grid
from solver import SolverMaxWeightMatching
from solver import SolverMinimax 


# Define the colors for the cell
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GREY = (211, 211, 211)

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
grid = Grid.grid_from_file('ensae-prog25/input/grid17.in', read_values=True)


rows, cols = grid.n, grid.m
cell_size = 50  # Set the cell size 
grid_width = cols * cell_size
grid_height = rows * cell_size


# Define scoreboard 
scoreboard_width = 200
scoreboard_height = grid_height
scoreboard_x = grid_width

# Set up display
size = width, height = grid_width + scoreboard_width, grid_height
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Jeu")

# Set up display for the menu
menu_width, menu_height = 800, 800
menu_screen = pygame.display.set_mode((menu_width, menu_height))

# Define color map
color_map = [[(255, 255, 255) for _ in range(cols)] for _ in range(rows)]
for i in range(rows):
    for j in range(cols):
        if grid.color[i][j] == 0:
            color_map[i][j] = WHITE
        elif grid.color[i][j] == 1:
            color_map[i][j] = RED
        elif grid.color[i][j] == 2:
            color_map[i][j] = BLUE
        elif grid.color[i][j] == 3:
            color_map[i][j] = GREEN
        elif grid.color[i][j] == 4:
            color_map[i][j] = BLACK



players = ["Player 1", "Player 2"]
current_player = 0  
scores = [0, 0]

font = pygame.font.SysFont(None, 36)

def display_current_player():
    player_text = font.render(f'{players[current_player]}\'s Turn', True, BLACK)
    screen.blit(player_text, (scoreboard_x + 10, 50))

def update_score():
    score_text = font.render(f'Score: {scores[0]} - {scores[1]}', True, BLACK)
    screen.blit(score_text, (scoreboard_x + 10, 10))

def is_valid_pair(cell1, cell2):
    return (cell1, cell2) in grid.all_pairs() or (cell2, cell1) in grid.all_pairs()

def update_pairs_and_check_winner():
    available_pairs = [pair for pair in grid.all_pairs() if color_map[pair[0][0]][pair[0][1]] != LIGHT_GREY and color_map[pair[1][0]][pair[1][1]] != LIGHT_GREY]
    if not available_pairs:
        if scores[0] == scores[1]:
            display_winner("Draw")
        else:
            winner = players[scores.index(min(scores))]
            display_winner(winner)
        return False
    return True


def display_winner(winner):
    if winner == "Draw":
        winner_text = font.render('Draw!', True, BLACK)
    else:
        winner_text = font.render(f'{winner} Wins!', True, BLACK)
    screen.fill(WHITE)
    screen.blit(winner_text, (width // 2 - winner_text.get_width() // 2, height // 2 - winner_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(10000)  


def display_menu():
    menu_screen.fill(WHITE)
    title_font = pygame.font.SysFont(None, 48)
    button_font = pygame.font.SysFont(None, 36)
    title_text = title_font.render('Menu', True, BLACK)
    menu_screen.blit(title_text, (menu_width // 2 - title_text.get_width() // 2, menu_height // 4 - title_text.get_height() // 2))
    button_1_text = button_font.render('1 joueur', True, BLACK)
    button_2_text = button_font.render('2 joueurs', True, BLACK)
    button_1_rect = pygame.Rect(menu_width // 2 - 100, menu_height // 2 - 50, 200, 50)
    button_2_rect = pygame.Rect(menu_width // 2 - 100, menu_height // 2 + 10, 200, 50)
    pygame.draw.rect(menu_screen, LIGHT_GREY, button_1_rect)
    pygame.draw.rect(menu_screen, LIGHT_GREY, button_2_rect)
    menu_screen.blit(button_1_text, (button_1_rect.x + button_1_rect.width // 2 - button_1_text.get_width() // 2, button_1_rect.y + button_1_rect.height // 2 - button_1_text.get_height() // 2))
    menu_screen.blit(button_2_text, (button_2_rect.x + button_2_rect.width // 2 - button_2_text.get_width() // 2, button_2_rect.y + button_2_rect.height // 2 - button_2_text.get_height() // 2))
    pygame.display.flip()
    return button_1_rect, button_2_rect



def single_player_minimax_game():
    """
    Special mode for "1 joueur" where Player 1 (AI) uses SolverMinimax and Player 2 (human) selects pairs directly from the grid.
    """
    global current_player  
    solver = SolverMinimax(grid)  # Initialize SolverMinimax for AI (it's the best solver for 1V1 that we developped)
    screen = pygame.display.set_mode((width, height))
    running = True
    selected_cells = []

    while running:
        if current_player == 1:  #player's turn
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if x < grid_width:  # Ensure the click is within the grid
                        col = x // cell_size
                        row = y // cell_size
                        if color_map[row][col] != LIGHT_GREY:  # Ensure the cell is not already used
                            selected_cells.append((row, col))
                            if len(selected_cells) == 2:  # Two cells selected
                                if is_valid_pair(selected_cells[0], selected_cells[1]):
                                    scores[current_player] += grid.cost((selected_cells[0], selected_cells[1]))
                                    color_map[selected_cells[0][0]][selected_cells[0][1]] = LIGHT_GREY
                                    color_map[selected_cells[1][0]][selected_cells[1][1]] = LIGHT_GREY
                                    current_player = 0  # Switch to AI
                                    solver.player_move((selected_cells[0], selected_cells[1]))
                                    if not update_pairs_and_check_winner():
                                        running = False
                                selected_cells = []
        elif current_player == 0:  # AI's turn
            move = solver.best_move()
            if move:
                # Update the score for the current player
                print(current_player)
                scores[current_player] += grid.cost(move)
                # Mark the chosen cells as used (light grey)
                color_map[move[0][0]][move[0][1]] = LIGHT_GREY
                color_map[move[1][0]][move[1][1]] = LIGHT_GREY
                solver.pairs.append(move)
                solver.remaining_pairs = solver.valid_pairs()
                current_player=1
            if not update_pairs_and_check_winner():
                running = False

        # Draw grid
        for row in range(rows):
            for col in range(cols):
                color = color_map[row][col]
                pygame.draw.rect(screen, color, (col * cell_size, row * cell_size, cell_size, cell_size))
                pygame.draw.rect(screen, BLACK, (col * cell_size, row * cell_size, cell_size, cell_size), 1)
                cell_value = str(grid.value[row][col])
                text = font.render(cell_value, True, (169, 169, 169))
                screen.blit(text, (col * cell_size + cell_size // 2 - text.get_width() // 2, row * cell_size + cell_size // 2 - text.get_height() // 2))
        pygame.draw.rect(screen, BLACK, (0, 0, grid_width, grid_height), 3)
        pygame.draw.rect(screen, WHITE, (scoreboard_x, 0, scoreboard_width, scoreboard_height))
        update_score()
        display_current_player()
        pygame.display.flip()
    pygame.quit()
    sys.exit()



def ia_vs_ia_game():
    """
    Mode where both players are AIs using SolverMinimax, alternating turns to minimize their scores.
    """
    global current_player  # Ensure current_player is accessible
    solver1 = SolverMinimax(grid)  # AI for Player 1
    solver2 = SolverMinimax(grid)  # AI for Player 2
    screen = pygame.display.set_mode((width, height))
    running = True

    while running:
        solver = solver1 if current_player == 1 else solver2
        solver.remaining_pairs = solver.valid_pairs()
        move = solver.best_move()
        if move:
            print(current_player)
            scores[current_player] += grid.cost(move)
            color_map[move[0][0]][move[0][1]] = LIGHT_GREY
            color_map[move[1][0]][move[1][1]] = LIGHT_GREY
            if current_player == 1 : 
                solver1.pairs.append(move)
                solver1.remaining_pairs = solver1.valid_pairs()
                solver2.player_move(move)
            else :
                solver2.pairs.append(move)
                solver2.remaining_pairs = solver2.valid_pairs()
                solver1.player_move(move)

            for row in range(rows):
                for col in range(cols):
                    color = color_map[row][col]
                    pygame.draw.rect(screen, color, (col * cell_size, row * cell_size, cell_size, cell_size))
                    pygame.draw.rect(screen, BLACK, (col * cell_size, row * cell_size, cell_size, cell_size), 1)
                    cell_value = str(grid.value[row][col])
                    text = font.render(cell_value, True, (169, 169, 169))
                    screen.blit(text, (col * cell_size + cell_size // 2 - text.get_width() // 2, row * cell_size + cell_size // 2 - text.get_height() // 2))

            pygame.draw.rect(screen, BLACK, (0, 0, grid_width, grid_height), 3)
            pygame.draw.rect(screen, WHITE, (scoreboard_x, 0, scoreboard_width, scoreboard_height))
            update_score()
            display_current_player()
            pygame.display.flip()
            pygame.time.wait(3000)  # Wait for 3 seconds to show the chosen pair
            current_player = 1 - current_player
            if not update_pairs_and_check_winner():
                running = False
        else:
            running = False # No valid moves left, end the game

    # Display final scores and winner
    screen.fill(WHITE)
    final_scores_text = font.render(f"Final Scores: Player 1: {scores[0]} - Player 2: {scores[1]}", True, BLACK)
    screen.blit(final_scores_text, (width // 2 - final_scores_text.get_width() // 2, height // 2 - 50))
    winner = "Player 1" if scores[0] < scores[1] else "Player 2" if scores[1] < scores[0] else "Draw"
    winner_text = font.render(f"Winner: {winner}", True, BLACK)
    screen.blit(winner_text, (width // 2 - winner_text.get_width() // 2, height // 2 + 10))
    pygame.display.flip()
    pygame.time.wait(5000)
    pygame.quit()
    sys.exit()


def handle_menu():
    button_1_rect, button_2_rect = display_menu()
    button_3_text = pygame.font.SysFont(None, 36).render('IA contre IA', True, BLACK)
    button_3_rect = pygame.Rect(menu_width // 2 - 100, menu_height // 2 + 70, 200, 50)
    pygame.draw.rect(menu_screen, LIGHT_GREY, button_3_rect)
    menu_screen.blit(button_3_text, (button_3_rect.x + button_3_rect.width // 2 - button_3_text.get_width() // 2, button_3_rect.y + button_3_rect.height // 2 - button_3_text.get_height() // 2))
    pygame.display.flip()
    in_menu = True

    while in_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_1_rect.collidepoint(event.pos):
                    in_menu = False
                    single_player_minimax_game()  
                elif button_2_rect.collidepoint(event.pos):
                    in_menu = False
                    main_game()
                elif button_3_rect.collidepoint(event.pos):
                    in_menu = False
                    ia_vs_ia_game()  



def display_blank_window():
    blank_screen = pygame.display.set_mode((menu_width, menu_height))
    blank_screen.fill(WHITE)
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()
    sys.exit()


# Main game function
def main_game():
    global current_player  
    screen = pygame.display.set_mode((width, height))
    running = True
    selected_cells = []
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x < grid_width:
                    col = x // cell_size
                    row = y // cell_size
                    if color_map[row][col] != LIGHT_GREY:  
                        selected_cells.append((row, col))
                        if len(selected_cells) == 2:
                            if is_valid_pair(selected_cells[0], selected_cells[1]):
                                scores[current_player] += grid.cost((selected_cells[0], selected_cells[1]))
                                color_map[selected_cells[0][0]][selected_cells[0][1]] = LIGHT_GREY
                                color_map[selected_cells[1][0]][selected_cells[1][1]] = LIGHT_GREY
                                current_player = (current_player + 1) % 2
                                if not update_pairs_and_check_winner():
                                    running = False
                            selected_cells = []

        for row in range(rows):
            for col in range(cols):
                color = color_map[row][col]
                pygame.draw.rect(screen, color, (col * cell_size, row * cell_size, cell_size, cell_size))
                pygame.draw.rect(screen, BLACK, (col * cell_size, row * cell_size, cell_size, cell_size), 1)  
                cell_value = str(grid.value[row][col])
                text = font.render(cell_value, True, (169, 169, 169))  
                screen.blit(text, (col * cell_size + cell_size // 2 - text.get_width() // 2, row * cell_size + cell_size // 2 - text.get_height() // 2))

        pygame.draw.rect(screen, BLACK, (0, 0, grid_width, grid_height), 3)
        pygame.draw.rect(screen, WHITE, (scoreboard_x, 0, scoreboard_width, scoreboard_height))
        update_score()
        display_current_player()
        pygame.display.flip()
    pygame.quit()
    sys.exit()

# Start the game with the menu
handle_menu()
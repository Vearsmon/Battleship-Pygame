import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
ARIAL_50 = pygame.font.SysFont('arial', 50)


def draw_ship(screen, battleship, cell_size):
    if battleship.horizontal:
        pygame.draw.line(screen, BLACK, (battleship.location_x, battleship.location_y),
                         (battleship.location_x + battleship.size[0] * cell_size, battleship.location_y), 8)
        pygame.draw.line(screen, BLACK, (battleship.location_x, battleship.location_y + battleship.size[1] * cell_size),
                         (battleship.location_x + battleship.size[0] * cell_size, battleship.location_y +
                          battleship.size[1] * cell_size), 8)
        pygame.draw.line(screen, BLACK, (battleship.location_x, battleship.location_y),
                         (battleship.location_x, battleship.location_y + battleship.size[1] * cell_size), 8)
        pygame.draw.line(screen, BLACK, (battleship.location_x + battleship.size[0] * cell_size, battleship.location_y),
                         (battleship.location_x + battleship.size[0] * cell_size, battleship.location_y +
                          battleship.size[1] * cell_size), 8)

    else:
        pygame.draw.line(screen, BLACK, (battleship.location_x, battleship.location_y),
                         (battleship.location_x, battleship.location_y + battleship.size[0] * cell_size), 8)
        pygame.draw.line(screen, BLACK, (battleship.location_x + battleship.size[1] * cell_size, battleship.location_y),
                         (battleship.location_x + battleship.size[1] * cell_size, battleship.location_y +
                          battleship.size[0] * cell_size), 8)
        pygame.draw.line(screen, BLACK, (battleship.location_x, battleship.location_y),
                         (battleship.location_x + battleship.size[1] * cell_size, battleship.location_y), 8)
        pygame.draw.line(screen, BLACK, (battleship.location_x, battleship.location_y + battleship.size[0] * cell_size),
                         (battleship.location_x + battleship.size[1] * cell_size, battleship.location_y +
                          battleship.size[0] * cell_size), 8)


def draw_board(screen, board):
    for i in range(board.board_size + 1):
        pygame.draw.line(screen, BLACK, (board.left_upper_corner[0] + i * board.cell_size, board.left_upper_corner[1]),
                         (board.left_upper_corner[0] + i * board.cell_size,
                          board.left_upper_corner[1] + board.board_size * board.cell_size), 2)
        pygame.draw.line(screen, BLACK, (board.left_upper_corner[0], board.left_upper_corner[1] + i * board.cell_size),
                         (board.left_upper_corner[0] + board.board_size * board.cell_size,
                          board.left_upper_corner[1] + i * board.cell_size), 2)


def draw_cross_on_cell(surf, x, y, color, board):
    if 0 <= x < board.board_size and 0 <= y < board.board_size:
        selected_cell_x = board.left_upper_corner[0] + board.cell_size * x
        selected_cell_y = board.left_upper_corner[1] + board.cell_size * y
        pygame.draw.line(surf, color, (selected_cell_x, selected_cell_y),
                         (selected_cell_x + board.cell_size, selected_cell_y + board.cell_size), 8)
        pygame.draw.line(surf, color, (selected_cell_x, selected_cell_y + board.cell_size),
                         (selected_cell_x + board.cell_size, selected_cell_y), 8)


def draw_buttons(buttons, surf, current_button_index, x, y, option_y_padding):
    for i, button_text in enumerate(buttons):
        button_surf = ARIAL_50.render(button_text, True, BLACK)
        button_rect = button_surf.get_rect()
        button_rect.center = (x, y + i * option_y_padding)
        if i == current_button_index:
            button_surf = ARIAL_50.render(button_text, True, WHITE)
            button_rect = button_surf.get_rect()
            button_rect.center = (x, y + i * option_y_padding)
            pygame.draw.rect(surf, BLACK, button_rect)
        surf.blit(button_surf, button_rect)


def draw_text(surf, x, y, text):
    text_surf = ARIAL_50.render(text, True, BLACK)
    text_rect = text_surf.get_rect()
    text_rect.center = (x, y)
    surf.blit(text_surf, text_rect)

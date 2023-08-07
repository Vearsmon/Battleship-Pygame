import pygame
import Game
import Drawing


WIDTH = 1280
HEIGHT = 480
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


menu_screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")


def accept_and_start(board_size, ships, mode, ship_setting_mode):
    game = Game.Game(board_size, ships, mode, ship_setting_mode)
    game.run()


def run_ships_settings_menu(board_size, mode, ship_setting_mode):
    current_button_index = 0
    buttons = ['ACCEPT']
    running = True
    ship_attributes = ''
    total_size = 0
    ships = []
    while running:
        menu_screen.fill(WHITE)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_e:
                    ship_attributes = ship_attributes.split()
                    ship_size = int(ship_attributes[0]) * int(ship_attributes[1]) + 4 + 2 * int(ship_attributes[0]) + 2 * int(ship_attributes[1])
                    if total_size + ship_size * int(ship_attributes[2]) <= board_size * board_size and \
                            int(ship_attributes[0]) + 2 <= board_size and int(ship_attributes[1]) + 2 <= board_size:
                        ships.append((min(int(ship_attributes[0]), int(ship_attributes[1])), max(int(ship_attributes[0]), int(ship_attributes[1])), int(ship_attributes[2])))
                        total_size = total_size + ship_size * int(ship_attributes[2])
                        ship_attributes = ''
                    else:
                        ship_attributes = ''
                if e.key == pygame.K_BACKSPACE:
                    if len(ship_attributes) > 0:
                        ship_attributes = ship_attributes[:-1]
                if e.key == pygame.K_f or total_size >= board_size * board_size - 9:
                    running = False
                    accept_and_start(board_size, ships, mode, ship_setting_mode)
                if e.key == pygame.K_d:
                    if len(ships) > 0:
                        deleted_ship = ships.pop()
                        total_size -= (deleted_ship[0] * deleted_ship[1] + 4 + 2 * deleted_ship[0] + 2 * deleted_ship[1]) * deleted_ship[2]
                else:
                    try:
                        if chr(e.key) in '1234567890 ':
                            if not (chr(e.key) == '0' and len(ship_attributes) == 0):
                                if not (chr(e.key) == ' ' and ship_attributes[-1] == ' '):
                                    if ship_attributes.count(' ') <= 2 - (1 if chr(e.key) == ' ' else 0):
                                        ship_attributes += chr(e.key)
                    except:
                        pass
        Drawing.draw_text(menu_screen, WIDTH / 2, HEIGHT / 2 - 100, 'ENTER SHIP SIZE:')
        Drawing.draw_text(menu_screen, WIDTH / 2, HEIGHT / 2 - 25, ship_attributes)
        Drawing.draw_text(menu_screen, 150, HEIGHT / 2 + 150, 'USING SHIPS:')
        for i,ship in enumerate(ships):
            Drawing.draw_text(menu_screen, 400 + i * 300, HEIGHT / 2 + 150, str(ship[0]) + 'x' + str(ship[1]) + ' - ' + str(ship[2]) + ' units')
        Drawing.draw_buttons(buttons, menu_screen, current_button_index, WIDTH / 2, HEIGHT / 2 + 50, 75)
        pygame.display.flip()


def run_ship_settings_menu(mode, ship_setting_mode):
    current_button_index = 0
    buttons = ['ACCEPT']
    running = True
    board_size = ''
    while running:
        menu_screen.fill(WHITE)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    if int(board_size) > 3:
                        running = False
                        run_ships_settings_menu(int(board_size), mode, ship_setting_mode)
                if e.key == pygame.K_BACKSPACE:
                    if len(board_size) > 0:
                        board_size = board_size[:-1]
                else:
                    try:
                        if chr(e.key) in '1234567890':
                            if not (chr(e.key) == '0' and len(board_size) == 0):
                                board_size += chr(e.key)
                    except:
                        pass
        Drawing.draw_text(menu_screen, WIDTH / 2, HEIGHT / 2 - 100, 'ENTER BOARD SIZE:')
        Drawing.draw_text(menu_screen, WIDTH / 2, HEIGHT / 2 - 25, board_size)
        Drawing.draw_buttons(buttons, menu_screen, current_button_index, WIDTH / 2, HEIGHT / 2 + 50, 75)
        pygame.display.flip()


def run_ship_setting_mode_menu(mode):
    current_button_index = 0
    buttons = ['MANUAL', 'AUTO']
    options = [lambda: run_ship_settings_menu(mode, 'manual'), lambda: run_ship_settings_menu(mode, 'auto')]
    running = True
    while running:
        menu_screen.fill(WHITE)
        Drawing.draw_text(menu_screen, WIDTH / 2, HEIGHT / 10, 'CHOOSE SHIP SETTING MODE')
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_w:
                    current_button_index = max(0, min(current_button_index - 1, len(buttons) - 1))
                if e.key == pygame.K_s:
                    current_button_index = max(0, min(current_button_index + 1, len(buttons) - 1))
                if e.key == pygame.K_SPACE:
                    running = False
                    options[current_button_index]()
                if e.key == pygame.K_ESCAPE:
                    exit()
        Drawing.draw_buttons(buttons, menu_screen, current_button_index, WIDTH / 2, HEIGHT / 2 - 100, 75)
        pygame.display.flip()


def run_main_menu():
    current_button_index = 0
    buttons = ['Player vs. Strong Bot', 'Player vs. Weak Bot', 'Player vs. Player', 'Quit']
    options = [lambda: run_ship_setting_mode_menu('strong bot'), lambda: run_ship_setting_mode_menu('weak bot'), lambda: run_ship_setting_mode_menu('2 players'), lambda: exit()]
    running = True
    while running:
        menu_screen.fill(WHITE)
        Drawing.draw_text(menu_screen, WIDTH / 2, HEIGHT / 10, '=BATTLESHIP=')
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_w:
                    current_button_index = max(0, min(current_button_index - 1, len(buttons) - 1))
                if e.key == pygame.K_s:
                    current_button_index = max(0, min(current_button_index + 1, len(buttons) - 1))
                if e.key == pygame.K_SPACE:
                    running = False
                    options[current_button_index]()
                if e.key == pygame.K_ESCAPE:
                    exit()
        Drawing.draw_buttons(buttons, menu_screen, current_button_index, WIDTH / 2, HEIGHT / 2 - 100, 75)
        pygame.display.flip()


def win_screen(winner):
    current_button_index = 0
    buttons = ['Back to menu']
    options = [lambda: run_main_menu()]
    running = True
    while running:
        menu_screen.fill(WHITE)
        Drawing.draw_text(menu_screen, WIDTH / 2, HEIGHT / 10, winner + ' won!')
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_w:
                    current_button_index = max(0, min(current_button_index - 1, len(buttons) - 1))
                if e.key == pygame.K_s:
                    current_button_index = max(0, min(current_button_index + 1, len(buttons) - 1))
                if e.key == pygame.K_SPACE:
                    running = False
                    options[current_button_index]()
                if e.key == pygame.K_ESCAPE:
                    exit()
        Drawing.draw_buttons(buttons, menu_screen, current_button_index, WIDTH / 2, HEIGHT / 2 - 100, 75)
        pygame.display.flip()

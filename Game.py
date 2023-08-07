import copy
import pygame
import Board
import Menu
import Ship
import random
import Drawing

WIDTH = 1280
HEIGHT = 480
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Battleship')


class Game:
    def __init__(self, board_size, ships, play_mode, ship_setting_mode):
        self.ships = ships
        self.ship_setting_mode = ship_setting_mode
        self.play_mode = play_mode
        self.destroyed_ships = []
        self.next_moves = []
        self.selected_cell_index_x = -1
        self.selected_cell_index_y = -1
        self.selected_cell_x = -1
        self.selected_cell_y = -1
        self.first_player_turn = True
        self.board_1 = Board.Board([40, 40], board_size, (HEIGHT - 60) / board_size)
        self.board_2 = Board.Board([600, 40], board_size, (HEIGHT - 60) / board_size)

    def check_hover(self, pos, board):
        if not (board.left_upper_corner[0] <= pos[0] <= board.right_lower_corner[0] and
                board.left_upper_corner[1] <= pos[1] <= board.right_lower_corner[1]):
            return
        self.selected_cell_x = -1
        self.selected_cell_y = -1
        for i in range(board.board_size):
            for j in range(board.board_size):
                current_cell_coord_x = board.left_upper_corner[0] + board.cell_size * i
                current_cell_coord_y = board.left_upper_corner[1] + board.cell_size * j
                if current_cell_coord_x < pos[0] < current_cell_coord_x + board.cell_size:
                    if current_cell_coord_y < pos[1] < current_cell_coord_y + board.cell_size:
                        pygame.draw.rect(screen, GREEN,
                                         (current_cell_coord_x, current_cell_coord_y,
                                          board.cell_size, board.cell_size))
                        self.selected_cell_index_x = i
                        self.selected_cell_index_y = j
                        self.selected_cell_x = current_cell_coord_x
                        self.selected_cell_y = current_cell_coord_y

    def check_input(self, board):
        pos = pygame.mouse.get_pos()
        self.check_hover(pos, board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.selected_cell_x != -1 and self.selected_cell_y != -1 and \
                            board.board[self.selected_cell_index_y][self.selected_cell_index_x] not in [-1, -2]:
                        board.board[self.selected_cell_index_y][self.selected_cell_index_x] = -1
                        self.first_player_turn = board != self.board_1

    def place_ships_manually(self, board):
        all_ships = []
        for ship_size in self.ships:
            for ship in range(ship_size[2]):
                all_ships.append((ship_size[0], ship_size[1]))
        ship_counter = 0
        ship_cell_x = 0
        ship_cell_y = 0
        horizontal = True
        while ship_counter != len(all_ships):
            screen.fill(WHITE)
            next_ship = all_ships[ship_counter]
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s and ship_cell_y + next_ship[1 if horizontal else 0] < board.board_size:
                        ship_cell_y += 1
                    if event.key == pygame.K_w and ship_cell_y > 0:
                        ship_cell_y -= 1
                    if event.key == pygame.K_d and ship_cell_x + next_ship[0 if horizontal else 1] < board.board_size:
                        ship_cell_x += 1
                    if event.key == pygame.K_a and ship_cell_x > 0:
                        ship_cell_x -= 1
                    if event.key == pygame.K_r:
                        horizontal = not horizontal
                        while not horizontal and ship_cell_y + next_ship[1] > board.board_size:
                            ship_cell_y -= 1
                        while horizontal and ship_cell_x + next_ship[0] > board.board_size:
                            ship_cell_x -= 1
                    if event.key == pygame.K_SPACE:
                        location_x = ship_cell_x * board.cell_size + board.left_upper_corner[0]
                        location_y = ship_cell_y * board.cell_size + board.left_upper_corner[1]
                        battleship = Ship.Ship(next_ship, location_x, location_y, ship_cell_x, ship_cell_y, horizontal)
                        if self.check_ships_collision(battleship, board):
                            board.ship_set.add(battleship)
                            self.fill_board_with_ship(battleship, board)
                            ship_cell_x = 0
                            ship_cell_y = 0
                            horizontal = True
                            ship_counter += 1

            for i in range(ship_cell_x, ship_cell_x + next_ship[0 if horizontal else 1]):
                for j in range(ship_cell_y, ship_cell_y + next_ship[1 if horizontal else 0]):
                    location_x = ship_cell_x * board.cell_size + board.left_upper_corner[0]
                    location_y = ship_cell_y * board.cell_size + board.left_upper_corner[1]
                    battleship = Ship.Ship(next_ship, location_x, location_y, ship_cell_x, ship_cell_y, horizontal)
                    pygame.draw.rect(screen, GREEN if (self.check_ships_collision(battleship, board)) else RED,
                                     (board.left_upper_corner[0] + board.cell_size * i,
                                      board.left_upper_corner[1] + board.cell_size * j,
                                      board.cell_size, board.cell_size))
            Drawing.draw_board(screen, board)
            for ship in self.board_1.ship_set:
                Drawing.draw_ship(screen, ship, board.cell_size)
            for ship in self.board_2.ship_set:
                Drawing.draw_ship(screen, ship, board.cell_size)
            pygame.display.flip()

    def place_ships_randomly(self, board):
        for ship_size in self.ships:
            for ship in range(ship_size[2]):
                size = (ship_size[0], ship_size[1])
                self.try_place_ship(size, board)

    def generate_ship_with_random_position(self, size, board):
        ship_cell_x = random.randint(0, board.board_size - 1)
        ship_cell_y = random.randint(0, board.board_size - 1)
        horizontal = bool(random.randint(0, 1))
        location_x = ship_cell_x * board.cell_size + board.left_upper_corner[0]
        location_y = ship_cell_y * board.cell_size + board.left_upper_corner[1]
        return Ship.Ship(size, location_x, location_y, ship_cell_x, ship_cell_y, horizontal)

    def try_place_ship(self, size, board):
        battleship = self.generate_ship_with_random_position(size, board)
        while not self.check_ship_borders(battleship, board):
            battleship = self.generate_ship_with_random_position(size, board)
        board.ship_set.add(battleship)
        self.fill_board_with_ship(battleship, board)

    def fill_board_with_ship(self, ship, board):
        for i in range(ship.size[0]):
            for j in range(ship.size[1]):
                board.board[ship.ship_cell_y + (j if ship.horizontal else i)][ship.ship_cell_x + (i if ship.horizontal else j)] = 1

    def check_ship_borders(self, ship, board):
        if ship.ship_cell_x + ship.size[0 if ship.horizontal else 1] <= board.board_size and \
                ship.ship_cell_y + ship.size[1 if ship.horizontal else 0] <= board.board_size:
            return self.check_ships_collision(ship, board)
        return False

    def check_ships_collision(self, ship, board):
        for i in range(ship.ship_cell_x - 1, ship.ship_cell_x + ship.size[0 if ship.horizontal else 1] + 1):
            for j in range(ship.ship_cell_y - 1, ship.ship_cell_y + ship.size[1 if ship.horizontal else 0] + 1):
                if 0 <= j < board.board_size and 0 <= i < board.board_size and board.board[j][i] == 1:
                    return False
        return True

    def check_target_inside_borders(self, target_x, target_y):
        return 0 <= target_x < self.board_1.board_size and 0 <= target_y < self.board_1.board_size

    def mark_non_relevant_cells(self, board):
        for i in range(board.board_size):
            for j in range(board.board_size):
                if board.board[j][i] == -1:
                    if self.check_target_inside_borders(j + 1, i + 1) and board.board[j + 1][i + 1] == board.board[j + 1][i] == -2:
                        if i - 1 >= 0:
                            board.board[j][i - 1] = -1
                        board.board[j][i + 1] = -1
                    if self.check_target_inside_borders(j + 1, i + 1) and board.board[j + 1][i + 1] == board.board[j][i + 1] == -2:
                        if j - 1 >= 0:
                            board.board[j - 1][i] = -1
                        board.board[j + 1][i] = -1
                    if self.check_target_inside_borders(j - 1, i - 1) and board.board[j - 1][i - 1] == board.board[j - 1][i] == -2:
                        if i + 1 < board.board_size:
                            board.board[j][i + 1] = -1
                        board.board[j][i - 1] = -1
                    if self.check_target_inside_borders(j - 1, i - 1) and board.board[j - 1][i - 1] == board.board[j][i - 1] == -2:
                        if j + 1 < board.board_size:
                            board.board[j + 1][i] = -1
                        board.board[j - 1][i] = -1
                    if self.check_target_inside_borders(j + 1, i - 1) and board.board[j + 1][i - 1] == board.board[j + 1][i] == -2:
                        if i + 1 < board.board_size:
                            board.board[j][i + 1] = -1
                        board.board[j][i - 1] = -1
                    if self.check_target_inside_borders(j + 1, i - 1) and board.board[j + 1][i - 1] == board.board[j][i - 1] == -2:
                        if j - 1 >= 0:
                            board.board[j - 1][i] = -1
                        board.board[j + 1][i] = -1
                    if self.check_target_inside_borders(j - 1, i + 1) and board.board[j - 1][i + 1] == board.board[j - 1][i] == -2:
                        if i - 1 >= 0:
                            board.board[j][i + 1] = -1
                        board.board[j][i - 1] = -1
                    if self.check_target_inside_borders(j - 1, i + 1) and board.board[j - 1][i + 1] == board.board[j][i + 1] == -2:
                        if j + 1 < board.board_size:
                            board.board[j + 1][i] = -1
                        board.board[j - 1][i] = -1

    def fill_board_with_crosses(self, board):
        for i in range(board.board_size):
            for j in range(board.board_size):
                if board.board[j][i] == -1:
                    if board.start_condition[j][i] == 1:
                        Drawing.draw_cross_on_cell(screen, i, j, RED, board)
                        self.detect_destroyed_ships(i, j, board)
                    else:
                        Drawing.draw_cross_on_cell(screen, i, j, BLACK, board)
                if board.board[j][i] == -2:
                    Drawing.draw_cross_on_cell(screen, i, j, RED, board)

    def detect_destroyed_ships(self, x, y, board):
        for ship in board.ship_set:
            if (x, y) in ship.all_ship_coords:
                board.board[y][x] = -2
                ship.health -= 1
                if ship.health <= 0:
                    self.destroyed_ships.append(ship)
                    self.mark_destroyed_ship_zone(ship, board)

    def mark_destroyed_ship_zone(self, ship, board):
        for x in range(ship.ship_cell_x - 1, ship.ship_cell_x + ship.size[0 if ship.horizontal else 1] + 1):
            for y in range(ship.ship_cell_y - 1, ship.ship_cell_y + ship.size[1 if ship.horizontal else 0] + 1):
                if (x, y) not in ship.all_ship_coords and 0 <= x < board.board_size and 0 <= y < board.board_size:
                    board.board[y][x] = -1

    def is_lose(self, ship_set):
        for ship in ship_set:
            if ship.health > 0:
                return False
        return True

    def play_game_with_2_players(self):
        self.check_input(self.board_1 if self.first_player_turn else self.board_2)
        for ship in (self.board_2.ship_set if self.first_player_turn else self.board_1.ship_set):
            Drawing.draw_ship(screen, ship, self.board_1.cell_size)
        for ship in self.destroyed_ships:
            Drawing.draw_ship(screen, ship, self.board_1.cell_size)

    def play_against_weak_bot(self):
        if self.first_player_turn:
            self.check_input(self.board_1)
        else:
            self.make_random_shot(change_tactic=False)
            self.first_player_turn = True
        for ship in self.board_2.ship_set:
            Drawing.draw_ship(screen, ship, self.board_1.cell_size)
        for ship in self.destroyed_ships:
            Drawing.draw_ship(screen, ship, self.board_1.cell_size)

    def make_random_shot(self, change_tactic=False):
        hit_x = random.randint(0, self.board_1.board_size - 1)
        hit_y = random.randint(0, self.board_1.board_size - 1)
        while self.board_2.board[hit_y][hit_x] == -1 or self.board_2.board[hit_y][hit_x] == -2:
            hit_x = random.randint(0, self.board_1.board_size - 1)
            hit_y = random.randint(0, self.board_1.board_size - 1)
        self.board_2.board[hit_y][hit_x] = -1
        if change_tactic and self.board_2.start_condition[hit_y][hit_x] == 1:
            self.next_moves = [(hit_x + 1, hit_y),
                               (hit_x - 1, hit_y),
                               (hit_x, hit_y + 1),
                               (hit_x, hit_y - 1),
                               (hit_x + 1, hit_y + 1),
                               (hit_x - 1, hit_y - 1),
                               (hit_x - 1, hit_y + 1),
                               (hit_x + 1, hit_y - 1)]

    def play_against_strong_bot(self):
        if self.first_player_turn:
            self.check_input(self.board_1)
        else:
            if self.next_moves:
                next_move = self.next_moves.pop(0)
                while (not self.check_target_inside_borders(next_move[0], next_move[1]) or
                       (self.board_2.board[next_move[1]][next_move[0]] == -1 or
                        self.board_2.board[next_move[1]][next_move[0]] == -2)) and \
                        len(self.next_moves) > 0:
                    next_move = self.next_moves.pop(0)
                if self.check_target_inside_borders(next_move[0], next_move[1]) and \
                        self.board_2.board[next_move[1]][next_move[0]] != -1 and \
                        self.board_2.board[next_move[1]][next_move[0]] != -2:
                    self.board_2.board[next_move[1]][next_move[0]] = -1
                    if self.board_2.start_condition[next_move[1]][next_move[0]] == 1:
                        self.next_moves.extend([(next_move[0] + 1, next_move[1]),
                                                (next_move[0] - 1, next_move[1]),
                                                (next_move[0], next_move[1] + 1),
                                                (next_move[0], next_move[1] - 1),
                                                (next_move[0] + 1, next_move[1] + 1),
                                                (next_move[0] - 1, next_move[1] - 1),
                                                (next_move[0] - 1, next_move[1] + 1),
                                                (next_move[0] + 1, next_move[1] - 1)])
                else:
                    self.make_random_shot(change_tactic=True)
            else:
                self.make_random_shot(change_tactic=True)
            self.first_player_turn = True
        for ship in self.board_2.ship_set:
            Drawing.draw_ship(screen, ship, self.board_1.cell_size)
        for ship in self.destroyed_ships:
            Drawing.draw_ship(screen, ship, self.board_1.cell_size)

    def run(self):
        if self.ship_setting_mode == 'manual':
            self.place_ships_manually(self.board_1)
            self.place_ships_manually(self.board_2)
        else:
            self.place_ships_randomly(self.board_1)
            self.place_ships_randomly(self.board_2)
        self.board_1.start_condition = copy.deepcopy(self.board_1.board)
        self.board_2.start_condition = copy.deepcopy(self.board_2.board)
        running = True
        while running:
            screen.fill(WHITE)
            Drawing.draw_board(screen, self.board_1)
            Drawing.draw_text(screen, self.board_1.left_upper_corner[0] + self.board_1.board_size * self.board_1.cell_size / 2,
                              self.board_1.left_upper_corner[1] - 25, 'Player 1')
            Drawing.draw_board(screen, self.board_2)
            Drawing.draw_text(screen, self.board_2.left_upper_corner[0] + self.board_1.board_size * self.board_1.cell_size / 2,
                              self.board_2.left_upper_corner[1] - 25, 'Player 2')
            if self.play_mode == 'weak bot':
                self.play_against_weak_bot()
            if self.play_mode == 'strong bot':
                self.play_against_strong_bot()
            if self.play_mode == '2 players':
                self.play_game_with_2_players()
            self.fill_board_with_crosses(self.board_1)
            self.mark_non_relevant_cells(self.board_1)
            self.fill_board_with_crosses(self.board_2)
            self.mark_non_relevant_cells(self.board_2)
            if self.is_lose(self.board_1.ship_set):
                running = False
                Menu.win_screen('Player 2')
            if self.is_lose(self.board_2.ship_set):
                running = False
                Menu.win_screen('Player 1')

            pygame.display.flip()

import copy

class Board():
    def __init__(self, start_pos, board_size, cell_size):
        self.board_size = board_size
        self.cell_size = cell_size
        self.left_upper_corner = start_pos
        self.right_lower_corner = [start_pos[0] + board_size * cell_size, start_pos[1] + board_size * cell_size]
        self.board = [[0 for _ in range(board_size)] for __ in range(board_size)]
        self.start_condition = copy.deepcopy(self.board)
        self.ship_set = set()
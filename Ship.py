
class Ship():
    def __init__(self, size, location_x, location_y, ship_cell_x, ship_cell_y, horizontal=True):
        self.size = size
        self.location_x = location_x
        self.location_y = location_y
        self.horizontal = horizontal
        self.ship_cell_x = ship_cell_x
        self.ship_cell_y = ship_cell_y
        self.health = self.size[0] * self.size[1]
        self.all_ship_coords = []
        for i in range(size[0]):
            for j in range(size[1]):
                self.all_ship_coords.append((ship_cell_x + (i if horizontal else j), ship_cell_y + (j if horizontal else i)))

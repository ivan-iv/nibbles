class WorldMap():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[None for i in range(height)] for i in range(width)]

    def set_cell(self, x, y, unit):
        self.cells[x][y] = unit

    def get_cell(self, x, y):
        return self.cells[x][y]

    def clean_cell(self, x, y):
        self.cells[x][y] = None

    def __str__(self):
        result = ''

        for y in range(self.height):
            for x in range(self.width):
                unit = self.cells[x][y]
                if unit:
                    symbol = unit.unit_type.value
                else:
                    symbol = 0
                result += '%s ' % symbol
            result += '\n'

        return result


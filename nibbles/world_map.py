class WorldMap():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._cells = [[None for i in range(height)] for i in range(width)]

    def set(self, coord, unit):
        self._cells[coord[0]][coord[1]] = unit

    def set_all(self, coords, unit):
        for c in coords:
            self.set(c, unit)

    def get(self, coord):
        return self._cells[coord[0]][coord[1]]

    def clean(self, coord):
        self._cells[coord[0]][coord[1]] = None

    def clean_all(self, coords):
        for c in coords:
            self.clean(c)

    def __str__(self):
        result = ''

        for y in range(self.height - 1, -1):
            for x in range(self.width):
                unit = self._cells[x][y]
                if unit:
                    symbol = unit.unit_type.value
                else:
                    symbol = 0
                result += '%s ' % symbol
            result += '\n'

        return result

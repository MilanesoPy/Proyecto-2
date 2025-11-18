from Cell import Cell
import random 

class Board:
    def __init__(self, size_x = 6, size_y = 6, mines=6):
        self.size_x = size_x
        self.size_y = size_y
        self.grid = [[Cell() for _ in range(size_x)] for _ in range(size_y)]
        self.mines = mines
        self.visited_dp = set()    # DP: evita repetir expansión
        self.place_mines()
        self.compute_adjacent_counts()

    def valid(self, x, y):
        return 0 <= x < self.size_x and 0 <= y < self.size_y

    def place_mines(self):
        pos_x = random.sample(range(self.size_x), self.mines)
        pos_y = random.sample(range(self.size_y), self.mines)
        for x, y in zip(pos_x, pos_y):
            self.grid[x][y].in_mine = True


    def compute_adjacent_counts(self):
        for x in range(self.size_x):
            for y in range(self.size_y):
                if self.grid[x][y].is_mine:
                    self.grid[x][y].adjacent_mines = -1
                    continue
                count = 0
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if self.valid(nx, ny) and self.grid[nx][ny].is_mine:
                            count += 1
                self.grid[x][y].adjacent_mines = count

    def reveal_cell(self, x, y):
        if not self.valid(x, y):
            print("Coordenada inválida.")
            return False

        cell = self.grid[x][y]

        if cell.is_flagged:
            print("La celda está marcada.")
            return False

        if cell.is_revealed:
            return True

        cell.is_revealed = True

        if cell.is_mine:
            return False

        if cell.adjacent_mines == 0:
            self.flood_fill(x, y)

        return True

    def flood_fill(self, x, y):
        # DP: si ya se expandió antes, no repetir
        if (x, y) in self.visited_dp:
            return
        self.visited_dp.add((x, y))

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if not self.valid(nx, ny):
                    continue
                neighbor = self.grid[nx][ny]
                if not neighbor.is_revealed and not neighbor.is_mine:
                    neighbor.is_revealed = True
                    if neighbor.adjacent_mines == 0:
                        self.flood_fill(nx, ny)  # expansión recursiva

    def print_board(self, show_mines=False):
        print("  y " + " ".join(str(i) for i in range(self.size)))
        print("x  " + "--" * self.size)
        for i in range(self.size):
            row = []
            for j in range(self.size):
                c = self.grid[i][j]
                if show_mines and c.is_mine:
                    row.append("*")
                else:
                    row.append(str(c))
            print(f"{i} | " + " ".join(row))

import random

class Cell:
    def __init__(self):
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

    def __str__(self):
        if not self.is_revealed:
            return "F" if self.is_flagged else "□"
        if self.is_mine:
            return "*"
        return str(self.adjacent_mines) if self.adjacent_mines > 0 else " "


class Board:
    def __init__(self, size=6, mines=6):
        self.size = size
        self.grid = [[Cell() for _ in range(size)] for _ in range(size)]
        self.mines = mines
        self.visited_dp = set()    # DP: evita repetir expansión
        self.place_mines()
        self.compute_adjacent_counts()

    def valid(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size

    def place_mines(self):
        positions = random.sample(range(self.size*self.size), self.mines)
        for pos in positions:
            x = pos // self.size
            y = pos % self.size
            self.grid[x][y].is_mine = True

    def compute_adjacent_counts(self):
        for x in range(self.size):
            for y in range(self.size):
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
        print("   " + " ".join(str(i) for i in range(self.size)))
        print("  " + "--" * self.size)
        for i in range(self.size):
            row = []
            for j in range(self.size):
                c = self.grid[i][j]
                if show_mines and c.is_mine:
                    row.append("*")
                else:
                    row.append(str(c))
            print(f"{i} | " + " ".join(row))


class Game:
    def __init__(self):
        self.board = Board()

    def play(self):
        print("Comandos:")
        print("   r x y   -> revelar")
        print("   f x y   -> marcar bandera")
        print("   q       -> salir")

        while True:
            self.board.print_board()
            cmd = input(">>> ").strip().split()

            if len(cmd) == 0:
                continue

            if cmd[0] == "q":
                print("Juego terminado.")
                break

            if len(cmd) != 3:
                print("Comando inválido.")
                continue

            action, x, y = cmd[0], cmd[1], cmd[2]

            if not (x.isdigit() and y.isdigit()):
                print("Coordenadas inválidas.")
                continue

            x, y = int(x), int(y)

            if action == "f":
                self.board.grid[x][y].is_flagged = not self.board.grid[x][y].is_flagged

            elif action == "r":
                ok = self.board.reveal_cell(x, y)
                if not ok:
                    print("BOOM! Has perdido.")
                    self.board.print_board(show_mines=True)
                    break

            if self.check_win():
                print("¡Ganaste! No quedan celdas seguras.")
                self.board.print_board(show_mines=True)
                break

    def check_win(self):
        for row in self.board.grid:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True


if __name__ == "__main__":
    Game().play()

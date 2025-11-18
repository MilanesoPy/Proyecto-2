from Cell import Cell
from Board import Board

class Game:
    def __init__(self):
        self.board = Board()

    def play(self):
        while True:
            print("Comandos:")
            print("   r x y   -> revelar")
            print("   f x y   -> marcar bandera")
            print("   q       -> salir")
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

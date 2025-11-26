from Cell import Cell
from NewBoard import Board

class Game:
    def __init__(self, size_x = 6, size_y = 6, mines=6):
        self.board = Board(size_x, size_y, mines)

    def play(self):
        while True:

            print("Comandos:")
            print("   r x y   -> revelar")
            print("   m x y   -> marcar bandera")
            print("   s       -> salir")
            self.board.print_board()
            cmd = input(">>> ").strip().split()
            

            if len(cmd) == 0:
                continue
            
            if cmd[0] == "boombastic":
                print("\nUBICACIÓN DE TODAS LAS BOMBAS:")
                self.board.print_board(show_mines=True)
                print("\n--------------------------------------\n")

            if cmd[0] == "s":
                print("Juego terminado.")
                break

            if len(cmd) != 3:
                print("Comando inválido.")
                continue

            action, x, y = cmd[0], cmd[1], cmd[2]

            x, y = int(x), int(y)

            if action == "m":
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
        count = 0
        for row in self.board.grid:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return False
                if cell.is_mine and cell.is_flagged:
                    count += 1
                    if count ==  self.board.mines:
                        return True
        return False



if __name__ == "__main__":
    Game(11, 11, 10).play()# 3. Iniciar el juego
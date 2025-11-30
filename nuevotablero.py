from Cell import Cell
from Board import Board

class Game:
    def __init__(self, size_x = 6, size_y = 6, mines=6):
        self.board = Board(size_x, size_y, mines)

    def play(self) -> None:
        """
        Juega una partida para un jugador humano
        """
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
                continue
                
                

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
                print("¡Ganaste!")
                self.board.print_board(show_mines=True)
                break

    def check_win(self)-> bool:
        """
        Entrega True si el tablero actual cumple la condicion de victoria
        """
        for row in self.board.grid:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True




if __name__ == "__main__":
    jugar = True
    while jugar:
        Ancho = int(input("Ancho del tablero: "))
        Alto = int(input("Alto del tablero: "))
        mines = int(input("Cantidad de bombas: "))

        Game(Ancho, Alto, mines).play()
        respuesta = str(input("Volver a jugar? y/n "))

        if respuesta == "y":
            jugar = True
        else:
            jugar = False


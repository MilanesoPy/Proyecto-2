from Cell import Cell
from NewBoard import Board
import random
import time

class RandomAgent:
    def __init__(self, board: Board, p: float):
        self.board = board
        self.prob = p   # Probabilidad de marcar

    def accion(self):
        """
        Devuelve:
            True  -> la partida continúa
            False -> la partida termina (ganó o perdió)
        """
        # Coordenadas aleatorias válidas
        x = random.randint(0, self.board.size_x - 1)
        y = random.randint(0, self.board.size_y - 1)

        # Marcado de bandera
        if random.random() < self.prob:
            self.board.grid[x][y].is_flagged = not self.board.grid[x][y].is_flagged
            return True, "marca", x, y   # El juego sigue

        # Revelado de celda
        ok = self.board.reveal_cell(x, y)

        return ok ,"revela", x, y

    def jugar(self, show=False):
        while True:
            sigue, jugada, x, y = self.accion()

            if show:
                print(f"{jugada} en {x}, {y}")
                self.board.print_board()
                print("-----------------------------")
                time.sleep(0.3)

            if not sigue:
                # Determinar si ganó o perdió
                if self.check_win():
                    if show:
                        print(f"{jugada} en {x}, {y}")
                        print("¡El agente ganó!")
                        self.board.print_board(show_mines=True)
                    return True 
                else:
                    if show:
                        print(f"{jugada} en {x}, {y}")
                        print("El agente perdió.")
                        self.board.print_board(show_mines=True)
                    return False

    def check_win(self):
        for row in self.board.grid:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True


if __name__ == "__main__":

    #agente = RandomAgent(Board(3, 3, 3), 0.2)
    #agente.jugar(show=True)
    #gana = False
    total = 10000
    wins = 0

    for i in range(total):
        game = Board(6, 6, 4)
        agent = RandomAgent(game, 0.35)

        result = agent.jugar(show=False)  # True si ganó, False si perdió
        if result:
            wins += 1

    print(f"Ganó {wins} de {total} partidas.")
    print(f"Winrate = {wins / total * 100:.2f}%")



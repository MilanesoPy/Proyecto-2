from Cell import Cell
from Board import Board
from Agent import RandomAgent
class Game:
    def __init__(self, size = 6, mines = 6):
        self.board = Board(size, mines)

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

def run_minesweeper_game(size, mines):
    # 1. Inicializar el juego y el agente
    board = Board(size, mines)
    agent = RandomAgent()
    
    game_result = "JUGANDO"
    turns = 0

    print("--- 💣 ¡Comenzando juego de Buscaminas! ---")
    
    # 2. Bucle principal del juego
    while game_result == "JUGANDO":
        
        # A. Mostrar el tablero actual (opcional, para visualización)
        # board.display() 
        
        # B. Obtener el estado del tablero visible para el agente
        # Esta es la 'percepción' del agente (casillas reveladas, no minas)
        board_state = board.get_agent_view() 
        
        # C. El agente calcula la siguiente jugada
        move = agent.get_move(board_state) 
        
        if move is None:
            # Esto puede pasar si el agente no encuentra movimientos válidos
            print("El agente no encontró movimientos válidos. ¡Fin del juego!")
            break
            
        row, col = move
        print(f"\nTurno {turns + 1}: El agente hace clic en ({row}, {col})")
        
        # D. Ejecutar la jugada en el tablero
        # El método 'reveal' debe devolver si el juego continúa, ganó o perdió.
        game_status = board.reveal(row, col)
        
        if game_status == "PERDIDO":
            game_result = "PERDIDO"
            print("❌ ¡El agente explotó una mina! Fin del juego.")
        elif game_status == "GANADO":
            game_result = "GANADO"
            print("🎉 ¡Felicidades! El agente ha ganado el juego.")
        
        turns += 1
        
        # Pequeña pausa opcional si quieres ver el juego más lento
        # import time
        # time.sleep(0.5) 
        
    print(f"\nJuego terminado en {turns} turnos. Resultado: {game_result}")
    # board.display_final_state()


if __name__ == "__main__":
    Game(7, 7).play()# 3. Iniciar el juego
import random

# ... (Clase Agent y otros métodos)

class RandomAgent:
    """
    Agente que toma decisiones completamente al azar para jugar Buscaminas.
    """
    def get_move(self, board_state):
        """
        Calcula y devuelve un movimiento aleatorio válido (fila, columna).
        
        :param board_state: La representación del tablero actual.
                            (Asume que es una lista de listas o similar,
                            donde cada elemento indica si la casilla está revelada,
                            marcada o desconocida).
        :return: Una tupla (row, col) con la coordenada de la casilla a revelar.
        """
        # Obtener las dimensiones del tablero
        rows = len(board_state)
        cols = len(board_state[0]) if rows > 0 else 0
        
        # 1. Encontrar todas las casillas que aún no han sido reveladas ni marcadas.
        valid_moves = []
        for r in range(rows):
            for c in range(cols):
                # Debes adaptar la condición de abajo a la estructura exacta de
                # cómo el 'board_state' representa una casilla oculta/desconocida
                # y una casilla marcada con bandera (flag).
                
                # EJEMPLO DE CONDICIÓN (ADAPTAR SEGÚN TU CÓDIGO):
                # Si board_state[r][c] == 'Desconocido' y NO es una bandera:
                # if board_state[r][c].is_unknown() and not board_state[r][c].is_flag():
                
                # Si en el repositorio usan 0 para oculta y -1 para bandera:
                # ADAPTAR SEGÚN LA ESTRUCTURA DE TU BOARD
                if board_state[r][c] == 0: # 0 podría significar 'oculta' en tu código
                     valid_moves.append((r, c))

        # 2. Elegir un movimiento al azar de la lista
        if not valid_moves:
            # No hay movimientos posibles (el juego terminó o algo está mal)
            return None 

        chosen_move = random.choice(valid_moves)
        
        # 3. Devolver la coordenada (fila, columna)
        return chosen_move
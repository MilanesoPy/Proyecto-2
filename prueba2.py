import numpy as np
import random
from collections import defaultdict
from nuevotablero import *   # Debe contener Game, Board, Cell

# ============================================================
#                ENTORNO BUSCAMINAS (CON BANDERAS)
# ============================================================
class MinesweeperEnv:
    def __init__(self, size_x=6, size_y=6, mines=3):
        self.size_x = size_x
        self.size_y = size_y
        self.mines = mines

        # --------- REWARDS (ajustables) ----------
        self.reward_click_repetido = -20
        self.reward_mina = -200
        self.reward_reveal_seguro = +8
        self.reward_reveal_cero = +20
        self.reward_ganar = +300

        self.reward_flag_correcta = +40
        self.reward_flag_incorrecta = -50
        self.reward_flag_repetida = -15
        # -----------------------------------------

        self.reset()

    def reset(self):
        self.game = Game(self.size_x, self.size_y, self.mines)
        self.board = self.game.board
        return self.get_state()

    def get_state(self):
        """Devuelve el estado observable por el agente como tupla de tuplas."""
        state = []
        for i in range(self.size_x):
            row = []
            for j in range(self.size_y):
                c = self.board.grid[i][j]
                if c.is_flagged:
                    row.append(-3)      # bandera
                elif not c.is_revealed:
                    row.append(-2)      # oculta
                elif c.is_mine:
                    row.append(-1)      # mina visible (solo si se mostró)
                else:
                    row.append(c.adjacent_mines)  # 0..8
            state.append(tuple(row))
        return tuple(state)

    def step(self, action):
        """
        acción: ("reveal", x, y) o ("flag", x, y)
        retorna: next_state, reward, done, info
        """
        tipo, x, y = action
        # validación básica de coordenadas
        if not (0 <= x < self.size_x and 0 <= y < self.size_y):
            return self.get_state(), -10.0, False, {"invalid": True}

        c = self.board.grid[x][y]

        # ----------------- FLAG (alternar) -----------------
        if tipo == "flag":
            # si ya revelada, penalizar intento de marcar
            if c.is_revealed:
                return self.get_state(), self.reward_flag_repetida, False, {}

            # alternar bandera
            if c.is_flagged:
                # quitar bandera (pequeña penalización)
                c.is_flagged = False
                return self.get_state(), -5.0, False, {}
            else:
                c.is_flagged = True
                if c.is_mine:
                    reward = self.reward_flag_correcta
                else:
                    reward = self.reward_flag_incorrecta

                done = self.game.check_win()
                if done:
                    reward += self.reward_ganar
                return self.get_state(), reward, done, {}

        # ----------------- REVEAL -----------------
        if tipo == "reveal":
            # si ya revelada, penaliza
            if c.is_revealed:
                return self.get_state(), self.reward_click_repetido, False, {}

            ok = self.board.reveal_cell(x, y)

            # pisó mina -> perdió
            if not ok:
                # revelar el tablero ya hecho por reveal_cell
                return self.get_state(), self.reward_mina, True, {}

            # reward por revelar
            if c.adjacent_mines == 0:
                reward = self.reward_reveal_cero
            else:
                reward = self.reward_reveal_seguro

            done = self.game.check_win()
            if done:
                reward += self.reward_ganar

            return self.get_state(), reward, done, {}

        # acción desconocida
        return self.get_state(), -10.0, False, {"invalid_type": True}


# ============================================================
#                UTILIDADES DE ACCIONES Y Q-LEARNING
# ============================================================

def all_actions(env):
    """
    Genera acciones válidas en el estado actual:
    - ("reveal", x, y) para celdas no reveladas
    - ("flag", x, y) para celdas no reveladas
    Esto reduce el espacio de acciones ignorando acciones obvias inválidas.
    """
    acts = []
    for x in range(env.size_x):
        for y in range(env.size_y):
            c = env.board.grid[x][y]
            if not c.is_revealed:
                acts.append(("reveal", x, y))
                acts.append(("flag", x, y))
    # si por alguna razón no hay acciones (no debería), devolver alguna válida
    if not acts:
        acts.append(("reveal", 0, 0))
    return acts


# ============================================================
#               POLÍTICA Y ACTUALIZACIÓN Q
# ============================================================
def choose_action(state, env, epsilon):
    acts = all_actions(env)
    if random.random() < epsilon:
        return random.choice(acts)
    # greedy
    best_a = None
    best_q = float("-inf")
    for a in acts:
        q = Q[(state, a)]
        if q > best_q:
            best_q = q
            best_a = a
    return best_a

def update_q(state, action, reward, next_state, env):
    next_acts = all_actions(env)
    best_next_q = max(Q[(next_state, a)] for a in next_acts)
    Q[(state, action)] += alpha * (reward + gamma * best_next_q - Q[(state, action)])


# ============================================================
#                     ENTRENAMIENTO
# ============================================================
def train_q_learning(env):
    global epsilon
    for episode in range(EPISODES):
        state = env.reset()
        done = False
        steps = 0

        # actualizar epsilon (exponencial) al inicio de cada episodio
        epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-epsilon_decay_rate * episode)

        while not done and steps < MAX_STEPS:
            action = choose_action(state, env, epsilon)
            next_state, reward, done, info = env.step(action)
            update_q(state, action, reward, next_state, env)
            state = next_state
            steps += 1

        if (episode + 1) % 200 == 0 or episode == 0:
            print(f"Episodio {episode+1}/{EPISODES}  epsilon={epsilon:.4f}")

    print("Entrenamiento finalizado.")


# ============================================================
#               FUNCIONES DE EVALUACIÓN / VISUALIZACIÓN
# ============================================================
def watch_agent(env, Q, max_steps=200):
    """Juega una partida imprimiendo el tablero paso a paso (greedy)."""
    state = env.reset()
    done = False
    steps = 0

    print("Estado inicial:")
    env.board.print_board()
    print()

    while not done and steps < max_steps:
        # elegir acción greedy (sin exploración)
        best_action = None
        best_q = float("-inf")
        for a in all_actions(env):
            q = Q[(state, a)]
            if q > best_q:
                best_q = q
                best_action = a

        print(f"Paso {steps}: Agente juega: {best_action} (Q={best_q:.3f})")
        state, reward, done, info = env.step(best_action)
        env.board.print_board()
        print()
        steps += 1

    print("Juego terminado. Recompensa final:", reward)
    print("\nTablero con minas reveladas:")
    env.board.print_board(show_mines=True)


def test_agent(env, Q, n=200, max_steps=200, verbose=False):
    """
    Ejecuta n partidas greedy y devuelve el % de victorias.
    Si verbose=True imprime estadísticas parciales.
    """
    wins = 0
    total_steps = 0
    for i in range(n):
        state = env.reset()
        done = False
        steps = 0

        while not done and steps < max_steps:
            # greedy
            best_action = None
            best_q = float("-inf")
            for a in all_actions(env):
                q = Q[(state, a)]
                if q > best_q:
                    best_q = q
                    best_action = a

            state, reward, done, info = env.step(best_action)
            steps += 1

        total_steps += steps
        if env.game.check_win():
            wins += 1
        if verbose and (i+1) % max(1, n//10) == 0:
            print(f"Progreso: {i+1}/{n}, wins so far: {wins}")

    win_rate = wins / n * 100.0
    avg_steps = total_steps / n
    print(f"Resultados sobre {n} episodios: victorias={wins}, win_rate={win_rate:.2f}%, pasos_promedio={avg_steps:.1f}")
    return win_rate



# ============================================================
#                      PARÁMETROS
# ============================================================
Q = defaultdict(float)

alpha = 0.2         # tasa de aprendizaje
gamma = 1        # factor de descuento

# epsilon decay params
max_epsilon = 1.0
min_epsilon = 0.05
epsilon_decay_rate = 0.00001  # ajustar según velocidad de decaimiento deseada
epsilon = max_epsilon

EPISODES = 8000 * 40 # 10 minutos 8000 * 40 
MAX_STEPS = 16     # límite por episodio para evitar loops


# ============================================================
#                            MAIN
# ============================================================
if __name__ == "__main__":
    # Ajustes para tu caso: tablero 6x6 con 3 minas
    env = MinesweeperEnv(size_x=6, size_y=6, mines=5)

    # Entrenar
    train_q_learning(env)

    # Evaluar: cuántas partidas gana el agente greedy tras entrenar
    print("\nEvaluando agente tras entrenamiento...")
    win_rate = test_agent(env, Q, n=500, max_steps=50, verbose=True)

    # Mostrar una partida paso a paso
    #print("\nVer una partida jugada por el agente (greedy):")
    #watch_agent(env, Q, max_steps=6)

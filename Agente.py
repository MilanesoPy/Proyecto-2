import numpy as np
from nuevotablero import *
import random
from collections import defaultdict

# ============================================================
#               ENTORNO BUSCAMINAS CON BANDERAS
# ============================================================

class MinesweeperEnv:
    def __init__(self, size_x=6, size_y=6, mines=6):
        self.size_x = size_x
        self.size_y = size_y
        self.mines = mines

        # Rewards configurables
        self.reward_click_repetido = -20
        self.reward_mina = -50
        self.reward_reveal_seguro = 40
        self.reward_reveal_cero = 10
        self.reward_ganar = 70

        self.reward_flag_correcta = 40
        self.reward_flag_incorrecta = -20
        self.reward_flag_repetida = -15

        self.reset()

    def reset(self):
        self.game = Game(self.size_x, self.size_y, self.mines)
        self.board = self.game.board
        return self.get_state()

    def get_state(self):
        state = []
        for i in range(self.size_x):
            row = []
            for j in range(self.size_y):
                c = self.board.grid[i][j]
                if not c.is_revealed and not c.is_flagged:
                    row.append(-2)
                elif c.is_flagged:
                    row.append(-3)
                elif c.is_mine:
                    row.append(-1)
                else:
                    row.append(c.adjacent_mines)
            row = tuple(row)
            state.append(row)
        return tuple(state)

    def step(self, action):
        tipo, x, y = action

        # ======================
        #      ACCIÓN FLAG
        # ======================
        if tipo == "flag":
            c = self.board.grid[x][y]

            if c.is_flagged:
                return self.get_state(), self.reward_flag_repetida, False, {}

            c.is_flagged = True

            if c.is_mine:
                reward = self.reward_flag_correcta
            else:
                reward = self.reward_flag_incorrecta

            done = self.game.check_win()
            if done:
                print("gano?")
                reward += self.reward_ganar

            return self.get_state(), reward, done, {}

        # ======================
        #    ACCIÓN REVEAL
        # ======================
        if tipo == "reveal":

            if self.board.grid[x][y].is_revealed:
                return self.get_state(), self.reward_click_repetido, False, {}

            ok = self.board.reveal_cell(x, y)

            if not ok:
                return self.get_state(), self.reward_mina, True, {}

            c = self.board.grid[x][y]
            reward = self.reward_reveal_cero if c.adjacent_mines == 0 else self.reward_reveal_seguro

            done = self.game.check_win()
            if done:
                reward += self.reward_ganar

            return self.get_state(), reward, done, {}

        raise ValueError("Acción desconocida:", action)


# ============================================================
#                Q-LEARNING PARA BUSCAMINAS
# ============================================================

def all_actions(env):
    acciones = []
    for x in range(env.size_x):
        for y in range(env.size_y):
            acciones.append(("reveal", x, y))
            acciones.append(("flag", x, y))
    return acciones


def choose_action(state, env, epsilon):
    acciones = all_actions(env)

    if random.random() < epsilon:
        return random.choice(acciones)

    best_a = None
    best_q = float("-inf")

    for a in acciones:
        q = Q[(state, a)]
        if q > best_q:
            best_q = q
            best_a = a

    return best_a


def update_q(state, action, reward, next_state, env):
    best_next_q = max(Q[(next_state, a)] for a in all_actions(env))

    Q[(state, action)] += alpha * (
        reward + gamma * best_next_q - Q[(state, action)]
    )


# ============================================================
#     ENTRENAMIENTO CON EPSILON DECAY EXPONENCIAL
# ============================================================

def train_q_learning(env):
    global epsilon

    for episode in range(EPISODES):

        # ---- EPSILON DECAY EXPONENCIAL ----
        epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-epsilon_decay_rate * episode)

        state = env.reset()
        done = False
        steps = 0

        while not done and steps < MAX_STEPS:
            action = choose_action(state, env, epsilon)
            next_state, reward, done, info = env.step(action)
            update_q(state, action, reward, next_state, env)

            state = next_state
            steps += 1

        if (episode + 1) % 200 == 0:
            print(f"Episodio {episode+1}/{EPISODES}   epsilon={epsilon:.4f}")

    print("Entrenamiento finalizado.")


# ============================================================
#                VER JUGAR AL AGENTE
# ============================================================

def watch_agent(env, Q, max_steps=15):
    state = env.reset()
    done = False
    steps = 0

    print("Estado inicial:")
    env.board.print_board()
    print()

    while not done and steps < max_steps:
        best_action = None
        best_q = float("-inf")

        for a in all_actions(env):
            q = Q[(state, a)]
            if q > best_q:
                best_q = q
                best_action = a

        print(f"Agente juega: {best_action}  (Q={best_q:.3f})")

        next_state, reward, done, info = env.step(best_action)
        env.board.print_board()
        print()

        state = next_state
        steps += 1

    print("Juego terminado. Recompensa final:", reward)
    print("\nTablero con minas reveladas:")
    env.board.print_board(show_mines=True)

def test_agent(env, Q, n=100, max_steps=8):
    wins = 0

    for _ in range(n):
        state = env.reset()
        done = False
        steps = 0

        while not done and steps < max_steps:
            # Selección greedy (misma que en watch_agent)
            best_action = None
            best_q = float("-inf")

            for a in all_actions(env):
                q = Q[(state, a)]
                if q > best_q:
                    best_q = q
                    best_action = a

            next_state, reward, done, info = env.step(best_action)
            state = next_state
            steps += 1

        # Si la recompensa incluye recompensa por ganar
        if env.game.check_win():
            wins += 1

    win_rate = wins / n * 100
    print(f"Victorias: {wins}/{n}  ({win_rate:.2f}%)")
    return win_rate

# ============================================================
#                   ENTRENAR Y VER JUEGO
# ============================================================

Q = defaultdict(float)

alpha = 0.7
gamma = 1

# ---- parámetros de epsilon decay ----
max_epsilon = 1.0
min_epsilon = 0.05
epsilon_decay_rate = 0.001
epsilon = max_epsilon

EPISODES = 20000
MAX_STEPS = 10

env = MinesweeperEnv(size_x=3, size_y=3, mines=1)
train_q_learning(env)
watch_agent(env, Q, max_steps=8)
test_agent(env, Q, n=4000, max_steps=25)


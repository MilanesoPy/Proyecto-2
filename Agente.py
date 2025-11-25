import numpy as np
from nuevotablero import *
import random
from collections import defaultdict

# ============================================================
#               ENTORNO BUSCAMINAS
# ============================================================

class MinesweeperEnv:
    def __init__(self, size_x=6, size_y=6, mines=6):
        self.size_x = size_x
        self.size_y = size_y
        self.mines = mines
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
            state.append(tuple(row))
        return tuple(state)

    def step(self, action):
        x, y = action
        reward = 0

        if self.board.grid[x][y].is_revealed:
            return self.get_state(), -1, False, {}

        ok = self.board.reveal_cell(x, y)

        if not ok:
            return self.get_state(), -50, True, {}

        c = self.board.grid[x][y]
        reward = 3 if c.adjacent_mines == 0 else 1

        done = self.game.check_win()
        if done:
            reward = 100

        return self.get_state(), reward, done, {}


# ============================================================
#                Q-LEARNING PARA BUSCAMINAS
# ============================================================


def choose_action(state, env):
    if random.random() < epsilon:
        return (random.randint(0, env.size_x - 1),
                random.randint(0, env.size_y - 1))

    best_a = None
    best_q = float("-inf")

    for x in range(env.size_x):
        for y in range(env.size_y):
            q = Q[(state, (x, y))]
            if q > best_q:
                best_q = q
                best_a = (x, y)

    return best_a


def update_q(state, action, reward, next_state, env):
    best_next_q = float("-inf")

    for x in range(env.size_x):
        for y in range(env.size_y):
            best_next_q = max(best_next_q, Q[(next_state, (x, y))])

    Q[(state, action)] += alpha * (reward + gamma * best_next_q - Q[(state, action)])


def train_q_learning(env):
    for episode in range(EPISODES):
        state = env.reset()
        done = False
        steps = 0

        while not done and steps < MAX_STEPS:
            action = choose_action(state, env)
            next_state, reward, done, info = env.step(action)
            update_q(state, action, reward, next_state, env)

            state = next_state
            steps += 1

        if (episode + 1) % 200 == 0:
            print(f"Episodio {episode+1}/{EPISODES} completado")

    print("Entrenamiento finalizado.")


# ============================================================
#                VER JUGAR AL AGENTE
# ============================================================

def watch_agent(env, Q, max_steps=8):
    state = env.reset()
    done = False
    steps = 0

    print("Estado inicial:")
    if hasattr(env.board, "print_board"):
        env.board.print_board()
    print()

    while not done and steps < max_steps:
        best_action = None
        best_q = float("-inf")

        # Buscar acción con mayor Q
        for x in range(env.size_x):
            for y in range(env.size_y):
                q = Q[(state, (x, y))]
                if q > best_q:
                    best_q = q
                    best_action = (x, y)

        print(f"Agente juega: {best_action} (Q={best_q:.3f})")

        # Ejecutar acción
        next_state, reward, done, info = env.step(best_action)

        # Mostrar tablero actualizado
        if hasattr(env.board, "print_board"):
            env.board.print_board()
        print()

        state = next_state
        steps += 1

    print("Juego terminado. Recompensa final:", reward)
    print("\nTablero con minas reveladas:")
    if hasattr(env.board, "print_board"):
        env.board.print_board(show_mines=True)


Q = defaultdict(float)

alpha = 0.3
gamma = 0.99
epsilon = 0.4
EPISODES = 10000
MAX_STEPS = 50

# ============================================================
#                   ENTRENAR Y VER JUEGO
# ============================================================

env = MinesweeperEnv()
train_q_learning(env)
watch_agent(env, Q)

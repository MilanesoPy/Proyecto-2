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
            row = tuple(row)
            state.append(row)
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
#                Q-LEARNING
# ============================================================

Q = defaultdict(float)
alpha = 0.1
gamma = 0.99
epsilon = 0.1

EPISODES = 2000
MAX_STEPS = 200


def choose_action(state, env):
    if random.random() < epsilon:
        return (random.randint(0, env.size_x-1),
                random.randint(0, env.size_y-1))

    best = None
    best_q = float("-inf")
    for x in range(env.size_x):
        for y in range(env.size_y):
            q = Q[(state, (x, y))]
            if q > best_q:
                best = (x, y)
                best_q = q
    return best


def update_q(state, action, reward, next_state, env):
    best_next = float("-inf")
    for x in range(env.size_x):
        for y in range(env.size_y):
            best_next = max(best_next, Q[(next_state, (x, y))])

    Q[(state, action)] += alpha * (reward + gamma * best_next - Q[(state, action)])


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
#              VER LO QUE APRENDIÓ (TOP ACCIONES)
# ============================================================

def ver_lo_que_aprendio(env, k=10):
    state = env.reset()  # estado inicial
    acciones = []

    for x in range(env.size_x):
        for y in range(env.size_y):
            acciones.append(((x, y), Q[(state, (x, y))]))

    acciones.sort(key=lambda x: x[1], reverse=True)

    print(f"Mejores {k} acciones aprendidas desde el estado inicial:")
    for a in acciones[:k]:
        print(a)


# ============================================================
#                  ENTRENAR Y VER RESULTADOS
# ============================================================

env = MinesweeperEnv()
train_q_learning(env)
ver_lo_que_aprendio(env)
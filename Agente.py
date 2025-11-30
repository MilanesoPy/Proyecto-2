import numpy as np 
from nuevotablero import *
import random
from collections import defaultdict 

class AgenteQ:

    #  hiperparametros de entrenamiento
    alpha = 0.7
    gamma = 0.75

    max_epsilon = 1.0
    min_epsilon = 0.1
    epsilon_decay_rate = 0.001
    epsilon = max_epsilon 

    EPISODES = 20000
    MAX_STEPS = 20

    def __init__(self, size_x: int =6 , size_y: int=6, mines: int = 6 ):
        self.size_x = size_x
        self.size_y = size_y
        self.mines = mines

        self.game = Game(self.size_x, self.size_y, self.mines)
        self.board = self.game.board

        self.Q_table = defaultdict(float)

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

    def reset(self) -> tuple:
        self.game = Game(self.size_x, self.size_y, self.mines)
        self.board = self.game.board
        return self.get_state()

    def get_state(self) -> tuple:
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

    def step(self, action: tuple) -> tuple:
        tipo, x, y = action

        # Acción bandera
        if tipo == "flag":
            c = self.board.grid[x][y]

            if c.is_flagged:
                return self.get_state(), self.reward_flag_repetida, False, {}

            c.is_flagged = True

            reward = self.reward_flag_correcta if c.is_mine else self.reward_flag_incorrecta

            done = self.game.check_win()
            if done:
                reward += self.reward_ganar

            return self.get_state(), reward, done, {}

        # Acción revelar
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


def all_actions(env: AgenteQ) -> list:
    """
    Entraga una lista de todas las acciones posibles de un tablero que puede tomar un agente
    """
    acciones = []
    for x in range(env.size_x):
        for y in range(env.size_y):
            acciones.append(("reveal", x, y))
            acciones.append(("flag", x, y))
    return acciones


def choose_action(state, env: AgenteQ, epsilon: float, Q: dict) -> tuple:
    """
    Elige que accion tomar de una tabla del AgenteQ
    """
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


def update_q(state: list, action: tuple, reward: float, next_state: list, env: AgenteQ, Q: dict) -> None:
    """
    Actualiza la tabla de un AgenteQ
    """
    best_next_q = max(Q[(next_state, a)] for a in all_actions(env))

    Q[(state, action)] += env.alpha * (
        reward + env.gamma * best_next_q - Q[(state, action)]
    )


def train_q_learning(env: AgenteQ, Q: dict, print_each: int =1000) -> None:
    """
    Entrena a un AgenteQ
    """
    for episode in range(env.EPISODES):

        # Epsilon decay
        env.epsilon = env.min_epsilon + (env.max_epsilon - env.min_epsilon) * np.exp(
            -env.epsilon_decay_rate * episode
        )

        state = env.reset()
        done = False
        steps = 0

        while not done and steps < env.MAX_STEPS:
            action = choose_action(state, env, env.epsilon, Q)
            next_state, reward, done, info = env.step(action)
            update_q(state, action, reward, next_state, env, Q)

            state = next_state
            steps += 1

        if (episode + 1) % print_each == 0:
            print(f"Episodio {episode+1}/{env.EPISODES}   epsilon={env.epsilon:.4f}")

    print("Entrenamiento finalizado.")


def watch_agent(env: AgenteQ, Q: dict, max_steps: int=15) -> None:
    """
    Muestra en terminal las jugadas de un AgenteQ
    """
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


def test_agent(env: AgenteQ, Q: dict, n: int =100, max_steps: int=8) -> float:
    """
    Entraga el porcentaje de victoria de un AgenteQ
    """
    wins = 0

    for _ in range(n):
        state = env.reset()
        done = False
        steps = 0

        while not done and steps < max_steps:
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

        if env.game.check_win():
            wins += 1

    win_rate = wins / n * 100
    print(f"Victorias: {wins}/{n}  ({win_rate:.2f}%)")
    return win_rate



if __name__ == "__main__":

    win_rates = []

    for _ in range(10):
        env = AgenteQ(size_x=4, size_y=4, mines=2)
        train_q_learning(env, env.Q_table, print_each=25000)
        win_rates.append(test_agent(env, env.Q_table, n=10000, max_steps=20))

    print(f"Media de winrate: {np.mean(win_rates)}")
    print(f"Desviación estándar: {np.std(win_rates)}")

    print(
        f"Parámetros: alpha={env.alpha}, gamma={env.gamma}, "
        f"eps=[{env.max_epsilon}, {env.min_epsilon}, decay={env.epsilon_decay_rate}]"
    )

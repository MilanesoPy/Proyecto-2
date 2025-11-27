from nuevotablero import *
from Agente import *
from RandomAgente import *

if __name__ == "__main__":
    Game(5, 5, 3).play()
    RandomAgent(Board(5, 5, 3), 0.35).jugar(show=True)

    env = MinesweeperEnv(size_x=5, size_y=5, mines=3)
    train_q_learning(env,env.Q_table ,print_each=25000)
    watch_agent(env, env.Q_table, max_steps=8)

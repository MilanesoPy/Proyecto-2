from nuevotablero import *
from Agente import *
from RandomAgente import *

if __name__ == "__main__":
    Game(4, 4, 2).play()
    RandomAgent(Board(4, 4, 2), 0.35).jugar(show=True)

    env = AgenteQ(size_x=4, size_y=4, mines=2)
    train_q_learning(env,env.Q_table ,print_each=25000)
    watch_agent(env, env.Q_table, max_steps=8)
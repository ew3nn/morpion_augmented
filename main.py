from env import *
import torch
from agent import * 
from nn import *
import random

# state_vector = [0] * 9 
# env = Env(state_vector)
# boucle(20, env)

# HYPERPARAMETERS
learning_rate = 0.01
epsilon = 0.99
epsilon_decay = 0.05
epoch = 200

def choose_action(state, epsilon, network, env):
    prob = random.random()
    if prob < epsilon :
        action = choose_hasard(env)
        return action
    else :
        state_tens = torch.tensor(state, dtype=torch.float32)
        q_values = network(state_tens)
        masked = mask(q_values, state)
        action = torch.argmax(masked).item()
        return action 


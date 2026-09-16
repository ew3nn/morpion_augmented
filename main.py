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




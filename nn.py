import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from env import legal_moves

device = torch.device(
    "cuda" if torch.cuda.is_available() else
    "cpu"
)

class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(9, 16),
            nn.ReLU(),
            nn.Linear(16, 32),
            nn.ReLU(),
            nn.Linear(32, 9)
        )

    def forward(self, x):
        q_values = self.linear_relu_stack(x)
        return q_values


def mask(q_values, state_vector):
    masked = q_values.clone()
    legal_move_list = legal_moves(state_vector)
    for i in range(len(state_vector)):
        if i not in legal_move_list:
            masked[i] = -float("inf")
    return masked



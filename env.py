def legal_moves(state):
    legal_move = []
    for i in range(len(state)):
        if state[i] == 0:
            legal_move.append(i)
    return legal_move


class Env:
    def __init__(self, state_vector):
        self.state_vector = state_vector

    def legal_moves(self, state=None):
        if state is None:
            state = self.state_vector
        legal_move = []
        for i in range(len(state)):
            if state[i] == 0:
                legal_move.append(i)
        return legal_move

    def victory(self, state=None):
        if state is None:
            state = self.state_vector
        victoire = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for a, b, c in victoire:
            if state[a] == state[b] == state[c] and state[a] != 0:
                return state[a]
        return 0

    def is_terminal(self, state=None):
        if state is None:
            state = self.state_vector
        winner = self.victory(state)
        if winner != 0:
            return True, winner
        if len(self.legal_moves(state)) == 0:
            return True, 0
        return False, 0

    def step(self, action, player, state=None):
        if state is None:
            state = self.state_vector
        reward = 0
        done = False
        moves = self.legal_moves(state)
        if action in moves:
            future_state = state.copy()
            future_state[action] = player
            fin, winner = self.is_terminal(future_state)
            if fin:
                done = True
                if winner != 0:
                    reward += 1
                return future_state, reward, done
            return future_state, reward, done
        return state, reward, done

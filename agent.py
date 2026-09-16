import random

def minimax(player, env, state=None):
    if state is None:
        state = env.state_vector

    fin, winner = env.is_terminal(state)
    if fin:
        return winner * player

    best_value = -float("inf")
    for i in env.legal_moves(state):
        next_state, reward, done = env.step(i, player, state)
        value = -minimax(-player, env, next_state)
        if value > best_value:
            best_value = value

    return best_value


def best_move(player, env):
    best_value = -float("inf")
    chosen_action = None

    for i in env.legal_moves():
        next_state, reward, done = env.step(i, player)
        value = -minimax(-player, env, next_state)

        if value > best_value:
            best_value = value
            chosen_action = i

    return chosen_action


def choose_hasard(env):
    action = env.legal_moves()
    number = random.choice(action)
    return number


def boucle(epoch, env):
    victoire = []
    score = {-1: 0, 1: 0, 0: 0}
    for i in range(epoch):
        fin = False
        player = random.choice([-1, 1])
        env.state_vector = [0] * 9

        while not fin:
            if player == -1:
                next_state, reward, fin = env.step(choose_hasard(env), player)
            else:
                next_state, reward, fin = env.step(best_move(player, env), player)
            env.state_vector = next_state
            player = -player

        _, winner = env.is_terminal()
        score[winner] += 1
        victoire.append(winner)
        print(f"Victoire de {winner} à l'épisode {i}")

    print(f"Voici le score de fin de partie {score} cela fait {score[1]/epoch*100}% gagné par le joueur 1")
    return victoire

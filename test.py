"""
Test manuel de choose_action.
A adapter aux noms exacts de tes imports (network.py, agent.py, env.py...).
"""

import torch
from env import Env
from agent import choose_action, choose_hasard  # adapte selon l'organisation de tes fichiers
from nn import NeuralNetwork 

# --- Etat de depart : plateau a moitie rempli, quelques cases libres ---
# 0 = case libre, on doit donc pouvoir jouer sur les index 1, 3, 4, 5, 8
state = [1, 0, -1, 0, 0, 0, -1, 1, 0]
env = Env(state)

network = NeuralNetwork()  # reseau non entraine, poids aleatoires : suffisant pour ce test
legal = env.legal_moves(state)
print(f"Coups legaux attendus : {legal}\n")

# --- Test 1 : epsilon = 1.0 -> doit TOUJOURS explorer (choix aleatoire) ---
print("=== Test exploration (epsilon = 1.0) ===")
for _ in range(10):
    action = choose_action(state, 1.0, network, env)
    ok = action in legal
    print(f"action = {action}  ->  {'OK' if ok else 'INVALIDE !!'}")
    assert ok, f"Action illegale en exploration : {action}"

# --- Test 2 : epsilon = 0.0 -> doit TOUJOURS exploiter (argmax du reseau masque) ---
print("\n=== Test exploitation (epsilon = 0.0) ===")
actions_vues = set()
for _ in range(10):
    action = choose_action(state, 0.0, network, env)
    ok = action in legal
    actions_vues.add(action)
    print(f"action = {action}  ->  {'OK' if ok else 'INVALIDE !!'}")
    assert ok, f"Action illegale en exploitation : {action}"

# Avec un reseau non entraine et un state fixe, l'argmax doit renvoyer
# TOUJOURS la meme action (le reseau est deterministe sans dropout/etc.)
print(f"\nActions distinctes vues en exploitation : {actions_vues}")
assert len(actions_vues) == 1, "L'exploitation devrait toujours choisir la meme action sur un state fixe !"

# --- Test 3 : le type renvoye doit etre un int Python, pas un tenseur ---
action_explore = choose_action(state, 1.0, network, env)
action_exploit = choose_action(state, 0.0, network, env)
print(f"\nType action (exploration) : {type(action_explore)}")
print(f"Type action (exploitation) : {type(action_exploit)}")
assert isinstance(action_explore, int), "choose_hasard doit renvoyer un int"
assert isinstance(action_exploit, int), "la branche exploitation doit renvoyer un int (verifie le .item())"

print("\nTous les tests sont passes.")

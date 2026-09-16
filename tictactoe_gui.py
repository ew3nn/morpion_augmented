"""
tictactoe_gui.py

Interface graphique minimale pour un morpion, pensee pour etre pilotee
par une logique de jeu / des agents externes (RL, minimax, humain...).
Ce fichier ne contient AUCUNE logique de jeu (regles, victoire, IA) :
seulement l'affichage et la remontee des clics.

Convention d'etat : liste de 9 entiers dans {-1, 0, 1}
    1  -> joueur A (dessine avec un rond)
   -1  -> joueur B (dessine avec une croix)
    0  -> case vide
Ce format colle directement a ce qu'un reseau de neurones attend en entree,
pas besoin de convertir entre "X"/"O" et des valeurs numeriques.

Usage typique :

    from tictactoe_gui import TicTacToeGUI

    def on_human_click(cell_index):
        ...  # appele quand l'humain clique sur une case

    gui = TicTacToeGUI(on_cell_click=on_human_click)
    gui.update_board([0]*9)
    gui.set_status("Au tour de 1")
    gui.run()  # bloquant, lance la boucle tkinter

Pour faire jouer des agents automatiquement (sans clic humain), utiliser
gui.after(delay_ms, callback) pour enchainer les coups : voir la demo
tout en bas du fichier (deux joueurs aleatoires qui s'affrontent).
"""

import tkinter as tk
from typing import Callable, List, Optional

Cell = int  # -1, 0 ou 1


class TicTacToeGUI:
    def __init__(
        self,
        on_cell_click: Optional[Callable[[int], None]] = None,
        on_reset: Optional[Callable[[], None]] = None,
        cell_size: int = 120,
        title: str = "Morpion",
    ):
        self.on_cell_click = on_cell_click
        self.on_reset = on_reset
        self.cell_size = cell_size
        board_px = cell_size * 3

        self.root = tk.Tk()
        self.root.title(title)
        self.root.resizable(False, False)

        self.status_var = tk.StringVar(value="")
        tk.Label(self.root, textvariable=self.status_var, font=("Helvetica", 14)).pack(pady=(10, 0))

        self.canvas = tk.Canvas(self.root, width=board_px, height=board_px, bg="white", highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)
        self.canvas.bind("<Button-1>", self._handle_click)

        tk.Button(self.root, text="Nouvelle partie", command=self._handle_reset).pack(pady=(0, 10))

        self._draw_grid()
        self._board_state: List[Cell] = [0] * 9

    # ---------- API publique ----------

    def update_board(self, state: List[Cell]) -> None:
        """state : liste de 9 entiers parmi -1, 0, 1 (0 = case vide)."""
        self._board_state = list(state)
        self.canvas.delete("mark")
        for index, value in enumerate(self._board_state):
            if value != 0:
                self._draw_mark(index, value)

    def set_status(self, text: str) -> None:
        self.status_var.set(text)

    def after(self, delay_ms: int, callback: Callable) -> None:
        """Planifie un appel differe (utile pour enchainer des coups d'agents)."""
        self.root.after(delay_ms, callback)

    def run(self) -> None:
        self.root.mainloop()

    def close(self) -> None:
        self.root.destroy()

    # ---------- interne ----------

    def _draw_grid(self) -> None:
        size = self.cell_size
        for i in (1, 2):
            self.canvas.create_line(i * size, 0, i * size, 3 * size, width=2)
            self.canvas.create_line(0, i * size, 3 * size, i * size, width=2)

    def _draw_mark(self, index: int, value: Cell) -> None:
        size = self.cell_size
        row, col = divmod(index, 3)
        x0, y0 = col * size, row * size
        pad = size * 0.2
        if value == 1:
            self.canvas.create_oval(x0 + pad, y0 + pad, x0 + size - pad, y0 + size - pad,
                                     width=4, outline="#3468c0", tags="mark")
        elif value == -1:
            self.canvas.create_line(x0 + pad, y0 + pad, x0 + size - pad, y0 + size - pad,
                                     width=4, fill="#d64545", tags="mark")
            self.canvas.create_line(x0 + size - pad, y0 + pad, x0 + pad, y0 + size - pad,
                                     width=4, fill="#d64545", tags="mark")

    def _handle_click(self, event: tk.Event) -> None:
        if self.on_cell_click is None:
            return
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if 0 <= row < 3 and 0 <= col < 3:
            index = row * 3 + col
            if self._board_state[index] == 0:
                self.on_cell_click(index)

    def _handle_reset(self) -> None:
        if self.on_reset is not None:
            self.on_reset()


# --------------------------------------------------------------------------
# Demo autonome : deux joueurs ALEATOIRES s'affrontent automatiquement.
# Ceci sert uniquement a montrer comment brancher la GUI sur une logique
# de jeu externe -- ce n'est pas l'agent RL que tu vas developper.
# --------------------------------------------------------------------------

def _demo_self_play() -> None:
    import random

    state: List[Cell] = [0] * 9
    players = [1, -1]
    turn = 0

    def check_winner(s: List[Cell]) -> Optional[int]:
        lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
                 (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
        for a, b, c in lines:
            if s[a] != 0 and s[a] == s[b] == s[c]:
                return s[a]
        return None

    gui = TicTacToeGUI(on_cell_click=None, title="Demo - self-play aleatoire")

    def play_next() -> None:
        nonlocal turn
        winner = check_winner(state)
        if winner is not None:
            gui.set_status(f"Le joueur {winner} gagne !")
            return
        if all(v != 0 for v in state):
            gui.set_status("Match nul.")
            return

        player = players[turn % 2]
        free_cells = [i for i, v in enumerate(state) if v == 0]
        move = random.choice(free_cells)
        state[move] = player
        gui.update_board(state)
        gui.set_status(f"Au tour du joueur {players[(turn + 1) % 2]}")
        turn += 1
        gui.after(500, play_next)

    gui.set_status(f"Au tour du joueur {players[0]}")
    gui.after(500, play_next)
    gui.run()


if __name__ == "__main__":
    _demo_self_play()

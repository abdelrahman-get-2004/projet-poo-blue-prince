# fichier: grille.py
from typing import Optional 
from room_defs import RoomTemplate

class Grille:
    """
    Représente le manoir 9x5 (9 rangées, 5 colonnes).
    """
    def __init__(self, rows=9, cols=5): # <--- CHANGÉ
        self.rows = rows
        self.cols = cols
        
        self.matrice = [[None for _ in range(cols)] for _ in range(rows)]
        
        # Position de départ : Rangée 8 (en bas), Colonne 2 (milieu)
        self.joueur_x = 8  # <--- CHANGÉ
        self.joueur_y = 2  # <--- CHANGÉ

    def get_piece(self, x, y) -> Optional[RoomTemplate]:
        # ... (pas de changement ici) ...
        if 0 <= x < self.rows and 0 <= y < self.cols:
            return self.matrice[x][y]
        return None

    def placer_piece(self, piece: RoomTemplate, x: int, y: int):
        # ... (pas de changement ici) ...
        if 0 <= x < self.rows and 0 <= y < self.cols:
            self.matrice[x][y] = piece
            print(f"Pièce {piece.name} placée en ({x}, {y})")

    def deplacer_joueur(self, dx, dy):
        # ... (pas de changement ici) ...
        new_x, new_y = self.joueur_x + dx, self.joueur_y + dy
        
        if 0 <= new_x < self.rows and 0 <= new_y < self.cols:
            self.joueur_x = new_x
            self.joueur_y = new_y
            print(f"Joueur déplacé en ({self.joueur_x}, {self.joueur_y})")
            return True 
        
        print("Déplacement hors limites impossible.")
        return False
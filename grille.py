from typing import Optional, Tuple
from piece import Piece

class Grille:
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.grid: list[list[Optional[Piece]]] = [[None for _ in range(cols)] for _ in range(rows)]
        self.player_pos: Tuple[int, int] = (rows // 2, cols // 2)

    def placer_piece(self, piece: Piece, row: int, col: int):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] = piece

    def get_piece(self, row: int, col: int) -> Optional[Piece]:
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None

    def set_player_pos(self, row: int, col: int):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.player_pos = (row, col)
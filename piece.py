from dataclasses import dataclass, field
from typing import Set, Dict, Optional, Callable

@dataclass
class Piece:
    name: str
    rarity: int  # 0..3, weight=1/(3**rarity)
    cost_gems: int
    doors: Set[str]
    color: str = "base"  # Default color is "base"
    items: Dict[str, int] = field(default_factory=dict)
    effect: Optional[str] = None
    constraint: Optional[Callable[[int, int, int, int], bool]] = None
    copies: int = 1

    def __post_init__(self):
        if self.constraint is None:
            self.constraint = lambda r, c, rs, cs: True

# Yellow (royal)
class PieceMagasin(Piece):
    color: str = "royal"

# Green (forest)
class PieceJardin(Piece):
    color: str = "forest"

# Red (danger)
class PieceDanger(Piece):
    color: str = "danger"

# Blue (sky)
class PieceBleue(Piece):
    color: str = "sky"

# Orange (sunset)
class PieceOrange(Piece):
    color: str = "sunset"
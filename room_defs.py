
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Set

@dataclass
class RoomTemplate:
    # --- Champs SANS valeur par défaut (obligatoires) ---
    name: str
    color: str
    doors: Set[str]
    cost_gems: int
    rarity: int
    items: Dict[str, int]
    copies: int
    effect: Optional[str]
    constraint: Optional[Callable[[int, int, int, int], bool]]
    
    # --- Champs AVEC valeur par défaut (optionnels) ---
    # Doit être en dernier
    interactables: List[str] = field(default_factory=list)


def edge_only(row: int, col: int, rows: int, cols: int) -> bool:
    return row == 0 or row == rows - 1 or col == 0 or col == cols - 1

def not_top_row(row: int, col: int, rows: int, cols: int) -> bool:
    return row != 0

def anywhere(row: int, col: int, rows: int, cols: int) -> bool:
    return True


def build_templates() -> List[RoomTemplate]:
    t: List[RoomTemplate] = []

    # --- NOMS MIS À JOUR POUR CORRESPONDRE AUX IMAGES ---

    # "Hall" est devenu "Entrance Hall"
    t.append(RoomTemplate(
        name="Entrance Hall",
        color="blue",
        doors={"up", "left", "right"},
        cost_gems=0,
        rarity=0,
        items={},
        copies=3,
        effect=None,
        constraint=anywhere,
    ))
    
    # "Guest Room" est correct
    t.append(RoomTemplate(
        name="Guest Room",
        color="blue",
        doors={"up", "down"},
        cost_gems=0,
        rarity=0,
        items={"coin": 1, "dice": 1},
        copies=4,
        effect=None,
        constraint=anywhere,
    ))

    # "General Store" est devenu "Commissary"
    t.append(RoomTemplate(
        name="Commissary",
        color="yellow",
        doors={"left", "right"},
        cost_gems=1,
        rarity=1,
        items={},
        copies=3,
        effect="shop",
        constraint=anywhere,
    ))

    # "Indoor Garden" est devenu "Veranda"
    t.append(RoomTemplate(
        name="Veranda",
        color="green",
        doors={"up"},
        cost_gems=0,
        rarity=0,
        items={"gem": 2},
        interactables=["dig_spot"],
        copies=5,
        effect=None,
        constraint=anywhere,
    ))
    
    # "Dig Site" est devenu "Terrace"
    t.append(RoomTemplate(
        name="Terrace",
        color="green",
        doors={"left"},
        cost_gems=0,
        rarity=1,
        items={"gem": 1, "coin": 1},
        copies=3,
        effect=None,
        constraint=edge_only,
    ))

    # "Bedroom" est correct
    t.append(RoomTemplate(
        name="Bedroom",
        color="purple",
        doors={"down"},
        cost_gems=0,
        rarity=0,
        items={},
        copies=6,
        effect="restore_steps",
        constraint=anywhere,
    ))

    # "Long Corridor" est devenu "Hallway"
    t.append(RoomTemplate(
        name="Hallway",
        color="orange",
        doors={"up", "down", "left"},
        cost_gems=0,
        rarity=0,
        items={},
        copies=6,
        effect=None,
        constraint=anywhere,
    ))
    
    # "Cross Corridor" est devenu "Corridor"
    t.append(RoomTemplate(
        name="Corridor",
        color="orange",
        doors={"up", "down", "left", "right"},
        cost_gems=1,
        rarity=1,
        items={},
        copies=3,
        effect=None,
        constraint=anywhere,
    ))

    # "Danger Storage" est devenu "Lavatory"
    t.append(RoomTemplate(
        name="Lavatory",
        color="red",
        doors={"right"},
        cost_gems=0,
        rarity=1,
        items={},
        copies=4,
        effect="trap",
        constraint=anywhere,
    ))
    
    # "Cellar" est devenu "Wine Cellar"
    t.append(RoomTemplate(
        name="Wine Cellar",
        color="red",
        doors={"up"},
        cost_gems=0,
        rarity=2,
        items={"coin": 2},
        interactables=["chest"],
        copies=2,
        effect="trap",
        constraint=not_top_row,
    ))

    # "Vault" est correct
    t.append(RoomTemplate(
        name="Vault",
        color="blue",
        doors={"left"},
        cost_gems=2,
        rarity=3,
        items={"coin": 3},
        copies=2,
        effect=None,
        constraint=edge_only,
    ))

    return t


def build_initial_deck() -> List[RoomTemplate]:
    templates = build_templates()
    deck: List[RoomTemplate] = []
    for tpl in templates:
        for _ in range(tpl.copies):
            deck.append(RoomTemplate(
                name=tpl.name,
                color=tpl.color,
                doors=set(tpl.doors),
                cost_gems=tpl.cost_gems,
                rarity=tpl.rarity,
                items=dict(tpl.items),
                interactables=list(tpl.interactables),
                effect=tpl.effect,
                constraint=tpl.constraint,
                copies=1,
            ))
    return deck


# --- PIÈCE DE VICTOIRE (Section 2.5) ---

ANTECHAMBER_TEMPLATE = RoomTemplate(
    name="Antechamber",
    color="purple",
    doors={"down"},
    cost_gems=0,
    rarity=99,
    items={},
    interactables=[],
    effect="WIN",
    constraint=anywhere,
    copies=1,
)
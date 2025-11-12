from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Set


# Directions use strings: "up", "down", "left", "right"


@dataclass
class RoomTemplate:
    name: str
    color: str  # blue/yellow/green/purple/orange/red
    doors: Set[str]  # default door set (placement ensures entrance connectivity)
    cost_gems: int
    rarity: int  # 0..3, weight=1/(3**rarity)
    items: Dict[str, int]  # e.g., {"gem": 2, "coin": 1}
    effect: Optional[str]  # e.g., "restore_steps", "trap", "shop"
    constraint: Optional[Callable[[int, int, int, int], bool]]  # (row, col, rows, cols) -> bool
    copies: int  # number of copies in initial deck


def edge_only(row: int, col: int, rows: int, cols: int) -> bool:
    return row == 0 or row == rows - 1 or col == 0 or col == cols - 1


def not_top_row(row: int, col: int, rows: int, cols: int) -> bool:
    return row != 0


def anywhere(row: int, col: int, rows: int, cols: int) -> bool:
    return True


def build_templates() -> List[RoomTemplate]:
    t: List[RoomTemplate] = []

    # Blue: common and varied effects
    t.append(RoomTemplate(
        name="Hall",
        color="blue",
        doors={"up", "left", "right"},
        cost_gems=0,
        rarity=0,
        items={},
        effect=None,
        constraint=anywhere,
        copies=3,
    ))
    t.append(RoomTemplate(
        name="Guest Room",
        color="blue",
        doors={"up", "down"},
        cost_gems=0,
        rarity=0,
        items={"coin": 1},
        effect=None,
        constraint=anywhere,
        copies=4,
    ))

    # Yellow: shop
    t.append(RoomTemplate(
        name="General Store",
        color="yellow",
        doors={"left", "right"},
        cost_gems=1,
        rarity=1,
        items={},
        effect="shop",
        constraint=anywhere,
        copies=3,
    ))

    # Green: indoor garden (gems)
    t.append(RoomTemplate(
        name="Indoor Garden",
        color="green",
        doors={"up"},
        cost_gems=0,
        rarity=0,
        items={"gem": 2},
        effect=None,
        constraint=anywhere,
        copies=5,
    ))
    t.append(RoomTemplate(
        name="Dig Site",
        color="green",
        doors={"left"},
        cost_gems=0,
        rarity=1,
        items={"gem": 1, "coin": 1},
        effect=None,
        constraint=edge_only,  # edge only
        copies=3,
    ))

    # Purple: bedroom (restore steps)
    t.append(RoomTemplate(
        name="Bedroom",
        color="purple",
        doors={"down"},
        cost_gems=0,
        rarity=0,
        items={},
        effect="restore_steps",
        constraint=anywhere,
        copies=6,
    ))

    # Orange: corridors (multiple doors)
    t.append(RoomTemplate(
        name="Long Corridor",
        color="orange",
        doors={"up", "down", "left"},
        cost_gems=0,
        rarity=0,
        items={},
        effect=None,
        constraint=anywhere,
        copies=6,
    ))
    t.append(RoomTemplate(
        name="Cross Corridor",
        color="orange",
        doors={"up", "down", "left", "right"},
        cost_gems=1,
        rarity=1,
        items={},
        effect=None,
        constraint=anywhere,
        copies=3,
    ))

    # Red: adverse effects
    t.append(RoomTemplate(
        name="Danger Storage",
        color="red",
        doors={"right"},
        cost_gems=0,
        rarity=1,
        items={},
        effect="trap",  # first entry: -1 step
        constraint=anywhere,
        copies=4,
    ))
    t.append(RoomTemplate(
        name="Cellar",
        color="red",
        doors={"up"},
        cost_gems=0,
        rarity=2,
        items={"coin": 2},
        effect="trap",
        constraint=not_top_row,
        copies=2,
    ))

    # Vault (blue or special case)
    t.append(RoomTemplate(
        name="Vault",
        color="blue",
        doors={"left"},
        cost_gems=2,
        rarity=3,
        items={"coin": 3},
        effect=None,
        constraint=edge_only,
        copies=2,
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
                effect=tpl.effect,
                constraint=tpl.constraint,
                copies=1,
            ))
    return deck
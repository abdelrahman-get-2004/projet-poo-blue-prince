from typing import List
from piece import Piece, PieceMagasin, PieceJardin, PieceDanger, PieceBleue, PieceOrange

def build_templates() -> List[Piece]:
    t: List[Piece] = []

    # Yellow (royal)
    t.append(PieceMagasin(
        name="Shop",
        doors={"left", "down", "right"},
        cost_gems=0,
        rarity=1,
        effect="shop",
        copies=3,
    ))

    # Green (forest)
    t.append(PieceJardin(
        name="Garden",
        doors={"left", "down", "right"},
        cost_gems=0,
        rarity=0,
        items={"gem": 2},
        copies=5,
    ))
    t.append(PieceJardin(
        name="Courtyard",
        doors={"left", "down", "right"},
        cost_gems=1,
        rarity=1,
        items={"coin": 1},
        copies=2,
    ))
    t.append(PieceJardin(
        name="Balcony",
        doors={"up", "down"},
        cost_gems=1,
        rarity=1,
        copies=2,
    ))
    t.append(PieceJardin(
        name="Greenhouse",
        doors={"down"},
        cost_gems=2,
        rarity=2,
        items={"gem": 1},
        copies=1,
    ))

    # Red (danger)
    t.append(PieceDanger(
        name="Gym",
        doors={"left", "right"},
        cost_gems=1,
        rarity=1,
        effect="trap",
        copies=2,
    ))
    t.append(PieceDanger(
        name="Chapel",
        doors={"up", "down"},
        cost_gems=2,
        rarity=2,
        items={"coin": 1},
        copies=1,
    ))
    t.append(PieceDanger(
        name="Maid's Room",
        doors={"down"},
        cost_gems=1,
        rarity=1,
        copies=2,
    ))
    t.append(PieceDanger(
        name="Furnace",
        doors={"down"},
        cost_gems=2,
        rarity=2,
        effect="trap",
        copies=1,
    ))

    # Blue (sky)
    t.append(PieceBleue(
        name="Office",
        doors={"left", "right"},
        cost_gems=1,
        rarity=1,
        items={"coin": 1},
        copies=2,
    ))
    t.append(PieceBleue(
        name="Hall of Mirrors",
        doors={"up", "down", "left", "right"},
        cost_gems=2,
        rarity=2,
        effect="teleport_random",
        copies=1,
    ))
    t.append(PieceBleue(
        name="Pool",
        doors={"up", "down", "left", "right"},
        cost_gems=2,
        rarity=2,
        copies=1,
    ))
    t.append(PieceBleue(
        name="Entrance Hall",
        doors={"up", "down", "left", "right"},
        cost_gems=1,
        rarity=1,
        copies=3,
    ))

    # Orange (sunset)
    t.append(PieceOrange(
        name="Hall",
        doors={"up", "down", "left", "right"},
        cost_gems=0,
        rarity=0,
        copies=3,
    ))
    t.append(PieceOrange(
        name="Long Corridor",
        doors={"up", "down", "left", "right"},
        cost_gems=0,
        rarity=0,
        copies=6,
    ))
    t.append(PieceOrange(
        name="Corridor",
        doors={"up", "down"},
        cost_gems=0,
        rarity=0,
        copies=4,
    ))
    t.append(PieceOrange(
        name="Foyer",
        doors={"up", "down"},
        cost_gems=0,
        rarity=0,
        copies=4,
    ))

    # Purple (sky)
    t.append(PieceBleue(
        name="Bedroom",
        doors={"left", "down"},
        cost_gems=0,
        rarity=0,
        effect="restore_steps",
        copies=6,
    ))
    t.append(PieceBleue(
        name="Master Bedroom",
        doors={"down"},
        cost_gems=1,
        rarity=2,
        effect="restore_steps",
        copies=1,
    ))

    return t

def build_initial_deck() -> List[Piece]:
    templates = build_templates()
    deck: List[Piece] = []
    for tpl in templates:
        for _ in range(tpl.copies):
            deck.append(tpl)
    return deck
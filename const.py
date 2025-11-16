ROWS, COLS = 9, 5
TILE = 96
PANEL_W = 260
MARGIN = 8
WIN_W = COLS * TILE + PANEL_W + MARGIN * 3
WIN_H = ROWS * TILE + MARGIN * 2

FONT_NAMES = [
    "Microsoft YaHei",
    "Microsoft YaHei UI",
    "SimHei",
    "Arial Unicode MS",
    "Noto Sans CJK SC",
    "Sarasa Gothic SC",
    "WenQuanYi Zen Hei",
    "sans-serif",
]

COLORS = {
    "grid_bg": (20, 18, 24),
    "panel_bg": (34, 32, 40),
    "text": (224, 220, 228),
    "disabled": (100, 96, 108),
    "base": (85, 80, 96),
    "forest": (60, 110, 80),
    "sky": (80, 120, 160),
    "royal": (140, 90, 160),
    "sunset": (190, 110, 80),
    "danger": (160, 70, 70),
    "goal": (210, 180, 100),
}

ROOM_NAME_TO_IMAGE_FILE = {
    "Shop": "商店.png",
    "Garden": "花园.png",
    "Courtyard": "庭院.png",
    "Balcony": "阳台.png",
    "Greenhouse": "温室.png",
    "Gym": "健身房.png",
    "Chapel": "教堂.png",
    "Maid's Room": "女仆间.png",
    "Furnace": "熔炉.png",
    "Office": "办公室.png",
    "Hall of Mirrors": "镜厅.png",
    "Pool": "泳池.png",
    "Entrance Hall": "入口大厅.png",
    "Hall": "hall.png",
    "Long Corridor": "走廊.png",
    "Corridor": "走廊.png",
    "Foyer": "门厅.png",
    "Bedroom": "卧室.png",
    "Master Bedroom": "主卧.png",
    "Starting Hall": "入口大厅.png",
}

DIRS = {
    "up": (-1, 0),
    "down": (1, 0),
    "left": (0, -1),
    "right": (0, 1),
}

def opposite_dir(d: str) -> str:
    return {"up": "down", "down": "up", "left": "right", "right": "left"}[d]
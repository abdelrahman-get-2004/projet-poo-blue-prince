import sys
import random
from typing import List, Optional, Dict, Set, Tuple
from dataclasses import dataclass

import pygame

from const import (
    ROWS, COLS, TILE, MARGIN, PANEL_W, WIN_W, WIN_H, COLORS, DIRS, FONT_NAMES, ROOM_NAME_TO_IMAGE_FILE, opposite_dir
)
from helpers import in_bounds
from piece import Piece
from catalogue import build_initial_deck
from grille import Grille
from joueur import Joueur

@dataclass
class RoomInstance:
    template: Piece
    doors: Set[str]
    items: Dict[str, int]
    effect_applied: bool = False

class Jeu:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Blue Prince")
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))
        self.clock = pygame.time.Clock()
        self.font = self._get_font(20)
        self.small = self._get_font(16)

        self.room_images: Dict[str, pygame.Surface] = {}
        self.room_thumb_images: Dict[str, pygame.Surface] = {}
        self._load_room_images()

        self.grille = Grille(ROWS, COLS)
        self.joueur = Joueur(12, 2, 0)
        self.deck: List[Piece] = build_initial_deck()

        self.goal_pos = (0, COLS // 2)
        self.grille.placer_piece(RoomInstance(
            template=Piece(
                name="Foyer",
                color="goal",
                doors={"down"},
                cost_gems=0,
                rarity=3,
                items={},
                effect=None,
                constraint=None,
                copies=1,
            ),
            doors={"down"},
            items={},
        ), self.goal_pos[0], self.goal_pos[1])

        self.joueur.r, self.joueur.c = ROWS - 1, COLS // 2
        start_tpl = Piece(
            name="Starting Hall",
            color="base",
            doors={"up", "left", "right"},
            cost_gems=0,
            rarity=0,
            items={"gem": 1},
            effect=None,
            constraint=None,
            copies=1,
        )
        self.grille.placer_piece(RoomInstance(template=start_tpl, doors=set(start_tpl.doors), items=dict(start_tpl.items)), self.joueur.r, self.joueur.c)
        self.visited_rooms: Set[Tuple[int, int]] = {(self.joueur.r, self.joueur.c)}
        self.special_effect_data: Dict[str, any] = {}

        self.placing: bool = False
        self.place_target: Optional[Tuple[int, int, str]] = None
        self.candidates: List[Piece] = []

        self.shop_open: bool = False

        self.running = True
        self.status_msg: str = ""
        self.status_timer: int = 0

    def _load_room_images(self):
        fig_path = "fig/"
        thumb_size = (64, 64)
        for name, filename in ROOM_NAME_TO_IMAGE_FILE.items():
            try:
                img = pygame.image.load(fig_path + filename).convert()
                self.room_images[name] = pygame.transform.scale(img, (TILE, TILE))
                self.room_thumb_images[name] = pygame.transform.scale(img, thumb_size)
            except pygame.error as e:
                print(f"Warning: Could not load image for {name}: {e}")

    def _get_font(self, size: int) -> pygame.font.Font:
        for name in FONT_NAMES:
            try:
                f = pygame.font.SysFont(name, size)
                if f is not None:
                    return f
            except Exception:
                continue
        return pygame.font.SysFont(None, size)

    def run(self) -> None:
        while self.running:
            self.clock.tick(60)
            self.handle_input()
            self.handle_shop()
            if self.status_timer > 0:
                self.status_timer -= 1
            self.draw()
        pygame.quit()
        sys.exit(0)

    def draw(self) -> None:
        self.screen.fill(COLORS["grid_bg"])
        # Grid
        for r in range(ROWS):
            for c in range(COLS):
                x = MARGIN + c * TILE
                y = MARGIN + r * TILE
                rect = pygame.Rect(x, y, TILE, TILE)
                pygame.draw.rect(self.screen, (60, 60, 60), rect, 1)
                inst = self.grille.get_piece(r, c)
                if inst is not None:
                    room_image = self.room_images.get(inst.template.name)
                    if room_image:
                        self.screen.blit(room_image, rect)
                    else:
                        # Fallback to solid colors if image is missing
                        color = COLORS.get(inst.template.color, (100, 100, 100))
                        if (r, c) == self.goal_pos:
                            color = COLORS["goal"]
                        pygame.draw.rect(self.screen, color, rect)

                    # Item preview (simplified: show gem/coin count)
                    items_txt = []
                    g = inst.items.get("gem", 0)
                    c = inst.items.get("coin", 0)
                    if g:
                        items_txt.append(f"G{g}")
                    if c:
                        items_txt.append(f"C{c}")
                    if items_txt:
                        it_surf = self.small.render(
                            ",".join(items_txt), True, COLORS["text"]
                        )
                        self.screen.blit(it_surf, (x + TILE - it_surf.get_width() - 6, y + 6))

        # Draw revealed rooms from Observatory
        if 'revealed_rooms' in self.special_effect_data:
            for r, c in self.special_effect_data['revealed_rooms']:
                x = MARGIN + c * TILE
                y = MARGIN + r * TILE
                # Draw a semi-transparent rectangle with a question mark
                s = pygame.Surface((TILE, TILE), pygame.SRCALPHA)
                s.fill((100, 100, 100, 100))
                self.screen.blit(s, (x, y))
                self.blit_text_fit("?", x + TILE // 2 - 8, y + TILE // 2 - 12, 20, base_size=24)

        # Player position
        px = MARGIN + self.joueur.c * TILE + TILE // 2
        py = MARGIN + self.joueur.r * TILE + TILE // 2
        pygame.draw.circle(self.screen, (240, 240, 240), (px, py), 10)

        # Right panel
        panel_x = MARGIN + COLS * TILE + MARGIN
        panel_rect = pygame.Rect(panel_x, MARGIN, PANEL_W, WIN_H - MARGIN * 2)
        pygame.draw.rect(self.screen, COLORS["panel_bg"], panel_rect)

        # Statistics (with icons)
        self.draw_metrics(panel_x)
        self.blit_text(f"Deck: {len(self.deck)}", panel_x + 14, MARGIN + 100)
        self.blit_text_fit("E: Pick   S: Shop   Q: Quit", panel_x + 14, MARGIN + 128, PANEL_W - 28, base_size=20, min_size=12)
        # Status message
        if self.status_timer > 0 and self.status_msg:
            self.blit_text_fit(self.status_msg, panel_x + 14, MARGIN + 188, PANEL_W - 28, base_size=20, min_size=12)

        # Placement UI
        if self.placing and self.place_target:
            self.draw_placing_ui(panel_x)

        # Shop prompt
        cur = self.current_room()
        if cur and cur.template.effect == "shop":
            self.blit_text_fit("Press S to open shop in a shop room", panel_x + 14, MARGIN + 160, PANEL_W - 28, base_size=20, min_size=12)
            if self.shop_open:
                self.draw_shop_ui(panel_x)

        # Win/Loss state
        self.draw_end_state(panel_x)

        pygame.display.flip()

    def blit_text(self, text: str, x: int, y: int, color=COLORS["text"]) -> None:
        surf = self.font.render(text, True, color)
        self.screen.blit(surf, (x, y))

    def blit_text_fit(self, text: str, x: int, y: int, max_width: int, base_size: int = 20, min_size: int = 12, color=COLORS["text"]) -> None:
        # Progressively shrink font, if still too wide, truncate and add ellipsis
        fitted = False
        for size in range(base_size, min_size - 1, -1):
            font = self._get_font(size)
            w, _ = font.size(text)
            if w <= max_width:
                surf = font.render(text, True, color)
                self.screen.blit(surf, (x, y))
                fitted = True
                break
        if fitted:
            return
        # Use minimum font size and truncate
        font = self._get_font(min_size)
        txt = text
        removed = 0
        while font.size(txt + ("…" if removed > 0 else ""))[0] > max_width and len(txt) > 1:
            # Batch reduction for efficiency
            cut = 2 if len(txt) > 6 else 1
            txt = txt[:-cut]
            removed += cut
        display = txt + ("…" if removed > 0 else "")
        surf = font.render(display, True, color)
        self.screen.blit(surf, (x, y))

    def draw_door(self, x: int, y: int, d: str) -> None:
        if d == "up":
            pygame.draw.line(self.screen, (20, 20, 20), (x + TILE // 2 - 10, y + 2), (x + TILE // 2 + 10, y + 2), 4)
        elif d == "down":
            pygame.draw.line(self.screen, (20, 20, 20), (x + TILE // 2 - 10, y + TILE - 2), (x + TILE // 2 + 10, y + TILE - 2), 4)
        elif d == "left":
            pygame.draw.line(self.screen, (20, 20, 20), (x + 2, y + TILE // 2 - 10), (x + 2, y + TILE // 2 + 10), 4)
        elif d == "right":
            pygame.draw.line(self.screen, (20, 20, 20), (x + TILE - 2, y + TILE // 2 - 10), (x + TILE - 2, y + TILE // 2 + 10), 4)

    def draw_placing_ui(self, panel_x: int) -> None:
        # Draw candidate card information
        x = panel_x + 14
        y = MARGIN + 200
        self.blit_text_fit("Choose a room to place:", x, y, PANEL_W - 28, base_size=20, min_size=12)
        if not self.candidates:
            self.blit_text_fit("(No candidates) ESC to cancel", x, y + 28, PANEL_W - 28, base_size=16, min_size=10, color=COLORS["disabled"])
            return
        for i, tpl in enumerate(self.candidates):
            cy = y + 36 + i * 88  # Increase vertical spacing for image
            bar = pygame.Rect(x, cy, PANEL_W - 28, 80) # Increase height for image
            pygame.draw.rect(self.screen, COLORS["panel_bg"], bar, 1)

            # Draw room thumbnail
            thumb_img = self.room_thumb_images.get(tpl.name)
            if thumb_img:
                self.screen.blit(thumb_img, (x + 5, cy + 8))

            # Adjust text position to be to the right of the thumbnail
            text_x = x + 75
            text_width = PANEL_W - 100

            name = f"{i+1}. {tpl.name} [{tpl.color}]"
            doors = ",".join(sorted(list(tpl.doors)))
            info = f"Doors:{doors}  Cost:{tpl.cost_gems}G  Rarity:{tpl.rarity}"
            self.blit_text_fit(name, text_x, cy + 12, text_width, base_size=18, min_size=10)
            # Gray out the second line if cost is insufficient
            color_txt = COLORS["text"] if self.joueur.gems >= tpl.cost_gems else COLORS["disabled"]
            self.blit_text_fit(info, text_x, cy + 40, text_width, base_size=16, min_size=10, color=color_txt)

    def draw_shop_ui(self, panel_x: int) -> None:
        x = panel_x + 14
        y = MARGIN + 360
        self.blit_text_fit("Shop: 1) 2 coins -> 1 gem  2) 1 coin -> 1 step", x, y, PANEL_W - 28, base_size=20, min_size=12)

    def draw_end_state(self, panel_x: int) -> None:
        # Victory: Reached the foyer
        if (self.joueur.r, self.joueur.c) == self.goal_pos:
            self.blit_text_fit("Reached the foyer! You win!", panel_x + 14, WIN_H - MARGIN - 80, PANEL_W - 28, base_size=20, min_size=12)
        # Defeat: Out of steps and unable to move (simplified to a hint when steps are 0)
        elif self.joueur.steps <= 0:
            self.blit_text_fit("Out of steps! You lose…", panel_x + 14, WIN_H - MARGIN - 80, PANEL_W - 28, base_size=20, min_size=12)

    # --- Panel Icons and Layout ---
    def draw_metrics(self, panel_x: int) -> None:
        # Icons size and positions
        base_x = panel_x + 14
        y_steps = MARGIN + 16
        y_gems = MARGIN + 44
        y_coins = MARGIN + 72

        # Steps icon (simple footprint shape)
        self.draw_steps_icon(base_x, y_steps, 14)
        self.blit_text(f"Steps: {self.joueur.steps}", base_x + 28, y_steps)

        # Gems icon (diamond)
        self.draw_diamond_icon(base_x, y_gems, 14, (0, 200, 255))
        self.blit_text(f"Gems: {self.joueur.gems}", base_x + 28, y_gems)

        # Coins icon (gold circle)
        self.draw_coin_icon(base_x, y_coins, 14, (212, 175, 55))
        self.blit_text(f"Coins: {self.joueur.coins}", base_x + 28, y_coins)

    def draw_diamond_icon(self, x: int, y: int, size: int, color: Tuple[int, int, int]) -> None:
        half = size // 2
        points = [(x, y + half), (x + half, y), (x + size, y + half), (x + half, y + size)]
        pygame.draw.polygon(self.screen, color, points)

    def draw_coin_icon(self, x: int, y: int, size: int, color: Tuple[int, int, int]) -> None:
        pygame.draw.circle(self.screen, color, (x + size // 2, y + size // 2), size // 2)
        pygame.draw.circle(self.screen, (150, 120, 40), (x + size // 2, y + size // 2), size // 2, 2)

    def draw_steps_icon(self, x: int, y: int, size: int) -> None:
        # Two small ellipses to resemble footprints
        s = size
        pygame.draw.ellipse(self.screen, (200, 200, 200), pygame.Rect(x, y, s // 2 + 2, s // 3))
        pygame.draw.ellipse(self.screen, (200, 200, 200), pygame.Rect(x + s // 2, y + s // 4, s // 2, s // 3))

    def set_status(self, msg: str, frames: int = 240) -> None:
        # About 4 seconds (60 FPS)
        self.status_msg = msg
        self.status_timer = frames

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
                if self.placing:
                    if event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                        self.placing = False
                        self.candidates = []
                        self.place_target = None
                    elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                        idx = {pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2}[event.key]
                        if 0 <= idx < len(self.candidates):
                            r, c, entry_dir = self.place_target
                            tpl = self.candidates[idx]
                            inst = self.place_room(tpl, r, c, entry_dir)
                            if inst is not None:
                                # Move to the new room and apply effects, consuming a step
                                self.joueur.r, self.joueur.c = r, c
                                self.joueur.steps = max(0, self.joueur.steps - 1)
                                self.apply_enter_effect(inst)
                                self.placing = False
                                self.candidates = []
                                self.place_target = None
                else:
                    # Not placing: room interaction or movement
                    if event.key == pygame.K_e:
                        self.collect_items()
                    if event.key == pygame.K_s:
                        # Open shop in a shop room
                        cur = self.current_room()
                        if cur and cur.template.effect == "shop":
                            self.shop_open = not self.shop_open
                    if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                        self.try_move(event.key)

    def current_room(self) -> Optional[RoomInstance]:
        return self.grille.get_piece(self.joueur.r, self.joueur.c)

    def collect_items(self) -> None:
        room = self.current_room()
        if not room:
            return
        # Simplified: Pick up all remaining items at once
        g = room.items.get("gem", 0)
        c = room.items.get("coin", 0)
        if g > 0:
            self.joueur.gems += g
            room.items["gem"] = 0
        if c > 0:
            self.joueur.coins += c
            room.items["coin"] = 0
        # Feedback message
        if g or c:
            self.set_status(f"Picked: +{g} gems, +{c} coins")
        else:
            self.set_status("No items to pick up")

    def try_move(self, key: int) -> None:
        # Clear special effects data on move
        if 'revealed_rooms' in self.special_effect_data:
            del self.special_effect_data['revealed_rooms']

        key_to_dir = {
            pygame.K_UP: "up",
            pygame.K_DOWN: "down",
            pygame.K_LEFT: "left",
            pygame.K_RIGHT: "right",
        }
        d = key_to_dir[key]
        dr, dc = DIRS[d]
        nr, nc = self.joueur.r + dr, self.joueur.c + dc
        if not in_bounds(nr, nc):
            return
        cur = self.current_room()
        if not cur or d not in cur.doors:
            return  # No door here
        target = self.grille.get_piece(nr, nc)
        if target is None:
            # Enter placement process
            self.candidates = self.draw_candidates(nr, nc, d)
            if not self.candidates:
                # No candidates -> cancel placing and notify
                self.set_status("No placeable room in this direction (constraints/deck)")
                self.placing = False
                self.place_target = None
            else:
                self.placing = True
                self.place_target = (nr, nc, d)
            return
        else:
            # Room exists, check for two-way door
            if opposite_dir(d) in target.doors:
                if self.joueur.steps <= 0:
                    self.set_status("You are out of steps!")
                    return
                self.joueur.r, self.joueur.c = nr, nc
                self.joueur.steps = max(0, self.joueur.steps - 1)
                self.apply_enter_effect(target)

    def handle_shop(self) -> None:
        if not self.shop_open:
            return
        # Simple implementation: Press 1 for 2 coins -> 1 gem; Press 2 for 1 coin -> 1 step
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            if self.joueur.coins >= 2:
                self.joueur.coins -= 2
                self.joueur.gems += 1
        elif keys[pygame.K_2]:
            if self.joueur.coins >= 1:
                self.joueur.coins -= 1
                self.joueur.steps += 1

    def place_room(self, tpl: Piece, r: int, c: int, entry_dir: str) -> Optional[RoomInstance]:
        # Pay gems
        if self.joueur.gems < tpl.cost_gems:
            self.set_status("Not enough gems!")
            return None
        self.joueur.gems -= tpl.cost_gems

        # If the template was a temporary one from the Library, get the original
        original_tpl = getattr(tpl, 'original_template', tpl)

        # Filter out doors that lead off the map
        doors = set()
        for d in original_tpl.doors:
            dr, dc = DIRS[d]
            if in_bounds(r + dr, c + dc):
                doors.add(d)
        
        # Add the entry door, which is always valid
        doors.add(opposite_dir(entry_dir))

        # Create the new room instance
        inst = RoomInstance(template=original_tpl, doors=doors, items=dict(original_tpl.items))
        
        # Place it on the grid
        self.grille.placer_piece(inst, r, c)
        
        # Apply any immediate effects of entering the room
        self.apply_enter_effect(inst)

        # Remove this copy from the deck (match by object)
        for i, t in enumerate(self.deck):
            if t is original_tpl:
                del self.deck[i]
                break
        return inst

    def apply_enter_effect(self, room: RoomInstance) -> None:
        if room.effect_applied:
            return
        
        self.visited_rooms.add((self.joueur.r, self.joueur.c))

        eff = room.template.effect
        if eff == "restore_steps":
            self.joueur.steps += 2
            self.set_status("Rested in a Bedroom. +2 steps.")
            room.effect_applied = True
        elif eff == "-1_step":
            self.joueur.steps = max(0, self.joueur.steps - 1)
            self.set_status("A wind tunnel pushes you back. -1 step.")
            room.effect_applied = True
        elif eff == "shop":
            # Entering doesn't force the shop open, press S to open
            self.set_status("You found a General Store. Press S to shop.")
            room.effect_applied = True
        elif eff == "reveal_3":
            self.set_status("The Observatory reveals nearby areas!")
            # Find 3 random unrevealed neighbors
            neighbors = []
            for dr, dc in DIRS.values():
                nr, nc = self.joueur.r + dr, self.joueur.c + dc
                if in_bounds(nr, nc) and self.grille.get_piece(nr, nc) is None:
                    neighbors.append((nr, nc))
            
            revealed = []
            random.shuffle(neighbors)
            for i in range(min(3, len(neighbors))):
                r, c = neighbors[i]
                # Just show a temporary marker, not a full room
                # We can store this in special_effect_data to draw it
                revealed.append((r, c))
            self.special_effect_data['revealed_rooms'] = revealed
            room.effect_applied = True
        elif eff == "teleport_random":
            if len(self.visited_rooms) > 1:
                # Exclude current room from teleport options
                options = list(self.visited_rooms - {(self.joueur.r, self.joueur.c)})
                target_r, target_c = random.choice(options)
                self.joueur.r, self.joueur.c = target_r, target_c
                self.set_status("ZAP! Teleported to a random room.")
            else:
                self.set_status("Teleporter fizzles. Nowhere to go.")
            room.effect_applied = True
        elif eff == "gamble_chance":
            roll = random.random()
            if roll < 0.4: # 40% chance to win
                win_amount = random.randint(1, 3)
                self.joueur.gems += win_amount
                self.set_status(f"Gambling pays off! +{win_amount} gems.")
            elif roll < 0.8: # 40% chance to lose
                lose_amount = random.randint(1, 2)
                self.joueur.gems = max(0, self.joueur.gems - lose_amount)
                self.set_status(f"Bad luck! Lost {lose_amount} gems.")
            else: # 20% chance for nothing
                self.set_status("You break even at the gambling table.")
            room.effect_applied = True
        elif eff == "costly_entry":
            self.set_status(f"Paid {room.template.cost_gems} gems for a Cursed Treasury.")
            # Cost is already paid during placement, this is just a notification
            room.effect_applied = True
        # draw_less is handled in draw_candidates

    def draw_candidates(self, r: int, c: int, from_dir: str) -> List[Piece]:
        num_candidates = 3
        cur = self.current_room()
        if cur and cur.template.effect == "draw_less":
            num_candidates = 2

        in_library = cur and cur.template.effect == "library"

        # Filter deck based on constraints
        allowed: List[Piece] = []
        for tpl in self.deck:
            if tpl.constraint(r, c, ROWS, COLS):
                allowed.append(tpl)

        if not allowed:
            # This can happen if no pieces in the deck satisfy the constraints
            return []

        weights = [self._weight(t, r, c) for t in allowed]
        
        picks = []
        # Use a temporary list to avoid modifying the original `allowed` list inside the loop
        temp_allowed = list(allowed)
        temp_weights = list(weights)

        for _ in range(num_candidates):
            if not temp_allowed: break
            choice = random.choices(temp_allowed, weights=temp_weights, k=1)[0]
            
            # If in library, reduce cost
            if in_library:
                # Create a temporary copy to modify the cost
                choice_copy = Piece(
                    name=choice.name,
                    couleur=choice.couleur,
                    portes=choice.portes,
                    cout=max(0, choice.cout - 1), # Reduce cost by 1, min 0
                    rarete=choice.rarete,
                    items=choice.items,
                    effet=choice.effet,
                    contrainte=choice.contrainte,
                    copies=1 # This is a temporary object
                )
                # We need to find the original template later when placing
                # So we attach the original to it.
                setattr(choice_copy, 'original_template', choice)
                picks.append(choice_copy)
            else:
                picks.append(choice)

            # Lower the weight of the chosen template to reduce duplicates in the same draw
            indices = [i for i, t in enumerate(temp_allowed) if t.name == choice.name]
            for i in indices:
                temp_weights[i] *= 0.2
        # Ensure at least one 0-cost candidate if possible
        if picks:
            has_zero_cost = any(p.cost_gems == 0 for p in picks)
            if not has_zero_cost:
                # Find available 0-cost templates from the allowed list
                zero_cost_options = [t for t in allowed if t.cost_gems == 0]
                if zero_cost_options:
                    # Find the most expensive candidate to replace
                    most_expensive_pick = max(picks, key=lambda p: p.cost_gems)
                    replace_idx = picks.index(most_expensive_pick)
                    
                    # Pick a random 0-cost room to replace it with
                    replacement = random.choice(zero_cost_options)

                    # If we are in a library, the replacement should also be a temporary copy
                    # This is for consistency, although its cost is 0 and won't be reduced.
                    if in_library:
                        replacement_copy = Piece(
                            name=replacement.name,
                            couleur=replacement.couleur,
                            portes=replacement.portes,
                            cout=0,
                            rarete=replacement.rarete,
                            items=replacement.items,
                            effet=replacement.effet,
                            contrainte=replacement.contrainte,
                            copies=1
                        )
                        setattr(replacement_copy, 'original_template', replacement)
                        picks[replace_idx] = replacement_copy
                    else:
                        picks[replace_idx] = replacement
        return picks

    def _weight(self, tpl: Piece, r: int, c: int) -> float:
        # Rarity: higher rarity = lower weight (less common)
        # 1 -> 1.0, 2 -> 0.5, 3 -> 0.25, 4 -> 0.1, 5 -> 0.05
        rarity_weight = 1.0 / (2**(tpl.rarity - 1)) if tpl.rarity > 1 else 1.0
        if tpl.rarity >= 4:
            rarity_weight /= 2.0

        # Proximity to center: slight bias for rooms to be closer to center
        dist_from_center_r = abs(r - ROWS // 2)
        dist_from_center_c = abs(c - COLS // 2)
        prox_weight = 1.0 - 0.05 * (dist_from_center_r + dist_from_center_c)

        return rarity_weight * prox_weight

if __name__ == "__main__":
    Jeu().run()
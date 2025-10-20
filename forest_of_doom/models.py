import random
from dataclasses import dataclass, field
from typing import Dict, Optional
import json
from pathlib import Path

# Base constants for stat generation
SKILL_BASE = 6
STAMINA_BASE = 12
LUCK_BASE = 6


@dataclass
class Player:
    skill: int = 0
    stamina: int = 0
    luck: int = 0
    backpack: Dict[str, int] = field(default_factory=lambda: {"gold": 10, "map": 1})
    potion: Optional[str] = None


def generate_stats(player: Player, rng=None) -> None:
    """Populate player's skill, stamina, and luck using optional RNG (for tests)."""
    if rng is None:
        rng = random
    player.skill = rng.randint(1, 6) + SKILL_BASE
    player.stamina = rng.randint(1, 6) + rng.randint(1, 6) + STAMINA_BASE
    player.luck = rng.randint(1, 6) + LUCK_BASE


def player_to_dict(player: Player) -> Dict:
    """Return a JSON-serializable dict representing the player."""
    return {
        'skill': player.skill,
        'stamina': player.stamina,
        'luck': player.luck,
        'backpack': player.backpack,
        'potion': player.potion,
    }


def player_from_dict(data: Dict) -> Player:
    """Create a Player from a dict (as produced by player_to_dict)."""
    p = Player()
    p.skill = int(data.get('skill', 0))
    p.stamina = int(data.get('stamina', 0))
    p.luck = int(data.get('luck', 0))
    p.backpack = dict(data.get('backpack', {}))
    p.potion = data.get('potion')
    return p


def save_player(player: Player, path: str | Path) -> None:
    """Save player state as JSON to the given path."""
    p = player_to_dict(player)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(p, f, ensure_ascii=False, indent=2)


def load_player(path: str | Path) -> Player:
    """Load player state from JSON file and return a Player instance."""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return player_from_dict(data)

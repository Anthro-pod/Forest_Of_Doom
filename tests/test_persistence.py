import json
from pathlib import Path

from Forrest_of_Doom.models import Player, save_player, load_player


def test_save_load_roundtrip(tmp_path: Path):
    p = Player(skill=10, stamina=18, luck=8, backpack={'gold': 42, 'map': 1}, potion='skill')
    path = tmp_path / 'player.json'
    save_player(p, path)
    loaded = load_player(path)
    assert loaded.skill == p.skill
    assert loaded.stamina == p.stamina
    assert loaded.luck == p.luck
    assert loaded.backpack == p.backpack
    assert loaded.potion == p.potion

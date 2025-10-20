import random

from forest_of_doom.models import Player, generate_stats


def test_generate_stats_ranges():
    player = Player()
    rng = random.Random(0)  # deterministic
    generate_stats(player, rng=rng)
    assert 7 <= player.skill <= 12
    assert 14 <= player.stamina <= 24
    assert 7 <= player.luck <= 12

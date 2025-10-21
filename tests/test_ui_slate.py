import builtins
import io
import sys

import pytest

from forest_of_doom import game
from forest_of_doom.models import Player
from forest_of_doom import ui


def test_yaztromo_populates_slate(monkeypatch, capsys):
    # Simulate the player choosing to "follow" Yaztromo upstairs.
    inputs = iter(["follow"])  # first prompt in yaztromo_intro
    monkeypatch.setattr('builtins.input', lambda prompt='': next(inputs))

    player = Player()
    # Run yaztromo_intro with fast=True to avoid slow_print pauses
    section = game.yaztromo_intro(player, fast=True)
    assert section == 'shop'

    # Slate should be populated with the expected items and prices
    assert hasattr(player, 'slate')
    assert isinstance(player.slate, list)
    assert len(player.slate) >= 1

    # Check a few items and their prices per the pricing rules
    names_to_prices = {item['name']: item['price'] for item in player.slate}
    assert names_to_prices['Potion of Healing'] == 3
    assert names_to_prices['Potion of Plant Control'] == 2
    assert names_to_prices['Potion of Insect Control'] == 2
    assert names_to_prices['Boots of Leaping'] == 2
    assert names_to_prices['Glove of Missile Dexterity'] == 2
    assert names_to_prices['Rod of Water-finding'] == 2
    assert names_to_prices['Garlic Buds'] == 2

    # The display_slate UI should print the slate lines
    ui.display_slate(player)
    captured = capsys.readouterr()
    assert 'Potion of Healing' in captured.out
    assert '3 gold' in captured.out
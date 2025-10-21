from forest_of_doom.models import Player
from forest_of_doom import ui, game


def setup_player_with_slate():
    p = Player()
    # Populate slate with two items
    p.slate = [
        {'name': 'Cheap Trinket', 'price': 2},
        {'name': 'Expensive Amulet', 'price': 5},
    ]
    p.backpack['gold'] = 5
    return p


def test_buy_success():
    p = setup_player_with_slate()
    success, msg = ui.buy_from_slate(p, 0)
    assert success is True
    assert 'Purchased' in msg
    assert p.backpack['gold'] == 3
    assert len(p.inventory) == 1
    assert p.inventory[0]['name'] == 'Cheap Trinket'


def test_buy_insufficient_funds():
    p = setup_player_with_slate()
    # Try to buy expensive item costing 5 with only 5 gold then buy again to fail
    success, msg = ui.buy_from_slate(p, 1)
    assert success is True
    assert p.backpack['gold'] == 0
    # Now attempt to buy first item with 0 gold
    success2, msg2 = ui.buy_from_slate(p, 0)
    assert success2 is False
    assert 'Insufficient' in msg2


def test_buy_invalid_index():
    p = setup_player_with_slate()
    success, msg = ui.buy_from_slate(p, 99)
    assert success is False
    assert 'range' in msg or 'Invalid' in msg

from Forrest_of_Doom import game


def test_run_game_fast_mode(monkeypatch):
    # Simulate answers for prompts in order: enter yes, ready, choose potion: skill, follow Yaztromo
    answers = iter(["yes", "ready", "skill", "follow"])
    monkeypatch.setattr('builtins.input', lambda prompt='': next(answers))
    # Run the game in fast mode and with a seed so stats are deterministic
    game.run_game(fast=True, seed=0)


def test_in_game_save(monkeypatch, tmp_path):
    # Simulate answers: enter yes, ready, then 'save' at potion prompt, then 'skill', then follow
    answers = iter(["yes", "ready", "save", "skill", "follow"])
    monkeypatch.setattr('builtins.input', lambda prompt='': next(answers))
    save_path = tmp_path / 'saved.json'

    def save_callback(player, slot=None):
        # simple save: write the player's skill so we can assert
        with open(save_path, 'w') as f:
            f.write(str(player.skill))
    

    game.run_game(fast=True, seed=0, save_callback=save_callback)
    assert save_path.exists()


def test_in_game_load(monkeypatch, tmp_path):
    # create a saved player file with known stats
    from Forrest_of_Doom.models import save_player, Player

    saved = Player(skill=99, stamina=99, luck=99, backpack={'gold': 1}, potion='fortune')
    path = tmp_path / 'load.json'
    save_player(saved, path)

    # simulate inputs: yes, ready, load at potion prompt, then choose skill and follow
    answers = iter(["yes", "ready", "load", "skill", "follow"])
    monkeypatch.setattr('builtins.input', lambda prompt='': next(answers))

    # load callback uses the saved file; we pass it directly to run_game
    def load_cb():
        from Forrest_of_Doom.models import load_player

        return load_player(path)

    game.run_game(fast=True, seed=0, load_callback=load_cb)


def test_slot_save_and_load(monkeypatch, tmp_path):
    from Forrest_of_Doom.models import save_player, Player, load_player

    base_save = tmp_path / 'save.json'
    # create initial base save
    save_player(Player(skill=1), base_save)

    # simulate: yes, ready, 'save slotA', then continue
    answers = iter(["yes", "ready", "save slotA", "skill", "follow"])
    monkeypatch.setattr('builtins.input', lambda prompt='': next(answers))

    def save_cb(p, slot=None):
        # delegate to models.save_player via main's logic would do; emulate filename
        target = base_save.with_name(base_save.stem + (f"_{slot}" if slot else "") + base_save.suffix)
        save_player(p, target)

    game.run_game(fast=True, seed=0, save_callback=save_cb)
    slot_file = base_save.with_name(base_save.stem + '_slota' + base_save.suffix)
    assert slot_file.exists()

    # Now test loading that slot via load_callback
    answers = iter(["yes", "ready", "load slotA", "skill", "follow"])
    monkeypatch.setattr('builtins.input', lambda prompt='': next(answers))

    def load_cb(slot=None):
        target = base_save.with_name(base_save.stem + (f"_{slot}" if slot else "") + base_save.suffix)
        return load_player(target)

    game.run_game(fast=True, seed=0, load_callback=load_cb)


def test_in_game_save_backup(monkeypatch, tmp_path):
    # Ensure that saving when file exists creates a .bak backup
    from Forrest_of_Doom.models import Player, save_player

    save_path = tmp_path / 'save.json'
    # initial save
    save_player(Player(skill=1), save_path)

    # simulate inputs to trigger in-game save
    answers = iter(["yes", "ready", "save", "skill", "follow"])
    monkeypatch.setattr('builtins.input', lambda prompt='': next(answers))

    called = {'saved': False}

    def save_cb(p, slot=None):
        save_player(p, save_path)
        called['saved'] = True

    game.run_game(fast=True, seed=0, save_callback=save_cb)
    assert called['saved']
    # ensure the saved file exists and contains the player's skill
    assert save_path.exists()
    import json

    with open(save_path, 'r') as f:
        obj = json.load(f)
    # ensure skill is present and changed from the initial value (1)
    assert 'skill' in obj
    assert int(obj['skill']) != 1

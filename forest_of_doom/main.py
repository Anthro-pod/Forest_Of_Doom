import argparse
from forest_of_doom import game
from pathlib import Path
from forest_of_doom import models


def parse_args():
    parser = argparse.ArgumentParser(description='Forest of Doom - text adventure')
    parser.add_argument('--fast', action='store_true', help='Skip pauses and print text normally')
    parser.add_argument('--seed', type=int, default=None, help='Optional RNG seed for deterministic runs')
    parser.add_argument('--load', type=str, default=None, help='Path to JSON file to load player state from')
    parser.add_argument('--save', type=str, default=None, help='Path to JSON file to save player state to on exit')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    initial_player = None
    if args.load:
        try:
            initial_player = models.load_player(Path(args.load))
        except Exception as e:
            print(f"Failed to load player from {args.load}: {e}")
            return

    # prepare save/load callbacks for in-game save/load
    def save_callback(player, slot=None):
        if not args.save:
            print('No --save path provided; in-game save ignored.')
            return
        p = Path(args.save)
        # support slot by inserting slot name before suffix
        if slot:
            p = p.with_name(p.stem + f"_{slot}" + p.suffix)
        # create timestamped backup if file exists
        if p.exists():
            import shutil
            from datetime import datetime

            bak = p.with_name(p.stem + '.' + datetime.utcnow().strftime('%Y%m%dT%H%M%SZ') + p.suffix + '.bak')
            try:
                p.replace(bak)
            except Exception:
                shutil.copy(p, bak)
        try:
            models.save_player(player, p)
            print(f"Saved player to {p}")
        except Exception as e:
            print(f"Failed to save player to {p}: {e}")

    def load_callback(slot=None):
        if not args.load:
            print('No --load path provided; in-game load ignored.')
            return None
        p = Path(args.load)
        if slot:
            p = p.with_name(p.stem + f"_{slot}" + p.suffix)
        try:
            return models.load_player(p)
        except Exception as e:
            print(f"Failed to load player from {p}: {e}")
            return None

    try:
        final_player = game.run_game(fast=args.fast, seed=args.seed, initial_player=initial_player, save_callback=save_callback, load_callback=load_callback)
    except (KeyboardInterrupt, EOFError):
        print('\nExiting... Goodbye!')
        return

    if args.save and final_player is not None:
        try:
            models.save_player(final_player, Path(args.save))
            print(f"Saved player to {args.save}")
        except Exception as e:
            print(f"Failed to save player to {args.save}: {e}")


if __name__ == '__main__':
    main()

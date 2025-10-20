import sys
import time
from typing import Iterable, Sequence, Optional, Dict, Callable, Any


def slow_print(text: str, delay: float = 0.03, pause: bool = True, fast: bool = False) -> None:
    """Print text slowly. If fast is True, prints normally. If pause is True, waits for Enter.

    Designed to be testable and to handle interrupts gracefully.
    """
    if fast:
        # In fast mode we print normally and skip any pause to avoid blocking/tests
        print(text)
        return

    try:
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()
        if pause:
            try:
                input("Press Enter to continue...")
            except (KeyboardInterrupt, EOFError):
                print()
    except (KeyboardInterrupt, EOFError):
        print("\n[Interrupted]")
        raise


def get_valid_input(prompt: str, valid_options: Sequence[str], special_handlers: Optional[Dict[str, Callable[[str], Any]]] = None) -> str:
    """Prompt until a valid option (case-insensitive) is entered.

    special_handlers is an optional dict mapping specific input strings (lowercase) to
    callables that will be executed when that input is entered. The handler is called
    and the prompt repeats.

    Raises KeyboardInterrupt/EOFError if user interrupts.
    """
    options = [opt.lower() for opt in valid_options]
    handlers = {k.lower(): v for k, v in (special_handlers or {}).items()}
    while True:
        try:
            choice = input(prompt).lower().strip()
        except (KeyboardInterrupt, EOFError):
            raise
        if choice in options:
            return choice
        # exact handler match
        if choice in handlers:
            try:
                handlers[choice](choice)
            except Exception as e:
                print(f"Handler for '{choice}' raised an error: {e}")
            continue
        # prefix handlers: keys ending with '*' match startswith(key[:-1])
        for hk, hv in handlers.items():
            if hk.endswith('*'):
                prefix = hk[:-1]
                if choice.startswith(prefix):
                    try:
                        hv(choice)
                    except Exception as e:
                        print(f"Handler for prefix '{prefix}' raised an error: {e}")
                    break
        else:
            print(f"Please choose one of: {', '.join(valid_options)}")
        print(f"Please choose one of: {', '.join(valid_options)}")


def display_status(player) -> None:
    # Player is expected to have attributes: skill, stamina, luck, backpack, potion
    print(f"\nStatus: Skill: {player.skill}, Stamina: {player.stamina}, Luck: {player.luck}")
    try:
        backpack_items = ', '.join(f'{k}: {v}' for k, v in player.backpack.items())
    except Exception:
        backpack_items = str(player.backpack)
    print(f"Backpack: {backpack_items}")
    if getattr(player, 'potion', None):
        print(f"Potion: {player.potion.capitalize()}")

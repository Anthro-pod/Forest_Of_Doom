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


def display_slate(player) -> None:
    """Display Yaztromo's slate of items (name and price) in a simple, test-friendly format."""
    slate = getattr(player, 'slate', []) or []
    if not slate:
        print("No items available.")
        return
    for item in slate:
        price = item.get('price')
        price_str = f"{price} gold" if price is not None else "(price unset)"
        print(f"- {item.get('name', '<unnamed>')}: {price_str}")


def buy_from_slate(player, index: int) -> tuple[bool, str]:
    """Attempt to buy an item from player's slate by 0-based index.

    Returns (True, message) on success and (False, message) on failure.
    Side effects on success: deducts gold from player.backpack['gold'] and
    appends the item dict to player.inventory.
    """
    slate = getattr(player, 'slate', []) or []
    if not isinstance(index, int):
        return False, "Invalid item index"
    if index < 0 or index >= len(slate):
        return False, "Item index out of range"
    item = slate[index]
    price = item.get('price')
    if price is None:
        return False, "Item has no price set"
    try:
        gold = int(player.backpack.get('gold', 0))
    except Exception:
        return False, "Player has no gold"
    if gold < price:
        return False, "Insufficient gold"
    # Deduct gold and move item to inventory
    player.backpack['gold'] = gold - price
    inv = getattr(player, 'inventory', None)
    if inv is None:
        player.inventory = []
        inv = player.inventory
    # Append a shallow copy of the item to inventory to avoid shared references
    inv.append(dict(item))
    return True, f"Purchased {item.get('name')} for {price} gold"


def use_item(player, index: int) -> tuple[bool, str]:
    """Use an item from the player's inventory by 0-based index.

    Applies a small, deterministic effect for a few known items and removes the
    item from the inventory. Returns (True, msg) on success, (False, msg) on failure.
    """
    inv = getattr(player, 'inventory', []) or []
    if not isinstance(index, int):
        return False, 'Invalid index'
    if index < 0 or index >= len(inv):
        return False, 'Index out of range'
    item = inv.pop(index)
    name = item.get('name', '')
    # Simple effect rules
    if 'Healing' in name:
        try:
            player.stamina += 2
        except Exception:
            pass
        return True, f"You use {name}. Stamina increased."
    if 'Skill' in name:
        try:
            player.skill += 1
        except Exception:
            pass
        return True, f"You use {name}. Skill increased."
    if 'Fortune' in name or 'Luck' in name:
        try:
            player.luck += 1
        except Exception:
            pass
        return True, f"You use {name}. Luck increased."
    # Default: no mechanical effect, but item is consumed
    return True, f"You use {name}."


def shop_loop(player, fast: bool = False, save_handler=None, load_handler=None) -> None:
    """Interactive shop loop. Commands:
    - list: show slate
    - buy <n>: buy item at index n
    - view <n>: show item details
    - use <n>: use item from inventory by index
    - exit: leave shop
    - save / save <slot>: call save_handler
    - load / load <slot>: call load_handler

    This is intentionally minimal and test-friendly.
    """
    def call_save(text: str):
        if save_handler is None:
            print('Save handler not available')
            return
        parts = text.split(maxsplit=1)
        slot = parts[1].strip() if len(parts) > 1 else None
        save_handler(player, slot=slot)

    def call_load(text: str):
        if load_handler is None:
            print('Load handler not available')
            return
        parts = text.split(maxsplit=1)
        slot = parts[1].strip() if len(parts) > 1 else None
        new_p = load_handler(slot=slot) if slot is not None else load_handler()
        if new_p is not None:
            # mutate fields
            player.skill = new_p.skill
            player.stamina = new_p.stamina
            player.luck = new_p.luck
            player.backpack = new_p.backpack
            player.potion = new_p.potion
            player.slate = new_p.slate
            player.inventory = new_p.inventory

    while True:
        try:
            cmd = input('shop> ').strip()
        except (KeyboardInterrupt, EOFError):
            print()
            break
        if not cmd:
            continue
        cmd_l = cmd.lower()
        if cmd_l == 'list':
            slate = getattr(player, 'slate', []) or []
            inv = getattr(player, 'inventory', []) or []
            gold = player.backpack.get('gold', 0)
            print(f"Yaztromo's Slate — You have {gold} gold")
            if not slate:
                print('  (no items)')
            else:
                # column widths
                name_w = max((len(i.get('name', '')) for i in slate), default=10)
                name_w = min(max(name_w, 10), 30)
                print(f"  {'#':>2}  {'Item':{name_w}}   Price")
                print('  ' + '-' * (name_w + 12))
                for i, item in enumerate(slate):
                    price = item.get('price')
                    price_str = f"{price}g" if price is not None else '(unset)'
                    name = item.get('name', '<unnamed>')
                    print(f"  {i:2d}. {name:{name_w}}   {price_str:>6}")
            # show inventory briefly
            print('\nInventory:')
            if not inv:
                print('  (empty)')
            else:
                for i, it in enumerate(inv):
                    print(f"  {i:2d}. {it.get('name')}" )
            continue
        if cmd_l.startswith('buy'):
            parts = cmd.split()
            if len(parts) < 2:
                print('Usage: buy <index>')
                continue
            try:
                idx = int(parts[1])
            except ValueError:
                print('Invalid index')
                continue
            slate = getattr(player, 'slate', []) or []
            if idx < 0 or idx >= len(slate):
                print('Index out of range')
                continue
            item = slate[idx]
            price = item.get('price')
            pname = item.get('name', '<unnamed>')
            if price is None:
                print('Item has no price set')
                continue
            # confirmation prompt
            try:
                resp = input(f"Buy '{pname}' for {price} gold? (yes/no): ").strip().lower()
            except (KeyboardInterrupt, EOFError):
                print()
                continue
            if resp not in ('y', 'yes'):
                print('Purchase cancelled')
                continue
            ok, msg = buy_from_slate(player, idx)
            print(msg)
            continue
        if cmd_l.startswith('view'):
            parts = cmd.split()
            if len(parts) < 2:
                print('Usage: view <index>')
                continue
            try:
                idx = int(parts[1])
            except ValueError:
                print('Invalid index')
                continue
            slate = getattr(player, 'slate', []) or []
            if idx < 0 or idx >= len(slate):
                print('Index out of range')
                continue
            item = slate[idx]
            # detailed view
            print('Item:')
            print(f"  Name : {item.get('name')}")
            print(f"  Price: {item.get('price')}")
            print(f"  Raw  : {item}")
            continue
        if cmd_l.startswith('use'):
            parts = cmd.split()
            if len(parts) < 2:
                print('Usage: use <index>')
                continue
            try:
                idx = int(parts[1])
            except ValueError:
                print('Invalid index')
                continue
            ok, msg = use_item(player, idx)
            print(msg)
            continue
        if cmd_l == 'exit':
            break
        if cmd_l.startswith('save'):
            call_save(cmd)
            continue
        if cmd_l.startswith('load'):
            call_load(cmd)
            continue
    print('Unknown command. Try: list, buy <n>, view <n>, use <n>, save, load, exit')

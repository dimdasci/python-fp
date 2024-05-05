from typing import Tuple

from src.core import GameState, move, render_state, take

COMMANDS = {"move": move, "take": take}


def mainloop(state: GameState) -> None:
    while True:
        state = step(state)


def step(state: GameState) -> GameState:
    print(render_state(state))

    try:
        cmd, arg = parse_line(input("> "))
        new_state = dispatch(state, cmd, arg)
        print("OK.")
        return new_state

    except ValueError as e:
        print(e)
        return state


def parse_line(line: str) -> Tuple[str, str]:
    parts = line.strip().split(" ", 1)
    if len(parts) != 2 or parts[0] not in COMMANDS:
        raise ValueError("Expected take <item> or move <direction> commands.")
    cmd, arg = parts
    return (cmd, arg)


def dispatch(state: GameState, cmd: str, arg: str) -> GameState:
    new_state = COMMANDS[cmd](state, arg)
    if new_state is None:
        raise ValueError("You can't do that.")
    else:
        print("OK.")
        return new_state

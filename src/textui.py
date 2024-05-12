import sys
from typing import Tuple

from effect import Effect
from effect.do import do
from effect.io import Display, Prompt

from src.core import GameState, move, render_state, take
from src.storage import SaveGame

COMMANDS = {"move": move, "take": take}


@do
def mainloop(state: GameState):
    while True:
        state = yield step(state)
        yield Effect(SaveGame(state=state))


def display(o):
    return Effect(Display(o))


@do
def step(state: GameState):
    yield display(render_state(state))

    try:
        user_input = yield Effect(Prompt("> "))
        cmd, arg = parse_line(user_input)
        new_state = dispatch(state, cmd, arg)
        yield display("OK.")
        return new_state
    except (EOFError, KeyboardInterrupt):
        yield display("Goodbye.")
        sys.exit(0)
    except ValueError as e:
        yield display(str(e))
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
        return new_state

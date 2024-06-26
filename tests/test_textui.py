from src.setup import initial_state, rusty_key
from src.textui import parse_line, dispatch, step, mainloop
from src.storage import SaveGame
from src.core import render_state
from pytest import raises
from effect.testing import noop, perform_sequence, raise_
from effect.io import Display, Prompt

in_street = initial_state.set(location_name="Street")


def test_parse_line():
    assert parse_line("move east") == ("move", "east")
    assert parse_line("take Rusty Key") == ("take", "Rusty Key")
    assert parse_line("move somewhere") == ("move", "somewhere")

def test_parse_line_exception():
    # pytest expects an exception of the ValueError type to be raised
    with raises(ValueError) as err:
        parse_line("move")
    assert "Expected" in str(err.value)

def test_dispatch():
    with_key = in_street.transform(
        ["inventory"], [rusty_key], # rusty_key is in the inventory
        ["world", "Street", "items"], {} # remove rusty_key from the street
    )

    assert dispatch(initial_state, "move", "east") == in_street
    assert dispatch(in_street, "take", "Rusty Key") == with_key

def test_dispatch_exception():
    with raises(ValueError) as err:
        dispatch(initial_state, "move", "up")
    assert "You can't do that" in str(err.value)
    with raises(ValueError) as err:
        dispatch(initial_state, "take", "Rusty Key")
    assert "You can't do that" in str(err.value)

from unittest.mock import patch

# @patch("src.textui.print")
# @patch("src.textui.input")
# def test_step(mock_input, mock_print):
#     mock_input.side_effect = ["move east", "take Rusty Key"]

#     state = step(initial_state)
#     in_street = initial_state.set(location_name="Street")

#     assert state == in_street
#     mock_input.assert_called_once_with("> ")
#     mock_print.assert_any_call(render_state(initial_state))
#     mock_print.assert_any_call("OK.")

#     state = step(in_street)
#     with_key = in_street.transform(
#         ["inventory"], [rusty_key], # rusty_key is in the inventory
#         ["world", "Street", "items"], {} # remove rusty_key from the street
#     )
#     assert state == with_key

def test_step():
    expected_effects = [
        (Display(render_state(initial_state)), noop),
        (Prompt("> "), lambda _: "move east"),
        (Display("OK."), noop),
    ]
    eff = step(initial_state)
    result = perform_sequence(expected_effects, eff)
    assert result == in_street

def test_step_bad_command():
    expected_effects = [
        (Display(render_state(initial_state)), noop),
        (Prompt("> "), lambda _: "move up"),
        (Display("You can't do that."), noop),
    ]
    eff = step(initial_state)
    result = perform_sequence(expected_effects, eff)
    assert result == initial_state

def test_quit_game():
    for exc in [EOFError()]:
        expected_effects = [
            (Display(render_state(initial_state)), noop),
            (Prompt("> "), lambda _: raise_(exc)),
            (Display("Goodbye."), noop),
        ]
        eff = step(initial_state)
        with raises(SystemExit):
            perform_sequence(expected_effects, eff)

def test_main_loop():
    expected_effects = [
        (Display(render_state(initial_state)), noop),
        (Prompt("> "), lambda _: "move east"),
        (Display("OK."), noop),
        (SaveGame(state=in_street), noop),
        (Display(render_state(in_street)), noop),
        (Prompt("> "), lambda _: raise_(EOFError())),
        (Display("Goodbye."), noop),
    ]
    eff = mainloop(initial_state)
    with raises(SystemExit):
        perform_sequence(expected_effects, eff)
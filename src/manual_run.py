from toolz.functoolz import thread_first

from src.core import move, multimove, render_state, take
from src.setup import initial_state


def main():
    # print(render_state(initial_state))
    # print("\n>> You go east >>\n")
    # state = move(initial_state, "east")
    # state = take(state, "Rusty Key")
    # print(render_state(state))
    # print("\n>> You go west >>\n")
    # state = move(state, "west")
    # print(render_state(state))
    # print("\n>> You go down >>\n")
    # state = move(state, "down")
    # print(render_state(state) if state is not None else "You can't go there")

    # Option with reduce function multimove
    solution = multimove(
        take(move(initial_state, "east"), "Rusty Key"), ["west", "down"]
    )

    # Option with thread_first
    solution = thread_first(
        initial_state,
        (move, "east"),
        (take, "Rusty Key"),
        (multimove, ["west", "down"]),
    )
    print(render_state(solution) if solution is not None else "You can't go there")


if __name__ == "__main__":
    main()

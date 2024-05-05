from effect import (
    ComposedDispatcher,
    Effect,
    TypeDispatcher,
    base_dispatcher,
    sync_perform,
    sync_performer,
)
from effect.do import do


def compliment(name: str) -> str:
    return f"Hello, {name}! You look amazing today!"


@do
def main():
    name = yield Effect(Input("You name: "))
    yield (Effect(Print(compliment(name))))


class Input:
    def __init__(self, prompt: str):
        self.prompt = prompt

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Input) and self.prompt == other.prompt


class Print:
    def __init__(self, message: str):
        self.message = message

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Print) and self.message == other.message


@sync_performer
def perform_input(dispatcher, intent: Input):
    return input(intent.prompt)


@sync_performer
def perform_print(dispatcher, intent: Print):
    print(intent.message)


io = TypeDispatcher({Input: perform_input, Print: perform_print})
dispatcher = ComposedDispatcher([io, base_dispatcher])


from effect.testing import SequenceDispatcher


def test_main():
    seq = SequenceDispatcher(
        [
            (Input("Your name: "), lambda _: "Alice"),
            (Print("Hello, Alice! You look amazing today!"), lambda _: None),
        ]
    )
    with seq.consume():
        sync_perform(ComposedDispatcher([seq, base_dispatcher]), main())


test_main()

# if __name__ == "__main__":
#     sync_perform(dispatcher, main())

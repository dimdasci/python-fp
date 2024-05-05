from src.setup import initial_state
from src.textui import mainloop
from src.storage import connect_db, initialize
from effect import sync_perform
from effect.io import stdio_dispatcher
from effect import base_dispatcher, ComposedDispatcher

def startup():
    conn = connect_db()
    save, state = initialize(conn)
    if state is None:
        state = initial_state
        print("New game.")
    else:
        print("Continue the game.")
    return save, state

if __name__ == "__main__":
    dispatcher = ComposedDispatcher([stdio_dispatcher, base_dispatcher])

    save, state = startup()
    main_eff = mainloop(save, state)
    sync_perform(dispatcher, main_eff)
    
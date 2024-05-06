from src.setup import initial_state
from src.textui import mainloop
from src.storage import connect_db, initialize, sqlite_dispatcher
from effect import sync_perform
from effect.io import stdio_dispatcher
from effect import base_dispatcher, ComposedDispatcher

def startup():
    conn = connect_db()
    state = initialize(conn)
    if state is None:
        state = initial_state
        print("New game.")
    else:
        print("Continue the game.")
    st_dispatcher = sqlite_dispatcher(conn)
    return st_dispatcher, state

if __name__ == "__main__":
    st_dispatcher, state = startup()
    dispatcher = ComposedDispatcher([stdio_dispatcher, base_dispatcher, st_dispatcher])
    main_eff = mainloop(state)
    sync_perform(dispatcher, main_eff)
    
from src.setup import initial_state
from src.textui import mainloop
from src.storage import connect_db, initialize

if __name__ == "__main__":
    conn = connect_db()
    save, state = initialize(conn)
    if state is None:
        state = initial_state
        print("New game.")
    else:
        print("Continue the game.")
    mainloop(save, state)

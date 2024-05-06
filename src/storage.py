import json
from functools import partial
from pyrsistent import pmap, pvector, PMap, PClass, field
from sqlite3 import connect
from src.setup import initial_state
from src.core import GameState, Thing, Location
from effect import sync_performer, TypeDispatcher

class SaveGame(PClass):
    state = field(type=GameState)


DB_NAME = "game.db" 

# SQL Constants
CREATE_LOCATION = """
CREATE TABLE IF NOT EXISTS location (name text primary key, description text, exits blob, items blob)
"""

CREATE_STATE = """
CREATE TABLE IF NOT EXISTS state (location_name text, inventory blob)
"""

INSERT_LOCATION = """
INSERT OR REPLACE INTO location (name, description, exits, items) VALUES (?, ?, ?, ?)
"""

INSERT_STATE = """
INSERT OR REPLACE INTO state (location_name, inventory) VALUES (?, ?)
"""

DELETE_STATE = """
DELETE FROM state
"""

SELECT_STATE = """
SELECT location_name, inventory FROM state
"""

SELECT_LOCATION = """
SELECT name, description, exits, items FROM location
"""

def setup(cursor):
    cursor.execute(CREATE_LOCATION)
    cursor.execute(CREATE_STATE)

def save_state(cursor, state):
    cursor.execute(DELETE_STATE)
    cursor.execute(INSERT_STATE, serialize_state(state))
    for params in serialize_world(state):
        cursor.execute(INSERT_LOCATION, params)

def serialize_world(state):
    return map(serialize_location, state.world.values())

def serialize_location(loc):
    items = json.dumps([x for x in loc.items.keys()])
    exits = serialize_exits(loc.exits)
    return (loc.name, loc.description, exits, items)        

def serialize_state(state):
    return (state.location_name, json.dumps([x.name for x in state.inventory]))

def serialize_exits(exits):
    return json.dumps([
        [direction, key.name if key is not None else None, destination] 
        for direction, (key, destination) in exits.items()
    ])

def load_state(cursor): 
    world = load_world(cursor.execute(SELECT_LOCATION))
    state_row = cursor.execute(SELECT_STATE).fetchone()
    return load_game_state(state_row, world) if state_row is not None else None

def load_game_state(state_row: list[str], world: PMap):
    return GameState(
        location_name=state_row[0],
        world=world,
        inventory=pvector([Thing(name=x) for x in json.loads(state_row[1])])
    )

def load_world(rows: list[list[str]]):
    return pmap({row[0]: load_location(row) for row in rows})


def load_location(row):
    name, description, exits_raw, items_raw = row

    return Location(
        name=name,
        description=description,
        exits=deserialize_exits(exits_raw),
        items=pmap({x: Thing(name=x) for x in json.loads(items_raw)})
    )

def deserialize_exits(exits):
    return pmap({
        direction: (Thing(name=key) if key is not None else None, destination)
        for direction, key, destination in json.loads(exits)
    })

def connect_db():
    return connect(DB_NAME)

def initialize(conn):
    cursor = conn.cursor()
    setup(cursor)
    conn.commit()

    return load_state(cursor)

@sync_performer
def perform_save_game_sqlite(conn, dispatcher, save_game):
    save_state(conn.cursor(), save_game.state)
    conn.commit()

def sqlite_dispatcher(conn):
    return TypeDispatcher({SaveGame: partial(perform_save_game_sqlite, conn)})

if __name__ == "__main__":
    with connect("game.db") as conn:
        cursor = conn.cursor()
        save_state(cursor, initial_state)

        assert load_state(cursor) == initial_state
        print("Ok")
        conn.commit()


from pyrsistent import pmap

from src.core import GameState, Location, Thing

rusty_key = Thing(name="Rusty Key")

home = Location(
    name="Home",
    description="You are at home",
    exits=pmap({"east": (None, "Street"), "down": (rusty_key, "Basement")}),
)
street = Location(
    name="Street",
    description="You are on the street",
    exits=pmap({"west": (None, "Home")}),
    items=pmap({rusty_key.name: rusty_key}),
)
basement = Location(
    name="Basement",
    description="You are in the basement",
    exits=pmap({"up": (None, "Home")}),
)
world = pmap({x.name: x for x in [home, street, basement]})
initial_state = GameState(location_name=home.name, world=world)

from functools import reduce

from pyrsistent import PClass, field, pmap_field, pvector_field


class Thing(PClass):
    name = field(type=str)


class Location(PClass):
    name = field(type=str)
    description = field(type=str)
    exits = pmap_field(str, tuple)  # direction_name -> (required_thing, location_name)
    items = pmap_field(str, Thing)  # item_name -> Thing


class GameState(PClass):
    location_name = field(type=str)
    world = pmap_field(str, Location)  # location_name -> Location
    inventory = pvector_field(Thing)

    @property
    def location(self):
        return self.world[self.location_name]


ROOM_FORMAT = """
* {name} *
{description}

Exits:
{exits}

Items:
{items}

Your inventory:
{inventory}
"""


def render_state(state: GameState) -> str:
    def render_exit(exit_name, key, destination) -> str:
        desc = f"* {exit_name} to {destination}"
        return desc + " (locked) " if key is not None else desc

    exits = "\n".join(
        render_exit(exit_name, key, destination)
        for exit_name, (key, destination) in state.location.exits.items()
    )

    items = ", ".join(state.location.items.keys())
    inventory = ", ".join(x.name for x in state.inventory)

    return ROOM_FORMAT.format(
        name=state.location.name,
        description=state.location.description,
        exits=exits,
        items=items,
        inventory=inventory,
    )


def move(state: GameState, direction: str) -> GameState:
    if direction not in state.location.exits:
        return None
    (required_thing, new_location_name) = state.location.exits[direction]
    if required_thing is not None and required_thing not in state.inventory:
        return None
    return state.set(location_name=new_location_name)


def take(state: GameState, item_name: str) -> GameState:
    item = state.location.items.get(item_name)
    if item is None:
        return None
    # we can use transform method instead of the following code
    return state.transform(
        ["inventory"],
        lambda inventory: inventory.append(item),
        ["world", state.location.name, "items"],
        lambda items: items.remove(item_name),
    )
    # new_items = state.location.items.remove(item_name)
    # new_location = state.location.set(items=new_items)
    # new_inventory = state.inventory.append(item)
    # new_world = state.world.set(new_location.name, new_location)
    # return GameState(location=new_location, world=new_world, inventory=new_inventory)


def multimove(state: GameState, directions: list[str]) -> GameState:
    return reduce(move, directions, state)

from pyrsistent import pvector, v, freeze, thaw
from toolz import curry

vec = pvector([1, 2, 3])
print(vec)

vec2 = v(1, 2, 3)
print(vec2)

d = { "sublist": [{1, 2, 4}, {3, 4, 5}]}
fd = freeze(d)
print(fd)

print(thaw(fd))

@curry
def add(x, y):
    return x + y

print(add(1))
print(add(1)(2))

from toolz.dicttoolz import merge, assoc, dissoc

d1 = { "a": 1, "b": 2 }
d2 = { "b": 3, "c": 4 }

print(merge(d1, d2))
print(assoc(d1, "a", 2))
print(dissoc(d1, "a"))

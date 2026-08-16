"""Import-only compatibility surface for the historical Omega verifier.

The historical verifier imports only ``JC_REPRESENTATIVES`` from the much
larger discovery probe of the same module name.  That discovery probe imports
python-flint for finite-field searches that the Omega proof never executes.
Keeping this exact constant in a separate leading ``PYTHONPATH`` entry lets a
fresh release replay the historical symbolic proof without installing an
unused compiled discovery dependency.

``verify_orbit_constant.py`` parses the frozen discovery source and proves
that this tuple is byte-independent but value-identical before the shim is
used.
"""

from itertools import permutations

JC_REPRESENTATIVES = (
    (0, 0, 0, 0),
    (0, 0, 1, 1),
    (0, 1, 0, 1),
    (0, 1, 1, 0),
    (0, 1, 2, 3),
    (1, 0, 0, 1),
    (1, 0, 1, 0),
    (1, 0, 2, 3),
    (1, 1, 0, 0),
    (1, 1, 1, 1),
    (1, 1, 2, 2),
    (1, 2, 0, 3),
    (1, 2, 1, 2),
    (1, 2, 2, 1),
    (1, 2, 3, 0),
)


def canonical_character_orbit(assignment):
    images = []
    for perm in permutations((1, 2, 3)):
        mapping = {0: 0, 1: perm[0], 2: perm[1], 3: perm[2]}
        images.append(tuple(mapping[value] for value in assignment))
    return min(images)


ORBIT_INDEX = {}
for assignment in (
    (a, b, c, a ^ b ^ c)
    for a in range(4)
    for b in range(4)
    for c in range(4)
):
    canonical = canonical_character_orbit(assignment)
    ORBIT_INDEX[assignment] = JC_REPRESENTATIVES.index(canonical)

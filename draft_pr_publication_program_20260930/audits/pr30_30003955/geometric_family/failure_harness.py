#!/usr/bin/env python3
"""Intentional failure: a noninterlaced dual-pair mutant cannot be a torus.

Run separately; expected exit is nonzero. Never describe this as a PASS run.
The correct model and controls live in geometric_controls.py.
"""
from geometric_controls import ribbon_surface
mutant = ribbon_surface([['ap', 'am', 'bp', 'bm']], [('ap', 'am'), ('bp', 'bm')])
assert (mutant['genus'], mutant['boundary']) == (1, 1), 'INTENTIONAL_MUTANT: noninterlaced rotations are pants, not a one-holed torus'

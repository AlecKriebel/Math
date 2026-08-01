#!/usr/bin/env python3
"""Primitive exact chart for the dense local-type block ``(00,00,00)``.

The three local highest-weight vectors of type ``00`` each contain eighteen
raw words, so expanding their tensor cube is needlessly expensive.  This
small 27-by-2 integer chart is independently derived and checked by
``verify_dth_gamma5_000_dense.py`` using exact dense rational coordinates.
"""


RAW_RANK = 27
SUPPORT_RANK = 2
DELTA_RANK = 0
FACE_RANK = 2
PIVOT_ROWS = (1, 3)

PRIMITIVE_CHART = (
    (0, 0),
    (4, 2),
    (2, 1),
    (-2, -4),
    (2, -2),
    (2, 1),
    (-1, -2),
    (-1, -2),
    (-1, 1),
    (-2, 2),
    (2, 4),
    (2, 1),
    (-4, -2),
    (0, 0),
    (2, 1),
    (-1, -2),
    (-1, -2),
    (1, -1),
    (-1, 1),
    (-1, 1),
    (-1, -2),
    (-1, 1),
    (-1, 1),
    (1, 2),
    (2, 1),
    (-2, -1),
    (0, 0),
)

assert len(PRIMITIVE_CHART) == RAW_RANK
assert all(len(row) == FACE_RANK for row in PRIMITIVE_CHART)
assert (PRIMITIVE_CHART[PIVOT_ROWS[0]][0]
        * PRIMITIVE_CHART[PIVOT_ROWS[1]][1]
        - PRIMITIVE_CHART[PIVOT_ROWS[0]][1]
        * PRIMITIVE_CHART[PIVOT_ROWS[1]][0]) == -12

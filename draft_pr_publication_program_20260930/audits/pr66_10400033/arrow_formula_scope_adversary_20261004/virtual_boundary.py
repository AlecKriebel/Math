#!/usr/bin/env python3
"""Check the explicit virtual RIII counterexample to the formal extension."""
from fractions import Fraction
import json

P = ((3, 0), (5, 1), (2, 4))
T = ((3, 0), (1, 4), (5, 2))

def matches(pattern, image):
    return any({((t + k) % 6, (h + k) % 6) for t, h in pattern} == set(image)
               for k in range(6))

def virtual_closure_gauss(word, bottom_to_top):
    current = [0, 1, 2]
    histories = [[], [], []]
    for crossing, generator in enumerate(word):
        i = generator - 1
        histories[current[i]].append((crossing, 'tail'))
        histories[current[i + 1]].append((crossing, 'head'))
        current[i], current[i + 1] = current[i + 1], current[i]
    bottom_position = {origin: pos for pos, origin in enumerate(current)}
    order = []
    origin = 0
    while origin not in order:
        order.append(origin)
        origin = bottom_to_top[bottom_position[origin]]
    assert origin == 0 and len(order) == 3
    sequence = [item for strand in order for item in histories[strand]]
    arrows = [(next(i for i, pair in enumerate(sequence) if pair == (c, 'tail')),
               next(i for i, pair in enumerate(sequence) if pair == (c, 'head')))
              for c in range(len(word))]
    value = Fraction(1, 2) if matches(P, arrows) else Fraction(1) if matches(T, arrows) else Fraction(0)
    return {'word':word, 'bottom_strand_origins':current,
            'strand_traversal_order':order, 'tail_head_sequence':sequence,
            'arrows':arrows, 'formal_value':str(value)}

closure = [0, 2, 1]
left = virtual_closure_gauss([1, 2, 1], closure)
right = virtual_closure_gauss([2, 1, 2], closure)
assert left['arrows'] == [(0, 2), (1, 4), (3, 5)]
assert right['arrows'] == [(2, 4), (0, 5), (1, 3)]
assert left['formal_value'] == '1/2' and right['formal_value'] == '0'
assert left['bottom_strand_origins'] == right['bottom_strand_origins']
print(json.dumps({'status':'PASS', 'left':left, 'right':right,
                  'crossing_signs':[1,1,1], 'bottom_to_top_virtual_closure':closure,
                  'deduction':'The positive braid RIII relation 121=212 holds inside a fixed virtual closure, which has one component. The formal arrow evaluation changes from 1/2 to 0, so it is not a virtual-knot invariant.'}, indent=2))

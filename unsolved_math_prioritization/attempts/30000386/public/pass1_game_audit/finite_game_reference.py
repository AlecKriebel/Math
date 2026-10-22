"""Exact finite-horizon two-dimensional Time-Bomb decision game.
Deliberately no symmetry quotient or search pruning. Suitable for tiny horizons.
This is an executable specification, not a claim of an infinite strategy.
"""
from functools import lru_cache
from itertools import product
from pathlib import Path
import json

MOVES = tuple(product((-1, 0, 1), repeat=2))

def relevant(qx, qy, k, h):
    return 1 <= k <= h and max(abs(qx), abs(qy)) <= k

@lru_cache(None)
def cone(h):
    return tuple((x, y, k) for k in range(1, h+1)
                 for x in range(-k, k+1) for y in range(-k, k+1))

def shift(B, move, h):
    sx, sy = move
    return frozenset((x-sx, y-sy, k-1) for x, y, k in B
                     if relevant(x-sx, y-sy, k-1, h))

@lru_cache(None)
def wins(h, B):
    if h == 0:
        return True
    for sx, sy in MOVES:  # Angel observes old bombs and moves first.
        if (sx, sy, 1) in B:
            continue
        C = shift(B, (sx, sy), h-1)
        # Null = any expired, post-horizon, or unreachable announcement.
        if not wins(h-1, C):
            continue
        # Devil observes this move, then chooses one of ALL effective bombs.
        if all(wins(h-1, C | {d}) for d in cone(h-1)):
            return True
    return False

def geometry_check():
    verified = 0
    min_slack = 100
    for mask in range(1, 1 << 9):
        Q = [MOVES[i] for i in range(9) if mask >> i & 1]
        C = {(x+dx, y+dy) for x, y in Q for dx, dy in MOVES}
        r, c = len({y for _, y in Q}), len({x for x, _ in Q})
        if len(C) < len(Q)+2*r+2*c+4:
            raise RuntimeError('Expansion lower bound failed')
        if len(C) < 2*len(Q)+7:
            raise RuntimeError('Covering-union lower bound failed')
        min_slack = min(min_slack, len(C)-(2*len(Q)+7))
        verified += 1
    return {'nonempty_center_subsets_verified': verified, 'minimum_union_bound_slack': min_slack}

if __name__ == '__main__':
    rows = []
    for h in range(1, 5):
        rows.append({'horizon': h, 'angel_wins': wins(h, frozenset()),
                     'cone_pairs': len(cone(h)), 'cache_states_so_far': wins.cache_info().currsize})
    out = {'model': 'Full 2D adaptive game, Angel first, only previous announcements lethal',
           'finite_horizons': rows, 'geometry': geometry_check(),
           'scope': 'Executable finite-game specification and small smoke tests; survival through17 is proved analytically.'}
    Path(__file__).with_name('finite_game_smoke_tests.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))

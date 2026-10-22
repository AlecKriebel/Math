"""Independent finite falsification controls, not an asymptotic proof.

No candidate code is imported or executed. Standard library only; no network.
Writes one JSON result in this script's directory. Exhaustive counts are actual.
"""
from collections import deque
from datetime import datetime, timezone
from fractions import Fraction
from itertools import combinations, product
from math import comb, e
from pathlib import Path
import json


def forward_edges(w, h):
    return tuple(((x, y), (x + 1, y)) for x in range(w) for y in range(h + 1)) + tuple(
        ((x, y), (x, y + 1)) for x in range(w + 1) for y in range(h)
    )


def neighbors(v, n):
    x, y = v
    for a, b in ((x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)):
        if 0 <= a <= n and 0 <= b <= n:
            yield (a, b)


def simple_paths(n):
    def visit(path, used):
        v = path[-1]
        if v == (n, n):
            yield tuple(path)
            return
        for u in neighbors(v, n):
            if u not in used:
                yield from visit(path + [u], used | {u})
    yield from visit([(0, 0)], {(0, 0)})


def backward(a, b):
    return sum(b) < sum(a)


def slices(path, length):
    result = []
    left = 0
    target = length
    for j in range(1, len(path)):
        if sum(path[j]) == target:
            result.append(path[left:j + 1])
            left = j
            target += length
    if left < len(path) - 1:
        result.append(path[left:])
    return result


def monotone_walk(a, b):
    assert a[0] <= b[0] and a[1] <= b[1]
    path = [a]
    while path[-1][0] < b[0]:
        x, y = path[-1]
        path.append((x + 1, y))
    while path[-1][1] < b[1]:
        x, y = path[-1]
        path.append((x, y + 1))
    return path


def segment_record(seg, h):
    start, end = seg[0], seg[-1]
    b = sum(backward(a, c) for a, c in zip(seg, seg[1:]))
    i, next_i = start[0] // h, end[0] // h
    s = b // h
    a = (s + 1) * h
    lo = (i * h - a, sum(start) - (i + 1) * h - a)
    hi = ((next_i + 1) * h + a, sum(end) - next_i * h + a)
    w, height = hi[0] - lo[0], hi[1] - lo[1]
    return dict(b=b, i=i, next_i=next_i, s=s, a=a, lo=lo, hi=hi,
                w=w, height=height, tau=sum(end) - sum(start))


def geometry_controls():
    totals = dict(paths=0, parameterized_paths=0, segments=0,
                  negative_endpoint_displacements=0, short_last_segments=0,
                  bad_segments=0)
    for n in (1, 2, 3):
        for path in simple_paths(n):
            totals['paths'] += 1
            for h, m in product((1, 2, 3), (1, 2, 3, 4)):
                length = m * h
                segs = slices(path, length)
                assert len(segs) == (2 * n + length - 1) // length
                totals['parameterized_paths'] += 1
                recs = []
                for j, seg in enumerate(segs):
                    r = segment_record(seg, h)
                    recs.append(r)
                    totals['segments'] += 1
                    assert all(r['lo'][d] <= v[d] <= r['hi'][d]
                               for v in seg for d in (0, 1))
                    assert r['w'] > h and r['height'] > h
                    assert r['w'] + r['height'] == r['tau'] + 2 * h + 4 * r['a']
                    z = r['next_i'] - r['i']
                    assert -r['s'] - 2 <= z <= m + r['s'] + 2
                    assert r['a'] > r['b']
                    if seg[-1][0] < seg[0][0] or seg[-1][1] < seg[0][1]:
                        totals['negative_endpoint_displacements'] += 1
                    if j < len(segs) - 1 and r['s'] == 0:
                        assert r['w'] == (z + 3) * h
                        assert r['height'] == (m - z + 3) * h
                        assert -2 <= z <= m + 2
                    else:
                        totals['bad_segments'] += 1
                if recs[-1]['tau'] < length:
                    totals['short_last_segments'] += 1
                total_b = sum(r['b'] for r in recs)
                bad = [r for j, r in enumerate(recs)
                       if r['s'] or j == len(recs) - 1]
                assert len(bad) <= sum(r['s'] for r in recs) + 1
                assert sum(r['w'] + r['height'] for r in bad) <= (
                    (m + 10) * total_b + length + 6 * h)
    return totals


def witness_controls():
    n = 2
    edge_list = forward_edges(n, n)
    paths = tuple(simple_paths(n))
    totals = dict(mark_configurations=1 << len(edge_list), paths=len(paths),
                  parameterized_path_configurations=0, segment_certificates=0,
                  positive_certificates=0, negative_segments=0,
                  nonnegative_path_count_controls=0)
    for mask in range(1 << len(edge_list)):
        marks = {edge for i, edge in enumerate(edge_list) if mask >> i & 1}
        for path in paths:
            k = sum((a, b) in marks for a, b in zip(path, path[1:]))
            back = sum(backward(a, b) for a, b in zip(path, path[1:]))
            if back <= k:
                starts = [(0, 0)] + [a for a, b in zip(path, path[1:])
                                      if (a, b) in marks] + [(n, n)]
                for d in (0, 1):
                    variation = sum(max(0, a[d] - b[d])
                                    for a, b in zip(starts, starts[1:]))
                    assert variation <= back <= k
                totals['nonnegative_path_count_controls'] += 1
            for h, m in ((1, 1), (1, 2), (2, 1), (2, 2)):
                totals['parameterized_path_configurations'] += 1
                witnesses = []
                rewards = []
                for seg in slices(path, h * m):
                    r = segment_record(seg, h)
                    witness = {(a, b) for a, b in zip(seg, seg[1:])
                               if (a, b) in marks}
                    reward = len(witness) - r['b']
                    rewards.append(max(0, reward))
                    totals['negative_segments'] += reward < 0
                    if reward <= 0:
                        witness = set()
                    else:
                        totals['positive_certificates'] += 1
                        padded = (monotone_walk(r['lo'], seg[0])[:-1] + list(seg)
                                  + monotone_walk(seg[-1], r['hi'])[1:])
                        min_reward = sum(-1 if backward(a, b) else int((a, b) in witness)
                                         for a, b in zip(padded, padded[1:]))
                        assert min_reward >= reward
                        assert all(r['lo'][d] <= v[d] <= r['hi'][d]
                                   for v in padded for d in (0, 1))
                    for previous in witnesses:
                        assert not previous & witness
                    witnesses.append(witness)
                    totals['segment_certificates'] += 1
                assert sum(rewards) >= k - back
    return totals


def reward(w, h, marks):
    # Original corner reward equals w+h minus directed 0/1 shortest cost.
    origin, end = (0, 0), (w, h)
    dist = {origin: 0}
    pending = deque([origin])
    while pending:
        a = pending.popleft()
        x, y = a
        for b in ((x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)):
            if not (0 <= b[0] <= w and 0 <= b[1] <= h):
                continue
            cost = 0 if backward(a, b) or (a, b) in marks else 1
            value = dist[a] + cost
            if value < dist.get(b, 10 ** 9):
                dist[b] = value
                if cost:
                    pending.append(b)
                else:
                    pending.appendleft(b)
    return w + h - dist[end]


def strict_chain(marks):
    positions = sorted(a for a, _ in marks)
    best = []
    for j, a in enumerate(positions):
        best.append(1 + max([best[i] for i in range(j)
                             if positions[i][0] < a[0] and positions[i][1] < a[1]] or [0]))
    return max(best or [0])


def stability_controls():
    w, h, max_marks = 6, 6, 2
    edges = forward_edges(w, h)
    tested = 0
    for k in range(max_marks + 1):
        for selected in combinations(edges, k):
            positions = [a for a, _ in selected]
            if any(abs(a[d] - b[d]) <= max_marks
                   for a, b in combinations(positions, 2) for d in (0, 1)):
                continue
            assert reward(w, h, set(selected)) == strict_chain(selected)
            tested += 1
    ties = {((0, 0), (1, 0)), ((1, 0), (2, 0))}
    assert reward(2, 1, ties) == 2 and strict_chain(ties) == 1
    return dict(rectangle=[w, h], max_marks=max_marks,
                exhaustive_separated_mark_sets=tested,
                tie_control=dict(reward=2, strict_chain=1,
                                 meaning='Separation is necessary; raw strict-chain equality fails.'))


def bk_controls():
    # All twenty increasing events on three coordinates, including impossible/always.
    configs = tuple(range(8))
    events = []
    for event in range(256):
        inside = [v for v in configs if event >> v & 1]
        if all((event >> b & 1) for a in inside for b in configs if a & b == a):
            minimal = tuple(v for v in inside if not any(u != v and u & v == u for u in inside))
            events.append((event, minimal))
    assert len(events) == 20
    qs = (Fraction(1, 7), Fraction(1, 2), Fraction(3, 4))
    probs = [[sum((q ** v.bit_count()) * ((1 - q) ** (3 - v.bit_count()))
                  for v in configs if event >> v & 1) for event, _ in events] for q in qs]
    inequalities = 0
    for i, j, k in product(range(len(events)), repeat=3):
        occurrence = set()
        for a, b, c in product(events[i][1], events[j][1], events[k][1]):
            if not (a & b or a & c or b & c):
                union = a | b | c
                occurrence.update(v for v in configs if union & v == union)
        for q_index, q in enumerate(qs):
            lhs = sum(q ** v.bit_count() * (1 - q) ** (3 - v.bit_count())
                      for v in occurrence)
            assert lhs <= probs[q_index][i] * probs[q_index][j] * probs[q_index][k]
            inequalities += 1
    return dict(coordinates=3, increasing_events=len(events),
                ordered_event_triples=len(events) ** 3,
                q_values=[str(q) for q in qs], exact_rational_inequalities=inequalities)


def count_controls():
    tested = 0
    for n in range(1, 7):
        for k in range(1, 6):
            actual = sum(sum(max(0, a - b) for a, b in zip((0,) + xs + (n,), xs + (n,))) <= k
                         for xs in product(range(n + 1), repeat=k))
            bound = sum(comb(k + 1, t) * comb(k, t) * comb(n + 2 * k - t, k - t)
                        for t in range(k + 1))
            assert actual <= bound
            tested += 1
    low = 2 * e ** 2 * (3 / 2) ** 6 / 32 ** 2
    high = 32 * e ** 2 * 10 ** -6 * 6 ** 2
    assert low < 1 / 4 and high < 1 / 4
    return dict(exhaustive_coordinate_count_pairs=tested,
                low_range_base_upper=low, high_range_base_upper=high)


def main():
    results = dict(timestamp_utc=datetime.now(timezone.utc).isoformat(),
                   status='PASS', proof_status='Finite controls only; not an asymptotic proof.',
                   command_role='python3 -I -S -B AUDIT/check_controls.py',
                   geometry=geometry_controls(), witnesses=witness_controls(),
                   sparse_stability=stability_controls(), product_bk=bk_controls(),
                   marked_list_counts=count_controls())
    path = Path(__file__).resolve().with_name('CONTROL_RESULTS.json')
    path.write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()

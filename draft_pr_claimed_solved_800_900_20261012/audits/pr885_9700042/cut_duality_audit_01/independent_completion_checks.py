"""Independently authored C4 deterministic completion diagnostics.

No original code is imported. Explicit exceptions remain active under -O.
This supplements, and does not replace, the frozen analytical derivation.
"""
import heapq
import itertools
import json


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def paths(N):
    def extend(v, seen, chain):
        if v == (N, N):
            yield chain
            return
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            w = (v[0] + dx, v[1] + dy)
            if 0 <= w[0] <= N and 0 <= w[1] <= N and w not in seen:
                yield from extend(w, seen | {w}, chain + [w])
    yield from extend((0, 0), {(0, 0)}, [(0, 0)])


def forward(a, b):
    return b[0] + b[1] > a[0] + a[1]


def reward_in_rectangle(lo, hi, marks):
    # Cost formulation independently computes the local maximum reward.
    dist = {lo: 0}
    todo = [(0, lo)]
    while todo:
        cost, a = heapq.heappop(todo)
        if dist[a] != cost:
            continue
        if a == hi:
            return (hi[0] - lo[0]) + (hi[1] - lo[1]) - cost
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            b = (a[0] + dx, a[1] + dy)
            if not (lo[0] <= b[0] <= hi[0] and lo[1] <= b[1] <= hi[1]):
                continue
            weight = int(forward(a, b) and (a, b) not in marks)
            candidate = cost + weight
            if candidate < dist.get(b, 10**12):
                dist[b] = candidate
                heapq.heappush(todo, (candidate, b))
    raise RuntimeError("rectangle target unreachable")


def all_mark_subsets(edges):
    for bits in range(1 << len(edges)):
        yield {e for j, e in enumerate(edges) if bits >> j & 1}


def main():
    counts = {"path_scale_cases": 0, "segments": 0, "bad_segments": 0,
              "mark_only_witnesses": 0, "marked_subsequences": 0,
              "short_last_segments": 0, "checks_failed": 0}
    for N in range(1, 4):
        for chain in paths(N):
            steps = list(zip(chain, chain[1:]))
            marked_candidates = [e for e in steps if forward(*e)]
            b_total = sum(not forward(*e) for e in steps)
            if N <= 2:
                mark_patterns = list(all_mark_subsets(marked_candidates))
            else:
                mark_patterns = [set(), set(marked_candidates),
                                 set(marked_candidates[::2]), set(marked_candidates[1::2])]
            for marks in mark_patterns:
                counts["marked_subsequences"] += 1
                ordered = [(0, 0)] + [a for a, b in steps if (a, b) in marks] + [(N, N)]
                for coord in (0, 1):
                    variation = sum(max(a[coord] - b[coord], 0) for a, b in zip(ordered, ordered[1:]))
                    need(variation <= b_total, "marked variation exceeds backward budget")
            for h, m in itertools.product(range(1, 4), range(1, 5)):
                counts["path_scale_cases"] += 1
                L = h * m
                targets = list(range(L, 2 * N, L)) + [2 * N]
                boundaries = [0]
                cursor = 0
                for target in targets:
                    while sum(chain[cursor]) != target:
                        cursor += 1
                    boundaries.append(cursor)
                need(len(boundaries) - 1 == (2 * N + L - 1) // L, "wrong segment count")
                bad_perimeter = 0
                for j, (start, stop) in enumerate(zip(boundaries, boundaries[1:])):
                    counts["segments"] += 1
                    segment = chain[start:stop + 1]
                    segment_steps = list(zip(segment, segment[1:]))
                    u, v = segment[0], segment[-1]
                    tau = sum(v) - sum(u)
                    b = sum(not forward(*e) for e in segment_steps)
                    s = b // h
                    a = (s + 1) * h
                    i, next_i = u[0] // h, v[0] // h
                    lo = (i * h - a, sum(u) - (i + 1) * h - a)
                    hi = ((next_i + 1) * h + a, sum(v) - next_i * h + a)
                    W, H = hi[0] - lo[0], hi[1] - lo[1]
                    need(W > 2 * a - b >= h and H > 2 * a - b >= h, "side positivity failed")
                    need(W + H == tau + 2 * h + 4 * a, "perimeter identity failed")
                    need(-s - 2 <= next_i - i <= m + s + 2, "coarse increment bound failed")
                    need(all(lo[0] <= w[0] <= hi[0] and lo[1] <= w[1] <= hi[1] for w in segment),
                         "enclosure failed")
                    last = j == len(boundaries) - 2
                    if last and tau < L:
                        counts["short_last_segments"] += 1
                    good = s == 0 and not last
                    if good:
                        z = next_i - i
                        need((W, H) == ((z + 3) * h, (m - z + 3) * h), "good shape failed")
                    else:
                        counts["bad_segments"] += 1
                        bad_perimeter += W + H
                    for marks in mark_patterns:
                        witness = {e for e in segment_steps if forward(*e) and e in marks}
                        original_reward = len(witness) - b
                        counts["mark_only_witnesses"] += 1
                        # All marks except this segment's original positive witness are absent.
                        need(reward_in_rectangle(lo, hi, witness) >= max(original_reward, 0),
                             "mark-only padded completion failed")
                need(bad_perimeter <= (m + 10) * b_total + L + 6 * h, "bad perimeter budget failed")
    print(json.dumps(counts, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

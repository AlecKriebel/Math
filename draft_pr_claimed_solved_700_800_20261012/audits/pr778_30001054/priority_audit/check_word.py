#!/usr/bin/env python3
"""Read-only finite verification for the stated PR778 word. No priority inference."""
import json
from collections import Counter
from math import comb

def need(condition, message):
    if not condition:
        raise SystemExit("FAIL: " + message)

def run():
    a, b, c = (1, 2, -1, -2), (1, 2, -2, -1), (2, 1, -2, -1)
    word = (a, b, a, b, c, b, c, b)
    n = 2
    reverse = lambda p: tuple(-x for x in reversed(p))
    need(len(word) == 8 * comb(n, 2), "length")
    for p in word:
        need(set(p) == {1, -1, 2, -2} and len(p) == 4, "permutation")
        need(all(p.index(i) < p.index(-i) for i in (1, 2)), "endpoint order")
    need(all(word[(k + 4) % 8] == reverse(p) for k, p in enumerate(word)), "half-period")
    least = next(d for d in range(1, 9) if all(word[k] == word[(k + d) % 8] for k in range(8)))
    need(least == 8, "primitive period")
    events = []
    for k, p in enumerate(word):
        q = word[(k + 1) % 8]
        changed = [i for i in range(4) if p[i] != q[i]]
        need(len(changed) == 2 and changed[1] == changed[0] + 1, "single adjacent switch")
        i, j = changed
        need(p[i] == q[j] and p[j] == q[i] and abs(p[i]) != abs(p[j]), "cross-body swap")
        events.append((q[i], q[j]))
    counts = Counter(events)
    supporting = {(1, 2), (2, 1), (-1, -2), (-2, -1)}
    mixed = {(1, -2), (-2, 1), (2, -1), (-1, 2)}
    need(set(counts) == supporting and all(counts[x] == 2 for x in supporting), "supporting counts")
    need(all(counts[x] == 0 for x in mixed), "zero mixed events")
    separated = {(1, -1, 2, -2), (2, -2, 1, -1)}
    need(not any(p in separated for p in word), "fully separated term absent")
    return {"status": "PASS", "primitive_period": least, "supporting_type_counts": sorted([list(x) + [counts[x]] for x in supporting]), "mixed_event_count": sum(counts[x] for x in mixed), "post_switch_events": events, "fully_separated_term_present": False}

if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True))

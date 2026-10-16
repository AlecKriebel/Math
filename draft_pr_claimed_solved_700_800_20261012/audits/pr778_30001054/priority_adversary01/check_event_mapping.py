#!/usr/bin/env python3
"""Small independent convention/multiplicity check; no topological theorem is tested."""
import collections
import json
import sys


def need(condition, label):
    if not condition:
        raise ValueError(label)


def body(label):
    return label.rstrip("'")


def main():
    a = ("1", "2", "1'", "2'")
    b = ("1", "2", "2'", "1'")
    c = ("2", "1", "2'", "1'")
    period = (a, b, a, b, c, b, c, b)
    post = []
    for k, before in enumerate(period):
        after = period[(k + 1) % len(period)]
        changed = [j for j in range(4) if before[j] != after[j]]
        need(len(changed) == 2 and changed[1] == changed[0] + 1, "not adjacent")
        i, j = changed
        need(before[i] == after[j] and before[j] == after[i], "not a swap")
        need(body(after[i]) != body(after[j]), "same body")
        post.append((after[i], after[j]))
    expected = [("2'", "1'"), ("1'", "2'"), ("2'", "1'"),
                ("2", "1"), ("1", "2"), ("2", "1"),
                ("1", "2"), ("1'", "2'")]
    need(post == expected, "unexpected post-switch convention")
    pre = [(y, x) for x, y in post]
    mixed = lambda p: p[0].endswith("'") != p[1].endswith("'")
    counts = collections.Counter(post)
    need(len(counts) == 4 and set(counts.values()) == {2}, "multiplicity")
    need(sum(map(mixed, post)) == 0 and sum(map(mixed, pre)) == 0, "mixed event")
    # DGHP uses pre-switch order; Novick/OWR use post-switch order.
    # Reversal changes order only and preserves the absence of mixed events.
    result = {
        "status": "PASS",
        "scope": "independent event/convention check only; topology supplied by primary sources",
        "post_switch_events": post,
        "pre_switch_events": pre,
        "post_counts": [{"event": list(k), "count": v} for k, v in sorted(counts.items())],
        "full_period_mixed_count": 0,
        "half_period_mixed_counts": [sum(map(mixed, post[:4])), sum(map(mixed, post[4:]))],
        "dghp_2005_once_per_ordered_type": False,
        "novick_2012_two_mixed_per_half_period": False,
        "inference": "The accepted weak word is excluded by both proper definitions. This does not demonstrate prior publication of a literal counterexample.",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, TypeError, IndexError) as error:
        print(json.dumps({"status": "FAIL", "error": str(error)}))
        sys.exit(1)

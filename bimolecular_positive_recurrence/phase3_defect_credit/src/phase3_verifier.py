#!/usr/bin/env python3
"""Independent deterministic verification driver for the Phase-III package."""
from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from pathlib import Path
import importlib
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))

MODULES = (
    "cone_lemma",
    "conservation_or_drain",
    "buffered_word",
    "fast_automaton",
    "fast_scc_analysis",
    "slow_skeleton",
    "reward_cycle",
    "bellman_certificate",
    "tier_induction",
    "foster_trace_chain",
)


def run_self_tests() -> None:
    for name in MODULES:
        mod = importlib.import_module(name)
        test = getattr(mod, "self_test", None)
        if test is None:
            raise AssertionError(f"{name} has no self_test")
        test()


def exact_canonical_checks() -> None:
    from src.generator import Reaction
    from conservation_or_drain import conservation_extension, drain_multiset
    from buffered_word import construct_buffered_word

    rs = [
        Reaction((0, 0), (1, 1), Fraction(2)),
        Reaction((1, 1), (0, 1), Fraction(3)),
        Reaction((0, 1), (0, 0), Fraction(5)),
    ]
    assert conservation_extension(rs, {0}) is None
    dm = drain_multiset(rs, {0})
    cert = construct_buffered_word(rs, dm.counts)
    assert cert.net_vector[1] == 0
    assert cert.net_vector[0] < 0


def exhaustive_two_phase_cycle_check() -> None:
    """Check the finite leak/service cycle inequality on all 2-phase edge sets.

    There are four complex labels: q=0 and q=1 at each of two phases.  The
    check is purely graph-theoretic and independent of numerical rate values.
    Whenever the complex graph is strongly connected and the induced phase
    graph has a positive reward cycle, it also has a strictly lower-resistance
    negative reward cycle.  This is the smallest nontrivial instance of the
    cycle-pivot lemma.
    """
    labels = tuple(range(4))
    q = (0, 0, 1, 1)
    phase = (0, 1, 0, 1)
    possible = tuple((u, v) for u in labels for v in labels if u != v)

    def strong(edges):
        for reverse in (False, True):
            adj = {v: [] for v in labels}
            for u, v in edges:
                a, b = (v, u) if reverse else (u, v)
                adj[a].append(b)
            seen = {0}
            stack = [0]
            while stack:
                u = stack.pop()
                for v in adj[u]:
                    if v not in seen:
                        seen.add(v)
                        stack.append(v)
            if len(seen) != 4:
                return False
        return True

    def cycles(edges):
        pedges = [(phase[u], phase[v], q[u], q[v] - q[u]) for u, v in edges]
        fast_at = [False, False]
        for s, _, fast, _ in pedges:
            fast_at[s] |= bool(fast)
        adj = {0: [], 1: []}
        for i, (s, t, fast, reward) in enumerate(pedges):
            resistance = 0 if fast or not fast_at[s] else 1
            adj[s].append((t, reward, resistance))
        # With two phase vertices every simple cycle has length one or two.
        vals = []
        for s in (0, 1):
            for t, r, c in adj[s]:
                if t == s:
                    vals.append((r, c))
                else:
                    for u, r2, c2 in adj[t]:
                        if u == s:
                            vals.append((r + r2, c + c2))
        return vals

    # Exhaust all subsets.  Empty/small non-strong graphs are skipped.
    for mask in range(1 << len(possible)):
        edges = tuple(possible[i] for i in range(len(possible)) if mask & (1 << i))
        if not strong(edges):
            continue
        vals = cycles(edges)
        pos = [c for r, c in vals if r > 0]
        if not pos:
            continue
        neg = [c for r, c in vals if r < 0]
        if not neg or min(neg) >= min(pos):
            raise AssertionError((edges, vals))


def main() -> None:
    run_self_tests()
    exact_canonical_checks()
    exhaustive_two_phase_cycle_check()
    print("Phase-III independent verification: ALL CHECKS PASSED")


if __name__ == "__main__":
    main()

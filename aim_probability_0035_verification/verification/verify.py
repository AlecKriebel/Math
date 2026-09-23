#!/usr/bin/env python3
"""Exact reconstruction of the supplied witness, including its marginal proof.

Python 3.10+, standard library only. No input/output files required. Run from
any directory; stdout is a reproducible JSON certificate. Checks remain active
under python -O. This verifies a fixed witness, not arbitrary Potts instances.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import json

A, B, C, D, E = range(5)
EDGES = ((A, B), (A, C), (A, D), (B, C), (B, E), (D, E))
WORD = (C, E, B, C, B, A, E, B, E)
CENSORED = WORD[:6] + (None,) + WORD[7:]
STATES = tuple(product(range(3), repeat=5))
TRIPLES = tuple(product(range(3), repeat=3))
ADJ = tuple(tuple(w if v == u else u for u, w in EDGES if v in (u, w))
            for v in range(5))


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def conditional(color, neighbors, activity=30, q=3):
    weights = [activity ** neighbors.count(r) for r in range(q)]
    return F(weights[color], sum(weights))


def update(law, site, activity=30, q=3):
    if site is None:
        return law.copy()
    out = {}
    for state, mass in law.items():
        neighbors = tuple(state[u] for u in ADJ[site])
        for color in range(q):
            dest = state[:site] + (color,) + state[site + 1:]
            out[dest] = out.get(dest, F(0)) + mass * conditional(
                color, neighbors, activity, q)
    check(sum(out.values()) == sum(law.values()), "mass conservation")
    check(all(p >= 0 for p in out.values()), "nonnegative probabilities")
    return out


def stationary(activity=30, q=3):
    weights = {s: activity ** sum(s[u] == s[v] for u, v in EDGES)
               for s in product(range(q), repeat=5)}
    z = sum(weights.values())
    return z, {s: F(w, z) for s, w in weights.items()}


def tv(law, pi):
    return sum((abs(law.get(s, F(0)) - p) for s, p in pi.items()), F(0)) / 2


def run(word, pi, activity=30, q=3):
    law = {(0,) * 5: F(1)}
    history = [tv(law, pi)]
    for site in word:
        law = update(law, site, activity, q)
        history.append(tv(law, pi))
        check(history[-1] <= history[-2], "each update contracts its own TV")
    return law, history


@lru_cache(None)
def h(r, s, t):
    return conditional(r, (s, t))


@lru_cache(None)
def j(r, s, t, u):
    return conditional(r, (s, t, u))


@lru_cache(None)
def r6(a, b, c, y):
    return h(y, 0, 0) * j(b, 0, c, y) * j(a, b, c, 0) * sum(
        h(x, 0, 0) * j(z, 0, x, y) * h(c, 0, z)
        for x, z in product(range(3), repeat=2))


def sign(x):
    return "+" if x > 0 else "-" if x < 0 else "0"


def main():
    z, pi = stationary()
    check(z == 2207656998, "partition function")
    poly = Counter(sum(s[u] == s[v] for u, v in EDGES) for s in STATES)
    check(dict(poly) == {0: 18, 1: 66, 2: 90, 3: 42, 4: 24, 6: 3},
          "partition polynomial by direct enumeration")
    for site in range(5):
        check(update(pi, site) == pi, "Gibbs stationarity at every site")
    mu, hist_mu = run(WORD, pi)
    nu, hist_nu = run(CENSORED, pi)
    six, _ = run(WORD[:6], pi)
    for a, b, c, y in product(range(3), repeat=4):
        check(r6(a, b, c, y) == six.get((a, b, c, 0, y), 0), "formula (1)")
    f, qlaw, pbar = {}, {}, {}
    for a, b, c in TRIPLES:
        t = (a, b, c)
        f[t] = sum(r6(a, u, c, y) * h(e, u, 0) * j(b, a, c, e)
                   for u, y, e in product(range(3), repeat=3))
        qlaw[t] = sum(r6(a, u, c, y) * j(b, a, c, y)
                      for u, y in product(range(3), repeat=2))
        pbar[t] = F(30 ** ((a == b) + (a == c) + (a == 0) + (b == c))
                    * (902 if b == 0 else 61), z)
        for e in range(3):
            s = (a, b, c, 0, e)
            check(mu[s] == f[t] * h(e, b, 0), "formulas (2),(4)")
            check(nu[s] == qlaw[t] * h(e, b, 0), "formulas (3),(5)")
            check(pi[s] == pbar[t] * h(e, b, 0), "formulas (6),(7)")
    check(sum(f.values()) == sum(qlaw.values()) == 1, "marginal normalization")
    check(sum(pbar.values()) == F(1, 3), "unconditioned slice mass")
    check(all(s[D] == 0 for law in (mu, nu) for s in law), "D never updated")
    expected = {
        "000": "--", "001": "--", "010": "--", "011": "--",
        "012": "--", "100": "--", "101": "++", "102": "--",
        "110": "--", "111": "++", "112": "-+", "120": "--",
        "121": "++", "122": "++"}
    rows = []
    for t in TRIPLES:
        swapped = tuple(0 if x == 0 else 3 - x for x in t)
        check((f[t], qlaw[t], pbar[t]) == (f[swapped], qlaw[swapped], pbar[swapped]),
              "color-swap symmetry")
        key = "".join(map(str, min(t, swapped)))
        check(sign(pbar[t] - f[t]) + sign(pbar[t] - qlaw[t]) == expected[key],
              "complete sign table")
        rows.append({"abc": "".join(map(str, t)), "F": str(f[t]),
                     "Q": str(qlaw[t]), "pi_bar": str(pbar[t]),
                     "pi_bar_minus_F": str(pbar[t] - f[t]),
                     "pi_bar_minus_Q": str(pbar[t] - qlaw[t])})
    deficit_f = sum(max(pbar[t] - f[t], 0) for t in TRIPLES)
    deficit_q = sum(max(pbar[t] - qlaw[t], 0) for t in TRIPLES)
    check(deficit_f == F(341299157366878803726062799858951625,
                        255345570503528934047286495273555254068), "F deficit")
    check(deficit_q == F(18608730448608839275198892178535,
                        13922371260779084768671794660693282), "Q deficit")
    check(tv(mu, pi) == F(2, 3) + deficit_f, "TV reduction for mu")
    check(tv(nu, pi) == F(2, 3) + deficit_q, "TV reduction for nu")
    check(tv(mu, pi) == F(511715038479158504505751178946687363011,
                          766036711510586802141859485820665762204), "mu TV")
    check(tv(nu, pi) == F(9300189570967998685056395332640723,
                          13922371260779084768671794660693282), "nu TV")
    gap = tv(mu, pi) - tv(nu, pi)
    check(gap == F(7905357280856578194954129502105,
                   766036711510586802141859485820665762204) > 0, "strict exact gap")
    controls = {}
    for activity, colors, label in ((1, 3, "independent_spins"), (30, 2, "Ising")):
        _, cp = stationary(activity, colors)
        cm, _ = run(WORD, cp, activity, colors)
        cn, _ = run(CENSORED, cp, activity, colors)
        cg = tv(cm, cp) - tv(cn, cp)
        check(cg == 0 if activity == 1 else cg <= 0, label + " control")
        controls[label] = str(cg)
    print(json.dumps({"status": "PASS", "Z": z, "tv_full": str(tv(mu, pi)),
                      "tv_censored": str(tv(nu, pi)), "gap": str(gap),
                      "history_full_minus_censored": [str(x-y) for x, y in zip(hist_mu, hist_nu)],
                      "controls": controls, "marginals": rows}, indent=2))


if __name__ == "__main__":
    main()

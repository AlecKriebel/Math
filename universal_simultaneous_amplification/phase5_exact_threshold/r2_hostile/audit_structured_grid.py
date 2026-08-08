#!/usr/bin/env python3
"""Exact multiscale hostile search for the fitness-two conjectures.

The corpus consists of tied-edge templates for dense modular graphs,
barbells with weak completion, multiple-hub systems, core--satellite graphs,
and chain/ring modules.  Relative role weights range over eight orders of
magnitude.  Every score, including the marked two-step promotion margin, is
computed over QQ.  This is an exact finite search, not a universal proof.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, product
from math import comb

from exact_fixation import Q, as_float, baseline, connected, fixation


ALPHABET = (
    Fraction(1, 10000),
    Fraction(1, 100),
    Fraction(1, 10),
    Fraction(1),
    Fraction(10),
    Fraction(100),
    Fraction(10000),
)


@dataclass(frozen=True)
class Template:
    name: str
    n: int
    roles: tuple[tuple[int, ...], ...]
    labels: tuple[str, ...]

    def weights(self, values) -> list[list[Q]]:
        qvalues = [Q(value.numerator, value.denominator) for value in values]
        return [
            [Q(0) if role < 0 else qvalues[role] for role in row]
            for row in self.roles
        ]


def make_template(name, n, classifier) -> Template:
    labels: list[str] = []
    role_of: dict[str, int] = {}
    roles = [[-1 for _ in range(n)] for _ in range(n)]
    for u, v in combinations(range(n), 2):
        label = classifier(u, v)
        if label is None:
            continue
        if label not in role_of:
            role_of[label] = len(labels)
            labels.append(label)
        role = role_of[label]
        roles[u][v] = roles[v][u] = role
    template = Template(name, n, tuple(tuple(row) for row in roles), tuple(labels))
    if len(labels) > 4:
        raise AssertionError((name, labels))
    if not connected(template.weights([Fraction(1)] * len(labels))):
        raise AssertionError(f"disconnected template {name}")
    return template


def block_index(vertex: int, sizes: tuple[int, ...]) -> int:
    total = 0
    for block, size in enumerate(sizes):
        total += size
        if vertex < total:
            return block
    raise IndexError(vertex)


def templates() -> list[Template]:
    answer: list[Template] = []
    for n in range(4, 8):
        # Complete two-class graphs with separate internal roles.
        for a in range(1, n // 2 + 1):
            sizes = (a, n - a)

            def two_class(u, v, sizes=sizes):
                bu, bv = block_index(u, sizes), block_index(v, sizes)
                return f"inside-{bu}" if bu == bv else "cross"

            answer.append(make_template(f"n{n}-two-block-{a}-{n-a}", n, two_class))

        # Three dense modules: one internal and three cross roles.
        for a in range(1, n - 1):
            for b in range(a, n - a):
                c = n - a - b
                if c < b:
                    continue
                sizes = (a, b, c)

                def three_class(u, v, sizes=sizes):
                    bu, bv = sorted((block_index(u, sizes), block_index(v, sizes)))
                    return "internal" if bu == bv else f"cross-{bu}-{bv}"

                answer.append(make_template(f"n{n}-three-block-{a}-{b}-{c}", n, three_class))

        # Two cliques joined by one bridge, with and without weak completion.
        for a in range(2, n - 1):
            b = n - a
            if b < 2 or a > b:
                continue

            def barbell_sparse(u, v, a=a):
                if u < a and v < a:
                    return "left-clique"
                if u >= a and v >= a:
                    return "right-clique"
                if (u, v) == (a - 1, a):
                    return "bridge"
                return None

            def barbell_complete(u, v, a=a):
                role = barbell_sparse(u, v, a)
                if role is not None:
                    return role
                return "weak-completion"

            answer.append(make_template(f"n{n}-barbell-{a}-{b}-sparse", n, barbell_sparse))
            answer.append(make_template(f"n{n}-barbell-{a}-{b}-completed", n, barbell_complete))

        # Two hubs, alternately assigned leaves, with sparse and dense variants.
        if n >= 5:
            def double_hub_sparse(u, v):
                if (u, v) == (0, 1):
                    return "hub-edge"
                if u < 2 <= v and u == (v - 2) % 2:
                    return "own-spoke"
                return None

            def double_hub_complete(u, v):
                role = double_hub_sparse(u, v)
                if role is not None:
                    return role
                if u < 2 <= v:
                    return "cross-spoke"
                return "leaf-completion"

            answer.append(make_template(f"n{n}-double-hub-sparse", n, double_hub_sparse))
            answer.append(make_template(f"n{n}-double-hub-completed", n, double_hub_complete))

        # Clique core plus K2/singleton satellites; all portal interactions tied.
        for core in range(2, n - 1):
            satellites = [(v - core) // 2 for v in range(core, n)]

            def core_sat(u, v, core=core, satellites=satellites):
                if v < core:
                    return "core"
                if u < core <= v:
                    return "portal"
                su, sv = satellites[u - core], satellites[v - core]
                return "satellite-internal" if su == sv else "satellite-cross"

            answer.append(make_template(f"n{n}-core-{core}-paired-satellites", n, core_sat))

        # A ring role, short chords, and all remaining completion edges.
        def ring(u, v, n=n):
            distance = min((v - u) % n, (u - v) % n)
            if distance == 1:
                return "ring"
            if distance == 2:
                return "short-chord"
            return "completion"

        answer.append(make_template(f"n{n}-ring-chord-completion", n, ring))

    # Deduplicate identical role matrices produced by small boundary cases.
    unique: dict[tuple[int, tuple[tuple[int, ...], ...]], Template] = {}
    for template in answer:
        unique.setdefault((template.n, template.roles), template)
    return list(unique.values())


def integrated_two_step(weights) -> Q:
    """The exact U M_P^2 psi value from the proved two-defect formula."""
    n = len(weights)
    N = n - 1
    degrees = [sum(row, Q(0)) for row in weights]
    P = [[weights[v][i] / degrees[v] for i in range(n)] for v in range(n)]
    complete_inverse_mean = Q(2**N - 1, N * 2 ** (N - 1))
    row_square = sum((P[v][i] ** 2 for v in range(n) for i in range(n)), Q(0))
    columns = [sum((P[v][i] for v in range(n)), Q(0)) for i in range(n)]
    column_square = sum((value**2 for value in columns), Q(0))
    mutual = sum((P[v][i] * P[i][v] for v in range(n) for i in range(n)), Q(0))
    defect_1 = row_square - Q(n, n - 1)
    defect_2 = (column_square - mutual) - (n - row_square)
    assert defect_1 >= 0 and defect_2 >= 0
    if n == 3:
        return complete_inverse_mean + defect_1 / 24
    s = n - 2
    integrated_sum = sum(
        (Q(comb(s - 2, j), (j + 1) * (j + 2) ** 2) for j in range(s - 1)),
        Q(0),
    )
    integrated_half = Q(2**s - 1, s) - Q(2 ** (s + 1) - 1, 2 * (s + 1))
    alpha = (integrated_half - integrated_sum) / (n * 2**s)
    beta = integrated_sum / (2 * n * 2**s)
    return complete_inverse_mean + alpha * defect_1 + beta * defect_2


def parameter_vectors(dimension: int):
    # Overall edge scale is irrelevant, so anchor the first role at one.
    for tail in product(ALPHABET, repeat=dimension - 1):
        yield (Fraction(1),) + tail


def fraction_text(value: Q) -> str:
    return str(value)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=7)
    parser.add_argument("--limit-templates", type=int, default=0)
    args = parser.parse_args()

    corpus = [template for template in templates() if template.n <= args.max_n]
    if args.limit_templates:
        corpus = corpus[: args.limit_templates]
    tested = 0
    db_violations = []
    simultaneous = []
    promotion_violations = []
    best_nontrivial_db = None
    best_nontrivial_sim = None
    smallest_promotion = None

    for number, template in enumerate(corpus, 1):
        local = 0
        for values in parameter_vectors(len(template.labels)):
            weights = template.weights(values)
            db = fixation(weights, "dB")
            bd = fixation(weights, "Bd")
            db_ratio = db / baseline(template.n, "dB")
            bd_ratio = bd / baseline(template.n, "Bd")
            minimum = min(db_ratio, bd_ratio)
            promotion = 1 / (template.n * db) - integrated_two_step(weights)
            record = (db_ratio, bd_ratio, promotion, template, values, weights)
            if db_ratio > 1:
                db_violations.append(record)
            if db_ratio > 1 and bd_ratio > 1:
                simultaneous.append(record)
            if promotion < 0:
                promotion_violations.append(record)
            if not (db_ratio == 1 and bd_ratio == 1):
                if best_nontrivial_db is None or db_ratio > best_nontrivial_db[0]:
                    best_nontrivial_db = record
                sim_record = (minimum,) + record
                if best_nontrivial_sim is None or minimum > best_nontrivial_sim[0]:
                    best_nontrivial_sim = sim_record
            if smallest_promotion is None or promotion < smallest_promotion[0]:
                smallest_promotion = (promotion,) + record
            tested += 1
            local += 1
        print(
            f"[{number}/{len(corpus)}] {template.name}: {local} exact assignments; "
            f"roles={template.labels}",
            flush=True,
        )

    assert best_nontrivial_db is not None
    assert best_nontrivial_sim is not None
    assert smallest_promotion is not None
    print(f"EXACT STRUCTURED GRID: {tested} rational graphs in {len(corpus)} templates")
    print(
        "dB violations=", len(db_violations),
        "simultaneous violations=", len(simultaneous),
        "promotion violations=", len(promotion_violations),
    )

    db_ratio, bd_ratio, promotion, template, values, _ = best_nontrivial_db
    print(
        "best nontrivial dB:", template.name, template.labels,
        tuple(map(str, values)),
        "dB ratio=", fraction_text(db_ratio), f"(~{as_float(db_ratio):.17g})",
        "Bd ratio=", f"{as_float(bd_ratio):.17g}",
        "promotion=", f"{as_float(promotion):.17g}",
    )
    minimum, db_ratio, bd_ratio, promotion, template, values, _ = best_nontrivial_sim
    print(
        "best nontrivial M:", template.name, template.labels,
        tuple(map(str, values)),
        "M=", fraction_text(minimum), f"(~{as_float(minimum):.17g})",
        "dB ratio=", f"{as_float(db_ratio):.17g}",
        "Bd ratio=", f"{as_float(bd_ratio):.17g}",
    )
    promotion, db_ratio, bd_ratio, _, template, values, _ = smallest_promotion
    print(
        "smallest promotion:", template.name, template.labels,
        tuple(map(str, values)),
        "margin=", fraction_text(promotion), f"(~{as_float(promotion):.17g})",
        "dB ratio=", f"{as_float(db_ratio):.17g}",
    )
    if db_violations or simultaneous or promotion_violations:
        raise AssertionError("exact hostile violation found; inspect records")
    print("PASS: no exact dB, simultaneous, or marked-promotion violation in corpus")
    print("This is finite evidence only; the universal r=2 sign remains open.")


if __name__ == "__main__":
    main()

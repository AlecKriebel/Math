#!/usr/bin/env python3
"""Bounded exact SAT probe for the order-13 unique-full-response slice.

This is a discovery tool, not a coverage certificate.  It fixes by relabeling
an independent triple S={0,1,2} and its unique full family-response vertex
x=3.  Edge variables encode H=complement(G).
"""

from __future__ import annotations

import argparse
import itertools
import subprocess
import tempfile
from pathlib import Path


N = 13
S = (0, 1, 2)
X = 3


def pair(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


class CNF:
    def __init__(self) -> None:
        self.names = [""]
        self.clauses: list[tuple[int, ...]] = []

    def var(self, name: str) -> int:
        self.names.append(name)
        return len(self.names) - 1

    def add(self, *lits: int) -> None:
        clause = tuple(lits)
        if not clause or any(lit == 0 for lit in clause):
            raise ValueError("malformed clause")
        self.clauses.append(clause)

    def dimacs(self) -> str:
        body = "\n".join(
            " ".join(map(str, clause)) + " 0" for clause in self.clauses
        )
        return f"p cnf {len(self.names) - 1} {len(self.clauses)}\n{body}\n"


def build(
    *,
    sort_signatures: bool = True,
    require_theta_gap: bool = True,
    require_unique_full: bool = True,
    require_closure: bool = True,
    use_witness_bound: bool = True,
    require_connected: bool = True,
    force_all_independent_states: bool = True,
    exact_q_size: int | None = None,
    tight_pattern: str | None = None,
) -> tuple[
    CNF,
    dict[tuple[int, int], int],
    dict[tuple[int, int, int], int],
]:
    cnf = CNF()
    vertices = range(N)
    triples = tuple(itertools.combinations(vertices, 3))
    edge = {
        uv: cnf.var(f"e_{uv[0]}_{uv[1]}")
        for uv in itertools.combinations(vertices, 2)
    }
    witness = {
        (u, v, w): cnf.var(f"w_{u}_{v}_{w}")
        for u, v in itertools.combinations(vertices, 2)
        for w in vertices
        if w not in (u, v)
    }
    family = {
        state: cnf.var("f_" + "_".join(map(str, state)))
        for state in triples
    }
    move = {
        (state, attacked, guard): cnf.var(
            "m_"
            + "_".join(map(str, state))
            + f"__{attacked}_{guard}"
        )
        for state in triples
        for attacked in vertices
        if attacked not in state
        for guard in state
    }

    def e(u: int, v: int) -> int:
        return edge[pair(u, v)]

    # alpha(G)<=3.
    for four in itertools.combinations(vertices, 4):
        cnf.add(*(-e(u, v) for u, v in itertools.combinations(four, 2)))

    # gamma(G)>=3.
    for u, v in itertools.combinations(vertices, 2):
        choices = [w for w in vertices if w not in (u, v)]
        cnf.add(*(witness[(u, v, w)] for w in choices))
        for w in choices:
            z = witness[(u, v, w)]
            cnf.add(-z, e(u, w))
            cnf.add(-z, e(v, w))

    # G connected.
    if require_connected:
        full = (1 << N) - 1
        for mask in range(1, full):
            if not mask & 1:
                continue
            cnf.add(
                *(
                    -e(u, v)
                    for u in vertices
                    if mask >> u & 1
                    for v in vertices
                    if not (mask >> v & 1)
                )
            )

    # Selected states dominate and, unless ablated, form a nonempty
    # one-guard eternal family.
    for state in triples:
        f = family[state]
        for y in vertices:
            if y not in state:
                cnf.add(-f, -e(y, state[0]), -e(y, state[1]), -e(y, state[2]))
    cnf.add(*family.values())
    if require_closure:
        for state in triples:
            f = family[state]
            for attacked in vertices:
                if attacked in state:
                    continue
                replies: list[int] = []
                for guard in state:
                    m = move[(state, attacked, guard)]
                    successor = tuple(sorted((set(state) - {guard}) | {attacked}))
                    replies.append(m)
                    cnf.add(-m, -e(guard, attacked))
                    cnf.add(-m, family[successor])
                cnf.add(-f, *replies)

    # Every H-triangle is a maximum independent state and hence is retained.
    if force_all_independent_states:
        for state in triples:
            cnf.add(
                -e(state[0], state[1]),
                -e(state[0], state[2]),
                -e(state[1], state[2]),
                family[state],
            )

    # S is an independent family state and x is its full response.
    for u, v in itertools.combinations(S, 2):
        cnf.add(e(u, v))
    cnf.add(family[S])
    for u in S:
        cnf.add(-e(u, X))
        cnf.add(family[tuple(sorted((set(S) - {u}) | {X}))])

    if tight_pattern is not None:
        if tight_pattern not in {"partition", "overlap", "six"}:
            raise ValueError("unknown tight pattern")
        # Tight five-nonneutral labeling:
        # p_0,p_1,p_2=4,5,6; external witnesses y,z=7,8;
        # the four additional neutral vertices are 9..12.
        spokes = (4, 5, 6)
        for u, p in zip(S, spokes, strict=True):
            cnf.add(e(X, p))
            cnf.add(e(u, p))
            for v in S:
                if v != u:
                    cnf.add(-e(v, p))
        if tight_pattern == "six":
            for y in (7, 8, 9):
                cnf.add(-e(X, y))
            for q in range(10, 13):
                for u in S:
                    cnf.add(-e(u, q))
            for u, p, y in ((0, 4, 7), (1, 5, 8), (2, 6, 9)):
                cnf.add(e(u, y))
                cnf.add(e(p, y))
                for v in S:
                    if v != u:
                        cnf.add(-e(v, y))
        else:
            for y in (7, 8):
                cnf.add(-e(X, y))
            for q in range(9, 13):
                for u in S:
                    cnf.add(-e(u, q))
        if tight_pattern == "partition":
            # Y_0=Y_1={7}, Y_2={8}, with no fourth incidence.
            for u, p in ((0, 4), (1, 5)):
                cnf.add(e(u, 7))
                cnf.add(e(p, 7))
            cnf.add(e(2, 8))
            cnf.add(e(6, 8))
            for u, p, y in ((2, 6, 7), (0, 4, 8), (1, 5, 8)):
                cnf.add(-e(u, y), -e(p, y))
        elif tight_pattern == "overlap":
            # Y_0={7,8}, Y_1={7}, Y_2={8}.
            for u, p, y in (
                (0, 4, 7),
                (0, 4, 8),
                (1, 5, 7),
                (2, 6, 8),
            ):
                cnf.add(e(u, y))
                cnf.add(e(p, y))
            for u, p, y in ((2, 6, 7), (1, 5, 8)):
                cnf.add(-e(u, y), -e(p, y))

    # x is the unique full family-response vertex at S.
    if require_unique_full:
        for y in range(4, N):
            successors = [
                family[tuple(sorted((set(S) - {u}) | {y}))]
                for u in S
            ]
            cnf.add(*(-f for f in successors))

    # Theorem 1.1: at least five outside vertices are not G-complete to S.
    # Since x is complete, among vertices 4..12 at most four may also be
    # complete.  This is redundant, human-proved strengthening.
    if use_witness_bound:
        for five in itertools.combinations(range(4, N), 5):
            cnf.add(*(e(u, y) for y in five for u in S))

    if exact_q_size is not None:
        if not 1 <= exact_q_size <= 10:
            raise ValueError("|Q_S| must lie in 1..10")
        q_variables = {y: cnf.var(f"q_{y}") for y in range(4, N)}
        for y, q in q_variables.items():
            for u in S:
                cnf.add(-q, -e(u, y))
            cnf.add(e(0, y), e(1, y), e(2, y), q)
        target = exact_q_size - 1  # x itself is always in Q_S.
        values = tuple(q_variables.values())
        for subset in itertools.combinations(values, target + 1):
            cnf.add(*(-q for q in subset))
        for subset in itertools.combinations(values, len(values) - target + 1):
            cnf.add(*subset)

    # theta(G)>3: with S colored 0,1,2, every assignment to the other ten
    # vertices has a monochromatic H-edge.
    if require_theta_gap:
        for colors_tail in itertools.product(range(3), repeat=N - 3):
            colors = S + colors_tail
            cnf.add(
                *(
                    e(u, v)
                    for u, v in itertools.combinations(vertices, 2)
                    if colors[u] == colors[v]
                )
            )

    if sort_signatures:
        # Sound S_9 symmetry breaking: sort the four-bit H-adjacency
        # signatures to (0,1,2,3) of vertices 4..12.
        core = (0, 1, 2, 3)
        for left in range(4, N - 1):
            right = left + 1
            for p in range(16):
                for q in range(p):
                    mismatch: list[int] = []
                    for bit, core_vertex in enumerate(core):
                        lp = (p >> bit) & 1
                        rq = (q >> bit) & 1
                        mismatch.append(-e(left, core_vertex) if lp else e(left, core_vertex))
                        mismatch.append(-e(right, core_vertex) if rq else e(right, core_vertex))
                    cnf.add(*mismatch)

    return cnf, edge, family


def solve(
    cnf: CNF,
    solver: Path,
    timeout: int,
    *,
    instance_path: Path | None = None,
    proof_path: Path | None = None,
    result_path: Path | None = None,
) -> tuple[str, str]:
    with tempfile.TemporaryDirectory(prefix="order13-single-full-") as raw:
        instance = instance_path or Path(raw) / "instance.cnf"
        instance.write_text(cnf.dimacs(), encoding="ascii")
        command = [str(solver), "--quiet", "--binary=false"]
        if result_path is not None:
            command.extend(("-w", str(result_path)))
        command.append(str(instance))
        if proof_path is not None:
            command.append(str(proof_path))
        try:
            completed = subprocess.run(
                command,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as error:
            output = (error.stdout or "") + (error.stderr or "")
            return "TIMEOUT", output
        status = (
            "SAT"
            if completed.returncode == 10
            else "UNSAT"
            if completed.returncode == 20
            else f"EXIT_{completed.returncode}"
        )
        return status, completed.stdout


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--no-sort", action="store_true")
    parser.add_argument("--omit-theta-gap", action="store_true")
    parser.add_argument("--omit-unique-full", action="store_true")
    parser.add_argument("--omit-closure", action="store_true")
    parser.add_argument("--omit-witness-bound", action="store_true")
    parser.add_argument("--omit-connected", action="store_true")
    parser.add_argument("--omit-all-independent-states", action="store_true")
    parser.add_argument("--q-size", type=int)
    parser.add_argument(
        "--tight-pattern", choices=("partition", "overlap", "six")
    )
    parser.add_argument("--instance", type=Path)
    parser.add_argument("--proof", type=Path)
    parser.add_argument("--result", type=Path)
    args = parser.parse_args()
    cnf, _, _ = build(
        sort_signatures=not args.no_sort,
        require_theta_gap=not args.omit_theta_gap,
        require_unique_full=not args.omit_unique_full,
        require_closure=not args.omit_closure,
        use_witness_bound=not args.omit_witness_bound,
        require_connected=not args.omit_connected,
        force_all_independent_states=not args.omit_all_independent_states,
        exact_q_size=args.q_size,
        tight_pattern=args.tight_pattern,
    )
    print(
        f"variables={len(cnf.names)-1} clauses={len(cnf.clauses)} "
        f"sorted={not args.no_sort}"
    )
    status, output = solve(
        cnf,
        args.solver,
        args.timeout,
        instance_path=args.instance,
        proof_path=args.proof,
        result_path=args.result,
    )
    print(f"status={status}")
    print(output[-4000:])


if __name__ == "__main__":
    main()

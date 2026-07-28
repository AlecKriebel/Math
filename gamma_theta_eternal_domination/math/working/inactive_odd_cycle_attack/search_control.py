#!/usr/bin/env python3
"""Exact SAT search for a genuine eternal-family inactive-C5 control.

This is a discovery program.  Edge variables encode H = complement(G).
It asks for:

* gamma(G) = alpha(G) = gamma^infinity(G) = 3;
* gamma(G-x) = alpha(G-x) = gamma^infinity(G-x) = theta(G-x) = 3;
* a full family response at the independent root {5,6,7};
* an induced C5 on vertices 0,...,4, all dynamically inactive at x.

Unlike the static C-109 control, vertices on the C5 are not forced to be
H-neighbors of x.  Thus a satisfying model need not contain the already
forbidden odd wheel centered at x.
"""

from __future__ import annotations

import argparse
import itertools
import subprocess
import tempfile
from pathlib import Path


R = (0, 1, 2, 3, 4)
ROOT = (5, 6, 7)


def pair(first: int, second: int) -> tuple[int, int]:
    if first == second:
        raise ValueError("loop")
    return (first, second) if first < second else (second, first)


class CNF:
    def __init__(self) -> None:
        self.names = [""]
        self.clauses: list[tuple[int, ...]] = []

    def var(self, name: str) -> int:
        self.names.append(name)
        return len(self.names) - 1

    def add(self, *literals: int) -> None:
        clause = tuple(literals)
        if not clause or any(literal == 0 for literal in clause):
            raise ValueError("malformed clause")
        if len(set(clause)) != len(clause):
            raise ValueError("duplicate literal")
        if any(-literal in clause for literal in clause):
            raise ValueError("tautological clause")
        self.clauses.append(clause)

    def dimacs(self) -> str:
        rows = [f"p cnf {len(self.names) - 1} {len(self.clauses)}"]
        rows.extend(" ".join(map(str, clause)) + " 0" for clause in self.clauses)
        return "\n".join(rows) + "\n"


def color_row(n: int) -> tuple[int, ...]:
    """A fixed deletion coloring compatible with the named C5 and root."""

    # On order 12 this is exactly the color pattern of the sharp C-109
    # deletion control.
    base = [0, 1, 0, 1, 2, 0, 1, 2, 1, 2, 2]
    base = base[: n - 1]
    for vertex in range(len(base), n - 1):
        base.append((vertex - 11) % 3)
    if len(base) != n - 1:
        raise AssertionError("color row length")
    return tuple(base)


def build(
    n: int,
    *,
    shape: str = "c5",
    require_physical_mix: bool = True,
    require_closure: bool = True,
    require_full_root: bool = True,
    require_deletion_coloring: bool = True,
    require_deletion_gamma: bool = True,
    force_divergent_witness: bool = False,
    force_rainbow_path: bool = False,
    require_global_gamma: bool = True,
    named_cycle_witnesses: bool = False,
    require_alpha_bound: bool = True,
    force_all_independent_states: bool = True,
    named_inactivity_only: bool = False,
    witness_partition: str | None = None,
) -> tuple[
    CNF,
    dict[tuple[int, int], int],
    dict[tuple[int, int, int], int],
]:
    if n < 6:
        raise ValueError("need C5 and x")
    if require_full_root and n < 9:
        raise ValueError("a full root needs R, ROOT, and x")
    x = n - 1
    if shape == "single":
        inactive = (0,)
    elif shape == "edge":
        inactive = (0, 1)
    elif shape == "path3":
        inactive = (0, 1, 2)
    elif shape == "c4":
        inactive = (0, 1, 2, 3)
    elif shape == "c5":
        inactive = R
    else:
        raise ValueError("unknown inactive shape")
    vertices = range(n)
    deletion = range(n - 1)
    triples = tuple(itertools.combinations(vertices, 3))
    cnf = CNF()
    edge = {
        uv: cnf.var(f"h_{uv[0]}_{uv[1]}")
        for uv in itertools.combinations(vertices, 2)
    }
    family = {
        state: cnf.var("f_" + "_".join(map(str, state)))
        for state in triples
    }
    witness = {
        (u, v, w): cnf.var(f"w_{u}_{v}_{w}")
        for u, v in itertools.combinations(vertices, 2)
        for w in vertices
        if w not in (u, v)
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

    def h(first: int, second: int) -> int:
        return edge[pair(first, second)]

    # alpha(G) <= 3, equivalently H is K4-free.
    if require_alpha_bound:
        for four in itertools.combinations(vertices, 4):
            cnf.add(*(-h(u, v) for u, v in itertools.combinations(four, 2)))

    # gamma(G) >= 3: every pair has a common H-neighbor.
    if require_global_gamma:
        for u, v in itertools.combinations(vertices, 2):
            choices = [w for w in vertices if w not in (u, v)]
            cnf.add(*(witness[(u, v, w)] for w in choices))
            for w in choices:
                z = witness[(u, v, w)]
                cnf.add(-z, h(u, w))
                cnf.add(-z, h(v, w))

    # The deletion also has gamma >= 3.
    if require_deletion_gamma:
        for u, v in itertools.combinations(deletion, 2):
            choices = [w for w in deletion if w not in (u, v)]
            local = [cnf.var(f"wd_{u}_{v}_{w}") for w in choices]
            cnf.add(*local)
            for z, w in zip(local, choices, strict=True):
                cnf.add(-z, h(u, w))
                cnf.add(-z, h(v, w))

    # An exact proper 3-coloring of H-x with free colors on all residual
    # vertices.  For C5, its canonical 0,1,0,1,2 pattern is WLOG up to a
    # dihedral cycle symmetry and color permutation.  The root labels can be
    # permuted independently inside their distinguished triangle.
    if require_deletion_coloring:
        color = {
            (vertex, value): cnf.var(f"c_{vertex}_{value}")
            for vertex in deletion
            for value in range(3)
        }
        for vertex in deletion:
            cnf.add(*(color[(vertex, value)] for value in range(3)))
            for first, second in itertools.combinations(range(3), 2):
                cnf.add(-color[(vertex, first)], -color[(vertex, second)])
        for u, v in itertools.combinations(deletion, 2):
            for value in range(3):
                cnf.add(-h(u, v), -color[(u, value)], -color[(v, value)])
        if require_full_root:
            for vertex, value in zip(ROOT, range(3), strict=True):
                cnf.add(color[(vertex, value)])
        if shape == "c5":
            for vertex, value in enumerate((0, 1, 0, 1, 2)):
                cnf.add(color[(vertex, value)])
        if force_rainbow_path:
            if shape != "path3":
                raise ValueError("rainbow path requires path3")
            for vertex, value in enumerate((0, 1, 2)):
                cnf.add(color[(vertex, value)])

    if shape in {"c4", "c5"}:
        # Named induced cycle in H-x.
        cycle_edges = {
            pair(inactive[index], inactive[(index + 1) % len(inactive)])
            for index in range(len(inactive))
        }
        for u, v in itertools.combinations(inactive, 2):
            cnf.add(h(u, v) if pair(u, v) in cycle_edges else -h(u, v))
    elif shape in {"edge", "path3"}:
        for u, v in zip(inactive, inactive[1:]):
            cnf.add(h(u, v))
    if force_divergent_witness:
        if shape != "path3" or n <= 11:
            raise ValueError("divergent witness requires path3 and n >= 12")
        cnf.add(h(0, 10))
        cnf.add(h(1, 10))
        cnf.add(-h(2, 10))
    if named_cycle_witnesses or witness_partition is not None:
        if shape != "c5":
            raise ValueError("named witnesses require C5")
        if witness_partition is None:
            witness_partition = "01234"
        if (
            len(witness_partition) != 5
            or witness_partition[0] != "0"
            or any(character not in "01234" for character in witness_partition)
        ):
            raise ValueError("witness partition must be a length-five RGS")
        labels = tuple(int(character) for character in witness_partition)
        maximum = -1
        for label in labels:
            if label > maximum + 1:
                raise ValueError("witness partition is not restricted-growth")
            maximum = max(maximum, label)
        if n != 7 + maximum:
            raise ValueError("order does not match witness partition")
        for index, label in enumerate(labels):
            witness_vertex = 5 + label
            cnf.add(h(index, witness_vertex))
            cnf.add(h((index + 1) % 5, witness_vertex))
            cnf.add(
                family[
                    tuple(sorted((index, (index + 1) % 5, witness_vertex)))
                ]
            )
            if named_inactivity_only:
                cnf.add(
                    -family[
                        tuple(sorted(((index + 1) % 5, witness_vertex, x)))
                    ]
                )
                cnf.add(
                    -family[tuple(sorted((index, witness_vertex, x)))]
                )

    # Selected family states dominate G.
    for state in triples:
        selected = family[state]
        for attacked in vertices:
            if attacked in state:
                continue
            # A state misses attacked in G exactly if attacked has an H-edge
            # to every occupied vertex.
            cnf.add(-selected, -h(attacked, state[0]),
                    -h(attacked, state[1]), -h(attacked, state[2]))

    # Literal one-guard closure.
    cnf.add(*family.values())
    if require_closure:
        for state in triples:
            selected = family[state]
            for attacked in vertices:
                if attacked in state:
                    continue
                responses: list[int] = []
                for guard in state:
                    z = move[(state, attacked, guard)]
                    successor = tuple(
                        sorted((set(state) - {guard}) | {attacked})
                    )
                    responses.append(z)
                    cnf.add(-z, -h(guard, attacked))
                    cnf.add(-z, family[successor])
                cnf.add(-selected, *responses)

    # Every H-triangle (maximum independent triple of G) is retained.
    if force_all_independent_states:
        for state in triples:
            cnf.add(
                -h(state[0], state[1]),
                -h(state[0], state[2]),
                -h(state[1], state[2]),
                family[state],
            )

    # The fixed root is an H-triangle and, normally, has a full family
    # response at x.
    if require_full_root:
        for u, v in itertools.combinations(ROOT, 2):
            cnf.add(h(u, v))
        cnf.add(family[ROOT])
        for guard in ROOT:
            cnf.add(-h(guard, x))
            successor = tuple(sorted((set(ROOT) - {guard}) | {x}))
            cnf.add(family[successor])

    # Every named C5 vertex is dynamically inactive at x.  Conditional on
    # an H-triangle T containing r, the successor T-r+x is excluded.
    if not named_inactivity_only:
        for r in inactive:
            for other in itertools.combinations(
                [v for v in deletion if v != r], 2
            ):
                state = tuple(sorted((r, *other)))
                successor = tuple(sorted((*other, x)))
                cnf.add(
                    -h(state[0], state[1]),
                    -h(state[0], state[2]),
                    -h(state[1], state[2]),
                    -family[successor],
                )

    # The accepted odd-wheel obstruction already eliminates the case in
    # which x is an H-neighbor of the entire C5.  Force at least one cycle
    # vertex to be physically adjacent to x in G, so a model tests the
    # genuinely dynamic boundary.
    if require_physical_mix:
        cnf.add(*(-h(r, x) for r in inactive))

    return cnf, edge, family


def solve(
    n: int,
    solver: Path,
    *,
    shape: str,
    require_physical_mix: bool,
    require_closure: bool,
    require_full_root: bool,
    require_deletion_coloring: bool,
    require_deletion_gamma: bool,
    force_divergent_witness: bool,
    force_rainbow_path: bool,
    require_global_gamma: bool,
    named_cycle_witnesses: bool,
    require_alpha_bound: bool,
    force_all_independent_states: bool,
    named_inactivity_only: bool,
    witness_partition: str | None,
) -> int:
    cnf, edge, family = build(
        n,
        shape=shape,
        require_physical_mix=require_physical_mix,
        require_closure=require_closure,
        require_full_root=require_full_root,
        require_deletion_coloring=require_deletion_coloring,
        require_deletion_gamma=require_deletion_gamma,
        force_divergent_witness=force_divergent_witness,
        force_rainbow_path=force_rainbow_path,
        require_global_gamma=require_global_gamma,
        named_cycle_witnesses=named_cycle_witnesses,
        require_alpha_bound=require_alpha_bound,
        force_all_independent_states=force_all_independent_states,
        named_inactivity_only=named_inactivity_only,
        witness_partition=witness_partition,
    )
    with tempfile.TemporaryDirectory(prefix="inactive-c5-dynamic-") as temp:
        instance = Path(temp) / "instance.cnf"
        model_path = Path(temp) / "model.out"
        instance.write_text(cnf.dimacs(), encoding="ascii")
        completed = subprocess.run(
            [str(solver), str(instance)],
            check=False,
            capture_output=True,
            text=True,
        )
        model_path.write_text(completed.stdout, encoding="utf-8")
    print(
        f"n={n} vars={len(cnf.names)-1} clauses={len(cnf.clauses)} "
        f"returncode={completed.returncode}"
    )
    print(completed.stdout)
    if completed.returncode != 10:
        return completed.returncode
    values: dict[int, bool] = {}
    for line in completed.stdout.splitlines():
        if not line.startswith("v "):
            continue
        for literal_text in line.split()[1:]:
            literal = int(literal_text)
            if literal:
                values[abs(literal)] = literal > 0
    h_edges = [uv for uv, variable in edge.items() if values.get(variable, False)]
    selected = [
        state
        for state, variable in family.items()
        if values.get(variable, False)
    ]
    print("H_EDGES", h_edges)
    print("FAMILY", selected)
    return 10


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument(
        "--shape",
        choices=("single", "edge", "path3", "c4", "c5"),
        default="c5",
    )
    parser.add_argument("--allow-odd-wheel", action="store_true")
    parser.add_argument("--no-closure", action="store_true")
    parser.add_argument("--no-full-root", action="store_true")
    parser.add_argument("--no-deletion-coloring", action="store_true")
    parser.add_argument("--no-deletion-gamma", action="store_true")
    parser.add_argument("--force-divergent-witness", action="store_true")
    parser.add_argument("--force-rainbow-path", action="store_true")
    parser.add_argument("--no-global-gamma", action="store_true")
    parser.add_argument("--named-cycle-witnesses", action="store_true")
    parser.add_argument("--no-alpha-bound", action="store_true")
    parser.add_argument("--no-force-all-independent", action="store_true")
    parser.add_argument("--named-inactivity-only", action="store_true")
    parser.add_argument("--witness-partition")
    arguments = parser.parse_args()
    raise SystemExit(
        solve(
            arguments.n,
            arguments.solver.resolve(),
            shape=arguments.shape,
            require_physical_mix=not arguments.allow_odd_wheel,
            require_closure=not arguments.no_closure,
            require_full_root=not arguments.no_full_root,
            require_deletion_coloring=not arguments.no_deletion_coloring,
            require_deletion_gamma=not arguments.no_deletion_gamma,
            force_divergent_witness=arguments.force_divergent_witness,
            force_rainbow_path=arguments.force_rainbow_path,
            require_global_gamma=not arguments.no_global_gamma,
            named_cycle_witnesses=arguments.named_cycle_witnesses,
            require_alpha_bound=not arguments.no_alpha_bound,
            force_all_independent_states=not arguments.no_force_all_independent,
            named_inactivity_only=arguments.named_inactivity_only,
            witness_partition=arguments.witness_partition,
        )
    )


if __name__ == "__main__":
    main()

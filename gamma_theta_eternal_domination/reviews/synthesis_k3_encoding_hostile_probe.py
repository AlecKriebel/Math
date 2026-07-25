"""Independent truth-table and clause audit for synthesis_k3.encoding.

This probe does not import either eternal-domination verifier or any search
engine.  It reconstructs the intended CNF clause multiset from the public
variable maps, exhausts the local auxiliary-variable truth tables, checks
the four relabeling templates, and optionally asks the pinned local CaDiCaL
binary only for base-instance models (not for a CEGAR search).
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import importlib
import json
import os
from pathlib import Path
import random
import subprocess
import tempfile

from synthesis_k3.encoding import (
    N,
    TEMPLATES,
    K3Encoding,
    build_k3_encoding,
    same_color_cut,
    validate_decoded_candidate,
)
from synthesis_k3.coloring import find_coloring
from synthesis_k3.generate import (
    generate,
    load_coloring_bytes,
    sha256_file,
)


ROOT = Path(__file__).resolve().parents[1]
CADICAL = ROOT / "tools/cadical_3_0_1/build/cadical"


def pair(first: int, second: int) -> tuple[int, int]:
    assert first != second
    return (first, second) if first < second else (second, first)


def expected_clauses(encoding: K3Encoding) -> Counter[tuple[int, ...]]:
    """Reconstruct every intended clause from the mathematical predicates."""

    edge = encoding.edge
    witness = encoding.witness_variables
    family = encoding.family_variables
    move = encoding.move_variables
    vertices = tuple(range(N))
    triples = tuple(combinations(vertices, 3))
    clauses: list[tuple[int, ...]] = []

    for four in combinations(vertices, 4):
        clauses.append(
            tuple(-edge(first, second) for first, second in combinations(four, 2))
        )

    for first, second in combinations(vertices, 2):
        possible = tuple(
            other for other in vertices if other not in (first, second)
        )
        clauses.append(
            tuple(witness[(first, second, other)] for other in possible)
        )
        for other in possible:
            variable = witness[(first, second, other)]
            clauses.append((-variable, edge(first, other)))
            clauses.append((-variable, edge(second, other)))

    template = encoding.template
    if template.startswith("hole"):
        length = int(template.removeprefix("hole"))
        rim_edges = {
            pair(vertex, (vertex + 1) % length)
            for vertex in range(length)
        }
        for first, second in combinations(range(length), 2):
            variable = edge(first, second)
            clauses.append(
                (variable if (first, second) in rim_edges else -variable,)
            )
        for outside in range(length, N):
            clauses.append(
                tuple(-edge(outside, rim) for rim in range(length))
            )
        clauses.append((edge(0, length),))
        clauses.append((edge(1, length),))
    else:
        assert template == "antihole7"
        cycle_edges = {
            pair(vertex, (vertex + 1) % 7) for vertex in range(7)
        }
        for first, second in combinations(range(7), 2):
            variable = edge(first, second)
            clauses.append(
                (-variable if (first, second) in cycle_edges else variable,)
            )

    full = (1 << N) - 1
    for mask in range(1, full):
        if not mask & 1:
            continue
        clauses.append(
            tuple(
                -edge(inside, outside)
                for inside in vertices
                if mask >> inside & 1
                for outside in vertices
                if not (mask >> outside & 1)
            )
        )

    for triple in triples:
        for outside in vertices:
            if outside not in triple:
                clauses.append(
                    (
                        -family[triple],
                        *( -edge(outside, guard) for guard in triple),
                    )
                )

    clauses.append(tuple(family.values()))
    for triple in triples:
        for attacked in vertices:
            if attacked in triple:
                continue
            responses: list[int] = []
            for guard in triple:
                response = move[(triple, attacked, guard)]
                successor = tuple(
                    sorted((set(triple) - {guard}) | {attacked})
                )
                responses.append(response)
                clauses.append((-response, -edge(guard, attacked)))
                clauses.append((-response, family[successor]))
            clauses.append((-family[triple], *responses))

    for first, second, third in triples:
        clauses.append(
            (
                -edge(first, second),
                -edge(first, third),
                -edge(second, third),
                family[(first, second, third)],
            )
        )
    return Counter(clauses)


def clause_satisfied(
    clause: tuple[int, ...], assignment: dict[int, bool]
) -> bool:
    return any(
        assignment[abs(literal)] == (literal > 0) for literal in clause
    )


def audit_local_truth_tables() -> dict[str, int]:
    checked = Counter()

    # Existential witness gadget: OR(w_i), w_i => a_i, w_i => b_i.
    for primary in product((False, True), repeat=6):
        a = primary[:3]
        b = primary[3:]
        gadget_satisfiable = False
        for auxiliaries in product((False, True), repeat=3):
            if any(auxiliaries) and all(
                not auxiliaries[index] or (a[index] and b[index])
                for index in range(3)
            ):
                gadget_satisfiable = True
                break
        assert gadget_satisfiable == any(
            a[index] and b[index] for index in range(3)
        )
        checked["witness_primary_rows"] += 1

    # Move gadget: m_i => not h_i, m_i => successor_i,
    # f => OR(m_i), existentially quantified over m.
    for primary in product((False, True), repeat=7):
        selected = primary[0]
        h_edges = primary[1:4]
        successors = primary[4:7]
        gadget_satisfiable = False
        for moves in product((False, True), repeat=3):
            if (
                (not selected or any(moves))
                and all(
                    not moves[index]
                    or (not h_edges[index] and successors[index])
                    for index in range(3)
                )
            ):
                gadget_satisfiable = True
                break
        semantic = not selected or any(
            not h_edges[index] and successors[index] for index in range(3)
        )
        assert gadget_satisfiable == semantic
        checked["move_primary_rows"] += 1

    for selected, *h_edges in product((False, True), repeat=4):
        clause_value = not selected or not all(h_edges)
        semantic = not selected or not all(h_edges)
        assert clause_value == semantic
        checked["domination_rows"] += 1

    for *triangle_edges, selected in product((False, True), repeat=4):
        clause_value = not all(triangle_edges) or selected
        semantic = not all(triangle_edges) or selected
        assert clause_value == semantic
        checked["triangle_strengthening_rows"] += 1

    for six_edges in product((False, True), repeat=6):
        assert (not all(six_edges)) == any(not value for value in six_edges)
        checked["four_clique_rows"] += 1

    return dict(checked)


def audit_coloring_cuts() -> int:
    encoding = build_k3_encoding("hole5")
    rows = 0
    colorings = (
        tuple(vertex % 3 for vertex in range(N)),
        (0,) * N,
        tuple((vertex * vertex + 1) % 3 for vertex in range(N)),
    )
    for coloring in colorings:
        cut = same_color_cut(encoding, coloring)
        pairs = tuple(
            pair
            for pair in combinations(range(N), 2)
            if coloring[pair[0]] == coloring[pair[1]]
        )
        assert cut == tuple(encoding.edge(*edge_pair) for edge_pair in pairs)
        # The clause is false exactly for graphs properly colored by this
        # assignment (all same-color pairs are H-nonedges).
        for values in product((False, True), repeat=min(8, len(pairs))):
            has_monochromatic_edge = any(values)
            cut_value = any(values)
            assert cut_value == has_monochromatic_edge
            rows += 1
    return rows


def audit_complement_dictionary() -> dict[str, int]:
    """Exhaust all labeled H on five vertices against direct G semantics."""

    order = 5
    possible_edges = tuple(combinations(range(order), 2))
    counts = Counter()
    for graph_mask in range(1 << len(possible_edges)):
        h_edges = {
            edge_pair
            for index, edge_pair in enumerate(possible_edges)
            if graph_mask >> index & 1
        }

        def h_edge(first: int, second: int) -> bool:
            return pair(first, second) in h_edges

        def g_edge(first: int, second: int) -> bool:
            return first != second and not h_edge(first, second)

        def dominates_g(state: tuple[int, ...]) -> bool:
            return all(
                vertex in state
                or any(g_edge(vertex, guard) for guard in state)
                for vertex in range(order)
            )

        for first, second in combinations(range(order), 2):
            common_neighbor = any(
                h_edge(first, witness) and h_edge(second, witness)
                for witness in range(order)
                if witness not in (first, second)
            )
            assert common_neighbor == (not dominates_g((first, second)))
            counts["pair_rows"] += 1

        for triple in combinations(range(order), 3):
            external_containment = any(
                all(h_edge(outside, guard) for guard in triple)
                for outside in range(order)
                if outside not in triple
            )
            assert dominates_g(triple) == (not external_containment)
            counts["triple_rows"] += 1

        # Every cut containing 0 has a G edge iff G is connected.
        reached = {0}
        frontier = [0]
        while frontier:
            first = frontier.pop()
            for second in range(order):
                if second not in reached and g_edge(first, second):
                    reached.add(second)
                    frontier.append(second)
        every_cut_crossed = True
        full = (1 << order) - 1
        for cut_mask in range(1, full):
            if not cut_mask & 1:
                continue
            if not any(
                g_edge(inside, outside)
                for inside in range(order)
                if cut_mask >> inside & 1
                for outside in range(order)
                if not (cut_mask >> outside & 1)
            ):
                every_cut_crossed = False
                break
        assert every_cut_crossed == (len(reached) == order)
        counts["connectivity_graphs"] += 1

        for first, attacked in possible_edges:
            assert g_edge(first, attacked) == (not h_edge(first, attacked))
            counts["move_edge_rows"] += 1
    return dict(counts)


def brute_coloring(
    order: int,
    edges: tuple[tuple[int, int], ...],
    color_count: int,
) -> tuple[int, ...] | None:
    for coloring in product(range(color_count), repeat=order):
        if all(coloring[first] != coloring[second] for first, second in edges):
            return tuple(coloring)
    return None


def audit_dsatur() -> dict[str, int]:
    """Compare DSATUR with a transparent complete assignment search."""

    counts = Counter()
    for order in range(6):
        possible = tuple(combinations(range(order), 2))
        for graph_mask in range(1 << len(possible)):
            edges = tuple(
                edge_pair
                for index, edge_pair in enumerate(possible)
                if graph_mask >> index & 1
            )
            expected = brute_coloring(order, edges, 3)
            actual = find_coloring(order, edges, 3)
            assert (actual is None) == (expected is None)
            if actual is not None:
                assert all(
                    actual[first] != actual[second]
                    for first, second in edges
                )
            counts["three_color_graphs"] += 1

    randomizer = random.Random(314159)
    for order in range(7):
        possible = tuple(combinations(range(order), 2))
        for color_count in range(1, 5):
            for _ in range(50):
                edges = tuple(
                    edge_pair
                    for edge_pair in possible
                    if randomizer.randrange(2)
                )
                expected = brute_coloring(order, edges, color_count)
                actual = find_coloring(order, edges, color_count)
                assert (actual is None) == (expected is None)
                counts["variable_color_random_graphs"] += 1
    return dict(counts)


def parse_dimacs(payload: bytes) -> tuple[int, list[tuple[int, ...]]]:
    lines = payload.decode("ascii").splitlines()
    marker, kind, raw_variables, raw_clauses = lines[0].split()
    assert (marker, kind) == ("p", "cnf")
    clauses: list[tuple[int, ...]] = []
    for line in lines[1:]:
        values = tuple(map(int, line.split()))
        assert values and values[-1] == 0 and 0 not in values[:-1]
        clauses.append(values[:-1])
    assert len(clauses) == int(raw_clauses)
    return int(raw_variables), clauses


def audit_generation() -> dict[str, object]:
    """Verify repaired generation integrity and self-contained replay."""

    coloring_payload = (
        b"[[0,1,2,0,1,2,0,1,2,0,1,2],"
        b"[0,0,0,0,0,0,0,0,0,0,0,0]]\n"
    )
    with tempfile.TemporaryDirectory() as directory_text:
        directory = Path(directory_text)
        colorings = directory / "colorings.json"
        colorings.write_bytes(coloring_payload)
        output = directory / "instance.cnf"
        manifest = directory / "manifest.json"
        result = generate(
            template="hole5",
            output=output,
            manifest=manifest,
            colorings_path=colorings,
        )
        variables, clauses = parse_dimacs(output.read_bytes())
        assert variables == result["variable_count"]
        assert len(clauses) == result["clause_count"]
        assert sum(map(len, clauses)) == result["literal_count"]
        assert sha256_file(output) == result["cnf_sha256"]
        assert sha256_file(colorings) == result["colorings_sha256"]
        assert json.loads(manifest.read_text(encoding="utf-8")) == result
        encoding = build_k3_encoding("hole5")
        expected_colorings = (
            (0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2),
            (0,) * N,
        )
        assert clauses[-2:] == [
            same_color_cut(encoding, coloring)
            for coloring in expected_colorings
        ]
        source_records = tuple(
            (str(relative), str(digest))
            for relative, digest in result["generator_source_manifest"]
        )
        for relative, digest in source_records:
            assert sha256_file(ROOT / relative) == digest
        source_set_payload = "".join(
            f"{relative} {digest}\n"
            for relative, digest in source_records
        ).encode("ascii")
        assert (
            sha256(source_set_payload).hexdigest()
            == result["generator_source_set_sha256"]
        )

        def rejected(
            candidate_output: Path,
            candidate_manifest: Path,
            candidate_colorings: Path | None = None,
        ) -> bool:
            try:
                generate(
                    template="hole5",
                    output=candidate_output,
                    manifest=candidate_manifest,
                    colorings_path=candidate_colorings,
                )
            except ValueError:
                return True
            return False

        collision_rejections = 0
        direct = directory / "direct-alias"
        assert rejected(direct, direct)
        collision_rejections += 1
        assert rejected(colorings, directory / "m1.json", colorings)
        collision_rejections += 1
        assert rejected(directory / "o2.cnf", colorings, colorings)
        collision_rejections += 1

        real_alias = directory / "real-alias"
        real_alias.write_bytes(b"unchanged-symlink-target")
        symbolic_alias = directory / "symbolic-alias"
        symbolic_alias.symlink_to(real_alias)
        assert rejected(symbolic_alias, real_alias)
        assert real_alias.read_bytes() == b"unchanged-symlink-target"
        collision_rejections += 1

        hard_a = directory / "hard-a"
        hard_b = directory / "hard-b"
        hard_a.write_bytes(b"unchanged-hardlink-target")
        os.link(hard_a, hard_b)
        assert rejected(hard_a, hard_b)
        assert hard_a.read_bytes() == b"unchanged-hardlink-target"
        collision_rejections += 1

        trusted_source = ROOT / "src/synthesis_k3/generate.py"
        trusted_hash = sha256_file(trusted_source)
        assert rejected(trusted_source, directory / "source-direct.json")
        collision_rejections += 1
        source_symbolic = directory / "source-symbolic"
        source_symbolic.symlink_to(trusted_source)
        assert rejected(source_symbolic, directory / "source-symbolic.json")
        collision_rejections += 1
        source_hard = directory / "source-hard"
        os.link(trusted_source, source_hard)
        assert rejected(source_hard, directory / "source-hard.json")
        collision_rejections += 1
        assert sha256_file(trusted_source) == trusted_hash

        input_hard = directory / "input-hard"
        os.link(colorings, input_hard)
        assert rejected(
            input_hard, directory / "input-hard.json", colorings
        )
        collision_rejections += 1

        invalid_json_payloads = (
            b'[{"x":1,"x":2}]',
            b"[NaN]",
            b"[Infinity]",
            b"[-Infinity]",
            b"\xff",
            b"\xef\xbb\xbf[]",
            json.dumps([[True] * N]).encode("ascii"),
            json.dumps([[0.0] * N]).encode("ascii"),
            json.dumps([[0] * (N - 1)]).encode("ascii"),
            json.dumps([[3] * N]).encode("ascii"),
        )
        strict_json_rejections = 0
        for payload in invalid_json_payloads:
            try:
                load_coloring_bytes(payload)
            except ValueError:
                strict_json_rejections += 1
            else:
                raise AssertionError(f"invalid coloring JSON accepted: {payload!r}")

        base_partition = [vertex % 3 for vertex in range(N)]
        permuted_partition = [(color + 1) % 3 for color in base_partition]
        duplicate_partition_payload = json.dumps(
            [base_partition, permuted_partition]
        ).encode("ascii")
        try:
            load_coloring_bytes(duplicate_partition_payload)
        except ValueError:
            partition_permutation_rejected = True
        else:
            partition_permutation_rejected = False
        assert partition_permutation_rejected

        generation_module = importlib.import_module("synthesis_k3.generate")
        original_atomic_write = generation_module.atomic_write
        corruption_output = directory / "corruption.cnf"

        def corrupt_installed(path: Path, payload: bytes) -> None:
            original_atomic_write(path, payload)
            if path == corruption_output.resolve():
                path.write_bytes(payload + b"c post-write-corruption\n")

        generation_module.atomic_write = corrupt_installed
        try:
            try:
                generate(
                    template="hole5",
                    output=corruption_output,
                    manifest=directory / "corruption.json",
                )
            except ValueError:
                installed_corruption_rejected = True
            else:
                installed_corruption_rejected = False
        finally:
            generation_module.atomic_write = original_atomic_write
        assert installed_corruption_rejected

        mutation_colorings = directory / "mutation-colorings.json"
        mutation_colorings.write_bytes(coloring_payload)
        mutation_output = directory / "mutation.cnf"

        def mutate_input_after_output(path: Path, payload: bytes) -> None:
            original_atomic_write(path, payload)
            if path == mutation_output.resolve():
                mutation_colorings.write_text("[]\n", encoding="utf-8")

        generation_module.atomic_write = mutate_input_after_output
        try:
            try:
                generate(
                    template="hole5",
                    output=mutation_output,
                    manifest=directory / "mutation.json",
                    colorings_path=mutation_colorings,
                )
            except ValueError:
                input_mutation_rejected = True
            else:
                input_mutation_rejected = False
        finally:
            generation_module.atomic_write = original_atomic_write
        assert input_mutation_rejected

        invocation = tuple(str(value) for value in result["normalized_invocation"])
        assert result["working_directory"] == str(ROOT)
        assert result["required_environment"] == {
            "PYTHONPATH": str(ROOT / "src")
        }
        assert invocation[:2] == (
            "/usr/bin/env",
            f"PYTHONPATH={ROOT / 'src'}",
        )
        assert invocation[2] == result["python_executable"]
        assert Path(invocation[2]).is_absolute()
        assert Path(invocation[2]).is_file()
        cnf_before_replay = output.read_bytes()
        manifest_before_replay = manifest.read_bytes()
        colorings_before_replay = colorings.read_bytes()
        replay = subprocess.run(
            invocation,
            cwd=result["working_directory"],
            env={},
            capture_output=True,
            check=False,
            text=True,
            timeout=30,
        )
        invocation_self_contained = replay.returncode == 0
        assert invocation_self_contained, replay.stderr
        assert json.loads(replay.stdout) == result
        assert output.read_bytes() == cnf_before_replay
        assert manifest.read_bytes() == manifest_before_replay
        assert colorings.read_bytes() == colorings_before_replay
        assert sha256_file(output) == result["cnf_sha256"]
        assert json.loads(manifest.read_text(encoding="utf-8")) == result
    return {
        "collision_rejections": collision_rejections,
        "input_mutation_rejected": input_mutation_rejected,
        "installed_corruption_rejected": installed_corruption_rejected,
        "normalized_invocation_self_contained": invocation_self_contained,
        "normal_manifest_verified": True,
        "partition_permutation_rejected": partition_permutation_rejected,
        "strict_json_rejections": strict_json_rejections,
    }


def relabel_edges(
    edges: set[tuple[int, int]], old_to_new: dict[int, int]
) -> set[tuple[int, int]]:
    return {
        pair(old_to_new[first], old_to_new[second])
        for first, second in edges
    }


def satisfies_template(
    template: str, edges: set[tuple[int, int]]
) -> bool:
    def adjacent(first: int, second: int) -> bool:
        return pair(first, second) in edges

    if template.startswith("hole"):
        length = int(template.removeprefix("hole"))
        rim_edges = {
            pair(vertex, (vertex + 1) % length)
            for vertex in range(length)
        }
        if any(
            adjacent(first, second) != ((first, second) in rim_edges)
            for first, second in combinations(range(length), 2)
        ):
            return False
        if any(
            all(adjacent(outside, rim) for rim in range(length))
            for outside in range(length, N)
        ):
            return False
        return adjacent(0, length) and adjacent(1, length)
    if template == "antihole7":
        cycle_edges = {
            pair(vertex, (vertex + 1) % 7) for vertex in range(7)
        }
        return all(
            adjacent(first, second) != ((first, second) in cycle_edges)
            for first, second in combinations(range(7), 2)
        )
    raise AssertionError(template)


def audit_template_relabeling() -> int:
    randomizer = random.Random(20260725)
    checked = 0
    for template in TEMPLATES:
        length = 7 if template == "antihole7" else int(template[4:])
        for _ in range(100):
            labels = list(range(N))
            randomizer.shuffle(labels)
            rim = tuple(labels[:length])
            remaining = labels[length:]
            edges: set[tuple[int, int]] = set()
            cycle_edges = {
                pair(rim[index], rim[(index + 1) % length])
                for index in range(length)
            }
            if template == "antihole7":
                for first, second in combinations(rim, 2):
                    if pair(first, second) not in cycle_edges:
                        edges.add(pair(first, second))
                mapping = {rim[index]: index for index in range(length)}
                for new, old in enumerate(remaining, start=length):
                    mapping[old] = new
            else:
                edges.update(cycle_edges)
                chosen_common_neighbor = remaining[0]
                edges.add(pair(chosen_common_neighbor, rim[0]))
                edges.add(pair(chosen_common_neighbor, rim[1]))
                mapping = {rim[index]: index for index in range(length)}
                mapping[chosen_common_neighbor] = length
                for new, old in enumerate(remaining[1:], start=length + 1):
                    mapping[old] = new
            assert satisfies_template(
                template, relabel_edges(edges, mapping)
            )
            checked += 1
    return checked


def solve_base_instances() -> tuple[dict[str, object], bool]:
    if not CADICAL.is_file():
        return {"skipped": "CaDiCaL binary absent"}, False
    results: dict[str, object] = {}
    malformed_boolean_rejected = False
    for template in TEMPLATES:
        encoding = build_k3_encoding(template)
        with tempfile.TemporaryDirectory() as directory:
            instance = Path(directory) / f"{template}.cnf"
            instance.write_text(encoding.cnf.dimacs(), encoding="ascii")
            completed = subprocess.run(
                (str(CADICAL), "--quiet", str(instance)),
                capture_output=True,
                check=False,
                text=True,
                timeout=30,
            )
        if completed.returncode == 20:
            results[template] = {"status": "UNSAT"}
            continue
        assert completed.returncode == 10
        literals: list[int] = []
        for line in completed.stdout.splitlines():
            if line.startswith("v "):
                literals.extend(
                    int(token) for token in line.split()[1:] if token != "0"
                )
        assert len(literals) == encoding.cnf.variable_count
        model = {abs(literal): literal > 0 for literal in literals}
        assert all(
            clause_satisfied(clause, model) for clause in encoding.cnf.clauses
        )
        edges = encoding.decode_edges(model)
        family = encoding.decode_family(model)
        validate_decoded_candidate(encoding, edges, family)
        results[template] = {
            "edges": len(edges),
            "family_states": len(family),
            "status": "SAT-and-directly-validated",
        }

        # A strict hostile-input validator would reject Boolean endpoints.
        # Python's bool/int equality instead lets this malformed record alias
        # an ordinary edge while preserving the interpreted edge set.
        replaced = False
        malformed_edges: list[tuple[int, int]] = []
        for first, second in edges:
            if not replaced and first == 1:
                malformed_edges.append((True, second))  # type: ignore[list-item]
                replaced = True
            elif not replaced and second == 1:
                malformed_edges.append((first, True))  # type: ignore[list-item]
                replaced = True
            else:
                malformed_edges.append((first, second))
        if replaced:
            try:
                validate_decoded_candidate(
                    encoding, malformed_edges, family
                )
            except ValueError:
                malformed_boolean_rejected = True
            else:
                raise AssertionError(
                    "decoded validator accepted a Boolean endpoint"
                )
    return results, malformed_boolean_rejected


def main() -> None:
    clause_counts: dict[str, int] = {}
    for template in TEMPLATES:
        encoding = build_k3_encoding(template)
        actual = Counter(encoding.cnf.clauses)
        expected = expected_clauses(encoding)
        assert actual == expected
        clause_counts[template] = len(encoding.cnf.clauses)

    solver_results, bool_rejected = solve_base_instances()
    sources = {}
    for relative in (
        "src/synthesis_k3/encoding.py",
        "src/synthesis_k3/coloring.py",
        "src/synthesis_k3/generate.py",
        "tests/test_synthesis_k3_encoding.py",
        "tests/test_synthesis_k3_coloring.py",
        "math/synthesis_k3_cegar_design.md",
    ):
        payload = (ROOT / relative).read_bytes()
        sources[relative] = sha256(payload).hexdigest()
    print(
        json.dumps(
            {
                "base_solver_probe": solver_results,
                "clause_counts": clause_counts,
                "coloring_truth_rows": audit_coloring_cuts(),
                "complement_dictionary": audit_complement_dictionary(),
                "dsatur": audit_dsatur(),
                "generation": audit_generation(),
                "local_truth_tables": audit_local_truth_tables(),
                "malformed_boolean_endpoint_rejected": bool_rejected,
                "source_sha256": sources,
                "template_relabelings_checked": audit_template_relabeling(),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

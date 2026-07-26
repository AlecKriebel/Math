#!/usr/bin/env python3
"""Clean-room audit of the order-13 strategy and exploratory pilot record.

This script imports only the Python standard library.  In particular, it
does not import any campaign encoder, coloring-bank generator, or checker.
It reconstructs the four exploratory k=3 DIMACS byte streams independently,
checks the generic anchored-formula census, and validates the pilot JSON and
all locally available source/tool/hardware bindings.

It never invokes a SAT solver on a formula.  The sole subprocess invocation
is ``cadical --version``.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Iterator, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
STRATEGY = ROOT / "math/lemmas/order13_strategy.md"
PILOT = ROOT / "results/logs/order13_strategy_k3_template_pilot.json"
SOURCE = ROOT / "src/synthesis_k3/encoding.py"
SOLVER = ROOT / "tools/cadical_3_0_1/build/cadical"

EXPECTED = {
    "strategy": {
        "sha256": "eca21b547641f5f205bf9f5325d49f6c8edb6e6c778ff9fefacc7d1449e6b5c8",
        "size_bytes": 14643,
    },
    "pilot": {
        "sha256": "331630a55b5d35d27f92e4104172811ab9e8ccac6aa14bb84de538dbc2b7148c",
        "size_bytes": 3177,
    },
    "source": {
        "sha256": "fda94aeb7a2c48e64f1b9a975c27263b100542359c13264f4a625f115ff563c6",
        "size_bytes": 15071,
    },
    "solver": {
        "sha256": "51c3c82b354f455c925fc60b37c701e8498afcf0f3bfab9a06e62149485df5f6",
        "size_bytes": 1571160,
    },
}

ORDER = 13
COLOR_COUNT = 3
TEMPLATES = ("hole5", "hole7", "hole9", "hole11")
EDGE_PAIRS = tuple(itertools.combinations(range(ORDER), 2))


class AuditError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def file_record(path: Path) -> dict[str, object]:
    payload = path.read_bytes()
    return {"sha256": sha256_bytes(payload), "size_bytes": len(payload)}


def canonical_json_bytes(value: object) -> bytes:
    return (
        json.dumps(value, allow_nan=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def strict_json(path: Path) -> tuple[object, bytes]:
    payload = path.read_bytes()
    text = payload.decode("utf-8")

    def reject_constant(token: str) -> object:
        raise AuditError(f"non-finite JSON constant {token!r}")

    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            require(key not in result, f"duplicate JSON key {key!r}")
            result[key] = value
        return result

    parsed = json.loads(
        text,
        object_pairs_hook=reject_duplicates,
        parse_constant=reject_constant,
    )
    return parsed, payload


def exact_keys(value: object, keys: set[str], role: str) -> Mapping[str, object]:
    require(isinstance(value, dict), f"{role} is not an object")
    require(set(value) == keys, f"{role} has unexpected keys")
    return value


def exact_int(value: object, role: str, *, minimum: int = 0) -> int:
    require(type(value) is int and value >= minimum, f"{role} is not an exact integer")
    return value


def finite_number(value: object, role: str, *, positive: bool = False) -> float:
    require(type(value) in (int, float), f"{role} is not numeric")
    result = float(value)
    require(math.isfinite(result), f"{role} is not finite")
    if positive:
        require(result > 0, f"{role} is not positive")
    return result


def pair(first: int, second: int) -> tuple[int, int]:
    require(first != second, "loop is not an edge")
    return (first, second) if first < second else (second, first)


def template_positive_edges(length: int) -> tuple[tuple[int, int], ...]:
    edges = {
        pair(vertex, (vertex + 1) % length) for vertex in range(length)
    }
    edges.update(((0, length), (1, length)))
    return tuple(sorted(edges))


def enumerate_rows(length: int) -> tuple[tuple[int, ...], ...]:
    """Enumerate restricted-growth rows proper on the forced true edges."""

    prior: list[list[int]] = [[] for _ in range(ORDER)]
    for first, second in template_positive_edges(length):
        prior[second].append(first)
    colors = [-1] * ORDER
    rows: list[tuple[int, ...]] = []

    def visit(vertex: int, maximum_used: int) -> None:
        if vertex == ORDER:
            rows.append(tuple(colors))
            return
        largest = min(COLOR_COUNT - 1, maximum_used + 1)
        for color in range(largest + 1):
            if any(colors[neighbor] == color for neighbor in prior[vertex]):
                continue
            colors[vertex] = color
            visit(vertex + 1, max(maximum_used, color))
            colors[vertex] = -1

    visit(0, -1)
    return tuple(rows)


def dimacs(variable_count: int, clauses: Sequence[Sequence[int]]) -> bytes:
    lines = [f"p cnf {variable_count} {len(clauses)}"]
    lines.extend(" ".join(map(str, clause)) + " 0" for clause in clauses)
    return ("\n".join(lines) + "\n").encode("ascii")


def reconstruct_template(length: int) -> dict[str, object]:
    """Independently reconstruct the exact runtime-parameterized bytes."""

    vertices = tuple(range(ORDER))
    triples = tuple(itertools.combinations(vertices, 3))
    next_variable = 1

    edges: dict[tuple[int, int], int] = {}
    for edge_pair in EDGE_PAIRS:
        edges[edge_pair] = next_variable
        next_variable += 1

    witnesses: dict[tuple[int, int, int], int] = {}
    for first, second in EDGE_PAIRS:
        for witness in vertices:
            if witness in (first, second):
                continue
            witnesses[(first, second, witness)] = next_variable
            next_variable += 1

    families: dict[tuple[int, int, int], int] = {}
    for triple in triples:
        families[triple] = next_variable
        next_variable += 1

    moves: dict[tuple[tuple[int, int, int], int, int], int] = {}
    for triple in triples:
        for attacked in vertices:
            if attacked in triple:
                continue
            for guard in triple:
                moves[(triple, attacked, guard)] = next_variable
                next_variable += 1

    variable_count = next_variable - 1
    require(variable_count == 9802, "clean-room variable allocation is wrong")

    def edge(first: int, second: int) -> int:
        return edges[pair(first, second)]

    clauses: list[tuple[int, ...]] = []

    for four_set in itertools.combinations(vertices, 4):
        clauses.append(
            tuple(
                -edge(first, second)
                for first, second in itertools.combinations(four_set, 2)
            )
        )

    for first, second in EDGE_PAIRS:
        available = tuple(v for v in vertices if v not in (first, second))
        clauses.append(
            tuple(witnesses[(first, second, witness)] for witness in available)
        )
        for witness in available:
            variable = witnesses[(first, second, witness)]
            clauses.append((-variable, edge(first, witness)))
            clauses.append((-variable, edge(second, witness)))

    rim = tuple(range(length))
    rim_edges = {
        pair(vertex, (vertex + 1) % length) for vertex in rim
    }
    for first, second in itertools.combinations(rim, 2):
        variable = edge(first, second)
        clauses.append((variable if (first, second) in rim_edges else -variable,))
    for outside in range(length, ORDER):
        clauses.append(tuple(-edge(outside, rim_vertex) for rim_vertex in rim))
    clauses.append((edge(0, length),))
    clauses.append((edge(1, length),))

    full = (1 << ORDER) - 1
    for mask in range(1, full):
        if not mask & 1:
            continue
        clauses.append(
            tuple(
                -edge(first, second)
                for first in vertices
                if mask >> first & 1
                for second in vertices
                if not (mask >> second & 1)
            )
        )

    for triple in triples:
        source = families[triple]
        for outside in vertices:
            if outside in triple:
                continue
            clauses.append(
                (
                    -source,
                    -edge(outside, triple[0]),
                    -edge(outside, triple[1]),
                    -edge(outside, triple[2]),
                )
            )

    clauses.append(tuple(families.values()))
    for triple in triples:
        source = families[triple]
        for attacked in vertices:
            if attacked in triple:
                continue
            response: list[int] = []
            for guard in triple:
                move = moves[(triple, attacked, guard)]
                successor = tuple(sorted((set(triple) - {guard}) | {attacked}))
                response.append(move)
                clauses.append((-move, -edge(guard, attacked)))
                clauses.append((-move, families[successor]))
            clauses.append((-source, *response))

    for triple in triples:
        clauses.append(
            (
                -edge(triple[0], triple[1]),
                -edge(triple[0], triple[2]),
                -edge(triple[1], triple[2]),
                families[triple],
            )
        )

    base_clauses = len(clauses)
    base_literals = sum(map(len, clauses))
    rows = enumerate_rows(length)
    for row in rows:
        clauses.append(
            tuple(
                edges[edge_pair]
                for edge_pair in EDGE_PAIRS
                if row[edge_pair[0]] == row[edge_pair[1]]
            )
        )

    payload = dimacs(variable_count, clauses)
    labeled_closed_form = (2**length - 2) * 3 ** (ORDER - length - 1)
    require(
        len(rows) * math.factorial(COLOR_COUNT) == labeled_closed_form,
        "coloring-bank count disagrees with cycle-polynomial orbit count",
    )
    return {
        "template": f"hole{length}",
        "variables": variable_count,
        "base_clauses": base_clauses,
        "base_literal_occurrences": base_literals,
        "complete_coloring_rows": len(rows),
        "full_clauses": len(clauses),
        "full_literal_occurrences": sum(map(len, clauses)),
        "full_size_bytes": len(payload),
        "full_sha256": sha256_bytes(payload),
        "labeled_coloring_count": labeled_closed_form,
        "color_orbit_size": math.factorial(COLOR_COUNT),
    }


def comparator_census(bits: int, comparators: int) -> tuple[int, int]:
    clauses = comparators * sum(2**prefix for prefix in range(bits))
    literals = comparators * sum(
        2**prefix * (2 * prefix + 2) for prefix in range(bits)
    )
    return clauses, literals


def generic_census(n: int, k: int) -> dict[str, object]:
    outer = n - k
    states = math.comb(n, k)
    move_variables = states * outer * k
    variables = (
        math.comb(n, 2)
        + math.comb(n, k - 1) * (n - k + 1)
        + states
        + move_variables
    )

    witnesses = math.comb(n, k - 1) * (n - k + 1)
    base_families = (
        (math.comb(n, k + 1), math.comb(n, k + 1) * math.comb(k + 1, 2)),
        (math.comb(n, k - 1), math.comb(n, k - 1) * (n - k + 1)),
        (witnesses * (k - 1), 2 * witnesses * (k - 1)),
        (math.comb(k, 2), math.comb(k, 2)),
        (2 ** (n - 1) - 1, math.comb(n, 2) * 2 ** (n - 2)),
        (states * outer, states * outer * (k + 1)),
        (1, states),
        (2 * move_variables, 4 * move_variables),
        (states * outer, states * outer * (k + 1)),
        (states, states * (math.comb(k, 2) + 1)),
    )
    base_clauses = sum(item[0] for item in base_families)
    base_literals = sum(item[1] for item in base_families)
    color_clauses = k**outer
    color_literals = outer * k**outer + math.comb(outer, 2) * k ** (outer - 1)
    row_clauses, row_literals = comparator_census(k, outer - 1)
    column_clauses, column_literals = comparator_census(outer, k - 1)

    return {
        "k": k,
        "states": states,
        "move_variables": move_variables,
        "all_variables": variables,
        "base_clauses": base_clauses,
        "base_literals": base_literals,
        "color_clauses": color_clauses,
        "color_literals": color_literals,
        "row_breaker_clauses": row_clauses,
        "row_breaker_literals": row_literals,
        "column_breaker_clauses": column_clauses,
        "column_breaker_literals": column_literals,
        "full_doublelex_clauses": (
            base_clauses + color_clauses + row_clauses + column_clauses
        ),
        "full_doublelex_literals": (
            base_literals + color_literals + row_literals + column_literals
        ),
    }


def signature_census(length: int) -> dict[str, int]:
    bits = length + 1
    free = ORDER - bits
    comparators = max(0, free - 1)
    clauses, literals = comparator_census(bits, comparators)
    return {
        "core_bits": bits,
        "free_vertices": free,
        "adjacent_comparators": comparators,
        "clauses": clauses,
        "literals": literals,
    }


def audit_pilot(
    parsed: object, reconstructed: Sequence[Mapping[str, object]]
) -> dict[str, object]:
    root = exact_keys(
        parsed,
        {
            "claim_boundary",
            "classification",
            "formula_generation",
            "hardware",
            "pilot",
            "repository_head",
            "schema",
            "schema_version",
            "timestamp_utc",
        },
        "pilot root",
    )
    require(root["classification"] == "OBSERVED", "classification is promoted")
    require(
        root["schema"] == "gamma-theta-order13-strategy-k3-template-pilot-v1"
        and root["schema_version"] == 1,
        "schema identity mismatch",
    )
    require(
        isinstance(root["claim_boundary"], str)
        and "not a mathematical claim" in root["claim_boundary"],
        "claim boundary is not explicit",
    )
    require(
        root["repository_head"] == "9df3a414e6ba9f631ff68bff69d5ab0a37048f5e",
        "repository head mismatch",
    )

    generation = exact_keys(
        root["formula_generation"], {"method", "source", "templates"}, "generation"
    )
    source = exact_keys(
        generation["source"], {"path", "sha256", "size_bytes"}, "source"
    )
    require(source["path"] == "src/synthesis_k3/encoding.py", "source path mismatch")
    require(source["sha256"] == EXPECTED["source"]["sha256"], "source hash mismatch")
    require(source["size_bytes"] == EXPECTED["source"]["size_bytes"], "source size mismatch")
    require(
        "runtime parameterization" in generation["method"]
        and "No repository source was modified" in generation["method"],
        "generation method boundary is missing",
    )

    require(isinstance(generation["templates"], list), "templates is not a list")
    pilot_template_keys = {
        "base_clauses",
        "base_literal_occurrences",
        "complete_coloring_rows",
        "full_clauses",
        "full_literal_occurrences",
        "full_size_bytes",
        "full_sha256",
        "template",
        "variables",
    }
    reconstructed_pilot_records = [
        {key: record[key] for key in pilot_template_keys}
        for record in reconstructed
    ]
    require(
        generation["templates"] == reconstructed_pilot_records,
        "pilot template records differ from independent byte reconstruction",
    )

    hardware = exact_keys(
        root["hardware"],
        {"logical_cpus", "model", "physical_memory_bytes"},
        "hardware",
    )
    require(hardware["logical_cpus"] == os.cpu_count(), "logical CPU binding mismatch")
    require(
        hardware["physical_memory_bytes"] == 17179869184,
        "physical memory binding mismatch",
    )
    require(hardware["model"] == "Apple M1 Pro", "hardware model mismatch")

    pilot = exact_keys(
        root["pilot"], {"formula_sha256", "formula_template", "result", "solver"}, "pilot"
    )
    require(pilot["formula_template"] == "hole11", "pilot template mismatch")
    require(pilot["result"] == "UNSAT_UNCERTIFIED", "pilot result is promoted")
    hole11 = reconstructed[-1]
    require(
        pilot["formula_sha256"] == hole11["full_sha256"],
        "pilot formula hash differs from clean-room bytes",
    )

    solver = exact_keys(
        pilot["solver"],
        {
            "exit_code",
            "internal_time_limit_seconds",
            "maximum_resident_set_size_bytes",
            "path",
            "seed",
            "sha256",
            "size_bytes",
            "wall_seconds",
        },
        "solver",
    )
    require(solver["exit_code"] == 20, "solver exit code is not UNSAT code 20")
    require(solver["internal_time_limit_seconds"] == 30, "time limit mismatch")
    exact_int(solver["maximum_resident_set_size_bytes"], "maximum RSS", minimum=1)
    require(solver["path"] == "tools/cadical_3_0_1/build/cadical", "solver path mismatch")
    require(solver["seed"] == 0, "solver seed mismatch")
    require(solver["sha256"] == EXPECTED["solver"]["sha256"], "solver hash mismatch")
    require(solver["size_bytes"] == EXPECTED["solver"]["size_bytes"], "solver size mismatch")
    finite_number(solver["wall_seconds"], "wall time", positive=True)

    return {
        "classification": root["classification"],
        "result": pilot["result"],
        "exact_formula_bytes_reconstructed": True,
        "formula_hash_bound": True,
        "source_binding_checked": True,
        "solver_binary_binding_checked": True,
        "hardware_binding_checked": True,
        "strict_json_no_duplicate_or_nonfinite_values": True,
        "canonical_sort_keys_serialization": False,
    }


def main() -> int:
    target_records = {
        "strategy": file_record(STRATEGY),
        "pilot": file_record(PILOT),
        "source": file_record(SOURCE),
        "solver": file_record(SOLVER),
    }
    require(target_records == EXPECTED, "one or more frozen byte bindings differ")
    parsed, _ = strict_json(PILOT)

    reconstructed = [reconstruct_template(length) for length in (5, 7, 9, 11)]
    generic = [generic_census(ORDER, k) for k in (3, 4, 5)]
    signatures = {
        f"hole{length}": signature_census(length) for length in (5, 7, 9, 11)
    }
    pilot_audit = audit_pilot(parsed, reconstructed)

    expected_generic_rows = {
        3: (286, 8580, 9802, 29774, 59049, 90932, 1740356),
        4: (715, 25740, 29393, 79320, 262144, 343117, 5109628),
        5: (1287, 51480, 59280, 157116, 390625, 548978, 5916975),
    }
    for row in generic:
        observed = (
            row["states"],
            row["move_variables"],
            row["all_variables"],
            row["base_clauses"],
            row["color_clauses"],
            row["full_doublelex_clauses"],
            row["full_doublelex_literals"],
        )
        require(observed == expected_generic_rows[row["k"]], "generic census mismatch")

    expected_signatures = {
        "hole5": (6, 7, 6, 378, 3852),
        "hole7": (8, 5, 4, 1020, 14344),
        "hole9": (10, 3, 2, 2046, 36868),
        "hole11": (12, 1, 0, 0, 0),
    }
    for template, row in signatures.items():
        observed = (
            row["core_bits"],
            row["free_vertices"],
            row["adjacent_comparators"],
            row["clauses"],
            row["literals"],
        )
        require(observed == expected_signatures[template], "signature census mismatch")

    version = subprocess.run(
        [str(SOLVER), "--version"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=10,
    )
    require(version.stderr == "", "cadical --version wrote stderr")
    require("3.0.1" in version.stdout, "solver binary does not report version 3.0.1")

    report = {
        "schema": "gamma-theta-order13-strategy-hostile-audit-v1",
        "verdict": "PASS_BYTE_AND_CENSUS_AUDIT",
        "target_bindings": target_records,
        "strict_pilot_audit": pilot_audit,
        "solver_version_stdout": version.stdout.strip(),
        "template_reconstructions": reconstructed,
        "generic_census": generic,
        "signature_breaker_census": signatures,
        "limitations": [
            "No SAT solver was run on any formula.",
            "The pilot execution transcript and exact argv are absent, so the historical solver invocation itself cannot be replayed.",
            "The proofless UNSAT return is not certificate evidence and was audited only as OBSERVED.",
        ],
    }
    sys.stdout.buffer.write(canonical_json_bytes(report))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AuditError, OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"AUDIT_FAILURE: {error}", file=sys.stderr)
        raise SystemExit(1)

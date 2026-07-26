#!/usr/bin/env python3
"""Standalone hostile auditor for the order-12 hole-template coloring banks.

This file deliberately imports only the Python standard library.  In
particular, it does not import ``src.synthesis_k3`` or any search/generator
module.  Its edge-variable convention is reconstructed directly from the
published design: ``e_uv`` for ``u < v`` occupy DIMACS variables 1 through
66 in lexicographic ``itertools.combinations(range(12), 2)`` order.

The mathematical object audited here is the complete bank of colorings that
are proper on the forced *H = complement(G)* edges of a named odd-hole
template.  A bank row is the first-use canonical representative of one
orbit under the six permutations of three color names.  Its clause is the
positive disjunction of every ``e_uv`` whose endpoints have the same color.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Mapping, Sequence


ORDER = 12
COLOR_COUNT = 3
TEMPLATES = ("hole5", "hole7", "hole9")
EXPECTED_COUNTS = {"hole5": 3645, "hole7": 1701, "hole9": 765}
EDGE_PAIRS = tuple(itertools.combinations(range(ORDER), 2))
EDGE_VARIABLE = {pair: index + 1 for index, pair in enumerate(EDGE_PAIRS)}
VARIABLE_EDGE = {variable: pair for pair, variable in EDGE_VARIABLE.items()}


class AuditError(ValueError):
    """Raised when an alleged bank or certificate binding is invalid."""


@dataclass(frozen=True)
class IndependentBank:
    template: str
    forced_edges: tuple[tuple[int, int], ...]
    forced_nonedges: tuple[tuple[int, int], ...]
    rows: tuple[tuple[int, ...], ...]
    clauses: tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class IndependentFormula:
    template: str
    variable_count: int
    base_clauses: tuple[tuple[int, ...], ...]
    complete_clauses: tuple[tuple[int, ...], ...]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def normalized_pair(first: int, second: int) -> tuple[int, int]:
    require(
        type(first) is int
        and type(second) is int
        and 0 <= first < ORDER
        and 0 <= second < ORDER
        and first != second,
        f"invalid edge endpoints {(first, second)!r}",
    )
    return (first, second) if first < second else (second, first)


def template_units(
    template: str,
) -> tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]]:
    """Reconstruct the forced H-edge and H-nonedge pairs from the design."""

    require(template in TEMPLATES, f"unsupported template {template!r}")
    length = int(template.removeprefix("hole"))
    rim = tuple(range(length))
    rim_edges = {
        normalized_pair(vertex, (vertex + 1) % length) for vertex in rim
    }
    rim_pairs = set(itertools.combinations(rim, 2))
    # Vertex `length` is the relabeled common H-neighbor of rim edge 01.
    forced_edges = rim_edges | {(0, length), (1, length)}
    forced_nonedges = rim_pairs - rim_edges
    return tuple(sorted(forced_edges)), tuple(sorted(forced_nonedges))


def canonicalize_coloring(
    raw: Sequence[int],
    *,
    require_three_colors: bool = False,
) -> tuple[int, ...]:
    require(len(raw) == ORDER, f"expected {ORDER} colors, got {len(raw)}")
    require(
        all(type(color) is int and 0 <= color < COLOR_COUNT for color in raw),
        "colors must be the exact integers 0, 1, or 2",
    )
    relabel: dict[int, int] = {}
    result: list[int] = []
    for color in raw:
        if color not in relabel:
            relabel[color] = len(relabel)
        result.append(relabel[color])
    if require_three_colors:
        require(len(relabel) == COLOR_COUNT, "coloring does not use all 3 colors")
    return tuple(result)


def is_first_use_canonical(row: Sequence[int]) -> bool:
    try:
        return tuple(row) == canonicalize_coloring(
            row, require_three_colors=True
        )
    except AuditError:
        return False


def proper_on_edges(
    coloring: Sequence[int], edges: Iterable[tuple[int, int]]
) -> bool:
    return all(coloring[first] != coloring[second] for first, second in edges)


def same_color_clause(coloring: Sequence[int]) -> tuple[int, ...]:
    canonicalize_coloring(coloring)
    return tuple(
        EDGE_VARIABLE[pair]
        for pair in EDGE_PAIRS
        if coloring[pair[0]] == coloring[pair[1]]
    )


def enumerate_first_use_rows(
    template: str,
    *,
    forced_edges_override: Iterable[tuple[int, int]] | None = None,
) -> tuple[tuple[int, ...], ...]:
    """Enumerate restricted-growth rows without using labeled assignments."""

    actual_edges, _ = template_units(template)
    if forced_edges_override is not None:
        actual_edges = tuple(
            sorted(normalized_pair(*pair) for pair in forced_edges_override)
        )
    prior_neighbors: list[list[int]] = [[] for _ in range(ORDER)]
    for first, second in actual_edges:
        prior_neighbors[second].append(first)

    colors = [-1] * ORDER
    rows: list[tuple[int, ...]] = []

    def visit(vertex: int, maximum_used: int) -> None:
        if vertex == ORDER:
            if maximum_used == COLOR_COUNT - 1:
                rows.append(tuple(colors))
            return
        largest = min(COLOR_COUNT - 1, maximum_used + 1)
        for color in range(largest + 1):
            if any(colors[prior] == color for prior in prior_neighbors[vertex]):
                continue
            colors[vertex] = color
            visit(vertex + 1, max(maximum_used, color))
            colors[vertex] = -1

    visit(0, -1)
    return tuple(rows)


def build_independent_bank(template: str) -> IndependentBank:
    forced_edges, forced_nonedges = template_units(template)
    rows = enumerate_first_use_rows(template)
    clauses = tuple(same_color_clause(row) for row in rows)
    bank = IndependentBank(
        template=template,
        forced_edges=forced_edges,
        forced_nonedges=forced_nonedges,
        rows=rows,
        clauses=clauses,
    )
    validate_bank(bank)
    return bank


def build_independent_formula(
    template: str, bank: IndependentBank | None = None
) -> IndependentFormula:
    """Reconstruct the complete base-plus-bank CNF from the written design.

    This is an independent implementation, not a call into the production
    encoder.  Variable allocation and clause order are made explicit so the
    resulting DIMACS can be compared byte-for-byte at the clause level.
    """

    require(template in TEMPLATES, f"unsupported template {template!r}")
    if bank is None:
        bank = build_independent_bank(template)
    require(bank.template == template, "bank/formula template mismatch")

    vertices = tuple(range(ORDER))
    triples = tuple(itertools.combinations(vertices, 3))
    next_variable = 1

    edge_variables: dict[tuple[int, int], int] = {}
    for pair in EDGE_PAIRS:
        edge_variables[pair] = next_variable
        next_variable += 1
    require(edge_variables == EDGE_VARIABLE, "edge variable allocation mismatch")

    witness_variables: dict[tuple[int, int, int], int] = {}
    for first, second in EDGE_PAIRS:
        for witness in vertices:
            if witness in (first, second):
                continue
            witness_variables[(first, second, witness)] = next_variable
            next_variable += 1

    family_variables: dict[tuple[int, int, int], int] = {}
    for triple in triples:
        family_variables[triple] = next_variable
        next_variable += 1

    move_variables: dict[tuple[tuple[int, int, int], int, int], int] = {}
    for triple in triples:
        for attacked in vertices:
            if attacked in triple:
                continue
            for guard in triple:
                move_variables[(triple, attacked, guard)] = next_variable
                next_variable += 1

    variable_count = next_variable - 1
    require(variable_count == 6886, "independent variable count is not 6886")

    def edge(first: int, second: int) -> int:
        return edge_variables[normalized_pair(first, second)]

    clauses: list[tuple[int, ...]] = []

    # No K4 in H.
    for four_set in itertools.combinations(vertices, 4):
        clauses.append(
            tuple(
                -edge(first, second)
                for first, second in itertools.combinations(four_set, 2)
            )
        )

    # Every pair has a common H-neighbor outside the pair.
    for first, second in EDGE_PAIRS:
        witnesses = tuple(
            witness
            for witness in vertices
            if witness not in (first, second)
        )
        clauses.append(
            tuple(
                witness_variables[(first, second, witness)]
                for witness in witnesses
            )
        )
        for witness in witnesses:
            variable = witness_variables[(first, second, witness)]
            clauses.append((-variable, edge(first, witness)))
            clauses.append((-variable, edge(second, witness)))

    # Exact induced odd hole, no external hub, and a selected external common
    # neighbor of rim edge 01.
    length = int(template.removeprefix("hole"))
    rim = tuple(range(length))
    rim_edges = set(bank.forced_edges) - {(0, length), (1, length)}
    for first, second in itertools.combinations(rim, 2):
        variable = edge(first, second)
        clauses.append(
            (variable if (first, second) in rim_edges else -variable,)
        )
    for outside in range(length, ORDER):
        clauses.append(tuple(-edge(outside, rim_vertex) for rim_vertex in rim))
    clauses.append((edge(0, length),))
    clauses.append((edge(1, length),))

    # G is connected: every proper cut whose selected side contains vertex 0
    # has at least one G-edge, equivalently at least one H-nonedge.
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

    # Every selected family state dominates G.
    for triple in triples:
        family_variable = family_variables[triple]
        for outside in vertices:
            if outside in triple:
                continue
            clauses.append(
                (
                    -family_variable,
                    -edge(outside, triple[0]),
                    -edge(outside, triple[1]),
                    -edge(outside, triple[2]),
                )
            )

    # Nonempty one-guard family and closure under each unoccupied attack.
    clauses.append(tuple(family_variables.values()))
    for triple in triples:
        family_variable = family_variables[triple]
        for attacked in vertices:
            if attacked in triple:
                continue
            responses: list[int] = []
            for guard in triple:
                move_variable = move_variables[(triple, attacked, guard)]
                successor = tuple(
                    sorted((set(triple) - {guard}) | {attacked})
                )
                responses.append(move_variable)
                clauses.append((-move_variable, -edge(guard, attacked)))
                clauses.append((-move_variable, family_variables[successor]))
            clauses.append((-family_variable, *responses))

    # Every maximum independent triple of G (triangle of H) lies in every
    # eternal family.
    for triple in triples:
        clauses.append(
            (
                -edge(triple[0], triple[1]),
                -edge(triple[0], triple[2]),
                -edge(triple[1], triple[2]),
                family_variables[triple],
            )
        )

    expected_base_counts = {"hole5": 20008, "hole7": 20017, "hole9": 20030}
    require(
        len(clauses) == expected_base_counts[template],
        f"{template}: independent base clause count is wrong",
    )
    base_clauses = tuple(clauses)
    complete_clauses = base_clauses + bank.clauses
    return IndependentFormula(
        template=template,
        variable_count=variable_count,
        base_clauses=base_clauses,
        complete_clauses=complete_clauses,
    )


def validate_bank(bank: IndependentBank) -> None:
    require(bank.template in TEMPLATES, "invalid template in bank")
    expected_count = EXPECTED_COUNTS[bank.template]
    require(
        len(bank.rows) == expected_count,
        f"{bank.template}: got {len(bank.rows)} rows, expected {expected_count}",
    )
    require(len(bank.clauses) == len(bank.rows), "row/clause count mismatch")
    require(tuple(sorted(bank.rows)) == bank.rows, "rows are not lexicographic")
    require(len(set(bank.rows)) == len(bank.rows), "duplicate bank row")
    require(len(set(bank.clauses)) == len(bank.clauses), "duplicate bank clause")
    forced_edge_variables = {
        EDGE_VARIABLE[pair] for pair in bank.forced_edges
    }
    for index, (row, clause) in enumerate(zip(bank.rows, bank.clauses)):
        require(
            is_first_use_canonical(row),
            f"row {index} is not first-use canonical",
        )
        require(
            proper_on_edges(row, bank.forced_edges),
            f"row {index} violates a forced H-edge",
        )
        expected_clause = same_color_clause(row)
        require(
            clause == expected_clause,
            f"row {index} has an inexact same-color clause",
        )
        require(
            all(type(literal) is int and 1 <= literal <= 66 for literal in clause),
            f"row {index} has a nonpositive or non-edge literal",
        )
        require(
            forced_edge_variables.isdisjoint(clause),
            f"row {index} clause contains a forced-true H-edge",
        )


def exhaustive_labeled_equivalence(bank: IndependentBank) -> dict[str, object]:
    """Check all 3^12 labeled assignments and their color-permutation orbits."""

    row_set = set(bank.rows)
    compatible_assignments = 0
    incompatible_assignments = 0
    canonical_multiplicity: Counter[tuple[int, ...]] = Counter()
    incompatible_without_forced_literal = 0
    forced_edge_variables = {
        EDGE_VARIABLE[pair] for pair in bank.forced_edges
    }

    for coloring in itertools.product(range(COLOR_COUNT), repeat=ORDER):
        clause = same_color_clause(coloring)
        if proper_on_edges(coloring, bank.forced_edges):
            compatible_assignments += 1
            canonical = canonicalize_coloring(
                coloring, require_three_colors=True
            )
            require(
                canonical in row_set,
                "compatible labeled assignment is absent from bank",
            )
            require(
                clause == same_color_clause(canonical),
                "color renaming changed a same-color clause",
            )
            canonical_multiplicity[canonical] += 1
        else:
            incompatible_assignments += 1
            if forced_edge_variables.isdisjoint(clause):
                incompatible_without_forced_literal += 1

    require(
        compatible_assignments == len(bank.rows) * 6,
        "compatible labeled count is not six times the partition count",
    )
    length = int(bank.template.removeprefix("hole"))
    # Chromatic polynomial of an odd cycle at q=3:
    # P(C_l,3) = (3-1)^l + (-1)^l(3-1) = 2^l - 2.
    # The selected common neighbor of edge 01 is forced to the third color,
    # and the remaining 11-l vertices are free.
    closed_form_labeled = (2**length - 2) * 3 ** (11 - length)
    require(
        compatible_assignments == closed_form_labeled,
        "exhaustive labeled count disagrees with the cycle-polynomial formula",
    )
    require(
        len(bank.rows) == closed_form_labeled // 6,
        "partition count disagrees with division by the six free color names",
    )
    require(
        set(canonical_multiplicity) == row_set,
        "labeled enumeration and first-use enumeration disagree",
    )
    require(
        set(canonical_multiplicity.values()) == {6},
        "a compatible partition does not have exactly six color relabelings",
    )
    require(
        incompatible_without_forced_literal == 0,
        "an incompatible assignment is not killed by a forced H-edge unit",
    )
    require(
        compatible_assignments + incompatible_assignments == COLOR_COUNT**ORDER,
        "labeled assignment accounting failed",
    )
    return {
        "template": bank.template,
        "canonical_partition_count": len(bank.rows),
        "compatible_labeled_assignments": compatible_assignments,
        "closed_form_labeled_assignments": closed_form_labeled,
        "closed_form_partitions": closed_form_labeled // 6,
        "incompatible_labeled_assignments": incompatible_assignments,
        "orbit_sizes": [6],
        "all_assignments": COLOR_COUNT**ORDER,
        "incompatible_assignments_killed_by_forced_edge_unit": incompatible_assignments,
    }


def strict_json_load(path: Path) -> object:
    def reject_constant(token: str) -> object:
        raise AuditError(f"non-finite JSON token {token!r} in {path}")

    def reject_duplicate_keys(
        pairs: list[tuple[str, object]],
    ) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            require(key not in result, f"duplicate JSON key {key!r} in {path}")
            result[key] = value
        return result

    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise AuditError(f"cannot read UTF-8 JSON {path}: {error}") from error
    try:
        return json.loads(
            text,
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_constant,
        )
    except json.JSONDecodeError as error:
        raise AuditError(f"malformed JSON {path}: {error}") from error


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for block in iter(lambda: handle.read(1 << 20), b""):
                digest.update(block)
    except OSError as error:
        raise AuditError(f"cannot hash {path}: {error}") from error
    return digest.hexdigest()


def canonical_json_bytes(payload: object) -> bytes:
    return (
        json.dumps(payload, allow_nan=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def dimacs_bytes(
    variable_count: int, clauses: Sequence[Sequence[int]]
) -> bytes:
    lines = [f"p cnf {variable_count} {len(clauses)}"]
    lines.extend(" ".join(map(str, clause)) + " 0" for clause in clauses)
    return ("\n".join(lines) + "\n").encode("ascii")


def _parse_row(raw: object, index: int) -> tuple[tuple[int, ...], tuple[int, ...] | None]:
    clause_raw: object | None = None
    if isinstance(raw, dict):
        require(
            set(raw) <= {"coloring", "colors", "clause", "literals", "index"},
            f"bank row {index} has unknown keys {sorted(set(raw) - {'coloring', 'colors', 'clause', 'literals', 'index'})}",
        )
        coloring_raw = raw.get("coloring", raw.get("colors"))
        clause_raw = raw.get("clause", raw.get("literals"))
        if "index" in raw:
            require(raw["index"] == index, f"bank row {index} has wrong index")
    else:
        coloring_raw = raw
    require(isinstance(coloring_raw, list), f"bank row {index} is not a list")
    coloring = tuple(coloring_raw)
    canonicalize_coloring(coloring)
    clause: tuple[int, ...] | None = None
    if clause_raw is not None:
        require(isinstance(clause_raw, list), f"bank clause {index} is not a list")
        require(
            all(type(literal) is int for literal in clause_raw),
            f"bank clause {index} contains a noninteger",
        )
        clause = tuple(clause_raw)
    return coloring, clause


def parse_bank_json(
    path: Path,
) -> tuple[str | None, tuple[tuple[int, ...], ...], tuple[tuple[int, ...], ...] | None]:
    payload = strict_json_load(path)
    declared_template: str | None = None
    raw_rows: object
    top_level_clauses: object | None = None
    if isinstance(payload, list):
        raw_rows = payload
    else:
        require(isinstance(payload, dict), "bank JSON root must be an object or list")
        allowed = {
            "schema",
            "schema_version",
            "template",
            "order",
            "color_count",
            "count",
            "rows",
            "colorings",
            "clauses",
            "edge_variable_count",
            "sha256",
        }
        require(
            set(payload) <= allowed,
            f"bank JSON has unknown keys {sorted(set(payload) - allowed)}",
        )
        declared_template_raw = payload.get("template")
        if declared_template_raw is not None:
            require(
                isinstance(declared_template_raw, str),
                "bank template is not a string",
            )
            declared_template = declared_template_raw
        if "order" in payload:
            require(payload["order"] == ORDER, "bank order is not 12")
        if "color_count" in payload:
            require(payload["color_count"] == COLOR_COUNT, "bank color count is not 3")
        raw_rows = payload.get("rows", payload.get("colorings"))
        top_level_clauses = payload.get("clauses")
        require(isinstance(raw_rows, list), "bank has no row list")
        if "count" in payload:
            require(payload["count"] == len(raw_rows), "bank count field is wrong")

    require(isinstance(raw_rows, list), "bank rows are not a list")
    rows: list[tuple[int, ...]] = []
    row_clauses: list[tuple[int, ...] | None] = []
    for index, raw in enumerate(raw_rows):
        row, clause = _parse_row(raw, index)
        rows.append(row)
        row_clauses.append(clause)

    clauses: tuple[tuple[int, ...], ...] | None
    if top_level_clauses is not None:
        require(
            all(clause is None for clause in row_clauses),
            "clauses occur both inside rows and at top level",
        )
        require(isinstance(top_level_clauses, list), "top-level clauses are not a list")
        parsed: list[tuple[int, ...]] = []
        for index, raw_clause in enumerate(top_level_clauses):
            require(isinstance(raw_clause, list), f"clause {index} is not a list")
            require(
                all(type(literal) is int for literal in raw_clause),
                f"clause {index} contains a noninteger",
            )
            parsed.append(tuple(raw_clause))
        clauses = tuple(parsed)
    elif any(clause is not None for clause in row_clauses):
        require(
            all(clause is not None for clause in row_clauses),
            "only some bank rows contain clauses",
        )
        clauses = tuple(clause for clause in row_clauses if clause is not None)
    else:
        clauses = None
    return declared_template, tuple(rows), clauses


def parse_dimacs(path: Path) -> tuple[int, tuple[tuple[int, ...], ...]]:
    try:
        lines = path.read_text(encoding="ascii").splitlines()
    except (OSError, UnicodeError) as error:
        raise AuditError(f"cannot read ASCII DIMACS {path}: {error}") from error
    variable_count: int | None = None
    declared_clause_count: int | None = None
    tokens: list[int] = []
    for line_number, raw_line in enumerate(lines, 1):
        line = raw_line.strip()
        if not line or line.startswith("c"):
            continue
        if line.startswith("p"):
            require(variable_count is None, "multiple DIMACS headers")
            fields = line.split()
            require(
                len(fields) == 4 and fields[:2] == ["p", "cnf"],
                f"invalid DIMACS header at line {line_number}",
            )
            try:
                variable_count = int(fields[2])
                declared_clause_count = int(fields[3])
            except ValueError as error:
                raise AuditError("nonnumeric DIMACS header") from error
            require(
                variable_count >= 0 and declared_clause_count >= 0,
                "negative DIMACS dimensions",
            )
            continue
        require(variable_count is not None, "DIMACS data precedes header")
        try:
            tokens.extend(int(token) for token in line.split())
        except ValueError as error:
            raise AuditError(f"nonnumeric DIMACS token at line {line_number}") from error
    require(variable_count is not None, "missing DIMACS header")
    clauses: list[tuple[int, ...]] = []
    current: list[int] = []
    for literal in tokens:
        if literal == 0:
            clauses.append(tuple(current))
            current.clear()
        else:
            require(
                abs(literal) <= variable_count,
                f"DIMACS literal {literal} exceeds variable count",
            )
            current.append(literal)
    require(not current, "unterminated DIMACS clause")
    require(
        len(clauses) == declared_clause_count,
        f"DIMACS has {len(clauses)} clauses, declares {declared_clause_count}",
    )
    return variable_count, tuple(clauses)


def audit_bank_artifact(path: Path, bank: IndependentBank) -> dict[str, object]:
    declared_template, rows, clauses = parse_bank_json(path)
    if declared_template is not None:
        require(
            declared_template == bank.template,
            f"bank declares {declared_template}, expected {bank.template}",
        )
    require(rows == bank.rows, "bank rows differ from independent enumeration")
    if clauses is not None:
        require(
            clauses == bank.clauses,
            "bank clauses differ from exact positive same-color clauses",
        )
    if clauses is None:
        require(
            path.read_bytes()
            == canonical_json_bytes([list(row) for row in bank.rows]),
            "bank bytes are not the canonical deterministic row serialization",
        )
    return {
        "path": str(path),
        "sha256": sha256_file(path),
        "row_count": len(rows),
        "embedded_clauses": clauses is not None,
    }


def audit_cnf_artifact(
    path: Path, bank: IndependentBank, formula: IndependentFormula
) -> dict[str, object]:
    variable_count, clauses = parse_dimacs(path)
    require(
        variable_count == formula.variable_count,
        f"CNF has {variable_count} variables, expected {formula.variable_count}",
    )
    require(
        clauses == formula.complete_clauses,
        "CNF is not the exact independently reconstructed base-plus-bank formula",
    )
    require(
        path.read_bytes()
        == dimacs_bytes(formula.variable_count, formula.complete_clauses),
        "CNF bytes are not the canonical independently reconstructed DIMACS",
    )
    prefix_count = len(formula.base_clauses)
    return {
        "path": str(path),
        "sha256": sha256_file(path),
        "variable_count": variable_count,
        "clause_count": len(clauses),
        "bank_clause_count": len(bank.clauses),
        "base_prefix_clause_count": prefix_count,
        "placement": "exact_independent_base_plus_bank",
    }


def audit_legacy_cut_artifacts(
    *,
    cuts_path: Path,
    legacy_cnf_path: Path | None,
    bank: IndependentBank,
    formula: IndependentFormula,
) -> dict[str, object]:
    declared_template, rows, embedded_clauses = parse_bank_json(cuts_path)
    if declared_template is not None:
        require(
            declared_template == bank.template,
            "legacy cuts declare the wrong template",
        )
    require(len(rows) > 0, "legacy cut stream is empty")
    require(len(set(rows)) == len(rows), "legacy cut stream has duplicate partitions")
    bank_row_set = set(bank.rows)
    for index, row in enumerate(rows):
        require(
            is_first_use_canonical(row),
            f"legacy cut row {index} is not first-use canonical",
        )
        require(
            proper_on_edges(row, bank.forced_edges),
            f"legacy cut row {index} violates a forced H-edge",
        )
        require(
            row in bank_row_set,
            f"legacy cut row {index} is absent from the complete bank",
        )
    clauses = tuple(same_color_clause(row) for row in rows)
    if embedded_clauses is not None:
        require(
            embedded_clauses == clauses,
            "legacy embedded clauses are not exact same-color clauses",
        )

    legacy_cnf_record: dict[str, object] | None = None
    if legacy_cnf_path is not None:
        variable_count, cnf_clauses = parse_dimacs(legacy_cnf_path)
        require(
            variable_count == formula.variable_count,
            "legacy CNF variable count differs from independent base",
        )
        require(
            cnf_clauses[: len(formula.base_clauses)] == formula.base_clauses,
            "legacy CNF prefix differs from the independently reconstructed base",
        )
        require(
            cnf_clauses[len(formula.base_clauses) :] == clauses,
            "legacy CNF suffix differs from its exact recorded coloring cuts",
        )
        legacy_cnf_record = {
            "path": str(legacy_cnf_path),
            "sha256": sha256_file(legacy_cnf_path),
            "variable_count": variable_count,
            "clause_count": len(cnf_clauses),
            "base_clause_count": len(formula.base_clauses),
            "cut_clause_count": len(clauses),
        }

    return {
        "cuts_path": str(cuts_path),
        "cuts_sha256": sha256_file(cuts_path),
        "cut_count": len(rows),
        "all_exact_members_of_complete_bank": True,
        "complete_bank_count": len(bank.rows),
        "legacy_cnf": legacy_cnf_record,
        "rup_monotonicity_condition": (
            "the legacy CNF clause set is a subset of the complete-bank CNF"
        ),
    }


def audit_manifest_artifact(
    path: Path,
    bank: IndependentBank,
    formula: IndependentFormula,
    bank_record: Mapping[str, object] | None,
    cnf_record: Mapping[str, object] | None,
) -> dict[str, object]:
    payload = strict_json_load(path)
    require(isinstance(payload, dict), "manifest root is not an object")
    expected_keys = {
        "schema",
        "schema_version",
        "template",
        "order",
        "canonicalization",
        "forced_positive_h_edges",
        "count_identity",
        "bank_count",
        "variable_count",
        "clause_count",
        "literal_count",
        "clause_layout",
        "artifacts",
        "runtime_source_manifest",
        "runtime_source_set_sha256",
        "git_source_binding",
        "generation_recipe",
    }
    require(
        set(payload) == expected_keys,
        f"manifest keys differ: {sorted(set(payload) ^ expected_keys)}",
    )
    require(
        payload["schema"] == "gamma-theta-k3-template-color-bank-v1"
        and payload["schema_version"] == 1
        and payload["template"] == bank.template
        and payload["order"] == ORDER
        and payload["canonicalization"]
        == "restricted-growth-string-first-use",
        "manifest identity fields are wrong",
    )
    require(
        payload["forced_positive_h_edges"]
        == [list(pair) for pair in bank.forced_edges],
        "manifest forced-positive-H-edge list is wrong",
    )
    length = int(bank.template.removeprefix("hole"))
    expected_identity = {
        "cycle_length": length,
        "labeled_cycle_colorings": 2**length - 2,
        "free_vertices": 11 - length,
        "color_permutation_orbit_size": 6,
        "expected_bank_count": len(bank.rows),
    }
    require(
        payload["count_identity"] == expected_identity,
        "manifest count identity is wrong",
    )
    expected_literal_count = sum(map(len, formula.complete_clauses))
    require(
        (
            payload["bank_count"],
            payload["variable_count"],
            payload["clause_count"],
            payload["literal_count"],
        )
        == (
            len(bank.rows),
            formula.variable_count,
            len(formula.complete_clauses),
            expected_literal_count,
        ),
        "manifest formula counts are wrong",
    )
    bank_clause_stream = b"".join(
        (" ".join(map(str, clause)) + " 0\n").encode("ascii")
        for clause in bank.clauses
    )
    base_payload = dimacs_bytes(formula.variable_count, formula.base_clauses)
    expected_clause_layout = {
        "base_clause_count": len(formula.base_clauses),
        "base_literal_count": sum(map(len, formula.base_clauses)),
        "base_cnf_sha256": hashlib.sha256(base_payload).hexdigest(),
        "bank_clause_first_index_zero_based": len(formula.base_clauses),
        "bank_clause_end_index_exclusive": len(formula.complete_clauses),
        "bank_clause_order": "coloring-bank-row-order",
        "bank_clause_stream_format": (
            "header-free-DIMACS-lines-terminal-zero-LF"
        ),
        "bank_clause_stream_sha256": hashlib.sha256(
            bank_clause_stream
        ).hexdigest(),
        "bank_clause_stream_size_bytes": len(bank_clause_stream),
    }
    require(
        payload["clause_layout"] == expected_clause_layout,
        "manifest clause layout differs from independent reconstruction",
    )
    artifacts = payload["artifacts"]
    require(
        isinstance(artifacts, dict)
        and set(artifacts) == {"coloring_bank", "cnf"},
        "manifest artifact map is malformed",
    )
    expected_artifacts = {
        "coloring_bank": ("coloring_bank.json", bank_record),
        "cnf": ("instance.cnf", cnf_record),
    }
    for role, (expected_name, external_record) in expected_artifacts.items():
        record = artifacts[role]
        require(
            isinstance(record, dict)
            and set(record) == {"path", "sha256", "size_bytes"},
            f"manifest {role} record is malformed",
        )
        require(
            record["path"] == expected_name,
            f"manifest {role} artifact name is wrong",
        )
        if external_record is not None:
            external_path = Path(str(external_record["path"]))
            require(
                external_path.name == expected_name,
                f"audited {role} path has unexpected name",
            )
            artifact_size = external_path.stat().st_size
            require(
                record["sha256"] == external_record["sha256"]
                and record["size_bytes"] == artifact_size,
                f"manifest does not exactly bind audited {role}",
            )

    recipe = payload["generation_recipe"]
    require(
        recipe
        == {
            "module": "synthesis_k3.template_color_bank",
            "subcommand": "generate",
            "validation_gate": True,
        },
        "manifest generation recipe is wrong",
    )

    source_rows = payload["runtime_source_manifest"]
    require(isinstance(source_rows, list), "runtime source manifest is not a list")
    campaign = Path(__file__).resolve().parents[1]
    normalized_source_rows: list[tuple[str, str]] = []
    for index, row in enumerate(source_rows):
        require(
            isinstance(row, list)
            and len(row) == 2
            and isinstance(row[0], str)
            and isinstance(row[1], str)
            and len(row[1]) == 64,
            f"runtime source row {index} is malformed",
        )
        relative, digest = row
        relative_path = Path(relative)
        require(
            not relative_path.is_absolute() and ".." not in relative_path.parts,
            f"runtime source row {index} has an unsafe path",
        )
        source = campaign / relative_path
        require(source.is_file(), f"runtime source row {index} is missing")
        require(
            sha256_file(source) == digest,
            f"runtime source row {index} hash differs from current source",
        )
        normalized_source_rows.append((relative, digest))
    require(
        len(set(relative for relative, _ in normalized_source_rows))
        == len(normalized_source_rows),
        "runtime source manifest has duplicate paths",
    )
    source_set = hashlib.sha256(
        "".join(
            f"{relative} {digest}\n"
            for relative, digest in normalized_source_rows
        ).encode("ascii")
    ).hexdigest()
    require(
        payload["runtime_source_set_sha256"] == source_set,
        "runtime source-set digest is wrong",
    )

    git_binding = payload["git_source_binding"]
    require(
        isinstance(git_binding, dict)
        and set(git_binding)
        == {
            "head_commit",
            "repository_relative_campaign_path",
            "runtime_sources_match_head",
            "runtime_source_mismatches",
            "global_worktree_cleanliness_required",
        },
        "git source binding is malformed",
    )
    head = git_binding["head_commit"]
    require(
        isinstance(head, str) and len(head) in (40, 64),
        "git source binding has malformed HEAD",
    )
    try:
        bytes.fromhex(head)
    except ValueError as error:
        raise AuditError("git source binding HEAD is not hexadecimal") from error
    repository = subprocess.run(
        ["git", "--no-pager", "-C", str(campaign), "rev-parse", "--show-toplevel"],
        stdin=subprocess.DEVNULL,
        capture_output=True,
        timeout=30,
        check=False,
    )
    require(repository.returncode == 0, "cannot independently resolve git root")
    try:
        repository_root = Path(
            repository.stdout.decode("utf-8").strip()
        ).resolve(strict=True)
    except UnicodeDecodeError as error:
        raise AuditError("git root is not UTF-8") from error
    campaign_relative = campaign.relative_to(repository_root).as_posix()
    require(
        git_binding["repository_relative_campaign_path"] == campaign_relative,
        "git binding campaign-relative path is wrong",
    )
    mismatches: list[str] = []
    git_environment = {
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_OPTIONAL_LOCKS": "0",
        "LC_ALL": "C",
        "PATH": "/usr/bin:/bin:/usr/sbin:/sbin",
    }
    for relative, digest in normalized_source_rows:
        repository_relative = (
            Path(campaign_relative) / relative
        ).as_posix()
        shown = subprocess.run(
            [
                "git",
                "--no-pager",
                "-C",
                str(repository_root),
                "show",
                f"{head}:{repository_relative}",
            ],
            env=git_environment,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            timeout=30,
            check=False,
        )
        if (
            shown.returncode != 0
            or hashlib.sha256(shown.stdout).hexdigest() != digest
        ):
            mismatches.append(relative)
    require(
        git_binding["runtime_source_mismatches"] == mismatches
        and git_binding["runtime_sources_match_head"] == (not mismatches)
        and git_binding["global_worktree_cleanliness_required"] is False,
        "git source binding disagrees with independent git-object replay",
    )
    # A development package may honestly record mismatches, but it is not a
    # publication/production input: its exact runtime source is not located
    # by the recorded commit.  Enforce the stronger production gate here.
    require(
        not mismatches,
        "production package runtime sources do not match recorded HEAD",
    )
    require(
        path.read_bytes() == canonical_json_bytes(payload),
        "manifest bytes are not canonical deterministic JSON",
    )
    return {
        "path": str(path),
        "sha256": sha256_file(path),
        "bound_source_count": len(normalized_source_rows),
        "runtime_source_set_sha256": source_set,
        "head_commit": head,
        "runtime_sources_match_head": True,
    }


def mutation_tests(banks: Mapping[str, IndependentBank]) -> dict[str, bool]:
    """Exercise traps for every critical semantic mistake in memory."""

    results: dict[str, bool] = {}
    hole5 = banks["hole5"]

    def rejected(label: str, operation: object) -> None:
        try:
            assert callable(operation)
            operation()
        except (AuditError, AssertionError, TypeError, ValueError):
            results[label] = True
        else:
            raise AuditError(f"mutation {label!r} was accepted")

    # Completeness and duplication.
    rejected(
        "missing_row",
        lambda: validate_bank(
            IndependentBank(
                hole5.template,
                hole5.forced_edges,
                hole5.forced_nonedges,
                hole5.rows[:-1],
                hole5.clauses[:-1],
            )
        ),
    )
    rejected(
        "duplicate_row",
        lambda: validate_bank(
            IndependentBank(
                hole5.template,
                hole5.forced_edges,
                hole5.forced_nonedges,
                hole5.rows[:-1] + (hole5.rows[-2],),
                hole5.clauses[:-1] + (hole5.clauses[-2],),
            )
        ),
    )

    # A noncanonical color permutation represents the same partition but is
    # forbidden as a bank row.
    permuted = tuple({0: 1, 1: 0, 2: 2}[color] for color in hole5.rows[0])
    rejected(
        "noncanonical_color_names",
        lambda: validate_bank(
            IndependentBank(
                hole5.template,
                hole5.forced_edges,
                hole5.forced_nonedges,
                (permuted,) + hole5.rows[1:],
                (same_color_clause(permuted),) + hole5.clauses[1:],
            )
        ),
    )

    # Complement-sign trap: e_uv means an H edge, so every coloring cut is
    # positive.  Negating even one literal must be rejected.
    sign_mutation = (
        (-hole5.clauses[0][0],) + hole5.clauses[0][1:]
    )
    rejected(
        "complement_sign_flip",
        lambda: validate_bank(
            IndependentBank(
                hole5.template,
                hole5.forced_edges,
                hole5.forced_nonedges,
                hole5.rows,
                (sign_mutation,) + hole5.clauses[1:],
            )
        ),
    )

    # Exact-clause trap: a forced H-nonedge literal may occur in a cut and
    # cannot simply be deleted from the serialized exact same-color clause.
    forced_nonedge_vars = {
        EDGE_VARIABLE[pair] for pair in hole5.forced_nonedges
    }
    affected_index = next(
        index
        for index, clause in enumerate(hole5.clauses)
        if forced_nonedge_vars.intersection(clause)
    )
    affected = hole5.clauses[affected_index]
    deleted_literal = next(iter(forced_nonedge_vars.intersection(affected)))
    shortened = tuple(literal for literal in affected if literal != deleted_literal)
    mutated_clauses = list(hole5.clauses)
    mutated_clauses[affected_index] = shortened
    rejected(
        "forced_nonedge_literal_deleted",
        lambda: validate_bank(
            IndependentBank(
                hole5.template,
                hole5.forced_edges,
                hole5.forced_nonedges,
                hole5.rows,
                tuple(mutated_clauses),
            )
        ),
    )

    # Forced-edge trap: replacing rim edge 01 by rim chord 02 happens to
    # retain a similarly sized graph, so compare exact labeled partitions,
    # not only a count.
    wrong_edges = set(hole5.forced_edges)
    wrong_edges.remove((0, 1))
    wrong_edges.add((0, 2))
    wrong_rows = enumerate_first_use_rows(
        "hole5", forced_edges_override=wrong_edges
    )
    require(
        set(wrong_rows) != set(hole5.rows),
        "forced-edge mutation unexpectedly preserved the exact bank",
    )
    results["forced_rim_edge_replaced_by_chord"] = True

    # A row with equal colors on forced edge 01 would create a clause
    # containing the forced-true literal e_01.  It must not enter the bank;
    # those incompatible assignments are already killed by the unit.
    violating = list(hole5.rows[0])
    violating[1] = violating[0]
    violating_row = canonicalize_coloring(violating)
    require(
        EDGE_VARIABLE[(0, 1)] in same_color_clause(violating_row),
        "forced-edge polarity trap was not constructed",
    )
    rejected(
        "forced_true_edge_inside_bank_clause",
        lambda: validate_bank(
            IndependentBank(
                hole5.template,
                hole5.forced_edges,
                hole5.forced_nonedges,
                (violating_row,) + hole5.rows[1:],
                (same_color_clause(violating_row),) + hole5.clauses[1:],
            )
        ),
    )

    # Edge-variable mapping trap: variable 1 is e_01, not a G-edge variable
    # and not an offset auxiliary variable.
    require(EDGE_VARIABLE[(0, 1)] == 1, "edge variable 1 mapping failed")
    require(EDGE_VARIABLE[(10, 11)] == 66, "edge variable 66 mapping failed")
    results["edge_variable_endpoints"] = True
    return results


def run_self_test() -> dict[str, object]:
    banks = {template: build_independent_bank(template) for template in TEMPLATES}
    formulas = {
        template: build_independent_formula(template, bank)
        for template, bank in banks.items()
    }
    exhaustive = {
        template: exhaustive_labeled_equivalence(bank)
        for template, bank in banks.items()
    }
    mutations = mutation_tests(banks)
    return {
        "status": "PASS",
        "standard_library_only": True,
        "edge_variable_mapping": {
            "first": {"pair": [0, 1], "variable": 1},
            "last": {"pair": [10, 11], "variable": 66},
        },
        "templates": {
            template: {
                "count": len(bank.rows),
                "base_clause_count": len(formulas[template].base_clauses),
                "complete_clause_count": len(formulas[template].complete_clauses),
                "forced_edges": [list(pair) for pair in bank.forced_edges],
                "forced_nonedges": [list(pair) for pair in bank.forced_nonedges],
                "first_row": list(bank.rows[0]),
                "last_row": list(bank.rows[-1]),
                "first_clause": list(bank.clauses[0]),
                "last_clause": list(bank.clauses[-1]),
                "row_stream_sha256": hashlib.sha256(
                    (
                        json.dumps(
                            [list(row) for row in bank.rows],
                            separators=(",", ":"),
                        )
                        + "\n"
                    ).encode("ascii")
                ).hexdigest(),
                "clause_stream_sha256": hashlib.sha256(
                    (
                        json.dumps(
                            [list(clause) for clause in bank.clauses],
                            separators=(",", ":"),
                        )
                        + "\n"
                    ).encode("ascii")
                ).hexdigest(),
            }
            for template, bank in banks.items()
        },
        "exhaustive_equivalence": exhaustive,
        "mutation_tests": mutations,
    }


def audit_artifacts(
    *,
    template: str,
    bank_path: Path | None,
    cnf_path: Path | None,
    manifest_path: Path | None,
    legacy_cuts_path: Path | None,
    legacy_cnf_path: Path | None,
) -> dict[str, object]:
    require(
        bank_path is not None or cnf_path is not None or legacy_cuts_path is not None,
        "artifact audit needs --bank, --cnf, and/or --legacy-cuts",
    )
    bank = build_independent_bank(template)
    formula = build_independent_formula(template, bank)
    # Always rerun the exhaustive equivalence proof in an artifact audit.
    exhaustive = exhaustive_labeled_equivalence(bank)
    bank_record = (
        audit_bank_artifact(bank_path, bank) if bank_path is not None else None
    )
    cnf_record = (
        audit_cnf_artifact(cnf_path, bank, formula)
        if cnf_path is not None
        else None
    )
    manifest_record = (
        audit_manifest_artifact(
            manifest_path, bank, formula, bank_record, cnf_record
        )
        if manifest_path is not None
        else None
    )
    legacy_record = (
        audit_legacy_cut_artifacts(
            cuts_path=legacy_cuts_path,
            legacy_cnf_path=legacy_cnf_path,
            bank=bank,
            formula=formula,
        )
        if legacy_cuts_path is not None
        else None
    )
    require(
        legacy_cnf_path is None or legacy_cuts_path is not None,
        "--legacy-cnf requires --legacy-cuts",
    )
    return {
        "status": "PASS",
        "template": template,
        "independent_count": len(bank.rows),
        "independent_base_clause_count": len(formula.base_clauses),
        "independent_complete_clause_count": len(formula.complete_clauses),
        "exhaustive_equivalence": exhaustive,
        "bank": bank_record,
        "cnf": cnf_record,
        "manifest": manifest_record,
        "legacy": legacy_record,
    }


def write_json_result(result: Mapping[str, object], output: Path | None) -> None:
    payload = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if output is None:
        sys.stdout.write(payload)
    else:
        # This reviewer output is nondecisive metadata; a direct write is
        # intentionally avoided in campaign use.  The CLI only emits stdout.
        raise AuditError("--output is intentionally unsupported; redirect stdout")


def parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    self_test = subparsers.add_parser(
        "self-test", help="run exhaustive independent checks and mutations"
    )
    self_test.add_argument(
        "--output",
        type=Path,
        help="unsupported; redirect stdout to preserve explicit provenance",
    )
    audit = subparsers.add_parser(
        "audit", help="audit a generated bank, CNF, and optional manifest"
    )
    audit.add_argument("--template", choices=TEMPLATES, required=True)
    audit.add_argument("--bank", type=Path)
    audit.add_argument("--cnf", type=Path)
    audit.add_argument("--manifest", type=Path)
    audit.add_argument(
        "--legacy-cuts",
        type=Path,
        help="accepted earlier cut stream to prove is a subset of the bank",
    )
    audit.add_argument(
        "--legacy-cnf",
        type=Path,
        help="accepted earlier CNF whose base and cut suffix are checked",
    )
    audit.add_argument(
        "--output",
        type=Path,
        help="unsupported; redirect stdout to preserve explicit provenance",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    arguments = parse_arguments(argv)
    try:
        if arguments.command == "self-test":
            result = run_self_test()
        else:
            result = audit_artifacts(
                template=arguments.template,
                bank_path=arguments.bank,
                cnf_path=arguments.cnf,
                manifest_path=arguments.manifest,
                legacy_cuts_path=arguments.legacy_cuts,
                legacy_cnf_path=arguments.legacy_cnf,
            )
        write_json_result(result, arguments.output)
    except (AuditError, OSError) as error:
        sys.stderr.write(f"FAIL: {error}\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Deterministically append the proposed k=4 DoubleLex column breaker.

This module does not import the synthesis encoder or production runner.  It
accepts only the exact frozen order-12, parameter-four parent and appends the
three auxiliary-free eight-bit comparators proved in
``math/lemmas/order12_k4_doublelex.md``.

Generating the strengthened CNF makes no SAT or UNSAT claim.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import combinations, product
import json
import os
from pathlib import Path
import tempfile
from typing import Iterable, Sequence


N = 12
ANCHOR = (0, 1, 2, 3)
OUTER = tuple(range(4, N))

PARENT_VARIABLE_COUNT = 18_381
PARENT_CLAUSE_COUNT = 114_742
PARENT_LITERAL_COUNT = 1_180_016
PARENT_SIZE_BYTES = 3_992_947
PARENT_SHA256 = (
    "adbe0c01614bae6cd3aed4ccdcd45a757ca56e7ef9c4f2f280f2d8ef200e40ac"
)

SUFFIX_CLAUSE_COUNT = 765
SUFFIX_LITERAL_COUNT = 10_758
DOUBLELEX_VARIABLE_COUNT = PARENT_VARIABLE_COUNT
DOUBLELEX_CLAUSE_COUNT = PARENT_CLAUSE_COUNT + SUFFIX_CLAUSE_COUNT
DOUBLELEX_LITERAL_COUNT = PARENT_LITERAL_COUNT + SUFFIX_LITERAL_COUNT


def _edge_map() -> dict[tuple[int, int], int]:
    return {
        pair: variable
        for variable, pair in enumerate(combinations(range(N), 2), start=1)
    }


EDGES = _edge_map()


def _edge(first: int, second: int) -> int:
    pair = (first, second) if first < second else (second, first)
    return EDGES[pair]


def comparator_clauses(
    left_anchor: int, right_anchor: int
) -> tuple[tuple[int, ...], ...]:
    """Return clauses encoding column(left) <=lex column(right)."""

    if (left_anchor, right_anchor) not in ((0, 1), (1, 2), (2, 3)):
        raise ValueError("only adjacent anchor comparators are generated")
    clauses: list[tuple[int, ...]] = []
    for first_difference in range(len(OUTER)):
        for prefix in product((0, 1), repeat=first_difference):
            literals: list[int] = []
            for coordinate, bit in enumerate(prefix):
                outer = OUTER[coordinate]
                left = _edge(left_anchor, outer)
                right = _edge(right_anchor, outer)
                if bit == 0:
                    literals.extend((left, right))
                else:
                    literals.extend((-left, -right))
            outer = OUTER[first_difference]
            literals.extend(
                (
                    -_edge(left_anchor, outer),
                    _edge(right_anchor, outer),
                )
            )
            clause = tuple(literals)
            if (
                not clause
                or 0 in clause
                or len(set(clause)) != len(clause)
                or any(-literal in clause for literal in clause)
            ):
                raise AssertionError("malformed DoubleLex clause")
            clauses.append(clause)
    if len(clauses) != 255 or sum(map(len, clauses)) != 3_586:
        raise AssertionError("eight-bit comparator census changed")
    return tuple(clauses)


def doublelex_suffix() -> tuple[tuple[int, ...], ...]:
    clauses = tuple(
        clause
        for left, right in zip(ANCHOR[:-1], ANCHOR[1:], strict=True)
        for clause in comparator_clauses(left, right)
    )
    if (
        len(clauses) != SUFFIX_CLAUSE_COUNT
        or sum(map(len, clauses)) != SUFFIX_LITERAL_COUNT
    ):
        raise AssertionError("DoubleLex suffix census changed")
    return clauses


def _parse_parent(payload: bytes) -> None:
    if len(payload) != PARENT_SIZE_BYTES:
        raise ValueError("parent byte size differs")
    if sha256(payload).hexdigest() != PARENT_SHA256:
        raise ValueError("parent SHA-256 differs")
    if not payload.endswith(b"\n"):
        raise ValueError("parent lacks final newline")
    try:
        lines = payload.decode("ascii").splitlines()
    except UnicodeDecodeError as error:
        raise ValueError("parent is not ASCII DIMACS") from error
    if lines[0] != (
        f"p cnf {PARENT_VARIABLE_COUNT} {PARENT_CLAUSE_COUNT}"
    ):
        raise ValueError("parent header differs")
    if len(lines) != PARENT_CLAUSE_COUNT + 1:
        raise ValueError("parent clause-line count differs")
    literal_count = 0
    for line_number, line in enumerate(lines[1:], start=2):
        try:
            tokens = tuple(map(int, line.split()))
        except ValueError as error:
            raise ValueError(
                f"parent clause {line_number} is not integer DIMACS"
            ) from error
        if not tokens or tokens[-1] != 0 or 0 in tokens[:-1]:
            raise ValueError(f"parent clause {line_number} terminator differs")
        clause = tokens[:-1]
        if not clause:
            raise ValueError(f"parent clause {line_number} is empty")
        if any(abs(literal) > PARENT_VARIABLE_COUNT for literal in clause):
            raise ValueError(
                f"parent clause {line_number} exceeds variable range"
            )
        literal_count += len(clause)
    if literal_count != PARENT_LITERAL_COUNT:
        raise ValueError("parent literal census differs")


def build_doublelex_payload(parent_payload: bytes) -> bytes:
    _parse_parent(parent_payload)
    first_newline = parent_payload.index(b"\n")
    body = parent_payload[first_newline + 1 :]
    suffix = doublelex_suffix()
    output = bytearray(
        (
            f"p cnf {DOUBLELEX_VARIABLE_COUNT} "
            f"{DOUBLELEX_CLAUSE_COUNT}\n"
        ).encode("ascii")
    )
    output.extend(body)
    for clause in suffix:
        output.extend(" ".join(map(str, clause)).encode("ascii"))
        output.extend(b" 0\n")
    return bytes(output)


def _atomic_write_new(path: Path, payload: bytes) -> None:
    path = path.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(f"refusing to replace {path}")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.link(temporary, path)
        directory_descriptor = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    finally:
        temporary.unlink(missing_ok=True)


def generate(
    *, parent_path: Path, output_path: Path, manifest_path: Path
) -> dict[str, object]:
    parent_payload = parent_path.read_bytes()
    output_payload = build_doublelex_payload(parent_payload)
    suffix = doublelex_suffix()
    manifest: dict[str, object] = {
        "claim_boundary": (
            "FORMULA_GENERATION_ONLY: no SAT, UNSAT, finite exclusion, or "
            "universal mathematical claim"
        ),
        "doublelex": {
            "clause_count": DOUBLELEX_CLAUSE_COUNT,
            "literal_count": DOUBLELEX_LITERAL_COUNT,
            "path": str(output_path.resolve()),
            "sha256": sha256(output_payload).hexdigest(),
            "size_bytes": len(output_payload),
            "variable_count": DOUBLELEX_VARIABLE_COUNT,
        },
        "parent": {
            "clause_count": PARENT_CLAUSE_COUNT,
            "literal_count": PARENT_LITERAL_COUNT,
            "path": str(parent_path.resolve()),
            "sha256": sha256(parent_payload).hexdigest(),
            "size_bytes": len(parent_payload),
            "variable_count": PARENT_VARIABLE_COUNT,
        },
        "schema": "gamma-theta-order12-k4-doublelex-formula-v1",
        "schema_version": 1,
        "suffix": {
            "clause_count": len(suffix),
            "literal_count": sum(map(len, suffix)),
            "sha256": sha256(
                b"".join(
                    (
                        " ".join(map(str, clause)) + " 0\n"
                    ).encode("ascii")
                    for clause in suffix
                )
            ).hexdigest(),
        },
    }
    manifest_payload = (
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    _atomic_write_new(output_path, output_payload)
    try:
        _atomic_write_new(manifest_path, manifest_payload)
    except BaseException:
        output_path.unlink(missing_ok=True)
        raise
    return manifest


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--parent", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    manifest = generate(
        parent_path=arguments.parent,
        output_path=arguments.output,
        manifest_path=arguments.manifest,
    )
    print(json.dumps(manifest, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

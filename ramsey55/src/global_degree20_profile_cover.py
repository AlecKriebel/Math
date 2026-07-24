#!/usr/bin/env python3
"""Exact 253-profile cover of the global minmax-degree-20 case.

Every graph in this case has all degrees in ``{20,21,22}``.  Write
``(a,b,c)`` for the multiplicities of degrees 20, 21, and 22.  The handshake
lemma makes ``b`` even.  Hence ``a+c=43-b`` is odd, so ``a != c``.
Complementation swaps ``a`` and ``c`` and preserves ``b``; orient uniquely
so that ``a>c``.  Finally relabel vertices into nondecreasing degree order.
This leaves exactly 253 multiplicity profiles.

Exact degree constraints use only false final thresholds of the direct
formula's forward counters.  Such units are semantically sound without
assuming reverse counter implications:

* degree 20: edge count < 21 and nonedge count < 23;
* degree 21: edge count < 22 and nonedge count < 22;
* degree 22: edge count < 23 and nonedge count < 21.

The two threshold-23 units are already implied by the global branch-20
interval, but are retained in every profile so each cube is self-contained.
The selector-union encoding is an exact symmetry cover, not a solve result.
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import json
import os
import tempfile
import time
from pathlib import Path
from typing import Iterable, Iterator, Sequence

from global_minmax_degree_cover import (
    BASE_CNF_SHA256,
    BASE_METADATA_SHA256,
    ORDER,
    direct_instance,
)


DEGREES = (20, 21, 22)
BASE_VARIABLE_COUNT = 65_403
BASE_CLAUSE_COUNT = 2_052_132
SCHEMA = "ramsey55.global_degree20_profile_cover.v1"
GENERATOR_ID = "ramsey55_global_degree20_profile_union_cnf_v1"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def clause_stream_sha256(clauses: Iterable[Sequence[int]]) -> str:
    digest = hashlib.sha256()
    for clause in clauses:
        digest.update((" ".join(map(str, clause)) + " 0\n").encode("ascii"))
    return digest.hexdigest()


def profiles() -> tuple[tuple[int, int, int], ...]:
    """Return all canonical ``(n20,n21,n22)`` triples."""

    result = tuple(
        (count20, count21, count22)
        for count21 in range(0, ORDER + 1, 2)
        for count22 in range(ORDER - count21 + 1)
        for count20 in (ORDER - count21 - count22,)
        if count20 > count22
    )
    if len(result) != 253 or len(set(result)) != len(result):
        raise AssertionError("unexpected degree-profile census")
    if any(
        sum(profile) != ORDER
        or profile[1] % 2
        or profile[0] <= profile[2]
        for profile in result
    ):
        raise AssertionError("invalid canonical profile")
    return result


@functools.lru_cache(maxsize=1)
def counter_finals() -> tuple[tuple[int, ...], ...]:
    instance = direct_instance()
    finals = tuple(counter.rows[-1] for counter in instance.counters)
    if len(finals) != 2 * ORDER:
        raise AssertionError("unexpected direct-counter count")
    return finals


def final_threshold(counter_index: int, threshold: int) -> int:
    final = counter_finals()[counter_index]
    if threshold < 1 or threshold > len(final):
        raise ValueError("threshold is not allocated")
    return final[threshold - 1]


def exact_degree_units(vertex: int, degree: int) -> tuple[int, ...]:
    """Units forcing one exact degree using edge/nonedge upper thresholds."""

    if not 0 <= vertex < ORDER:
        raise ValueError("vertex outside order")
    if degree not in DEGREES:
        raise ValueError(f"degree must be one of {DEGREES}")
    edge_counter = 2 * vertex
    nonedge_counter = edge_counter + 1
    if degree == 20:
        return (
            -final_threshold(edge_counter, 21),
            -final_threshold(nonedge_counter, 23),
        )
    if degree == 21:
        return (
            -final_threshold(edge_counter, 22),
            -final_threshold(nonedge_counter, 22),
        )
    return (
        -final_threshold(edge_counter, 23),
        -final_threshold(nonedge_counter, 21),
    )


def profile_units(profile: Sequence[int]) -> tuple[int, ...]:
    if tuple(profile) not in profiles():
        raise ValueError("profile is not a canonical degree-20 profile")
    result: list[int] = []
    vertex = 0
    for degree, multiplicity in zip(DEGREES, profile):
        for _ in range(multiplicity):
            result.extend(exact_degree_units(vertex, degree))
            vertex += 1
    if vertex != ORDER:
        raise AssertionError("profile did not assign every vertex")
    if len(result) != 2 * ORDER or len(set(map(abs, result))) != 2 * ORDER:
        raise AssertionError("profile units are not on 86 distinct thresholds")
    return tuple(result)


def selector_clauses(
    first_selector: int = BASE_VARIABLE_COUNT + 1,
) -> Iterator[tuple[int, ...]]:
    canonical = profiles()
    selectors = tuple(range(first_selector, first_selector + len(canonical)))
    yield selectors
    for selector, profile in zip(selectors, canonical):
        for literal in profile_units(profile):
            yield (-selector, literal)


def build_plan() -> dict[str, object]:
    canonical = profiles()
    records: list[dict[str, object]] = []
    for index, profile in enumerate(canonical):
        units = profile_units(profile)
        count20, count21, count22 = profile
        edge_count = (
            20 * count20 + 21 * count21 + 22 * count22
        ) // 2
        records.append(
            {
                "profile_index": index,
                "profile_id": (
                    f"n20_{count20:02d}_n21_{count21:02d}_n22_{count22:02d}"
                ),
                "multiplicities": list(profile),
                "edge_count": edge_count,
                "assumption_count": len(units),
                "assumptions_sha256": clause_stream_sha256(
                    (literal,) for literal in units
                ),
            }
        )
    additions = tuple(selector_clauses())
    return {
        "schema": SCHEMA,
        "status": "EXACT_PROFILE_COVER_AND_UNION_ENCODING_NO_SOLVE_CLAIM",
        "order": ORDER,
        "degree_values": list(DEGREES),
        "base_cnf_sha256": BASE_CNF_SHA256,
        "base_metadata_sha256": BASE_METADATA_SHA256,
        "base_variable_count": BASE_VARIABLE_COUNT,
        "base_clause_count": BASE_CLAUSE_COUNT,
        "profile_count": len(canonical),
        "profiles": records,
        "profile_stream_sha256": hashlib.sha256(
            "".join(
                f"{count20} {count21} {count22}\n"
                for count20, count21, count22 in canonical
            ).encode("ascii")
        ).hexdigest(),
        "selector_union": {
            "selector_variable_first": BASE_VARIABLE_COUNT + 1,
            "selector_variable_count": len(canonical),
            "variable_count": BASE_VARIABLE_COUNT + len(canonical),
            "selector_at_least_one_clause_count": 1,
            "selector_implication_clause_count": 2 * ORDER * len(canonical),
            "appended_clause_count": len(additions),
            "appended_clause_stream_sha256": clause_stream_sha256(additions),
            "clause_count": BASE_CLAUSE_COUNT + len(additions),
        },
        "cover_argument": (
            "In the minmax-degree-20 case all degrees are 20, 21, or 22. "
            "Handshake parity makes n21 even, so n20 and n22 differ. "
            "Complement to make n20>n22, then relabel vertices by degree."
        ),
        "claim_limit": (
            "This is an exact symmetry cover and union encoding only. It "
            "contains no SAT model and no UNSAT certificate."
        ),
    }


def write_union_cnf(
    base_cnf: Path,
    output: Path,
    *,
    expected_base_sha256: str = BASE_CNF_SHA256,
) -> dict[str, object]:
    actual_base_sha256 = sha256_file(base_cnf)
    if actual_base_sha256 != expected_base_sha256:
        raise ValueError("base CNF SHA-256 mismatch")
    additions = tuple(selector_clauses())
    variable_count = BASE_VARIABLE_COUNT + len(profiles())
    clause_count = BASE_CLAUSE_COUNT + len(additions)
    output.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256()
    byte_count = 0
    base_header_seen = False
    temporary_name: str | None = None
    started = time.monotonic()
    try:
        with base_cnf.open("rb") as source, tempfile.NamedTemporaryFile(
            mode="wb",
            prefix=output.name + ".",
            suffix=".tmp",
            dir=output.parent,
            delete=False,
        ) as target:
            temporary_name = target.name

            def write(data: bytes) -> None:
                nonlocal byte_count
                target.write(data)
                digest.update(data)
                byte_count += len(data)

            for raw in source:
                fields = raw.split()
                if fields[:2] == [b"p", b"cnf"]:
                    if base_header_seen or len(fields) != 4:
                        raise ValueError("invalid or duplicate base CNF header")
                    if int(fields[2]) != BASE_VARIABLE_COUNT:
                        raise ValueError("unexpected base variable count")
                    if int(fields[3]) != BASE_CLAUSE_COUNT:
                        raise ValueError("unexpected base clause count")
                    write(f"c generator {GENERATOR_ID}\n".encode("ascii"))
                    write(
                        b"c exact degree-20 profile selector union; "
                        b"n20>n22 canonical complement orientation\n"
                    )
                    write(
                        f"p cnf {variable_count} {clause_count}\n".encode(
                            "ascii"
                        )
                    )
                    base_header_seen = True
                else:
                    write(raw)
            if not base_header_seen:
                raise ValueError("base CNF has no problem line")
            for clause in additions:
                write((" ".join(map(str, clause)) + " 0\n").encode("ascii"))
            target.flush()
            os.fsync(target.fileno())
        os.replace(temporary_name, output)
        temporary_name = None
    finally:
        if temporary_name is not None:
            Path(temporary_name).unlink(missing_ok=True)

    return {
        "generator": GENERATOR_ID,
        "schema": SCHEMA,
        "status": "GENERATED_NOT_SOLVED",
        "base_cnf_sha256": actual_base_sha256,
        "base_variable_count": BASE_VARIABLE_COUNT,
        "base_clause_count": BASE_CLAUSE_COUNT,
        "profile_count": len(profiles()),
        "variable_count": variable_count,
        "clause_count": clause_count,
        "appended_clause_count": len(additions),
        "appended_clause_stream_sha256": clause_stream_sha256(additions),
        "cnf_path": str(output.resolve()),
        "cnf_sha256": digest.hexdigest(),
        "cnf_bytes": byte_count,
        "generation_wall_seconds": time.monotonic() - started,
        "generator_source_sha256": sha256_file(Path(__file__)),
        "solve_attempted": False,
        "claim_limit": (
            "This is a symmetry-complete branch encoding, not a SAT/UNSAT "
            "result."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--base-cnf", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--metadata", type=Path)
    args = parser.parse_args()
    if args.base_cnf is None:
        if args.output is not None or args.metadata is not None:
            raise SystemExit(
                "--output/--metadata require --base-cnf; use --plan alone"
            )
        result = build_plan()
        destination = args.plan
    else:
        if args.output is None:
            raise SystemExit("--base-cnf requires --output")
        result = write_union_cnf(args.base_cnf, args.output)
        destination = args.metadata
    rendered = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if destination:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

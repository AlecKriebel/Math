#!/usr/bin/env python3
"""Exact multiplicity-profile cover of the global minmax-degree-19 branch.

Every graph in this branch has all degrees in ``{19,20,21,22,23}`` and has
at least one vertex of degree 19 or 23.  Write

``(a,b,c,d,e) = (n19,n20,n21,n22,n23)``.

The handshake lemma makes ``a+c+e`` even.  Complementation sends the profile
to ``(e,d,c,b,a)``.  A fixed profile would have ``a=e`` and ``b=d``; because
the order is 43 this would make ``c`` odd, and hence ``a+c+e`` odd.  Thus
complementation has no fixed admissible profile.  Orient each pair uniquely
by ``(a,b) > (e,d)`` and then relabel vertices into nondecreasing degree
order.  Exactly 44,275 canonical profiles remain.

Exact degrees use only false final thresholds of the direct formula's
forward counters.  Degree ``q`` is imposed by

* edge count < q+1, and
* nonedge count < 43-q.

Since the two counts sum to 42, these two sound upper bounds force equality.
The selector union is an exact symmetry cover, not a solve result.
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


DEGREES = (19, 20, 21, 22, 23)
BASE_VARIABLE_COUNT = 65_403
BASE_CLAUSE_COUNT = 2_052_132
EXPECTED_PROFILE_COUNT = 44_275
SCHEMA = "ramsey55.global_degree19_profile_cover.v1"
GENERATOR_ID = "ramsey55_global_degree19_profile_union_cnf_v1"


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


@functools.lru_cache(maxsize=1)
def profiles() -> tuple[tuple[int, int, int, int, int], ...]:
    """Return every canonical ``(n19,n20,n21,n22,n23)`` profile."""

    result: list[tuple[int, int, int, int, int]] = []
    for count19 in range(ORDER + 1):
        for count20 in range(ORDER - count19 + 1):
            for count21 in range(ORDER - count19 - count20 + 1):
                remaining = ORDER - count19 - count20 - count21
                for count22 in range(remaining + 1):
                    count23 = remaining - count22
                    profile = (
                        count19,
                        count20,
                        count21,
                        count22,
                        count23,
                    )
                    if (count19 + count21 + count23) % 2:
                        continue
                    if count19 + count23 == 0:
                        continue
                    if (count19, count20) <= (count23, count22):
                        continue
                    result.append(profile)
    canonical = tuple(sorted(result))
    if len(canonical) != EXPECTED_PROFILE_COUNT:
        raise AssertionError("unexpected degree-19 profile census")
    if len(set(canonical)) != len(canonical):
        raise AssertionError("duplicate canonical degree profile")
    for profile in canonical:
        if (
            sum(profile) != ORDER
            or (profile[0] + profile[2] + profile[4]) % 2
            or profile[0] + profile[4] == 0
            or (profile[0], profile[1]) <= (profile[4], profile[3])
        ):
            raise AssertionError("invalid canonical degree-19 profile")
    return canonical


@functools.lru_cache(maxsize=1)
def profile_set() -> frozenset[tuple[int, int, int, int, int]]:
    return frozenset(profiles())


@functools.lru_cache(maxsize=1)
def counter_finals() -> tuple[tuple[int, ...], ...]:
    instance = direct_instance()
    finals = tuple(counter.rows[-1] for counter in instance.counters)
    if len(finals) != 2 * ORDER:
        raise AssertionError("unexpected direct-counter count")
    if any(len(final) < 24 for final in finals):
        raise AssertionError("direct counters do not allocate threshold 24")
    return finals


def final_threshold(counter_index: int, threshold: int) -> int:
    final = counter_finals()[counter_index]
    if threshold < 1 or threshold > len(final):
        raise ValueError("threshold is not allocated")
    return final[threshold - 1]


def exact_degree_units(vertex: int, degree: int) -> tuple[int, int]:
    """Force one exact degree using only sound false final thresholds."""

    if not 0 <= vertex < ORDER:
        raise ValueError("vertex outside order")
    if degree not in DEGREES:
        raise ValueError(f"degree must be one of {DEGREES}")
    edge_counter = 2 * vertex
    nonedge_counter = edge_counter + 1
    return (
        -final_threshold(edge_counter, degree + 1),
        -final_threshold(nonedge_counter, ORDER - degree),
    )


def profile_units(profile: Sequence[int]) -> tuple[int, ...]:
    canonical = tuple(profile)
    if canonical not in profile_set():
        raise ValueError("profile is not a canonical degree-19 profile")
    result: list[int] = []
    vertex = 0
    for degree, multiplicity in zip(DEGREES, canonical):
        for _ in range(multiplicity):
            result.extend(exact_degree_units(vertex, degree))
            vertex += 1
    if vertex != ORDER:
        raise AssertionError("profile did not assign every vertex")
    if len(result) != 2 * ORDER or len(set(map(abs, result))) != 2 * ORDER:
        raise AssertionError("profile units are not on 86 distinct thresholds")
    if any(literal >= 0 for literal in result):
        raise AssertionError("exact-degree units must all be false thresholds")
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


def profile_stream_sha256(
    canonical: Iterable[tuple[int, int, int, int, int]] | None = None,
) -> str:
    if canonical is None:
        canonical = profiles()
    digest = hashlib.sha256()
    for profile in canonical:
        digest.update((" ".join(map(str, profile)) + "\n").encode("ascii"))
    return digest.hexdigest()


def build_plan() -> dict[str, object]:
    canonical = profiles()
    records: list[dict[str, object]] = []
    for index, profile in enumerate(canonical):
        units = profile_units(profile)
        edge_degree_sum = sum(
            degree * multiplicity
            for degree, multiplicity in zip(DEGREES, profile)
        )
        if edge_degree_sum % 2:
            raise AssertionError("handshake parity failed inside canonical profile")
        records.append(
            {
                "profile_index": index,
                "profile_id": "_".join(
                    f"n{degree}_{multiplicity:02d}"
                    for degree, multiplicity in zip(DEGREES, profile)
                ),
                "multiplicities": list(profile),
                "edge_count": edge_degree_sum // 2,
                "assumption_count": len(units),
                "assumptions_sha256": clause_stream_sha256(
                    (literal,) for literal in units
                ),
            }
        )
    appended_clause_count = 1 + 2 * ORDER * len(canonical)
    appended_hash = clause_stream_sha256(selector_clauses())
    return {
        "schema": SCHEMA,
        "status": "EXACT_MINMAX19_PROFILE_COVER_AND_UNION_ENCODING_NO_SOLVE_CLAIM",
        "order": ORDER,
        "degree_values": list(DEGREES),
        "base_cnf_sha256": BASE_CNF_SHA256,
        "base_metadata_sha256": BASE_METADATA_SHA256,
        "base_variable_count": BASE_VARIABLE_COUNT,
        "base_clause_count": BASE_CLAUSE_COUNT,
        "admissible_profile_count_before_complement": 2 * len(canonical),
        "complement_fixed_profile_count": 0,
        "profile_count": len(canonical),
        "profiles": records,
        "profile_stream_sha256": profile_stream_sha256(canonical),
        "selector_union": {
            "selector_variable_first": BASE_VARIABLE_COUNT + 1,
            "selector_variable_count": len(canonical),
            "variable_count": BASE_VARIABLE_COUNT + len(canonical),
            "selector_at_least_one_clause_count": 1,
            "selector_implication_clause_count": 2 * ORDER * len(canonical),
            "appended_clause_count": appended_clause_count,
            "appended_clause_stream_sha256": appended_hash,
            "clause_count": BASE_CLAUSE_COUNT + appended_clause_count,
        },
        "cover_argument": (
            "In the exact minmax-degree-19 branch every degree is 19..23 "
            "and n19+n23>0. Handshake parity makes n19+n21+n23 even. "
            "Complement swaps (n19,n20,n21,n22,n23) with "
            "(n23,n22,n21,n20,n19). A fixed profile would force n21 odd "
            "and violate handshake parity. Orient uniquely by "
            "(n19,n20)>(n23,n22), then relabel vertices by degree."
        ),
        "threshold_argument": (
            "For degree q, the negative edge threshold q+1 and negative "
            "nonedge threshold 43-q are sound in the forward counters. "
            "Their two upper bounds, with edges+nonedges=42, force degree q."
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
    profile_count = len(profiles())
    appended_clause_count = 1 + 2 * ORDER * profile_count
    variable_count = BASE_VARIABLE_COUNT + profile_count
    clause_count = BASE_CLAUSE_COUNT + appended_clause_count
    output.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256()
    appended_digest = hashlib.sha256()
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
                        b"c exact minmax-degree-19 profile selector union; "
                        b"(n19,n20)>(n23,n22) complement orientation\n"
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
            for clause in selector_clauses():
                rendered = (" ".join(map(str, clause)) + " 0\n").encode("ascii")
                write(rendered)
                appended_digest.update(rendered)
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
        "profile_count": profile_count,
        "variable_count": variable_count,
        "clause_count": clause_count,
        "appended_clause_count": appended_clause_count,
        "appended_clause_stream_sha256": appended_digest.hexdigest(),
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
        if destination.exists():
            raise FileExistsError(f"refusing to overwrite {destination}")
        destination.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Independent reconstruction and proof check for the order-5 80-leaf bundle.

This checker deliberately does not import the producing workflow or its
fixed-split search module.  It rebuilds the prime-automorphism CNF through the
independent generic checker, derives the all-ones cube and residual symmetry
action directly, reconstructs every residual CNF, and checks each stored DRAT
and LRAT proof after decompression.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Mapping, Sequence


ROOT = Path(__file__).resolve().parents[1]

import sys

sys.path.insert(0, str(ROOT / "verify"))

from automorphism_orbit_cnf_check import (  # noqa: E402
    independently_build,
    read_dimacs,
)


CHECKER_ID = "ramsey55_order5_allones_internal80_independent_checker_v1"
EXPECTED_PLAN_ID = "ramsey55_order5_allones_internal80_certificate_plan_v1"
EXPECTED_RESULT_ID = "ramsey55_order5_allones_internal80_certificate_result_v1"

DEFAULT_BASE_CNF = (
    ROOT / "certificates" / "order43_automorphism5_eight_cycles.cnf"
)
DEFAULT_PLAN = (
    ROOT
    / "results"
    / "benchmark_plans"
    / "automorphism5_allones_internal80_certification_v1.json"
)
DEFAULT_BUNDLE = (
    ROOT
    / "certificates"
    / "order43_automorphism5_allones_internal80"
)
DEFAULT_RESULT = (
    ROOT
    / "results"
    / "verification"
    / "automorphism5_allones_internal80_certificate_check.json"
)


class CheckError(RuntimeError):
    """The frozen cover or one of its certificates failed verification."""


def sha256_file(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def sha256_json(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def atomic_json(path: Path, value: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            prefix=path.name + ".",
            suffix=".tmp",
            dir=path.parent,
            delete=False,
        ) as stream:
            temporary = stream.name
            json.dump(value, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            Path(temporary).unlink(missing_ok=True)


def checker_says_verified(output: str) -> bool:
    return any(
        "VERIFIED" in line and "NOT VERIFIED" not in line
        for line in output.splitlines()
    )


def run_checked(command: Sequence[str]) -> tuple[subprocess.CompletedProcess[str], float]:
    started = time.monotonic()
    completed = subprocess.run(
        list(command), text=True, capture_output=True, check=False
    )
    elapsed = time.monotonic() - started
    if completed.returncode != 0:
        raise CheckError(
            f"command failed ({completed.returncode}): {' '.join(command)}\n"
            f"{completed.stdout[-2000:]}\n{completed.stderr[-2000:]}"
        )
    return completed, elapsed


def edge_variable_from_orbits(
    orbits: Sequence[Sequence[tuple[int, int]]],
) -> dict[tuple[int, int], int]:
    return {
        edge: variable
        for variable, orbit in enumerate(orbits, start=1)
        for edge in orbit
    }


def allones_masks() -> tuple[int, ...]:
    """Masks in the canonical realization with first subset cycles 0..3."""
    return (1, 3, 5, 7, 0, 2, 4, 6)


def independent_orientations() -> tuple[tuple[bool, ...], ...]:
    masks = allones_masks()
    cycle_of_mask = {mask: cycle for cycle, mask in enumerate(masks)}
    if len(cycle_of_mask) != 8:
        raise CheckError("membership masks are not unique")

    def endpoint_swap(bits: tuple[bool, ...]) -> tuple[bool, ...]:
        result = [False] * 8
        for old_cycle, mask in enumerate(masks):
            swapped_mask = (
                (mask & ~3)
                | ((mask & 1) << 1)
                | ((mask & 2) >> 1)
            )
            result[cycle_of_mask[swapped_mask]] = bits[old_cycle]
        return tuple(result)

    representatives: set[tuple[bool, ...]] = set()
    for bits in itertools.product((False, True), repeat=8):
        swapped = endpoint_swap(bits)
        representatives.add(
            min(
                bits,
                swapped,
                tuple(not bit for bit in bits),
                tuple(not bit for bit in swapped),
            )
        )
    result = tuple(sorted(representatives))
    if len(result) != 80:
        raise CheckError("independent orientation quotient is not size 80")
    return result


def independent_fixed_assumptions(
    edge_variable: Mapping[tuple[int, int], int],
) -> tuple[int, ...]:
    subsets = (
        frozenset((0, 1, 2, 3)),
        frozenset((1, 3, 5, 7)),
        frozenset((2, 3, 6, 7)),
    )
    assignment: dict[int, bool] = {
        edge_variable[(40, 41)]: True,
        edge_variable[(40, 42)]: False,
        edge_variable[(41, 42)]: False,
    }
    for fixed_index, fixed_vertex in enumerate((40, 41, 42)):
        for cycle in range(8):
            assignment[edge_variable[(5 * cycle, fixed_vertex)]] = (
                cycle in subsets[fixed_index]
            )
    if len(assignment) != 27:
        raise CheckError("fixed cube does not assign 27 distinct variables")
    return tuple(
        variable if value else -variable
        for variable, value in sorted(assignment.items())
    )


def independent_internal_assumptions(
    orientation: Sequence[bool],
    edge_variable: Mapping[tuple[int, int], int],
) -> tuple[int, ...]:
    literals: list[int] = []
    for cycle, second_distance in enumerate(orientation):
        base = 5 * cycle
        first = edge_variable[(base, base + 1)]
        second = edge_variable[(base, base + 2)]
        literals.extend(
            (
                -first if second_distance else first,
                second if second_distance else -second,
            )
        )
    if len(set(map(abs, literals))) != 16:
        raise CheckError("internal cube does not assign 16 distinct variables")
    return tuple(literals)


def residual_clauses(
    clauses: Sequence[Sequence[int]], assumptions: Sequence[int]
) -> tuple[tuple[int, ...], ...]:
    assignment = {abs(literal): literal > 0 for literal in assumptions}
    if len(assignment) != len(assumptions):
        raise CheckError("cube variables overlap")
    result: set[tuple[int, ...]] = set()
    for original in clauses:
        if any(
            variable in assignment
            and assignment[variable] == (literal > 0)
            for literal in original
            for variable in (abs(literal),)
        ):
            continue
        reduced = tuple(
            literal for literal in original if abs(literal) not in assignment
        )
        if not reduced:
            raise CheckError("cube directly falsifies an independent base clause")
        result.add(reduced)
    return tuple(sorted(result))


def dimacs_digest(
    variable_count: int, clauses: Sequence[Sequence[int]]
) -> tuple[str, int]:
    state = hashlib.sha256()
    byte_count = 0
    for payload in (
        f"p cnf {variable_count} {len(clauses)}\n".encode("ascii"),
        *(
            (" ".join(map(str, clause)) + " 0\n").encode("ascii")
            for clause in clauses
        ),
    ):
        state.update(payload)
        byte_count += len(payload)
    return state.hexdigest(), byte_count


def write_dimacs(
    path: Path, variable_count: int, clauses: Sequence[Sequence[int]]
) -> None:
    with path.open("w", encoding="ascii", newline="\n") as stream:
        stream.write(f"p cnf {variable_count} {len(clauses)}\n")
        for clause in clauses:
            stream.write(" ".join(map(str, clause)) + " 0\n")


def independent_cover(
    plan: Mapping[str, object],
    base_cnf: Path,
) -> tuple[
    tuple[tuple[int, ...], ...],
    dict[tuple[int, int], int],
    tuple[tuple[bool, ...], ...],
    tuple[tuple[int, ...], ...],
]:
    _, orbits, independent_clauses = independently_build(5, 8)
    variables, declared, actual_clauses = read_dimacs(base_cnf)
    if (
        variables != len(orbits)
        or declared != len(independent_clauses)
        or actual_clauses != independent_clauses
    ):
        raise CheckError("shared CNF differs from independent reconstruction")
    base = plan.get("base_formula")
    if (
        not isinstance(base, dict)
        or base.get("sha256") != sha256_file(base_cnf)
        or base.get("bytes") != base_cnf.stat().st_size
        or base.get("variable_count") != variables
        or base.get("clause_count") != declared
    ):
        raise CheckError("plan base-formula pins are invalid")
    edge_variable = edge_variable_from_orbits(orbits)
    orientations = independent_orientations()
    fixed = independent_fixed_assumptions(edge_variable)
    exact = plan.get("exact_cover")
    orientation_lists = [
        [int(value) for value in orientation] for orientation in orientations
    ]
    if (
        not isinstance(exact, dict)
        or exact.get("labeled_orientation_count") != 256
        or exact.get("group_order") != 4
        or exact.get("representative_count") != 80
        or exact.get("representatives") != orientation_lists
        or exact.get("representatives_sha256") != sha256_json(orientation_lists)
    ):
        raise CheckError("plan does not contain the independent exact cover")

    expected_cubes: list[tuple[int, ...]] = []
    plan_orbits = plan.get("orbits")
    if not isinstance(plan_orbits, list) or len(plan_orbits) != 80:
        raise CheckError("plan orbit schedule is not exactly 80 records")
    for index, (orientation, plan_orbit) in enumerate(
        zip(orientations, plan_orbits, strict=True)
    ):
        if not isinstance(plan_orbit, dict):
            raise CheckError("malformed plan orbit")
        cube = (*fixed, *independent_internal_assumptions(
            orientation, edge_variable
        ))
        residual = residual_clauses(independent_clauses, cube)
        digest, byte_count = dimacs_digest(variables, residual)
        bits = "".join("1" if value else "0" for value in orientation)
        if (
            plan_orbit.get("index") != index
            or plan_orbit.get("id") != f"orbit_{index:03d}_{bits}"
            or plan_orbit.get("orientation")
            != [int(value) for value in orientation]
            or plan_orbit.get("assumptions") != list(cube)
            or plan_orbit.get("residual_variable_count") != variables
            or plan_orbit.get("residual_clause_count") != len(residual)
            or plan_orbit.get("residual_dimacs_sha256") != digest
            or plan_orbit.get("residual_dimacs_bytes") != byte_count
        ):
            raise CheckError(f"plan orbit {index} failed independent reconstruction")
        expected_cubes.append(tuple(cube))
    return independent_clauses, edge_variable, orientations, tuple(expected_cubes)


def validate_tool_pins(plan: Mapping[str, object]) -> dict[str, Path]:
    raw = plan.get("tools")
    if not isinstance(raw, dict):
        raise CheckError("tool pins are missing")
    result: dict[str, Path] = {}
    for name in (
        "python",
        "pysat_solvers_py",
        "pysolvers_extension",
        "drat_trim",
        "lrat_check",
        "zstd",
    ):
        entry = raw.get(name)
        if not isinstance(entry, dict):
            raise CheckError(f"tool pin is missing: {name}")
        path = Path(str(entry.get("path")))
        if (
            not path.is_file()
            or entry.get("sha256") != sha256_file(path)
            or entry.get("bytes") != path.stat().st_size
        ):
            raise CheckError(f"tool pin changed: {name}")
        result[name] = path
    return result


def decompress(
    archive: Path, target: Path, zstd: Path
) -> tuple[str, int, float]:
    started = time.monotonic()
    with target.open("wb") as stream:
        completed = subprocess.run(
            (str(zstd), "-d", "-c", "-q", str(archive)),
            stdout=stream,
            stderr=subprocess.PIPE,
            check=False,
        )
    elapsed = time.monotonic() - started
    if completed.returncode != 0:
        raise CheckError(
            f"zstd rejected {archive}: "
            f"{completed.stderr.decode(errors='replace')[-2000:]}"
        )
    return sha256_file(target), target.stat().st_size, elapsed


def reusable_verification(
    prior: Mapping[str, object] | None,
    *,
    leaf_id: str,
    residual_hash: str,
    drat_archive_hash: str,
    lrat_archive_hash: str,
) -> dict[str, object] | None:
    if (
        prior is not None
        and prior.get("id") == leaf_id
        and prior.get("valid") is True
        and prior.get("residual_dimacs_sha256") == residual_hash
        and prior.get("drat_zstd_sha256") == drat_archive_hash
        and prior.get("lrat_zstd_sha256") == lrat_archive_hash
        and prior.get("drat_trim_valid") is True
        and prior.get("lrat_check_valid") is True
    ):
        result = dict(prior)
        result["resumed"] = True
        return result
    return None


def progress_payload(
    *,
    plan_path: Path,
    base_cnf: Path,
    bundle: Path,
    records: Sequence[Mapping[str, object]],
    status: str,
    started: float,
) -> dict[str, object]:
    return {
        "checker": CHECKER_ID,
        "valid": (
            status == "VALID"
            and len(records) == 80
            and all(record.get("valid") for record in records)
        ),
        "status": status,
        "claim_scope": (
            "Independent formula, symmetry-cover, residual, DRAT, and LRAT "
            "verification for the normalized order-5 all-ones leaf only."
        ),
        "plan_path": str(plan_path.resolve()),
        "plan_sha256": sha256_file(plan_path),
        "base_cnf_path": str(base_cnf.resolve()),
        "base_cnf_sha256": sha256_file(base_cnf),
        "bundle_directory": str(bundle.resolve()),
        "checker_sha256": sha256_file(Path(__file__).resolve()),
        "scheduled_orbit_count": 80,
        "verified_orbit_count": len(records),
        "all_orbits_verified": (
            len(records) == 80 and all(record.get("valid") for record in records)
        ),
        "records": list(records),
        "runtime_seconds": time.monotonic() - started,
    }


def verify(
    *,
    plan_path: Path,
    base_cnf: Path,
    bundle: Path,
    result_path: Path,
) -> dict[str, object]:
    started = time.monotonic()
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    if plan.get("plan") != EXPECTED_PLAN_ID:
        raise CheckError("unexpected plan identifier")
    tools = validate_tool_pins(plan)
    base_clauses, _, orientations, cubes = independent_cover(plan, base_cnf)
    plan_orbits = plan["orbits"]
    assert isinstance(plan_orbits, list)

    prior_by_id: dict[str, Mapping[str, object]] = {}
    if result_path.is_file():
        try:
            prior_result = json.loads(result_path.read_text(encoding="utf-8"))
            if (
                prior_result.get("checker") == CHECKER_ID
                and prior_result.get("plan_sha256") == sha256_file(plan_path)
                and prior_result.get("base_cnf_sha256") == sha256_file(base_cnf)
                and prior_result.get("checker_sha256")
                == sha256_file(Path(__file__).resolve())
            ):
                prior_by_id = {
                    str(record["id"]): record
                    for record in prior_result.get("records", [])
                    if isinstance(record, dict) and "id" in record
                }
        except (OSError, UnicodeError, json.JSONDecodeError):
            prior_by_id = {}

    records: list[dict[str, object]] = []
    work_root = Path(
        tempfile.mkdtemp(prefix="r55-aut5-allones-check-", dir=bundle.parent)
    )
    try:
        for plan_orbit, orientation, cube in zip(
            plan_orbits, orientations, cubes, strict=True
        ):
            assert isinstance(plan_orbit, dict)
            leaf_id = str(plan_orbit["id"])
            record_path = bundle / f"{leaf_id}.result.json"
            drat_archive = bundle / f"{leaf_id}.drat.zst"
            lrat_archive = bundle / f"{leaf_id}.lrat.zst"
            if not all(path.is_file() for path in (
                record_path, drat_archive, lrat_archive
            )):
                raise CheckError(f"certificate artifacts are missing for {leaf_id}")
            producer = json.loads(record_path.read_text(encoding="utf-8"))
            drat_archive_hash = sha256_file(drat_archive)
            lrat_archive_hash = sha256_file(lrat_archive)
            if (
                producer.get("result") != EXPECTED_RESULT_ID
                or producer.get("status") != "CERTIFIED_UNSAT"
                or producer.get("id") != leaf_id
                or producer.get("orientation")
                != [int(value) for value in orientation]
                or producer.get("assumptions") != list(cube)
                or producer.get("residual_dimacs_sha256")
                != plan_orbit["residual_dimacs_sha256"]
                or not producer.get("drat_trim_core_valid")
                or not producer.get("lrat_check_valid")
            ):
                raise CheckError(f"producer record is invalid for {leaf_id}")
            for key, archive, digest in (
                ("drat", drat_archive, drat_archive_hash),
                ("lrat", lrat_archive, lrat_archive_hash),
            ):
                compressed = producer.get(f"{key}_zstd")
                if (
                    not isinstance(compressed, dict)
                    or compressed.get("sha256") != digest
                    or compressed.get("bytes") != archive.stat().st_size
                ):
                    raise CheckError(f"{key} archive pin failed for {leaf_id}")

            reused = reusable_verification(
                prior_by_id.get(leaf_id),
                leaf_id=leaf_id,
                residual_hash=str(plan_orbit["residual_dimacs_sha256"]),
                drat_archive_hash=drat_archive_hash,
                lrat_archive_hash=lrat_archive_hash,
            )
            if reused is not None:
                records.append(reused)
                print(
                    json.dumps(
                        {
                            "event": "verification_resumed",
                            "id": leaf_id,
                            "verified": len(records),
                            "scheduled": 80,
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )
                continue

            leaf_work = work_root / leaf_id
            leaf_work.mkdir()
            residual = residual_clauses(base_clauses, cube)
            digest, byte_count = dimacs_digest(183, residual)
            if (
                digest != plan_orbit["residual_dimacs_sha256"]
                or byte_count != plan_orbit["residual_dimacs_bytes"]
                or len(residual) != plan_orbit["residual_clause_count"]
            ):
                raise CheckError(f"residual fingerprint failed for {leaf_id}")
            cnf = leaf_work / "residual.cnf"
            drat = leaf_work / "core.drat"
            lrat = leaf_work / "proof.lrat"
            write_dimacs(cnf, 183, residual)
            if sha256_file(cnf) != digest:
                raise CheckError("materialized residual hash mismatch")
            drat_hash, drat_bytes, drat_decompress_wall = decompress(
                drat_archive, drat, tools["zstd"]
            )
            lrat_hash, lrat_bytes, lrat_decompress_wall = decompress(
                lrat_archive, lrat, tools["zstd"]
            )
            drat_uncompressed = producer.get("drat_uncompressed")
            lrat_uncompressed = producer.get("lrat_uncompressed")
            if (
                not isinstance(drat_uncompressed, dict)
                or drat_uncompressed.get("sha256") != drat_hash
                or drat_uncompressed.get("bytes") != drat_bytes
                or not isinstance(lrat_uncompressed, dict)
                or lrat_uncompressed.get("sha256") != lrat_hash
                or lrat_uncompressed.get("bytes") != lrat_bytes
            ):
                raise CheckError(f"decompressed proof pins failed for {leaf_id}")
            drat_checked, drat_wall = run_checked(
                (
                    str(tools["drat_trim"]),
                    str(cnf),
                    str(drat),
                    "-I",
                )
            )
            drat_valid = checker_says_verified(
                drat_checked.stdout + drat_checked.stderr
            )
            lrat_checked, lrat_wall = run_checked(
                (str(tools["lrat_check"]), str(cnf), str(lrat))
            )
            lrat_valid = checker_says_verified(
                lrat_checked.stdout + lrat_checked.stderr
            )
            if not drat_valid or not lrat_valid:
                raise CheckError(f"proof verification failed for {leaf_id}")
            record = {
                "id": leaf_id,
                "index": plan_orbit["index"],
                "orientation": plan_orbit["orientation"],
                "valid": True,
                "residual_dimacs_sha256": digest,
                "residual_clause_count": len(residual),
                "drat_zstd_sha256": drat_archive_hash,
                "drat_zstd_bytes": drat_archive.stat().st_size,
                "drat_uncompressed_sha256": drat_hash,
                "drat_uncompressed_bytes": drat_bytes,
                "drat_decompress_wall_seconds": drat_decompress_wall,
                "drat_trim_valid": drat_valid,
                "drat_trim_wall_seconds": drat_wall,
                "lrat_zstd_sha256": lrat_archive_hash,
                "lrat_zstd_bytes": lrat_archive.stat().st_size,
                "lrat_uncompressed_sha256": lrat_hash,
                "lrat_uncompressed_bytes": lrat_bytes,
                "lrat_decompress_wall_seconds": lrat_decompress_wall,
                "lrat_check_valid": lrat_valid,
                "lrat_check_wall_seconds": lrat_wall,
                "resumed": False,
            }
            records.append(record)
            shutil.rmtree(leaf_work)
            atomic_json(
                result_path,
                progress_payload(
                    plan_path=plan_path,
                    base_cnf=base_cnf,
                    bundle=bundle,
                    records=records,
                    status="IN_PROGRESS",
                    started=started,
                ),
            )
            print(
                json.dumps(
                    {
                        "event": "orbit_verified",
                        "id": leaf_id,
                        "verified": len(records),
                        "scheduled": 80,
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
    finally:
        shutil.rmtree(work_root, ignore_errors=True)

    result = progress_payload(
        plan_path=plan_path,
        base_cnf=base_cnf,
        bundle=bundle,
        records=records,
        status="VALID",
        started=started,
    )
    if not result["valid"]:
        raise CheckError("aggregate 80-orbit verification is incomplete")
    atomic_json(result_path, result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--base-cnf", type=Path, default=DEFAULT_BASE_CNF)
    parser.add_argument("--bundle", type=Path, default=DEFAULT_BUNDLE)
    parser.add_argument("--result", type=Path, default=DEFAULT_RESULT)
    args = parser.parse_args()
    result = verify(
        plan_path=args.plan,
        base_cnf=args.base_cnf,
        bundle=args.bundle,
        result_path=args.result,
    )
    print(json.dumps({"event": "verification_complete", **result}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CheckError as error:
        print(
            json.dumps(
                {"checker": CHECKER_ID, "valid": False, "error": str(error)},
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        raise SystemExit(1)

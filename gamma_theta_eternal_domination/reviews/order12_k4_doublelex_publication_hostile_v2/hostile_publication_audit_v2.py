#!/usr/bin/env python3
"""Clean-room hostile audit of the V2 compact DoubleLex publication package.

This reviewer-written harness never invokes a SAT solver.  It independently
audits the publication manifest, reconstructs the accepted LRAT from the zstd
payload, compares it byte-for-byte with the frozen author LRAT, reruns the
package's one-command verifier from a private mirror, and probes fail-closed
behavior under isolated mutations.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from typing import Any


REVIEW_DIR = Path(__file__).resolve().parent
CAMPAIGN = REVIEW_DIR.parents[1]
PACKAGE = (
    CAMPAIGN
    / "certificates/order12_k4_doublelex_seed0_lrat_publication"
)
FORMULA = CAMPAIGN / "instances/order12_k4_connected_doublelex/instance.cnf"
CHECKER = CAMPAIGN / "tools/drat_trim_2023_05_22/lrat-check"
AUTHOR_PACKAGE = (
    CAMPAIGN / "certificates/order12_k4_doublelex_seed0_lrat"
)
AUTHOR_CERTIFICATE = AUTHOR_PACKAGE / "certificate.json"
AUTHOR_MANIFEST = AUTHOR_PACKAGE / "artifact-manifest.json"
AUTHOR_LRAT = AUTHOR_PACKAGE / "proof/proof.converted.lrat"
HOSTILE_REVIEW_DIR = (
    CAMPAIGN / "reviews/order12_k4_doublelex_lrat_hostile_0814a4f4"
)
HOSTILE_REVIEW = HOSTILE_REVIEW_DIR / "REVIEW.md"
HOSTILE_EVIDENCE = HOSTILE_REVIEW_DIR / "hostile-evidence.json"
V1_REVIEW_DIR = (
    CAMPAIGN / "reviews/order12_k4_doublelex_publication_hostile"
)

FORMULA_SHA256 = (
    "14284db1f0b9cfb37b91d834fbabac1d0ca06d36e0d2782683e35cbd04a976e7"
)
FORMULA_SIZE = 4_030_657
FORMULA_VARIABLES = 18_381
FORMULA_CLAUSES = 115_507
FORMULA_LITERALS = 1_190_774
LRAT_SHA256 = (
    "0e04eb639a3f7f7d335126d56040abb4ef11e8548770262c316a608390659263"
)
LRAT_SIZE = 228_381_671
COMPRESSED_SHA256 = (
    "edc0f6b76bc96b2b26677f399566ae437cc47a6fc0cc921eaff81d77b72a50da"
)
COMPRESSED_SIZE = 64_288_636
CHECKER_SHA256 = (
    "5d7d77a57457db82e57f2505ea9d0267ff0bceff197235b6edfc8fda1f26c7a2"
)
CHECKER_SIZE = 36_520
AUTHOR_CERTIFICATE_SHA256 = (
    "a21bd3db71fb271965859237d7665c5d0c38d32d061fdf3eda285c014e366991"
)
AUTHOR_CERTIFICATE_SIZE = 15_723
AUTHOR_MANIFEST_SHA256 = (
    "846a646ba951569f50a76b562fdc8ec005dcf0f06ff57e48b4e3d4d330fbd607"
)
AUTHOR_MANIFEST_SIZE = 16_369
AUTHOR_INVENTORY_SHA256 = (
    "0814a4f435f9a50784eb12dcd99116f5b4529587a78723bff328dcec86ec7113"
)
AUTHOR_INVENTORY_FILES = 35
AUTHOR_INVENTORY_SIZE = 260_029_326
HOSTILE_REVIEW_SHA256 = (
    "fb95934b5d5acd75c9f6deb9142be3b903900f5abd02a5cc21d9884788f38395"
)
HOSTILE_REVIEW_SIZE = 7_519
HOSTILE_EVIDENCE_SHA256 = (
    "2651f9d286582c068fb872acf862b82c4d4ab8e5fc07f6b99825b9335dd40b63"
)
HOSTILE_EVIDENCE_SIZE = 21_904

TARGET_FILES = {
    "README.md": (
        2_720,
        "07f73c23dd194b7c3b06c9d4743ef3f637a1ff299a1a0d9d28bdb535da6f848f",
    ),
    "proof.converted.lrat.zst": (COMPRESSED_SIZE, COMPRESSED_SHA256),
    "publication-manifest.json": (
        2_766,
        "409214887b0bae931af7cc1d03d0d1eaaf8de667f4adfa3d2e03d6b291c6f77b",
    ),
    "verify_publication.py": (
        8_065,
        "5bceb1c04756c4dcdfedcfd6609270e54b76ad9949de0b7dcee9be4c258c1c05",
    ),
}
V1_REVIEW_FILES = {
    "REVIEW.log": (
        1_207,
        "6031ded4b853dcb0f890cb1d4145d58e8128f2ece610ee417d1d18730af381bf",
    ),
    "REVIEW.md": (
        7_551,
        "2931d5ace745b8441c2bc46a7fd347fdb95ea5b4db94f1071b79ff0968fb0837",
    ),
    "hostile-evidence.json": (
        17_094,
        "3c40bdac300d3d3a1aafefdfdc4dbade9351b2aff7dff1f66e0f0d9223782454",
    ),
    "hostile_publication_audit.py": (
        39_986,
        "d05aa5847db10cdaca2d8452a83062b533bdc77b107a7d8d4d21250afa474994",
    ),
}


class AuditError(RuntimeError):
    """A fail-closed hostile-audit error."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def canonical_json_bytes(value: object, *, pretty: bool = True) -> bytes:
    if pretty:
        encoded = json.dumps(
            value, allow_nan=False, indent=2, sort_keys=True
        )
    else:
        encoded = json.dumps(
            value,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    return (encoded + "\n").encode("utf-8")


def reject_constant(value: str) -> None:
    raise AuditError(f"non-finite JSON constant {value}")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def load_json(path: Path) -> Any:
    try:
        return json.loads(
            path.read_bytes(),
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise AuditError(f"malformed JSON {path}: {error}") from error


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def regular_single_link(path: Path, role: str) -> os.stat_result:
    try:
        metadata = path.lstat()
    except FileNotFoundError as error:
        raise AuditError(f"{role}: missing {path}") from error
    require(
        stat.S_ISREG(metadata.st_mode) and not stat.S_ISLNK(metadata.st_mode),
        f"{role}: not a regular non-symlink file",
    )
    require(metadata.st_nlink == 1, f"{role}: hard-link count is not one")
    return metadata


def binding(
    path: Path,
    role: str,
    expected_size: int | None = None,
    expected_sha256: str | None = None,
) -> dict[str, object]:
    metadata = regular_single_link(path, role)
    actual_sha256 = sha256_file(path)
    if expected_size is not None:
        require(
            metadata.st_size == expected_size,
            f"{role}: size {metadata.st_size}, expected {expected_size}",
        )
    if expected_sha256 is not None:
        require(
            actual_sha256 == expected_sha256,
            f"{role}: SHA-256 {actual_sha256}, expected {expected_sha256}",
        )
    return {
        "path": str(path.resolve()),
        "size_bytes": metadata.st_size,
        "sha256": actual_sha256,
    }


def files_equal(left: Path, right: Path) -> bool:
    if left.stat().st_size != right.stat().st_size:
        return False
    with left.open("rb") as first, right.open("rb") as second:
        while True:
            first_block = first.read(1 << 20)
            second_block = second.read(1 << 20)
            if first_block != second_block:
                return False
            if not first_block:
                return True


def package_snapshot(
    package: Path, *, exact_paths: set[str] | None = None
) -> dict[str, object]:
    entries: list[dict[str, object]] = []
    seen_paths: set[str] = set()
    for path in sorted(package.rglob("*")):
        require(not path.is_symlink(), f"package symlink found: {path}")
        if path.is_dir():
            continue
        require(path.is_file(), f"unexpected package entry: {path}")
        relative = path.relative_to(package).as_posix()
        seen_paths.add(relative)
        metadata = regular_single_link(path, f"package file {relative}")
        entries.append(
            {
                "mode": oct(metadata.st_mode & 0o777),
                "nlink": metadata.st_nlink,
                "path": relative,
                "sha256": sha256_file(path),
                "size_bytes": metadata.st_size,
                "symlink": False,
            }
        )
    if exact_paths is not None:
        require(
            seen_paths == exact_paths,
            "publication inventory differs: "
            f"found={sorted(seen_paths)!r}, expected={sorted(exact_paths)!r}",
        )
    return {
        "file_count": len(entries),
        "total_size_bytes": sum(
            int(entry["size_bytes"]) for entry in entries
        ),
        "inventory_sha256": hashlib.sha256(
            canonical_json_bytes(entries, pretty=False)
        ).hexdigest(),
        "inventory": entries,
    }


def audit_target_inventory() -> dict[str, object]:
    snapshot = package_snapshot(PACKAGE, exact_paths=set(TARGET_FILES))
    by_path = {
        str(entry["path"]): entry for entry in snapshot["inventory"]  # type: ignore[index]
    }
    for relative, (expected_size, expected_sha256) in TARGET_FILES.items():
        record = by_path[relative]
        require(
            record["size_bytes"] == expected_size
            and record["sha256"] == expected_sha256,
            f"target publication file differs from frozen input: {relative}",
        )
    require(snapshot["file_count"] == 4, "target package file count mismatch")
    require(
        snapshot["total_size_bytes"] == 64_302_187,
        "target package total size mismatch",
    )
    return snapshot


def audit_v1_frozen() -> dict[str, object]:
    snapshot = package_snapshot(
        V1_REVIEW_DIR, exact_paths=set(V1_REVIEW_FILES)
    )
    by_path = {
        str(entry["path"]): entry for entry in snapshot["inventory"]  # type: ignore[index]
    }
    for relative, (expected_size, expected_sha256) in V1_REVIEW_FILES.items():
        record = by_path[relative]
        require(
            record["size_bytes"] == expected_size
            and record["sha256"] == expected_sha256,
            f"frozen V1 review file changed: {relative}",
        )
    return {
        key: snapshot[key]
        for key in ("file_count", "total_size_bytes", "inventory_sha256")
    }


def audit_manifest() -> dict[str, object]:
    manifest_path = PACKAGE / "publication-manifest.json"
    manifest = load_json(manifest_path)
    require(isinstance(manifest, dict), "publication manifest is not an object")
    require(
        set(manifest)
        == {
            "accepted_author_package",
            "accepted_hostile_review",
            "claim_boundary",
            "compression",
            "created_at",
            "files",
            "formula",
            "recovered_lrat",
            "revised_at",
            "schema",
            "schema_version",
            "status",
            "verification",
        },
        "publication manifest root schema mismatch",
    )
    require(
        manifest["schema"]
        == "gamma-theta-doublelex-lrat-publication-package-v1"
        and manifest["schema_version"] == 1,
        "publication manifest schema identifier/version mismatch",
    )
    require(
        manifest["created_at"] == "2026-07-26T06:19:02-07:00",
        "publication manifest creation time changed",
    )
    require(
        manifest["revised_at"] == "2026-07-26T06:35:00-07:00",
        "publication manifest revision time changed",
    )
    require(
        manifest["status"]
        == "PENDING_INDEPENDENT_PUBLICATION_PACKAGE_REVIEW_V2",
        "publication manifest status is not the frozen V2 review value",
    )
    require(
        manifest["claim_boundary"]
        == (
            "The exact DoubleLex CNF with SHA-256 "
            f"{FORMULA_SHA256} is UNSAT. Transfer to the connected order-12 "
            "parameter-four graph slice uses separately reviewed mathematical "
            "implications."
        ),
        "publication manifest claim boundary changed",
    )
    require(
        manifest["compression"]
        == {
            "format": "zstd",
            "producer": "Zstandard CLI 1.5.7",
            "level": 9,
            "threads": 1,
            "checksum": True,
            "command": (
                "zstd -9 -T1 --check -f proof.converted.lrat "
                "-o proof.converted.lrat.zst"
            ),
        },
        "publication manifest compression record mismatch",
    )
    expected_files = {
        "readme": {
            "path": "README.md",
            "size_bytes": TARGET_FILES["README.md"][0],
            "sha256": TARGET_FILES["README.md"][1],
        },
        "verifier": {
            "path": "verify_publication.py",
            "integrity": "bound by the external hostile-review inventory",
            "role": "hard-coded trust root for every other publication-package byte",
        },
        "compressed_lrat": {
            "path": "proof.converted.lrat.zst",
            "size_bytes": COMPRESSED_SIZE,
            "sha256": COMPRESSED_SHA256,
        },
    }
    require(manifest["files"] == expected_files, "manifest file map mismatch")
    require(
        manifest["recovered_lrat"]
        == {"size_bytes": LRAT_SIZE, "sha256": LRAT_SHA256},
        "manifest recovered-LRAT binding mismatch",
    )
    require(
        manifest["formula"]
        == {
            "path": "instances/order12_k4_connected_doublelex/instance.cnf",
            "size_bytes": FORMULA_SIZE,
            "variables": FORMULA_VARIABLES,
            "clauses": FORMULA_CLAUSES,
            "literal_occurrences": FORMULA_LITERALS,
            "sha256": FORMULA_SHA256,
        },
        "manifest formula binding/census mismatch",
    )
    require(
        manifest["accepted_author_package"]
        == {
            "path": "certificates/order12_k4_doublelex_seed0_lrat",
            "inventory_sha256": AUTHOR_INVENTORY_SHA256,
            "certificate_sha256": AUTHOR_CERTIFICATE_SHA256,
            "artifact_manifest_sha256": AUTHOR_MANIFEST_SHA256,
        },
        "manifest accepted-author-package binding mismatch",
    )
    require(
        manifest["accepted_hostile_review"]
        == {
            "path": "reviews/order12_k4_doublelex_lrat_hostile_0814a4f4",
            "verdict": "ACCEPT_EXACT_DOUBLELEX_CNF_UNSAT_ONLY",
            "review_sha256": HOSTILE_REVIEW_SHA256,
            "evidence_sha256": HOSTILE_EVIDENCE_SHA256,
        },
        "manifest accepted-hostile-review binding mismatch",
    )
    require(
        manifest["verification"]
        == {
            "command": (
                "python3 certificates/"
                "order12_k4_doublelex_seed0_lrat_publication/"
                "verify_publication.py"
            ),
            "expected_verdict": (
                "VERIFIED_EXACT_DOUBLELEX_CNF_UNSAT_ONLY"
            ),
            "checker_sha256": CHECKER_SHA256,
            "required_success_marker": "c VERIFIED",
        },
        "manifest verification record mismatch",
    )
    return {
        "schema_validation": "PASS_EXACT_SCHEMA_AND_VALUES",
        "verifier_trust_root": binding(
            PACKAGE / "verify_publication.py",
            "externally reviewed publication verifier",
            TARGET_FILES["verify_publication.py"][0],
            TARGET_FILES["verify_publication.py"][1],
        ),
        "binding": binding(
            manifest_path,
            "publication manifest",
            TARGET_FILES["publication-manifest.json"][0],
            TARGET_FILES["publication-manifest.json"][1],
        ),
    }


def strict_dimacs_census(path: Path) -> dict[str, int]:
    header_seen = False
    variables = -1
    declared_clauses = -1
    clauses = 0
    literal_occurrences = 0
    maximum_variable = 0
    current_clause_literals = 0
    with path.open("rt", encoding="ascii", newline="") as stream:
        for line_number, line in enumerate(stream, start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("c"):
                continue
            if stripped.startswith("p"):
                require(not header_seen, f"duplicate DIMACS header at {line_number}")
                fields = stripped.split()
                require(
                    len(fields) == 4 and fields[:2] == ["p", "cnf"],
                    f"malformed DIMACS header at {line_number}",
                )
                variables = int(fields[2])
                declared_clauses = int(fields[3])
                require(
                    variables >= 0 and declared_clauses >= 0,
                    "negative DIMACS census",
                )
                header_seen = True
                continue
            require(header_seen, f"clause before header at {line_number}")
            for token in stripped.split():
                literal = int(token)
                if literal == 0:
                    clauses += 1
                    current_clause_literals = 0
                    continue
                require(
                    abs(literal) <= variables,
                    f"literal out of range at line {line_number}",
                )
                literal_occurrences += 1
                current_clause_literals += 1
                maximum_variable = max(maximum_variable, abs(literal))
    require(header_seen, "missing DIMACS header")
    require(current_clause_literals == 0, "unterminated trailing DIMACS clause")
    require(clauses == declared_clauses, "DIMACS clause-count mismatch")
    return {
        "variables": variables,
        "declared_clauses": declared_clauses,
        "parsed_clauses": clauses,
        "literal_occurrences": literal_occurrences,
        "maximum_variable": maximum_variable,
    }


def audit_accepted_bindings() -> dict[str, object]:
    records = {
        "formula": binding(
            FORMULA, "exact DoubleLex formula", FORMULA_SIZE, FORMULA_SHA256
        ),
        "checker": binding(
            CHECKER, "pinned lrat-check", CHECKER_SIZE, CHECKER_SHA256
        ),
        "author_certificate": binding(
            AUTHOR_CERTIFICATE,
            "accepted author certificate",
            AUTHOR_CERTIFICATE_SIZE,
            AUTHOR_CERTIFICATE_SHA256,
        ),
        "author_manifest": binding(
            AUTHOR_MANIFEST,
            "accepted author manifest",
            AUTHOR_MANIFEST_SIZE,
            AUTHOR_MANIFEST_SHA256,
        ),
        "author_lrat": binding(
            AUTHOR_LRAT, "accepted author LRAT", LRAT_SIZE, LRAT_SHA256
        ),
        "hostile_review": binding(
            HOSTILE_REVIEW,
            "accepted hostile review",
            HOSTILE_REVIEW_SIZE,
            HOSTILE_REVIEW_SHA256,
        ),
        "hostile_evidence": binding(
            HOSTILE_EVIDENCE,
            "accepted hostile evidence",
            HOSTILE_EVIDENCE_SIZE,
            HOSTILE_EVIDENCE_SHA256,
        ),
    }
    census = strict_dimacs_census(FORMULA)
    require(
        census
        == {
            "variables": FORMULA_VARIABLES,
            "declared_clauses": FORMULA_CLAUSES,
            "parsed_clauses": FORMULA_CLAUSES,
            "literal_occurrences": FORMULA_LITERALS,
            "maximum_variable": FORMULA_VARIABLES,
        },
        f"independent formula census mismatch: {census!r}",
    )
    hostile = load_json(HOSTILE_EVIDENCE)
    require(
        isinstance(hostile, dict)
        and hostile.get("schema")
        == "gamma-theta-order12-k4-doublelex-lrat-hostile-evidence-v1"
        and hostile.get("schema_version") == 1
        and hostile.get("verdict")
        == "ACCEPT_EXACT_DOUBLELEX_CNF_UNSAT_ONLY",
        "accepted hostile evidence schema/verdict mismatch",
    )
    proof_bindings = hostile.get("proof_bindings")
    require(isinstance(proof_bindings, dict), "hostile proof bindings absent")
    for role in ("fresh_lrat", "retained_lrat_copy"):
        record = proof_bindings.get(role)
        require(
            isinstance(record, dict)
            and record.get("sha256") == LRAT_SHA256
            and record.get("size_bytes") == LRAT_SIZE,
            f"accepted hostile evidence {role} binding mismatch",
        )
    formula_record = proof_bindings.get("formula")
    require(
        isinstance(formula_record, dict)
        and formula_record.get("sha256") == FORMULA_SHA256
        and formula_record.get("size_bytes") == FORMULA_SIZE,
        "accepted hostile evidence formula binding mismatch",
    )
    accepted_snapshot = hostile.get("author_package_snapshot")
    require(
        isinstance(accepted_snapshot, dict)
        and accepted_snapshot.get("inventory_sha256")
        == AUTHOR_INVENTORY_SHA256
        and accepted_snapshot.get("file_count") == AUTHOR_INVENTORY_FILES
        and accepted_snapshot.get("total_size_bytes")
        == AUTHOR_INVENTORY_SIZE,
        "accepted hostile author snapshot binding mismatch",
    )
    live_snapshot = package_snapshot(AUTHOR_PACKAGE)
    require(
        live_snapshot["inventory_sha256"] == AUTHOR_INVENTORY_SHA256
        and live_snapshot["file_count"] == AUTHOR_INVENTORY_FILES
        and live_snapshot["total_size_bytes"] == AUTHOR_INVENTORY_SIZE,
        "live author package differs from accepted hostile snapshot",
    )
    require(
        live_snapshot["inventory"] == accepted_snapshot.get("inventory"),
        "live author package inventory is not entry-identical to accepted snapshot",
    )
    return {
        "bindings": records,
        "formula_census": census,
        "hostile_verdict": hostile["verdict"],
        "author_package_snapshot": {
            key: live_snapshot[key]
            for key in (
                "file_count",
                "total_size_bytes",
                "inventory_sha256",
            )
        },
    }


def run_command(
    command: list[str],
    *,
    cwd: Path,
    timeout: int = 600,
    env: dict[str, str] | None = None,
) -> dict[str, object]:
    started_ns = time.time_ns()
    started_monotonic = time.monotonic()
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            env=env,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
        )
        timed_out = False
    except subprocess.TimeoutExpired as error:
        return {
            "command": command,
            "exit_code": None,
            "timed_out": True,
            "wall_seconds": time.monotonic() - started_monotonic,
            "stdout": (error.stdout or b"").decode("utf-8", "replace"),
            "stderr": (error.stderr or b"").decode("utf-8", "replace"),
        }
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    return {
        "command": command,
        "exit_code": result.returncode,
        "timed_out": timed_out,
        "started_unix_ns": started_ns,
        "finished_unix_ns": time.time_ns(),
        "wall_seconds": time.monotonic() - started_monotonic,
        "user_cpu_seconds": after.ru_utime - before.ru_utime,
        "system_cpu_seconds": after.ru_stime - before.ru_stime,
        "maximum_resident_set_size_raw": after.ru_maxrss,
        "stdout": result.stdout.decode("utf-8", "strict"),
        "stderr": result.stderr.decode("utf-8", "strict"),
    }


def audit_zstd_and_recovery(work: Path) -> dict[str, object]:
    zstd = shutil.which("zstd")
    require(zstd is not None, "zstd not found")
    version = run_command([zstd, "--version"], cwd=CAMPAIGN)
    require(
        version["exit_code"] == 0
        and "v1.5.7" in str(version["stdout"])
        and not version["stderr"],
        "unexpected zstd version output",
    )
    compressed = PACKAGE / "proof.converted.lrat.zst"
    compressed_binding = binding(
        compressed,
        "compressed publication LRAT",
        COMPRESSED_SIZE,
        COMPRESSED_SHA256,
    )
    frame = run_command([zstd, "-lv", str(compressed)], cwd=CAMPAIGN)
    frame_text = str(frame["stdout"]) + str(frame["stderr"])
    require(
        frame["exit_code"] == 0
        and "# Zstandard Frames: 1" in frame_text
        and "DictID: 0" in frame_text
        and "Decompressed Size: 218 MiB (228381671 B)"
        in frame_text
        and "Check: XXH64 " in frame_text,
        "zstd frame metadata/checksum audit failed",
    )
    integrity = run_command(
        [zstd, "-t", "--no-progress", str(compressed)], cwd=CAMPAIGN
    )
    require(
        integrity["exit_code"] == 0 and not integrity["stdout"],
        "zstd integrity test failed",
    )

    recovered = work / "proof.recovered.lrat"
    decompression = run_command(
        [
            zstd,
            "-d",
            "--quiet",
            "--force",
            str(compressed),
            "-o",
            str(recovered),
        ],
        cwd=work,
    )
    require(
        decompression["exit_code"] == 0
        and not decompression["stdout"]
        and not decompression["stderr"],
        "private zstd decompression failed or wrote output",
    )
    recovered_binding = binding(
        recovered, "recovered LRAT", LRAT_SIZE, LRAT_SHA256
    )
    require(
        files_equal(recovered, AUTHOR_LRAT),
        "recovered LRAT is not byte-identical to accepted author LRAT",
    )

    recompressed = work / "proof.recompressed.lrat.zst"
    recompression = run_command(
        [
            zstd,
            "-9",
            "-T1",
            "--check",
            "--quiet",
            "--force",
            str(recovered),
            "-o",
            str(recompressed),
        ],
        cwd=work,
    )
    require(
        recompression["exit_code"] == 0
        and not recompression["stdout"]
        and not recompression["stderr"],
        "deterministic private recompression failed or wrote output",
    )
    recompressed_binding = binding(
        recompressed,
        "privately recompressed LRAT",
        COMPRESSED_SIZE,
        COMPRESSED_SHA256,
    )
    require(
        files_equal(recompressed, compressed),
        "private zstd -9 -T1 --check output is not byte-identical",
    )
    return {
        "zstd_version": str(version["stdout"]).strip(),
        "compressed_binding": compressed_binding,
        "frame_listing": frame_text,
        "frame_listing_sha256": hashlib.sha256(
            frame_text.encode("utf-8")
        ).hexdigest(),
        "integrity_test": {
            "exit_code": integrity["exit_code"],
            "stderr": integrity["stderr"],
        },
        "decompression": {
            key: decompression[key]
            for key in (
                "exit_code",
                "wall_seconds",
                "user_cpu_seconds",
                "system_cpu_seconds",
            )
        },
        "recovered_binding": recovered_binding,
        "byte_identical_to_author_lrat": True,
        "recompression": {
            key: recompression[key]
            for key in (
                "exit_code",
                "wall_seconds",
                "user_cpu_seconds",
                "system_cpu_seconds",
            )
        },
        "recompressed_binding": recompressed_binding,
        "byte_identical_recompression": True,
    }


PRIVATE_RELATIVE_FILES = [
    "certificates/order12_k4_doublelex_seed0_lrat_publication/README.md",
    (
        "certificates/order12_k4_doublelex_seed0_lrat_publication/"
        "proof.converted.lrat.zst"
    ),
    (
        "certificates/order12_k4_doublelex_seed0_lrat_publication/"
        "publication-manifest.json"
    ),
    (
        "certificates/order12_k4_doublelex_seed0_lrat_publication/"
        "verify_publication.py"
    ),
    "instances/order12_k4_connected_doublelex/instance.cnf",
    "tools/drat_trim_2023_05_22/lrat-check",
    "certificates/order12_k4_doublelex_seed0_lrat/certificate.json",
    "certificates/order12_k4_doublelex_seed0_lrat/artifact-manifest.json",
    "reviews/order12_k4_doublelex_lrat_hostile_0814a4f4/REVIEW.md",
    (
        "reviews/order12_k4_doublelex_lrat_hostile_0814a4f4/"
        "hostile-evidence.json"
    ),
]


def populate_private_campaign(private_campaign: Path) -> None:
    for relative in PRIVATE_RELATIVE_FILES:
        source = CAMPAIGN / relative
        destination = private_campaign / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        shutil.copymode(source, destination)
        regular_single_link(destination, f"private copy {relative}")


def private_verifier_command(private_campaign: Path) -> list[str]:
    return [
        sys.executable,
        str(
            private_campaign
            / "certificates/order12_k4_doublelex_seed0_lrat_publication/"
            "verify_publication.py"
        ),
    ]


def run_private_verifier(
    private_campaign: Path, *, path_override: str | None = None
) -> dict[str, object]:
    env = {
        "HOME": os.environ.get("HOME", ""),
        "LANG": "C",
        "LC_ALL": "C",
        "PATH": path_override
        if path_override is not None
        else os.environ.get("PATH", ""),
        "PYTHONHASHSEED": "0",
        "TMPDIR": str(private_campaign.parent),
    }
    return run_command(
        private_verifier_command(private_campaign),
        cwd=private_campaign,
        timeout=600,
        env=env,
    )


def validate_successful_verifier(run: dict[str, object]) -> dict[str, object]:
    require(
        run["exit_code"] == 0
        and not run["timed_out"]
        and run["stderr"] == "",
        f"clean private verifier failed: {run!r}",
    )
    stdout = str(run["stdout"])
    require(stdout.endswith("\n"), "verifier stdout lacks terminal newline")
    lines = stdout.splitlines()
    require(len(lines) == 1, f"verifier stdout is not one JSON line: {lines!r}")
    try:
        payload = json.loads(
            lines[0],
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
        )
    except json.JSONDecodeError as error:
        raise AuditError(f"verifier stdout is malformed JSON: {error}") from error
    require(
        isinstance(payload, dict)
        and set(payload)
        == {
            "bindings",
            "claim_boundary",
            "lrat_check",
            "recovered_lrat",
            "schema",
            "verdict",
        },
        "verifier success payload schema mismatch",
    )
    require(
        payload["schema"]
        == "gamma-theta-doublelex-publication-verifier-v2"
        and payload["verdict"]
        == "VERIFIED_EXACT_DOUBLELEX_CNF_UNSAT_ONLY",
        "verifier schema/verdict mismatch",
    )
    require(
        payload["claim_boundary"]
        == (
            "This verifies UNSAT only for the exact DoubleLex CNF. "
            "Transfer to graphs uses the separately reviewed "
            "C-037/C-045 implication."
        ),
        "verifier claim boundary mismatch",
    )
    require(
        payload["recovered_lrat"]["sha256"] == LRAT_SHA256
        and payload["recovered_lrat"]["size_bytes"] == LRAT_SIZE,
        "verifier recovered-LRAT binding mismatch",
    )
    require(
        payload["lrat_check"]
        == {
            "exit_code": 0,
            "verified_marker_count": 1,
            "stderr_bytes": 0,
        },
        "verifier checker-result record mismatch",
    )
    return payload


def mutate_one_byte(path: Path) -> None:
    payload = bytearray(path.read_bytes())
    require(bool(payload), f"cannot mutate empty file {path}")
    position = len(payload) // 2
    payload[position] ^= 1
    path.write_bytes(payload)


def restore_private_file(private_campaign: Path, relative: str) -> Path:
    source = CAMPAIGN / relative
    destination = private_campaign / relative
    if destination.exists() or destination.is_symlink():
        destination.unlink()
    shutil.copyfile(source, destination)
    shutil.copymode(source, destination)
    return destination


def require_rejection(
    label: str, run: dict[str, object]
) -> dict[str, object]:
    stderr = str(run["stderr"])
    stdout = str(run["stdout"])
    require(
        run["exit_code"] == 1
        and not run["timed_out"]
        and stdout == ""
        and stderr.startswith("REJECTED: "),
        f"mutation {label} was not rejected fail-closed: {run!r}",
    )
    return {
        "label": label,
        "expected": "REJECT",
        "observed_exit_code": run["exit_code"],
        "observed_stdout": stdout,
        "observed_stderr": stderr,
        "passed": True,
    }


def decisive_mutation_probes(
    private_campaign: Path,
) -> list[dict[str, object]]:
    probes: list[dict[str, object]] = []
    relative_targets = [
        (
            "formula_one_byte",
            "instances/order12_k4_connected_doublelex/instance.cnf",
        ),
        (
            "compressed_lrat_one_byte",
            (
                "certificates/order12_k4_doublelex_seed0_lrat_publication/"
                "proof.converted.lrat.zst"
            ),
        ),
        (
            "checker_one_byte",
            "tools/drat_trim_2023_05_22/lrat-check",
        ),
        (
            "author_certificate_one_byte",
            "certificates/order12_k4_doublelex_seed0_lrat/certificate.json",
        ),
        (
            "author_manifest_one_byte",
            (
                "certificates/order12_k4_doublelex_seed0_lrat/"
                "artifact-manifest.json"
            ),
        ),
        (
            "hostile_review_one_byte",
            "reviews/order12_k4_doublelex_lrat_hostile_0814a4f4/REVIEW.md",
        ),
        (
            "hostile_evidence_one_byte",
            (
                "reviews/order12_k4_doublelex_lrat_hostile_0814a4f4/"
                "hostile-evidence.json"
            ),
        ),
    ]
    for label, relative in relative_targets:
        target = restore_private_file(private_campaign, relative)
        mutate_one_byte(target)
        probes.append(
            require_rejection(label, run_private_verifier(private_campaign))
        )
        restore_private_file(private_campaign, relative)

    formula_relative = (
        "instances/order12_k4_connected_doublelex/instance.cnf"
    )
    formula = restore_private_file(private_campaign, formula_relative)
    formula.unlink()
    formula.symlink_to(FORMULA)
    probes.append(
        require_rejection(
            "formula_symlink", run_private_verifier(private_campaign)
        )
    )
    restore_private_file(private_campaign, formula_relative)

    formula = restore_private_file(private_campaign, formula_relative)
    sibling = formula.with_name("instance.hardlink.cnf")
    if sibling.exists():
        sibling.unlink()
    os.link(formula, sibling)
    probes.append(
        require_rejection(
            "formula_multiple_hard_links",
            run_private_verifier(private_campaign),
        )
    )
    sibling.unlink()
    restore_private_file(private_campaign, formula_relative)

    compressed_relative = (
        "certificates/order12_k4_doublelex_seed0_lrat_publication/"
        "proof.converted.lrat.zst"
    )
    compressed = restore_private_file(private_campaign, compressed_relative)
    with compressed.open("r+b") as stream:
        stream.truncate(COMPRESSED_SIZE - 1)
    probes.append(
        require_rejection(
            "compressed_lrat_truncated",
            run_private_verifier(private_campaign),
        )
    )
    restore_private_file(private_campaign, compressed_relative)

    probes.append(
        require_rejection(
            "zstd_absent_from_path",
            run_private_verifier(
                private_campaign, path_override="/usr/bin:/bin"
            ),
        )
    )
    return probes


def metadata_mutation_probes(
    private_campaign: Path,
) -> list[dict[str, object]]:
    probes: list[dict[str, object]] = []
    manifest_relative = (
        "certificates/order12_k4_doublelex_seed0_lrat_publication/"
        "publication-manifest.json"
    )
    manifest = restore_private_file(private_campaign, manifest_relative)
    payload = manifest.read_text(encoding="utf-8")
    old = '"schema_version": 1'
    new = '"schema_version": 2'
    require(old in payload and len(old) == len(new), "manifest mutation setup failed")
    manifest.write_text(payload.replace(old, new, 1), encoding="utf-8")
    run = run_private_verifier(private_campaign)
    probes.append(
        require_rejection(
            "publication_manifest_schema_version_one_byte", run
        )
    )
    restore_private_file(private_campaign, manifest_relative)

    readme_relative = (
        "certificates/order12_k4_doublelex_seed0_lrat_publication/README.md"
    )
    readme = restore_private_file(private_campaign, readme_relative)
    mutate_one_byte(readme)
    run = run_private_verifier(private_campaign)
    probes.append(require_rejection("readme_one_byte", run))
    restore_private_file(private_campaign, readme_relative)
    return probes


def audit_private_verifier(work: Path) -> dict[str, object]:
    private_campaign = work / "private-campaign"
    populate_private_campaign(private_campaign)
    clean_run = run_private_verifier(private_campaign)
    clean_payload = validate_successful_verifier(clean_run)
    decisive_probes = decisive_mutation_probes(private_campaign)
    metadata_probes = metadata_mutation_probes(private_campaign)
    return {
        "private_layout_file_count": len(PRIVATE_RELATIVE_FILES),
        "clean_run": {
            key: clean_run[key]
            for key in (
                "exit_code",
                "timed_out",
                "wall_seconds",
                "user_cpu_seconds",
                "system_cpu_seconds",
                "maximum_resident_set_size_raw",
                "stdout",
                "stderr",
            )
        },
        "clean_payload": clean_payload,
        "decisive_mutation_probes": decisive_probes,
        "metadata_mutation_probes": metadata_probes,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    output = arguments.output.resolve()
    require(
        output.parent == REVIEW_DIR,
        "evidence output must be directly inside the review directory",
    )
    require(
        not output.exists() and not output.is_symlink(),
        "refuse to overwrite hostile evidence",
    )

    started_ns = time.time_ns()
    v1_snapshot_initial = audit_v1_frozen()
    initial_snapshot = audit_target_inventory()
    manifest_audit = audit_manifest()
    accepted_bindings = audit_accepted_bindings()

    with tempfile.TemporaryDirectory(
        prefix="gamma-theta-doublelex-publication-hostile-"
    ) as temporary:
        work = Path(temporary)
        zstd_audit = audit_zstd_and_recovery(work)
        verifier_audit = audit_private_verifier(work)

    final_snapshot = audit_target_inventory()
    v1_snapshot_final = audit_v1_frozen()
    require(
        initial_snapshot == final_snapshot,
        "frozen publication target changed during hostile audit",
    )
    require(
        v1_snapshot_initial == v1_snapshot_final,
        "frozen V1 publication review changed during V2 audit",
    )
    evidence = {
        "schema": (
            "gamma-theta-order12-k4-doublelex-publication-hostile-evidence-v2"
        ),
        "schema_version": 2,
        "started_unix_ns": started_ns,
        "finished_unix_ns": time.time_ns(),
        "target_package": {
            "path": str(PACKAGE.resolve()),
            "snapshot": final_snapshot,
        },
        "v1_review_unchanged": v1_snapshot_final,
        "manifest_audit": manifest_audit,
        "accepted_bindings": accepted_bindings,
        "zstd_and_recovery": zstd_audit,
        "private_verifier": verifier_audit,
        "no_sat_solver_invoked": True,
        "claim_boundary": (
            "The compact package faithfully carries the already accepted LRAT "
            "certificate for UNSAT of the exact DoubleLex CNF only. This audit "
            "does not prove the graph-to-CNF transfer, exclude the connected "
            "(12,4) slice by itself, or resolve the universal conjecture."
        ),
        "verdict": (
            "ACCEPT_EXACT_DOUBLELEX_CNF_UNSAT_PUBLICATION_PACKAGE_V2_ONLY"
        ),
        "defects": [],
    }
    output.write_bytes(canonical_json_bytes(evidence))
    regular_single_link(output, "hostile evidence output")
    print(
        json.dumps(
            {
                "evidence": str(output),
                "evidence_sha256": sha256_file(output),
                "target_inventory_sha256": final_snapshot[
                    "inventory_sha256"
                ],
                "verdict": evidence["verdict"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (
        AuditError,
        OSError,
        subprocess.SubprocessError,
        UnicodeError,
        ValueError,
    ) as error:
        print(f"REJECTED: {error}", file=sys.stderr)
        raise SystemExit(1)

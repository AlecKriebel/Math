#!/usr/bin/env python3
"""Postcommit binding audit for the hole5 S6 signature breaker.

This probe binds author bytes to Git commit 10acf379, independently rebuilds
the comparator stream and strengthened CNF, and then compares those bytes with
the frozen author's pure routines.  It performs no SAT solve.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Sequence


SCHEMA = "gamma-theta-hole5-signature-implementation-binding-v1"
BINDING_COMMIT = "10acf379329411d9d05267b3411d6703047e705e"
CAMPAIGN_RELATIVE = Path("gamma_theta_eternal_domination")
EXPECTED_SOURCE_CNF_SHA256 = (
    "76bf36ecb663cd37272acded2208206fdba6aa571dd5f2e757cc132bd533e0b7"
)
EXPECTED_INDEPENDENT_STREAM_SHA256 = (
    "ddd32969558030c22b7b4f182dfd9f96b65bb572a7e240957d202fb32b0158c6"
)
EXPECTED_BREAKER_JSON_SHA256 = (
    "62ce8f60ecfe74f58bcd113166009637f854d7d663aea2e59395ae224682d18a"
)
EXPECTED_DERIVED_CNF_SHA256 = (
    "c6a0811c718ff8e9352f253e4ce225ce2826def9c3e4a9cd55f0b0152703d104"
)
EXPECTED_PRIOR_PROBE_SHA256 = (
    "3515adc846e961738b86c572a90aa0f42945cfa6794e3700986c392999c4ab66"
)
EXPECTED_PRIOR_LOG_SHA256 = (
    "f1d8f6d8d6f85bdffadcf39e5d4c4504b9cf0d1b8a609d8e5fe540523091b9de"
)

BOUND_PATHS = {
    "author_source": {
        "path": (
            "gamma_theta_eternal_domination/src/synthesis_k3/"
            "hole5_signature_breaker.py"
        ),
        "blob_oid": "a793e0f4d119be44b142a98824ceaeafbe06037c",
        "sha256": (
            "cc1dc4249dc20f78e8eff4de14ffdca632da1e9455a381000786faa28c950c77"
        ),
        "size": 34_324,
    },
    "theorem_note": {
        "path": (
            "gamma_theta_eternal_domination/math/lemmas/"
            "hole5_signature_symmetry.md"
        ),
        "blob_oid": "45cfb9e22774de4c2d1d491b33f52ea85944f1d6",
        "sha256": (
            "8f8192774c3de65c2468115cc2d4aadd392fa7a1f73261c23fa49886d9c183e8"
        ),
        "size": 6_044,
    },
    "author_tests": {
        "path": (
            "gamma_theta_eternal_domination/tests/"
            "test_hole5_signature_breaker.py"
        ),
        "blob_oid": "74806aade5e467b8466ce404be6204c3db797839",
        "sha256": (
            "cd73ae2275d1d08363a1ed7db5990ad294952270e449d5cec8229312d738a892"
        ),
        "size": 10_503,
    },
    "author_validation_log": {
        "path": (
            "gamma_theta_eternal_domination/results/logs/"
            "hole5-signature-breaker-validation.json"
        ),
        "blob_oid": "79dfdc73c37d7a73b85c1afa11c2fbd1916c21a5",
        "sha256": (
            "dafe1cdfe66bac034e71faaa0ba3f157fc88b21a317cbd6cba5f62e598f6d442"
        ),
        "size": 4_987,
    },
    "independent_probe": {
        "path": (
            "gamma_theta_eternal_domination/reviews/"
            "hole5_signature_symmetry_hostile_probe.py"
        ),
        "blob_oid": "fb9fe1bed9301184bcc294215cd83b6e5be00dc5",
        "sha256": EXPECTED_PRIOR_PROBE_SHA256,
        "size": 42_662,
    },
    "independent_log": {
        "path": (
            "gamma_theta_eternal_domination/reviews/"
            "hole5_signature_symmetry_hostile_probe_log.json"
        ),
        "blob_oid": "f06bbaa61b901e493a7bedf164159e3e88f6d7f1",
        "sha256": EXPECTED_PRIOR_LOG_SHA256,
        "size": 14_910,
    },
    "independent_review": {
        "path": (
            "gamma_theta_eternal_domination/reviews/"
            "hole5_signature_symmetry_hostile_review.md"
        ),
        "blob_oid": "5366848a25e72d504d2075c1408f55565fe55062",
        "sha256": (
            "169b99e083fe2079b3957de3095591142162aca76a10b42f9bb61266775ef223"
        ),
        "size": 11_237,
    },
}


class BindingFailure(ValueError):
    """One supposedly frozen implementation binding failed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise BindingFailure(message)


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def git_blob_oid(payload: bytes) -> str:
    header = f"blob {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()


def canonical_json(value: object) -> bytes:
    return (
        json.dumps(value, allow_nan=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def repository_root() -> Path:
    source = Path(__file__).resolve()
    for ancestor in source.parents:
        if (ancestor / ".git").exists():
            return ancestor
    raise BindingFailure("cannot locate repository root")


def git(repo: Path, *arguments: str) -> bytes:
    result = subprocess.run(
        ("git", *arguments),
        cwd=repo,
        check=False,
        capture_output=True,
    )
    require(
        result.returncode == 0,
        f"git {' '.join(arguments)} failed: "
        f"{result.stderr.decode('utf-8', 'replace')}",
    )
    return result.stdout


def bind_git_paths(repo: Path) -> dict[str, object]:
    resolved_commit = git(
        repo, "rev-parse", f"{BINDING_COMMIT}^{{commit}}"
    ).decode("ascii").strip()
    require(resolved_commit == BINDING_COMMIT, "binding commit changed")
    bindings: dict[str, object] = {}
    for role, expected in BOUND_PATHS.items():
        path = expected["path"]
        require(type(path) is str, f"{role}: malformed path constant")
        actual_oid = git(
            repo,
            "rev-parse",
            f"{BINDING_COMMIT}:{path}",
        ).decode("ascii").strip()
        require(
            actual_oid == expected["blob_oid"],
            f"{role}: Git blob OID mismatch",
        )
        object_payload = git(repo, "cat-file", "blob", actual_oid)
        working_payload = (repo / path).read_bytes()
        require(
            object_payload == working_payload,
            f"{role}: working tree differs from bound Git bytes",
        )
        require(
            git_blob_oid(object_payload) == actual_oid,
            f"{role}: independently computed blob OID mismatch",
        )
        require(
            len(object_payload) == expected["size"],
            f"{role}: byte size mismatch",
        )
        require(
            sha256(object_payload) == expected["sha256"],
            f"{role}: SHA-256 mismatch",
        )
        bindings[role] = {
            "path": path,
            "git_blob_oid_sha1": actual_oid,
            "git_object_size_bytes": len(object_payload),
            "git_object_sha256": sha256(object_payload),
            "working_tree_size_bytes": len(working_payload),
            "working_tree_sha256": sha256(working_payload),
            "working_tree_byte_identical_to_git_object": True,
        }
    return bindings


def independent_edge_variables() -> dict[tuple[int, int], int]:
    return {
        edge: index
        for index, edge in enumerate(
            itertools.combinations(range(12), 2),
            start=1,
        )
    }


def independent_comparator_stream() -> tuple[bytes, int, int]:
    edge = independent_edge_variables()
    clauses: list[tuple[int, ...]] = []
    for left_vertex, right_vertex in zip(range(6, 11), range(7, 12)):
        left = tuple(edge[(core, left_vertex)] for core in range(6))
        right = tuple(edge[(core, right_vertex)] for core in range(6))
        for pivot in range(6):
            for prefix in itertools.product((False, True), repeat=pivot):
                clause: list[int] = []
                for index, bit in enumerate(prefix):
                    if bit:
                        clause.extend((-left[index], -right[index]))
                    else:
                        clause.extend((left[index], right[index]))
                clause.extend((-left[pivot], right[pivot]))
                clauses.append(tuple(clause))
    require(len(clauses) == 315, "independent clause count mismatch")
    literal_count = sum(map(len, clauses))
    require(literal_count == 3_210, "independent literal count mismatch")
    stream = b"".join(
        (" ".join(map(str, clause)) + " 0\n").encode("ascii")
        for clause in clauses
    )
    require(
        sha256(stream) == EXPECTED_INDEPENDENT_STREAM_SHA256,
        "independent comparator stream changed",
    )
    return stream, len(clauses), literal_count


def parse_dimacs_counts(payload: bytes) -> dict[str, int]:
    variable_count: int | None = None
    declared_clauses: int | None = None
    clause_count = 0
    literal_count = 0
    for line in payload.splitlines():
        if not line or line.startswith(b"c"):
            continue
        fields = line.split()
        if fields[0] == b"p":
            require(
                len(fields) == 4 and fields[1] == b"cnf",
                "malformed DIMACS header",
            )
            require(variable_count is None, "multiple DIMACS headers")
            variable_count = int(fields[2])
            declared_clauses = int(fields[3])
            continue
        require(variable_count is not None, "clause precedes DIMACS header")
        literals = tuple(map(int, fields))
        require(literals and literals[-1] == 0, "clause lacks final zero")
        require(0 not in literals[:-1], "internal DIMACS zero")
        require(
            all(abs(literal) <= variable_count for literal in literals[:-1]),
            "DIMACS variable exceeds header",
        )
        clause_count += 1
        literal_count += len(literals) - 1
    require(variable_count is not None, "DIMACS header missing")
    require(clause_count == declared_clauses, "DIMACS clause count mismatch")
    return {
        "variables": variable_count,
        "clauses": clause_count,
        "literals": literal_count,
    }


def run_prior_probe(repo: Path) -> dict[str, object]:
    probe_path = repo / BOUND_PATHS["independent_probe"]["path"]
    log_path = repo / BOUND_PATHS["independent_log"]["path"]
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        (sys.executable, "-B", str(probe_path)),
        cwd=repo,
        env=environment,
        check=False,
        capture_output=True,
    )
    require(result.returncode == 0, "independent hostile probe failed")
    require(not result.stderr, "independent hostile probe wrote stderr")
    retained_log = log_path.read_bytes()
    require(
        result.stdout == retained_log,
        "independent hostile probe output differs from retained log",
    )
    value = json.loads(result.stdout)
    require(
        value["verdict"] == "ACCEPT_SIGNATURE_BREAKER_REJECT_SHORTCUTS",
        "independent hostile verdict changed",
    )
    checks = value["s6_invariance"]["checks"]
    require(len(checks) == 5, "independent covariance count changed")
    require(
        all(
            check["full_cnf_multiset"]["equal"] is True
            and check["base_cnf_multiset"]["equal"] is True
            and check["bank_cnf_multiset"]["equal"] is True
            for check in checks
        ),
        "independent covariance check failed",
    )
    require(
        value["signature_comparator"]["dimacs_clause_stream_sha256"]
        == EXPECTED_INDEPENDENT_STREAM_SHA256,
        "retained independent stream binding changed",
    )
    return {
        "probe_exit_code": result.returncode,
        "stdout_byte_identical_to_retained_log": True,
        "verdict": value["verdict"],
        "covariance_generators_checked": len(checks),
        "comparator_assignments_checked": sum(
            row["assignment_count"]
            for row in value["signature_comparator"]["adjacent_pair_checks"]
        ),
        "comparator_semantic_mismatches": sum(
            row["semantic_mismatch_count"]
            for row in value["signature_comparator"]["adjacent_pair_checks"]
        ),
    }


def run() -> dict[str, object]:
    repo = repository_root()
    campaign = repo / CAMPAIGN_RELATIVE
    bindings = bind_git_paths(repo)
    prior = run_prior_probe(repo)

    # Import only after the Git-object/working-tree identity gates pass.
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(campaign / "src"))
    from synthesis_k3 import hole5_signature_breaker as author

    source_package = (
        campaign / "results/synthesis_k3_template_bank_packages/hole5"
    )
    source_path = source_package / "instance.cnf"
    source_payload = source_path.read_bytes()
    require(
        sha256(source_payload) == EXPECTED_SOURCE_CNF_SHA256,
        "source CNF hash mismatch",
    )

    independent_stream, independent_clause_count, independent_literal_count = (
        independent_comparator_stream()
    )
    author_clauses = author.signature_breaker_clauses()
    author_stream = author.breaker_clause_stream_bytes(author_clauses)
    require(
        author_stream == independent_stream,
        "author comparator stream differs byte-for-byte",
    )
    author_breaker_json = author.breaker_payload_bytes()
    require(
        sha256(author_breaker_json) == EXPECTED_BREAKER_JSON_SHA256,
        "author breaker JSON hash mismatch",
    )

    author_derived = author._derive_cnf_bytes(source_payload, author_clauses)
    source_header, source_body = source_payload.split(b"\n", 1)
    independent_derived = b"p cnf 6886 23968\n" + source_body + independent_stream
    require(
        author_derived == independent_derived,
        "author and independent derived CNF bytes differ",
    )
    require(
        sha256(author_derived) == EXPECTED_DERIVED_CNF_SHA256,
        "derived CNF hash mismatch",
    )
    derived_header, derived_body = author_derived.split(b"\n", 1)
    require(
        derived_body[: len(source_body)] == source_body,
        "derived CNF does not retain the exact source body prefix",
    )
    require(
        derived_body[len(source_body) :] == independent_stream,
        "derived CNF suffix differs from independent comparator stream",
    )
    source_counts = parse_dimacs_counts(source_payload)
    derived_counts = parse_dimacs_counts(author_derived)
    require(
        source_counts
        == {"variables": 6_886, "clauses": 23_653, "literals": 188_959},
        "source formula counts mismatch",
    )
    require(
        derived_counts
        == {"variables": 6_886, "clauses": 23_968, "literals": 192_169},
        "derived formula counts mismatch",
    )

    resolved_source, source_report, parsed_source = (
        author._validate_source_identity(source_package, exhaustive=True)
    )
    require(resolved_source == source_package.resolve(), "source path changed")
    require(source_report["bank_count"] == 3_645, "source bank audit changed")
    comparator_report = author.exhaustive_comparator_audit()
    covariance_report = author.covariance_audit(parsed_source)
    expected_generators = [[6, 7], [7, 8], [8, 9], [9, 10], [10, 11]]
    require(
        comparator_report["total_assignments_checked"] == 20_480,
        "author comparator audit count mismatch",
    )
    require(
        covariance_report["generator_count"] == 5
        and covariance_report["generator_transpositions_checked"]
        == expected_generators,
        "author covariance audit mismatch",
    )

    validation = json.loads(
        (repo / BOUND_PATHS["author_validation_log"]["path"]).read_bytes()
    )
    require(
        validation["author_artifacts"]["generator"]["sha256"]
        == BOUND_PATHS["author_source"]["sha256"],
        "validation log source binding mismatch",
    )
    require(
        validation["author_artifacts"]["theorem_note"]["sha256"]
        == BOUND_PATHS["theorem_note"]["sha256"],
        "validation log note binding mismatch",
    )
    require(
        validation["author_artifacts"]["tests"]["sha256"]
        == BOUND_PATHS["author_tests"]["sha256"],
        "validation log test binding mismatch",
    )
    require(
        validation["formula"]["signature_breaker"][
            "header_free_dimacs_stream_sha256"
        ]
        == EXPECTED_INDEPENDENT_STREAM_SHA256,
        "validation log stream binding mismatch",
    )
    require(
        validation["formula"]["derived_cnf_sha256"]
        == EXPECTED_DERIVED_CNF_SHA256,
        "validation log derived-CNF binding mismatch",
    )

    probe_path = Path(__file__).resolve()
    return {
        "schema": SCHEMA,
        "verdict": "ACCEPT_POSTCOMMIT_IMPLEMENTATION_BINDING",
        "claim_boundary": {
            "sat_solver_run": False,
            "hole5_sat_claim": False,
            "hole5_unsat_claim": False,
            "audit_scope": "formula-generation-and-symmetry-implementation",
        },
        "binding_commit": BINDING_COMMIT,
        "git_object_bindings": bindings,
        "binding_probe": {
            "path": str(probe_path.relative_to(repo)),
            "sha256": sha256(probe_path.read_bytes()),
        },
        "independent_hostile_probe_replay": prior,
        "comparator_stream": {
            "author_byte_identical_to_independent": True,
            "clause_count": independent_clause_count,
            "literal_count": independent_literal_count,
            "size_bytes": len(independent_stream),
            "sha256": sha256(independent_stream),
            "author_breaker_json_size_bytes": len(author_breaker_json),
            "author_breaker_json_sha256": sha256(author_breaker_json),
        },
        "derived_cnf": {
            "author_byte_identical_to_independent": True,
            "source_header": source_header.decode("ascii"),
            "derived_header": derived_header.decode("ascii"),
            "source_body_exact_prefix": True,
            "source_body_size_bytes": len(source_body),
            "source_body_sha256": sha256(source_body),
            "appended_suffix_exactly_independent_stream": True,
            "size_bytes": len(author_derived),
            "sha256": sha256(author_derived),
            "source_counts": source_counts,
            "derived_counts": derived_counts,
        },
        "author_pure_audits": {
            "source_exhaustive_oracle_checked": True,
            "source_bank_rows_checked": source_report["bank_count"],
            "comparator_report": comparator_report,
            "covariance_report": covariance_report,
        },
        "author_validation_log_cross_check": {
            "author_hashes_match_git_objects": True,
            "comparator_stream_hash_matches": True,
            "derived_cnf_hash_matches": True,
            "recorded_claim_status": validation["claim_status"],
        },
    }


def main() -> int:
    try:
        result = run()
    except (
        BindingFailure,
        OSError,
        ValueError,
        KeyError,
        subprocess.SubprocessError,
    ) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    sys.stdout.buffer.write(canonical_json(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

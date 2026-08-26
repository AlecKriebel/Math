#!/usr/bin/env python3
"""Isolated mutations for the integrated K3P-SAME classification gate."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
VERIFIER = HERE / "verify_k3p_same_classification.py"
OUTPUT = HERE / "K3P_SAME_CLASSIFICATION_MUTATION_REPORT.json"
EXCLUDED_PARTS = {
    ".venv", "__pycache__", "manuscript", "supplement", "submission",
    "release", "history", "logs", "pointwise_algebra",
}


class MutationFailure(RuntimeError):
    pass


def require(condition: bool, message: object) -> None:
    if not condition:
        raise MutationFailure(str(message))


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def sha_object(value: object) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".mutation-tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def reseal(path: Path, value: dict, exclude: tuple[str, ...] = ()) -> None:
    value.pop("payload_sha256", None)
    body = dict(value)
    for field in exclude:
        body.pop(field, None)
    value["payload_sha256"] = sha_object(body)
    atomic_write(path, value)


def mutate_json(root: Path, relative: str, mutate, reseal_payload: bool = False,
                exclude: tuple[str, ...] = ()) -> dict:
    path = root / relative
    value = json.loads(path.read_text())
    mutate(value)
    if reseal_payload:
        reseal(path, value, exclude)
    else:
        atomic_write(path, value)
    return value


def hardlink_bundle(target: Path) -> None:
    for source in PROJECT.rglob("*"):
        relative = source.relative_to(PROJECT)
        if any(part in EXCLUDED_PARTS for part in relative.parts):
            continue
        if not source.is_file():
            continue
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.link(source, destination)
        except OSError:
            shutil.copy2(source, destination)


def run_gate(root: Path, optimized: bool = False) -> subprocess.CompletedProcess[str]:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend([
        str(VERIFIER), "--project-root", str(root), "--artifact-only",
        "--no-write-report",
    ])
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        command, cwd=PROJECT, env=environment, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
        timeout=120,
    )


def case(name: str, expected: str, mutation) -> dict:
    with tempfile.TemporaryDirectory(prefix="k3p-same-mutation-") as directory:
        root = Path(directory) / "project"
        root.mkdir()
        hardlink_bundle(root)
        mutation(root)
        result = run_gate(root)
        require(result.returncode != 0, ("mutation survived", name, result.stdout[-2000:]))
        require(expected in result.stdout,
                ("wrong failure class", name, expected, result.stdout[-2000:]))
        return {
            "name": name,
            "expected_failure_class": expected,
            "diagnostic_observed": True,
            "exit_code": result.returncode,
            "status": "REJECTED",
        }


def rebind_h14(root: Path, mutate) -> None:
    relative = "triangle_h14/K3P_H14_CONTEXT_CERTIFICATE.json"
    h14 = mutate_json(root, relative, mutate, True)
    manifest_relative = "global_infrastructure/GLOBAL_INFRASTRUCTURE_MANIFEST.json"
    manifest_path = root / manifest_relative
    manifest = json.loads(manifest_path.read_text())
    record = manifest["artifacts"][relative]
    record["sha256"] = sha_file(root / relative)
    record["payload_sha256"] = h14["payload_sha256"]
    record["schema"] = h14["schema"]
    reseal(manifest_path, manifest)


def rebind_probe_restoration(root: Path, mutate) -> None:
    mutate_json(root, "probes/RESTORATION_MANIFEST.json", mutate, True)


def restoration_mutation_report(root: Path) -> None:
    relative = "restoration/K3P_RESTORATION_MUTATION_CERTIFICATE.json"
    mutation = mutate_json(
        root, relative,
        lambda x: (x.__setitem__("mutation_count", 19),
                   x.__setitem__("rejected", 19), x.__setitem__("accepted", 1)),
        True,
    )
    probe_path = root / "probes/RESTORATION_MANIFEST.json"
    probe = json.loads(probe_path.read_text())
    record = probe["standalone_k3p_restoration"]["mutation_certificate"]
    record.update({
        "sha256": sha_file(root / relative),
        "payload_sha256": mutation["payload_sha256"],
        "mutation_count": 19,
        "rejected": 19,
    })
    reseal(probe_path, probe)


def main() -> int:
    require(__debug__ and not sys.flags.optimize, "optimized Python forbidden")
    clean = run_gate(PROJECT)
    require(clean.returncode == 0 and "K3P_SAME_CLASSIFICATION_GATE_PASS" in clean.stdout,
            ("clean artifact gate", clean.stdout[-3000:]))

    cases = [
        case(
            "substitute_universal_pointwise_cut_rank_iff",
            "claim-lock cut boundary",
            lambda root: mutate_json(
                root, "FINAL_CLAIM_LOCK.json",
                lambda x: x["cut_transfer"].__setitem__(
                    "universal_arbitrary_network_pointwise_cut_rank_iff", "ACTIVE_USED"
                ),
            ),
        ),
        case(
            "promote_ordinary_triangle_to_rank_15",
            "triangle orientation ranks",
            lambda root: rebind_h14(
                root, lambda x: x["orientations"]["1"].__setitem__("rank", 15)
            ),
        ),
        case(
            "claim_ambient_open_triangle_germ",
            "ambient-rank-15 triangle sufficiency rejected",
            lambda root: rebind_h14(
                root, lambda x: x.__setitem__("ambient_open_triangle_germ", True)
            ),
        ),
        case(
            "allow_proper_directed_containment_inside_strong_class",
            "proper directed containment inside strong class rejected",
            lambda root: mutate_json(
                root, "FINAL_CLAIM_LOCK.json",
                lambda x: x["classification"].__setitem__(
                    "proper_one_sided_containment_in_strong_class", True
                ),
            ),
        ),
        case(
            "drop_coherent_boundary_transports",
            "claim-lock triangle equivalence definition",
            lambda root: mutate_json(
                root, "FINAL_CLAIM_LOCK.json",
                lambda x: x["classification"]["triangle_equivalence"].__setitem__(
                    "coherent_boundary_transports_required", False
                ),
            ),
        ),
        case(
            "weaken_all_n_sharpness_nontriangle_scope",
            "claim-lock sharpness all-n scope",
            lambda root: mutate_json(
                root, "FINAL_CLAIM_LOCK.json",
                lambda x: x["sharpness"].__setitem__(
                    "all_n_nontriangle_equivalent", False
                ),
            ),
        ),
        case(
            "restore_pending_v1_probe_restoration_manifest",
            "RESTORATION_MANIFEST.json",
            lambda root: rebind_probe_restoration(
                root, lambda x: (x.__setitem__("schema", "k3p-restoration-manifest-v1"),
                                 x.__setitem__("status", "GRAPH_CONTRACT_PASS_K3P_ALGEBRA_PENDING"))
            ),
        ),
        case(
            "conflate_minimal_terminals_with_legacy_leaves",
            "stale restoration counts rejected",
            lambda root: rebind_probe_restoration(
                root, lambda x: x["restoration_count_distinctions"].__setitem__(
                    "minimal_k3p_terminal_rows", 36_792
                )
            ),
        ),
        case(
            "activate_legacy_restoration_continuation",
            "stale restoration counts rejected",
            lambda root: rebind_probe_restoration(
                root, lambda x: x["restoration_count_distinctions"].__setitem__(
                    "active_k3p_continuations", 1
                )
            ),
        ),
        case(
            "make_restoration_replay_import_producer",
            "probe restoration independence boundary",
            lambda root: rebind_probe_restoration(
                root, lambda x: x["standalone_k3p_restoration"]["independent_replay"].__setitem__(
                    "uses_producer_code", True
                )
            ),
        ),
        case(
            "reactivate_historical_k2p_restoration_algebra",
            "probe restoration independence boundary",
            lambda root: rebind_probe_restoration(
                root, lambda x: x["standalone_k3p_restoration"].__setitem__(
                    "uses_historical_k2p_algebra", True
                )
            ),
        ),
        case(
            "impose_k2p_sector_equality_in_restoration",
            "probe restoration independence boundary",
            lambda root: rebind_probe_restoration(
                root, lambda x: x["standalone_k3p_restoration"].__setitem__(
                    "uses_k2p_sector_equality", True
                )
            ),
        ),
        case(
            "drift_standalone_restoration_hash",
            "probe restoration binding",
            lambda root: rebind_probe_restoration(
                root, lambda x: x["standalone_k3p_restoration"]["manifest"].__setitem__(
                    "sha256", "0" * 64
                )
            ),
        ),
        case(
            "accept_restoration_mutation_and_reduce_count",
            "restoration 20 mutations",
            restoration_mutation_report,
        ),
        case(
            "delete_continuous_time_specialization_bridge",
            "continuous-time specialization bridge",
            lambda root: mutate_json(
                root, "FINAL_CLAIM_LOCK.json",
                lambda x: x.pop("continuous_time_specialization"),
            ),
        ),
        case(
            "reverse_ct_to_principal_necessity_transfer",
            "continuous-time specialization bridge",
            lambda root: mutate_json(
                root, "FINAL_CLAIM_LOCK.json",
                lambda x: x["continuous_time_specialization"].__setitem__(
                    "necessity_transfer",
                    "Every D3+ witness is a CT witness; no openness check is needed."
                ),
            ),
        ),
        case(
            "claim_submission_ready_without_publication_engineering",
            "publication overclaim rejected",
            lambda root: mutate_json(
                root, "FINAL_CLAIM_LOCK.json",
                lambda x: x["final_promotion"].__setitem__("submission_ready", True),
            ),
        ),
    ]

    optimized = run_gate(PROJECT, optimized=True)
    require(optimized.returncode != 0 and "optimized Python forbidden" in optimized.stdout,
            ("optimized gate survived", optimized.stdout[-2000:]))
    cases.append({
        "name": "optimized_python_bypass",
        "expected_failure_class": "optimized Python forbidden",
        "diagnostic_observed": True,
        "exit_code": optimized.returncode,
        "status": "REJECTED",
    })
    report = {
        "schema": "k3p-same-integrated-classification-mutations-v1",
        "status": "PASS",
        "clean_artifact_replay": "PASS",
        "mutation_count": len(cases),
        "rejected": len(cases),
        "survived": 0,
        "mutations": cases,
        "verifier_sha256": sha_file(VERIFIER),
    }
    report["payload_sha256"] = sha_object(report)
    atomic_write(OUTPUT, report)
    print("K3P_SAME_CLASSIFICATION_MUTATIONS_PASS")
    print(json.dumps({
        "status": "PASS", "mutations": len(cases), "rejected": len(cases),
        "payload_sha256": report["payload_sha256"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (MutationFailure, KeyError, IndexError, TypeError, ValueError,
            OSError, json.JSONDecodeError, subprocess.SubprocessError) as error:
        raise SystemExit(f"K3P_SAME_CLASSIFICATION_MUTATION_FAIL:{error}") from error

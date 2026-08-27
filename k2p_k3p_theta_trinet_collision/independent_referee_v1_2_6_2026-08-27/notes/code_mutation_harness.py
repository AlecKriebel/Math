#!/usr/bin/env python3
"""Independent hostile-mutation audit for referee packet v1.2.6.

This is referee-written code.  It never edits the packet: every executable
mutation is made in a fresh temporary copy.  The tests distinguish operative
rejections from allowed changes to fields that the supplied coverage inventory
explicitly classifies as informational.
"""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from typing import Callable


AUDIT_ROOT = Path(__file__).resolve().parents[1]
PACKET = (
    AUDIT_ROOT
    / "packet_copy"
    / "k2p-k3p-theta-ai-referee-v1.2.6"
)
MATERIALS = PACKET / "materials"

REJECTIONS = 0
EXPECTED_PASSES = 0


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"},
    )


def rejected(label: str, completed: subprocess.CompletedProcess[str], diagnostic: str | None = None) -> None:
    global REJECTIONS
    combined = completed.stdout + completed.stderr
    if completed.returncode == 0:
        raise AssertionError(f"mutation unexpectedly passed: {label}")
    if diagnostic is not None and diagnostic not in combined:
        raise AssertionError(
            f"{label} failed for a different reason; expected {diagnostic!r}\n{combined}"
        )
    REJECTIONS += 1
    print(f"[rejected] {label}")


def accepted(label: str, completed: subprocess.CompletedProcess[str]) -> None:
    global EXPECTED_PASSES
    if completed.returncode != 0:
        raise AssertionError(
            f"declared-informational mutation unexpectedly failed: {label}\n"
            + completed.stdout
            + completed.stderr
        )
    EXPECTED_PASSES += 1
    print(f"[informational pass] {label}")


def duplicate_first_key(raw: str) -> str:
    decoder = json.JSONDecoder(object_pairs_hook=lambda pairs: pairs)
    pairs = decoder.decode(raw)
    first_key = pairs[0][0]
    marker = f'"{first_key}":'
    if raw.count(marker) != 1:
        raise AssertionError(f"cannot uniquely duplicate {marker}")
    return raw.replace(marker, f'"{first_key}": null,\n  {marker}', 1)


def duplicate_nested_marker(raw: str, marker: str, duplicate: str) -> str:
    if raw.count(marker) != 1:
        raise AssertionError(f"nested marker is not unique: {marker!r}")
    return raw.replace(marker, duplicate + "\n" + marker, 1)


def strict_loader_tests() -> None:
    sys.path.insert(0, str(MATERIALS))
    from strict_json import load_canonical_certificate

    names = (
        "certificate_k2p_simple.json",
        "certificate_k2p_continuous_time.json",
        "certificate_k3p.json",
        "jacobian_certificate_k3p.json",
        "continuous_time_certificate_k3p.json",
    )
    deep_duplicate_specs = {
        "certificate_k2p_simple.json": (
            '"id": "rho",',
            '"id": "shadow",',
        ),
        "certificate_k2p_continuous_time.json": (
            '"id": "rho",',
            '"id": "shadow",',
        ),
        "certificate_k3p.json": (
            '"id": "rho",',
            '"id": "shadow",',
        ),
        "jacobian_certificate_k3p.json": (
            '"name": "e_rho_1.a_C",',
            '"name": "shadow",',
        ),
        "continuous_time_certificate_k3p.json": (
            '"parameter": "e_rho_1.a_C",',
            '"parameter": "shadow",',
        ),
    }
    for name in names:
        source = MATERIALS / name
        with tempfile.TemporaryDirectory(prefix="v126-raw-json-") as td:
            target = Path(td) / name
            target.write_text(duplicate_first_key(source.read_text(encoding="utf-8")), encoding="utf-8")
            try:
                load_canonical_certificate(target)
            except ValueError as exc:
                if "duplicate JSON object key" not in str(exc):
                    raise
            else:
                raise AssertionError(f"duplicate raw key passed: {name}")
            global REJECTIONS
            REJECTIONS += 1
            print(f"[rejected] duplicate raw key in {name}")

        marker, duplicate = deep_duplicate_specs[name]
        with tempfile.TemporaryDirectory(prefix="v126-deep-json-") as td:
            target = Path(td) / name
            target.write_text(
                duplicate_nested_marker(
                    source.read_text(encoding="utf-8"), marker, duplicate
                ),
                encoding="utf-8",
            )
            try:
                load_canonical_certificate(target)
            except ValueError as exc:
                if "duplicate JSON object key" not in str(exc):
                    raise
            else:
                raise AssertionError(f"deep duplicate raw key passed: {name}")
            REJECTIONS += 1
            print(f"[rejected] deep duplicate raw key in {name}")

        value = load_canonical_certificate(source)
        value["referee_unknown_field"] = True
        with tempfile.TemporaryDirectory(prefix="v126-schema-") as td:
            target = Path(td) / name
            target.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
            try:
                load_canonical_certificate(target)
            except ValueError as exc:
                if "closed JSON schema mismatch" not in str(exc):
                    raise
            else:
                raise AssertionError(f"unknown field passed: {name}")
            REJECTIONS += 1
            print(f"[rejected] unknown field in {name}")

    source = MATERIALS / "certificate_k2p_simple.json"
    raw = source.read_text(encoding="utf-8")
    for token in ("NaN", "Infinity", "-Infinity"):
        changed = raw.replace('"schema_version": "1.0"', f'"schema_version": {token}', 1)
        with tempfile.TemporaryDirectory(prefix="v126-constant-") as td:
            target = Path(td) / source.name
            target.write_text(changed, encoding="utf-8")
            try:
                load_canonical_certificate(target)
            except ValueError as exc:
                if "non-standard JSON numeric constant" not in str(exc):
                    raise
            else:
                raise AssertionError(f"nonstandard constant passed: {token}")
            REJECTIONS += 1
            print(f"[rejected] nonstandard constant {token}")

    changed = raw.replace('"schema_version": "1.0"', '"schema_version": 1e999', 1)
    with tempfile.TemporaryDirectory(prefix="v126-huge-exponent-") as td:
        target = Path(td) / source.name
        target.write_text(changed, encoding="utf-8")
        try:
            load_canonical_certificate(target)
        except ValueError as exc:
            if "closed JSON schema mismatch" not in str(exc):
                raise
        else:
            raise AssertionError("valid-JSON 1e999 type substitution passed")
        REJECTIONS += 1
        print("[rejected] valid-JSON huge exponent 1e999 by closed schema")


def simple_bundle() -> Path:
    td = Path(tempfile.mkdtemp(prefix="v126-simple-"))
    for name in ("strict_json.py", "verify_k2p_simple.py", "certificate_k2p_simple.json"):
        shutil.copy2(MATERIALS / name, td / name)
    return td


def run_simple_mutation(label: str, mutate: Callable[[dict], None], diagnostic: str | None = None) -> None:
    td = simple_bundle()
    cert_path = td / "certificate_k2p_simple.json"
    cert = json.loads(cert_path.read_text(encoding="utf-8"))
    mutate(cert)
    cert_path.write_text(json.dumps(cert, indent=2) + "\n", encoding="utf-8")
    rejected(label, run([sys.executable, "verify_k2p_simple.py"], td), diagnostic)
    shutil.rmtree(td)


def k2p_tests() -> None:
    for name in ("K", "K_odot_K", "U", "V", "S", "T"):
        run_simple_mutation(
            f"compact K2P network transition row {name}",
            lambda cert, name=name: cert["network_transition_probabilities"][name][0].__setitem__(0, "999"),
            f"{name} stored transition row",
        )
    for name in ("alpha", "beta", "gamma"):
        run_simple_mutation(
            f"compact K2P tree transition row {name}",
            lambda cert, name=name: cert["comparison_tree"]["transition_probabilities"][name][0].__setitem__(0, "999"),
            f"{name} stored tree transition row",
        )
    run_simple_mutation(
        "compact K2P rooted endpoint",
        lambda cert: cert["rooted_network"]["arcs"][0].__setitem__("parent", "q"),
    )
    run_simple_mutation(
        "compact K2P inheritance weight",
        lambda cert: cert["mixing_parameters"].__setitem__("r2", "2/3"),
        "inheritance parameters must both equal 1/2",
    )

    td = Path(tempfile.mkdtemp(prefix="v126-k2p-pruning-"))
    for name in ("strict_json.py", "verify_k2p_displayed_trees.py", "certificate_k2p_simple.json"):
        shutil.copy2(MATERIALS / name, td / name)
    script = td / "verify_k2p_displayed_trees.py"
    raw = script.read_text(encoding="utf-8")
    old = "kernel[parent_state ^ child_state]"
    if raw.count(old) != 1:
        raise AssertionError("unexpected compact-K2P transition-index source")
    script.write_text(raw.replace(old, "kernel[(parent_state + child_state) % 4]"), encoding="utf-8")
    rejected(
        "compact K2P ordinary-state pruning uses cyclic rather than Klein addition",
        run([sys.executable, script.name], td),
    )
    shutil.rmtree(td)


def k3p_bundle() -> Path:
    td = Path(tempfile.mkdtemp(prefix="v126-k3p-"))
    (td / "src").mkdir()
    shutil.copy2(MATERIALS / "strict_json.py", td / "strict_json.py")
    shutil.copy2(MATERIALS / "src" / "verify_k3p.py", td / "src" / "verify_k3p.py")
    for name in (
        "certificate_k3p.json",
        "jacobian_certificate_k3p.json",
        "continuous_time_certificate_k3p.json",
    ):
        shutil.copy2(MATERIALS / name, td / name)
    return td


def write_k3p(td: Path, cert: dict, *, sync_sidecars: bool = False) -> None:
    (td / "certificate_k3p.json").write_text(json.dumps(cert, indent=2) + "\n", encoding="utf-8")
    if sync_sidecars:
        (td / "jacobian_certificate_k3p.json").write_text(
            json.dumps(cert["jacobian"], indent=2) + "\n", encoding="utf-8"
        )
        (td / "continuous_time_certificate_k3p.json").write_text(
            json.dumps(cert["continuous_time"], indent=2) + "\n", encoding="utf-8"
        )


def run_k3p_mutation(
    label: str,
    mutate: Callable[[dict], None],
    diagnostic: str | None = None,
    *,
    sync_sidecars: bool = False,
    should_pass: bool = False,
) -> None:
    td = k3p_bundle()
    cert_path = td / "certificate_k3p.json"
    cert = json.loads(cert_path.read_text(encoding="utf-8"))
    mutate(cert)
    write_k3p(td, cert, sync_sidecars=sync_sidecars)
    completed = run([sys.executable, "src/verify_k3p.py"], td)
    if should_pass:
        accepted(label, completed)
    else:
        rejected(label, completed, diagnostic)
    shutil.rmtree(td)


def k3p_tests() -> None:
    base = json.loads((MATERIALS / "certificate_k3p.json").read_text(encoding="utf-8"))
    for index, row in enumerate(base["rooted_network"]["arcs"]):
        replacement = "q" if row["parent"] != "q" else "p"
        run_k3p_mutation(
            f"K3P canonical endpoint on {row['id']}",
            lambda cert, index=index, replacement=replacement: cert["rooted_network"]["arcs"][index].__setitem__("parent", replacement),
            "canonical rooted arc ID/endpoint/vector map",
        )

    for retic_index, retic in enumerate(base["rooted_network"]["reticulations"]):
        for incoming_index, descriptor in enumerate(retic["incoming"]):
            wrong = "q" if descriptor["parent"] == "p" else "p"
            run_k3p_mutation(
                f"K3P reticulation parent descriptor {retic['vertex']}[{incoming_index}]",
                lambda cert, ri=retic_index, ii=incoming_index, wrong=wrong: cert["rooted_network"]["reticulations"][ri]["incoming"][ii].__setitem__("parent", wrong),
                "reticulation descriptor parent",
            )
            run_k3p_mutation(
                f"K3P reticulation choice descriptor {retic['vertex']}[{incoming_index}]",
                lambda cert, ri=retic_index, ii=incoming_index, wrong=wrong: cert["rooted_network"]["reticulations"][ri]["incoming"][ii].__setitem__("choice", wrong),
                "reticulation descriptor choice",
            )

    run_k3p_mutation(
        "K3P duplicate vertex identifier without length change",
        lambda cert: cert["rooted_network"]["vertices"][1].__setitem__("id", "rho"),
        "duplicate vertex identifier",
    )

    for name in ("K", "K_odot_K", "U", "V", "S", "T"):
        run_k3p_mutation(
            f"K3P parameter transition row {name}",
            lambda cert, name=name: cert["parameter_vectors"][name]["transition_probabilities"][0].__setitem__(0, "999"),
            "inverse Fourier probabilities",
        )
    for leaf in ("1", "2", "3"):
        run_k3p_mutation(
            f"K3P comparison-tree transition row leaf {leaf}",
            lambda cert, leaf=leaf: cert["comparison_tree"]["leaf_edge_vectors"][leaf]["transition_probabilities"][0].__setitem__(0, "999"),
            "inverse Fourier probabilities",
        )
    for row in base["root_suppression"]["effective_semi_directed_edges"]:
        edge_id = row["id"]
        run_k3p_mutation(
            f"K3P suppressed transition row {edge_id}",
            lambda cert, edge_id=edge_id: next(
                item for item in cert["root_suppression"]["effective_semi_directed_edges"] if item["id"] == edge_id
            )["transition_probabilities"][0].__setitem__(0, "999"),
            "probabilities",
        )

    run_k3p_mutation(
        "K3P stored Jacobian matrix entry",
        lambda cert: cert["jacobian"]["matrix"][0][0].__setitem__(0, "999"),
        "reconstructed Jacobian matrix",
        sync_sidecars=True,
    )
    run_k3p_mutation(
        "K3P stored Jacobian determinant",
        lambda cert: cert["jacobian"]["determinant"].__setitem__(0, "999"),
        "Jacobian determinant",
        sync_sidecars=True,
    )

    def coordinated_column_swap(cert: dict) -> None:
        columns = cert["jacobian"]["column_order"]
        columns[3], columns[4] = columns[4], columns[3]
        for row in cert["jacobian"]["matrix"]:
            row[3], row[4] = row[4], row[3]
        pivots = cert["continuous_time"]["pivot_derivatives"]
        pivots[3], pivots[4] = pivots[4], pivots[3]

    run_k3p_mutation(
        "K3P coordinated Jacobian descriptor/matrix/pivot swap",
        coordinated_column_swap,
        "canonical Jacobian descriptor order",
        sync_sidecars=True,
    )
    run_k3p_mutation(
        "K3P pivot tangent value",
        lambda cert: cert["continuous_time"]["pivot_derivatives"][0]["value"].__setitem__(0, "999"),
        "linearized fixed-output identity",
        sync_sidecars=True,
    )
    run_k3p_mutation(
        "K3P free-direction descriptor",
        lambda cert: cert["continuous_time"]["free_direction"][0].__setitem__("character", "G"),
        "canonical continuous-time free-direction descriptors",
        sync_sidecars=True,
    )
    run_k3p_mutation(
        "K3P stored Fourier coordinate",
        lambda cert: cert["fourier_coordinates"]["network"][1].__setitem__(0, "999"),
        "stored network Fourier coordinate",
    )
    run_k3p_mutation(
        "K3P stored ordinary pattern probability",
        lambda cert: cert["leaf_pattern_probabilities"]["network"][0].__setitem__(0, "999"),
        "stored network pattern probability",
    )

    td = k3p_bundle()
    script = td / "src" / "verify_k3p.py"
    raw = script.read_text(encoding="utf-8")
    replacements = {
        "transitions[edge_id][parent_state ^ child_state]":
            "transitions[edge_id][(parent_state + child_state) % 4]",
        "transitions[leaf][root_state ^ pattern[position]]":
            "transitions[leaf][(root_state + pattern[position]) % 4]",
    }
    for old, new in replacements.items():
        if raw.count(old) != 1:
            raise AssertionError(f"unexpected K3P pruning source for {old}")
        raw = raw.replace(old, new)
    script.write_text(raw, encoding="utf-8")
    rejected(
        "K3P ordinary-state pruning uses cyclic rather than Klein addition",
        run([sys.executable, "src/verify_k3p.py"], td),
    )
    shutil.rmtree(td)

    run_k3p_mutation(
        "K3P title is informational",
        lambda cert: cert.__setitem__("title", "hostile informational title"),
        should_pass=True,
    )
    run_k3p_mutation(
        "K3P ansatz form prose is informational",
        lambda cert: cert["construction_ansatz"]["form"].__setitem__(
            "U", "hostile informational prose"
        ),
        should_pass=True,
    )
    run_k3p_mutation(
        "K3P Jacobian number-field prose is informational",
        lambda cert: cert["jacobian"].__setitem__("number_field", "hostile informational prose"),
        sync_sidecars=True,
        should_pass=True,
    )


def integrity_tests() -> None:
    def execute(label: str, mutate: Callable[[Path], None]) -> None:
        with tempfile.TemporaryDirectory(prefix="v126-integrity-") as td:
            destination = Path(td) / "packet"
            shutil.copytree(PACKET, destination, symlinks=True)
            mutate(destination)
            rejected(label, run(["bash", "./RUN_REFEREE_REPLAY.sh"], destination))

    execute(
        "packet changed byte",
        lambda root: (root / "START_HERE.md").write_text(
            (root / "START_HERE.md").read_text(encoding="utf-8") + "x",
            encoding="utf-8",
        ),
    )
    execute(
        "packet extra file",
        lambda root: (root / "rogue.txt").write_text("rogue\n", encoding="utf-8"),
    )

    def missing(root: Path) -> None:
        (root / "START_HERE.md").unlink()

    execute("packet missing file", missing)

    def symlink(root: Path) -> None:
        target = root / "START_HERE.md"
        target.unlink()
        target.symlink_to("PACKET_PROVENANCE.txt")

    execute("packet symbolic link", symlink)
    execute("packet extra directory", lambda root: (root / "rogue-directory").mkdir())


def main() -> None:
    strict_loader_tests()
    k2p_tests()
    k3p_tests()
    integrity_tests()
    print()
    print(f"OPERATIVE/INTEGRITY MUTATIONS REJECTED: {REJECTIONS}")
    print(f"DECLARED-INFORMATIONAL VALUE MUTATIONS ACCEPTED: {EXPECTED_PASSES}")
    print("ALL INDEPENDENT HOSTILE MUTATION TESTS PASSED")


if __name__ == "__main__":
    main()

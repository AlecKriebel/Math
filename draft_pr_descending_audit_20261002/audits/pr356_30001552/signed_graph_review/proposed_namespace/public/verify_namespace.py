"""Read-only package inventory/evidence checks; never reruns mathematical code."""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text())


def safe_file(namespace, relative):
    parts = PurePosixPath(relative).parts
    assert parts and not PurePosixPath(relative).is_absolute()
    assert all(part not in ("..", ".") for part in parts), relative
    path = namespace.joinpath(*parts)
    assert path.is_file() and not path.is_symlink(), relative
    assert namespace.resolve() in path.resolve().parents, relative
    return path


def check_inventory(namespace, inventory):
    for relative, record in inventory.items():
        path = safe_file(namespace, relative)
        assert path.stat().st_size == record["bytes"], (relative, "size")
        assert sha(path) == record["sha256"], (relative, "sha256")


def scope_files(namespace, partition):
    start = namespace / partition
    assert start.is_dir() and not start.is_symlink(), partition
    files = set()
    for path in start.rglob("*"):
        assert not path.is_symlink(), str(path)
        if path.is_file():
            files.add(path.relative_to(namespace).as_posix())
    return files


def check_saved_evidence(namespace):
    native = namespace / "private" / "native_outputs"
    pins_path = native / "PREEXECUTION_PINS.json"
    pins = load(pins_path)
    assert pins["assertions_enabled"] is True
    assert pins["candidate_paths_read_only"] is True
    runner = safe_file(namespace, "private/run_evidence.py")
    assert sha(runner) == pins["runner_sha256"]
    mappings = {
        "signed_graph_review/check_signed_graph.py": "public/check_signed_graph.py",
        "30001552_antimorphic_periods/check_turn1.py": "private/candidate_code/check_turn1.py",
        "30001552_antimorphic_periods/review/run_portable.py": "private/candidate_code/review/run_portable.py",
        "30001552_antimorphic_periods/review/check_independent.py": "private/candidate_code/review/check_independent.py",
    }
    mapped = set()
    for original, expected in pins["programs"].items():
        destinations = [target for suffix, target in mappings.items()
                        if original.endswith("/" + suffix)]
        assert len(destinations) == 1, ("unmapped original code path", original)
        target = destinations[0]
        assert sha(safe_file(namespace, target)) == expected, target
        mapped.add(target)
    assert mapped == set(mappings.values())
    receipt_map = {
        "independent_signed_graph": "SIGNED_GRAPH_CHECKS.json",
        "submitted_author": "AUTHOR_REPLAY.json",
        "submitted_portable": "PORTABLE_REPLAY.json",
    }
    stream_checks = []
    for name, receipt in receipt_map.items():
        meta = load(native / (name + ".meta.json"))
        assert meta["name"] == name and meta["exit_code"] == 0
        assert meta["argv"] == pins["commands"][name]
        assert meta["preexecution_pin_sha256"] == sha(pins_path)
        for kind in ("stdout", "stderr"):
            stream = safe_file(namespace, "private/native_outputs/" + name + "." + kind)
            assert stream.stat().st_size == meta[kind + "_bytes"]
            assert sha(stream) == meta[kind + "_sha256"]
            stream_checks.append(name + "." + kind)
        assert (native / (name + ".stderr")).read_bytes() == b""
        assert safe_file(namespace, "public/" + receipt).read_bytes() == (native / (name + ".stdout")).read_bytes()
        if name in ("submitted_author", "submitted_portable"):
            assert meta["receipt_bytes_match"] is True
    summary = load(native / "NATIVE_RUN_SUMMARY.json")
    assert summary["all_exit_codes_zero"] is True
    assert len(summary["native_runs"]) == 3
    for meta in summary["native_runs"]:
        assert meta == load(native / (meta["name"] + ".meta.json"))
    baseline = namespace / "private" / "source_baseline"
    gate = load(baseline / "GATE_MANIFEST.json")
    for name, expected in gate["files"].items():
        assert sha(safe_file(namespace, "private/source_baseline/" + name)) == expected
    assert sha(baseline / "owr2010-37.pdf") == gate["source_sha256"]
    gate_digest = (baseline / "GATE_MANIFEST.sha256").read_text().split()[0]
    assert sha(baseline / "GATE_MANIFEST.json") == gate_digest
    initial_pins = {}
    for line in (namespace / "private" / "RUNNER_PREEXECUTION.sha256").read_text().splitlines():
        expected, name = line.split()
        initial_pins[name] = expected
    assert initial_pins["check_signed_graph.py"] == sha(namespace / "public" / "check_signed_graph.py")
    assert initial_pins["run_evidence.py"] == sha(runner)
    verifier_capture = namespace / "private" / "namespace_verifier_native"
    verifier_streams = []
    if verifier_capture.is_dir():
        verifier_pin_path = verifier_capture / "PREEXECUTION_PINS.json"
        verifier_pins = load(verifier_pin_path)
        assert verifier_pins["program_sha256"] == sha(namespace / "public" / "verify_namespace.py")
        assert verifier_pins["runner_sha256"] == sha(namespace / "private" / "run_namespace_verifier_evidence.py")
        for name in ("full", "public"):
            meta = load(verifier_capture / (name + ".meta.json"))
            assert meta["exit_code"] == 0
            assert meta["argv"] == verifier_pins["commands"][name]
            assert meta["preexecution_pin_sha256"] == sha(verifier_pin_path)
            for kind in ("stdout", "stderr"):
                stream = verifier_capture / (name + "." + kind)
                assert stream.stat().st_size == meta[kind + "_bytes"]
                assert sha(stream) == meta[kind + "_sha256"]
                verifier_streams.append(name + "." + kind)
            assert (verifier_capture / (name + ".stderr")).read_bytes() == b""
        assert load(verifier_capture / "UNCHANGED_CHECK.json")["namespace_bytes_unchanged"] is True
    return {"whole_native_streams_checked": stream_checks,
            "code_pins_checked": sorted(mapped) + ["private/run_evidence.py"],
            "source_first_gate_payloads_checked": len(gate["files"]),
            "whole_saved_verifier_streams_checked": verifier_streams,
            "original_optional_source5_mode_reproduced": False,
            "math_programs_rerun_by_verifier": False}


ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("--namespace", type=Path, default=Path(__file__).resolve().parent.parent)
ap.add_argument("--mode", choices=("full", "public"), default="full")
ap.add_argument("--proposal", type=Path, help="Check a pinned pre-closure proposal instead of final inventories/seal.")
args = ap.parse_args()
namespace = args.namespace.resolve()
assert namespace.is_dir()

if args.proposal:
    proposal = load(args.proposal)
    all_items = proposal["files"]
    public_items = {name: record for name, record in all_items.items() if name.startswith("public/")}
    private_items = {name: record for name, record in all_items.items() if name.startswith("private/")}
    assert len(public_items) + len(private_items) == len(all_items)
    public_expected = set(public_items)
    private_expected = set(private_items)
    seal_status = "UNSEALED_PROPOSAL_CHECK"
    omitted_private_count = len(private_items)
else:
    seal_path = safe_file(namespace, "public/CLOSURE_SEAL.json")
    seal = load(seal_path)
    assert seal["status"] == "SEALED_ONCE_READ_ONLY"
    public_inventory_path = safe_file(namespace, "public/PUBLIC_INVENTORY.json")
    assert sha(public_inventory_path) == seal["public_inventory_sha256"]
    public_items = load(public_inventory_path)["files"]
    assert all(name.startswith("public/") for name in public_items)
    public_expected = set(public_items) | {"public/PUBLIC_INVENTORY.json", "public/CLOSURE_SEAL.json"}
    omitted_private_count = seal["private_payload_file_count"]
    if args.mode == "full":
        private_inventory_path = safe_file(namespace, "private/PRIVATE_INVENTORY.json")
        assert sha(private_inventory_path) == seal["private_inventory_sha256"]
        private_items = load(private_inventory_path)["files"]
        assert all(name.startswith("private/") for name in private_items)
        assert len(private_items) == omitted_private_count
        private_expected = set(private_items) | {"private/PRIVATE_INVENTORY.json"}
    else:
        private_items = {}
        private_expected = set()
    seal_status = "SEALED_INVENTORY_CHECK"

assert scope_files(namespace, "public") == public_expected, "public inventory is not exact"
check_inventory(namespace, public_items)
if args.mode == "full":
    assert scope_files(namespace, "private") == private_expected, "private inventory is not exact"
    check_inventory(namespace, private_items)
    evidence = check_saved_evidence(namespace)
    status = "PASS_FULL_SAVED_EVIDENCE"
    omissions = ["No mathematical code is executed by this verifier.",
                 "Original optional five-source reviewer mode is not reproduced or certified."]
else:
    evidence = {"whole_native_streams_checked": [], "code_pins_checked": [],
                "source_first_gate_payloads_checked": 0,
                "math_programs_rerun_by_verifier": False}
    status = "PASS_PUBLIC_INVENTORY_ONLY"
    omissions = ["Private payload inventory and its file bodies are not checked.",
                 "Private pre-execution pins, original code payloads, native stderr/metadata, source-first gate and raw source pages are omitted.",
                 "Public receipts are checked as inventory bytes only; their private native-stream/code-pin bindings are omitted.",
                 "Original optional five-source reviewer mode is not reproduced or certified.",
                 "No mathematical code is executed by this verifier."]
print(json.dumps({"status": status, "mode": args.mode, "seal_status": seal_status,
                  "public_payload_files_checked": len(public_items),
                  "private_payload_files_checked": len(private_items) if args.mode == "full" else 0,
                  "private_payload_files_omitted": 0 if args.mode == "full" else omitted_private_count,
                  "evidence": evidence, "explicit_scope_omissions": omissions,
                  "filesystem_mutations_performed": False}, indent=2))

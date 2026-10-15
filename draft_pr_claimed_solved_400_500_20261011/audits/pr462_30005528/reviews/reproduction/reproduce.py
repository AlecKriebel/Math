#!/usr/bin/env python3
"""Read-only frozen-packet audit; executions and invalid fixtures live in temp dirs."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def execute(command, cwd, optimized=False):
    env = dict(os.environ)
    env["PYTHONOPTIMIZE"] = "1" if optimized else "0"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run(command, cwd=cwd, env=env, capture_output=True)
    return proc, {
        "returncode": proc.returncode,
        "stdout_bytes": len(proc.stdout),
        "stdout_sha256": sha(proc.stdout),
        "stderr_bytes": len(proc.stderr),
        "stderr_final_line": proc.stderr.decode(errors="replace").splitlines()[-1:] or [],
        "PYTHONOPTIMIZE": env["PYTHONOPTIMIZE"],
    }


def audit(case):
    root = case / "source_snapshot"
    packet = root / "unsolved_math_prioritization/attempts/30005528"
    receipt = json.loads((case / "SOURCE_RECEIPT.json").read_text())
    inventory = []
    for item in receipt["files"]:
        data = (root / item["path"]).read_bytes()
        okay = len(data) == item["bytes"] and sha(data) == item["sha256"]
        require(okay, "Source-receipt mismatch: " + item["path"])
        inventory.append({"path": item["path"], "bytes": len(data), "sha256": sha(data), "matches": okay})
    actual = sorted(str(p.relative_to(root)) for p in root.rglob("*") if p.is_file())
    require(actual == sorted(x["path"] for x in receipt["files"]), "Snapshot inventory mismatch")
    manifests = []
    frozen = json.loads((packet / "audit/FROZEN_INPUTS.json").read_text())
    for item in frozen["files"]:
        data = (packet / "release" / item["path"]).read_bytes()
        okay = len(data) == item["bytes"] and sha(data) == item["sha256"]
        require(okay, "FROZEN_INPUTS mismatch: " + item["path"])
        manifests.append({"manifest": "audit/FROZEN_INPUTS.json", "target": "release/" + item["path"], "matches": okay})
    manifest = json.loads((packet / "audit/AUDIT_MANIFEST.json").read_text())
    for name, digest in manifest["portable_files"].items():
        data = (packet / "audit" / name).read_bytes()
        require(sha(data) == digest, "AUDIT_MANIFEST mismatch: " + name)
        manifests.append({"manifest": "audit/AUDIT_MANIFEST.json", "target": "audit/" + name, "matches": True})
    author_record = (packet / "release/checks/verification_results.json").read_bytes()
    controls_record = (packet / "audit/audit_controls.json").read_bytes()
    replay = {}
    guards = []
    mutations = {
        "unreduced_claimed_period": ("q = n // gcd(m, n)", "q = n"),
        "approximation_from_below": ("m = isqrt(2 * n * n) + 1", "m = isqrt(2 * n * n)"),
        "omit_initial_symbol_cost": ("range(N + 1)", "range(N)"),
        "wrong_height_sign": ("t = Qsqrt2(angle, Q(-1))", "t = Qsqrt2(angle, Q(1))"),
        "wrong_rationalization_identity": ("Q(p*p - 2*q*q, q*q)", "Q(p*p + 2*q*q, q*q)"),
        "invert_exact_sign_comparison": ("delta = a * a - 2 * b * b", "delta = 2 * b * b - a * a"),
    }
    mutation_results = []
    source = (packet / "release/checks/verify_rotation_family.py").read_text()
    with tempfile.TemporaryDirectory(prefix="pr462-reproduction-") as temp:
        temp = Path(temp)
        work = temp / "outside-source"
        work.mkdir()
        copy = temp / "packet"
        shutil.copytree(packet, copy)
        for optimized in (False, True):
            mode = "optimized" if optimized else "normal"
            flags = ["-B", "-O"] if optimized else ["-B"]
            author = copy / "release/checks/verify_rotation_family.py"
            proc, info = execute([sys.executable, *flags, str(author)], work, optimized)
            info["stdout_equals_recorded"] = proc.stdout == author_record
            info["regenerated_json_equals_recorded"] = author.with_name("verification_results.json").read_bytes() == author_record
            require(proc.returncode == 0 and info["stdout_equals_recorded"] and info["regenerated_json_equals_recorded"], "Author baseline mismatch: " + mode)
            replay["author_" + mode] = info
            proc, info = execute([sys.executable, *flags, str(copy / "audit/audit_controls.py"), "--release", str(copy / "release")], work, optimized)
            info["stdout_equals_recorded"] = proc.stdout == controls_record
            if proc.returncode == 0:
                info["actual_json"] = json.loads(proc.stdout)
            replay["historical_controls_" + mode] = info
            for name, (old, new) in mutations.items():
                require(source.count(old) == 1, "Nonunique mutation target: " + name)
                path = temp / (name + ".py")
                path.write_text(source.replace(old, new))
                proc, info = execute([sys.executable, *flags, str(path)], work, optimized)
                info.update({"name": name, "mode": mode, "rejected": proc.returncode != 0, "stdout_equals_original_record": proc.stdout == author_record})
                mutation_results.append(info)
            # Each guard targets a separate boundary, and runs with optimized guards too.
            for guard in ("inventory", "length", "sha256", "strict_cli"):
                guard_copy = temp / ("guard_" + mode + "_" + guard)
                shutil.copytree(packet, guard_copy)
                if guard == "inventory":
                    (guard_copy / "release/unexpected.txt").write_text("invalid fixture\n")
                elif guard == "length":
                    target = guard_copy / "release/README.md"
                    target.write_bytes(target.read_bytes() + b"\n")
                elif guard == "sha256":
                    target = guard_copy / "release/README.md"
                    data = target.read_bytes()
                    target.write_bytes(b"!" + data[1:])
                command = [sys.executable, *flags, str(guard_copy / "audit/audit_controls.py"), "--release", str(guard_copy / "release")]
                if guard == "strict_cli":
                    command.append("--not-a-valid-option")
                proc, info = execute(command, work, optimized)
                info.update({"guard": guard, "mode": mode, "rejected": proc.returncode != 0})
                require(info["rejected"], "Historical guard silently accepted " + mode + "/" + guard)
                guards.append(info)
    for item in receipt["files"]:
        require(sha((root / item["path"]).read_bytes()) == item["sha256"], "Source changed")
    return {
        "reviewer": "independent reproduction subagent",
        "pr": 462, "problem_id": 30005528,
        "frozen_head": receipt["head_sha"],
        "python_version": sys.version.split()[0],
        "source_hash_checks": inventory,
        "source_files_checked": len(inventory),
        "named_manifest_references": manifests,
        "named_manifest_references_checked": len(manifests),
        "manifest_coverage": {
            "FROZEN_INPUTS.json": "Six release files; does not self-attest or attest audit files.",
            "AUDIT_MANIFEST.json": "Four other audit files; does not self-attest or attest PUBLICATION_NOTES.md. These omitted files are attested by the 12-file source receipt.",
            "self_reference_rule": "No manifest contains its own hash. None is claimed here to be self-attesting."
        },
        "replays": replay, "strict_guard_controls": guards,
        "author_mutation_subprocesses": mutation_results,
        "source_unchanged_after_execution": True,
        "limitations": ["Finite controls establish no all-irrational theorem, topological density, novelty, or packing realization.", "No third-party source content or environment data is saved in this result."]
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(audit(args.case.resolve()), indent=2, sort_keys=True))

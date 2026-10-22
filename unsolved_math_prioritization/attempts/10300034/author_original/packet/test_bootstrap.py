#!/usr/bin/env python3
"""Adversarial finite artifact controls; authenticate this file before executing."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

class Rejected(Exception):
    pass

def require(value, message):
    if not value:
        raise Rejected(message)

def run_process(root, flags=(), args=(), env=None):
    return subprocess.run([sys.executable, "-I", "-S", "-B", *flags,
                           str(root / "bootstrap.py"), *args], cwd=root.parent,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          timeout=60, env=env)

def restore_permissions(root):
    for current, dirs, files in os.walk(root, followlinks=False):
        os.chmod(current, 0o755)
        for name in files:
            p = Path(current) / name
            if not p.is_symlink():
                os.chmod(p, 0o644)

def rehash_manifest(root):
    p = root / "AUTHOR_MANIFEST.json"
    data = json.loads(p.read_text())
    for item in data["files"]:
        raw = (root / "packet" / item["path"]).read_bytes()
        item["bytes"] = len(raw)
        item["sha256"] = hashlib.sha256(raw).hexdigest()
    p.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")

def mutate(root, name):
    packet = root / "packet"
    manifest = root / "AUTHOR_MANIFEST.json"
    if name == "changed_proof":
        with (packet / "PROOF.md").open("ab") as f:
            f.write(b"\nchanged\n")
    elif name == "missing_proof":
        (packet / "PROOF.md").unlink()
    elif name == "extra_payload":
        (packet / "extra.txt").write_text("unexpected")
    elif name == "extra_payload_directory":
        (packet / "extra").mkdir()
    elif name == "extra_root":
        (root / "extra.txt").write_text("unexpected")
    elif name == "payload_symlink":
        target = root.parent / "outside-proof"
        shutil.copy2(packet / "PROOF.md", target)
        (packet / "PROOF.md").unlink()
        (packet / "PROOF.md").symlink_to(target)
    elif name == "manifest_symlink":
        target = root.parent / "outside-manifest"
        shutil.copy2(manifest, target)
        manifest.unlink()
        manifest.symlink_to(target)
    elif name == "bootstrap_symlink":
        target = root.parent / "outside-bootstrap"
        shutil.copy2(root / "bootstrap.py", target)
        (root / "bootstrap.py").unlink()
        (root / "bootstrap.py").symlink_to(target)
    elif name == "packet_symlink":
        target = root.parent / "outside-packet"
        packet.rename(target)
        packet.symlink_to(target, target_is_directory=True)
    elif name == "payload_is_directory":
        (packet / "PROOF.md").unlink()
        (packet / "PROOF.md").mkdir()
    elif name == "truncated_manifest":
        manifest.write_bytes(b'{"schema":')
    elif name == "duplicate_key_manifest":
        manifest.write_bytes(b'{"files":[],"files":[]}')
    elif name == "nonfinite_manifest":
        manifest.write_bytes(b'{"files":NaN}')
    elif name == "invalid_utf8_manifest":
        manifest.write_bytes(b'\xff\xfe')
    elif name == "boolean_integer_manifest":
        data = json.loads(manifest.read_text())
        data["problem_id"] = True
        manifest.write_text(json.dumps(data))
    elif name == "unsafe_manifest_path":
        data = json.loads(manifest.read_text())
        data["files"][0]["path"] = "../outside"
        manifest.write_text(json.dumps(data))
    elif name == "duplicate_inventory":
        data = json.loads(manifest.read_text())
        data["files"].append(data["files"][0])
        manifest.write_text(json.dumps(data))
    elif name == "forged_solved_and_rehashed":
        data = json.loads((packet / "CLAIMS.json").read_text())
        data["disposition"] = "solved"
        (packet / "CLAIMS.json").write_text(json.dumps(data))
        rehash_manifest(root)
    elif name == "malicious_verifier_and_rehashed":
        (packet / "verify.py").write_text("raise RuntimeError('UNAUTHENTICATED_CODE_EXECUTED')\n")
        rehash_manifest(root)
    elif name == "malformed_claims":
        (packet / "CLAIMS.json").write_text("{broken")
    elif name == "malformed_diagnostics":
        (packet / "DIAGNOSTICS.json").write_text("[]")
    elif name == "unreadable_payload":
        os.chmod(packet / "PROOF.md", 0)
    else:
        raise Rejected("unknown mutation")

def run():
    require(len(sys.argv) == 1, "test harness accepts no arguments")
    original = Path(__file__).resolve().parents[1]
    mutations = ["changed_proof", "missing_proof", "extra_payload", "extra_payload_directory",
                 "extra_root", "payload_symlink", "manifest_symlink", "bootstrap_symlink",
                 "packet_symlink", "payload_is_directory", "truncated_manifest", "duplicate_key_manifest",
                 "nonfinite_manifest", "invalid_utf8_manifest", "boolean_integer_manifest",
                 "unsafe_manifest_path", "duplicate_inventory", "forged_solved_and_rehashed",
                 "malicious_verifier_and_rehashed", "malformed_claims", "malformed_diagnostics",
                 "unreadable_payload"]
    reports = []
    expected_output = None
    for flags in ((), ("-O",), ("-OO",)):
        accepted = rejected = 0
        with tempfile.TemporaryDirectory(prefix="transverse-surgery-controls-") as tmp:
            base = Path(tmp)
            good = base / "relocated author with spaces"
            shutil.copytree(original, good)
            p = run_process(good, flags)
            require(p.returncode == 0, "relocated positive failed: " + p.stderr.decode())
            if expected_output is None:
                expected_output = p.stdout
            require(p.stdout == expected_output, "optimization output mismatch")
            accepted += 1
            for item in good.rglob("*"):
                os.chmod(item, 0o555 if item.is_dir() else 0o444)
            os.chmod(good, 0o555)
            try:
                p = run_process(good, flags)
                require(p.returncode == 0 and p.stdout == expected_output, "read-only positive failed")
                accepted += 1
            finally:
                restore_permissions(good)
            hostile = base / "hostile"
            hostile.mkdir()
            (hostile / "json.py").write_text("raise RuntimeError('hostile import')\n")
            env = dict(os.environ, PYTHONPATH=str(hostile), PYTHONSTARTUP=str(hostile / "json.py"))
            p = run_process(good, flags, env=env)
            require(p.returncode == 0 and p.stdout == expected_output, "hostile import path")
            accepted += 1
            p = run_process(good, flags, args=("unexpected",))
            require(p.returncode != 0, "unexpected argument accepted")
            rejected += 1
            link = base / "symlink author"
            link.symlink_to(good, target_is_directory=True)
            p = run_process(link, flags)
            require(p.returncode != 0, "symlink ancestor accepted")
            rejected += 1
            for number, name in enumerate(mutations):
                bad = base / ("bad-" + str(number))
                shutil.copytree(original, bad)
                mutate(bad, name)
                try:
                    p = run_process(bad, flags)
                    require(p.returncode != 0, "mutation accepted: " + name)
                    require(b"UNAUTHENTICATED_CODE_EXECUTED" not in p.stderr,
                            "unauthenticated verifier was run")
                    rejected += 1
                finally:
                    restore_permissions(bad)
            # External malformed corpus inputs must fail before any contents are emitted.
            bad_input = base / "malformed-input.json"
            for raw in (b"", b"{bad", b"[]", b"{}", b'{"x":1,"x":2}', b'{"x":NaN}', b"\xff"):
                bad_input.write_bytes(raw)
                p = subprocess.run([sys.executable, "-I", "-S", "-B", *flags,
                                    str(good / "packet" / "verify_corpus.py"), str(bad_input), str(bad_input)],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
                require(p.returncode != 0 and not p.stdout, "malformed corpus accepted or emitted")
                rejected += 1
            reports.append({"mode": "normal" if not flags else flags[0], "accepted_controls": accepted,
                            "rejected_controls": rejected})
    return {"schema": "transverse-surgery-bootstrap-controls-v1", "status": "pass", "modes": reports,
            "limits": "finite artifact controls, not a formal proof or filesystem-race defense"}

if __name__ == "__main__":
    try:
        print(json.dumps(run(), sort_keys=True, separators=(",", ":")))
    except (Rejected, OSError, ValueError, TypeError, KeyError, subprocess.SubprocessError) as exc:
        print("REJECT: " + str(exc), file=sys.stderr)
        sys.exit(1)

"""Replay the pinned verifier source against clean and deliberately damaged packets.

Run with Python -I -B. Temporary copies are outside the packet and deleted afterward.
Integrity controls do not establish the mathematical theorem.
"""
import base64
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def main():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / "MANIFEST.json").read_text())
    binding = next(x for x in manifest["files"] if x["name"] == "VERIFY.py")
    verifier = (root / "VERIFY.py").read_bytes()
    require(hashlib.sha256(verifier).hexdigest() == binding["sha256"], "verifier source hash mismatch")
    require(len(verifier) == binding["bytes"], "verifier size mismatch")
    encoded = base64.b64encode(verifier).decode("ascii")
    runner = "import base64,sys;sys.argv=['verified-verifier',sys.argv[1]];exec(compile(base64.b64decode(" + repr(encoded) + "),'<pinned VERIFY.py>','exec'),{'__name__':'__main__'})"
    # Even a mutated VERIFY.py inside a test packet is never executed.
    modes = [("normal", []), ("optimized", ["-O"])]
    passed = []
    with tempfile.TemporaryDirectory(prefix="free-rank-controls-") as tmp:
        temp = Path(tmp)

        def replay(packet, flags):
            return subprocess.run([sys.executable, "-I", "-B"] + flags + ["-c", runner, str(packet)],
                                  cwd=temp, text=True, capture_output=True, timeout=30)

        for mode, flags in modes:
            result = replay(root, flags)
            require(result.returncode == 0, "baseline " + mode + ": " + result.stderr)
            baseline = json.loads(result.stdout)
            moved = temp / ("relocated-" + mode)
            shutil.copytree(root, moved)
            rerun = replay(moved, flags)
            require(rerun.returncode == 0 and json.loads(rerun.stdout) == baseline, "relocation failed")
            passed += ["baseline:" + mode, "relocation:" + mode]

        def rehash(packet, name):
            path = packet / "MANIFEST.json"
            m = json.loads(path.read_text())
            data = (packet / name).read_bytes()
            for item in m["files"]:
                if item["name"] == name:
                    item["sha256"] = hashlib.sha256(data).hexdigest()
                    item["bytes"] = len(data)
            path.write_text(json.dumps(m, sort_keys=True, indent=2) + "\n")

        def append_proof(p):
            with (p / "PROOF.md").open("a") as f:
                f.write("\nAltered proof.\n")

        def same_size_proof(p):
            data = (p / "PROOF.md").read_bytes()
            (p / "PROOF.md").write_bytes(b"!" + data[1:])

        def cache(p):
            (p / "__pycache__").mkdir()
            (p / "__pycache__" / "CHECKS.cpython-313.pyc").write_bytes(b"untrusted bytecode")

        def symlink(p):
            (p / "PROOF.md").unlink()
            (p / "PROOF.md").symlink_to(root / "PROOF.md")

        def duplicate_manifest(p):
            path = p / "MANIFEST.json"
            m = json.loads(path.read_text())
            m["files"].append(m["files"][0])
            path.write_text(json.dumps(m))

        def unsafe_manifest(p):
            path = p / "MANIFEST.json"
            m = json.loads(path.read_text())
            m["files"][0]["name"] = "../escaped"
            path.write_text(json.dumps(m))

        def wrong_arithmetic(p):
            path = p / "CHECKS.py"
            original = path.read_text()
            changed = original.replace("if any((k * w) % order == 0 for w in weights)",
                                       "if all((k * w) % order == 0 for w in weights)")
            require(changed != original, "semantic mutation was not applied")
            path.write_text(changed)
            rehash(p, "CHECKS.py")

        def wrong_ring(p):
            path = p / "CHECKS.py"
            original = path.read_text()
            changed = original.replace("ans ^= 1 << (i | j)", "ans |= 1 << (i | j)")
            require(changed != original, "ring mutation was not applied")
            path.write_text(changed)
            rehash(p, "CHECKS.py")

        def wrong_expected(p):
            path = p / "EXPECTED_RESULTS.json"
            m = json.loads(path.read_text())
            m["odd_primes_checked"] += 1
            path.write_text(json.dumps(m))
            rehash(p, "EXPECTED_RESULTS.json")

        def wrong_binding(p):
            path = p / "PROVENANCE.json"
            m = json.loads(path.read_text())
            m["review_sha256"] = "0" * 64
            path.write_text(json.dumps(m))
            rehash(p, "PROVENANCE.json")

        cases = {
            "appended-proof": append_proof,
            "same-size-proof": same_size_proof,
            "missing-file": lambda p: (p / "PROOF.md").unlink(),
            "extra-file": lambda p: (p / "unexpected.txt").write_text("unexpected"),
            "cache-directory": cache,
            "payload-symlink": symlink,
            "fifo": lambda p: os.mkfifo(p / "unexpected.pipe"),
            "extra-directory": lambda p: (p / "unexpected-directory").mkdir(),
            "duplicate-manifest": duplicate_manifest,
            "unsafe-manifest": unsafe_manifest,
            "rehash-wrong-weight-semantics": wrong_arithmetic,
            "rehash-wrong-ring-semantics": wrong_ring,
            "rehash-wrong-expected-results": wrong_expected,
            "rehash-wrong-review-binding": wrong_binding,
        }
        for label, mutate in cases.items():
            packet = temp / label
            shutil.copytree(root, packet)
            mutate(packet)
            for mode, flags in modes:
                result = replay(packet, flags)
                require(result.returncode != 0 and "FAIL:" in result.stderr,
                        "damaged packet accepted: " + label + ":" + mode)
                passed.append(label + ":" + mode)
        result = {"status": "PASS", "baseline_and_relocation_runs": 4,
                  "mutation_cases": len(cases), "mutant_rejections": 2*len(cases),
                  "controls": passed, "verifier_source_pinned_before_execution": True,
                  "scope": "Packaging and finite arithmetic, not mathematical proof verification."}
        print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()

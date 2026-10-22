#!/usr/bin/env python3
"""Disposable-copy checks of the publication wrapper's integrity boundary."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def need(value, message):
    if not value:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    root = Path(__file__).resolve().parent
    expected = digest(root / "PUBLICATION_MANIFEST.json")
    results = []

    def invoke(candidate, pin):
        p = subprocess.run([sys.executable, "-B", candidate / "verify_publication.py",
                            "--expected-manifest-sha256", pin], capture_output=True, text=True)
        need(not p.stderr, "unexpected test stderr")
        return p.returncode, json.loads(p.stdout)

    def flip(p):
        b = p.read_bytes()
        p.write_bytes(bytes([b[0] ^ 1]) + b[1:])

    def update_manifest(c):
        p = c / "PUBLICATION_MANIFEST.json"
        m = json.loads(p.read_text())
        for e in m["files"]:
            f = c / e["path"]
            e.update(bytes=f.stat().st_size, sha256=digest(f))
        p.write_text(json.dumps(m, indent=2, sort_keys=True) + "\n")

    code, output = invoke(root, expected)
    need(code == 0 and output["source_verification"] == "NOT_RUN_MISSING_SOURCES", "clean portable baseline")
    with tempfile.TemporaryDirectory(prefix="lyapunov-publication-controls-") as temp:
        temp = Path(temp)

        def case(name, mutate, rebind_publication=False):
            c = temp / name
            shutil.copytree(root, c)
            mutate(c)
            pin = expected
            if rebind_publication:
                update_manifest(c)
                pin = digest(c / "PUBLICATION_MANIFEST.json")
            code, out = invoke(c, pin)
            need(code == 1 and out["result"] == "FAIL", "mutation accepted: " + name)
            results.append({"case": name, "result": "REJECTED_AS_REQUIRED"})

        case("same_size_author_proof", lambda c: flip(c / "safe_freeze/PROOF.md"))
        case("same_size_corrected_audit", lambda c: flip(c / "independent_audit_corrected/AUDIT.md"))
        case("correction_receipt", lambda c: flip(c / "independent_audit_corrected/CORRECTION_RECEIPT.json"))
        case("missing_payload", lambda c: (c / "README.md").unlink())
        case("renamed_payload", lambda c: (c / "README.md").rename(c / "OTHER.md"))
        case("unexpected_file", lambda c: (c / "UNEXPECTED.txt").write_text("test\n"))
        case("publication_manifest_whitespace", lambda c: (c / "PUBLICATION_MANIFEST.json").write_bytes((c / "PUBLICATION_MANIFEST.json").read_bytes() + b"\n"))
        def symlink(c):
            (c / "README.md").unlink()
            (c / "README.md").symlink_to(root / "README.md")
        case("payload_symlink", symlink)
        case("directory_symlink", lambda c: (c / "LINK").symlink_to(root, target_is_directory=True))
        def coordinated_publication(c):
            flip(c / "README.md")
            update_manifest(c)
        case("coordinated_payload_publication_manifest", coordinated_publication)
        case("author_manifest_rebound_only_at_publication", lambda c: (c / "safe_freeze/MANIFEST.json").write_bytes((c / "safe_freeze/MANIFEST.json").read_bytes() + b"\n"), True)
        case("audit_manifest_rebound_only_at_publication", lambda c: (c / "independent_audit_corrected/MANIFEST.json").write_bytes((c / "independent_audit_corrected/MANIFEST.json").read_bytes() + b"\n"), True)
        c = temp / "relocated_clean"
        shutil.copytree(root, c)
        code, out = invoke(c, expected)
        need(code == 0 and out["source_verification"] == "NOT_RUN_MISSING_SOURCES", "relocated replay")
    print(json.dumps({"result": "PASS", "negative_control_count": len(results),
                      "controls": results, "relocated_replay": "PASS_PORTABLE_ONLY",
                      "source_verification": "NOT_RUN_MISSING_SOURCES",
                      "formal_proof_verification": False}, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"result": "FAIL", "error": str(exc)}, sort_keys=True))
        sys.exit(1)

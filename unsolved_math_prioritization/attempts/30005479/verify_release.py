#!/usr/bin/env python3
"""Strict portable integrity gate; optional assertion-enabled exact replay."""
import argparse, hashlib, json, pathlib, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parent
AUTHOR = {"README.md", "REPOSITORY_GATE.json", "RESEARCH_LOG.md", "RESULT.md", "SHA256SUMS.json", "SOURCE_GATE.md", "SOURCE_MANIFEST.json", "STATUS.json", "check_results.json", "turns.jsonl", "verify_dimensions.py", "verify_manifest.py"}
AUDIT = {"README.md", "AUDIT.md", "AUDIT_RESULT.json", "SOURCE_AUDIT.json", "independent_verify.py", "independent_results.json", "replayed_check_results.json", "verify_audit.py", "AUDIT_MANIFEST.json"}
TOP = {"README.md", "RELEASE_VERIFICATION.json", "RELEASE_MANIFEST.json", "verify_release.py"}
EXPECTED = TOP | {"author/" + x for x in AUTHOR} | {"audit/" + x for x in AUDIT}
def require(value, message):
    if not value:
        raise SystemExit("Integrity failure: " + message)
def digest(raw):
    return hashlib.sha256(raw).hexdigest()
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replay", action="store_true")
    args = parser.parse_args()
    found = set()
    directories = set()
    for p in ROOT.rglob("*"):
        rel = p.relative_to(ROOT).as_posix()
        require(not p.is_symlink(), "symlink: " + rel)
        if p.is_dir():
            directories.add(rel)
        else:
            require(p.is_file(), "not a regular file: " + rel)
            found.add(rel)
    require(found == EXPECTED, "file inventory")
    require(directories == {"author", "audit"}, "directory inventory")
    manifest = json.loads((ROOT / "RELEASE_MANIFEST.json").read_text())
    require(set(manifest["files"]) == EXPECTED - {"RELEASE_MANIFEST.json"}, "manifest inventory")
    for rel, meta in manifest["files"].items():
        raw = (ROOT / rel).read_bytes()
        require(len(raw) == meta["bytes"], "byte count: " + rel)
        require(digest(raw) == meta["sha256"], "SHA256: " + rel)
    require(digest((ROOT / "author/SHA256SUMS.json").read_bytes()) == "4edef8fe79ffe05582edec1331e8aeff3df8a7e6382d5db824dc016cd8b7d7f8", "frozen author manifest")
    require(digest((ROOT / "audit/AUDIT_MANIFEST.json").read_bytes()) == "3a9780d9482b9b7bed6907fad1dec3acd181018369adef6336287eadbd2983be", "frozen audit manifest")
    for folder, name in [("author", "SHA256SUMS.json"), ("audit", "AUDIT_MANIFEST.json")]:
        sub = json.loads((ROOT / folder / name).read_text())
        for rel, meta in sub["files"].items():
            require(rel in (AUTHOR if folder == "author" else AUDIT), "submanifest path")
            raw = (ROOT / folder / rel).read_bytes()
            require(len(raw) == meta["bytes"] and digest(raw) == meta["sha256"], "submanifest: " + folder + "/" + rel)
    replays = []
    if args.replay:
        for script, expected in [("author/verify_dimensions.py", "author/check_results.json"), ("audit/independent_verify.py", "audit/independent_results.json")]:
            result = subprocess.run([sys.executable, "-I", "-B", str(ROOT / script)], capture_output=True)
            require(result.returncode == 0, "replay execution: " + script)
            require(result.stdout == (ROOT / expected).read_bytes(), "replay mismatch: " + script)
            replays.append(script)
    print(json.dumps({"passed": True, "files": len(found), "replays": replays}, sort_keys=True))
if __name__ == "__main__":
    main()

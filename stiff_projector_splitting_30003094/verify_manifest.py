"""Check the complete package inventory, byte counts, and SHA-256 digests."""
import hashlib
import json
import pathlib


def main():
    root = pathlib.Path(__file__).resolve().parent
    manifest = json.loads((root / "MANIFEST.json").read_text())
    expected = {}
    for entry in manifest["files"]:
        name = entry["path"]
        relative = pathlib.PurePosixPath(name)
        if relative.is_absolute() or ".." in relative.parts or name in expected:
            raise SystemExit("Invalid or duplicate manifest path: " + name)
        expected[name] = entry
    actual = set()
    for path in root.rglob("*"):
        if path.is_symlink():
            raise SystemExit("Symbolic links are not permitted: " + path.name)
        relative = path.relative_to(root).as_posix()
        if path.is_file() and relative != "MANIFEST.json":
            actual.add(relative)
    if actual != set(expected):
        raise SystemExit("Inventory mismatch: missing=" + repr(sorted(set(expected) - actual))
                         + "; extra=" + repr(sorted(actual - set(expected))))
    total = 0
    for name, entry in expected.items():
        data = (root / name).read_bytes()
        if len(data) != entry["bytes"]:
            raise SystemExit("Byte-count mismatch: " + name)
        if hashlib.sha256(data).hexdigest() != entry["sha256"]:
            raise SystemExit("SHA-256 mismatch: " + name)
        total += len(data)
    if len(expected) != manifest["file_count_excluding_manifest"]:
        raise SystemExit("Manifest file count is inconsistent.")
    if total != manifest["total_bytes_excluding_manifest"]:
        raise SystemExit("Manifest total bytes are inconsistent.")
    acceptance = json.loads((root / "AUDIT_ACCEPTANCE.json").read_text())
    if acceptance["verdict"] != "PASS_WITH_EXPLICIT_SCOPE_LIMITS" or acceptance["overall_problem_status"] != "UNSOLVED":
        raise SystemExit("Unexpected mathematical acceptance scope.")
    frozen = acceptance["frozen_manuscripts"] + [acceptance["audit_report"]]
    for entry in frozen:
        name = entry["file"]
        if name not in expected:
            raise SystemExit("Audited file is absent from payload manifest: " + name)
        if any(entry[key] != expected[name][key] for key in ("bytes", "sha256")):
            raise SystemExit("Audited version differs from payload: " + name)
    source_report = json.loads((root / "SOURCE_METADATA.json").read_text())["authored_report"]
    source_name = source_report["filename"]
    if source_name not in expected or any(source_report[key] != expected[source_name][key]
                                          for key in ("bytes", "sha256")):
        raise SystemExit("Source-gate metadata differs from payload.")
    print(json.dumps({"status": "PASS", "verified_files": len(expected),
                      "verified_bytes": total, "algorithm": "SHA-256",
                      "audited_manuscripts_and_audit_match": True,
                      "source_gate_metadata_matches": True,
                      "overall_problem_status": "UNSOLVED"}, indent=2))


if __name__ == "__main__":
    main()

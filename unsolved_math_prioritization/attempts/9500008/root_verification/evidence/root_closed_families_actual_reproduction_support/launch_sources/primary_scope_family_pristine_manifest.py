"""Exact own-root membership. Only the root manifest excludes itself; no basename exemptions."""
from pathlib import Path
import argparse
import datetime
import hashlib
import json

HERE = Path(__file__).resolve().parent
SELF = "PRIMARY_SCOPE_FAMILY_MANIFEST.json"
FOREIGN_CONTROL_ROOTS = {"baseline", "nested_manifest_same_basename", "missing_first_party_checker", "foreign_pdf_corrupted"}


def is_foreign(rel):
    parts = Path(rel).parts
    return parts[0] == "foreign_sources" or (
        len(parts) >= 4 and parts[0] == "actual_manifest_controls"
        and parts[1] in FOREIGN_CONTROL_ROOTS and parts[2] == "foreign_sources")


def observed(root):
    out = {}
    for p in root.rglob("*"):
        if p.is_symlink():
            raise ValueError("Unexpected symlink: " + str(p.relative_to(root)))
        if p.is_file():
            rel = str(p.relative_to(root))
            if rel == SELF:
                continue
            b = p.read_bytes()
            out[rel] = {"bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
    return out


def build(root):
    all_files = observed(root)
    own = {k: v for k, v in all_files.items() if not is_foreign(k)}
    foreign = {k: v for k, v in all_files.items() if is_foreign(k)}
    out = {"created_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "self_exclusion_exact_relative_path": SELF,
           "first_party_members": own,
           "foreign_source_materials_and_extractions": foreign,
           "scope": "Every file in this own family root is sealed except this exact root manifest. Downloaded foreign source material is distinguished from first-party code, prose, receipts, replays, and controls; both categories have exact membership and byte checks. Nested files with the manifest basename receive no exclusion."}
    (root / SELF).write_text(json.dumps(out, indent=2) + "\n")
    return out


def verify(root):
    obj = json.loads((root / SELF).read_text())
    if obj["self_exclusion_exact_relative_path"] != SELF:
        raise ValueError("Unexpected self exclusion")
    a = obj["first_party_members"]
    f = obj["foreign_source_materials_and_extractions"]
    if set(a) & set(f) or any(is_foreign(k) for k in a) or any(not is_foreign(k) for k in f):
        raise ValueError("Foreign/first-party category mismatch")
    expected = dict(a, **f)
    actual = observed(root)
    if set(expected) != set(actual):
        raise ValueError("Exact membership mismatch: " + json.dumps({"extra": sorted(set(actual) - set(expected)), "missing": sorted(set(expected) - set(actual))}))
    for rel in expected:
        if actual[rel] != expected[rel]:
            raise ValueError("Byte seal mismatch: " + rel)
    return {"passed": True, "first_party_members": len(a), "foreign_materials": len(f),
            "exact_root_self_only": True, "nested_basename_exemptions": False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["build", "verify"])
    parser.add_argument("root", nargs="?", type=Path, default=HERE)
    args = parser.parse_args()
    try:
        if args.mode == "build":
            build(args.root.resolve())
        print(json.dumps(verify(args.root.resolve()), indent=2))
    except Exception as exc:
        print(json.dumps({"passed": False, "reason": str(exc)}, indent=2))
        raise SystemExit(1)


if __name__ == "__main__":
    main()

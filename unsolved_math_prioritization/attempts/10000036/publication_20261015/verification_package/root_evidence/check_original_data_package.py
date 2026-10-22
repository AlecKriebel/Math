#!/usr/bin/env python3
"""Check the exact frozen data-only PR838 package without extracting it.

Byte identity and archive safety do not verify mathematical claims.
"""
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import stat
import sys
import zipfile

BASE = Path(__file__).resolve().parent
SOURCE = BASE / "source"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def pairs(items):
    value = {}
    for k, v in items:
        require(k not in value, "Duplicate JSON key")
        value[k] = v
    return value


def load(data):
    return json.loads(data.decode("utf-8"), object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError("Nonfinite JSON")))


def path_ok(name):
    require(isinstance(name, str) and name, "Missing member path")
    p = PurePosixPath(name)
    require(not p.is_absolute() and "\\" not in name and ":" not in name
            and all(s not in ("", ".", "..") for s in name.split("/")), "Unsafe member path")
    require(p.suffix in (".md", ".json"), "Non-data archive member")


def identity(data, expected):
    require(len(data) == expected["bytes"] and sha(data) == expected["sha256"], "Identity mismatch")


def regular(path):
    require(not path.is_symlink() and stat.S_ISREG(path.lstat().st_mode), "Nonregular file")
    return path.read_bytes()


def inspect_zip(data, expected_rows):
    expected = {r["path"]: r for r in expected_rows}
    require(len(expected) == len(expected_rows), "Manifest duplicate")
    actual = {}
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for member in z.infolist():
            path_ok(member.filename)
            require(member.filename not in actual, "Duplicate ZIP member")
            mode = member.external_attr >> 16
            require(member.create_system == 3 and stat.S_ISREG(mode)
                    and not mode & 0o111, "Nonregular/executable ZIP member")
            require(not member.flag_bits & 1, "Encrypted ZIP member")
            require(member.filename in expected, "Unexpected ZIP member")
            require(member.file_size <= 100000, "Unexpectedly large data member")
            content = z.read(member)
            content.decode("utf-8")
            if member.filename.endswith(".json"):
                load(content)
            identity(content, expected[member.filename])
            actual[member.filename] = content
    require(set(actual) == set(expected), "ZIP inventory mismatch")
    return actual


def main():
    outer = load(regular(BASE / "SOURCE_MANIFEST.json"))
    require(outer["pr"] == 838 and outer["problem_id"] == 10000036
            and outer["frozen_head"] == "ed2de7249953ba0c1afad253adca9b820d7297c5"
            and outer["exact_gate"] == "claimed_solved", "Frozen identity mismatch")
    expected = {r["path"]: r for r in outer["files"]}
    require(len(expected) == len(outer["files"]) == 27, "Frozen duplicate/count")
    actual = set()
    for p in SOURCE.rglob("*"):
        require(not p.is_symlink(), "Symlink in frozen source")
        if not p.is_dir():
            actual.add(p.relative_to(SOURCE).as_posix())
            regular(p)
    require(actual == set(expected), "Frozen source closed inventory")
    for name, row in expected.items():
        data = regular(SOURCE / name)
        require(row["mode"] == "100644", "Unexpected Git mode")
        identity(data, row)
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        require(blob == row["git_blob"], "Frozen Git blob mismatch")
        if name.endswith(".json"):
            load(data)
    publication = load(regular(SOURCE / "PUBLICATION_MANIFEST.json"))
    inv = publication["inventory"]
    require(len(inv) == 26 and {r["path"] for r in inv} == actual - {"PUBLICATION_MANIFEST.json"},
            "Publication inventory mismatch")
    for row in inv:
        identity(regular(SOURCE / row["path"]), row)
        require(row["git_blob_sha"] == expected[row["path"]]["git_blob"], "Publication Git binding")
    specifications = [
        ("INTERNAL_THRESHOLD_10000036_AUTHOR_EXTERNAL_MANIFEST.json", "author", 6),
        ("INTERNAL_THRESHOLD_10000036_AUDIT_EXTERNAL_MANIFEST.json", "independent_audit", 4),
        ("INTERNAL_THRESHOLD_10000036_SECOND_ADVERSARIAL_REVIEW_EXTERNAL_MANIFEST.json",
         "second_independent_review", 5),
    ]
    archives = []
    acceptance = load(regular(SOURCE / "PUBLICATION_ACCEPTANCE.json"))
    for external_name, folder, count in specifications:
        external = load(regular(SOURCE / "archives" / external_name))
        archive_name = external["archive"].get("filename", external["archive"].get("path"))
        require(isinstance(archive_name, str) and "/" not in archive_name, "Unsafe archive path")
        data = regular(SOURCE / "archives" / archive_name)
        identity(data, external["archive"])
        rows = external["files"] + [external["manifest"]]
        members = inspect_zip(data, rows)
        require(len(members) == count, "Archive member count")
        for name, content in members.items():
            require("/" not in name and content == regular(SOURCE / folder / name), "Unpacked copy mismatch")
        manifest = load(members["MANIFEST.json"])
        require(manifest["problem_id"] == 10000036 and manifest["files"] == external["files"],
                "Inner/external manifest disagreement")
        matches = [r for r in acceptance["archives"] if r["archive"]["filename"] == archive_name]
        require(len(matches) == 1 and matches[0]["members"] == count, "Acceptance archive binding")
        identity(data, matches[0]["archive"])
        identity(regular(SOURCE / "archives" / external_name), matches[0]["external_manifest"])
        archives.append({"filename": archive_name, "member_count": count, "sha256": sha(data)})
    for key, name in [("author_proof", "author/PROOF.md"),
                      ("first_acceptance", "independent_audit/ACCEPTANCE.md"),
                      ("second_acceptance", "second_independent_review/SECOND_ACCEPTANCE_REPORT.md")]:
        identity(regular(SOURCE / name), acceptance[key])
    rejected = []
    for name in ("/absolute.md", "../parent.md", "x/../parent.md", "x\\bad.md", "x/./bad.md", "x//bad.md", "run.py"):
        try:
            path_ok(name)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError("Unsafe path control passed")
    for content in (b'{"a":1,"a":2}', b'{"a":NaN}', b'\xff', b'{'):
        try:
            load(content)
        except (ValueError, UnicodeDecodeError):
            rejected.append("invalid JSON " + sha(content))
        else:
            raise ValueError("JSON control passed")
    result = {"timestamp_utc": datetime.now(timezone.utc).isoformat(), "status": "PASS",
              "optimization_level": sys.flags.optimize, "source_file_count": 27,
              "publication_inventory_entries": 26, "archive_member_total": 15,
              "all_archives_match_unpacked_files": True, "acceptance_bindings_match": True,
              "negative_parser_path_controls_rejected": len(rejected), "archives": archives,
              "scope": "Static data identity and safety only. No archive member executed. No mathematical acceptance. Historical 21-control checker was not distributed and is not claimed reproduced."}
    out = BASE / ("ROOT_ORIGINAL_DATA_INTEGRITY_O.json" if sys.flags.optimize else "ROOT_ORIGINAL_DATA_INTEGRITY.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()

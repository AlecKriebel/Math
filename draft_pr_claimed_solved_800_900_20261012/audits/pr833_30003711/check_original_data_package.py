#!/usr/bin/env python3
"""Independently check the frozen data-only source package, without extraction.

This checks identity and archive structure; it cannot validate mathematics.
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
    p = PurePosixPath(name)
    require(isinstance(name, str) and name and not p.is_absolute()
            and "\\" not in name and ":" not in name
            and all(s not in ("", ".", "..") for s in name.split("/")), "Unsafe member path")
    require(p.suffix in (".md", ".json"), "Non-data archive member")


def identity(data, expected):
    require(len(data) == expected["bytes"] and sha(data) == expected["sha256"], "Identity mismatch")


def inspect_zip(data, manifest):
    expected = {r["path"]: r for r in manifest["expected_files"]}
    require(len(expected) == len(manifest["expected_files"]) == manifest["files_count"], "Manifest duplicate/count")
    actual = {}
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for member in z.infolist():
            path_ok(member.filename)
            require(member.filename not in actual, "Duplicate ZIP member")
            require(member.create_system == 3 and stat.S_ISREG(member.external_attr >> 16)
                    and not (member.external_attr >> 16) & 0o111, "Nonregular/executable ZIP member")
            require(not member.flag_bits & 1, "Encrypted ZIP member")
            content = z.read(member)
            content.decode("utf-8")
            if member.filename.endswith(".json"):
                load(content)
            require(member.filename in expected, "Unexpected ZIP member")
            identity(content, expected[member.filename])
            actual[member.filename] = content
    require(set(actual) == set(expected), "ZIP inventory mismatch")
    return actual


def main():
    outer = load((BASE / "SOURCE_MANIFEST.json").read_bytes())
    expected = {r["path"]: r for r in outer["files"]}
    actual = {str(p.relative_to(SOURCE)) for p in SOURCE.rglob("*") if p.is_file()}
    require(actual == set(expected) and len(actual) == 28, "Frozen source closed inventory")
    for name, row in expected.items():
        p = SOURCE / name
        require(not p.is_symlink() and stat.S_ISREG(p.lstat().st_mode), "Nonregular frozen source")
        data = p.read_bytes()
        identity(data, row)
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        require(blob == row["git_blob"], "Frozen Git blob mismatch")
        if p.suffix == ".json":
            load(data)
    publication = load((SOURCE / "PUBLICATION_MANIFEST.json").read_bytes())
    require({r["path"] for r in publication["inventory"]} == actual - {"PUBLICATION_MANIFEST.json"},
            "Publication inventory mismatch")
    for row in publication["inventory"]:
        identity((SOURCE / row["path"]).read_bytes(), row)
        require(row["git_blob_sha"] == expected[row["path"]]["git_blob"], "Publication Git binding")
    archives, all_members = [], {}
    author_members = None
    preservation = False
    for p in sorted((SOURCE / "archives").glob("*_EXTERNAL_MANIFEST.json")):
        m = load(p.read_bytes())
        data = (p.parent / m["archive"]["filename"]).read_bytes()
        identity(data, m["archive"])
        members = inspect_zip(data, m)
        for name, content in members.items():
            if name.startswith("flex_point_genus_30003711_second_review/"):
                target = SOURCE / "second_review" / name.split("/", 1)[1]
            elif "/independent_audit/" in name:
                target = SOURCE / "independent_audit" / name.split("/independent_audit/", 1)[1]
            else:
                target = SOURCE / "author" / name.split("/", 1)[1]
            require(target.read_bytes() == content, "Unpacked working-copy mismatch")
        if m["kind"] == "author_safe_freeze_external_manifest":
            author_members = members
        if m["kind"] == "independent_audit_safe_external_manifest":
            require(author_members is not None, "Author inventory must be read first")
            require(all(members.get(n) == v for n, v in author_members.items()), "Author preservation mismatch")
            preservation = True
        archives.append({"archive": m["archive"], "member_count": len(members)})
        all_members.update(members)
    require(len(archives) == 3 and sum(r["member_count"] for r in archives) == 21
            and len(all_members) == 16 and preservation, "Archive totals or preservation mismatch")
    acceptance = load((SOURCE / "PUBLICATION_ACCEPTANCE.json").read_bytes())
    bindings = [("proof", "author/PROOF.md"), ("first_acceptance", "independent_audit/ACCEPTANCE_AND_SCOPE.md"),
                ("second_acceptance", "second_review/ACCEPTANCE.json")]
    for key, name in bindings:
        identity((SOURCE / name).read_bytes(), acceptance[key])
    # Small parser/path falsification controls, not a replay of the undistributed historical checker.
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
            rejected.append("invalid JSON control " + sha(content))
        else:
            raise ValueError("JSON control passed")
    result = {"timestamp_utc": datetime.now(timezone.utc).isoformat(), "status": "PASS",
              "optimization_level": sys.flags.optimize, "source_file_count": 28,
              "closed_publication_inventory_entries": 27, "archive_member_total": 21,
              "distinct_archived_authored_files": 16, "all_archives_match_unpacked_files": True,
              "author_five_preserved_in_first_audit": True, "acceptance_bindings_match": True,
              "negative_parser_path_controls_rejected": len(rejected), "archives": archives,
              "scope": "Data identity and static structure only. Historical 16-control checker was not distributed and is not claimed reproduced. No archive member executed. No mathematical acceptance."}
    out = BASE / ("ROOT_ORIGINAL_DATA_INTEGRITY_O.json" if sys.flags.optimize else "ROOT_ORIGINAL_DATA_INTEGRITY.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()

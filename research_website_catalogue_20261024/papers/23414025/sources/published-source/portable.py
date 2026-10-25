#!/usr/bin/env python3
"""PR894 / 30005737: byte authentication and finite diagnostics only.
Run with Python >=3.11 -I -S -B. Authenticate this startup file independently.
No theorem, novelty, priority, visual PDF or publication approval is supplied.
"""
import argparse
import contextlib
from datetime import datetime, timezone
import hashlib
import io
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import stat
import struct
import subprocess
import sys
import tempfile
import traceback
import zipfile
import zlib

MAX_FILE = 256 * 1024 * 1024
MAX_TOTAL = 512 * 1024 * 1024
MAX_INDEX = 4 * 1024 * 1024
def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "duplicate JSON key: " + key)
            result[key] = value
        return result
    def constant(value):
        raise ValueError("nonfinite JSON constant: " + value)
    def number(value):
        result = float(value)
        require(math.isfinite(result), "overflow/nonfinite JSON number")
        return result
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant, parse_float=number)


def digest(value):
    require(type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value), "SHA256 syntax")
    return value


def safe_name(name):
    require(type(name) is str and 0 < len(name) <= 512 and
            re.fullmatch(r"[A-Za-z0-9_./-]+", name), "relative path alphabet/length")
    require(all(p not in ("", ".", "..") for p in name.split("/")) and
            not PurePosixPath(name).is_absolute() and str(PurePosixPath(name)) == name,
            "unsafe relative path: " + name)
    return name


def pin_row(row, git=False):
    keys = {"path", "bytes", "sha256"} | ({"git_blob"} if git else set())
    require(type(row) is dict and set(row) == keys, "inventory row schema")
    safe_name(row["path"])
    require(type(row["bytes"]) is int and 0 <= row["bytes"] <= MAX_FILE, "typed byte count")
    digest(row["sha256"])
    if git:
        require(type(row["git_blob"]) is str and re.fullmatch(r"[0-9a-f]{40}", row["git_blob"]), "Git blob syntax")
    return row


def rows_map(rows, git=False):
    require(type(rows) is list and 0 < len(rows) <= 10000, "inventory list")
    result, aliases = {}, set()
    for row in rows:
        pin_row(row, git)
        name = row["path"]
        require(name.casefold() not in aliases, "duplicate/aliased inventory path")
        aliases.add(name.casefold())
        result[name] = row
    require(sum(r["bytes"] for r in rows) <= MAX_TOTAL, "inventory total limit")
    for name in result:
        require(not any(str(p).casefold() in aliases for p in PurePosixPath(name).parents if str(p) != "."), "file/directory collision")
    # Reject directory spellings that alias even when leaf names differ.
    directories = {}
    for name in result:
        for p in PurePosixPath(name).parents:
            if str(p) != ".":
                key = str(p).casefold()
                require(key not in directories or directories[key] == str(p), "directory name alias")
                directories[key] = str(p)
    return result


def read_regular(path, expected_size=None, limit=MAX_FILE):
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode), "nonregular input: " + path.name)
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0))
    with os.fdopen(fd, "rb") as stream:
        info = os.fstat(stream.fileno())
        require(stat.S_ISREG(info.st_mode) and (info.st_dev, info.st_ino) == (before.st_dev, before.st_ino), "input changed during open")
        require(info.st_size <= limit and (expected_size is None or info.st_size == expected_size), "input size mismatch/limit: " + path.name)
        bound = expected_size if expected_size is not None else limit
        raw = stream.read(bound + 1)
        require(len(raw) == info.st_size and len(raw) <= bound, "bounded input read mismatch")
        after = os.fstat(stream.fileno())
        require((after.st_size, after.st_mtime_ns) == (info.st_size, info.st_mtime_ns), "input changed during read")
    return raw


def stream_pin(path, size, expected):
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode) and before.st_size == size, "source input type/size")
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0))
    h, count = hashlib.sha256(), 0
    with os.fdopen(fd, "rb") as stream:
        opened = os.fstat(stream.fileno())
        require(stat.S_ISREG(opened.st_mode) and (opened.st_dev, opened.st_ino) == (before.st_dev, before.st_ino), "source input changed")
        while True:
            chunk = stream.read(min(1024 * 1024, size + 1 - count))
            if not chunk:
                break
            h.update(chunk)
            count += len(chunk)
            require(count <= size, "source input exceeds pin")
        after = os.fstat(stream.fileno())
        require((after.st_size, after.st_mtime_ns) == (opened.st_size, opened.st_mtime_ns), "source changed during hash")
    require(count == size and h.hexdigest() == expected, "complete streaming source pin mismatch")


def within(root, name):
    safe_name(name)
    p = root
    for part in PurePosixPath(name).parts[:-1]:
        p = p / part
        require(stat.S_ISDIR(p.lstat().st_mode), "nonregular input directory: " + part)
    return root / name


def authenticate(raw, row, label):
    require(len(raw) == row["bytes"] and sha(raw) == row["sha256"], "pin mismatch: " + label)


def selected_root(path):
    require(stat.S_ISDIR(path.lstat().st_mode), "root must be ordinary directory")
    for ancestor in path.absolute().parents:
        require(stat.S_ISDIR(ancestor.lstat().st_mode), "root ancestor must be nonsymlink directory")
    return path.resolve()


def closed_tree(root, names):
    require(stat.S_ISDIR(root.lstat().st_mode), "root must be ordinary directory")
    expected = set(names)
    rows_map([{"path": n, "bytes": 0, "sha256": "0" * 64} for n in sorted(expected)])
    directories = {str(p) for n in expected for p in PurePosixPath(n).parents if str(p) != "."}
    seen = set()
    def visit(folder, prefix=""):
        with os.scandir(folder) as entries:
            for entry in entries:
                name = prefix + entry.name
                mode = entry.stat(follow_symlinks=False).st_mode
                if stat.S_ISDIR(mode):
                    require(name in directories, "unlisted directory: " + name)
                    visit(Path(entry.path), name + "/")
                else:
                    require(stat.S_ISREG(mode), "nonregular tree entry: " + name)
                    require(name in expected, "unlisted file: " + name)
                    seen.add(name)
    visit(root)
    require(seen == expected, "missing inventory file")


def zip_payloads(raw, expected, generated=False):
    # Closed representation: contiguous local records from byte zero, contiguous
    # central records, one terminal EOCD; no extraction, prefixes, gaps or trailers.
    require(type(raw) is bytes and 22 <= len(raw) <= MAX_TOTAL, "ZIP truncated/limit")
    end_at = len(raw) - 22
    end = struct.unpack_from("<4s4H2IH", raw, end_at)
    require(end[0] == b"PK\x05\x06" and end[1] == end[2] == end[7] == 0 and
            end[3] == end[4] == len(expected) and end[6] + end[5] == end_at, "ZIP end metadata/extent")
    result = {}
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        infos = archive.infolist()
        require(archive.start_dir == end[6] and not archive.comment and
                [i.filename for i in infos] == sorted(expected), "ZIP closed sorted member set")
        cursor, central = 0, end[6]
        for info in infos:
            name = safe_name(info.filename)
            want = expected[name]
            require(type(want) is bytes and len(want) <= MAX_FILE, "ZIP expected payload bound")
            mode = info.external_attr >> 16
            require(info.create_system == 3 and info.create_version == info.extract_version == 20 and
                    info.external_attr == ((stat.S_IFREG | (0o644 if generated else stat.S_IMODE(mode))) << 16) and
                    stat.S_ISREG(mode) and stat.S_IMODE(mode) in ((0o644,) if generated else (0o444, 0o644)) and
                    info.flag_bits == 0 and info.compress_type == zipfile.ZIP_DEFLATED and
                    not info.extra and not info.comment and info.volume == info.internal_attr == 0 and
                    (not generated or info.date_time == (2026, 10, 16, 0, 0, 0)), "ZIP unsafe central metadata: " + name)
            require(info.file_size == len(want) and info.header_offset == cursor and cursor + 30 <= end[6], "ZIP local offset/size")
            local = struct.unpack_from("<4s5H3I2H", raw, cursor)
            dosdate = ((info.date_time[0] - 1980) << 9) | (info.date_time[1] << 5) | info.date_time[2]
            dostime = (info.date_time[3] << 11) | (info.date_time[4] << 5) | (info.date_time[5] // 2)
            require(local[:9] == (b"PK\x03\x04", 20, info.flag_bits, 8, dostime, dosdate, info.CRC, info.compress_size, info.file_size) and local[10] == 0, "ZIP local/central metadata disagreement")
            encoded = name.encode("utf-8" if info.flag_bits & 0x800 else "cp437")
            start = cursor + 30
            require(local[9] == len(encoded) and raw[start:start + local[9]] == encoded, "ZIP local name disagreement")
            cursor = start + local[9] + info.compress_size
            require(cursor <= end[6], "ZIP local payload boundary")
            require(central + 46 <= end_at, "ZIP central truncation")
            c = struct.unpack_from("<4s6H3I5H2I", raw, central)
            require(c == (b"PK\x01\x02", (3 << 8) | 20, 20, info.flag_bits, 8, dostime, dosdate,
                    info.CRC, info.compress_size, info.file_size, len(encoded), 0, 0, 0, 0, info.external_attr, info.header_offset), "ZIP raw central disagreement")
            require(raw[central + 46:central + 46 + len(encoded)] == encoded, "ZIP raw central name")
            central += 46 + len(encoded)
            # ZipExtFile accepts unused bytes after the first DEFLATE stream.
            # Validate the complete declared raw region independently, with one
            # extra output byte as an expansion bound. EOF plus empty suffix and
            # tail are necessary even when the expected output bytes match.
            compressed = raw[start + local[9]:cursor]
            decoder = zlib.decompressobj(-15)
            inflated = decoder.decompress(compressed, len(want) + 1)
            consumed = len(compressed) - len(decoder.unused_data) - len(decoder.unconsumed_tail)
            require(inflated == want and decoder.eof and not decoder.unused_data and
                    not decoder.unconsumed_tail and consumed == info.compress_size == len(compressed),
                    "ZIP raw DEFLATE exact-consumption mismatch: " + name)
            with archive.open(info) as stream:
                payload = stream.read(len(want) + 1)
                require(not stream.read(1), "ZIP expanded bound")
            require(payload == want, "ZIP byte-exact member mismatch: " + name)
            if name.endswith(".json"):
                strict_json(payload)
            result[name] = payload
        require(cursor == end[6] and central == end_at, "ZIP local/central gap")
    return result

SOURCE_MANIFEST_SHA256 = "1d677ef16697e1e294f9f86800c10fe3189270cf2d9771a75d7c4e64954c0d1c"
FROZEN_HEAD = "401f86e018e8cc5075e37a29bae9350eb9f89c36"
ROOT_SHA256 = "8e9fba86534cfb75167f9b47a24206d6ca2e03ada94c91725b9023dd026e125b"
CHECKER_SHA256 = "c927b95210e0ce19144f0dddab2e1e18fca2520c42d94a7de1cfa00a67593446"
RESULT_PIN = (966, "2a0062610f5116c92c3689cbb2d12747260d0f42664a277cbb41aee3424046ff")
PAIR_PIN = (3524, "b27d5dbb0f92c0ab330bf44891ec4467f7d8c593cef610196cbd82d4cc6d5298")
STATEMENT_PIN = (183, "a8224e60e73ef6f78e8af57e836e4cc5246a0b1cd12d1af10393d8fd0104149e")
INPUT_PINS = {
    "catalog.json": (21735099, "891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566"),
    "problems.json": (68931837, "04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf"),
    "research_results.json": (80334822, "8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b"),
}
PRIMARY_PINS = {
    "owr2023.pdf": (348993, "e33479028da10623035810f64b50e920d9191dee800d20da30e36afa96372626"),
    "perfect-v1.pdf": (197580, "08ed658cbd8bd2979e4ec540c0a2f20df30a02fee5c3014350f306d4f878c8f3"),
    "perfect-author2024.pdf": (300408, "e33ac0e3b1bf7c0a899b813aa800fb32beb5787e8ff62e23a13f282719c1859b"),
    "rigidity-v1.pdf": (201169, "20c1adbae9647a004a1a167599683e6fedc2f0b41c6874cdd4940569eee2a332"),
    "etingof2024.pdf": (4247073, "ffb09776bafa3fa50dfc2bc83ee36b89058f98b7f80ff6fa90e2e34962cc9046"),
}
PACKAGE_SCHEMA = "post-lie-30005737-verification-v1"
CURRENT_SCHEMA = "post-lie-30005737-current-publication-v1"
LAYOUT_SCHEMA = "post-lie-30005737-current-layout-v1"
REQUIRED = {"portable.py", "root_evidence/SOURCE_MANIFEST.json", "README.md", "dependencies.json", "note.tex", "metadata.json", "zenodo-deposit.json"}
DEPENDENCIES = {
    "schema": "post-lie-30005737-dependencies-v1", "python_minimum": "3.11",
    "third_party_packages": [],
    "execution": "Selected Python interpreter and standard library only, under actual -I -S -B; diagnostic runs use actual optimize=0 and optimize=1.",
    "trusted_runtime": "The selected Python interpreter, standard library, native extensions and standard-library bytecode are trusted and not byte-pinned. No OS sandbox or general TOCTOU guarantee is supplied.",
}
SCOPE = "Closed byte authentication and exact finite diagnostics only; no mathematical proof, novelty, priority, human review, PDF visual QA or publication approval."
ROOT_RESULT = {
    "integrity": "passed", "packet_files": 18, "original_archive_members": 9,
    "later_audits": 2, "finite_diagnostic_conditions_per_run": 2896,
    "normal_and_optimized_outputs_match": True,
    "scope": "Integrity and finite diagnostics only; not a formal proof.",
}
FLAG_NAMES = ("optimize", "isolated", "no_site", "dont_write_bytecode", "ignore_environment", "safe_path")


def pin_bytes(raw):
    return {"bytes": len(raw), "sha256": sha(raw)}


def flags():
    return {name: getattr(sys.flags, name) for name in FLAG_NAMES}


def wanted_flags(mode):
    return {"optimize": mode, "isolated": 1, "no_site": 1, "dont_write_bytecode": 1, "ignore_environment": 1, "safe_path": True}


def typed_index(raw, schema):
    value = strict_json(raw)
    require(type(value) is dict and set(value) == {"schema", "problem_id", "files"} and
            type(value["schema"]) is str and value["schema"] == schema and
            type(value["problem_id"]) is str and value["problem_id"] == "30005737", "typed index identity/schema")
    return rows_map(value["files"])


def original_inputs(blobs):
    raw = blobs["root_evidence/SOURCE_MANIFEST.json"]
    require(sha(raw) == SOURCE_MANIFEST_SHA256, "immutable source manifest pin")
    m = strict_json(raw)
    require(type(m) is dict and set(m) == {"timestamp_utc", "pr", "problem_id", "original_head", "files", "completion_estimate_percent"} and
            type(m["timestamp_utc"]) is str and type(m["pr"]) is int and m["pr"] == 894 and
            type(m["problem_id"]) is str and m["problem_id"] == "30005737" and
            m["original_head"] == FROZEN_HEAD and type(m["completion_estimate_percent"]) is int and m["completion_estimate_percent"] == 5,
            "immutable source typed metadata")
    require(type(m["files"]) is list and len(m["files"]) == 18, "all18 source rows")
    plain = []
    for row in m["files"]:
        require(type(row) is dict and set(row) == {"path", "bytes", "sha256", "git_blob", "git_mode"} and
                type(row["git_mode"]) is str and row["git_mode"] == "100644", "source mode/schema")
        plain.append({k: v for k, v in row.items() if k != "git_mode"})
    pins = rows_map(plain, git=True)
    source = {name[7:]: data for name, data in blobs.items() if name.startswith("source/")}
    require(set(source) == set(pins) and sum(r["bytes"] for r in pins.values()) == 91564, "exact source inventory/bytes")
    # Authenticate ALL original bytes before parsing any original JSON or execution.
    for name, row in pins.items():
        raw = source[name]
        authenticate(raw, row, "source/" + name)
        require(hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == row["git_blob"], "immutable Git blob mismatch")
    require(sha(source["verify_publication.py"]) == ROOT_SHA256 and sha(source["authored/check_algebra.py"]) == CHECKER_SHA256,
            "immutable executable pins")
    for name, data in source.items():
        if name.endswith(".json"):
            strict_json(data)
    outer = strict_json(source["PUBLICATION_MANIFEST.json"])
    require(type(outer) is dict and set(outer) == {"problem_id", "rank", "status", "turns", "original_archive_contains_audits", "files"} and
            type(outer["problem_id"]) is int and outer["problem_id"] == 30005737 and
            type(outer["rank"]) is int and outer["rank"] == 953 and outer["status"] == "claimed_solved" and
            outer["turns"] == "1/5" and outer["original_archive_contains_audits"] is False, "original publication schema")
    listed = rows_map(outer["files"])
    require(set(listed) | {"PUBLICATION_MANIFEST.json"} == set(source) and len(listed) == 17, "original root exact18 inventory")
    for name, row in listed.items():
        authenticate(source[name], row, name)
    inner = strict_json(source["authored/MANIFEST.json"])
    require(type(inner) is dict and set(inner) == {"status", "author_approaches", "files"} and
            inner["status"] == "complete_candidate_pending_independent_review" and
            type(inner["author_approaches"]) is int and inner["author_approaches"] == 1, "original authored schema")
    payload_pins = rows_map(inner["files"])
    require(len(payload_pins) == 8 and not any("AUDIT" in n for n in payload_pins), "original eight payloads")
    archive = {"MANIFEST.json": source["authored/MANIFEST.json"]}
    for name, row in payload_pins.items():
        archive[name] = source["authored/" + name]
        authenticate(archive[name], row, "authored/" + name)
    zip_payloads(source["AUTHOR_CANDIDATE.zip"], archive)
    require((len(source["authored/CHECK_RESULTS.json"]), sha(source["authored/CHECK_RESULTS.json"])) == RESULT_PIN, "immutable diagnostic output")
    result = strict_json(source["authored/CHECK_RESULTS.json"])
    require(type(result) is dict and type(result["checks"]) is int and result["checks"] == 2896 and
            result["invalid_R_identity_detected"] is True, "diagnostic finite scope")
    h = strict_json(source["authored/SOURCE_HASHES.json"])
    require(type(h) is dict and set(h) == {"source_files_not_included", "sources"} and
            h["source_files_not_included"] is True and type(h["sources"]) is list and len(h["sources"]) == 5,
            "primary source list")
    require({(r["bytes"], r["sha256"]) for r in h["sources"]} == set(PRIMARY_PINS.values()), "primary pins agree with immutable source")
    return source


def publication_metadata(blobs):
    metadata = strict_json(blobs["metadata.json"])
    keys = {"title", "upload_type", "publication_type", "publication_date", "version", "description", "creators", "access_right", "license", "keywords", "references", "related_identifiers"}
    require(type(metadata) is dict and set(metadata) == keys, "publication metadata exact keys")
    fixed = {"title": "Post-Lie nonexistence with a semisimple target", "upload_type": "publication",
             "publication_type": "preprint", "publication_date": "2026-10-16", "version": "1.0.0", "access_right": "open", "license": "cc-by-4.0"}
    require(all(type(metadata[k]) is str and metadata[k] == v for k, v in fixed.items()), "publication metadata fixed identity")
    require(type(metadata["description"]) is str and 0 < len(metadata["description"]) <= 100000, "metadata description string/bound")
    require(type(metadata["creators"]) is list and metadata["creators"] == [{"name": "Kriebel, Alec", "affiliation": "Independent researcher", "orcid": "0009-0001-9320-500X"}], "exact sole creator")
    for key in ("keywords", "references"):
        require(type(metadata[key]) is list and len(metadata[key]) <= 1000 and all(type(v) is str and 0 < len(v) <= 20000 for v in metadata[key]), "metadata string list: " + key)
    require(type(metadata["related_identifiers"]) is list and len(metadata["related_identifiers"]) <= 1000, "related identifiers list")
    for row in metadata["related_identifiers"]:
        require(type(row) is dict and {"identifier", "relation"} <= set(row) <= {"identifier", "relation", "scheme", "resource_type"} and all(type(v) is str and 0 < len(v) <= 20000 for v in row.values()), "related identifier schema")
    deposit = strict_json(blobs["zenodo-deposit.json"])
    require(type(deposit) is dict and set(deposit) == {"metadata", "files"} and type(deposit["metadata"]) is dict and deposit["metadata"] == metadata, "deposit metadata exact copy")
    require(type(deposit["files"]) is list and deposit["files"] == [
        {"name": "post-lie-note.pdf", "path": "post-lie-note.pdf"},
        {"name": "post-lie-verification.zip", "path": "post-lie-verification.zip"}], "exact two deposit assets")
    require(strict_json(blobs["dependencies.json"]) == DEPENDENCIES, "exact standard-library dependency contract")


def package_inputs(root, external_pin):
    digest(external_pin)
    raw = read_regular(root / "package_index.json", limit=MAX_INDEX)
    require(sha(raw) == external_pin, "external index pin mismatch")
    pins = typed_index(raw, PACKAGE_SCHEMA)
    require("package_index.json" not in pins and REQUIRED <= set(pins), "required portable inventory")
    closed_tree(root, set(pins) | {"package_index.json"})
    blobs = {"package_index.json": raw}
    for name, row in pins.items():
        data = read_regular(within(root, name), row["bytes"])
        authenticate(data, row, name)
        blobs[name] = data
    # All indexed bytes now authenticated. No archival execution in this path.
    original_inputs(blobs)
    for name, data in blobs.items():
        if name.endswith(".json"):
            strict_json(data)
    require(read_regular(Path(__file__).absolute()) == blobs["portable.py"], "authenticated startup copy mismatch")
    publication_metadata(blobs)
    return blobs


def materialize(root, blobs):
    root.mkdir()
    for name, data in blobs.items():
        target = root / safe_name(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as stream:
            stream.write(data)
        target.chmod(0o644)


def deterministic_zip(blobs):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in sorted(blobs):
            info = zipfile.ZipInfo(safe_name(name), (2026, 10, 16, 0, 0, 0))
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, blobs[name], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return stream.getvalue()


def source_only(values, primary_dir=None):
    require(len(values) == 3 and all(v is not None for v in values), "all three complete corpus paths required")
    paths = dict(zip(INPUT_PINS, values))
    for path in paths.values():
        selected_root(path.absolute().parent)
    # Mandatory COMPLETE first pass before parsing or selecting ANY native record.
    for name, path in paths.items():
        stream_pin(path, *INPUT_PINS[name])
    found, receipts = {}, []
    for name, path in paths.items():
        size, expected = INPUT_PINS[name]
        raw = read_regular(path, size)
        require(sha(raw) == expected, "native input changed after complete authentication")
        data = strict_json(raw)
        if name == "research_results.json":
            require(type(data) is dict and "OWR-14298013-001" not in data, "expected absent target report")
        else:
            require(type(data) is list and all(type(r) is dict for r in data), "native corpus list")
            exact = [r for r in data if type(r.get("id")) in (str, int) and str(r["id"]) == "30005737"]
            require(len(exact) == 1, "exact target ID uniqueness")
            found[name] = exact[0]
        receipts.append({"name": name, "bytes": size, "sha256": expected, "complete_pin_before_any_extraction": True})
        del raw, data
    cat, record = found["catalog.json"], found["problems.json"]
    require(type(cat["rank"]) is int and cat["rank"] == 953 and cat["problem_number"] == record["problem_number"] == "OWR-14298013-001" and
            type(cat["title"]) is str and cat["title"] == record["title"], "canonical native target identity")
    pair = json.dumps([record, {}], sort_keys=True).encode("utf-8")
    require((len(pair), sha(pair)) == PAIR_PIN and cat["review_hash"] == PAIR_PIN[1], "entire native canonical pair")
    require(type(record["statement"]) is str, "statement string")
    statement = record["statement"].encode("utf-8")
    require((len(statement), sha(statement)) == STATEMENT_PIN and cat["statement_hash"] == STATEMENT_PIN[1], "entire native statement")
    return {"status": "PASS", "inputs": receipts, "canonical_pair": pin_bytes(pair), "statement": pin_bytes(statement),
            "target_report": "ABSENT", "archival_code_read": False, "archival_code_executed": False,
            "source_bodies_copied": False, "primary_sources": primary_only(primary_dir) if primary_dir is not None else "NOT_RUN"}


def primary_only(directory):
    directory = selected_root(directory)
    closed_tree(directory, set(PRIMARY_PINS))
    receipts = []
    for name, (size, expected) in PRIMARY_PINS.items():
        stream_pin(within(directory, name), size, expected)
        receipts.append({"name": name, "bytes": size, "sha256": expected})
    return {"status": "PASS", "pins": receipts, "technical_theorems_verified_by_hash": False, "bodies_copied": False}

# Shared recorder writes raw streams and their hashes BEFORE interpreting success.
# Failed runs are retained. This helper is current tool code, not archival code.
RECORD_COMMON = r'''
from datetime import datetime, timezone
import hashlib, json, os, subprocess, time
from pathlib import Path

def stamp(): return datetime.now(timezone.utc).isoformat()
def pin(raw): return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def write_new(path, raw):
    with path.open('xb') as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
def record_process(command, cwd, base, timeout, environment=None):
    inherited=dict(os.environ)
    removed=sorted(k for k in inherited if k.upper().startswith('PYTHON') or k=='__PYVENV_LAUNCHER__')
    selected={k:v for k,v in inherited.items() if k not in removed} if environment is None else dict(environment)
    environment_policy='PYTHON variables and __PYVENV_LAUNCHER__ removed' if environment is None else 'explicit test environment'
    started=stamp(); mono=time.monotonic_ns(); process=None; expired=False
    try:
        process=subprocess.Popen(command,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=selected)
        launched=stamp()
        try: stdout,stderr=process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            expired=True; process.kill(); stdout,stderr=process.communicate()
        ended=stamp(); elapsed=time.monotonic_ns()-mono
        rc=process.returncode
        meta={'started_utc':started,'launched_utc':launched,'ended_utc':ended,'elapsed_monotonic_ns':elapsed,
              'pid':process.pid,'returncode':rc,'timeout':expired,'stdout':pin(stdout),'stderr':pin(stderr)}
    except OSError as error:
        ended=stamp(); stdout=b''; stderr=(type(error).__name__+': '+str(error)).encode()
        meta={'started_utc':started,'ended_utc':ended,'elapsed_monotonic_ns':time.monotonic_ns()-mono,
              'pid':None,'returncode':None,'timeout':False,'launch_error_type':type(error).__name__,'stdout':pin(stdout),'stderr':pin(stderr)}
    meta['environment_policy']=environment_policy
    meta['removed_environment_keys']=removed if environment is None else []
    write_new(Path(str(base)+'.stdout.bin'),stdout)
    write_new(Path(str(base)+'.stderr.bin'),stderr)
    write_new(Path(str(base)+'.json'),(json.dumps(meta,indent=2,sort_keys=True)+'\n').encode())
    return meta,stdout,stderr
'''
exec(RECORD_COMMON)

CHILD = r'''
import hashlib, json, sys
from pathlib import Path
c=json.loads(sys.argv[1]); p=Path(c['path']); raw=p.read_bytes()
measured={n:getattr(sys.flags,n) for n in ('optimize','isolated','no_site','dont_write_bytecode','ignore_environment','safe_path')}
Path(c['measurement']).write_text(json.dumps(measured,sort_keys=True)+'\n')
if hashlib.sha256(raw).hexdigest()!=c['expected_sha256']:
    raise ValueError('CORRUPT_REJECTED_BEFORE_EXECUTION')
Path(c['began']).write_bytes(b'ORIGINAL_EXECUTION_BEGIN\n')
namespace={'__name__':'__main__' if c['kind']=='positive' else '__control__','__file__':str(p)}
sys.argv=[str(p)]
exec(compile(raw,str(p),'exec'),namespace)
if c['kind']=='semantic_negative':
    # R=I gives x*y=[x,y] and source bracket 3[x,y]; PA2 is false.
    # Both the verification mechanism and raising require() are ORIGINAL code.
    namespace['verify_pa']('semantic_negative',3,namespace['sl2'],namespace['sl2'])
    raise ValueError('INVALID_PRODUCT_WAS_ACCEPTED')
if c['kind']=='require_false':
    namespace['require'](False,'explicit_false_control')
    raise ValueError('FALSE_REQUIRE_WAS_ACCEPTED')
'''

HARNESS = r'''
import contextlib, hashlib, io, json, subprocess, sys, traceback
from pathlib import Path
c=json.loads(sys.argv[1]); root=Path(c['root']); audit=Path(c['audit']); scratch=Path(c['scratch'])
exec(c['record_common'])
def require(ok, reason):
    if not ok: raise ValueError(reason)
def flags(): return {n:getattr(sys.flags,n) for n in ('optimize','isolated','no_site','dont_write_bytecode','ignore_environment','safe_path')}
def wanted(mode): return {'optimize':mode,'isolated':1,'no_site':1,'dont_write_bytecode':1,'ignore_environment':1,'safe_path':True}
require(flags()==wanted(c['mode']),'actual root wrapper flags')
raw=(root/'verify_publication.py').read_bytes()
require(pin(raw)['sha256']==c['root_sha256'],'original root preexecution pin')
events=[]
def run_child(path,kind,mode,requested):
    seq=len(events); stem=audit/('child-%02d'%seq)
    measurement=Path(str(stem)+'.flags.json'); began=Path(str(stem)+'.began')
    config={'path':str(path),'measurement':str(measurement),'began':str(began),'kind':kind,'expected_sha256':c['checker_sha256']}
    effective=['-I','-S','-B']+(['-O'] if mode else [])
    meta,stdout,stderr=record_process([sys.executable,*effective,'-c',c['child'],json.dumps(config)],scratch,stem,120)
    # Raw files and actual rc/start/end were committed by record_process above.
    measured=json.loads(measurement.read_bytes())
    event={'kind':kind,'requested_by_original':requested,'effective_flags':effective,'measured_flags':measured,
           'compile_optimize':measured['optimize'],'original_sha256':c['checker_sha256'],
           'original_execution_began':began.exists(),'process':meta,'raw_receipt_stem':stem.name}
    write_new(Path(str(stem)+'.event.json'),(json.dumps(event,indent=2,sort_keys=True)+'\n').encode())
    events.append(event)
    require(measured==wanted(mode),'actual diagnostic flags')
    require(not meta['timeout'],'diagnostic timeout')
    if kind=='positive':
        require(meta['returncode']==0 and stderr==b'' and stdout==(root/'authored/CHECK_RESULTS.json').read_bytes(),'positive diagnostic differs')
        result=json.loads(stdout)
        require(type(result['checks']) is int and result['checks']==2896 and result['invalid_R_identity_detected'] is True,'finite diagnostic scope')
    elif kind=='semantic_negative':
        require(meta['returncode']!=0 and began.exists() and b'RuntimeError: semantic_negative: PA2' in stderr and b'INVALID_PRODUCT_WAS_ACCEPTED' not in stderr,'original PA2 did not reject invalid R=I product')
    elif kind=='require_false':
        require(meta['returncode']!=0 and began.exists() and b'RuntimeError: explicit_false_control' in stderr and b'FALSE_REQUIRE_WAS_ACCEPTED' not in stderr,'original explicit require guard disabled')
    elif kind=='corrupt':
        require(meta['returncode']!=0 and not began.exists() and b'CORRUPT_REJECTED_BEFORE_EXECUTION' in stderr,'damaged source executed')
    else: raise ValueError('unexpected child kind')
    return subprocess.CompletedProcess([],meta['returncode'],stdout,stderr)

def guarded(command,*positional,**kwargs):
    require(not positional and type(command) is list,'original nested call shape')
    index=len(events); require(index<2,'unexpected original nested child')
    requested=[] if index==0 else ['-O']
    expected=[sys.executable,*requested,str(root/'authored/check_algebra.py')]
    require(command==expected and set(kwargs)=={'stdout','stderr','check'} and kwargs['stdout']==subprocess.PIPE and kwargs['stderr']==subprocess.PIPE and kwargs['check'] is True,'original nested call contract')
    result=run_child(root/'authored/check_algebra.py','positive',index,requested)
    return subprocess.CompletedProcess(command,result.returncode,result.stdout,result.stderr)
subprocess.run=guarded
out=io.StringIO(); err=io.StringIO(); started=stamp(); exception=None
try:
    with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
        sys.argv=[str(root/'verify_publication.py')]
        exec(compile(raw,str(root/'verify_publication.py'),'exec'),{'__name__':'__main__','__file__':str(root/'verify_publication.py')})
except BaseException as error:
    exception=type(error).__name__
    traceback.print_exc(file=err)
finally:
    ended=stamp(); stdout=out.getvalue().encode(); stderr=err.getvalue().encode()
    write_new(audit/'original-root.stdout.bin',stdout); write_new(audit/'original-root.stderr.bin',stderr)
    write_new(audit/'original-root.execution.json',(json.dumps({'started_utc':started,'ended_utc':ended,
        'execution_kind':'unchanged original source inside actual measured wrapper process','exception_type':exception,
        'stdout':pin(stdout),'stderr':pin(stderr),'measured_flags':flags(),'compile_optimize':sys.flags.optimize},indent=2,sort_keys=True)+'\n').encode())
require(exception is None and stderr==b'','original root execution failed; raw receipts retained')
require(len(events)==2,'original root did not launch exactly two diagnostics')
require(json.loads(stdout)==c['root_result'],'original root semantic output')
for mode in (0,1):
    run_child(root/'authored/check_algebra.py','semantic_negative',mode,[])
    run_child(root/'authored/check_algebra.py','require_false',mode,[])
    folder=scratch/('corrupt-%d'%mode); folder.mkdir()
    path=folder/'check_algebra.py'; path.write_bytes((root/'authored/check_algebra.py').read_bytes()+b'\nCORRUPT_SOURCE_MUST_NOT_EXECUTE\n')
    run_child(path,'corrupt',mode,[])
print(json.dumps({'root_sha256':pin(raw)['sha256'],'root_flags':flags(),'root_compile_optimize':sys.flags.optimize,
    'root_stdout':pin(stdout),'root_output':json.loads(stdout),'events':events},sort_keys=True))
'''


def replay(source, receipt_directory):
    # Source bytes have already passed immutable full-packet authentication.
    # Scratch and ALL raw failure outputs persist; there is no synthetic recovery.
    frozen = receipt_directory / "frozen"
    scratch = receipt_directory / "scratch"
    audit = receipt_directory / "processes"
    unrelated = receipt_directory / "unrelated"
    materialize(frozen, source)
    scratch.mkdir(); audit.mkdir(); unrelated.mkdir()
    config = {"root": str(frozen), "scratch": str(scratch), "audit": str(audit),
              "mode": int(bool(sys.flags.optimize)), "root_sha256": ROOT_SHA256,
              "checker_sha256": CHECKER_SHA256, "root_result": ROOT_RESULT,
              "child": CHILD, "record_common": RECORD_COMMON}
    effective = ["-I", "-S", "-B"] + (["-O"] if sys.flags.optimize else [])
    meta, stdout, stderr = record_process([sys.executable, *effective, "-c", HARNESS, json.dumps(config)],
                                          unrelated, receipt_directory / "root-wrapper", 900)
    # Process streams and metadata are on disk before these first assertions.
    require(meta["returncode"] == 0 and not meta["timeout"] and stderr == b"", "authenticated root replay failed; raw process receipts retained at " + str(receipt_directory))
    receipt = strict_json(stdout)
    require(type(receipt) is dict and set(receipt) == {"root_sha256", "root_flags", "root_compile_optimize", "root_stdout", "root_output", "events"}, "replay receipt schema")
    mode = int(bool(sys.flags.optimize))
    require(receipt["root_flags"] == wanted_flags(mode) and receipt["root_compile_optimize"] == mode and
            receipt["root_sha256"] == ROOT_SHA256 and receipt["root_output"] == ROOT_RESULT, "unchanged actual root flags/output")
    expected_stdout = (json.dumps(ROOT_RESULT, indent=2, sort_keys=True) + "\n").encode()
    require(receipt["root_stdout"] == pin_bytes(expected_stdout), "original root stdout bytes")
    events = receipt["events"]
    require(type(events) is list and len(events) == 8 and [e["kind"] for e in events] == ["positive", "positive", "semantic_negative", "require_false", "corrupt", "semantic_negative", "require_false", "corrupt"], "actual nested process schedule")
    require([e["measured_flags"]["optimize"] for e in events] == [0, 1, 0, 0, 0, 1, 1, 1], "actual normal/optimized diagnostics and controls")
    for event in events:
        require(event["measured_flags"] == wanted_flags(event["measured_flags"]["optimize"]), "isolated child flags")
        if event["kind"] == "positive":
            require(event["process"]["stdout"] == {"bytes": RESULT_PIN[0], "sha256": RESULT_PIN[1]} and event["process"]["returncode"] == 0,
                    "positive original diagnostic receipt")
        else:
            require(type(event["process"]["returncode"]) is int and event["process"]["returncode"] != 0, "negative process actually failed")
    closed_tree(frozen, source)
    require(all(read_regular(within(frozen, n), len(b)) == b for n, b in source.items()), "replay modified original private copy")
    return {"status": "PASS", "label": "ORIGINAL_ROOT_AND_FINITE_DIAGNOSTICS_REPLAYED", "archival_code_executed": True,
            "original_effort": "1/5", "direct_root_wrapper_processes": 1, "unchanged_original_root_executions": 1,
            "original_requested_diagnostic_children": 2, "extra_control_children": 6,
            "positive_runs": 2, "semantic_invalid_product_rejections": 2, "explicit_require_false_rejections": 2, "corrupt_preexecution_rejections": 2,
            "originals_unchanged": True, "runtime_boundary": DEPENDENCIES["trusted_runtime"],
            "receipt_directory": str(receipt_directory), "wrapper_process": meta, "launcher": receipt}


def isolated():
    require(sys.version_info >= (3, 11), "Python>=3.11 required")
    require(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path,
            "run with actual -I -S -B")
    require(sys.flags.optimize in (0, 1), "use normal or single -O mode")


def source_options(parser):
    for name in ("catalog", "problems", "reports", "primary-dir"):
        parser.add_argument("--" + name, type=Path)


def optional_sources(args):
    values = [args.catalog, args.problems, args.reports]
    require(all(v is not None for v in values) or all(v is None for v in values), "all three corpus paths together")
    if all(v is not None for v in values):
        return source_only(values, args.primary_dir)
    return {"corpora": "NOT_RUN", "primary_sources": primary_only(args.primary_dir) if args.primary_dir is not None else "NOT_RUN"}


def guard_parent(root, blobs, parent, args):
    parent = selected_root(parent)
    directories = {""}
    for name in blobs:
        safe_name(name)
        directories.update(str(p) for p in PurePosixPath(name).parents if str(p) != ".")
    input_directories = [root / name for name in directories]
    if args.primary_dir is not None:
        input_directories.append(selected_root(args.primary_dir))
    for path in (args.catalog, args.problems, args.reports):
        if path is not None:
            input_directories.append(selected_root(path.absolute().parent))
    identities = set()
    for directory in input_directories:
        info = directory.lstat()
        require(stat.S_ISDIR(info.st_mode), "indexed input directory changed/nonregular")
        identities.add((info.st_dev, info.st_ino))
    for directory in (parent, *parent.parents):
        info = directory.stat()
        require((info.st_dev, info.st_ino) not in identities,
                "output must be outside every indexed input directory (physical device/inode alias)")
    return parent


def fresh_target(root, blobs, requested, args, filename=None):
    requested = requested.absolute()
    if filename is not None:
        require(requested.name == filename, "exact output asset filename required")
    require(not requested.exists() and not requested.is_symlink(), "output must be fresh; no overwrite")
    parent = guard_parent(root, blobs, requested.parent, args)
    out = parent / requested.name
    require(not out.exists() and not out.is_symlink(), "output appeared during preflight")
    return out


def receipt_location(root, blobs, args):
    if args.receipt_dir is not None:
        out = fresh_target(root, blobs, args.receipt_dir, args)
        out.mkdir(mode=0o700)
        return out
    parent = Path(tempfile.gettempdir()).resolve(strict=True)
    guard_parent(root, blobs, parent, args)
    return Path(tempfile.mkdtemp(prefix="post-lie-30005737-replay-", dir=parent))


def verify_result(root, blobs, index_pin, args, guard_blobs=None):
    originals = original_inputs(blobs)
    source_check = optional_sources(args)
    if args.verify_only:
        require(args.receipt_dir is None, "--verify-only creates zero archival process receipts; omit --receipt-dir")
        replay_result = {"status": "NOT_RUN", "archival_code_executed": False,
                         "label": "VERIFY_ONLY_BYTE_AUTHENTICATION_NO_ARCHIVAL_EXECUTION"}
    else:
        replay_result = replay(originals, receipt_location(root, blobs if guard_blobs is None else guard_blobs, args))
    return {"status": "PASS", "scope": SCOPE, "index_sha256": index_pin, "package_member_count": len(blobs),
            "original_files": 18, "original_bytes": 91564, "original_effort": "1/5",
            "source_authentication": source_check, "replay": replay_result}


def current_inputs(root, external_pin):
    digest(external_pin)
    raw = read_regular(root / "CURRENT_PUBLICATION_MANIFEST.json", limit=MAX_INDEX)
    require(sha(raw) == external_pin, "external current manifest pin mismatch")
    pins = typed_index(raw, CURRENT_SCHEMA)
    require("CURRENT_PUBLICATION_MANIFEST.json" not in pins and
            {"CURRENT_PUBLICATION.json", "portable.py", "metadata.json", "zenodo-deposit.json", "note.tex", "post-lie-note.pdf", "post-lie-verification.zip"} <= set(pins),
            "current required inventory")
    closed_tree(root, set(pins) | {"CURRENT_PUBLICATION_MANIFEST.json"})
    blobs = {"CURRENT_PUBLICATION_MANIFEST.json": raw}
    for name, row in pins.items():
        data = read_regular(within(root, name), row["bytes"])
        authenticate(data, row, name)
        blobs[name] = data
    require(read_regular(Path(__file__).absolute()) == blobs["portable.py"], "current startup copy mismatch")
    layout = strict_json(blobs["CURRENT_PUBLICATION.json"])
    require(type(layout) is dict and set(layout) == {"schema", "problem_id", "portable_prefix", "zip_path", "pdf_path", "tex_path"} and
            layout == {"schema": LAYOUT_SCHEMA, "problem_id": "30005737", "portable_prefix": "verification",
                       "zip_path": "post-lie-verification.zip", "pdf_path": "post-lie-note.pdf", "tex_path": "note.tex"}, "exact typed current layout")
    prefix = "verification/"
    portable = {name[len(prefix):]: data for name, data in blobs.items() if name.startswith(prefix)}
    require("package_index.json" in portable and len(portable["package_index.json"]) <= MAX_INDEX, "portable index exists/bounded")
    inner_pins = typed_index(portable["package_index.json"], PACKAGE_SCHEMA)
    require("package_index.json" not in inner_pins and REQUIRED <= set(inner_pins) and
            set(portable) == set(inner_pins) | {"package_index.json"}, "current portable closed inventory")
    for name, row in inner_pins.items():
        authenticate(portable[name], row, "portable " + name)
    original_inputs(portable)
    for name, data in blobs.items():
        if name.endswith(".json"):
            strict_json(data)
    publication_metadata(portable)
    for name in ("portable.py", "metadata.json", "zenodo-deposit.json", "note.tex"):
        require(blobs[name] == portable[name], "outer/portable exact copy mismatch: " + name)
    # Deliberately HEADER ONLY. No claim of a valid, complete or visually reviewed PDF.
    require(blobs["post-lie-note.pdf"].startswith(b"%PDF-"), "PDF header required (visual QA separate)")
    zip_payloads(blobs["post-lie-verification.zip"], portable, generated=True)
    require(deterministic_zip(portable) == blobs["post-lie-verification.zip"], "same-runtime exact ZIP rebuild differs")
    return blobs, portable


def build_output(root, blobs, index_pin, args):
    # Mandatory preflight BEFORE optional native parsing, replay, scratch or output.
    out = fresh_target(root, blobs, args.output, args, "post-lie-verification.zip")
    result = verify_result(root, blobs, index_pin, args)
    raw = deterministic_zip(blobs)
    zip_payloads(raw, blobs, generated=True)
    require(raw == deterministic_zip(blobs), "same-runtime independent ZIP rebuild")
    # Hard-link a fresh fsynced temporary file: no replace/overwrite semantics.
    with tempfile.TemporaryDirectory(prefix="post-lie-30005737-build-", dir=out.parent) as td:
        candidate = Path(td) / out.name
        fd = os.open(candidate, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o644)
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw); stream.flush(); os.fsync(stream.fileno())
        candidate.chmod(0o644)
        require(not out.exists() and not out.is_symlink(), "output appeared during build")
        os.link(candidate, out, follow_symlinks=False)
    return {"status": "PASS", "scope": SCOPE, "archive_name": out.name, "bytes": len(raw), "sha256": sha(raw),
            "member_count": len(blobs), "fixed_zip_timestamp": "2026-10-16T00:00:00Z", "same_runtime_exact_rebuild": True,
            "python_version": sys.version.split()[0], "zlib_runtime": zlib.ZLIB_RUNTIME_VERSION,
            "reproducibility_scope": "Same input bytes, Python ZIP implementation and zlib; cross-runtime compressed bytes are not promised.",
            "verification": result}


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    sub = parser.add_subparsers(dest="command", required=True)
    for mode in ("verify", "build", "current"):
        p = sub.add_parser(mode, allow_abbrev=False)
        p.add_argument("external_sha256", help="Independently supplied index/manifest SHA256")
        p.add_argument("--root", type=Path, default=Path(__file__).absolute().parent)
        p.add_argument("--receipt-dir", type=Path, help="Fresh directory outside all input directories; retains raw process evidence, including failures")
        if mode != "build":
            p.add_argument("--verify-only", action="store_true", help="Authenticate bytes; execute zero archival code")
        else:
            p.add_argument("output", type=Path)
            p.set_defaults(verify_only=False)
        source_options(p)
    p = sub.add_parser("source-only", allow_abbrev=False)
    source_options(p)
    args = parser.parse_args()
    if args.command == "source-only":
        result = source_only([args.catalog, args.problems, args.reports], args.primary_dir)
    elif args.command == "current":
        root = selected_root(args.root)
        blobs, portable = current_inputs(root, args.external_sha256)
        result = {"status": "PASS", "scope": SCOPE, "current_manifest_sha256": args.external_sha256,
                  "outer_files": len(blobs), "same_runtime_exact_zip_rebuild": True,
                  "pdf_validation": "HEADER_ONLY", "visual_qa": "SEPARATE_REVIEW_REQUIRED",
                  "portable": verify_result(root, portable, sha(portable["package_index.json"]), args, blobs)}
    else:
        root = selected_root(args.root)
        blobs = package_inputs(root, args.external_sha256)
        result = build_output(root, blobs, args.external_sha256, args) if args.command == "build" else verify_result(root, blobs, args.external_sha256, args)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        isolated(); main()
    except (ValueError, OSError, KeyError, TypeError, RuntimeError, OverflowError, RecursionError,
            zipfile.BadZipFile, zlib.error, subprocess.TimeoutExpired, UnicodeError, struct.error) as exc:
        print(json.dumps({"status": "REJECTED", "reason": str(exc)}, sort_keys=True)); sys.exit(1)

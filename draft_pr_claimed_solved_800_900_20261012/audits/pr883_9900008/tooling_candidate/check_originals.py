#!/usr/bin/env python3
"""PR883 artifact authentication and finite replay only. Authenticate startup independently.
Standard library; no novelty, mathematical-proof, human-review or publication approval.
"""
import argparse
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
import zipfile
import zlib

MAX_FILE = 256 * 1024 * 1024
MAX_TOTAL = 512 * 1024 * 1024
MAX_INDEX = 4 * 1024 * 1024
SOURCE_MANIFEST_SHA256 = "53bba0a85fa099146f7bb6d7520bc8a3a423894b702a9e8e4cb9f63ded3a48ab"
FROZEN_HEAD = "af25d26e21945a1a132aace5e600485152777070"
REQUIRED = {"check_originals.py", "verify_package.py", "build_verification.py", "root_evidence/SOURCE_MANIFEST.json"}


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
    require(len(raw) >= 22, "ZIP truncated")
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
                    info.flag_bits in (0, 0x800) and info.compress_type == zipfile.ZIP_DEFLATED and
                    not info.extra and not info.comment and info.volume == info.internal_attr == 0 and
                    (not generated or info.date_time == (2026, 10, 15, 0, 0, 0)), "ZIP unsafe central metadata: " + name)
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


def package_inputs(root, index_sha256, startup=None):
    digest(index_sha256)
    raw = read_regular(root / "package_index.json", limit=MAX_INDEX)
    require(sha(raw) == index_sha256, "external index pin mismatch")
    index = strict_json(raw)
    require(type(index) is dict and set(index) == {"schema", "problem_id", "files"} and
            index["schema"] == "diffuse-9900008-verification-v1" and index["problem_id"] == "9900008", "portable typed identity/schema")
    pins = rows_map(index["files"])
    require("package_index.json" not in pins and REQUIRED <= set(pins), "portable required inventory")
    closed_tree(root, set(pins) | {"package_index.json"})
    blobs = {"package_index.json": raw}
    for name, row in pins.items():
        data = read_regular(within(root, name), row["bytes"])
        authenticate(data, row, name)
        if name.endswith(".json"):
            strict_json(data)
        blobs[name] = data
    if startup:
        require(read_regular(Path(__file__).resolve()) == blobs[startup], "startup copy mismatch")
    return pins, blobs


def materialize(root, blobs):
    root.mkdir()
    for name, data in blobs.items():
        target = root / safe_name(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as stream:
            stream.write(data)
        target.chmod(0o644)


def isolated():
    require(sys.version_info >= (3, 10), "Python >=3.10 required")
    require(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode, "run with -I -S -B")


def rejected_main(main):
    try:
        isolated()
        main()
    except (ValueError, OSError, KeyError, TypeError, RuntimeError, OverflowError, RecursionError,
            zipfile.BadZipFile, zlib.error, subprocess.TimeoutExpired, UnicodeError, struct.error) as exc:
        print(json.dumps({"status": "REJECTED", "reason": str(exc)}, sort_keys=True))
        sys.exit(1)

from fractions import Fraction

PAIR_PIN = (5255, "5ccf640125437cbff98966972b50bc5f73f19e1ae1735dff8a49829cfbcdc42a")
STATEMENT_PIN = "85140471a18e2a6974b1e984ead6f94e6954f1d619201d414dc8be50244c8c54"
INPUT_PINS = {
    "catalog.json": (21735099, "891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566"),
    "problems.json": (68931837, "04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf"),
    "research_results.json": (80334822, "8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b"),
    "some-open-probability-problems.pdf": (107028, "efe6b6e78e36185a2b278ba0cf5593c2e92f43b479f80159d6f6b7ecc4f6efaf"),
    "0906.2062.pdf": (307591, "0a4c4813cef44e99c232d0687aa704554248675c621755be85568d0588999719"),
    "1405.7566.pdf": (221490, "b265c6d7984627f4b186ffbef8efa8faf75a94db674f55ae1333698d20c7c0cb"),
    "2112.13053.pdf": (237659, "f1400d56b382b86dd4e0740093d53744b313c91dc6cf9512607aa5cfdfaac18c"),
    "2303.05137.pdf": (166912, "5de5f2453372883da6c769c4ef9d78cf909360bc8ca21406f40c22111253ff85"),
}
BUNDLES = [
    ("DIFFUSE_MASS_9900008_AUTHOR_SAFE_FREEZE.zip", "author", 8),
    ("DIFFUSE_MASS_9900008_FRESH_REVIEW_ACCEPTED_SAFE.zip", "review2", 7),
]


def certificate_typed(data):
    strings = {"schema", "problem_id", "period", "root_phase", "equivariance", "allocation_randomness", "unit_square_mass", "shifted_heavy_root_probability", "original_heavy_root_probability"}
    keys = strings | {"dimension", "source_coset_count", "line_offsets", "line_weights", "expected_preserving_target_labels", "normalized_palm_phase_weights"}
    require(type(data) is dict and set(data) == keys, "certificate keys")
    require(all(type(data[k]) is str for k in strings), "certificate typed strings")
    require(data["schema"] == "periodic-diffuse-allocation-counterexample-v1" and data["problem_id"] == "9900008", "certificate identity")
    require(type(data["dimension"]) is int and data["dimension"] == 2 and type(data["source_coset_count"]) is int and data["source_coset_count"] == 2, "certificate typed integers")
    for key in ("line_offsets", "line_weights", "normalized_palm_phase_weights"):
        require(type(data[key]) is list and len(data[key]) == 2 and all(type(x) is str for x in data[key]), "certificate rational array schema")
    rationals = [data[k] for k in ("period", "root_phase", "unit_square_mass", "shifted_heavy_root_probability", "original_heavy_root_probability")]
    rationals += data["line_offsets"] + data["line_weights"] + data["normalized_palm_phase_weights"]
    for value in rationals:
        require(len(value) <= 128 and re.fullmatch(r"-?[0-9]+(?:/[1-9][0-9]*)?", value), "certificate rational syntax")
        Fraction(value)
    labels = data["expected_preserving_target_labels"]
    require(type(labels) is list and len(labels) == 1 and type(labels[0]) is list and len(labels[0]) == 2 and
            all(type(x) is int for x in labels[0]) and labels == [[0, 1]], "certificate typed preserving labels")
    return data


def original_inputs(blobs):
    raw = blobs["root_evidence/SOURCE_MANIFEST.json"]
    require(sha(raw) == SOURCE_MANIFEST_SHA256, "frozen source manifest external pin")
    m = strict_json(raw)
    require(type(m) is dict and set(m) == {"timestamp_utc", "problem_id", "pr", "frozen_head", "source_prefix", "files"} and
            type(m["timestamp_utc"]) is str and type(m["problem_id"]) is int and m["problem_id"] == 9900008 and
            type(m["pr"]) is int and m["pr"] == 883 and m["frozen_head"] == FROZEN_HEAD and
            m["source_prefix"] == "unsolved_math_prioritization/attempts/9900008/", "frozen source typed identity")
    pins = rows_map(m["files"], git=True)
    require(len(pins) == 26 and sum(r["bytes"] for r in pins.values()) == 211771, "frozen source count/bytes")
    source = {name[7:]: data for name, data in blobs.items() if name.startswith("source/")}
    require(set(source) == set(pins), "frozen source closed membership")
    for name, row in pins.items():
        data = source[name]
        authenticate(data, row, "source/" + name)
        require(hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest() == row["git_blob"], "Git blob mismatch")
        if name.endswith(".json"):
            strict_json(data)
    outer = strict_json(source["PUBLICATION_MANIFEST.json"])
    require(type(outer) is dict and set(outer) == {"schema", "files"} and outer["schema"] == "diffuse-9900008-publication-manifest-v1", "historical publication schema")
    outer_pins = rows_map(outer["files"])
    require(set(outer_pins) == set(source) - {"PUBLICATION_MANIFEST.json"}, "historical outer membership")
    for name, row in outer_pins.items():
        authenticate(source[name], row, "historical publication " + name)
    archives = []
    for archive_name, folder, count in BUNDLES:
        members = {name[len(folder) + 1:]: data for name, data in source.items() if name.startswith(folder + "/")}
        require(len(members) == count and all("/" not in name for name in members), "historical archive membership")
        zip_payloads(source["archives/" + archive_name], members)
        archives.append({"archive": archive_name, "members": count, "byte_exact": True})
    for folder, filename, schema in [("author", "MANIFEST.json", "diffuse-mass-safe-manifest-v1"), ("review2", "REVIEW_MANIFEST.json", "fresh-independent-review-safe-manifest-v1")]:
        inner = strict_json(source[folder + "/" + filename])
        require(type(inner) is dict and set(inner) == {"schema", "files"} and inner["schema"] == schema, "historical inner schema")
        inner_pins = rows_map(inner["files"])
        actual = {name[len(folder) + 1:] for name in source if name.startswith(folder + "/")}
        require(actual == set(inner_pins) | {filename} and all("/" not in n for n in inner_pins), "historical inner closed membership")
        for name, row in inner_pins.items():
            authenticate(source[folder + "/" + name], row, "historical inner " + name)
    certificate_typed(strict_json(source["author/certificate.json"]))
    acceptance = strict_json(source["review2/ACCEPTANCE.json"])
    require(type(acceptance) is dict and acceptance["decision"] == "ACCEPTED_WITH_REQUIRED_SOURCE_CREDIT_ADDENDUM" and
            acceptance["problem_id"] == "9900008" and acceptance["mathematical_verdict"] == "PASS" and
            type(acceptance["mathematical_repair_required"]) is bool and acceptance["mathematical_repair_required"] is False,
            "historical acceptance typed scope")
    for key, name in [("frozen_author_archive", "archives/" + BUNDLES[0][0]), ("accepted_unchanged_proof", "author/PROOF.md"), ("reviewed_original_source_audit", "author/SOURCE_AUDIT.md"), ("acceptance_report", "review2/AUDIT.md"), ("required_credit_addendum", "CREDIT_ADDENDUM.md"), ("verification_metadata", "review2/REVIEW_METADATA.json")]:
        r = acceptance[key]
        require(type(r) is dict and set(r) == {"filename", "bytes", "sha256"} and r["filename"] == PurePosixPath(name).name, "acceptance row schema/filename")
        row = {"path": name, "bytes": r["bytes"], "sha256": r["sha256"]}
        pin_row(row)
        authenticate(source[name], row, "acceptance " + name)
    require(source["CREDIT_ADDENDUM.md"] == source["review2/CREDIT_ADDENDUM.md"], "credit copies differ")
    return source, archives


def supplied_inputs(values):
    catalog, problems, reports, pdf_dir = values
    pdf_dir = selected_root(pdf_dir)
    paths = dict(zip(("catalog.json", "problems.json", "research_results.json"), (catalog, problems, reports)))
    paths.update({name: within(pdf_dir, name) for name in INPUT_PINS if name.endswith(".pdf")})
    found = {}
    receipts = []
    for name, path in paths.items():
        size, expected = INPUT_PINS[name]
        stream_pin(path, size, expected)
        raw = read_regular(path, size)
        require(sha(raw) == expected, "source parse copy differs from streaming pin")
        if name.endswith(".pdf"):
            require(raw.startswith(b"%PDF-"), "primary PDF magic")
        else:
            data = strict_json(raw)
            if name == "research_results.json":
                require(type(data) is dict and "AMR-098-0008" in data and type(data["AMR-098-0008"]) is dict, "exact report schema")
                found[name] = data["AMR-098-0008"]
            else:
                require(type(data) is list and all(type(row) is dict for row in data), "corpus record-array schema")
                exact = [row for row in data if type(row.get("id")) in (str, int) and str(row["id"]) == "9900008"]
                require(len(exact) == 1, "strict exact-ID uniqueness")
                found[name] = exact[0]
            del data
        del raw
        receipts.append({"name": name, "bytes": size, "sha256": expected, "streamed_complete_pin": True})
    cat, record, report = (found[n] for n in ("catalog.json", "problems.json", "research_results.json"))
    require(type(cat["rank"]) is int and cat["rank"] == 938 and cat["problem_number"] == record["problem_number"] == "AMR-098-0008" and
            type(cat["title"]) is str and cat["title"] == record["title"], "canonical target identity")
    pair = json.dumps([record, report], sort_keys=True).encode()
    require((len(pair), sha(pair)) == PAIR_PIN and cat["review_hash"] == PAIR_PIN[1], "entire canonical record/report pair")
    require(type(record["statement"]) is str and sha(record["statement"].encode()) == cat["statement_hash"] == STATEMENT_PIN, "entire statement binding")
    return {"status": "PASS", "inputs": receipts, "canonical_pair_bytes": len(pair), "canonical_pair_sha256": sha(pair), "statement_sha256": STATEMENT_PIN, "archival_source_checker_exists": False}


# This current harness executes an unchanged authenticated archival body. The
# reviewed interceptor allows only its exact eight author commands and injects
# mandatory interpreter isolation. It does not provide a sandbox.
PUBLICATION_HARNESS = r'''import contextlib
import io
import json
from pathlib import Path
import runpy
import subprocess
import sys
root = Path(sys.argv[1]).resolve()
script = root / "check_publication.py"
original_run = subprocess.run
calls = []
def guarded(command, **kwargs):
    if not (type(command) is list and command[0] == sys.executable and command[-2] == str(root / "author/verify.py") and command[-1] in ("--self-test", "--integrity") and command[1:-2] in ([], ["-O"], ["-I"], ["-I", "-O"])):
        raise ValueError("unallowlisted archival child command")
    effective = [sys.executable, "-I", "-S", "-B"] + (["-O"] if "-O" in command[1:-2] else []) + command[-2:]
    result = original_run(effective, timeout=90, **kwargs)
    calls.append({"requested_flags": command[1:-2], "effective_flags": effective[1:-2], "argument": command[-1], "returncode": result.returncode})
    return result
subprocess.run = guarded
sys.argv = [str(script), "--self-test"]
output = io.StringIO()
with contextlib.redirect_stdout(output):
    runpy.run_path(str(script), run_name="__main__")
if len(calls) != 8:
    raise ValueError("archival publication child count")
print(json.dumps({"archival_stdout": output.getvalue(), "actual_children": calls}, sort_keys=True))
'''


def replay(blobs, values=None, verify_only=False):
    source, archives = original_inputs(blobs)
    source_receipt = supplied_inputs(values) if values else "NOT_RUN"
    expected_self = source["review2/checker_rerun.json"]
    expected_integrity = (json.dumps({"status": "pass", "verified_files": 7}, indent=2, sort_keys=True) + "\n").encode()
    expected_publication = strict_json(source["PUBLICATION_CHECKS.json"])["runs"]
    require(type(expected_publication) is list and len(expected_publication) == 4 and all(row["result"] == expected_publication[0]["result"] for row in expected_publication), "historical publication result consistency")
    expected_publication_raw = (json.dumps(expected_publication[0]["result"], indent=2, sort_keys=True) + "\n").encode()
    self_data = strict_json(expected_self)
    require(self_data["status"] == "pass" and self_data["quotient_target_cases"] == 9 and self_data["translation_pair_exact_samples"] == 361 and self_data["unit_window_exact_samples"] == 530 and
            len(self_data["self_test"]["negative_controls"]) == 18 and len(self_data["self_test"]["positive_variants"]) == 2 and
            all(type(r["rejected"]) is bool and r["rejected"] for r in self_data["self_test"]["negative_controls"]), "historical finite invariants")
    direct, nested = [], []
    if not verify_only:
        with tempfile.TemporaryDirectory(prefix="diffuse authenticated replay ") as td:
            work = Path(td)
            relocated = work / "frozen"
            materialize(relocated, source)
            unrelated = work / "unrelated"
            unrelated.mkdir()
            for optimized in (False, True):
                flags = ["-I", "-S", "-B"] + (["-O"] if optimized else [])
                for argument, expected in [("--self-test", expected_self), ("--integrity", expected_integrity)]:
                    proc = subprocess.run([sys.executable, *flags, str(relocated / "author/verify.py"), argument], cwd=unrelated, capture_output=True, timeout=90)
                    require(proc.returncode == 0 and not proc.stderr and proc.stdout == expected, "archival author exact replay failed")
                    direct.append({"script": "author/verify.py", "argument": argument, "flags": flags, "returncode": 0, "stdout_bytes": len(proc.stdout), "stdout_sha256": sha(proc.stdout), "exact_historical_output": True})
                proc = subprocess.run([sys.executable, *flags, "-c", PUBLICATION_HARNESS, str(relocated)], cwd=unrelated, capture_output=True, timeout=700)
                require(proc.returncode == 0 and not proc.stderr, "guarded archival publication replay failed")
                receipt = strict_json(proc.stdout)
                output = receipt["archival_stdout"].encode()
                require(output == expected_publication_raw, "archival publication exact output mismatch")
                children = receipt["actual_children"]
                expected_modes = [[], ["-O"], ["-I"], ["-I", "-O"]]
                require(type(children) is list and len(children) == 8, "nested archival child count")
                for i, child in enumerate(children):
                    requested = expected_modes[i // 2]
                    require(child == {"requested_flags": requested, "effective_flags": ["-I", "-S", "-B"] + (["-O"] if "-O" in requested else []), "argument": ("--self-test" if i % 2 == 0 else "--integrity"), "returncode": 0}, "nested archival exact mode contract")
                    nested.append({"publication_optimized": optimized, **child})
                direct.append({"script": "check_publication.py", "argument": "--self-test", "flags": flags, "returncode": 0, "stdout_bytes": len(output), "stdout_sha256": sha(output), "exact_historical_output": True, "nested_children": 8, "isolation_injected_by_current_harness": True})
            closed_tree(relocated, source)
            for name, raw in source.items():
                require(read_regular(within(relocated, name), len(raw)) == raw, "archival replay modified frozen copy")
        require(len(direct) == 6 and len(nested) == 16, "exact current replay counts")
    return {"status": "PASS", "scope": "Frozen bytes and finite diagnostics only; no proof, priority, novelty or publication approval.", "original_files": 26, "original_bytes": 211771, "archives": archives,
            "finite_diagnostics": "NOT_RUN" if verify_only else "PASS", "direct_subprocess_count": len(direct), "nested_author_subprocess_count": len(nested), "total_archival_subprocess_count": len(direct) + len(nested), "direct_receipts": direct, "nested_receipts": nested,
            "archival_publication_body_executed_unchanged": not verify_only, "archival_subprocess_isolation_injected": not verify_only,
            "historical_executable_audit_replayed": False, "historical_executable_audit_distributed": False, "source_authentication": source_receipt,
            "original_artifacts_changed": False, "source_fixtures_copied": False}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("index_sha256")
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    p.add_argument("--verify-only", action="store_true")
    for name in ("catalog", "problems", "reports", "pdf-dir"):
        p.add_argument("--" + name, type=Path)
    args = p.parse_args()
    values = [args.catalog, args.problems, args.reports, args.pdf_dir]
    require(all(values) or not any(values), "all four source locations required together")
    _, blobs = package_inputs(selected_root(args.root), args.index_sha256, "check_originals.py")
    print(json.dumps(replay(blobs, values if all(values) else None, args.verify_only), sort_keys=True, indent=2))


if __name__ == "__main__":
    rejected_main(main)

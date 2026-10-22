#!/usr/bin/env python3
"""PR888 artifact authentication and finite replay only. Authenticate startup independently.
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
SOURCE_MANIFEST_SHA256 = "49a72d6bf90d3a74be69ed855c7a9cfc0f3b1d83a4e4e3ce997c0ca7c07d1cbc"
FROZEN_HEAD = "a7571ddbbbe2de3600b96bd7ccccf86e4d5748e7"
REQUIRED = {"portable.py", "root_evidence/SOURCE_MANIFEST.json", "README.md", "dependencies.json", "note.tex", "metadata.json", "zenodo-deposit.json"}


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


PACKAGE_SCHEMA = "rank-two-fano-30005079-verification-v1"
CURRENT_SCHEMA = "rank-two-fano-30005079-current-publication-v1"
LAYOUT_SCHEMA = "rank-two-fano-30005079-current-layout-v1"
ROOT_SHA = "0b90c28e34e309823c10a1704b57b935f2058820be867243dcdfa3cb7803719f"
PAIR_PIN = (5415, "6bbb2826e583f9ccbbb38411ce780e865c0b9564b74bf9f6eca5250f4b06e083")
STATEMENT_PIN = (126, "89284283d8e9e26eea1e01f6862da8c4ebd61a27bc03a36512d29cb746e9f0d3")
INPUT_PINS = {
    "catalog.json": (21735099, "891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566"),
    "problems.json": (68931837, "04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf"),
    "research_results.json": (80334822, "8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b"),
}
PRIMARY_PINS = {
    "owr2022_17.pdf": (1032709, "c997329409f016d06867ecc06dd38c59cea4919aa9ecf34791ed6a95f63345ec"),
    "miao_wang_solitons_v4.pdf": (433443, "2548f933f5d2ddb4013d5f4e1c6ea938aeb9acc518f66c72f6a7a19ed631b6d4"),
    "miao_wang_optimal_v2.pdf": (538390, "85285e55a256fe342d511f716530ed790801d695bdd5f21090ff9d56039b8049"),
    "han_li_optimal_arxiv.pdf": (558188, "939691d9bd0c24444f43b944b91c1ac9684fef628d3b23393cc7f6fd3b5db0ff"),
    "han_li_gytd.pdf": (641357, "cd44c6a91351619ffc41aae32bba1d144afb6f9eda11f4dbee74f3677502e9a6"),
    "wang_zhu_toric.pdf": (221336, "93aa63348add332cca1df8519bd864065f1956ae5f898e09065651d5f92245b1"),
    "BLXZ_2103.15278v2.pdf": (443588, "8d56f0d92d9146ea85c53be8c04fc02e90f4b09a57fc3f591a996d1b040c1351"),
}
CHECKERS = [
    ("checks/verify_construction.py", "checks/CHECK_RESULTS.json"),
    ("audits/reviewer_b/independent_checks.py", "audits/reviewer_b/INDEPENDENT_CHECK_RESULTS.json"),
]
WHEELS = [
    {"filename":"sympy-1.14.0-py3-none-any.whl", "bytes":6299353,
     "sha256":"e091cc3e99d2141a0ba2847328f5479b05d94a6635cb96148ccb3f34671bd8f5",
     "url":"https://files.pythonhosted.org/packages/a2/09/77d55d46fd61b4a135c444fc97158ef34a095e5681d0a6c10b75bf356191/sympy-1.14.0-py3-none-any.whl"},
    {"filename":"mpmath-1.3.0-py3-none-any.whl", "bytes":536198,
     "sha256":"a0b2b9fe80bbcd81a6647ff13108738cfb482d481d826cc0e02f5b35e5c88d2c",
     "url":"https://files.pythonhosted.org/packages/43/e3/7d92a15f894aa0c9c4b49b8ee9ac9850d6e63b03c9c32c0367a13ae62209/mpmath-1.3.0-py3-none-any.whl"},
]
DEPENDENCIES = {
    "schema":"rank-two-fano-30005079-dependencies-v1", "python_minimum":"3.11",
    "versions":{"sympy":"1.14.0", "mpmath":"1.3.0"}, "wheels":WHEELS,
    "execution":"Explicit local authenticated wheels imported directly as ZIPs under -I -S -B; no automatic download or installation.",
    "trusted_runtime":"The selected CPython interpreter and its standard library, including native extensions and any standard-library bytecode, are trusted and are not byte-pinned by this tool. No OS sandbox or formal proof verifier is supplied.",
}
SCOPE = "Closed byte authentication and finite auxiliary diagnostics only; no proof, priority, novelty, human-review or publication approval."


def typed_index(raw, schema):
    value = strict_json(raw)
    require(type(value) is dict and set(value) == {"schema", "problem_id", "files"} and
            type(value["schema"]) is str and value["schema"] == schema and
            type(value["problem_id"]) is str and value["problem_id"] == "30005079", "typed index identity/schema")
    return rows_map(value["files"])


def original_inputs(blobs):
    raw = blobs["root_evidence/SOURCE_MANIFEST.json"]
    require(sha(raw) == SOURCE_MANIFEST_SHA256, "immutable source manifest pin")
    m = strict_json(raw)
    require(type(m) is dict and set(m) == {"timestamp_utc","pr","problem_id","head","source_prefix","files","total_bytes","scope"} and
            type(m["timestamp_utc"]) is str and type(m["pr"]) is int and m["pr"] == 888 and
            m["problem_id"] == "30005079" and m["head"] == FROZEN_HEAD and
            m["source_prefix"] == "unsolved_math_prioritization/attempts/30005079/" and
            type(m["total_bytes"]) is int and m["total_bytes"] == 98055 and type(m["scope"]) is str,
            "immutable source typed metadata")
    require(type(m["files"]) is list and len(m["files"]) == 21, "all21 source rows")
    plain = []
    for row in m["files"]:
        require(type(row) is dict and set(row) == {"path","bytes","sha256","git_blob","mode"} and row["mode"] == "100644", "source mode/schema")
        plain.append({k:v for k,v in row.items() if k != "mode"})
    pins = rows_map(plain, git=True)
    source = {name[7:]: data for name,data in blobs.items() if name.startswith("source/")}
    require(set(source) == set(pins) and sum(r["bytes"] for r in pins.values()) == 98055, "exact source inventory/bytes")
    for name,row in pins.items():
        raw = source[name]
        authenticate(raw,row,"source/" + name)
        require(hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == row["git_blob"], "immutable Git blob mismatch")
    require(sha(source["verify_publication.py"]) == ROOT_SHA, "immutable root pin")
    return source


def publication_metadata(blobs):
    metadata = strict_json(blobs["metadata.json"])
    keys = {"title","upload_type","publication_type","publication_date","version","description","creators","access_right","license","keywords","references","related_identifiers"}
    require(type(metadata) is dict and set(metadata) == keys, "publication metadata exact keys")
    fixed = {"title":"An explicit rank-two entropy-minimizing Fano degeneration", "upload_type":"publication",
             "publication_type":"preprint", "publication_date":"2026-10-16", "version":"1.0.0", "access_right":"open", "license":"cc-by-4.0"}
    require(all(type(metadata[k]) is str and metadata[k] == v for k,v in fixed.items()), "publication metadata fixed identity")
    require(type(metadata["description"]) is str and 0 < len(metadata["description"]) <= 100000, "metadata description string/bound")
    require(type(metadata["creators"]) is list and metadata["creators"] == [{"name":"Kriebel, Alec","affiliation":"Independent researcher","orcid":"0009-0001-9320-500X"}], "exact sole creator")
    for key in ("keywords","references"):
        require(type(metadata[key]) is list and len(metadata[key]) <= 1000 and all(type(v) is str and 0 < len(v) <= 20000 for v in metadata[key]), "metadata string list: " + key)
    require(type(metadata["related_identifiers"]) is list and len(metadata["related_identifiers"]) <= 1000, "metadata related identifiers list")
    for row in metadata["related_identifiers"]:
        require(type(row) is dict and {"identifier","relation"} <= set(row) <= {"identifier","relation","scheme","resource_type"} and all(type(v) is str and 0 < len(v) <= 20000 for v in row.values()), "metadata related identifier schema")
    deposit = strict_json(blobs["zenodo-deposit.json"])
    require(type(deposit) is dict and set(deposit) == {"metadata","files"} and type(deposit["metadata"]) is dict and deposit["metadata"] == metadata, "deposit metadata exact copy")
    require(type(deposit["files"]) is list and deposit["files"] == [
        {"name":"rank-two-fano-note.pdf","path":"rank-two-fano-note.pdf"},
        {"name":"rank-two-fano-verification.zip","path":"rank-two-fano-verification.zip"}], "exact two deposit asset names/paths")
    deps = strict_json(blobs["dependencies.json"])
    require(deps == DEPENDENCIES and type(deps) is dict and type(deps["wheels"]) is list and all(type(w) is dict and type(w["bytes"]) is int for w in deps["wheels"]), "exact typed pinned dependency contract")


def package_inputs(root, external_pin):
    digest(external_pin)
    raw = read_regular(root / "package_index.json", limit=MAX_INDEX)
    require(sha(raw) == external_pin, "external index pin mismatch")
    pins = typed_index(raw,PACKAGE_SCHEMA)
    require("package_index.json" not in pins and REQUIRED <= set(pins), "required portable inventory")
    closed_tree(root,set(pins) | {"package_index.json"})
    blobs = {"package_index.json":raw}
    for name,row in pins.items():
        data = read_regular(within(root,name),row["bytes"])
        authenticate(data,row,name)
        if name.endswith(".json"): strict_json(data)
        blobs[name] = data
    require(read_regular(Path(__file__).absolute()) == blobs["portable.py"], "authenticated startup copy mismatch")
    original_inputs(blobs)
    publication_metadata(blobs)
    return blobs


def materialize(root, blobs):
    root.mkdir()
    for name,data in blobs.items():
        target = root / safe_name(name)
        target.parent.mkdir(parents=True,exist_ok=True)
        with target.open("xb") as stream: stream.write(data)
        target.chmod(0o644)


def deterministic_zip(blobs):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for name in sorted(blobs):
            info = zipfile.ZipInfo(safe_name(name),(2026,10,16,0,0,0))
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info,blobs[name],compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    return stream.getvalue()


def source_only(values, primary_dir=None):
    require(len(values) == 3 and all(v is not None for v in values), "all three complete corpus paths required")
    paths = dict(zip(INPUT_PINS,values))
    # This whole pass must finish before parsing or selecting ANY target record.
    for name,path in paths.items(): stream_pin(path,*INPUT_PINS[name])
    found,receipts = {},[]
    for name,path in paths.items():
        size,expected = INPUT_PINS[name]
        raw = read_regular(path,size)
        require(sha(raw) == expected, "source changed after complete authentication")
        data = strict_json(raw)
        if name == "research_results.json":
            require(type(data) is dict and "OWR-10252925-004" not in data, "expected absent target report")
        else:
            require(type(data) is list and all(type(r) is dict for r in data), "native corpus list")
            exact = [r for r in data if type(r.get("id")) in (str,int) and str(r["id"]) == "30005079"]
            require(len(exact) == 1, "exact target ID uniqueness")
            found[name] = exact[0]
        receipts.append({"name":name,"bytes":size,"sha256":expected,"complete_pin_before_any_extraction":True})
        del raw,data
    cat,record = found["catalog.json"],found["problems.json"]
    require(type(cat["rank"]) is int and cat["rank"] == 947 and cat["problem_number"] == record["problem_number"] == "OWR-10252925-004" and type(cat["title"]) is str and cat["title"] == record["title"], "canonical target identity")
    pair = (json.dumps([cat,record],indent=2,ensure_ascii=False) + "\n").encode("utf-8")
    require((len(pair),sha(pair)) == PAIR_PIN, "exact native canonical pair")
    require(type(record["statement"]) is str, "statement string")
    statement = record["statement"].encode("utf-8")
    require((len(statement),sha(statement)) == STATEMENT_PIN and cat["statement_hash"] == STATEMENT_PIN[1], "entire target statement")
    review = json.dumps([record,{}],sort_keys=True).encode()
    require(sha(review) == cat["review_hash"], "native review hash with absent report")
    return {"status":"PASS","inputs":receipts,"canonical_pair_bytes":len(pair),"canonical_pair_sha256":sha(pair),"statement_bytes":len(statement),"statement_sha256":sha(statement),"target_report":"ABSENT","archival_code_read":False,"archival_code_executed":False,"source_bodies_copied":False,"primary_sources":primary_only(primary_dir) if primary_dir is not None else "NOT_RUN"}


def primary_only(directory):
    directory = selected_root(directory)
    closed_tree(directory,set(PRIMARY_PINS))
    receipts = []
    for name,(size,expected) in PRIMARY_PINS.items():
        stream_pin(within(directory,name),size,expected)
        receipts.append({"name":name,"bytes":size,"sha256":expected})
    return {"status":"PASS","pins":receipts,"technical_theorems_verified_by_hash":False,"bodies_copied":False}


def dependency_inputs(directory):
    require(directory is not None, "default replay requires --dependency-dir containing the two pinned official wheels")
    directory = selected_root(directory)
    closed_tree(directory,{w["filename"] for w in WHEELS})
    result = {}
    for row in WHEELS:
        raw = read_regular(within(directory,row["filename"]),row["bytes"])
        authenticate(raw,row,row["filename"])
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            names = [i.filename for i in archive.infolist()]
            require(len(names) == len(set(names)), "duplicate wheel member")
            require(all(not n.endswith((".pyc",".pyo",".pth",".so",".dylib",".pyd")) and "__pycache__" not in n.split("/") for n in names), "wheel executable-site/bytecode/native-extension exclusion")
        result[row["filename"]] = raw
    return result

# The current harness executes the unchanged original root with actual optimize=0,
# because its own CLI rejects -O. Children use the requested actual optimization
# mode but compile the authenticated ORIGINAL source with optimize=0. No flags
# are spoofed. The two narrow subprocess calls of the reviewed root are checked.
HARNESS = r'''import contextlib,hashlib,io,json,os
from pathlib import Path
import subprocess,sys,tempfile
config=json.loads(sys.argv[1]); root=Path(config['root']).resolve(); scratch=Path(config['scratch']).resolve(); wheels=Path(config['wheels']).resolve()
mode=config['checker_optimize']; os.environ['TMPDIR']=str(scratch); tempfile.tempdir=str(scratch)
wheel_paths=[str(wheels/n) for n in config['wheel_names']]
sys.path[:0]=wheel_paths
import sympy,mpmath
def require(ok,message):
    if not ok: raise ValueError(message)
def pin(raw): return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def flags(): return {n:getattr(sys.flags,n) for n in ('optimize','isolated','no_site','dont_write_bytecode','ignore_environment','safe_path')}
require(sympy.__version__=='1.14.0' and mpmath.__version__=='1.3.0','dependency versions')
require(sympy.__file__.startswith(wheel_paths[0]+'/sympy/') and mpmath.__file__.startswith(wheel_paths[1]+'/mpmath/'),'dependency import provenance')
require(flags()=={'optimize':0,'isolated':1,'no_site':1,'dont_write_bytecode':1,'ignore_environment':1,'safe_path':True},'actual root flags')
source=(root/'verify_publication.py').read_bytes()
require(hashlib.sha256(source).hexdigest()==config['root_sha256'],'original root preexecution pin')
checkers=config['checkers']; original_run=subprocess.run; events=[]
CHILD=r"""import hashlib,json,sys
from pathlib import Path
c=json.loads(sys.argv[1]); p=Path(c['path']); raw=p.read_bytes()
f={n:getattr(sys.flags,n) for n in ('optimize','isolated','no_site','dont_write_bytecode','ignore_environment','safe_path')}
Path(c['measurement']).write_text(json.dumps(f,sort_keys=True))
if hashlib.sha256(raw).hexdigest()!=c['expected_sha256']:
    raise ValueError('CORRUPT_REJECTED_BEFORE_EXECUTION')
sys.path[:0]=c['wheels']
import sympy,mpmath
if sympy.__version__!='1.14.0' or mpmath.__version__!='1.3.0' or not sympy.__file__.startswith(c['wheels'][0]+'/sympy/') or not mpmath.__file__.startswith(c['wheels'][1]+'/mpmath/'):
    raise ValueError('dependency provenance/versions')
if c['kind']=='negative' and c['checker_index']==0:
    # A controlled mathematical defect makes the ORIGINAL first assertion false.
    sympy.integrate=lambda *args,**kwargs:sympy.Integer(0)
Path(c['began']).write_bytes(b'ORIGINAL_EXECUTION_BEGIN\n')
sys.argv=[str(p)]
exec(compile(raw,str(p),'exec',optimize=0),{'__name__':'__main__','__file__':str(p)})
"""
def run_child(p,index,kind,requested):
    script,output=checkers[index]; sequence=len(events)
    measurement=scratch/('flags-%02d.json'%sequence); began=scratch/('began-%02d'%sequence)
    c={'path':str(p),'expected_sha256':pin((root/script).read_bytes())['sha256'],'wheels':wheel_paths,'measurement':str(measurement),'began':str(began),'kind':kind,'checker_index':index}
    effective=['-I','-S','-B']+(['-O'] if mode else [])
    result=original_run([sys.executable,*effective,'-c',CHILD,json.dumps(c)],cwd=p.parent,capture_output=True,timeout=300)
    actual=json.loads(measurement.read_bytes())
    require(actual=={'optimize':mode,'isolated':1,'no_site':1,'dont_write_bytecode':1,'ignore_environment':1,'safe_path':True},'measured actual child flags')
    require((result.returncode==0)==(kind=='positive'),'child success/failure schedule')
    if kind=='negative': require(b'AssertionError' in result.stderr and began.read_bytes()==b'ORIGINAL_EXECUTION_BEGIN\n','original assertion did not fail')
    if kind=='corrupt': require(b'CORRUPT_REJECTED_BEFORE_EXECUTION' in result.stderr and not began.exists(),'corrupt original executed')
    event={'kind':kind,'checker':script,'original_sha256':c['expected_sha256'],'requested_by_original':requested,'effective_flags':effective,'measured_flags':actual,'compile_optimize':0,'returncode':result.returncode,'stdout':pin(result.stdout),'stderr':pin(result.stderr),'original_execution_began':began.exists()}
    if kind=='positive':
        expected=(root/output).read_bytes(); generated=p.with_name(Path(output).name).read_bytes()
        require(generated==expected,'generated checker output differs')
        stdout=expected+b'\n' if index==0 else b'PASS: exact integration, independently bounded roots, fan and barycenter checks; candidate hash unchanged.\n'
        require(result.stdout==stdout and result.stderr==b'','original stdout/stderr differ')
        event['generated_output']=pin(generated)
    events.append(event)
    return result

def guarded(command,*positional,**kwargs):
    require(not positional and type(command) is list and all(type(v) is str for v in command),'original nested command shape')
    index=len(events); require(index<2,'unexpected original nested process')
    script,output=checkers[index]
    require(len(command)==3 and command[:2]==[sys.executable,'-B'],'original requested executable/flags')
    p=Path(command[2]); cwd=Path(kwargs.get('cwd',''))
    require(p.is_absolute() and scratch in p.resolve().parents and p.name==Path(script).name and p.read_bytes()==(root/script).read_bytes(),'original private checker path/bytes')
    require(set(kwargs)=={'cwd','text','capture_output','timeout'} and kwargs['text'] is True and kwargs['capture_output'] is True and kwargs['timeout']==300 and cwd.is_dir() and scratch in cwd.resolve().parents,'original subprocess keyword allowlist')
    result=run_child(p,index,'positive',['-B'])
    return subprocess.CompletedProcess(command,result.returncode,result.stdout.decode(),result.stderr.decode())
subprocess.run=guarded
namespace={'__name__':'__main__','__file__':str(root/'verify_publication.py')}
sys.argv=[str(root/'verify_publication.py')]
text=io.StringIO()
with contextlib.redirect_stdout(text): exec(compile(source,str(root/'verify_publication.py'),'exec',optimize=0),namespace)
require(len(events)==2,'original root did not launch both exact checkers')
# Four genuine extra subprocesses: each original checker has one forced-assertion
# defect and one damaged-code preexecution rejection. None are synthetic counts.
for index,(script,output) in enumerate(checkers):
    for kind in ('negative','corrupt'):
        folder=scratch/('control-%d-%s'%(index,kind)); folder.mkdir()
        p=folder/script; p.parent.mkdir(parents=True,exist_ok=True)
        raw=(root/script).read_bytes(); p.write_bytes(raw+(b'\nCONTROL_MUST_NOT_EXECUTE\n' if kind=='corrupt' else b''))
        proof=folder/'authored/PROOF_CANDIDATE_v4.md'; proof.parent.mkdir()
        proof.write_bytes((root/'PROOF.md').read_bytes()+(b'\nCONTROL_CANDIDATE_DAMAGE\n' if kind=='negative' and index==1 else b''))
        run_child(p,index,kind,[])
# The original editions() already checked all four hashes and three forward and
# reverse transitions. Independently invoke its exact-context parser on three
# damaged candidate texts to prove the contextual failures remain enforced.
patch_events=[]; apply=namespace['apply_unified']; v4=(root/'PROOF.md').read_bytes()
v2=apply(v4,(root/'corrections/CITATION_CORRECTION.patch').read_bytes(),reverse=True)
for name,data in [('CITATION_CORRECTION.patch',v4),('NUMERICAL_CORRECTION_v1_to_v2.patch',v2),('POLYSTABILITY_CITATION_v3_to_v4.patch',v4)]:
    patch=(root/'corrections'/name).read_bytes(); damaged=b'DAMAGED_CONTEXT\n'*len(data.splitlines())
    try: apply(damaged,patch,reverse=True)
    except RuntimeError as exc:
        require(str(exc)=='Patch context mismatch','unexpected damaged-patch rejection')
        patch_events.append({'patch':name,'kind':'damaged_context','rejected':True,'damaged_input':pin(damaged),'patch_pin':pin(patch)})
    else: raise ValueError('damaged patch accepted')
print(json.dumps({'root_stdout':text.getvalue(),'root_flags':flags(),'root_compile_optimize':0,'root_sha256':pin(source)['sha256'],'dependency_versions':{'sympy':sympy.__version__,'mpmath':mpmath.__version__},'events':events,'patch_controls':patch_events},sort_keys=True))
'''


def replay(source, wheels):
    # Authenticated wheel BYTES are copied privately; imported code cannot race
    # against the caller's wheel files after authentication. No site tree is used.
    with tempfile.TemporaryDirectory(prefix="rank-two-fano-authenticated-") as td:
        work=Path(td); frozen=work/"frozen"; scratch=work/"scratch"; deps=work/"wheels"; unrelated=work/"unrelated"
        materialize(frozen,source); materialize(deps,wheels); scratch.mkdir(); unrelated.mkdir()
        config={"root":str(frozen),"scratch":str(scratch),"wheels":str(deps),"wheel_names":[r["filename"] for r in WHEELS],"root_sha256":ROOT_SHA,"checkers":CHECKERS,"checker_optimize":int(bool(sys.flags.optimize))}
        # Actual original root optimization must be zero; it expressly rejects -O.
        effective=["-I","-S","-B"]
        proc=subprocess.run([sys.executable,*effective,"-c",HARNESS,json.dumps(config)],cwd=unrelated,capture_output=True,timeout=1200)
        require(proc.returncode==0 and not proc.stderr,"authenticated root replay failed: "+proc.stderr.decode(errors="replace")[-4000:])
        receipt=strict_json(proc.stdout)
        require(type(receipt) is dict and set(receipt)=={"root_stdout","root_flags","root_compile_optimize","root_sha256","dependency_versions","events","patch_controls"},"replay receipt schema")
        require(receipt["root_flags"]=={"optimize":0,"isolated":1,"no_site":1,"dont_write_bytecode":1,"ignore_environment":1,"safe_path":True} and receipt["root_compile_optimize"]==0 and receipt["root_sha256"]==ROOT_SHA,"actual root flag/hash contract")
        raw=receipt.pop("root_stdout").encode(); result=strict_json(raw)
        expected={"packet_files_verified":21,"edition_hashes_verified":4,"forward_and_reverse_patches_verified":3,"author_results_byte_identical":True,"independent_results_byte_identical":True,"python_version":sys.version.split()[0],"sympy_version":"1.14.0","scope":"Integrity and auxiliary exact checks only; mathematical acceptance is in the two AI audit reports. No formal-proof or novelty certification."}
        require(type(result) is dict and result==expected,"unchanged original root semantic output")
        events=receipt["events"]
        require(type(events) is list and len(events)==6,"actual nested subprocess count")
        counts={k:sum(e["kind"]==k for e in events) for k in ("positive","negative","corrupt")}
        require(counts=={"positive":2,"negative":2,"corrupt":2},"real subprocess kind counts")
        require(len(receipt["patch_controls"])==3 and all(r["rejected"] is True for r in receipt["patch_controls"]),"three genuine in-process damaged-context controls")
        closed_tree(frozen,source)
        require(all(read_regular(within(frozen,n),len(b))==b for n,b in source.items()),"replay modified original copy")
    return {"status":"PASS","outer_measured_optimize":sys.flags.optimize,"direct_root_launches":1,"effective_root_flags":effective,"nested_subprocess_count":6,"counts":counts,"in_process_patch_damage_controls":3,"original_root_stdout":pin_bytes(raw),"original_root_output":result,"launcher":receipt,"root_compile_optimize":0,"checker_compile_optimize":0,"root_actual_optimization":"Always0 because unchanged original root rejects-O; actual checker mode follows outer optimization.","runtime_boundary":DEPENDENCIES["trusted_runtime"],"wheel_pins":[{k:v for k,v in w.items() if k!='url'} for w in WHEELS],"originals_unchanged":True}


def pin_bytes(raw):
    return {"bytes":len(raw),"sha256":sha(raw)}


def isolated():
    require(sys.version_info >= (3,11),"Python>=3.11 required")
    require(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,"run with -I -S -B")


def source_options(parser):
    for name in ("catalog","problems","reports","primary-dir"): parser.add_argument("--"+name,type=Path)


def optional_sources(args):
    values=[args.catalog,args.problems,args.reports]
    require(all(v is not None for v in values) or all(v is None for v in values),"all three corpus paths together")
    if all(v is not None for v in values): return source_only(values,args.primary_dir)
    return {"corpora":"NOT_RUN","primary_sources":primary_only(args.primary_dir) if args.primary_dir is not None else "NOT_RUN"}


def verify_result(blobs,index_pin,args):
    originals=original_inputs(blobs)
    source_check=optional_sources(args)
    replay_result="NOT_RUN" if args.verify_only else replay(originals,dependency_inputs(args.dependency_dir))
    return {"status":"PASS","scope":SCOPE,"index_sha256":index_pin,"package_member_count":len(blobs),"original_files":21,"original_bytes":98055,"original_effort":"1/5","source_authentication":source_check,"replay":replay_result}


def current_inputs(root,external_pin):
    digest(external_pin)
    raw=read_regular(root/"CURRENT_PUBLICATION_MANIFEST.json",limit=MAX_INDEX)
    require(sha(raw)==external_pin,"external current manifest pin mismatch")
    pins=typed_index(raw,CURRENT_SCHEMA)
    require("CURRENT_PUBLICATION_MANIFEST.json" not in pins and {"CURRENT_PUBLICATION.json","portable.py","metadata.json","zenodo-deposit.json","note.tex","rank-two-fano-note.pdf","rank-two-fano-verification.zip"} <= set(pins),"current required inventory")
    closed_tree(root,set(pins)|{"CURRENT_PUBLICATION_MANIFEST.json"})
    blobs={"CURRENT_PUBLICATION_MANIFEST.json":raw}
    for name,row in pins.items():
        data=read_regular(within(root,name),row["bytes"])
        authenticate(data,row,name)
        if name.endswith(".json"): strict_json(data)
        blobs[name]=data
    require(read_regular(Path(__file__).absolute())==blobs["portable.py"],"current startup copy mismatch")
    layout=strict_json(blobs["CURRENT_PUBLICATION.json"])
    require(type(layout) is dict and set(layout)=={"schema","problem_id","portable_prefix","zip_path","pdf_path","tex_path"} and layout=={"schema":LAYOUT_SCHEMA,"problem_id":"30005079","portable_prefix":"verification","zip_path":"rank-two-fano-verification.zip","pdf_path":"rank-two-fano-note.pdf","tex_path":"note.tex"},"exact typed current layout")
    prefix="verification/"
    portable={n[len(prefix):]:b for n,b in blobs.items() if n.startswith(prefix)}
    require("package_index.json" in portable and len(portable["package_index.json"])<=MAX_INDEX,"portable index exists/bounded")
    inner_pins=typed_index(portable["package_index.json"],PACKAGE_SCHEMA)
    require("package_index.json" not in inner_pins and REQUIRED <= set(inner_pins) and set(portable)==set(inner_pins)|{"package_index.json"},"current portable closed inventory")
    for name,row in inner_pins.items(): authenticate(portable[name],row,"portable "+name)
    original_inputs(portable); publication_metadata(portable)
    for name in ("portable.py","metadata.json","zenodo-deposit.json","note.tex"):
        require(blobs[name]==portable[name],"outer/portable exact copy mismatch: "+name)
    require(blobs["rank-two-fano-note.pdf"].startswith(b"%PDF-"),"actual paper PDF required")
    zip_payloads(blobs["rank-two-fano-verification.zip"],portable,generated=True)
    require(deterministic_zip(portable)==blobs["rank-two-fano-verification.zip"],"same-runtime independent ZIP rebuild differs")
    return blobs,portable


def output_preflight(root,blobs,requested,dependency_dir=None,primary_dir=None):
    # This MUST run before optional archival replay, scratch creation or output.
    requested=requested.absolute()
    require(requested.name=="rank-two-fano-verification.zip","exact verification asset filename")
    require(not requested.exists() and not requested.is_symlink(),"output must be fresh")
    parent=requested.parent
    for p in (parent,*parent.parents):
        require(stat.S_ISDIR(p.lstat().st_mode),"output parent/ancestor must be nonsymlink directory")
    parent=parent.resolve(strict=True)
    out=parent/requested.name
    directories={""}
    for name in blobs:
        safe_name(name)
        directories.update(str(p) for p in PurePosixPath(name).parents if str(p)!=".")
    input_directories=[root/n for n in directories]
    if dependency_dir is not None: input_directories.append(selected_root(dependency_dir))
    if primary_dir is not None: input_directories.append(selected_root(primary_dir))
    identities=set()
    for p in input_directories:
        info=p.lstat(); require(stat.S_ISDIR(info.st_mode),"input directory changed/nonregular")
        identities.add((info.st_dev,info.st_ino))
    for p in (parent,*parent.parents):
        info=p.stat()
        require((info.st_dev,info.st_ino) not in identities,"output must be outside every indexed input directory (physical alias)")
    require(not out.exists() and not out.is_symlink(),"output appeared during preflight")
    return out


def build_output(blobs,index_pin,args):
    root=selected_root(args.root)
    out=output_preflight(root,blobs,args.output,args.dependency_dir,args.primary_dir)
    result=verify_result(blobs,index_pin,args)
    raw=deterministic_zip(blobs); zip_payloads(raw,blobs,generated=True)
    require(raw==deterministic_zip(blobs),"same-runtime independent ZIP rebuild")
    with tempfile.TemporaryDirectory(prefix="rank-two-fano-build-",dir=out.parent) as td:
        candidate=Path(td)/out.name
        fd=os.open(candidate,os.O_WRONLY|os.O_CREAT|os.O_EXCL|getattr(os,"O_NOFOLLOW",0),0o644)
        with os.fdopen(fd,"wb") as stream:
            stream.write(raw); stream.flush(); os.fsync(stream.fileno())
        candidate.chmod(0o644)
        require(not out.exists() and not out.is_symlink(),"output appeared during build")
        os.link(candidate,out,follow_symlinks=False)
    return {"status":"PASS","scope":SCOPE,"archive_name":out.name,"bytes":len(raw),"sha256":sha(raw),"member_count":len(blobs),"fixed_zip_timestamp":"2026-10-16T00:00:00Z","same_runtime_exact_rebuild":True,"python_version":sys.version.split()[0],"zlib_runtime":zlib.ZLIB_RUNTIME_VERSION,"reproducibility_scope":"Same input bytes, Python ZIP implementation and zlib; cross-runtime compressed bytes are not promised.","verification":result}


def main():
    parser=argparse.ArgumentParser(description=__doc__,allow_abbrev=False)
    sub=parser.add_subparsers(dest="command",required=True)
    for mode in ("verify","build","current"):
        p=sub.add_parser(mode,allow_abbrev=False)
        p.add_argument("external_sha256",help="Independently supplied index/manifest SHA256")
        p.add_argument("--root",type=Path,default=Path(__file__).absolute().parent)
        p.add_argument("--dependency-dir",type=Path)
        if mode!="build": p.add_argument("--verify-only",action="store_true",help="Authenticate bytes; execute zero archival code")
        else:
            p.add_argument("output",type=Path)
            p.set_defaults(verify_only=False)
        source_options(p)
    p=sub.add_parser("source-only",allow_abbrev=False); source_options(p)
    args=parser.parse_args()
    if args.command=="source-only": result=source_only([args.catalog,args.problems,args.reports],args.primary_dir)
    elif args.command=="current":
        blobs,portable=current_inputs(selected_root(args.root),args.external_sha256)
        result={"status":"PASS","scope":SCOPE,"current_manifest_sha256":args.external_sha256,"outer_files":len(blobs),"same_runtime_exact_zip_rebuild":True,"portable":verify_result(portable,sha(portable["package_index.json"]),args)}
    else:
        blobs=package_inputs(selected_root(args.root),args.external_sha256)
        result=build_output(blobs,args.external_sha256,args) if args.command=="build" else verify_result(blobs,args.external_sha256,args)
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=="__main__":
    try:
        isolated(); main()
    except (ValueError,OSError,KeyError,TypeError,RuntimeError,OverflowError,RecursionError,zipfile.BadZipFile,zlib.error,subprocess.TimeoutExpired,UnicodeError,struct.error) as exc:
        print(json.dumps({"status":"REJECTED","reason":str(exc)},sort_keys=True)); sys.exit(1)

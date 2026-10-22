#!/usr/bin/env python3
"""PR885 artifact authentication and finite replay only. Authenticate startup independently.
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
SOURCE_MANIFEST_SHA256 = "6b1d1281848190f616f6759f40454183c937b65e65219b893202254be6c3617d"
FROZEN_HEAD = "4b1ef9bbeb723a4171949a6c3934db98962ac615"
REQUIRED = {"portable.py", "root_evidence/SOURCE_MANIFEST.json"}


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
                    info.flag_bits in (0, 0x800) and info.compress_type == zipfile.ZIP_DEFLATED and
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


PACKAGE_SCHEMA = "oriented-flow-9700042-verification-v1"
CURRENT_SCHEMA = "oriented-flow-9700042-current-publication-v1"
LAYOUT_SCHEMA = "oriented-flow-9700042-current-layout-v1"
ROOT_SHA = "13233e679fd24dffcf87407d934dcce80af7eb23132fe490227ce6edb62d85b9"
PAIR_PIN = (5104, "fef71ca1603c57d1335d95fdd80a4e3d8dad6e0ed454e92fd60b3945e229ca06")
STATEMENT_PIN = (145, "abd6df90fc1875d313d62fc5c4c3d26c55878cad686b63685885be06a1c979bb")
INPUT_PINS = {
    "catalog.json": (21735099, "891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566"),
    "problems.json": (68931837, "04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf"),
    "research_results.json": (80334822, "8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b"),
}
PRIMARY_PINS = {
    "aldous_hammersley_flow_20261007.html": (3576, "1c3078bb05b25554b7ab7bc12e6d8567b777407b6c6ad24fecfc89715088a301"),
    "deuschel_zeitouni_1999.pdf": (234108, "039d17fdb2f1e0fb0860e97a314d487554079fe0d34d1abb6d01b4d1e4479713"),
    "van_den_berg_jonasson_1105.3862.pdf": (152575, "61fc0dcb5a13eab3b8bb5a42f03f8b10423db8ed3aabf8f7b8d7b3965b6b7438"),
    "basdevant_gouere_theret_2106.12266.pdf": (967612, "9d78c8dd86aaa62dbaa7bfcaf40195c901c3cc9dee025bffd4a6e29af64339ba"),
}
CHECKERS = [
    ("verify_resume_turn1.py", "TURN_C1_CHECKS.json"),
    ("verify_resume_turn4.py", "TURN_C4_CHECKS.json"),
    ("audit_c1/check_independent.py", "audit_c1/INDEPENDENT_CHECKS.json"),
    ("audit_a/check_independent_c4.py", "audit_a/INDEPENDENT_CHECKS.json"),
    ("audit_b/independent_checks.py", "audit_b/INDEPENDENT_CHECKS.json"),
]
C1_STDOUT = (1253, "28676c0051f922b388d2d0f56287c964917ae5c99814f203c6644aa133f56f41")
SCOPE = "Closed byte authentication and finite diagnostics only; no proof, priority, novelty, human-review or publication approval."


def typed_index(raw, schema):
    value = strict_json(raw)
    require(type(value) is dict and set(value) == {"schema", "problem_id", "files"} and
            type(value["schema"]) is str and value["schema"] == schema and
            type(value["problem_id"]) is str and value["problem_id"] == "9700042", "typed index identity/schema")
    return rows_map(value["files"])


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
        if name.endswith(".json"):
            strict_json(data)
        blobs[name] = data
    require(read_regular(Path(__file__).absolute()) == blobs["portable.py"], "authenticated startup copy mismatch")
    original_inputs(blobs)
    return blobs


def original_inputs(blobs):
    raw = blobs["root_evidence/SOURCE_MANIFEST.json"]
    require(sha(raw) == SOURCE_MANIFEST_SHA256, "immutable source manifest pin")
    m = strict_json(raw)
    keys = {"timestamp_utc", "pr", "problem_id", "head", "prefix", "original_effort", "files", "original_file_count", "original_total_bytes", "scope"}
    require(type(m) is dict and set(m) == keys and type(m["timestamp_utc"]) is str and
            type(m["pr"]) is int and m["pr"] == 885 and m["problem_id"] == "9700042" and
            m["head"] == FROZEN_HEAD and m["prefix"] == "unsolved_math_prioritization/attempts/9700042/" and
            m["original_effort"] == "5/5" and type(m["original_file_count"]) is int and m["original_file_count"] == 30 and
            type(m["original_total_bytes"]) is int and m["original_total_bytes"] == 214980 and type(m["scope"]) is str,
            "immutable source typed metadata")
    pins = rows_map(m["files"], git=True)
    source = {name[7:]: data for name, data in blobs.items() if name.startswith("source/")}
    require(set(source) == set(pins) and len(pins) == 30 and sum(r["bytes"] for r in pins.values()) == 214980,
            "all30 exact source files required")
    for name, row in pins.items():
        data = source[name]
        authenticate(data, row, "source/" + name)
        require(hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest() == row["git_blob"], "immutable Git blob mismatch")
    require(sha(source["verify_packet.py"]) == ROOT_SHA, "immutable root pin")
    return source


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
    # All three COMPLETE corpora pass before any corpus is parsed or target extracted.
    require(len(values) == 3 and all(value is not None for value in values), "all three corpus paths required")
    paths = dict(zip(INPUT_PINS, values))
    for name, path in paths.items():
        stream_pin(path, *INPUT_PINS[name])
    found, receipts = {}, []
    for name, path in paths.items():
        size, expected = INPUT_PINS[name]
        raw = read_regular(path, size)
        require(sha(raw) == expected, "source changed after whole-corpus authentication")
        data = strict_json(raw)
        if name == "research_results.json":
            require(type(data) is dict and type(data.get("AMR-096-0042")) is dict, "exact target report")
            found[name] = data["AMR-096-0042"]
        else:
            require(type(data) is list and all(type(row) is dict for row in data), "corpus record array")
            exact = [row for row in data if type(row.get("id")) in (str, int) and str(row["id"]) == "9700042"]
            require(len(exact) == 1, "exact target ID uniqueness")
            found[name] = exact[0]
        del data, raw
        receipts.append({"name": name, "bytes": size, "sha256": expected, "complete_pin_before_any_extraction": True})
    cat, record, report = (found[n] for n in INPUT_PINS)
    require(type(cat["rank"]) is int and cat["rank"] == 937 and
            cat["problem_number"] == record["problem_number"] == "AMR-096-0042" and
            type(cat["title"]) is str and cat["title"] == record["title"], "canonical target identity")
    pair = json.dumps([record, report], sort_keys=True).encode()
    require((len(pair), sha(pair)) == PAIR_PIN and cat["review_hash"] == PAIR_PIN[1], "exact canonical pair")
    require(type(record["statement"]) is str, "statement text")
    statement = record["statement"].encode()
    require((len(statement), sha(statement)) == STATEMENT_PIN and cat["statement_hash"] == STATEMENT_PIN[1], "entire statement binding")
    return {"status": "PASS", "inputs": receipts, "canonical_pair_bytes": len(pair), "canonical_pair_sha256": sha(pair),
            "statement_bytes": len(statement), "statement_sha256": sha(statement), "archival_code_read": False,
            "archival_code_executed": False, "source_bodies_copied": False,
            "primary_sources": primary_only(primary_dir) if primary_dir is not None else "NOT_RUN"}


def primary_only(directory):
    directory = selected_root(directory)
    receipts = []
    for name, (size, expected) in PRIMARY_PINS.items():
        stream_pin(within(directory, name), size, expected)
        receipts.append({"name": name, "bytes": size, "sha256": expected, "complete_pin": True})
    return {"status": "PASS", "pins": receipts, "technical_theorems_verified_by_hash": False, "bodies_copied": False}


# Narrow interception of the reviewed original's exact scheduled commands. The
# original root bytes and original checker bootstrap remain unchanged. A child
# wrapper records sys.flags before executing that exact bootstrap. No sandbox.
HARNESS = r'''import ast, contextlib, hashlib, io, json, os
from pathlib import Path
import subprocess, sys, tempfile
root = Path(sys.argv[1]).resolve()
scratch = Path(sys.argv[2]).resolve()
os.environ['TMPDIR'] = str(scratch)
tempfile.tempdir = str(scratch)
source = (root / 'verify_packet.py').read_bytes()
if hashlib.sha256(source).hexdigest() != '13233e679fd24dffcf87407d934dcce80af7eb23132fe490227ce6edb62d85b9':
    raise ValueError('root hash before execution')
tree = ast.parse(source)
bootstrap = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'BOOTSTRAP' for t in n.targets))
checkers = [('verify_resume_turn1.py','TURN_C1_CHECKS.json'), ('verify_resume_turn4.py','TURN_C4_CHECKS.json'), ('audit_c1/check_independent.py','audit_c1/INDEPENDENT_CHECKS.json'), ('audit_a/check_independent_c4.py','audit_a/INDEPENDENT_CHECKS.json'), ('audit_b/independent_checks.py','audit_b/INDEPENDENT_CHECKS.json')]
patches = [('TURN_C1_MARKED_DEFECT_BOUND.md','audit_c1/C1_CLARIFICATION.patch'), ('TURN_C4_BK_POISSON_CANDIDATE.md','C4_CLARIFICATION.patch')]
modes = [[], ['-O'], ['-I'], ['-I','-O']]
schedule = [(s,o,m,k) for s,o in checkers for m in modes for k in ('positive','negative','corrupt')]
original_run = subprocess.run
events = []
def pin(raw):
    return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def flags():
    return {n:getattr(sys.flags,n) for n in ('optimize','isolated','no_site','dont_write_bytecode','ignore_environment','safe_path')}
def require(ok, message):
    if not ok: raise ValueError(message)
def private_path(raw):
    p = Path(raw)
    require(p.is_absolute() and scratch in p.resolve().parents and p.parent.is_dir() and not p.is_symlink(), 'nested path outside private scratch')
    return p

def guarded(command, *positional, **kwargs):
    require(not positional and type(command) is list and all(type(s) is str for s in command), 'nested command shape')
    i = len(events)
    if i < 4:
        original, patch_name = patches[i//2]
        require(len(command)==4 and command[:3]==['patch','--batch','--fuzz=0'], 'patch command allowlist')
        p = private_path(command[3])
        require(p.name==Path(original).name and set(kwargs)=={'input','cwd','capture_output'} and kwargs['cwd']==str(p.parent) and kwargs['capture_output'] is True and kwargs['input']==(root/patch_name).read_bytes(), 'patch invocation allowlist')
        result = original_run(command, timeout=60, **kwargs)
        require((result.returncode==0) == (i%2==0), 'patch success/failure schedule')
        events.append({'kind':'patch_positive' if i%2==0 else 'patch_damaged_context', 'returncode':result.returncode, 'stdout':pin(result.stdout), 'stderr':pin(result.stderr), 'stdin':pin(kwargs['input'])})
        return result
    require(i < 64, 'extra nested command')
    script, output, requested, kind = schedule[i-4]
    require(len(command)==len(requested)+6 and command[0]==sys.executable and command[1:1+len(requested)]==requested and command[1+len(requested):3+len(requested)]==['-c',bootstrap], 'Python command allowlist')
    p = private_path(command[-3])
    expected = hashlib.sha256((root/script).read_bytes()).hexdigest()
    require(p.name==Path(script).name and command[-2]==expected and command[-1]==('negative' if kind=='negative' else 'positive'), 'checker schedule/hash/mode')
    require(set(kwargs)=={'cwd','capture_output','timeout'} and kwargs['cwd']==str(p.parent) and kwargs['capture_output'] is True and kwargs['timeout']==(600 if kind=='positive' else 30), 'checker invocation allowlist')
    measurement = scratch/('flags-%02d.json'%i)
    effective = ['-I','-S','-B'] + (['-O'] if '-O' in requested else [])
    wrapper = 'import json,sys\nfrom pathlib import Path\nPath('+repr(str(measurement))+').write_text(json.dumps({n:getattr(sys.flags,n) for n in '+repr(tuple(flags()))+'},sort_keys=True))\nexec(compile('+repr(bootstrap)+',"<unchanged checker bootstrap>","exec",optimize=0))\n'
    result = original_run([sys.executable,*effective,'-c',wrapper,*command[-3:]], **kwargs)
    actual_flags = json.loads(measurement.read_bytes())
    require(actual_flags=={'optimize':int('-O' in requested),'isolated':1,'no_site':1,'dont_write_bytecode':1,'ignore_environment':1,'safe_path':True}, 'measured effective child flags')
    measurement.unlink()
    require((result.returncode==0) == (kind=='positive'), 'checker success/failure schedule')
    if kind=='negative': require(b'NEGATIVE_CONTROL_ASSERTION' in result.stderr, 'forced assertion failure missing')
    if kind=='corrupt': require(b'Checker hash mismatch before execution' in result.stderr, 'preexecution hash rejection missing')
    event = {'kind':kind,'checker':script,'requested_flags':requested,'effective_flags':effective,'measured_flags':actual_flags,'checker_compile_optimize':0,'returncode':result.returncode,'stdout':pin(result.stdout),'stderr':pin(result.stderr),'corrupt_rejected_before_checker_execution':kind=='corrupt'}
    if kind=='positive':
        generated = p.with_name(Path(output).name).read_bytes()
        require(generated==(root/output).read_bytes(), 'checker output mismatch')
        event['generated_output']=pin(generated)
    events.append(event)
    return result
subprocess.run = guarded
sys.argv = [str(root/'verify_packet.py')]
text = io.StringIO()
with contextlib.redirect_stdout(text):
    exec(compile(source,str(root/'verify_packet.py'),'exec',optimize=0), {'__name__':'__main__','__file__':str(root/'verify_packet.py')})
require(len(events)==64, 'exact nested count')
print(json.dumps({'root_stdout':text.getvalue(),'root_flags':flags(),'root_compile_optimize':0,'root_sha256':hashlib.sha256(source).hexdigest(),'events':events},sort_keys=True))
'''


def replay(source, scratch_parent=None):
    with tempfile.TemporaryDirectory(prefix="oriented-flow-authenticated-", dir=scratch_parent) as td:
        work = Path(td)
        frozen, scratch, unrelated = work / "frozen", work / "scratch", work / "unrelated"
        materialize(frozen, source)  # Exactly the 30 authenticated originals, no extra source code.
        scratch.mkdir()
        unrelated.mkdir()
        flags = ["-I", "-S", "-B"] + (["-O"] if sys.flags.optimize else [])
        proc = subprocess.run([sys.executable, *flags, "-c", HARNESS, str(frozen), str(scratch)],
                              cwd=unrelated, capture_output=True, timeout=3600)
        require(proc.returncode == 0 and not proc.stderr, "authenticated root replay failed: " + proc.stderr.decode(errors="replace")[-4000:])
        receipt = strict_json(proc.stdout)
        require(type(receipt) is dict and set(receipt) == {"root_stdout", "root_flags", "root_compile_optimize", "root_sha256", "events"}, "launcher receipt shape")
        expected_flags = {"optimize":int(bool(sys.flags.optimize)),"isolated":1,"no_site":1,
                          "dont_write_bytecode":1,"ignore_environment":1,"safe_path":True}
        require(receipt["root_flags"] == expected_flags and receipt["root_compile_optimize"] == 0 and
                receipt["root_sha256"] == ROOT_SHA, "measured isolated root flags/hash/compilation contract")
        raw = receipt.pop("root_stdout").encode()
        actual, historical = strict_json(raw), strict_json(source["REPLAY_RESULTS.json"])
        current_version, frozen_version = actual.pop("python"), historical.pop("python")
        require(actual == historical and actual["all_passed"] is True, "root semantic replay differs beyond Python version")
        events = receipt["events"]
        require(type(events) is list and len(events) == 64, "nested receipt count")
        counts = {k: sum(e["kind"] == k for e in events) for k in ("positive", "negative", "corrupt", "patch_positive", "patch_damaged_context")}
        require(counts == {"positive":20,"negative":20,"corrupt":20,"patch_positive":2,"patch_damaged_context":2}, "nested kind counts")
        for e in events:
            if e["kind"] == "positive":
                output = dict(CHECKERS)[e["checker"]]
                expected = {"bytes":len(source[output]),"sha256":sha(source[output])}
                require(e["generated_output"] == expected, "exact checker generated JSON hash")
                stdout = {"bytes": C1_STDOUT[0], "sha256": C1_STDOUT[1]} if e["checker"] == CHECKERS[0][0] else expected
                require(e["stdout"] == stdout and e["stderr"] == {"bytes":0,"sha256":sha(b"")}, "checker actual stdout/stderr hash")
        closed_tree(frozen, source)
        require(all(read_regular(within(frozen,n),len(b))==b for n,b in source.items()), "replay modified original copy")
    return {"status":"PASS", "direct_root_launches":1, "nested_subprocess_count":64, "counts":counts,
            "direct_flags":flags, "launcher":receipt, "root_stdout":{"bytes":len(raw),"sha256":sha(raw)},
            "semantic_root_equal_excluding_python":True, "current_python":current_version,"frozen_python":frozen_version,
            "original_root_and_bootstrap_unchanged":True,"child_isolation_injected_by_current_launcher":True,
            "historical_format_acceptance_hardened":False,"historical_format_boundaries":"See original-artifact audit; current closed-index checks are a separate authenticated wrapper."}

def isolated():
    require(sys.version_info >= (3, 11), "Python >=3.11 required")
    require(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode, "run with -I -S -B")


def source_options(parser):
    for name in ("catalog", "problems", "reports", "primary-dir"):
        parser.add_argument("--" + name, type=Path)


def optional_sources(args):
    values = [args.catalog, args.problems, args.reports]
    require(all(v is not None for v in values) or all(v is None for v in values), "all three corpus paths together")
    if all(v is not None for v in values):
        return source_only(values, args.primary_dir)
    return {"corpora":"NOT_RUN", "primary_sources":primary_only(args.primary_dir) if args.primary_dir is not None else "NOT_RUN"}


def verify_result(blobs, index_pin, args):
    originals = original_inputs(blobs)
    source_check = optional_sources(args)
    replay_result = "NOT_RUN" if args.verify_only else replay(originals)
    return {"status":"PASS", "scope":SCOPE, "index_sha256":index_pin,"package_member_count":len(blobs),
            "original_files":30,"original_bytes":214980,"original_effort":"5/5",
            "source_authentication":source_check,"replay":replay_result}


def current_inputs(root, external_pin):
    digest(external_pin)
    raw = read_regular(root / "CURRENT_PUBLICATION_MANIFEST.json", limit=MAX_INDEX)
    require(sha(raw) == external_pin, "external current manifest pin mismatch")
    pins = typed_index(raw, CURRENT_SCHEMA)
    require("CURRENT_PUBLICATION_MANIFEST.json" not in pins and {"CURRENT_PUBLICATION.json", "portable.py"} <= set(pins), "current required inventory")
    closed_tree(root, set(pins) | {"CURRENT_PUBLICATION_MANIFEST.json"})
    blobs = {"CURRENT_PUBLICATION_MANIFEST.json":raw}
    for name, row in pins.items():
        data = read_regular(within(root,name),row["bytes"])
        authenticate(data,row,name)
        if name.endswith(".json"):
            strict_json(data)
        blobs[name] = data
    require(read_regular(Path(__file__).absolute()) == blobs["portable.py"], "current startup copy mismatch")
    layout = strict_json(blobs["CURRENT_PUBLICATION.json"])
    require(type(layout) is dict and set(layout) == {"schema","problem_id","portable_prefix","zip_path","pdf_path","tex_path"} and
            layout["schema"] == LAYOUT_SCHEMA and layout["problem_id"] == "9700042", "typed current layout")
    prefix = safe_name(layout["portable_prefix"]) + "/"
    require(layout["zip_path"] == "oriented-flow-verification.zip" and layout["pdf_path"] == "oriented-flow-note.pdf" and
            layout["tex_path"] == "note.tex", "exact two publication asset names and TeX")
    portable = {name[len(prefix):]:data for name,data in blobs.items() if name.startswith(prefix)}
    require("package_index.json" in portable and len(portable["package_index.json"]) <= MAX_INDEX, "portable index exists")
    inner_pins = typed_index(portable["package_index.json"], PACKAGE_SCHEMA)
    require("package_index.json" not in inner_pins and REQUIRED <= set(inner_pins) and
            set(portable) == set(inner_pins) | {"package_index.json"}, "current portable closed inventory")
    for name,row in inner_pins.items():
        authenticate(portable[name],row,"portable " + name)
    original_inputs(portable)
    require(portable["portable.py"] == blobs["portable.py"], "outer/portable tool copies differ")
    require("metadata.json" in blobs and "metadata.json" in portable and
            blobs["metadata.json"] == portable["metadata.json"], "outer/portable metadata copies differ")
    metadata = strict_json(blobs["metadata.json"])
    metadata_keys = {"title","upload_type","publication_type","publication_date","version","description",
                     "creators","access_right","license","keywords","references","related_identifiers"}
    require(type(metadata) is dict and set(metadata) == metadata_keys, "publication metadata exact keys")
    for key in ("title","upload_type","publication_type","publication_date","version","description","access_right","license"):
        require(type(metadata[key]) is str and bool(metadata[key]), "publication metadata string: " + key)
    require(metadata["title"] == "Near-one oriented-percolation flow from Bernoulli first-passage estimates" and
            metadata["upload_type"] == "publication" and metadata["publication_type"] == "preprint" and
            metadata["publication_date"] == "2026-10-16" and metadata["version"] == "1.0.0" and
            metadata["access_right"] == "open" and metadata["license"] == "cc-by-4.0", "publication metadata identity")
    require(type(metadata["creators"]) is list and len(metadata["creators"]) == 1, "publication creator list")
    creator = metadata["creators"][0]
    require(type(creator) is dict and creator == {"name":"Kriebel, Alec","affiliation":"Independent researcher",
            "orcid":"0009-0001-9320-500X"}, "exact publication creator/affiliation/ORCID")
    for key in ("keywords","references"):
        require(type(metadata[key]) is list and all(type(x) is str and bool(x) for x in metadata[key]), "publication metadata string list: " + key)
    require(type(metadata["related_identifiers"]) is list, "publication related identifiers list")
    for row in metadata["related_identifiers"]:
        require(type(row) is dict and {"identifier","relation"} <= set(row) <= {"identifier","relation","scheme","resource_type"} and
                all(type(x) is str and bool(x) for x in row.values()), "publication related identifier row")
    require("zenodo-deposit.json" in blobs and "zenodo-deposit.json" in portable and
            blobs["zenodo-deposit.json"] == portable["zenodo-deposit.json"], "outer/portable deposit copies differ")
    deposit = strict_json(blobs["zenodo-deposit.json"])
    require(type(deposit) is dict and set(deposit) == {"metadata","files"} and
            type(deposit["metadata"]) is dict and
            json.dumps(deposit["metadata"],sort_keys=True) == json.dumps(metadata,sort_keys=True), "typed deposit metadata contract")
    require(type(deposit["files"]) is list and deposit["files"] == [
            {"name":"oriented-flow-note.pdf","path":"oriented-flow-note.pdf"},
            {"name":"oriented-flow-verification.zip","path":"oriented-flow-verification.zip"}], "exact two deposit asset names/paths")
    require(layout["tex_path"] in blobs and layout["tex_path"] in portable and
            blobs[layout["tex_path"]] == portable[layout["tex_path"]], "outer/portable actual TeX equality")
    require(layout["pdf_path"] in blobs and blobs[layout["pdf_path"]].startswith(b"%PDF-"), "actual paper PDF required")
    require(layout["zip_path"] in blobs and not layout["zip_path"].startswith(prefix), "ZIP outside portable prefix")
    zip_payloads(blobs[layout["zip_path"]], portable, generated=True)
    rebuilt = deterministic_zip(portable)
    require(rebuilt == blobs[layout["zip_path"]], "same-runtime deterministic ZIP rebuild differs")
    return blobs, portable


def build_output(blobs, index_pin, args):
    # Fully authenticate, validate and replay before creating the publication ZIP.
    require(not args.output.is_symlink(), "output symlink")
    requested = args.output.absolute()
    require(requested.name == "oriented-flow-verification.zip", "exact verification asset filename")
    parent = requested.parent.resolve(strict=True)
    require(stat.S_ISDIR(parent.lstat().st_mode), "output parent must be an existing directory")
    out = parent / requested.name
    root = selected_root(args.root)
    require(root != out and root not in out.parents, "output must be outside input tree")
    require(not out.exists() and not out.is_symlink(), "output must be fresh")
    result = verify_result(blobs,index_pin,args)
    raw = deterministic_zip(blobs)
    zip_payloads(raw,blobs,generated=True)
    require(raw == deterministic_zip(blobs), "same-runtime exact ZIP rebuild")
    with tempfile.TemporaryDirectory(prefix="oriented-flow-build-",dir=out.parent) as td:
        candidate = Path(td) / out.name
        candidate.write_bytes(raw)
        require(not out.exists() and not out.is_symlink(), "output appeared during build")
        # Atomic no-clobber publication on the same filesystem.
        os.link(candidate,out)
    return {"status":"PASS","scope":SCOPE,"archive_name":out.name,"bytes":len(raw),"sha256":sha(raw),
            "member_count":len(blobs),"fixed_zip_timestamp":"2026-10-16T00:00:00Z",
            "same_runtime_exact_rebuild":True,"python_version":sys.version.split()[0],"zlib_runtime":zlib.ZLIB_RUNTIME_VERSION,
            "reproducibility_scope":"Same input bytes, Python ZIP implementation and zlib; cross-runtime compressed bytes are not promised.",
            "verification":result}


def main():
    parser = argparse.ArgumentParser(description=__doc__,allow_abbrev=False)
    sub = parser.add_subparsers(dest="command",required=True)
    for mode in ("verify","build","current"):
        p = sub.add_parser(mode,allow_abbrev=False)
        p.add_argument("external_sha256",help="Independent package-index or current-manifest SHA256")
        p.add_argument("--root",type=Path,default=Path(__file__).absolute().parent)
        p.add_argument("--verify-only",action="store_true",help="Authenticate structure and bytes; execute zero archival code")
        source_options(p)
        if mode=="build":
            p.add_argument("output",type=Path)
            # A build is the validated default; do not let its CLI bypass replay.
            p.set_defaults(verify_only=False)
    p = sub.add_parser("source-only",allow_abbrev=False)
    source_options(p)
    args = parser.parse_args()
    if args.command == "source-only":
        result = source_only([args.catalog,args.problems,args.reports],args.primary_dir)
    elif args.command == "current":
        blobs,portable = current_inputs(selected_root(args.root),args.external_sha256)
        result = {"status":"PASS","scope":SCOPE,"current_manifest_sha256":args.external_sha256,
                  "outer_files":len(blobs),"same_runtime_exact_zip_rebuild":True,
                  "portable":verify_result(portable,sha(portable["package_index.json"]),args)}
    else:
        blobs = package_inputs(selected_root(args.root),args.external_sha256)
        if args.command == "build":
            require(args.verify_only is False, "build requires the default complete replay")
            result = build_output(blobs,args.external_sha256,args)
        else:
            result = verify_result(blobs,args.external_sha256,args)
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__ == "__main__":
    try:
        isolated()
        main()
    except (ValueError,OSError,KeyError,TypeError,RuntimeError,OverflowError,RecursionError,
            zipfile.BadZipFile,zlib.error,subprocess.TimeoutExpired,UnicodeError,struct.error) as exc:
        print(json.dumps({"status":"REJECTED","reason":str(exc)},sort_keys=True))
        sys.exit(1)

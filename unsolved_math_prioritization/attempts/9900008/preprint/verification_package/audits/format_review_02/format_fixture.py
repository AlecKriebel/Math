#!/usr/bin/env python3
"""Finite independent PR883 format checks; stdlib only; isolated execution required.

Usage: python3 -I -S -B [-O] format_fixture.py AUDIT_ROOT RESULT_JSON
Read this entire file and all authenticated executable inputs before running.
No source input is modified. All generated package files live in a private
temporary directory beneath this script's directory and are removed afterward.
"""
import hashlib
import io
import json
import os
from pathlib import Path
import runpy
import stat
import struct
import subprocess
import sys
import tempfile
import time
import zipfile
import zlib

PINS = {
    "check_originals.py": (30482, "e4fb73b16db72ed4387c08c38662a1ad9f836f9b0ecd2ff91778347deb74829b"),
    "verify_package.py": (16013, "e80ce30e89547c52d63c44237a554f0b3bf1ae1959783bbbba1f3f1703e9f7f8"),
    "build_verification.py": (17641, "2b0521d74a49360cbdd6d48427cb02763b586f3a5196766ec16f6ddc2fa41f2c"),
    "verify_current_publication.py": (21129, "3fc89372bae6cc3ed2f6a8d4f93d890e94e9fd635b712223853630d26f034672"),
    "TOOLING_MANIFEST.json": (1006, "86290fcc61e5a54a51a2108b55c408961938c45380a9a2bac156fdec8d264585"),
    "README.md": (9874, "c4b30b40eaa4afe087cce8b7cd4c985ae90d8587cb46b0110ddae5404a613350"),
}
SOURCE_PIN = "53bba0a85fa099146f7bb6d7520bc8a3a423894b702a9e8e4cb9f63ded3a48ab"
ARCHIVAL_CODE = {
    "author/verify.py": "020486719783210fe4fe714d368f8168c503269f8aaf878e8f37cce021a05887",
    "check_publication.py": "ffabe0fb3a3ba791eb7b3bb2af93b755bb1fc9410ce12ac385b353d3f96b63fd",
}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def row(name, data):
    return {"path": name, "bytes": len(data), "sha256": sha(data)}


def manifest(blobs, schema):
    return json_bytes({"schema": schema, "problem_id": "9900008",
                       "files": [row(n, blobs[n]) for n in sorted(blobs)]})


def write_tree(root, blobs):
    root.mkdir()
    for name, raw in blobs.items():
        dest = root / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(raw)


def raw_deflate(payload):
    compressor = zlib.compressobj(9, zlib.DEFLATED, -15)
    return compressor.compress(payload) + compressor.flush()


def make_zip(payloads, replacement=None, method=8, crc_delta=0, size_delta=0):
    """Pack a closed ZIP independently of zipfile/candidate; replacement=(name,raw)."""
    locals_, centrals, offset = [], [], 0
    for name in sorted(payloads):
        data = payloads[name]
        encoded = name.encode("ascii")
        compressed = raw_deflate(data) if method == 8 else data
        if replacement is not None and name == replacement[0]:
            compressed = replacement[1]
        crc = (zlib.crc32(data) ^ crc_delta) & 0xffffffff
        usize, csize = len(data) + size_delta, len(compressed)
        dosdate = (46 << 9) | (10 << 5) | 15
        local = struct.pack("<4s5H3I2H", b"PK\x03\x04", 20, 0, method,
                            0, dosdate, crc, csize, usize, len(encoded), 0)
        local += encoded + compressed
        central = struct.pack("<4s6H3I5H2I", b"PK\x01\x02", (3 << 8) | 20,
                              20, 0, method, 0, dosdate, crc, csize, usize,
                              len(encoded), 0, 0, 0, 0,
                              (stat.S_IFREG | 0o644) << 16, offset)
        centrals.append(central + encoded)
        locals_.append(local)
        offset += len(local)
    central = b"".join(centrals)
    end = struct.pack("<4s4H2IH", b"PK\x05\x06", 0, 0, len(payloads),
                      len(payloads), len(central), offset, 0)
    return b"".join(locals_) + central + end


def stream_oracle(compressed, expected):
    try:
        decoder = zlib.decompressobj(-15)
        actual = decoder.decompress(compressed, len(expected) + 1)
        return {"output_exact": actual == expected, "eof": decoder.eof,
                "unused_bytes": len(decoder.unused_data),
                "unconsumed_bytes": len(decoder.unconsumed_tail),
                "valid": actual == expected and decoder.eof and
                not decoder.unused_data and not decoder.unconsumed_tail}
    except zlib.error as exc:
        return {"valid": False, "zlib_error": str(exc)}


def source_snapshot(audit):
    candidate = {}
    for name, (size, expected) in PINS.items():
        data = (audit / "tooling_candidate" / name).read_bytes()
        need((len(data), sha(data)) == (size, expected), "candidate pin changed: " + name)
        candidate[name] = data
    manifest_raw = (audit / "SOURCE_MANIFEST.json").read_bytes()
    need(sha(manifest_raw) == SOURCE_PIN, "frozen manifest pin changed")
    original = {}
    source_rows = json.loads(manifest_raw)["files"]
    for r in source_rows:
        data = (audit / "source" / r["path"]).read_bytes()
        need((len(data), sha(data)) == (r["bytes"], r["sha256"]), "original pin changed")
        need(hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest() == r["git_blob"], "original Git pin changed")
        original[r["path"]] = data
    need(len(original) == 26 and sum(map(len, original.values())) == 211771, "original set")
    for name, expected in ARCHIVAL_CODE.items():
        need(sha(original[name]) == expected, "archival executable pin changed")
    pins = [row("tooling_candidate/" + n, b) for n, b in sorted(candidate.items())]
    pins += [row("SOURCE_MANIFEST.json", manifest_raw)]
    pins += [row("source/" + n, b) for n, b in sorted(original.items())]
    return candidate, original, manifest_raw, pins


def run_cli(script, arguments, env, cwd, expected_pass=True):
    flags = ["-I", "-S", "-B"] + (["-O"] if sys.flags.optimize else [])
    command = [sys.executable, *flags, str(script), *map(str, arguments)]
    started = time.monotonic()
    proc = subprocess.run(command, cwd=cwd, env=env, capture_output=True, timeout=1800)
    need(not proc.stderr, "unexpected CLI stderr: " + proc.stderr.decode(errors="replace"))
    output = json.loads(proc.stdout)
    need((proc.returncode == 0 and output.get("status") == "PASS") == expected_pass,
         "CLI decision mismatch: " + str(command) + " " + str(output))
    if not expected_pass:
        need(proc.returncode == 1 and output.get("status") == "REJECTED", "unstructured rejection")
    return {"script": script.name, "arguments": [str(a).replace(str(cwd), "PRIVATE_TMP") for a in arguments],
            "flags": flags, "returncode": proc.returncode,
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "stdout_bytes": len(proc.stdout), "stdout_sha256": sha(proc.stdout), "result": output}


def main():
    need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode, "requires -I -S -B")
    audit, output_path = map(Path, sys.argv[1:])
    audit = audit.resolve()
    review = Path(__file__).resolve().parent
    need(output_path.resolve().parent == review, "output must be in review directory")
    candidate, original, source_manifest, before = source_snapshot(audit)
    results = {"schema": "pr883-independent-format-review-v1", "optimized": bool(sys.flags.optimize),
               "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "python": sys.version, "zlib_runtime": zlib.ZLIB_RUNTIME_VERSION,
               "pins_before": before, "stream_cases": [], "original_archives": [], "cli": []}
    with tempfile.TemporaryDirectory(prefix="format-review-02-", dir=review) as td:
        work = Path(td)
        nested = work / "nested"
        nested.mkdir()
        env = dict(os.environ, TMPDIR=str(nested))
        copies = work / "reviewed_tools"
        write_tree(copies, {n: b for n, b in candidate.items() if n.endswith(".py")})
        modules = {n: runpy.run_path(str(copies / n), run_name="independent_review_" + n[:-3])
                   for n in candidate if n.endswith(".py")}
        payload = b"line one\r\nline two\n\x00\xff\x80\tend"
        compressed = raw_deflate(payload)
        empty = raw_deflate(b"")
        cases = [("valid_binary_crlf", payload, compressed, True),
                 ("valid_empty", b"", empty, True),
                 ("suffix_zero", payload, compressed + b"\x00", False),
                 ("suffix_bytes", payload, compressed + b"INERT", False),
                 ("second_empty_stream", payload, compressed + empty, False),
                 ("second_nonempty_stream", payload, compressed + raw_deflate(b"second"), False),
                 ("empty_suffix_zero", b"", empty + b"\x00", False),
                 ("empty_second_stream", b"", empty + empty, False),
                 ("empty_no_stream", b"", b"", False),
                 ("empty_truncated", b"", empty[:-1], False),
                 ("corrupt_block_type", payload, b"\x07", False),
                 ("extra_inflated_byte", payload, raw_deflate(payload + b"x"), False)]
        cases += [("truncated_" + str(n), payload, compressed[:-n], False) for n in (1, 2, 3)]
        for name, want, stream, expected in cases:
            oracle = stream_oracle(stream, want)
            need(oracle["valid"] == expected, "independent oracle setup: " + name)
            archive = make_zip({"inert.bin": want}, ("inert.bin", stream))
            entry = {"name": name, "expected_accept": expected, "archive_bytes": len(archive),
                     "archive_sha256": sha(archive), "compressed_hex": stream.hex(),
                     "expected_payload_hex": want.hex(), "oracle": oracle, "decisions": []}
            for script, module in modules.items():
                for generated in (False, True):
                    try:
                        actual = module["zip_payloads"](archive, {"inert.bin": want}, generated=generated)
                        accepted, reason = actual == {"inert.bin": want}, "accepted"
                    except (ValueError, zipfile.BadZipFile, zlib.error, struct.error) as exc:
                        accepted, reason = False, str(exc)
                    entry["decisions"].append({"script": script, "generated": generated,
                                               "accepted": accepted, "reason": reason})
                    need(accepted == expected, "format verdict mismatch: " + name + ": " + script)
                    if not expected and name != "corrupt_block_type":
                        need("raw DEFLATE exact-consumption" in reason, "unrelated rejection: " + name)
            results["stream_cases"].append(entry)
        for name, raw in [("stored_is_outside_contract", make_zip({"inert.bin": payload}, method=0)),
                          ("crc_disagreement", make_zip({"inert.bin": payload}, crc_delta=1)),
                          ("declared_size_disagreement", make_zip({"inert.bin": payload}, size_delta=1))]:
            decisions = []
            for script, module in modules.items():
                try:
                    module["zip_payloads"](raw, {"inert.bin": payload}, generated=True)
                except (ValueError, zipfile.BadZipFile, zlib.error, struct.error) as exc:
                    decisions.append({"script": script, "accepted": False, "reason": str(exc)})
                else:
                    raise ValueError("metadata negative accepted: " + name)
            results["stream_cases"].append({"name": name, "expected_accept": False, "archive_sha256": sha(raw), "decisions": decisions})
        for archive_name, folder in [("DIFFUSE_MASS_9900008_AUTHOR_SAFE_FREEZE.zip", "author"),
                                     ("DIFFUSE_MASS_9900008_FRESH_REVIEW_ACCEPTED_SAFE.zip", "review2")]:
            expected = {n[len(folder)+1:]: b for n, b in original.items() if n.startswith(folder + "/")}
            raw = original["archives/" + archive_name]
            for module in modules.values():
                need(module["zip_payloads"](raw, expected) == expected, "original archive mismatch")
            results["original_archives"].append({"name": archive_name, "members": len(expected),
                                                  "bytes": len(raw), "sha256": sha(raw), "all_four_accepted": True})
        portable = {"source/" + n: b for n, b in original.items()}
        portable.update({n: candidate[n] for n in ("check_originals.py", "verify_package.py", "build_verification.py")})
        portable["root_evidence/SOURCE_MANIFEST.json"] = source_manifest
        portable["extras/inert.bin"], portable["extras/empty.bin"] = payload, b""
        portable["package_index.json"] = manifest(portable, "diffuse-9900008-verification-v1")
        index_sha = sha(portable["package_index.json"])
        package = work / "package"
        write_tree(package, portable)
        for verify_only in (True, False):
            args = [index_sha, "--root", package] + (["--verify-only"] if verify_only else [])
            results["cli"].append(run_cli(package / "verify_package.py", args, env, work))
        built = []
        for i in (1, 2):
            destination = work / ("built" + str(i))
            receipt = run_cli(package / "build_verification.py",
                              [package, index_sha, PINS["verify_package.py"][1], destination], env, work)
            results["cli"].append(receipt)
            raw = (destination / "verification.zip").read_bytes()
            need(sha(raw) == receipt["result"]["sha256"], "builder output receipt mismatch")
            built.append(raw)
        need(built[0] == built[1], "builder nondeterminism")
        with zipfile.ZipFile(io.BytesIO(built[0])) as archive:
            need(set(archive.namelist()) == set(portable), "builder membership")
            need(all(archive.read(n) == b for n, b in portable.items()), "builder changed source bytes")
            need(all(i.date_time == (2026, 10, 15, 0, 0, 0) and i.external_attr == (stat.S_IFREG | 0o644) << 16 and
                     i.compress_type == 8 and not i.extra and not i.comment for i in archive.infolist()), "builder metadata")
        results["deterministic_build"] = {"runs": 2, "byte_identical": True, "archive_bytes": len(built[0]),
                                           "archive_sha256": sha(built[0]), "source_files_exact": 26,
                                           "all_member_bytes_exact": True, "package_index_sha256": index_sha}
        preserved = sorted(set(original) - {"README.md", "RESEARCH_LOG.md"})
        outer = {n: original[n] for n in preserved}
        outer.update({"portable/" + n: b for n, b in portable.items()})
        outer["verify_current_publication.py"] = candidate["verify_current_publication.py"]
        outer["verification.zip"] = built[0]
        outer["CURRENT_PUBLICATION.json"] = json_bytes({"tooling_layout": {
            "portable_prefix": "portable", "zip_path": "verification.zip", "copy_pairs": [],
            "preserved_source_paths": preserved, "json_equal_groups": []}})
        for name, stream, expect in [("valid", None, True), ("suffix", compressed + b"INERT", False),
                                     ("second_stream", compressed + empty, False), ("truncated", compressed[:-1], False),
                                     ("invalid_block_type", b"\x07", False)]:
            root = work / ("current_" + name)
            variant = dict(outer)
            if stream is not None:
                variant["verification.zip"] = make_zip(portable, ("extras/inert.bin", stream))
            variant["CURRENT_PUBLICATION_MANIFEST.json"] = manifest(variant, "diffuse-9900008-current-publication-v1")
            outer_sha = sha(variant["CURRENT_PUBLICATION_MANIFEST.json"])
            write_tree(root, variant)
            args = [outer_sha, "--root", root, "--verify-only"]
            receipt = run_cli(root / "verify_current_publication.py", args, env, work, expect)
            if not expect:
                reason = receipt["result"]["reason"]
                need(("invalid block type" if name == "invalid_block_type" else "raw DEFLATE exact-consumption") in reason,
                     "outer unrelated rejection")
            receipt["fixture"] = name
            results["cli"].append(receipt)
        need(all((package / n).read_bytes() == b for n, b in portable.items()), "input fixture changed")
    _, _, _, after = source_snapshot(audit)
    need(before == after, "source identity changed during review")
    results["pins_after"] = after
    results["source_unchanged"] = True
    results["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    results["status"] = "PASS"
    output_path.write_bytes(json_bytes(results))
    print(json.dumps({"status": "PASS", "optimized": results["optimized"], "stream_cases": len(results["stream_cases"]),
                      "raw_decisions": sum(len(c["decisions"]) for c in results["stream_cases"]),
                      "cli_runs": len(results["cli"]), "archive_sha256": results["deterministic_build"]["archive_sha256"],
                      "result_bytes": output_path.stat().st_size, "result_sha256": sha(output_path.read_bytes())}, sort_keys=True))


if __name__ == "__main__":
    main()

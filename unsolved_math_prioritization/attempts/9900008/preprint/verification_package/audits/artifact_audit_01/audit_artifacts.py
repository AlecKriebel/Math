#!/usr/bin/env python3
"""Independent read-only provenance and private-copy replay for PR 883.

No original candidate, source input, or Git state is modified. No extraction of
untrusted ZIP paths is performed. This is an artifact audit, not a proof checker.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import struct
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
import zipfile

AUDIT = Path(__file__).resolve().parent
EFFORT = AUDIT.parent
SOURCE = EFFORT / "source"
REPO = EFFORT.parents[2]
HEAD = "af25d26e21945a1a132aace5e600485152777070"
PREFIX = "unsolved_math_prioritization/attempts/9900008/"
SOURCE_MANIFEST_PIN = "53bba0a85fa099146f7bb6d7520bc8a3a423894b702a9e8e4cb9f63ded3a48ab"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def strict_json(data):
    def pairs(rows):
        out = {}
        for key, value in rows:
            need(key not in out, "duplicate JSON key: " + key)
            out[key] = value
        return out
    def bad(value):
        raise ValueError("nonfinite JSON constant: " + value)
    return json.loads(data, object_pairs_hook=pairs, parse_constant=bad)


def load(path):
    return strict_json(path.read_bytes())


def write(name, data):
    (AUDIT / name).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def stream_pin(path):
    h = hashlib.sha256()
    count = 0
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            count += len(chunk)
            h.update(chunk)
    return {"bytes": count, "sha256": h.hexdigest()}


def provenance():
    manifest_path = EFFORT / "SOURCE_MANIFEST.json"
    need(sha(manifest_path.read_bytes()) == SOURCE_MANIFEST_PIN, "external frozen manifest mismatch")
    manifest = load(manifest_path)
    need(manifest["frozen_head"] == HEAD, "wrong head")
    expected = {row["path"]: row for row in manifest["files"]}
    need(len(expected) == 26 and sum(row["bytes"] for row in expected.values()) == 211771, "unexpected frozen extent")
    actual = set()
    directories = []
    for path in SOURCE.rglob("*"):
        mode = path.lstat().st_mode
        rel = path.relative_to(SOURCE).as_posix()
        need(not stat.S_ISLNK(mode), "symlink in frozen source")
        if stat.S_ISDIR(mode):
            directories.append(rel)
            continue
        need(stat.S_ISREG(mode), "nonregular frozen source")
        actual.add(rel)
    need(actual == set(expected), "frozen source membership changed")
    git_rows = []
    for name, row in sorted(expected.items()):
        data = (SOURCE / name).read_bytes()
        need(len(data) == row["bytes"] and sha(data) == row["sha256"], "frozen digest mismatch: " + name)
        blob_sha = hashlib.sha1(("blob " + str(len(data)) + "\0").encode() + data).hexdigest()
        need(blob_sha == row["git_blob"], "Git blob digest mismatch: " + name)
        process = subprocess.run(["git", "cat-file", "blob", HEAD + ":" + PREFIX + name], cwd=REPO, capture_output=True)
        need(process.returncode == 0 and process.stdout == data, "actual immutable head blob differs: " + name)
        git_rows.append({"path": name, "bytes": len(data), "sha256": sha(data), "git_blob": blob_sha})
    manifest_data = load(SOURCE / "PUBLICATION_MANIFEST.json")
    pubrows = {row["path"]: row for row in manifest_data["files"]}
    need(len(pubrows) == len(manifest_data["files"]) == 25, "publication manifest duplicates/count")
    need(set(pubrows) | {"PUBLICATION_MANIFEST.json"} == actual, "publication manifest membership")
    for name, row in pubrows.items():
        need({key: expected[name][key] for key in ("path", "bytes", "sha256")} == row, "publication row mismatch")
    archive_rows = []
    inputs = load(SOURCE / "PUBLICATION_INPUTS.json")
    for entry in inputs["inputs"]:
        if not entry.get("distributed"):
            continue
        filename = entry["archive"]
        path = SOURCE / "archives" / filename
        raw = path.read_bytes()
        need(len(raw) == entry["bytes"] and sha(raw) == entry["sha256"], "archive input pin mismatch")
        directory = "author" if "AUTHOR_SAFE" in filename else "review2"
        with zipfile.ZipFile(path) as z:
            infos = z.infolist()
            names = [info.filename for info in infos]
            need(len(names) == len(set(names)) == entry["member_count"], "ZIP duplicate/count")
            need(set(names) == {p.name for p in (SOURCE / directory).iterdir()}, "ZIP closed membership")
            need(z.testzip() is None, "ZIP CRC")
            members = []
            ends = []
            for info in infos:
                name = info.filename
                need(name == PurePosixPath(name).name and name not in ("", ".", "..") and "\\" not in name, "ZIP unsafe name")
                need(not info.is_dir() and not info.flag_bits & 1, "ZIP encrypted/directory")
                mode = info.external_attr >> 16
                need(not stat.S_ISLNK(mode), "ZIP symlink")
                need(not stat.S_IFMT(mode) or stat.S_ISREG(mode), "ZIP special member")
                data = z.read(info)
                need(data == (SOURCE / directory / name).read_bytes(), "ZIP/member byte mismatch")
                local = struct.unpack_from("<4s5H3I2H", raw, info.header_offset)
                need(local[0] == b"PK\x03\x04", "ZIP local signature")
                nlen, xlen = local[-2:]
                lname = raw[info.header_offset + 30:info.header_offset + 30 + nlen].decode("utf-8" if info.flag_bits & 0x800 else "cp437")
                need(lname == name, "ZIP local name disagreement")
                need(local[2] == info.flag_bits and local[3] == info.compress_type, "ZIP local metadata disagreement")
                need(not info.flag_bits & 8, "data descriptor not independently implemented")
                need(local[6:9] == (info.CRC, info.compress_size, info.file_size), "ZIP local sizes/CRC disagreement")
                ends.append((info.header_offset, info.header_offset + 30 + nlen + xlen + info.compress_size))
                members.append({"path": name, "bytes": len(data), "sha256": sha(data), "mode": oct(mode), "is_code": name.endswith(".py")})
            ends.sort()
            need(ends[0][0] == 0 and all(a[1] == b[0] for a, b in zip(ends, ends[1:])), "ZIP preamble/gaps/overlap")
            eocd = raw.rfind(b"PK\x05\x06")
            need(eocd >= 0 and eocd + 22 + struct.unpack_from("<H", raw, eocd + 20)[0] == len(raw), "ZIP trailer")
            fields = struct.unpack_from("<4s4H2IH", raw, eocd)
            need(fields[1] == fields[2] == 0 and fields[3] == fields[4] == len(infos), "ZIP multidisk/count")
            need(ends[-1][1] == fields[6] and fields[6] + fields[5] == eocd, "ZIP central extent")
            archive_rows.append({"archive": filename, "members": members, "safe": True, "exact_parity": True})
    primary_meta = load(SOURCE / "author/PUBLIC_METADATA.json")
    corpus_locations = {
        "catalog.json": REPO / "unsolved_math_prioritization/catalog.json",
        "problems.json": REPO / "unsolved_math_prioritization/cache/problems.json",
        "research_results.json": REPO / "unsolved_math_prioritization/cache/research_results.json",
    }
    corpus_rows = []
    parsed = {}
    for row in primary_meta["corpora"]:
        name = row["public_dataset_label"]
        path = corpus_locations[name]
        pin = stream_pin(path)
        need(pin == {key: row[key] for key in ("bytes", "sha256")}, "whole corpus mismatch")
        # Whole corpus is parsed locally for exact target authentication only.
        # Raw records and other-status PR evidence are never emitted or audited.
        parsed[name] = load(path)
        corpus_rows.append({"label": name, **pin, "whole_file_authenticated": True})
    problems = parsed["problems.json"]
    need(type(problems) is list, "unknown problem corpus shape")
    matching = [row for row in problems if str(row.get("id")) == "9900008"]
    need(len(matching) == 1, "unique exact record")
    record = matching[0]
    report = parsed["research_results.json"].get("AMR-098-0008", {})
    pair = json.dumps([record, report], sort_keys=True).encode()
    need(len(pair) == 5255 and sha(pair) == "5ccf640125437cbff98966972b50bc5f73f19e1ae1735dff8a49829cfbcdc42a", "canonical exact target pair mismatch")
    catalog_rows = [row for row in parsed["catalog.json"] if str(row.get("id")) == "9900008"]
    need(len(catalog_rows) == 1, "unique exact catalog row")
    catalog_row = catalog_rows[0]
    need(catalog_row["review_hash"] == sha(pair), "actual catalog review binding")
    need(catalog_row["statement_hash"] == sha(record["statement"].encode()), "actual catalog statement binding")
    pdf_rows = []
    filenames = ["some-open-probability-problems.pdf", "0906.2062.pdf", "1405.7566.pdf", "2112.13053.pdf", "2303.05137.pdf"]
    for row, name in zip(primary_meta["sources"], filenames):
        pin = stream_pin(EFFORT / "private_sources" / name)
        need(pin == {"bytes": row["pdf_bytes"], "sha256": row["pdf_sha256"]}, "primary PDF mismatch")
        need((EFFORT / "private_sources" / name).read_bytes().startswith(b"%PDF-"), "PDF magic")
        pdf_rows.append({"file": name, **pin, "matches_original_pin": True})
    result = {"timestamp_utc": datetime.now(timezone.utc).isoformat(), "status": "pass", "external_frozen_manifest_sha256": SOURCE_MANIFEST_PIN, "head": HEAD, "files": git_rows, "directories": sorted(directories), "archives": archive_rows, "whole_corpora": corpus_rows, "exact_target_pair": {"bytes": len(pair), "sha256": sha(pair), "actual_catalog_review_hash_matches": True, "statement_sha256": catalog_row["statement_hash"]}, "primary_pdfs": pdf_rows, "code_bodies": ["check_publication.py", "author/verify.py"], "code_read_before_execution": True, "third_party_content_redistributed": False}
    write("PROVENANCE_RESULTS.json", result)
    return result


def run_checked(command, cwd):
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(command, cwd=cwd, capture_output=True, timeout=60, env=env)
    return {"returncode": result.returncode, "stdout": result.stdout.decode(), "stderr": result.stderr.decode(), "stdout_sha256": sha(result.stdout)}


def replays():
    # The prior provenance output must exist; reauthenticate every candidate
    # byte against its externally pinned manifest before executing safe copies.
    provenance()
    private = AUDIT / "private_replay"
    private.mkdir(exist_ok=True)
    destination = private / "baseline path with spaces"
    need(not destination.exists(), "refuse overwrite of previous baseline")
    shutil.copytree(SOURCE, destination, copy_function=shutil.copyfile)
    rows = []
    modes = [[], ["-O"], ["-I"], ["-I", "-O"]]
    for flags in modes:
        for argument in ([], ["--self-test"], ["--integrity"]):
            result = run_checked([sys.executable, "-B"] + flags + [str(destination / "author/verify.py")] + argument, private)
            need(result["returncode"] == 0 and not result["stderr"], "author baseline execution failed")
            parsed = strict_json(result["stdout"])
            need(parsed["status"] == "pass", "author baseline status")
            if argument == ["--self-test"]:
                need(len(parsed["self_test"]["negative_controls"]) == 18 and all(row["rejected"] is True for row in parsed["self_test"]["negative_controls"]), "author negative controls")
                need(len(parsed["self_test"]["positive_variants"]) == 2, "author positive variants")
            rows.append({"script": "author/verify.py", "flags": flags, "args": argument, **result})
        for argument in ([], ["--self-test"]):
            result = run_checked([sys.executable, "-B"] + flags + [str(destination / "check_publication.py")] + argument, private)
            need(result["returncode"] == 0 and not result["stderr"], "publication baseline execution failed")
            parsed = strict_json(result["stdout"])
            need(parsed["status"] == "pass" and len(parsed["author_replays"]) == 8, "publication baseline status")
            if argument:
                need(len(parsed["negative_controls"]) == 5 and all(row["rejected"] is True for row in parsed["negative_controls"]), "publication negative controls")
            rows.append({"script": "check_publication.py", "flags": flags, "args": argument, **result})
    write("BASELINE_REPLAYS.json", {"timestamp_utc": datetime.now(timezone.utc).isoformat(), "runs": rows, "status": "pass", "top_level_runs": len(rows), "nested_author_replays": 64})
    return rows


def consistency():
    current = load(AUDIT / "BASELINE_REPLAYS.json")["runs"]
    author_runs = [row for row in current if row["script"] == "author/verify.py"]
    by_argument = {tuple(row["args"]): strict_json(row["stdout"]) for row in author_runs}
    historical = load(SOURCE / "author/verification_results.json")
    need(historical["all_passed"] is True and len(historical["executions"]) == 16, "historical author run extent")
    for row in historical["executions"]:
        argument = ("--self-test",) if row["self_test"] else ()
        need(row["exit_code"] == 0 and row["output"] == by_argument[argument], "historical author output not reproduced")
    fresh_review = load(SOURCE / "review2/REVIEW_METADATA.json")
    for row in fresh_review["supplemental_checker_runs"]:
        matches = [run for run in author_runs if run["flags"] == row["python_flags"] and run["args"] == [row["argument"]]]
        need(len(matches) == 1 and row["exit_code"] == 0 and matches[0]["stdout_sha256"] == row["stdout_sha256"], "review2 output not reproduced")
    need((SOURCE / "review2/checker_rerun.json").read_bytes() == next(row["stdout"].encode() for row in author_runs if row["args"] == ["--self-test"]), "review2 detailed output mismatch")
    publication = load(SOURCE / "PUBLICATION_CHECKS.json")
    for row in publication["runs"]:
        matches = [run for run in current if run["script"] == "check_publication.py" and run["flags"] == row["python_flags"] and run["args"] == [row["argument"]]]
        need(len(matches) == 1 and matches[0]["stdout_sha256"] == row["stdout_sha256"] and strict_json(matches[0]["stdout"]) == row["result"], "historical publication output not reproduced")
    # Frozen bindings are checked independently of the imported acceptance
    # verdicts. Omitted executables and their claimed 10,028 controls remain
    # historical testimony; these counts have not been reenacted here.
    a = load(SOURCE / "review2/ACCEPTANCE.json")
    bindings = {
        "frozen_author_archive": "archives/DIFFUSE_MASS_9900008_AUTHOR_SAFE_FREEZE.zip",
        "accepted_unchanged_proof": "author/PROOF.md",
        "reviewed_original_source_audit": "author/SOURCE_AUDIT.md",
        "acceptance_report": "review2/AUDIT.md",
        "required_credit_addendum": "CREDIT_ADDENDUM.md",
        "verification_metadata": "review2/REVIEW_METADATA.json",
    }
    for key, path in bindings.items():
        need(stream_pin(SOURCE / path) == {field: a[key][field] for field in ("bytes", "sha256")}, "independent acceptance binding mismatch")
    result = {"timestamp_utc": datetime.now(timezone.utc).isoformat(), "status": "pass", "historical_author_outputs_reproduced": 16, "historical_review2_output_hashes_reproduced": 8, "historical_publication_outputs_reproduced": 4, "acceptance_byte_bindings_checked": len(bindings), "historical_omitted_executable_replayed": False, "historical_independent_10028_controls_reasserted": False, "math_or_priority_verdict_imported": False}
    write("HISTORICAL_CONSISTENCY.json", result)
    provenance()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=["provenance", "replays", "consistency"])
    args = parser.parse_args()
    value = {"provenance": provenance, "replays": replays, "consistency": consistency}[args.phase]()
    print(json.dumps({"phase": args.phase, "status": "pass", "count": len(value)}))


if __name__ == "__main__":
    main()

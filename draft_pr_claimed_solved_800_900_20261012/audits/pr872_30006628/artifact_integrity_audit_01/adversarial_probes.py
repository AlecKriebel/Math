#!/usr/bin/env python3
"""Independent PR872 historical-artifact audit. No original file is changed.

Authenticate this harness and SOURCE_MANIFEST.json from an independent record.
The source-manifest literal below is the parent-supplied frozen trust anchor,
not an independently retrieved GitHub object. No Git command is used.
Raw corpora/PDFs are read only when --full-sources is supplied; never emitted.
"""
import argparse
import datetime
import hashlib
import importlib.util
import io
import json
import os
import pathlib
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

MANIFEST_SHA = "4589f9b70e9a65ae67356544b5ad59644290902bb9b3df80406710a22559e3f8"
WRAPPER_SHA = "11ca693b078d4616b34af6d340327b6dfc262d995a2f1c73b2b1bd4ff1f44eeb"
BUNDLES = [
    ("RANDOM_PROPERTY_T_30006628_AUTHOR_SAFE_FREEZE.zip", "RANDOM_PROPERTY_T_30006628_AUTHOR_EXTERNAL_MANIFEST.json"),
    ("RANDOM_PROPERTY_T_30006628_INDEPENDENT_AUDIT.zip", "RANDOM_PROPERTY_T_30006628_INDEPENDENT_AUDIT_MANIFEST.json"),
    ("RANDOM_PROPERTY_T_30006628_SECOND_INDEPENDENT_REVIEW_SAFE.zip", "RANDOM_PROPERTY_T_30006628_SECOND_INDEPENDENT_REVIEW_EXTERNAL_MANIFEST.json"),
]


def require(ok, label):
    if not ok:
        raise RuntimeError(label)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def pinned(path, pin):
    require(stat.S_ISREG(path.lstat().st_mode), "nonregular frozen input: " + path.name)
    raw = path.read_bytes()
    require(len(raw) == pin["bytes"] and sha(raw) == pin["sha256"], "pin mismatch: " + path.name)
    return raw


def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "duplicate JSON key")
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=pairs)


def frozen_inputs(base):
    raw = (base / "SOURCE_MANIFEST.json").read_bytes()
    require(sha(raw) == MANIFEST_SHA, "external frozen manifest mismatch")
    manifest = strict_json(raw)
    source = base / "source"
    names = [x["path"] for x in manifest["files"]]
    require(len(names) == len(set(names)), "duplicate frozen source path")
    require(set(names) == {x.name for x in source.iterdir()}, "frozen source file set")
    blobs = {}
    for row in manifest["files"]:
        raw = pinned(source / row["path"], row)
        git_blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        require(git_blob == row["git_blob"], "Git blob identifier mismatch")
        blobs[row["path"]] = raw
    outer = strict_json(blobs["PUBLICATION_MANIFEST.json"])
    require(set(x["path"] for x in outer["files"]) == set(names) - {"PUBLICATION_MANIFEST.json"}, "outer manifest coverage")
    for row in outer["files"]:
        require(len(blobs[row["path"]]) == row["bytes"] and sha(blobs[row["path"]]) == row["sha256"], "outer manifest pin")
    all_members = {}
    inventories = []
    for archive, manifest_name in BUNDLES:
        m = strict_json(blobs[manifest_name])
        rows = {x["path"]: x for x in m["members"]}
        require(len(rows) == len(m["members"]), "duplicate manifest member")
        archive_pin = m.get("zip", m.get("archive"))
        require(len(blobs[archive]) == archive_pin["bytes"] and sha(blobs[archive]) == archive_pin["sha256"], "external archive pin")
        with zipfile.ZipFile(io.BytesIO(blobs[archive])) as z:
            names = z.namelist()
            require(len(names) == len(set(names)) and set(names) == set(rows), "ZIP member set")
            for info in z.infolist():
                p = pathlib.PurePosixPath(info.filename)
                mode = info.external_attr >> 16
                require(not p.is_absolute() and ".." not in p.parts and "\\" not in info.filename, "unsafe archive path")
                require(not info.is_dir() and stat.S_IFMT(mode) in (0, stat.S_IFREG), "nonregular archive member")
                raw = z.read(info.filename)
                require(len(raw) == rows[info.filename]["bytes"] and sha(raw) == rows[info.filename]["sha256"], "member pin")
                require(info.filename not in all_members, "cross-archive duplicate")
                all_members[info.filename] = raw
        inventories.append({"archive": archive, "member_count": len(names)})
    for inner, loose in [
        ("random_property_t_30006628/PROOF.md", "PROOF.md"),
        ("random_property_t_30006628_independent_audit/INDEPENDENT_MATHEMATICAL_AUDIT.md", "INDEPENDENT_MATHEMATICAL_AUDIT.md"),
        ("random_property_t_30006628_second_review/INDEPENDENT_MATHEMATICAL_REVIEW.md", "SECOND_INDEPENDENT_MATHEMATICAL_REVIEW.md"),
    ]:
        require(all_members[inner] == blobs[loose], "readable copy binding")
    require(sha(blobs["verify_publication.py"]) == WRAPPER_SHA, "wrapper external pin")
    return manifest, blobs, all_members, inventories


def run_checked(wrapper, package, flags, extra=(), timeout=30):
    require(sha(wrapper.read_bytes()) == WRAPPER_SHA, "startup external wrapper mismatch")
    return subprocess.run([sys.executable, "-I", "-S", "-B", *flags, str(wrapper), "--package", str(package), *extra],
                          cwd=package.parent, capture_output=True, timeout=timeout)


def require_rejected(proc, reason):
    require(proc.returncode == 1 and not proc.stderr, "unexpected rejection process")
    data = json.loads(proc.stdout)
    require(data == {"status": "REJECTED", "reason": reason}, "wrong rejection reason")


def main(args):
    base = args.base.resolve()
    manifest, blobs, members, inventories = frozen_inputs(base)
    records = []
    def row(name, classification, **extra):
        records.append({"name": name, "classification": classification, **extra})
    with tempfile.TemporaryDirectory(prefix="pr872 independent artifacts ") as temp:
        root = pathlib.Path(temp)
        trusted_wrapper = root / "externally authenticated wrapper.py"
        trusted_wrapper.write_bytes(blobs["verify_publication.py"])
        def fixture(label):
            folder = root / label
            folder.mkdir()
            for name, raw in blobs.items():
                (folder / name).write_bytes(raw)
            return folder
        for mode, flags in [("normal", []), ("optimized", ["-O"])]:
            original = fixture(mode + " original")
            proc = run_checked(trusted_wrapper, original, flags, ["--verify-only"])
            result = json.loads(proc.stdout)
            require(proc.returncode == 0 and not proc.stderr and result["archive_member_count"] == 26, "baseline verify-only")
            row("verify_only", "positive_control", mode=mode, result=result)
            spec = importlib.util.spec_from_file_location("trusted_pr872_wrapper_" + mode, trusted_wrapper)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            for name in mod.PINS:
                copy = fixture(mode + " corrupt " + name)
                raw = (copy / name).read_bytes()
                (copy / name).write_bytes(bytes([raw[0] ^ 1]) + raw[1:])
                proc = run_checked(trusted_wrapper, copy, flags, ["--verify-only"])
                require_rejected(proc, "pin mismatch: " + name)
                row("corrupt_pinned_file", "expected_rejection", mode=mode, file=name)
            for kind in ("missing", "symlink", "directory", "fifo"):
                copy = fixture(mode + " " + kind)
                path = copy / BUNDLES[2][0]
                path.unlink()
                if kind == "symlink":
                    path.symlink_to(original / path.name)
                elif kind == "directory":
                    path.mkdir()
                elif kind == "fifo":
                    os.mkfifo(path)
                proc = run_checked(trusted_wrapper, copy, flags, ["--verify-only"], timeout=3)
                require_rejected(proc, "missing or unsafe file: " + path.name)
                row(kind + "_core_file", "expected_rejection", mode=mode)
            corrupt = root / (mode + " substituted startup.py")
            marker = root / (mode + " MUST_NOT_EXIST")
            corrupt.write_text("from pathlib import Path\nPath(" + repr(str(marker)) + ").write_text('executed')\n")
            try:
                run_checked(corrupt, original, flags, ["--verify-only"])
                raise RuntimeError("modified startup was executed")
            except RuntimeError as exc:
                require(str(exc) == "startup external wrapper mismatch", "wrong startup failure")
            require(not marker.exists(), "startup marker exists")
            row("modified_startup_external_guard", "expected_rejection_before_execution", mode=mode, marker_absent=True)
            for name in ["README.md", "PUBLICATION_ACCEPTANCE.json", "PREFLIGHT_VALIDATION.json", "QUEUE_DELTA.json", "PUBLICATION_MANIFEST.json"]:
                copy = fixture(mode + " unpinned " + name)
                (copy / name).write_text("deliberately altered unpinned wrapper metadata\n")
                proc = run_checked(trusted_wrapper, copy, flags, ["--verify-only"])
                require(proc.returncode == 0 and json.loads(proc.stdout)["status"] == "PASS", "historical unpinned coverage changed")
                row("outside_wrapper_pin_scope", "accepted_mutation_scope_limit", mode=mode, file=name)
            copy = fixture(mode + " extra file")
            (copy / "UNLISTED_EXTRA.txt").write_text("extra")
            proc = run_checked(trusted_wrapper, copy, flags, ["--verify-only"])
            require(proc.returncode == 0, "extra-file historical scope")
            row("extra_file", "accepted_mutation_scope_limit", mode=mode)
            alias = root / (mode + " parent symlink")
            alias.symlink_to(original, target_is_directory=True)
            proc = run_checked(trusted_wrapper, alias, flags, ["--verify-only"])
            require(proc.returncode == 0, "ancestor-symlink historical scope")
            row("package_directory_symlink", "accepted_alias_scope_limit", mode=mode)
            proc = run_checked(trusted_wrapper, original, flags, ["--catalog", str(root / "unused")])
            require_rejected(proc, "supply all four source locations or none")
            row("incomplete_source_arguments", "expected_rejection", mode=mode)
            # A source FIFO is not an authenticated source; this tests only whether
            # the historical wrapper rejects the nonregular path before reading it.
            fifo = root / (mode + " catalog fifo")
            os.mkfifo(fifo)
            try:
                run_checked(trusted_wrapper, original, flags,
                            ["--catalog", str(fifo), "--problems", str(root / "notread1"),
                             "--reports", str(root / "notread2"), "--pdf-dir", str(root)], timeout=1)
                raise RuntimeError("source FIFO unexpectedly returned")
            except subprocess.TimeoutExpired:
                row("source_catalog_fifo", "confirmed_pre_read_guard_gap", mode=mode, timeout_seconds=1)
        # These probes deliberately replace trusted in-memory PINS to reach the
        # parser. They are not attacks that bypass the actual immutable pins.
        for name, mutation in [("duplicate_manifest_member", "duplicate"), ("traversal_member", "traversal"),
                               ("absolute_member", "absolute"), ("backslash_member", "backslash"),
                               ("symlink_member", "symlink"), ("fifo_zip_metadata", "fifo")]:
            copy = fixture("resealed parser " + name)
            archive, meta_name = BUNDLES[0]
            m = json.loads(blobs[meta_name])
            if mutation == "duplicate":
                m["members"].append(dict(m["members"][0]))
            else:
                with zipfile.ZipFile(io.BytesIO(blobs[archive])) as z:
                    entries = [(i, z.read(i.filename)) for i in z.infolist()]
                target = entries[0][0].filename
                replacement = {"traversal": "../escape.txt", "absolute": "/escape.txt", "backslash": "x\\escape.txt"}.get(mutation, target)
                m["members"][0]["path"] = replacement
                buffer = io.BytesIO()
                with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as z:
                    for info, raw in entries:
                        if info.filename == target:
                            info.filename = replacement
                            if mutation == "symlink":
                                info.external_attr = (stat.S_IFLNK | 0o777) << 16
                            if mutation == "fifo":
                                info.external_attr = (stat.S_IFIFO | 0o600) << 16
                        z.writestr(info, raw)
                (copy / archive).write_bytes(buffer.getvalue())
            (copy / meta_name).write_text(json.dumps(m))
            saved = dict(mod.PINS)
            for file in [archive, meta_name]:
                raw = (copy / file).read_bytes()
                mod.PINS[file] = {"bytes": len(raw), "sha256": sha(raw)}
            try:
                try:
                    mod.verify(copy)
                    accepted = True
                    reason = None
                except ValueError as exc:
                    accepted = False
                    reason = str(exc)
                if mutation == "fifo":
                    require(accepted, "historical FIFO-mode metadata scope changed")
                    row(name, "accepted_resealed_parser_scope_limit", actual_files_written_regular=True)
                else:
                    require(not accepted, "resealed unsafe parser input accepted")
                    row(name, "resealed_parser_expected_rejection", reason=reason)
            finally:
                mod.PINS = saved
        if args.full_sources:
            source_metadata = strict_json(members["random_property_t_30006628/sources.json"])
            repo = args.repo.resolve()
            paths = {"catalog": repo / "unsolved_math_prioritization/catalog.json",
                     "problems": repo / "unsolved_math_prioritization/cache/problems.json",
                     "reports": repo / "unsolved_math_prioritization/cache/research_results.json"}
            loaded = {k: strict_json(pinned(p, source_metadata["corpus"][k])) for k,p in paths.items()}
            problem = [x for x in loaded["problems"] if str(x.get("id")) == "30006628"]
            require(len(problem) == 1, "exact problem count")
            report = loaded["reports"].get(problem[0]["problem_number"], {})
            canonical = json.dumps([problem[0], report], sort_keys=True).encode()
            cp = source_metadata["canonical_pair"]
            require(len(canonical) == cp["bytes"] and sha(canonical) == cp["sha256"], "complete canonical record pair")
            catalog = [x for x in loaded["catalog"] if str(x.get("id")) == "30006628"]
            require(len(catalog) == 1 and catalog[0]["review_hash"] == sha(canonical), "catalog pair binding")
            for pin in source_metadata["primary_sources"]:
                pinned(base / "private_sources" / pin["filename"], pin)
            row("independent_complete_source_binding", "positive_control", corpus_count=3,
                pdf_count=6, pair_bytes=len(canonical), pair_sha256=sha(canonical), report_record_empty=(report == {}))
            extra = []
            for key, path in paths.items():
                extra += ["--" + key, str(path)]
            extra += ["--pdf-dir", str(base / "private_sources")]
            full_receipts = []
            for mode, flags in [("normal", []), ("optimized", ["-O"])]:
                copy = fixture(mode + " full source replay")
                proc = run_checked(trusted_wrapper, copy, flags, extra, timeout=300)
                require(proc.returncode == 0 and not proc.stderr, "full-source wrapper failed")
                data = json.loads(proc.stdout)
                require(data["status"] == "PASS" and data["source_replay"] == "PASS", "source replay result")
                positives = sum(x["kind"] == "positive" for x in data["receipts"])
                negatives = sum(x["kind"] == "negative" for x in data["receipts"])
                require((positives, negatives) == (8,12), "historical receipt counts")
                full_receipts.append({"mode": mode, "stdout_bytes": len(proc.stdout), "stdout_sha256":sha(proc.stdout),
                                      "positive_diagnostic_receipts":positives,"negative_diagnostic_receipts":negatives,"result":data})
                row("full_source_wrapper_replay", "positive_control", mode=mode, positives=positives, negatives=negatives)
            require(full_receipts[0]["stdout_sha256"] == full_receipts[1]["stdout_sha256"], "outer normal/-O replay mismatch")
        else:
            full_receipts = []
    # Reauthenticate originals after all probes and temporary replay.
    frozen_inputs(base)
    counts = {}
    for x in records:
        counts[x["classification"]] = counts.get(x["classification"], 0) + 1
    result = {"timestamp_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "status":"PASS_WITH_DOCUMENTED_HISTORICAL_WRAPPER_LIMITS", "python":sys.version,
              "harness_optimized":not __debug__, "frozen_head":manifest["frozen_head"],
              "external_source_manifest_sha256":MANIFEST_SHA,
              "frozen_files_authenticated":15,"archive_members_authenticated":26,
              "inventories":inventories,"probe_counts_by_classification":counts,
              "probes":records,"full_source_replay_receipts":full_receipts,
              "originals_reauthenticated_after_probes":True,
              "limitations":["Finite diagnostics do not prove the all-length asymptotic theorem or priority.",
                              "Parent supplied frozen source manifest is the external trust anchor; no independent remote Git fetch.",
                              "Artificial resealed parser probes intentionally replace in-memory pins; they do not defeat immutable hashes.",
                              "Source FIFO test demonstrates availability limitation, not execution of unauthenticated code."]}
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status":result["status"], "counts":counts, "full_source_replays":len(full_receipts)},sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=pathlib.Path, required=True)
    parser.add_argument("--repo", type=pathlib.Path, required=True)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    parser.add_argument("--full-sources", action="store_true")
    main(parser.parse_args())

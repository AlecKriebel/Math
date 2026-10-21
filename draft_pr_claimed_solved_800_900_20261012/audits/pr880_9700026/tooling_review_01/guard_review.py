#!/usr/bin/env python3
"""Independent PR880 tooling probes. All fixtures are synthetic and disposable.

This is engineering evidence, never final paper/package assembly or a proof.
No network, Git, external communication, corpus writes, or PDF marker execution.
Run: python3 -I -S -B guard_review.py [--with-provenance]
"""
import argparse
import ast
import hashlib
import io
import json
import os
from pathlib import Path
import runpy
import shutil
import socket
import stat
import struct
import subprocess
import sys
import time
import warnings
import zipfile

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
WORKSPACE = BASE.parents[2]
PRIVATE = HERE / "private"
MARK = b"SYNTHETIC TOOLING FIXTURE -- NOT THE REAL PAPER OR PUBLICATION\n"
SOURCE_SHA = "b0b0cdc72798cfcffc5fefeec1de30ff422f54bde83d0f8a91fd2e6a87311d8b"
FILES = ["preprint/check_originals.py", "preprint/verify_package.py", "preprint/build_verification.py",
         "local_tools/pr880_verify_current_publication.py", "local_tools/pr880_assemble.py"]


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def row(path, raw):
    return {"path": path, "bytes": len(raw), "sha256": sha(raw)}


def put(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    path.chmod(0o644)  # Own byte copies only, never corpus inputs or hardlinks.


def index(blobs, outer=False):
    return encoded({"schema": "city-ode-current-publication-v1" if outer else "city-ode-verification-v1",
                    "problem_id": "9700026", "files": [row(n, r) for n, r in sorted(blobs.items())]})


def archive(blobs, alter=None, duplicate=False):
    stream = io.BytesIO()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for name, data in sorted(blobs.items()):
                info = zipfile.ZipInfo(name, (2026, 10, 15, 0, 0, 0))
                info.create_system = 3
                info.external_attr = (stat.S_IFREG | 0o644) << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                if alter:
                    alter(info)
                z.writestr(info, data, compress_type=info.compress_type, compresslevel=9)
            if duplicate:
                name = sorted(blobs)[0]
                z.writestr(name, blobs[name])
    return stream.getvalue()


class Review:
    def __init__(self, full):
        self.full = full
        self.receipts = []
        self.modules = {}
        self.candidate = {}
        self.start = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        self.runroot = PRIVATE / ("run_with_provenance" if full else "run_source_free")
        need(not self.runroot.exists(), "remove own old run fixture before repeating")
        self.runroot.mkdir(parents=True)

    def record(self, name, kind, passed, **details):
        self.receipts.append({"name": name, "kind": kind, "passed": bool(passed), **details})
        need(passed, "independent probe failed: " + name + " " + str(details))

    def reject(self, name, fn):
        try:
            fn()
        except (ValueError, OSError, KeyError, TypeError, OverflowError, zipfile.BadZipFile) as exc:
            self.record(name, "helper_rejection", True, exception=type(exc).__name__, reason=str(exc))
        else:
            self.record(name, "helper_rejection", False, reason="unexpected acceptance")

    def cli(self, name, script, args, expected="PASS", optimized=False, umask=0o022, timeout=240):
        flags = ["-I", "-S", "-B"] + (["-O"] if optimized else [])
        runtime_tmp = self.runroot / "runtime_tmp"
        runtime_tmp.mkdir(exist_ok=True)
        child_env = dict(os.environ)
        child_env["TMPDIR"] = str(runtime_tmp)
        proc = subprocess.run([sys.executable, *flags, str(script), *map(str, args)],
                              cwd=self.runroot, capture_output=True, timeout=timeout, umask=umask, env=child_env)
        try:
            result = json.loads(proc.stdout)
        except (ValueError, UnicodeError):
            result = None
        good = (not proc.stderr and isinstance(result, dict) and result.get("status") == expected
                and (proc.returncode == 0 if expected != "REJECTED" else proc.returncode != 0))
        self.record(name, "cli", good, optimized=optimized, umask=oct(umask), exit_code=proc.returncode,
                    stdout_bytes=len(proc.stdout), stdout_sha256=sha(proc.stdout), stderr_bytes=len(proc.stderr), result=result)
        return result

    def freeze(self):
        for file in FILES:
            raw = (BASE / file).read_bytes()
            self.candidate[file] = raw
            frozen = self.runroot / "tools" / file
            put(frozen, raw)
            self.modules[file] = runpy.run_path(str(frozen), run_name="independent_import_only")
            tree = ast.parse(raw)
            self.record(file + ":no_asserts", "static", not any(isinstance(n, ast.Assert) for n in ast.walk(tree)))
            self.record(file + ":no_stale_PR872", "static", b"PR872" not in raw and b"pr872" not in raw and b"9600044" not in raw)

    def common(self):
        tree = self.runroot / "common_tree"
        tree.mkdir()
        put(tree / "sub" / "file", b"guard fixture\n")
        for file, m in self.modules.items():
            prefix = file + ":"
            good = m["strict_json"](b'{"bytes": 7, "name": "ok", "p": 0.1}')
            self.record(prefix + "strict_json_positive", "helper_positive", good["bytes"] == 7)
            for label, raw in {"duplicate": b'{"a":1,"a":2}', "nan": b'{"a":NaN}', "inf": b'{"a":Infinity}',
                               "negative_inf": b'{"a":-Infinity}', "overflow": b'{"a":1e999}'}.items():
                self.reject(prefix + "json_" + label, lambda raw=raw: m["strict_json"](raw))
            for v in [True, False, -1, 1.0, "1", 256 * 1024 * 1024 + 1]:
                self.reject(prefix + "bytes_" + repr(v), lambda v=v: m["pin_row"]({"path": "safe", "bytes": v, "sha256": "0" * 64}))
            for bad in ["", "/abs", "../escape", "a/../b", "./a", "a//b", "a/", "a\\b", "a:b", "a\0b", "a\nb", "a\x7fb", "a" * 513, 7, True]:
                self.reject(prefix + "unsafe_path_" + repr(bad), lambda bad=bad: m["safe_name"](bad))
            m["closed_tree"](tree, {"sub/file"})
            self.record(prefix + "closed_tree_positive", "helper_positive", True)
            put(tree / "unlisted", b"x")
            self.reject(prefix + "unlisted_file", lambda: m["closed_tree"](tree, {"sub/file"}))
            (tree / "unlisted").unlink()
            (tree / "empty").mkdir()
            self.reject(prefix + "unlisted_empty_dir", lambda: m["closed_tree"](tree, {"sub/file"}))
            (tree / "empty").rmdir()
            (tree / "alias").symlink_to(tree / "sub" / "file")
            self.reject(prefix + "symlink_leaf_tree", lambda: m["closed_tree"](tree, {"sub/file", "alias"}))
            self.reject(prefix + "symlink_leaf_read", lambda: m["read_regular"](tree / "alias"))
            (tree / "alias").unlink()
            (tree / "aliasdir").symlink_to(tree / "sub", target_is_directory=True)
            self.reject(prefix + "symlink_dir_tree", lambda: m["closed_tree"](tree, {"sub/file", "aliasdir/file"}))
            self.reject(prefix + "symlink_dir_within", lambda: m["within"](tree, "aliasdir/file"))
            self.reject(prefix + "symlink_root", lambda: m["selected_root"](tree / "aliasdir"))
            (tree / "aliasdir").unlink()
            os.mkfifo(tree / "fifo")
            self.reject(prefix + "fifo_read", lambda: m["read_regular"](tree / "fifo"))
            self.reject(prefix + "fifo_tree", lambda: m["closed_tree"](tree, {"sub/file", "fifo"}))
            (tree / "fifo").unlink()
            sock = socket.socket(socket.AF_UNIX)
            try:
                previous_cwd = Path.cwd()
                try:
                    os.chdir(tree)
                    sock.bind("socket")  # Avoid the short Unix-socket absolute-path bound.
                finally:
                    os.chdir(previous_cwd)
                self.reject(prefix + "socket_tree", lambda: m["closed_tree"](tree, {"sub/file", "socket"}))
                self.reject(prefix + "socket_read", lambda: m["read_regular"](tree / "socket"))
            finally:
                sock.close()
                (tree / "socket").unlink()
            self.reject(prefix + "missing_file", lambda: m["closed_tree"](tree, {"sub/file", "missing"}))
            self.reject(prefix + "file_dir_collision", lambda: m["rows_map"]([row("a", b"x"), row("a/b", b"x")]))
            self.reject(prefix + "duplicate_row", lambda: m["rows_map"]([row("a", b"x"), row("a", b"x")]))
            self.reject(prefix + "read_declared_bound", lambda: m["read_regular"](tree / "sub/file", 1))
            self.reject(prefix + "read_limit", lambda: m["read_regular"](tree / "sub/file", limit=1))

    def original_fixture(self):
        raw = (BASE / "SOURCE_MANIFEST.json").read_bytes()
        need(sha(raw) == SOURCE_SHA, "external source manifest identity")
        manifest = json.loads(raw)
        blobs = {"root_evidence/SOURCE_MANIFEST.json": raw}
        for pin in manifest["files"]:
            data = (BASE / "source" / pin["path"]).read_bytes()
            need(len(data) == pin["bytes"] and sha(data) == pin["sha256"], "authentic source mismatch")
            need(hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest() == pin["git_blob"], "authentic Git mismatch")
            blobs["source/" + pin["path"]] = data
        self.record("source40_preflight", "identity", len(manifest["files"]) == 40,
                    source_manifest_sha256=sha(raw), bytes=sum(len(r) for n, r in blobs.items() if n.startswith("source/")))
        for name in ["check_originals.py", "verify_package.py", "build_verification.py"]:
            blobs[name] = self.candidate["preprint/" + name]
        for name in ["README.md", "note.tex", "note.pdf", "CURRENT_PRIORITY.md"]:
            blobs[name] = MARK + name.encode() + b"\n"
        blobs["metadata.json"] = encoded({"title": MARK.decode().strip(), "fixture": True})
        return blobs

    def write_tree(self, folder, blobs):
        folder.mkdir(parents=True)
        for n, data in blobs.items():
            put(folder / n, data)

    def make_spec(self, seed, blobs, kind, name):
        spec = {"schema": "city-ode-explicit-assembly-v1", "kind": kind,
                "files": [{"source": n, **row(n, data)} for n, data in sorted(blobs.items())]}
        path = self.runroot / (name + ".json")
        put(path, encoded(spec))
        return spec, path, sha(path.read_bytes())

    def materialize(self, blobs):
        seed = self.runroot / "seed"
        self.write_tree(seed, blobs)
        put(seed / "UNALLOWLISTED_PRIVATE_SENTINEL", MARK + b"must never be copied\n")
        spec, specpath, specsha = self.make_spec(seed, blobs, "portable", "portable_spec")
        portable_root = self.runroot / "synthetic_portable"
        assembler = self.runroot / "tools/local_tools/pr880_assemble.py"
        result = self.cli("assembler_positive_explicit_allowlist", assembler, [seed, specpath, specsha, portable_root], expected="ASSEMBLED_REQUIRES_INDEPENDENT_VERIFICATION")
        portable = dict(blobs)
        portable["package_index.json"] = (portable_root / "package_index.json").read_bytes()
        self.record("assembler_excludes_unallowlisted_file", "helper_positive", not (portable_root / "UNALLOWLISTED_PRIVATE_SENTINEL").exists())
        for kind in ["portable", "outer"]:
            required = dict(blobs) if kind == "portable" else {"README.md": MARK, "RESEARCH_LOG.md": MARK, "CURRENT_PUBLICATION.json": b"{}\n", "verify_current_publication.py": self.candidate["local_tools/pr880_verify_current_publication.py"]}
            for suffix in ["", "/x"]:
                bad = dict(required)
                index_name = "package_index.json" if kind == "portable" else "PUBLICATION_MANIFEST.json"
                bad[index_name + suffix] = b"{}\n" if not suffix else MARK
                badseed = self.runroot / ("bad_seed_" + kind + ("_child" if suffix else "_exact"))
                self.write_tree(badseed, bad)
                _, p, digest = self.make_spec(badseed, bad, kind, badseed.name + "_spec")
                out = self.runroot / (badseed.name + "_output")
                collision = self.cli("assembler_generated_index_collision_" + kind + repr(suffix), assembler, [badseed, p, digest, out], expected="REJECTED")
                self.record("assembler_exact_collision_guard_" + kind + repr(suffix), "semantics", collision["reason"] == "generated index file/directory collision")
                self.record("assembler_no_materialization_" + kind + repr(suffix), "filesystem", not out.exists())
        for label, output in [("ancestor", seed), ("source_collision", seed / "README.md")]:
            self.cli("assembler_output_" + label, assembler, [seed, specpath, specsha, output], expected="REJECTED")
        altered = dict(spec)
        altered["files"] = [dict(r) for r in spec["files"]]
        altered["files"][0]["bytes"] = True
        p = self.runroot / "bool_assembly_spec.json"; put(p, encoded(altered))
        self.cli("assembler_bool_bytes", assembler, [seed, p, sha(p.read_bytes()), self.runroot / "no_bool_output"], expected="REJECTED")
        return portable_root, portable, result["index_sha256"]

    def portable_tests(self, root, portable, pin):
        checker = root / "check_originals.py"
        verify = root / "verify_package.py"
        builder = root / "build_verification.py"
        for optimized in [False, True]:
            tag = "optimized" if optimized else "normal"
            r = self.cli("original_verify_only_" + tag, checker, ["--root", root, "--verify-only"], optimized=optimized)
            self.record("verify_only_truthful_" + tag, "semantics", r["source_replay"] == r["finite_diagnostics"] == "NOT_RUN" and r["receipts"] == [])
            r = self.cli("original_eight_replays_" + tag, checker, ["--root", root], optimized=optimized)
            self.record("source_free_truthful_" + tag, "semantics", r["source_replay"] == "NOT_RUN" and r["source_inputs_authenticated"] is False and len(r["receipts"]) == 8 and r["finite_diagnostics"] == "PASS")
            r = self.cli("portable_inventory_only_" + tag, verify, [pin, "--root", root], optimized=optimized)
            self.record("portable_no_full_truthful_" + tag, "semantics", r["full_replay"] == "NOT_RUN")
            self.cli("portable_full_umask077_" + tag, verify, [pin, "--root", root, "--full"], optimized=optimized, umask=0o077)
        for opt in [False, True]:
            out = self.runroot / ("builder_optimized" if opt else "builder_normal")
            r = self.cli("builder_positive_" + str(opt), builder, [root, pin, sha(portable["verify_package.py"]), out], optimized=opt)
            need(r["assembly_replay"]["full_replay"]["finite_diagnostics"] == "PASS", "builder must really replay")
        a = (self.runroot / "builder_normal/verification.zip").read_bytes()
        b = (self.runroot / "builder_optimized/verification.zip").read_bytes()
        self.record("builder_determinism_normal_optimized", "reproducibility", a == b and a == archive(portable), zip_sha256=sha(a), bytes=len(a))
        for label, output in [("input_root", root), ("inside_input", root / "output"), ("file_collision", root / "README.md")]:
            self.cli("builder_output_" + label, builder, [root, pin, sha(portable["verify_package.py"]), output], expected="REJECTED")
        for script in [checker, verify]:
            args = ["--root", root] if script == checker else [pin, "--root", root, "--full"]
            self.cli(script.name + ":partial_optional", script, [*args, "--catalog", self.runroot / "absent"], expected="REJECTED")
            self.cli(script.name + ":pdf2012_alone", script, [*args, "--pdf-2012", self.runroot / "absent"], expected="REJECTED")
        self.cli("portable_requires_full_for_sources", verify, [pin, "--root", root, "--catalog", "a", "--problems", "b", "--reports", "c", "--pdf-dir", "d"], expected="REJECTED")
        marker = self.runroot / "SHOULD_NEVER_EXECUTE"
        poisoned = self.runroot / "poisoned"
        self.write_tree(poisoned, portable)
        put(poisoned / "verify_package.py", ("from pathlib import Path\nPath(" + repr(str(marker)) + ").write_text('EXECUTED')\n").encode())
        self.cli("builder_altered_startup_marker_fixed_pins", builder, [poisoned, pin, sha(portable["verify_package.py"]), self.runroot / "poisoned_output"], expected="REJECTED")
        self.record("startup_marker_never_executed", "filesystem", not marker.exists())
        changed = {n: (poisoned/n).read_bytes() for n in portable if n != "package_index.json"}
        put(poisoned / "package_index.json", index(changed))
        newpin = sha((poisoned / "package_index.json").read_bytes())
        self.cli("builder_altered_startup_marker_resealed_index_old_verifier_pin", builder, [poisoned, newpin, sha(portable["verify_package.py"]), self.runroot / "poisoned_output2"], expected="REJECTED")
        self.record("resealed_startup_marker_never_executed", "filesystem", not marker.exists())
        for label, mutate in [("extra_empty", lambda p: (p/"unlisted_empty").mkdir()), ("extra_file", lambda p: put(p/"unlisted", MARK)),
                              ("fifo", lambda p: os.mkfifo(p/"extra_fifo")), ("leaf_alias", lambda p: ((p/"README.md").unlink(), (p/"README.md").symlink_to(root/"README.md"))),
                              ("directory_alias", lambda p: (shutil.rmtree(p/"source/author"), (p/"source/author").symlink_to(root/"source/author", target_is_directory=True)))]:
            damaged = self.runroot / ("portable_damage_" + label)
            self.write_tree(damaged, portable); mutate(damaged)
            self.cli("portable_rejects_" + label, verify, [pin, "--root", damaged], expected="REJECTED")
        invalid_indexes = {"duplicate": b'{"schema":"city-ode-verification-v1","schema":"city-ode-verification-v1","problem_id":"9700026","files":[]}',
                           "overflow": b'{"schema":"city-ode-verification-v1","problem_id":"9700026","files":[{"path":"safe","bytes":1e999,"sha256":"' + b'0'*64 + b'"}]}',
                           "nan": b'{"schema":"city-ode-verification-v1","problem_id":"9700026","files":[{"path":"safe","bytes":NaN,"sha256":"' + b'0'*64 + b'"}]}'}
        for label, value in [("bool_bytes", True), ("unsafe_path", "../escape")]:
            bad = json.loads(portable["package_index.json"])
            bad["files"][0]["bytes" if label == "bool_bytes" else "path"] = value
            invalid_indexes[label] = encoded(bad)
        for label, bad_index in invalid_indexes.items():
            damaged = self.runroot / ("invalid_index_" + label)
            changed = dict(portable); changed["package_index.json"] = bad_index
            self.write_tree(damaged, changed)
            for opt in [False, True]:
                self.cli("portable_index_" + label + "_O" + str(opt), verify, [sha(bad_index), "--root", damaged], expected="REJECTED", optimized=opt)
                self.cli("builder_index_" + label + "_O" + str(opt), builder, [damaged, sha(bad_index), sha(portable["verify_package.py"]), self.runroot / ("unused_" + label + str(opt))], expected="REJECTED", optimized=opt)
        return a

    def outer_tests(self, portable, zipraw):
        m = self.modules["local_tools/pr880_verify_current_publication.py"]
        prefix = "publication_20261015/"
        outer = {"README.md": MARK, "RESEARCH_LOG.md": MARK, "verify_current_publication.py": self.candidate["local_tools/pr880_verify_current_publication.py"]}
        outer["CURRENT_PUBLICATION.json"] = encoded({"zenodo_metadata": json.loads(portable["metadata.json"]), "fixture": True})
        for name, raw in portable.items():
            outer[prefix + "verification_package/" + name] = raw
        for dest, src in {"note.tex": "note.tex", "output/pdf/note.pdf": "note.pdf", "README.md": "README.md", "metadata.json": "metadata.json", "CURRENT_PRIORITY.md": "CURRENT_PRIORITY.md", "check_originals.py": "check_originals.py", "verify_package.py": "verify_package.py", "build_verification.py": "build_verification.py", "package_index.json": "package_index.json"}.items():
            outer[prefix + "preprint/" + dest] = portable[src]
        outer[prefix + "preprint/verification.zip"] = zipraw
        outer[prefix + "preprint/zenodo-deposit.json"] = encoded({"metadata": json.loads(portable["metadata.json"]), "files": m["DEPOSIT_FILES"]})
        for n, raw in portable.items():
            if n.startswith("source/") and n[7:] not in ["README.md", "PUBLICATION_MANIFEST.json"]:
                outer[n[7:]] = raw
        seed = self.runroot / "outer_seed"; self.write_tree(seed, outer)
        _, specpath, specsha = self.make_spec(seed, outer, "outer", "outer_spec")
        root = self.runroot / "synthetic_outer"
        assembler = self.runroot / "tools/local_tools/pr880_assemble.py"
        r = self.cli("assembler_outer_positive", assembler, [seed, specpath, specsha, root], expected="ASSEMBLED_REQUIRES_INDEPENDENT_VERIFICATION")
        wrapper = root / "verify_current_publication.py"
        for opt in [False, True]:
            tag = "optimized" if opt else "normal"
            r1 = self.cli("outer_positive_inventory_" + tag, wrapper, [r["index_sha256"], "--root", root], optimized=opt)
            self.record("outer_source_free_truthful_" + tag, "semantics", r1["inner_verifier_result"]["full_replay"] == "NOT_RUN" and r1["historical_wrapper_executed"] is False)
            r2 = self.cli("outer_positive_full_" + tag, wrapper, [r["index_sha256"], "--root", root, "--full"], optimized=opt)
            self.record("outer_full_eight_truthful_" + tag, "semantics", len(r2["inner_verifier_result"]["full_replay"]["receipts"]) == 8)
        self.cli("outer_partial_optional", wrapper, [r["index_sha256"], "--root", root, "--full", "--catalog", "absent"], expected="REJECTED")
        self.cli("outer_pdf2012_alone", wrapper, [r["index_sha256"], "--root", root, "--pdf-2012", "absent"], expected="REJECTED")
        for label, alter in [("symlink", lambda i: setattr(i, "external_attr", (stat.S_IFLNK | 0o644) << 16)),
                             ("mode", lambda i: setattr(i, "external_attr", (stat.S_IFREG | 0o600) << 16)),
                             ("timestamp", lambda i: setattr(i, "date_time", (2025, 1, 1, 0, 0, 0))),
                             ("platform", lambda i: setattr(i, "create_system", 0)),
                             ("stored", lambda i: setattr(i, "compress_type", zipfile.ZIP_STORED)),
                             ("extra", lambda i: setattr(i, "extra", b"\x01\x00\x00\x00")),
                             ("member_comment", lambda i: setattr(i, "comment", MARK))]:
            self.reject("outer_zip_" + label, lambda alter=alter: m["archive_copies"](archive(portable, alter), portable))
        self.reject("outer_zip_duplicates", lambda: m["archive_copies"](archive(portable, duplicate=True), portable))
        wrong = dict(portable); wrong["README.md"] = wrong["README.md"][:-1] + b"?"
        self.reject("outer_zip_payload_mismatch", lambda: m["archive_copies"](archive(wrong), portable))
        too_short = dict(portable); too_short["README.md"] = b""
        self.reject("outer_zip_declared_size_mismatch", lambda: m["archive_copies"](archive(too_short), portable))
        commented = bytearray(zipraw); commented[-2:] = struct.pack("<H", 1); commented += b"x"
        self.reject("outer_zip_archive_comment", lambda: m["archive_copies"](bytes(commented), portable))
        observations = {"trailing_bytes": zipraw + MARK, "prefix_bytes": MARK + zipraw}
        local = bytearray(zipraw)
        need(local[:4] == b"PK\x03\x04", "local header fixture")
        local[10:12] = struct.pack("<H", 2)  # Alter local DOS time only; central remains fixed.
        observations["local_timestamp_mismatch"] = bytes(local)
        for label, raw in observations.items():
            try:
                count = m["archive_copies"](raw, portable)
            except (ValueError, OSError, zipfile.BadZipFile) as exc:
                self.record("zip_representation_" + label, "boundary_observation", True, accepted=False, reason=str(exc))
            else:
                self.record("zip_representation_" + label, "boundary_observation", False, accepted=True, members=count,
                            limitation="Expected the revised outer wrapper to reject this previously accepted representation.")
        return root, r["index_sha256"]

    def original_archive_tests(self, portable):
        m = self.modules["preprint/check_originals.py"]
        author = portable["source/CITY_STABILITY_9700026_AUTHOR_SAFE_FREEZE.zip"]
        pins = json.loads(portable["source/CITY_STABILITY_9700026_AUTHOR_EXTERNAL_MANIFEST.json"])["files"]
        good = m["zip_payloads"](author, pins, "authentic author")
        self.record("original_zip_positive", "helper_positive", len(good) == 8)
        for name in ["source/audit_a/AUTHOR_SAFE_FREEZE.zip", "source/audit_a/author/verify.py", "source/author/verify.py"]:
            changed = dict(portable)
            changed[name] += MARK
            folder = self.runroot / ("source_mutation_" + name.replace("/", "_"))
            self.write_tree(folder, changed)
            self.cli("original_nested_or_readable_tamper_" + name, folder / "check_originals.py", ["--root", folder, "--verify-only"], expected="REJECTED")
        for label, alter in [("symlink", lambda i: setattr(i, "external_attr", (stat.S_IFLNK | 0o644) << 16)), ("platform", lambda i: setattr(i, "create_system", 0))]:
            self.reject("original_zip_" + label, lambda alter=alter: m["zip_payloads"](archive(good, alter), pins, "bad fixture"))
        self.reject("original_zip_duplicates", lambda: m["zip_payloads"](archive(good, duplicate=True), pins, "bad duplicate fixture"))

    def provenance(self, portable_root, outer_root, outerpin, portablepin):
        if not self.full:
            self.record("optional_provenance", "scope", True, status="NOT_RUN", reason="source-free independent run")
            return
        sources = {"catalog": WORKSPACE / "unsolved_math_prioritization/catalog.json", "problems": WORKSPACE / "unsolved_math_prioritization/cache/problems.json", "reports": WORKSPACE / "unsolved_math_prioritization/cache/research_results.json", "pdf_dir": BASE / "private_sources", "pdf_2012": BASE / "private_sources/1209.5120v1.pdf"}
        paths = [sources["catalog"], sources["problems"], sources["reports"], sources["pdf_dir"] / "cities-notes.pdf", sources["pdf_2012"]]
        before = [{"name": p.name, "bytes": p.stat().st_size, "mode": stat.S_IMODE(p.stat().st_mode), "sha256": sha(p.read_bytes())} for p in paths]
        checker = portable_root / "check_originals.py"
        args = ["--catalog", sources["catalog"], "--problems", sources["problems"], "--reports", sources["reports"], "--pdf-dir", sources["pdf_dir"], "--pdf-2012", sources["pdf_2012"]]
        for opt in [False, True]:
            tag = "optimized" if opt else "normal"
            r = self.cli("provenance_verify_only_" + tag, checker, ["--root", portable_root, "--verify-only", *args], optimized=opt)
            self.record("provenance_verify_only_truthful_" + tag, "semantics", r["source_inputs_authenticated"] is True and r["source_replay"] == r["finite_diagnostics"] == "NOT_RUN" and not r["receipts"])
            r = self.cli("provenance_full_" + tag, checker, ["--root", portable_root, *args], optimized=opt)
            self.record("provenance_full_ten_receipts_" + tag, "semantics", r["source_replay"] == "PASS" and len(r["receipts"]) == 10)
        for script, prefix, root, pin in [(portable_root/"verify_package.py", "portable", portable_root, portablepin), (outer_root/"verify_current_publication.py", "outer", outer_root, outerpin)]:
            self.cli(prefix + "_provenance_full_positive", script, [pin, "--root", root, "--full", *args])
        alias = self.runroot / "2012_alias.pdf"; alias.symlink_to(sources["pdf_2012"])
        for label, replacement in [("wrong_2012_mapping", sources["pdf_dir"] / "cities-notes.pdf"), ("2012_leaf_alias", alias)]:
            bad = list(args); bad[-1] = replacement
            self.cli(label, checker, ["--root", portable_root, "--verify-only", *bad], expected="REJECTED")
        after = [{"name": p.name, "bytes": p.stat().st_size, "mode": stat.S_IMODE(p.stat().st_mode), "sha256": sha(p.read_bytes())} for p in paths]
        self.record("provenance_all_inputs_unchanged", "identity", before == after, inputs=after)

    def finish(self, success):
        finalpins = [row(f, raw) for f, raw in sorted(self.candidate.items())]
        still = all((BASE / p["path"]).read_bytes() == self.candidate[p["path"]] for p in finalpins)
        result = {"schema": "pr880-independent-tooling-receipts-v1", "scope": "Engineering tooling review using synthetic paper fixtures. No final assembly, mathematical/priority certification, external action, or repeated PDF marker.",
                  "start_utc": self.start, "end_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "with_provenance": self.full,
                  "harness_sha256": sha(Path(__file__).read_bytes()), "candidate_files": finalpins, "candidate_unchanged_during_run": still,
                  "success": bool(success and still), "probe_count": len(self.receipts), "receipts": self.receipts}
        out = HERE / ("RECEIPTS_WITH_PROVENANCE.json" if self.full else "RECEIPTS_SOURCE_FREE.json")
        put(out, encoded(result))
        shutil.rmtree(self.runroot)
        print(json.dumps({"success": result["success"], "probe_count": len(self.receipts), "receipt": out.name, "sha256": sha(out.read_bytes()), "private_run_removed": not self.runroot.exists()}))
        return result["success"]

    def run(self):
        ok = False
        try:
            self.freeze()
            self.common()
            blobs = self.original_fixture()
            root, portable, pin = self.materialize(blobs)
            zipraw = self.portable_tests(root, portable, pin)
            outer, outerpin = self.outer_tests(portable, zipraw)
            self.original_archive_tests(portable)
            self.provenance(root, outer, outerpin, pin)
            ok = True
        finally:
            self.finish(ok)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--with-provenance", action="store_true")
    args = parser.parse_args()
    Review(args.with_provenance).run()

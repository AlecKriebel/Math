#!/usr/bin/env python3
"""Offline adversarial probes of an exact frozen checkpoint-tool source.

All fixture writes remain under this review folder. The real subprocess entry
point is disabled, and every GitHub API operation is replaced by a local model.
"""
import ast
import base64
import contextlib
import datetime as dt
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import random
import shutil
import socket
import subprocess
import sys
import types
from unittest import mock
import zipfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
LIVE = HERE.parent.parent
RESULTS = []
EVENTS = []


def digest(kind, data):
    return hashlib.sha1(kind.encode() + b" " + str(len(data)).encode() + b"\0" + data).hexdigest()


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def load_snapshot(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def blocked(*args, **kwargs):
    raise AssertionError("A real subprocess/network call was attempted")


def record(name, function):
    try:
        details = function()
    except Exception as exc:
        RESULTS.append({"name": name, "passed": False, "exception": type(exc).__name__, "detail": str(exc)})
    else:
        RESULTS.append({"name": name, "passed": True, "details": details})


def expect_error(function, text):
    try:
        function()
    except (RuntimeError, ValueError, KeyError, FileNotFoundError) as exc:
        assert text in str(exc), (text, str(exc))
        return str(exc)
    raise AssertionError("Expected rejection: " + text)


def pdf_bytes():
    parts = [b"%PDF-1.7\n%\xe2\xe3\xcf\xd3\n"]
    offsets = [0]
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Count 1 /Kids [3 0 R] >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 10 10] /Contents 4 0 R >>",
        b"<< /Length 0 >>\nstream\n\nendstream",
    ]
    for i, content in enumerate(objects, 1):
        offsets.append(sum(map(len, parts)))
        parts.append(str(i).encode() + b" 0 obj\n" + content + b"\nendobj\n")
    start = sum(map(len, parts))
    parts.append(b"xref\n0 5\n0000000000 65535 f \n")
    parts.extend(f"{offset:010d} 00000 n \n".encode() for offset in offsets[1:])
    parts.append(b"trailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n" + str(start).encode() + b"\n%%EOF\n")
    return b"".join(parts)


def zip_bytes():
    memory = io.BytesIO()
    with zipfile.ZipFile(memory, "w", zipfile.ZIP_DEFLATED) as archive:
        info = zipfile.ZipInfo("all-bytes.bin", date_time=(2020, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        archive.writestr(info, bytes(range(256)) * 4)
        info = zipfile.ZipInfo("unicode.txt", date_time=(2020, 1, 1, 0, 0, 0))
        archive.writestr(info, "café — Ω — 𐍈\n".encode())
    return memory.getvalue()


PDF = pdf_bytes()
ZIP = zip_bytes()
UTF8 = "café — Ω — 𐍈\0\r\n\ufeffe\u0301\n".encode()
EXTRAS = [
    "remote_checkpoint.py",
    "reviews/inventory_adversary_02/REMOTE_CHECKPOINT_REVIEW.md",
    "reviews/pr0248_ledger_repair_adversary/REVIEW.md",
    "reviews/pr0248_ledger_repair_adversary/VERIFICATION.json",
]


class FakeGitHub:
    """Independent Git-object model with local JSON request round trips."""

    def __init__(self, root, selected, fault=None, races=0):
        self.root = root
        self.folder = root.name
        self.selected = selected
        self.fault = fault
        self.races = races
        self.calls = []
        self.trees = {}
        self.blobs = {}
        self.commits = {}
        self.ref_updates = []
        self.pending = None
        self.sequence = 0
        leaves = {
            "other.txt": self.blob_entry(b"unrelated root file\n", mode="100755"),
            "other_folder/keep.bin": self.blob_entry(b"\x00\xffoutside"),
            "submodule": {"mode": "160000", "type": "commit", "sha": "7" * 40},
            self.folder + "/foreign_nested/keep.bin": self.blob_entry(b"\xffowned-folder-unselected", mode="100755"),
            self.folder + "/foreign_link": self.blob_entry(b"foreign_nested/keep.bin", mode="120000"),
        }
        for name in selected:
            leaves[self.folder + "/" + name] = self.blob_entry(b"old:" + name.encode())
        self.initial_leaves = dict(leaves)
        self.ref = self.make_commit(self.make_tree(leaves), [], "initial")
        self.initial_ref = self.ref

    def blob_entry(self, data, mode="100644"):
        sha = digest("blob", data)
        self.blobs[sha] = data
        return {"mode": mode, "type": "blob", "sha": sha}

    def make_node(self, entries):
        ordered = sorted(entries, key=lambda name: name.encode() + (b"/" if entries[name]["type"] == "tree" else b""))
        raw = b"".join(entries[name]["mode"].lstrip("0").encode() + b" " + name.encode() + b"\0" + bytes.fromhex(entries[name]["sha"]) for name in ordered)
        sha = digest("tree", raw)
        self.trees[sha] = [{"path": name, **entries[name]} for name in ordered]
        return sha

    def make_tree(self, leaves):
        entries, groups = {}, {}
        for path, value in leaves.items():
            head, separator, tail = path.partition("/")
            if separator:
                groups.setdefault(head, {})[tail] = value
            else:
                entries[head] = dict(value)
        assert not (set(entries) & set(groups)), "Invalid leaf/directory collision in fixture"
        for name, group in groups.items():
            entries[name] = {"mode": "040000", "type": "tree", "sha": self.make_tree(group)}
        return self.make_node(entries)

    def recursive(self, sha, prefix=""):
        result = []
        for entry in self.trees[sha]:
            row = {**entry, "path": prefix + entry["path"]}
            result.append(row)
            if entry["type"] == "tree":
                result.extend(self.recursive(entry["sha"], row["path"] + "/"))
        return result

    def leaves(self, sha):
        return {row["path"]: {key: row[key] for key in ("mode", "type", "sha")} for row in self.recursive(sha) if row["type"] != "tree"}

    def make_commit(self, tree, parents, message):
        self.sequence += 1
        sha = digest("commit", json.dumps({"tree": tree, "parents": parents, "message": message, "sequence": self.sequence}, sort_keys=True).encode())
        self.commits[sha] = {"sha": sha, "tree": {"sha": tree}, "parents": [{"sha": p} for p in parents]}
        return sha

    def advance(self):
        leaves = self.leaves(self.commits[self.ref]["tree"]["sha"])
        name = f"parallel_writer/{self.sequence}.txt"
        leaves[name] = self.blob_entry(b"new unrelated concurrent work\n")
        self.ref = self.make_commit(self.make_tree(leaves), [self.ref], "concurrent work")

    def ancestor(self, ancestor, descendant):
        if ancestor == descendant:
            return True
        return any(self.ancestor(ancestor, row["sha"]) for row in self.commits[descendant]["parents"])

    def api(self, endpoint, method="GET", body=None):
        # Reproduce the real API wrapper's JSON/UTF-8 transport before modeling
        # the server. This catches Unicode/NUL transport assumptions locally.
        if body is not None:
            body = json.loads(json.dumps(body, ensure_ascii=False).encode("utf-8"))
        self.calls.append({"endpoint": endpoint, "method": method, "body": body})
        if endpoint == "git/ref/heads/main" and method == "GET":
            if self.pending and self.fault == "prepatch_race" and self.races:
                self.races -= 1
                self.pending = None
                self.advance()
            return {"object": {"sha": self.ref}}
        if endpoint.startswith("git/commits/") and method == "GET":
            return self.commits[endpoint.split("/")[-1]]
        if endpoint.startswith("git/trees/") and method == "GET":
            sha = endpoint.removeprefix("git/trees/").split("?")[0]
            tree = self.recursive(sha) if "?recursive=1" in endpoint else self.trees[sha]
            return {"sha": sha, "tree": tree, "truncated": self.fault == "truncated"}
        if endpoint == "git/blobs" and method == "POST":
            assert body["encoding"] == "base64"
            data = base64.b64decode(body["content"], validate=True)
            sha = self.blob_entry(data)["sha"]
            if self.fault == "blob_sha_mismatch":
                return {"sha": "0" * 40}
            if self.fault == "blob_sha_missing":
                return {}
            if self.fault == "blob_error":
                raise RuntimeError("simulated binary blob upload failed")
            return {"sha": sha}
        if endpoint == "git/trees" and method == "POST":
            leaves = self.leaves(body["base_tree"])
            for entry in body["tree"]:
                assert not ("content" in entry and "sha" in entry)
                assert entry["mode"] == "100644" and entry["type"] == "blob"
                sha = entry.get("sha")
                if "content" in entry:
                    data = entry["content"].encode()
                    if self.fault == "utf8_corruption" and entry["path"].endswith("utf8-nul.txt"):
                        data = data.replace(b"\0", b"")
                    sha = self.blob_entry(data)["sha"]
                assert sha in self.blobs
                leaves[entry["path"]] = {"mode": entry["mode"], "type": entry["type"], "sha": sha}
            if self.fault == "root_mode_corruption":
                leaves["other.txt"] = {**leaves["other.txt"], "mode": "100644"}
            if self.fault == "nested_delete":
                del leaves[self.folder + "/foreign_nested/keep.bin"]
            if self.fault == "nested_mode_corruption":
                name = self.folder + "/foreign_link"
                leaves[name] = {**leaves[name], "mode": "100644"}
            sha = self.make_tree(leaves)
            return {"sha": sha}
        if endpoint == "git/commits" and method == "POST":
            sha = self.make_commit(body["tree"], body["parents"], body["message"])
            self.pending = sha
            result = dict(self.commits[sha])
            if self.fault == "commit_parent_corruption":
                result["parents"] = []
            if self.fault == "commit_tree_corruption":
                result["tree"] = {"sha": "0" * 40}
            return result
        if endpoint == "git/refs/heads/main" and method == "PATCH":
            assert body["force"] is False
            if self.fault == "nonff_race" and self.races:
                self.races -= 1
                self.advance()
                raise RuntimeError("simulated non-fast-forward update rejection")
            if self.fault == "static_patch_failure":
                raise RuntimeError("simulated unchanged-parent patch failure")
            assert self.ancestor(self.ref, body["sha"]), "Ref update would not fast-forward"
            self.ref = body["sha"]
            self.pending = None
            self.ref_updates.append(dict(body))
            if self.fault == "postpatch_race":
                self.advance()
            return {"object": {"sha": self.ref}}
        if endpoint.startswith("compare/"):
            first, second = endpoint.removeprefix("compare/").split("...")
            if self.fault == "bad_compare":
                return {"status": "diverged"}
            return {"status": "identical" if first == second else ("ahead" if self.ancestor(first, second) else "diverged")}
        raise AssertionError("Unexpected offline API call: " + method + " " + endpoint)

    def mutations(self, endpoint=None):
        return [call for call in self.calls if call["method"] != "GET" and (endpoint is None or call["endpoint"] == endpoint)]


def fixture(name, fault=None, races=0, custom_names=None):
    repo = HERE / "fixtures" / name
    root = repo / "owned"
    if repo.exists():
        shutil.rmtree(repo)
    root.mkdir(parents=True)
    selected = {
        "STATE.json": json.dumps({"next_pr": 10, "last_completely_processed_pr": 9, "completion_estimate_percent": 42}).encode(),
        "dispositions.jsonl": b'{"pr":9,"disposition":"test"}\n',
        "artifact.pdf": PDF,
        "package.zip": ZIP,
        "utf8-nul.txt": UTF8,
        "all-bytes.bin": bytes(range(256)),
        "empty.txt": b"",
        "PR0292_PUBLICATION_VERIFICATION.json": b'{"fixture":true}\n',
    }
    for extra in EXTRAS:
        selected[extra] = b"fixture placeholder\n"
    for relative, data in selected.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    names = custom_names if custom_names is not None else [name for name in selected if name not in EXTRAS and not name.startswith("PR0292_")]
    fake = FakeGitHub(root, selected, fault=fault, races=races)
    return repo, root, names, selected, fake


def run_main(case, *, execute=True, expected_error=None, mutate=None, destination_fail_at=None, after_freeze=None):
    repo, root, names, selected, fake = case
    if mutate:
        mutate(root, names, selected, fake)
    calls = {"destination": 0}

    def destination():
        calls["destination"] += 1
        if calls["destination"] == destination_fail_at:
            raise RuntimeError("fixture destination mismatch")
        return "https://github.com/AlecKriebel/Math.git"

    def api(endpoint, method="GET", body=None):
        if after_freeze and not fake.calls:
            after_freeze(root)
        return fake.api(endpoint, method, body)

    stdout = io.StringIO()
    argv = ["remote_checkpoint.py", "--message", "offline binary safety control"] + (["--execute"] if execute else [])
    with mock.patch.multiple(TOOL, ROOT=root, REPO=repo, NAMES=names, api=api, verify_destination=destination), mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(stdout):
        if expected_error:
            error = expect_error(TOOL.main, expected_error)
            receipt = json.loads(stdout.getvalue()) if stdout.getvalue().strip() else None
        else:
            TOOL.main()
            error = None
            receipt = json.loads(stdout.getvalue())
    EVENTS.append({"case": repo.name, "calls": [{"endpoint": call["endpoint"], "method": call["method"]} for call in fake.calls], "destination_checks": calls["destination"], "error": error})
    return receipt, fake, calls


def direct_helper_property():
    generator = random.Random(292)
    payloads = [b"", b"plain\n", UTF8, b"\xef\xbb\xbfBOM\n", PDF, ZIP, bytes(range(256)) * 256, b"\xc0\x80", b"\xed\xa0\x80"]
    payloads.extend(bytes([i]) for i in range(256))
    payloads.extend(generator.randbytes(n) for n in (1, 2, 3, 7, 32, 256, 1024, 4096))
    rows, binary, text = [], 0, 0
    for i, data in enumerate(payloads):
        uploads = []

        def upload(endpoint, method="GET", body=None):
            assert endpoint == "git/blobs" and method == "POST"
            body = json.loads(json.dumps(body, ensure_ascii=False).encode())
            decoded = base64.b64decode(body["content"], validate=True)
            assert body["encoding"] == "base64" and decoded == data
            uploads.append(decoded)
            return {"sha": digest("blob", decoded)}

        with mock.patch.object(TOOL, "api", upload):
            entry = TOOL.overlay_entry("folder", f"payload-{i}", data)
        assert entry["path"] == f"folder/payload-{i}" and entry["mode"] == "100644" and entry["type"] == "blob"
        if "content" in entry:
            text += 1
            assert not uploads and "sha" not in entry
            transported = json.loads(json.dumps(entry, ensure_ascii=False).encode())
            assert transported["content"].encode() == data
        else:
            binary += 1
            assert len(uploads) == 1 and entry["sha"] == digest("blob", data)
        assert TOOL.blob_sha(data) == digest("blob", data)
        rows.append({"index": i, "bytes": len(data), "sha256": sha256(data), "git_blob": digest("blob", data), "mode": "inline_utf8" if "content" in entry else "base64_blob"})
    (HERE / "PAYLOAD_CONTROLS.json").write_text(json.dumps(rows, indent=2) + "\n")
    return {"payloads": len(payloads), "binary_uploads": binary, "utf8_inline": text, "pdf_bytes": len(PDF), "zip_bytes": len(ZIP)}


def positive_main(fault=None, races=0):
    case = fixture("success_" + (fault or "ordinary"), fault=fault, races=races)
    receipt, fake, calls = run_main(case)
    assert receipt["status"] == "pushed_and_verified" and len(fake.ref_updates) == 1
    leaves = fake.leaves(fake.commits[fake.ref]["tree"]["sha"])
    for name, data in case[3].items():
        assert leaves[case[1].name + "/" + name] == {"mode": "100644", "type": "blob", "sha": digest("blob", data)}
    for name, entry in fake.initial_leaves.items():
        if not (name.startswith(case[1].name + "/") and name.removeprefix(case[1].name + "/") in case[3]):
            assert leaves[name] == entry
    if fault in ("prepatch_race", "nonff_race", "postpatch_race"):
        assert any(name.startswith("parallel_writer/") for name in leaves)
    assert all(update["force"] is False for update in fake.ref_updates)
    assert (case[1] / "LATEST_CHECKPOINT_RECEIPT.json").is_file()
    return {"status": receipt["status"], "binary_uploads": len(fake.mutations("git/blobs")), "tree_creations": len(fake.mutations("git/trees")), "ref_updates": len(fake.ref_updates), "preserved_unrelated_leaves": len(fake.initial_leaves) - len(case[3]), "destination_checks": calls["destination"]}


def dry_run():
    case = fixture("dry_run")
    receipt, fake, _ = run_main(case, execute=False)
    assert not fake.mutations() and not (case[1] / "LATEST_CHECKPOINT_RECEIPT.json").exists()
    assert len(receipt["changed_paths"]) == len(case[3])
    assert any(name.endswith(".pdf") for name in receipt["changed_paths"])
    return {"read_calls": len(fake.calls), "mutations": 0, "receipt_files": len(receipt["files"])}


def already_recorded():
    case = fixture("already_recorded")
    fake = case[4]
    leaves = dict(fake.initial_leaves)
    for name, data in case[3].items():
        leaves[case[1].name + "/" + name] = fake.blob_entry(data)
    fake.ref = fake.make_commit(fake.make_tree(leaves), [fake.ref], "already checkpointed")
    receipt, fake, _ = run_main(case)
    assert receipt["status"] == "already_recorded" and not fake.mutations()
    return {"status": receipt["status"], "mutations": 0}


def failure(fault, message, *, before_commit=False, before_tree=False, patch_attempts=0):
    case = fixture("failure_" + fault, fault=fault)
    _, fake, _ = run_main(case, expected_error=message)
    if before_tree:
        assert not fake.mutations("git/trees")
    if before_commit:
        assert not fake.mutations("git/commits")
    assert len(fake.mutations("git/refs/heads/main")) == patch_attempts and not fake.ref_updates and fake.ref == fake.initial_ref
    return {"mutations_by_endpoint": {endpoint: len(fake.mutations(endpoint)) for endpoint in ("git/blobs", "git/trees", "git/commits", "git/refs/heads/main")}, "main_unchanged": True}


def cursor_guard(kind):
    case = fixture("cursor_" + kind)

    def mutate(root, names, selected, fake):
        if kind == "journal_gap":
            (root / "dispositions.jsonl").write_bytes(b'{"pr":10}\n')
        else:
            state = json.loads((root / "STATE.json").read_bytes())
            state["last_completely_processed_pr"] = 8
            (root / "STATE.json").write_text(json.dumps(state))

    message = "cursor/journal" if kind == "journal_gap" else "cursor mismatch"
    _, fake, _ = run_main(case, mutate=mutate, expected_error=message)
    assert not fake.calls
    return {"api_calls": 0}


def unsafe_path(kind):
    case = fixture("path_" + kind)

    def mutate(root, names, selected, fake):
        if kind == "traversal":
            names.append("../escape.txt")
            (root.parent / "escape.txt").write_bytes(b"not selected")
        elif kind == "absolute":
            names.append(str(root / "empty.txt"))
        elif kind == "symlink":
            target = root / "artifact.pdf"
            target.unlink()
            (root.parent / "outside.bin").write_bytes(PDF)
            target.symlink_to(root.parent / "outside.bin")
        elif kind == "nested_symlink":
            names.append("alias/file.txt")
            (root.parent / "outside").mkdir()
            (root.parent / "outside/file.txt").write_bytes(b"not selected")
            (root / "alias").symlink_to(root.parent / "outside", target_is_directory=True)
        elif kind == "missing":
            names.append("absent.bin")

    _, fake, _ = run_main(case, mutate=mutate, expected_error="Unsafe or absent checkpoint path")
    assert not fake.calls
    return {"api_calls": 0}


def stable_read_guard():
    case = fixture("read_changed")
    original = Path.read_bytes
    target = case[1] / "artifact.pdf"

    def change(path):
        data = original(path)
        if path == target:
            path.write_bytes(data + b"concurrent change")
        return data

    with mock.patch.object(Path, "read_bytes", change):
        _, fake, _ = run_main(case, expected_error="Checkpoint input changed during read")
    assert not fake.calls
    return {"api_calls": 0}


def frozen_retry_bytes():
    case = fixture("freeze_then_retry", fault="prepatch_race", races=1)
    receipt, fake, _ = run_main(case, after_freeze=lambda root: (root / "artifact.pdf").write_bytes(b"later local replacement"))
    leaves = fake.leaves(fake.commits[fake.ref]["tree"]["sha"])
    assert leaves[case[1].name + "/artifact.pdf"]["sha"] == digest("blob", PDF)
    assert receipt["status"] == "pushed_and_verified"
    return {"frozen_original_bytes_preserved": True, "tree_attempts": len(fake.mutations("git/trees"))}


def exhausted_races():
    case = fixture("three_prepatch_races", fault="prepatch_race", races=3)
    _, fake, _ = run_main(case, expected_error="Main advanced three times")
    assert len(fake.mutations("git/trees")) == 3 and not fake.mutations("git/refs/heads/main")
    assert fake.ref != fake.initial_ref
    return {"tree_attempts": 3, "ref_update_attempts": 0, "concurrent_main_work_preserved": True}


def destination_guard():
    case = fixture("destination_change")
    _, fake, calls = run_main(case, destination_fail_at=2, expected_error="destination mismatch")
    assert calls["destination"] == 2 and not fake.mutations("git/refs/heads/main")
    return {"ref_update_attempts": 0, "destination_checks": 2}


def postpush_verification_failure():
    case = fixture("postpush_ancestry_reject", fault="bad_compare")
    _, fake, _ = run_main(case, expected_error="ancestry not verified")
    assert len(fake.ref_updates) == 1
    assert not (case[1] / "LATEST_CHECKPOINT_RECEIPT.json").exists()
    return {"checkpoint_ref_was_updated_before_final_verification": True, "false_success_receipt": False}


def api_transport():
    captured = []

    def subprocess_stub(command, **kwargs):
        captured.append((command, kwargs))
        body = json.loads(kwargs["input"])
        assert body == {"encoding": "base64", "content": base64.b64encode(ZIP).decode("ascii")}
        return types.SimpleNamespace(returncode=0, stdout=b'{"sha":"test"}', stderr=b"")

    with mock.patch.object(subprocess, "run", subprocess_stub):
        result = REAL_API("git/blobs", "POST", {"encoding": "base64", "content": base64.b64encode(ZIP).decode("ascii")})
    command, kwargs = captured[0]
    assert command == ["gh", "api", "--hostname", "github.com", "repos/AlecKriebel/Math/git/blobs", "--method", "POST", "--input", "-"]
    assert "shell" not in kwargs and kwargs["capture_output"] is True
    assert result == {"sha": "test"}
    return {"fixed_api_host": "github.com", "fixed_repository": "AlecKriebel/Math", "structured_stdin": True, "shell": False}


def receipt_write_failure():
    case = fixture("receipt_enospc")

    def no_space(*args, **kwargs):
        raise RuntimeError("simulated ENOSPC after save")

    # main prints its final success receipt before writing it locally.
    captured = io.StringIO()
    with mock.patch.object(TOOL, "atomic_json", no_space), contextlib.redirect_stdout(captured):
        receipt, fake, _ = run_main(case, expected_error="ENOSPC after save")
    assert len(fake.ref_updates) == 1
    assert receipt["status"] == "pushed_and_verified"
    return {"checkpoint_ref_saved": True, "local_receipt_write_rejected": True, "printed_success_receipt_retained": True}


if __name__ == "__main__":
    START = dt.datetime.now(dt.timezone.utc).isoformat()
    with mock.patch.object(subprocess, "run", blocked), mock.patch.object(socket, "socket", blocked):
        load_snapshot("sweep_io", "reviewed_sweep_io.py")
        CHECKPOINT = load_snapshot("checkpoint", "reviewed_checkpoint.py")
        TOOL = load_snapshot("reviewed_remote_checkpoint", "reviewed_remote_checkpoint.py")
        REAL_API = TOOL.api
        record("273 payload exactness and strict UTF8/base64 dispatch", direct_helper_property)
        record("full binary and NUL-UTF8 checkpoint preserves unrelated entries", positive_main)
        record("dry-run uploads no blob/tree/commit/ref", dry_run)
        record("already recorded binary files cause no mutations", already_recorded)
        for fault in ("blob_sha_mismatch", "blob_sha_missing"):
            record(fault, lambda fault=fault: failure(fault, "binary blob identity mismatch", before_tree=True, before_commit=True))
        record("binary upload failure stops publication", lambda: failure("blob_error", "binary blob upload failed", before_tree=True, before_commit=True))
        record("UTF8 NUL corruption is caught by final tree hash", lambda: failure("utf8_corruption", "exact checkpoint overlay", before_commit=True))
        record("unrelated root mode corruption is rejected", lambda: failure("root_mode_corruption", "Unrelated root entry changed", before_commit=True))
        for fault in ("nested_delete", "nested_mode_corruption"):
            record(fault, lambda fault=fault: failure(fault, "exact checkpoint overlay", before_commit=True))
        for fault in ("commit_parent_corruption", "commit_tree_corruption"):
            record(fault, lambda fault=fault: failure(fault, "Commit binding mismatch"))
        record("truncated base tree is rejected", lambda: failure("truncated", "Tree listing truncated", before_tree=True, before_commit=True))
        record("retry after fresh-main check race", lambda: positive_main("prepatch_race", 1))
        record("retry after nonfastforward patch race", lambda: positive_main("nonff_race", 1))
        record("concurrent descendant after patch verifies as ahead", lambda: positive_main("postpatch_race"))
        record("three races abort before any ref mutation", exhausted_races)
        record("unchanged-parent patch failure is not retried", lambda: failure("static_patch_failure", "unchanged-parent patch failure", patch_attempts=1))
        for kind in ("journal_gap", "last_cursor"):
            record("state/journal " + kind, lambda kind=kind: cursor_guard(kind))
        for kind in ("traversal", "absolute", "symlink", "nested_symlink", "missing"):
            record("selected path " + kind, lambda kind=kind: unsafe_path(kind))
        record("read-time file change is rejected", stable_read_guard)
        record("retry uses frozen bytes despite later local change", frozen_retry_bytes)
        record("second destination guard stops ref mutation", destination_guard)
        record("ancestry failure cannot emit a success receipt", postpush_verification_failure)
        record("real API wrapper fixed host and structured binary body", api_transport)
        record("post-save local receipt failure remains distinguishable", receipt_write_failure)
    bindings = {name: sha256((HERE / name).read_bytes()) for name in ("reviewed_remote_checkpoint.py", "reviewed_checkpoint.py", "reviewed_sweep_io.py", "independent_controls.py")}
    output = {"started_at": START, "finished_at": dt.datetime.now(dt.timezone.utc).isoformat(), "completion_estimate_percent": 90, "source_sha256": bindings, "all_passed": all(row["passed"] for row in RESULTS), "tests": len(RESULTS), "passed": sum(row["passed"] for row in RESULTS), "network_or_subprocess_executed": False, "live_mutating_api_calls": 0, "results": RESULTS}
    (HERE / "CONTROL_RESULTS.json").write_text(json.dumps(output, indent=2) + "\n")
    (HERE / "API_EVENT_SUMMARY.json").write_text(json.dumps(EVENTS, indent=2) + "\n")
    print(json.dumps(output, indent=2))
    raise SystemExit(0 if output["all_passed"] else 1)

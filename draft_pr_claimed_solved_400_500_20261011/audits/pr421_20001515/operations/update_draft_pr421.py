#!/usr/bin/env python3
"""Manifest-bound PR421 author-packet update. Plan is the default; see README.md.

No checkout, index, QUEUE write, PR metadata write, merge, or release operation.
All remote mutations pass through an fsync'd append-only intent journal.
"""
import argparse
import base64
import datetime as dt
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys

REPO = "AlecKriebel/Math"
PR = 421
BRANCH = "research/20001515-explicit-cubulation"
PREFIX = "unsolved_math_prioritization/attempts/20001515/"
QUEUE = "unsolved_math_prioritization/QUEUE.md"
AUTHOR_NAME = "Alec Kriebel"  # Root-confirmed checkout git config identity, 2026-10-12.
AUTHOR_EMAIL = "me@aleckriebel.com"
SHA_RE = re.compile(r"[0-9a-f]{40}\Z")
HASH_RE = re.compile(r"[0-9a-f]{64}\Z")
SECRET_RE = re.compile(rb"(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)")


class GateError(Exception):
    pass


class Uncertain(Exception):
    pass


class PacketDrift(GateError):
    """Publication was observed, but the current packet no longer passes its gates."""
    def __init__(self, message, evidence):
        super().__init__(message)
        self.evidence = evidence


def require(ok, message):
    if not ok:
        raise GateError(message)


def utc():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def git_hash(kind, content):
    return hashlib.sha1(kind.encode() + b" " + str(len(content)).encode() + b"\0" + content).hexdigest()


class GhAPI:
    """No tokens are read, stored, or echoed. gh uses its existing authentication."""
    def call(self, method, path, body=None):
        command = ["gh", "api", "--method", method, "-H", "Accept: application/vnd.github+json",
                   "-H", "X-GitHub-Api-Version: 2022-11-28", f"repos/{REPO}/{path}"]
        if body is not None:
            command += ["--input", "-"]
        result = subprocess.run(command, input=None if body is None else json.dumps(body).encode(),
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        # Do not echo arbitrary HTTP/CLI output: it could contain authentication data.
        if result.returncode != 0:
            raise Uncertain(f"API {method} {path} did not produce a confirmed response")
        try:
            return json.loads(result.stdout)
        except (ValueError, UnicodeError) as exc:
            raise Uncertain(f"API {method} {path} response was not JSON") from exc


def api_get(api, path):
    return api.call("GET", path)


def queue_row(content, require_status=True):
    """Locate exact ID using table header names, never fixed column offsets."""
    headers = None
    rows = []
    for line in content.decode("utf-8").splitlines():
        if not line.strip().startswith("|"):
            continue
        fields = [x.strip() for x in line.strip().strip("|").split("|")]
        if "ID / code" in fields and "Status" in fields:
            require(headers is None, "ambiguous QUEUE table header")
            require(len(set(fields)) == len(fields), "duplicate QUEUE header")
            headers = fields
            continue
        if headers is not None and len(fields) == len(headers):
            row = dict(zip(headers, fields))
            if row["ID / code"].split("/", 1)[0].strip() == "20001515":
                rows.append(row)
    require(headers is not None and len(rows) == 1, "QUEUE exact ID must occur once")
    if require_status:
        require(rows[0]["Status"] == "claimed_solved", "QUEUE Status is not claimed_solved")
    return headers, rows[0]


def blob_bytes(api, sha):
    blob = api_get(api, "git/blobs/" + sha)
    require(blob.get("sha") == sha and blob.get("encoding") == "base64", "blob identity/encoding mismatch")
    try:
        content = base64.b64decode(blob["content"], validate=False)
    except (KeyError, ValueError, TypeError) as exc:
        raise GateError("invalid blob content") from exc
    require(git_hash("blob", content) == sha, "blob bytes do not match Git SHA")
    return content


def tree_hash(entries):
    names = sorted(entries, key=lambda name: (name + ("/" if entries[name]["type"] == "tree" else "")).encode("utf-8"))
    content = b"".join(("40000" if entries[name]["type"] == "tree" else entries[name]["mode"]).encode() +
                       b" " + name.encode("utf-8") + b"\0" + bytes.fromhex(entries[name]["sha"]) for name in names)
    return git_hash("tree", content)


def tree_entries(api, tree_sha, cache=None):
    """One complete nonrecursive tree object; untouched subtree bodies stay opaque."""
    if cache is not None and tree_sha in cache:
        return cache[tree_sha]
    response = api_get(api, "git/trees/" + tree_sha)
    require(response.get("sha") == tree_sha and response.get("truncated") is False,
            "tree identity mismatch or nonrecursive tree truncated")
    entries = {}
    for entry in response.get("tree", []):
        path = entry.get("path")
        require(isinstance(path, str) and normalized_path(path) == path and "/" not in path,
                "nonrecursive tree entry must be one normalized component")
        require(SHA_RE.fullmatch(entry.get("sha", "")) is not None, "invalid tree entry SHA")
        kind, mode = entry.get("type"), entry.get("mode")
        require((kind, mode) in {("tree", "040000"), ("blob", "100644"),
                                ("blob", "100755"), ("blob", "120000"), ("commit", "160000")},
                "unrecognized remote tree mode/type")
        require(path not in entries, "duplicate remote tree path")
        entries[path] = {"mode": mode, "type": kind, "sha": entry["sha"]}
    require(tree_hash(entries) == tree_sha, "nonrecursive tree bytes do not match its Git SHA")
    if cache is not None:
        cache[tree_sha] = entries
    return entries


def path_entry(api, root_sha, path, cache):
    parts = normalized_path(path).split("/")
    sha = root_sha
    for component in parts[:-1]:
        entry = tree_entries(api, sha, cache).get(component)
        if entry is None or entry["type"] != "tree":
            return None
        sha = entry["sha"]
    return tree_entries(api, sha, cache).get(parts[-1])


def admin_gate(api, expected_head, expected_branch):
    require(expected_branch == BRANCH, "only the fixed PR421 branch is permitted")
    require(SHA_RE.fullmatch(expected_head) is not None, "expected head must be an exact Git SHA")
    pr = api_get(api, f"pulls/{PR}")
    require(pr.get("number") == PR and pr.get("state") == "open" and pr.get("draft") is True,
            "PR421 must still be OPEN and draft")
    head = pr.get("head", {})
    require(head.get("sha") == expected_head and head.get("ref") == expected_branch,
            "PR421 source head or branch changed")
    require(head.get("repo", {}).get("full_name") == REPO, "PR421 must use this repository's branch")
    ref = api_get(api, "git/ref/heads/" + expected_branch)
    require(ref.get("object", {}).get("sha") == expected_head, "branch ref differs from expected source head")
    queued = api_get(api, "contents/" + QUEUE + "?ref=" + expected_head)
    require(queued.get("type") == "file" and queued.get("encoding") == "base64", "QUEUE response invalid")
    content = base64.b64decode(queued["content"])
    require(git_hash("blob", content) == queued.get("sha"), "QUEUE bytes do not match Git blob SHA")
    headers, row = queue_row(content)
    return {"checked_at_utc": utc(), "head_sha": expected_head, "branch": expected_branch,
            "state": pr["state"], "draft": pr["draft"], "queue_header": headers,
            "queue_selected_row": row, "queue_sha256": hashlib.sha256(content).hexdigest()}


def normalized_path(value):
    require(isinstance(value, str) and value and "\\" not in value and "\0" not in value,
            "path must be a nonempty POSIX relative path")
    require(not value.startswith("/") and all(p not in ("", ".", "..") for p in value.split("/")),
            "absolute, empty, dot, or traversal path rejected")
    return str(PurePosixPath(value))


def safe_candidate_name(path):
    lowered = path.lower().split("/")
    forbidden = {".git", "venv", ".venv", "__pycache__", "private", "private_sources", ".env"}
    require(not any(p in forbidden or p.startswith("private") or p.startswith(".env") or
                    "token" in p or "credential" in p or "secret" in p or
                    p in ("id_rsa", "id_ed25519") or p.endswith((".pyc", ".pyo")) for p in lowered),
            "private/runtime/credential candidate path rejected")


def open_regular(case, relative):
    """Open every component with O_NOFOLLOW; fd remains pinned across later renames."""
    relative = normalized_path(relative)
    fd = os.open(case, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        parts = relative.split("/")
        for component in parts[:-1]:
            next_fd = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = next_fd
        result = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
        info = os.fstat(result)
        if not stat.S_ISREG(info.st_mode):
            os.close(result)
            raise GateError("candidate is not a regular file")
        return result
    except OSError as exc:
        raise GateError("candidate path cannot be opened without symlinks") from exc
    finally:
        os.close(fd)


def read_fd(fd):
    with os.fdopen(fd, "rb") as source:
        return source.read()


def load_candidates(case, manifest_path, expected_head, expected_branch):
    manifest_bytes = read_fd(open_regular(case, manifest_path))
    try:
        manifest = json.loads(manifest_bytes)
    except (ValueError, UnicodeError) as exc:
        raise GateError("candidate manifest is not JSON") from exc
    require(set(manifest) in ({"expected_head", "expected_branch", "entries"},
                              {"schema_version", "expected_head", "expected_branch", "entries"}),
            "unknown/missing manifest fields")
    if "schema_version" in manifest:
        require(manifest["schema_version"] == 1, "unsupported candidate manifest schema version")
    require(manifest["expected_head"] == expected_head and manifest["expected_branch"] == expected_branch,
            "manifest source head/branch do not match explicit arguments")
    entries = manifest["entries"]
    require(isinstance(entries, list) and entries, "positive candidate allowlist must be nonempty")
    opened, bound, local_names, remote_names = [], [], set(), set()
    try:
        # Validate/open the entire positive allowlist before reading any candidate bytes.
        for entry in entries:
            require(isinstance(entry, dict) and set(entry) == {"local_path", "remote_path", "sha256"},
                    "unknown/missing candidate entry fields")
            local = normalized_path(entry["local_path"])
            remote = normalized_path(entry["remote_path"])
            safe_candidate_name(local)
            safe_candidate_name(remote)
            require(remote.startswith(PREFIX) and len(remote) > len(PREFIX), "remote candidate is outside PR421 packet")
            require(local not in local_names and remote not in remote_names, "duplicate candidate path")
            require(isinstance(entry["sha256"], str) and HASH_RE.fullmatch(entry["sha256"]) is not None,
                    "candidate SHA256 must be explicit")
            local_names.add(local)
            remote_names.add(remote)
            opened.append((entry.copy(), open_regular(case, local)))
        for entry, fd in opened:
            content = read_fd(fd)
            # The descriptor is now closed, but remove it from the cleanup list only after this read.
            entry["content"] = content
            require(hashlib.sha256(content).hexdigest() == entry["sha256"], "candidate content hash mismatch")
            require(SECRET_RE.search(content) is None, "candidate contains a recognizable authentication secret")
            entry["blob_sha"] = git_hash("blob", content)
            bound.append(entry)
    finally:
        for _, fd in opened:
            try:
                os.close(fd)
            except OSError:
                pass
    return bound, hashlib.sha256(manifest_bytes).hexdigest()


def expected_tree(api, base_tree_sha, entries):
    """Copy modified-directory entries; preserve opaque siblings; hash bottom-up."""
    trie = {"children": {}, "file": None}
    seen = set()
    for entry in entries:
        path = normalized_path(entry["remote_path"])
        require(path.startswith(PREFIX) and path not in seen, "duplicate or out-of-scope overlay path")
        require(SHA_RE.fullmatch(entry.get("blob_sha", "")) is not None, "invalid candidate Git blob SHA")
        seen.add(path)
        node = trie
        for component in path.split("/"):
            require(node["file"] is None, "candidate paths conflict as file and directory")
            node = node["children"].setdefault(component, {"children": {}, "file": None})
        require(not node["children"] and node["file"] is None, "candidate paths conflict as file and directory")
        node["file"] = entry
    cache, proof, expected = {}, {}, {}
    def descend(directory, base_sha, node):
        original = {} if base_sha is None else tree_entries(api, base_sha, cache)
        copied = {name: item.copy() for name, item in original.items()}
        for name, child in node["children"].items():
            path = name if not directory else directory + "/" + name
            old = copied.get(name)
            if child["file"] is not None:
                require(old is None or (old["type"] == "blob" and old["mode"] in ("100644", "100755")),
                        "candidate cannot replace a directory, symlink, or submodule")
                copied[name] = {"type": "blob", "mode": "100644" if old is None else old["mode"],
                                "sha": child["file"]["blob_sha"]}
                expected[path] = copied[name].copy()
            else:
                require(old is None or old["type"] == "tree", "candidate ancestor is a leaf, symlink, or submodule")
                copied[name] = {"type": "tree", "mode": "040000",
                                "sha": descend(path, None if old is None else old["sha"], child)}
        sha = tree_hash(copied)
        proof[directory] = {"base_sha": base_sha, "expected_sha": sha,
                            "base_entries": original, "expected_entries": copied}
        return sha
    root_sha = descend("", base_tree_sha, trie)
    return expected, proof, root_sha


def verify_tree(api, sha, expected, proof):
    require(proof[""]["expected_sha"] == sha, "overlay root binding mismatch")
    cache = {}
    for node in proof.values():
        actual = tree_entries(api, node["expected_sha"], cache)
        require(actual == node["expected_entries"], "created directory differs from complete Merkle overlay")
    for path, entry in expected.items():
        require(path_entry(api, sha, path, cache) == entry, "created candidate path differs from approved binding")


class Journal:
    def __init__(self, directory):
        directory.mkdir(mode=0o700, parents=True, exist_ok=False)
        self.directory = directory
        self.fd = os.open(directory / "journal.jsonl", os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        self.sync_directory(directory.parent)
        self.sync_directory(directory)

    @staticmethod
    def sync_directory(directory):
        fd = os.open(directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)

    def append(self, event):
        event = {"at_utc": utc(), **event}
        data = (json.dumps(event, sort_keys=True) + "\n").encode()
        offset = 0
        while offset < len(data):
            written = os.write(self.fd, data[offset:])
            require(written > 0, "journal write made no progress")
            offset += written
        os.fsync(self.fd)

    def receipt(self, value):
        content = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()
        fd = os.open(self.directory / "receipt.json", os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        try:
            with os.fdopen(fd, "wb") as destination:
                destination.write(content)
                destination.flush()
                os.fsync(destination.fileno())
            self.sync_directory(self.directory)
        except BaseException:
            raise

    def claim_head(self, head, planned_sha):
        # Survives process death and prevents a fresh run-id from blindly repeating
        # a write against the same original head after an uncertain outcome.
        claims = self.directory.parent / "head_claims"
        claims.mkdir(mode=0o700, exist_ok=True)
        self.sync_directory(self.directory.parent)
        fd = os.open(claims / (head + ".json"), os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        with os.fdopen(fd, "wb") as destination:
            destination.write((json.dumps({"run_id": self.directory.name, "planned_commit": planned_sha}) + "\n").encode())
            destination.flush()
            os.fsync(destination.fileno())
        self.sync_directory(claims)

    def claim_resume(self, original_run_id, original_hash, planned_sha):
        claims = self.directory.parent / "resume_claims"
        claims.mkdir(mode=0o700, exist_ok=True)
        self.sync_directory(self.directory.parent)
        fd = os.open(claims / (original_run_id + ".json"), os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        with os.fdopen(fd, "wb") as destination:
            destination.write((json.dumps({"original_run_id": original_run_id, "original_journal_sha256": original_hash,
                                          "resume_run_id": self.directory.name, "planned_commit": planned_sha}) + "\n").encode())
            destination.flush()
            os.fsync(destination.fileno())
        self.sync_directory(claims)

    def close(self):
        os.close(self.fd)


def mutate(api, journal, kind, path, body, expected_sha, verify):
    journal.append({"event": "intent", "kind": kind, "method": "POST", "path": path,
                    "expected_sha": expected_sha})
    try:
        answer = api.call("POST", path, body)
        require(answer.get("sha") == expected_sha, kind + " response SHA differs from deterministic identity")
        verify(expected_sha)
        disposition = "confirmed"
    except Exception:
        # Reconciliation is read-only. A present content-addressed object is sufficient.
        try:
            verify(expected_sha)
        except Exception as exc:
            journal.append({"event": "uncertain", "kind": kind, "expected_sha": expected_sha})
            raise Uncertain(kind + " outcome is uncertain; no retry or ref update permitted") from exc
        disposition = "reconciled_read_only"
    journal.append({"event": "object_verified", "kind": kind, "sha": expected_sha,
                    "disposition": disposition})
    return expected_sha


def commit_spec(tree_sha, parent_sha, message, date):
    require(isinstance(message, str) and message and "\0" not in message, "invalid commit message")
    message = message.rstrip("\n") + "\n"
    name, email = AUTHOR_NAME, AUTHOR_EMAIL
    require(isinstance(name, str) and isinstance(email, str) and name and email and
            not any(c in name + email for c in "\r\n<>\0"), "configured author identity is not safe for deterministic commit")
    epoch = int(dt.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc).timestamp())
    identity = f"{name} <{email}> {epoch} +0000"
    content = f"tree {tree_sha}\nparent {parent_sha}\nauthor {identity}\ncommitter {identity}\n\n{message}".encode("utf-8")
    person = {"name": name, "email": email, "date": date}
    return git_hash("commit", content), {"tree": tree_sha, "parents": [parent_sha], "message": message,
                                         "author": person, "committer": person}


def verify_commit(api, sha, spec, expected, proof):
    commit = api_get(api, "git/commits/" + sha)
    require(commit.get("sha") == sha and commit.get("tree", {}).get("sha") == spec["tree"] and
            [x.get("sha") for x in commit.get("parents", [])] == spec["parents"],
            "created commit identity/tree/parent mismatch")
    for field in ("author", "committer"):
        actual = commit.get(field, {})
        require(all(actual.get(key) == value for key, value in spec[field].items()), "created commit attribution mismatch")
    verify_tree(api, spec["tree"], expected, proof)
    submitted = spec["message"]
    actual_message = commit.get("message")
    one_final_newline_omitted = (submitted.endswith("\n") and not submitted.endswith("\n\n") and
                                 actual_message == submitted[:-1])
    require(actual_message == submitted or one_final_newline_omitted,
            "created commit message differs beyond one omitted final newline")


def readback(api, created_sha, expected, entries, verify_published=None):
    pr = api_get(api, f"pulls/{PR}")
    head = pr.get("head", {})
    actual = head.get("sha")
    require(isinstance(actual, str) and SHA_RE.fullmatch(actual) is not None, "readback head invalid")
    ref = api_get(api, "git/ref/heads/" + BRANCH)
    relation = "actual_head"
    if actual != created_sha:
        comparison = api_get(api, "compare/" + created_sha + "..." + actual)
        require(comparison.get("status") == "ahead" and
                comparison.get("merge_base_commit", {}).get("sha") == created_sha,
                "created commit is neither actual head nor verified ancestor")
        relation = "verified_ancestor"
    # Administrative QUEUE reading precedes ALL candidate tree/body verification,
    # including a reconciliation callback for the historical created commit.
    queued = api_get(api, "contents/" + QUEUE + "?ref=" + actual)
    require(queued.get("type") == "file" and queued.get("encoding") == "base64", "readback QUEUE response invalid")
    content = base64.b64decode(queued["content"])
    require(git_hash("blob", content) == queued.get("sha"), "readback QUEUE blob mismatch")
    header, row = queue_row(content, require_status=False)
    def administrative_drift(observation, reference):
        current_head = observation.get("head", {})
        reasons = []
        if current_head.get("sha") != actual or reference.get("object", {}).get("sha") != actual:
            reasons.append("PR/ref head changed or disagrees during readback")
        if current_head.get("ref") != BRANCH or current_head.get("repo", {}).get("full_name") != REPO:
            reasons.append("PR branch identity differs during readback")
        if observation.get("state") != "open":
            reasons.append("PR421 is no longer OPEN")
        if observation.get("draft") is not True:
            reasons.append("PR421 is no longer draft")
        return reasons
    before_candidates = api_get(api, f"pulls/{PR}")
    before_ref = api_get(api, "git/ref/heads/" + BRANCH)
    drift = administrative_drift(pr, ref) + administrative_drift(before_candidates, before_ref)
    if row["Status"] != "claimed_solved":
        drift.append("QUEUE Status is no longer claimed_solved")
    drift = list(dict.fromkeys(drift))
    bindings = [{key: entry[key] for key in ("local_path", "remote_path", "sha256", "blob_sha")} |
                {"checked_at_actual_head": False, "present_at_actual_head": None,
                 "expected_mode": expected[entry["remote_path"]]["mode"],
                 "actual_head_mode": None, "actual_head_sha256": None} for entry in entries]
    evidence = {"pr": PR, "url": f"https://github.com/{REPO}/pull/{PR}", "actual_head": actual,
            "created_commit": created_sha, "publication_relation": relation, "branch": head.get("ref"),
            "state": before_candidates.get("state"), "draft": before_candidates.get("draft"), "queue_header": header,
            "last_observed_head": before_candidates.get("head", {}).get("sha"),
            "last_observed_ref": before_ref.get("object", {}).get("sha"),
            "queue_selected_row": row, "queue_sha256": hashlib.sha256(content).hexdigest(),
            "files": bindings, "candidate_present_at_actual_head": None,
            "candidate_verification": "skipped_administrative_drift" if drift else "pending",
            "current_packet_verified": False, "current_packet_drift": drift}
    if drift:
        return evidence
    if verify_published is not None:
        verify_published()  # Only now may recovery verify candidate trees/commit.
    current_commit = api_get(api, "git/commits/" + actual)
    current_tree = current_commit["tree"]["sha"]
    tree_cache = {}
    for entry, binding in zip(entries, bindings):
        path = entry["remote_path"]
        actual_entry = path_entry(api, current_tree, path, tree_cache)
        matches = actual_entry == expected[path]
        actual_hash = None
        if actual_entry is not None and actual_entry["type"] == "blob":
            actual_hash = hashlib.sha256(blob_bytes(api, actual_entry["sha"])).hexdigest()
        binding.update({"checked_at_actual_head": True,
                        "present_at_actual_head": matches and actual_hash == entry["sha256"],
                        "actual_head_mode": None if actual_entry is None else actual_entry["mode"],
                        "actual_head_sha256": actual_hash})
    final_pr = api_get(api, f"pulls/{PR}")
    final_ref = api_get(api, "git/ref/heads/" + BRANCH)
    candidate_present = all(x["present_at_actual_head"] for x in bindings)
    drift = administrative_drift(final_pr, final_ref)
    if not candidate_present:
        drift.append("candidate byte bindings changed at actual head")
    evidence.update({"state": final_pr.get("state"), "draft": final_pr.get("draft"),
                     "last_observed_head": final_pr.get("head", {}).get("sha"),
                     "last_observed_ref": final_ref.get("object", {}).get("sha"),
                     "candidate_present_at_actual_head": candidate_present, "candidate_verification": "checked",
                     "current_packet_verified": not drift, "current_packet_drift": drift})
    return evidence


def run(api, case, manifest_path, expected_head, expected_branch, journal, apply=False,
        message="PR421: update reviewed author packet"):
    # This must happen before opening the manifest or any candidate file.
    administrative = admin_gate(api, expected_head, expected_branch)
    entries, manifest_hash = load_candidates(case, manifest_path, expected_head, expected_branch)
    base_commit = api_get(api, "git/commits/" + expected_head)
    require(base_commit.get("sha") == expected_head, "base commit identity mismatch")
    expected, merkle_proof, root_sha = expected_tree(api, base_commit["tree"]["sha"], entries)
    created_sha, spec = commit_spec(root_sha, expected_head, message, utc())
    bindings = [{key: entry[key] for key in ("local_path", "remote_path", "sha256", "blob_sha")} |
                {"mode": expected[entry["remote_path"]]["mode"]} for entry in entries]
    plan = {"format": "pr421-author-packet-merkle-admin-first-v5", "mode": "apply" if apply else "plan", "at_utc": utc(),
            "repo": REPO, "pr": PR, "expected_head": expected_head, "expected_branch": expected_branch,
            "administrative_gate": administrative, "manifest_sha256": manifest_hash, "files": bindings,
            "base_tree": base_commit["tree"]["sha"], "expected_tree": root_sha,
            "planned_commit": created_sha, "commit_spec": spec, "merkle_overlay": merkle_proof}
    journal.append({"event": "validated_plan", **plan})
    if not apply:
        journal.receipt(plan)
        return plan
    # Recheck the complete administrative gate after reading candidate bytes and before object writes.
    admin_gate(api, expected_head, expected_branch)
    journal.claim_head(expected_head, created_sha)
    for entry in entries:
        mutate(api, journal, "blob", "git/blobs",
               {"content": base64.b64encode(entry["content"]).decode(), "encoding": "base64"},
               entry["blob_sha"], lambda sha: require(blob_bytes(api, sha) == entry["content"], "created blob bytes mismatch"))
    overlays = [{"path": entry["remote_path"], **expected[entry["remote_path"]]} for entry in entries]
    mutate(api, journal, "tree", "git/trees", {"base_tree": plan["base_tree"], "tree": overlays}, root_sha,
           lambda sha: verify_tree(api, sha, expected, merkle_proof))
    mutate(api, journal, "commit", "git/commits", spec, created_sha,
           lambda sha: verify_commit(api, sha, spec, expected, merkle_proof))
    # Durable created-commit record precedes the only PATCH. Verify again before moving the ref.
    journal.append({"event": "created_commit_before_ref", "sha": created_sha, "parent": expected_head,
                    "tree": root_sha, "files": bindings})
    verify_commit(api, created_sha, spec, expected, merkle_proof)
    admin_gate(api, expected_head, expected_branch)
    return publish_ref(api, journal, plan, expected, entries)


def publish_ref(api, journal, plan, expected, entries):
    """Exactly one journaled non-force PATCH, then GET-only disposition."""
    created_sha, expected_head = plan["planned_commit"], plan["expected_head"]
    journal.append({"event": "intent", "kind": "ref", "method": "PATCH", "path": "git/refs/heads/" + BRANCH,
                    "expected_old_head": expected_head, "new_head": created_sha, "force": False})
    try:
        answer = api.call("PATCH", "git/refs/heads/" + BRANCH, {"sha": created_sha, "force": False})
        require(answer.get("object", {}).get("sha") == created_sha, "PATCH response did not confirm requested head")
        disposition = "confirmed"
    except Exception:
        disposition = "response_unconfirmed_read_only_reconciliation"
    try:
        published = readback(api, created_sha, expected, entries)
    except Exception as exc:
        journal.append({"event": "uncertain", "kind": "ref", "created_commit": created_sha})
        raise Uncertain("ref publication is uncertain; use read-only reconciliation, never retry PATCH blindly") from exc
    verified = published["current_packet_verified"]
    receipt = {**plan, "result": "published_current_packet_verified" if verified else "published_current_packet_drift",
               "publication_observed": True, "current_packet_verified": verified,
               "patch_disposition": disposition, "readback": published}
    journal.append({"event": "publication_observed", "created_commit": created_sha, "actual_head": published["actual_head"],
                    "publication_relation": published["publication_relation"]})
    journal.append({"event": "current_packet_verified" if verified else "current_packet_drift",
                    "actual_head": published["actual_head"], "readback": published})
    journal.receipt(receipt)
    if not verified:
        raise PacketDrift("publication observed, but current packet drifted: " + "; ".join(published["current_packet_drift"]) +
                          "; historical evidence is in receipt.json; no mutation retry permitted", receipt)
    return receipt


def resume_existing(api, case, original_run_id, manifest_path, expected_head, expected_branch, journal, apply=False):
    """Verify original objects; default GET-only; explicit apply performs no POSTs."""
    require(re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,79}", original_run_id) is not None,
            "invalid original run-id")
    require(original_run_id != journal.directory.name, "resume must use a fresh distinct run-id")
    administrative = admin_gate(api, expected_head, expected_branch)
    original_path = "private_sources/operations/runs/" + original_run_id + "/journal.jsonl"
    original_bytes = read_fd(open_regular(case, original_path))
    original_hash = hashlib.sha256(original_bytes).hexdigest()
    try:
        events = [json.loads(line) for line in original_bytes.splitlines()]
    except (ValueError, UnicodeError) as exc:
        raise GateError("original journal is incomplete; resume forbidden") from exc
    plans = [event for event in events if event.get("event") == "validated_plan"]
    require(len(plans) == 1 and plans[0].get("mode") == "apply", "resume requires one original validated apply plan")
    original = {key: value for key, value in plans[0].items() if key != "event"}
    require(original.get("phase") != "resume_existing_commit", "resume must refer to the original object-creation run")
    require(original.get("repo") == REPO and original.get("pr") == PR and
            original.get("expected_head") == expected_head and original.get("expected_branch") == expected_branch,
            "original plan source/repository/PR binding mismatch")
    ref_intents = [event for event in events if event.get("event") == "intent" and
                   (event.get("kind") == "ref" or event.get("method") == "PATCH")]
    commit_intents = [event for event in events if event.get("event") == "intent" and event.get("kind") == "commit"]
    require(not ref_intents and len(commit_intents) == 1, "original run must have one commit intent and zero ref intents")
    intent = commit_intents[0]
    require(intent.get("method") == "POST" and intent.get("path") == "git/commits" and
            intent.get("expected_sha") == original.get("planned_commit"), "original commit intent binding mismatch")
    claim_path = "private_sources/operations/runs/head_claims/" + expected_head + ".json"
    claim = json.loads(read_fd(open_regular(case, claim_path)))
    require(claim.get("run_id") == original_run_id and claim.get("planned_commit") == original["planned_commit"],
            "original source-head claim binding mismatch")
    entries, manifest_hash = load_candidates(case, manifest_path, expected_head, expected_branch)
    require(manifest_hash == original["manifest_sha256"], "resume candidate manifest differs from original plan")
    base = api_get(api, "git/commits/" + expected_head)
    require(base.get("sha") == expected_head and base.get("tree", {}).get("sha") == original["base_tree"],
            "original base commit/tree binding mismatch")
    expected, proof, tree_sha = expected_tree(api, original["base_tree"], entries)
    bindings = [{key: entry[key] for key in ("local_path", "remote_path", "sha256", "blob_sha")} |
                {"mode": expected[entry["remote_path"]]["mode"]} for entry in entries]
    require(bindings == original["files"] and proof == original.get("merkle_overlay") and
            tree_sha == original["expected_tree"], "resume candidate pins/Merkle proof differ from original plan")
    spec = original["commit_spec"]
    predicted, rebuilt_spec = commit_spec(tree_sha, expected_head, spec["message"], spec["author"]["date"])
    require(predicted == original["planned_commit"] and rebuilt_spec == spec,
            "original deterministic commit SHA/spec binding mismatch")
    verify_commit(api, predicted, spec, expected, proof)
    for entry in entries:
        require(blob_bytes(api, entry["blob_sha"]) == entry["content"], "existing commit candidate bytes differ from original pins")
    admin_gate(api, expected_head, expected_branch)
    plan = {**original, "format": "pr421-ref-only-resume-v5", "phase": "resume_existing_commit",
            "mode": "apply" if apply else "plan", "at_utc": utc(), "administrative_gate": administrative,
            "original_run_id": original_run_id, "original_journal_sha256": original_hash,
            "resume_run_id": journal.directory.name, "objects_created_by_resume": 0,
            "existing_commit_verified": True}
    journal.append({"event": "validated_plan", **plan})
    if not apply:
        journal.receipt(plan)
        return plan
    journal.claim_resume(original_run_id, original_hash, predicted)
    journal.append({"event": "resume_claimed", "original_run_id": original_run_id,
                    "original_journal_sha256": original_hash, "resume_run_id": journal.directory.name})
    require(hashlib.sha256(read_fd(open_regular(case, original_path))).hexdigest() == original_hash,
            "original journal changed before resume ref update")
    journal.append({"event": "existing_commit_before_ref", "sha": predicted, "parent": expected_head,
                    "tree": tree_sha, "files": bindings, "original_journal_sha256": original_hash})
    admin_gate(api, expected_head, expected_branch)
    return publish_ref(api, journal, plan, expected, entries)


def reconcile(api, case, run_id):
    """Only GET calls. Never resumes object creation or a ref update."""
    path = "private_sources/operations/runs/" + run_id + "/journal.jsonl"
    try:
        events = [json.loads(line) for line in read_fd(open_regular(case, path)).splitlines()]
    except (ValueError, UnicodeError) as exc:
        raise Uncertain("journal is incomplete or unreadable; no write resumption permitted") from exc
    plans = [event for event in events if event.get("event") == "validated_plan"]
    require(len(plans) == 1 and plans[0].get("mode") == "apply", "reconcile requires one apply plan")
    plan = plans[0]
    require(plan.get("repo") == REPO and plan.get("pr") == PR and plan.get("expected_branch") == BRANCH,
            "journal repository/PR/branch binding mismatch")
    ref_intents = [event for event in events if event.get("event") == "intent" and event.get("kind") == "ref"]
    require(len(ref_intents) <= 1, "journal contains repeated ref intents")
    if not ref_intents:
        return {"result": "no_ref_intent_recorded", "planned_commit": plan["planned_commit"],
                "last_intent": next((event for event in reversed(events) if event.get("event") == "intent"), None),
                "write_resumption_permitted": False}
    require(ref_intents[0].get("new_head") == plan["planned_commit"] and
            ref_intents[0].get("expected_old_head") == plan["expected_head"] and
            ref_intents[0].get("force") is False, "journal ref-intent binding mismatch")
    # Recover mode/hash bindings from the durable plan without touching research
    # trees. The actual-head administrative gate decides whether verification runs.
    expected = {}
    for entry in plan["files"]:
        path = normalized_path(entry["remote_path"])
        require(path.startswith(PREFIX) and path not in expected and entry.get("mode") in ("100644", "100755"),
                "journal candidate path/mode binding invalid")
        require(SHA_RE.fullmatch(entry.get("blob_sha", "")) is not None, "journal candidate blob binding invalid")
        expected[path] = {"type": "blob", "mode": entry["mode"], "sha": entry["blob_sha"]}
    def verify_published():
        if plan.get("phase") == "resume_existing_commit":
            original_path = "private_sources/operations/runs/" + plan["original_run_id"] + "/journal.jsonl"
            require(hashlib.sha256(read_fd(open_regular(case, original_path))).hexdigest() == plan["original_journal_sha256"],
                    "original journal changed since resume binding")
        rebuilt, merkle_proof, tree_sha = expected_tree(api, plan["base_tree"], plan["files"])
        require(tree_sha == plan["expected_tree"] and rebuilt == expected, "journal overlay tree/file binding mismatch")
        require(merkle_proof == plan.get("merkle_overlay"), "journal Merkle proof binding mismatch")
        verify_commit(api, plan["planned_commit"], plan["commit_spec"], expected, merkle_proof)
    result = readback(api, plan["planned_commit"], expected, plan["files"], verify_published)
    if not result["current_packet_verified"]:
        evidence = {"result": "publication_observed_current_packet_drift", "publication_observed": True,
                    "current_packet_verified": False, "run_id": run_id,
                    "manifest_sha256": plan["manifest_sha256"], "readback": result,
                    "write_resumption_permitted": False}
        raise PacketDrift("publication observed but current packet drifted: " + "; ".join(result["current_packet_drift"]) +
                          "; read-only reconciliation cannot verify the current packet or resume writes", evidence)
    return {"result": "current_packet_verified_by_read_only_reconciliation", "publication_observed": True,
            "current_packet_verified": True, "run_id": run_id,
            "manifest_sha256": plan["manifest_sha256"], "readback": result, "write_resumption_permitted": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", help="CASE-relative candidate-manifest JSON")
    parser.add_argument("--expected-head")
    parser.add_argument("--expected-branch")
    parser.add_argument("--run-id", required=True, help="fresh lowercase slug; never reuse a mutation journal")
    parser.add_argument("--message", default="PR421: update reviewed author packet")
    parser.add_argument("--apply", action="store_true", help="explicitly execute the already authorized update")
    parser.add_argument("--reconcile", action="store_true", help="read-only inspection of the existing run-id journal")
    parser.add_argument("--resume-existing-commit", metavar="ORIGINAL_RUN_ID",
                        help="verify original durable apply plan and existing commit; --apply permits one ref-only PATCH")
    args = parser.parse_args()
    require(re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,79}", args.run_id) is not None, "invalid run-id")
    case = Path(__file__).resolve().parent.parent
    if args.reconcile:
        require(not args.apply and args.resume_existing_commit is None, "reconciliation cannot apply or resume writes")
        try:
            result = reconcile(GhAPI(), case, args.run_id)
        except PacketDrift as exc:
            print(json.dumps(exc.evidence, indent=2, sort_keys=True))
            print("PacketDrift: " + str(exc), file=sys.stderr)
            return 2
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    require(args.manifest is not None and args.expected_head is not None and args.expected_branch is not None,
            "plan/apply require manifest, expected-head, and expected-branch")
    journal = Journal(case / "private_sources" / "operations" / "runs" / args.run_id)
    try:
        if args.resume_existing_commit is not None:
            result = resume_existing(GhAPI(), case, args.resume_existing_commit, args.manifest,
                                     args.expected_head, args.expected_branch, journal, args.apply)
        else:
            result = run(GhAPI(), case, args.manifest, args.expected_head, args.expected_branch,
                         journal, args.apply, args.message)
        print(json.dumps(result, indent=2, sort_keys=True))
    except Exception as exc:
        journal.append({"event": "stopped", "error_type": type(exc).__name__})
        print(type(exc).__name__ + ": " + str(exc), file=sys.stderr)
        return 2
    finally:
        journal.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""PR421 QUEUE DOI integration and final merge. GET-only plan is the default.

This file does not import another case's helper or touch a checkout/index. See
README.md for the intentionally explicit evidence binding and recovery contract.
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
import urllib.request

REPO = "AlecKriebel/Math"
PR = 421
BRANCH = "research/20001515-explicit-cubulation"
PREFIX = "unsolved_math_prioritization/attempts/20001515/"
QUEUE = "unsolved_math_prioritization/QUEUE.md"
ID = "20001515"
SHA = re.compile(r"[0-9a-f]{40}\Z")
HASH = re.compile(r"[0-9a-f]{64}\Z")
MD5 = re.compile(r"[0-9a-f]{32}\Z")
DOI = re.compile(r"10\.5281/zenodo\.[1-9][0-9]*\Z")
SECRET = re.compile(rb"(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)")


class Stop(Exception):
    pass


class Uncertain(Stop):
    pass


def need(condition, message):
    if not condition:
        raise Stop(message)


def utc():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def git_sha(kind, data):
    return hashlib.sha1(kind.encode() + b" " + str(len(data)).encode() + b"\0" + data).hexdigest()


def path_name(value):
    need(isinstance(value, str) and value and not value.startswith("/") and
         "\\" not in value and "\0" not in value and
         all(part not in ("", ".", "..") for part in value.split("/")), "invalid relative POSIX path")
    return str(PurePosixPath(value))


def read_regular(case, path):
    """Pin regular-file bytes through directory FDs without any symlink."""
    path = path_name(path)
    directory = os.open(case, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    fd = None
    try:
        parts = path.split("/")
        for part in parts[:-1]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory)
            os.close(directory)
            directory = child
        fd = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
        need(stat.S_ISREG(os.fstat(fd).st_mode), "input is not a regular file")
        with os.fdopen(fd, "rb") as source:
            fd = None
            data = source.read()
    except OSError as exc:
        raise Stop("cannot open pinned input without symlinks") from exc
    finally:
        if fd is not None:
            os.close(fd)
        os.close(directory)
    return data


def read_local(case, path, expected_hash):
    """All candidate and original-evidence opens require a caller-pinned hash."""
    need(HASH.fullmatch(expected_hash or "") is not None, "local input needs an explicit SHA256")
    data = read_regular(case, path)
    need(digest(data) == expected_hash, "local input hash differs from caller binding")
    need(SECRET.search(data) is None, "recognizable authentication secret in input")
    return data


def document(case, reference):
    need(isinstance(reference, dict) and set(reference) == {"path", "sha256"}, "invalid document reference")
    try:
        return json.loads(read_local(case, reference["path"], reference["sha256"]))
    except (ValueError, UnicodeError) as exc:
        raise Stop("bound evidence is not JSON") from exc


def pointer(value, selector):
    """RFC6901 pointer only; there is no executable selector or default value."""
    need(isinstance(selector, str) and selector.startswith("/"), "evidence pointer must be explicit")
    for part in selector[1:].split("/"):
        need(re.search(r"~(?![01])", part) is None, "invalid JSON pointer escape")
        part = part.replace("~1", "/").replace("~0", "~")
        try:
            if isinstance(value, list):
                need(re.fullmatch(r"0|[1-9][0-9]*", part) is not None, "invalid JSON array pointer")
                value = value[int(part)]
            else:
                need(isinstance(value, dict), "pointer does not resolve to a JSON object")
                value = value[part]
        except (KeyError, IndexError) as exc:
            raise Stop("evidence pointer does not exist") from exc
    return value


class API:
    """Existing gh auth only. No credential command, environment dump, or raw error output."""
    def call(self, method, route, body=None):
        need(method in ("GET", "POST", "PATCH", "PUT"), "unrecognized API verb")
        target = "graphql" if route == "graphql" else "repos/" + REPO + "/" + route
        command = ["gh", "api", "--method", method, "-H", "Accept: application/vnd.github+json",
                   "-H", "X-GitHub-Api-Version: 2022-11-28", target]
        if body is not None:
            command += ["--input", "-"]
        result = subprocess.run(command, input=None if body is None else encoded(body),
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if result.returncode:
            raise Uncertain("GitHub API response unconfirmed; raw command output suppressed")
        try:
            return json.loads(result.stdout)
        except (ValueError, UnicodeError) as exc:
            raise Uncertain("GitHub API did not return confirmed JSON") from exc

    def production_record(self, record_id):
        url = "https://zenodo.org/api/records/" + str(record_id)
        request = urllib.request.Request(url, headers={"Accept": "application/json"})
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, request, fp, code, message, headers, new_url):
                return None
        try:
            with urllib.request.build_opener(NoRedirect).open(request, timeout=40) as response:
                need(response.geturl() == url, "production record redirected")
                return json.loads(response.read())
        except (OSError, ValueError, UnicodeError) as exc:
            raise Uncertain("production record GET did not confirm JSON") from exc


def get(api, route):
    return api.call("GET", route)


def split_cells(line):
    """Byte spans preserve every byte outside the two selected cell interiors."""
    pipes = []
    for index, char in enumerate(line):
        if char == 124:
            backslashes, at = 0, index - 1
            while at >= 0 and line[at] == 92:
                backslashes += 1
                at -= 1
            if backslashes % 2 == 0:
                pipes.append(index)
    if len(pipes) < 2 or line[:pipes[0]].strip() or line[pipes[-1] + 1:].strip():
        return None
    return [(pipes[i] + 1, pipes[i + 1]) for i in range(len(pipes) - 1)]


def selected_row(content, required=True):
    need(isinstance(content, bytes), "QUEUE must be bytes")
    header, found, offset = None, [], 0
    try:
        for line in content.splitlines(keepends=True):
            spans = split_cells(line.rstrip(b"\r\n"))
            if spans is None and header is not None and line.count(b"|") >= 2 and re.search(rb"\b20001515\b", line):
                raise Stop("malformed selected-ID table line makes QUEUE ambiguous")
            if spans is not None:
                fields = [line[start:end].decode("utf-8").strip() for start, end in spans]
                if "ID / code" in fields and "Status" in fields:
                    need(header is None and len(fields) == len(set(fields)), "ambiguous/duplicate QUEUE header")
                    need(all(key in fields for key in ("ID / code", "Status", "DOI", "Findings")), "QUEUE field missing")
                    header = fields
                elif header is not None:
                    id_index = header.index("ID / code")
                    possible = len(fields) > id_index and fields[id_index].split("/", 1)[0].strip() == ID
                    if possible:
                        need(len(fields) == len(header), "selected QUEUE row has ambiguous cell count")
                        found.append({"fields": dict(zip(header, fields)), "line_span": (offset, offset + len(line)), "spans":
                                      {key: (offset + start, offset + end) for key, (start, end) in zip(header, spans)}})
                    elif re.search(rb"\b20001515\b", line):
                        # A malformed/escaped/shifted selected ID must never become an ignored row.
                        need(len(fields) == len(header) and not any(field.split("/", 1)[0].strip() == ID for field in fields),
                             "ambiguous/shifted selected ID in QUEUE")
            offset += len(line)
    except UnicodeError as exc:
        raise Stop("QUEUE is not valid UTF-8") from exc
    need(header is not None and len(found) == 1, "QUEUE selected ID must occur exactly once")
    if required:
        need(found[0]["fields"]["Status"] == "claimed_solved", "selected Status is not claimed_solved")
    return header, found[0]


def queue_mask(content, all_selected=False):
    _, row = selected_row(content, required=False)
    keys = list(row["spans"]) if all_selected else ["DOI", "Findings"]
    for start, end in sorted((row["spans"][key] for key in keys), reverse=True):
        content = content[:start] + b"<BOUND-CELL>" + content[end:]
    return content


def queue_update(content, doi, findings):
    need(DOI.fullmatch(doi or "") is not None, "DOI is not a production Zenodo DOI")
    header, row = selected_row(content)
    wanted = {"DOI": "[DOI](https://doi.org/" + doi + ")", "Findings": findings}
    for key, value in wanted.items():
        need(isinstance(value, str) and not any(char in value for char in "|\r\n\0"), "invalid target cell text")
    updated = content
    for key, (start, end) in sorted(row["spans"].items(), key=lambda item: item[1][0], reverse=True):
        if key not in wanted:
            continue
        original = content[start:end]
        left = original[:len(original) - len(original.lstrip(b" \t"))]
        right = original[len(original.rstrip(b" \t")):]
        updated = updated[:start] + left + wanted[key].encode() + right + updated[end:]
    need(queue_mask(content) == queue_mask(updated), "QUEUE bytes changed outside selected DOI/Findings")
    new_header, new_row = selected_row(updated)
    need(header == new_header and all(row["fields"][key] == new_row["fields"][key]
         for key in header if key not in wanted), "selected non-target cell changed")
    need(all(new_row["fields"][key] == value for key, value in wanted.items()), "target cells differ")
    return updated


def queue_without_selected(content):
    _, row = selected_row(content, required=False)
    start, end = row["line_span"]
    return content[:start] + content[end:]


def queue_transplant(main_content, accepted_content, doi, findings):
    """Carry the accepted PR row, preserving all other current-main bytes."""
    main_header, main_row = selected_row(main_content, required=False)
    accepted_header, _ = selected_row(accepted_content)
    need(main_header == accepted_header, "main/accepted QUEUE headers differ")
    published = queue_update(accepted_content, doi, findings)
    _, published_row = selected_row(published)
    start, end = published_row["line_span"]
    selected = published[start:end]
    start, end = main_row["line_span"]
    updated = main_content[:start] + selected + main_content[end:]
    need(queue_without_selected(main_content) == queue_without_selected(updated), "unrelated main QUEUE bytes changed")
    _, observed = selected_row(updated)
    need(observed["fields"] == published_row["fields"], "accepted selected row not preserved")
    return updated


def blob(api, sha):
    answer = get(api, "git/blobs/" + sha)
    need(answer.get("sha") == sha and answer.get("encoding") == "base64", "blob identity/encoding mismatch")
    try:
        content = base64.b64decode(answer["content"], validate=False)
    except (KeyError, ValueError, TypeError) as exc:
        raise Stop("invalid blob response") from exc
    need(git_sha("blob", content) == sha, "blob bytes differ from Git object SHA")
    return content


def node_identity(entries):
    ordered = sorted(entries.items(), key=lambda item: (item[0] + ("/" if item[1]["type"] == "tree" else "")).encode())
    raw = b"".join(("40000" if item["type"] == "tree" else item["mode"]).encode() + b" " + name.encode() +
                   b"\0" + bytes.fromhex(item["sha"]) for name, item in ordered)
    return git_sha("tree", raw)


class Merkle:
    """Verify immediate Git tree objects; never trust a truncated recursive list.

    Untouched subtrees stay opaque SHA-bound objects. Only ancestors of QUEUE/
    the selected case and the selected case's own contents are traversed.
    """
    def __init__(self, api):
        self.api, self.cache = api, {git_sha("tree", b""): {}}

    def node(self, sha):
        if sha in self.cache:
            return self.cache[sha]
        response = get(self.api, "git/trees/" + sha)
        need(response.get("sha") == sha and response.get("truncated") is False and isinstance(response.get("tree"), list),
             "nonrecursive tree unavailable/truncated/unbound")
        entries = {}
        for item in response["tree"]:
            name = path_name(item.get("path"))
            need("/" not in name and name not in entries, "nonrecursive tree has nested/duplicate name")
            mode, kind, identity = item.get("mode"), item.get("type"), item.get("sha")
            need(SHA.fullmatch(identity or "") is not None and
                 (mode, kind) in {("040000", "tree"), ("100644", "blob"), ("100755", "blob"),
                                  ("120000", "blob"), ("160000", "commit")}, "invalid nonrecursive entry")
            entries[name] = {"mode": mode, "type": kind, "sha": identity}
        need(node_identity(entries) == sha, "immediate tree bytes do not reproduce Git SHA")
        self.cache[sha] = entries
        return entries

    def at(self, root, path):
        parts = path_name(path).split("/")
        sha = root
        for index, part in enumerate(parts):
            item = self.node(sha).get(part)
            if item is None:
                return None
            if index == len(parts) - 1:
                return dict(item)
            need(item["type"] == "tree", "target path traverses an existing leaf")
            sha = item["sha"]
        raise Stop("empty Merkle lookup")

    def selected_inventory(self, root):
        top = self.at(root, PREFIX.rstrip("/"))
        if top is None:
            return {}, set(), None
        need(top["type"] == "tree", "selected case is not a directory")
        leaves, directories = {}, {PREFIX.rstrip("/")}
        pending = [(PREFIX.rstrip("/"), top["sha"])]
        while pending:
            prefix, sha = pending.pop()
            for name, item in self.node(sha).items():
                path = prefix + "/" + name
                if item["type"] == "tree":
                    directories.add(path)
                    pending.append((path, item["sha"]))
                else:
                    leaves[path] = dict(item)
        return leaves, directories, top

    def restricted_diff(self, old, new, permitted, prefix=""):
        if old == new:
            return
        old_entries, new_entries = self.node(old), self.node(new)
        for name in old_entries.keys() | new_entries.keys():
            before, after = old_entries.get(name), new_entries.get(name)
            if before == after:
                continue
            path = name if not prefix else prefix + "/" + name
            if path in permitted:
                continue
            need(any(allowed.startswith(path + "/") for allowed in permitted), "PR changes an unapproved unrelated subtree/leaf")
            need((before is None or before["type"] == "tree") and (after is None or after["type"] == "tree"),
                 "PR replaces an ancestor with an unrelated leaf")
            self.restricted_diff(git_sha("tree", b"") if before is None else before["sha"],
                                 git_sha("tree", b"") if after is None else after["sha"], permitted, path)

    def overlay(self, root, replacements):
        """Return computed root and changed immediate nodes, child before parent."""
        created = []
        def visit(existing_sha, parts):
            entries = {name: dict(item) for name, item in self.node(existing_sha).items()} if existing_sha is not None else {}
            grouped = {}
            for path, item in parts.items():
                first, separator, remainder = path.partition("/")
                grouped.setdefault(first, {})[remainder if separator else ""] = item
            for name, descendants in grouped.items():
                if "" in descendants:
                    need(len(descendants) == 1, "overlapping overlay replacement")
                    entries[name] = dict(descendants[""])
                else:
                    previous = entries.get(name)
                    need(previous is None or previous["type"] == "tree", "overlay traverses a leaf")
                    child = visit(None if previous is None else previous["sha"], descendants)
                    entries[name] = {"mode": "040000", "type": "tree", "sha": child}
            identity = node_identity(entries)
            if identity != existing_sha:
                created.append({"sha": identity, "entries": entries})
            return identity
        expected = visit(root, replacements)
        return expected, created


def commit_root(api, sha):
    answer = get(api, "git/commits/" + sha)
    need(answer.get("sha") == sha and SHA.fullmatch(answer.get("tree", {}).get("sha", "")) is not None,
         "commit/tree identity mismatch")
    return answer, answer["tree"]["sha"]


def fresh_gate(api, expected_head, expected_main=None, draft=None, closed=False):
    need(SHA.fullmatch(expected_head or "") is not None, "expected head must be explicit")
    if expected_main is not None:
        need(SHA.fullmatch(expected_main or "") is not None, "expected main must be explicit")
    pr = get(api, "pulls/421")
    need(pr.get("number") == PR and pr.get("state") in (("open", "closed") if closed else ("open",)), "PR state invalid")
    head, base = pr.get("head", {}), pr.get("base", {})
    need(head.get("sha") == expected_head and head.get("ref") == BRANCH and
         head.get("repo", {}).get("full_name") == REPO, "PR421 exact head/branch/repository drift")
    need(base.get("ref") == "main" and base.get("repo", {}).get("full_name") == REPO, "PR421 base identity drift")
    need(isinstance(pr.get("draft"), bool), "PR draft value unavailable")
    if draft is not None:
        need(pr["draft"] is draft, "PR draft/readiness state differs from caller binding")
    ref = get(api, "git/ref/heads/" + BRANCH)
    need(ref.get("object", {}).get("sha") == expected_head, "PR head/ref mismatch")
    content = get(api, "contents/" + QUEUE + "?ref=" + expected_head)
    need(content.get("type") == "file" and content.get("encoding") == "base64", "QUEUE contents response invalid")
    try:
        queue = base64.b64decode(content["content"], validate=False)
    except (KeyError, ValueError, TypeError) as exc:
        raise Stop("invalid QUEUE encoding") from exc
    need(git_sha("blob", queue) == content.get("sha"), "QUEUE content identity mismatch")
    header, row = selected_row(queue, required=False)
    # Stop/skip BEFORE any evidence/manifest/candidate open or selected math blob read.
    if row["fields"]["Status"] != "claimed_solved":
        return {"skip": True, "status": row["fields"]["Status"], "head": expected_head}, pr, queue
    # Contents is separately Merkle-bound to this exact commit before opening
    # evidence or any mathematical packet. A valid stale blob is insufficient.
    _, head_root = commit_root(api, expected_head)
    actual_queue_entry = Merkle(api).at(head_root, QUEUE)
    need(actual_queue_entry is not None and actual_queue_entry["type"] == "blob" and
         actual_queue_entry["mode"] in ("100644", "100755") and actual_queue_entry["sha"] == content["sha"],
         "QUEUE Contents response is not bound to exact head Merkle tree")
    main = get(api, "git/ref/heads/main").get("object", {}).get("sha")
    need(SHA.fullmatch(main or "") is not None and (expected_main is None or main == expected_main), "remote main changed")
    return {"skip": False, "checked_at_utc": utc(), "head": expected_head, "main": main,
            "draft": pr["draft"], "queue_sha256": digest(queue), "header": header,
            "selected_row": row["fields"]}, pr, queue


def validate_manifest(value, reviewed_head):
    need(isinstance(value, dict) and set(value) == {"format", "reviewed_head", "entries", "payloads", "findings_path"},
         "unknown/missing package manifest fields")
    need(value["format"] == "pr421-reviewed-package-v1" and value["reviewed_head"] == reviewed_head,
         "package manifest reviewed-head binding mismatch")
    need(isinstance(value["entries"], list) and value["entries"], "package allowlist empty")
    files = {}
    for entry in value["entries"]:
        need(isinstance(entry, dict) and set(entry) == {"remote_path", "sha256", "mode"}, "invalid package entry")
        name = path_name(entry["remote_path"])
        need(name.startswith(PREFIX) and len(name) > len(PREFIX) and name not in files, "package path outside selected case/duplicate")
        need(HASH.fullmatch(entry["sha256"] or "") is not None and entry["mode"] in ("100644", "100755"), "invalid package hash/mode")
        need(not any(part.startswith(("private", ".env")) or part in (".git", "__pycache__") or
                     "credential" in part or "token" in part for part in name.lower().split("/")), "private package path")
        files[name] = entry
    findings = path_name(value["findings_path"])
    need(findings in files and findings.endswith("/README.md") and "/publication/" in findings,
         "Findings must point to an actual accepted publication README")
    need(isinstance(value["payloads"], list) and len(value["payloads"]) == 3, "publication must bind exactly three payloads")
    names, paths = set(), set()
    for payload in value["payloads"]:
        need(isinstance(payload, dict) and set(payload) == {"name", "remote_path", "size", "sha256", "md5"}, "invalid payload entry")
        name = payload["name"]
        need(isinstance(name, str) and path_name(name) == name and "/" not in name and name not in names, "invalid/duplicate payload name")
        need(payload["remote_path"] in files and payload["remote_path"] not in paths and
             payload["sha256"] == files[payload["remote_path"]]["sha256"], "payload not bound to an accepted case file")
        need(type(payload["size"]) is int and payload["size"] > 0 and MD5.fullmatch(payload["md5"] or "") is not None,
             "payload size/MD5 invalid")
        names.add(name)
        paths.add(payload["remote_path"])
    need(sum(name.endswith(".pdf") for name in names) == 1 and sum(name.endswith(".zip") for name in names) == 2,
         "approved payload set must contain one PDF and two ZIPs")
    return files


def load_evidence(case, reference, expected_reviewed_head, api):
    binding = document(case, reference)
    need(isinstance(binding, dict) and set(binding) == {"format", "reviewed_head", "package", "reviews", "publication", "sheet"},
         "unknown/missing evidence binding fields")
    need(binding["format"] == "pr421-original-evidence-bindings-v1" and binding["reviewed_head"] == expected_reviewed_head,
         "evidence reviewed-head mismatch")
    package = binding["package"]
    need(isinstance(package, dict) and set(package) == {"candidate", "update_manifest", "application", "payloads", "findings_path"},
         "native candidate/update-manifest references required")
    original_candidate = document(case, package["candidate"])
    original_update = document(case, package["update_manifest"])
    package_hash = package["candidate"]["sha256"]
    update_hash = package["update_manifest"]["sha256"]
    candidate_source = original_candidate.get("original_source_head")
    need(SHA.fullmatch(candidate_source or "") is not None and
         original_candidate.get("candidate_update_manifest_sha256") == update_hash and
         original_update.get("expected_head") == candidate_source and original_update.get("expected_branch") == BRANCH,
         "native candidate/original update-manifest source/hash/branch binding differs")
    native_files, native_entries = original_candidate.get("candidate_files"), original_update.get("entries")
    need(isinstance(native_files, dict) and native_files and isinstance(native_entries, list) and native_entries,
         "original native positive file inventories missing")
    local_names, entries = set(), []
    for entry in native_entries:
        need(isinstance(entry, dict) and set(entry) == {"local_path", "remote_path", "sha256"}, "invalid native original update entry")
        local = path_name(entry["local_path"])
        need(local not in local_names and native_files.get(local) == entry["sha256"], "candidate/local-to-remote hash join differs")
        local_names.add(local)
        entries.append({"remote_path": entry["remote_path"], "sha256": entry["sha256"], "mode": "100644"})
    need(local_names == set(native_files), "original candidate/update manifest file inventories differ")
    # This in-memory view is not a replacement manifest or a review claim. Its
    # bytes/path pins come directly from BOTH immutable native source documents.
    manifest = {"format": "pr421-reviewed-package-v1", "reviewed_head": expected_reviewed_head,
                "entries": entries, "payloads": package["payloads"], "findings_path": package["findings_path"]}
    files = validate_manifest(manifest, expected_reviewed_head)
    application = document(case, package["application"])
    app_readback = application.get("readback", {})
    need(application.get("current_packet_verified") is True and application.get("manifest_sha256") == update_hash and
         app_readback.get("actual_head") == expected_reviewed_head and app_readback.get("queue_selected_row", {}).get("Status") == "claimed_solved",
         "original actual-head application receipt does not bind verified source package")
    app_files = app_readback.get("files")
    need(isinstance(app_files, list) and len(app_files) == len(native_entries), "original application file inventory differs")
    by_remote, by_local = {}, {}
    for item in app_files:
        need(isinstance(item, dict) and isinstance(item.get("remote_path"), str) and isinstance(item.get("local_path"), str) and
             item["remote_path"] not in by_remote and item["local_path"] not in by_local, "ambiguous application file mapping")
        need(SHA.fullmatch(item.get("blob_sha", "")) is not None and item.get("present_at_actual_head") is True and
             item.get("expected_mode") == item.get("actual_head_mode") == "100644" and
             item.get("sha256") == item.get("actual_head_sha256"), "original application file byte/mode verification differs")
        by_remote[item["remote_path"]], by_local[item["local_path"]] = item, item
    need(set(by_remote) == set(files) and set(by_local) == local_names and
         all(by_remote[item["remote_path"]]["local_path"] == item["local_path"] and
             by_remote[item["remote_path"]]["sha256"] == item["sha256"] for item in native_entries),
         "candidate/update/application path/hash join differs")
    if candidate_source != expected_reviewed_head:
        comparison = get(api, "compare/" + candidate_source + "..." + expected_reviewed_head)
        need(comparison.get("status") == "ahead" and comparison.get("merge_base_commit", {}).get("sha") == candidate_source,
             "actual reviewed head does not descend from original candidate source")
    reviews = binding["reviews"]
    need(isinstance(reviews, list) and len(reviews) == 2, "two full-package original reviews required")
    identities, hashes, actual_head_reviewed = set(), set(), False
    for review in reviews:
        need(isinstance(review, dict) and set(review) == {"document", "reviewer_family", "expected_review_head", "head_pointer", "package_pointer", "verdict_pointer", "accepted_value"},
             "invalid original review binding")
        need(isinstance(review["reviewer_family"], str) and review["reviewer_family"] and review["reviewer_family"] not in identities,
             "independent reviewer families must differ")
        source = document(case, review["document"])
        need(review["document"]["sha256"] not in hashes, "same original review bound twice")
        review_head = review["expected_review_head"]
        need(review_head in (candidate_source, expected_reviewed_head) and pointer(source, review["head_pointer"]) == review_head and
             pointer(source, review["package_pointer"]) == package_hash, "original review head/package mismatch")
        actual_head_reviewed = actual_head_reviewed or review_head == expected_reviewed_head
        accepted = review["accepted_value"]
        need(isinstance(accepted, str) and accepted.lower() in {"accept", "accepted", "pass", "passed", "accepted_full_package", "accept_full_package"},
             "review acceptance must be an explicit inspected original verdict string")
        need(pointer(source, review["verdict_pointer"]) == accepted, "original review verdict differs from inspected binding")
        identities.add(review["reviewer_family"])
        hashes.add(review["document"]["sha256"])
    need(actual_head_reviewed, "one original full-package review must bind the actual updated reviewed head")
    pub = binding["publication"]
    need(isinstance(pub, dict) and set(pub) == {"document", "tool", "record_id_pointer", "doi_pointer", "state_pointer", "environment_pointer", "verified_utc_pointer", "receipt_payloads", "production_constraints"},
         "invalid original publication binding")
    source = document(case, pub["document"])
    tool = pub["tool"]
    need(isinstance(tool, dict) and set(tool) == {"path", "sha256"}, "publication tool source hash reference missing")
    read_local(case, tool["path"], tool["sha256"])
    record_id, doi = pointer(source, pub["record_id_pointer"]), pointer(source, pub["doi_pointer"])
    need(type(record_id) is int and record_id > 0 and DOI.fullmatch(doi or "") is not None and doi == "10.5281/zenodo." + str(record_id),
         "record ID/production DOI mismatch")
    need(pointer(source, pub["state_pointer"]) == "published" and pointer(source, pub["environment_pointer"]) == "production",
         "original pinned production tool receipt does not report published production state")
    verified = pointer(source, pub["verified_utc_pointer"])
    need(isinstance(verified, str), "original production tool verification time missing")
    try:
        observed_time = dt.datetime.fromisoformat(verified.replace("Z", "+00:00"))
    except ValueError as exc:
        raise Stop("invalid original publication verification timestamp") from exc
    need(observed_time.tzinfo is not None and observed_time.utcoffset() == dt.timedelta(0), "publication verification time must be UTC")
    receipt_payloads = pub["receipt_payloads"]
    need(isinstance(receipt_payloads, list) and len(receipt_payloads) == 3, "original publication requires three pinned SHA256 payload selectors")
    manifest_payloads = {item["name"]: item for item in manifest["payloads"]}
    observed_names, observed_selectors = set(), set()
    for item in receipt_payloads:
        need(isinstance(item, dict) and {"name", "sha256_pointer"} <= set(item) <= {"name", "sha256_pointer", "size_pointer", "md5_pointer"},
             "invalid original payload selector binding")
        name, selector = item["name"], item["sha256_pointer"]
        need(name in manifest_payloads and name not in observed_names and selector not in observed_selectors,
             "duplicate/unknown original payload selector")
        expected = manifest_payloads[name]
        need(pointer(source, selector) == expected["sha256"], "original publication payload SHA256 differs")
        if "size_pointer" in item:
            need(pointer(source, item["size_pointer"]) == expected["size"], "original payload size differs")
        if "md5_pointer" in item:
            checksum = pointer(source, item["md5_pointer"])
            if isinstance(checksum, str) and checksum.startswith("md5:"):
                checksum = checksum[4:]
            need(checksum == expected["md5"], "original payload MD5 differs")
        observed_names.add(name)
        observed_selectors.add(selector)
    record = api.production_record(record_id)
    need(record.get("id", record.get("recid")) == record_id and record.get("doi") == doi, "production record identity/DOI mismatch")
    record_files = record.get("files")
    need(isinstance(record_files, list), "production record files missing")
    by_name = {}
    for item in record_files:
        name = item.get("key", item.get("filename"))
        need(isinstance(name, str) and name not in by_name, "duplicate/invalid production file name")
        by_name[name] = item
    need(set(by_name) == {item["name"] for item in manifest["payloads"]}, "production record payload name set differs")
    for payload in manifest["payloads"]:
        observed = by_name[payload["name"]]
        checksum = observed.get("checksum", "")
        need(isinstance(checksum, str), "production checksum missing")
        if checksum.startswith("md5:"):
            checksum = checksum[4:]
        need(checksum == payload["md5"] and observed.get("size", observed.get("filesize")) == payload["size"],
             "production payload MD5/size mismatch")
    constraints = pub["production_constraints"]
    need(isinstance(constraints, list) and constraints, "approved production metadata constraints missing")
    seen = set()
    for constraint in constraints:
        need(isinstance(constraint, dict) and set(constraint) == {"pointer", "value"} and
             constraint["pointer"].startswith("/metadata/") and constraint["pointer"] not in seen,
             "invalid/duplicate approved production metadata constraint")
        need(pointer(record, constraint["pointer"]) == constraint["value"], "approved production metadata differs")
        seen.add(constraint["pointer"])
    need("/metadata/title" in seen and any(item.startswith("/metadata/creators") for item in seen),
         "production title and creator constraints required")
    sheet = binding["sheet"]
    need(isinstance(sheet, dict) and set(sheet) == {"document", "spreadsheet_id_pointer", "range_pointer", "values_pointer", "id_column", "doi_column"},
         "invalid original Sheet readback binding")
    source = document(case, sheet["document"])
    spreadsheet, range_name = pointer(source, sheet["spreadsheet_id_pointer"]), pointer(source, sheet["range_pointer"])
    need(isinstance(spreadsheet, str) and spreadsheet and isinstance(range_name, str) and range_name,
         "original Sheet readback identity/range missing")
    values = pointer(source, sheet["values_pointer"])
    need(isinstance(values, list) and len(values) == 1 and isinstance(values[0], list), "Sheet verified range must identify one read-back row")
    columns = (sheet["id_column"], sheet["doi_column"])
    need(all(type(column) is int and 0 <= column < len(values[0]) for column in columns) and columns[0] != columns[1], "Sheet column bindings invalid")
    sheet_id = values[0][columns[0]]
    need(isinstance(sheet_id, str) and sheet_id.split("/", 1)[0].strip() == ID and
         values[0][columns[1]] in (doi, "https://doi.org/" + doi), "actual Sheet readback selected ID/DOI differs")
    return {"manifest": manifest, "files": files, "package_sha256": package_hash, "update_manifest_sha256": update_hash,
            "application_sha256": package["application"]["sha256"],
            "application_blob_shas": {name: item["blob_sha"] for name, item in by_remote.items()},
            "original_candidate_source_head": candidate_source,
            "bindings_sha256": reference["sha256"], "doi": doi, "record_id": record_id,
            "review_hashes": sorted(hashes), "publication_sha256": pub["document"]["sha256"], "publication_tool_sha256": tool["sha256"],
            "sheet_sha256": sheet["document"]["sha256"], "sheet_range": range_name,
            "production_approved_fields_sha256": digest(encoded({"id": record_id, "doi": doi,
                "constraints": constraints, "payloads": [{"name": item["name"], "size": item["size"], "md5": item["md5"]}
                for item in manifest["payloads"]]}))}


def accepted_files(api, leaves, evidence):
    files, manifest = evidence["files"], evidence["manifest"]
    need({name for name in leaves if name.startswith(PREFIX)} == set(files), "selected case tree differs from complete reviewed package allowlist")
    bindings = {}
    payloads = {item["remote_path"]: item for item in manifest["payloads"]}
    for name, entry in files.items():
        leaf = leaves[name]
        need(leaf["type"] == "blob" and leaf["mode"] == entry["mode"], "accepted file type/mode drift")
        need(leaf["sha"] == evidence["application_blob_shas"][name], "accepted Git blob differs from original actual-head application receipt")
        content = blob(api, leaf["sha"])
        need(digest(content) == entry["sha256"], "accepted file SHA256 drift")
        if name in payloads:
            payload = payloads[name]
            need(len(content) == payload["size"] and hashlib.md5(content).hexdigest() == payload["md5"],
                 "immutable publication payload size/MD5 drift")
        bindings[name] = dict(leaf)
    return bindings


def prospective(api, head, main, head_queue, evidence):
    """Only selected case blobs and administrative QUEUE blobs are opened."""
    view = Merkle(api)
    _, source_root = commit_root(api, head)
    _, main_root = commit_root(api, main)
    comparison = get(api, "compare/" + main + "..." + head)
    base = comparison.get("merge_base_commit", {}).get("sha")
    need(SHA.fullmatch(base or "") is not None, "merge base unavailable")
    _, base_root = commit_root(api, base)
    view.restricted_diff(base_root, source_root, {QUEUE, PREFIX.rstrip("/")})
    source_queue_entry = view.at(source_root, QUEUE)
    need(source_queue_entry is not None and source_queue_entry["type"] == "blob" and
         source_queue_entry["sha"] == git_sha("blob", head_queue), "head QUEUE contents/commit Merkle binding mismatch")
    head_leaves, _, selected_top = view.selected_inventory(source_root)
    accepted = accepted_files(api, head_leaves, evidence)
    main_top, base_top = view.at(main_root, PREFIX.rstrip("/")), view.at(base_root, PREFIX.rstrip("/"))
    need(main_top == base_top or main_top == selected_top, "main has conflicting selected-case subtree; cannot preserve both")
    main_queue_entry = view.at(main_root, QUEUE)
    need(main_queue_entry is not None and main_queue_entry["type"] == "blob" and main_queue_entry["mode"] in ("100644", "100755"),
         "main QUEUE is not a regular file")
    main_queue = blob(api, main_queue_entry["sha"])
    base_queue_entry = view.at(base_root, QUEUE)
    if base_queue_entry is not None and base_queue_entry["type"] == "blob":
        base_queue = blob(api, base_queue_entry["sha"])
        need(queue_without_selected(head_queue) == queue_without_selected(base_queue),
             "PR QUEUE changed unrelated rows/header bytes")
    else:
        raise Stop("QUEUE absent at merge base; preserving row history cannot be established")
    findings = "[Publication README](" + evidence["manifest"]["findings_path"][len("unsolved_math_prioritization/"):] + ")"
    updated = queue_transplant(main_queue, head_queue, evidence["doi"], findings)
    queue_entry = {"type": "blob", "mode": main_queue_entry["mode"], "sha": git_sha("blob", updated)}
    replacements = {PREFIX.rstrip("/"): selected_top, QUEUE: queue_entry}
    expected_root, changed_nodes = view.overlay(main_root, replacements)
    return {"source_tree": source_root, "main_tree": main_root, "merge_base": base,
            "replacements": replacements, "changed_nodes": changed_nodes, "expected_tree": expected_root,
            "accepted_leaves": accepted, "queue_before_sha256": digest(main_queue), "queue_after_sha256": digest(updated),
            "main_queue_content_b64": base64.b64encode(main_queue).decode(),
            "accepted_queue_content_b64": base64.b64encode(head_queue).decode(),
            "queue_content_b64": base64.b64encode(updated).decode(), "doi": evidence["doi"], "findings": findings}


def new_commit(tree_sha, head, main, date):
    need(head != main, "source/main are identical; no integration merge parent")
    message = "PR421: bind published DOI and preserve current main\n"
    epoch = int(dt.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc).timestamp())
    identity = "Alec Kriebel <me@aleckriebel.com> " + str(epoch) + " +0000"
    raw = ("tree " + tree_sha + "\nparent " + head + "\nparent " + main + "\nauthor " + identity +
           "\ncommitter " + identity + "\n\n" + message).encode()
    person = {"name": "Alec Kriebel", "email": "me@aleckriebel.com", "date": date}
    return git_sha("commit", raw), {"tree": tree_sha, "parents": [head, main], "message": message,
                                    "author": person, "committer": person}


def verify_inventory(api, sha, expected):
    need(sha == expected["expected_tree"], "root tree differs from exact Merkle preservation overlay")
    view = Merkle(api)
    for node in expected["changed_nodes"]:
        need(view.node(node["sha"]) == node["entries"], "changed immediate tree differs from preservation plan")
    view.node(sha)


def verify_created(api, sha, spec, expected):
    answer = get(api, "git/commits/" + sha)
    returned_message = answer.get("message")
    message_matches = returned_message == spec["message"] or (
        spec["message"].endswith("\n") and returned_message == spec["message"][:-1])
    need(answer.get("sha") == sha and answer.get("tree", {}).get("sha") == spec["tree"] and
         [item.get("sha") for item in answer.get("parents", [])] == spec["parents"] and message_matches,
         "created integration commit metadata differs")
    need(all(all(answer.get(field, {}).get(key) == value for key, value in spec[field].items()) for field in ("author", "committer")),
         "created integration commit attribution differs")
    verify_inventory(api, spec["tree"], expected)


class Journal:
    def __init__(self, directory):
        directory.mkdir(mode=0o700, parents=True, exist_ok=False)
        self.directory = directory
        self.fd = os.open(directory / "journal.jsonl", os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        self.sync(directory.parent)
        self.sync(directory)

    @staticmethod
    def sync(directory):
        fd = os.open(directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)

    def add(self, event):
        data = encoded({"at_utc": utc(), **event}) + b"\n"
        offset = 0
        while offset < len(data):
            count = os.write(self.fd, data[offset:])
            need(count > 0, "journal did not advance")
            offset += count
        os.fsync(self.fd)

    def claim(self, action, head):
        root = self.directory.parent / "claims"
        root.mkdir(mode=0o700, exist_ok=True)
        self.sync(self.directory.parent)
        try:
            fd = os.open(root / (action + "-" + head + ".json"), os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        except FileExistsError as exc:
            raise Stop("durable action/head claim already exists; read-only reconcile, never blind retry") from exc
        with os.fdopen(fd, "wb") as stream:
            stream.write(encoded({"run_id": self.directory.name, "action": action, "head": head}) + b"\n")
            stream.flush()
            os.fsync(stream.fileno())
        self.sync(root)

    def finish(self, value):
        fd = os.open(self.directory / "receipt.json", os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        with os.fdopen(fd, "wb") as stream:
            stream.write(json.dumps(value, indent=2, sort_keys=True).encode() + b"\n")
            stream.flush()
            os.fsync(stream.fileno())
        self.sync(self.directory)
        return value

    def close(self):
        os.close(self.fd)


def mutation(api, journal, method, route, body, kind, verify):
    journal.add({"event": "intent", "kind": kind, "method": method, "route": route, "body_sha256": digest(encoded(body))})
    try:
        answer = api.call(method, route, body)
        verify(answer)
    except Exception as exc:
        journal.add({"event": "response_unconfirmed", "kind": kind})
        raise Uncertain(kind + " response unconfirmed; reconciliation is GET-only, no mutation continuation") from exc
    journal.add({"event": "response_confirmed", "kind": kind,
                 **({"observed_sha": answer.get("sha"), "merged": answer.get("merged")} if kind == "merge" else {})})
    return answer


def object_write(api, journal, route, body, kind, sha, verify):
    journal.add({"event": "intent", "kind": kind, "method": "POST", "route": route, "expected_sha": sha,
                 "body_sha256": digest(encoded(body))})
    try:
        answer = api.call("POST", route, body)
        need(answer.get("sha") == sha, "content-addressed object response identity differs")
        verify()
    except Exception:
        # GET may establish an existing exact object; POST is never repeated.
        try:
            verify()
        except Exception as exc:
            journal.add({"event": "uncertain", "kind": kind, "expected_sha": sha})
            raise Uncertain("object outcome uncertain; no write continuation") from exc
        journal.add({"event": "object_verified_after_response_loss", "kind": kind, "sha": sha})
        return
    journal.add({"event": "object_verified", "kind": kind, "sha": sha})


def selected_at_head(api, head, evidence, doi, findings, closed=False):
    gate, pr, queue = fresh_gate(api, head, draft=None, closed=closed)
    need(not gate["skip"], "current selected status drifted")
    _, root = commit_root(api, head)
    leaves, _, _ = Merkle(api).selected_inventory(root)
    accepted_files(api, leaves, evidence)
    _, row = selected_row(queue)
    need(row["fields"]["DOI"] == "[DOI](https://doi.org/" + doi + ")" and row["fields"]["Findings"] == findings,
         "actual selected DOI/Findings drift")
    return gate, pr


def summary(evidence):
    return {key: evidence[key] for key in ("package_sha256", "update_manifest_sha256", "application_sha256", "original_candidate_source_head", "bindings_sha256", "doi", "record_id", "review_hashes",
                                         "publication_sha256", "publication_tool_sha256", "sheet_sha256", "sheet_range", "production_approved_fields_sha256")}


def historical_metadata(api):
    """GET-only factual observations, even after scope drift; no packet read."""
    try:
        pr = get(api, "pulls/421")
        need(pr.get("number") == PR and pr.get("head", {}).get("repo", {}).get("full_name") == REPO,
             "historical PR identity differs")
        head, merge_sha = pr.get("head", {}).get("sha"), pr.get("merge_commit_sha")
        return {"observation_available": True, "at_utc": utc(), "pr": PR,
                "actual_head": head if isinstance(head, str) and SHA.fullmatch(head) else None,
                "state": pr.get("state") if pr.get("state") in ("open", "closed") else None,
                "draft": pr.get("draft") if isinstance(pr.get("draft"), bool) else None,
                "merged": pr.get("merged") if isinstance(pr.get("merged"), bool) else None,
                "merge_commit": merge_sha if isinstance(merge_sha, str) and SHA.fullmatch(merge_sha) else None,
                "merged_at": pr.get("merged_at") if isinstance(pr.get("merged_at"), str) and
                    re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z", pr["merged_at"]) else None}
    except Exception:
        return {"observation_available": False, "at_utc": utc(), "pr": PR}


def apply_queue(api, journal, head, main, evidence, proposal, plan):
    gate, _, _ = fresh_gate(api, head, main, draft=True)
    need(not gate["skip"], "selected status drifted before object writes")
    journal.claim("queue", head)
    content = base64.b64decode(proposal["queue_content_b64"])
    queue_sha = proposal["replacements"][QUEUE]["sha"]
    object_write(api, journal, "git/blobs", {"content": base64.b64encode(content).decode(), "encoding": "base64"}, "queue_blob", queue_sha,
                 lambda: need(blob(api, queue_sha) == content, "created QUEUE bytes differ"))
    # Each POST contains exactly one complete immediate directory. Untouched
    # child SHA IDs, empty directories, modes, symlinks and submodules are retained.
    for node in proposal["changed_nodes"]:
        entries = [{"path": name, **item} for name, item in node["entries"].items()]
        object_write(api, journal, "git/trees", {"tree": entries}, "preservation_tree", node["sha"],
                     lambda node=node: need(Merkle(api).node(node["sha"]) == node["entries"], "created immediate tree differs"))
    created, spec = plan["integrated_head"], plan["commit_spec"]
    object_write(api, journal, "git/commits", spec, "integration_commit", created,
                 lambda: verify_created(api, created, spec, proposal))
    verify_created(api, created, spec, proposal)
    gate, _, _ = fresh_gate(api, head, main, draft=True)
    need(not gate["skip"], "selected status drifted before ref update")
    journal.add({"event": "ref_binding", "old_head": head, "new_head": created, "force": False})
    try:
        mutation(api, journal, "PATCH", "git/refs/heads/" + BRANCH, {"sha": created, "force": False}, "ref",
                 lambda answer: need(answer.get("object", {}).get("sha") == created, "ref response identity differs"))
    except Uncertain:
        # No writes follow response loss, even when historical publication is
        # observed. Reconciliation can be repeated with GET, never with PATCH.
        try:
            gate, _ = selected_at_head(api, created, evidence, proposal["doi"], proposal["findings"])
            observed = {"result": "queue_observed_after_response_loss", "integrated_head": created, "readback": gate}
            journal.finish({**plan, **observed, "mutation_resume_permitted": False})
        except Exception:
            journal.add({"event": "uncertain", "kind": "ref", "new_head": created})
            journal.finish({**plan, "result": "queue_response_unconfirmed", "historical_metadata": historical_metadata(api),
                            "current_packet_verified": False, "mutation_resume_permitted": False})
        raise
    try:
        gate, pr = selected_at_head(api, created, evidence, proposal["doi"], proposal["findings"])
        need(pr["draft"] is True and gate["main"] == main, "post-integration readiness/main drift")
        verify_created(api, created, spec, proposal)
    except Exception as exc:
        journal.finish({**plan, "result": "queue_observed_readback_drift", "historical_ref_response_head": created,
                        "current_packet_verified": False, "error_type": type(exc).__name__})
        raise
    return journal.finish({**plan, "result": "queue_integrated_verified", "readback": gate,
                           "accepted_package_unchanged": True, "remote_main_preserved": True})


def verify_final_merge(api, head, evidence, proposal, merge_sha=None):
    # Closed/non-draft is expected here; no pending mutation is performed.
    gate, pr, _ = fresh_gate(api, head, draft=False, closed=True)
    need(not gate["skip"] and pr.get("state") == "closed" and pr.get("merged") is True and isinstance(pr.get("merged_at"), str),
         "PR421 has not been confirmed merged")
    actual = pr.get("merge_commit_sha")
    need(SHA.fullmatch(actual or "") is not None and (merge_sha is None or actual == merge_sha), "merged commit receipt differs")
    merged, merged_root = commit_root(api, actual)
    parents = [item.get("sha") for item in merged.get("parents", [])]
    need(len(parents) == 2 and parents[1] == head and SHA.fullmatch(parents[0] or "") is not None, "merge commit parents do not include exact accepted PR head")
    _, baseline_root = commit_root(api, parents[0])
    view = Merkle(api)
    baseline_queue = view.at(baseline_root, QUEUE)
    need(baseline_queue is not None and baseline_queue["type"] == "blob" and baseline_queue["mode"] in ("100644", "100755"),
         "actual main parent QUEUE missing/irregular")
    before_queue = blob(api, baseline_queue["sha"])
    _, prior_row = selected_row(base64.b64decode(proposal["main_queue_content_b64"]), required=False)
    _, actual_parent_row = selected_row(before_queue, required=False)
    _, accepted_row = selected_row(base64.b64decode(proposal["accepted_queue_content_b64"]))
    need(actual_parent_row["fields"] in (prior_row["fields"], accepted_row["fields"]),
         "actual main parent has concurrent selected-row changes; cannot certify preservation")
    # A concurrent main advance is checked against the ACTUAL first parent,
    # rather than making a stale-main preservation claim.
    accepted_queue = base64.b64decode(proposal["accepted_queue_content_b64"])
    target_queue = queue_transplant(before_queue, accepted_queue, proposal["doi"], proposal["findings"])
    replacements = {PREFIX.rstrip("/"): proposal["replacements"][PREFIX.rstrip("/")],
                    QUEUE: {"mode": baseline_queue["mode"], "type": "blob", "sha": git_sha("blob", target_queue)}}
    expected_root, _ = view.overlay(baseline_root, replacements)
    need(merged_root == expected_root, "merge root does not preserve actual main parent plus exact allowed overlay")
    merged_queue_entry = view.at(merged_root, QUEUE)
    merged_queue = blob(api, merged_queue_entry["sha"])
    _, merged_row = selected_row(merged_queue, required=False)
    need(merged_row["fields"]["Status"] == "claimed_solved", "merged selected Status drift; no case read permitted")
    merged_leaves, _, _ = view.selected_inventory(merged_root)
    accepted_files(api, merged_leaves, evidence)
    main = get(api, "git/ref/heads/main").get("object", {}).get("sha")
    need(SHA.fullmatch(main or "") is not None, "actual main ref invalid")
    if main != actual:
        comparison = get(api, "compare/" + actual + "..." + main)
        need(comparison.get("status") == "ahead" and comparison.get("merge_base_commit", {}).get("sha") == actual,
             "resulting main does not descend from verified merge")
    _, current_root = commit_root(api, main)
    current_queue_entry = view.at(current_root, QUEUE)
    need(current_queue_entry is not None and current_queue_entry["type"] == "blob", "resulting main QUEUE missing")
    current_queue = blob(api, current_queue_entry["sha"])
    _, row = selected_row(current_queue, required=False)
    need(row["fields"]["Status"] == "claimed_solved", "current-main Status drift; no current-main case read permitted")
    current_leaves, _, _ = view.selected_inventory(current_root)
    accepted_files(api, current_leaves, evidence)
    need(row["fields"]["DOI"] == "[DOI](https://doi.org/" + evidence["doi"] + ")" and row["fields"]["Findings"] == proposal["findings"],
         "resulting main selected DOI/Findings drift")
    return {"merged": True, "merged_at": pr["merged_at"], "merge_commit": actual, "actual_main": main,
            "actual_main_parent": parents[0], "actual_pr_head": head, "merge_tree": merged_root,
            "actual_parent_queue_sha256": digest(before_queue), "merged_queue_sha256": digest(target_queue),
            "actual_main_queue_sha256": digest(current_queue), "selected_row": row["fields"],
            "immutable_payloads_verified": evidence["manifest"]["payloads"], "unrelated_main_leaves_preserved": True}


def apply_merge(api, journal, head, main, evidence, proposal, plan, expected_draft):
    gate, pr, _ = fresh_gate(api, head, main, draft=expected_draft)
    need(not gate["skip"], "selected status drifted before readiness/merge")
    if expected_draft:
        node_id = pr.get("node_id")
        need(isinstance(node_id, str) and node_id, "PR GraphQL node ID unavailable")
        journal.claim("ready", head)
        body = {"query": "mutation($id:ID!){markPullRequestReadyForReview(input:{pullRequestId:$id}){pullRequest{id isDraft headRefOid}}}",
                "variables": {"id": node_id}}
        gate, current_pr, _ = fresh_gate(api, head, main, draft=True)
        need(not gate["skip"] and current_pr.get("node_id") == node_id, "head/main/readiness drift before ready mutation")
        try:
            mutation(api, journal, "POST", "graphql", body, "ready",
                     lambda answer: need(not answer.get("errors") and
                     answer.get("data", {}).get("markPullRequestReadyForReview", {}).get("pullRequest") == {"id": node_id, "isDraft": False, "headRefOid": head},
                     "ready transition response did not confirm exact PR"))
        except Uncertain:
            try:
                gate, _, _ = fresh_gate(api, head, main, draft=False)
                need(not gate["skip"], "selected status drifted after ready response loss")
                journal.finish({**plan, "result": "ready_observed_after_response_loss", "readback": gate,
                                "mutation_resume_permitted": False})
            except Exception:
                journal.add({"event": "uncertain", "kind": "ready"})
                journal.finish({**plan, "result": "ready_response_unconfirmed", "historical_metadata": historical_metadata(api),
                                "current_packet_verified": False, "mutation_resume_permitted": False})
            raise
    try:
        gate, pr, _ = fresh_gate(api, head, main, draft=False)
        need(not gate["skip"] and pr.get("mergeable") is True and pr.get("mergeable_state") == "clean",
             "PR must be non-draft and GitHub-mergeable clean; no bypass/force path")
    except Exception as exc:
        if expected_draft:
            journal.finish({**plan, "result": "ready_observed_readback_drift", "historical_metadata": historical_metadata(api),
                            "current_packet_verified": False, "error_type": type(exc).__name__})
        raise
    journal.claim("merge", head)
    body = {"sha": head, "merge_method": "merge", "commit_title": "Merge PR421: published solution for 20001515"}
    try:
        answer = mutation(api, journal, "PUT", "pulls/421/merge", body, "merge",
                          lambda value: need(value.get("merged") is True and SHA.fullmatch(value.get("sha", "")) is not None,
                                             "merge response did not confirm a merged commit"))
    except Uncertain:
        try:
            observed = verify_final_merge(api, head, evidence, proposal)
            journal.finish({**plan, "result": "merged_verified_after_response_loss", "readback": observed,
                            "mutation_resume_permitted": False})
        except Exception:
            journal.add({"event": "uncertain", "kind": "merge"})
            journal.finish({**plan, "result": "merge_response_unconfirmed_or_drift", "historical_metadata": historical_metadata(api),
                            "current_packet_verified": False, "mutation_resume_permitted": False})
        raise
    try:
        observed = verify_final_merge(api, head, evidence, proposal, answer["sha"])
    except Exception as exc:
        journal.finish({**plan, "result": "merge_observed_readback_drift", "historical_merge_response":
                        {"merged": True, "sha": answer["sha"]}, "current_packet_verified": False,
                        "error_type": type(exc).__name__})
        raise
    return journal.finish({**plan, "result": "merged_verified", "readback": observed})


def run(api, case, phase, head, main, reviewed_head, binding_ref, journal, apply=False, expected_draft=True, integration_ref=None):
    need(phase in ("queue", "merge"), "phase invalid")
    gate, _, queue = fresh_gate(api, head, main, draft=True if phase == "queue" else expected_draft)
    if gate["skip"]:
        return journal.finish({"format": "pr421-finalization-v1", "mode": "apply" if apply else "plan", "phase": phase,
                               "result": "skipped_status", "gate": gate, "candidate_or_evidence_read": False})
    # This is the first local evidence/manifest read and first selected-case blob read.
    evidence = load_evidence(case, binding_ref, reviewed_head, api)
    if phase == "queue":
        need(head == reviewed_head, "QUEUE integration source must be the exact reviewed head")
    else:
        need(integration_ref is not None, "merge requires original verified DOI integration receipt")
        receipt = document(case, integration_ref)
        need(receipt.get("format") == "pr421-finalization-v1" and receipt.get("phase") == "queue" and
             receipt.get("result") in ("queue_integrated_verified", "queue_observed_after_response_loss", "queue_reconciled_verified") and
             receipt.get("integrated_head") == head and receipt.get("reviewed_head") == reviewed_head and
             receipt.get("evidence") == summary(evidence), "integration receipt binding differs")
    proposal = prospective(api, head, main, queue, evidence)
    plan = {"format": "pr421-finalization-v1", "at_utc": utc(), "phase": phase, "mode": "apply" if apply else "plan",
            "repo": REPO, "pr": PR, "branch": BRANCH, "expected_head": head, "expected_main": main,
            "reviewed_head": reviewed_head, "expected_draft": expected_draft, "evidence": summary(evidence), "gate": gate,
            "expected_tree": proposal["expected_tree"], "source_tree": proposal["source_tree"], "main_tree": proposal["main_tree"],
            "merge_base": proposal["merge_base"], "queue_before_sha256": proposal["queue_before_sha256"],
            "queue_after_sha256": proposal["queue_after_sha256"], "doi": proposal["doi"], "findings": proposal["findings"],
            "accepted_package_files": evidence["manifest"]["entries"], "immutable_payloads": evidence["manifest"]["payloads"],
            "preservation_inventory_sha256": digest(encoded({"replacements": proposal["replacements"], "nodes": proposal["changed_nodes"]}))}
    if phase == "queue":
        plan["integrated_head"], plan["commit_spec"] = new_commit(proposal["expected_tree"], head, main, utc())
    else:
        need(proposal["expected_tree"] == proposal["source_tree"], "main advanced or PR content requires new integration; do not merge")
        need(main == receipt["expected_main"], "main changed since DOI integration; a new reviewed integration is required")
        plan["integration_receipt_sha256"] = integration_ref["sha256"]
    journal.add({"event": "validated_plan", "plan": plan, "proposal": proposal,
                 "manifest": evidence["manifest"], "evidence_summary": summary(evidence)})
    if not apply:
        return journal.finish({**plan, "result": "plan_verified_no_remote_writes"})
    if phase == "queue":
        return apply_queue(api, journal, head, main, evidence, proposal, plan)
    return apply_merge(api, journal, head, main, evidence, proposal, plan, expected_draft)


def reconcile(api, case, run_id):
    """Only GET; never resume an object/ref/ready/merge write."""
    run_path = "private_sources/merge_preparation/runs/" + run_id + "/journal.jsonl"
    # Journal is administrative metadata, not candidate bytes. The first candidate
    # blob read in recovery is still preceded by fresh header-derived Status.
    try:
        data = read_regular(case, run_path)
        need(data and data.endswith(b"\n"), "incomplete journal tail; no write resumption")
        events = [json.loads(line) for line in data.splitlines()]
        need(all(isinstance(item, dict) for item in events), "invalid journal event")
    except (OSError, ValueError, UnicodeError) as exc:
        raise Stop("incomplete journal; no mutation resumption") from exc
    records = [item for item in events if item.get("event") == "validated_plan"]
    need(len(records) == 1 and records[0]["plan"].get("mode") == "apply", "one apply plan required for reconciliation")
    record, plan = records[0], records[0]["plan"]
    need(plan.get("repo") == REPO and plan.get("pr") == PR and plan.get("branch") == BRANCH, "journal identity mismatch")
    proposal = record["proposal"]
    need(proposal["expected_tree"] == plan["expected_tree"] and
         all(node_identity(node["entries"]) == node["sha"] for node in proposal["changed_nodes"]) and
         digest(encoded({"replacements": proposal["replacements"], "nodes": proposal["changed_nodes"]})) == plan["preservation_inventory_sha256"],
         "journal preservation inventory binding differs")
    evidence = {"manifest": record["manifest"], "files": validate_manifest(record["manifest"], plan["reviewed_head"]),
                "application_blob_shas": {name: item["sha"] for name, item in proposal["accepted_leaves"].items()},
                **record["evidence_summary"]}
    intents = [item for item in events if item.get("event") == "intent"]
    counts = {kind: sum(item.get("kind") == kind for item in intents) for kind in ("ref", "ready", "merge")}
    need(all(count <= 1 for count in counts.values()), "repeated mutation intent in journal")
    if plan["phase"] == "queue":
        if not counts["ref"]:
            return {"result": "no_ref_intent", "mutation_resume_permitted": False}
        created = plan["integrated_head"]
        try:
            gate, _, _ = fresh_gate(api, created, draft=None)
        except Exception:
            return {**plan, "result": "queue_response_unconfirmed_or_drift", "historical_metadata": historical_metadata(api),
                    "current_packet_verified": False, "mutation_resume_permitted": False}
        if gate["skip"]:
            return {"result": "skipped_status", "gate": gate, "mutation_resume_permitted": False}
        verify_created(api, created, plan["commit_spec"], proposal)
        gate, _ = selected_at_head(api, created, evidence, proposal["doi"], proposal["findings"])
        return {**plan, "result": "queue_reconciled_verified", "readback": gate, "mutation_resume_permitted": False}
    if counts["merge"]:
        try:
            actual = verify_final_merge(api, plan["expected_head"], evidence, proposal)
            return {**plan, "result": "merged_reconciled_verified", "readback": actual, "mutation_resume_permitted": False}
        except Exception:
            return {**plan, "result": "merge_response_unconfirmed_or_drift", "historical_metadata": historical_metadata(api),
                    "current_packet_verified": False, "mutation_resume_permitted": False}
    if counts["ready"]:
        try:
            gate, _, _ = fresh_gate(api, plan["expected_head"], draft=False)
            return {"result": "ready_observed" if not gate["skip"] else "skipped_status", "gate": gate, "mutation_resume_permitted": False}
        except Exception:
            return {"result": "ready_response_unconfirmed_or_drift", "historical_metadata": historical_metadata(api),
                    "current_packet_verified": False, "mutation_resume_permitted": False}
    return {"result": "no_ready_or_merge_intent", "mutation_resume_permitted": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=("queue", "merge"))
    parser.add_argument("--expected-head")
    parser.add_argument("--expected-main")
    parser.add_argument("--reviewed-head")
    parser.add_argument("--bindings")
    parser.add_argument("--bindings-sha256")
    parser.add_argument("--integration-receipt")
    parser.add_argument("--integration-receipt-sha256")
    parser.add_argument("--expected-draft", choices=("true", "false"), default="true")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--reconcile", action="store_true")
    args = parser.parse_args()
    need(re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,79}", args.run_id) is not None, "invalid run-id")
    case = Path(__file__).resolve().parent.parent
    if args.reconcile:
        need(not args.apply, "reconciliation cannot apply")
        print(json.dumps(reconcile(API(), case, args.run_id), indent=2, sort_keys=True))
        return 0
    need(all((args.phase, args.expected_head, args.expected_main, args.reviewed_head, args.bindings, args.bindings_sha256)), "explicit plan/apply bindings missing")
    reference = {"path": args.bindings, "sha256": args.bindings_sha256}
    integration = None if args.integration_receipt is None else {"path": args.integration_receipt, "sha256": args.integration_receipt_sha256}
    journal = Journal(case / "private_sources" / "merge_preparation" / "runs" / args.run_id)
    try:
        result = run(API(), case, args.phase, args.expected_head, args.expected_main, args.reviewed_head, reference,
                     journal, args.apply, args.expected_draft == "true", integration)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except Exception as exc:
        journal.add({"event": "stopped", "error_type": type(exc).__name__})
        print(type(exc).__name__ + ": " + str(exc), file=sys.stderr)
        return 2
    finally:
        journal.close()


if __name__ == "__main__":
    sys.exit(main())

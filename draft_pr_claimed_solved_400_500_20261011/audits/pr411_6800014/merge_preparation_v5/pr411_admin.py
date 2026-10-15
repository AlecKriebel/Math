#!/usr/bin/env python3
"""Administration only. Default CLI phases are GET-only; no scientific logic.

Approved source head and immutable native evidence are caller-pinned inputs.
Each later live mutation requires a separate exact-plan approval and durable
exclusive intent. Unknown outcomes always STOP; reconciliation is GET-only.
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
import time
import urllib.parse
import urllib.request

REPO = "AlecKriebel/Math"
PR = 411
BRANCH = "research/ricci-pinching-6800014"
PREFIX = "unsolved_math_prioritization/attempts/6800014/"
QUEUE = "unsolved_math_prioritization/QUEUE.md"
ID = "6800014"
SHA = re.compile(r"[0-9a-f]{40}\Z")
HASH = re.compile(r"[0-9a-f]{64}\Z")
DOI = re.compile(r"10\.5281/zenodo\.[1-9][0-9]*\Z")
SHEET = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
GID = 1254632077
TITLE = 'Math Puzzles'
HEADERS = ['Original Problem', 'Solution Chat URL', 'DOI', 'Notes']
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
    directory = secure_directory(case)
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
                   "-H", "X-GitHub-Api-Version: 2022-11-28", "-H", "Cache-Control: no-cache", target]
        if body is not None:
            command += ["--input", "-"]
        try:
            result = subprocess.run(command, input=None if body is None else encoded(body),
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=45)
        except subprocess.TimeoutExpired as exc:
            raise Uncertain('GitHub transport timed out; outcome unconfirmed') from exc
        if result.returncode:
            raise Uncertain("GitHub API response unconfirmed; raw command output suppressed")
        try:
            return json.loads(result.stdout)
        except (ValueError, UnicodeError) as exc:
            raise Uncertain("GitHub API did not return confirmed JSON") from exc

    def production_record(self, record_id, native=False):
        url = "https://zenodo.org/api/records/" + str(record_id)
        request = urllib.request.Request(url, headers={"Accept": "application/vnd.inveniordm.v1+json" if native else "application/json"})
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
    api._native_get_count = getattr(api, '_native_get_count', 0) + 1
    answer = api.call("GET", route)
    need(isinstance(answer, dict), 'native GitHub GET is not a confirmed JSON object')
    return answer


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
    header, header_span, found, offset = None, None, [], 0
    try:
        for line in content.splitlines(keepends=True):
            spans = split_cells(line.rstrip(b"\r\n"))
            if spans is None and header is not None and line.count(b"|") >= 2 and re.search(rb"\b6800014\b", line):
                raise Stop("malformed selected-ID table line makes QUEUE ambiguous")
            if spans is not None:
                fields = [line[start:end].decode("utf-8").strip() for start, end in spans]
                if "ID / code" in fields and "Status" in fields:
                    need(header is None and len(fields) == len(set(fields)), "ambiguous/duplicate QUEUE header")
                    need(all(key in fields for key in ("ID / code", "Status", "Turns", "DOI", "Findings")), "QUEUE field missing")
                    header = fields
                    header_span = (offset, offset + len(line))
                elif header is not None:
                    id_index = header.index("ID / code")
                    possible = len(fields) > id_index and fields[id_index].split("/", 1)[0].strip() == ID
                    if possible:
                        need(len(fields) == len(header), "selected QUEUE row has ambiguous cell count")
                        found.append({"fields": dict(zip(header, fields)), "header_span": header_span, "line_span": (offset, offset + len(line)), "spans":
                                      {key: (offset + start, offset + end) for key, (start, end) in zip(header, spans)}})
                    elif re.search(rb"\b6800014\b", line):
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


def blob(api, sha):
    # Git objects are immutable. Reuse only bytes whose full Git SHA was
    # recomputed; every selected path still checks its own mode/size/SHA256.
    cache = getattr(api, '_verified_blob_cache', None)
    if cache is None:
        cache = api._verified_blob_cache = {}
    if sha in cache:
        return cache[sha]
    answer = get(api, "git/blobs/" + sha)
    need(answer.get("sha") == sha and answer.get("encoding") == "base64", "blob identity/encoding mismatch")
    try:
        content = base64.b64decode(answer["content"], validate=False)
    except (KeyError, ValueError, TypeError) as exc:
        raise Stop("invalid blob response") from exc
    need(git_sha("blob", content) == sha, "blob bytes differ from Git object SHA")
    cache[sha] = content
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


def fresh_gate(api, expected_head, expected_main=None, draft=None, closed=False, require_merged=False):
    need(SHA.fullmatch(expected_head or "") is not None, "expected head must be explicit")
    if expected_main is not None:
        need(SHA.fullmatch(expected_main or "") is not None, "expected main must be explicit")
    for metadata_attempt in range(1, 6):
        pr = get(api, 'pulls/411')
        need(pr.get('number') == PR and pr.get('state') in (('open', 'closed') if closed else ('open',)), 'PR state invalid')
        head, base = pr.get('head', {}), pr.get('base', {})
        need(head.get('ref') == BRANCH and head.get('repo', {}).get('full_name') == REPO, 'PR branch/repository drift')
        need(base.get('ref') == 'main' and base.get('repo', {}).get('full_name') == REPO, 'PR base identity drift')
        need(isinstance(pr.get('draft'), bool), 'PR draft value unavailable')
        ref = get(api, 'git/ref/heads/' + BRANCH)
        matches = (head.get('sha') == expected_head and ref.get('object', {}).get('sha') == expected_head
                   and (draft is None or pr['draft'] is draft)
                   and (not require_merged or (pr['state'] == 'closed' and pr.get('merged') is True)))
        if matches:
            break
        if metadata_attempt == 5:
            raise Stop('bounded GET-only PR/ref/readiness refresh exhausted; no science input read, no write replay')
        time.sleep(0.2)
    content = get(api, "contents/" + QUEUE + "?ref=" + expected_head)
    need(content.get("type") == "file" and content.get("encoding") == "base64", "QUEUE contents response invalid")
    try:
        queue = base64.b64decode(content["content"], validate=False)
    except (KeyError, ValueError, TypeError) as exc:
        raise Stop("invalid QUEUE encoding") from exc
    need(git_sha("blob", queue) == content.get("sha"), "QUEUE content identity mismatch")
    header, row = selected_row(queue, required=False)
    # Stop/skip BEFORE any evidence/manifest/candidate open or selected math blob read.
    if row["fields"]["Status"] != "claimed_solved" or row["fields"]["Turns"] != "2/5":
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
            'metadata_GET_attempts': metadata_attempt,
            "draft": pr["draft"], "queue_sha256": digest(queue), "header": header,
            "selected_row": row["fields"]}, pr, queue


def queue_mask(content):
    _, row = selected_row(content, required=False)
    for start, end in sorted((row['spans'][key] for key in ('Status', 'Turns', 'Findings', 'DOI')), reverse=True):
        content = content[:start] + b'<BOUND-CELL>' + content[end:]
    return content


def queue_overlay(content, doi, findings):
    need(DOI.fullmatch(doi or '') is not None, 'not an actual production DOI')
    _, row = selected_row(content, required=False)
    fields = row['fields']
    need(fields['Status'] in ('queued', 'claimed_solved'), 'main Status already solved or incompatible')
    need((fields['Status'], fields['Turns']) in {('queued', '0/5'), ('claimed_solved', '2/5')}, 'main turn accounting drift')
    target_doi = '[DOI](https://doi.org/' + doi + ')'
    need(fields['DOI'] in ('', target_doi, doi, 'https://doi.org/' + doi), 'incompatible existing main DOI')
    need(fields['Findings'] in ('', findings), 'incompatible existing main Findings')
    wanted = {'Status': 'claimed_solved', 'Turns': '2/5', 'Findings': findings, 'DOI': target_doi}
    updated = content
    for key, value in wanted.items():
        need(isinstance(value, str) and not any(c in value for c in '|\r\n\0'), 'unsafe queue cell')
    for key in sorted(wanted, key=lambda k: row['spans'][k][0], reverse=True):
        start, end = row['spans'][key]
        prior = content[start:end]
        left = prior[:len(prior) - len(prior.lstrip(b' \t'))]
        right = prior[len(prior.rstrip(b' \t')):]
        updated = updated[:start] + left + wanted[key].encode() + right + updated[end:]
    need(queue_mask(content) == queue_mask(updated), 'QUEUE changed outside four selected cell interiors')
    _, result = selected_row(updated)
    need(result['fields']['Turns'] == '2/5' and all(result['fields'][k] == v for k, v in wanted.items()), 'QUEUE result differs')
    return updated


def accepted_map(value, head):
    fields = {'format', 'scientific_head', 'selected_tree_sha', 'entries', 'findings_path', 'assets'}
    need(isinstance(value, dict) and set(value) == fields and value['format'] == 'pr411-approved-science-map-v1'
         and SHA.fullmatch(head or '') is not None and value['scientific_head'] == head and SHA.fullmatch(value['selected_tree_sha'] or '') is not None,
         'root-approved map/head/tree binding invalid')
    need(isinstance(value['entries'], list) and value['entries'], 'positive selected map missing')
    files = {}
    for item in value['entries']:
        need(isinstance(item, dict) and set(item) == {'path', 'mode', 'bytes', 'sha256', 'git_blob_sha1'}, 'invalid approved file entry')
        path = path_name(item['path'])
        need(path.startswith(PREFIX) and path not in files and path != PREFIX.rstrip('/'), 'path outside selected subtree/duplicate')
        need(not any(part in ('.git', '__pycache__', 'private_sources', 'venv', '.venv', 'fixtures', 'raw_logs')
                     or part.startswith('.env') for part in path.lower().split('/')), 'private/runtime path cannot be selected')
        need(item['mode'] in ('100644', '100755') and type(item['bytes']) is int and item['bytes'] >= 0
             and HASH.fullmatch(item['sha256'] or '') is not None and SHA.fullmatch(item['git_blob_sha1'] or '') is not None,
             'approved scientific bytes/hash/mode invalid')
        files[path] = item
    need(value['findings_path'] in files and value['findings_path'].endswith(('/README.md', '/PUBLICATION.md')), 'Findings is not an accepted publication document')
    assets = value['assets']
    need(isinstance(assets, list) and len(assets) == 3, 'exactly three immutable published assets required')
    names, asset_paths = set(), set()
    for asset in assets:
        need(isinstance(asset, dict) and set(asset) == {'name', 'path', 'bytes', 'sha256'}, 'invalid asset entry')
        name = path_name(asset['name'])
        need('/' not in name and name not in names and asset['path'] not in asset_paths and asset['path'] in files,
             'duplicate/out-of-map asset')
        need(type(asset['bytes']) is int and asset['bytes'] > 0 and all(asset[k] == files[asset['path']][k] for k in ('bytes', 'sha256')), 'asset map differs')
        names.add(name)
        asset_paths.add(asset['path'])
    need(sum(n.endswith('.pdf') for n in names) == 1 and sum(n.endswith('.zip') for n in names) == 2, 'one PDF/two ZIPs required')
    return files


def verify_selected(api, tree, approved):
    started, before = time.monotonic(), getattr(api, '_native_get_count', 0)
    view = Merkle(api)
    leaves, directories, top = view.selected_inventory(tree)
    files = accepted_map(approved, approved['scientific_head'])
    need(top is not None and top == {'type': 'tree', 'mode': '040000', 'sha': approved['selected_tree_sha']}
         and set(leaves) == set(files), 'accepted positive subtree identity/inventory differs')
    expected_dirs = {PREFIX.rstrip('/')}
    for path, item in files.items():
        parts = path.split('/')
        expected_dirs.update('/'.join(parts[:i]) for i in range(len(PREFIX.rstrip('/').split('/')) + 1, len(parts)))
        leaf = leaves[path]
        need(leaf == {'mode': item['mode'], 'type': 'blob', 'sha': item['git_blob_sha1']}, 'scientific file mode/Git blob drift')
        data = blob(api, leaf['sha'])
        need(len(data) == item['bytes'] and digest(data) == item['sha256'], 'scientific positive file SHA256/size drift')
    need(directories == expected_dirs, 'unlisted empty directory in accepted subtree')
    observations = getattr(api, '_selected_verification_observations', None)
    if observations is None:
        observations = api._selected_verification_observations = []
    observations.append({'tree': tree, 'paths_checked': len(files), 'unique_git_blobs': len({item['git_blob_sha1'] for item in files.values()}),
                         'native_GET_calls': getattr(api, '_native_get_count', 0) - before,
                         'elapsed_seconds': round(time.monotonic() - started, 6)})
    return top


def timestamp(value):
    need(isinstance(value, str), 'native receipt capture timestamp missing')
    try:
        result = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError as exc:
        raise Stop('invalid native timestamp') from exc
    need(result.tzinfo is not None and result.utcoffset() == dt.timedelta(0), 'native timestamp must be UTC')
    return result


def production_asset(record_id, name, limit):
    url = 'https://zenodo.org/api/records/' + str(record_id) + '/files/' + urllib.parse.quote(name, safe='') + '/content'
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, request, fp, code, message, headers, new_url):
            return None
    try:
        with urllib.request.build_opener(NoRedirect).open(url, timeout=60) as response:
            need(response.geturl() == url, 'public asset redirected')
            data = response.read(limit + 1)
    except OSError as exc:
        raise Uncertain('public asset GET unconfirmed') from exc
    need(len(data) == limit, 'published asset length differs')
    return data


def canonical_range(value):
    need(isinstance(value, str), 'native Sheet range missing')
    prefix, separator, cells = value.partition('!')
    need(separator and prefix in (TITLE, "'" + TITLE + "'"), 'wrong native Sheet tab')
    return cells


def original_intent(case, ref, service, operation, params=None):
    raw = document(case, ref)
    intent = raw.get('intent', {})
    need(intent.get('evidence_kind') == 'native_production_api' and intent.get('service') == service
         and intent.get('operation') == operation and intent.get('params') == params, 'original native request intent differs')
    return intent


def gws_receipt(case, intent_ref, native_ref, response_ref, method, params, fresh=True):
    intent = original_intent(case, intent_ref, 'sheet', method, params)
    age = (dt.datetime.now(dt.timezone.utc) - timestamp(intent.get('utc'))).total_seconds()
    need(age >= 0 and (not fresh or age <= 300), 'native GWS request stale or future')
    native, response = document(case, native_ref), document(case, response_ref)
    need(native.get('service') == 'gws' and native.get('method') == method and native.get('params') == params
         and type(native.get('returncode')) is int and native['returncode'] == 0, 'native GWS command/target/result differs')
    try:
        actual = json.loads(base64.b64decode(native['stdout_base64'], validate=True))
    except (KeyError, ValueError, TypeError) as exc:
        raise Stop('original GWS stdout is not confirmed JSON') from exc
    need(actual == response, 'native GWS stdout/parsed response join differs')
    return response


def evidence(case, binding, approved, api):
    need(isinstance(binding, dict) and set(binding) == {'format', 'doi', 'publication', 'sheet'}
         and binding['format'] == 'pr411-native-administration-bindings-v1' and DOI.fullmatch(binding['doi'] or '') is not None,
         'native administration binding invalid')
    doi = binding['doi']
    record_id = int(doi.rsplit('.', 1)[1])
    pub = binding['publication']
    fields = {'submitted_intent', 'submitted_response', 'legacy_public_response', 'legacy_public_native',
              'authenticated_native_response', 'public_native_response', 'public_native_native', 'approved_native_snapshot', 'result'}
    need(isinstance(pub, dict) and set(pub) == fields, 'original native publication references incomplete')
    # The audited client exposes parsed legacy responses, not HTTP status.
    # Accept an authentic submitted GET readback or original publish response;
    # neither is silently converted into a fabricated HTTP certificate.
    submit_intent = document(case, pub['submitted_intent']).get('intent', {})
    allowed = ('POST /api/deposit/depositions/' + str(record_id) + '/actions/publish',
               'GET /api/deposit/depositions/' + str(record_id))
    need(submit_intent.get('evidence_kind') == 'native_production_api' and submit_intent.get('service') == 'zenodo'
         and submit_intent.get('operation') in allowed, 'original submitted native intent differs')
    submitted = document(case, pub['submitted_response'])
    need(isinstance(submitted, dict) and str(submitted.get('id')) == str(record_id) and submitted.get('submitted') is True
         and (submitted.get('doi') or submitted.get('metadata', {}).get('doi')) == doi, 'native legacy submitted state/DOI not confirmed')
    pinned_public = document(case, pub['legacy_public_response'])
    pinned_native = document(case, pub['public_native_response'])
    auth_native = document(case, pub['authenticated_native_response'])
    snapshot = document(case, pub['approved_native_snapshot'])
    need(set(snapshot) == {'metadata', 'access', 'custom_fields'} and isinstance(snapshot['metadata'], dict)
         and snapshot['metadata'] and isinstance(snapshot['access'], dict) and snapshot['custom_fields'] == {}, 'root-pinned actual native snapshot missing')
    for key, reference_key, accept in ((pinned_public, 'legacy_public_native', 'application/json'),
                                     (pinned_native, 'public_native_native', 'application/vnd.inveniordm.v1+json')):
        raw = document(case, pub[reference_key])
        need(raw.get('url') == 'https://zenodo.org/api/records/' + str(record_id) and raw.get('accept') == accept
             and raw.get('status') == 200, 'actual public JSON HTTP custody differs')
        try:
            body = json.loads(base64.b64decode(raw['body_base64'], validate=True))
        except (KeyError, ValueError, TypeError) as exc:
            raise Stop('public native raw JSON missing') from exc
        need(encoded(body) == encoded(key), 'public raw/parsed response join differs')
    public, native = api.production_record(record_id), api.production_record(record_id, native=True)
    need(isinstance(public, dict) and isinstance(native, dict), 'fresh public records are not confirmed JSON objects')
    need(str(public.get('id', public.get('recid'))) == str(record_id) and public.get('doi') == doi
         and isinstance(public.get('metadata'), dict) and encoded(public['metadata']) == encoded(pinned_public.get('metadata')),
         'fresh public DOI or pinned actual legacy metadata differs')
    # Explicit observed Zenodo legacy projection, never a generic normalizer.
    legacy = submitted.get('metadata', {})
    same = {'access_right', 'creators', 'description', 'keywords', 'language', 'notes', 'publication_date', 'title', 'version'}
    auth_keys = same | {'doi', 'imprint_publisher', 'license', 'prereserve_doi', 'publication_type', 'upload_type'}
    public_keys = same | {'doi', 'license', 'relations', 'resource_type'}
    need(isinstance(legacy, dict) and set(legacy) == auth_keys and set(public['metadata']) == public_keys,
         'actual authenticated15/public13 legacy key set differs')
    need(all(encoded(public['metadata'][key]) == encoded(legacy[key]) for key in same), 'actual nine shared public legacy fields differ')
    need(legacy['doi'] == public['metadata']['doi'] == doi
         and isinstance(legacy['prereserve_doi'], dict) and type(legacy['prereserve_doi'].get('recid')) is int
         and encoded(legacy['prereserve_doi']) == encoded({'doi': doi, 'recid': record_id})
         and legacy['imprint_publisher'] == 'Zenodo', 'actual authenticated DOI reservation/default publisher differs')
    need(legacy['license'] == 'cc-by-4.0' and public['metadata']['license'] == {'id': legacy['license']}
         and legacy['upload_type'] == 'publication' and legacy['publication_type'] == 'preprint'
         and public['metadata']['resource_type'] == {'type': legacy['upload_type'], 'subtype': legacy['publication_type'], 'title': 'Preprint'},
         'explicit legacy license/resource type projection differs')
    need(str(native.get('id')) == str(record_id) and native.get('pids', {}).get('doi', {}).get('identifier') == doi,
         'fresh native record/DOI differs')
    for record in (auth_native, pinned_native, native):
        need(all(encoded(record.get(k)) == encoded(v) for k, v in snapshot.items())
             and encoded(record.get('pids')) == encoded(pinned_native.get('pids')),
             'root-pinned actual native metadata/access/pids differs')
        if 'is_published' in record:
            need(type(record['is_published']) is bool and record['is_published'] is True, 'native publication flag is not true')
    # Publisher is established by actual authenticated/public native metadata
    # and the root-approved snapshot; its absent legacy field is not invented.
    need(snapshot['metadata'].get('publisher') == 'Zenodo', 'approved native publisher differs')
    parent = auth_native.get('parent')
    need(isinstance(parent, dict) and isinstance(parent.get('access'), dict), 'authenticated native concept parent missing')
    concept = parent.get('id')
    need(isinstance(concept, str) and re.fullmatch(r'[1-9][0-9]*', concept) is not None and concept != str(record_id),
         'authenticated native concept parent identity invalid')
    need(parent.get('pids', {}).get('doi') == {'client': 'datacite', 'provider': 'datacite', 'identifier': '10.5281/zenodo.' + concept},
         'authenticated native concept DOI/record identity differs')
    parent_access = parent['access']
    need(parent_access.get('grants') == [] and parent_access.get('links') == [], 'authenticated parent access decorators not observed empty values')
    projected_parent = {**parent, 'access': {key: value for key, value in parent_access.items() if key not in ('grants', 'links')}}
    for record in (pinned_native, native):
        need(encoded(record.get('parent')) == encoded(projected_parent), 'public native parent differs beyond only empty grants/links omission')
    for record in (auth_native, pinned_native, native):
        need(record.get('pids', {}).get('doi') == {'client': 'datacite', 'provider': 'datacite', 'identifier': doi}
             and record.get('pids', {}).get('oai') == {'identifier': 'oai:zenodo.org:' + str(record_id), 'provider': 'oai'}
             and record.get('is_draft') is False,
             'actual native record PID/first-version/draft identity differs')
    need(encoded(auth_native.get('versions')) == encoded({'index': 1, 'is_latest': True, 'is_latest_draft': True}),
         'authenticated native first-version shape differs')
    for record in (pinned_native, native):
        need(encoded(record.get('versions')) == encoded({'index': 1, 'is_latest': True}),
             'public native first-version shape differs; absent private latest-draft flag is not invented')
    need(encoded(public['metadata']['relations']) == encoded({'version': [{'index': 0, 'is_last': True, 'parent': {'pid_type': 'recid', 'pid_value': concept}}]}),
         'actual public first-version relation differs from authentic native concept PID')
    access = snapshot['access']
    need(access.get('record') == access.get('files') == 'public' and access.get('embargo', {}).get('active', False) is False,
         'actual native metadata/access not public')
    files = public.get('files')
    need(isinstance(files, list), 'public record files missing')
    by_name = {}
    for item in files:
        need(isinstance(item, dict), 'invalid public file')
        name = item.get('key', item.get('filename'))
        need(isinstance(name, str) and name not in by_name, 'duplicate/missing public filename')
        by_name[name] = item
    need(set(by_name) == {a['name'] for a in approved['assets']}, 'public three-asset file set differs')
    actual_assets = []
    for asset in approved['assets']:
        remote = by_name[asset['name']]
        need(remote.get('size', remote.get('filesize')) == asset['bytes'], 'public asset size metadata drift')
        data = api.production_asset(record_id, asset['name'], asset['bytes']) if hasattr(api, 'production_asset') else production_asset(record_id, asset['name'], asset['bytes'])
        need(len(data) == asset['bytes'] and digest(data) == asset['sha256'], 'actual public asset SHA256 differs')
        checksum = remote.get('checksum')
        need(checksum in ('sha256:' + digest(data), 'md5:' + hashlib.md5(data).hexdigest()), 'public checksum differs')
        actual_assets.append({'name': asset['name'], 'sha256': digest(data), 'size': len(data)})
    result = document(case, pub['result'])
    need(result.get('evidence_kind') == 'native_production_api' and result.get('status') in
         ('tracker_verified', 'tracker_already_exact')
         and result.get('id') == record_id and result.get('doi') == doi
         and type(result.get('id')) is int
         and sorted(result.get('asset_hashes', []), key=lambda x: x['name']) == sorted(actual_assets, key=lambda x: x['name']),
         'authentic publication tool result/raw receipt/asset join differs')
    sheet = binding['sheet']
    fields = {'metadata_intent', 'metadata_native', 'metadata_response', 'batch_intent', 'batch_native', 'batch_response',
              'row_range', 'expected_row', 'append_intent', 'append_native', 'append_response'}
    need(isinstance(sheet, dict) and set(sheet) == fields, 'exact GWS target-row/header binding missing')
    row_range = sheet['row_range']
    match = re.fullmatch(r'A([1-9][0-9]*):D\1', canonical_range(row_range))
    need(match is not None and int(match[1]) >= 2, 'target tracker row is not exact A:D data row')
    need(canonical_range(result.get('tracker_range')) == canonical_range(row_range), 'original tracker result/actual returned row differ')
    metadata = gws_receipt(case, sheet['metadata_intent'], sheet['metadata_native'], sheet['metadata_response'],
                           'get', {'spreadsheetId': SHEET, 'fields': 'spreadsheetId,sheets.properties'})
    need(metadata.get('spreadsheetId') == SHEET and isinstance(metadata.get('sheets'), list), 'native spreadsheet metadata missing')
    matching = [s.get('properties', {}) for s in metadata['sheets'] if s.get('properties', {}).get('sheetId') == GID]
    need(len(matching) == 1 and matching[0].get('title') == TITLE, 'native tracker gid/title differs')
    ranges = ["'" + TITLE + "'!A1:D1", row_range]
    batch = gws_receipt(case, sheet['batch_intent'], sheet['batch_native'], sheet['batch_response'], 'batchGet',
                       {'spreadsheetId': SHEET, 'ranges': ranges, 'majorDimension': 'ROWS', 'valueRenderOption': 'UNFORMATTED_VALUE'})
    need(batch.get('spreadsheetId') == SHEET and isinstance(batch.get('valueRanges'), list) and len(batch['valueRanges']) == 2,
         'native returned-row batchGet identity/count differs')
    for actual, requested in zip(batch['valueRanges'], ranges):
        need(canonical_range(actual.get('range')) == canonical_range(requested) and actual.get('majorDimension') == 'ROWS',
             'native batchGet exact range/dimension differs')
    row = sheet['expected_row']
    need(batch['valueRanges'][0].get('values') == [HEADERS] and batch['valueRanges'][1].get('values') == [row]
         and isinstance(row, list) and len(row) == 4 and all(isinstance(cell, str) and cell for cell in row), 'exact native four-cell tracker/header differs')
    need(row[0] == 'https://www.imo.universite-paris-saclay.fr/~pierre.pansu/problems_MTDG.pdf#page=12', 'root-pinned original problem page differs')
    need(row[1] == 'https://github.com/' + REPO + '/pull/411' and row[2] == 'https://doi.org/' + doi,
         'native tracker PR URL/canonical DOI differs')
    append_refs = [sheet[k] for k in ('append_intent', 'append_native', 'append_response')]
    need(all(ref is None for ref in append_refs) or all(isinstance(ref, dict) for ref in append_refs), 'partial original append custody')
    if sheet['append_response'] is not None:
        need(result['status'] == 'tracker_verified', 'actual append/result status differs')
        params = {'spreadsheetId': SHEET, 'range': "'" + TITLE + "'!A:D", 'valueInputOption': 'RAW', 'insertDataOption': 'INSERT_ROWS',
                  'includeValuesInResponse': True, 'responseValueRenderOption': 'UNFORMATTED_VALUE'}
        appended = gws_receipt(case, sheet['append_intent'], sheet['append_native'], sheet['append_response'], 'append', params, fresh=False)
        original_append = document(case, sheet['append_intent'])
        expected_payload = {'majorDimension': 'ROWS', 'values': [row]}
        need(encoded(original_append.get('payload')) == encoded(expected_payload)
             and original_append['intent'].get('payload_sha256') == digest((json.dumps(expected_payload, sort_keys=True, indent=2, ensure_ascii=False) + '\n').encode()),
             'actual append intent did not bind exact four cells')
        updates = appended.get('updates', {})
        need(appended.get('spreadsheetId') == SHEET and updates.get('spreadsheetId') == SHEET
             and canonical_range(updates.get('updatedRange')) == canonical_range(row_range)
             and all(type(updates.get(k)) is int and updates[k] == v for k, v in (('updatedRows', 1), ('updatedColumns', 4), ('updatedCells', 4))),
             'actual returned append range/counts differs')
    else:
        need(result['status'] == 'tracker_already_exact', 'missing original append receipt cannot be fabricated or inferred')
    sheet_utcs = [document(case, sheet[key])['intent']['utc'] for key in ('metadata_intent', 'batch_intent')]
    deadline = (min(timestamp(value) for value in sheet_utcs) + dt.timedelta(seconds=300)).strftime('%Y-%m-%dT%H:%M:%SZ')
    return {'doi': doi, 'record_id': record_id, 'actual_assets': actual_assets,
            'sheet_freshness_deadline_utc': deadline,
            'public_metadata_sha256': digest(encoded(public['metadata'])), 'approved_native_snapshot_sha256': pub['approved_native_snapshot']['sha256'],
            'submitted_native_sha256': pub['submitted_response']['sha256'], 'publication_result_sha256': pub['result']['sha256'],
            'native_publication_flags': [record.get('is_published') for record in (auth_native, pinned_native, native)],
            'missing_native_publication_flag': 'Unavailable fields remain null; legacy submitted=true and fresh public reads establish publication, no flag is invented',
            'sheet_batch_native_sha256': sheet['batch_native']['sha256'], 'sheet_batch_response_sha256': sheet['batch_response']['sha256'],
            'sheet_id': SHEET, 'sheet_gid': GID, 'sheet_row_range': row_range,
            'append_response_available': sheet['append_response'] is not None}


def evidence_fresh(observed):
    # This fixed deadline derives from the bound original GET intent, rather
    # than an observed age or current timestamp in the approval digest.
    need(dt.datetime.now(dt.timezone.utc) <= timestamp(observed.get('sheet_freshness_deadline_utc')),
         'bound native Sheet GET freshness window expired; obtain new genuine GET receipts and a new separate plan approval')


def ancestry(api, before, after):
    if before == after:
        return
    comparison = get(api, 'compare/' + before + '...' + after)
    need(comparison.get('status') == 'ahead' and comparison.get('merge_base_commit', {}).get('sha') == before,
         'required main ancestry not confirmed')


def selected_main_snapshot(api, main):
    _, tree = commit_root(api, main)
    view = Merkle(api)
    entry = view.at(tree, QUEUE)
    need(entry is not None and entry['type'] == 'blob' and entry['mode'] in ('100644', '100755'), 'main QUEUE not regular')
    queue = blob(api, entry['sha'])
    _, row = selected_row(queue, required=False)
    top = view.at(tree, PREFIX.rstrip('/'))
    need(top is None or (top['type'] == 'tree' and top['mode'] == '040000'), 'main selected subtree is irregular')
    hs, he = row['header_span']
    rs, re_ = row['line_span']
    return {'queue_mode': entry['mode'], 'header_bytes_b64': base64.b64encode(queue[hs:he]).decode(),
            'selected_row_bytes_b64': base64.b64encode(queue[rs:re_]).decode(), 'selected_top': top}


def descendant_main_guard(api, anchor, snapshot, requested=None):
    """Admit only native descendants with exact selected administrative state.

    Remote main is a moving ref, not a CAS target. Observed SHA/time is a
    factual side channel; M remains the immutable integration tree basis.
    """
    need(SHA.fullmatch(anchor or '') is not None, 'main anchor invalid')
    if requested is not None:
        need(SHA.fullmatch(requested or '') is not None, 'caller observed main invalid')
        ancestry(api, anchor, requested)
        need(selected_main_snapshot(api, requested) == snapshot, 'caller main selected snapshot drift')
    for _ in range(4):
        current = get(api, 'git/ref/heads/main').get('object', {}).get('sha')
        need(SHA.fullmatch(current or '') is not None, 'latest native main invalid')
        ancestry(api, anchor, current)
        if requested is not None:
            ancestry(api, requested, current)
        need(selected_main_snapshot(api, current) == snapshot, 'latest descendant main header/full-row/mode/subtree drift')
        after = get(api, 'git/ref/heads/main').get('object', {}).get('sha')
        if after == current:
            return {'observed_main': current, 'observed_at_utc': utc(), 'main_anchor': anchor,
                    'descends_from_anchor': True, 'exact_selected_snapshot_preserved': True}
    raise Stop('main kept moving during bounded GET guard; no stable observation, no mutation retry')


def canonical_plan(plan):
    """Only observed tip/time may vary under the explicitly approved predicate."""
    return {key: value for key, value in plan.items() if key != 'native_observations'}


def proposal(api, science_head, main, source_queue, approved, doi):
    view = Merkle(api)
    _, science_root = commit_root(api, science_head)
    _, main_root = commit_root(api, main)
    comparison = get(api, 'compare/' + main + '...' + science_head)
    base = comparison.get('merge_base_commit', {}).get('sha')
    need(SHA.fullmatch(base or '') is not None, 'native merge base missing')
    _, base_root = commit_root(api, base)
    view.restricted_diff(base_root, science_root, {QUEUE, PREFIX.rstrip('/')})
    base_queue_entry = view.at(base_root, QUEUE)
    need(base_queue_entry is not None and base_queue_entry['type'] == 'blob', 'merge-base queue missing')
    need(queue_mask(blob(api, base_queue_entry['sha'])) == queue_mask(source_queue), 'science head changed non-target queue bytes/cells')
    main_queue_entry = view.at(main_root, QUEUE)
    need(main_queue_entry is not None and main_queue_entry['type'] == 'blob' and main_queue_entry['mode'] in ('100644', '100755'), 'main queue not regular')
    main_queue = blob(api, main_queue_entry['sha'])
    # Parse/reject administrative main conflicts BEFORE selected scientific bytes.
    findings = '[Publication package](' + approved['findings_path'][len('unsolved_math_prioritization/'):] + ')'
    source_fields = selected_row(source_queue)[1]['fields']
    need(source_fields['DOI'] in ('', '[DOI](https://doi.org/' + doi + ')', doi, 'https://doi.org/' + doi)
         and source_fields['Findings'] in ('', findings), 'accepted science QUEUE has incompatible registration')
    after_queue = queue_overlay(main_queue, doi, findings)
    selected_top = verify_selected(api, science_root, approved)
    main_top, base_top = view.at(main_root, PREFIX.rstrip('/')), view.at(base_root, PREFIX.rstrip('/'))
    need(main_top in (base_top, selected_top), 'concurrent main selected-case subtree drift')
    replacements = {PREFIX.rstrip('/'): selected_top,
                    QUEUE: {'type': 'blob', 'mode': main_queue_entry['mode'], 'sha': git_sha('blob', after_queue)}}
    expected_tree, nodes = view.overlay(main_root, replacements)
    return {'source_tree': science_root, 'main_tree': main_root, 'merge_base': base,
            'expected_tree': expected_tree, 'changed_nodes': nodes, 'replacements': replacements,
            'main_queue_content_b64': base64.b64encode(main_queue).decode(),
            'queue_content_b64': base64.b64encode(after_queue).decode(),
            'queue_before_sha256': digest(main_queue), 'queue_after_sha256': digest(after_queue), 'findings': findings, 'doi': doi}


def commit_spec(tree, science_head, main, person, date):
    need(science_head != main and isinstance(person, dict) and set(person) == {'name', 'email'}, 'explicit commit identity missing')
    need(all(isinstance(v, str) and v and not any(c in v for c in '\r\n\0<>') for v in person.values()), 'unsafe commit identity')
    parsed = timestamp(date)
    need(re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z', date) is not None, 'explicit second-resolution UTC commit date required')
    who = person['name'] + ' <' + person['email'] + '> ' + str(int(parsed.timestamp())) + ' +0000'
    message = 'PR411: bind published DOI and preserve fresh main\n'
    raw = ('tree ' + tree + '\nparent ' + science_head + '\nparent ' + main + '\nauthor ' + who + '\ncommitter ' + who + '\n\n' + message).encode()
    identity = dict(person, date=date)
    return git_sha('commit', raw), {'tree': tree, 'parents': [science_head, main], 'author': identity, 'committer': identity, 'message': message}


def secure_directory(path):
    parts = str(Path(path).absolute()).split('/')[1:]
    need(all(part not in ('', '.', '..') for part in parts), 'unsafe journal directory')
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for part in parts:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = child
        return fd
    except OSError as exc:
        os.close(fd)
        raise Stop('journal directory must exist without symlinks') from exc


def pre_intent_continuation(case, root, descriptor_ref, plan):
    """Validate one terminal merge abort with no remote intent, read-only.

    The prior claim survives. The new plan binds this descriptor and must
    independently pass all existing evidence, scope and approval gates.
    """
    need(plan.get('phase') == 'merge' and plan.get('expected_head') == plan.get('integrated_head')
         and plan.get('pre_intent_continuation') == {'descriptor': descriptor_ref}, 'continuation not bound to a merge plan')
    spec = document(case, descriptor_ref)
    fields = {'format', 'journal_root', 'prior_run_id', 'prior_plan', 'prior_claim', 'prior_journal', 'prior_stop',
              'prior_cli_native', 'root_stop_acceptance'}
    need(isinstance(spec, dict) and set(spec) == fields and spec['format'] == 'pr411-merge-pre-intent-continuation-v1',
         'continuation descriptor schema differs')
    prior_run = spec['prior_run_id']
    need(re.fullmatch(r'[A-Za-z0-9_-]{1,80}', prior_run or '') is not None, 'prior continuation run invalid')
    root_relative = path_name(spec['journal_root'])
    need(Path(root).absolute() == Path(case).absolute() / root_relative, 'continuation must use the exact original journal root')
    handle = secure_directory(root)
    os.close(handle)
    for key in fields - {'format', 'journal_root', 'prior_run_id'}:
        ref = spec[key]
        need(isinstance(ref, dict) and set(ref) == {'path', 'sha256'} and HASH.fullmatch(ref['sha256'] or '') is not None,
             'continuation original reference invalid')
        path_name(ref['path'])
    prior = document(case, spec['prior_plan'])
    need(prior.get('format') == 'pr411-administration-plan-v1' and prior.get('phase') == 'merge'
         and prior.get('expected_head') == plan['expected_head'] == prior.get('integrated_head')
         and 'pre_intent_continuation' not in prior, 'only original merge pre-intent abort can continue once')
    allowed_refresh = {'helper_sha256', 'evidence_bindings_sha256', 'native_evidence', 'pre_intent_continuation'}
    need(encoded({k: v for k, v in canonical_plan(prior).items() if k not in allowed_refresh}) ==
         encoded({k: v for k, v in canonical_plan(plan).items() if k not in allowed_refresh}),
         'continuation changed original source/head/main/registration/confirmed phase bindings')
    prior_hash = digest(encoded(canonical_plan(prior)))
    head = plan['expected_head']
    paths = {'prior_claim': root_relative + '/claims/merge-' + head + '.json',
             'prior_journal': root_relative + '/' + prior_run + '/journal.jsonl',
             'prior_stop': root_relative + '/' + prior_run + '/receipt.json'}
    need(all(spec[key]['path'] == value for key, value in paths.items()), 'prior claim/journal/STOP is outside the exact original run/root')
    claim_raw = read_local(case, spec['prior_claim']['path'], spec['prior_claim']['sha256'])
    claim = json.loads(claim_raw)
    need(claim_raw == encoded(claim) + b'\n' and encoded(claim) == encoded({'run_id': prior_run, 'phase': 'merge',
         'head': head, 'plan_sha256': prior_hash}), 'original exclusive claim/run/head/plan differs')
    journal_raw = read_local(case, spec['prior_journal']['path'], spec['prior_journal']['sha256'])
    need(journal_raw.endswith(b'\n') and len(journal_raw.splitlines()) == 1, 'original journal torn or has any additional event; no retry')
    exclusive = json.loads(journal_raw)
    need(isinstance(exclusive, dict) and set(exclusive) == {'at_utc', 'event', 'phase', 'head', 'plan_sha256'}
         and exclusive['event'] == 'exclusive_intent' and exclusive['phase'] == 'merge' and exclusive['head'] == head
         and exclusive['plan_sha256'] == prior_hash and journal_raw == encoded(exclusive) + b'\n',
         'original journal is not a sole canonical zero-write exclusive event')
    need(timestamp(exclusive['at_utc']) <= dt.datetime.now(dt.timezone.utc), 'original exclusive event is in the future')
    stopped = document(case, spec['prior_stop'])
    need(set(stopped) == {'format', 'phase', 'result', 'plan', 'error_type', 'mutation_resume_permitted'}
         and stopped['format'] == 'pr411-administration-result-v1' and stopped['phase'] == 'merge'
         and stopped['result'] == 'STOP_UNCONFIRMED_OR_DRIFT' and stopped['error_type'] == 'Stop'
         and stopped['mutation_resume_permitted'] is False and encoded(canonical_plan(stopped['plan'])) == encoded(canonical_plan(prior)),
         'original terminal STOP/plan differs; no intent-free continuation')
    native = document(case, spec['prior_cli_native'])
    need(native.get('evidence_kind') == 'actual_root_in_process_python_CLI_capture' and type(native.get('returncode')) is int
         and native['returncode'] == 2 and native.get('helper_sha256') == prior.get('helper_sha256')
         and native.get('stdout_base64') == '' and base64.b64decode(native.get('stderr_base64', ''), validate=True) ==
         b'STOP: ordinary merge not clean/mergeable\n', 'original completed CLI did not confirm the pre-intent guard STOP')
    argv = native.get('argv')
    need(isinstance(argv, list) and len(argv) >= 2 and argv[1] == 'apply' and len(argv[2:]) % 2 == 0
         and all(isinstance(v, str) for v in argv), 'original CLI argument custody missing')
    pairs = list(zip(argv[2::2], argv[3::2]))
    need(len({key for key, value in pairs}) == len(pairs), 'duplicate original CLI options')
    options = dict(pairs)
    need(all(options.get(key) == value for key, value in {'--phase': 'merge', '--head': head, '--run-id': prior_run,
         '--case': str(Path(case).absolute()), '--journal-root': str(Path(root).absolute()),
         '--plan': spec['prior_plan']['path'] + ':' + spec['prior_plan']['sha256']}.items()),
         'completed CLI does not bind the original exclusive run/root/plan')
    acceptance = document(case, spec['root_stop_acceptance'])
    need(acceptance.get('result') == 'VERIFIED_PREINTENT_MERGE_ABORT_NO_REMOTE_WRITE_ATTEMPT' and acceptance.get('head') == head
         and acceptance.get('original_exclusive_claim_retained') is True and acceptance.get('original_terminal_STOP_retained') is True
         and all(type(acceptance.get(k)) is int and acceptance[k] == v for k, v in
                 (('original_journal_events', 1), ('original_mutation_intents', 0), ('original_acknowledgments', 0)))
         and all(acceptance.get('pins', {}).get(spec[k]['path']) == spec[k]['sha256'] for k in
                 ('prior_claim', 'prior_journal', 'prior_stop', 'prior_cli_native')),
         'root zero-write acceptance does not join the actual original custody')
    return {'descriptor': descriptor_ref, 'journal_root': root_relative, 'prior_run_id': prior_run,
            'prior_plan_sha256': prior_hash, 'prior_claim': spec['prior_claim'], 'prior_journal': spec['prior_journal'],
            'prior_stop': spec['prior_stop'], 'prior_cli_native': spec['prior_cli_native'], 'root_stop_acceptance': spec['root_stop_acceptance']}


class Journal:
    """FD-anchored exclusive phase/head claim and fsynced append-only intents."""
    def __init__(self, root, run_id, phase, head, plan_hash, continuation=None):
        need(re.fullmatch(r'[A-Za-z0-9_-]{1,80}', run_id or '') is not None and phase in ('integrate', 'ready', 'merge')
             and SHA.fullmatch(head or '') is not None and HASH.fullmatch(plan_hash or '') is not None, 'journal identity invalid')
        self.root = secure_directory(root)
        self.fd = self.directory = None
        self.continuation = self.continuation_guard = None
        try:
            if continuation is not None:
                need(isinstance(continuation, tuple) and len(continuation) == 3, 'continuation custody inputs missing')
                case, descriptor_ref, plan = continuation
                need(phase == 'merge' and plan['expected_head'] == head and digest(encoded(canonical_plan(plan))) == plan_hash,
                     'continuation journal/new plan binding differs')
                certificate = pre_intent_continuation(case, root, descriptor_ref, plan)
                need(run_id != certificate['prior_run_id'], 'continuation cannot reuse the stopped run')
                self.continuation = (case, root, descriptor_ref, plan, certificate, plan_hash)
            try:
                os.mkdir('claims', mode=0o700, dir_fd=self.root)
            except FileExistsError:
                pass
            claims = os.open('claims', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=self.root)
            try:
                if self.continuation is None:
                    try:
                        claim = os.open(phase + '-' + head + '.json', os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=claims)
                    except FileExistsError as exc:
                        raise Stop('exclusive phase/head intent already exists; GET-only reconcile, never retry') from exc
                    with os.fdopen(claim, 'wb') as stream:
                        stream.write(encoded({'run_id': run_id, 'phase': phase, 'head': head, 'plan_sha256': plan_hash}) + b'\n')
                        stream.flush()
                        os.fsync(stream.fileno())
                    os.fsync(claims)
                else:
                    try:
                        os.mkdir('continuations', mode=0o700, dir_fd=self.root)
                    except FileExistsError:
                        pass
                    guards = os.open('continuations', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=self.root)
                    try:
                        name = 'merge-' + head + '.json'
                        try:
                            guard = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=guards)
                        except FileExistsError as exc:
                            raise Stop('the one merge continuation guard is already consumed; no further attempt') from exc
                        guard_raw = encoded({'run_id': run_id, 'phase': phase, 'head': head, 'plan_sha256': plan_hash,
                                             'pre_intent_continuation': certificate}) + b'\n'
                        with os.fdopen(guard, 'wb') as stream:
                            stream.write(guard_raw)
                            stream.flush()
                            os.fsync(stream.fileno())
                        os.fsync(guards)
                        os.fsync(self.root)
                        self.continuation_guard = {'path': certificate['journal_root'] + '/continuations/' + name,
                                                   'sha256': digest(guard_raw)}
                    finally:
                        os.close(guards)
            finally:
                os.close(claims)
            os.mkdir(run_id, mode=0o700, dir_fd=self.root)
            self.directory = os.open(run_id, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=self.root)
            self.fd = os.open('journal.jsonl', os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=self.directory)
            os.fsync(self.directory)
            os.fsync(self.root)
            self.add({'event': 'exclusive_intent', 'phase': phase, 'head': head, 'plan_sha256': plan_hash})
        except Exception:
            self.close()
            raise

    def add(self, event):
        if event.get('event') == 'intent' and self.continuation is not None:
            directory, journal_fd = self.directory, self.fd
            need(type(directory) is int and type(journal_fd) is int, 'closed continuation journal cannot claim a remote intent')
            try:
                os.stat('receipt.json', dir_fd=directory, follow_symlinks=False)
            except FileNotFoundError:
                pass
            else:
                raise Stop('terminal continuation receipt already exists; this phase cannot attempt a remote write')
            case, root, ref, plan, certificate, plan_hash = self.continuation
            need(digest(encoded(canonical_plan(plan))) == plan_hash, 'continuation plan drift before remote intent')
            need(pre_intent_continuation(case, root, ref, plan) == certificate, 'original pre-intent custody drift before remote intent')
            read_local(case, self.continuation_guard['path'], self.continuation_guard['sha256'])
            body = {'sha': plan['integrated_head'], 'merge_method': 'merge',
                    'commit_title': 'Merge PR411: published result for 6800014'}
            need(event.get('method') == 'PUT' and event.get('route') == 'pulls/411/merge'
                 and event.get('expected') == plan['integrated_head']
                 and encoded(event.get('native_request_body')) == encoded(body)
                 and event.get('body_sha256') == digest(encoded(body)), 'continuation remote intent is not the exact ordinary merge action')
            try:
                fence = os.open('remote_intent_guard.json', os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                                0o600, dir_fd=directory)
            except FileExistsError as exc:
                raise Stop('continuation remote intent already claimed; no second write or retry') from exc
            fence_raw = encoded({'plan_sha256': plan_hash, 'descriptor': ref,
                                 'remote_intent_sha256': digest(encoded(event))}) + b'\n'
            with os.fdopen(fence, 'wb') as stream:
                stream.write(fence_raw)
                stream.flush()
                os.fsync(stream.fileno())
            os.fsync(self.directory)
        raw = encoded({'at_utc': utc(), **event}) + b'\n'
        while raw:
            count = os.write(self.fd, raw)
            need(count > 0, 'durable intent write failed')
            raw = raw[count:]
        os.fsync(self.fd)

    def finish(self, value):
        fd = os.open('receipt.json', os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=self.directory)
        with os.fdopen(fd, 'wb') as stream:
            stream.write(encoded(value) + b'\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.fsync(self.directory)
        return value

    def close(self):
        for key in ('fd', 'directory', 'root'):
            fd = getattr(self, key, None)
            if fd is not None:
                os.close(fd)
                setattr(self, key, None)


def mutate(api, journal, method, route, body, expected, verify):
    journal.add({'event': 'intent', 'method': method, 'route': route, 'body_sha256': digest(encoded(body)),
                 'native_request_body': body, 'expected': expected})
    try:
        answer = api.call(method, route, body)
        journal.add({'event': 'response_received', 'route': route, 'response_sha256': digest(encoded(answer)), 'native_parsed_response': answer})
        verify(answer)
    except Exception as exc:
        journal.add({'event': 'outcome_unconfirmed', 'route': route, 'write_continuation_permitted': False})
        raise Uncertain('unknown/invalid write response; STOP, only separate GET-only reconciliation permitted') from exc
    journal.add({'event': 'response_confirmed', 'route': route, 'response_sha256': digest(encoded(answer)), 'native_parsed_response': answer})
    return answer


def prepare(api, case, phase, head, main, map_ref, evidence_ref, person=None, date=None, integration_ref=None, ready_ref=None, anchor_override=None):
    need(phase in ('integrate', 'ready', 'merge'), 'invalid administration phase')
    started, before = time.monotonic(), getattr(api, '_native_get_count', 0)
    api._verified_blob_cache, api._selected_verification_observations = {}, []
    gate, pr, queue = fresh_gate(api, head, draft=False if phase == 'merge' else True)
    if gate['skip']:
        raise Stop('current exact science/PR queue is not claimed_solved 2/5; no local evidence or scientific file read')
    approved = document(case, map_ref)
    science_head = head if phase == 'integrate' else approved.get('scientific_head')
    accepted_map(approved, science_head)
    binding = document(case, evidence_ref)
    evidence_started = time.monotonic()
    observed = evidence(case, binding, approved, api)
    evidence_seconds = time.monotonic() - evidence_started
    # Public asset and Sheet checks can take time. Recheck the native claimed
    # scope immediately before traversing or opening any selected science.
    refreshed, _, queue = fresh_gate(api, head, draft=False if phase == 'merge' else True)
    need(not refreshed['skip'], 'scope drift during administration evidence reads; no scientific bytes opened')
    gate = refreshed
    if phase == 'integrate':
        anchor = main if anchor_override is None else anchor_override
        snapshot = selected_main_snapshot(api, anchor)
        descendant_main_guard(api, anchor, snapshot, requested=main)
        proposed = proposal(api, science_head, anchor, queue, approved, observed['doi'])
        integrated_head, spec = commit_spec(proposed['expected_tree'], science_head, anchor, person, date)
    else:
        need(integration_ref is not None, 'original confirmed integration receipt required')
        receipt = document(case, integration_ref)
        need(receipt.get('format') == 'pr411-administration-result-v1' and receipt.get('phase') == 'integrate'
             and receipt.get('result') in ('CONFIRMED', 'CONFIRMED_RESPONSE_LATER_READBACK') and receipt.get('plan', {}).get('integrated_head') == head
             and receipt['plan'].get('approved_map_sha256') == map_ref['sha256'], 'integration native receipt/head/map differs')
        validate_recovery_receiver(api, case, receipt)
        previous = receipt['plan']
        need(previous['source_head'] == science_head, 'integrated source scientific head differs')
        proposed, integrated_head, spec = previous['proposal'], head, previous['commit_spec']
        anchor = previous['main_head']
        snapshot = previous['main_snapshot']
        descendant_main_guard(api, anchor, snapshot, requested=main)
        verify_created(api, head, spec, proposed)
        verify_selected(api, spec['tree'], approved)
        need(blob(api, Merkle(api).at(spec['tree'], QUEUE)['sha']) == base64.b64decode(proposed['queue_content_b64']), 'integrated QUEUE bytes differ')
        need(observed['doi'] == proposed['doi'], 'actual published DOI changed')
        if phase == 'merge':
            need(ready_ref is not None, 'original CONFIRMED ready receipt required; unknown ready cannot advance')
            ready = document(case, ready_ref)
            ready_plan = ready.get('plan', {})
            need(ready.get('format') == 'pr411-administration-result-v1' and ready.get('phase') == 'ready'
                 and ready.get('result') in ('CONFIRMED', 'CONFIRMED_RESPONSE_LATER_READBACK') and ready_plan.get('integrated_head') == head
                 and ready_plan.get('approved_map_sha256') == map_ref['sha256'] and ready_plan.get('commit_spec') == spec
                 and ready_plan.get('source_head') == science_head and ready_plan.get('main_head') == anchor
                 and ready.get('readback', {}).get('head') == head and ready['readback'].get('draft') is False,
                 'ready original response/readback/head/map binding differs; no observation-only continuation')
            validate_recovery_receiver(api, case, ready)
    ancestry(api, anchor, integrated_head) if phase != 'integrate' else None
    main_observation = descendant_main_guard(api, anchor, snapshot, requested=main)
    # Observation timestamps are retained in native private capture, not the
    # stable approval digest; otherwise every fresh GET would invalidate it.
    evidence_fresh(observed)
    original_gate = gate
    gate = {key: value for key, value in gate.items() if key not in ('checked_at_utc', 'main', 'metadata_GET_attempts')}
    return {'format': 'pr411-administration-plan-v1', 'phase': phase, 'source_head': science_head,
            'expected_head': head, 'main_head': anchor, 'main_snapshot': snapshot,
            'main_policy': 'Admit native descendants of the immutable integration main anchor only while exact selected header/full-row/QUEUE-mode/subtree snapshot is preserved; unrelated changes are preserved by the actual first-parent merge overlay.',
            'integrated_head': integrated_head, 'commit_spec': spec,
            'approved_map_sha256': map_ref['sha256'], 'evidence_bindings_sha256': evidence_ref['sha256'],
            'integration_receipt_sha256': None if integration_ref is None else integration_ref['sha256'],
            'ready_receipt_sha256': None if ready_ref is None else ready_ref['sha256'],
            'helper_sha256': digest(Path(__file__).read_bytes()),
            'native_evidence': observed, 'proposal': proposed, 'gate': gate,
            'native_observations': {'scope_gate': original_gate, 'descendant_main': main_observation,
                                    'verification_cost': {'native_GitHub_GET_calls': getattr(api, '_native_get_count', 0) - before,
                                                          'public_record_GET_calls': 2, 'public_asset_GET_calls': 3,
                                                          'evidence_elapsed_seconds': round(evidence_seconds, 6),
                                                          'total_prepare_elapsed_seconds': round(time.monotonic() - started, 6),
                                                          'selected_verifications': list(api._selected_verification_observations),
                                                          'sheet_seconds_remaining': round((timestamp(observed['sheet_freshness_deadline_utc']) - dt.datetime.now(dt.timezone.utc)).total_seconds(), 3)}},
            'approval_boundary': 'Approval binds this exact integration I rooted at M and the selected-preserving descendant-main predicate, not a fixed future ordinary-merge tree; current observed tip/time is recorded separately.'}, approved


def verify_integrated(api, plan, approved, draft=True):
    gate, _, queue = fresh_gate(api, plan['integrated_head'], draft=draft)
    need(not gate['skip'], 'integrated status/accounting drift')
    verify_created(api, plan['integrated_head'], plan['commit_spec'], plan['proposal'])
    verify_selected(api, plan['commit_spec']['tree'], approved)
    need(queue == base64.b64decode(plan['proposal']['queue_content_b64']), 'native integrated QUEUE differs')
    ancestry(api, plan['main_head'], plan['integrated_head'])
    main_observation = descendant_main_guard(api, plan['main_head'], plan['main_snapshot'])
    return dict(gate, descendant_main=main_observation, integration_tree_basis=plan['main_head'])


def verify_merge(api, plan, approved, expected_merge=None):
    gate, pr, _ = fresh_gate(api, plan['integrated_head'], draft=False, closed=True, require_merged=True)
    need(not gate['skip'] and pr['state'] == 'closed' and pr.get('merged') is True, 'ordinary merge not confirmed')
    merged_sha = pr.get('merge_commit_sha')
    need(SHA.fullmatch(merged_sha or '') is not None and (expected_merge is None or merged_sha == expected_merge), 'actual merge commit differs')
    commit, tree = commit_root(api, merged_sha)
    parents = [item.get('sha') for item in commit.get('parents', [])]
    need(len(parents) == 2 and parents[1] == plan['integrated_head'] and SHA.fullmatch(parents[0] or '') is not None, 'ordinary merge parents differ')
    ancestry(api, plan['main_head'], parents[0])
    _, parent_tree = commit_root(api, parents[0])
    view = Merkle(api)
    before_entry = view.at(parent_tree, QUEUE)
    need(before_entry is not None and before_entry['type'] == 'blob' and before_entry['mode'] in ('100644', '100755'), 'actual first-parent QUEUE irregular')
    before = blob(api, before_entry['sha'])
    need(selected_main_snapshot(api, parents[0]) == plan['main_snapshot'], 'actual first-parent selected header/full-row/mode/subtree drift')
    after = queue_overlay(before, plan['proposal']['doi'], plan['proposal']['findings'])
    replacements = {PREFIX.rstrip('/'): plan['proposal']['replacements'][PREFIX.rstrip('/')],
                    QUEUE: {'type': 'blob', 'mode': before_entry['mode'], 'sha': git_sha('blob', after)}}
    expected_tree, _ = view.overlay(parent_tree, replacements)
    need(tree == expected_tree, 'merge tree differs from actual first parent plus exact permitted overlay')
    merged_queue = blob(api, view.at(tree, QUEUE)['sha'])
    need(merged_queue == after, 'merged native queue differs')
    verify_selected(api, tree, approved)
    latest_main = get(api, 'git/ref/heads/main').get('object', {}).get('sha')
    need(SHA.fullmatch(latest_main or '') is not None, 'latest main invalid')
    ancestry(api, merged_sha, latest_main)
    _, latest_tree = commit_root(api, latest_main)
    latest_queue = blob(api, view.at(latest_tree, QUEUE)['sha'])
    _, latest_row = selected_row(latest_queue)
    need(latest_row['fields']['Turns'] == '2/5' and all(latest_row['fields'][k] == selected_row(after)[1]['fields'][k]
         for k in ('Status', 'Turns', 'Findings', 'DOI')), 'latest-main registration/status drift')
    verify_selected(api, latest_tree, approved)
    hs, he = latest_row['header_span']
    rs, re_ = latest_row['line_span']
    _, after_row = selected_row(after)
    ahs, ahe = after_row['header_span']
    ars, are = after_row['line_span']
    need(latest_queue[hs:he] == after[ahs:ahe] and latest_queue[rs:re_] == after[ars:are]
         and view.at(latest_tree, QUEUE)['mode'] == before_entry['mode'], 'latest-main full selected row/header/mode drift')
    return {'merge_sha': merged_sha, 'parents': parents, 'tree': tree, 'actual_first_parent': parents[0],
            'latest_main': latest_main, 'latest_main_descends_from_merge': True,
            'unrelated_first_parent_tree_preserved': True, 'native_selected_queue_sha256': digest(merged_queue)}


def check_approval(plan, approval):
    need(approval == {'format': 'pr411-explicit-administration-approval-v1', 'phase': plan['phase'],
                      'plan_sha256': digest(encoded(canonical_plan(plan))), 'expected_head': plan['expected_head'],
                      'expected_main': plan['main_head'], 'authorize_one_phase': True}, 'separate exact-plan approval missing/different')


def execute(api, plan, approved, journal, approval):
    check_approval(plan, approval)
    evidence_fresh(plan['native_evidence'])
    phase = plan['phase']
    gate, pr, queue = fresh_gate(api, plan['expected_head'], draft=False if phase == 'merge' else True)
    need(not gate['skip'], 'fresh pre-write claimed scope drift')
    descendant_main_guard(api, plan['main_head'], plan['main_snapshot'])
    try:
        if phase == 'integrate':
            content = base64.b64decode(plan['proposal']['queue_content_b64'])
            sha = git_sha('blob', content)
            mutate(api, journal, 'POST', 'git/blobs', {'content': base64.b64encode(content).decode(), 'encoding': 'base64'}, sha,
                   lambda a: need(a.get('sha') == sha, 'queue blob POST identity differs'))
            need(blob(api, sha) == content, 'created queue blob bytes differ')
            for node in plan['proposal']['changed_nodes']:
                mutate(api, journal, 'POST', 'git/trees', {'tree': [{'path': name, **item} for name, item in node['entries'].items()]}, node['sha'],
                       lambda a, node=node: need(a.get('sha') == node['sha'], 'tree POST identity differs'))
                need(Merkle(api).node(node['sha']) == node['entries'], 'created immediate tree differs')
            mutate(api, journal, 'POST', 'git/commits', plan['commit_spec'], plan['integrated_head'],
                   lambda a: need(a.get('sha') == plan['integrated_head'], 'commit POST identity differs'))
            verify_created(api, plan['integrated_head'], plan['commit_spec'], plan['proposal'])
            gate, _, _ = fresh_gate(api, plan['expected_head'], draft=True)
            need(not gate['skip'], 'last-read scope drift before ref PATCH')
            descendant_main_guard(api, plan['main_head'], plan['main_snapshot'])
            evidence_fresh(plan['native_evidence'])
            mutate(api, journal, 'PATCH', 'git/refs/heads/' + BRANCH, {'sha': plan['integrated_head'], 'force': False}, plan['integrated_head'],
                   lambda a: need(a.get('object', {}).get('sha') == plan['integrated_head'], 'ref PATCH response differs'))
            readback = verify_integrated(api, plan, approved)
        elif phase == 'ready':
            verify_integrated(api, plan, approved)
            node = pr.get('node_id')
            need(isinstance(node, str) and node, 'native PR GraphQL ID missing')
            body = {'query': 'mutation($id:ID!){markPullRequestReadyForReview(input:{pullRequestId:$id}){pullRequest{id isDraft headRefOid}}}',
                    'variables': {'id': node}}
            evidence_fresh(plan['native_evidence'])
            mutate(api, journal, 'POST', 'graphql', body, plan['integrated_head'],
                   lambda a: need(not a.get('errors') and a.get('data', {}).get('markPullRequestReadyForReview', {}).get('pullRequest') ==
                                  {'id': node, 'isDraft': False, 'headRefOid': plan['integrated_head']}, 'ready response did not confirm exact head'))
            readback = verify_integrated(api, plan, approved, draft=False)
        else:
            verify_integrated(api, plan, approved, draft=False)
            gate, current, _ = fresh_gate(api, plan['integrated_head'], draft=False)
            need(not gate['skip'] and current.get('mergeable') is True and current.get('mergeable_state') == 'clean', 'ordinary merge not clean/mergeable')
            descendant_main_guard(api, plan['main_head'], plan['main_snapshot'])
            body = {'sha': plan['integrated_head'], 'merge_method': 'merge', 'commit_title': 'Merge PR411: published result for 6800014'}
            evidence_fresh(plan['native_evidence'])
            response = mutate(api, journal, 'PUT', 'pulls/411/merge', body, plan['integrated_head'],
                              lambda a: need(a.get('merged') is True and SHA.fullmatch(a.get('sha', '')) is not None, 'ordinary merge response unconfirmed'))
            readback = verify_merge(api, plan, approved, response['sha'])
        return journal.finish({'format': 'pr411-administration-result-v1', 'phase': phase, 'result': 'CONFIRMED', 'plan': plan, 'readback': readback})
    except Exception as exc:
        journal.finish({'format': 'pr411-administration-result-v1', 'phase': phase, 'result': 'STOP_UNCONFIRMED_OR_DRIFT',
                        'plan': plan, 'error_type': type(exc).__name__, 'mutation_resume_permitted': False})
        raise


def reconcile(api, plan, approved, intent=None):
    """GET-only outcome inspection; no continuation authorization is returned."""
    if plan['phase'] != 'merge':
        descendant_main_guard(api, plan['main_head'], plan['main_snapshot'])
    if intent is not None and plan['phase'] == 'integrate' and intent.get('route') in ('git/blobs', 'git/trees', 'git/commits'):
        identity = intent.get('expected')
        need(SHA.fullmatch(identity or '') is not None and intent.get('method') == 'POST', 'original uncertain object intent invalid')
        if intent['route'] == 'git/blobs':
            need(identity == plan['proposal']['replacements'][QUEUE]['sha']
                 and blob(api, identity) == base64.b64decode(plan['proposal']['queue_content_b64']), 'uncertain queue object differs')
        elif intent['route'] == 'git/trees':
            nodes = {node['sha']: node['entries'] for node in plan['proposal']['changed_nodes']}
            need(identity in nodes and Merkle(api).node(identity) == nodes[identity], 'uncertain tree object differs')
        else:
            need(identity == plan['integrated_head'], 'uncertain commit object differs')
            verify_created(api, identity, plan['commit_spec'], plan['proposal'])
        observed = {'object_present_exact': True, 'route': intent['route'], 'sha': identity,
                    'branch_updated': 'NOT CERTIFIED; object presence is not branch confirmation'}
    elif plan['phase'] == 'merge':
        observed = verify_merge(api, plan, approved)
    else:
        observed = verify_integrated(api, plan, approved, draft=plan['phase'] == 'integrate')
    return {'format': 'pr411-administration-reconciliation-v1', 'result': 'OBSERVED_EXACT_OUTCOME',
            'phase': plan['phase'], 'readback': observed, 'mutation_resume_permitted': False}


def validate_known_ack_custody(api, case, plan, stop_ref, journal_ref):
    """Check original ordered native ACKs without imposing historical PR state.

    This permits an authentic recovered integration receipt to be received
    after ready while still requiring its original complete native custody.
    """
    stopped = document(case, stop_ref)
    need(stopped.get('format') == 'pr411-administration-result-v1' and stopped.get('result') == 'STOP_UNCONFIRMED_OR_DRIFT'
         and stopped.get('phase') == plan['phase'] and stopped.get('plan') == plan and stopped.get('mutation_resume_permitted') is False, 'original STOP receipt/plan differs')
    raw = read_local(case, journal_ref['path'], journal_ref['sha256'])
    need(raw.endswith(b'\n'), 'original journal has torn final line')
    events = [json.loads(line) for line in raw.splitlines()]
    need(events and events[0].get('event') == 'exclusive_intent' and events[0].get('phase') == plan['phase']
         and events[0].get('head') == plan['expected_head'] and events[0].get('plan_sha256') == digest(encoded(canonical_plan(plan))),
         'original exclusive journal binding differs')
    need(not any(e.get('event') == 'outcome_unconfirmed' for e in events), 'unconfirmed write cannot become a confirmed response from GET observations')
    intents, responses = [], []
    pending, received = None, None
    for event in events[1:]:
        need(isinstance(event, dict), 'original journal event is not an object')
        if event.get('event') == 'intent':
            need(pending is None, 'unmatched/duplicate original intent')
            need(event.get('body_sha256') == digest(encoded(event.get('native_request_body'))), 'original exact request-body hash differs')
            intents.append(event)
            pending = event
        elif event.get('event') == 'response_received':
            need(pending is not None and received is None and event.get('route') == pending['route'], 'original received response order differs')
            received = event.get('native_parsed_response')
            need(isinstance(received, dict) and event.get('response_sha256') == digest(encoded(received)), 'original received native response hash differs')
        elif event.get('event') == 'response_confirmed':
            need(pending is not None and event.get('route') == pending['route'], 'original response without matching ordered intent')
            answer = event.get('native_parsed_response')
            need(isinstance(answer, dict) and received == answer and event.get('response_sha256') == digest(encoded(answer)), 'original received/confirmed native parsed response/hash differs')
            responses.append(answer)
            pending, received = None, None
        else:
            raise Stop('extra/unrecognized original journal event')
    need(pending is None and len(intents) == len(responses), 'original write response absent; GET cannot supply it')
    phase = plan['phase']
    if phase == 'integrate':
        expected = [('POST', 'git/blobs', plan['proposal']['replacements'][QUEUE]['sha'])]
        expected += [('POST', 'git/trees', node['sha']) for node in plan['proposal']['changed_nodes']]
        expected += [('POST', 'git/commits', plan['integrated_head']), ('PATCH', 'git/refs/heads/' + BRANCH, plan['integrated_head'])]
    elif phase == 'ready':
        expected = [('POST', 'graphql', plan['integrated_head'])]
    else:
        expected = [('PUT', 'pulls/411/merge', plan['integrated_head'])]
    need([(i.get('method'), i.get('route'), i.get('expected')) for i in intents] == expected, 'missing/extra/reordered native write confirmation')
    nodes = {n['sha']: n['entries'] for n in plan['proposal']['changed_nodes']}
    for intent, answer in zip(intents, responses):
        route, body = intent['route'], intent['native_request_body']
        if route == 'git/blobs':
            need(body == {'encoding': 'base64', 'content': plan['proposal']['queue_content_b64']} and answer.get('sha') == intent['expected'], 'original queue POST confirmation differs')
        elif route == 'git/trees':
            need(isinstance(body, dict) and set(body) == {'tree'} and isinstance(body['tree'], list), 'original immediate tree request missing')
            entries = {}
            for item in body['tree']:
                need(isinstance(item, dict) and set(item) == {'path', 'mode', 'type', 'sha'} and item['path'] not in entries, 'original tree request invalid/duplicate')
                entries[item['path']] = {key: item[key] for key in ('mode', 'type', 'sha')}
            need(entries == nodes.get(intent['expected']) and node_identity(entries) == intent['expected'] and answer.get('sha') == intent['expected'], 'original tree confirmation differs')
        elif route == 'git/commits':
            need(body == plan['commit_spec'] and answer.get('sha') == plan['integrated_head'], 'original two-parent commit confirmation differs')
        elif route.startswith('git/refs/'):
            need(body == {'sha': plan['integrated_head'], 'force': False} and answer.get('object', {}).get('sha') == plan['integrated_head'], 'original nonforce PATCH confirmation differs')
        elif route == 'graphql':
            pr = get(api, 'pulls/411')
            wanted = {'id': pr.get('node_id'), 'isDraft': False, 'headRefOid': plan['integrated_head']}
            need(body == {'query': 'mutation($id:ID!){markPullRequestReadyForReview(input:{pullRequestId:$id}){pullRequest{id isDraft headRefOid}}}',
                          'variables': {'id': wanted['id']}} and not answer.get('errors')
                 and answer.get('data', {}).get('markPullRequestReadyForReview', {}).get('pullRequest') == wanted, 'original ready ACK not confirmed for exact head/PR')
        else:
            need(body == {'sha': plan['integrated_head'], 'merge_method': 'merge', 'commit_title': 'Merge PR411: published result for 6800014'}
                 and answer.get('merged') is True and SHA.fullmatch(answer.get('sha', '')) is not None, 'original ordinary merge ACK differs')
    return responses


def known_response_recovery(api, case, plan, approved, stop_ref, journal_ref):
    """GET-only new receipt; original STOP/ACK bytes remain unchanged.

    A write with no valid original ACK stays observations-only. Recovery
    authorizes no retry and does not relabel the original STOP result.
    """
    responses = validate_known_ack_custody(api, case, plan, stop_ref, journal_ref)
    phase = plan['phase']
    readback = verify_merge(api, plan, approved, responses[-1]['sha']) if phase == 'merge' else verify_integrated(api, plan, approved, draft=phase == 'integrate')
    return {'format': 'pr411-administration-result-v1', 'phase': phase, 'result': 'CONFIRMED_RESPONSE_LATER_READBACK',
            'plan': plan, 'readback': readback, 'original_stop_receipt': stop_ref, 'original_native_journal': journal_ref,
            'original_stop_receipt_sha256': stop_ref['sha256'],
            'original_native_journal_sha256': journal_ref['sha256'], 'original_stop_receipt_unchanged': True,
            'native_response_was_confirmed_before_recovery': True, 'recovery_is_GET_only': True,
            'original_phase_retry_permitted': False, 'later_phase_requires_separate_explicit_approval': True,
            'recovered_at_utc': utc()}


def validate_recovery_receiver(api, case, receipt):
    if receipt.get('result') != 'CONFIRMED_RESPONSE_LATER_READBACK':
        return
    fields = {'format', 'phase', 'result', 'plan', 'readback', 'original_stop_receipt', 'original_native_journal',
              'original_stop_receipt_sha256', 'original_native_journal_sha256', 'original_stop_receipt_unchanged',
              'native_response_was_confirmed_before_recovery', 'recovery_is_GET_only', 'original_phase_retry_permitted',
              'later_phase_requires_separate_explicit_approval', 'recovered_at_utc'}
    need(set(receipt) == fields and isinstance(receipt['readback'], dict), 'recovered receipt complete provenance missing')
    for key in ('original_stop_receipt_unchanged', 'native_response_was_confirmed_before_recovery', 'recovery_is_GET_only',
                'later_phase_requires_separate_explicit_approval'):
        need(receipt[key] is True, 'recovered receipt provenance flag differs')
    need(receipt['original_phase_retry_permitted'] is False and timestamp(receipt['recovered_at_utc']) <= dt.datetime.now(dt.timezone.utc),
         'recovery retry/future timestamp invalid')
    for key in ('original_stop_receipt', 'original_native_journal'):
        ref = receipt[key]
        need(isinstance(ref, dict) and set(ref) == {'path', 'sha256'} and ref['sha256'] == receipt[key + '_sha256'],
             'recovery original custody reference/hash differs')
    validate_known_ack_custody(api, case, receipt['plan'], receipt['original_stop_receipt'], receipt['original_native_journal'])


def reference(value):
    path, separator, sha = value.rpartition(':')
    need(separator and HASH.fullmatch(sha or '') is not None, 'input must be relative/path:SHA256')
    return {'path': path_name(path), 'sha256': sha}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('plan', 'apply', 'reconcile', 'recover'))
    parser.add_argument('--phase', choices=('integrate', 'ready', 'merge'), required=True)
    parser.add_argument('--case', type=Path, required=True)
    parser.add_argument('--head', required=True)
    parser.add_argument('--main', required=True)
    parser.add_argument('--map', dest='map_reference', required=True)
    parser.add_argument('--evidence', required=True)
    parser.add_argument('--integration')
    parser.add_argument('--ready')
    parser.add_argument('--person-name')
    parser.add_argument('--person-email')
    parser.add_argument('--commit-date')
    parser.add_argument('--plan')
    parser.add_argument('--approval')
    parser.add_argument('--intent-journal')
    parser.add_argument('--stop-receipt')
    parser.add_argument('--journal-root', type=Path)
    parser.add_argument('--run-id')
    parser.add_argument('--continuation', help='Pinned merge-only original pre-intent STOP descriptor; one successor under the same root')
    args = parser.parse_args()
    api = API()
    # No local input is opened until this fresh native head/claimed QUEUE gate.
    gate, _, _ = fresh_gate(api, args.head, draft=None, closed=args.operation in ('reconcile', 'recover') and args.phase == 'merge')
    need(not gate['skip'], 'STOP: nonclaimed/out-of-scope; no local evidence read')
    need(args.continuation is None or (args.operation in ('plan', 'apply') and args.phase == 'merge' and args.journal_root is not None),
         'pre-intent continuation is merge plan/apply only and requires the original journal root')
    map_ref, evidence_ref = reference(args.map_reference), reference(args.evidence)
    if args.operation in ('reconcile', 'recover'):
        need(args.plan is not None, 'reconcile needs the pinned original plan')
        plan = document(args.case, reference(args.plan))
        approved = document(args.case, map_ref)
        need(plan['approved_map_sha256'] == map_ref['sha256'] and plan['phase'] == args.phase
             and args.head in (plan['integrated_head'], plan['expected_head']), 'reconcile pinned plan/head differs')
        intent = None
        if args.intent_journal:
            ref = reference(args.intent_journal)
            raw = read_local(args.case, ref['path'], ref['sha256'])
            need(raw.endswith(b'\n'), 'intent journal has torn final line')
            events = [json.loads(line) for line in raw.splitlines()]
            need(events and events[0].get('event') == 'exclusive_intent' and events[0].get('plan_sha256') == digest(encoded(canonical_plan(plan))), 'intent journal plan binding differs')
            intents = [event for event in events if event.get('event') == 'intent']
            need(intents, 'original mutation intent missing')
            intent = intents[-1]
        if args.operation == 'recover':
            need(args.stop_receipt and args.intent_journal, 'known-response recovery requires original STOP and journal pins')
            result = known_response_recovery(api, args.case, plan, approved, reference(args.stop_receipt), reference(args.intent_journal))
        else:
            result = reconcile(api, plan, approved, intent)
    else:
        pinned_plan = None
        if args.operation == 'apply':
            need(args.plan is not None, 'apply requires original pinned plan')
            pinned_plan = document(args.case, reference(args.plan))
        plan, approved = prepare(api, args.case, args.phase, args.head, args.main, map_ref, evidence_ref,
                                 {'name': args.person_name, 'email': args.person_email}, args.commit_date,
                                 None if args.integration is None else reference(args.integration),
                                 None if args.ready is None else reference(args.ready),
                                 None if pinned_plan is None or args.phase != 'integrate' else pinned_plan['main_head'])
        if args.continuation is not None:
            plan['pre_intent_continuation'] = {'descriptor': reference(args.continuation)}
            pre_intent_continuation(args.case, args.journal_root, reference(args.continuation), plan)
        if args.operation == 'plan':
            result = {'canonical_plan_sha256': digest(encoded(canonical_plan(plan))), 'plan': plan, 'native_write': False}
        else:
            need(args.plan and args.approval and args.journal_root and args.run_id, 'apply needs pinned plan/approval and exclusive journal')
            need(canonical_plan(pinned_plan) == canonical_plan(plan), 'fresh substantive plan differs from approved plan; STOP without mutation')
            approval = document(args.case, reference(args.approval))
            check_approval(plan, approval)
            evidence_fresh(plan['native_evidence'])
            journal = Journal(args.journal_root, args.run_id, args.phase, args.head, digest(encoded(canonical_plan(plan))),
                              None if args.continuation is None else (args.case, reference(args.continuation), plan))
            try:
                result = execute(api, plan, approved, journal, approval)
            finally:
                journal.close()
    print(json.dumps(result, indent=2, sort_keys=True))


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


if __name__ == '__main__':
    try:
        main()
    except (Stop, OSError, KeyError, TypeError, ValueError) as error:
        print('STOP: ' + str(error), file=sys.stderr)
        sys.exit(2)

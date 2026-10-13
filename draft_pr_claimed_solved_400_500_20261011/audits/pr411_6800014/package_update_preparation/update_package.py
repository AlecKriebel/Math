#!/usr/bin/env python3
"""PR411 only. Prepared-byte updater; no mathematical or priority conclusion.

All writes require an approved, exact plan digest. A journal may never be reused
for apply. Unknown results stop; reconcile performs GETs only, never retries.
GitHub ref PATCH has no atomic compare-and-swap: the final read minimizes, but
cannot eliminate, its race. No force update is ever sent.
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
import uuid

REPO = "AlecKriebel/Math"
PR = 411
BRANCH = "research/ricci-pinching-6800014"
HEAD = "ac8b960bdda61c154cc30d7e3aba70389a9b139e"
PREFIX = "unsolved_math_prioritization/attempts/6800014/"
QUEUE = "unsolved_math_prioritization/QUEUE.md"
QBLOB = "81f397cb34eeb6ce1d3c828992abc0969ab2d74d"
QHASH = "0a7d24f03ae65b0e7ef87cd4be265b9229666323e9c1e66ae404542d30864f02"
HERE = Path(__file__).resolve().parent
CASE = HERE.parent
PRIVATE = CASE / "private_sources/package_update_preparation"
DENIED = {"private_sources", ".git", ".ssh", ".aws", "credentials", "secrets"}


class Stop(RuntimeError):
    pass


def need(condition, message):
    if not condition:
        raise Stop(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encoded(obj):
    return (json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode()


def oid(kind, data):
    return hashlib.sha1(kind.encode() + b" " + str(len(data)).encode() + b"\0" + data).hexdigest()


def fields(obj, keys):
    need(isinstance(obj, dict) and set(obj) == set(keys), "unexpected/missing mapping fields")


def safe_path(path, *, private=False):
    p = Path(path).absolute()
    need(".." not in Path(path).parts, "local traversal")
    need(private or not ({x.casefold() for x in p.parts} & DENIED), "private local path")
    for a in [*reversed(p.parents), p]:
        if a.exists() or a.is_symlink():
            need(not a.is_symlink(), "symlink in local path")
    return p


def read_regular(path, *, private=False):
    p = safe_path(path, private=private)
    st = p.lstat()
    need(stat.S_ISREG(st.st_mode), "nonregular local file")
    fd = os.open(p, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        now = os.fstat(fd)
        need((now.st_dev, now.st_ino, now.st_mode, now.st_size, now.st_mtime_ns, now.st_ctime_ns) ==
             (st.st_dev, st.st_ino, st.st_mode, st.st_size, st.st_mtime_ns, st.st_ctime_ns), "local file replaced/changed")
        with os.fdopen(fd, "rb", closefd=False) as f:
            data = f.read()
        end = os.fstat(fd)
        need((now.st_mode, now.st_size, now.st_mtime_ns, now.st_ctime_ns) ==
             (end.st_mode, end.st_size, end.st_mtime_ns, end.st_ctime_ns), "local file changed during read")
    finally:
        os.close(fd)
    return data, "100755" if st.st_mode & 0o111 else "100644"


def durable(path, obj, *, exclusive=False, private=False):
    p = safe_path(path, private=private)
    p.parent.mkdir(parents=True, exist_ok=True)
    safe_path(p.parent, private=private)
    if exclusive:
        need(not p.exists(), "journal/output already exists; use GET-only reconcile")
    tmp = p.with_name(p.name + "." + uuid.uuid4().hex + ".tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, "wb") as f:
        f.write(encoded(obj)); f.flush(); os.fsync(f.fileno())
    if exclusive:
        try:
            # Atomic absent-target claim: unlike check-then-replace, concurrent
            # apply invocations cannot both acquire the same journal.
            os.link(tmp, p, follow_symlinks=False)
        except FileExistsError as exc:
            raise Stop("journal/output already exists; use GET-only reconcile") from exc
        finally:
            tmp.unlink()
    else:
        os.replace(tmp, p)
    fd = os.open(p.parent, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def remote(path):
    need(isinstance(path, str) and path.startswith(PREFIX), "outside positive scientific prefix")
    parts = PurePosixPath(path).parts
    need(str(PurePosixPath(path)) == path and not ({x.casefold() for x in parts} & DENIED)
         and all(x not in (".", "..") and "\0" not in x for x in parts), "unsafe remote path")
    return path


def tree_bytes(entries):
    names = set()
    for e in entries:
        need(set(e) >= {"path", "mode", "type", "sha"}, "malformed tree entry")
        n, m, t = e["path"], e["mode"], e["type"]
        need(isinstance(n, str) and n and n not in (".", "..") and "/" not in n
             and "\0" not in n and n not in names, "non-immediate/duplicate tree entry")
        need((m, t) in {("040000", "tree"), ("100644", "blob"), ("100755", "blob"),
                        ("120000", "blob"), ("160000", "commit")}, "unknown tree mode/type")
        need(re.fullmatch(r"[0-9a-f]{40}", e["sha"]) is not None, "bad object SHA")
        names.add(n)
    order = sorted(entries, key=lambda e: (e["path"] + ("/" if e["type"] == "tree" else "")).encode())
    return b"".join((e["mode"].lstrip("0") + " " + e["path"]).encode() + b"\0" +
                    bytes.fromhex(e["sha"]) for e in order)


class Native:
    """gh API uses its configured authentication; never reads/prints credentials."""
    def request(self, method, endpoint, payload=None):
        cmd = ["gh", "api", "--method", method, "repos/" + REPO + "/" + endpoint]
        data = None
        if payload is not None:
            cmd += ["--input", "-"]
            data = json.dumps(payload).encode()
        self.last_native = {"method": method, "endpoint": endpoint, "request_sha256": sha(data or b"")}
        try:
            r = subprocess.run(cmd, input=data, capture_output=True, timeout=120)
        except subprocess.TimeoutExpired as exc:
            self.last_native.update({"returncode": None, "uncertain": True,
                                     "stdout_base64": base64.b64encode(exc.stdout or b"").decode(),
                                     "stderr_base64": base64.b64encode(exc.stderr or b"").decode()})
            raise
        self.last_native.update({"returncode": r.returncode, "stdout": r.stdout.decode("utf-8", errors="replace"),
                                 "stderr": r.stderr.decode("utf-8", errors="replace"),
                                 "stdout_base64": base64.b64encode(r.stdout).decode(),
                                 "stderr_base64": base64.b64encode(r.stderr).decode()})
        need(r.returncode == 0, "native request failed; response custody retained by caller")
        return json.loads(r.stdout)


class Engine:
    def __init__(self, api, evidence_dir, journal=None):
        self.api, self.evidence_dir, self.journal = api, safe_path(evidence_dir, private=True), journal
        self.evidence_dir.mkdir(parents=True, exist_ok=False)
        self.records, self.state, self.trees = [], {}, {}
        self.kind = "native_gh_api" if isinstance(api, Native) else "offline_mock"

    def save(self):
        if self.journal:
            durable(self.journal, self.state)

    def call(self, method, endpoint, payload=None):
        i = len(self.records)
        rec = {"index": i, "method": method, "endpoint": endpoint,
               "payload_sha256": sha(encoded(payload)), "utc": dt.datetime.now(dt.timezone.utc).isoformat()}
        self.records.append(rec)
        if method != "GET":
            need(self.journal is not None, "write has no durable journal")
            self.state["intent"] = rec; self.state["phase"] = "intent_recorded"; self.save()
        durable(self.evidence_dir / (f"{i:04d}_intent.json"), {"record": rec, "payload": payload,
                "evidence_kind": self.kind}, exclusive=True, private=True)
        try:
            response = self.api.request(method, endpoint, payload)
            if self.kind == "native_gh_api":
                durable(self.evidence_dir / (f"{i:04d}_native.json"), self.api.last_native, exclusive=True, private=True)
            durable(self.evidence_dir / (f"{i:04d}_response.json"), response, exclusive=True, private=True)
        except Exception as exc:
            if self.kind == "native_gh_api" and getattr(self.api, "last_native", None):
                native_file = self.evidence_dir / (f"{i:04d}_native.json")
                if not native_file.exists():
                    durable(native_file, self.api.last_native, exclusive=True, private=True)
            if method != "GET":
                self.state["phase"] = "unknown_write"; self.state["unknown_endpoint"] = endpoint; self.save()
            raise Stop("STOP: request result uncertain/failure; GET-only reconcile, no retry") from exc
        if method != "GET":
            self.state["last_response_sha256"] = sha(encoded(response)); self.save()
        return response

    def tree(self, ident):
        if ident not in self.trees:
            r = self.call("GET", "git/trees/" + ident)
            need(r.get("sha") == ident and r.get("truncated") is False, "truncated/wrong immediate tree")
            entries = [{k: e[k] for k in ("path", "mode", "type", "sha")} for e in r["tree"]]
            need(oid("tree", tree_bytes(entries)) == ident, "immediate tree fails Git SHA")
            self.trees[ident] = entries
        return self.trees[ident]

    def lookup(self, root, path):
        entry = {"sha": root, "type": "tree", "mode": "040000"}
        for part in PurePosixPath(path).parts:
            need(entry["type"] == "tree", "path blocked by non-tree")
            matches = [e for e in self.tree(entry["sha"]) if e["path"] == part]
            need(len(matches) == 1, "missing source path")
            entry = matches[0]
        return entry

    def blob(self, ident):
        r = self.call("GET", "git/blobs/" + ident)
        need(r.get("sha") == ident and r.get("encoding") == "base64", "wrong native blob")
        data = base64.b64decode(r["content"], validate=False)
        need(oid("blob", data) == ident and len(data) == r["size"], "native blob byte mismatch")
        return data

    def gate(self, head=HEAD, body_hash=None, title_hash=None):
        p = self.call("GET", f"pulls/{PR}")
        r = self.call("GET", "git/ref/heads/" + BRANCH)
        need(p["number"] == PR and p["state"] == "open" and p["draft"] is True and
             p["head"]["ref"] == BRANCH and p["head"]["sha"] == head and
             p["head"]["repo"]["full_name"] == REPO and r["ref"] == "refs/heads/" + BRANCH and
             r["object"]["type"] == "commit" and r["object"]["sha"] == head, "PR/ref gate drift")
        bh, th = sha((p["body"] or "").encode()), sha(p["title"].encode())
        need(body_hash is None or bh == body_hash, "PR body drift")
        need(title_hash is None or th == title_hash, "PR title drift")
        c = self.call("GET", "git/commits/" + head)
        need(c["sha"] == head, "source commit native identity mismatch")
        root = c["tree"]["sha"]
        q = self.lookup(root, QUEUE)
        need(q["sha"] == QBLOB and q["mode"] == "100644", "QUEUE object drift")
        data = self.blob(q["sha"])
        need(sha(data) == QHASH, "QUEUE original bytes drift")
        header, rows = None, []
        for line in data.decode().splitlines():
            if not line.startswith("|"):
                continue
            cells = [x.strip() for x in line.strip().strip("|").split("|")]
            if {"ID / code", "Status", "Turns"}.issubset(cells):
                need(len(set(cells)) == len(cells), "duplicate QUEUE header")
                header = cells
            elif header and len(cells) == len(header):
                row = dict(zip(header, cells))
                if row["ID / code"] == "6800014 / AMR-067-0014":
                    rows.append(row)
        need(len(rows) == 1 and rows[0]["Status"] == "claimed_solved" and rows[0]["Turns"] == "2/5",
             "selected QUEUE status/turns gate drift")
        return {"head": head, "root_tree": root, "body_sha256": bh, "title_sha256": th,
                "queue_blob_sha": QBLOB, "queue_sha256": QHASH}

    def load_spec(self, spec_path):
        raw, _ = read_regular(spec_path)
        s = json.loads(raw)
        fields(s, ["schema", "package_root", "files", "body", "source_receipt", "commit"])
        need(s["schema"] == 1 and isinstance(s["files"], list) and s["files"], "empty/bad mapping")
        root = safe_path(s["package_root"])
        need(root.is_dir() and root.is_relative_to(CASE) and root != CASE, "package root outside case")
        inventory = set()
        for parent, dirs, files in os.walk(root, followlinks=False):
            for name in dirs + files:
                p = safe_path(Path(parent) / name)
                need(p.is_dir() or stat.S_ISREG(p.lstat().st_mode), "nonregular package extra")
                if name in files:
                    inventory.add(str(p))
        entries, content, locals_seen, remotes_seen = [], {}, set(), set()
        for f in s["files"]:
            fields(f, ["local_path", "remote_path", "sha256", "blob_sha", "mode", "size"])
            p, rp = safe_path(f["local_path"]), remote(f["remote_path"])
            need(p.is_relative_to(root) and str(p) not in locals_seen and rp not in remotes_seen,
                 "duplicate/outside local mapping")
            data, mode = read_regular(p)
            need(mode == f["mode"] and mode in ("100644", "100755") and len(data) == f["size"]
                 and sha(data) == f["sha256"] and oid("blob", data) == f["blob_sha"], "candidate pin mismatch")
            locals_seen.add(str(p)); remotes_seen.add(rp); content[rp] = data
            entries.append({k: f[k] for k in ("remote_path", "sha256", "blob_sha", "mode", "size")})
        need(inventory == locals_seen, "package contains unlisted file extras")
        for p in remotes_seen:
            need(not any(other.startswith(p + "/") for other in remotes_seen), "remote file/path conflict")
        b = s["body"]
        fields(b, ["local_path", "sha256", "complete_packet_approved"])
        need(b["complete_packet_approved"] is True, "parent complete-packet body approval missing")
        need(safe_path(b["local_path"]).is_relative_to(CASE), "body outside case")
        body_data, _ = read_regular(b["local_path"])
        need(sha(body_data) == b["sha256"], "body pin mismatch")
        body = body_data.decode("utf-8")
        receipt = s["source_receipt"]
        fields(receipt, ["local_path", "sha256"])
        need(safe_path(receipt["local_path"]).is_relative_to(CASE), "receipt outside case")
        source_data, _ = read_regular(receipt["local_path"])
        need(sha(source_data) == receipt["sha256"], "independent source receipt digest mismatch")
        source = json.loads(source_data)
        need(source["pr"] == PR and source["problem_id"] == "6800014" and source["source_head"] == HEAD
             and source["branch"] == BRANCH and source["queue_blob_sha"] == QBLOB
             and source["queue_sha256"] == QHASH and source["status"] == "claimed_solved"
             and source["author_turns"] == "2/5", "independent source receipt differs")
        return s, sorted(entries, key=lambda f: f["remote_path"]), content, body, source, sha(raw)

    def replace(self, source_root, replacements):
        trie = {}
        for f in replacements:
            node = trie
            parts = PurePosixPath(f["remote_path"]).parts
            for part in parts[:-1]:
                node = node.setdefault(part, {})
            node[parts[-1]] = {"leaf": {"path": parts[-1], "mode": f["mode"], "type": "blob", "sha": f["blob_sha"]}}
        created = []
        def walk(old, edits):
            before = {e["path"]: e for e in self.tree(old)} if old else {}
            after = dict(before)
            for name, node in edits.items():
                prior = before.get(name)
                if "leaf" in node:
                    need(prior is None or prior["type"] == "blob" and prior["mode"] in ("100644", "100755"),
                         "replacement collides with nonregular source object")
                    after[name] = node["leaf"]
                else:
                    need(prior is None or prior["type"] == "tree", "replacement ancestor not tree")
                    child = walk(prior["sha"] if prior else None, node)
                    after[name] = {"path": name, "mode": "040000", "type": "tree", "sha": child}
            entries = list(after.values()); ident = oid("tree", tree_bytes(entries))
            if ident != old:
                created.append({"sha": ident, "entries": sorted(entries, key=lambda e: e["path"])})
            return ident
        return walk(source_root, trie), created

    def receipt_tree(self, files):
        trie = {}
        need(len(files) > 0, "empty source receipt")
        for f in files:
            rp = remote(f["remote_path"])[len(PREFIX):]
            node = trie
            for name in PurePosixPath(rp).parts[:-1]:
                node = node.setdefault(name, {})
            name = PurePosixPath(rp).name
            need(name not in node and f["mode"] in ("100644", "100755"), "duplicate/bad source receipt")
            node[name] = {"leaf": {"path": name, "mode": f["mode"], "type": "blob", "sha": f["blob_sha"]}}
        def walk(node):
            entries = [v["leaf"] if "leaf" in v else {"path": k, "mode": "040000", "type": "tree", "sha": walk(v)}
                       for k, v in node.items()]
            return oid("tree", tree_bytes(entries))
        return walk(trie)

    def commit_object(self, commit, tree):
        fields(commit, ["message", "author", "committer"])
        msg = commit["message"]
        need(isinstance(msg, str) and msg.endswith("\n") and not msg.endswith("\n\n") and "\0" not in msg,
             "commit message must have exactly one final newline")
        lines = ["tree " + tree, "parent " + HEAD]
        for role in ("author", "committer"):
            who = commit[role]; fields(who, ["name", "email", "date"])
            need(all(isinstance(who[k], str) and who[k] and not re.search(r"[\r\n<>\0]", who[k])
                     for k in ("name", "email")), "unsafe commit identity")
            need(re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", who["date"]), "explicit UTC commit timestamp required")
            stamp = int(dt.datetime.strptime(who["date"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc).timestamp())
            lines.append(f"{role} {who['name']} <{who['email']}> {stamp} +0000")
        raw = ("\n".join(lines) + "\n\n" + msg).encode()
        payload = {"tree": tree, "parents": [HEAD], **commit}
        return oid("commit", raw), sha(raw), payload

    def prepare(self, spec_path):
        gate = self.gate()  # FIRST, before selected local-byte or receipt reads.
        spec, files, content, body, source, spec_hash = self.load_spec(spec_path)
        selected = self.lookup(gate["root_tree"], PREFIX.rstrip("/"))
        need(selected["type"] == "tree" and selected["sha"] == source["selected_tree_sha"]
             and source["source_file_count"] == len(source["files"])
             and self.receipt_tree(source["files"]) == selected["sha"], "independent source snapshot binding fails")
        root, trees = self.replace(gate["root_tree"], files)
        need(root != gate["root_tree"], "no scientific byte changes")
        commit, raw_hash, payload = self.commit_object(spec["commit"], root)
        plan = {"schema": 1, "repo": REPO, "pr": PR, "branch": BRANCH, "source": gate,
                "spec_sha256": spec_hash, "source_receipt_sha256": spec["source_receipt"]["sha256"],
                "files": files, "body_sha256": sha(body.encode()), "root_tree": root,
                "trees": trees, "commit_sha": commit, "commit_raw_sha256": raw_hash, "commit_payload": payload}
        return plan, content, body

    def verify_commit(self, plan):
        c = self.call("GET", "git/commits/" + plan["commit_sha"])
        need(c["sha"] == plan["commit_sha"] and c["tree"]["sha"] == plan["root_tree"] and
             [x["sha"] for x in c["parents"]] == [HEAD], "planned native commit identity mismatch")
        payload = plan["commit_payload"]
        # Native message text may remove its final newline. Never rehash that
        # textual representation as if it were historical commit object bytes.
        need(c["message"] in (payload["message"], payload["message"][:-1]), "new commit message differs")
        for role in ("author", "committer"):
            need(all(c[role][k] == payload[role][k] for k in ("name", "email")), "new commit identity differs")
            need(dt.datetime.fromisoformat(c[role]["date"].replace("Z", "+00:00")) ==
                 dt.datetime.fromisoformat(payload[role]["date"].replace("Z", "+00:00")), "new commit date differs")

    def verify_package(self, plan, body_hash):
        self.trees = {}
        gate = self.gate(plan["commit_sha"], body_hash, plan["source"]["title_sha256"])
        need(gate["root_tree"] == plan["root_tree"], "final root/preservation mismatch")
        self.verify_commit(plan)
        for f in plan["files"]:
            e = self.lookup(gate["root_tree"], f["remote_path"])
            need(e["sha"] == f["blob_sha"] and e["mode"] == f["mode"] and e["type"] == "blob", "final file mode/object differs")
            data = self.blob(e["sha"])
            need(sha(data) == f["sha256"] and len(data) == f["size"], "final file bytes differ")
        # A root equals the deterministic replacement of the verified old root:
        # every untouched sibling and all outside-positive paths are preserved.
        self.gate(plan["commit_sha"], body_hash, plan["source"]["title_sha256"])
        return gate

    def apply(self, plan, content, body):
        self.state = {"schema": 1, "evidence_kind": self.kind, "plan_sha256": sha(encoded(plan)), "plan": plan,
                      "phase": "prepared", "evidence_dir": str(self.evidence_dir)}
        durable(self.journal, self.state, exclusive=True)
        self.gate(HEAD, plan["source"]["body_sha256"], plan["source"]["title_sha256"])
        for f in plan["files"]:
            response = self.call("POST", "git/blobs", {"content": base64.b64encode(content[f["remote_path"]]).decode(), "encoding": "base64"})
            need(response.get("sha") == f["blob_sha"], "created blob has wrong SHA; stop/reconcile")
        for t in plan["trees"]:
            response = self.call("POST", "git/trees", {"tree": t["entries"]})
            need(response.get("sha") == t["sha"], "created tree has wrong SHA; stop/reconcile")
        response = self.call("POST", "git/commits", plan["commit_payload"])
        need(response.get("sha") == plan["commit_sha"], "created commit has wrong SHA; stop/reconcile")
        self.verify_commit(plan)
        # Native API offers no CAS; never claim an atomic lease. One nonforced
        # PATCH only, immediately following fresh PR/ref/QUEUE/body/title checks.
        self.gate(HEAD, plan["source"]["body_sha256"], plan["source"]["title_sha256"])
        response = self.call("PATCH", "git/refs/heads/" + BRANCH, {"sha": plan["commit_sha"], "force": False})
        need(response.get("object", {}).get("sha") == plan["commit_sha"], "ref response differs; reconcile")
        self.verify_package(plan, plan["source"]["body_sha256"])
        self.state["phase"] = "branch_verified_body_pending"; self.save()
        self.gate(plan["commit_sha"], plan["source"]["body_sha256"], plan["source"]["title_sha256"])
        response = self.call("PATCH", f"pulls/{PR}", {"body": body})
        need(sha((response.get("body") or "").encode()) == plan["body_sha256"], "body response differs; reconcile")
        self.verify_package(plan, plan["body_sha256"])
        self.state["phase"] = "confirmed_complete"; self.save()
        return {"status": "confirmed_complete", "evidence_kind": self.kind, "commit_sha": plan["commit_sha"],
                "old_body_sha256": plan["source"]["body_sha256"], "new_body_sha256": plan["body_sha256"]}

    def reconcile(self, journal_path, approved_plan=None):
        raw, _ = read_regular(journal_path)
        j = json.loads(raw); plan = j["plan"]
        need(j["plan_sha256"] == sha(encoded(plan)) and plan["repo"] == REPO and plan["pr"] == PR
             and plan["branch"] == BRANCH and plan["source"]["head"] == HEAD, "journal/plan binding fails")
        need(approved_plan is None or approved_plan == j["plan_sha256"], "reconcile approved plan digest differs")
        p = self.call("GET", f"pulls/{PR}"); r = self.call("GET", "git/ref/heads/" + BRANCH)
        head, body_hash = p["head"]["sha"], sha((p["body"] or "").encode())
        need(r["object"]["sha"] == head, "PR/ref read disagreement: unresolved")
        need(head in (HEAD, plan["commit_sha"]), "head drift; reconciliation unresolved")
        allowed = (plan["source"]["body_sha256"],) if head == HEAD else (plan["source"]["body_sha256"], plan["body_sha256"])
        need(body_hash in allowed, "body drift during reconciliation")
        self.gate(head, body_hash, plan["source"]["title_sha256"])
        original = self.call("GET", "git/commits/" + HEAD)
        need(original["sha"] == HEAD and original["tree"]["sha"] == plan["source"]["root_tree"], "reconcile source root differs")
        root, trees = self.replace(original["tree"]["sha"], plan["files"])
        need(root == plan["root_tree"] and trees == plan["trees"], "reconcile preservation prediction differs")
        c = plan["commit_payload"]
        ident, raw_hash, payload = self.commit_object({k: c[k] for k in ("message", "author", "committer")}, root)
        need(ident == plan["commit_sha"] and raw_hash == plan["commit_raw_sha256"] and payload == c,
             "reconcile exact planned commit differs")
        if head == HEAD:
            self.gate(HEAD, plan["source"]["body_sha256"], plan["source"]["title_sha256"])
            status = "source_head_observed_no_branch_confirmation"
        elif head == plan["commit_sha"]:
            need(body_hash in (plan["source"]["body_sha256"], plan["body_sha256"]), "body drift during reconciliation")
            self.verify_package(plan, body_hash)
            status = "confirmed_complete" if body_hash == plan["body_sha256"] else "branch_confirmed_body_pending"
        else:
            raise Stop("head drift; reconciliation unresolved")
        return {"status": status, "evidence_kind": self.kind, "read_only": True, "journal_sha256": sha(raw),
                "old_body_sha256": plan["source"]["body_sha256"], "new_body_sha256": plan["body_sha256"],
                "observed_body_sha256": body_hash, "observed_head": head,
                "caution": "GET observations do not authorize retries; stale source reads cannot prove no write occurred."}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("mode", choices=("plan", "apply", "reconcile"))
    p.add_argument("--spec"); p.add_argument("--plan-out"); p.add_argument("--journal")
    p.add_argument("--approved-plan-sha256")
    a = p.parse_args()
    need(a.mode != "apply" or a.journal and a.approved_plan_sha256, "apply requires explicit journal and approved plan digest")
    need(a.mode != "reconcile" or a.journal and a.approved_plan_sha256,
         "reconcile requires existing journal and original approved plan digest")
    need(a.mode == "reconcile" or a.spec, "plan/apply require positive mapping spec")
    if a.journal:
        need(safe_path(a.journal).parent == HERE, "journal must be in preparation directory")
    if a.mode == "apply":
        need(not Path(a.journal).exists(), "existing journal forbids apply; reconcile only")
    evidence = PRIVATE / (dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_" + uuid.uuid4().hex)
    e = Engine(Native(), evidence, a.journal if a.mode == "apply" else None)
    if a.mode == "reconcile":
        result = e.reconcile(a.journal, a.approved_plan_sha256)
    else:
        plan, content, body = e.prepare(a.spec)
        digest = sha(encoded(plan))
        if a.mode == "plan":
            need(a.plan_out and safe_path(a.plan_out).parent == HERE, "plan output must be in preparation directory")
            durable(a.plan_out, plan, exclusive=True)
            result = {"status": "read_only_prepared_plan", "plan_sha256": digest,
                      "planned_commit": plan["commit_sha"], "native_evidence": str(evidence)}
        else:
            need(digest == a.approved_plan_sha256, "approved plan no longer matches fresh source/candidate/body")
            result = e.apply(plan, content, body)
    durable(evidence / "RESULT.json", result, exclusive=True, private=True)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (Stop, OSError, ValueError, KeyError, TypeError) as exc:
        print("STOP: " + str(exc), file=sys.stderr)
        sys.exit(2)

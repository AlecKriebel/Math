#!/usr/bin/env python3
"""PR789 complete Git-Merkle scope proof; only read operations.

Every untouched directory entry is retained by object ID. Rehashing all changed
ancestors yields the complete expected root, so comparing a final root checks
every path, mode and object, including source/data and other problem statuses.
This creates no Git object, branch, index, commit, ref, or integration candidate.
"""
import argparse, copy, datetime, hashlib, json, re, subprocess, sys, urllib.request
from pathlib import Path
sys.dont_write_bytecode = True
T = Path(__file__).resolve().parents[2]
REPO = T.parents[3]
H = "aa44dec3baf8c1cd179cf8b55f32be95c74ee81a"
PARENT = "0aaee0476b4d63565abe240ac3ba5c6c3cabf983"
IDENTITY_SHA = "92c0b6666f23bcab7624a7801d79247d8dc9a3d01333da8a300d2328da75db70"
Q = "unsolved_math_prioritization/QUEUE.md"
PREFIX = "unsolved_math_prioritization/attempts/30001478/"
BASELINE = b"| 827 | 30001478 / OWR-4335-003 | Prime Ideals and Coordinate-Ring Maps of $R(\\alpha,\\beta)$ | 0.0983 | 5.5 | 3 | 2010 | queued | 0/5 |  |  |  |"

def need(value, reason):
    if not value:
        raise RuntimeError(reason)

def oid(kind, raw):
    return hashlib.sha1(kind.encode()+b" "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

def safe_oid(value):
    need(isinstance(value, str) and re.fullmatch("[0-9a-f]{40}", value), "Not an exact object ID")
    return value

def tree_oid(rows):
    ordered = sorted(rows.items(), key=lambda x: x[0].encode()+(b"/" if x[1]["type"] == "tree" else b""))
    raw = b"".join(r["mode"].lstrip("0").encode()+b" "+n.encode()+b"\0"+bytes.fromhex(r["sha"]) for n,r in ordered)
    return oid("tree", raw)

class Local:
    def __init__(self, repo):
        self.repo = repo; self.cache = {}
    def raw(self, kind, sha):
        safe_oid(sha)
        raw = subprocess.check_output(["git", "cat-file", kind, sha], cwd=self.repo)
        need(oid(kind, raw) == sha, "Local object bytes differ")
        return raw
    def commit(self, sha):
        lines = self.raw("commit", sha).split(b"\n\n", 1)[0].splitlines()
        return {"sha": sha, "tree": next(x[5:].decode() for x in lines if x.startswith(b"tree ")),
                "parents": [x[7:].decode() for x in lines if x.startswith(b"parent ")]}
    def entries(self, sha):
        if sha is None:
            return {}
        if sha not in self.cache:
            raw = self.raw("tree", sha); rows = {}; offset = 0
            while offset < len(raw):
                space = raw.index(b" ", offset); nul = raw.index(b"\0", space)
                mode = raw[offset:space].decode().zfill(6); name = raw[space+1:nul].decode()
                object_sha = raw[nul+1:nul+21].hex(); offset = nul+21
                need(name not in rows and "/" not in name, "Duplicate/noncanonical tree entry")
                rows[name] = {"mode": mode, "type": "tree" if mode == "040000" else "commit" if mode == "160000" else "blob", "sha": object_sha}
            need(tree_oid(rows) == sha, "Tree rehash differs")
            self.cache[sha] = rows
        return copy.deepcopy(self.cache[sha])
    def blob(self, commit, path):
        r = entry(self, self.commit(commit)["tree"], path)
        need(r and r["mode"] == "100644" and r["type"] == "blob", "Expected regular file")
        return self.raw("blob", r["sha"])

class PublicGitHub:
    """Only unauthenticated HTTPS GETs. Bodies remain memory-only."""
    def __init__(self):
        self.cache = {}; self.commits = {}; self.gets = []
    def get(self, url):
        self.gets.append(url)
        req = urllib.request.Request(url, headers={"User-Agent": "PR789-independent-Merkle-audit"})
        with urllib.request.urlopen(req, timeout=60) as r:
            need(r.status == 200, "Public GET status")
            return r.read()
    def commit(self, sha):
        safe_oid(sha)
        if sha not in self.commits:
            d = json.loads(self.get("https://api.github.com/repos/AlecKriebel/Math/git/commits/"+sha))
            need(d["sha"] == sha, "Public commit identity differs")
            self.commits[sha] = {"sha": sha, "tree": d["tree"]["sha"], "parents": [p["sha"] for p in d["parents"]]}
        return self.commits[sha]
    def entries(self, sha):
        if sha is None:
            return {}
        if sha not in self.cache:
            d = json.loads(self.get("https://api.github.com/repos/AlecKriebel/Math/git/trees/"+safe_oid(sha)))
            need(d["sha"] == sha and not d.get("truncated"), "Public tree truncated or changed")
            rows = {r["path"]: {k: r[k] for k in ("mode", "type", "sha")} for r in d["tree"]}
            need(len(rows) == len(d["tree"]) and tree_oid(rows) == sha, "Public complete tree Merkle hash differs")
            self.cache[sha] = rows
        return copy.deepcopy(self.cache[sha])
    def blob(self, commit, path):
        r = entry(self, self.commit(commit)["tree"], path)
        need(r and r["mode"] == "100644" and r["type"] == "blob", "Expected regular public file")
        raw = self.get("https://raw.githubusercontent.com/AlecKriebel/Math/"+safe_oid(commit)+"/"+path)
        need(oid("blob", raw) == r["sha"], "Public immutable blob differs")
        return raw

def parts(path):
    p = path.split("/")
    need(p and all(x and x not in (".", "..") for x in p) and "\\" not in path and "\0" not in path, "Noncanonical path")
    return p

def entry(adapter, root, path):
    p = parts(path)
    for i, name in enumerate(p):
        row = adapter.entries(root).get(name)
        if row is None:
            return None
        if i == len(p)-1:
            return row
        need(row["type"] == "tree", "Non-directory path ancestor")
        root = row["sha"]

def expected_tree(adapter, root, updates):
    trie = {}
    for path, row in updates.items():
        p = parts(path); node = trie
        for n in p[:-1]:
            node = node.setdefault(n, {})
            need(isinstance(node, dict), "Conflicting update")
        need(p[-1] not in node, "Duplicate update")
        node[p[-1]] = ("leaf", row)
    def walk(sha, changes):
        rows = adapter.entries(sha)
        for name, change in changes.items():
            old = rows.get(name)
            if isinstance(change, tuple):
                need(old is None or old["type"] == "blob", "Cannot overwrite a nonblob")
                rows[name] = change[1]
            else:
                need(old is None or old["type"] == "tree", "Directory collision")
                rows[name] = {"mode": "040000", "type": "tree", "sha": walk(None if old is None else old["sha"], change)}
        return tree_oid(rows)
    return walk(root, trie)

def own_row(raw):
    found = [line.rstrip(b"\r\n") for line in raw.splitlines(keepends=True) if line.startswith(b"| ") and b" 30001478 / " in line]
    need(len(found) == 1, "Own queue row not unique")
    return found[0]

def queue_update(raw, candidate):
    before = own_row(raw); need(before in (BASELINE, candidate), "Main own row is neither exact baseline nor candidate")
    out = []
    for line in raw.splitlines(keepends=True):
        content = line.rstrip(b"\r\n")
        out.append(candidate+line[len(content):] if content == before else line)
    return b"".join(out)

def original(local):
    raw = (T/"intake/ROOT_SOURCE_IDENTITY.json").read_bytes()
    need(hashlib.sha256(raw).hexdigest() == IDENTITY_SHA, "Frozen original identity receipt changed")
    identity = json.loads(raw); rows = identity["original_files"]
    need(len(rows) == 58 and len({r["path"] for r in rows}) == 58, "Not 58 unique originals")
    need(local.commit(H)["parents"] == [PARENT], "Scientific head parent differs")
    changes = {}
    for r in rows:
        need(r["changeType"] == "ADDED" and r["path"].startswith(PREFIX), "Not an own original addition")
        data = local.blob(H, r["path"])
        need(len(data) == r["bytes"] and hashlib.sha256(data).hexdigest() == r["sha256"]
             and oid("blob", data) == r["git_blob"], "An original blob differs")
        changes[r["path"]] = {"mode": "100644", "type": "blob", "sha": r["git_blob"]}
    candidate = own_row(local.blob(H, Q))
    need(candidate.split(b"|")[8].strip() == b"claimed_solved" and candidate.split(b"|")[9].strip() == b"1/5", "Scientific candidate status/budget changed")
    before = local.blob(PARENT, Q); need(own_row(before) == BASELINE, "Original-parent baseline differs")
    changes[Q] = {"mode": "100644", "type": "blob", "sha": oid("blob", queue_update(before, candidate))}
    need(expected_tree(local, local.commit(PARENT)["tree"], changes) == local.commit(H)["tree"], "Original scientific commit contains another path or row change")
    return changes, candidate, identity

def expected_for(adapter, base, originals, candidate, identity):
    root = adapter.commit(base)["tree"]
    need(entry(adapter, root, PREFIX.rstrip("/")) is None, "Own candidate subtree already exists on main; reconcile")
    need(entry(adapter, root, PREFIX+"acceptance.json") is None, "Acceptance exists")
    selected = [x for x in json.loads(adapter.blob(base, "unsolved_math_prioritization/catalog.json")) if x["id"] == "30001478"]
    need(len(selected) == 1 and selected[0]["statement_hash"] == identity["statement_sha256"]
         and selected[0]["review_hash"] == identity["review_hash"], "Premerge source identity differs")
    before = adapter.blob(base, Q); after = queue_update(before, candidate)
    updates = copy.deepcopy(originals); updates[Q]["sha"] = oid("blob", after)
    expected = expected_tree(adapter, root, updates)
    return expected, {"base": base, "base_tree": root, "expected_tree": expected,
                      "queue_before_sha256": hashlib.sha256(before).hexdigest(),
                      "queue_after_sha256": hashlib.sha256(after).hexdigest(),
                      "only_own_queue_row_changed": before == after or before.replace(own_row(before), b"__OWN_ROW__", 1) == after.replace(candidate, b"__OWN_ROW__", 1),
                      "original_additions": 58, "all_other_paths_modes_and_objects_preserved": True}

def controls(local, originals, candidate, identity):
    root = local.commit(PARENT)["tree"]; target = local.commit(H)["tree"]
    rows = []
    def test(name, updates, equal):
        same = expected_tree(local, root, updates) == target
        rows.append({"case": name, "matches_original_complete_root": same, "control_pass": same == equal})
    test("exact_58_additions_and_own_row", originals, True)
    altered = copy.deepcopy(originals); first = sorted(p for p in altered if p != Q)[0]
    altered[first]["sha"] = "0"*40; test("changed_original_blob", altered, False)
    altered = copy.deepcopy(originals); altered[first]["mode"] = "100755"; test("changed_original_mode", altered, False)
    altered = copy.deepcopy(originals); altered.pop(first); test("missing_original_blob", altered, False)
    altered = copy.deepcopy(originals); altered[PREFIX+"EXTRA"] = altered[first]; test("extra_own_path", altered, False)
    altered = copy.deepcopy(originals); altered["unsolved_math_prioritization/catalog.json"] = altered[first]; test("source_catalog_overwrite", altered, False)
    altered = copy.deepcopy(originals); altered[Q]["sha"] = oid("blob", local.blob(H, Q)+b"unauthorized other row\n"); test("another_queue_change", altered, False)
    need(all(r["control_pass"] for r in rows), "Merkle negative control failed")
    return rows

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", type=Path, default=REPO); p.add_argument("--base")
    p.add_argument("--merge"); p.add_argument("--head", default=H)
    p.add_argument("--integration-base"); p.add_argument("--public-github", action="store_true")
    p.add_argument("--out", type=Path); a = p.parse_args()
    local = Local(a.repo); originals, candidate, identity = original(local)
    result = {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "original_scientific_head": H, "original_parent": PARENT,
              "identity_receipt_sha256": IDENTITY_SHA, "original_complete_tree_exact": True,
              "controls": controls(local, originals, candidate, identity),
              "no_Git_or_remote_mutations": True}
    adapter = PublicGitHub() if a.public_github else local
    if a.base:
        expected, detail = expected_for(adapter, safe_oid(a.base), originals, candidate, identity)
        result["premerge_scope"] = detail
        if a.head != H:
            need(a.integration_base, "Administrative integration requires the exact main base used")
            iroot, idetail = expected_for(adapter, safe_oid(a.integration_base), originals, candidate, identity)
            icommit = adapter.commit(safe_oid(a.head))
            need(icommit["parents"] in ([H], [H, a.integration_base]), "Integration does not directly preserve the original scientific head")
            need(icommit["tree"] == iroot, "Administrative integration tree has other changes")
            result["integration"] = dict(idetail, head=a.head, parents=icommit["parents"], original_scientific_head_preserved=True)
        else:
            need(not a.integration_base, "Unexpected integration base")
        if a.merge:
            m = adapter.commit(safe_oid(a.merge))
            need(m["parents"] == [a.base, a.head], "Actual merge parents differ from exact premerge main and eligible head")
            need(m["tree"] == expected, "Actual complete merge tree exceeds exact scope")
            result["actual_merge"] = dict(m, all_original_58_blobs_exact=True,
                                          only_own_candidate_queue_row_changed=True,
                                          every_other_path_preserved_from_premerge_main=True)
    else:
        need(not a.merge and not a.integration_base and a.head == H, "Missing exact premerge base")
    if isinstance(adapter, PublicGitHub):
        result["unauthenticated_public_GETs"] = adapter.gets
    result["result"] = "PASS_ACTUAL_EXACT_MERGE" if a.merge else "PASS_SCOPE_DESIGN_AND_CONTROLS"
    raw = json.dumps(result, indent=2)+"\n"
    if a.out:
        need(a.out.resolve().is_relative_to(Path(__file__).resolve().parents[1]), "Output outside owned admin area")
        a.out.write_text(raw)
    print(raw)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Independent raw-Merkle verifier; does not import the index builder."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
TARGET = b"unsolved_math_prioritization/attempts/30005468"
QUEUE = b"unsolved_math_prioritization/QUEUE.md"
AUTHOR = "c5252db6ec25ffdbfd2259bfdcf2fb6228e1846e"


def require(value, message):
    if not value:
        raise ValueError(message)


def oid(kind, data):
    return hashlib.sha1(kind.encode() + b" " + str(len(data)).encode() + b"\0" + data).hexdigest()


class RawObjects:
    def __init__(self):
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL="/dev/null",
                   GIT_OBJECT_DIRECTORY=str(ROOT / "private_objects"),
                   GIT_ALTERNATE_OBJECT_DIRECTORIES=str(ROOT.parent / "objects.git/objects"))
        self.process = subprocess.Popen(["git", "--git-dir", str(ROOT / "driver.git"),
                                         "cat-file", "--batch"], env=env,
                                        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
        self.cache = {}

    def get(self, sha):
        if sha not in self.cache:
            self.process.stdin.write(sha.encode() + b"\n")
            self.process.stdin.flush()
            header = self.process.stdout.readline().split()
            require(len(header) == 3 and header[0].decode() == sha, "Missing exact raw object " + sha)
            data = self.process.stdout.read(int(header[2]))
            require(self.process.stdout.read(1) == b"\n", "Bad batch framing")
            kind = header[1].decode()
            require(oid(kind, data) == sha, "Raw object SHA1 mismatch")
            self.cache[sha] = kind, data
        return self.cache[sha]

    def close(self):
        self.process.stdin.close()
        require(self.process.wait(timeout=10) == 0, "Raw batch reader failed")


def tree_entries(raw):
    entries = {}
    pos = 0
    while pos < len(raw):
        space = raw.index(b" ", pos)
        zero = raw.index(b"\0", space + 1)
        mode, name = raw[pos:space], raw[space + 1:zero]
        sha = raw[zero + 1:zero + 21].hex()
        require(len(sha) == 40 and name not in entries, "Malformed/duplicate raw tree entry")
        entries[name] = mode, sha
        pos = zero + 21
    require(pos == len(raw), "Raw tree length mismatch")
    return entries


def encode_tree(entries):
    ordered = sorted(entries, key=lambda name: name + (b"/" if entries[name][0] == b"40000" else b""))
    return b"".join(entries[name][0] + b" " + name + b"\0" + bytes.fromhex(entries[name][1]) for name in ordered)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", help="Prepared candidate directory")
    args = parser.parse_args()
    directory = Path(args.candidate).resolve()
    require(directory.parent == ROOT, "Candidate must be a direct child of reconciliation")
    proposal = json.loads((directory / "PROPOSAL.json").read_bytes())
    manifest = json.loads((directory / "BOUND_AUTHOR61.json").read_bytes())
    database = RawObjects()
    preserved_siblings, rewritten_directories = [], []

    def read_tree(sha):
        kind, data = database.get(sha)
        require(kind == "tree", "Expected tree")
        entries = tree_entries(data)
        require(encode_tree(entries) == data, "Tree not canonical by independent serializer")
        return entries

    def walk(sha, prefix=b""):
        result = {}
        for name, (mode, child) in read_tree(sha).items():
            path = prefix + name
            result[path] = (mode, child)
            if mode == b"40000":
                result.update(walk(child, path + b"/"))
        return result

    def compose(base, edits, prefix=b""):
        current = read_tree(base) if base else {}
        result = dict(current)
        groups = {}
        for path, replacement in edits.items():
            head, *tail = path.split(b"/", 1)
            groups.setdefault(head, {})[tail[0] if tail else b""] = replacement
        for name, descendants in groups.items():
            if b"" in descendants:
                require(len(descendants) == 1, "Replacement includes ancestor and descendant")
                result[name] = descendants[b""]
            else:
                old = current.get(name)
                require(old is None or old[0] == b"40000", "Changed-path ancestor not a tree")
                child = compose(old[1] if old else None, descendants, prefix + name + b"/")
                result[name] = (b"40000", child)
        for name in current.keys() - groups.keys():
            require(result[name] == current[name], "Untouched sibling identity not conserved")
            mode, sha = current[name]
            preserved_siblings.append({"path": (prefix + name).decode(), "raw_mode": mode.decode(), "sha": sha})
        raw = encode_tree(result)
        sha = oid("tree", raw)
        rewritten_directories.append({"directory": prefix.decode().rstrip("/"),
                                      "before": base, "independent_expected_after": sha})
        require(database.get(sha) == ("tree", raw), "Candidate raw tree differs from independent composition")
        return sha

    author_kind, author_raw = database.get(AUTHOR)
    require(author_kind == "commit", "Author object is not commit")
    author_root = author_raw.split(b"\n", 1)[0].split()[1].decode()
    author_paths = walk(author_root)
    require(author_paths[TARGET] == (b"40000", proposal["target_subtree"]), "Actual author target subtree differs")
    author_target = {p: v for p, v in author_paths.items() if p.startswith(TARGET + b"/") and v[0] != b"40000"}
    require(len(author_target) == len(manifest) == 61, "Independent author61 census differs")
    bound = {e["path"].encode(): e for e in manifest}
    require(set(bound) == set(author_target), "Full logical61 path set differs")
    for path, (mode, sha) in author_target.items():
        e = bound[path]
        kind, body = database.get(sha)
        require(kind == "blob" and mode == b"100644" and e["mode"] == "100644" and e["sha"] == sha
                and e["bytes"] == len(body) and e["sha256"] == hashlib.sha256(body).hexdigest(),
                "Independent full author body/mode mismatch: " + path.decode())
    main_kind, main_raw = database.get(proposal["main"])
    require(main_kind == "commit", "MAIN object is not commit")
    main_root = main_raw.split(b"\n", 1)[0].split()[1].decode()
    require(main_root == proposal["before_tree"], "Explicit MAIN root differs")
    main_paths = walk(main_root)
    qmode, qsha = main_paths[QUEUE]
    qkind, old_queue = database.get(qsha)
    require(qkind == "blob" and qsha == proposal["queue_before_blob"], "MAIN QUEUE identity differs")
    old_lines = old_queue.splitlines(keepends=True)
    target_indices = [i for i, line in enumerate(old_lines)
                      if len(line.split(b"|")) > 3
                      and line.split(b"|")[2].strip() == b"30005468 / OWR-12697710-015"]
    require(len(target_indices) == 1, "Exact row occurrence differs")
    index = target_indices[0]
    _, author_queue = database.get(author_paths[QUEUE][1])
    row = [line for line in author_queue.splitlines(keepends=True)
           if len(line.split(b"|")) > 3
           and line.split(b"|")[2].strip() == b"30005468 / OWR-12697710-015"]
    require(len(row) == 1 and row[0] == proposal["queue_accepted_row"].encode(), "Actual accepted author row differs")
    expected_lines = list(old_lines)
    expected_lines[index] = row[0]
    expected_queue = b"".join(expected_lines)
    queue_kind, actual_queue = database.get(proposal["queue_after_blob"])
    require(queue_kind == "blob" and expected_queue == actual_queue, "Full QUEUE non-target bytes differ")
    changes = {TARGET: author_paths[TARGET], QUEUE: (qmode, oid("blob", expected_queue))}
    expected_root = compose(main_root, changes)
    require(expected_root == proposal["candidate_tree"], "Independent raw Merkle root differs from private index")
    candidate_paths = walk(expected_root)
    main_leaves = {p: e for p, e in main_paths.items() if e[0] != b"40000"}
    candidate_leaves = {p: e for p, e in candidate_paths.items() if e[0] != b"40000"}
    expected_leaves = dict(main_leaves)
    expected_leaves.update(author_target)
    expected_leaves[QUEUE] = changes[QUEUE]
    require(candidate_leaves == expected_leaves, "Complete candidate leaf census/modes/OIDs differ")
    changed = sorted(p for p in main_leaves.keys() | candidate_leaves.keys()
                     if main_leaves.get(p) != candidate_leaves.get(p))
    require(set(changed) <= set(author_target) | {QUEUE}, "Unselected MAIN path changed")
    commit_kind, commit_raw = database.get(proposal["candidate_commit"])
    require(commit_kind == "commit" and commit_raw == (directory / "commit.raw").read_bytes(), "Draft raw commit differs")
    headers = commit_raw.split(b"\n\n", 1)[0].splitlines()
    parents = [h.split()[1].decode() for h in headers if h.startswith(b"parent ")]
    require(parents == [AUTHOR, proposal["main"]] == proposal["ordered_parents"], "Ordered parents differ")
    require(headers[0] == b"tree " + expected_root.encode(), "Draft commit root differs")
    commit_payload = json.loads((directory / "COMMIT_PAYLOAD.json").read_bytes())
    require(commit_payload["parents"] == parents and commit_payload["tree"] == expected_root,
            "Provider commit payload tree/parents differ")
    actor_headers = []
    for role in ("author", "committer"):
        actor = commit_payload[role]
        timestamp = datetime.datetime.strptime(actor["date"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
        require(actor == {"name": "Alec Kriebel", "email": "me@aleckriebel.com", "date": proposal["date"]},
                "Provider commit actor identity/date differs")
        actor_headers.append((role + " " + actor["name"] + " <" + actor["email"] + "> " +
                              str(int(timestamp.timestamp())) + " +0000").encode())
    payload_raw = (b"tree " + expected_root.encode() + b"\n" +
                   b"".join(b"parent " + parent.encode() + b"\n" for parent in parents) +
                   b"\n".join(actor_headers) + b"\n\n" + commit_payload["message"].encode())
    require(payload_raw == commit_raw, "Entire provider commit payload does not reproduce raw draft commit")
    payload = json.loads((directory / "TREE_PAYLOAD.json").read_bytes())
    require(payload == {"base_tree": main_root, "tree": [
        {"path": TARGET.decode(), "mode": "040000", "type": "tree", "sha": author_paths[TARGET][1]},
        {"path": QUEUE.decode(), "mode": qmode.decode(), "type": "blob", "content": expected_queue.decode()}]},
        "Compact provider tree payload differs from exact composition")
    cas_payload = json.loads((directory / "CAS_PAYLOAD.json").read_bytes())
    require(cas_payload["query"] == "mutation PR278ScopedCAS($input:UpdateRefsInput!){updateRefs(input:$input){clientMutationId}}",
            "Provider CAS query differs")
    cas = cas_payload["variables"]["input"]
    require(cas["repositoryId"] == "R_kgDOTfIvPw" and cas["clientMutationId"] == "pr278-scoped-" + proposal["candidate_commit"],
            "Provider CAS repository/client identity differs")
    require(cas["refUpdates"] == [{"name": "refs/heads/dot/math-30005468", "beforeOid": AUTHOR,
                                   "afterOid": proposal["candidate_commit"], "force": False}],
            "CAS is not exact old-author nonforce branch-only update")
    database.close()
    report = {
        "schema": "pr278-independent-raw-merkle-scope-proof-v1",
        "UTC": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
        "main": proposal["main"], "candidate_tree": expected_root,
        "candidate_commit": proposal["candidate_commit"], "ordered_parents": parents,
        "verified": True, "provider_mutations": 0,
        "mechanism": "Raw tree parser/canonical serializer recursively replaces two paths without importing index builder; independently walks complete MAIN/candidate leaves and hashes61 full author logical bodies.",
        "complete_MAIN_leaf_count": len(main_leaves), "complete_candidate_leaf_count": len(candidate_leaves),
        "author_target_leaves": 61, "author_distinct_blob_objects": len({e[1] for e in author_target.values()}),
        "changed_paths": [p.decode() for p in changed], "changed_path_count": len(changed),
        "preserved_nonselected_MAIN_leaves": len(main_leaves.keys() - set(author_target) - {QUEUE}),
        "preserved_MAIN_symlinks": sum(v[0] == b"120000" for p, v in main_leaves.items() if p not in changes),
        "preserved_MAIN_gitlinks": sum(v[0] == b"160000" for p, v in main_leaves.items() if p not in changes),
        "QUEUE_total_rows": len(old_lines), "QUEUE_only_changed_row": index + 1,
        "all_other_QUEUE_bytes_identical": True,
        "rewritten_ancestor_directories": rewritten_directories,
        "preserved_whole_Merkle_sibling_count": len(preserved_siblings),
        "preserved_whole_Merkle_siblings": preserved_siblings,
        "raw_objects_consumed": len(database.cache),
        "limitations": ["Preparation snapshot only; not proof of future MAIN identity or provider mutation/readback.",
                        "Host/runtime and Git SHA1 object integrity assumptions apply; no hermetic custody claim.",
                        "Atomic author beforeOid CAS alone does not guard independently advancing MAIN."],
    }
    (directory / "INDEPENDENT_SCOPE_PROOF.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ["verified", "candidate_tree", "complete_MAIN_leaf_count",
                                           "complete_candidate_leaf_count", "changed_path_count",
                                           "preserved_nonselected_MAIN_leaves", "preserved_whole_Merkle_sibling_count",
                                           "all_other_QUEUE_bytes_identical"]}, indent=2))


if __name__ == "__main__":
    main()

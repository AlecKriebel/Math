#!/usr/bin/env python3
"""Private research-checkpoint preparation. This program cannot execute provider writes."""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess

ROOT = Path(__file__).resolve().parent
WORKSPACE = Path("/Users/alec/Documents/Math")
PROGRAM = "draft_pr_descending_audit_20261002"
DRIVER = ROOT / "driver.git"
OBJECTS = ROOT / "private_objects"
ALTERNATES = [ROOT.parent / "reconciliation/private_objects", ROOT.parent / "objects.git/objects"]
ACTOR = {"name": "Alec Kriebel", "email": "me@aleckriebel.com"}
CAS_QUERY = "mutation ScopedResearchCheckpoint($input:UpdateRefsInput!){updateRefs(input:$input){clientMutationId}}"
TEXT_SUFFIXES = {".md", ".json", ".py", ".txt", ".tsv", ".csv", ".tex"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def git_oid(kind, data):
    return hashlib.sha1(kind.encode() + b" " + str(len(data)).encode() + b"\0" + data).hexdigest()


def file_pin(path):
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def load_json_no_duplicates(path):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "Duplicate JSON key " + key)
            result[key] = value
        return result
    return json.loads(path.read_bytes(), object_pairs_hook=pairs)


def path_is_allowed(path):
    require(type(path) is str and path != "", "Selection path must be nonempty text")
    parts = PurePosixPath(path).parts
    require(not path.startswith("/") and PurePosixPath(path).as_posix() == path
            and len(parts) > 1 and parts[0] == PROGRAM
            and all(p not in (".", "..", "") for p in parts)
            and not any(c in path for c in ("\0", "\n", "\r", "\\")),
            "Unknown/outside/noncanonical program path: " + path)
    lowered = [p.lower() for p in parts]
    private = {"private", "private_objects", "__pycache__", "node_modules", "skills", ".agents", ".codex",
               "source_pdfs", "source_pdf", "third_party", "third-party", "thirdparty", "import_records"}
    require(not any(p in private or p.endswith(".git") for p in lowered), "Excluded private/generated/import path: " + path)
    name = lowered[-1]
    require(not name.endswith((".index", ".lock", ".pdf", ".png", ".jpg", ".zip", ".xlsx", ".xls"))
            and name != "skill.md" and "full_workbook" not in name and "workbook_metadata" not in name
            and "thirdparty" not in name and "third_party" not in name and "import_record" not in name
            and PurePosixPath(path).suffix.lower() in TEXT_SUFFIXES,
            "Excluded non-authored/binary/private selection: " + path)
    return WORKSPACE / path


def regular_source(path):
    require(path.is_absolute() and path.is_relative_to(WORKSPACE), "Source outside workspace")
    require(path.resolve() == path, "Noncanonical/symlink source path")
    current = WORKSPACE
    require(not current.is_symlink(), "Workspace is symlink")
    for component in path.relative_to(WORKSPACE).parts:
        current = current / component
        require(not current.is_symlink(), "Symlink in source path: " + str(current))
    require(path.exists() and stat.S_ISREG(path.stat().st_mode), "Removed/nonregular source: " + str(path))


def sources_from_manifest(allowlist_path, manifest_path):
    regular_source(allowlist_path)
    regular_source(manifest_path)
    require(allowlist_path.is_relative_to(WORKSPACE / PROGRAM)
            and manifest_path.is_relative_to(WORKSPACE / PROGRAM), "Control files must be inside this program")
    allowed = load_json_no_duplicates(allowlist_path)
    manifest = load_json_no_duplicates(manifest_path)
    require(type(allowed) is dict and set(allowed) == {"allowed_paths"}
            and type(allowed["allowed_paths"]) is list, "Expected exact Root allowed_paths list")
    paths = allowed["allowed_paths"]
    require(len(paths) > 0 and all(type(p) is str for p in paths)
            and len(set(paths)) == len(paths), "Empty/duplicate/invalid allowlist")
    for path in paths:
        path_is_allowed(path)
    require(type(manifest) is dict and set(manifest) == {"files"} and type(manifest["files"]) is list,
            "Expected exact full-body manifest files list; deletion actions unsupported")
    selected = {}
    for record in manifest["files"]:
        require(type(record) is dict and set(record) == {"path", "source", "bytes", "sha256"},
                "Unknown manifest fields or removal action")
        path = record["path"]
        source = path_is_allowed(path)
        require(path in paths and path not in selected, "Unknown/duplicate selected path: " + path)
        require(type(record["source"]) is str and record["source"] == str(source), "Source/destination path mismatch")
        regular_source(source)
        body = source.read_bytes()
        require(type(record["bytes"]) is int and record["bytes"] >= 0 and record["bytes"] == len(body)
                and type(record["sha256"]) is str and re.fullmatch(r"[0-9a-f]{64}", record["sha256"])
                and hashlib.sha256(body).hexdigest() == record["sha256"], "Selected full source hash/size differs: " + path)
        text = body.decode("utf-8")
        require(b"\0" not in body, "Selected source is binary despite UTF8 decoding: " + path)
        selected[path] = {"body": body, "content": text, "git_blob": git_oid("blob", body), "source": record}
    require(set(selected) == set(paths), "Allowed and selected paths differ; missing manifest entries")
    return selected


def private_environment(output):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1", GIT_TERMINAL_PROMPT="0",
               GIT_NO_LAZY_FETCH="1",
               GIT_INDEX_FILE=str(output / "private.index"), GIT_OBJECT_DIRECTORY=str(OBJECTS),
               GIT_ALTERNATE_OBJECT_DIRECTORIES=os.pathsep.join(str(p) for p in ALTERNATES if p.exists()))
    return env


def run_git(env, *args, data=None):
    return subprocess.run(["git", "--no-replace-objects", "--git-dir", str(DRIVER), *args], input=data, env=env,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, timeout=60).stdout


def inventory(env, tree):
    result = {}
    for row in run_git(env, "ls-tree", "-r", "-z", "-t", tree).split(b"\0"):
        if row:
            identity, path = row.split(b"\t", 1)
            mode, kind, sha = identity.decode().split()
            path = path.decode("utf-8")
            require(path not in result, "Duplicate tree path")
            result[path] = {"mode": mode, "type": kind, "sha": sha}
    return result


class RawReader:
    def __init__(self, env):
        self.process = subprocess.Popen(["git", "--no-replace-objects", "--git-dir", str(DRIVER), "cat-file", "--batch"],
                                        env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.cache = {}

    def get(self, sha):
        if sha not in self.cache:
            self.process.stdin.write(sha.encode() + b"\n")
            self.process.stdin.flush()
            header = self.process.stdout.readline().split()
            require(len(header) == 3 and header[0].decode() == sha, "Missing explicit private raw object: " + sha)
            body = self.process.stdout.read(int(header[2]))
            require(self.process.stdout.read(1) == b"\n", "Raw batch framing differs")
            kind = header[1].decode()
            require(git_oid(kind, body) == sha, "Raw object identity differs")
            self.cache[sha] = kind, body
        return self.cache[sha]

    def tree(self, sha):
        kind, body = self.get(sha)
        require(kind == "tree", "Expected raw tree")
        entries = {}
        offset = 0
        while offset < len(body):
            space = body.index(b" ", offset)
            zero = body.index(b"\0", space + 1)
            mode, name = body[offset:space], body[space + 1:zero]
            require(name not in entries, "Duplicate raw tree name")
            entries[name] = mode, body[zero + 1:zero + 21].hex()
            offset = zero + 21
        require(offset == len(body) and encode_tree(entries) == body, "Raw tree serialization differs")
        return entries

    def walk(self, root, prefix=b""):
        result = {}
        for name, (mode, sha) in self.tree(root).items():
            path = prefix + name
            result[path] = mode, sha
            if mode == b"40000":
                result.update(self.walk(sha, path + b"/"))
        return result

    def close(self):
        self.process.stdin.close()
        require(self.process.wait(timeout=10) == 0, "Raw reader failed")


def encode_tree(entries):
    names = sorted(entries, key=lambda name: name + (b"/" if entries[name][0] == b"40000" else b""))
    return b"".join(entries[name][0] + b" " + name + b"\0" + bytes.fromhex(entries[name][1]) for name in names)


def census_hash(leaves):
    digest = hashlib.sha256()
    for path, (mode, sha) in sorted(leaves.items()):
        digest.update(mode + b" " + sha.encode() + b"\t" + path + b"\0")
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--main", required=True, help="Literal immutable40-hex MAIN commit; no default")
    parser.add_argument("--date", required=True, help="Literal UTC YYYY-MM-DDTHH:MM:SSZ commit timestamp")
    parser.add_argument("--allowlist", required=True, help="Root-authored exact allowed_paths JSON")
    parser.add_argument("--manifest", required=True, help="Root-authored exact full-body files JSON")
    parser.add_argument("--output", required=True, help="New direct child directory under checkpoint_resume")
    parser.add_argument("--message", required=True, help="Exact checkpoint commit message")
    args = parser.parse_args()
    require(re.fullmatch(r"[0-9a-f]{40}", args.main), "MAIN must be literal40-hex SHA")
    require(re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", args.date), "Commit date must be literal UTC seconds")
    timestamp = dt.datetime.strptime(args.date, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    require(timestamp <= dt.datetime.now(dt.timezone.utc), "Future-dated checkpoint rejected")
    require(args.message.strip() != "" and "\0" not in args.message, "Commit message must be nonempty text")
    allowlist = Path(args.allowlist).absolute()
    manifest = Path(args.manifest).absolute()
    selected = sources_from_manifest(allowlist, manifest)
    output = Path(args.output).absolute()
    require(output.parent == ROOT and output.resolve() == output and not output.exists(), "Output must be new own nonsymlink child")
    output.mkdir()
    require(not OBJECTS.is_symlink() and OBJECTS.resolve() == OBJECTS
            and not DRIVER.is_symlink() and DRIVER.resolve() == DRIVER, "Private metadata paths must not be symlinks")
    OBJECTS.mkdir(exist_ok=True)
    env = private_environment(output)
    if not DRIVER.exists():
        subprocess.run(["git", "--no-replace-objects", "init", "--bare", "--initial-branch=main", str(DRIVER)], env=env,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, timeout=45)
    remote = subprocess.run(["git", "--no-replace-objects", "--git-dir", str(DRIVER), "config", "--local", "--get-regexp", "^remote\\."],
                            env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
    require(remote.returncode == 1 and remote.stdout == b"", "Private driver must have no remote configuration")
    require(run_git(env, "cat-file", "-t", args.main).decode().strip() == "commit", "Explicit MAIN object must be commit")
    before_tree = run_git(env, "rev-parse", args.main + "^{tree}").decode().strip()
    before = inventory(env, args.main)
    leaves = {p: e for p, e in before.items() if e["type"] != "tree"}
    nonempty = set()
    for path in leaves:
        components = path.split("/")
        nonempty.update("/".join(components[:i]) for i in range(1, len(components)))
    require(all(path in nonempty for path, e in before.items() if e["type"] == "tree"), "MAIN empty trees cannot be preserved by index; stop")
    for path in selected:
        if path in before:
            require(before[path]["mode"] == "100644" and before[path]["type"] == "blob", "Selected existing target is not100644 regular blob: " + path)
        components = path.split("/")
        require(all("/".join(components[:i]) not in before or before["/".join(components[:i])]["type"] == "tree"
                    for i in range(1, len(components))), "Selected ancestor collides with MAIN leaf: " + path)
    run_git(env, "read-tree", "--empty")
    index_rows = b"".join((e["mode"] + " " + e["sha"] + "\t" + p).encode() + b"\0" for p, e in sorted(leaves.items()))
    run_git(env, "update-index", "--info-only", "-z", "--index-info", data=index_rows)
    for record in selected.values():
        require(run_git(env, "hash-object", "-w", "--stdin", data=record["body"]).decode().strip() == record["git_blob"], "Selected private blob hash differs")
    updates = b"".join(("100644 " + record["git_blob"] + "\t" + path).encode() + b"\0" for path, record in sorted(selected.items()))
    run_git(env, "update-index", "-z", "--index-info", data=updates)
    tree = run_git(env, "write-tree", "--missing-ok").decode().strip()
    after = inventory(env, tree)
    expected_leaves = dict(leaves)
    expected_leaves.update({p: {"mode": "100644", "type": "blob", "sha": e["git_blob"]} for p, e in selected.items()})
    require({p: e for p, e in after.items() if e["type"] != "tree"} == expected_leaves, "Whole MAIN/candidate leaf conservation differs")
    raw = RawReader(env)
    main_kind, main_body = raw.get(args.main)
    require(main_kind == "commit", "Literal MAIN raw object must be commit")
    first_header = main_body.split(b"\n", 1)[0]
    require(re.fullmatch(rb"tree [0-9a-f]{40}", first_header)
            and first_header == b"tree " + before_tree.encode(), "Literal MAIN raw first tree header differs from baseline")
    before_raw = raw.walk(before_tree)
    after_raw = raw.walk(tree)
    raw_leaves = {p: e for p, e in before_raw.items() if e[0] != b"40000"}
    expected_raw_leaves = dict(raw_leaves)
    expected_raw_leaves.update({p.encode(): (b"100644", e["git_blob"]) for p, e in selected.items()})
    require({p: e for p, e in after_raw.items() if e[0] != b"40000"} == expected_raw_leaves, "Independent whole raw leaf/path/mode/OID comparison differs")
    rewritten, siblings = [], []

    def compose(base, edits, prefix=b""):
        old = raw.tree(base) if base else {}
        new = dict(old)
        grouped = {}
        for path, entry in edits.items():
            head, *tail = path.split(b"/", 1)
            grouped.setdefault(head, {})[tail[0] if tail else b""] = entry
        for name, edits_below in grouped.items():
            if b"" in edits_below:
                require(len(edits_below) == 1, "Selected path contains another selected path")
                new[name] = edits_below[b""]
            else:
                prior = old.get(name)
                require(prior is None or prior[0] == b"40000", "Raw selected ancestor is not tree")
                new[name] = (b"40000", compose(prior[1] if prior else None, edits_below, prefix + name + b"/"))
        for name in old.keys() - grouped.keys():
            require(new[name] == old[name], "Whole sibling identity changed")
            siblings.append((prefix + name, old[name]))
        body = encode_tree(new)
        expected = git_oid("tree", body)
        require(raw.get(expected) == ("tree", body), "Independent raw composition differs from private index")
        rewritten.append({"directory": prefix.decode().rstrip("/"), "before": base, "after": expected})
        return expected

    expected_tree = compose(before_tree, {p.encode(): (b"100644", e["git_blob"]) for p, e in selected.items()})
    require(expected_tree == tree, "Independently computed root differs")
    actor = dict(ACTOR, date=args.date)
    message = args.message if args.message.endswith("\n") else args.message + "\n"
    commit_payload = {"tree": tree, "parents": [args.main], "message": message, "author": actor, "committer": actor}
    person = ACTOR["name"] + " <" + ACTOR["email"] + "> " + str(int(timestamp.timestamp())) + " +0000"
    commit_raw = ("tree " + tree + "\nparent " + args.main + "\nauthor " + person + "\ncommitter " + person + "\n\n" + message).encode()
    commit = git_oid("commit", commit_raw)
    require(run_git(env, "hash-object", "-t", "commit", "-w", "--stdin", data=commit_raw).decode().strip() == commit
            and raw.get(commit) == ("commit", commit_raw), "Private and independent raw commit identities differ")
    raw.close()
    tree_payload = {"base_tree": before_tree, "tree": [{"path": p, "mode": "100644", "type": "blob", "content": e["content"]} for p, e in sorted(selected.items())]}
    cas_payload = {"query": CAS_QUERY, "variables": {"input": {"repositoryId": "R_kgDOTfIvPw",
                   "refUpdates": [{"name": "refs/heads/main", "beforeOid": args.main, "afterOid": commit, "force": False}]}}}
    unselected = {p: e for p, e in raw_leaves.items() if p.decode() not in selected}
    changed = sorted(p for p in set(leaves) | set(expected_leaves) if leaves.get(p) != expected_leaves.get(p))
    proof = {"schema": "scoped-research-checkpoint-proof-v1", "preparation_only": True, "provider_mutations": 0,
             "UTC": dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z"), "main": args.main,
             "before_tree": before_tree, "candidate_tree": tree, "candidate_commit": commit, "parents": [args.main],
             "allowlist": file_pin(allowlist), "manifest": file_pin(manifest), "helper": file_pin(Path(__file__).resolve()),
             "selected_bodies": [dict(e["source"], mode="100644", git_blob=e["git_blob"]) for p, e in sorted(selected.items())],
             "selected_count": len(selected), "changed_paths": changed, "MAIN_leaves": len(leaves), "candidate_leaves": len(expected_leaves),
             "unselected_conserved_count": len(unselected), "unselected_full_mode_path_oid_sha256": census_hash(unselected),
             "preserved_whole_Merkle_siblings": len(siblings), "preserved_sibling_census_sha256": census_hash(dict(siblings)),
             "rewritten_ancestors": rewritten, "independent_raw_tree_commit_checks": True, "no_deletions": True,
             "remaining_gap": "Root's actual provider merge/readback, explicit final selection and fresh MAIN conservation; later provider object creation/CAS and actual readback require Root execution. No action is performed by this helper."}
    for name, value in [("TREE_PAYLOAD.json", tree_payload), ("COMMIT_PAYLOAD.json", commit_payload), ("CAS_PAYLOAD.json", cas_payload), ("PROOF.json", proof)]:
        (output / name).write_text(json.dumps(value, indent=2) + "\n")
    (output / "commit.raw").write_bytes(commit_raw)
    print(json.dumps({k: proof[k] for k in ("main", "candidate_tree", "candidate_commit", "selected_count", "changed_paths", "unselected_conserved_count")}, indent=2))


if __name__ == "__main__":
    main()

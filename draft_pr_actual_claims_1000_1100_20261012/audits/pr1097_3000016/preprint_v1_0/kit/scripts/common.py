"""Portable integrity and pre-write guards; no network or third-party modules."""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import os
from pathlib import Path
import stat

KIT = Path(__file__).absolute().parent.parent
ARCHIVE_NAME = "pr1097_support_v1_0.zip"

def require(condition, message):
    if not condition:
        raise ValueError(message)

def lexical(path):
    p = Path(path).expanduser()
    require(".." not in p.parts, "parent traversals are not accepted")
    return p.absolute()

def no_links(path, leaf_required=True, directory=False):
    p = lexical(path)
    parts = list(reversed([p] + list(p.parents)))
    for q in parts:
        try:
            s = q.lstat()
        except FileNotFoundError:
            require(q == p and not leaf_required, "missing ancestor/input: " + str(q))
            continue
        require(not stat.S_ISLNK(s.st_mode), "symlink component: " + str(q))
        if q != p or directory:
            require(stat.S_ISDIR(s.st_mode), "non-directory ancestor: " + str(q))
        else:
            require(stat.S_ISREG(s.st_mode), "input must be regular: " + str(q))
    return p

def read_json(path):
    p = no_links(path)
    with p.open("rb") as stream:
        value = json.load(stream)
    require(isinstance(value, dict), "JSON object required: " + str(p))
    return value

def sha(path):
    h = hashlib.sha256()
    with no_links(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1048576), b""):
            h.update(block)
    return h.hexdigest()

def record(path):
    p = no_links(path)
    return {"bytes": p.stat().st_size, "sha256": sha(p)}

def inside(path, root):
    return path == root or root in path.parents

def fresh_output(path, is_directory=False):
    """Reject existing leaves (including hardlinks) and every linked ancestor.

    A file's parent must already exist. A directory is allocated as a new leaf.
    Canonical package/original audit roots remain protected even after extraction.
    Existing directory identities also exclude filesystem case/normalization aliases.
    No subprocess or writer runs until this preflight has succeeded. This is not
    a guarantee against hostile concurrent changes to filesystem components.
    """
    p = lexical(path)
    no_links(p.parent, directory=True)
    require(not os.path.lexists(p), "output must be a fresh nonexistent path")
    config = read_json(KIT / "PROTECTED_PATHS.json")
    roots = [KIT] + [lexical(v) for v in config["original_protected_roots"]]
    protected_identities = set()
    for root in roots:
        require(not inside(p, root), "output inside protected tree: " + str(root))
        try:
            root_stat = root.stat()
        except FileNotFoundError:
            # Original paths need not exist on another machine or after extraction.
            continue
        protected_identities.add((root_stat.st_dev, root_stat.st_ino))
    for ancestor in p.parents:
        ancestor_stat = ancestor.stat()  # no_links has already required real directories.
        require((ancestor_stat.st_dev, ancestor_stat.st_ino) not in protected_identities,
                "output ancestor aliases a protected root: " + str(ancestor))
    if is_directory:
        os.mkdir(p, 0o700)
        return p
    # Returning an exclusively opened descriptor prevents leaf-alias replacement.
    fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600)
    return os.fdopen(fd, "wb")

def inventory():
    # Bootstrap validation happens before parsing the self-excluded manifest.
    manifest = read_json(KIT / "MANIFEST.json")
    require(set(manifest) == {"schema", "scope", "entries"}, "unexpected manifest keys")
    require(manifest["schema"] == 1, "unsupported manifest schema")
    entries = manifest["entries"]
    require(isinstance(entries, list) and entries, "nonempty inventory required")
    names = []
    for row in entries:
        require(set(row) == {"path", "bytes", "sha256"}, "unexpected inventory row")
        name = row["path"]
        require(isinstance(name, str) and name and "\\" not in name, "bad inventory path")
        rel = Path(name)
        require(not rel.is_absolute() and ".." not in rel.parts and rel.as_posix() == name,
                "noncanonical inventory path")
        require(name != "MANIFEST.json", "manifest may not hash itself")
        names.append(name)
        require(record(KIT / rel) == {"bytes": row["bytes"], "sha256": row["sha256"]},
                "payload mismatch: " + name)
    require(names == sorted(set(names)), "inventory must be sorted and unique")
    actual = []
    for parent, dirs, files in os.walk(KIT, followlinks=False):
        for name in dirs:
            no_links(Path(parent) / name, directory=True)
        for name in files:
            p = no_links(Path(parent) / name)
            actual.append(p.relative_to(KIT).as_posix())
    require(sorted(actual) == sorted(names + ["MANIFEST.json"]), "extra/missing package files")
    metadata = read_json(KIT / "metadata.json")
    require(read_json(KIT / "zenodo-metadata.json") == {"metadata": metadata}, "metadata wrapper mismatch")
    custody = read_json(KIT / "provenance" / "CUSTODY.json")
    pins = read_json(KIT / "provenance" / "INPUT_PINS.json")
    baseline = {r["path"]: r for r in pins["entries"]}
    require(len(baseline) == len(pins["entries"]), "duplicate original pins")
    require(set(baseline) == {r["original_path"] for r in custody["entries"]}, "incomplete custody decisions")
    copies = 0
    for row in custody["entries"]:
        before = baseline[row["original_path"]]
        require(row["bytes"] == before["bytes"] and row["sha256"] == before["sha256"], "custody pin mismatch")
        if row["decision"] == "EXACT_AUTHORED_COPY":
            require(record(KIT / row["copy_path"]) == {"bytes": row["bytes"], "sha256": row["sha256"]}, "authored copy mismatch")
            copies += 1
        else:
            require(row["decision"] == "EXCLUDED" and row.get("reason"), "unexplained exclusion")
    return {"metadata": metadata, "payloads": len(names), "copies": copies,
            "baseline_files": len(baseline), "manifest_sha256": sha(KIT / "MANIFEST.json")}

def binding_check(path=None, required=False):
    p = lexical(path) if path is not None else KIT.parent / "DEPOSIT_BINDING.json"
    # lexists deliberately sees broken symlinks, which must fail regular preflight.
    if not os.path.lexists(p):
        require(not required and path is None, "required/passed binding is missing")
        return {"state": "ABSENT_OPTIONAL", "required": False}
    value = read_json(p)
    require(set(value) == {"schema", "metadata", "kit_manifest_sha256", "files", "native_manifest"}, "bad binding schema")
    require(value["schema"] == 1, "bad binding version")
    metadata = read_json(KIT / "metadata.json")
    require(value["metadata"] == metadata, "bound metadata mismatch")
    require(value["kit_manifest_sha256"] == sha(KIT / "MANIFEST.json"), "bound kit mismatch")
    expected = ["paper.pdf", ARCHIVE_NAME]
    require([r["name"] for r in value["files"]] == expected, "bound asset names/order mismatch")
    for row in value["files"]:
        require(set(row) == {"name", "bytes", "sha256"}, "bad bound asset record")
        require(record(p.parent / row["name"]) == {"bytes": row["bytes"], "sha256": row["sha256"]}, "bound asset mismatch")
    require(value["native_manifest"] == "zenodo-deposit.json", "unexpected native manifest path")
    native = read_json(p.parent / value["native_manifest"])
    require(native == {"metadata": metadata, "files": [{"path": n, "name": n} for n in expected]}, "native uploader manifest mismatch")
    require(read_json(p.parent / ".zenodo.json") == metadata, "external bare metadata mismatch")
    require(read_json(p.parent / "zenodo-metadata.json") == {"metadata": metadata}, "external metadata wrapper mismatch")
    return {"state": "PRESENT_VERIFIED", "required": required, "sha256": sha(p)}

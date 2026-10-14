"""Shared static-file guards; no concurrency or hostile-race security claim."""
from pathlib import Path, PurePosixPath
import hashlib, json, os, stat
ROOT = Path(__file__).resolve().parent
ARCHIVE = "pr1085_support_v1_0.zip"
FIXED_TIME = (2026, 10, 14, 0, 0, 0)
EPOCH = "1791936000"

def require(ok, message):
    if not ok:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def regular(path):
    path = Path(path).absolute()
    for part in [path, *path.parents]:
        require(not part.is_symlink(), "symlink input or ancestor: " + str(path))
    require(path.is_file() and stat.S_ISREG(path.stat().st_mode),
            "regular input required: " + str(path))
    return path

def json_bytes(data):
    def pairs(items):
        out = {}
        for key, val in items:
            require(key not in out, "duplicate JSON key: " + key)
            out[key] = val
        return out
    return json.loads(data.decode("utf-8"), object_pairs_hook=pairs)

def read_json(path):
    return json_bytes(regular(path).read_bytes())

def members():
    # Bootstrap and every allowlisted member are regular before JSON ingestion.
    regular(ROOT / "PAYLOAD_MEMBERS.txt")
    rows = (ROOT / "PAYLOAD_MEMBERS.txt").read_text().splitlines()
    require(rows == sorted(set(rows)) and bool(rows), "member list sorted unique")
    for name in rows:
        p = PurePosixPath(name)
        require(str(p) == name and not p.is_absolute() and ".." not in p.parts
                and "\\" not in name, "unsafe member name")
        regular(ROOT / name)
    regular(ROOT / "SUPPORT_MANIFEST.json")
    return rows

def protected(extra=()):
    paths = [p for p in ROOT.rglob("*") if p.is_file() or p.is_symlink()]
    # In the local audit tree preserve every pre-authoring frozen source.
    pins = ROOT / "PREPARATION_INPUT_PINS.json"
    if pins.is_file() and not pins.is_symlink():
        obj = read_json(pins)
        audit = ROOT.parent
        for row in obj["files"]:
            p = audit / row["path"]
            if p.is_file() or p.is_symlink():
                paths.append(p)
    paths.extend(Path(p) for p in extra)
    return paths

def safe_output(path, extra=()):
    """Reject direct, resolved, symlink and existing hardlink input aliases.
    Run before opening output, making directories or calling a compiler.
    The supported scope is a static local filesystem, not concurrent races.
    """
    p = Path(path).absolute()
    for part in [p, *p.parents]:
        require(not part.is_symlink(), "output symlink or ancestor")
    target = p.resolve()
    require(target != ROOT and ROOT not in target.parents,
            "output must be outside canonical kit directory")
    for source in protected(extra):
        require(target != source.resolve(), "output aliases protected input")
        if p.exists() and source.exists():
            require(not os.path.samefile(p, source), "output hardlinks protected input")
    return p

def emit(obj, output=None, extra=()):
    data = json.dumps(obj, indent=2, sort_keys=True) + "\n"
    if output:
        p = safe_output(output, extra)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(data)
    print(data, end="")

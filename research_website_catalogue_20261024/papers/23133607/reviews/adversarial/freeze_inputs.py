"""Opaque source/core custody only; no scientific body is displayed or run."""
from pathlib import Path
import datetime
import hashlib
import json
import stat

E = Path(__file__).resolve().parent
S = E.parents[1] / "sources"
if (E / ".gitignore").read_text() != "inputs/\nrasters/\nprimary/\n":
    raise RuntimeError("Private-input ignore must preexist raw creation")
core = json.loads((E / "QUALIFIED_CORE_PATHS.json").read_text())
if len(core) != 18:
    raise RuntimeError("Qualified18 core paths required")
files, dirs = [], []
for p in sorted(S.rglob("*")):
    if p.is_symlink():
        raise RuntimeError("Source symlink")
    mode = p.lstat().st_mode
    if stat.S_ISREG(mode): files.append(p)
    elif stat.S_ISDIR(mode): dirs.append(p.relative_to(S).as_posix())
    else: raise RuntimeError("Nonordinary source namespace entry")
if len(files) != 97 or len(dirs) != 9:
    raise RuntimeError("Complete original source97/9 required")
blobs = E / "inputs/blobs"
blobs.mkdir(parents=True, exist_ok=False)
rows = []
for p in files + [Path(n) for n in core]:
    if p.is_symlink() or not stat.S_ISREG(p.lstat().st_mode):
        raise RuntimeError("Nonordinary protected file")
    b = p.read_bytes()
    h = hashlib.sha256(b).hexdigest()
    f = blobs / h
    if f.exists() and f.read_bytes() != b:
        raise RuntimeError("Blob collision")
    f.write_bytes(b)
    rows.append({"path": str(p), "copy": str(f.relative_to(E)), "bytes": len(b), "SHA256": h})
obj = {"UTC": datetime.datetime.now(datetime.timezone.utc).isoformat(), "files": rows,
       "source_namespace": {"path": str(S), "files": [p.relative_to(S).as_posix() for p in files], "directories": dirs},
       "core_files": core, "core_qualification": "17original plus sole separately root-authorized405b checkpoint helper",
       "opaque_copy_only_no_scientific_code_results_or_opinion_exposure": True,
       "raw_inputs_ignored_before_creation": True, "source_programmes_executed": []}
(E / "PROTECTED_INPUTS.json").write_text(json.dumps(obj, indent=2) + "\n")
print(json.dumps({"source_files": len(files), "source_directories": len(dirs), "protected_paths": len(rows)}))

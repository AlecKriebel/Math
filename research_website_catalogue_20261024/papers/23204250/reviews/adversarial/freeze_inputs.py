"""Own opaque custody intake only; no scientific body is displayed or run."""
from pathlib import Path
import datetime
import hashlib
import json
import stat

E = Path(__file__).resolve().parent
S = E.parents[1] / "sources"
require_ignore = (E / ".gitignore").read_text()
if require_ignore != "inputs/\nrasters/\nprimary/\n":
    raise RuntimeError("Private-input ignore must preexist creation")
core = json.loads((E / "QUALIFIED_CORE_PATHS.json").read_text())
if len(core) != 18:
    raise RuntimeError("Qualified core18 paths required")
files, directories = [], []
for p in sorted(S.rglob("*")):
    if p.is_symlink():
        raise RuntimeError("Source symlink")
    mode = p.lstat().st_mode
    if stat.S_ISREG(mode):
        files.append(p)
    elif stat.S_ISDIR(mode):
        directories.append(p.relative_to(S).as_posix())
    else:
        raise RuntimeError("Nonordinary source entry")
if len(files) != 104 or len(directories) != 13:
    raise RuntimeError("Expected actual complete source104/13")
blobdir = E / "inputs/blobs"
blobdir.mkdir(parents=True, exist_ok=False)
rows = []
for p in files + [Path(n) for n in core]:
    if p.is_symlink() or not stat.S_ISREG(p.lstat().st_mode):
        raise RuntimeError("Nonordinary protected input")
    b = p.read_bytes()
    h = hashlib.sha256(b).hexdigest()
    out = blobdir / h
    if out.exists() and out.read_bytes() != b:
        raise RuntimeError("Blob collision")
    out.write_bytes(b)
    rows.append({"path": str(p), "copy": str(out.relative_to(E)), "bytes": len(b), "SHA256": h})
obj = {"UTC": datetime.datetime.now(datetime.timezone.utc).isoformat(), "files": rows,
       "source_namespace": {"path": str(S), "files": [p.relative_to(S).as_posix() for p in files], "directories": directories},
       "core_files": core, "core_qualification": "17original plus sole separately root-authorized405b checkpoint helper",
       "opaque_copy_only_no_scientific_code_results_or_opinion_exposure": True,
       "raw_inputs_ignored_before_creation": True, "source_programmes_executed": []}
(E / "PROTECTED_INPUTS.json").write_text(json.dumps(obj, indent=2) + "\n")
print(json.dumps({"source_files": len(files), "source_directories": len(directories), "protected_paths": len(rows)}))

"""Root offline comparisons only; no science, project imports, subprocess, network or writes."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import stat

R = Path(__file__).resolve().parent
A = R.parent / "adversarial"
C = R.parent / "scope"
S = R.parent.parent / "sources"
checks = 0
typed_nodes = 0

def need(ok, label):
    global checks
    checks += 1
    if not ok:
        raise ValueError(label)

def raw(path):
    need(path.is_file() and not path.is_symlink(), "ordinary regular file")
    return path.read_bytes()

def obj(path):
    return json.loads(raw(path))

def same(a, b):
    global typed_nodes
    typed_nodes += 1
    need(type(a) is type(b), "exact scalar/container type")
    if isinstance(a, dict):
        need(list(a) == list(b), "whole ordered object keys")
        for key in a:
            same(a[key], b[key])
    elif isinstance(a, list):
        need(len(a) == len(b), "whole ordered array length")
        for left, right in zip(a, b):
            same(left, right)
    else:
        need(a == b, "exact scalar or null")

def extent(root, wanted_files, wanted_dirs):
    need(root.resolve() == root and root.is_dir() and not root.is_symlink(), "ordinary namespace root")
    files, dirs = [], []
    for path in root.rglob("*"):
        mode = path.lstat().st_mode
        need(not stat.S_ISLNK(mode), "no namespace symlink")
        if stat.S_ISREG(mode):
            files.append(path.relative_to(root).as_posix())
        elif stat.S_ISDIR(mode):
            dirs.append(path.relative_to(root).as_posix())
        else:
            raise ValueError("special namespace entry")
    need(sorted(files) == sorted(wanted_files), "exact complete file namespace")
    need(sorted(dirs) == sorted(wanted_dirs), "exact complete directory namespace")
    return {"files": len(files), "directories": len(dirs)}

def pinned(path, row):
    body = raw(path)
    need(len(body) == row["bytes"], "whole byte length")
    need(hashlib.sha256(body).hexdigest() == row["SHA256"], "whole SHA256")
    return body

source = obj(A / "INPUT_MANIFEST.json")
source_extent = extent(S, [row["relative"] for row in source["files"]], source["exact_relative_directories"])
need(source_extent["files"] == 291, "original291 source files")
for row in source["files"]:
    need(Path(row["path"]).is_relative_to(S), "bounded source path")
    pinned(Path(row["path"]), row)

scope = obj(C / "FINAL_MANIFEST.json")
terminals = ["FINAL_MANIFEST.json", "FINAL_CLOSURE.json", "FINAL_SEAL.json"]
need(sorted(scope["excluded_terminal_files"]) == sorted(terminals), "only exact scope root terminals")
scope_files = [row["path"] for row in scope["files"]] + terminals
scope_dirs = sorted({parent.as_posix() for name in scope_files
                     for parent in PurePosixPath(name).parents if parent.as_posix() != "."})
scope_extent = extent(C, scope_files, scope_dirs)
for row in scope["files"]:
    pinned(C / row["path"], row)

adversarial = obj(A / "OWNED_MANIFEST.json")
adversarial_extent = extent(A, [row["path"] for row in adversarial["files"]] + ["OWNED_MANIFEST.json", "SEAL.json"],
                           adversarial["exact_relative_directories"])
for row in adversarial["files"]:
    pinned(A / row["path"], row)

ready = obj(S / "SOURCE_READY.json")
same(obj(A / "VERDICT.json")["whole_original_SOURCE_READY"], ready)
native_objects = obj(A / "NATIVE_OBJECT_READ.json")["whole_original_object_copies"]
for row in native_objects:
    copy = pinned(Path(row["copy_path"]), row)
    original = raw(Path(row["source_path"]))
    need(copy == original, "whole native object copied raw bytes")
    same(json.loads(copy), json.loads(original))

replay = obj(A / "NATIVE_REPLAY.json")
need(len(replay["runs"]) == 2, "exactly two historical native runs")
need([row["mode"] for row in replay["runs"]] == ["NORMAL", "OPTIMIZED"], "actual native mode order")
outputs = []
for row in replay["runs"]:
    actual = pinned(Path(row["whole_stdout"]["path"]), row["whole_stdout"])
    expected = pinned(Path(row["original_expected"]["path"]), row["original_expected"])
    need(actual == expected, "whole actual expected4091 output")
    same(json.loads(actual), row["original_expected"]["whole_literal_object"])
    same(json.loads(actual), json.loads(expected))
    need(pinned(Path(row["whole_stderr"]["path"]), row["whole_stderr"]) == b"", "actual empty stderr")
    need(row["exit_code"] == 0, "actual successful native exit")
    outputs.append(actual)
need(outputs[0] == outputs[1] and len(outputs[0]) == 4091, "whole normal O equality")
need(replay["source_checker_SHA256"] == hashlib.sha256(raw(S / "published-source/asset-001/audit/math_schur/schur_tensor_check.py")).hexdigest(),
     "actual fully read selected checker identity")

print(json.dumps({"status": "PASS_ROOT_OFFLINE_INTERFACES_NO_SCIENTIFIC_REPLAY",
                  "checks": checks, "typed_nodes": typed_nodes,
                  "source_extent": source_extent, "scope_extent": scope_extent,
                  "adversarial_extent": adversarial_extent,
                  "whole_native_source_JSON_objects_compared": len(native_objects),
                  "whole_original_READY_embedded_in_literal_verdict_compared": True,
                  "two_whole_actual_expected_native_outputs_bytes_each": 4091,
                  "scope_directory_omission_compensated_by_strict_current_parent_extent": True,
                  "native_or_own_science_project_imports_subprocess_network_or_writes": False}, indent=2))

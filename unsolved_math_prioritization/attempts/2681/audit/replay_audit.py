#!/usr/bin/env python3
"""Replay the source-free author package and arithmetic mutations read-only.

Usage: python3 replay_audit.py /path/to/author/package
The recorded audit used real/effective UID1000. This runner accepts any nonroot
UID and records the actual IDs. It never edits the supplied package.
"""
from pathlib import Path
import argparse
import ast
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile


MUTATIONS = [
    ("wrong_monodromy_order", '[("A2", 2, [(0, 1)], 3, 6),',
     '[("A2", 2, [(0, 1)], 3, 5),', "A2 finite order"),
    ("broken_cyclotomic_companion", "phi6, phi30 = [1, -1, 1],",
     "phi6, phi30 = [1, 1, 1],", "formal Alexander normalization"),
    ("wrong_BK_determinant", "abs(peval(q, -1)) == 4*n+5",
     "abs(peval(q, -1)) == 4*n+7", "BK determinant"),
    ("wrong_ADE_boundary", "b == 2 and c <= 4",
     "b == 2 and c <= 5", "bounded check of proved ADE classification"),
    ("wrong_FDTC_residual", "exceptions == [0, 1]",
     "exceptions == [0]", "two exceptional filling slopes"),
    ("broken_triangle_projection", "g[i][d+i] = 1",
     "g[i][d+i] = 0", "triangle exact at B"),
    ("broken_spectral_differential", "boundary[d+r+i][d+i] = 1",
     "boundary[d+r+i][d+i] = 0", "spectral model minimal terminal rank"),
    ("unprotected_permanent_cycle", "boundary[d+r+i][d+i] = 1",
     "boundary[0 if i == 0 else d+r+i][d+i] = 1", "protected cycle not boundary"),
]


def demand(test, message):
    if not test:
        raise ValueError(message)


def execute(path, cwd, flag):
    command = [sys.executable, "-I", "-B"]+([flag] if flag else [])+[str(path)]
    return subprocess.run(command, cwd=cwd, capture_output=True, timeout=120)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path)
    args = parser.parse_args()
    author = args.package.resolve()
    demand(os.getuid() != 0 and os.geteuid() != 0, "Use a real nonroot user")
    expected = (author/"verification.json").read_bytes()
    saved = json.loads(expected)
    source = (author/"verify.py").read_text()
    demand(not any(isinstance(n, ast.Assert) for n in ast.walk(ast.parse(source))), "assert validation found")
    original = {f.name:hashlib.sha256(f.read_bytes()).hexdigest()
                for f in author.iterdir() if f.is_file()}
    replays, mutations, denied = [], [], []
    with tempfile.TemporaryDirectory(prefix="double_cover_audit_") as temporary:
        root = Path(temporary)
        ro = root/"readonly"
        ro.mkdir()
        for name in ["verify.py", "verification.json"]:
            shutil.copyfile(author/name, ro/name)
            (ro/name).chmod(0o444)
        ro.chmod(0o555)
        try:
            for label, path in [("file_append",ro/"verify.py"),
                                ("directory_create",ro/"write_probe")]:
                try:
                    with path.open("ab") as stream:
                        stream.write(b"probe")
                except PermissionError:
                    denied.append(label)
                else:
                    raise ValueError("Read-only probe unexpectedly wrote: "+label)
            for flag in [None,"-O","-OO"]:
                run = execute(ro/"verify.py",ro,flag)
                demand(run.returncode == 0 and run.stdout == expected, "Replay failed: "+str(flag))
                replays.append({"mode":flag or "normal", "returncode":run.returncode,
                                "output_sha256":hashlib.sha256(run.stdout).hexdigest(),
                                "matches_saved_output":True,"stderr_bytes":len(run.stderr)})
            for label, old, new, failure in MUTATIONS:
                demand(source.count(old) == 1,"Nonunique mutation: "+label)
                file = root/(label+".py")
                file.write_text(source.replace(old,new))
                file.chmod(0o444)
                modes = []
                for flag in [None,"-O","-OO"]:
                    run = execute(file,ro,flag)
                    demand(run.returncode != 0 and failure.encode() in run.stderr,
                           "Mutation not rejected as intended: "+label+" "+str(flag))
                    modes.append({"mode":flag or "normal","returncode":run.returncode,
                                  "expected_failure":failure,"stdout_bytes":len(run.stdout)})
                mutations.append({"mutation":label,"modes":modes})
        finally:
            ro.chmod(0o755)
            for file in root.rglob("*"):
                if file.is_file():
                    file.chmod(0o644)
    demand(all(hashlib.sha256((author/name).read_bytes()).hexdigest() == digest
               for name,digest in original.items()), "Author input changed")
    output = {"result":"PASS","uid":os.getuid(),"euid":os.geteuid(),
              "python_version":sys.version.split()[0],"readonly_directory_mode":"0555",
              "readonly_file_modes":"0444","write_denied_probes":denied,
              "author_replays":replays,"positive_controls_per_replay":saved["positive_controls"],
              "internal_negative_controls_per_replay":saved["negative_controls"],
              "external_mutations":mutations,"external_mutation_runs":len(MUTATIONS)*3,
              "source_documents_required":False,"network_required":False,
              "author_checker_uses_assert":False}
    print(json.dumps(output,indent=2,sort_keys=True))


if __name__ == "__main__":
    main()

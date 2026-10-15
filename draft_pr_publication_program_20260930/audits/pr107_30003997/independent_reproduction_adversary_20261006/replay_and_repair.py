#!/usr/bin/env python3
"""Copy immutable inputs byte-exact; propose explicit gate repair in own copies."""
import datetime
import difflib
import hashlib
import json
import pathlib
from record_run import run, meta

ROOT = pathlib.Path(__file__).resolve().parent
ORIGINAL = ROOT.parent/"original_source_authentication_20261006"/"original_attempt"


def copy_originals():
    copies = {"author_replay/verify.py":ORIGINAL/"verify.py",
              "author_replay/PROOF.md":ORIGINAL/"PROOF.md",
              "author_replay/verification.json":ORIGINAL/"verification.json",
              "old_checker_replay/independent_checks.py":ORIGINAL/"review"/"independent_checks.py",
              "old_checker_replay/independent_results.json":ORIGINAL/"review"/"independent_results.json"}
    inputs=[]
    for destination, source in copies.items():
        target=ROOT/destination
        target.parent.mkdir(exist_ok=True)
        target.write_bytes(source.read_bytes())
        inputs.append({"source":meta(source),"copy":meta(target),"byte_exact":source.read_bytes()==target.read_bytes()})
    (ROOT/"FROZEN_REPLAY_COPY_MANIFEST.json").write_text(json.dumps({"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"copies":inputs},indent=2)+"\n")


def repair():
    for kind, relative in (("author","author_replay/verify.py"),("independent","old_checker_replay/independent_checks.py")):
        original=(ROOT/relative).read_text()
        if kind == "author":
            modified=original.replace(" assert b,k\n"," if not b:\n  raise AssertionError(k)\n")
            modified=modified.replace("   assert u not in seen\n","   if u in seen:\n    raise AssertionError('cycle in parent path')\n")
            filename="verify.py"
        else:
            modified=original.replace(" assert p,k\n"," if not p:\n  raise AssertionError(k)\n")
            filename="independent_checks.py"
        if modified == original or "assert " in modified:
            raise RuntimeError("repair did not replace every original assert")
        destination=ROOT/(kind+"_suggested_repair")
        destination.mkdir(exist_ok=True)
        (destination/filename).write_text(modified)
        if kind == "author":
            (destination/"PROOF.md").write_bytes((ORIGINAL/"PROOF.md").read_bytes())
        patch=''.join(difflib.unified_diff(original.splitlines(True),modified.splitlines(True),fromfile=relative,tofile=kind+"_suggested_repair/"+filename))
        (ROOT/(kind+"_suggested_repair.diff")).write_text(patch)


def execute():
    python="/opt/homebrew/bin/python3"
    receipts=[]
    runs=[("independent_initial_optimized",[python,"-O","independent_initial.py","--output","independent_initial_optimized.json"]),
          ("independent_initial_false_normal",[python,"independent_initial.py","--false-control"]),
          ("independent_initial_false_optimized",[python,"-O","independent_initial.py","--false-control"])]
    for kind, folder, filename in (("author","author_replay","verify.py"),("independent","old_checker_replay","independent_checks.py"),
                                   ("author_repaired","author_suggested_repair","verify.py"),("independent_repaired","independent_suggested_repair","independent_checks.py")):
        guard_kind="author" if kind.startswith("author") else "independent"
        for label,optimization in (("normal",[]),("optimized",["-O"])):
            script=str(ROOT/folder/filename)
            runs.append((kind+"_"+label,[python,*optimization,script]))
            runs.append((kind+"_false_"+label,[python,*optimization,"guard_probe.py",guard_kind,script]))
    for name,argv in runs:
        receipts.append(run(name,argv))
    comparison={}
    for kind, expected in (("author",ROOT/"author_replay"/"verification.json"),("independent",ROOT/"old_checker_replay"/"independent_results.json")):
        for label in ("normal","optimized"):
            actual=ROOT/"actual_runs"/(kind+"_"+label)/"stdout.bin"
            comparison[kind+"_"+label]={"actual":meta(actual),"expected":meta(expected),"byte_exact":actual.read_bytes()==expected.read_bytes()}
    (ROOT/"REPLAY_COMPARISON.json").write_text(json.dumps(comparison,indent=2)+"\n")
    (ROOT/"RUN_INDEX.json").write_text(json.dumps(receipts,indent=2)+"\n")


if __name__ == "__main__":
    copy_originals()
    repair()
    execute()

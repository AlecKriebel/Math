#!/usr/bin/env python3
"""Portable author-packet replay; external archive hash anchors authenticity.

This script verifies frozen core content, strict inventory, replay and damage
controls. It cannot defend against replacement of both this verifier and its
external trusted archive/hash. It does not certify mathematical proofs.
"""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

FROZEN = {'CONTROL_RESULTS.json': {'bytes': 1750, 'sha256': 'fc6882d30e1aea7b2f024660f104094bb88cee89f98bad66bb26316bd61c443e'}, 'LITERATURE.md': {'bytes': 3817, 'sha256': '6d5cafe0e68463dbda75a4132d0dbe5f68c78426e51c6a94721eb136b123127c'}, 'PROOF.md': {'bytes': 15792, 'sha256': '7f605cf0c12e2441e9877fbb2fddd8d77aabb4de128165ed5e6571022255b398'}, 'README.md': {'bytes': 2300, 'sha256': '4e9b4d5db7e0a39744c2ae229a5f07cede65cf9638b071267b57d5313debe150'}, 'RESEARCH_LOG.md': {'bytes': 3192, 'sha256': 'f4890b146cdcb1775490e2ca686ba227b7341457a5bae09930011889af84c1c0'}, 'SOURCE_VERIFICATION.json': {'bytes': 13649, 'sha256': 'd4867469064abf2b5ae09c6958b29306563943d1870c07617db9e3ef7d3bd721'}, 'controls.py': {'bytes': 7151, 'sha256': '4b5037648aab74e6408ec73e4a483a1a2d5bd082e50285fed45d0bb224fb77a9'}}


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def filemeta(path):
    data = path.read_bytes()
    return {"bytes":len(data), "sha256":hashlib.sha256(data).hexdigest()}


def no_duplicates(pairs):
    result = {}
    for key, val in pairs:
        need(key not in result, "duplicate JSON key")
        result[key] = val
    return result


def inventory(root):
    expected = set(FROZEN) | {"verify.py", "MANIFEST.json"}
    need({p.name for p in root.iterdir()} == expected, "strict file inventory")
    need(all(p.is_file() and not p.is_symlink() for p in root.iterdir()),
         "nonregular or linked file")
    m = json.loads((root/"MANIFEST.json").read_text(), object_pairs_hook=no_duplicates)
    need(set(m) == {"format", "problem_id", "files"}, "manifest schema")
    need(m["format"] == 1 and m["problem_id"] == 30003264, "manifest identity")
    need(set(m["files"]) == expected-{"MANIFEST.json"}, "manifest inventory")
    for name, frozen in FROZEN.items():
        need(m["files"][name] == frozen, "frozen manifest entry: "+name)
        need(filemeta(root/name) == frozen, "frozen bytes: "+name)
    need(filemeta(root/"verify.py") == m["files"]["verify.py"], "verifier bytes")
    return len(expected)


def rewrite_manifest(root, name):
    p=root/"MANIFEST.json"
    m=json.loads(p.read_text())
    m["files"][name]=filemeta(root/name)
    p.write_text(json.dumps(m,indent=2,sort_keys=True)+"\n")


def damage_controls(root):
    cases = ["missing_proof", "extra_file", "changed_proof", "changed_controls",
             "changed_results", "rehashed_proof", "rehashed_source_metadata",
             "wrong_problem", "symlink_proof", "invalid_manifest",
             "missing_manifest", "duplicate_manifest_key"]
    rejected=[]
    with tempfile.TemporaryDirectory(prefix="prebloch-integrity-") as temp:
        base=Path(temp)
        intact=base/"intact"
        shutil.copytree(root,intact)
        inventory(intact)
        for case in cases:
            p=base/case
            shutil.copytree(root,p)
            if case=="missing_proof":
                (p/"PROOF.md").unlink()
            elif case=="extra_file":
                (p/"unexpected.txt").write_text("synthetic extra file\n")
            elif case in ("changed_proof","rehashed_proof"):
                with (p/"PROOF.md").open("ab") as f: f.write(b"\nchanged\n")
                if case.startswith("rehashed"): rewrite_manifest(p,"PROOF.md")
            elif case=="changed_controls":
                with (p/"controls.py").open("ab") as f: f.write(b"\n# changed\n")
            elif case=="changed_results":
                with (p/"CONTROL_RESULTS.json").open("ab") as f: f.write(b" ")
            elif case=="rehashed_source_metadata":
                with (p/"SOURCE_VERIFICATION.json").open("ab") as f: f.write(b" ")
                rewrite_manifest(p,"SOURCE_VERIFICATION.json")
            elif case=="wrong_problem":
                m=json.loads((p/"MANIFEST.json").read_text());m["problem_id"]=0
                (p/"MANIFEST.json").write_text(json.dumps(m))
            elif case=="symlink_proof":
                (p/"PROOF.md").unlink();(p/"PROOF.md").symlink_to(root/"PROOF.md")
            elif case=="invalid_manifest":
                (p/"MANIFEST.json").write_text("{")
            elif case=="missing_manifest":
                (p/"MANIFEST.json").unlink()
            elif case=="duplicate_manifest_key":
                t=(p/"MANIFEST.json").read_text()
                (p/"MANIFEST.json").write_text(t.replace('{','{"problem_id":30003264,',1))
            try:
                inventory(p)
            except (ValueError, OSError, TypeError, KeyError):
                rejected.append(case)
            else:
                raise ValueError("damaged package accepted: "+case)
    return {"intact_control_accepted": True,
            "rejected_count":len(rejected),"rejected":rejected}


def main():
    root=Path(__file__).resolve().parent
    count=inventory(root)
    expected=(root/"CONTROL_RESULTS.json").read_bytes()
    for opts in ([],["-O"]):
        result=subprocess.run([sys.executable,"-I","-B",*opts,str(root/"controls.py")],
                              cwd=root,capture_output=True,check=True,timeout=60)
        need(result.stdout==expected,"control replay mismatch")
        need(result.stderr==b"","unexpected control stderr")
    result={"problem_id":30003264,"files_verified":count,
            "core_files_pinned":len(FROZEN),
            "normal_and_optimized_replays":"byte-identical",
            "replay_output":filemeta(root/"CONTROL_RESULTS.json"),
            "damage_controls":damage_controls(root),
            "scope":"author integrity and finite controls; independent mathematical audit pending"}
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=="__main__":
    main()

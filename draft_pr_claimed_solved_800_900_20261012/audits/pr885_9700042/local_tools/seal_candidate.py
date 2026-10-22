#!/usr/bin/env python3
"""Close the actual already-built PR885 current candidate; no archival code."""
from pathlib import Path
import datetime
import hashlib
import json
import stat

A = Path(__file__).resolve().parent.parent
ROOT = A / "replay/revision_r1"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def need(ok, why):
    if not ok:
        raise RuntimeError(why)


def regular(p):
    need(stat.S_ISREG(p.lstat().st_mode), "nonregular seal input")
    return p.read_bytes()


def jbytes(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def main():
    need(not (ROOT / "CURRENT_PUBLICATION_MANIFEST.json").exists(), "fresh current seal required")
    build = json.loads(regular(A / "preprint/NORMAL_BUILD_RECEIPT.json"))
    need(build["exit"] == 0 and build["result"]["status"] == "PASS", "actual completed build required")
    archive = regular(A / "preprint/oriented-flow-verification.zip")
    need(len(archive) == build["result"]["bytes"] == 388193 and
         sha(archive) == build["result"]["sha256"] == "824b7f037be72f7c7337dba4ea00c6d72b11be5a8cf026e928e4e1b751753f3b", "actual archive pin")
    with (ROOT / "oriented-flow-verification.zip").open("xb") as stream:
        stream.write(archive)

    old_readme = regular(ROOT / "README.md")
    readme = old_readme.decode().replace("# Current PR885 publication candidate", "# PR885 publication package")
    readme = readme.replace("This is a candidate awaiting actual package execution and final independent reviews; no DOI or acceptance is asserted here. Final review records and publication receipts are maintained in the separate PR885 audit folder.",
        "Final review records and publication receipts are maintained in the separate PR885 audit folder and must be checked at the documented accepted revision. This README does not itself assert a DOI, completed review or acceptance.")
    need(readme != old_readme.decode(), "current README status-neutral update")
    (ROOT / "README.md").write_text(readme)

    original = json.loads(regular(A / "SOURCE_MANIFEST.json"))
    portable_raw = regular(ROOT / "verification/package_index.json")
    need(sha(portable_raw) == "a45d6799b5770cd51cfb4e0bdbcd4461d981f13be733dfb1f57236ad838f51b9", "actual portable index")
    portable = json.loads(portable_raw)
    names = {r["path"] for r in original["files"]}
    names |= {"portable.py", "note.tex", "metadata.json", "zenodo-deposit.json", "oriented-flow-note.pdf", "oriented-flow-verification.zip", "CURRENT_PUBLICATION.json"}
    names |= {"verification/" + r["path"] for r in portable["files"]}
    names.add("verification/package_index.json")
    rows = []
    for name in sorted(names):
        raw = regular(ROOT / name)
        rows.append({"path": name, "bytes": len(raw), "sha256": sha(raw)})
    need(len(rows) == 196, "complete expected current file count")
    manifest = jbytes({"schema": "oriented-flow-9700042-current-publication-v1", "problem_id": "9700042", "files": rows})
    with (ROOT / "CURRENT_PUBLICATION_MANIFEST.json").open("xb") as stream:
        stream.write(manifest)

    tool = regular(ROOT / "portable.py")
    need(sha(tool) == "8832a44a53f0df4867cb8196d725209dd7ac5944c82b4f296b7514155fe72e6c", "reviewed startup")
    api = {"__name__": "parent_seal_authentication_only", "__file__": str(ROOT / "portable.py")}
    exec(compile(tool, str(ROOT / "portable.py"), "exec"), api)
    api["closed_tree"](ROOT, names | {"CURRENT_PUBLICATION_MANIFEST.json"})
    # This is structural authentication only. Actual normal/O current CLI follows.
    api["current_inputs"](ROOT, sha(manifest))
    core_names = ["portable.py", "note.tex", "metadata.json", "zenodo-deposit.json", "oriented-flow-note.pdf", "oriented-flow-verification.zip", "CURRENT_PUBLICATION.json", "CURRENT_PUBLICATION_MANIFEST.json", "verification/package_index.json", "verification/portable.py", "verification/note.tex", "verification/metadata.json", "verification/zenodo-deposit.json"]
    baseline = rows + [{"path": "CURRENT_PUBLICATION_MANIFEST.json", "bytes": len(manifest), "sha256": sha(manifest)}]
    receipt = {"timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "status": "SEALED_STRUCTURAL_AUTHENTICATION_PASS_DEFAULT_CURRENT_PENDING", "candidate_relative_path": "replay/revision_r1", "current_manifest_sha256": sha(manifest), "portable_index_sha256": sha(portable_raw), "original_head": original["head"], "original_effort": "5/5", "all_current_files": len(baseline), "portable_members": 159, "current_rows": baseline, "core_rows": [r for r in baseline if r["path"] in core_names], "whole_package_CLEAR_count": 0, "default_current": "NOT_RUN", "normal_build": "PASS", "earlier_optimized_build": "FAILED: checker schedule mismatch; exact cause unobserved during contemporary ENOSPC"}
    with (A / "preprint/CANDIDATE_SEAL.json").open("x") as stream:
        stream.write(jbytes(receipt).decode())
    print(json.dumps({k:v for k,v in receipt.items() if k not in ("current_rows", "core_rows")}, sort_keys=True))


if __name__ == "__main__":
    main()

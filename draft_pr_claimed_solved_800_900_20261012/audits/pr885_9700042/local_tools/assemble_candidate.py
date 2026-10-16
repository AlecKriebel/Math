#!/usr/bin/env python3
"""Explicit PR885 candidate assembly; no Git, network or archival execution."""
from pathlib import Path, PurePosixPath
import datetime
import hashlib
import json
import shutil
import stat

A = Path(__file__).resolve().parent.parent
OUT = A / "replay/revision_r1"
PORTABLE = OUT / "verification"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def need(ok, reason):
    if not ok:
        raise RuntimeError(reason)


def regular(path):
    need(stat.S_ISREG(path.lstat().st_mode), "nonregular assembly input")
    return path.read_bytes()


def jbytes(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def safe(name):
    p = PurePosixPath(name)
    need(not p.is_absolute() and name == str(p) and all(x not in ("", ".", "..") for x in name.split("/")), "unsafe relative path")


def materialize(root, values):
    root.mkdir(parents=True)
    for name, raw in sorted(values.items()):
        safe(name)
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as stream:
            stream.write(raw)
        target.chmod(0o644)


def main():
    need(not OUT.exists(), "candidate must be fresh")
    blobs, provenance = {}, []

    def add(name, raw, origin):
        safe(name)
        need(name not in blobs, "duplicate assembly destination " + name)
        need(b"/Users/" not in raw and b"/var/folders/" not in raw and b"Bearer " not in raw,
             "machine path or token requires explicit review: " + name)
        blobs[name] = raw
        provenance.append({"path": name, "origin": origin, "bytes": len(raw), "sha256": sha(raw)})

    def row(folder, item, relative_key="path"):
        name = item[relative_key]
        safe(name)
        raw = regular(A / folder / name)
        need(len(raw) == item["bytes"] and sha(raw) == item["sha256"], "allowlist pin " + folder + "/" + name)
        add(folder + "/" + name, raw, "explicit authenticated family allowlist")

    original_raw = regular(A / "SOURCE_MANIFEST.json")
    need(sha(original_raw) == "6b1d1281848190f616f6759f40454183c937b65e65219b893202254be6c3617d", "source envelope")
    original = json.loads(original_raw)
    originals = {}
    for item in original["files"]:
        raw = regular(A / "source" / item["path"])
        need(len(raw) == item["bytes"] and sha(raw) == item["sha256"], "original SHA pin")
        need(hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == item["git_blob"], "original Git blob pin")
        originals[item["path"]] = raw
        add("source/" + item["path"], raw, "immutable assigned-head original")
    need(len(originals) == 30 and sum(map(len, originals.values())) == 214980, "all30 originals")
    add("SOURCE_MANIFEST.json", original_raw, "byte-identical convenience copy")
    add("root_evidence/SOURCE_MANIFEST.json", original_raw, "immutable external source trust root")

    families = [
        ("blind_flow_audit_01", "be575031ea35006a06c53003d1cb3760ed8e34b7823d3adbf6f4751b349a0d1b", "relative_path", 8),
        ("cut_duality_audit_01", "e116829cafff7c8fcba034cfdeb3474215a5c9ec469568e1626c004ee7dc9e23", "path", 13),
        ("bk_poisson_audit_01", "62ff01184f8244fc7259d7f0048dc6481a22052d8c535c6b694e1f8d6e1e278b", "path", 8),
        ("artifact_audit_01", "9d7f8f2d9ffa9961c98748f3f63f2e5bb34c497a6bfdeedb51c09e00f6af3863", "path", 32),
    ]
    for folder, pin, key, count in families:
        raw = regular(A / folder / "PUBLIC_MANIFEST.json")
        need(sha(raw) == pin, "initial family envelope")
        items = json.loads(raw)["files"]
        need(len(items) == count, "initial family count")
        for item in items:
            row(folder, item, key)
        add(folder + "/PUBLIC_MANIFEST.json", raw, "external authenticated initial envelope")

    raw = regular(A / "priority_classical_01/PUBLIC_MANIFEST.json")
    need(sha(raw) == "21b765ca90521f2fb563f5f4b1b93d2d46f0a7643da9023da2e3c2cb3c0842a2", "classical priority envelope")
    items = json.loads(raw)
    need(len(items) == 9, "classical priority count")
    for item in items:
        row("priority_classical_01", item)
    add("priority_classical_01/PUBLIC_MANIFEST.json", raw, "authenticated priority envelope")

    raw = regular(A / "priority_completion_02/PUBLIC_MANIFEST.json")
    need(sha(raw) == "c7851a158a2ad175b34fc5881b07e835d0e56dc68cea87f6b33ec1cebaa0e4f1", "completion priority envelope")
    items = json.loads(raw)["payload"]
    need(len(items) == 12, "completion priority count")
    for item in items:
        raw_item = regular(A / item["path"])
        need(len(raw_item) == item["bytes"] and sha(raw_item) == item["sha256"], "completion priority pin")
        add(item["path"], raw_item, "authenticated completion payload")
    add("priority_completion_02/PUBLIC_MANIFEST.json", raw, "authenticated completion envelope")
    old_allowlist = json.loads(regular(A / "priority_completion_02/PARENT_INTEGRATION_ALLOWLIST.json"))
    for item in old_allowlist["safe_existing_recent"] + old_allowlist["safe_existing_disposition"]:
        raw_item = regular(A / item["path"])
        need(len(raw_item) == item["bytes"] and sha(raw_item) == item["sha256"], "newly dated existing-family pin")
        add(item["path"], raw_item, "completion-time current-byte authentication; not retroactive historical envelope")

    root_names = [
        "ROOT_SOURCE_CONTRACT.md", "ROOT_INDEPENDENT_RECONSTRUCTION.md",
        "ROOT_PRIORITY_MODEL_COMPARISON.md", "FINAL_PRIORITY_DISPOSITION.md",
        "ROOT_FINITE_PRIORITY_MODEL_DISTINCTION.json", "ROOT_OLD_ESTIMATE_INCLUSION_CONTROLS.json",
        "ROOT_ORIGINAL_REPLAY.json", "ROOT_NATIVE_SOURCE_AUTHENTICATION.json",
        "INITIAL_AUDIT_INTEGRATION.json", "INITIAL_AUDIT_INTEGRATION.md",
        "PRIORITY_INTEGRATION_AUTHENTICATION.json",
    ]
    for name in root_names:
        add("root_evidence/" + name, regular(A / name), "explicit parent-authored historical evidence")
    for name in ["check_old_estimate_event_inclusion.py", "check_priority_model_distinction.py"]:
        add(name, regular(A / name), "parent-authored stdout-only finite diagnostic")

    tool_raw = regular(A / "publication_tools_03/portable.py")
    need(len(tool_raw) == 41629 and sha(tool_raw) == "8832a44a53f0df4867cb8196d725209dd7ac5944c82b4f296b7514155fe72e6c", "V4 startup pin")
    add("portable.py", tool_raw, "reviewed V4 current wrapper")
    add("PRIMARY_SOURCE_PINS.json", regular(A / "publication_tools_02/PRIMARY_SOURCE_PINS.json"), "explicit four-primary fingerprints, no source bodies")
    for name, pin in [
        ("note.tex", "493e7b3756487bd47c2eb0f804e5bf253082b63e86f54c661c0ffbf40b7d39ea"),
        ("metadata.json", "9cf4e1d1f3c9a9602999646f1f68bbed15da7283a005c6afdacd371fe02e879a"),
        ("zenodo-deposit.json", "dec24c56cd7db7027221123d790f0c3a7837b4db04c5863adb7457ce9c9264b1"),
    ]:
        raw = regular(A / "preprint" / name)
        need(sha(raw) == pin, "current paper/metadata pin")
        add(name, raw, "current authored publication core")

    readme = """# Verification archive: near-one oriented Bernoulli flow

This archive supports the note *Near-one oriented-percolation flow from Bernoulli first-passage estimates*, Alec Kriebel, version1.0.0, 16October2026. The exact Aldous edge-capacity model satisfies (1-v(1-q))/sqrt(2q) ->1, with volume first and q second. The note presents the entire asymptotic as an explicitly attributed corollary of Basdevant-Gouere-Theret's older strict-chain scaling and numerical weighted-list bound. No novelty, first-recognition or present-day-openness certificate is claimed. Original proof-search effort remains5/5.

The original30 assigned-head files are frozen under `source/`, not active publication metadata. Their older titles, candidate proofs, audit statuses and priority statements are historical records; the current note and metadata govern the published scope. The revised C1/C4 argument is preserved as an independently audited longer alternative. All dated audit reports describe their recorded stage, including earlier incomplete states. Initial mathematical, priority and format audits are not the two final whole-package reviews. Those final reports are maintained separately from this sealed archive.

Authenticate this archive's exact ZIP and startup `portable.py` independently using the accepted Git revision or publication hashes. Obtain the complete `package_index.json` SHA256 independently; a self-consistent downloaded index is not an external trust root. The wrapper additionally pins the immutable source manifest, all30 SHA256 and Git blob identities, assigned head and5/5 effort.

Using Python3.11 or later and the system `patch` program:

```
python3 -I -S -B portable.py verify INDEX_SHA256 --root .
python3 -I -S -B -O portable.py verify INDEX_SHA256 --root .
python3 -I -S -B portable.py verify INDEX_SHA256 --root . --verify-only
python3 -I -S -B portable.py build INDEX_SHA256 OUTSIDE_DIRECTORY/oriented-flow-verification.zip --root .
python3 -I -S -B check_old_estimate_event_inclusion.py
python3 -I -S -B check_priority_model_distinction.py
```

Replace INDEX_SHA256 with the independently authenticated actual index pin and OUTSIDE_DIRECTORY with an existing directory outside this complete authenticated input tree. A build destination must be fresh. The complete input tree is closed, regular and case-unaliased; unlisted directories, symlinks and special files reject. Filesystem containment compares canonical paths, output ancestors and every authenticated input-directory identity, including APFS aliases. No concurrent hostile filesystem-replacement guarantee or execution sandbox is claimed.

Default verification authenticates first, copies exactly30 originals to scratch, runs one actual isolated launcher and the64 original nested requests (20 positive,20 assertion-negative,20 corrupt-checker and4 patch). Actual child -I-S-B flags and original requested labels are distinct; archival compile optimize=0 retains assertions. Complete raw root output is checked except the parsed Python-version metadata field, and original scratch bytes are reauthenticated. `--verify-only` performs no archival execution. These are byte and finite-diagnostic checks, not proof, novelty or human-review certificates. Historical inner JSON/filesystem permissiveness is preserved and separately documented; it is not attributed to the stricter wrapper.

The two stdout-only parent controls check finite geometry/model distinction. Their outputs and those of the archived independent checks supplement the analytic proof. Finite cases do not prove a limit or priority. In particular the tiny parent event controls did not distinguish per-increment negative parts from a net negative part; actual source inspection and the analytic backward-variation bound establish that distinction.

`source-only` can authenticate the complete catalog, problems and research-results corpora before extracting this exact target pair and statement; all three external corpus paths are mandatory. Optional `--primary-dir` authenticates the four complete source bodies by filenames/pins in PRIMARY_SOURCE_PINS.json. No corpus, third-party primary body or credential is distributed. Source hashes authenticate bytes, not source interpretations.

The sorted0644 DEFLATE9 ZIP has fixed epoch2026-10-16T00:00Z. Exact compressed rebuild is promised only for the same Python ZIP implementation and zlib runtime. The current note PDF is a separate publication asset. `note.tex`, metadata.json and zenodo-deposit.json are also included here; their kit paths name the two separate outer publication assets. There is no recursive ZIP self-hash.

AI tools were used extensively for research, writing, computations and adversarial checking. Recorded independent reviews were by AI agents. This is an unrefereed preprint, without completed independent human peer review or formal proof-assistant verification. Author: Alec Kriebel, ORCID0009-0001-9320-500X. LicenseCC-BY4.0.
"""
    add("README.md", readme.encode(), "current publication and reproduction instructions")
    add("RESEARCH_LOG.md", ("# Frozen verification-archive chronology\n\n2026-10-15: exact claimed_solved5/5 source authenticated; independent finite-cut, stochastic/full-proof and artifact families completed.\n\n2026-10-16: complete older-input corollary verified, with corrected source negative parts and explicit site threshold; short attributed note prepared. V2 physical-alias defect reproduced and V4 closed-input-directory mechanism reviewed. Paper layout checked on all six final pages. This snapshot precedes final actual package execution and the two final whole-package reviews, whose reports remain outside this sealed ZIP. No final acceptance, publication or human review is asserted by this chronology.\n").encode(), "frozen stage chronology, not later acceptance receipt")

    index = jbytes({"schema": "oriented-flow-9700042-verification-v1", "problem_id": "9700042", "files": [
        {"path": name, "bytes": len(raw), "sha256": sha(raw)} for name, raw in sorted(blobs.items())]})
    blobs["package_index.json"] = index
    materialize(PORTABLE, blobs)

    # The active outer README/log replace only their two historical counterparts.
    # All30 originals remain byte-identical inside verification/source/.
    outer = dict(originals)
    outer["README.md"] = ("# Current PR885 publication candidate\n\nThe research note and its attributed BGT-corollary scope supersede historical priority language. Read oriented-flow-note.pdf and note.tex. All30 original assigned-head files are preserved unchanged under verification/source/;28 other historical outer files remain unchanged. Original effort5/5 is preserved.\n\nAuthenticate CURRENT_PUBLICATION_MANIFEST.json externally, then run `python3 -I -S -B portable.py current MANIFEST_SHA256 --root .` (also supported with -O). `--verify-only` authenticates without archival execution. The sealed archive has separate instructions in verification/README.md. Current wrappers and archive hashes are finite authentication, not proof/priority or human-review certificates. The paper is unrefereed and extensive AI use is disclosed.\n\nThis is a candidate awaiting actual package execution and final independent reviews; no DOI or acceptance is asserted here. Final review records and publication receipts are maintained in the separate PR885 audit folder.\n").encode()
    outer["RESEARCH_LOG.md"] = ("# Current publication chronology\n\nOriginal central proof-search effort:5/5, unchanged.\n\n2026-10-16: historical source and original reports preserved, independently audited longer proof retained, full BGT older-input corollary mapped explicitly, short six-page note and supporting archive assembled for final execution and reviews. No current novelty or first-recognition claim. Actual acceptance, merge and publication are recorded separately after required reviews.\n").encode()
    for name in ["portable.py", "note.tex", "metadata.json", "zenodo-deposit.json"]:
        outer[name] = blobs[name]
    pdf = regular(A / "preprint/output/pdf/note.pdf")
    need(len(pdf) == 82047 and sha(pdf) == "e8ef086a61d1425c0e4892279a42f64079be1216c7936fff81628471c1ed2fba", "actual final PDF pin")
    outer["oriented-flow-note.pdf"] = pdf
    outer["CURRENT_PUBLICATION.json"] = jbytes({"schema": "oriented-flow-9700042-current-layout-v1", "problem_id": "9700042", "portable_prefix": "verification", "zip_path": "oriented-flow-verification.zip", "pdf_path": "oriented-flow-note.pdf", "tex_path": "note.tex"})
    for name, raw in sorted(outer.items()):
        p = OUT / name
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("xb") as f:
            f.write(raw)
    preprint_pdf = A / "preprint/oriented-flow-note.pdf"
    with preprint_pdf.open("xb") as stream:
        stream.write(pdf)

    receipt = {"timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "status": "ASSEMBLED_NOT_EXECUTED", "original_head": original["head"], "original_effort": "5/5", "portable_files": len(blobs), "portable_bytes": sum(map(len, blobs.values())), "index_sha256": sha(index), "portable_tool_sha256": sha(tool_raw), "all30_source_pins_verified": True, "all30_inner_originals_unchanged": True, "outer_historical_files_unchanged": 28, "provenance": provenance, "default_replay": "NOT_RUN", "zip_build": "NOT_RUN", "current_manifest": "NOT_YET_WRITTEN", "whole_package_CLEAR_count": 0}
    with (A / "preprint/ASSEMBLY_RECEIPT.json").open("x") as stream:
        stream.write(jbytes(receipt).decode())
    print(json.dumps({k:v for k,v in receipt.items() if k != "provenance"}, sort_keys=True))


if __name__ == "__main__":
    main()

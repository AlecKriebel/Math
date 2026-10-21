#!/usr/bin/env python3
"""Build only this candidate's reviewed source/verification publication files."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import sys
import zipfile

AUDIT = Path(__file__).resolve().parent
EFFORT = AUDIT.parents[1]
sys.path.insert(0, str(EFFORT))
from sweep_io import atomic_bytes, atomic_json

FAMILY_SEALS = {
    "flow_adversary_01": "8d1ffde1ef986ed4bfd6f7a2c4117da7733c09892bf47a24f13c051f71c4f3ec",
    "probability_adversary_01": "623a63535125ee8abd00ba3cdfd5ae1004464e14b3ae9c85c616ac7ffc715a55",
    "priority_scope_adversary_01": "59562219252e327d8f2c2b8b1bea97ee6644e8131e5b9b44b2fd538565836e4b",
}
REPAIR_SEAL = "eb10e8c4ef05ac08c546effef7c4932036303e888c814a25798bca62b769a8fb"
PREFIX = "congestion-fragmentation-verification"
TITLE = "A designed tree model with a sharp congestion\u2013fragmentation transition"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_text())


def normalized(entries):
    return entries if isinstance(entries, list) else [{"path": k, **v} for k, v in entries.items()]


def safe(name):
    path = PurePosixPath(name)
    if path.is_absolute() or ".." in path.parts or str(path) != name:
        raise RuntimeError("Unsafe selected path")
    return name


def verify_seal(directory, filename, expected):
    path = directory / filename
    if sha(path.read_bytes()) != expected:
        raise RuntimeError("Review seal changed")
    value = read(path)
    for entry in normalized(value["files"]):
        name = safe(entry["path"])
        data = (directory / name).read_bytes()
        if len(data) != entry["bytes"] or sha(data) != entry["sha256"]:
            raise RuntimeError("Sealed artifact changed: " + name)
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iteration", required=True, type=int)
    args = parser.parse_args()
    if args.iteration < 1:
        raise RuntimeError("Positive iteration required")
    preprint = AUDIT / "preprint"
    source = preprint / "main.tex"
    pdf = preprint / "build/main.pdf"
    build = read(preprint / "build/BUILD_RECEIPT.json")
    qa = read(preprint / "PDF_VISUAL_QA.json")
    if build["returncode"] != 0 or build["source_sha256"] != sha(source.read_bytes()):
        raise RuntimeError("PDF is not built from current source")
    if build["pdf_sha256"] != sha(pdf.read_bytes()) or qa["pdf_sha256"] != sha(pdf.read_bytes()):
        raise RuntimeError("PDF/QA custody changed")
    if not qa["all_pages_visually_inspected"] or qa["material_layout_findings"]:
        raise RuntimeError("PDF QA is incomplete")
    support = AUDIT / "publication_support"
    verify_seal(support, "REPAIR_MANIFEST.json", REPAIR_SEAL)
    work = preprint / ("package_" + str(args.iteration).zfill(2))
    work.mkdir(exist_ok=False)
    tree = work / PREFIX
    tree.mkdir()
    selected = {}

    def add(name, data):
        safe(name)
        if name in selected:
            raise RuntimeError("Repeated payload path: " + name)
        selected[name] = data

    snapshot = read(AUDIT / "SOURCE_SNAPSHOT.json")
    if len(snapshot["files"]) != 24:
        raise RuntimeError("Unexpected original inventory")
    for entry in snapshot["files"]:
        data = (AUDIT / entry["local"]).read_bytes()
        if len(data) != entry["bytes"] or sha(data) != entry["sha256"]:
            raise RuntimeError("Original changed")
        blob = hashlib.sha1(("blob " + str(len(data)) + "\0").encode() + data).hexdigest()
        if blob != entry["git_blob"]:
            raise RuntimeError("Original Git identity mismatch")
        add("candidate/" + entry["local"].removeprefix("original/"), data)
    add("SOURCE_SNAPSHOT.json", (AUDIT / "SOURCE_SNAPSHOT.json").read_bytes())
    for family, expected in FAMILY_SEALS.items():
        directory = AUDIT / "reviews" / family
        manifest = verify_seal(directory, "MANIFEST.json", expected)
        for entry in normalized(manifest["files"]):
            add("reviews/" + family + "/" + entry["path"], (directory / entry["path"]).read_bytes())
        add("reviews/" + family + "/MANIFEST.json", (directory / "MANIFEST.json").read_bytes())
    for name in read(support / "PUBLICATION_FILES.json")["files"]:
        add(name, (support / safe(name)).read_bytes())
    for name in ["ROOT_MATHEMATICAL_AUDIT.md", "ROOT_PRIORITY_ASSESSMENT.md"]:
        add(name, (AUDIT / name).read_bytes())
    add("PKG01_RUNTIME_REPAIR.json", (AUDIT / "PKG01_RUNTIME_REPAIR.json").read_bytes())
    add("paper/main.tex", source.read_bytes())
    add("PDF_VISUAL_QA.json", (preprint / "PDF_VISUAL_QA.json").read_bytes())
    add("README.md", (AUDIT / "SUPPLEMENT_README.md").read_bytes())
    add("LICENSE.txt", ("Authored manuscript and supplement: Creative Commons Attribution 4.0 International.\n"
                        "https://creativecommons.org/licenses/by/4.0/\n"
                        "Copyright Alec Kriebel. Mathematical antecedents remain credited.\n"
                        "No third-party full text is included.\n").encode())

    metadata = {
        "title": TITLE, "upload_type": "publication", "publication_type": "preprint",
        "description": (
            "<p>We give an analytically tractable designed-tree example motivated by Aldous's conceptual congestion toy-model request. "
            "For a bounded-degree binary physical tree with k leaves on each root side and k squared cross-root demand streams, "
            "strictly positive linear capacity prices uniquely give the cheapest fixed-topology enlargement carrying doubled unit demands. "
            "After design, each stream grows affinely at an independent fixed-law Exp(1) rate. An exact transportation-cut formula and "
            "an all-cuts probability estimate confine the joint marginal-admission and spare-connectivity change to an interval of width "
            "16 sqrt(log(k)/k) around mean doubled demand. In the two outer phases every optimizer respectively leaves the whole tree "
            "spare or saturates every edge. The window is an upper bound, not an exact critical scaling theorem.</p>"
            "<p>Dense traffic, capacities increasing with graph size, quadratic time variance and normalization by the realized offered-demand "
            "slope are essential declared features. No canonical right-model, universal congestion, adaptive-growth, critical-profile or first-transition "
            "claim is made. Classical flow/concentration, random transportation, HOT and prior congestion/percolation models are credited, including "
            "Aldous's earlier tree-realism reservation. A bounded primary-source priority audit found no authenticated exact earlier construction/theorem "
            "in inspected material; the final 1993 Karp-Motwani-Nisan journal body, unindexed/unpublished work and uninspected editions remain limitations.</p>"
            "<p>The paper and source/verification ZIP preserve all 24 original research files, independent flow/probability controls and source comparisons. "
            "A new narrowly tested replay derivative preserves the original wrapper, requires exact active second-turn output and permits only explicitly "
            "bounded older floating diagnostics and documented metadata/projection differences. Python 3.9.6, NumPy 2.0.2 and SciPy 1.13.1 were tested; "
            "unpinned historical bitwise replay is not claimed. The preserved optional priority checker separately requires Python 3.10 or later, "
            "was tested with Python 3.14.6 and exactly reproduces its 32 retained controls. The analytic proof does not depend on finite computations.</p>"
            "<p>AI tools were extensively involved in mathematical research, model and proof development, computational verification, literature search, "
            "manuscript preparation and adversarial auditing. This is an unrefereed preprint and has not undergone formal independent human peer review. "
            "Internal AI reviews do not constitute human peer review.</p>"
        ),
        "creators": [{"name": "Kriebel, Alec", "affiliation": "Independent researcher",
                      "orcid": "0009-0001-9320-500X"}],
        "access_right": "open", "license": "cc-by-4.0", "publication_date": "2026-10-21",
        "version": "1.0", "language": "eng",
        "keywords": ["congestion", "multicommodity flow", "spare capacity", "binary trees",
                     "highly optimized tolerance", "random transportation", "phase transition",
                     "Chernoff bounds", "Aldous toy model", "9700002", "AMR-096-0002"],
        "related_identifiers": [
            {"identifier": "https://github.com/AlecKriebel/Math/pull/397",
             "relation": "isSupplementTo", "scheme": "url"},
            {"identifier": "https://www.stat.berkeley.edu/~aldous/Research/OP/congestion.html",
             "relation": "references", "scheme": "url"},
            {"identifier": "10.1287/moor.13.1.80", "relation": "references", "scheme": "doi"},
            {"identifier": "10.1287/moor.18.1.71", "relation": "references", "scheme": "doi"},
        ],
        "references": [
            "D. Aldous, Congestion in networks: SOC, HOT and the percolation-fragmentation phase transition. Problem posted May2003; update marked February2018. Primary page accessed21October2026.",
            "L. R. Ford Jr. and D. R. Fulkerson, Maximal flow through a network, Canadian Journal of Mathematics8(1956),399-404. doi:10.4153/CJM-1956-045-5.",
            "R. Hassin and E. Zemel, Probabilistic analysis of the capacitated transportation problem, Mathematics of Operations Research13(1)(1988),80-89. doi:10.1287/moor.13.1.80.",
            "R. M. Karp, R. Motwani and N. Nisan, Probabilistic analysis of network flow algorithms, Mathematics of Operations Research18(1)(1993),71-97. doi:10.1287/moor.18.1.71. Actual comparison uses the December1988 Berkeley report CSD-88-392; final journal body not inspected.",
            "J. M. Carlson and J. Doyle, Complexity and robustness, PNAS99(Suppl.1)(2002),2538-2545. doi:10.1073/pnas.012582499.",
            "M. Kim and F. Radicchi, Shortest-path percolation on random networks, Physical Review Letters133(2024),047402. doi:10.1103/PhysRevLett.133.047402.",
            "D. Aldous, Flows through random networks, Ottawa talk, June2005, slide5.",
        ],
    }
    deposit = {"metadata": metadata, "files": [
        {"path": "congestion-fragmentation.pdf", "name": "congestion-fragmentation.pdf"},
        {"path": "congestion-fragmentation-verification.zip",
         "name": "congestion-fragmentation-verification.zip"}]}
    deposit_data = (json.dumps(deposit, ensure_ascii=False, indent=2) + "\n").encode()
    add("publication-metadata.json", deposit_data)
    for name, data in selected.items():
        path = tree / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    payload = {name: {"bytes": len(data), "sha256": sha(data)} for name, data in sorted(selected.items())}
    manifest = {"algorithm": "sha256", "scope": "Every payload; MANIFEST.json alone self-excluded.",
                "files": payload}
    atomic_json(tree / "MANIFEST.json", manifest)
    archive = work / "congestion-fragmentation-verification.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipped:
        for path in sorted(tree.rglob("*")):
            if path.is_file():
                info = zipfile.ZipInfo(PREFIX + "/" + path.relative_to(tree).as_posix(),
                                       date_time=(2026, 10, 21, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                zipped.writestr(info, path.read_bytes())
    with zipfile.ZipFile(archive) as zipped:
        if zipped.testzip() or len(zipped.namelist()) != len(payload) + 1:
            raise RuntimeError("Built ZIP integrity/set mismatch")
    publication = preprint / "publication"
    publication.mkdir(exist_ok=True)
    outputs = {
        "congestion-fragmentation.pdf": pdf.read_bytes(),
        "congestion-fragmentation.tex": source.read_bytes(),
        "congestion-fragmentation-verification.zip": archive.read_bytes(),
        "zenodo-deposit.json": deposit_data,
        "README.md": (AUDIT / "PUBLICATION_README.md").read_bytes(),
    }
    old = work / "prior_release"
    for name, data in outputs.items():
        target = publication / name
        if target.exists():
            old.mkdir(exist_ok=True)
            shutil.copyfile(target, old / name)
        atomic_bytes(target, data)
    release = {"timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
               "iteration": args.iteration, "publication_ready": False,
               "status": "Exact candidate for fresh independent complete-package review.",
               "archive_payloads": len(payload), "archive_members": len(payload) + 1,
               "files": [{"path": name, "bytes": len(data), "sha256": sha(data)}
                         for name, data in outputs.items()]}
    atomic_json(publication / "RELEASE_FILES.json", release)
    atomic_json(work / "BUILD_PACKAGE_RECEIPT.json", release)
    print(json.dumps(release, indent=2))


if __name__ == "__main__":
    main()

"""Build and test the three PR411 research-note assets.

Standard library only. Run with --case, an existing private --python
interpreter containing SymPy 1.14.0, and an isolated --private-dir.
Never resolve the private interpreter symlink: doing so loses its venv.
Writes only support/, source_bundle/, the three assets/, and
SUPPORT_ASSEMBLY_RESULTS.json under case/publication_package, plus private
extractions/raw logs under --private-dir. It does not alter source inputs,
Git, remote applications, or the paper.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import zipfile

FIXED_TIME = (1980, 1, 1, 0, 0, 0)
PINS = {
    "publication_package/paper/local_ricci_pinching_maxima.tex":
        "8bcaec828c6c40fb990ce92ed1cf36f7fbdb643546168fb5f4d884c75db41c72",
    "publication_package/paper/local_ricci_pinching_maxima.pdf":
        "13d6fcdb924ea1461a6c44d4bb4e6aec1f278598218f8a34f26252d52ca0d37b",
    "verification_v2/FINAL_SEAL.json":
        "6fb571bf3f2e8c36cdea70832efcdab15a48bab75db40e67a9ebce496390e7fb",
    "verification_v2/PUBLICATION_WHITELIST.json":
        "6ea7bf4432ef4659340a94b1077fc804b1203d141fbf4231868f8844644fddf1",
    "root_checks/exact_boundary_koszul.py":
        "baa51a6edff59df85a224f2fe52b1adda350c6a5c9e5c0fc65b7317a1ac11dd0",
    "root_checks/primary_Et_formula_check.py":
        "fa41cd597a88857c6910d8332abdd92c1a227b36b208874d7bd8610dab663a79",
}
SELECTED = [
    "MATH_GATE_ACCEPTANCE.json",
    "PRIORITY_GATE_ACCEPTANCE.json",
    "SOFTWARE_GATE_ACCEPTANCE_V2.json",
    "ROOT_V2_FINAL_REPLAY.json",
    "reviews/algebra_reproduction/CRITERIA.md",
    "reviews/algebra_reproduction/INDEPENDENT_DERIVATION.md",
    "reviews/algebra_reproduction/VERDICT.md",
    "reviews/algebra_reproduction/NATIVE_VERDICT.json",
    "reviews/geometry_adversary/ACCEPTANCE_CRITERIA.md",
    "reviews/geometry_adversary/INDEPENDENT_RECONSTRUCTION.md",
    "reviews/geometry_adversary/GEOMETRIC_AUDIT.md",
    "reviews/geometry_adversary/FINAL_NATIVE_VERDICT.json",
    "reviews/priority_classification_adversary/INDEPENDENT_CRITERIA.md",
    "reviews/priority_classification_adversary/INDEPENDENT_RECONSTRUCTION.md",
    "reviews/priority_classification_adversary/ADVERSARIAL_REPORT.md",
    "reviews/priority_classification_adversary/NATIVE_VERDICT.json",
    "root_checks/exact_boundary_koszul.py",
    "root_checks/primary_Et_formula_check.py",
    "root_checks/exact_boundary_results_normal.json",
    "root_checks/exact_boundary_results_optimized.json",
    "root_checks/primary_Et_formula_results_normal.json",
    "root_checks/primary_Et_formula_results_optimized.json",
    "root_checks/ROOT_EXACT_CHECK_REPLAY.json",
    "root_checks/ROOT_PRIMARY_Et_REPLAY.json",
    "root_checks/PRIORITY_FORMULA_NORMAL_NATIVE.json",
]

SOURCE_README = """# Standalone source for Local Ricci-pinching maxima on an almost-abelian group

Author: Alec Kriebel. ORCID: https://orcid.org/0009-0001-9320-500X.

This research-note source package contains the exact final standalone
[TeX source](local_ricci_pinching_maxima.tex) and a positive
[source manifest](SOURCE_MANIFEST.json). The manifest lists all payloads
except itself; the separate assembly/delivery record pins its actual hash.

Build with Tectonic:

    tectonic local_ricci_pinching_maxima.tex

Alternatively run pdflatex twice on that file. It uses article, geometry,
amsmath, amssymb, amsthm, and hyperref, with no external inputs or bibliography
files. A first Tectonic build may download its TeX support bundle. The root
compiled and visually checked all six PDF pages. Rebuilding renders the note;
different compiler versions or PDF metadata can change the PDF's byte hash.
The accompanying production PDF is copied exactly from the root's checked
90558-byte PDF, SHA-256
13d6fcdb924ea1461a6c44d4bb4e6aec1f278598218f8a34f26252d52ca0d37b.

The claim is a non-strict local maximum for every 0<u<1/2 among all nearby
left-invariant metrics on the specified fixed five-dimensional group, with
F=1/3, failure of that group's algebraic solvsoliton equation, and a same-group
metric with F=9/17. The metric is a Ricci soliton on another transitive
presentation. The family and value are Lauret–Will's prior work, and Lauret's
23 July 2018 slides already announced the negative existence statement.
Only the actually inspected arXiv versions are described; the full final
journal text was unavailable. No new family, first assertion, first proof,
novelty, or present community-open status is claimed.

This is an unrefereed, extensively AI-assisted account. AI tools were used
in solving, symbolic computation, source review, writing, and adversarial
verification. Machine agents are not independent human referees; no external
human peer review is certified, and the author retains responsibility.
The author proof-search record remains 2/5 with zero added assembly turns.
Whole-package acceptance and release status are tracked separately from
these source and historical component records.
No third-party full sources, raw searches, private state, or runtime are included.
"""

SUPPORT_README = """# Ricci-pinching verification and selected supporting material

This support package accompanies Alec Kriebel's note
Local Ricci-pinching maxima on an almost-abelian group.
The mathematical claim is the non-strict, all-nearby-metrics local maximum
for 0<u<1/2 on the fixed group, with F=1/3 and failure of that group's
solvsoliton equation. The metric is geometrically a Ricci soliton.
Lauret–Will's known family/value and Lauret's exact 23 July 2018 existence
announcement have priority. No new family, first assertion, first proof,
novelty, present community-open status, or inaccessible final-journal text is
certified. Primary PDFs and raw search material remain outside this archive.

## Contents and custody

- [verification_v2/README.md](verification_v2/README.md): intact accepted
  component, 71 positive payloads plus its authentic whitelist and final seal.
  No files were inserted or altered inside it. Its final seal SHA-256 is
  6fb571bf3f2e8c36cdea70832efcdab15a48bab75db40e67a9ebce496390e7fb;
  whitelist SHA-256 is
  6ea7bf4432ef4659340a94b1077fc804b1203d141fbf4231868f8844644fddf1.
- [acceptance/SOFTWARE_GATE_ACCEPTANCE_V2.json](acceptance/SOFTWARE_GATE_ACCEPTANCE_V2.json)
  and [acceptance/ROOT_V2_FINAL_REPLAY.json](acceptance/ROOT_V2_FINAL_REPLAY.json):
  later parent acceptance and actual final normal/optimized replay. Authentic
  component-review prose inside the core remains historical; this
  separate gate applies to its actual final 71/73-file state.
- [acceptance/MATH_GATE_ACCEPTANCE.json](acceptance/MATH_GATE_ACCEPTANCE.json)
  and [acceptance/PRIORITY_GATE_ACCEPTANCE.json](acceptance/PRIORITY_GATE_ACCEPTANCE.json):
  mathematical and qualified priority acceptance, with their limitations.
- [reviews/algebra_reproduction/VERDICT.md](reviews/algebra_reproduction/VERDICT.md),
  [reviews/geometry_adversary/GEOMETRIC_AUDIT.md](reviews/geometry_adversary/GEOMETRIC_AUDIT.md),
  and [reviews/priority_classification_adversary/ADVERSARIAL_REPORT.md](reviews/priority_classification_adversary/ADVERSARIAL_REPORT.md):
  complete individual reports with selected criteria, reconstructions, and
  native verdicts. The core also contains its complete software-adversary report.
- [root_checks/exact_boundary_koszul.py](root_checks/exact_boundary_koszul.py)
  and [root_checks/primary_Et_formula_check.py](root_checks/primary_Et_formula_check.py):
  exact, separately reviewed standard-library checks, kept together unchanged.
  Their normal/optimized native JSON results and root replay receipts are
  alongside them. PRIORITY_FORMULA_NORMAL_NATIVE.json is additional authored
  symbolic output, not a claim that its separate checker is bundled.
- [SUPPORT_MANIFEST.json](SUPPORT_MANIFEST.json): positive member manifest
  excluding itself; the external assembly/delivery record pins its actual hash.

Outside verification_v2 this is explicitly a PARTIAL selection of complete
authored artifacts, not a full sealed review corpus. Copied reports and
acceptances retain their original case-relative references and authentic
custody hashes. Referenced source PDFs, raw responses, complete reviewer file
sets, and private fixtures are not included; their presence or replay is not
attested by this archive. The core's own positive inventory is complete.
Whole-package acceptance and release status are tracked separately from
the historical component reviews and assembly records.

## Reproduce the accepted core

Authenticate the actual core seal hash above through a trusted independent
delivery record before executing code. A replacement of all code, manifests,
and custody together is outside this unkeyed-integrity check. Hashes bind
reviewed bytes, not arbitrary prose semantics.
Use Python with SymPy 1.14.0, preferably a private venv outside this extraction.
For example, from the extracted archive root:

    python -m venv "/path/to/private venv"
    "/path/to/private venv/bin/python" -m pip install sympy==1.14.0
    "/path/to/private venv/bin/python" -B verification_v2/run_all.py
    "/path/to/private venv/bin/python" -B -O verification_v2/run_all.py

Both top-level core runs must return PASS with 54 mandatory evaluations of
39 original predicates and 71 positive whitelist payloads. Do not place venvs,
caches, logs, or extra files inside verification_v2; its exact inventory is
checked. Do not use -I, which removes the script's sibling-module import path.
Do not resolve the venv interpreter symlink to its base interpreter.
The optional 38-control harness writes only private fixtures/logs:

    "/path/to/private venv/bin/python" -B verification_v2/reproduce_controls.py --private-log-dir "/path/to/private raw logs"

The current guarded normal/-O runs certify their checks and byte bindings.
Original historical optimized assertion output is NOT CERTIFIED validation.
The missing historical standalone source-manifest bytes with SHA-256
f5446c816081c5322e4279bcd9a61dca5bfb63cfacf69d105d1587ed9d93b7fb
and pre-layout checker bytes with SHA-256
eccde3c2a903b1fca0f232e7e392d537479ddd3936281a37e87c4f7e7047be97
remain UNATTESTED. No substitute objects or fabricated self-hashes are supplied.

## Reproduce the standard-library supplementary checks

From the extraction root, with any compatible Python 3:

    python3 -B root_checks/exact_boundary_koszul.py
    python3 -B -O root_checks/exact_boundary_koszul.py
    python3 -B root_checks/primary_Et_formula_check.py
    python3 -B -O root_checks/primary_Et_formula_check.py

Each prints a PASS JSON record. These finite exact computations supplement the
written uniform-neighborhood proof; they do not replace its analytic coverage.
The second script locates the first by its own directory, so keep both together.
It checks the old displayed E_t matrix directly: its actual ratio is
25t^4/(59t^4+32t^2), differing from the inspected preprint's printed formula.
No claim is made about whether the inaccessible journal corrected that formula.
The note's 9/17 comparison is independent of this peripheral source correction.

AI tools were used extensively in solving, symbolic computation, source review,
writing, and adversarial verification. Machine agents are not independent
human referees; the work is unrefereed and no external human peer review is
certified. The author retains responsibility. Status remains claimed_solved,
2/5 author proof-search turns, with zero new assembly/proof-search turns.
"""


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()


def safe_name(name):
    require(isinstance(name, str) and name and "\\" not in name and "\0" not in name,
            "unsafe member name")
    p = PurePosixPath(name)
    require(not p.is_absolute() and p.as_posix() == name
            and all(x not in ("", ".", "..") for x in p.parts), "unsafe member path")
    return name


def regular_tree(root):
    require(root.is_dir() and not root.is_symlink(), "nonregular directory")
    members = set()
    for base, dirs, files in os.walk(root, followlinks=False):
        for name in dirs + files:
            p = Path(base) / name
            mode = p.lstat().st_mode
            require(stat.S_ISDIR(mode) or stat.S_ISREG(mode), "special source entry: " + str(p))
            if stat.S_ISREG(mode):
                members.add(safe_name(p.relative_to(root).as_posix()))
    return members


def read_regular(root, relative):
    safe_name(relative)
    current = root
    for part in PurePosixPath(relative).parts:
        current = current / part
        require(not current.is_symlink(), "symlink source component")
    require(stat.S_ISREG(current.lstat().st_mode), "nonregular source file")
    return current.read_bytes()


def payload_rows(files, origins):
    return [{"path": name, "bytes": len(files[name]), "sha256": sha(files[name]),
             "origin": origins[name]} for name in sorted(files)]


def write_tree(root, files):
    if root.exists():
        require(regular_tree(root) <= set(files), "unexpected existing output member")
    root.mkdir(parents=True, exist_ok=True)
    for name, data in sorted(files.items()):
        dest = root / safe_name(name)
        dest.parent.mkdir(parents=True, exist_ok=True)
        require(not dest.is_symlink(), "output symlink")
        dest.write_bytes(data)
        dest.chmod(0o644)
    require(regular_tree(root) == set(files), "output inventory mismatch")


def zip_bytes(files):
    import io
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_STORED) as archive:
        for name in sorted(files):
            info = zipfile.ZipInfo(safe_name(name), FIXED_TIME)
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.compress_type = zipfile.ZIP_STORED
            info.extra = b""
            info.comment = b""
            archive.writestr(info, files[name])
    return stream.getvalue()


def validate_zip(data, expected):
    import io
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        infos = archive.infolist()
        names = [i.filename for i in infos]
        require(len(names) == len(set(names)), "duplicate member")
        require(names == sorted(expected) and set(names) == set(expected), "unlisted/missing/unsorted members")
        for info in infos:
            safe_name(info.filename)
            mode = info.external_attr >> 16
            require(stat.S_ISREG(mode) and stat.S_IMODE(mode) == 0o644, "nonregular/nonfixed ZIP mode")
            require(info.date_time == FIXED_TIME and info.create_system == 3, "nonfixed ZIP metadata")
            require(info.compress_type == zipfile.ZIP_STORED and not info.extra and not info.comment,
                    "nonfixed ZIP attributes")
            require(not info.flag_bits & 1, "encrypted ZIP member")
            actual = archive.read(info)
            require(actual == expected[info.filename], "ZIP exact readback mismatch")
        require(not archive.comment, "nonfixed ZIP comment")
    return {"member_count": len(expected), "exact_member_bytes_and_hashes": True,
            "sorted_unique_regular_safe_names": True, "fixed_metadata": True}


def extract_checked(data, files, target):
    validate_zip(data, files)
    require(not target.exists(), "clean extraction target already exists")
    write_tree(target, files)
    require(all(read_regular(target, n) == d for n, d in files.items()), "extraction mismatch")


def negative_archive_tests(private):
    """Private packaging falsifiers; no mathematics is replaced or reimplemented."""
    import io
    tests = []
    for label, name, mode in [
        ("traversal", "../escape", stat.S_IFREG | 0o644),
        ("absolute", "/escape", stat.S_IFREG | 0o644),
        ("backslash", "dir\\escape", stat.S_IFREG | 0o644),
        ("symlink", "ok", stat.S_IFLNK | 0o777),
        ("fifo", "ok", stat.S_IFIFO | 0o644),
        ("unlisted", "extra", stat.S_IFREG | 0o644),
        ("duplicate", "ok", stat.S_IFREG | 0o644),
    ]:
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, "w") as z:
            info = zipfile.ZipInfo(name, FIXED_TIME)
            info.create_system = 3
            info.external_attr = mode << 16
            z.writestr(info, b"x")
            if label == "duplicate":
                # Duplicate test deliberately writes identical named entries.
                import warnings
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", UserWarning)
                    z.writestr(info, b"x")
        data = stream.getvalue()
        (private / (label + ".zip")).write_bytes(data)
        rejected = False
        try:
            validate_zip(data, {"ok": b"x"})
        except ValueError:
            rejected = True
        require(rejected, "negative archive accepted: " + label)
        tests.append({"fixture": label, "rejected": True})
    for name in ("../escape", "/escape", "a/../escape", "./escape", "a//escape", "a\\escape"):
        rejected = False
        try:
            safe_name(name)
        except ValueError:
            rejected = True
        require(rejected, "unsafe path accepted")
    return tests


def run(command, cwd, private, label):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONNOUSERSITE="1")
    env.pop("PYTHONPATH", None)
    proc = subprocess.run(command, cwd=cwd, env=env, capture_output=True, timeout=180)
    (private / (label + ".stdout")).write_bytes(proc.stdout)
    (private / (label + ".stderr")).write_bytes(proc.stderr)
    require(proc.returncode == 0 and not proc.stderr, "replay failed: " + label)
    output = json.loads(proc.stdout)
    require(output.get("result") == "PASS", "non-PASS replay")
    return {"label": label, "command": command, "cwd": str(cwd),
            "returncode": proc.returncode, "stdout_sha256": sha(proc.stdout),
            "stderr_sha256": sha(proc.stderr), "native": output}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", type=Path, required=True)
    parser.add_argument("--python", type=str, required=True)
    parser.add_argument("--private-dir", type=Path, required=True)
    args = parser.parse_args()
    case = args.case.absolute()
    output = case / "publication_package"
    private = args.private_dir.absolute()
    require(private.is_relative_to(case / "private_sources/support_assembly"), "private path outside own scope")
    require(not private.exists(), "fresh private run directory required")
    private.mkdir(parents=True)
    inputs = {}
    for name, pin in PINS.items():
        inputs[name] = read_regular(case, name)
        require(sha(inputs[name]) == pin, "authenticated input pin changed: " + name)
    require(len(inputs["publication_package/paper/local_ricci_pinching_maxima.pdf"]) == 90558,
            "final PDF size changed")
    core = case / "verification_v2"
    whitelist = json.loads(inputs["verification_v2/PUBLICATION_WHITELIST.json"])
    core_entries = {e["path"]: e for e in whitelist["files"]}
    require(len(core_entries) == 71 and len(whitelist["files"]) == 71, "core positive count/duplicates")
    core_names = set(core_entries) | {"PUBLICATION_WHITELIST.json", "FINAL_SEAL.json"}
    require(len(core_names) == 73 and regular_tree(core) == core_names, "intact core inventory")
    support = {}
    origins = {}
    for name in sorted(core_names):
        data = read_regular(core, name)
        if name in core_entries:
            require(len(data) == core_entries[name]["bytes"] and sha(data) == core_entries[name]["sha256"],
                    "core payload changed")
        dest = "verification_v2/" + name
        support[dest] = data
        origins[dest] = "exact case/" + dest
    for name in SELECTED:
        dest = name if "/" in name else "acceptance/" + name
        require(dest not in support, "duplicate selected path")
        support[dest] = read_regular(case, name)
        origins[dest] = "exact case/" + name
    acceptance = json.loads(support["acceptance/SOFTWARE_GATE_ACCEPTANCE_V2.json"])
    require(acceptance["result"] == "PASS"
            and acceptance["actual_final_seal_sha256"] == PINS["verification_v2/FINAL_SEAL.json"]
            and acceptance["actual_whitelist_sha256"] == PINS["verification_v2/PUBLICATION_WHITELIST.json"],
            "actual parent v2 acceptance mismatch")
    support["README.md"] = SUPPORT_README.encode()
    origins["README.md"] = "authored support assembly README"
    support_manifest = {"schema": "pr411-support-positive-manifest-v1",
        "excluded_self": "SUPPORT_MANIFEST.json", "core_complete": "71 payloads plus authentic whitelist and seal",
        "outside_core_selection": "PARTIAL selection of complete artifacts; source/review corpora not included",
        "files": payload_rows(support, origins)}
    support["SUPPORT_MANIFEST.json"] = encoded(support_manifest)
    source = {"local_ricci_pinching_maxima.tex": inputs["publication_package/paper/local_ricci_pinching_maxima.tex"],
              "README.md": SOURCE_README.encode()}
    source_origins = {"local_ricci_pinching_maxima.tex": "exact case/publication_package/paper/local_ricci_pinching_maxima.tex",
                      "README.md": "authored source assembly README"}
    source["SOURCE_MANIFEST.json"] = encoded({"schema": "pr411-source-positive-manifest-v1",
        "excluded_self": "SOURCE_MANIFEST.json", "files": payload_rows(source, source_origins)})
    write_tree(output / "support", support)
    write_tree(output / "source_bundle", source)
    assets = output / "assets"
    assets.mkdir(exist_ok=True)
    expected_assets = {"local_ricci_pinching_maxima.pdf", "local_ricci_pinching_maxima_source.zip",
                       "local_ricci_pinching_maxima_verification.zip"}
    require(regular_tree(assets) <= expected_assets, "unexpected existing asset")
    source_zip, support_zip = zip_bytes(source), zip_bytes(support)
    require(source_zip == zip_bytes(source) and support_zip == zip_bytes(support), "nondeterministic ZIP")
    asset_data = {"local_ricci_pinching_maxima.pdf": inputs["publication_package/paper/local_ricci_pinching_maxima.pdf"],
                  "local_ricci_pinching_maxima_source.zip": source_zip,
                  "local_ricci_pinching_maxima_verification.zip": support_zip}
    write_tree(assets, asset_data)
    zip_checks = {"source": validate_zip(source_zip, source), "verification": validate_zip(support_zip, support)}
    extraction = private / "clean extraction with spaces"
    extract_checked(source_zip, source, extraction / "source")
    extract_checked(support_zip, support, extraction / "support")
    negative = negative_archive_tests(private)
    extracted = extraction / "support"
    replay = []
    for optimized in (False, True):
        mode = ["-B"] + (["-O"] if optimized else [])
        label = "core_" + ("optimized" if optimized else "normal")
        record = run([args.python] + mode + [str(extracted / "verification_v2/run_all.py")],
                     private, private, label)
        require(record["native"]["runtime_checkpoints"] == 54
                and record["native"]["positive_whitelist_files"] == 71, "core native count mismatch")
        replay.append(record)
        for script, result in [("exact_boundary_koszul.py", "exact_boundary_results"),
                               ("primary_Et_formula_check.py", "primary_Et_formula_results")]:
            label = script.removesuffix(".py") + "_" + ("optimized" if optimized else "normal")
            record = run([args.python] + mode + [str(extracted / "root_checks" / script)],
                         private, private, label)
            stored = json.loads(support["root_checks/" + result + "_" +
                                       ("optimized" if optimized else "normal") + ".json"])
            require(record["native"] == stored, "root native output differs from reviewed result")
            replay.append(record)
    require(regular_tree(extracted / "verification_v2") == core_names, "replay added core files")
    require(all(read_regular(case, name) == data for name, data in inputs.items()), "input changed during assembly")
    result = {"schema": "pr411-support-assembly-results-v1",
        "time_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "result": "PASS", "scope": "Local assembly/replay only; whole-package approval remains separate",
        "author_turns": "2/5", "new_author_proof_search_turns": 0,
        "core": {"positive_files": 71, "total_files": 73, "copied_exactly": True},
        "zip": zip_checks, "zip_serialization": "ZIP_STORED, sorted names, 1980-01-01 timestamp, regular 0644 mode, no extra/comment",
        "deterministic_rebuild_bytes": True, "safe_clean_extraction_with_path_spaces": True,
        "negative_archive_tests": negative, "source_manifest_sha256": sha(source["SOURCE_MANIFEST.json"]),
        "support_manifest_sha256": sha(support["SUPPORT_MANIFEST.json"]),
        "assets": payload_rows(asset_data, {n: "assembled reviewed asset" for n in asset_data}),
        "replays": replay, "root_inputs_unchanged": True,
        "private_runtime_raw_logs_fixtures_in_assets": False}
    (output / "SUPPORT_ASSEMBLY_RESULTS.json").write_bytes(encoded(result))
    print(json.dumps({"result": "PASS", "support_members": len(support), "source_members": len(source),
                      "assets": result["assets"], "replay_runs": len(replay),
                      "whole_package_approval": False}, indent=2))


if __name__ == "__main__":
    main()

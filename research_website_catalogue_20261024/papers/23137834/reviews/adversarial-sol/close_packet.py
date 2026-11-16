#!/usr/bin/env python3
"""Fixed-scope data-only custody and finite seal; no mathematical execution."""
import hashlib
import json
import stat
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER = HERE.parent.parent
SOURCE = PAPER / "sources"
EXPECTED = Path("/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23137834/reviews/adversarial-sol")
if HERE != EXPECTED:
    raise ValueError("Wrong owned folder")

def sha(data):
    return hashlib.sha256(data).hexdigest()

def pin(path, base):
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode):
        raise ValueError("Nonregular file: " + str(path))
    data = path.read_bytes()
    return dict(path=str(path.relative_to(base)), bytes=len(data),
                sha256=sha(data), mode=oct(stat.S_IMODE(info.st_mode)))

def inventory(base):
    files, dirs = [], []
    for path in sorted(base.rglob("*")):
        info = path.lstat()
        if stat.S_ISLNK(info.st_mode):
            raise ValueError("Symlink: " + str(path))
        if stat.S_ISDIR(info.st_mode):
            dirs.append(str(path.relative_to(base)))
        elif stat.S_ISREG(info.st_mode):
            files.append(pin(path, base))
        else:
            raise ValueError("Unexpected type: " + str(path))
    return files, dirs

def write(name, value):
    data = (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()
    path = HERE / name
    with path.open("xb") as handle:
        handle.write(data)
    return pin(path, HERE)

def load(name):
    return json.loads((HERE / name).read_text())

now = datetime.now(timezone.utc).isoformat()
initial = load("INITIAL_SEAL.json")
for expected in initial["payload_pins"]:
    if pin(HERE / expected["path"], HERE) != expected:
        raise ValueError("INITIAL payload changed: " + expected["path"])
initial_seal = pin(HERE / "INITIAL_SEAL.json", HERE)
if initial_seal["bytes"] != 3379 or initial_seal["sha256"] != "f761e06f635cf76dbdcec7fa11659623c5e72ecf906451713e73897602367e88":
    raise ValueError("INITIAL seal changed")
custody = load("SOURCE_CUSTODY.json")
source_files, source_dirs = inventory(SOURCE)
if source_files != custody["files"] or source_dirs != custody["directories"]:
    raise ValueError("Source boundary changed")
if (len(source_files), len(source_dirs)) != (97, 7):
    raise ValueError("Source extent mismatch")
cache = load("PRIMARY_CACHE_AUTH.json")
for item in cache["primaries"]:
    raw = Path(item["actual_raw_path"])
    actual = pin(raw, raw.parent)
    if (actual["bytes"], actual["sha256"]) != (item["bytes"], item["sha256"]):
        raise ValueError("Primary raw cache changed: " + item["name"])

programs = SOURCE / "published-source/container-001/tree/programs"
names = ["arithmetic.py", "division_finite.py", "geometry_source.py",
         "geometry_quotient.py", "division_model.py", "division_quintic.py",
         "geometry.py", "division_chord.py", "geometry_primitivity.py"]
code_pins = [pin(programs / name, SOURCE) for name in names]
source_arithmetic = (programs / "arithmetic.py").read_bytes()
if source_arithmetic != (HERE / "native-run/arithmetic.py").read_bytes():
    raise ValueError("Native owned copy differs")
execution = load("NATIVE_EXECUTION.json")
output = load("native-run/stdout.json")
if execution["ordinary_invocations"] != 1 or execution["actual_exit"] != 0 or execution["reruns"] != 0:
    raise ValueError("Unexpected native execution receipt")
if (HERE / "native-run/stderr.txt").read_bytes() != b"":
    raise ValueError("Native stderr changed")
if output["status"] != "PASS" or output["finite_field_fibers"] != 1364 or output["cover_fibers"] != 1364:
    raise ValueError("Unexpected native output")
if sum(output["categories"].values()) != 1364 or len(output["witnesses"]) != 6:
    raise ValueError("Finite output inventory mismatch")

write("CODE_READ.json", dict(timestamp_utc=now, whole_actual_bodies_read=code_pins,
    executed=["arithmetic.py"], ordinary_invocations=1,
    all_other_listed_programs="Static body reading only; not imported or executed",
    no_archived_result_REPORT_README_audit_or_acceptance_bodies_read=True,
    own_data_only_closure="This complete body read from disk before its sole execution"))
write("PRIMARY_READINGS.json", dict(timestamp_utc=now,
    raw_authentication="PRIMARY_CACHE_AUTH.json; seven actual cached PDFs, pins rechecked at close",
    fresh_live_byte_equivalence_claimed=False,
    passages=[
      dict(name="AIM", owned_text="primaries/aim.txt", lines="2428-2465",
           actual="Question 17 p.51, its remarks, incidental adjacent Question 18",
           limit="Not the whole workshop list; one current official URL open returned 404"),
      dict(name="Fisher", owned_text="primaries/fisher.txt", lines="185-242; 627-805; 1430-1490",
           actual="Lemma 1.1/Tate normal form; section 2 fine full-level moduli/quotient; Lemma 3.4 and proof",
           limit="Not the whole paper; printed Lemma 3.4 is over Q, base-change interface separately explained"),
      dict(name="Verdure", owned_text="primaries/verdure.txt", text_extraction="18 formfeed characters, no readable body",
           actual="Ten personally viewed scanned pages: physical 5-14, printed 79-88; Proposition 3, Corollaries, Theorem 5 and its decisive proof; incidental adjacent 3/7 torsion formulas",
           images="primaries/verdure-pages/page-05.png through page-14.png",
           limit="Printed 75-78 and 89-92 not read; general resolvent prelude not wholly read",
           display_receipt="Over-budget call not counted; physical 5-8 re-viewed in two bounded calls"),
      dict(name="Morton v4", owned_text="primaries/morton_v4.txt", lines="1-462",
           actual="Introduction, section 2 table/radical/Theorem 2.1 and proof, Theorem 3.1/doubling proof and tail; start of section 4",
           limit="Not later continued-fraction sections; 426-462 reread after display-budget truncation"),
      dict(name="Morton v1", owned_text="primaries/morton_v1.txt", lines="1-58; 104-183",
           actual="Version header/abstract and early residual table/radical/Theorem 2.1 opening",
           limit="Not the full v1 proof or paper; no live version-identity claim"),
      dict(name="Sutherland Lecture 5", owned_text="primaries/sutherland5.txt", lines="538-710; 810-833",
           actual="Division-polynomial definitions/recurrences/Theorem 5.21 proof and separability/degree Theorem 5.25",
           limit="Intervening degree-lemma proof not wholly read; other lecture material unread"),
      dict(name="Sutherland Lecture 23", owned_text="primaries/sutherland23.txt", lines="635-708",
           actual="Theorem 23.29 pairing properties/proof, Corollaries 23.30-31",
           limit="Not the whole lecture")],
    current_root_peer_findings_opened=False, scope_findings_opened=False,
    no_priority_or_current_open_status_certification=True))
write("RESULT_INSPECTION.json", dict(timestamp_utc=now,
    literal_stdout_pin=pin(HERE / "native-run/stdout.json", HERE),
    literal_stderr_pin=pin(HERE / "native-run/stderr.txt", HERE),
    whole_stdout_personally_read=True, actual_exit=0, ordinary_invocations=1,
    output=output, independent_interpretation="POST_INITIAL_DERIVATIONS.md final section",
    counts_are_implementation_checks_not_independent_theorems=True,
    no_second_run_no_mutant_no_harness_no_environment_install=True,
    limits="One ordinary arithmetic route only; static other-code reading is not a run receipt"))
write("CLOSING_CUSTODY.json", dict(timestamp_utc=now,
    initial13payloads_plus_seal_unchanged=True, initial_seal=initial_seal,
    source97files7dirs_all_paths_bytes_modes_unchanged=True,
    source_boundary_pin=pin(HERE / "SOURCE_CUSTODY.json", HERE),
    source_regular_files=len(source_files), source_child_directories=len(source_dirs),
    raw_primary7pins_unchanged=True, native_source_and_copy_exact=True,
    new_scientific_handles_running=0, completion_percent_estimate=100,
    follow_up=None, parent_handoff="Readiness/pins/extent only; findings closed",
    no_source_W_Git_Sheet_Zenodo_release_or_external_contact_actions=True))

files, dirs = inventory(HERE)
if any(item["path"] in ("MANIFEST.json", "FINAL.json") for item in files):
    raise ValueError("Existing final seal; no retry")
manifest = write("MANIFEST.json", dict(schema="whole-owned-finite-payload-manifest-v1",
    timestamp_utc=now, payload_regular_files=len(files), payload_pins=files,
    child_directories=dirs, self_and_FINAL_excluded=True))
expected_names = sorted([item["path"] for item in files] + ["MANIFEST.json", "FINAL.json"])
final = write("FINAL.json", dict(schema="scientific-adversarial-final-v1",
    timestamp_utc=now, status="FROZEN_COMPLETE", disposition="PASS_FULL_ORIGINAL",
    record="23137834", row=170,
    reviewed_original="Full 5-torsion of the regular-pentagon quintic pencil",
    report=pin(HERE / "REPORT.md", HERE),
    post_initial_derivations=pin(HERE / "POST_INITIAL_DERIVATIONS.md", HERE),
    immutable_INITIAL_seal=initial_seal, manifest=manifest,
    exact_extent=dict(regular_files=len(expected_names), child_directories=len(dirs),
                      files=expected_names, directories=dirs),
    source_regular_files=97, source_child_directories=7, source_unchanged=True,
    native_ordinary_invocations=1, actual_native_exit=0,
    strongest_verified_result="Original characteristic-zero geometry, complete kernel and exact division-field theorem with its original field and parameter boundaries",
    substantive_remaining_gap=None, repaired_or_narrowed_substitute=False,
    follow_up=None, completion_percent_estimate=100,
    limitations=["Ordinary mathematical checking, not formal proof-assistant certification",
      "One native arithmetic route; no claim all scripts were reproduced",
      "Selected actual cached primary passages, not whole papers or a new priority survey",
      "No independent external human review or publication authority"],
    root_peer_findings_unread=True, findings_closed_to_parent=True,
    raw_only_family_coordination=True, owned_work_quiescent_after_seal=True,
    self_hash_excluded=True))
actual_files, actual_dirs = inventory(HERE)
if [item["path"] for item in actual_files] != expected_names or actual_dirs != dirs:
    raise ValueError("Final finite extent differs")
print(json.dumps(dict(final=final, manifest=manifest,
                     regular_files=len(actual_files), child_directories=len(actual_dirs),
                     quiescent=True), indent=2))

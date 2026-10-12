#!/usr/bin/env python3
"""Read-only review evidence verifier; no reruns, installs or network."""
import argparse, hashlib, json, sys, zipfile
from pathlib import Path, PurePosixPath
PUB = Path(__file__).resolve().parent
BASE = PUB.parent
def need(value, why):
    if not value:
        raise ValueError(why)
def binding(p):
    b = p.read_bytes()
    return {"bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
def read(p):
    return json.loads(p.read_text(encoding="utf-8"))
def files(p):
    out = {}
    for q in sorted(p.rglob("*")):
        need(not q.is_symlink(), "symlink: " + str(q))
        if q.is_file():
            out[q.relative_to(p).as_posix()] = binding(q)
    return out
def validate(p, pins):
    for name, pin in pins.items():
        n = PurePosixPath(name)
        need(not n.is_absolute() and ".." not in n.parts, "unsafe manifest path")
        need(binding(p / name) == pin, "binding mismatch: " + name)
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--include-external", action="store_true")
    args = ap.parse_args()
    need(not args.include_external or args.full, "external mode requires --full")
    final = (PUB / "PUBLIC_MANIFEST.json").exists()
    if final:
        public = read(PUB / "PUBLIC_MANIFEST.json")["files"]
    else:
        public = read(BASE / "PRE_CLOSURE.json")["public_files"]
    validate(PUB, public)
    actual_public = files(PUB)
    if final:
        actual_public.pop("PUBLIC_MANIFEST.json")
    need(actual_public == public, "public exact inventory mismatch")
    default = (PUB / "DEFAULT_PACKAGE.stdout").read_bytes()
    full = (PUB / "FULL_PACKAGE.stdout").read_bytes()
    own = (PUB / "INDEPENDENT_LITERAL_CHECKS.json").read_bytes()
    for data, count, sha in [
        (default, 1586, "cef38ef1a41ebcd26f090f73ef2991e2dbf8d6022c68c0f202d0f959e675fd9e"),
        (full, 2960, "9555386bf072f272e069bfec19c3cc665c9ace49486d6772069fc3a1171f73d4"),
        (own, 1443, "3f5defdd0d8ba115fadf6449a101345265cf97d416015f391f69c53c93083a78")]:
        need(len(data) == count and hashlib.sha256(data).hexdigest() == sha,
             "whole public native stream mismatch")
    for data, mode, count in [(default, "integrity", 4), (full, "full", 10)]:
        j = json.loads(data)
        need(j["status"] == "PASS" and j["mode"] == mode
             and j["payload_files_checked"] == 68 and j["submitted_files_checked"] == 16
             and j["package_bytes_unchanged"] and len(j["runs"]) == count,
             "wrapper scope")
        need(all(r["exit_code"] == 0 and r["whole_expected_stdout_equal"]
                 for r in j["runs"]), "wrapper native receipt")
    literal = json.loads(own)
    need(literal["status"] == "pass", "literal status")
    totals = [sum(m[k] for m in literal["models"]) for k in
              ["words", "extension_equivalences", "theorem_instances", "exact_threshold_instances"]]
    need(totals == [14062, 89984, 22232, 14496], "literal totals")
    need(all(literal[k] for k in ["general_period_definition_mutant_rejected",
             "ordinary_gcd_mutant_rejected", "orientation_mutant_rejected",
             "uniform_sharpness_checked"]), "mutant controls")
    checked = len(public)
    external = 0
    if args.full:
        if final:
            closure = read(BASE / "CLOSURE.json")
            need(binding(PUB / "PUBLIC_MANIFEST.json") == closure["public_manifest"], "public seal")
            need(binding(BASE / "PRIVATE_MANIFEST.json") == closure["private_manifest"], "private seal")
            pins = read(BASE / "PRIVATE_MANIFEST.json")["files"]
            validate(BASE, pins)
            actual = files(BASE)
            actual.pop("PRIVATE_MANIFEST.json")
            actual.pop("CLOSURE.json")
            need(actual == pins, "final whole namespace inventory")
            checked = len(pins)
        else:
            proposal = read(BASE / "PRE_CLOSURE.json")
            pins = proposal["files"]
            validate(BASE, pins)
            actual = files(BASE)
            actual.pop("PRE_CLOSURE.json")
            extras = set(actual) - set(pins)
            need(extras <= set(proposal["terminal_capture_allowlist"]), "unplanned file before closure")
            need({k:v for k,v in actual.items() if k in pins} == pins, "preclosure exact payload tree")
            checked = len(pins)
        gate = read(BASE / "source_first_gate.json")
        for item in gate["artifact_hashes"]:
            name = item["path"]
            if name == "research_log.md":
                name = "source_private/research_log_at_source_gate.md"
            need(binding(BASE / name) == {k:item[k] for k in ["bytes", "sha256"]},
                 "immutable source-first gate payload")
        freeze = read(BASE / "analytic_freeze.json")
        need(binding(BASE / freeze["artifact"])["sha256"] == freeze["sha256"], "analytic freeze")
        need(not any(freeze[k] for k in ["included_prior_audit_or_control_code_seen",
             "deposit_metadata_content_seen", "zip_member_content_seen"]), "early independence declaration")
        released = read(BASE / "candidate_release_record.json")
        for name, sha in released["candidate_pins"].items():
            need(binding(BASE / "candidate_private" / name)["sha256"] == sha, "released candidate")
        zpath = BASE / "candidate_private/alternating-antimorphic-verification.zip"
        with zipfile.ZipFile(zpath) as z:
            prefix = "alternating-antimorphic-verification/"
            members = {}
            for i in z.infolist():
                if i.is_dir():
                    continue
                need(i.filename.startswith(prefix), "ZIP prefix")
                name = i.filename[len(prefix):]
                n = PurePosixPath(name)
                need(not n.is_absolute() and ".." not in n.parts and name not in members,
                     "ZIP path or duplicate")
                need((i.external_attr >> 16) & 0o170000 != 0o120000, "ZIP symlink")
                data = z.read(i)
                members[name] = {"bytes":len(data), "sha256":hashlib.sha256(data).hexdigest()}
            need(len(members) == 69, "ZIP count")
        audit = read(BASE / "every_file_audit.json")
        need(audit["members"] == 69 and audit["payloads"] == 68, "every-file audit")
        need({r["path"]:{k:r[k] for k in ["bytes","sha256"]} for r in audit["files"]}
             == members, "every-file ZIP bindings")
        for label, public_data in [("default", default), ("full", full), ("independent_literal", own)]:
            cap = BASE / "execution_private"
            before = read(cap / (label + ".before.json"))
            after = read(cap / (label + ".after.json"))
            need(before["package_pins"] == members and before["optimization"] == 0, "native prepins")
            for name, pin in before["candidate_pins"].items():
                need(binding(BASE / "candidate_private" / name) == pin, "native candidate prepins")
            need(binding(BASE / "controls/run_native.py") == before["runner"], "capture runner")
            need(binding(cap / (label + ".before.json")) == after["before_record"], "native before binding")
            need(binding(cap / (label + ".stdout")) == after["stdout"]
                 and binding(cap / (label + ".stderr")) == after["stderr"], "native whole stream bindings")
            need((cap / (label + ".stdout")).read_bytes() == public_data
                 and (cap / (label + ".stderr")).read_bytes() == b"", "whole public/private output")
            need(after["exit_code"] == 0 and after["package_tree_unchanged"]
                 and after["whole_stdout_byte_equal"], "native successful execution receipt")
            if label != "independent_literal":
                need((cap / (label + ".expected.stdout")).read_bytes() == public_data
                     and binding(cap / (label + ".expected.stdout")) == before["expected_stdout"],
                     "whole independently expected stream")
            else:
                need(binding(BASE / "controls/independent_literal_controls.py")
                     == before["independent_program_pin"], "literal prepin")
        need((PUB / "independent_literal_controls.py").read_bytes()
             == (BASE / "controls/independent_literal_controls.py").read_bytes(), "public own code copy")
        if args.include_external:
            refs = read(BASE / "references_private/primary_bindings.json")
            for r in refs["references"]:
                need(binding(Path(r["path"])) == {k:r[k] for k in ["bytes","sha256"]}, "external source binding")
                external += 1
            for name, sha in released["candidate_pins"].items():
                need(binding(BASE.parent / "preprint" / name)["sha256"] == sha, "external current candidate")
                external += 1
            need(binding(Path(gate["official_source"]["path"]))
                 == {k:gate["official_source"][k] for k in ["bytes","sha256"]}, "external original source")
            external += 1
    if args.full and final:
        for label in ["public", "full"]:
            cap = BASE / "verification_private"
            before = read(cap / (label + ".before.json"))
            after = read(cap / (label + ".after.json"))
            need(before["proposal"] == binding(BASE / "PRE_CLOSURE.json")
                 and before["verifier"] == binding(PUB / "verify_review.py")
                 and before["runner"] == binding(BASE / "controls/capture_review.py")
                 and before["optimization"] == 0, "terminal verification prepins")
            need(after["before"] == binding(cap / (label + ".before.json"))
                 and after["stdout"] == binding(cap / (label + ".stdout"))
                 and after["stderr"] == binding(cap / (label + ".stderr")), "terminal stream bindings")
            need(after["exit_code"] == 0 and after["whole_namespace_unchanged_during_verifier"]
                 and (cap / (label + ".stderr")).read_bytes() == b"", "read-only verifier receipt")
            result = read(cap / (label + ".stdout"))
            need(result["status"] == "PASS" and result["mode"] == label
                 and result["state"] == "preclosure" and result["read_only"]
                 and not result["mathematical_reruns"], "terminal complete output")
            need(result["external_files_checked"] == (10 if label == "full" else 0),
                 "terminal external scope")
    print(json.dumps({"status":"PASS", "mode":"full" if args.full else "public",
          "state":"closed" if final else "preclosure", "files_bound":checked,
          "external_files_checked":external, "whole_default_bytes":len(default),
          "whole_full_bytes":len(full), "literal_totals":totals,
          "read_only":True, "mathematical_reruns":False, "network_or_installs":False}, indent=2))
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(json.dumps({"status":"FAIL", "error":str(e)}), file=sys.stderr)
        raise SystemExit(1)


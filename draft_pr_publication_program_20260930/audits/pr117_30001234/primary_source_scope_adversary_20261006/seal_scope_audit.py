#!/usr/bin/env python3
"""Run owned scope controls and seal metadata, without publishing or Git writes."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

BASE = Path(__file__).resolve().parent
ORIGINAL = BASE.parent / "original_head_authentication_20261006"
PYTHON = "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14"


def pin(path):
    b = path.read_bytes()
    return {"path": str(path.relative_to(BASE)) if path.is_relative_to(BASE) else str(path),
            "byte_count": len(b), "sha256": hashlib.sha256(b).hexdigest()}


def save(name, obj):
    (BASE / name).write_text(json.dumps(obj, indent=2) + "\n")


utc = datetime.now(timezone.utc).isoformat()
receipt = {"started_utc": utc, "parent_pid": os.getpid(), "runs": []}
env = {"PATH": "/usr/bin:/bin", "LC_ALL": "C", "LANG": "C", "TZ": "UTC",
       "__CF_USER_TEXT_ENCODING": "0x1F5:0x0:0x0"}
for optimized in (False, True):
    for false_control in (False, True):
        args = [PYTHON, "-E", "-S", "-B", "-P"]
        if optimized:
            args.append("-O")
        args.append(str(BASE / "source_scope_controls.py"))
        if false_control:
            args.append("--force-failure")
        child = subprocess.Popen(args, cwd=BASE, env=env,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = child.communicate(timeout=30)
        suffix = ("optimized" if optimized else "normal") + ("_false_guard" if false_control else "")
        (BASE / (suffix + ".stdout.txt")).write_bytes(out)
        (BASE / (suffix + ".stderr.txt")).write_bytes(err)
        run = {"arguments": args, "child_pid": child.pid, "exit_code": child.returncode,
               "optimized": optimized, "false_guard_control": false_control,
               "stdout": pin(BASE / (suffix + ".stdout.txt")),
               "stderr": pin(BASE / (suffix + ".stderr.txt"))}
        receipt["runs"].append(run)
        save("CONTROL_PROCESS_RECEIPT.json", receipt)
        if false_control:
            if child.returncode == 0 or b"Deliberate false guard" not in err:
                raise ValueError("False guard did not fail explicitly")
        else:
            if child.returncode != 0 or err:
                raise ValueError("Scope controls failed")
            result = json.loads(out)
            if result.get("checks") != 810 or result.get("status") != "PASS":
                raise ValueError("Unexpected success result")
receipt["finished_utc"] = datetime.now(timezone.utc).isoformat()
receipt["all_success_and_false_guard_controls_passed"] = True
save("CONTROL_PROCESS_RECEIPT.json", receipt)

source_entries = json.loads((BASE / "RETRIEVAL_RECEIPT.json").read_text())["sources"]
ranges = {
    "owr21_2009.pdf": {"text_read": "Complete Takagi contribution, printed1136–1139 / physical36–39",
                        "visual_read": "Printed1137–1139; complete decisive300dpi hypotheses, constraint/quantifier and Question8 crops",
                        "observations": {"field": "characteristic zero", "ambient_ring": "polynomial ring",
                                         "exponent_domain": "nonnegative integer vectors excluding the zero vector",
                                         "coefficient_domain": "nonzero field elements", "lp_constraint": "nonstrict<=",
                                         "lp_coordinates": "nonnegative rationals", "hypothesis": "exists an optimal singleton augmented-image fiber",
                                         "question_additions": "no monomial and minimal binomial generators"}},
    "shibuta_takagi_0810.1278v3.pdf": {"text_read": "All sixteen pages; complete Prop2.1 proof6–8, Q2.2 p8, Thm2.4 proof8–10, Thm3.1 scope10–14, Example3.2 pp14–15",
                                      "visual_read": "Full pp6,8,9 at220dpi; separate decisive300dpi constraint/quantifier, question and complete regular-sequence hypothesis crops",
                                      "observations": {"lp_constraint": "nonstrict<=", "lp_coordinates": "nonnegative rationals",
                                                       "hypothesis": "exists an optimal singleton augmented-image fiber",
                                                       "regular_sequence": "additional condition of Theorem2.4, not Question2.2",
                                                       "Laurent_ring": "proof device in Theorem2.4, not target minimality ring",
                                                       "space_curve": "specialized canonical numerical-semigroup ideal in three polynomial variables"}},
    "laclair_2304.13299v2.pdf": {"text_read": "pp3,9–11,14; exact subset definition, LP8, biconnected variant, Remark3.15",
                               "visual_read": "Full pp9 and14 at220dpi; LP8 constraints at300dpi",
                               "observations": {"full_subset": "U={1,2,3} is allowed",
                                                "extra_bound": "sum over all triangle edge weights<=2",
                                                "candidate_total": "3; excluded by modified LP",
                                                "novelty_implication": "none authenticated"}}
}
manifest_sources = []
for source in source_entries:
    body = BASE / "private_sources" / source["name"]
    body_pin = pin(body)
    if body_pin["byte_count"] != source["byte_count"] or body_pin["sha256"] != source["sha256"]:
        raise ValueError("Retrieved source changed before seal")
    manifest_sources.append({**source, **ranges[source["name"]],
                             "classification": "private copyright-bearing reference; exclude body, text and renders from public package"})

private_pins = [pin(p) for folder in (BASE / "private_sources", BASE / "private_renders")
                for p in sorted(folder.iterdir()) if p.is_file()]
original_pins = [pin(ORIGINAL / "original_attempt" / name)
                 for name in ("CANDIDATE.md", "source_record.json")]
original_pins.append(pin(ORIGINAL / "PRIOR_REPORT.json"))
if json.loads((ORIGINAL / "PRIOR_REPORT.json").read_text()) != {}:
    raise ValueError("Prior report is not the authenticated empty object")
save("SOURCE_MANIFEST.json", {"utc": datetime.now(timezone.utc).isoformat(),
                             "original_head": "8163ee0dc7a0f944570925984cef2dc0fb291ad8",
                             "review_inputs": original_pins, "primary_sources": manifest_sources,
                             "private_artifact_pins": private_pins,
                             "source_gaps": ["Published Shibuta–Takagi full body not retrieved; use exact authenticated v3 and official OWR target.",
                                             "Published2025 LaClair version not authenticated; modified-LP claim verified against actual v2.",
                                             "Blanco–Encinas contextual procedure not read in this bounded source audit; no dependence in counterexample."],
                             "broad_priority_search_performed": False,
                             "outside_contact": False, "copyright_bodies_public": False})
save("RESULT.json", {"utc": datetime.now(timezone.utc).isoformat(),
                     "status": "PASS", "scope_gate_percent": 100,
                     "mandatory_source_scope_findings": [],
                     "strongest_verified_result": "Candidate is a literal full negative answer to OWR21/2009 Question8 and arXiv0810.1278v3 Question2.2's existential augmented-image condition.",
                     "proof_search_turns_added": 0, "original_effort": "1/5",
                     "scope_controls": {"guards_each_mode": 810, "rational_parameters": 81,
                                        "cyclic_grid_controls": 125, "normal_and_optimized_pass": True,
                                        "normal_and_optimized_false_guards_fail": True},
                     "novelty_clearance": False, "publication_clearance": False,
                     "math_gate_dependencies": "Other independent algebra/LP families and root adjudication remain responsible for full gate.",
                     "review_inputs": original_pins,
                     "sources": [{"name": x["name"], "sha256": x["sha256"], "byte_count": x["byte_count"]}
                                 for x in manifest_sources]})
with (BASE / "RESEARCH_LOG.md").open("a") as log:
    log.write("\n" + datetime.now(timezone.utc).isoformat() + " — Source audit100% complete. Complete exact primary target, hypotheses, quantifiers, localization boundary and modified-LP distinction verified independently. Mandatory scope findings none. Normal/-O each810 guards pass; deliberate false guards fail in both. Novelty/publication not evaluated. Only owned files written; originals and Git/services untouched.\n")

public = [p for p in sorted(BASE.iterdir()) if p.is_file()
          and p.name not in ("OUTPUT_MANIFEST.json", "SHA256SUMS")]
if any(p.suffix in (".pdf", ".png") for p in public):
    raise ValueError("Private source body escaped public scope")
pins = [pin(p) for p in public]
save("OUTPUT_MANIFEST.json", {"utc": datetime.now(timezone.utc).isoformat(),
                             "scope": "Public own reasoning, guard code, actual execution receipts and source metadata only",
                             "files": pins, "file_count": len(pins),
                             "private_excluded_directories": ["private_sources", "private_renders"],
                             "gate_status": "source_scope_PASS_only", "novelty_clearance": False})
(BASE / "SHA256SUMS").write_text("".join(x["sha256"] + "  " + x["path"] + "\n" for x in pins))
print(json.dumps({"status": "PASS", "public_file_count": len(pins),
                  "manifest": pin(BASE / "OUTPUT_MANIFEST.json"),
                  "report": pin(BASE / "REPORT.md"), "result": pin(BASE / "RESULT.json")}, indent=2))

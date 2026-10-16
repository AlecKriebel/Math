#!/usr/bin/env python3
"""Replay exact controls and seal artifacts; writes only this dedicated folder."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import platform
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/"original_submission/files/unsolved_math_prioritization/attempts/30000229"
HEAD="58bee8514677549ee5a7cd699028a5f3a616c5bc"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run(args,label):
    env=dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"]="1"
    p=subprocess.run(args,cwd=ROOT,env=env,text=True,capture_output=True)
    (ROOT/(label+".stdout.txt")).write_text(p.stdout)
    (ROOT/(label+".stderr.txt")).write_text(p.stderr)
    return {"argv":args,"cwd":str(ROOT),"exit_code":p.returncode,
            "stdout_path":str(ROOT/(label+".stdout.txt")),
            "stderr_path":str(ROOT/(label+".stderr.txt"))},p

commands=[]
for optimized,label in [(False,"normal_run"),(True,"optimized_run")]:
    args=[sys.executable]+(["-O"] if optimized else [])
    args += [str(ROOT/"independent_exact_controls.py"),
             str(ROOT/("controls_optimized.json" if optimized else "controls_normal.json"))]
    record,p=run(args,label)
    commands.append(record)
    if p.returncode!=0:
        raise RuntimeError("Exact controls failed: "+label)

normal=json.loads((ROOT/"controls_normal.json").read_text())
optimized=json.loads((ROOT/"controls_optimized.json").read_text())
for key in normal:
    if key!="python_optimized" and normal[key]!=optimized.get(key):
        raise RuntimeError("Normal/-O mathematical output mismatch: "+key)

checker=ROOT/"independent_exact_controls.py"
bad=ROOT/"negative_mutant_correction_19.py"
text=checker.read_text()
needle="def bubble(a, b, correction=20):"
if text.count(needle)!=1:
    raise RuntimeError("Mutation target missing or ambiguous")
bad.write_text(text.replace(needle,"def bubble(a, b, correction=19):",1))
negative_runs=[]
for optimized_mode,label in [(False,"negative_mutant_normal"),(True,"negative_mutant_optimized")]:
    args=[sys.executable]+(["-O"] if optimized_mode else [])
    args += [str(bad),str(ROOT/(label+"_unexpected_output.json"))]
    record,p=run(args,label)
    commands.append(record)
    passed=(p.returncode!=0 and '"name": "bubble_01_corrected_mean"' in p.stderr
            and '"actual": "1/120"' in p.stderr and '"expected": "0"' in p.stderr)
    if not passed:
        raise RuntimeError("Wrong-correction mutant was not rejected as expected: "+label)
    negative_runs.append({"mode":"-O" if optimized_mode else "normal",
                          "rejected_as_expected":True,"exit_code":p.returncode,
                          "failure":"bubble_01_corrected_mean actual1/120 expected0"})
(ROOT/"negative_mutation_results.json").write_text(json.dumps({
    "status":"PASS","source_sha256":sha(checker),"mutant_sha256":sha(bad),
    "mutation":"default cubic correction changed from20 to19",
    "runs":negative_runs},indent=2)+"\n")

utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
result={
    "problem_id":30000229,"problem_number":"OWR-829-001","pr":154,
    "original_head":HEAD,"review_utc":utc,"completion_estimate_percent":100,
    "original_effort":"2/5 preserved","status":"MATHEMATICAL_PASS_WITH_ANCILLARY_REPAIRS",
    "review_kind":"initial mathematics; not publication clearance",
    "historical_independent_review_read":False,
    "original_claim_verified":"u in A^(1/2); actual best P0 H^-1 error not O(N^-1/2) on the stated NVB family",
    "strongest_verified_claim":{
        "C1":"1+6*C_comp, C_comp>=1 is the fixed compatible-NVB conforming-completion constant",
        "subsequence":"E_(4^n)(f) >= n*2^(-n)/(6*sqrt(C1)) for all n>=1",
        "all_budgets":"E_N(f) >= log(N)/(12*log(4)*sqrt(C1)*sqrt(N)) for all integers N>=4",
        "mechanism":"selected fine-edge bubble patches stay in levels<=n, so the infinite tail pairs exactly to zero",
        "submission_relation":"separate stronger review deduction; original reverse-triangle proof remains valid"
    },
    "all_mesh_bridge_verified":True,"arbitrary_P0_coefficients_annihilated":True,
    "global_H10_validity_verified":True,"edge_cancellation_failure_found":False,
    "unresolved_central_mathematical_gap":None,
    "external_theorem_dependencies":[
        "compatible-NVB linear conforming completion, CDN Lemma2.1/(2.2)",
        "same-master-forest overlay bound, CDN(2.4)"
    ],
    "ancillary_repairs":[
        {"item":"literal fill bisections","incorrect":"3*4^j",
         "correct":"4*(4^j-1)","impact":"no change to O(4^n) or bound6*4^n"},
        {"item":"only micro-square-interior edges have nonzero jumps",
         "correct":"additional square-boundary jumps can be nonzero",
         "impact":"submitted selected-segment proof does not rely on the false source sentence"},
        {"item":"original verifier relies on asserts",
         "correct":"this independent checker uses explicit raised-error checks",
         "impact":"normal and -O both execute all checks; original source left unchanged"}
    ],
    "controls":{"normal":"PASS","optimized":"PASS",
        "explicit_checks_each":normal["explicit_check_count"],
        "negative_controls_each":normal["negative_control_count"],
        "mutant_rejection_normal_and_optimized":True,"checker_sha256":sha(checker),
        "finite_controls_replace_universal_proof":False},
    "negative_stronger_claim_counterexamples":[
        "boundary deltas vanish on H10, invalidating a boundary-edge extension",
        "8-triangle anisotropic strip: edge weight1, H^-1 error squared<=epsilon/6"
    ],
    "exact_remaining_nonpromotion_gaps":[
        "novelty and publication priority not established",
        "complete present literature status not established",
        "no matching upper bound for actual best P0 error",
        "no extension to unrelated triangulations or unbounded shape constants",
        "no negative answer for every fixed s<1/2",
        "new whole-package review required after promotion or substantive edits"
    ],
    "mutations":{"outside_dedicated_folder":False,"MAIN":False,"Git":False,
        "index":False,"PR":False,"tracker":False,"publication":False},
    "external_individual_communication":False,
    "original_input_sha256":{name:sha(SOURCE/name) for name in
                             ["COUNTEREXAMPLE.md","README.md","source_record.json","verify.py"]},
    "manifest":"INPUT_OUTPUT_MANIFEST.json","detailed_review":"REVIEW.md"
}
(ROOT/"RESULT.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")

inputs=[{"path":str(SOURCE/name),"sha256":sha(SOURCE/name),"bytes":(SOURCE/name).stat().st_size}
        for name in ["COUNTEREXAMPLE.md","README.md","source_record.json","verify.py"]]
remote_inputs=[
    {"url":"https://math.umd.edu/~rhn/papers/pdf/afemH-1.pdf",
     "saved_pdf":str(ROOT/"primary_cdn.pdf"),"sha256":sha(ROOT/"primary_cdn.pdf"),
     "extracted_text":str(ROOT/"primary_cdn.txt"),"text_sha256":sha(ROOT/"primary_cdn.txt"),
     "content_read":"Section2 and Section6.4; download read-only"},
    {"url":"https://ems.press/content/serial-article-files/45998?nt=1",
     "saved_pdf":str(ROOT/"primary_owr24_2005.pdf"),"sha256":sha(ROOT/"primary_owr24_2005.pdf"),
     "extracted_text":str(ROOT/"primary_owr24_2005.txt"),"text_sha256":sha(ROOT/"primary_owr24_2005.txt"),
     "content_read":"Stevenson contribution printed pp1306-1307, including web PDF text"}]
manifest={"schema":"independent-research-input-output-manifest-v1","sealed_utc":utc,
    "original_head":HEAD,"root":str(ROOT),"filesystem_inputs":inputs,
    "primary_remote_inputs":remote_inputs,
    "instruction_inputs":["user-supplied AGENTS.md context for /Users/alec/Documents/Math",
                          "parent subagent task and subsequent internal coordination"],
    "historical_reviews":{"content_read":False,
        "file_names_seen_only_in_initial_rg_inventory":True},
    "environment":{"python_executable":sys.executable,"python_version":sys.version,
                   "platform":platform.platform(),"bytecode_writes_disabled":True},
    "commands":commands,
    "earlier_read_only_preparation_commands":[
        "rg --files of original submission (inventory only)",
        "cat of four original input files",
        "curl --fail --location --max-time30 of the two primary PDFs, outputs within ROOT",
        "pdftotext -layout of both primary PDFs, outputs within ROOT",
        "targeted rg and sed reads of primary_cdn.txt",
        "python3 import sympy diagnostic: module unavailable; independent checker uses stdlib"
    ],
    "outputs":[{"path":str(p),"sha256":sha(p),"bytes":p.stat().st_size}
               for p in sorted(ROOT.iterdir()) if p.is_file() and p.name!="INPUT_OUTPUT_MANIFEST.json"],
    "manifest_self_hash":"omitted to avoid recursive hashing; all other output bytes are hashed",
    "mutation_boundary":"only dedicated folder writes; original inputs retained unchanged"}
(ROOT/"INPUT_OUTPUT_MANIFEST.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
print(json.dumps({"status":result["status"],"normal_and_optimized_checks":normal["explicit_check_count"],
    "negative_controls_each":normal["negative_control_count"],"mutants_rejected":2,
    "output_files_hashed":len(manifest["outputs"]),"sealed_utc":utc},sort_keys=True))

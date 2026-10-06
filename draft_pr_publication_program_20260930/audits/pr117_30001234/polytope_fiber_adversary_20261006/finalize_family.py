from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os

HERE=Path(__file__).resolve().parent
ORIGINAL=HERE.parent/"original_head_authentication_20261006"/"original_attempt"
inputs=json.loads((HERE/"INPUT_PINS.json").read_text())
for name,pin in inputs["input_pins"].items():
    body=(ORIGINAL/name).read_bytes()
    if len(body)!=pin["bytes"] or hashlib.sha256(body).hexdigest()!=pin["sha256"]:
        raise RuntimeError("Candidate/source record changed")
checkpoint=json.loads((HERE/"INDEPENDENCE_CHECKPOINT.json").read_text())
for name,pin in checkpoint["files"].items():
    body=(HERE/name).read_bytes()
    if len(body)!=pin["bytes"] or hashlib.sha256(body).hexdigest()!=pin["sha256"]:
        raise RuntimeError("Independent construction body changed after comparison")
run=json.loads((HERE/"RUN_RECEIPT.json").read_text())
comparison=json.loads((HERE/"ORIGINAL_COMPARISON_RECEIPT.json").read_text())
if run["status"]!="PASS" or comparison["status"]!="PASS":
    raise RuntimeError("Passed receipts required")
for name,pin in comparison["input_pins"].items():
    body=(ORIGINAL/name).read_bytes()
    if len(body)!=pin["bytes"] or hashlib.sha256(body).hexdigest()!=pin["sha256"]:
        raise RuntimeError("Original comparison input changed")
stamp=datetime.now(timezone.utc).isoformat()
result={
    "verdict":"PASS_AUGMENTED_POLYTOPE_AND_UNIVERSAL_FIBER_COUNTEREXAMPLE",
    "completed_utc":stamp,"finalizer_pid":os.getpid(),
    "original_head":inputs["original_head"],
    "candidate_sha256":inputs["input_pins"]["CANDIDATE.md"]["sha256"],
    "source_record_sha256":inputs["input_pins"]["source_record.json"]["sha256"],
    "mandatory_mathematical_findings":[],
    "polytope_vertices":15,"exact_active_bases":5005,"nonsingular_bases":1792,
    "rank":5,"kernel_generator":[1,1,1,-1,-1,-1],"optimal_value":"3",
    "optimal_face":"(t,t,t,1-t,1-t,1-t), t rational in [0,1]",
    "optimal_image":[1]*9,"all_optimal_fibers_nonsingleton":True,
    "normal_and_optimized_explicit_guards_each":1729,
    "independent_children":[r["pid"] for r in run["children"]],
    "original_normal_assertions":[3045,5368],
    "original_reproduction_children":[r["pid"] for r in comparison["children"]],
    "original_receipts_byte_identical":True,"originals_unchanged":True,
    "original_optimized_validity_claim":False,
    "original_effort_turns":1,"new_central_proof_search_turns":0,
    "mathematical_family_completion_percent":100,
    "primary_source_typography_independently_authenticated":False,
    "historical_priority_clearance":False,"publication_clearance":False,
    "human_peer_review_claim":False,
    "mechanism":"Independent full convex-hull decomposition and equality-case analysis, exact active-basis enumeration, rational partner construction, rank/kernel and primal/dual certificates",
    "remaining_gap":"Separate primary-source authentication, historical priority and any later publication-package review are outside this family's mathematical verdict."
}
(HERE/"RESULT.json").write_text(json.dumps(result,indent=2)+"\n")
log=HERE/"RESEARCH_LOG.md"
log.write_text(log.read_text()+"\n"+stamp+" — Original normal author/review receipts reproduced byte for byte after independent construction (3045/5368 assertions, PIDs60289/60292, reaped exit zero). Final report finds no mandatory mathematical correction in the augmented-LP/fiber scope. Original proof/source and compared inputs rehashed unchanged. Mathematical-family completion estimate:100%; priority/publication remain uncleared. Report and public-safe manifest sealed.\n")
datafiles=[p for p in sorted(HERE.rglob("*")) if p.is_file() and p.name not in ("OUTPUT_MANIFEST.json","SHA256SUMS")]
for p in datafiles:
    if p.is_symlink():
        raise RuntimeError("No symlink allowed in public-safe manifest")
lines=[]
for p in datafiles:
    lines.append(hashlib.sha256(p.read_bytes()).hexdigest()+"  "+str(p.relative_to(HERE)))
(HERE/"SHA256SUMS").write_text("\n".join(lines)+"\n")
files=datafiles+[HERE/"SHA256SUMS"]
members=[]
for p in files:
    body=p.read_bytes()
    members.append({"path":str(p.relative_to(HERE)),"bytes":len(body),"sha256":hashlib.sha256(body).hexdigest(),
                    "classification":"project-authored mathematical proof/code/control/receipt; public-safe; no third-party source body"})
manifest={"completed_utc":stamp,"verdict":result["verdict"],"member_count":len(members),
          "members":members,"manifest_self_excluded":True,
          "third_party_pdf_text_or_images_included":False,
          "historical_priority_clearance":False,"publication_clearance":False}
(HERE/"OUTPUT_MANIFEST.json").write_text(json.dumps(manifest,indent=2)+"\n")
for m in members:
    body=(HERE/m["path"]).read_bytes()
    if len(body)!=m["bytes"] or hashlib.sha256(body).hexdigest()!=m["sha256"]:
        raise RuntimeError("Manifest readback mismatch")
print(json.dumps({"verdict":result["verdict"],"member_count":len(members),
                  "report_sha256":hashlib.sha256((HERE/"REPORT.md").read_bytes()).hexdigest(),
                  "result_sha256":hashlib.sha256((HERE/"RESULT.json").read_bytes()).hexdigest(),
                  "manifest_sha256":hashlib.sha256((HERE/"OUTPUT_MANIFEST.json").read_bytes()).hexdigest(),
                  "finalizer_pid":os.getpid()}))

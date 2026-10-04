from pathlib import Path
import hashlib,json,sys
from capture_command import HERE,run
O=HERE/"original";P=HERE/"private_replays";P.mkdir(exist_ok=False)
def pin(p):
    b=p.read_bytes();return {"path":str(p),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
jobs=[]
specs=[("author_current","check_denominators.py","check_results.json","SOURCE_STATUS.md","check_results.json",284),
       ("historical_submitted","review/submitted_check_denominators.py","review/submitted_check_results.json","review/source_snapshot.md","check_results.json",284),
       ("historical_independent","review/independent_checks.py","review/independent_results.json","review/REVIEW.md","independent_results.json",6463)]
for name,code,reference,context,written,expected in specs:
    d=P/name;d.mkdir();target=d/Path(code).name;target.write_bytes((O/code).read_bytes())
    cap,out,err=run(name,["/usr/bin/python3","-B",str(target)],cwd=d,sources=[target,O/context])
    assert cap["exit_code"]==0,(name,cap,err)
    receipt=d/written;assert receipt.exists()
    result=json.loads(receipt.read_bytes());assert result["status"]=="PASS" and result["exact_assertions"]==expected
    assert receipt.read_bytes()==(O/reference).read_bytes(),("written receipt mismatch",name)
    stdout=json.loads(out);assert stdout["status"]=="PASS" and stdout["exact_assertions"]==expected
    fullstdout=out==receipt.read_bytes()
    if name!="historical_independent":assert fullstdout
    jobs.append({"name":name,"capture":str(HERE/"captures"/name/"CAPTURE.json"),"actual_child_pid":cap["child_pid"],
                 "actual_operator_pid":cap["operator_pid"],"utc_start":cap["utc_start"],"utc_end":cap["utc_end"],"argv":cap["argv"],"cwd":cap["cwd"],
                 "exit_code":cap["exit_code"],"exact_assertions":expected,"sources":cap["sources"],
                 "written_receipt":pin(receipt),"exact_original_reference":pin(O/reference),"written_receipt_byte_equal":True,
                 "stdout_full_written_receipt":fullstdout,"code_hashes_proof":False,
                 "artifact_context_prelaunch_bound_but_not_read_by_checker":str(O/context),"new_mathematical_independence":False})
old=(O/"review/source_snapshot.md").read_bytes();final=(O/"SOURCE_STATUS.md").read_bytes()
before=b"Separate adversarial review is pending."
after=b"Separate adversarial source and mathematical review passed; see [the report](review/REVIEW.md)."
assert old.count(before)==1 and old.replace(before,after)==final
result={"schema":"pr58-original-historical-reproduction/v1","jobs":jobs,"historical_reviewed_snapshot":pin(O/"review/source_snapshot.md"),
"current_head_artifact":pin(O/"SOURCE_STATUS.md"),"exact_one_metadata_sentence_replacement_recovers_current":True,
"scope":"Private byte-exact diagnostic copies only. Both author programs write and print full receipts; old independent program writes its full receipt and prints a documented subset.",
"new_math_verdict_credit":False,"new_priority_verdict_credit":False,"new_route_increment":False,"root_approval":False,
"limits":["284 and 6463 are bounded diagnostic assertion counts, not universal mathematical proofs.",
"These programs do not read/hash proof files; full prelaunch contextual proof/review bodies are retained by the capture operator only.",
"Historical primary PDF checksums, complete manuscript reading, source-page visual inspections and prior publication-access claims are preserved as historical assertions; no new PDF reproduction is claimed.",
"The exact old reviewed mathematical snapshot is present and recovered by the recorded one-sentence metadata replacement. Historical scope is not transferred to a new independent review."]}
(HERE/"REPRODUCTION.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
print(json.dumps({"status":"HISTORICAL_DIAGNOSTICS_REPRODUCED_SOURCE_ONLY","jobs":[{k:j[k] for k in ["name","actual_child_pid","utc_start","utc_end","exit_code","exact_assertions","stdout_full_written_receipt"]} for j in jobs],"new_independence":False},indent=2))

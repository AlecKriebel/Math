#!/usr/bin/env python3
"""Terminal custody for the existing bounded repair; no candidate mutation."""
import collections, datetime, difflib, hashlib, io, json, subprocess, sys, zipfile
from pathlib import Path
W=Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
A=W.parents[1]
D=A/"preprint_v1_0"
K=D/"verification_kit"
WRITE="--write" in sys.argv

def need(c,m):
    if not c: raise RuntimeError(m)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def row(p,root): return {"path":p.relative_to(root).as_posix(),"bytes":p.stat().st_size,"sha256":sha(p)}
def same(p,r): return p.is_file() and not p.is_symlink() and p.stat().st_size==r["bytes"] and sha(p)==r["sha256"]
def obj(p): return json.loads(p.read_text())
def dump(p,d):
    if WRITE: p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+"\n")

need(not (W/"TERMINAL_SEAL.json").exists(),"No automatic terminal reseal")
old=obj(W/"IMMEDIATE_INPUT_PINS.json")["files"]
cur={p.relative_to(A).as_posix():p for p in A.rglob("*") if p.is_file() and not p.is_relative_to(W)}
before={r["original_path"]:r for r in obj(W/"BEFORE_COPIES.json")["files"]}
changed=[]; protected=[]
for r in old:
    n=r["path"]; need(n in cur,"Missing baseline "+n)
    if same(cur[n],r): protected.append(r)
    else:
        need(n in before,"Unauthorized mutation "+n); b=before[n]
        need((b["bytes"],b["sha256"])==(r["bytes"],r["sha256"]),"Before hash differs")
        need(same(A/b["source_snapshot"],b) and same(K/b["destination"],b),"Before copies differ")
        changed.append({"path":n,"before":r,"after":row(cur[n],A),"source_snapshot":b["source_snapshot"],"delivered_before":b["destination"]})
new=sorted(set(cur)-{r["path"] for r in old})
need((len(old),len(changed),len(protected),len(new),len(cur))==(309,11,298,51,360),"Unexpected current counts")
need(set(before)=={r["path"] for r in changed},"Before set differs")
dump(W/"CHANGE_ACCOUNTING.json",{"baseline_count":309,"changed_count":11,"unchanged_count":298,"new_count":51,"current_count":360,"changes":changed,"new_files":[row(cur[n],A) for n in new]})
dump(W/"PROTECTED_INPUT_PINS.json",{"scope":"All 298 unchanged immediate inputs; mathematical paper, source credits and preceding reviews are protected.","files":protected})
currentpins=[row(cur[n],A) for n in sorted(cur)]
dump(W/"CURRENT_INPUT_PINS.json",{"scope":"All audit files outside this bounded repair workspace at the terminal stage; not mathematical or publication certification.","files":currentpins})
textual=[c["path"] for c in changed if c["path"].endswith((".py",".md")) or c["path"].endswith(("/metadata.json","/deposit_metadata.json","/EXTERNAL_BINDING.json"))]
textual += [n for n in new if "/repair01_history/" not in n and (n.endswith((".py",".md")) or n.endswith(("/research_metadata.json","/CURRENT_STATUS_REPAIR01.json")))]
patch=[]
for n in sorted(textual):
    prior=(A/before[n]["source_snapshot"]).read_text().splitlines(keepends=True) if n in before else []
    patch.extend(difflib.unified_diff(prior,cur[n].read_text().splitlines(keepends=True),fromfile="before/"+n if n in before else "/dev/null",tofile="after/"+n))
if WRITE: (W/"COMPLETE_CODE_PROSE_DIFF.patch").write_text("".join(patch))
hist=obj(K/"REPAIR01_HISTORY_RESOLUTION.json")
counts={"immediate-before-repair01":309,"preparation-input194":194,"preparation-output90":90,"whole01-input289":289,"whole01-output17":17}
prefix={"immediate-before-repair01":"","preparation-input194":"","preparation-output90":"preprint_v1_0/","whole01-input289":"","whole01-output17":"reviews/package_01/"}
need(hist["inventory_counts"]==counts,"History counts differ")
groups=collections.defaultdict(list)
for r in hist["references"]:
    groups[r["stage"]].append(r)
    if r["disposition"]=="exact_captured_stage_or_canonical_copy": need(same(K/r["destination"],r),"Historical copy differs")
    else: need(r["disposition"]=="omitted" and bool(r["reason"]),"Unexplained omission")
need(set(groups)==set(counts),"Missing stage")
for stage,refs in groups.items():
    inventory=obj(A/refs[0]["inventory"])["files"]
    expect=[(prefix[stage]+r["path"],r["bytes"],r["sha256"]) for r in inventory]
    actual=[(r["original_path"],r["bytes"],r["sha256"]) for r in refs]
    need(actual==expect and len(refs)==counts[stage],"Historical inventory rows differ "+stage)
stagecopies=obj(K/"REPAIR01_STAGE_COPIES.json")["files"]
for r in stagecopies: need(same(A/r["source_snapshot"],r) and same(K/r["destination"],r),"Stage copy source differs")
ledger=obj(K/"COPY_EXCLUSION_LEDGER.json"); copycount=0
need(len(ledger["files"])==194 and len(ledger["historical_pin_references"])==269,"Old ledger counts differ")
for r in ledger["files"]:
    if r["disposition"]=="byte_identical_copy": need(same(K/r["destination"],r),"Old copy differs"); copycount+=1
    else: need(r["disposition"]=="omitted" and bool(r["reason"]),"Old omission unexplained")
for r in ledger["historical_pin_references"]:
    if r["disposition"]=="hash_identical_canonical_copy": need(sha(K/r["destination"])==r["sha256"],"Old stage hash differs")
    else: need(r["disposition"]=="omitted" and bool(r["reason"]),"Old stage omission unexplained")
need(copycount==60 and len(stagecopies)==44,"Copy counts differ")
native=obj(D/"metadata.json"); wrapper=obj(D/"deposit_metadata.json")
need((D/"metadata.json").read_bytes()==(K/"metadata.json").read_bytes(),"Native bare bytes differ")
need(set(wrapper)=={"metadata","files"} and wrapper["metadata"]==native,"Native wrapper differs")
need(wrapper["files"]==[{"path":"preprint.pdf","name":"preprint.pdf"},{"path":"verification_kit.zip","name":"verification_kit.zip"}],"Attachment list differs")
research=(A/before["preprint_v1_0/metadata.json"]["source_snapshot"]).read_bytes()
need(research==(D/"research_metadata.json").read_bytes()==(K/"research_metadata.json").read_bytes(),"Custom history bytes differ")
need((D/"CURRENT_STATUS_REPAIR01.json").read_bytes()==(K/"CURRENT_STATUS_REPAIR01.json").read_bytes(),"Current stage copies differ")
status=obj(D/"CURRENT_STATUS_REPAIR01.json")
need(status["whole_reviews_completed"]==1 and status["minimum_whole_reviews"]==2 and status["new_complete_review_required"] and not status["publication_ready"] and not status["published"] and status["services_held_at"]==1032,"Gate status differs")
names=obj(K/"ALLOWLIST.json")["members"]; buf=io.BytesIO()
with zipfile.ZipFile(buf,"w",compression=zipfile.ZIP_STORED) as z:
    for n in names:
        i=zipfile.ZipInfo("verification_kit/"+n,(2026,10,14,0,0,0)); i.create_system=3; i.external_attr=0o100644<<16; i.compress_type=zipfile.ZIP_STORED
        z.writestr(i,(K/n).read_bytes())
need(buf.getvalue()==(D/"verification_kit.zip").read_bytes(),"Independent closed ZIP differs")
payloads=[]
with zipfile.ZipFile(D/"verification_kit.zip") as z:
    need(z.namelist()==["verification_kit/"+n for n in names] and z.testzip() is None and not z.comment,"ZIP order/CRC")
    for i in z.infolist():
        need(i.date_time==(2026,10,14,0,0,0) and i.create_system==3 and i.external_attr==0o100644<<16 and i.compress_type==zipfile.ZIP_STORED and not i.extra and not i.comment and not i.is_dir(),"ZIP header")
        body=z.read(i); need(body==(K/i.filename.removeprefix("verification_kit/")).read_bytes(),"ZIP payload")
        payloads.append({"path":i.filename,"bytes":len(body),"sha256":hashlib.sha256(body).hexdigest()})
need(payloads==obj(W/"ARCHIVE_PAYLOAD_CHECKS.json")["headers_and_payloads"] and len(names)==121,"Saved reproduction payload differs")
receipts=[json.loads(l) for l in (W/"REPRODUCTION_RECEIPTS.jsonl").read_text().splitlines()]
need(len(receipts)==27,"Receipt count")
for r in receipts: need(r["returncode"]==0 if r["expected"]==0 else r["returncode"]!=0,"Receipt failure")
summary=obj(W/"REPRODUCTION_SUMMARY.json")
need(summary["status"]=="PASS" and summary["archive_sha256"]==sha(D/"verification_kit.zip") and summary["canonical_inputs_unchanged_during_reproduction"]==360,"Reproduction stage differs")
guards=[json.loads(r["stdout"]) for r in receipts if "output_guard_checks.py" in r["argv"]]
need(len(guards)==2 and all(g["status"]=="PASS" and g["rejection_count"]==272 for g in guards),"Guard receipts")
positives=[json.loads(r["stdout"]) for r in receipts if "run_checks.py" in r["argv"]]
need(len(positives)==2 and positives[0]==positives[1],"Normal optimized result differs")
historical=obj(W/"HISTORICAL_REGRESSION_RESULTS.json")
need(historical["status"]=="PASS" and len(historical["observations"])==5 and all(r["historical_defect_reproduced"] for r in historical["observations"]),"Historical regression differs")
fresh=[]
for opt in [False,True]:
    argv=[sys.executable,"-I","-B"]+(["-O"] if opt else [])+[str(K/"verify.py"),"--require-binding"]
    r=subprocess.run(argv,cwd=K,capture_output=True,text=True,timeout=120)
    need(r.returncode==0,"Fresh binding failed "+r.stderr)
    fresh.append({"argv":argv,"cwd":str(K),"returncode":r.returncode,"stdout":r.stdout,"stderr":r.stderr})
repo=A.parents[2]
argv=[sys.executable,"-B",str(repo/"zenodo_deposit_tool/zenodo.py"),"check",str(D/"deposit_metadata.json")]
r=subprocess.run(argv,cwd=repo,capture_output=True,text=True,timeout=120)
need(r.returncode==0 and json.loads(r.stdout)==obj(W/"REPOSITORY_LOCAL_CHECK.json"),"Fresh local check differs")
fresh.append({"argv":argv,"cwd":str(repo),"returncode":r.returncode,"stdout":r.stdout,"stderr":r.stderr})
dump(W/"TERMINAL_READ_ONLY_RECEIPTS.json",fresh)
for r in currentpins: need(same(A/r["path"],r),"Terminal checks changed candidate")
verification={"status":"PASS_BOUNDED_REPAIR_PENDING_NEW_FULL_WHOLE02","as_of_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"scope":"Metadata/writer repair and custody only; no new mathematical, source, visual or whole review.","immediate_input_count":309,"authorized_changes":11,"unchanged_protected_inputs":298,"new_candidate_files":51,"current_audit_files_outside_repair":360,"before_snapshots":11,"new_delivered_captured_stage_copies":44,"old_delivered_copies_unchanged":60,"old_copy_omission_rows":194,"old_stage_references_unchanged":269,"new_stage_resolution_rows":899,"new_stage_resolution_counts":dict(collections.Counter(r["disposition"] for r in hist["references"])),"old_inventory_counts":counts,"archive":row(D/"verification_kit.zip",D),"archive_members":121,"manifest_payload_rows":120,"independent_closed_zip_byte_exact":True,"all_zip_headers_payload_crcs_checked":True,"pdf":row(D/"preprint.pdf",D),"tex":row(D/"preprint.tex",D),"native_metadata_bare_bytes_identical":True,"wrapper_metadata_object_equal":True,"historical_research_metadata_exact":True,"native_local_uploader_checks_pass":True,"full_reproduction_commands":27,"read_only_terminal_commands":3,"historical_defect_commands":5,"guard_invocations":2,"each_guard_rejections":272,"guard_total_rejections":544,"each_guard_invocation_tests_both_python_modes":True,"normal_optimized_full_result_json_equal":True,"unchanged_pdf_compiled_or_rendered":False,"whole_reviews_completed":1,"minimum_whole_reviews":2,"fresh_whole02_required":True,"publication_ready":False,"published":False,"services_held_at":1032,"math_research_completion_best_guess_percent":60,"bounded_repair_completion_percent":100}
dump(W/"FINAL_VERIFICATION.json",verification)
print(json.dumps(verification,indent=2))


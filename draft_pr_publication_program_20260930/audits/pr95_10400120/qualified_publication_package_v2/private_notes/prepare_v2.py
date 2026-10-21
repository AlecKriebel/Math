from pathlib import Path
import json,hashlib,datetime,shutil
P=Path("/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr95_10400120/qualified_publication_package_v2");V1=Path("/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr95_10400120/qualified_publication_package_v1");A=V1.parent
F=P/"publicfiles";N=P/"private_notes";(F/"verification").mkdir(parents=True,exist_ok=True);N.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf-8")
for name in ["pr95_note.tex","pr95_note.pdf","README.md","LICENSE.txt","PR95_PRIORITY_QUALIFICATION.md"]:
 shutil.copyfile(V1/"publicfiles"/name,F/name)
for name in ["VERIFY_README.md","SOURCE_PROVENANCE.json","run_all.py","verify.py","independent_checks.py","root_lattice_check.py"]:
 shutil.copyfile(V1/"publicfiles/verification"/name,F/"verification"/name)
shutil.copyfile(V1/"zenodo-deposit.json",P/"zenodo-deposit.json")
runner=F/"verification/run_all.py"
old=runner.read_text()
anchor='        p=ROOT/q\n        require(p.is_file() and not p.is_symlink(),"missing/linked payload: "+str(q))'
replacement='''        p=ROOT/q
        component=ROOT
        for part in q.parts:
            component=component/part
            require(not component.is_symlink(),
                    "symlinked payload path component: "+str(q)+" ["+part+"]")
        require(p.is_file(),"missing payload: "+str(q))'''
if old.count(anchor)!=1:raise RuntimeError("repair anchor")
runner.write_text(old.replace(anchor,replacement),encoding="utf-8")
for q in [F/"README.md",F/"verification/VERIFY_README.md"]:
 s=q.read_text()
 if q.name=="README.md":
  s=s.replace("The runner performs the full payload hash guard,","The runner performs the full payload hash guard, rejecting every symlinked path component beneath the package root,")
 else:
  s=s.replace("rejects missing, linked, changed or unsafe paths.","rejects missing, changed or unsafe paths and every symlinked file or ancestor directory component beneath the package root.")
  s=s.replace("recorded_results.json and recorded_processes/ preserve actual initial assembly executions as historical results. The final clean-extraction run is separately retained in private preparation evidence, leaving archive bytes fixed.","recorded_results.json and recorded_processes/ preserve actual current V2 assembly executions as historical evidence. The final clean-extraction run is separately retained in private preparation evidence, leaving archive bytes fixed. Frozen V1 receipts remain in the preserved V1 sibling; their successes did not test the repaired ancestor-directory guard.")
 q.write_text(s,encoding="utf-8")
prov=F/"verification/SOURCE_PROVENANCE.json"
d=json.loads(prov.read_text())
d["package_revision"]="V2 preparation; deposit version remains1.0 because no release exists."
d["runner_repair"]={"required_review_item":"R1","v1_runner_sha256":sha(V1/"publicfiles/verification/run_all.py"),"v2_runner_sha256":sha(runner),
 "scope":"Reject each symlinked component beneath ROOT in every declared relative payload path, before following file content. Exact math/checkers/manuscript/PDF unchanged."}
dump(prov,d)
support=["pr95_note.tex","README.md","LICENSE.txt","PR95_PRIORITY_QUALIFICATION.md"]+["verification/"+n for n in ["VERIFY_README.md","SOURCE_PROVENANCE.json","run_all.py","verify.py","independent_checks.py","root_lattice_check.py"]]
dump(F/"PAYLOAD_MANIFEST.json",{"schema":"pr95-support-payload/v1","files":[{"file":s,"bytes":(F/s).stat().st_size,"sha256":sha(F/s)} for s in sorted(support)],"hash_scope":"Initial current V2 source inputs; final expanded archive also binds fresh recorded process evidence."})
dump(N/"INPUTS.json",{"UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),"repair_scope":"R1 only, no mathematics/manuscript/PDF/metadata change",
 "files":[{"file":str(q.relative_to(A)),"bytes":q.stat().st_size,"sha256":sha(q)} for q in
 [A/"whole_qualified_package_round1_20261005/REPORT.md",A/"whole_qualified_package_round1_20261005/CLOSED_MANIFEST.json",V1/"PREPARATION_MANIFEST.json",V1/"CLOSURE.json",V1/"private_notes/FROZEN_CANDIDATE_MANIFEST.json"]+
 [V1/"publicfiles"/s for s in support]+[V1/"publicfiles/pr95_note.pdf",V1/"zenodo-deposit.json"]]})
(N/"RESEARCH_LOG.md").write_text("# PR95 V2 package repair log\n\n"+datetime.datetime.now(datetime.timezone.utc).isoformat()+" - Round1 report read, R1 isolated to ancestor symlinks. V1 frozen evidence preserved in place. Copied only active public sources/docs/PDF and exact deposit metadata. Implemented every-component rejection under ROOT and precise docs/provenance. Manuscript/PDF bytes identical, version1.0 unchanged; mathematical code unchanged. Preparation estimate35%; narrow mathematics100%; priority unresolved; publication clearancefalse. Original effort2/5, zero new central proof-search turns; no outreach/Git/UI/service change.\n",encoding="utf-8")
print(json.dumps({"v2":str(P),"runner_sha256":sha(runner),"same_note":sha(F/"pr95_note.tex")==sha(V1/"publicfiles/pr95_note.tex"),"same_pdf":sha(F/"pr95_note.pdf")==sha(V1/"publicfiles/pr95_note.pdf"),"same_metadata":sha(P/"zenodo-deposit.json")==sha(V1/"zenodo-deposit.json")}))

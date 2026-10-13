from pathlib import Path
from datetime import datetime, timezone
from hashlib import sha256
import difflib,json,os,shutil,subprocess,sys

N=Path(__file__).resolve().parent
A=N.parent
V=A/"corrected_attempt_preparation_20261006"
I=V/"corrected_attempt"
O=A/"original_head_authentication_20261006/original_attempt"
F=A/"coefficient_literature_priority_adversary_20261006"
C=N/"corrected_attempt"
B=N/"input_v2"
PID=os.getpid()
START=datetime.now(timezone.utc).isoformat()
def utc():return datetime.now(timezone.utc).isoformat()
def pin(p):
 b=p.read_bytes();return {"bytes":len(b),"sha256":sha256(b).hexdigest()}
def ck(v,m):
 if not v:raise RuntimeError(m)
def js(p,x):
 p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n")
def textfile(p,s):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
def journal(action,**kw):
 with (N/"PROCESS_JOURNAL.jsonl").open("a") as f:f.write(json.dumps({"utc":utc(),"actual_operator_pid":PID,"action":action,**kw},ensure_ascii=False)+"\n")
def authenticate_manifest(root,expected_hash,count):
 p=root/"FINAL_MANIFEST.json";ck(pin(p)["sha256"]==expected_hash,"Manifest changed: "+str(root))
 m=json.loads(p.read_text());ck(m["member_count"]==count,"Manifest member count")
 for r in m["members"]:ck(pin(root/r["path"])=={k:r[k] for k in ["bytes","sha256"]},"Sealed member changed: "+str(root/r["path"]))
 return m
ck(not C.exists() and not B.exists(),"New output root already populated")
vm=authenticate_manifest(V,"fef895ae92c3fe73d3a723dbec4ca662932d7268540c44bbcf8fd404595a1620",166)
fm=authenticate_manifest(F,"07b33afe74644acf8c9064149c4a9946a0a84d89875275ab460e07930bd6b349",78)
fresh=A/"original_target_disposition_adversary_20261006"
fresh_m=authenticate_manifest(fresh,"76015f64bfa61ad0a4e92d20e47d1b78c2bcfd9be65f86b4b56fd6cb5c2322e9",31)
gate_path=A/"ROOT_ORIGINAL_TARGET_DISPOSITION_READY_20261006.json"
ck(pin(gate_path)=={"bytes":5072,"sha256":"1a3aa4f259f9b94afdbc02dae85969d9f49ff4e391a92ae6ed87cbce0cc9ef0f"},"Accepted disposition gate pin")
gate=json.loads(gate_path.read_text())
ck(gate["fresh_disposition_review_PASS"] is True and gate["original_target_native_status_supported"]=="already_solved","Gate disposition")
ck(gate["candidate_math"]=="PASS" and gate["candidate_whole_historical_subsumption_established"] is False and gate["alternative_polynomial_criterion_novelty"]=="UNRESOLVED" and gate["publication_authorization"] is False,"Gate scope qualifiers")
for x in gate["input_pins"].values():ck(pin(Path(x["path"]))=={k:x[k] for k in ["bytes","sha256"]},"Gate input pin changed")
ck(pin(fresh/"REPORT.md")["sha256"]=="5f05db76d89edda6a694e06f8c307c2ec6dc535b30bfeeacb609c37bde627623","Fresh report pin")
auth=json.loads((F/"INPUT_AUTHENTICATION.json").read_text())
original=auth["original_files"]
ck({str(p.relative_to(O)):pin(p) for p in O.rglob("*") if p.is_file()}==original,"Original17 changed")
v2={str(p.relative_to(I)):pin(p) for p in I.rglob("*") if p.is_file()}
ck(len(v2)==17 and set(v2)==set(original),"Input17 members")
ck(v2["CANDIDATE.md"]["sha256"]=="fe20c46ed59355387ac63efa41f1e311cdca4697babbb7dbcae06ef0220bb80b","Exact reviewed v2 candidate")
hard="4ccfb72d1f9e41c92eed9f26becd9ae1ece41f43718a74038bf993edf413686d"
ck(v2["review/independent_checks.py"]["sha256"]==hard,"Unchanged explicit-if checker")
journal("authenticate_frozen_inputs",v2_manifest=pin(V/"FINAL_MANIFEST.json"),v2_members=166,frozen_family_members=78,fresh_scientific_members=31,accepted_gate=pin(gate_path),original17_unchanged=True)
for rel in v2:
 for target in [C/rel,B/rel]:
  target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(I/rel,target)
(N/"supporting_receipts").mkdir()
copy_sources=[
 (gate_path,"ROOT_ORIGINAL_TARGET_DISPOSITION_READY_20261006.json"),
 (fresh/"REPORT.md","FRESH_DISPOSITION_REPORT.md"),
 (fresh/"RESULT.json","FRESH_DISPOSITION_RESULT.json"),
 (fresh/"FINAL_MANIFEST.json","FRESH_DISPOSITION_FINAL_MANIFEST.json"),
 (A/"parent_priority_reconciliation_20261006/FRESH_DISPOSITION_REVIEW_AUTHENTICATION.json","FRESH_DISPOSITION_REVIEW_AUTHENTICATION.json"),
 (fresh/"private/SOURCE_RENDER_RECEIPT.json","FRESH_DISPOSITION_SOURCE_RENDER_RECEIPT.json"),
 (V/"REPLAY_RESULTS.json","V2_REPLAY_RESULTS.json"),
 (V/"REPLAY_JOURNAL.jsonl","V2_REPLAY_JOURNAL.jsonl"),
 (A/"PARENT_RELATED_SOURCE_COUNTEREXAMPLES_20261006.json","PARENT_RELATED_SOURCE_COUNTEREXAMPLES_20261006.json"),
 (A/"MATHEMATICS_SOURCE_GATE_20261006.json","MATHEMATICS_SOURCE_GATE_20261006.json")
]
for src,name in copy_sources:shutil.copyfile(src,N/"supporting_receipts"/name)
(N/".gitignore").write_text("private_primary_sources/\nprivate_previews/\n")
source_specs=[
 ("Silverman1975","Univalent Functions with Negative Coefficients","https://doi.org/10.1090/S0002-9939-1975-0369678-0",F/"private_sources/silverman1975.pdf",470613,"69b8ea6331c33f36cd5d934ce5795910a2d396204e1de1ca06662d7dd13c3bd1","Theorem1 and immediate corollary, printed110; arbitrary complex coefficient sufficient direction"),
 ("Mocanu–Reade1975","The Radius of Alpha-Convexity for the Class of Starlike Univalent Functions, Alpha Real","https://doi.org/10.1090/S0002-9939-1975-0374404-5",A/"private_primary_sources_20261006/mocanu_reade1975.pdf",393960,"7f224cd8e4b1636dfeb220037803284d522fab52501451919a5783fd9440e164","Printed397; radius of full starlike class, every real alpha, negative branch leading minus visually verified")
]
sources=[]
for sid,title,url,p,size,h,loc in source_specs:
 ck(pin(p)=={"bytes":size,"sha256":h},"Full1975 primary bytes")
 sources.append({"id":sid,"title":title,"primary_url":url,"private_external_path":str(p),"bytes":size,"sha256":h,"locator":loc,"full_paper_read_by_accepted_fresh_adversary":True,"full_paper_read_by_this_new_staging_operation":False,"source_bytes_copied_into_public_stage":False})
js(N/"SOURCE_PINS.json",{"actual_writer_pid":PID,"utc":utc(),"scope":"Source identity/accepted review provenance; primary PDFs and previews stay private and excluded","full1975_sources":sources,"accepted_scientific_gate":pin(gate_path),"fresh_report":pin(fresh/"REPORT.md"),"fresh_manifest":pin(fresh/"FINAL_MANIFEST.json"),"new_download_or_outreach":False})

outcome={
 "original_target_disposition":"already_solved",
 "original_target_classification_basis":"Verified mathematical consequence of full published1975 sufficient coefficient and radius theorems",
 "scientific_disposition_clearance":"PASS_NARROW_ORIGINAL_LITERAL_TARGET",
 "candidate_mathematics":"PASS",
 "whole_candidate_historical_subsumption_established":False,
 "alternative_polynomial_criterion_novelty":"UNRESOLVED",
 "alternative_priority_clearance":False,
 "express_first_named_answer_priority":"UNVERIFIED",
 "publication_authorization":False,
 "publication_readiness":False,
 "closure_operation_performed":False,
 "actual_closure_url":None,
 "actual_closure_status":None,
 "closure_service_readback":None,
 "native_author_global_propagation":"PENDING_SEPARATE_REVIEWED_WRITER",
 "service_or_global_completion_claimed":False,
 "preprint_created":False,"zenodo_created":False,"doi":None,
 "tracker_entry_created":False,"tracker_entry":None,
 "overall_program_complete":False
}
old_answer="""## 6. Accepted original-target disposition and older all-real answer

The accepted fresh scientific disposition distinguishes the original question from the alternative polynomial theorem above. The original literal all-real sufficient-generalization target is already mathematically answerable by the following consequence of published1975 results. Candidate mathematics remains PASS; the whole polynomial criterion is not proved historically subsumed, and its alternative novelty remains UNRESOLVED. No express first named-problem answer is assigned. This is scientific disposition clearance only: actual PR closure and native/author/global propagation remain pending, with no publication authorization.

[Silverman1975, Univalent Functions with Negative Coefficients, Theorem1 and its immediate corollary, printed110](https://doi.org/10.1090/S0002-9939-1975-0369678-0), gives sufficient absolute-coefficient conditions for arbitrary complex coefficients: sum n|a_n|<1 implies starlikeness and sum n²|a_n|<1 implies convexity. The negative-coefficient restriction applies to the converse, not to this sufficient direction. [Mocanu–Reade1975, The Radius of Alpha-Convexity for the Class of Starlike Univalent Functions, Alpha Real, printed397](https://doi.org/10.1090/S0002-9939-1975-0374404-5), gives the alpha-convexity radius of the entire starlike univalent class:

    R_alpha=(1+alpha)-sqrt((1+alpha)²-1),                   alpha>=0;
            sqrt[(2-sqrt(-alpha))/(2+sqrt(-alpha))],        -3<=alpha<=0;
            -(1+alpha)-sqrt((1+alpha)²-1),                  alpha<=-3.

The leading minus in the last branch is essential and was visually verified by the source/disposition reviewers. The branches agree at alpha=-3; R_0=1, and 0<R_alpha<1 for every nonzero alpha.

Define W_0(n)=n and W_1(n)=n². At every other real alpha define W_alpha(n)=n R_alpha^(1-n). Then

    sum_(n>=2) W_alpha(n)|a_n|<1

is an all-real sufficient generalization with both exact endpoint tests. For a nonendpoint alpha put R=R_alpha and define

    h(w)=w+sum_(n>=2) a_n R^(1-n) w^n.

The weighted bound makes sum n|a_n R^(1-n)|<1, so the series for h and h' converge on the closed disk and h is analytic on the open disk. The notation h(w)=R f(w/R) refers to this justified power-series extension, not an extra assumption that the original f was already defined outside its disk. Silverman's criterion makes h starlike. Nonvanishing also follows directly from |h/w-1|<=B/2<1 and |h'-1|<=B<1, with B=sum n|a_n R^(1-n)|.

Mocanu–Reade gives Re J_alpha[h](w)>0 on |w|<R. The radius conclusion is used only on this open disk; no positivity on its boundary is asserted. The exact identities

    h(Rz)=R f(z), h'(Rz)=f'(z), h''(Rz)=f''(z)/R,
    J_alpha[h](Rz)=J_alpha[f](z)

transfer strict positivity and both nonzero factors to every |z|<1. At zero the removable expressions equal1. The two endpoints follow directly from Silverman's coefficient conditions. All weights are positive and finite, and sufficiently small polynomial perturbations satisfy them. The source question does not require continuous parameter dependence or polynomial weights; the endpoint patch is explicit.

This is an audit deduction from older published theorems, not a claim that the1975 authors printed this scaling deduction or expressly answered Miller–Hayman6.64. It establishes the accepted original-target already_solved classification by mathematical consequence, while express historical named-answer priority remains unverified.

The two coefficient balls must not be conflated. For a nonendpoint alpha and epsilon=1/[2(1+kappa)], the coefficients a_n=epsilon/n⁴ give candidate sum below1/2 by sum_(n>=2)1/n²<1, yet have radius of convergence exactly1. Since R<1, the old terms epsilon R^(1-n)/n³ do not tend to zero. Thus the candidate ball is not fully subsumed by the old exponential test. Conversely, at alpha=-1/2, kappa=1, f=z-(3/10)z² has candidate total6/5>1 but old total(3/5)/R<1: here R=sqrt[(2-1/sqrt2)/(2+1/sqrt2)]>3/5, as verified by32>34/sqrt2. The balls are incomparable at this negative parameter. No uniformly stronger-ball claim is made.

The original1/5 effort, one substantive approach, zero added central proof-search turns, and no human-review claim are preserved. The accepted fresh report reviewed the sealed v2 input and proposed scientific outcome; it did not certify these newly prepared source/status postimage bytes or execute a service/global writer. A separate reviewed writer step is still required. No preprint, Zenodo DOI, or tracker entry is authorized or created.
"""
s=(C/"CANDIDATE.md").read_text()
old="**Status:** corrected-postimages-preparation_only; mathematical gate PASS, PRIORITY_NOT_CLEARED. No publication or disposition readiness.  "
new="**Status:** final-operative-disposition-postimages-preparation_only. Original target already_solved by verified older mathematical consequence; candidate mathematics PASS; alternative polynomial novelty UNRESOLVED. Actual closure/global propagation pending; no publication authorization.  "
ck(s.count(old)==1,"Candidate status anchor");s=s.replace(old,new)
s=s.replace("This preparation is an AI-reviewed staging artifact, not human peer review, publication readiness, a novelty certificate, or a final problem disposition.","This staging artifact records accepted scientific clearance for the narrow original-target already_solved outcome; it is not human peer review, publication authorization, an alternative-novelty certificate, or a completed closure/global operation.")
s=s.replace("Priority and mathematical-substance reconciliation remain pending.","Alternative polynomial-criterion priority and mathematical-substance reconciliation remain pending; the distinct original-target conclusion is recorded in section6.")
s=s.replace("The independent checker is the previously exercised explicit-if version, with normal and optimized execution and an optimized false-parameter guard control.","The independent checker remains the previously exercised explicit-if version; its actual earlier normal/optimized and optimized false-parameter guard receipts are retained with their original PIDs/dates and are not claimed rerun by this stage.")
(C/"CANDIDATE.md").write_text(s+"\n"+old_answer)
shutil.copyfile(C/"CANDIDATE.md",C/"review/author_replay/CANDIDATE.md")
candidate=pin(C/"CANDIDATE.md")
journal("prepare_qualified_candidate_disposition",candidate=candidate,proof_sections_2_3_4_unchanged=True,publication_authorization=False)

src=(C/"SOURCES.md").read_text()
old="Current correction date: 2026-10-06. Status: corrected-postimages-preparation_only; mathematics PASS; PRIORITY_NOT_CLEARED. No publication or disposition readiness. The original2026-09-30 source record and receipts remain separately preserved in archival_original."
new="Current disposition-preparation date: 2026-10-06. Status: final-operative-disposition-postimages-preparation_only. Original target already_solved by verified older consequence; candidate mathematics PASS; alternative polynomial novelty UNRESOLVED; express first named-answer priority unverified. Scientific disposition clearance only; closure/global propagation pending, no publication authorization. Original and sealed v1/v2 source records remain immutable in their earlier folders."
ck(src.count(old)==1,"Sources status anchor");src=src.replace(old,new)
src=src.replace("The exact prior status of the all-real formal statement, the substantive novelty threshold, and express historical named-problem priority remain for parent reconciliation and a separate reviewed writer/disposition step.","The exact prior status and substance of the alternative polynomial theorem, and express first named-answer priority, remain unresolved. The original literal existence target has separately received scientific already_solved clearance as explained below; actual closure/global propagation remain pending.")
src+="\n## Full1975 sources and accepted original-target consequence\n\n"
src+="[Silverman1975, Univalent Functions with Negative Coefficients, Proc.AMS51(1),109–116](https://doi.org/10.1090/S0002-9939-1975-0369678-0), full470613bytes, SHA-25669b8ea6331c33f36cd5d934ce5795910a2d396204e1de1ca06662d7dd13c3bd1. Theorem1 and corollary, printed110, supply sufficient absolute-coefficient tests for arbitrary complex coefficients. The title's negative-coefficient restriction applies to the converse, not the sufficient direction.\n\n"
src+="[Mocanu–Reade1975, The Radius of Alpha-Convexity for the Class of Starlike Univalent Functions, Alpha Real, Proc.AMS51(2),395–400](https://doi.org/10.1090/S0002-9939-1975-0374404-5), full393960bytes, SHA-2567f224cd8e4b1636dfeb220037803284d522fab52501451919a5783fd9440e164. Printed397 gives R_alpha for the whole starlike class and every real alpha; the leading minus in the alpha<=-3 branch was visually verified. The full-source/scaling argument was independently accepted by the fresh disposition review.\n\n"
src+="Candidate section6 records R_alpha, W_0=n,W_1=n²,W_alpha=n R_alpha^(1-n) otherwise, and the h(w)=R f(w/R) power-series/scaling deduction. It answers the unrestricted all-real sufficient-generalization target using older theorems, with no extra analytic-continuation assumption. This is an audit consequence, not a verified express historical named answer. It neither proves historical subsumption of the whole polynomial criterion nor makes that ball uniformly stronger: the tail witness shows non-subsumption, and alpha=-1/2 gives incomparability. Alternative-criterion novelty remains UNRESOLVED.\n\n"
src+="Accepted root scientific gate SHA-2561a3aa4f259f9b94afdbc02dae85969d9f49ff4e391a92ae6ed87cbce0cc9ef0f; fresh disposition report SHA-2565f05db76d89edda6a694e06f8c307c2ec6dc535b30bfeeacb609c37bde627623. These support a qualified original-target classification only; they do not approve unexecuted global/service changes or authorize publication.\n"
(C/"SOURCES.md").write_text(src)

old_review=(I/"review/REVIEW.md").read_text()
banner="# Current qualified original-target disposition — "+utc()+"\n\n**final-operative-disposition-postimages-preparation_only. Original target already_solved by verified older mathematical consequence; candidate mathematics PASS; alternative polynomial novelty UNRESOLVED; express first named-answer priority unverified.** Accepted scientific disposition clearance only. Actual closure/native/author/global propagation are pending and no publication is authorized. The sealed v2 review bundle below is archival; its earlier pending-disposition wording predates the accepted fresh gate. Neither the original reviewer nor the fresh disposition reviewer is represented as having approved these newly edited postimage bytes.\n\n---\n\n"
add="\n## Dated operative-disposition preparation addendum — "+utc()+"\n\nActual stage PID "+str(PID)+". Current prepared candidate SHA-256 "+candidate["sha256"]+". Proof sections2–4 remain byte-identical to original and sealed v2. The fresh scientific disposition report5f05db76d89edda6a694e06f8c307c2ec6dc535b30bfeeacb609c37bde627623 and accepted root gate1a3aa4f259f9b94afdbc02dae85969d9f49ff4e391a92ae6ed87cbce0cc9ef0f reviewed the sealed v2 input and narrow original-target outcome, not an unexecuted closure/global operation.\n\n"+old_answer.split("## 6. Accepted original-target disposition and older all-real answer\n\n",1)[1]
add+="\nThe source/checker corrections from v2 remain operative: no valid sufficiency credit to the malformed/intended-false2016 criterion, no imported false June2026 Proposition2.2, and the unchanged explicit-if checker at SHA"+hard+". New author/replay normal receipts bind to this prepared candidate hash. The earlier independent normal/optimized and optimized false guard retain their actual original PIDs/dates; this stage does not rerun or relabel them as fresh executions. Original effort1/5, substantive1,newproof0,no human referee.\n"
(C/"review/REVIEW.md").write_text(banner+old_review+add)
review_pin=pin(C/"review/REVIEW.md")

readme="""# Qualified original-target disposition — staging only

**2306064 / AMR-022-6064. final-operative-disposition-postimages-preparation_only. Original target already_solved by a verified older mathematical consequence. Candidate mathematics PASS; alternative polynomial novelty UNRESOLVED. Express first named-answer priority unverified.**

The accepted fresh scientific review finds the literal all-real sufficient-generalization question answerable from full Silverman1975 and Mocanu–Reade1975 theorems through the R_alpha/W_alpha/power-series scaling deduction in [candidate section6](CANDIDATE.md). The candidate's proof sections2–4 are unchanged. Whole-candidate historical subsumption is false as an established claim: its ball is not fully accepted by the old exponential test, and the two balls are incomparable at alpha=-1/2. No uniformly stronger-ball claim is made.

[SOURCES.md](SOURCES.md) preserves the2016/2026 source corrections, credits the valid2017 mechanism and limited1985 preview, and adds the full1975 pins. The [review](review/REVIEW.md) explicitly preserves the prior bundle as archival and adds the accepted scientific distinction; no historical reviewer is claimed to have approved the newly edited text.

Current author/replay normal receipts each pass50840 finite exact controls against the new candidate hash. The unchanged explicit-if independent checker's actual earlier normal/optimized28722 and optimized false-guard rejection are retained with original PIDs/dates, not rerun here. See ../REPLAY_RESULTS.json and ../RETAINED_INDEPENDENT_EXERCISE.json. Finite controls remain diagnostics; the written proof establishes the theorem.

Actual PR closure/comment/readback and native/author/global propagation are PENDING_SEPARATE_REVIEWED_WRITER. This stage claims no completed service or global operation. No publication is authorized; preprint/Zenodo/tracker created=false, DOI=null. Original effort1/5, substantive approach1, added central proof0, no human review. Earlier stages and original17 remain sealed. This folder is excluded from the current core checkpoint plan. Any eventual closure URL/status must be recorded in a new dated operation receipt without overwriting this frozen stage.
"""
(C/"README.md").write_text(readme)

vr=json.loads((V/"REPLAY_RESULTS.json").read_text())
independent=[r for r in vr["runs"] if r["name"].startswith("independent")]
ck(len(independent)==3,"Retained independent run set")
ck(all(r["expected_failure_observed"] for r in independent),"Retained run outcome")
for r in independent:
 old_dir=V/"runs"/r["name"]
 ck(pin(old_dir/"stdout.txt")==r["stdout"] and pin(old_dir/"stderr.txt")==r["stderr"],"Retained actual run outputs changed")
 newdir=N/"retained_independent_runs"/r["name"];newdir.mkdir(parents=True)
 for leaf in ["RUN_RECEIPT.json","stdout.txt","stderr.txt"]:shutil.copyfile(old_dir/leaf,newdir/leaf)
retained={"actual_record_writer_pid":PID,"recorded_utc":utc(),"checker_sha256":hard,"checker_unchanged":True,"performed_by_this_stage":False,"rerun_claimed":False,"original_run_source":str(V/"REPLAY_RESULTS.json"),"original_source_pin":pin(V/"REPLAY_RESULTS.json"),"original_runs":independent,"diagnostic_scope":"Unchanged theorem algebra; current source/status edit does not alter formulas tested. Independent checker itself does not read or hash candidate text."}
js(N/"RETAINED_INDEPENDENT_EXERCISE.json",retained)

author=[]
for name,script in [("author_final_normal",C/"verify.py"),("author_replay_final_normal",C/"review/author_replay/verify.py")]:
 d=N/"runs"/name;d.mkdir(parents=True)
 t=utc();p=subprocess.Popen([sys.executable,str(script)],cwd=str(script.parent),stdout=subprocess.PIPE,stderr=subprocess.PIPE,env={**os.environ,"PYTHONDONTWRITEBYTECODE":"1"})
 cp=p.pid;out,err=p.communicate();(d/"stdout.txt").write_bytes(out);(d/"stderr.txt").write_bytes(err)
 ck(p.returncode==0,"Final author run failed")
 result=json.loads(out);ck(result["artifact_sha256"]==candidate["sha256"] and result["exact_assertions"]==50840,"Actual refreshed artifact receipt")
 old_result=json.loads((I/"verification.json").read_text())
 ck({k:v for k,v in result.items() if k!="artifact_sha256"}=={k:v for k,v in old_result.items() if k!="artifact_sha256"},"Author controls changed beyond artifact hash")
 script.with_name("verification.json").write_bytes(out)
 receipt={"name":name,"actual_runner_pid":PID,"actual_child_pid":cp,"started_utc":t,"completed_utc":utc(),"command":[sys.executable,str(script)],"script":pin(script),"exit_code":p.returncode,"stdout":pin(d/"stdout.txt"),"stderr":pin(d/"stderr.txt"),"complete_output":result}
 js(d/"RUN_RECEIPT.json",receipt)
 with (N/"REPLAY_JOURNAL.jsonl").open("a") as f:f.write(json.dumps(receipt,ensure_ascii=False)+"\n")
 author.append(receipt)
ck(pin(C/"verification.json")==pin(C/"review/author_replay/verification.json"),"New author/replay receipt mismatch")
js(N/"REPLAY_RESULTS.json",{"actual_writer_pid":PID,"utc":utc(),"candidate":candidate,"author_replay_candidate":pin(C/"review/author_replay/CANDIDATE.md"),"actual_new_author_runs":author,"author_assertions_each":50840,"author_replay_receipts_byte_identical_to_each_other":True,"byte_identical_to_v2_receipt":False,"difference_from_v2":"candidate artifact_sha256 only","retained_independent_exercise":"RETAINED_INDEPENDENT_EXERCISE.json","new_independent_runs_performed":False,"retained_independent_assertions":28722,"retained_optimized_false_guard_rejected":True})
journal("refresh_actual_author_hash_receipts",candidate=candidate,child_pids=[r["actual_child_pid"] for r in author],independent_runs_reused_not_rerun=True)

sv=json.loads((I/"review/source_verification.json").read_text())
sv.update({"status":"final-operative-disposition-postimages-preparation_only","current_correction_utc":utc(),"actual_preparation_pid":PID,"candidate_sha256":candidate["sha256"],"mathematics":"PASS","priority":"ALTERNATIVE_POLYNOMIAL_CRITERION_UNRESOLVED","scientific_disposition_clearance":"PASS_NARROW_ORIGINAL_LITERAL_TARGET","original_target_disposition":"already_solved","whole_candidate_historical_subsumption_established":False,"alternative_polynomial_criterion_novelty":"UNRESOLVED","express_first_named_answer_priority":"UNVERIFIED","publication_authorization":False,"publication_readiness":False,"scientific_disposition_readiness":True,"disposition_execution_complete":False,"native_author_global_propagation":"PENDING_SEPARATE_REVIEWED_WRITER","actual_closure_url":None,"actual_closure_status":None,"preprint_created":False,"zenodo_created":False,"doi":None,"tracker_entry_created":False,"tracker_entry":None})
sv.pop("disposition_readiness",None)
sv["current_source_checks"].extend([{"url":p["primary_url"],"title":p["title"],"sha256":p["sha256"],"bytes":p["bytes"],"locator":p["locator"],"dependency":"Accepted fresh full-source disposition review; full1975 theorem with qualified scaling deduction","source_pdf_copied_or_published":False} for p in sources])
sv["accepted_scientific_gate"]={"path":"../../supporting_receipts/ROOT_ORIGINAL_TARGET_DISPOSITION_READY_20261006.json",**pin(gate_path)}
sv["fresh_reviewed_input_candidate_sha256"]=v2["CANDIDATE.md"]["sha256"]
sv["fresh_review_scope_notice"]="Fresh disposition report reviewed sealed v2 and proposed scientific outcome, not these new postimage bytes or an unexecuted global/service writer."
sv["exact_remaining_priority_gap"]="Original literal existence target already answerable by verified1975 consequence; alternative polynomial-criterion novelty and express first named-answer priority remain unresolved."
sv["preview_path_notice"]="Preview page hashes refer to sealed v2 private images; no primary PDF/preview copied into this public staging folder."
js(C/"review/source_verification.json",sv)

summary=json.loads((I/"review/review_summary.json").read_text())
summary.update({"status":"final-operative-disposition-postimages-preparation_only","verdict":"PASS_NARROW_ORIGINAL_TARGET_ALREADY_SOLVED_CANDIDATE_MATH_PASS_ALTERNATIVE_UNRESOLVED","prepared_utc":utc(),"actual_preparation_pid":PID,"reviewed_artifact_sha256":candidate["sha256"],"review_sha256":review_pin["sha256"],"review_binding_notice":"Current hash binds staged archival-review plus dated scientific-disposition addendum; original and fresh reviewers did not certify new postimage bytes.","priority":"ALTERNATIVE_POLYNOMIAL_CRITERION_UNRESOLVED","original_target_disposition":"already_solved","candidate_mathematics":"PASS","whole_candidate_historical_subsumption_established":False,"alternative_polynomial_criterion_novelty":"UNRESOLVED","express_first_named_answer_priority":"UNVERIFIED","publication_authorization":False,"publication_readiness":False,"scientific_disposition_readiness":True,"disposition_execution_complete":False,"native_author_global_propagation":"PENDING_SEPARATE_REVIEWED_WRITER","closure_operation_performed":False,"actual_closure_url":None,"actual_closure_status":None,"doi":None,"tracker_entry_created":False,"tracker_entry":None,"fresh_scientific_report":pin(fresh/"REPORT.md"),"accepted_scientific_gate":pin(gate_path),"retained_independent_exercise":"../../RETAINED_INDEPENDENT_EXERCISE.json","new_independent_runs_performed":False,"current_author_receipts_refreshed":True})
summary.pop("disposition_readiness",None)
summary.pop("citation_only_v2_receipt_notice",None)
summary["receipt_notice"]="Two new actual normal author/replay runs bind current candidate; unchanged independent actual earlier normal/optimized/false guard retain original PIDs/dates and are not rerun."
js(C/"review/review_summary.json",summary)

ready=json.loads((I/"readiness.json").read_text())
ready.update({"status":"final-operative-disposition-postimages-preparation_only","mathematical_status":"PASS","original_target_disposition":"already_solved","priority_status":"ALTERNATIVE_POLYNOMIAL_CRITERION_UNRESOLVED","whole_candidate_historical_subsumption_established":False,"alternative_polynomial_criterion_novelty":"UNRESOLVED","express_first_named_answer_priority":"UNVERIFIED","publication_authorization":False,"publication_readiness":False,"scientific_disposition_readiness":True,"disposition_execution_complete":False,"closure_operation_performed":False,"actual_closure_url":None,"actual_closure_status":None,"native_author_global_propagation":"PENDING_SEPARATE_REVIEWED_WRITER","preprint_created":False,"zenodo_created":False,"doi":None,"tracker_entry_created":False,"tracker_entry":None,"overall_program_complete":False})
ready.pop("disposition_readiness",None)
ready["archival_v2_corrections"]=ready.pop("current_corrections")
ready["current_corrections"]={"prepared_utc":utc(),"actual_preparation_pid":PID,"candidate_sha256":candidate["sha256"],"review_sha256":review_pin["sha256"],"hardened_independent_checker_sha256":hard,"author_assertions_each_actual_new_run":50840,"retained_independent_assertions":28722,"independent_rerun_claimed":False,"accepted_scientific_gate":pin(gate_path),"fresh_disposition_report":pin(fresh/"REPORT.md"),"fresh_report_reviewed_input_candidate_sha256":v2["CANDIDATE.md"]["sha256"],"source_status":"Full1975 original-target consequence accepted; existing2016/2026 source repairs retained; alternative polynomial novelty unresolved","included_in_current_archive_checkpoint_plan":False,"propagation":"pending separate reviewed writer"}
ready["independent_review"]={"verdict":"MATHEMATICS_PASS_ORIGINAL_TARGET_ALREADY_SOLVED_ALTERNATIVE_UNRESOLVED","review_sha256":review_pin["sha256"],"review_notice":"Historical review archival; fresh scientific outcome accepted for earlier input, no new postimage or service/global approval fabricated","author_assertions":50840,"independent_assertions":28722,"independent_runs_reused_not_rerun":True,"human_peer_review":False}
js(C/"readiness.json",ready)

record=json.loads((I/"source_record.json").read_text())
record["archival_source_dataset_status"]={k:record[k] for k in ["status","research_classification","research_summary","updated_at"]}
record["status"]="already_solved"
record["research_classification"]="ALREADY_SOLVED_ORIGINAL_LITERAL_TARGET_BY_OLDER_CONSEQUENCE"
record["research_summary"]="Original all-real sufficient-generalization target follows from verified1975 coefficient/radius theorems and scaling. Candidate mathematics PASS; alternative polynomial criterion novelty UNRESOLVED; whole historical subsumption not established; express first named-answer priority unverified. Draft correction only; actual native/global and closure operations pending."
record["archival_provenance_notice"]="Original dataset dates/status and triage are preserved as historical provenance; this postimage's already_solved is a prepared scientific correction, not a performed native/service update."
record["current_preparation"]={"status":"final-operative-disposition-postimages-preparation_only","prepared_utc":utc(),"actual_preparation_pid":PID,**outcome,"propagated_to_native_author_or_global":False,"human_peer_review":False}
js(C/"source_record.json",record)

with (C/"RESEARCH_LOG.md").open("a") as f:
 f.write("\n## Accepted original-target disposition preparation — "+utc()+"\n\nActual stage PID "+str(PID)+". Accepted fresh scientific gate supports original literal target already_solved by full Silverman1975/Mocanu–Reade1975 theorem consequence with R/W/h scaling. Candidate mathematics PASS; whole candidate historical subsumption not established; polynomial novelty UNRESOLVED; express first named history unverified. Prepared source/status/readiness/review/README duplicates without changing proof sections2–4. Actual new author/replay hash receipts pass50840 each; unchanged independent earlier28722 normal/optimized and false guard are retained with original PIDs/dates, not rerun. Effort1/5, substantive1,newproof0,no human referee. Actual closure/native/author/global pending, publication unauthorized, preprint/Zenodo/tracker false, DOI null. Completion estimate:100% bounded new disposition-postimage staging, not service/global/program completion.\n")

proofmark="## 2. One explicit weighted sum, including all real alpha"
def proof(s):return s.split(proofmark,1)[1].split("## 5.",1)[0]
ck(proof((C/"CANDIDATE.md").read_text())==proof((I/"CANDIDATE.md").read_text())==proof((O/"CANDIDATE.md").read_text()),"Proof sections2–4 changed")
post={str(p.relative_to(C)):pin(p) for p in C.rglob("*") if p.is_file()}
ck(len(post)==17 and set(post)==set(v2),"Exactly17 postimages required")
ck({str(p.relative_to(B)):pin(p) for p in B.rglob("*") if p.is_file()}==v2,"Preserved input_v2 snapshot changed")
ck(pin(C/"review/independent_checks.py")["sha256"]==hard,"Independent checker altered")
ck(pin(C/"review/independent_results.json")==v2["review/independent_results.json"],"Independent result altered")
for p in C.rglob("*.json"):json.loads(p.read_text())
d=N/"diffs_from_sealed_v2";d.mkdir()
changes=[]
for rel in v2:
 changed=post[rel]!=v2[rel];dp=None
 if changed:
  dp="diffs_from_sealed_v2/"+rel.replace("/","__")+".diff"
  textfile(N/dp,"".join(difflib.unified_diff((I/rel).read_text().splitlines(keepends=True),(C/rel).read_text().splitlines(keepends=True),fromfile="sealed_v2/"+rel,tofile="final_prepared_postimage/"+rel)))
 changes.append({"path":rel,"changed_from_v2":changed,"sealed_v2":v2[rel],"new_postimage":post[rel],"original_archival":original[rel],"diff_path":dp,"diff":pin(N/dp) if dp else None})
js(N/"CORRECTED_17_MANIFEST.json",{"schema":"pr134-final-qualified-disposition17/v1","actual_writer_pid":PID,"utc":utc(),"status":"final-operative-disposition-postimages-preparation_only","member_count":17,"changed_from_sealed_v2":sum(x["changed_from_v2"] for x in changes),"members":changes,"proof_sections2_3_4_byte_unchanged":True,"candidate_replay_identical":pin(C/"CANDIDATE.md")==pin(C/"review/author_replay/CANDIDATE.md"),"input_v2_preserved_byte_identically":True,"original17_unchanged":True,"hardened_checker_sha256":hard,"accepted_gate":pin(gate_path),"fresh_scientific_report":pin(fresh/"REPORT.md"),"source_pins":pin(N/"SOURCE_PINS.json"),"scientific_outcome":outcome,"excluded_from_current_core_checkpoint_plan":True})

report="# Final qualified disposition-postimage preparation\n\nStatus: final-operative-disposition-postimages-preparation_only. Exactly17 new postimages are prepared from authenticated sealed v2, with an exact input_v2 snapshot and all changed-path diffs. Original17, sealed v1/v2's166 members, the independent coefficient family's78 members, and the fresh disposition family's31 members remain unchanged. Proof sections2–4 are byte-identical to original and v2.\n\n"+old_answer.split("## 6. Accepted original-target disposition and older all-real answer\n\n",1)[1]
report+="\n## Actual staging receipts and remaining execution\n\nActual new normal author and duplicate replay each pass50840 controls and bind to candidate SHA"+candidate["sha256"]+". Unchanged explicit-if independent checker SHA"+hard+" is not rerun here; its earlier normal/optimized28722 and optimized false guard are copied with original actual PIDs/dates and identified as retained evidence. No historical review approval of edited postimage bytes is fabricated. No source PDF/preview is copied or published; SOURCE_PINS.json authenticates external private full1975 bytes, and private-primary-source directories are ignored/excluded.\n\nThe accepted scientific gate is copied at SHA1a3aa4f259f9b94afdbc02dae85969d9f49ff4e391a92ae6ed87cbce0cc9ef0f; fresh report5f05db76d89edda6a694e06f8c307c2ec6dc535b30bfeeacb609c37bde627623 and manifest76015f64bfa61ad0a4e92d20e47d1b78c2bcfd9be65f86b4b56fd6cb5c2322e9 are pinned/copied. Original effort1/5, one substantive approach, zero added central proof-search turns, and no human review remain unchanged.\n\nThis folder is excluded from the current core checkpoint plan. Actual closure URL/status and native/author/global propagation are pending a separate reviewed writer and may later be recorded in a new dated operation receipt; this seal must not be overwritten. No author/native/main/index/PR/service/package-publication writes or external individual outreach occurred. Bounded staging completion100%; overall program/service/global completion is not claimed.\n"
textfile(N/"REPORT.md",report)
js(N/"DOI_TRACKER_METADATA.json",{"actual_writer_pid":PID,"utc":utc(),"publication_authorization":False,"preprint_created":False,"zenodo_created":False,"doi":None,"tracker_entry_created":False,"tracker_entry":None,"closure_operation_performed":False,"actual_closure_url":None,"actual_closure_status":None,"native_author_global_propagation":"PENDING_SEPARATE_REVIEWED_WRITER"})
textfile(N/"README.md","# Frozen final disposition-postimage staging\n\nSee REPORT.md, CORRECTED_17_MANIFEST.json, corrected_attempt/ and diffs_from_sealed_v2/. Original target already_solved by verified older consequence; candidate math PASS; alternative polynomial novelty UNRESOLVED; express first named history unverified. Scientific clearance only. Actual closure/global/native/author pending; publication unauthorized; preprint/Zenodo/tracker false, DOI null. Earlier seals are untouched. No PDF/preview source bytes are copied. Current core checkpoint plan excludes this folder. A later actual operation must receive a new dated receipt without overwriting this stage.\n")
textfile(N/"RESEARCH_LOG.md","# Final disposition-stage research log\n\n- "+START+" (actual stage PID "+str(PID)+"): Authenticated accepted scientific gate, full fresh scientific seal, sealed v2/family and original17. Prepare new17 in own folder only. Completion estimate:5%.\n- "+utc()+" (actual stage PID "+str(PID)+"): Full1975/R/W/h source-qualified target already_solved classification prepared; candidate math PASS, polynomial novelty UNRESOLVED, express first named history unverified. Proof unchanged; current author/replay hash receipts refreshed; unchanged independent runs retained with original PIDs/dates. All17/diffs/pins/report and DOI/tracker false/null metadata sealed. Completion estimate:100% bounded preparation; actual closure/global/program work pending.\n")
# Final unchanged-input checks are read-only.
authenticate_manifest(V,"fef895ae92c3fe73d3a723dbec4ca662932d7268540c44bbcf8fd404595a1620",166)
authenticate_manifest(F,"07b33afe74644acf8c9064149c4a9946a0a84d89875275ab460e07930bd6b349",78)
authenticate_manifest(fresh,"76015f64bfa61ad0a4e92d20e47d1b78c2bcfd9be65f86b4b56fd6cb5c2322e9",31)
ck({str(p.relative_to(O)):pin(p) for p in O.rglob("*") if p.is_file()}==original,"Original17 final equality")
js(N/"RESULT.json",{"schema":"pr134-final-disposition-preparation-result/v1","status":"final-operative-disposition-postimages-preparation_only","actual_writer_pid":PID,"started_utc":START,"completed_utc":utc(),"completion_percent":100,"completion_scope":"Bounded reviewable disposition-stage17 only","candidate":candidate,"corrected17_manifest":pin(N/"CORRECTED_17_MANIFEST.json"),"report":pin(N/"REPORT.md"),"member_count":17,"changed_from_v2":sum(x["changed_from_v2"] for x in changes),"scientific_outcome":outcome,"proof_sections2_3_4_unchanged":True,"original17_v1_v2_family_fresh_seals_unchanged":True,"actual_new_author_assertions_each":50840,"independent_exercises_reused_not_rerun":True,"original_effort":"1/5","original_substantive_approaches":1,"added_central_proofs":0,"human_peer_review":False,"author_native_main_index_pr_service_packagepublish_writes":False,"new_outreach_or_download":False,"private_primary_bytes_copied":False,"excluded_from_current_core_checkpoint_plan":True})
journal("seal_final_disposition_staging",candidate=candidate,corrected17=17,changed_from_v2=sum(x["changed_from_v2"] for x in changes),scientific_clearance_only=True,actual_closure_global_pending=True,publication_authorization=False)
allmembers=[{"path":str(p.relative_to(N)),**pin(p)} for p in sorted(N.rglob("*")) if p.is_file() and p.name!="FINAL_MANIFEST.json"]
js(N/"FINAL_MANIFEST.json",{"schema":"pr134-final-disposition-postimages-seal/v1","actual_writer_pid":PID,"utc":utc(),"root":str(N),"status":"final-operative-disposition-postimages-preparation_only","self_excluded":True,"members":allmembers,"member_count":len(allmembers),"corrected17_manifest":pin(N/"CORRECTED_17_MANIFEST.json"),"input_v2_candidate_sha256":v2["CANDIDATE.md"]["sha256"],"input_v2_seal":pin(V/"FINAL_MANIFEST.json"),"accepted_scientific_gate":pin(gate_path),"scientific_outcome":outcome,"excluded_private_primary_paths":["private_primary_sources/","private_previews/"],"private_primary_bytes_copied":False,"excluded_from_current_core_checkpoint_plan":True})
for r in allmembers:ck(pin(N/r["path"])=={k:r[k] for k in ["bytes","sha256"]},"Final stage hash drift")
print(json.dumps({"status":"final-operative-disposition-postimages-preparation_only","actual_pid":PID,"utc":utc(),"candidate":candidate,"postimages":17,"changed_from_v2":sum(x["changed_from_v2"] for x in changes),"manifest":pin(N/"FINAL_MANIFEST.json"),"scientific_original_target":"already_solved","candidate_math":"PASS","alternative_polynomial_novelty":"UNRESOLVED","closure_and_global":"PENDING","publication_authorization":False},indent=2))


from pathlib import Path
import contextlib,datetime,io,json,sys
R=Path("/Users/alec/Documents/Math");D=R/"draft_pr_claimed_solved_700_800_20261012";T=D/"audits/pr789_30001478/tmp";M=T/"root-receipts";sys.path.insert(0,str(D));from graphql_scoped_commit import Remote,head_oid,commit_updates
assert not(M/"GUARD_REPAIR_CHECKPOINT_RECEIPT.json").exists();assert not(T/"FINAL_READINESS.json").exists()and not(T/"publication/STAGE_RECEIPT.json").exists()
updates={}
for name in["root-receipts","verification_recipes","publication"]:
 for p in(T/name).rglob("*"):
  if p.is_file():assert not p.is_symlink();updates[p.relative_to(R).as_posix()]=p.read_bytes()
for n in["publication_driver.py","READINESS_PLAN.json","TRACKER_SCOPE.json"]:
 p=T/n;updates[p.relative_to(R).as_posix()]=p.read_bytes()
for p in(D/"final_delivery").iterdir():
 if p.is_file():assert not p.is_symlink();updates[p.relative_to(R).as_posix()]=p.read_bytes()
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
entry="\n## "+now+" — PR789 prepublication guards hardened; first whole review ongoing\n\nFresh independent administrative adversary found2required guard improvements before any production action: the earlier driver trusted a numeric review count/truthy clean flag without binding actual completed artifacts, and fresh eligibility ran only before staging. Repaired driverSHA7c20099c6d07df06eceeda198df27c618c2b8e2ab150e6de5d596c103a09f24f now requires strict int/bool fields, at least2distinct freshly initialized completed whole reviewers, closed regular singly linked nonsymlinked authored packets with external MF/checker hashes, authenticated target/head/source/six-bound root-replay receipts, and a final current exact-package zero-issue review. Exact claimed-only/source/noacceptance/original-baseline-or-candidate eligibility rechecks immediately before the one publish POST as well as stage. Admin independently reports41mocked no-network controlsPASS across flags/types/identity/receipt/packet/specialfile/current-package/eligibility-race cases; final sealed admin/rootreplay still pending. These are administrative repairs only; frozen source151andall6 unchanged. FINAL_READINESS intentionally absent and READINESS_PLAN explicitlyPENDING; no production record, tracker append, PRready or merge.\n\nRoot additionally tested closed151-member source archive relocation to an owned path with spaces under Python3.14normal/3.12optimized, core custody0externalbodies; full10processreplay is separately bound to initial source verification, not falsely claimed for this root relocation. Whole reviewer01 has independently derived the universal theorem, read all source/checker/control code, reproduced four-page clean visual/typeset text and six files, and is completing runtime/source-history checks. Its ancillary frozen standalone test_publication harness needs ordinary TMPDIR on this Mac because the operative wrapper correctly rejects /var symlink ancestry; core --replay is unaffected. Exact v1willremainpreserved before any documented repair if recommended.\n\nRestored the8already-published authored PDF deliverables to final_delivery after old RAM mounts disappeared: exact bytes verified against native acceptance and public Zenodo records, total578245bytes, DOI/source bindings in RESTORATION_RECEIPT. This is artifact custody/delivery restoration only, with no other draft processing or repeated mathematical/priority audit, publication, tracker write or merge. All source bodies/private configs/controlscratch excluded. Current proof budget1/5/newsearchturns0. Case70%; shard83%.\n"
for retry in range(3):
 r=Remote(head_oid());u=dict(updates)
 for n in["RESEARCH_LOG.md","audits/pr789_30001478/RESEARCH_LOG.md"]:u[D.name+"/"+n]=r.read(D.name+"/"+n)+entry
 state=json.loads(r.read(D.name+"/STATE.json"));assert len(state["processed"])==10;state.update(updated_at=now,current_pr=789,current_stage="PR789 first fresh whole review ongoing; administrative publication guards repaired before production",overall_completion_estimate_percent=83);u[D.name+"/STATE.json"]=json.dumps(state,indent=2)+"\n"
 log=r.read(D.name+"/checkpoint_receipts.jsonl");prev=json.loads((M/"PREPRINT_CHECKPOINT_RECEIPT.json").read_text())
 if not any(json.loads(l).get("commit")==prev["commit"]for l in log.splitlines()if l):log+=json.dumps(prev)+"\n"
 u[D.name+"/checkpoint_receipts.jsonl"]=log;buf=io.StringIO()
 with contextlib.redirect_stdout(buf):receipt=commit_updates(r,u,"Harden PR789 review-bound publication and eligibility guards before production")
 (M/"GUARD_REPAIR_CHECKPOINT_RAW.txt").write_text(buf.getvalue())
 if receipt:break
else:raise RuntimeError("Three main races; reconcile")
(M/"GUARD_REPAIR_CHECKPOINT_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n");print(json.dumps({"result":"PASS","commit":receipt["commit"],"case_percent":70,"shard_percent":83,"production_mutation":False}))

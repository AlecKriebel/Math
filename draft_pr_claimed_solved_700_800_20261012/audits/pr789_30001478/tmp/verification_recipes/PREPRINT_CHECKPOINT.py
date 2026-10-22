from pathlib import Path
import contextlib,datetime,io,json,sys
R=Path("/Users/alec/Documents/Math");D=R/"draft_pr_claimed_solved_700_800_20261012";T=D/"audits/pr789_30001478/tmp";P=T/"preprint";M=T/"root-receipts";sys.path.insert(0,str(D));from graphql_scoped_commit import Remote,head_oid,commit_updates
assert not(M/"PREPRINT_CHECKPOINT_RECEIPT.json").exists()
freeze=json.loads((M/"PACKAGE_FREEZE_V1.json").read_text());repro=json.loads((M/"ROOT_RELEASE_REPRODUCTION.json").read_text());assert freeze["source_files"]==151 and repro["result"]=="PASS"
updates={}
for dirname in["intake","root-receipts","verification_recipes","publication"]:
 for p in(T/dirname).rglob("*"):
  if p.is_file():assert not p.is_symlink();updates[p.relative_to(R).as_posix()]=p.read_bytes()
for dirname in["math_source_geometry","math_quotient_algebra","priority_direct_history","priority_structural"]:
 w=T/dirname
 for row in json.loads((w/"MANIFEST.json").read_text())["files"]+[{"path":"MANIFEST.json"}]:
  p=w/row["path"];assert p.name==row["path"];updates[p.relative_to(R).as_posix()]=p.read_bytes()
for p in(P/"source").rglob("*"):
 if p.is_file():assert not p.is_symlink();updates[p.relative_to(R).as_posix()]=p.read_bytes()
for row in json.loads((P/"PACKAGE_INVENTORY.json").read_text())["files"]+[{"path":"PACKAGE_INVENTORY.json"},{"path":"RELEASE_INVENTORY.json"}]:
 p=P/row["path"];updates[p.relative_to(R).as_posix()]=p.read_bytes()
p=T/"publication_driver.py";updates[p.relative_to(R).as_posix()]=p.read_bytes()
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
entry="\n## "+now+" — PR789 four-page preprint and verification package frozen for fresh whole review\n\nPrepared A projective-line quotient of the Rogalski–Sierra algebra, version1.0,16October2026,CCBY4.0,AlecKriebel/ORCID. Full self-contained exact-quotient proof refutes both literal source assertions for all independent parameters; stronger direct-presentation theorem covers every field/beta²!=1/alpha arbitrary. Characteristic2/direct-versus-journal-family distinction, singular boundaries, exact positive-dimensional THCR image, classical credits, mandatory Nevins–Sierra inspected-preprint repetition/canonical-hypothesis gaps, Campbell distinctions and unresolved historical priority are carried through paper, README and exact metadata. AI-extensive/unrefereed/noexternalhuman/noformalproof disclosures explicit. Root corrected OWRcontributor to SusanJ.Sierra(jointDanRogalski) and strong-noetherian referencep1236 before source freeze; no candidate58file changed.\n\nBuilt-in editor compilation and actual Tectonic both succeeded; fourpages, no overflow/undefined warnings, all4renders root visually read. Closed source151files/MF6287da0dabdad505f3d312dfeefc9e75f34caaeccb267fada3f9119502cfa6be/checker700eaab42e6d98589fb2f1c6fa4a3077b4dd74cad4f336a00cb53bd6dfe47489. Frozen six distribution identities in PACKAGE_INVENTORY. Root portable source replay ran10normal/optimized processes (original operative wrapper+4independent families) and optionally rehashed139current primary evidence files; it explicitly distinguishes raw custody from reading and full-dataset historical receipts. Four Python3.14/3.12normal/O source baselines and four deterministic six-byte-identical package rebuilds PASS;17meaningful source/builder/PDF/path/alias/JSON rejection controls PASS. Initial builder correctly rejected an output alias of its input PDF; caller corrected to separate typeset input; source inventory caller excluded only rootmanifest, preserving all four nested packet manifests. No sealed packet/scientific repair needed. Original unchanged Zenodotool local strict check PASS; NO production record created. Driver preserves exact original-parent queued0/5 baseline or exact candidate row, sameclaimedhead/source/noacceptance and requires2completed whole reviews with final current zeroissues. Firstfresh whole-preprint adversary now has independent target-first position and is auditing full source/math/priority/PDF/package; final publication readiness not yet granted. Full third-party bodies/private configs/control andrender scratch excluded. Case65%; shard83%.\n"
for retry in range(3):
 remote=Remote(head_oid());u=dict(updates)
 for n in["RESEARCH_LOG.md","audits/pr789_30001478/RESEARCH_LOG.md"]:u[D.name+"/"+n]=remote.read(D.name+"/"+n)+entry
 state=json.loads(remote.read(D.name+"/STATE.json"));assert len(state["processed"])==10;state.update(updated_at=now,current_pr=789,current_stage="PR789 four-page package frozen and reproduced; fresh whole-preprint review01 underway",overall_completion_estimate_percent=83);u[D.name+"/STATE.json"]=json.dumps(state,indent=2)+"\n"
 log=remote.read(D.name+"/checkpoint_receipts.jsonl");prev=json.loads((M/"PRIORITY_CHECKPOINT_RECEIPT.json").read_text())
 if not any(json.loads(l).get("commit")==prev["commit"]for l in log.splitlines()if l):log+=json.dumps(prev)+"\n"
 u[D.name+"/checkpoint_receipts.jsonl"]=log
 capture=io.StringIO()
 with contextlib.redirect_stdout(capture):receipt=commit_updates(remote,u,"Prepare and reproduce PR789 projective-line quotient research note for fresh adversarial review")
 (M/"PREPRINT_CHECKPOINT_RAW.txt").write_text(capture.getvalue())
 if receipt:break
else:raise RuntimeError("Three main races; reconcile")
(M/"PREPRINT_CHECKPOINT_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps({"result":"PASS","commit":receipt["commit"],"source_files":151,"case_percent":65,"shard_percent":83}))

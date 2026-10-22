from pathlib import Path
import contextlib,datetime,hashlib,io,json,sys
R=Path("/Users/alec/Documents/Math");D=R/"draft_pr_claimed_solved_700_800_20261012";T=D/"audits/pr789_30001478/tmp";P=T/"preprint";M=T/"root-receipts";sys.path.insert(0,str(D));from graphql_scoped_commit import Remote,head_oid,commit_updates
assert not(M/"WHOLE01_V2_CHECKPOINT_RECEIPT.json").exists()and not(T/"FINAL_READINESS.json").exists()
assert json.loads((M/"ROOT_RELEASE_REPRODUCTION_V2.json").read_text())["result"]=="PASS"
updates={}
for name in["root-receipts","verification_recipes","publication"]:
 for p in(T/name).rglob("*"):
  if p.is_file():assert not p.is_symlink();updates[p.relative_to(R).as_posix()]=p.read_bytes()
for n in["publication_driver.py","READINESS_PLAN.json","TRACKER_SCOPE.json"]:
 p=T/n;updates[p.relative_to(R).as_posix()]=p.read_bytes()
for package in[P,T/"package_versions/v1_review01"]:
 for p in(package/"source").rglob("*"):
  if p.is_file():assert not p.is_symlink();updates[p.relative_to(R).as_posix()]=p.read_bytes()
 for row in json.loads((package/"PACKAGE_INVENTORY.json").read_text())["files"]+[{"path":"PACKAGE_INVENTORY.json"},{"path":"RELEASE_INVENTORY.json"}]:
  p=package/row["path"];updates[p.relative_to(R).as_posix()]=p.read_bytes()
w=T/"whole_preprint_round01"
for row in json.loads((w/"MANIFEST.json").read_text())["files"]+[{"path":"MANIFEST.json"}]:
 p=w/row["path"];assert p.name==row["path"];updates[p.relative_to(R).as_posix()]=p.read_bytes()
pins={"DRIVER_CONTROLS.py":"8d9d2c001634dffd3cedb9a3ebb513ceed62c0400f68e96d4028e9bfa3dbb5bb","MERGE_SCOPE.py":"175d1ead75b4de1eafa3b44ce45b86d618074a290f890ab377e72adfc43cdfff","PUBLIC_VERIFY.py":"6d4a708434399d4a0e379bc23b623ae097b0461bc6e9d166387020221656b7ae"}
for n,pin in pins.items():
 p=T/"admin_scope/packet"/n;assert hashlib.sha256(p.read_bytes()).hexdigest()==pin;updates[p.relative_to(R).as_posix()]=p.read_bytes()
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
entry="\n## "+now+" — PR789 first whole review complete; documentation clarified and different fresh second review underway\n\nFresh whole01completed41-file sealed packet MF01cdfc5148cf15b9251dd3a20f3c6cdcebc96f29576183634d6215c074d311a1/checkerd63c0aca0b293579c19ee7252b28fe8241862c5b73bf2ed0eee186d213e31884. Root read the full extensive report and independently authenticated/replayed4Python3.14/3.12normal/O packet modes plus4positive16negative packet controls. Peer fully read all151source files/25Python/32Markdown/88JSON/TeX/license/patch and duplicate archives, independently derived both spanning and whole-ideal tensor mechanisms, verified source/priorityboundaries, fetched6primaryPDFs, visually read4pages and separateTectonictextmatch, reran40sourceprocesses and exact6build, allPASS. Zero required mathematical/source/credit/priority/package repairs. One low nonblocking ancillary reproduction noteL1 was recorded: frozen standalone test_publication needs ordinary owned absolute TMPDIR on this Mac, because /var symlink ancestry is correctly rejected; all24unchanged controls pass with workaround. Core --replay unaffected; optional primarybodyargument documentedabsolute.\n\nPreserved exact first-reviewedv1source151and6 plus inventories at package_versions/v1_review01 before repair. Current sourceREADME now documents ordinary TMPDIR for that optional separate harness while retaining all58originals and ancestryguards. ONLY README+rootMANIFEST differ amongsame151sourcepaths; ONLY sourceZIP+conveniencekit differ among6releasefiles. TeX/PDF(60080bytes/SHA66d6d448245656cbedc8f219989833529723879561a2d5e6483b5289c6732c83), metadata, deposit and fourmath/prioritypackets remain byteidentical. Publication version remains first unpublished1.0. Current sourceMF5d7bccdc118a464da0e149804c4b512c88a9d28cbff2d8b3bc280d963dd4f348/checker700eaab42e6d98589fb2f1c6fa4a3077b4dd74cad4f336a00cb53bd6dfe47489. Root reran4coremodes/4exact-six-bytebuilds/17rejectioncontrols and2archive-relocationmodes; currentoptional139bodyfiles rehashed by4custodyjobs. Historicalv1full10/peer40process receipts are explicitly distinguished from currentfullreplay, which the newly initialized fresh whole02 is independently checking. Whole02 initialposition timestamp17:15:46Z preceded candidate/priorverdict exposure. No premature promotion or productionrecord.\n\nAdministrative adversary found/fixed a further scientific-identitycoupling gap: drivera02c7910936f6d871fc760af4f5f41005f2ca055dc7cc99e84913a0893a47f96 now derives and hardpins originalH/statement/fullreview from verified source, couplesreadiness to them, and requiresliteral originalH for stage/publish. Readonlypostpublication administrativeintegration canretainexplicit originalH binding. Combined strict completed-reviewartifact receipts/currentfinalzero/types/closedpaths and freshprestage/prepublishclaimedeligibility guards pass48independentmockedcontrols, independently rerun by root againstcurrentV2; 7completeMerkle scopecontrols/preintegrationdesign against5c2581... also rootPASS. Final production/publicmetadata/DOI/tracker/actualmerge/adminseal stillpending. Readinessplanhas1historicalcompletedreview/L1count1, finalcurrentfalse; FINAL_READINESS absent. No newsubstantiveproofsearchturns, budget1/5 unchanged. Full thirdparty bodies/extracts/renders/privateconfigs and allcontrols scratchexcluded. Case80%; shard83%.\n"
for retry in range(3):
 r=Remote(head_oid());u=dict(updates)
 for n in["RESEARCH_LOG.md","audits/pr789_30001478/RESEARCH_LOG.md"]:u[D.name+"/"+n]=r.read(D.name+"/"+n)+entry
 state=json.loads(r.read(D.name+"/STATE.json"));assert len(state["processed"])==10;state.update(updated_at=now,current_pr=789,current_stage="PR789 first fresh whole review complete; source documentation repaired; different fresh whole02 audits current package",overall_completion_estimate_percent=83);u[D.name+"/STATE.json"]=json.dumps(state,indent=2)+"\n"
 log=r.read(D.name+"/checkpoint_receipts.jsonl");prev=json.loads((M/"GUARD_REPAIR_CHECKPOINT_RECEIPT.json").read_text())
 if not any(json.loads(l).get("commit")==prev["commit"]for l in log.splitlines()if l):log+=json.dumps(prev)+"\n"
 u[D.name+"/checkpoint_receipts.jsonl"]=log;buf=io.StringIO()
 with contextlib.redirect_stdout(buf):receipt=commit_updates(r,u,"Preserve PR789 whole-review v1 and verify TMPDIR documentation repair for fresh final audit")
 (M/"WHOLE01_V2_CHECKPOINT_RAW.txt").write_text(buf.getvalue())
 if receipt:break
else:raise RuntimeError("Three main races; reconcile")
(M/"WHOLE01_V2_CHECKPOINT_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n");print(json.dumps({"result":"PASS","commit":receipt["commit"],"case_percent":80,"shard_percent":83,"source_files":151,"production_created":False}))

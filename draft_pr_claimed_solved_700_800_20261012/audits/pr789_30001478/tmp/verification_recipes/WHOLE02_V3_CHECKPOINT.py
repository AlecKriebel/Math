from pathlib import Path
import contextlib,datetime,hashlib,io,json,sys
R=Path("/Users/alec/Documents/Math");D=R/"draft_pr_claimed_solved_700_800_20261012";T=D/"audits/pr789_30001478/tmp";P=T/"preprint";M=T/"root-receipts";sys.path.insert(0,str(D))
from graphql_scoped_commit import Remote,head_oid,commit_updates
assert not(M/"WHOLE02_V3_CHECKPOINT_RECEIPT.json").exists()and not(T/"FINAL_READINESS.json").exists()
assert json.loads((M/"ROOT_RELEASE_REPRODUCTION_V3.json").read_text())["result"]=="PASS"
updates={}
for name in["root-receipts","verification_recipes","publication"]:
 for p in(T/name).rglob("*"):
  if p.is_file():assert not p.is_symlink();updates[p.relative_to(R).as_posix()]=p.read_bytes()
for n in["publication_driver.py","READINESS_PLAN.json","TRACKER_SCOPE.json"]:
 p=T/n;updates[p.relative_to(R).as_posix()]=p.read_bytes()
for package in[P,T/"package_versions/v1_review01",T/"package_versions/v2_review02"]:
 for p in(package/"source").rglob("*"):
  if p.is_file():assert not p.is_symlink();updates[p.relative_to(R).as_posix()]=p.read_bytes()
 for row in json.loads((package/"PACKAGE_INVENTORY.json").read_text())["files"]+[{"path":"PACKAGE_INVENTORY.json"},{"path":"RELEASE_INVENTORY.json"}]:
  p=package/row["path"];updates[p.relative_to(R).as_posix()]=p.read_bytes()
for name in["whole_preprint_round01","whole_preprint_round02"]:
 w=T/name
 for row in json.loads((w/"MANIFEST.json").read_text())["files"]+[{"path":"MANIFEST.json"}]:
  p=w/row["path"];assert p.name==row["path"];updates[p.relative_to(R).as_posix()]=p.read_bytes()
pins={"DRIVER_CONTROLS.py":"702b8dbf1b6a71a8b721910d57a3bfdd1990e18d8b605eb2a4a0cdcd5445ded1","MERGE_SCOPE.py":"175d1ead75b4de1eafa3b44ce45b86d618074a290f890ab377e72adfc43cdfff","PUBLIC_VERIFY.py":"cba5bba7181469cdf29617c3a6a4502b9b610ec9e8ec33ef4bc83289e31ffe68","TRACKER_VERIFY.py":"1df0acfdfe81ead0a824de028392f95e6455a685bf9222fab713512fbd2697e6"}
for n,pin in pins.items():
 p=T/"admin_scope/packet"/n;assert hashlib.sha256(p.read_bytes()).hexdigest()==pin;updates[p.relative_to(R).as_posix()]=p.read_bytes()
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
entry="\n## "+now+" — PR789 second complete fresh review, two low repairs, V3 sealed for new complete third review\n\nFresh whole02 completed a13-file independently sealed complete review (MFa794fd6e28e73159fa3d472feda611639bda59547dfcfd0fd6bbbac036054f0c,checker38bf8e99aa33b66f7f1e0c563aa8c34ccbebf57faa74b9904a43cc74d97f570f), including all151sourcefiles, universal independent derivation,40inner core processes,139current primary evidence files,four family controls14positive84negative,21own controls,all4PDFpages and matching independent Tectonicrender, freshprimary passages and conservativepriority. Zero mathematical/source-semantic/priority-scope issues; exactly2lowrequired repairs: OWR contribution bibliography ends1363 (not1362), while bodylocators1361–1362 staycorrect; optional algebra control test_packet accepts no--replay and needs an owned wholepacketcopy outsideclosedsource. Root manually read report, reproduced bothfindings and corrected2positive16negativealgebracontrols, independently checked closed13files/fourinterpreter modes/21controls.\n\nExact second-reviewedV2source151/six andinventories preserved at package_versions/v2_review02 beforeanyrepair. CurrentV3changesONLYmain.tex onebibliographicdigit,README explicit superseding correct ancillarycommand,PREPRINT_BINDINGS androotMANIFEST; other147sourcepaths/all58originals/fourmathprioritypackets unchanged. Mainclaims unchanged;metadata/deposit byteexact. Recompiled4pages with actualTectonic and editorcompiler; root visually checkedall4newrenders,first3renderPNGs byteidentical. NewPDF60079SHA c91648374d0467758de9773c95ef37b32c275993a20d2e0d9067c20702f18994. CurrentMF50baca75de83bb4959f52b88762b020a65181428d200dffc4f343db8e026f9de, unchangedchecker700eaab42e6d98589fb2f1c6fa4a3077b4dd74cad4f336a00cb53bd6dfe47489. Root4coremodes/4exact6builds/17negativecontrols and2archivecorerelocations PASS;139freshoptionalbodyfiles/4custodyjobsPASS; originalZenodotoollocalcheckPASS. Publicationversion staysfirstunpublished1.0.\n\nDifferent newly initialized whole03 independently positions on target beforecandidate/priorverdicts, then audits fullcurrentpackage. Readinessplan binds2historicalcompletedreviewpackets/rootreceipts andtheir actualfindings, finalcurrentfalse; FINAL_READINESS absent. Adminsourcepins explicitlyreboundV3; rootreran48mockedguardcontrols with exactdrivera02, separate13metadata and12trackerparser controls prepared. No deposit,publication,trackerappend,ready/merge/native mutation yet. PriorityUNRESOLVED/no firstness/currentworldwideopen claim; no newsubstantiveproofturns,budget1/5unchanged. Authmaterial/fullthirdpartybodies/renders/scratch excluded. Case80%;shard83%.\n"
for retry in range(3):
 r=Remote(head_oid());u=dict(updates)
 for n in["RESEARCH_LOG.md","audits/pr789_30001478/RESEARCH_LOG.md"]:u[D.name+"/"+n]=r.read(D.name+"/"+n)+entry
 state=json.loads(r.read(D.name+"/STATE.json"));assert len(state["processed"])==10;state.update(updated_at=now,current_pr=789,current_stage="PR789 whole02 complete; two low corrections sealed V3; fresh full whole03 underway",overall_completion_estimate_percent=83);u[D.name+"/STATE.json"]=json.dumps(state,indent=2)+"\n"
 log=r.read(D.name+"/checkpoint_receipts.jsonl");prev=json.loads((M/"WHOLE01_V2_CHECKPOINT_RECEIPT.json").read_text())
 if not any(json.loads(l).get("commit")==prev["commit"]for l in log.splitlines()if l):log+=json.dumps(prev)+"\n"
 u[D.name+"/checkpoint_receipts.jsonl"]=log;buf=io.StringIO()
 with contextlib.redirect_stdout(buf):receipt=commit_updates(r,u,"Preserve PR789 second whole review and seal bibliography/reproduction corrections for fresh full audit")
 (M/"WHOLE02_V3_CHECKPOINT_RAW.txt").write_text(buf.getvalue())
 if receipt:break
else:raise RuntimeError("Three main races; reconcile")
(M/"WHOLE02_V3_CHECKPOINT_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps({"result":"PASS","commit":receipt["commit"],"case_percent":80,"shard_percent":83,"production_created":False}))


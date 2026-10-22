from pathlib import Path
import contextlib,datetime,hashlib,io,json,sys
R=Path("/Users/alec/Documents/Math");D=R/"draft_pr_claimed_solved_700_800_20261012";T=D/"audits/pr789_30001478/tmp";P=T/"preprint";M=T/"root-receipts";sys.path.insert(0,str(D));from graphql_scoped_commit import Remote,head_oid,commit_updates
assert not(M/"CANONICAL_HANDLE_V4_CHECKPOINT_RECEIPT.json").exists()
g=json.loads((T/"FINAL_READINESS.json").read_text());assert g["result"]=="PENDING_FRESH_WHOLE04_CANONICAL_METADATA"and g["final_current_round_clean"]is False
assert json.loads((M/"ROOT_RELEASE_REPRODUCTION_V4.json").read_text())["result"]=="PASS"
updates={}
for n in["root-receipts","verification_recipes","publication"]:
 for p in(T/n).rglob("*"):
  if p.is_file():assert not p.is_symlink();updates[p.relative_to(R).as_posix()]=p.read_bytes()
for n in["publication_driver.py","READINESS_PLAN.json","FINAL_READINESS.json","TRACKER_SCOPE.json"]:
 p=T/n;updates[p.relative_to(R).as_posix()]=p.read_bytes()
for package in[P,T/"package_versions/v3_review03"]:
 for p in(package/"source").rglob("*"):
  if p.is_file():assert not p.is_symlink();updates[p.relative_to(R).as_posix()]=p.read_bytes()
 for row in json.loads((package/"PACKAGE_INVENTORY.json").read_text())["files"]+[{"path":"PACKAGE_INVENTORY.json"},{"path":"RELEASE_INVENTORY.json"}]:
  p=package/row["path"];updates[p.relative_to(R).as_posix()]=p.read_bytes()
 for n in["FINAL_READINESS_AT_CREATION_STAGE.json","READINESS_AT_PUBLICATION_ORIGINAL.json"]:
  p=package/n
  if p.exists():updates[p.relative_to(R).as_posix()]=p.read_bytes()
pins={"DRIVER_CONTROLS.py":"3ff99091083bca1e8c2beb54238865d86cd4fefcb0c42da9f83278aff49cb88d","PUBLIC_VERIFY.py":"101928f4a7217437e9085c1f9e3a2c87938fa683a35670d1c9d8ad5b9e65669f","MERGE_SCOPE.py":"175d1ead75b4de1eafa3b44ce45b86d618074a290f890ab377e72adfc43cdfff","TRACKER_VERIFY.py":"1df0acfdfe81ead0a824de028392f95e6455a685bf9222fab713512fbd2697e6"}
for n,pin in pins.items():
 p=T/"admin_scope/packet"/n;assert hashlib.sha256(p.read_bytes()).hexdigest()==pin;updates[p.relative_to(R).as_posix()]=p.read_bytes()
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
entry="\n## "+now+" — PR789 sole unpublished draft retained; canonical Handle metadata V4 requires fresh full review\n\nThe third complete fresh review and rootreplay cleared exactV3 source151/six withzeroissues; checkpoint e0eca0b865f7e79474c9ce3eb40981a969a1fe33 preserved actual3-roundPASSgate SHA27beef2982540a003d0f95a30153c51d8ef182b5a721418afa904ad3ee24c0ea. Productionstage then created exactlyONEdraft23423736 anduploadedbothcorrectfiles, but unchangedstrictuploadtool rejected related_identifiers. NOTPUBLISHED, no publicationintent; knownstate saved immediately, nosecondcreate. AuthenticatedreadonlyGET found exactlyonefourthentry canonicalization: Campbell https://hdl.handle.net/1842/22886 schemeurl becomes1842/22886 schemehandle, samereferencesrelation/order/allotherfields. OfficialZenodoAPI related_identifiersdocumentation independentlyread byroot/admin explicitlysupportsHandle/automaticnormalization. We chosegloballycanonicalauthoredmetadata, avoidinganycaseadapter or hiddennormalization.\n\nExactV3source/six/inventories andg90 preservedpackage_versions/v3_review03. Originalpublication/READINESS_AT_PUBLICATION.json27beef remainsimmutable ascreation-stage snapshot; a distinct READINESS_AT_PUBLICATION_V4.json willbindthefuturecompleted04gatebeforepublication. LiveFINAL_READINESS andREADINESS_PLAN nowPENDING_FRESH_WHOLE04_CANONICAL_METADATA/currentfalse; deliberatelycannotpublish. ExactlyTWOsourcepathschangevsV3:zenodo-metadata.jsonandrootMANIFEST; other149—includingproof,TeX,PDFbindings,checker,builder,58originalsand4familypackets—byteexact. SixonlyZIP/deposit/metadata/kit changed;PDF60079/c916...unchanged,noretypesetting orPDFmarkerrepeat. CurrentMFb20f39f39a33b18822cff51850f8b5b220e139af4d7badec23a7f5a7e17805aa/checker700ea...;ZIP338683/9dfb13a945de2fe4d088eef8cd86ca1f9ecdb75b87162285a8fa4b7c1aab94b6. Root4coremodes/4exact6builds/17negativecontrols/2archivecorerelocations/139freshcustodyPASS. V4administrative49controls explicitlyrejectactualpendinggate;13canonicalmetadatacontrolsPASS. Thesearepreparationtests, notpublicationapproval.\n\nNewfreshwhole04 frozeindependenttargetonlystrategy SHA0f626c482745e311f1a50c226dda4f98d766973e3b4278ba19cb13b568e9140e beforecandidate/oldverdicts, independentlyfoundscalarandstronger2generatorP1quotient,andnowauditsfullcurrentmath/source/priority/code/PDF/reproduction. Lateronlyaftercurrent04zero/rootreplay, replaceONLYoldunpublishedZIPandconfirmcanonicalmetadata inSAMEknown23423736usingunchangedoriginaltool; noadditionalcreate. Authorsemantics/acceptedmath/priorityUNRESOLVEDunchanged. No firstness/absence/currentworldwideopenclaim, no newsubstantiveproofturns,budget1/5preserved. No GWSappend, PRready/merge/nativeyet. Privateauth/fullthirdpartybodies/renders/controlscratch excluded. Case82%;shard83%.\n"
for retry in range(3):
 r=Remote(head_oid());u=dict(updates)
 for n in["RESEARCH_LOG.md","audits/pr789_30001478/RESEARCH_LOG.md"]:u[D.name+"/"+n]=r.read(D.name+"/"+n)+entry
 state=json.loads(r.read(D.name+"/STATE.json"));assert len(state["processed"])==10;state.update(updated_at=now,current_pr=789,current_stage="PR789 canonical Handle metadata V4; sole unpublished draft23423736; fresh whole04 required",overall_completion_estimate_percent=83);u[D.name+"/STATE.json"]=json.dumps(state,indent=2)+"\n"
 log=r.read(D.name+"/checkpoint_receipts.jsonl");prev=json.loads((M/"WHOLE_REVIEW_READY_CHECKPOINT_RECEIPT.json").read_text())
 if not any(json.loads(l).get("commit")==prev["commit"]for l in log.splitlines()if l):log+=json.dumps(prev)+"\n"
 u[D.name+"/checkpoint_receipts.jsonl"]=log;buf=io.StringIO()
 with contextlib.redirect_stdout(buf):receipt=commit_updates(r,u,"Canonicalize PR789 thesis Handle metadata and preserve sole unpublished draft for fresh full audit")
 (M/"CANONICAL_HANDLE_V4_CHECKPOINT_RAW.txt").write_text(buf.getvalue())
 if receipt:break
else:raise RuntimeError("Three main races; reconcile")
(M/"CANONICAL_HANDLE_V4_CHECKPOINT_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps({"result":"PASS","commit":receipt["commit"],"case_percent":82,"shard_percent":83,"known_only_draft":23423736,"published":False}))


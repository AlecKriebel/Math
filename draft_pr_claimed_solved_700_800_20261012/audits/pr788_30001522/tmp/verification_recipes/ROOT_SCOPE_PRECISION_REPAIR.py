from pathlib import Path
import datetime,hashlib,json,shutil
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr788_30001522/tmp");P=T/"preprint";S=P/"source";M=T/"root-receipts"
# Execute only after first completed adversarial packet has been sealed and authenticated.
review=T/"whole_review01_restarted"
if not(review/"MANIFEST.json").exists()or not(review/"VERDICT.json").exists():raise RuntimeError("First completed whole-review packet must be sealed before repairing its exact inputs")
oldpin="bdfe29cd2a46d035cda5d83a101775283125c17b1f432b0f0f0994b5ba0819ff"
assert hashlib.sha256((S/"MANIFEST.json").read_bytes()).hexdigest()==oldpin
old_inventory=json.loads((P/"PACKAGE_INVENTORY.json").read_text())
version=T/"package_versions/v1_review01";version.parent.mkdir(parents=True,exist_ok=True)
if version.exists():raise RuntimeError("The reviewed version snapshot already exists; reconcile rather than overwrite")
shutil.copytree(P,version)
for row in old_inventory["files"]:
 b=(P/row["path"]).read_bytes();assert len(b)==row["bytes"]and hashlib.sha256(b).hexdigest()==row["sha256"]
 target=version/row["path"];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b)
(version/"PACKAGE_INVENTORY.json").write_text(json.dumps(old_inventory,indent=2)+"\n")
for name in["paper.tex","README.md","zenodo-metadata.json"]:
 path=S/name;before=path.read_text()
 after=before.replace("no continuous circle action","no nontrivial continuous circle action").replace("while continuous circle actions are excluded","while nontrivial continuous circle actions are excluded")
 if name=="paper.tex":
  old_date="Specific locators refer to the author-hosted version dated 22 July 2025,\npp.~20--22:"
  new_date="Specific locators refer to the author-hosted arXiv v2 (header 22 July 2025;\ninternal Date line 23 July 2025), pp.~20--22:"
  assert old_date in after
  after=after.replace(old_date,new_date)
 assert after!=before,name
 path.write_text(after)
scope=json.loads((T/"TRACKER_SCOPE.json").read_text());scope["priority_summary"]=scope["priority_summary"].replace("no continuous circle action","no nontrivial continuous circle action")
(T/"TRACKER_SCOPE.json").write_text(json.dumps(scope,indent=2,ensure_ascii=False)+"\n")
clarification="# Circle-action wording in the related-work discussion\n\nThe current manuscript, metadata and archive README explicitly say that the Cappell–Weinberger–Yan/Mundet predecessor examples have no nontrivial continuous circle action. Every space admits the trivial action. Excluding effective circle actions implies the stated exclusion of nontrivial actions: the kernel of a nontrivial continuous circle action is a proper closed subgroup and therefore finite; the quotient is again a circle acting effectively. In particular no free circle action exists.\n\nEarlier sealed review packets and immutable original files are preserved byte for byte. Their standard shorthand about absence of a circle action is interpreted in this precise nontrivial/effective sense. This editorial clarification changes no Wu-manifold theorem, proof, priority disposition or exclusion by the nonabelian fundamental group. All historical gates and reproduction records in the archive retain their own dates and input versions; current release identities are bound by MANIFEST.json and PREPRINT_BINDINGS.json.\n"
(S/"PUBLICATION_SCOPE_CLARIFICATION.md").write_text(clarification)
(M/"ROOT_CIRCLE_ACTION_PRECISION_REPAIR.json").write_text(json.dumps({"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PRECISION_INTEGRATED_BEFORE_RECOMPILE_REBIND","old_source_manifest_sha256":oldpin,"original48_changed":False,"sealed_review_packets_changed":False,"manuscript_metadata_README_tracker_updated":True,"Debray_Yu_arxiv_header22July2025_and_internalDate23July2025_distinguished":True,"first_review_inputs_preserved":str(version),"new_PDF_bindings_manifest_six_and_second_review_required":True,"publication_ready":False},indent=2)+"\n")
print("Precision applied; compile, bind, rebuild, reproduce and new whole reviewer still required.")

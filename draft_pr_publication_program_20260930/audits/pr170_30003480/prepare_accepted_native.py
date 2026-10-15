"""Record actual reviewed publication in an operational native template."""
from pathlib import Path
import datetime,hashlib,json,shutil
A=Path(__file__).resolve().parent
ORIGINAL="d04c7991532ef65d70782c7d7fdfc1dcbfdf90a7"
def require(c,m):
 if not c:raise RuntimeError(m)
def save(p,j):p.write_text(json.dumps(j,indent=2)+"\n")
def pin(p):
 b=p.read_bytes();return {"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
def main():
 gate=json.loads((A/"ROOT_PUBLICATION_GATE.json").read_text());pub=json.loads((A/"ZENODO_PUBLICATION_READBACK.json").read_text());tracker=json.loads((A/"TRACKER_ACCEPTANCE.json").read_text())
 require(gate["status"]=="READY_FOR_AUTHORIZED_PUBLICATION" and gate["fresh_seal_first_review_clean"],"Final scientific gate required")
 require(pub["state"]=="published" and tracker["DOI"]==pub["doi"] and tracker["DOI_count"]==1,"Actual publication and unique tracker required")
 before=A/"native_proposal_v2";after=A/"integration_preparation/native_accepted"
 require(not after.exists(),"Existing unknown native preparation needs reconciliation")
 prep=json.loads((A/"PACKAGE_V2_PREPARATION.json").read_text())
 for n,v in prep["native_files"].items():require(pin(before/n)==v,"Reviewed native input changed")
 after.parent.mkdir(exist_ok=True);shutil.copytree(before,after)
 for p in after.rglob("*"):
  if p.is_file():p.chmod(0o644)
 now=datetime.datetime.now(datetime.UTC).isoformat()
 paragraph="Case checkpoint50%: mathematics and bounded priority audit cleared; whole-package review and publication/disposition pending. No DOI or tracker entry exists yet."
 text=(after/"README.md").read_text();require(paragraph in text,"Prepared README differs")
 text=text.replace(paragraph,"Published and tracked after the review/repair loop. The initial V1 package review's accidental prior-summary exposure remains qualified; its two presentation/evidence issues were repaired. A new reviewer sealed a substantive direct-input reconstruction before earlier verdicts and cleared the complete frozen V2 package. DOI: "+pub["doi_url"]+". Tracker: "+tracker["range"]+", DOI occurs once. Original-head MAIN integration remains pending; case90%.")
 (after/"README.md").write_text(text)
 old=(after/"COUNTEREXAMPLE.md").read_text()
 ending="Publication and final disposition require completion of the fresh package-review loop."
 require(ending in old,"Expected prepared note ending absent")
 text=old.replace(ending,"The review/repair loop is complete: the initial package assessment remains explicitly qualified, and the new direct-input seal-first reviewer found no substantive issue in the frozen V2 package. Published research note: "+pub["doi_url"]+". One tracker row is verified. Original-head MAIN integration remains pending.")
 (after/"COUNTEREXAMPLE.md").write_text(text)
 require(old.split("## 8.",1)[0]==text.split("## 8.",1)[0],"Reviewed proof/source sections changed")
 j=json.loads((after/"source_record.json").read_text())
 j["current_audit"].update({"UTC":now,"whole_package_review_pending":False,"whole_package_review_complete":True,"first_package_review_independence":"qualified accidental prior-summary exposure","final_fresh_seal_first_review_clean":True,"publication_package":"publication_package_v2","DOI":pub["doi"],"tracker_range":tracker["range"],"original_head_merge_pending":True})
 j["literature_assessment"]=j["literature_assessment"].replace("Package publication/disposition pending.","Package published at "+pub["doi_url"]+" after a fresh clean complete-package review; original-head integration pending.")
 save(after/"source_record.json",j)
 for name in ["audit_status.json","upstream_report.json"]:
  j=json.loads((after/name).read_text())
  j.update({"UTC":now,"status":"PUBLISHED_TRACKED_ORIGINAL_HEAD_MERGE_PENDING" if name=="audit_status.json" else "claimed_solved","whole_package_clearance":True,"preprint_publication_pending":False,"DOI":pub["doi"],"tracker_row":tracker["range"],"original_head_merge_pending":True,"first_package_review_independence":"qualified accidental prior-summary exposure","final_fresh_seal_first_review_clean":True})
  save(after/name,j)
 with (after/"RESEARCH_LOG.md").open("a") as f:f.write("\n"+now+" — Case90%: frozen V2 PDF/support and exact metadata actually published at "+pub["doi_url"]+"; one GWS tracker row "+tracker["range"]+" accepted. Initial qualified review and its two presentation/evidence repairs preserved; new direct-input seal-first complete-package adversary clean. Mathematical proof, publication bytes,17historical files unchanged. Original-head merge remains pending.\n")
 for name in ["ZENODO_PUBLICATION_READBACK.json","TRACKER_ACCEPTANCE.json"]:shutil.copyfile(A/name,after/name)
 save(after/"readiness.json",{"UTC":now,"status":"PUBLISHED_TRACKED_ORIGINAL_HEAD_MERGE_PENDING","PR":170,"problem_id":30003480,"original_head":ORIGINAL,"mathematics_cleared":True,"bounded_priority_audit_complete":True,"qualified_contemporary_disclosure":True,"exclusive_priority_or_mutual_independence_certified":False,"whole_package_review_rounds":2,"uncontaminated_fresh_final_reviews":1,"initial_review_independence":"qualified accidental prior-summary exposure","fresh_seal_first_review_clean":True,"published":True,"DOI":pub["doi"],"tracker_range":tracker["range"],"tracker_DOI_count":1,"merged":False,"case_percent":90,"unrefereed":True,"extensive_AI_assistance":True})
 allowed={"README.md","COUNTEREXAMPLE.md","RESEARCH_LOG.md","source_record.json","audit_status.json","upstream_report.json","SHA256SUMS"}
 for p in before.rglob("*"):
  if p.is_file() and str(p.relative_to(before)) not in allowed:require(p.read_bytes()==(after/p.relative_to(before)).read_bytes(),"Reviewed science/package/history changed")
 originals={str(p.relative_to(before)) for p in before.rglob("*") if p.is_file()}
 names={str(p.relative_to(after)) for p in after.rglob("*") if p.is_file()}
 require(names==originals|{"readiness.json","ZENODO_PUBLICATION_READBACK.json","TRACKER_ACCEPTANCE.json"},"Unexpected native member")
 (after/"SHA256SUMS").write_text("".join(pin(after/n)["sha256"]+"  "+n+"\n" for n in sorted(names-{"SHA256SUMS"})))
 save(after.parent/"CURRENT_TEMPLATE.json",{"UTC":now,"current_template":"native_accepted","reviewed_proposal":"native_proposal_v2","reviewed_package":gate["package"],"science_and_deposited_bytes_unchanged":True,"proof_sections_unchanged":True,"original17_history_unchanged":True,"post_review_operational_changes":sorted(allowed|{"readiness.json","ZENODO_PUBLICATION_READBACK.json","TRACKER_ACCEPTANCE.json"}),"MAIN_integration_pending":True,"native_files":len(names)})
 body="""The original single-polynomial proposal is resolved negatively in its stated real binary-tensor closed-unit-ball domain. For every n>=3 no determinant-only polynomial P defines the Gram locus by P>=0 inside its cube or convex hull. The higher-n proof uses exact zero-determinant faces; the note also supplies a strictly positive rational n4 counterexample to Seigal's proposed Q1-Q2 formula. No stronger positive-only all-n or finite-conjunction result is claimed.

Established marginal polygon criteria, real constructions and general boundary multiplicity principles are credited. GitHub records the original theorem-bearing PR on September30 at13:15:23UTC. Ferudun's October2 preprint DOI10.5281/zenodo.23111048 proves the exact overlapping result with an equivalent mechanism and a stronger positive-interior higher-n scope, and receives explicit credit. These are contemporaneous separate disclosures. Historical visibility lacks an independent archive; commit dates are author-controlled. Literal simultaneity, mutual independence and exclusive firstness are not certified. The formal preprint is dated October12.

Three distinct mathematics families and three fresh bounded-priority families assessed the result. The first full-package review's accidental preseal-summary exposure remains explicitly qualified. Its two presentation/evidence issues were repaired across the V2 supplement and native note. A new reviewer sealed a substantive direct-input mathematical reconstruction before reading previous verdicts, then cleared the complete frozen package. Exact controls perform46274 finite checks per baseline with identical ordinary/optimized outputs and eight deliberate semantic false variants rejected; the universal theorem rests on the written proof.

Published research note, source, exact controls and namespaced audit/evidence supplement: [DOI](DOI_URL). Exact intended metadata and uploaded bytes were checked. One Google Workspace tracker row TRACKER_RANGE was verified by returned values and fresh reads. Extensive AI assistance; unrefereed and no conventional human peer review.

The original17-file submission is preserved unchanged in historical_original_submission/. Active controls and the scientific publication package are distinct from the historical assert-based checkers. Original author-head integration and actual MAIN acceptance remain pending.
"""
 body=body.replace("[DOI](DOI_URL)","["+pub["doi"]+"]("+pub["doi_url"]+")").replace("TRACKER_RANGE",tracker["range"])
 (A/"PR_BODY_ACCEPTED.md").write_text(body)
 save(A/"CURRENT_CASE_STATUS.json",{"UTC":now,"status":"PUBLISHED_TRACKED_ORIGINAL_HEAD_MERGE_PENDING","PR":170,"problem_id":30003480,"completion_estimate_percent":90,"mathematics_cleared":True,"priority_audit_complete":True,"publication_clearance":True,"fresh_final_review_clean":True,"DOI":pub["doi"],"tracker_row":tracker["range"],"MAIN_disposition_complete":False,"fully_completed_count":33,"published_count":19,"goal_complete":False})
 print(json.dumps({"status":"ACTUAL_PUBLISHED_TRACKED_NATIVE_TEMPLATE_PREPARED","native_files":len(names),"DOI":pub["doi"],"tracker":tracker["range"],"science_unchanged":True}))
if __name__=="__main__":main()


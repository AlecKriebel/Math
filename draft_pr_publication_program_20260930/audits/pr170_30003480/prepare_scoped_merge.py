"""Prepare exactly the granted two-parent overlay; never move a local ref."""
from pathlib import Path
import base64,datetime,hashlib,importlib.util,json,re,sys
A=Path(__file__).resolve().parent;C=A.parents[2];P=A.parents[1]
sp=importlib.util.spec_from_file_location("api152",P/"audits/pr152_5000006/prepare_scoped_merge.py");m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
api,require,save,lookup,changed_leaves,body_at=m.api,m.require,m.save,m.lookup,m.changed_leaves,m.body_at
ORIGINAL="d04c7991532ef65d70782c7d7fdfc1dcbfdf90a7"
def pin(p):
 b=p.read_bytes();return {"local_path":str(p),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest(),"git_blob":hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()}
def check_grant(expected):
 grant=json.loads((A/"private/MERGE_WRITER_RETURN.json").read_text())
 require(grant["explicit_acknowledgement_received"] and grant["expected_MAIN"]==expected,"Fresh exact bounded acknowledgement absent")
 require(datetime.datetime.now(datetime.UTC)<datetime.datetime.fromisoformat(grant["expires_UTC"]),"Window expired")
 require(hashlib.sha256((A/"SCOPED_MERGE_SCOPE_PLAN.json").read_bytes()).hexdigest()==grant["scope_plan_sha256"],"Granted scope changed")
 return grant
def main(expected):
 check_grant(expected)
 plan=json.loads((A/"SCOPED_MERGE_SCOPE_PLAN.json").read_text());gate=json.loads((A/"ROOT_PUBLICATION_GATE.json").read_text());pub=json.loads((A/"ZENODO_PUBLICATION_READBACK.json").read_text());tracker=json.loads((A/"TRACKER_ACCEPTANCE.json").read_text())
 require(gate["status"]=="READY_FOR_AUTHORIZED_PUBLICATION" and gate["fresh_seal_first_review_clean"],"Scientific gate absent")
 require(pub["state"]=="published" and pub["doi"]==tracker["DOI"] and tracker["DOI_count"]==1,"Actual publication/tracker absent")
 require(api("git/ref/heads/main")["object"]["sha"]==expected,"MAIN moved; no rebase/adoption")
 pr=api("pulls/170");require(pr["state"]=="open" and not pr["draft"] and pr["head"]["sha"]==ORIGINAL and pr["body"]==(A/"PR_BODY_ACCEPTED.md").read_text(),"Actual original PR state/head/body changed")
 parent=api("git/commits/"+expected);overlay={}
 for n,v in plan["selected_files"].items():
  p=Path(v["local_path"]);require(pin(p)==v,"Selected bytes changed "+n);overlay[n]=p
 out=A/"merge_checkpoint";require(not out.exists(),"Existing unknown merge objects require reconciliation");out.mkdir()
 now=datetime.datetime.now(datetime.UTC).isoformat()
 qpath="unsolved_math_prioritization/QUEUE.md";old=body_at(qpath,expected).decode();lines=old.splitlines(keepends=True)
 indices=[i for i,line in enumerate(lines) if "| 30003480 /" in line];require(len(indices)==1,"Target QUEUE row not unique")
 i=indices[0];cells=lines[i].rstrip("\n").split("|");require(len(cells)==14,"QUEUE schema changed")
 cells[8]=" claimed_solved ";cells[9]=" 2/5 "
 cells[11]=" Verified full negative resolution of determinant-only single-polynomial description in original closed real binary Frobenius ball, cube/hull, n>=3; positive n4 rational counterexample. Known marginal/real-construction/boundary principles credited. Sep30 GitHub record precedes exact stronger Oct2 Ferudun overlap DOI10.5281/zenodo.23111048; contemporaneous separate disclosures, no exclusive priority or independence certificate.46274 finite controls per baseline, eight false variants rejected; initial package review qualified, new direct-input seal-first final review clean. Extensive AI; unrefereed. "
 cells[12]=" ["+pub["doi"]+"]("+pub["doi_url"]+") ";lines[i]="|".join(cells)+"\n";new="".join(lines)
 require(len(old.splitlines())==len(new.splitlines()) and sum(x!=y for x,y in zip(old.splitlines(),new.splitlines()))==1,"Other QUEUE rows changed")
 (out/"QUEUE.accepted.md").write_text(new);overlay[qpath]=out/"QUEUE.accepted.md"
 prefix="draft_pr_publication_program_20260930/"
 j=json.loads(body_at(prefix+"CURRENT_PROGRESS.json",expected))
 require(j["fully_completed_count"]==33 and len(j["fully_completed_eligible_PRs"])==33 and j["published_count"]==18 and len(j["published_PRs"])==18 and j["current_PR"]==170 and j["last_completed_PR"]==166,"Actual programme census differs")
 require(170 not in j["published_PRs"],"Publication already accounted")
 j.setdefault("historical_preparation_snapshots",[]).append({"UTC":now,"PR":170,"fields":{k:v for k,v in j.items() if k.startswith("current_")},"note":"Actual publication/tracker accepted; original-head merge still pending at preparation."})
 j["published_PRs"].append(170);j["published_count"]=19;j.pop("persistent_goal_status",None)
 j.update({"UTC":now,"updated_UTC":now,"current_status":"PUBLISHED_TRACKED_ORIGINAL_HEAD_MERGE_PENDING","current_PR_workflow_percent":90,"current_workflow_estimate_percent":90,"current_publication_ready":True,"current_publication_package_reviews_complete":True,"current_publication_package_reviews_required":False,"current_publication_package_review_round":2,"current_publication_package_review_status":"Initial R1 scientific pass qualified by accidental preseal-summary exposure; two presentation/evidence repairs in V2; new direct-input seal-first R2 complete-package clean.","current_publication_package_version":"publication_package_v2","current_publication_package_review_clearance":True,"current_Zenodo_published":True,"current_DOI":pub["doi"],"current_tracker_updated":True,"current_tracker_range":tracker["range"],"current_original_PR_merged":False,"current_publication_disposition_pending":True,"current_remaining_required_steps":"Actual scoped original-head merge, fresh provider/scope/native acceptance, factual completion metadata and actual acceptance.","current_publication_gate":"audits/pr170_30003480/ROOT_PUBLICATION_GATE.json","current_historical_novelty_or_exclusive_priority_certified":False,"current_mutual_independence_certified":False,"next_numeric_intake_cursor":171,"advance_to_next_PR_authorized_now":False,"persistent_goal_complete":False,"actual_goal_runtime_status_last_read":"blocked; direct human-authorized work continues","program_snapshot_semantics":"Actual publication/tracker accepted; original-head merge pending. Completed33/dated99,19 actual publications. Completion awaits actual disposition.","program_snapshot_authority_condition":"MERGE_AND_NATIVE_ACCEPTANCE.json must authenticate actual MAIN/tree/parents, full selected scope and provider merged state.","active_checkpoint_commit":None,"active_checkpoint_acceptance_receipt":"audits/pr170_30003480/MERGE_AND_NATIVE_ACCEPTANCE.json","completion_metadata_checkpoint_pending_at_snapshot":True,"next_step":"Complete actual PR170 original-head merge/readbacks and factual completion metadata; no171 intake."})
 save(out/"CURRENT_PROGRESS.json",j);overlay[prefix+"CURRENT_PROGRESS.json"]=out/"CURRENT_PROGRESS.json"
 note="\n\n"+now+" — PR170 published/tracked, original-head merge pending. Full original-domain no-one-polynomial theorem and exact positive n4 witness verified; known ingredients and exact stronger Oct2 overlap credited; Sep30/Oct2 contemporaneous separate disclosures, no exclusive priority or mutual-independence certificate. Initial qualified package assessment preserved, V2 evidence/presentation repairs and new direct-input seal-first final review clean. Exact publication "+pub["doi_url"]+", one tracker "+tracker["range"]+" accepted. Case90%, completed33/dated99,19 actual publications; goal unfinished. Only selected native/target QUEUE/audit/programme paths; other actual MAIN paths preserved.\n"
 for name in ["CURRENT_PROGRESS.md","RESEARCH_LOG.md"]:
  (out/name).write_bytes(body_at(prefix+name,expected)+note.encode());overlay[prefix+name]=out/name
 require(set(overlay)==set(plan["selected_files"])|set(plan["programme_metadata_paths"])|{qpath},"Concrete granted overlay differs")
 originals={e["repo_path"]:e for e in json.loads((A/"ORIGINAL_FILE_MANIFEST.json").read_text())["files"]};deletions=[]
 for n in plan["conditional_original_native_deletions"]:
  actual=lookup(parent["tree"]["sha"],n)
  if actual is not None:
   require(actual==("100644","blob",originals[n]["Git_blob"]),"Changed original obsolete native body "+n);deletions.append(n)
 pins={n:pin(p) for n,p in sorted(overlay.items())};entries=[{"path":n,"mode":"100644","type":"blob","sha":None} for n in deletions]
 for n,p in sorted(overlay.items()):
  b=p.read_bytes();e={"path":n,"mode":"100644","type":"blob"}
  try:e["content"]=b.decode("utf8")
  except UnicodeDecodeError:
   blob=api("git/blobs","POST",{"content":base64.b64encode(b).decode(),"encoding":"base64"});require(blob["sha"]==pins[n]["git_blob"],"Binary identity differs");e["sha"]=blob["sha"]
  entries.append(e)
 tree=api("git/trees","POST",{"base_tree":parent["tree"]["sha"],"tree":entries})
 changed={n for n,v in pins.items() if lookup(parent["tree"]["sha"],n)!=("100644","blob",v["git_blob"])}|set(deletions)
 require(changed_leaves(parent["tree"]["sha"],tree["sha"])==changed,"Full actual semantic diff exceeds selection")
 for n,v in pins.items():require(lookup(tree["sha"],n)==("100644","blob",v["git_blob"]),"Selected actual tree body differs "+n)
 commit=api("git/commits","POST",{"message":"Merge PR170: verified Gram-locus obstruction and qualified publication\n\nOriginal closed-domain single-polynomial problem resolved negatively. Established ingredients, exact stronger Oct2 overlap and documented Sep30/Oct2 disclosures credited without exclusive priority or mutual-independence certificate. Initial qualified review repaired; fresh seal-first full-package review clean. Publication "+pub["doi_url"]+", one tracker "+tracker["range"]+". Preserve17historical originals and every other actual MAIN path.","tree":tree["sha"],"parents":[expected,ORIGINAL]})
 actual=api("git/commits/"+commit["sha"]);require(actual["tree"]["sha"]==tree["sha"] and [x["sha"] for x in actual["parents"]]==[expected,ORIGINAL],"Actual merge tree/parents differ")
 check_grant(expected);require(api("git/ref/heads/main")["object"]["sha"]==expected,"MAIN moved; no stale update")
 result={"UTC":datetime.datetime.now(datetime.UTC).isoformat(),"status":"SCOPED_TWO_PARENT_MERGE_PREPARED_MAIN_NOT_UPDATED","expected_main":expected,"parent_tree":parent["tree"]["sha"],"tree":tree["sha"],"commit":commit["sha"],"original_PR_head":ORIGINAL,"selected_files":pins,"actual_changed_paths":sorted(changed),"conditional_native_deletions_applied":deletions,"QUEUE_rows_changed":1,"native_paths":sum(n.startswith("unsolved_math_prioritization/attempts/30003480/") for n in pins),"DOI":pub["doi"],"tracker_range":tracker["range"],"all_other_actual_base_tree_paths_preserved":True,"local_Git_index_ref_checkout_mutated":False}
 save(A/"SCOPED_MERGE_PREPARATION.json",result)
 print(json.dumps({k:result[k] for k in ["status","expected_main","tree","commit","native_paths","DOI","tracker_range"]}));print("Selected",len(pins),"Changed",len(changed))
if __name__=="__main__":
 require(len(sys.argv)==2 and re.fullmatch("[0-9a-f]{40}",sys.argv[1]),"Pass actual freshly granted MAIN");main(sys.argv[1])


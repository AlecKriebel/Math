"""Status-only intake after actual PR193 completion. No mathematics or remote writes."""
from pathlib import Path
import datetime,hashlib,importlib.util,json,re,sys
D=Path(__file__).resolve().parent;P=D.parent;A=P/"audits/pr193_30004563"
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def main(first,last):
 s=importlib.util.spec_from_file_location("status_only193",P/"audits/pr190_5000007/prepare_final_scoped_merge.py");h=importlib.util.module_from_spec(s);s.loader.exec_module(h);h.m.TREE_CACHE_PATH=D/"IMMUTABLE_TREE_CACHE.json"
 rb=(A/"actual_completion_reconciliation_preparation_01/generation_receipt01/CHECKPOINT_ACCEPTANCE.json").read_bytes();r=json.loads(rb)
 h.require(len(rb)==1312 and hashlib.sha256(rb).hexdigest()=="fb3d320ba717bbc2c6d29e703ce457a83792bfc6445b060105da0ecd92cd2c43","Previous own receipt changed")
 h.require(r["accepted"] is True and r["status"]=="ACTUAL_PR193_FINAL_RECEIPT_NATIVE_METADATA_RECONCILIATION_CHECKPOINT_ACCEPTED" and r["current_native_completion_flags_and_PR_metadata_actual"] is True and r["every_selected_identity_checked_at_actual_observed_MAIN"] is True and r["next_status_only_intake_authorized"] is True and (r["fully_completed_count"],r["published_count"],r["last_completed_PR"])==(41,25,193),"Previous actual completion missing")
 tip=h.api("git/ref/heads/main")["object"]["sha"];h.require(h.api("compare/"+r["checkpoint_commit"]+"..."+tip)["status"] in ["identical","ahead"],"Previous own checkpoint absent")
 progress=json.loads(h.body_at("draft_pr_publication_program_20260930/CURRENT_PROGRESS.json",tip))
 h.require((progress["last_completed_PR"],progress["fully_completed_count"],progress["published_count"],progress["next_numeric_intake_cursor"])==(193,41,25,194) and progress["current_completed"] is True and progress["actual_factual_checkpoint_accepted"] is True and progress["advance_to_next_PR_authorized_now"] is True,"Fresh prior completion/cursor differs")
 for number in range(first,last+1):
  path=D/f"PR{number}_ORIGINAL_STATUS_INTAKE.json";h.require(not path.exists(),"Never overwrite original intake")
  pr=h.api(f"pulls/{number}");head=pr["head"]["sha"];match=re.search(r"(?<!\d)(\d{6,})(?!\d)",pr["title"]);h.require(match is not None,"Need explicit problem identity from metadata")
  pid=int(match.group(1));rows=[v for v in h.body_at("unsolved_math_prioritization/QUEUE.md",head).decode().splitlines() if f"| {pid} /" in v];h.require(len(rows)==1,"Original QUEUE row must be unique")
  cells=rows[0].split("|");h.require(len(cells)==14,"QUEUE schema differs");status=cells[8].strip();eligible=status=="claimed_solved"
  out={"UTC":stamp(),"PR":number,"title":pr["title"],"original_head":head,"state_at_intake":pr["state"],"draft_at_intake":pr["draft"],"merged_at_intake":pr["merged"],"problem_id":pid,"original_QUEUE_status":status,"original_effort":cells[9].strip(),"original_QUEUE_row":rows[0],"row_SHA256":hashlib.sha256(rows[0].encode()).hexdigest(),"decision":"ELIGIBLE_CLAIMED_SOLVED_UNREVIEWED" if eligible else "SKIP_UNTOUCHED_NON_CLAIMED_SOLVED","mathematical_review_performed":False,"priority_review_performed":False,"PR_or_QUEUE_or_native_attempt_mutations":0,"prior_PR193_factual_commit":r["prior_actual_factual_commit"],"prior_PR193_actual_own_checkpoint":r["checkpoint_commit"],"prior_actual_own_receipt_sha256":hashlib.sha256(rb).hexdigest(),"fresh_MAIN_observed":tip,"completed":41,"published":25}
  with path.open("x") as f:json.dump(out,f,indent=2);f.write("\n")
  path.chmod(0o444)
  with (D/"RESEARCH_LOG.md").open("a") as f:f.write("\n"+out["UTC"]+f" — PR{number}/{pid}, original head{head}, status{status}: "+out["decision"]+". Status classification100%; mathematical/priority/publication review0%. No PR/QUEUE/native mutation;41completed/25published, broader goal active.\n")
  print(json.dumps({k:out[k] for k in ["PR","title","original_head","state_at_intake","draft_at_intake","merged_at_intake","problem_id","original_QUEUE_status","original_effort","decision"]}),flush=True)
  if eligible:break
if __name__=="__main__":
 if not sys.dont_write_bytecode:raise RuntimeError("Use -B")
 main(int(sys.argv[1]),int(sys.argv[2]))

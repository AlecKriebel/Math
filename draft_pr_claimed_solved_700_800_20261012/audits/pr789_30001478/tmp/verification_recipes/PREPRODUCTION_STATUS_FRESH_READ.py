from pathlib import Path
import datetime,json,sys
R=Path("/Users/alec/Documents/Math");D=R/"draft_pr_claimed_solved_700_800_20261012";T=D/"audits/pr789_30001478/tmp";M=T/"root-receipts";sys.path.insert(0,str(D))
from graphql_scoped_commit import get_pr,Remote,head_oid
p=get_pr(789);assert p["state"]=="open"and p["draft"]and not p["merged"]and p["head"]["sha"]=="aa44dec3baf8c1cd179cf8b55f32be95c74ee81a"
head=Remote(p["head"]["sha"]);mainsha=head_oid();main=Remote(mainsha);qpath="unsolved_math_prioritization/QUEUE.md"
own=lambda raw:next(l for l in raw.splitlines()if l.startswith("| ")and" 30001478 / "in l)
row=own(head.read(qpath));baseline=own(main.read(qpath));assert row.split("|")[8].strip()=="claimed_solved"and row.split("|")[9].strip()=="1/5"
assert main.entry("unsolved_math_prioritization/attempts/30001478/acceptance.json")is None
r={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS_READONLY_CONCURRENT_ELIGIBILITY","PR":p,"main_head":mainsha,"PR_head_own_row":row,"main_own_row":baseline,"native_acceptance_absent":True,"publication_gate_still_absent":not(T/"FINAL_READINESS.json").exists(),"mutation_performed":False}
(M/"PREPRODUCTION_STATUS_FRESH_READ.json").write_text(json.dumps(r,indent=2)+"\n")
print(json.dumps({"result":r["result"],"PR":789,"original_draft_head_unchanged":True,"PR_queue_status":"claimed_solved","explicit_budget":"1/5","main_current_status":baseline.split("|")[8].strip(),"native_acceptance_absent":True,"production_mutation":False}))


from pathlib import Path
import sys,json,datetime
R=Path("/Users/alec/Documents/Math");D=R/"draft_pr_claimed_solved_700_800_20261012";sys.path.insert(0,str(D));from graphql_scoped_commit import gql,Remote,get_pr
p=gql('query($n:Int!){repository(owner:"AlecKriebel",name:"Math"){pullRequest(number:$n){number title url state isDraft merged headRefOid headRefName}}}',{'n':789})['repository']['pullRequest']
if p["state"]!="OPEN"or not p["isDraft"]or p["merged"]:print(json.dumps({"result":"SKIP_METADATA_NOT_OPEN_DRAFT","PR":p}));raise SystemExit
r=Remote(p["headRefOid"]);rows=[l for l in r.read("unsolved_math_prioritization/QUEUE.md").splitlines()if l.startswith("| ")and" 30001478 / "in l];assert len(rows)==1;status=rows[0].split("|")[8].strip()
if status!="claimed_solved":print(json.dumps({"result":"SKIP_NONCLAIMED","status":status,"PR":p,"row":rows[0]}));raise SystemExit
A=D/"audits/pr789_30001478";T=A/"tmp";I=T/"intake";I.mkdir(parents=True,exist_ok=True);assert not(I/"ELIGIBILITY_GATE.json").exists(),"Existing intake; reconcile rather than replace"
gate={"screened_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"ELIGIBLE","problem":"30001478","pr":789,"queue_status":status,"head_queue_row":rows[0],"original_explicit_budget":rows[0].split("|")[9].strip(),"pr_metadata":p,"skip_rule":"Only exact claimed_solved immutable PR-head statuses are processed","new_substantive_proof_turns":0}
(I/"ELIGIBILITY_GATE.json").write_text(json.dumps(gate,indent=2)+"\n")
cat=json.loads(r.read("unsolved_math_prioritization/catalog.json"));own=[x for x in cat if x["id"]=="30001478"];assert len(own)==1
(I/"CATALOG_ENTRY.json").write_text(json.dumps(own[0],indent=2)+"\n")
for s in[A/"RESEARCH_LOG.md",I/"RESEARCH_LOG.md"]:
 assert not s.exists();s.write_text("# PR789 /30001478 independent audit\n\n"+gate["screened_utc"]+" — Fresh immutable PR-head gate ELIGIBLE exactly claimed_solved; original budget"+gate["original_explicit_budget"]+",0newproofsearchturns. No mathematical conclusion assumed; target/source intake next. Case5%; shard83%.\n")
print(json.dumps({"gate":gate,"selected_catalog":own[0]},indent=2))

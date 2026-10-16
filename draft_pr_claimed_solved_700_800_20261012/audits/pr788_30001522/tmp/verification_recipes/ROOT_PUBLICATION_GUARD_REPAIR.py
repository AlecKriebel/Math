from pathlib import Path
import hashlib,json,datetime,sys
D=Path("draft_pr_claimed_solved_700_800_20261012").resolve();T=D/"audits/pr788_30001522/tmp";P=T/"preprint";U=T/"publication";M=T/"root-receipts";sys.path.insert(0,str(D))
from graphql_scoped_commit import Remote,head_oid,gql
p=T/"publication_driver.py";old=p.read_text();oldsha=hashlib.sha256(p.read_bytes()).hexdigest()
assert not(U/"CREATION_INTENT.json").exists()and not(U/"STAGE_RECEIPT.json").exists()
parents=gql('query($o:GitObjectID!){repository(owner:"AlecKriebel",name:"Math"){object(oid:$o){...on Commit{parents(first:2){nodes{oid}}}}}}',{'o':'3412d5a074c3f3a03f75735a9ccf1755e172204a'})['repository']['object']['parents']['nodes'];assert [x['oid']for x in parents]==['f36cb1e34696d460b9cfb5b03425998de48c4669']
def row(r):
 x=[l for l in r.read("unsolved_math_prioritization/QUEUE.md").splitlines()if l.startswith("| ")and" 30001522 / "in l];assert len(x)==1;return x[0]
baseline=row(Remote(parents[0]['oid']));candidate=row(Remote('3412d5a074c3f3a03f75735a9ccf1755e172204a'))
assert baseline.split('|')[8].strip()=='queued'and baseline.split('|')[9].strip()=='0/5'
assert candidate.split('|')[8].strip()=='claimed_solved'and candidate.split('|')[9].strip()=='2/5'
needle='    need(len(rows2)==1 and rows2[0].split("|")[8].strip()in("unsolved","claimed_solved"),\\n         "Main has a competing disposition; reconcile rather than overwrite")'
replacement='    baseline_row='+repr(baseline)+'\\n    need(len(rows2)==1 and rows2[0]in(baseline_row,rows[0]),\\n         "Main differs from both the exact original-parent baseline and exact eligible candidate; reconcile rather than overwrite")\\n    selected=[x for x in json.loads(main.read("unsolved_math_prioritization/catalog.json"))if x["id"]=="30001522"]\\n    need(len(selected)==1 and selected[0]["statement_hash"]==g["statement_hash"]\\n         and selected[0]["review_hash"]==g["review_hash"],"Main source identity changed")'
needle=needle.replace('\\n','\n');replacement=replacement.replace('\\n','\n');assert old.count(needle)==1
new=old.replace(needle,replacement).replace('main can still carry its unmerged unsolved baseline.','main must carry the exact original-parent queued baseline or exact candidate row.')
compile(new,str(p),'exec');p.write_text(new)
rec={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','issue':'Administrative guard excluded verified original queued baseline; no publication mutation was attempted.','original_head':'3412d5a074c3f3a03f75735a9ccf1755e172204a','original_parent':parents[0]['oid'],'exact_parent_row':baseline,'exact_candidate_row':candidate,'before_driver_sha256':oldsha,'after_driver_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'frozen_six_unchanged':True,'allowed_main_rows':'EXACT original-parent queued0/5 row OR EXACT reviewed candidate claimed_solved2/5 row; source statement/review hashes unchanged and no native acceptance','creation_intent_absent':True,'percentage_case':90,'percentage_shard':75}
(M/"PUBLICATION_GUARD_BASELINE_REPAIR.json").write_text(json.dumps(rec,indent=2)+'\n')
print(json.dumps(rec))

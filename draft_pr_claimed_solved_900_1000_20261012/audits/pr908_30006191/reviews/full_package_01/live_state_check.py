#!/usr/bin/env python3
"""Read-only end-state gate; keep raw API bodies private."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess

HERE=Path(__file__).resolve().parent
HEAD='a35667b1bb0bafed69916709997a4684223ecc93'
BODY='3b6678ba45571e86e44360e45cffd2e00d75b8f05c5d3a8a407c43c5680f708d'
def command(args):return subprocess.run(args,capture_output=True,text=True,check=True).stdout
def require(ok,why):
    if not ok:raise RuntimeError(why)
def main():
    pr=json.loads(command(['gh','pr','view','908','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,headRefName,baseRefName,title,body']))
    private=HERE/'private_sources';private.mkdir(exist_ok=True)
    (private/'pr_end.json').write_text(json.dumps(pr))
    require(pr['state']=='OPEN' and pr['isDraft'] is True and pr['headRefOid']==HEAD and pr['baseRefName']=='main','PR eligibility changed')
    bodyhash=hashlib.sha256(pr['body'].encode()).hexdigest();require(bodyhash==BODY,'live body changed before first review seal')
    sha=command(['git','ls-remote','origin','refs/heads/main']).split()[0]
    raw=command(['gh','api','repos/AlecKriebel/Math/contents/unsolved_math_prioritization/catalog.json?ref='+sha,'--header','Accept: application/vnd.github.raw+json'])
    (private/'catalog_end.json').write_text(raw)
    targets=[x for x in json.loads(raw) if str(x['id'])=='30006191'];require(len(targets)==1,'ambiguous target')
    t=targets[0];pre=json.loads((HERE.parents[1]/'TARGET_IDENTITY_PREFLIGHT.json').read_text())
    require(all(t[k]==pre[k] for k in ['review_hash','statement_hash','holds','present']),'source target changed')
    q=command(['git','show',HEAD+':unsolved_math_prioritization/QUEUE.md'])
    rows=[s for s in q.splitlines() if s.startswith('|') and len(s.split('|'))>8 and s.split('|')[2].strip().split(' / ')[0]=='30006191']
    require(len(rows)==1 and rows[0].split('|')[8].strip()=='claimed_solved' and rows[0].split('|')[9].strip()=='1/5','immutable queue gate changed')
    result={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','pr':{k:v for k,v in pr.items() if k!='body'},'pr_body_sha256':bodyhash,'body_unchanged_during_review':True,'main_sha':sha,'target':{k:t[k] for k in ['id','review_hash','statement_hash','holds','present']},'head_queue_status':'claimed_solved','candidate_turns':'1/5','raw_api_bodies_private':True}
    (HERE/'LIVE_END_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()

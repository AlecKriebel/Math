"""Install the concrete reviewed PR body and readiness without merging."""
from pathlib import Path
import json,subprocess,datetime,hashlib
A=Path(__file__).resolve().parent;P=A.parents[1]
m=json.loads((A/'repaired_snapshot_manifest.json').read_bytes());body=(A/'accepted_pr_body.txt').read_text()
def run(args,tag):
    r=subprocess.run(args,cwd=P.parent,capture_output=True);(A/(tag+'.stdout')).write_bytes(r.stdout);(A/(tag+'.stderr')).write_bytes(r.stderr)
    assert r.returncode==0,(tag,r.stderr);return r.stdout
before=json.loads(run(['gh','pr','view','371','--json','state,isDraft,headRefOid'],'body_before'))
assert before['state']=='OPEN' and before['headRefOid']==m['head']
run(['gh','pr','edit','371','--body-file',str(A/'accepted_pr_body.txt')],'body_edit')
if before['isDraft']:run(['gh','pr','ready','371'],'ready')
after=json.loads(run(['gh','api','repos/AlecKriebel/Math/pulls/371'],'ready_live_api'))
assert after['state']=='open' and not after['draft'] and after['head']['sha']==m['head'] and after['base']['sha']==m['base'] and after['body']==body
c=json.loads((A/'acceptance_criteria.json').read_bytes());c.update(reviewed_head=m['head'],reviewed_current_main=m['base'],workflow_completion_percent=90)
(A/'acceptance_criteria.json').write_text(json.dumps(c,indent=2)+'\n')
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':m['head'],'base':m['base'],'body_sha256':hashlib.sha256(body.encode()).hexdigest(),'open_ready_body_exact':True,'mergeable':after['mergeable'],'mergeable_state':after['mergeable_state'],'test_merge':after['merge_commit_sha']},indent=2))

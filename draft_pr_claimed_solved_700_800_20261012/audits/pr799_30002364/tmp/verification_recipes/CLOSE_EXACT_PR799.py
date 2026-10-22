from pathlib import Path
import datetime,hashlib,json,sys
R=Path('/Users/alec/Documents/Math');D=R/'draft_pr_claimed_solved_700_800_20261012'
A=D/'audits/pr799_30002364';T=A/'tmp';M=T/'root-receipts'
sys.path.insert(0,str(D))
from graphql_scoped_commit import Remote
from remote_scoped_commit import api
def need(ok,msg):
 if not ok: raise RuntimeError(msg)
H='cc45ec9dc93515593c3b2a228def86c3a562e13f'
gate=json.loads((M/'PRIORITY_GATE.json').read_text())
need(gate['reviewed_head']==H and gate['remaining_central_priority_gaps']==[],'unresolved gate')
need(gate['fresh_priority_adversaries']==2 and gate['recommended_PR_disposition']=='close_without_merge_with_explanation','scope')
replay=json.loads((M/'ROOT_PRIORITY_REPLAYS.json').read_text());need(replay['result']=='PASS','replay')
need(not (M/'CLOSE_ACTION_INTENT.json').exists(),'Reconcile existing intent; never repeat blindly')
pr=api('pulls/799');need(pr['state']=='open' and pr['draft'] and not pr['merged'] and pr['head']['sha']==H,'fresh exact eligible draft')
q=Remote(H).read('unsolved_math_prioritization/QUEUE.md')
rows=[l for l in q.splitlines() if l.startswith('| ') and ' 30002364 / ' in l]
need(len(rows)==1 and rows[0].split('|')[8].strip()=='claimed_solved' and rows[0].split('|')[9].strip()=='5/5','fresh claimed-only gate')
comment=(M/'CLOSE_COMMENT.md').read_text();digest=hashlib.sha256(comment.encode()).hexdigest()
intent={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pr':799,'reviewed_head':H,'fresh_head_row':rows[0],
 'comment_sha256':digest,'requested_actions':['one explanatory issue comment','close PR without merge'],
 'authorized_by_user':True,'no_new_deposit_or_tracker_row':True}
(M/'CLOSE_ACTION_INTENT.json').write_text(json.dumps(intent,indent=2)+'\n')
existing=[]
for page in range(1,101):
 batch=api('issues/799/comments?per_page=100&page='+str(page))
 existing.extend(c for c in batch if c['body']==comment)
 if len(batch)<100:break
else:raise RuntimeError('Comments inventory incomplete')
need(len(existing)<=1,'duplicate exact comments require reconciliation')
response=existing[0] if existing else api('issues/799/comments','POST',{'body':comment})
need(response['body']==comment,'comment readback')
cr={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'id':response['id'],'url':response['html_url'],
 'body_sha256':digest,'created_new':not existing,'result':'PASS'}
(M/'CLOSE_COMMENT_RECEIPT.json').write_text(json.dumps(cr,indent=2)+'\n');print(json.dumps(cr),flush=True)
fresh=api('pulls/799');need(fresh['state']=='open' and fresh['head']['sha']==H and not fresh['merged'],'head changed after comment')
closed=api('pulls/799','PATCH',{'state':'closed'})
need(closed['state']=='closed' and not closed['merged'] and closed['head']['sha']==H,'closure response')
verify=api('pulls/799');checkcomment=api('issues/comments/'+str(cr['id']))
need(verify['state']=='closed' and not verify['merged'] and verify['head']['sha']==H,'closure readback')
need(checkcomment['body']==comment,'immutable comment readback')
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','pr':799,'problem':'30002364',
 'closed_without_merge':True,'reviewed_head':H,'closed_at':verify['closed_at'],'draft_preserved':verify['draft'],
 'comment':cr,'new_Zenodo_deposit':False,'tracker_row_added':False,'original_candidate_edited':False}
(M/'CLOSE_VERIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt),flush=True)

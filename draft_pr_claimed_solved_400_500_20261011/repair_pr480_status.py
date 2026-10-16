#!/usr/bin/env python3
"""One-time reviewed status repair; immutable exact-head and single-row guards."""
import base64,datetime,hashlib,json,re,subprocess,urllib.parse
from pathlib import Path
R=Path(__file__).resolve().parent;P=R/'audits/pr480_30003656'
REPO='AlecKriebel/Math';EXPECTED='cd9025795f40bd9ebc2b32de50917d73ca0f2bfa'
PATH='unsolved_math_prioritization/QUEUE.md';BRANCH='research/rank506-wraith-redundancy-30003656-20261003'

def gh(*a):return subprocess.check_output(['gh',*a])
def api(endpoint,payload=None,method='POST'):
 c=['gh','api','repos/'+REPO+'/'+endpoint]
 if payload is not None:c+=['--method',method,'--input','-']
 q=subprocess.run(c,input=None if payload is None else json.dumps(payload),text=True,capture_output=True)
 if q.returncode:raise RuntimeError(q.stderr)
 return json.loads(q.stdout)

def main():
 pr=json.loads(gh('pr','view','480','--repo',REPO,'--json','number,state,isDraft,headRefOid,headRefName'))
 if pr['state']!='OPEN' or not pr['isDraft'] or pr['headRefOid']!=EXPECTED or pr['headRefName']!=BRANCH:raise RuntimeError('PR/head changed; stop and re-evaluate scope')
 before=gh('api',f'repos/{REPO}/contents/{PATH}?ref={EXPECTED}','-H','Accept: application/vnd.github.raw+json')
 stored=P.joinpath('queue_before_status_repair.md').read_bytes()
 if before!=stored:raise RuntimeError('Frozen queue mismatch')
 lines=before.decode().splitlines(keepends=True)
 idx=[i for i,l in enumerate(lines) if '| 30003656 / OWR-15958-003 |' in l]
 if len(idx)!=1:raise RuntimeError('Ambiguous selected row')
 cells=lines[idx[0]].split('|')
 if cells[8].strip()!='claimed_solved':raise RuntimeError('Exact status scope gate failed')
 publication=json.loads(R.joinpath('checkpoints/checkpoint03_push.json').read_text())
 link=f"https://github.com/{REPO}/blob/{publication['commit_sha']}/draft_pr_claimed_solved_400_500_20261011/audits/pr480_30003656/DISPOSITION.md"
 finding='2026-10-11: priority correction: the literal algebraic question has a credited routine prior-method negative resolution (published generic-model calculations plus geometric classical conservativity). Exact one-constant alpha is valid and a routine BBC Theorem 5.11 specialization. Earlier explicit printing of alpha or prior recognition of the algebraic resolution was not established; no new-discovery/first-priority claim accepted. [Independent disposition audit]('+link+'). Corrected to already_solved, then skipped under exact-status scope; no publication or merge.'
 cells[8]=' already_solved ';cells[11]=' '+finding+' '
 lines[idx[0]]='|'.join(cells)
 after=''.join(lines).encode()
 changes=[i for i,(x,y) in enumerate(zip(before.decode().splitlines(),after.decode().splitlines())) if x!=y]
 if changes!=idx or len(before.decode().splitlines())!=len(after.decode().splitlines()):raise RuntimeError('Non-target queue change')
 P.joinpath('queue_after_status_repair.md').write_bytes(after)
 blob=api('git/blobs',{'content':base64.b64encode(after).decode(),'encoding':'base64'})['sha']
 parent=api('git/commits/'+EXPECTED)
 tree=api('git/trees',{'base_tree':parent['tree']['sha'],'tree':[{'path':PATH,'mode':'100644','type':'blob','sha':blob}]})['sha']
 commit=api('git/commits',{'message':'Correct Wraith algebraic target priority classification after independent audit','tree':tree,'parents':[EXPECTED]})['sha']
 ref='git/refs/heads/'+urllib.parse.quote(BRANCH,safe='')
 api(ref,{'sha':commit,'force':False},method='PATCH')
 # Status readback only. This establishes exclusion; no further PR processing.
 final=gh('api',f'repos/{REPO}/contents/{PATH}?ref={commit}','-H','Accept: application/vnd.github.raw+json')
 if final!=after:raise RuntimeError('Status repair readback mismatch')
 receipt={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pr':480,'problem_id':'30003656','old_status':'claimed_solved','new_status':'already_solved','old_head':EXPECTED,'repair_commit':commit,'branch':BRANCH,'files_changed':[PATH],'old_queue_sha256':hashlib.sha256(before).hexdigest(),'new_queue_sha256':hashlib.sha256(after).hexdigest(),'readback':'exact bytes matched','subsequent_scope':'skip; no paper/Zenodo/tracker/merge/close/comment','basis':'published prior-method implication; earlier explicit recognition/printing not established','shared_checkout_index':'untouched main'}
 P.joinpath('STATUS_REPAIR_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()

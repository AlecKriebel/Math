#!/usr/bin/env python3
"""Narrow exact-head priority correction; default read-only, then immediate skip."""
import argparse,base64,datetime,hashlib,json,subprocess,urllib.parse
from pathlib import Path
PROGRAM=Path(__file__).resolve().parent
AUDIT=PROGRAM/'audits/pr466_30000999'
REPO='AlecKriebel/Math'
ORIGINAL='77a27c5da92b8f42f79b2f27e40f5c9a6403ddb9'
QUEUE='unsolved_math_prioritization/QUEUE.md'
def require(c,m):
 if not c:raise RuntimeError(m)
def api(s,payload=None,method='POST'):
 cmd=['gh','api','repos/'+REPO+'/'+s]
 if payload is not None:cmd+=['--method',method,'--input','-']
 p=subprocess.run(cmd,input=None if payload is None else json.dumps(payload),capture_output=True,text=True)
 require(p.returncode==0,p.stderr.strip())
 return json.loads(p.stdout)
def dump(n,v):(AUDIT/n).write_text(json.dumps(v,indent=2)+'\n')
def ensure_eligible(branch):
 pr=api('pulls/466')
 require(pr['state']=='open' and pr['draft'] is True and pr['head']['sha']==ORIGINAL and pr['head']['ref']==branch and pr['head']['repo']['full_name']==REPO and pr['base']['ref']=='main' and pr['base']['repo']['full_name']==REPO,'Original full eligible draft snapshot changed')
 require(api('git/ref/heads/'+urllib.parse.quote(branch,safe=''))['object']['sha']==ORIGINAL,'Original branch ref changed')
 return pr
def main():
 a=argparse.ArgumentParser();a.add_argument('--apply',action='store_true');args=a.parse_args()
 gate=json.loads((AUDIT/'PRIORITY_DISPOSITION_GATE.json').read_text())
 require(gate['verdict']=='ACCEPTED_PRIORITY_CLASSIFICATION' and gate['problem_id']=='30000999' and gate['pr']==466 and gate['recommended_status']=='already_solved' and gate['original_head']==ORIGINAL,'Final exact priority gate absent')
 require(len(gate['reviews'])>=3,'Independent priority and fresh disposition reviews absent')
 require(len({x['path'] for x in gate['reviews']})==len(gate['reviews']) and len({x['family'] for x in gate['reviews']})==len(gate['reviews']) and {'priority_original','priority_even','disposition_adversary'}.issubset({x['family'] for x in gate['reviews']}),'Distinct independent priority/disposition review identities absent')
 for x in gate['reviews']:
  f=(AUDIT/x['path']).resolve()
  require(f.is_relative_to(AUDIT) and hashlib.sha256(f.read_bytes()).hexdigest()==x['sha256'],'Review byte drift')
  require(type(x.get('blocking_issue_count')) is int and x['blocking_issue_count']==0 and type(x.get('unresolved_disposition_issue_count')) is int and x['unresolved_disposition_issue_count']==0,'Unresolved disposition issue')
 original_meta=json.loads((AUDIT/'pr_metadata.json').read_text());branch=original_meta['headRefName']
 pr=ensure_eligible(branch)
 original_commit=api('git/commits/'+ORIGINAL);tree=original_commit['tree']['sha'];cache={}
 for part in QUEUE.split('/'):
  if tree not in cache:cache[tree]={e['path']:e for e in api('git/trees/'+tree)['tree']}
  e=cache[tree][part];tree=e['sha']
 require(e['type']=='blob','QUEUE not regular Git blob')
 before=base64.b64decode(api('git/blobs/'+tree)['content']);source=json.loads((AUDIT/'SOURCE_RECEIPT.json').read_text());require(hashlib.sha256(before).hexdigest()==source['queue_sha256'],'Frozen original QUEUE changed')
 lines=before.decode().splitlines(keepends=True);h=next(x for x in lines if x.startswith('|') and 'ID / code' in x and 'Status' in x);columns=[x.strip() for x in h.split('|')[1:-1]]
 indices=[i for i,x in enumerate(lines) if x.startswith('|') and x.split('|')[2].strip().startswith('30000999 /')];require(len(indices)==1,'Selected row not unique');i=indices[0];cells=lines[i].rstrip('\r\n').split('|')[1:-1];require(len(cells)==len(columns),'QUEUE schema mismatch');require(cells[columns.index('Status')].strip()=='claimed_solved','Excluded status: stop, do not process')
 old_row=lines[i].rstrip('\r\n');cells[columns.index('Status')]=' already_solved '
 link=gate['published_disposition_url'];require(link.startswith('https://github.com/'+REPO+'/blob/'),'Published audit checkpoint link absent')
 finding=('2026-10-12: Priority correction: literal all-probability inverse Wasserstein question has a routine negative answer from classical antipodal noninjectivity (Funk 1913; normalized operator Quellmalz 2020). R delta_u = R delta_-u, input W_p = pi, output distance 0. Earlier explicit printing of this exact Wasserstein answer was not established. Separate even-density instability is mathematically verified but its all-p priority remains unverified and does not change the original target classification. Report volume 2008, published 2009. [Independent disposition audit]('+link+'). Corrected to already_solved, then immediately skipped; no paper, DOI or merge.')
 cells[columns.index('Findings')]=' '+finding+' ';ending='\r\n' if lines[i].endswith('\r\n') else '\n' if lines[i].endswith('\n') else '';lines[i]='|'+'|'.join(cells)+'|'+ending;after=''.join(lines).encode()
 require(len(before.decode().splitlines())==len(after.decode().splitlines()) and [j for j,(a,b) in enumerate(zip(before.decode().splitlines(),after.decode().splitlines())) if a!=b]==indices,'Non-target QUEUE alteration')
 summary={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pr':466,'problem_id':'30000999','old_status':'claimed_solved','new_status':'already_solved','old_head':ORIGINAL,'branch':branch,'files_changed':[QUEUE],'old_queue_sha256':hashlib.sha256(before).hexdigest(),'new_queue_sha256':hashlib.sha256(after).hexdigest(),'selected_old_row':old_row,'selected_new_row':lines[i].rstrip('\r\n'),'state':'read_only_preflight','shared_checkout_index':'untouched main','subsequent_scope':'immediate skip: no paper/Zenodo/tracker/merge/close/comment'}
 dump('STATUS_REPAIR_PREFLIGHT.json',summary)
 if not args.apply:print(json.dumps(summary,indent=2));return
 require(not (AUDIT/'STATUS_REPAIR_OPERATION.json').exists(),'Prior operation exists: inspect recorded commit instead of repeating mutation')
 blob=api('git/blobs',{'content':base64.b64encode(after).decode(),'encoding':'base64'})['sha'];new_tree=api('git/trees',{'base_tree':original_commit['tree']['sha'],'tree':[{'path':QUEUE,'mode':'100644','type':'blob','sha':blob}]})['sha']
 ensure_eligible(branch)
 commit=api('git/commits',{'message':'Correct literal Radon inverse question priority classification after independent audit','tree':new_tree,'parents':[ORIGINAL]})['sha'];diff=api('compare/'+ORIGINAL+'...'+commit);require([x['filename'] for x in diff['files']]==[QUEUE],'Commit changes other paths')
 summary.update(state='commit_created_before_ref_update',repair_commit=commit,queue_git_blob_sha=blob);dump('STATUS_REPAIR_OPERATION.json',summary)
 ref='git/refs/heads/'+urllib.parse.quote(branch,safe='')
 # This narrows the final race; Git-data ref PATCH is not expected-old-SHA CAS.
 ensure_eligible(branch)
 try:api(ref,{'sha':commit,'force':False},method='PATCH')
 except RuntimeError:require(api('git/ref/heads/'+urllib.parse.quote(branch,safe=''))['object']['sha']==commit,'Branch update uncertain; no retry')
 require(api('git/ref/heads/'+urllib.parse.quote(branch,safe=''))['object']['sha']==commit,'Selected branch readback differs')
 final=base64.b64decode(api('git/blobs/'+blob)['content']);require(final==after,'Status blob exact-byte readback differs')
 summary.update(state='status_repair_verified_immediately_excluded',verified_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),readback='Exact selected branch ref and immutable QUEUE blob bytes matched',basis='Routine deduction of original target from documented classical obstruction; exact earlier Wasserstein answer/adjunct priority not certified',concurrency_scope='Full eligible PR and exact original ref checked immediately before nonforced update. Git-data ref PATCH is not atomic expected-old-commit CAS.')
 dump('STATUS_REPAIR_RECEIPT.json',summary);print(json.dumps({'pr':466,'new_status':'already_solved','repair_commit':commit,'state':summary['state'],'subsequent_scope':summary['subsequent_scope']},indent=2))
if __name__=='__main__':main()

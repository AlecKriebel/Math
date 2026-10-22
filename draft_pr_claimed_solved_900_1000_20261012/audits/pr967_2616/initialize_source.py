#!/usr/bin/env python3
"""Read-only source initialization for the already-selected exact claimed PR.

Never ranks, syncs, changes source cache, records a proof turn, or writes outside
this program's selected effort. Excluded statuses return before reading math.
The research charter and actual claim must still be written after full reading.
"""
import argparse,hashlib,json,sqlite3,stat,subprocess
from pathlib import Path
from datetime import datetime,timezone
P=Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012')
ROOT=P.parent
QUEUE='unsolved_math_prioritization/QUEUE.md'
def require(x,label):
 if not x:raise RuntimeError(label)
def cmd(a):return subprocess.run(a,cwd=ROOT,capture_output=True,text=True,check=True).stdout

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--pr',type=int,required=True);ap.add_argument('--problem-id',required=True);args=ap.parse_args()
 require(900<=args.pr<=1000 and args.problem_id.isdigit(),'Outside selected shard/numeric identity')
 state=json.loads((P/'CURRENT_STATE.json').read_text())
 require(state['active_pr']==args.pr and str(state['active_problem_id'])==args.problem_id,'Not the selected next gate')
 a=P/'audits'/f'pr{args.pr}_{args.problem_id}';gate=json.loads((a/'ELIGIBILITY_GATE.json').read_text())
 pr=json.loads(cmd(['gh','pr','view',str(args.pr),'--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,headRefName,baseRefName,url']))
 if pr['state']!='OPEN' or not pr['isDraft']:
  print(json.dumps({'pr':args.pr,'status':'SKIP_NOT_OPEN_DRAFT','math_source_read':False}));return
 cmd(['git','fetch','--no-write-fetch-head','origin',pr['headRefOid']])
 rows=[s for s in cmd(['git','show',pr['headRefOid']+':'+QUEUE]).splitlines() if '| '+args.problem_id+' /' in s]
 require(len(rows)==1,'Ambiguous target gate')
 row=rows[0];cells=row.split('|');status=cells[8].strip()
 if status!='claimed_solved':
  print(json.dumps({'pr':args.pr,'problem_id':args.problem_id,'status':status,'action':'SKIP_STATUS_ONLY','math_source_read':False}));return
 require(pr['headRefOid']==gate['headRefOid'] and pr['baseRefName']=='main','Immutable selected head/base changed; resnapshot gate before source reading')
 require(not (a/'TARGET_IDENTITY_PREFLIGHT.json').exists(),'Source initialization already recorded; inspect existing evidence')
 parent=cmd(['git','ls-remote','origin','refs/heads/main']).split()[0];cmd(['git','fetch','--no-write-fetch-head','origin',parent])
 catalog=json.loads(cmd(['git','show',parent+':unsolved_math_prioritization/catalog.json']))
 matches=[t for t in catalog if str(t['id'])==args.problem_id];require(len(matches)==1,'Ambiguous source ID')
 t=matches[0];require(t['present'] is True and t['holds']==[],'Source absent or readiness hold requires resolution')
 policy=json.loads(cmd(['git','show',parent+':unsolved_math_prioritization/policy.json']));require(policy['turn_limit']==5,'Five-turn source policy changed')
 dbpath=ROOT/'unsolved_math_prioritization/cache/catalog.sqlite';require(dbpath.is_file() and not dbpath.is_symlink(),'Source cache unavailable/nonregular')
 with sqlite3.connect(dbpath.as_uri()+'?mode=ro&immutable=1',uri=True) as db:
  raw=db.execute('SELECT payload,report FROM records WHERE key=?',(args.problem_id,)).fetchone()
 require(raw is not None,'Numeric source ID absent from cache')
 problem,prior=map(json.loads,raw)
 # Match the repository's exact serialization: default ASCII escaping/separators.
 review=hashlib.sha256(json.dumps([problem,prior],sort_keys=True).encode()).hexdigest()
 statement=hashlib.sha256((problem.get('statement') or '').encode()).hexdigest()
 require(review==t['review_hash'] and statement==t['statement_hash'],'Cached full statement/report do not match current main identity')
 snapshot=json.loads((a/'ORIGINAL_SNAPSHOT.json').read_text());require(snapshot['head']==pr['headRefOid'],'Wrong original snapshot')
 for name,pin in snapshot['files'].items():
  path=a/'original'/name;require(stat.S_ISREG(path.lstat().st_mode),'Nonregular original snapshot file')
  require(hashlib.sha256(path.read_bytes()).hexdigest()==pin,'Original snapshot drift')
 groups_raw=cmd(['git','show',parent+':unsolved_math_prioritization/review_v2/related_target_groups.json']);groups=json.loads(groups_raw)
 def contains(v):
  if type(v) in (str,int):return str(v)==args.problem_id
  if type(v) is list:return any(contains(x) for x in v)
  if type(v) is dict:return any(str(k)==args.problem_id or contains(x) for k,x in v.items())
  return False
 related={'membership_found':True,'manual_targeted_group_check_required':True,'file_sha256':hashlib.sha256(groups_raw.encode()).hexdigest()} if contains(groups) else {}
 now=datetime.now(timezone.utc).isoformat()
 private={'review_hash':review,'problem':problem,'prior_research':prior}
 (a/'source_record_private.txt').write_text(json.dumps(private,indent=2,ensure_ascii=False)+'\n')
 (a/'source_record_private.txt').chmod(0o600)
 public={'utc':now,'remote_main':parent,'id':args.problem_id,'problem_number':t['problem_number'],'title':t['title'],'review_hash':review,'statement_hash':statement,'source_review_hash_matches_raw':True,'present':True,'holds':[],'turn_limit':5,'original_candidate_turns':cells[9].strip(),'earlier_history':'Unavailable according to recovered queue note' if 'unavailable' in row.lower() else 'Not independently adjudicated by this initializer','verification_attempts_increment_proof_budget':False,'related_target_groups':related,'original_head':pr['headRefOid'],'original_files':len(snapshot['files']),'read_only_sqlite_source_access':True,'research_charter_and_independent_audits':'NOT_YET_COMPLETED'}
 (a/'TARGET_IDENTITY_PREFLIGHT.json').write_text(json.dumps(public,indent=2)+'\n')
 metadata=json.loads(cmd(['gh','pr','view',str(args.pr),'--repo','AlecKriebel/Math','--json','number,title,body,state,isDraft,headRefOid,url']))
 require(metadata['state']=='OPEN' and metadata['isDraft'] and metadata['headRefOid']==pr['headRefOid'],'Live head changed during initialization')
 (a/'PR_METADATA_SNAPSHOT.json').write_text(json.dumps(metadata,indent=2)+'\n');(a/'PR_DESCRIPTION_ANCHOR.md').write_text(metadata['body'])
 (a/'GATED_QUEUE_ROW.md').write_text(row+'\n')
 state.update(utc=now,phase=f'PR{args.pr}_source_identity_initialized_before_math_audits',active_original_head=pr['headRefOid'],original_candidate_turns=cells[9].strip(),active_pr_completion_estimate_percent=0)
 (P/'CURRENT_STATE.json').write_text(json.dumps(state,indent=2)+'\n')
 count=len(state['completed_prs']);denom=len(state['eligible_prs']);entry=f'\n{now} — PR{args.pr} initialization checkpoint0% workflow/shard{100*count/denom:.2f}% complete: exact immutable-head claimed_solved gate retained; complete cached statement/prior-report and currentmain source hashes match, present=true/holds empty, related membership checked. Original {len(snapshot["files"])} files unchanged, observed candidate label {cells[9].strip()} preserved without certifying complete author history. Full source/proof reading, exact charter and independent mathematical families still required before priority/publication. No proof turn or external mutation.\n'
 for log in [P/'RESEARCH_LOG.md',a/'RESEARCH_LOG.md']:
  with log.open('a') as f:f.write(entry)
 print(json.dumps(public,indent=2))
if __name__=='__main__':main()

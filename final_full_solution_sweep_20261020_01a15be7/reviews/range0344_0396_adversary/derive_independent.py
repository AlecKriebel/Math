"""Read immutable objects and live metadata; never reads root dispositions."""
from pathlib import Path
import subprocess,json,re,hashlib,datetime
ROOT=Path('/Users/alec/Documents/Math')
EFFORT=ROOT/'final_full_solution_sweep_20261020_01a15be7'
OWN=EFFORT/'reviews/range0344_0396_adversary'
PRIVATE=EFFORT/'private/pr0344_0396_review'
QUEUE='unsolved_math_prioritization/QUEUE.md'
def git(*args): return subprocess.check_output(['git',*args],cwd=ROOT)
def sha(x): return hashlib.sha256(x).hexdigest()
def row(line):
 c=[t.strip() for t in line.strip().strip('|').split('|')]
 if len(c)<9 or not c[0].isdigit(): return None
 ids=re.findall(r'(?<!\d)\d{4,}(?!\d)',c[1])
 if not ids:return None
 return dict(problem_id=ids[0],alias=c[1],status=c[7],turns=c[8])
prs=json.loads((PRIVATE/'pinned_inventory.json').read_text())
live={r['pr']:r['response']['structuredContent'] for r in json.loads((PRIVATE/'live_pr_info.json').read_text())['results']}
result=[]
for pr in prs:
 n=pr['number']; assert 344<=n<=396
 base=pr['baseRefOid']; head=pr['headRefOid']; mb=git('merge-base',base,head).decode().strip()
 paths=git('diff','--no-renames','--name-only',mb,head).decode().splitlines()
 ns=git('diff','--no-renames','--name-status',mb,head).decode().splitlines()
 ids=sorted(set(m.group(1) for p in paths for m in [re.search(r'(?:attempts|problems)/(\d{4,})(?:[/_]|$)',p)] if m))
 patch=git('diff','--no-ext-diff','--unified=0',mb,head,'--',QUEUE)
 (PRIVATE/f'pr{n:04d}_queue.patch').write_bytes(patch)
 added=[row(s[1:]) for s in patch.decode().splitlines() if s.startswith('+|')]
 added=[r for r in added if r and r['problem_id'] in ids]
 own_head=[]
 try:
  queue=git('show',f'{head}:{QUEUE}')
  own_head=[r for s in queue.decode().splitlines() for r in [row(s)] if r and r['problem_id'] in ids]
 except subprocess.CalledProcessError:queue=b''
 ownstatus=sorted(set(r['status'] for r in added))
 if ownstatus and all(s in ['unsolved','already_solved','partial','blocked','abandoned','not_solved','source_verification_hold'] for s in ownstatus): cls='explicit_nonclaim_queue'
 elif ownstatus and all(s not in ['claimed_solved','claimed_solved5','queued'] for s in ownstatus):cls='explicit_nonclaim_queue_other_status'
 elif ownstatus and any(s.startswith('claimed_solved') for s in ownstatus):cls='claimed_solved_requires_publication_or_audit'
 elif ownstatus==['queued']:cls='changed_own_queued_requires_context'
 else:cls='no_usable_changed_own_queue_requires_substantive_read'
 files=[]
 for s in ns:
  status,path=s.split('\t',1)
  b=None
  if status!='D':
   b=git('show',f'{head}:{path}')
   oid=git('rev-parse',f'{head}:{path}').decode().strip()
  else:oid=None
  files.append(dict(path=path,status=status,head_git_blob=oid,sha256=sha(b) if b is not None else None,bytes=len(b) if b is not None else None))
 out=dict(pr=n,derived_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),problem_ids=ids,input_base=base,head=head,actual_merge_base=mb,comparison_base_is_merge_base=base==mb,changed_path_count=len(paths),changed_paths=files,queue_patch_sha256=sha(patch),changed_corresponding_rows=added,head_corresponding_statuses=own_head,independent_preclassification=cls,live_head=live[n]['head_sha'],live_base=live[n]['base_sha'],live_state=live[n]['state'],live_merged=live[n]['merged'],live_head_matches_pin=live[n]['head_sha']==head,live_base_matches_pin=live[n]['base_sha']==base)
 result.append(out)
(OWN/'independent_classification_initial.json').write_text(json.dumps(dict(schema=1,root_dispositions_consulted=False,scope=[344,396],classifications=result),indent=2)+'\n')
print('\n'.join(f"PR{r['pr']} {','.join(r['problem_ids'])} paths={r['changed_path_count']} changed_status={','.join(x['status'] for x in r['changed_corresponding_rows']) or 'NONE'} head_status={','.join(x['status'] for x in r['head_corresponding_statuses']) or 'NONE'} => {r['independent_preclassification']}" for r in result))
print('mergebase differs', [r['pr'] for r in result if not r['comparison_base_is_merge_base']])
print('drift', [r['pr'] for r in result if not r['live_head_matches_pin'] or not r['live_base_matches_pin']])

from pathlib import Path
import subprocess,json,hashlib,datetime,collections,re
BASE=Path('/Users/alec/Documents/Math'); R=BASE/'final_full_solution_sweep_20261020_01a15be7'; O=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.run(['git',*a],cwd=BASE,capture_output=True,check=True).stdout
def row(line,path):
 c=[x.strip() for x in line.split('|')[1:-1]]
 if len(c)<9 or not c[0].isdigit(): return None
 m=re.match(r'^(\d+)(?:\s*/|$)',c[1])
 if not m:return None
 return dict(path=path,problem_id=m.group(1),status=c[7],turns=c[8],source_line=line)
ip=O/'inputs/inventory_private.json'
if not ip.exists(): ip.write_bytes((R/'rest_inventory.json').read_bytes())
inv=json.loads(ip.read_text())
results=[]; failures=[]
for n in range(833,883):
 p=next(p for p in inv['pull_requests'] if p['number']==n); e=json.loads((O/f'inputs/eligibility_{n:04}.json').read_text()); d=json.loads((O/f'inputs/disposition_{n:04}.json').read_text())
 for typ,path in [('eligibility',R/f'eligibility/pr{n:04}.json'),('disposition',R/f'PR{n:04}_DISPOSITION.json')]:
  saved=O/'inputs'/f'{typ}_{n:04}.json'
  if not saved.exists(): saved.write_bytes(path.read_bytes())
 comp=p['baseRefOid']+'...'+p['headRefOid']; paths=git('diff','--no-ext-diff','--no-renames','--name-only','-z',comp).decode().rstrip('\0').split('\0')
 cached=e['changed_paths']; added=[]; blobs=[]
 for path in paths:
  actual=git('rev-parse',p['headRefOid']+':'+path).decode().strip(); ce=next(x for x in e['files'] if x['filename']==path)
  blobs.append({'path':path,'actual':actual,'cached':ce['sha'],'equal':actual==ce['sha']})
  if path in ['QUEUE.md','unsolved_math_prioritization/QUEUE.md']:
   diff=git('diff','--no-ext-diff','--no-renames','--unified=0',comp,'--',path).decode()
   for line in diff.splitlines():
    if line.startswith('+') and not line.startswith('+++'):
     a=row(line[1:],path)
     if a:added.append(a)
 statuses=sorted(set(a['status'] for a in added)); own=[a for a in added if a['problem_id'] in d['problem_ids']]
 eqrow=lambda a:sorted((x.get('queue_path',x.get('path')),x['source_line'],x['problem_id'],x['status']) for x in a)
 checks={'path_sets_equal':len(paths)==len(set(paths))==e['file_count'] and set(paths)==set(cached) and len(e['files'])==len(paths),'added_rows_equal':eqrow(added)==eqrow(e['added_queue_rows']),'inventory_bound':e['inventory_head_sha']==p['headRefOid']==d['inventory_head_sha'] and e['inventory_base_sha']==p['baseRefOid']==d['inventory_base_sha'],'body_bound':sha(p['body'].encode())==d['inventory_body_sha256'],'own_row_exactly_one':len(own)==1,'own_problem_id_set':set(a['problem_id'] for a in added)==set(d['problem_ids'])}
 if d['disposition']=='skip_explicit_non_claimed_solved': checks['negative_status_authorized']=statuses==d['explicit_pr_queue_statuses'] and 'claimed_solved' not in statuses and d['current_classification'] in statuses
 if n in [833,838,872,880]: checks['claim_status']='claimed_solved' in statuses
 scientific=[b for b in blobs if b['path'] not in ['QUEUE.md','unsolved_math_prioritization/QUEUE.md'] and b['cached'] is not None]
 checks['scientific_cached_head_blobs_equal']=all(b['equal'] for b in scientific)
 if n in [838,872,880]:
  merge=p['mergeCommit']['oid']; mp=git('diff','--no-ext-diff','--no-renames','--name-only','-z',merge+'^1',merge).decode().rstrip('\0').split('\0'); checks['merge_first_parent_same_paths']=set(mp)==set(paths)
 bad=[k for k,v in checks.items() if not v]; failures.extend((n,k) for k in bad)
 a={'pr':n,'head':p['headRefOid'],'base':p['baseRefOid'],'comparison':comp,'path_count':len(paths),'checks':checks,'added_rows':added,'blob_checks':blobs,'disposition':d['disposition'],'classification':d['current_classification'],'scientific_body_read':n in [833,838,872,880]}
 results.append(a)
 (O/'per_pr').mkdir(exist_ok=True); (O/'per_pr'/f'PR{n:04}_ASSESSMENT.json').write_text(json.dumps(a,indent=2)+'\n')
summary={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'range':[833,882],'cases':len(results),'counts':dict(collections.Counter(a['disposition'] for a in results)),'statuses':dict(collections.Counter(a['added_rows'][0]['status'] for a in results)),'paths':sum(a['path_count'] for a in results),'failures':failures,'nonnull_cached_blob_mismatches':[{'pr':a['pr'],'blobs':[b for b in a['blob_checks'] if b['cached'] is not None and not b['equal']]} for a in results if any(b['cached'] is not None and not b['equal'] for b in a['blob_checks'])], 'null_cached_blobs_disclosed':{a['pr']:sum(b['cached'] is None for b in a['blob_checks']) for a in results if any(b['cached'] is None for b in a['blob_checks'])}}
(O/'PINNED_SCOPE_RESULTS.json').write_text(json.dumps(summary,indent=2)+'\n'); print(json.dumps(summary,indent=2))

#!/usr/bin/env python3
"""Read-only independent pinned Git comparison; no captured scripts run."""
import json,subprocess,pathlib,hashlib,re,datetime
W=pathlib.Path(__file__).resolve().parent; REPO=W.parents[2]
def git(*a):return subprocess.check_output(['git','-C',str(REPO),*a])
def sha(x):return hashlib.sha256(x).hexdigest()
def rows(patch):
 out=[]
 for line in patch.decode().splitlines():
  if line.startswith('+|'):
   s=line[1:];c=[v.strip() for v in s.strip().strip('|').split('|')]
   if len(c)>=8 and re.match(r'^\d+$',c[0]) and re.match(r'^\d+',c[1]):out.append({'queue_path':'unsolved_math_prioritization/QUEUE.md','source_line':s,'problem_id':re.match(r'^\d+',c[1]).group(),'status':c[7]})
 return out
results=[]
for n in range(883,906):
 d=json.loads((W/'inputs'/f'PR{n:04}_DISPOSITION.json').read_text());e=json.loads((W/'inputs'/f'pr{n:04}.json').read_text());b=d['inventory_base_sha'];h=d['inventory_head_sha'];comparison=f'{b}...{h}'
 changed=git('diff','--name-only','-z',comparison).decode().rstrip('\0').split('\0');changed=sorted(filter(None,changed));patch=git('diff','--no-ext-diff','--unified=0',comparison,'--','unsolved_math_prioritization/QUEUE.md');actual=rows(patch)
 bindings=[]
 for p in changed:
  q=subprocess.run(['git','-C',str(REPO),'rev-parse',f'{h}:{p}'],capture_output=True,text=True)
  z=q.stdout.strip() if q.returncode==0 else None; cached=[f.get('sha') for f in e['files'] if f.get('filename')==p]
  bindings.append({'path':p,'head_blob':z,'cached_blobs':cached,'cached_blob_equal':z in cached})
 (W/'inputs'/f'pr{n:04}_queue.patch').write_bytes(patch)
 a={'pr':n,'head':h,'base':b,'merge_base':git('merge-base',b,h).decode().strip(),'comparison':comparison,'path_count':len(changed),'changed_paths':changed,'paths_equal':changed==sorted(e['changed_paths']),'queue_patch_sha256':sha(patch),'own_added_rows':actual,'rows_equal':actual==[{k:x[k] for k in ['queue_path','source_line','problem_id','status']} for x in e['added_queue_rows']],'disposition':d['disposition'],'problem_ids':d['problem_ids'],'bindings':bindings,'cache_blob_mismatches':[x['path'] for x in bindings if any(v is not None for v in x['cached_blobs']) and not x['cached_blob_equal']], 'cache_unbound_blobs':[x['path'] for x in bindings if not any(v is not None for v in x['cached_blobs'])]}
 if (W/'inputs'/f'PR{n:04}_PUBLICATION_COVERAGE_DETAILS.json').exists():
  c=json.loads((W/'inputs'/f'PR{n:04}_PUBLICATION_COVERAGE_DETAILS.json').read_text()); covered={x['path']:x.get('actual_head_blob',x.get('head_blob')) for x in c.get('head_blob_bindings',[])}
  a['coverage_head_blob_bindings_equal']=all(covered.get(x['path'])==x['head_blob'] for x in bindings) if 'head_blob_bindings' in c else None;a['coverage_binding_count']=len(covered)
  if c.get('pinned_actual_merge'):
   m=c['pinned_actual_merge'];a['actual_merge_parents']=git('show','-s','--format=%P',m).decode().strip().split();a['merge_second_parent_is_head']=a['actual_merge_parents'][1]==h;a['merge_first_parent_paths_equal']=sorted(git('diff','--name-only',f'{m}^1',m).decode().splitlines())==changed
 if d['disposition']=='skip_explicit_non_claimed_solved':
  target=[x for x in actual if x['problem_id'] in d['problem_ids']];a['explicit_status_verified']=bool(target) and all(x['status'] in ['unsolved','already_solved'] for x in target) and sorted({x['status'] for x in target})==sorted(d['explicit_pr_queue_statuses'])
 else:a['claimed_status_verified']=bool(actual) and all(x['status']=='claimed_solved' for x in actual if x['problem_id'] in d['problem_ids'])
 results.append(a)
(W/'SCOPE_CHECKS.json').write_text(json.dumps({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':results},indent=2)+'\n')
for x in results:print(x['pr'],x['path_count'],x['paths_equal'],x['rows_equal'],[v['status'] for v in x['own_added_rows']],len(x['cache_blob_mismatches']),x.get('explicit_status_verified',x.get('claimed_status_verified')))

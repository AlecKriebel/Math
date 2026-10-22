from pathlib import Path
import subprocess,json,hashlib,re,datetime
W=Path(__file__).resolve().parent;R=W.parent.parent;REPO=R.parent;I=W/'private/inputs'
def git(*a):return subprocess.check_output(['git','-C',str(REPO),*a])
def h(b):return hashlib.sha256(b).hexdigest()
res=[]
for n in range(906,938):
 e=json.loads((I/f'eligibility/pr{n:04}.json').read_text());d=json.loads((I/f'PR{n:04}_DISPOSITION.json').read_text());b=d['inventory_base_sha'];head=d['inventory_head_sha'];compare=f'{b}...{head}'
 paths=git('diff','--name-only','--no-renames',compare).decode().splitlines();cached=e['changed_paths'];queue=[p for p in paths if p.endswith('/QUEUE.md')];actualrows=[];blobs=[]
 for p in queue:
  patch=git('diff','--no-ext-diff','--no-renames','--unified=0',compare,'--',p).decode(); (W/'private'/f'pr{n:04}_queue.patch').write_text(patch)
  for ln in patch.splitlines():
   if ln.startswith('+|'):
    raw=ln[1:];cols=[x.strip() for x in raw.split('|')[1:-1]]
    if len(cols)>8 and cols[0].isdigit():actualrows.append({'queue_path':p,'source_line':raw,'problem_id':cols[1].split('/')[0].strip(),'alias':cols[1],'title':cols[2],'status':cols[7],'turns':cols[8]})
 for p in paths:
  v=git('ls-tree',head,'--',p).decode().strip();fields=v.split(None,3);actual=fields[2] if len(fields)>2 else None
  cachedsha=next((x.get('sha') for x in e['files'] if x['filename']==p),None)
  blobs.append({'path':p,'head_blob':actual,'cached_blob':cachedsha,'cached_present':cachedsha is not None,'matches':actual is not None and cachedsha is not None and actual==cachedsha})
 cachedrows=sorted((x['queue_path'],x['source_line']) for x in e['added_queue_rows']); rows=sorted((x['queue_path'],x['source_line']) for x in actualrows)
 own=[x for x in actualrows if x['problem_id'] in d['problem_ids']]; ownpaths=[p for p in paths if any('/'+pid+'/' in p or '_'+pid+'/' in p for pid in d['problem_ids'])]
 result={'pr':n,'comparison':compare,'paths':paths,'path_count':len(paths),'path_cache_equal':set(paths)==set(cached),'added_rows':actualrows,'added_rows_cache_equal':rows==cachedrows,'all_blob_ids_match':all(x['matches'] for x in blobs),'blobs':blobs,'own_row_count':len(own),'own_path_count':len(ownpaths),'own_statuses':[x['status'] for x in own],'own_turns':[x['turns'] for x in own],'disposition':d['disposition'],'own_row_status_matches_disposition':(all(x['status']!='claimed_solved' for x in own) if d['disposition']=='skip_explicit_non_claimed_solved' else all(x['status']=='claimed_solved' for x in own))}
 res.append(result)
(W/'SCOPE_CHECKS.json').write_text(json.dumps({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cases':res},indent=2)+'\n')
for x in res: print(x['pr'],x['path_count'],x['own_path_count'],','.join(x['own_statuses']),','.join(x['own_turns']),x['path_cache_equal'],x['added_rows_cache_equal'],x['all_blob_ids_match'],x['disposition'])

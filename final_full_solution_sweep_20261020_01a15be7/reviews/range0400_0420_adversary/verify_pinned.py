from pathlib import Path
import json,subprocess,os,hashlib,datetime,shutil,re
root=Path('/Users/alec/Documents/Math');p=root/'final_full_solution_sweep_20261020_01a15be7';out=p/'reviews/range0400_0420_adversary';env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'}
def git(*args): return subprocess.check_output(['git',*args],cwd=root,env=env)
def sha(b):return hashlib.sha256(b).hexdigest()
metas={x['pr']:x['result']['structuredContent'] for x in json.loads((out/'live_metadata.json').read_text())}
inv={x['number']:x for x in json.loads((out/'inventory_snapshot.json').read_text())}
results=[];blob_manifest=[]
(out/'inputs').mkdir(exist_ok=True);(out/'diffs').mkdir(exist_ok=True);(out/'queue_diffs').mkdir(exist_ok=True)
for n in range(400,421):
 d=json.loads((p/f'PR{n:04d}_DISPOSITION.json').read_text());e=json.loads((p/f'eligibility/pr{n:04d}.json').read_text());m=metas[n];h=m['head_sha'];b=m['base_sha'];comp=f'{b}...{h}'
 paths=git('diff','--name-only',comp).decode().splitlines();patch=git('diff','--no-ext-diff','--no-renames',comp);(out/'diffs'/f'pr{n:04d}.diff').write_bytes(patch)
 queues=[x for x in paths if x.endswith('QUEUE.md')];qpatch=git('diff','--no-ext-diff','--no-renames',comp,'--',*queues) if queues else b'';(out/'queue_diffs'/f'pr{n:04d}.diff').write_bytes(qpatch)
 rows=[x[1:] for x in qpatch.decode().splitlines() if x.startswith('+|')];minus=[x[1:] for x in qpatch.decode().splitlines() if x.startswith('-|')]
 file_checks=[]
 for f in e['files']:
  path=f['filename'];proc=subprocess.run(['git','rev-parse',f'{h}:{path}'],cwd=root,env=env,capture_output=True,text=True);actual=proc.stdout.strip() if proc.returncode==0 else None
  file_checks.append({'path':path,'cached_sha':f.get('sha'),'actual_head_blob':actual,'equal':actual==f.get('sha')})
 qblobs=[]
 for qp in queues:
  blob=git('rev-parse',f'{h}:{qp}').decode().strip();data=git('cat-file','blob',blob);qblobs.append({'path':qp,'blob':blob,'bytes':len(data),'sha256':sha(data)})
  blob_manifest.append({'pr':n,**qblobs[-1]})
  (out/'inputs'/f'pr{n:04d}_queue_head.txt').write_bytes(data)
 own=d.get('problem_ids',[]);own_added={x:[r for r in rows if re.search(r'\|\s*'+re.escape(x)+r'\s*(?:/|\|)',r)] for x in own};own_all={x:[r for qp in queues for r in git('show',f'{h}:{qp}').decode().splitlines() if re.search(r'^\|\s*\d+\s*\|\s*'+re.escape(x)+r'\s*(?:/|\|)',r)] for x in own}
 result={'pr':n,'head':h,'base':b,'pinned_paths':paths,'pinned_path_count':len(paths),'live_changed_files':m.get('changed_files'),'paths_match_cache':sorted(paths)==sorted(e['changed_paths']),'cache_file_count_matches':len(paths)==e['file_count'],'live_file_count_matches':len(paths)==m.get('changed_files'),'head_matches_inventory_disposition_eligibility':h==inv[n]['headRefOid']==d['inventory_head_sha']==e['inventory_head_sha'],'base_matches_inventory_disposition_eligibility':b==inv[n]['baseRefOid']==d['inventory_base_sha']==e['inventory_base_sha'],'body_matches_inventory_and_disposition':m['body']==inv[n]['body'] and sha(m['body'].encode())==d['inventory_body_sha256'],'state_matches_inventory':m['state'].upper()==inv[n]['state'] or (m['merged'] and inv[n]['state']=='MERGED'),'patch_sha256':sha(patch),'queue_patch_sha256':sha(qpatch),'queue_added_rows':rows,'queue_removed_rows':minus,'queue_added_rows_match_cache':sorted(rows)==sorted(x['source_line'] for x in e['added_queue_rows']),'own_added_rows':own_added,'own_head_rows':own_all,'file_blob_mismatches':[x for x in file_checks if x['cached_sha'] and not x['equal']],'missing_cached_blob_shas':[x['path'] for x in file_checks if not x['cached_sha']],'file_checks':file_checks,'queues':qblobs}
 results.append(result)
 for file in [p/f'PR{n:04d}_DISPOSITION.json',p/f'eligibility/pr{n:04d}.json']:shutil.copyfile(file,out/'inputs'/file.name)
for f in ['CLASSIFICATION_POLICY.md','PR0411_PINNED_SCOPE_VERIFICATION.json','PR0411_PUBLICATION_VERIFICATION.json','PR0411_PUBLICATION_LEADS.json','PR0415_MISSING_STATUS_CLASSIFICATION.json']:shutil.copyfile(p/f,out/'inputs'/f)
(out/'pinned_checks.json').write_text(json.dumps({'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':results},indent=2)+'\n')
(out/'GIT_BLOB_INPUT_MANIFEST.json').write_text(json.dumps(blob_manifest,indent=2)+'\n')
for r in results:print(r['pr'],r['pinned_path_count'],'paths',r['paths_match_cache'],'rows',r['queue_added_rows_match_cache'],'head',r['head_matches_inventory_disposition_eligibility'],'base',r['base_matches_inventory_disposition_eligibility'],'body',r['body_matches_inventory_and_disposition'],'state',r['state_matches_inventory'],'file_mismatches',len(r['file_blob_mismatches']),'ownrowcounts', {k:len(v) for k,v in r['own_head_rows'].items()})

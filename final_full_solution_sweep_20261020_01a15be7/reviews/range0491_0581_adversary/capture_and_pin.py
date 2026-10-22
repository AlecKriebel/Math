from pathlib import Path
import collections,datetime as dt,hashlib,json,os,re,subprocess,sys
sys.dont_write_bytecode=True
os.environ.update(PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0')
Q=Path(__file__).resolve().parent;R=Q.parent.parent;REPO=R.parent
now=lambda:dt.datetime.now(dt.timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(n,d):
 p=Q/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(d if isinstance(d,bytes) else (json.dumps(d,indent=2)+'\n').encode())
def run(args):return subprocess.run(args,cwd=REPO,capture_output=True,check=True).stdout
entries=[]
def cap(src,dst):
 p=R/src;assert not p.is_symlink() and p.is_file();b=p.read_bytes();save(dst,b);entries.append(dict(source=str(p),path=str(dst),bytes=len(b),sha256=sha(b),captured_at=now()));return b
save('RESEARCH_LOG.json',[dict(at=now(),completion_estimate_percent=3,event='Independent491–581 review begun. Writes confined to new review directory, no provider/Git mutations or communication.')])
for _ in range(50):
 a={n:(R/n).read_bytes() for n in ['STATE.json','rest_inventory.json','dispositions.jsonl']};s=json.loads(a['STATE.json']);j=[json.loads(x) for x in a['dispositions.jsonl'].splitlines() if x];coherent=[e['pr'] for e in j]==list(range(s['start_pr'],s['next_pr']))
 if coherent and all((R/n).read_bytes()==b for n,b in a.items()):break
else:raise RuntimeError('Could not capture coherent prefix')
for n,b in a.items():save('inputs/'+n,b);entries.append(dict(source=str(R/n),path='inputs/'+n,bytes=len(b),sha256=sha(b),captured_at=now()))
inv=json.loads(a['rest_inventory.json']);prs={p['number']:p for p in inv['pull_requests']};js={e['pr']:e for e in j};assert all(n in js for n in range(491,582));results=[];blobentries=[]
def git_blob(rev,path,out):
 oid=run(['git','rev-parse',rev+':'+path]).decode().strip();b=run(['git','show',rev+':'+path]);save(out,b);blobentries.append(dict(pr=current,commit=rev,repository_path=path,oid=oid,sha256=sha(b),bytes=len(b),captured_path=out));return b
for current in range(491,582):
 p=prs[current];e=json.loads(cap(f'eligibility/pr{current:04d}.json',f'inputs/eligibility/pr{current:04d}.json'));disp=json.loads(cap(f'PR{current:04d}_DISPOSITION.json',f'inputs/PR{current:04d}_DISPOSITION.json'));assert disp==js[current]
 assert e['pr']==current and e['inventory_head_sha']==p['headRefOid'] and e['inventory_base_sha']==p['baseRefOid']
 for rev in [p['headRefOid'],p['baseRefOid']]:
  if subprocess.run(['git','cat-file','-e',rev+'^{commit}'],cwd=REPO,capture_output=True).returncode:run(['git','fetch','--no-write-fetch-head','origin',rev])
 compare=p['baseRefOid']+'...'+p['headRefOid'];raw=run(['git','diff','--no-ext-diff','--no-renames','--name-only','-z',compare]);paths=raw.decode().rstrip('\0').split('\0') if raw else [];assert len(paths)==len(set(paths)) and set(paths)==set(e['changed_paths']);assert e['file_count']==len(paths) and sorted(x['filename'] for x in e['files'])==sorted(paths)
 rows=[];patches=[]
 for path in sorted(set(paths)&{'QUEUE.md','unsolved_math_prioritization/QUEUE.md'}):
  patch=run(['git','diff','--no-ext-diff','--no-renames','--unified=0',compare,'--',path]);save(f'pinned/pr{current:04d}/QUEUE.patch',patch);patches.append(dict(path=path,sha256=sha(patch)))
  for line in patch.decode().splitlines():
   if not line.startswith('+') or line.startswith('+++'):continue
   cells=[c.strip() for c in re.split(r'(?<!\\)\|',line[1:].strip().strip('|'))]
   if len(cells)>=9 and cells[0].isdigit():rows.append(dict(problem_id=cells[1].split('/')[0].strip(),status=cells[7],source_line=line[1:],path=path))
  git_blob(p['headRefOid'],path,f'pinned/pr{current:04d}/QUEUE.head.md')
 key=lambda x:(x.get('path',x.get('queue_path')),x['source_line'],x['problem_id'],x['status'])
 assert sorted(map(key,rows))==sorted(map(key,e['added_queue_rows']))
 own=disp.get('problem_ids',[]);assert len(own)==1;ownid=own[0];ownrows=[x for x in rows if x['problem_id']==ownid]
 # Capture body+complete changed files for nonstandard folders and publication original source.
 extras=[x for x in paths if x not in {'QUEUE.md','unsolved_math_prioritization/QUEUE.md'} and not re.search(r'(?:^|/)(?:attempts|problems)/'+re.escape(ownid)+r'(?=/|_)',x)]
 if extras or current in [521,533,563,570]:
  for path in paths:
   if path not in {'QUEUE.md','unsolved_math_prioritization/QUEUE.md'}:git_blob(p['headRefOid'],path,'pinned/pr%04d/files/'%current+path)
 if current==523:pass
 elif disp['disposition']=='skip_explicit_non_claimed_solved':
  assert ownrows and len({x['status'] for x in ownrows})==1 and ownrows[0]['status']!='claimed_solved'
 else:assert disp['disposition']=='skip_entirely_already_published' and ownrows and ownrows[0]['status']=='claimed_solved'
 results.append(dict(pr=current,state=p['state'],title=p['title'],head=p['headRefOid'],base=p['baseRefOid'],disposition=disp['disposition'],problem_id=ownid,actual_path_count=len(paths),complete_paths_equal=True,actual_paths=paths,actual_added_rows=rows,corresponding_rows=ownrows,nonstandard_paths=extras,body_sha256=sha((p.get('body') or '').encode()),patches=patches))
for n in ['CURRENT_CANONICAL_QUEUE_SNAPSHOT.json','PR0523_WITHDRAWAL_VERIFICATION.json']:
 cap(n,'inputs/'+n)
for current in [521,533,563,570]:
 for suffix in ['PUBLICATION_LEADS','PUBLICATION_VERIFICATION','PUBLICATION_COVERAGE_DETAILS']:
  n=f'PR{current:04d}_{suffix}.json';cap(n,'inputs/'+n)
save('pinned_scope_checks.json',results);save('GIT_BLOB_INPUT_MANIFEST.json',blobentries);save('INPUT_MANIFEST.json',dict(at=now(),files=entries,note='Each original source captured exactly. Coherent local prefix snapshot; changing canonical files may advance afterwards. Actual pinned Git blobs independently captured separately.'));save('capture_coherence.json',dict(at=now(),next_pr=s['next_pr'],journal_count=len(j),coherent_prefix=True,range_count=len(results)))
print(json.dumps(dict(range_count=len(results),counts=dict(collections.Counter(x['disposition'] for x in results)),nonstandard=[x['pr'] for x in results if x['nonstandard_paths']],blobs=len(blobentries))))

from pathlib import Path
import collections,datetime as dt,hashlib,json,os,re,subprocess,sys
sys.dont_write_bytecode=True
os.environ.update(PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0')
Q=Path(__file__).resolve().parent; R=Q.parent.parent; REPO=R.parent
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def require(ok,message):
 if not ok: raise RuntimeError(message)
def run(args,**kw): return subprocess.run(args,cwd=REPO,capture_output=True,check=True,**kw).stdout
def save(rel,obj):
 p=Q/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2)+'\n')
captures=[];blobs=[]
def capture(src,rel=None):
 require(src.is_file() and not src.is_symlink(),'nonregular input '+str(src));b=src.read_bytes();rel=Path('private/inputs')/(src.relative_to(R) if rel is None else rel)
 p=Q/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 captures.append(dict(source=str(src),path=str(rel),bytes=len(b),sha256=sha(b),captured_at=now(),source_mtime_ns=src.stat().st_mtime_ns));return b
def row(line,path):
 c=[s.strip() for s in re.split(r'(?<!\\)\|',line.strip().strip('|'))]
 if len(c)>=9 and c[0].isdigit():return dict(queue_path=path,problem_id=c[1].split('/')[0].strip(),status=c[7],source_line=line)
log=[dict(at=now(),completion_estimate_percent=5,event='Independent bounded 44 PR review started; only own new directory written.')];save('RESEARCH_LOG.json',log)
for attempt in range(30):
 raw={n:(R/n).read_bytes() for n in ['STATE.json','dispositions.jsonl','rest_inventory.json']};state=json.loads(raw['STATE.json']);journal=[json.loads(x) for x in raw['dispositions.jsonl'].splitlines() if x]
 if all((R/n).read_bytes()==b for n,b in raw.items()) and [e['pr'] for e in journal]==list(range(9,state['next_pr'])): break
else: raise RuntimeError('No coherent source capture')
for n,b in raw.items():
 got=capture(R/n);require(got==b,'capture race '+n)
for n in ['CLASSIFICATION_POLICY.md','COVERAGE_SNAPSHOT.json']:capture(R/n)
save('capture_coherence.json',dict(at=now(),attempt=attempt,next_pr=state['next_pr'],last_processed=state['last_completely_processed_pr'],journal_count=len(journal),coherent=True))
inv=json.loads(raw['rest_inventory.json']);prs={p['number']:p for p in inv['pull_requests']};ds={d['pr']:d for d in journal}
query='query { repository(owner:"AlecKriebel",name:"Math") {'+' '.join(f'p{n}:pullRequest(number:{n}){{number title body state isDraft mergedAt updatedAt headRefOid baseRefOid mergeCommit{{oid}}}}' for n in range(628,672))+'} }'
wire=run(['gh','api','--hostname','github.com','graphql','--input','-'],input=json.dumps({'query':query}).encode());live=json.loads(wire);require('errors' not in live,'provider errors');save('private/initial_live_prs.json',live);(Q/'private/initial_live_wire.json').write_bytes(wire)
diffs=[]
for n in range(628,672):
 p=live['data']['repository'][f'p{n}'];delta=[k for k in p if p[k]!=prs[n].get(k)]
 if delta:diffs.append(dict(pr=n,fields=delta))
save('initial_live_metadata_receipt.json',dict(at=now(),raw_sha256=sha(wire),count=44,differences=diffs))
assessments=[];scopes=[];blob_values=[]
for n in range(628,672):
 e=json.loads(capture(R/f'eligibility/pr{n:04d}.json'));d=json.loads(capture(R/f'PR{n:04d}_DISPOSITION.json'));p=prs[n]
 require(d==ds[n] and e['pr']==n,'journal or eligibility mismatch '+str(n));require(e['inventory_head_sha']==p['headRefOid'] and e['inventory_base_sha']==p['baseRefOid'],'eligibility commit mismatch')
 for commit in [p['baseRefOid'],p['headRefOid']]+([p['mergeCommit']['oid']] if p['mergeCommit'] else []):
  if subprocess.run(['git','cat-file','-e',commit+'^{commit}'],cwd=REPO,capture_output=True).returncode:run(['git','fetch','--no-write-fetch-head','origin',commit])
 comparison=p['baseRefOid']+'...'+p['headRefOid'];basis='inventory_base_three_dot_head';extra={}
 if n==662:
  m=p['mergeCommit']['oid'];comparison=m+'^1..'+m;parents=run(['git','show','--no-patch','--format=%P',m]).decode().split();require(len(parents)==2 and parents[1]==p['headRefOid'],'actual merge parent mismatch');require(e['pinned_comparison']==comparison,'cached fallback basis mismatch');basis='actual_merge_first_parent_delta';extra=dict(actual_merge=m,parents=parents)
 wire=run(['git','diff','--no-ext-diff','--no-renames','--name-only','-z',comparison]);paths=wire.decode().rstrip('\0').split('\0') if wire else []
 require(len(paths)==len(set(paths))==e['file_count']==len(e['files']),'file count mismatch '+str(n));require(set(paths)==set(e['changed_paths'])=={f['filename'] for f in e['files']},'path mismatch '+str(n));cached={f['filename']:f for f in e['files']}
 qp=set(paths)&{'QUEUE.md','unsolved_math_prioritization/QUEUE.md'};rows=[]
 for path in qp:
  patch=run(['git','diff','--no-ext-diff','--no-renames','--unified=0',comparison,'--',path]);rel=Path('private/git_inputs')/f'pr{n:04d}'/'QUEUE.patch';dest=Q/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(patch)
  for line in patch.decode().splitlines():
   if line.startswith('+') and not line.startswith('+++'):
    rr=row(line[1:],path)
    if rr:rows.append(rr)
 require(len(rows)==1,'expected one own changed row '+str(n));pid=rows[0]['problem_id'];require(d['problem_ids']==[pid],'row PID differs from disposition');key=lambda rr:(rr['queue_path'],rr['source_line'],rr['problem_id'],rr['status']);require(sorted(map(key,rows))==sorted(map(key,e['added_queue_rows'])),'added row differs '+str(n))
 require(all(path in qp or path.startswith('unsolved_math_prioritization/attempts/'+pid+'/') or n==662 and path.startswith('unsolved_math_prioritization/publications/'+pid+'/') for path in paths),'unrelated changed scope '+str(n))
 for path in paths:
  blob=run(['git','rev-parse',p['headRefOid']+':'+path]).decode().strip();cachedblob=cached[path].get('sha');ceq=blob==cachedblob if cachedblob is not None else None
  require(ceq is not False,'cached science SHA differs '+str(n)+' '+path)
  entry=dict(pr=n,path=path,head=p['headRefOid'],git_blob=blob,cached_blob=cachedblob,cached_blob_equal=ceq)
  if n==662:entry['actual_merge_blob']=run(['git','rev-parse',p['mergeCommit']['oid']+':'+path]).decode().strip();require(entry['actual_merge_blob']==blob,'head actual merge blob differs')
  blob_values.append(entry)
  if path in qp or n in [628,630,662]:
   b=run(['git','show',p['headRefOid']+':'+path]);rel=Path('private/git_inputs')/f'pr{n:04d}'/path;dest=Q/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b);blobs.append(dict(**entry,captured_path=str(rel),bytes=len(b),sha256=sha(b),captured_at=now()))
 if n==662:
  for suffix in ['PUBLICATION_VERIFICATION','PUBLICATION_LEADS','PUBLICATION_COVERAGE_DETAILS','PINNED_SCOPE_VERIFICATION']:capture(R/f'PR{n:04d}_{suffix}.json')
 elif n in [628,630]:
  require(rows[0]['status']=='claimed_solved' and d['disposition']=='skip_priority_gate_not_met','hold classification differs')
 else:require(rows[0]['status'] in {'unsolved','already_solved'} and d['disposition']=='skip_explicit_non_claimed_solved' and d['current_classification']==rows[0]['status'],'negative status failure '+str(n))
 scope_rows=[dict(queue_path=rr['queue_path'],problem_id=rr['problem_id'],status=rr['status'],source_line_sha256=sha(rr['source_line'].encode())) for rr in rows]
 scopes.append(dict(pr=n,comparison=comparison,basis=basis,path_count=len(paths),complete_paths=paths,complete_paths_equal=True,own_rows=scope_rows,all_paths_own_problem=True,**extra))
 assessments.append(dict(pr=n,problem_id=pid,explicit_status=rows[0]['status'],disposition=d['disposition'],recorded_classification=d['current_classification'],scope_verified=True,negative_science_bodies_skipped=n not in [628,630,662],missing_status_inference_required=False))
save('INPUT_MANIFEST.json',dict(at=now(),files=captures));save('GIT_BLOB_INPUT_MANIFEST.json',dict(at=now(),files=blobs));save('pinned_blob_values.json',blob_values);save('pinned_scope_checks.json',scopes);save('per_pr_assessments.json',assessments)
log.append(dict(at=now(),completion_estimate_percent=35,event='All 44 actual complete pinned scopes and own added rows independently checked; 41 explicit negatives, two holds, one existing publication.'));save('RESEARCH_LOG.json',log)
print(json.dumps(dict(prs=len(scopes),git_blob_bodies=len(blobs),path_blob_checks=len(blob_values),classifications=dict(collections.Counter(x['recorded_classification'] for x in assessments)),live_differences=diffs)))

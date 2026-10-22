from pathlib import Path
import collections,datetime as dt,hashlib,json,os,re,subprocess,sys
sys.dont_write_bytecode=True
os.environ.update(PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0')
Q=Path(__file__).resolve().parent
R=Q.parent.parent
REPO=R.parent
PUB={582:('30004404',23386475,97),585:('30001232',23387814,101),618:('30004609',23331709,73),623:('30001184',23356540,88)}
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,d):
 p=Q/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+'\n')
def run(args):return subprocess.run(args,cwd=REPO,capture_output=True,check=True).stdout
captures=[]
def capture(src,rel,data=None):
 assert not src.is_symlink() and src.is_file()
 b=src.read_bytes() if data is None else data;p=Q/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 captures.append(dict(source=str(src),path=str(rel),bytes=len(b),sha256=sha(b),captured_at=now()))
def row(line,path):
 c=[s.strip() for s in re.split(r'(?<!\\)\|',line.strip().strip('|'))]
 if len(c)>=9 and c[0].isdigit():return dict(queue_path=path,problem_id=c[1].split('/')[0].strip(),status=c[7],source_line=line)
log=[dict(at=now(),completion_estimate_percent=5,event='Independent46PR range review started; writes restricted to own new directory; no provider/Git mutations.')]
save('RESEARCH_LOG.json',log)
for attempt in range(30):
 raw={n:(R/n).read_bytes() for n in ['STATE.json','dispositions.jsonl','rest_inventory.json']};state=json.loads(raw['STATE.json']);journal=[json.loads(x) for x in raw['dispositions.jsonl'].splitlines() if x]
 stable=all((R/n).read_bytes()==b for n,b in raw.items());coherent=[e['pr'] for e in journal]==list(range(9,state['next_pr']))
 if stable and coherent:break
else:raise RuntimeError('No coherent capture')
save('capture_coherence.json',dict(at=now(),attempt=attempt,stable=stable,coherent=coherent,next_pr=state['next_pr'],count=len(journal)))
for n,b in raw.items():capture(R/n,Path('inputs')/n,b)
inventory=json.loads(raw['rest_inventory.json']);prs={p['number']:p for p in inventory['pull_requests']};dispositions={e['pr']:e for e in journal}
assessments=[];scopes=[];blobs=[]
for n in range(582,628):
 epath=f'eligibility/pr{n:04d}.json';dpath=f'PR{n:04d}_DISPOSITION.json'
 for name in [epath,dpath]:capture(R/name,Path('inputs')/name)
 e=json.loads((Q/'inputs'/epath).read_text());d=json.loads((Q/'inputs'/dpath).read_text());p=prs[n]
 assert d==dispositions[n] and e['pr']==n and e['inventory_head_sha']==p['headRefOid'] and e['inventory_base_sha']==p['baseRefOid']
 for commit in [p['baseRefOid'],p['headRefOid']]+([p['mergeCommit']['oid']] if p['mergeCommit'] else []):
  if subprocess.run(['git','cat-file','-e',commit+'^{commit}'],cwd=REPO,capture_output=True).returncode:run(['git','fetch','--no-write-fetch-head','origin',commit])
 comparison=p['baseRefOid']+'...'+p['headRefOid'];basis='inventory_base_three_dot_head'
 if n in [618,623]:
  m=p['mergeCommit']['oid'];comparison=m+'^1..'+m;parents=run(['git','show','--no-patch','--format=%P',m]).decode().split()
  assert len(parents)==2 and parents[1]==p['headRefOid'];assert e['pinned_comparison']==comparison
  assert e['file_list_source']=='complete pinned merged-commit first-parent diff; large live file-list endpoint bypassed'
  basis='actual_merge_first_parent_delta';extra=dict(actual_merge=m,parents=parents)
 else:extra={}
 wire=run(['git','diff','--no-ext-diff','--no-renames','--name-only','-z',comparison]);paths=wire.decode().rstrip('\0').split('\0') if wire else []
 assert len(paths)==len(set(paths))==e['file_count']==len(e['files'])
 assert set(paths)==set(e['changed_paths']) and sorted(paths)==sorted(x['filename'] for x in e['files'])
 queuepaths=set(paths)&{'QUEUE.md','unsolved_math_prioritization/QUEUE.md'};rows=[]
 for qp in queuepaths:
  patch=run(['git','diff','--no-ext-diff','--no-renames','--unified=0',comparison,'--',qp]).decode()
  for line in patch.splitlines():
   if line.startswith('+') and not line.startswith('+++'):
    rr=row(line[1:],qp)
    if rr:rows.append(rr)
  b=run(['git','show',p['headRefOid']+':'+qp]);rel=Path('git_inputs')/f'pr{n:04d}'/'QUEUE.head.md';dest=Q/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b);blobs.append(dict(pr=n,path=qp,commit=p['headRefOid'],git_blob=run(['git','rev-parse',p['headRefOid']+':'+qp]).decode().strip(),captured_path=str(rel),bytes=len(b),sha256=sha(b)))
 assert len(rows)==1;pid=rows[0]['problem_id'];assert d['problem_ids']==[pid]
 key=lambda rr:(rr['queue_path'],rr['source_line'],rr['problem_id'],rr['status'])
 assert sorted(map(key,rows))==sorted(map(key,e['added_queue_rows']))
 assert all(path in queuepaths or path.startswith('unsolved_math_prioritization/attempts/'+pid+'/') or path.startswith('attempts/'+pid+'/') for path in paths)
 if n in PUB or n==615:
  for path in paths:
   if path in queuepaths:continue
   b=run(['git','show',p['headRefOid']+':'+path]);blob=run(['git','rev-parse',p['headRefOid']+':'+path]).decode().strip();rel=Path('git_inputs')/f'pr{n:04d}'/path;dest=Q/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b);entry=dict(pr=n,path=path,commit=p['headRefOid'],git_blob=blob,captured_path=str(rel),bytes=len(b),sha256=sha(b))
   if n in [618,623]:
    mergeblob=run(['git','rev-parse',p['mergeCommit']['oid']+':'+path]).decode().strip();assert mergeblob==blob;entry['actual_merge_blob_equal']=True
   blobs.append(entry)
 if n in PUB:
  assert rows[0]['status']=='claimed_solved' and d['disposition']=='skip_entirely_already_published'
  for suffix in ['PUBLICATION_VERIFICATION','PUBLICATION_LEADS','PUBLICATION_COVERAGE_DETAILS','PINNED_SCOPE_VERIFICATION']:
   name=f'PR{n:04d}_{suffix}.json';capture(R/name,Path('inputs')/name)
 elif n==615:
  assert rows[0]['status']=='claimed_solved' and d['disposition']=='skip_priority_gate_not_met';assert d['pr_state']=='CLOSED'
 else:
  assert rows[0]['status'] in {'unsolved','already_solved'} and d['disposition']=='skip_explicit_non_claimed_solved';assert d['current_classification']==rows[0]['status']
 scopes.append(dict(pr=n,comparison=comparison,basis=basis,path_count=len(paths),complete_paths_equal=True,own_rows=rows,all_paths_own_problem=True,**extra))
 assessments.append(dict(pr=n,problem_id=pid,explicit_status=rows[0]['status'],disposition=d['disposition'],recorded_classification=d['current_classification'],scope_verified=True))
for name in ['ROOT_FINAL_RECHECK_ACCEPTANCE.json','ROOT_ORIGINAL_REPLAY.json','DUPLICATE_ACCOUNT_CHECK.json','DUPLICATE_AND_EXISTING_PACKAGE_RECONCILIATION.json','ROOT_PRIOR_IMPLICATION_RECHECK.md','reviews/priority_recheck01/REPORT.md','reviews/priority_recheck01/DERIVATION.md','reviews/priority_recheck01/OUTPUT_MANIFEST.json']:
 src=R/'audits/pr0615_4200010'/name;capture(src,Path('inputs/audits/pr0615_4200010')/name)
save('INPUT_MANIFEST.json',dict(at=now(),files=captures,note='Exact individual captures; coherent numerical prefix. Later canonical progress expected.'))
save('GIT_BLOB_INPUT_MANIFEST.json',dict(at=now(),files=blobs))
save('pinned_scope_checks.json',scopes);save('per_pr_assessments.json',assessments)
log.append(dict(at=now(),completion_estimate_percent=35,event='All46 actual pinned scopes/ownrows independently verified; four publications and one priorhold identified.'))
save('RESEARCH_LOG.json',log)
print(json.dumps(dict(prs=len(scopes),git_blobs=len(blobs),outcomes=dict(collections.Counter(x['recorded_classification'] for x in assessments)))))

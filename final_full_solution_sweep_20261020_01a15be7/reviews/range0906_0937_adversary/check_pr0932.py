from pathlib import Path,PurePosixPath
import json,hashlib,subprocess,datetime,shutil
W=Path(__file__).resolve().parent;A=W/'private/pr0932_audit';REPO=W.parents[2];F=W/'private/fresh932'
def h(b):return hashlib.sha256(b).hexdigest()
def require(t,m):
 if not t:raise ValueError(m)
def verify_files(root,items):
 if isinstance(items,dict):items=[dict(v,path=k) for k,v in items.items()]
 names=[]
 for x in items:
  p=PurePosixPath(x['path']);require(not p.is_absolute() and '..' not in p.parts and str(p)==x['path'],'unsafe pin')
  f=root/x['path'];require(f.is_file() and not f.is_symlink(),'nonregular pin');b=f.read_bytes();require(len(b)==x['bytes'] and h(b)==x['sha256'],'hash '+str(f));names.append(x['path'])
 require(len(names)==len(set(names)),'duplicate pin')
 return names
out={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'errors':[]}
snap=json.loads((A/'SOURCE_SNAPSHOT.json').read_text());prefix=snap['prefix'];head=snap['head'];actual=subprocess.check_output(['git','-C',str(REPO),'ls-tree','-r','--name-only',head,'--',prefix]).decode().splitlines();require(sorted(x[len(prefix):] for x in actual)==sorted(x['path'] for x in snap['files']),'original inventory');verify_files(A/'original',snap['files'])
for x in snap['files']:
 b=subprocess.check_output(['git','-C',str(REPO),'show',head+':'+prefix+x['path']]);require(b==(A/'original'/x['path']).read_bytes(),'original blob')
out['immutable_originals_exact']=len(snap['files']);out['original_manifest_payloads']={}
for name in ['PUBLICATION_MANIFEST.json','public/MANIFEST.json','audit_a/AUDIT_MANIFEST.json','audit_b/AUDIT_MANIFEST.json']:
 p=A/'original'/name;d=json.loads(p.read_text());out['original_manifest_payloads'][name]=len(verify_files(p.parent,d['files']))
for family,manifest,seal in [('proof_recheck01','REVIEW_MANIFEST.json','SEAL.txt'),('priority_recheck01','MANIFEST.json','MANIFEST.json.sha256')]:
 p=A/'reviews'/family;m=p/manifest;b=m.read_bytes();require(h(b)==(p/seal).read_text().split()[0],'seal '+family);d=json.loads(b);names=verify_files(p,d['files']);out[family]={'manifest_sha256':h(b),'payloads':len(names),'seal_valid':True}
 if family=='priority_recheck01':
  private=json.loads((p/'PRIVATE_SOURCE_MANIFEST.json').read_text())['files'];pn=verify_files(p/'private',private);actualpriv=sorted(x.relative_to(p/'private').as_posix() for x in (p/'private').rglob('*') if x.is_file());require(sorted(pn)==actualpriv,'private closure');out[family]['private_payloads']=len(pn)
  for opt in [False,True]:
   cmd=['python3']+(['-O'] if opt else [])+['-B',str(p/'verify_review.py')];proc=subprocess.run(cmd,capture_output=True,check=True);(W/'private'/('priority_replay_optimized.json' if opt else 'priority_replay_normal.json')).write_bytes(proc.stdout)
  require((W/'private/priority_replay_normal.json').read_bytes()==(W/'private/priority_replay_optimized.json').read_bytes(),'priority normal/O mismatch');out[family]['normal_and_optimized_copied_replay_equal']=True
 else:
  savedres=(p/'EVIDENCE_RESULTS.json').read_bytes();savedbind=(p/'SOURCE_BINDINGS.json').read_bytes();driver=W/'private/proof_replay_driver.py'; driver.write_text((p/'EVIDENCE.py').read_text().replace('HERE = Path(__file__).resolve().parent', 'HERE = Path('+repr(str(p))+')').replace('REPO = AUDIT.parents[2]', 'REPO = Path('+repr(str(REPO))+')')); proc=subprocess.run(['python3','-B',str(driver)],capture_output=True,check=True); out[family]['path_only_relocation']={'original_source_sha256':h((p/'EVIDENCE.py').read_bytes()),'runner_sha256':h(driver.read_bytes()),'changes':['HERE fixed to private copied reviewer directory','REPO fixed to actual repository root'],'reason':'unmodified copied runner computes repo from original nesting; git ls-tree paths otherwise interpreted from wrong subdirectory'};(W/'private/proof_replay_stdout.json').write_bytes(proc.stdout);require((p/'EVIDENCE_RESULTS.json').read_bytes()==savedres and (p/'SOURCE_BINDINGS.json').read_bytes()==savedbind,'proof replay mismatch');out[family]['normal_copied_complete_certificate_equal']=True
  sourcepins=json.loads(savedbind)['primary_downloads'];out[family]['primary_bodies']=[]
  for x in sourcepins:
   b=(p/'private'/(x['name']+'.pdf')).read_bytes();require(len(b)==x['bytes'] and h(b)==x['sha256'],'source body');out[family]['primary_bodies'].append({'name':x['name'],'sha256':h(b),'bytes':len(b)})
# Independently tie fresh platform records to content addressed theorem PDF.
run=json.loads((F/'winter_run.json').read_text());jobs=json.loads((F/'winter_jobs.json').read_text())['jobs'];commit=json.loads((F/'winter_commit.json').read_text());deployment=json.loads((F/'winter_deployment.json').read_text());statuses=json.loads((F/'winter_statuses.json').read_text());success=next(s for s in statuses if s['id']==17842306951);pdf=(F/'winter_pinned.pdf').read_bytes();blob=hashlib.sha1(b'blob '+str(len(pdf)).encode()+b'\0'+pdf).hexdigest();pdfentry=next(x for x in commit['files'] if x['filename']=='pdf/publications/Stokers_conjecture.pdf')
require(blob==pdfentry['sha']=='592725cde9a0783de0f4a6216f241ab07db2518b','content address');require(pdf==(A/'reviews/priority_recheck01/private/winter_pinned.pdf').read_bytes(),'review theorem PDF');sha='766c313bc2187a5eafd5757dca43ffefc6a9ced6';require(run['head_sha']==deployment['sha']==commit['sha']==sha,'platform sha');require(run['id']==33918657115 and run['conclusion']=='success' and run['created_at']=='2026-09-04T20:55:50Z','run');require(len(jobs)==3 and all(j['head_sha']==sha and j['conclusion']=='success' and j['run_id']==run['id'] for j in jobs),'jobs');require(deployment['id']==6272679551 and deployment['created_at']=='2026-09-04T20:56:21Z','deployment');require(success['state']=='success' and success['created_at']=='2026-09-04T20:56:33Z' and success['environment_url']=='https://martinwintermath.github.io/','status');out['fresh_platform_chain']={'exact_sha':sha,'run_id':run['id'],'run_created':run['created_at'],'successful_jobs':len(jobs),'deployment':deployment['id'],'success_status':success['id'],'success_at':success['created_at'],'pdf_sha256':h(pdf),'pdf_git_blob':blob,'no_September_HTTP_snapshot':True}
pr=json.loads((F/'pr.json').read_text());closure=json.loads((F/'closure.json').read_text());inv=json.loads((W/'private/inputs/rest_inventory.json').read_text());originalpr=next(x for x in inv['pull_requests'] if x['number']==932);require(pr['head']['sha']==head and pr['state']=='closed' and not pr['merged'] and pr['title']==originalpr['title'] and pr['body']==originalpr['body'],'live PR');assessment=json.loads((A/'ROOT_FINAL_ASSESSMENT.json').read_text());require(h(closure['body'].encode())==assessment['existing_closure_sha256'],'closure');out['live_pr_and_closure']={'closed_unmerged_same_head_title_body':True,'closure_id':closure['id'],'closure_body_sha256':h(closure['body'].encode()),'new_provider_write':False}
# Reinspect retained root account payload; this is a separately parsed captured account, not a fresh account request.
account=A/'private/final_account.json';ac=json.loads(account.read_text());require(ac['total']==197 and ac['pages']==8 and len(ac['records'])==197 and len({x['id'] for x in ac['records']})==197,'account counts');rootlive=json.loads((A/'ROOT_FINAL_LIVE_CHECK.json').read_text());require(h(account.read_bytes())==rootlive['account_sha256'],'account pin');terms=['30003471','owr-15427-013','/pull/932','pr932','pr #932','stoker','dihedral','facet normal','facet-normal'];hits=[]
for rec in ac['records']:
 txt=json.dumps(rec).lower()
 if any(t in txt for t in terms):hits.append({'record':rec['id'],'title':rec['metadata']['title']})
require(not hits,'account lead');out['captured_account_reinspection']={'total':197,'pages':8,'unique_records':197,'sha256':h(account.read_bytes()),'matches':hits,'fresh_authenticated_account_request':False}
# Independent current local deposited-state scan, isolated snapshot kept ignored.
state=REPO/'.zenodo-state';files=sorted(state.rglob('*.json'));local=[];copy=W/'private/local_zenodo_state';copy.mkdir(exist_ok=True)
for f in files:
 b=f.read_bytes();rel=f.relative_to(state);target=copy/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b);txt=b.decode().lower();local.append({'path':rel.as_posix(),'bytes':len(b),'sha256':h(b),'matches':[t for t in terms if t in txt]})
out['local_deposit_state']={'files_scanned':len(local),'matches':[x for x in local if x['matches']]};(W/'private/LOCAL_DEPOSIT_SCAN.json').write_text(json.dumps(local,indent=2)+'\n')
(W/'PR0932_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

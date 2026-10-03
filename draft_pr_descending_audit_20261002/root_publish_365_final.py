"""Publish only owned PR365 closed audits, exact acceptance and post evidence."""
from pathlib import Path,PurePosixPath
import datetime,hashlib,json,subprocess
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr365_2303002';paths=set();sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def add(p):
 assert p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(P)
 rel=p.relative_to(P)
 if any('private' in x or x in {'tmp','__pycache__','raw_sources'} for x in rel.parts):return
 if p.parent.name=='root_family_streams' and p.name.startswith('poisson_api_'):return
 assert p.suffix not in {'.pdf','.png','.html','.log'}
 paths.add(str(p.relative_to(R)))
def directory(d):
 for p in d.rglob('*'):
  if p.is_file():add(p)
def manifest(d,name):
 m=json.loads((d/name).read_bytes());fs=m.get('files',m.get('public_files'));fs={e['path']:e for e in fs} if isinstance(fs,list) else fs
 for path,e in fs.items():
  q=PurePosixPath(path);assert not q.is_absolute() and '..' not in q.parts and q.as_posix()==path
  b=(d/path).read_bytes();assert len(b)==e.get('bytes',e.get('stored_bytes')) and sha(b)==e.get('sha256',e.get('stored_sha256'));add(d/path)
 add(d/name);add(d/'FINAL_SEAL.json');return {'family':d.name,'manifest':name,'manifest_sha256':sha((d/name).read_bytes()),'seal_sha256':sha((d/'FINAL_SEAL.json').read_bytes()),'public_files':len(fs)}
assert git('branch','--show-current')==b'main\n'
assert subprocess.run(['git','rev-parse','-q','--verify','MERGE_HEAD'],cwd=R,capture_output=True).returncode!=0
assert not git('diff','--name-only','--diff-filter=U')
actual=json.loads((A/'ACTUAL_MERGE_VERIFICATION.json').read_bytes());assert actual['status']=='already_solved' and actual['turns']=='0/5' and actual['all_target_file_hashes_exact']==18 and actual['only_queue_pipe_cells']==[8]
post=json.loads((A/'root_postmerge_verification_receipt.json').read_bytes());assert post['status'].startswith('PASS') and post['actual_merge']==actual['actual_merge']
assert git('rev-parse','HEAD').decode().strip()==post['current_main'],'current main changed after ROOT post gate'
assert subprocess.run(['git','merge-base','--is-ancestor',actual['actual_merge'],'HEAD'],cwd=R).returncode==0
c=json.loads((A/'acceptance_criteria.json').read_bytes());assert c['workflow_completion_percent']==100 and c['post_merge_pending'] is False and c['audit_artifact_publication_pending'] is True
for p in A.iterdir():
 if p.is_file():add(p)
for name in ['snapshot','repaired_snapshot','queue_refresh_history']:
 if (A/name).exists():directory(A/name)
families=[]
for family,name in [('path_geometry_review','PUBLIC_MANIFEST.json'),('poisson_components_review','PUBLIC_MANIFEST.json'),('poisson_components_corrections','SUPPLEMENT_MANIFEST.json'),('clean_final_adversary','PUBLIC_MANIFEST.json'),('post_merge_review','PUBLIC_MANIFEST.json')]:families.append(manifest(A/family,name))
for d in A.iterdir():
 if d.is_dir() and d.name.startswith('root_') and 'streams' in d.name:directory(d)
for name in ['inventory.json','RESEARCH_LOG.md',Path(__file__).name,'root_refresh_partial_queue.py','root_integrate_reviewed_pr.py','checkpoint_365_math_allowlist.json','checkpoint_365_math_stage.stdout','checkpoint_365_math_stage.stderr','checkpoint_365_math_commit.stdout','checkpoint_365_math_commit.stderr','checkpoint_365_math_push.stdout','checkpoint_365_math_push.stderr']:
 if (P/name).exists():add(P/name)
for name in ['root_dedup_completed_private_evidence.py','ROOT_PRIVATE_EVIDENCE_DEDUP_20261003_2003.json','ROOT_PRIVATE_EVIDENCE_DEDUP_20261003_2003.jsonl']:
 add(P/name)
B=P/'audits/pr364_30004048'
for name in ['.gitignore','README.md','RESEARCH_LOG.md','snapshot_manifest.json','ROOT_PRIMARY_RECEIPTS.json','ROOT_SOURCE_FIRST_ANALYSIS.md','ROOT_CANDIDATE_ANALYTIC_ASSESSMENT.md','ROOT_TARGET_PATHS.json','root_fetch_primary.py','root_reproduce_original.py','root_original_reproduction_receipt.json','root_original_reproduction_progress.json']:
 if (B/name).is_file():add(B/name)
directory(B/'snapshot')
allow=P/'checkpoint_365_final_allowlist.json';paths.add(str(allow.relative_to(R)));allow.write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'explicit_owned_paths':sorted(paths),'families':families,'excluded':'All unlisted paths, private raw sources/API/captures/runtime material and foreign index entries; no paper/Zenodo/DOI/tracker/release'},indent=2)+'\n')
def foreign():
 result={}
 for row in git('ls-files','--stage','-z').split(b'\0'):
  if row:
   meta,p=row.split(b'\t',1)
   if p.decode() not in paths:result.setdefault(p,[]).append(meta)
 return result
original_foreign=foreign();parent=git('rev-parse','HEAD').decode().strip()
for label,args in [('stage',['git','add','--',*sorted(paths)]),('commit',['git','commit','--only','-m','Publish credited harmonic path acceptance and independent audit','--',*sorted(paths)]),('push',['git','push','origin','main'])]:
 s=subprocess.run(args,cwd=R,capture_output=True);(P/('checkpoint_365_final_'+label+'.stdout')).write_bytes(s.stdout);(P/('checkpoint_365_final_'+label+'.stderr')).write_bytes(s.stderr);assert s.returncode==0,(label,s.stderr);assert foreign()==original_foreign,'foreign index changed'
commit=git('rev-parse','HEAD').decode().strip();changed=set(git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines());assert changed<=paths
out={'status':'PUBLISHED_PR365_FINAL','commit':commit,'parent':parent,'changed_owned_paths':len(changed),'foreign_index_preserved':True,'families':families,'actual_merge':actual['actual_merge'],'completed_by_descending':json.loads((P/'inventory.json').read_bytes())['completed_by_descending']}
(P/'checkpoint_365_final_publication_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

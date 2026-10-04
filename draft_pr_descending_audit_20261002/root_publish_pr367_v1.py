"""Publish only the fully accepted PR367 preprint/audit/publication evidence.
Exact allowlist; private sources/runtime/tracker inputs and foreign index excluded.
"""
from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
import hashlib,json,subprocess
P=Path(__file__).resolve().parent;REPO=P.parent;A=P/'audits/pr367_11000151'
sha=lambda b:hashlib.sha256(b).hexdigest()
paths=set()
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO)
def add(p):
 assert p.is_file() and not p.is_symlink()
 p=p.resolve();assert p.is_relative_to(P)
 parts=p.relative_to(P).parts
 if any(x in {'tmp','raw_sources','__pycache__'} or 'private' in x for x in parts):return
 if p.name.startswith('agent_fresh_source_'):return
 assert p.suffix not in {'.png','.jpg','.jpeg','.html','.ps'}
 assert p.suffix!='.pdf' or p==A/'preprint/fixed_generator_classification.pdf'
 paths.add(p.relative_to(REPO).as_posix())
def manifest(d,name,count):
 m=json.loads((d/name).read_bytes());seen=set()
 for r in m['files']:
  q=PurePosixPath(r['path']);assert not q.is_absolute() and '..' not in q.parts and q.as_posix()==r['path'] and r['path'] not in seen
  seen.add(r['path']);p=d/q;b=p.read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256'];add(p)
 assert len(seen)==count;add(d/name)
def directory(d):
 for p in d.rglob('*'):
  if p.is_file():add(p)
def immediate(d):
 for p in d.iterdir():
  if p.is_file():add(p)
assert git('branch','--show-current')==b'main\n'
assert subprocess.run(['git','rev-parse','-q','--verify','MERGE_HEAD'],cwd=REPO,capture_output=True).returncode!=0
assert not git('diff','--name-only','--diff-filter=U').strip()
status=json.loads((A/'CURRENT_PUBLICATION_STATUS.json').read_bytes())
assert status['workflow_completion_percent']==100 and status['status']=='MERGED_PUBLISHED_AND_TRACKER_VERIFIED'
assert status['doi']=='10.5281/zenodo.23124601' and status['actual_merge']=='1d9831741c4f3ee56f590d45240a9d56559a8df2'
assert json.loads((A/'root_postmerge_scope_receipt.json').read_bytes())['status']=='PASS_ENTIRE_POSTMERGE_REPORT_AND_EVERY_FULL_CAPTURE'
assert json.loads((A/'publication/PUBLIC_RECORD_VERIFICATION.json').read_bytes())['status']=='PASS_PUBLIC_RECORD_EXACT_METADATA_AND_ALL_FILE_BYTES'
assert json.loads((A/'publication/TRACKER_COMPLETE.json').read_bytes())['updatedRange']=="'Math Puzzles'!A13:D13"
immediate(A);directory(A/'snapshot');directory(A/'repaired_snapshot');directory(A/'queue_refresh_history')
for family,count in [('group_presentations_review',40),('mapping_class_geometry_review',52),('clean_final_adversary',127)]:
 manifest(A/family,'PUBLIC_MANIFEST.json',count)
 if (A/family/'FINAL_SEAL.json').exists():add(A/family/'FINAL_SEAL.json')
for family,count in [('priority_audit',8),('preprint_review_01',14),('preprint_review_02',34)]:
 manifest(A/family,'IMMUTABLE_MANIFEST.json',count)
 if (A/family/'FINAL_SEAL.json').exists():add(A/family/'FINAL_SEAL.json')
for family,count in [('clean_final_adversary/final_live',110),('final_live_refresh_02',104),('post_merge_review',24)]:manifest(A/family,'PUBLIC_MANIFEST.json',count)
for d in A.iterdir():
 if d.is_dir() and (d.name.startswith('root_') and ('streams' in d.name or 'failed' in d.name)):directory(d)
manifest(A/'preprint/verification','MANIFEST.json',58)
for p in (A/'preprint').iterdir():
 if p.is_file():add(p)
directory(A/'publication')
for r in json.loads((A/'PUBLISHING_CLEARANCE.json').read_bytes())['sealed_submission_files']:
 b=(A/'preprint'/r['path']).read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256']
for name in ['inventory.json','RESEARCH_LOG.md','root_refresh_claimed_solved_queue.py','root_refresh_claimed_solved_queue_v1.py','root_refresh_claimed_solved_queue_v2.py','root_recover_claimed_refresh.py','root_integrate_claimed_solved_pr.py','root_compress_completed_pr374_streams.py','root_remove_completed_module_caches.py','ROOT_COMPLETED_PRIVATE_INDEX_REMOVAL_20261003.json','ROOT_COMPLETED_PRIVATE_GZIP_20261003.jsonl','ROOT_STORAGE_RECOVERY_20261003_1617.json','ROOT_COMPLETED_RUNTIME_CACHE_REMOVAL_20261003.json','ROOT_COMPLETED_RUNTIME_CACHE_REMOVAL_20261003.jsonl.gz',Path(__file__).name]:add(P/name)
allow=P/'checkpoint_pr367_published_public_allowlist.json';paths.add(allow.relative_to(REPO).as_posix())
allow.write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'scope':'PR367 complete fixed-generator accepted result, two sequential cleared preprint reviews, full exact/postmerge audit, actual Zenodo publication and one verified tracker row; descending22/349=6.3037%','explicit_owned_paths':sorted(paths),'excluded':'Every unlisted path, every private runtime/raw primary/tracker input, fresh primary PDF copies and foreign staged entries; no GitHub release'},indent=2)+'\n')
def foreign_index():
 out={}
 for row in git('ls-files','--stage','-z').split(b'\0'):
  if row:
   meta,path=row.split(b'\t',1)
   if path.decode() not in paths:out.setdefault(path,[]).append(meta)
 return out
foreign=foreign_index();parent=git('rev-parse','HEAD').decode().strip()
assert subprocess.run(['git','merge-base','--is-ancestor',status['actual_merge'],parent],cwd=REPO).returncode==0
for label,args in [('stage',['git','add','--',*sorted(paths)]),('commit',['git','commit','--only','-m','Publish audited Wajnryb quotient preprint DOI and verified tracker receipt','--',*sorted(paths)]),('push',['git','push','origin','main'])]:
 assert subprocess.run(['git','rev-parse','-q','--verify','MERGE_HEAD'],cwd=REPO,capture_output=True).returncode!=0
 r=subprocess.run(args,cwd=REPO,capture_output=True);(P/('checkpoint_pr367_published_'+label+'.stdout')).write_bytes(r.stdout);(P/('checkpoint_pr367_published_'+label+'.stderr')).write_bytes(r.stderr)
 assert r.returncode==0,(label,r.stderr);assert foreign_index()==foreign,'foreign index entries changed'
commit=git('rev-parse','HEAD').decode().strip();changed=set(git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines());assert changed<=paths
print(json.dumps({'status':'PUBLISHED_FULL_PR367_ACCEPTANCE_ZENODO_AND_TRACKER','commit':commit,'parent':parent,'changed_owned_paths':len(changed),'foreign_index_preserved':True,'doi':status['doi'],'workflow_completion_percent':100},indent=2))

"""Explicit owned source/math checkpoint; preserve every foreign index entry."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr366_2303016';paths=set();sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
def add(p):
 assert p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(P)
 assert not any('private' in x or x in {'tmp','__pycache__'} for x in p.relative_to(P).parts)
 assert p.suffix not in {'.pdf','.png','.html'}
 paths.add(p.relative_to(R).as_posix())
assert git('branch','--show-current').strip()==b'main'
assert subprocess.run(['git','rev-parse','-q','--verify','MERGE_HEAD'],cwd=R,capture_output=True).returncode!=0
assert not git('diff','--name-only','--diff-filter=U').strip()
o=json.loads((A/'root_original_reproduction_receipt.json').read_bytes());assert o['status']=='PASS' and o['check_count']==158 and o['binding_count']==48 and all(x['passed'] for x in o['checks'])
now=datetime.now(timezone.utc).isoformat()
entry=f'\n{now}: PR366 source/math/reproduction checkpoint60%. Complete fresh primary hashes, root pre-candidate mechanism seal, full21-file analytical review, actual one-turn14-file history,158 root checks/all22 Git/API bindings/all48 nested instances,2690 author+1909 historical complete byte replays PASS. Credited direct-method mathematical resolution100%; novel original theorem0%, priority certificate false. Two independent families closing; new whole adversary and current-main integration pending. Program22/349=6.3037%. No paper/Zenodo/tracker. Safe own completed-private storage recovery preserves every full stream.\n'
for p in [P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:
 with p.open('a') as f:f.write(entry)
inv=json.loads((P/'inventory.json').read_bytes());next(x for x in inv['items'] if x['number']==366).update(audit_workflow_percent=60,audit_completion_percent=60,audit_disposition='SOURCE_MATH_REPRODUCTION_PASS_FINAL_AND_LIVE_PENDING',credited_method_resolution_percent=100,novel_original_problem_resolution_claimed=False);(P/'inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
for p in A.iterdir():
 if p.is_file():add(p)
for d in [A/'snapshot',A/'root_original_streams']:
 for p in d.rglob('*'):
  if p.is_file():add(p)
for n in ['root_remove_completed_module_caches_1720.py','ROOT_COMPLETED_RUNTIME_CACHE_REMOVAL_20261003_1720.json','ROOT_COMPLETED_RUNTIME_CACHE_REMOVAL_20261003_1720.jsonl.gz','root_compress_completed_370_372_streams.py','ROOT_COMPLETED_PRIVATE_GZIP_20261003_1738.json','ROOT_COMPLETED_PRIVATE_GZIP_20261003_1738.jsonl','inventory.json','RESEARCH_LOG.md',Path(__file__).name]:add(P/n)
for n in ['CURRENT_PUBLICATION_STATUS.json','publication/GIT_PUBLICATION_RECEIPT.json']:add(P/'audits/pr367_11000151'/n)
allow=P/'checkpoint_366_source_math_allowlist.json';paths.add(allow.relative_to(R).as_posix());allow.write_text(json.dumps({'utc':now,'explicit_owned_paths':sorted(paths),'excluded':'Every unlisted or foreign index path; active family work, private sources/captures and runtimes'},indent=2)+'\n')
def foreign():
 out={}
 for row in git('ls-files','--stage','-z').split(b'\0'):
  if row:
   meta,p=row.split(b'\t',1)
   if p.decode() not in paths:out.setdefault(p,[]).append(meta)
 return out
f=foreign();parent=git('rev-parse','HEAD').decode().strip()
for label,args in [('stage',['git','add','--',*sorted(paths)]),('commit',['git','commit','--only','-m','Checkpoint direct capacity proof source-first and reproducibility audit','--',*sorted(paths)]),('push',['git','push','origin','main'])]:
 r=subprocess.run(args,cwd=R,capture_output=True);(P/('checkpoint_366_source_math_'+label+'.stdout')).write_bytes(r.stdout);(P/('checkpoint_366_source_math_'+label+'.stderr')).write_bytes(r.stderr);assert r.returncode==0,(label,r.stderr);assert foreign()==f,'foreign index changed'
c=git('rev-parse','HEAD').decode().strip();changed=set(git('diff-tree','--no-commit-id','--name-only','-r',c).decode().splitlines());assert changed<=paths
print(json.dumps({'status':'PUBLISHED_PR366_SOURCE_MATH60','commit':c,'parent':parent,'changed_owned_paths':len(changed),'foreign_index_preserved':True},indent=2))

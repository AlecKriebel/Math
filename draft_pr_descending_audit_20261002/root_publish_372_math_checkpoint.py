"""Publish an explicit PR372 mathematical checkpoint without foreign staging."""
from pathlib import Path
import datetime,hashlib,json,subprocess
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr372_9700034';paths=set();sha=lambda b:hashlib.sha256(b).hexdigest()
def add(p):
 p=p.resolve();assert p.is_relative_to(P) and p.is_file();assert not any(x in p.parts for x in ['tmp','private','private_live','raw_sources','__pycache__']);assert p.suffix not in ['.pdf','.png','.jpg','.html'];paths.add(str(p.relative_to(R)))
for p in A.iterdir():
 if p.is_file():add(p)
for family in ['measure_tail_review','metric_moments_review','geometric_capture_review']:
 D=A/family;mp=D/'PUBLIC_MANIFEST.json';m=json.loads(mp.read_bytes());add(mp)
 for f in m['files']:
  p=D/f['path'];b=p.read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256'];add(p)
for f in json.loads((A/'snapshot_manifest.json').read_bytes())['files']:
 p=A/'snapshot'/f['path'];b=p.read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256'];add(p)
for folder in ['root_original_streams','root_family_streams']:
 for p in (A/folder).iterdir():assert p.is_file() and p.suffix in ['.stdout','.stderr'];add(p)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (A/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+now+' — Checkpoint80% audit,0% general discovery. Full five-turn root reconstruction/source correction addendum sealed; all503419 author/2507 old-review assertions11 complete original runs,116 manifest instances/49original paths/38actualWIP files reproduced. Three independent source-first families agree at partial scopes;39 public bindings,15 full author stream comparisons and37212 new controls independently reproduced by root. Fresh whole reviewer mathematics agrees; exact-live administrative guard repairs and current-main refresh still pending.\n')
with (P/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+now+' — PR372 mathematical checkpoint80%; unsolved target0% full-resolution estimate. Descending acceptance16/349=4.5845%. Publish own complete proof/code/reproduction and three independent family packages; fresh exact-live gate remains pending.\n')
p=P/'inventory.json';q=json.loads(p.read_bytes())
def update(obj):
 if isinstance(obj,dict):
  if str(obj.get('number',obj.get('pr','')))=='372':obj.update({'audit_completion_percent':80,'audit_disposition':'SCOPED_MATHEMATICS_VALID_REPRODUCED_LIVE_GATE_PENDING','general_discovery_completion_percent':0})
  for v in obj.values():update(v)
 elif isinstance(obj,list):
  for v in obj:update(v)
update(q);p.write_text(json.dumps(q,indent=2)+'\n')
for name in ['inventory.json','RESEARCH_LOG.md',Path(__file__).name]:add(P/name)
report=P/'checkpoint_372_math_public_allowlist.json';paths.add(str(report.relative_to(R)));report.write_text(json.dumps({'utc':now,'checkpoint':'PR372 source-first mathematical audit80%; actual final live acceptance pending','explicit_owned_paths':sorted(paths),'excluded':'Raw sources, extracts, renders, temporary/private clones, all unlisted and foreign paths','audit_percent':80,'general_discovery_percent':0,'program_completed':16,'program_total':349},indent=2)+'\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def indexmap():
 out={}
 for x in git('ls-files','--stage','-z').split(b'\0'):
  if x:
   meta,path=x.split(b'\t',1);out.setdefault(path,[]).append(meta)
 return out
initial=indexmap();foreign={k:v for k,v in initial.items() if k.decode() not in paths};parent=git('rev-parse','HEAD').decode().strip();assert git('branch','--show-current').decode().strip()=='main'
for label,cmd in [('stage',['git','add','--',*sorted(paths)]),('commit',['git','commit','--only','-m','Publish PR372 independently verified mathematics and three adversarial families','--',*sorted(paths)])]:
 r=subprocess.run(cmd,cwd=R,capture_output=True);(P/f'checkpoint_372_math_{label}.stdout').write_bytes(r.stdout);(P/f'checkpoint_372_math_{label}.stderr').write_bytes(r.stderr);assert r.returncode==0,r.stderr
commit=git('rev-parse','HEAD').decode().strip();changed=set(git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines());assert changed<=paths
assert {k:v for k,v in indexmap().items() if k.decode() not in paths}==foreign,'foreign index changed'
r=subprocess.run(['git','push','origin','main'],cwd=R,capture_output=True);(P/'checkpoint_372_math_push.stdout').write_bytes(r.stdout);(P/'checkpoint_372_math_push.stderr').write_bytes(r.stderr);assert r.returncode==0,r.stderr
print(json.dumps({'status':'PUBLISHED_EXPLICIT_OWN_MATH_CHECKPOINT','commit':commit,'parent':parent,'changed_owned_paths':len(changed),'foreign_index_unchanged':True,'audit_percent':80,'general_discovery_percent':0}))

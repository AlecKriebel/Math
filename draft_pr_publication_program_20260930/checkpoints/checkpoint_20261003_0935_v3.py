"""Checkpoint completed owned findings, preserving concurrent foreign work."""
from pathlib import Path
import datetime as dt, hashlib, json, os, stat, subprocess
P=Path(__file__).absolute().parents[1]; R=P.parent
A={n:P/'audits'/s for n,s in [(45,'pr45_9900007'),(46,'pr46_30004438'),(47,'pr47_2849'),(48,'pr48_2961'),(49,'pr49_30000703'),(50,'pr50_10600042')]}
names=set()
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
def add(p):
 assert not p.is_symlink() and all(not q.is_symlink() for q in p.parents)
 assert stat.S_ISREG(p.stat().st_mode) and p.stat().st_size<100*1024*1024
 if p.suffix.lower()=='.sqlite':
  assert p.name=='catalog.sqlite' and p.read_bytes()==b'private\n' and 'fixtures_20261003T045907.597040Z' in p.parts
 else:assert p.suffix.lower() not in {'.db','.pdf','.png','.jpg','.jpeg','.gif','.webp'}
 names.add(p.relative_to(R).as_posix())
def tree(d):
 for p in d.rglob('*'):
  assert not p.is_symlink()
  if p.is_file():add(p)
def closed(d,n,h):
 b=(d/n).read_bytes();assert sha(b)==h;m=json.loads(b)
 rows=m['files'];assert len(rows)==m['files_count']
 for z in rows:
  q=d/z['path'];b=q.read_bytes()
  assert len(b)==z['bytes'] and sha(b)==z['sha256'] and stat.S_IMODE(q.stat().st_mode)==0o444
  add(q)
 add(d/n)
assert __debug__ and git('branch','--show-current')==b'main\n' and not git('diff','--cached','--name-only')
head=git('rev-parse','HEAD').decode().strip()
post=json.loads((A[46]/'ROOT_ACTUAL_POST_INSPECTION.json').read_bytes())
assert post['status']=='PASS' and post['completed_primary_prs']==36 and len(post)==22
for z in post['current13']:
 q=R/z['path'];b=q.read_bytes()
 assert stat.S_IMODE(q.stat().st_mode)==z['worktree_mode']==0o644
 if z['path']=='unsolved_math_prioritization/QUEUE.md':
  assert git('show','HEAD:'+z['path'])==b
 else:assert len(b)==z['bytes'] and sha(b)==z['sha256']
assert subprocess.run(['git','merge-base','--is-ancestor',post['entire_post']['merge_commit'],head],cwd=R).returncode==0
assert json.loads((P/'inventory.json').read_bytes())['completed_count']==36
tree(A[46])
for n,folder,mf,h in [
 (47,'acceptance_source_adversary_family','SELF_MANIFEST.json','a4c15b8bc831c71b61e0b6d830904813519eab147d1c7bd1d96987b2e98c0222'),
 (48,'acceptance_preparation_family','PREPARATION_MANIFEST.json','2f5e572078066a5a895ac813e813106b140f4cc3beabd38f488b7633d07b9c86'),
 (48,'acceptance_source_adversary_family','SELF_MANIFEST.json','e32146a5f566158b30de3b403184e38067f4628a924c11748e43a28e514b35f6'),
 (49,'reviewed_candidate','MANIFEST.json','8ca8820e1e1493391224ea8f93dde859bd9b3f6316c41763e86433dc85a1fa47'),
 (49,'current_whole_adversary_family','SELF_MANIFEST.json','b3d91982e7a2cfbda0ffce7fe0e45141dabafcb374aecd52078ad3d66a1e9736'),
 (50,'classical_markov_adversary_family','MANIFEST.json','8104131acb399550c9dd96ae140b2dc911d8197d7c473c2605fb75db23c4e436')]:closed(A[n]/folder,mf,h)
vm=A[50]/'virtual_markov_priority_adversary_family'
assert sha((vm/'SELF_ONLY_CLOSURE.json').read_bytes())=='3e17bb22f337a64f7cee81c74c0fa84b34df88bfcd60cc82c9b941e6e2e612dd'
tree(vm)
for n in (47,48,49):
 for p in A[n].iterdir():
  if p.is_file() and p.name.startswith('ROOT_'):add(p)
for folder in ('root_current_prerequisite_Git_actual_captures','tmp'):
 q=A[49]/folder
 if q.exists():tree(q)
for p in A[50].iterdir():
 if p.is_file():add(p)
for folder in ('original','captures','priority_adversary_family','preprint_v1'):tree(A[50]/folder)
for p in A[45].iterdir():
 if p.is_dir() and (p/'CAPTURE.json').exists():
  c=json.loads((p/'CAPTURE.json').read_bytes())
  if c.get('schema')=='root-explicit-command-capture/v1' and c.get('started_utc','')>='2026-10-03T08:09:03':
   assert c['completed'] is True and c['actual_execution'] is True and c['operator_unchanged'] is True
   for k in ('stdout','stderr'):
    b=(p/c[k]['path']).read_bytes();assert len(b)==c[k]['bytes'] and sha(b)==c[k]['sha256']
   tree(p)
for n in ['draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl']:add(R/n)
tree(R/'unsolved_math_prioritization/attempts/30004438')
utc=dt.datetime.now(dt.timezone.utc).isoformat()
note=('\n'+utc+' — Checkpoint36/180=20%, next47. PR46 merged eb3c6dbe6a1d978e39c30518137264bdc69ec30b; all six actual acceptance phases and native mirror passed. ROOT complete post7933 PASS; entire22-key record17777f55... and separate dated foreign readback1e9bf1dd... personally fully read. Later PR373 foreign log append after actual post is explicitly qualified; no live-unchanged claim or foreign rewrite. Native37targets44turns36primaries and original0/5+response1; credited Kozhasov–Kummer known theorem, no paper/DOI/tracker. PR47 SOURCE adversary85+self actual78280 closure/81503 readback passed; earlier mistyped-hash81281 failure retained. Restricted0644/0022 runtime authority preparation pending; no general mode-writer approval. PR48 SOURCE121+self actual76301/78175 closed; new independent adverse45+self actual4313/4558 closed correction-bearing: M1 atomic replacement fails0600 mode preservation, robust V2 repair pending. Science remains valid UNSOLVED shared2/5 partial. PR49 current1544/deps1407 and new WHOLE127+self actual267 close/755 readback passed; prior82903 mutable-dated-body closure failure and444 wrong-hash readback retained. Exactly3083 fixed+4 dated native observations+failed5 custody corrected; credited2007 reflection theorem already_solved0/5, no new result. PR50 original15 fully read/reproduced; independent classical and virtual universal derivations passed, actual closed34/27 families; bounded priority7-file review found Fiedler comparison and9–61 pagination repairs, applied throughout new preprint_v1. New standalone note and standard-library7106-check support completed, fresh different preprint adversary active, no publication approval. Preliminary native compilation succeeded; final-source compile/PDF visual check pending. Disk ENOSPC before helper launch resolved by pip regenerable download-cache purge1045.3MB; no research/installed-package/history deletion. Original budgets unchanged/new0/audit0; publication/discovery novelty unestablished for50. Active47ROOT/48V2/49SOURCE/50freshpaper/51original preparation excluded; stable19-file author draft preserved as explicitly unpublished. Goal active, no release/outside outreach. Acceptance20%,46workflow100%,47acceptance70%,48repairedsource0%,49current100%,50packagepreparation100%/publication0%.\n')
for p in [P/'RESEARCH_LOG.md',*[A[n]/'ROOT_RESEARCH_LOG.md' for n in (46,47,48,49,50)]]:
 with p.open('a') as f:f.write(note);f.flush();os.fsync(f.fileno())
 add(p)
for n in ('checkpoint_20261003_0935.py','checkpoint_20261003_0935_v2.py','checkpoint_20261003_0935_v3.py'):add(Path(__file__).with_name(n))
foreign=[]
for n in git('diff','--name-only','-z').decode().split('\0'):
 if n and n not in names:
  p=R/n;b=p.read_bytes();foreign.append(dict(path=n,bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(p.stat().st_mode)))
rows=[]
for n in sorted(names):
 p=R/n;b=p.read_bytes();rows.append(dict(path=n,bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(p.stat().st_mode)))
C=P/'checkpoints/CHECKPOINT_20261003_0935.json'
with C.open('x') as f:json.dump(dict(schema='ROOT_completed_owned_checkpoint/v4',utc=utc,actual_pid=os.getpid(),main_before=head,owned_files=rows,foreign_tracked_dirty=foreign,active_families_included=False,completed36of180_percent=20.0,current_pr=47,post46_current13_is_dated=True,later_other_program_QUEUE_commit_preserved=True,current_QUEUE_sha256=sha((R/'unsolved_math_prioritization/QUEUE.md').read_bytes()),QUEUE_staged_by_this_checkpoint=False,future_acceptance_approved=False),f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
add(C)
assert git('rev-parse','HEAD').decode().strip()==head and not git('diff','--cached','--name-only')
subprocess.run(['git','add','-f','--pathspec-from-file=-','--pathspec-file-nul'],cwd=R,input=b''.join(n.encode()+b'\0' for n in sorted(names)),check=True)
staged={n for n in git('diff','--cached','--name-only','-z').decode().split('\0') if n}
assert staged<=names and not staged&{z['path'] for z in foreign}
for n in staged:assert git('show',':'+n)==(R/n).read_bytes(),n
for z in foreign:
 p=R/z['path'];b=p.read_bytes();assert len(b)==z['bytes'] and sha(b)==z['sha256'] and stat.S_IMODE(p.stat().st_mode)==z['full_mode']
print(json.dumps(dict(status='PASS_EXACT_COMPLETED_OWNED_STAGE',actual_pid=os.getpid(),main_before=head,owned_files=len(names),staged_files=len(staged),foreign_preserved=len(foreign),completed_count=36,completion_percent=20.0)))

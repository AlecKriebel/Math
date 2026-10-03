"""Publish completed first-party PR46-48 reviews; exclude all active and foreign work."""
from pathlib import Path,PurePosixPath
import datetime as dt,hashlib,json,os,stat,subprocess
P=Path(__file__).absolute().parents[1];R=P.parent;A45=P/'audits/pr45_9900007';A46=P/'audits/pr46_30004438';A47=P/'audits/pr47_2849';A48=P/'audits/pr48_2961';names=set()
assert __debug__
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def add(p):
 assert not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode) and p.stat().st_size<100*1024*1024
 assert p.suffix.lower() not in {'.pdf','.png','.jpg','.jpeg','.webp','.gif','.db','.sqlite'}
 names.add(p.relative_to(R).as_posix())
def closed(d,n,expected):
 b=(d/n).read_bytes();assert sha(b)==expected;m=json.loads(b)
 for row in m['files']:
  p=d/row['path'];body=p.read_bytes();assert len(body)==row['bytes'] and sha(body)==row['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444
  add(p)
 add(d/n)
def capture(d):
 c=json.loads((d/'CAPTURE.json').read_bytes());assert c['completed'] is True and c['actual_execution'] is True and type(c['exit_code']) is int and c['operator_unchanged'] is True
 assert {p.name for p in d.iterdir()}=={'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'}
 for k in ['stdout','stderr']:
  b=(d/c[k]['path']).read_bytes();assert len(b)==c[k]['bytes'] and sha(b)==c[k]['sha256']
 for p in d.iterdir():add(p)
assert git('branch','--show-current')==b'main\n' and not git('diff','--cached','--name-only')
head=git('rev-parse','HEAD').decode().strip()
for d,n,h in [(A46/'current_whole_adversary_family','MANIFEST.json','be3fa099c6a080d5f9cddcf42f39ac51b51c8f89cd76d09fb5d360a99d1990e2'),(A47/'current_source_adversary_family','SELF_MANIFEST.json','ed0aba6a7a42e752012399daed24d460e25108afd7b66c89ee1907473eb76a85'),(A48/'smooth_geometry_family','MANIFEST.json','7248e58e1a86cc6aa574233826d5d8b645858917ab7c94836091d74235a3bdef'),(A48/'algebra_cocycle_family','MANIFEST.json','127120bc00894444c01d44b49739685f03f229361a10568f1aec4f52c001dcd3'),(A48/'root_original_actual_reproduction_v2','MANIFEST.json','f4d8a828e659c5f233053fb3309c38c8d3fe1c90520d6abef2d73b30df7776e9')]:closed(d,n,h)
for a in [A46,A47,A48]:
 for p in a.iterdir():
  if p.is_file() and (p.name.startswith('ROOT_') or p.name.startswith(('author_ROOT_whole_review','reproduce_original_ROOT','audit_raw_provenance_ROOT','close_ROOT_reproduction','verify_ROOT_reproduction'))):add(p)
# ROOT alone generated this failed V1 subtree, before any helper ran; preserve all191 original members.
for p in (A48/'root_original_actual_reproduction').rglob('*'):
 assert not p.is_symlink()
 if p.is_file():add(p)
for p in A45.iterdir():
 if p.is_dir() and (p.name.startswith(('root_pr46_whole','root_pr47_adverse_source','root_pr48_')) or p.name in {'root_checkpoint_0524_commit_actual_capture','root_checkpoint_0524_push_actual_capture','root_checkpoint_0524_reconciliation_v4_actual_capture'}):capture(p)
for p in (P/'checkpoints').iterdir():
 if p.is_file():add(p)
utc=dt.datetime.now(dt.timezone.utc).isoformat()
note='\n'+utc+' — Completed mathematical evidence checkpoint:35/180=19.444444444444446%, current46. PR46 WHOLE clean known-result verdict:245+self/49dirs MFbe3fa099..., genuine ROOTclosing10245/readback10633, adjacent ROOTfullrecord14371 binds all245first-party+1877external bodies (1946historicalrows includes69own644→444 closure modes). Entire target credited Kozhasov–Kummer2020, already_solved0/5 plus1source-verification response,new0audit0; acceptance SOURCE active, no future merge authority. Failed ROOTrecord13237 preserved, corrected V2 succeeds. PR47 ADVERSE SOURCE81+self/15dirs MFed0aba6... ROOT12168/readback13238, exactly one repairable line150 null-Git capture-class defect; all mathematical partial checks valid UNSOLVED1/5; distinct V2 source repair active, no production freeze. PR48 independent algebra489+self/95dirs/85captures ROOT20740/readback20855 MF127120bc... passespartial; smooth268+self/50dirs ROOT15467/readback16307 MF7248e58e... passespartial. ROOTfull38Git+4helpers11716 reproduces historical6570/duplicate6570/final6570/independent228; genuine old/final note changes include humanpeerreviewdisclosure and finalreceiptchangesonlypartialSHA. Failed ROOT3042 old-history assumption/source/captures retained. ROOT16308 independently reads149266659rawbytes/all15458typedSQL; both targetreportkeysABSENT/fallback{}nopriorfile. ROOTclosed254+self/53dirs19105/readback19580 MFf4d8a828... strongpartialambientcl(f×id_S2)≤4 onlyincludedsubgroup; fullKP4.85 unresolved and exactduplicate30004403 shared2/5,new0audit0; SOURCEcurrent repair active for null/stale-review/history qualification. No newpaperDOItrackerreleaseoroutreach. Active families, all foreign PDF/OCR/pixels/rawSQL/cache bodies and other chat state/index excluded; shared descendantmain preserved.\n'
for p in [P/'RESEARCH_LOG.md',A46/'ROOT_RESEARCH_LOG.md',A47/'ROOT_RESEARCH_LOG.md',A48/'ROOT_RESEARCH_LOG.md']:
 with p.open('a') as f:f.write(note);f.flush();os.fsync(f.fileno())
 add(p)
foreign=[]
for n in git('diff','--name-only','-z').decode().split('\0'):
 if n and n not in names:
  p=R/n;b=p.read_bytes();foreign.append(dict(path=n,bytes=len(b),sha256=sha(b)))
rows=[]
for n in sorted(names):
 p=R/n;b=p.read_bytes();rows.append(dict(path=n,bytes=len(b),sha256=sha(b),observed_full_mode=stat.S_IMODE(p.stat().st_mode)))
C=P/'checkpoints/CHECKPOINT_20261003_0600.json'
with C.open('x') as f:json.dump(dict(schema='ROOT_exact_completed_owned_checkpoint/v3',utc=utc,actual_pid=os.getpid(),main_before=head,owned_files=rows,foreign_dirty_before=foreign,foreign_bodies_included=False,active_families_included=False,completed_count=35,current_pr=46,total=180,completion_estimate_percent=35/180*100),f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
add(C)
assert git('rev-parse','HEAD').decode().strip()==head
subprocess.run(['git','add','-f','--pathspec-from-file=-','--pathspec-file-nul'],cwd=R,input=b''.join(n.encode()+b'\0' for n in sorted(names)),check=True)
staged={n for n in git('diff','--cached','--name-only','-z').decode().split('\0') if n}
assert staged<=names and not staged&{r['path'] for r in foreign}
for n in staged:
 assert git('show',':'+n)==(R/n).read_bytes(),n
print(json.dumps(dict(status='PASS_EXACT_COMPLETED_FIRST_PARTY_STAGE',actual_pid=os.getpid(),main_before=head,owned_files=len(names),staged_files=len(staged),foreign_tracked_dirty=len(foreign),completed=35,current=46,future_acceptance_approved=False)))

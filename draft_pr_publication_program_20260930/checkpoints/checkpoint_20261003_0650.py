"""Publish completed first-party PR46-49 audits; exclude active and foreign work."""
from pathlib import Path,PurePosixPath
import datetime as dt,hashlib,json,os,stat,subprocess
P=Path(__file__).absolute().parents[1];R=P.parent;A45=P/'audits/pr45_9900007';A46=P/'audits/pr46_30004438';A47=P/'audits/pr47_2849';A48=P/'audits/pr48_2961';A49=P/'audits/pr49_30000703';names=set()
assert __debug__
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def add(p):
 assert not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode) and p.stat().st_size<100*1024*1024
 assert p.suffix.lower() not in {'.pdf','.png','.jpg','.jpeg','.webp','.gif','.db','.sqlite'}
 names.add(p.relative_to(R).as_posix())
def closed(d,n,expected):
 b=(d/n).read_bytes();assert sha(b)==expected;m=json.loads(b)
 members=m.get('files',m.get('members',m.get('payload_files')));assert type(members) is list
 for row in members:
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
for d,n,h in [(A46/'acceptance_preparation_family','PREPARATION_MANIFEST.json','d97fb190b4b20a2566a1415130e4b7729cb1f8377f8b823e0fd0b263a3315dab'),(A47/'current_preparation_family_v2','PREPARATION_MANIFEST.json','da314f40d628606f8e80cc198c3ab4a94b71554e929f70c63fce31cc195def10'),(A47/'current_source_adversary_family_v2','SELF_MANIFEST.json','3312457f63a076a55974e94fc8cd6a93e860007e33b992dd3546a418f1170524'),(A47/'reviewed_candidate','MANIFEST.json','a7d1acc9dbbf8cd5435d0bebd8f6b1a540ecb0f2aea8d0c616c46bc5bf6b4ea5'),(A48/'current_preparation_family','PREPARATION_MANIFEST.json','ee165341f8980110f1362a19c27f697db6df2e68eac01cc110a31c8d08ee9640'),(A49,'ORIGINAL_PREPARATION_MANIFEST.json','2eecad772938f3b220936c3317f1266d9a98de0f9d9750a6efa725c665f63b4c'),(A49/'boundary_analysis_family','MANIFEST.json','24543fa2de740787f3374e958cca7dc170ab92797f0c42f94b0b3c3f71fa756e'),(A49/'hyperbolic_geometry_family','SELF_MANIFEST.json','07650b4164489112dbeb4668f9c08d9e87944a5d948c1dd33aa7549e42b239c6'),(A49/'root_original_actual_reproduction','MANIFEST.json','6a0f39d01777401d85df104be5ba1489f107cf8707dc5151fdc6ebaff2d26796')]:closed(d,n,h)
for a in [A46,A47,A48,A49]:
 for p in a.iterdir():
  if p.is_file() and (p.name.startswith('ROOT_') or p.name.startswith(('author_ROOT','reproduce_original_ROOT','audit_raw_provenance_ROOT','close_ROOT_reproduction','verify_ROOT_reproduction','inspect_ROOT_actual_current_freeze'))):add(p)
for d in [A47/'root_current_prerequisite_Git_actual_captures',A47/'tmp/root_pr47_current_outer_20261003T063156.236399Z',A47/'tmp/root_pr47_current_build_20261003T063156.293697Z']:
 for p in d.rglob('*'):
  assert not p.is_symlink()
  if p.is_file():add(p)
for p in A45.iterdir():
 if p.is_dir() and (p/'CAPTURE.json').is_file():
  c=json.loads((p/'CAPTURE.json').read_bytes())
  if c.get('schema')=='root-explicit-command-capture/v1' and c.get('started_utc','')>='2026-10-03T06:00:00':capture(p)
for p in (P/'checkpoints').iterdir():
 if p.is_file():add(p)
utc=dt.datetime.now(dt.timezone.utc).isoformat()
note='\n'+utc+' — Completed review checkpoint:35/180=19.444444444444446%, current46. PR46 acceptance SOURCE V1 166+self MFd97fb190... genuinely closed41857/read47451; independent SOURCE adversary has confirmed repairable protected program-log append contradiction, full adverse closure pending, distinct V2 repair active. No mathematical defect or acceptance yet. PR47 corrected SOURCE V2 139+self MFda314f40... ROOT32176/read32684; different clean SOURCE263+self/93dirs MF3312457... ROOT48213/read48451 full149840controls. Genuine ROOTfive author53137 dated main e491808c..., actualcurrentoperator53866/builder53867 froze1328+self/282dirs MFa7d1acc9..., original final49 actualGit versus frozen47prefix, ROOTfull1422dependencies and allpacket readback56799 passed. Initial ROOT56454 inspector mistaken printed-field assumption retained; no production defect. New different WHOLE review active, no native acceptance. PR48 currentSOURCE55+self MF ee165341... ROOT50088/read50493, fullreport/builder/operator/contract personally read, independentSOURCEadversary active; math UNSOLVEDduplicate2961/30004403 shared2/5. PR49 original350+self/63dirs MF2eecad77... ROOT48827/read49240, boundary473+self/92inclroot MF24543fa... ROOT54633/read55199, geometry107+self/15dirs MF07650b41... ROOT58282/read58412; both independently support credited2007 unrestricted reflection criterion, knownresult already_solved0/5 no novel discovery. ROOTfull16/9JSONvalues/primaryOWR-v1-publishertext, both universal proofs, actual33Git and unchanged69/duplicate69/187 child60012 passed. ROOTraw62744 reads149266659bytes/all15458 literal SQL+types+every original row witness; two own raw comparison failures60964schema/61299order retained with distinct V3 success. ROOT reproduction192+self/39dirs MF6a0f39d0... actual64641/read64976, complete result/raw/notes/externalbindings. No separate original source-response counter is invented. Exactfull2007journal proof remains credited import, no false full-proof/PDFpixel authentication by ROOT. PR49 currentSOURCE preparation active. New paper/DOI/tracker/release/outside communication0; activefamilies and foreign raw/SQL/PDF/OCR/pixels/state/index excluded. Concurrent descendantmain preserved; these dated checkpoints confer no future merge authority.\n'
for p in [P/'RESEARCH_LOG.md',A46/'ROOT_RESEARCH_LOG.md',A47/'ROOT_RESEARCH_LOG.md',A48/'ROOT_RESEARCH_LOG.md',A49/'ROOT_RESEARCH_LOG.md']:
 with p.open('a') as f:f.write(note);f.flush();os.fsync(f.fileno())
 add(p)
foreign=[]
for n in git('diff','--name-only','-z').decode().split('\0'):
 if n and n not in names:
  p=R/n;b=p.read_bytes();foreign.append(dict(path=n,bytes=len(b),sha256=sha(b)))
rows=[]
for n in sorted(names):
 p=R/n;b=p.read_bytes();rows.append(dict(path=n,bytes=len(b),sha256=sha(b),observed_full_mode=stat.S_IMODE(p.stat().st_mode)))
C=P/'checkpoints/CHECKPOINT_20261003_0650.json'
with C.open('x') as f:json.dump(dict(schema='ROOT_exact_completed_owned_checkpoint/v3',utc=utc,actual_pid=os.getpid(),main_before=head,owned_files=rows,foreign_dirty_before=foreign,foreign_bodies_included=False,active_families_included=False,completed_count=35,current_pr=46,total=180,completion_estimate_percent=35/180*100),f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
add(C)
assert git('rev-parse','HEAD').decode().strip()==head
subprocess.run(['git','add','-f','--pathspec-from-file=-','--pathspec-file-nul'],cwd=R,input=b''.join(n.encode()+b'\0' for n in sorted(names)),check=True)
staged={n for n in git('diff','--cached','--name-only','-z').decode().split('\0') if n}
assert staged<=names and not staged&{r['path'] for r in foreign}
for n in staged:
 assert git('show',':'+n)==(R/n).read_bytes(),n
print(json.dumps(dict(status='PASS_EXACT_COMPLETED_FIRST_PARTY_STAGE',actual_pid=os.getpid(),main_before=head,owned_files=len(names),staged_files=len(staged),foreign_tracked_dirty=len(foreign),completed=35,current=46,future_acceptance_approved=False)))

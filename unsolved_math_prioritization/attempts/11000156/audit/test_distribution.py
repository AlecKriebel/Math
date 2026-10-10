#!/usr/bin/env python3
"""Independent non-root read-only replay and pinned-mutation tests."""
from pathlib import Path
import hashlib,json,os,shutil,stat,subprocess,sys,tarfile,tempfile
BASE=Path(__file__).resolve().parent; ORIGINAL=BASE.parent/'boundary_twist_11000156'
ARCHIVE_SHA='3f8104fcf841db20f90769427c0a218971bf5a542c5d24a9747a5c931f28da06'
MANIFEST_SHA='913c3e9341eb863e7906d234707bf92188bd78f7af8a4833d1ee47b859c8a077'
BOOTSTRAP_SHA='dcc50e895d0373014bc9098742b4c20bb090753958b1bc338c244f32003c03b1'
def require(v,m):
 if not v:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def emit(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def run(args):return subprocess.run([sys.executable,'-B',*args],capture_output=True,text=True,timeout=40,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
def snapshot(root):return {str(p.relative_to(root)):sha(p) for p in root.rglob('*') if p.is_file()}
def readonly(root):
 for p in root.rglob('*'):p.chmod(0o555 if p.is_dir() else 0o444)
 root.chmod(0o555)
def remove(root):
 for p in root.rglob('*'):
  if p.is_dir() and not p.is_symlink():p.chmod(0o755)
 root.chmod(0o755);shutil.rmtree(root)
def mutate_manifest(d,f):
 p=d/'FREEZE_MANIFEST.json';x=json.loads(p.read_text());f(x);p.write_text(json.dumps(x))
def repin_file(d,name):
 p=d/'packet'/name;mutate_manifest(d,lambda x:x['files'].__setitem__(name,{'bytes':p.stat().st_size,'sha256':sha(p)}))
def status(d,field,value):
 p=d/'packet/STATUS.json';x=json.loads(p.read_text());x[field]=value;p.write_text(json.dumps(x));repin_file(d,'STATUS.json')
def replacement(d,name,kind):
 p=d/'packet'/name;p.unlink()
 if kind=='link':p.symlink_to(ORIGINAL/'packet'/name)
 elif kind=='fifo':os.mkfifo(p)
 elif kind=='dir':p.mkdir()

def exact(root):
 require(os.geteuid()!=0,'must not run as root')
 before=snapshot(root); results=[];denials=[]
 for flags in [[],['-O'],['-OO']]:
  p=run([*flags,str(root/'bootstrap.py'),str(root/'packet')]);require(p.returncode==0,p.stderr)
  results.append(json.loads(p.stdout))
 for p,mode in [(root/'packet/REPORT.md','ab'),(root/'packet/forbidden-create','wb'),(root/'FREEZE_MANIFEST.json','ab'),(root/'forbidden-create','wb')]:
  try:
   with p.open(mode):pass
  except PermissionError:denials.append(str(p.relative_to(root)))
  else:raise ValueError('read-only operation unexpectedly allowed')
 require(snapshot(root)==before,'distribution changed during replay')
 return {'modes':results,'read_only_denials':denials,'uid':os.geteuid(),'unchanged':True,'packet_permissions':oct((root/'packet').stat().st_mode&0o777),'distribution_permissions':oct(root.stat().st_mode&0o777)}

def hostile(root):
 pins=json.loads((root/'BOOTSTRAP_PINS.json').read_text());results=[]
 def rehash_report(d):
  (d/'packet/REPORT.md').write_text('authored mutation test');repin_file(d,'REPORT.md')
 def duplicate_status(d):
  p=d/'packet/STATUS.json';s=p.read_text().replace('"problem_id": 11000156,','"problem_id": 11000156, "problem_id": 11000156,');p.write_text(s);repin_file(d,'STATUS.json')
 cases=[
 ('changed report',lambda d:(d/'packet/REPORT.md').write_text('changed'),False),
 ('extra file',lambda d:(d/'packet/extra.txt').write_text('extra'),False),
 ('missing file',lambda d:(d/'packet/STATUS.json').unlink(),False),
 ('symlink member',lambda d:replacement(d,'REPORT.md','link'),False),
 ('FIFO member',lambda d:replacement(d,'REPORT.md','fifo'),False),
 ('directory member',lambda d:replacement(d,'REPORT.md','dir'),False),
 ('oversize actual file',lambda d:(d/'packet/REPORT.md').write_bytes(b'x'*2000001),False),
 ('verifier substitution',lambda d:(d/'packet/verify.py').write_text('print("fake")'),False),
 ('changed data and rehashed manifest',rehash_report,False),
 ('malformed JSON',lambda d:(d/'FREEZE_MANIFEST.json').write_text('{'),True),
 ('duplicate manifest keys',lambda d:(d/'FREEZE_MANIFEST.json').write_text('{"schema":"x","schema":"x","files":{}}'),True),
 ('unexpected schema',lambda d:mutate_manifest(d,lambda x:x.__setitem__('schema','other')),True),
 ('wrong top-level type',lambda d:(d/'FREEZE_MANIFEST.json').write_text('[]'),True),
 ('wrong files type',lambda d:mutate_manifest(d,lambda x:x.__setitem__('files',[])),True),
 ('empty file map',lambda d:mutate_manifest(d,lambda x:x.__setitem__('files',{})),True),
 ('traversal path',lambda d:mutate_manifest(d,lambda x:x['files'].__setitem__('../out',{'bytes':0,'sha256':'0'*64})),True),
 ('absolute path',lambda d:mutate_manifest(d,lambda x:x['files'].__setitem__('/tmp/out',{'bytes':0,'sha256':'0'*64})),True),
 ('boolean byte count',lambda d:mutate_manifest(d,lambda x:x['files']['REPORT.md'].__setitem__('bytes',True)),True),
 ('negative byte count',lambda d:mutate_manifest(d,lambda x:x['files']['REPORT.md'].__setitem__('bytes',-1)),True),
 ('oversize byte count',lambda d:mutate_manifest(d,lambda x:x['files']['REPORT.md'].__setitem__('bytes',2000001)),True),
 ('float byte count',lambda d:mutate_manifest(d,lambda x:x['files']['REPORT.md'].__setitem__('bytes',13413.0)),True),
 ('wrong digest type',lambda d:mutate_manifest(d,lambda x:x['files']['REPORT.md'].__setitem__('sha256',{})),True),
 ('uppercase digest',lambda d:mutate_manifest(d,lambda x:x['files']['REPORT.md'].__setitem__('sha256','A'*64)),True),
 ('extra record field',lambda d:mutate_manifest(d,lambda x:x['files']['REPORT.md'].__setitem__('extra',1)),True),
 ('code string',lambda d:(d/'FREEZE_MANIFEST.json').write_text('__import__("os").system("false")'),True),
 ('duplicate status keys',duplicate_status,True),
 ('wrong problem scope',lambda d:status(d,'problem_id',11000157),True),
 ('wrong turns',lambda d:status(d,'turns',4),True),
 ('false solved claim',lambda d:status(d,'main_problem_resolved',True),True),
 ('false formal certification',lambda d:status(d,'formal_certification',True),True),
 ]
 for flags in [[],['-O'],['-OO']]:
  for name,mutator,repin in cases:
   d=Path(tempfile.mkdtemp(prefix='boundary-audit-case-'))
   try:
    shutil.copytree(root/'packet',d/'packet');(d/'packet').chmod(0o755)
    for p in (d/'packet').iterdir():p.chmod(0o644)
    for name2 in ['FREEZE_MANIFEST.json','bootstrap.py']:
     shutil.copyfile(root/name2,d/name2)
    mutator(d)
    if repin:
     args=[*flags,str(root/'packet/verify.py'),'--packet',str(d/'packet'),'--manifest',str(d/'FREEZE_MANIFEST.json'),'--manifest-sha256',sha(d/'FREEZE_MANIFEST.json')]
    else:args=[*flags,str(d/'bootstrap.py'),str(d/'packet')]
    p=run(args);require(p.returncode!=0,'malformed case accepted: '+name)
    results.append({'case':name,'optimization':0 if not flags else len(flags[0])-1,'rejected':True,'returncode':p.returncode,'repinned_schema_test':repin})
   finally:remove(d)
  # A symlink packet root must be rejected even when all member hashes match.
  d=Path(tempfile.mkdtemp(prefix='boundary-audit-root-'))
  try:
   (d/'packet').symlink_to(root/'packet',target_is_directory=True)
   p=run([*flags,str(root/'bootstrap.py'),str(d/'packet')]);require(p.returncode!=0,'symlink root accepted')
   results.append({'case':'symlink packet root','optimization':0 if not flags else len(flags[0])-1,'rejected':True,'returncode':p.returncode,'repinned_schema_test':False})
  finally:remove(d)
 return results

def main():
 require(sha(ORIGINAL/'source_free_packet.tar.gz')==ARCHIVE_SHA,'archive trusted pin')
 require(sha(ORIGINAL/'FREEZE_MANIFEST.json')==MANIFEST_SHA,'manifest trusted pin')
 require(sha(ORIGINAL/'bootstrap.py')==BOOTSTRAP_SHA,'bootstrap pin')
 original_snapshot=snapshot(ORIGINAL/'packet')
 temp=Path(tempfile.mkdtemp(prefix='boundary-audit-archive-'))
 try:
  expected={'boundary_twist_11000156/'+p for p in ['packet/'+n for n in ['README.md','REPORT.md','STATUS.json','SOURCES.json','proof_checks.py','verify.py']]+['FREEZE_MANIFEST.json','bootstrap.py','BOOTSTRAP_PINS.json','ACCEPTANCE.json']}
  with tarfile.open(ORIGINAL/'source_free_packet.tar.gz','r:gz') as tar:
   members=tar.getmembers();actual={m.name for m in members if m.isfile()};require(actual==expected,'archive file membership')
   for m in members:
    require(not Path(m.name).is_absolute() and '..' not in Path(m.name).parts and (m.isfile() or m.isdir()),'unsafe archive member')
    target=temp/m.name
    if m.isdir():target.mkdir(parents=True,exist_ok=True)
    else:
     target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(tar.extractfile(m).read())
  root=temp/'boundary_twist_11000156';readonly(root)
  original_exact=exact(root); original_hostile=hostile(root)
 finally:remove(temp)
 corrected=BASE/'corrected_distribution'
 corrected_exact=exact(corrected);corrected_hostile=hostile(corrected)
 indep=[]
 for flags in [[],['-O'],['-OO']]:
  p=run([*flags,str(BASE/'independent_checks.py')]);require(p.returncode==0,p.stderr);indep.append(json.loads(p.stdout))
 require(snapshot(ORIGINAL/'packet')==original_snapshot,'original packet changed')
 receipt={'schema':'boundary-twist-independent-audit-receipt-v1','uid':os.geteuid(),'original_archive':{'bytes':(ORIGINAL/'source_free_packet.tar.gz').stat().st_size,'sha256':ARCHIVE_SHA},'original_exact':original_exact,'original_hostile':original_hostile,'corrected_exact':corrected_exact,'corrected_hostile':corrected_hostile,'independent_checks':indep,'original_packet_unchanged':True,'malformed_rejections':len(original_hostile)+len(corrected_hostile),'main_problem_resolved':False,'formal_certification':False}
 emit(BASE/'AUDIT_RECEIPT.json',receipt)
 print(json.dumps({'uid':os.geteuid(),'exact_modes_per_distribution':3,'malformed_rejections':receipt['malformed_rejections'],'original_unchanged':True,'independent_modes':3}))
if __name__=='__main__':main()

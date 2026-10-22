#!/usr/bin/env python3
"""Publication replay of the corrected 34-case author integrity matrix.
Run only after the publication bootstrap authenticates this file and the accepted slice.
"""
import hashlib,json,os,pathlib,shutil,stat,subprocess,sys,tempfile
ROOT=pathlib.Path(sys.argv[1]).absolute()
require_args = len(sys.argv)==2
if not require_args:raise SystemExit('usage: REPLAY_CORRECTED_CONTROLS.py CORRECTED_SLICE')
PACKET=ROOT/'packet';FREEZE=ROOT/'freeze'
PINS=json.loads((FREEZE/'BOOTSTRAP_PINS.json').read_text())
MODES=[[],['-O'],['-OO']]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot():
 return {str(p.relative_to(ROOT)):{'sha256':digest(p),'mode':stat.S_IMODE(p.stat().st_mode)} for folder in [PACKET,FREEZE] for p in sorted(folder.iterdir())}
def require(x,message):
 if not x:raise RuntimeError(message)
before=snapshot()
require(os.geteuid()!=0,'root cannot establish read-only denial')
receipt={'schema':'erdos-cycle-sets-acceptance-v1','uid':os.geteuid(),'euid':os.geteuid(),'modes':[],'read_only_denials':[],'hostile_tests':[],'formal_certification':False,'scope':'Packet integrity and finite diagnostics, not independent mathematical review.'}
require(digest(FREEZE/'bootstrap.py')==PINS['bootstrap_sha256'],'external bootstrap pin')
require(digest(FREEZE/'FREEZE_MANIFEST.json')==PINS['manifest_sha256'],'external manifest pin')
for flags in MODES:
 p=subprocess.run([sys.executable,'-I','-B',*flags,str(FREEZE/'bootstrap.py'),str(PACKET)],capture_output=True,text=True,timeout=40)
 require(p.returncode==0,p.stderr)
 receipt['modes'].append(json.loads(p.stdout))
for p in [PACKET/'REPORT.md',PACKET/'forbidden-create',FREEZE/'FREEZE_MANIFEST.json',FREEZE/'forbidden-create']:
 try:fd=os.open(p,os.O_WRONLY|os.O_CREAT,0o600)
 except PermissionError:receipt['read_only_denials'].append(str(p.relative_to(ROOT)))
 else:
  os.close(fd);raise RuntimeError('read-only denial not enforced')

def sandbox():
 d=pathlib.Path(tempfile.mkdtemp(prefix='erdos-cycle-sets-mutation-'))
 for folder in ['packet','freeze']:
  shutil.copytree(ROOT/folder,d/folder)
  (d/folder).chmod(0o755)
  for p in (d/folder).iterdir():p.chmod(0o644)
 return d

def rewrite(d,change):
 p=d/'freeze/FREEZE_MANIFEST.json';data=json.loads(p.read_text());change(data);p.write_text(json.dumps(data))

def repin_file(d,name):
 p=d/'packet'/name
 rewrite(d,lambda x:x['files'].__setitem__(name,{'bytes':p.stat().st_size,'sha256':digest(p)}))

def status_change(d,key,val):
 p=d/'packet/STATUS.json';s=json.loads(p.read_text());s[key]=val;p.write_text(json.dumps(s));repin_file(d,'STATUS.json')

def reject(name,mutate,direct=False,repin=False,root_link=False,no_isolation=False):
 for flags in MODES:
  d=sandbox()
  try:
   mutate(d)
   packet=d/'packet'
   if root_link:
    (d/'packet-link').symlink_to(packet,target_is_directory=True);packet=d/'packet-link'
   if direct:
    sha=digest(d/'freeze/FREEZE_MANIFEST.json') if repin else PINS['manifest_sha256']
    cmd=[sys.executable,'-I','-B',*flags,str(PACKET/'verify.py'),'--packet',str(packet),'--manifest',str(d/'freeze/FREEZE_MANIFEST.json'),'--manifest-sha256',sha]
   else:cmd=[sys.executable,*([] if no_isolation else ['-I']),'-B',*flags,str(d/'freeze/bootstrap.py'),str(packet)]
   env=dict(os.environ,PYTHONPATH=str(d/'packet'))
   p=subprocess.run(cmd,capture_output=True,text=True,timeout=15,cwd=d,env=env)
   require(p.returncode!=0,'hostile case accepted: '+name)
   require(not (d/'executed-marker').exists(),'untrusted code executed: '+name)
   receipt['hostile_tests'].append({'case':name,'optimize':2 if flags==['-OO'] else 1 if flags else 0,'rejected':True,'returncode':p.returncode})
  finally:
   shutil.rmtree(d)

reject('changed report',lambda d:(d/'packet/REPORT.md').write_text('changed'))
reject('extra file',lambda d:(d/'packet/extra.txt').write_text('extra'))
reject('extra directory',lambda d:(d/'packet/nested').mkdir())
reject('missing file',lambda d:(d/'packet/STATUS.json').unlink())
def symlink(d):
 p=d/'packet/REPORT.md';p.unlink();p.symlink_to(PACKET/'REPORT.md')
reject('symlink file',symlink)
reject('symlink root',lambda d:None,root_link=True)
def fifo(d):
 p=d/'packet/REPORT.md';p.unlink();os.mkfifo(p)
reject('FIFO file',fifo)
def dirfile(d):
 p=d/'packet/REPORT.md';p.unlink();p.mkdir()
reject('directory replacing file',dirfile)
reject('malformed manifest',lambda d:(d/'freeze/FREEZE_MANIFEST.json').write_text('{'),True,True)
reject('duplicate manifest keys',lambda d:(d/'freeze/FREEZE_MANIFEST.json').write_text('{"schema":"erdos-cycle-sets-packet-v1","schema":"erdos-cycle-sets-packet-v1","files":{}}'),True,True)
reject('manifest top-level array',lambda d:(d/'freeze/FREEZE_MANIFEST.json').write_text('[]'),True,True)
reject('manifest NaN',lambda d:(d/'freeze/FREEZE_MANIFEST.json').write_text('{"schema":NaN,"files":{}}'),True,True)
reject('path traversal',lambda d:rewrite(d,lambda x:x['files'].__setitem__('../outside',{'bytes':0,'sha256':'0'*64})),True,True)
reject('absolute path',lambda d:rewrite(d,lambda x:x['files'].__setitem__('/tmp/outside',{'bytes':0,'sha256':'0'*64})),True,True)
reject('boolean byte count',lambda d:rewrite(d,lambda x:x['files']['REPORT.md'].__setitem__('bytes',True)),True,True)
reject('negative byte count',lambda d:rewrite(d,lambda x:x['files']['REPORT.md'].__setitem__('bytes',-1)),True,True)
reject('excessive byte count',lambda d:rewrite(d,lambda x:x['files']['REPORT.md'].__setitem__('bytes',2_000_001)),True,True)
reject('invalid digest type',lambda d:rewrite(d,lambda x:x['files']['REPORT.md'].__setitem__('sha256',{})),True,True)
reject('invalid file-record shape',lambda d:rewrite(d,lambda x:x['files'].__setitem__('REPORT.md',[])),True,True)
reject('unexpected manifest schema',lambda d:rewrite(d,lambda x:x.__setitem__('schema','other')),True,True)
reject('verifier substitution',lambda d:(d/'packet/verify.py').write_text('print("fake pass")'))
def rehashed(d):
 (d/'packet/REPORT.md').write_text('altered report');repin_file(d,'REPORT.md')
reject('altered report with rehashed manifest',rehashed)
reject('manifest Python string',lambda d:(d/'freeze/FREEZE_MANIFEST.json').write_text('__import__("pathlib").Path("executed-marker").touch()'),True,True)
reject('false solved status',lambda d:status_change(d,'main_problem_resolved',True),True,True)
reject('false formal-certification status',lambda d:status_change(d,'formal_certification',True),True,True)
reject('wrong problem id',lambda d:status_change(d,'problem_id',1920),True,True)
reject('boolean proof-turn count',lambda d:status_change(d,'turns',True),True,True)
reject('false lower assertion',lambda d:status_change(d,'lower_assertion','solved'),True,True)
reject('false upper assertion',lambda d:status_change(d,'upper_assertion','newly_proved_here'),True,True)
reject('unearned review',lambda d:status_change(d,'independent_review','passed'),True,True)
reject('wrong proof-turn count',lambda d:status_change(d,'turns',4),True,True)
def bad_status(d):
 (d/'packet/STATUS.json').write_text('[]');repin_file(d,'STATUS.json')
reject('malformed status shape',bad_status,True,True)
def shadow(d):
 (d/'packet/subprocess.py').write_text('from pathlib import Path\nPath("executed-marker").touch()\n')
reject('module shadowing and PYTHONPATH injection',shadow)
reject('nonisolated bootstrap',lambda d:None,no_isolation=True)
# Successful relocated read-only replay from hostile cwd/PYTHONPATH and flags.
receipt['relocated_hostile_successes']=[]
for flags in MODES:
 d=sandbox()
 try:
  (d/'json.py').write_text('from pathlib import Path\nPath("executed-marker").touch()\nraise RuntimeError("hijacked")\n')
  (d/'sitecustomize.py').write_text('from pathlib import Path\nPath("executed-marker").touch()\n')
  for folder in ['packet','freeze']:
   for p in (d/folder).iterdir():p.chmod(0o444)
   (d/folder).chmod(0o555)
  cmd=[sys.executable,'-I','-B',*flags,str(d/'freeze/bootstrap.py'),str(d/'packet')]
  env=dict(os.environ,PYTHONPATH=str(d),PYTHONHOME=str(d/'invalid-home'),PYTHONOPTIMIZE='2',PYTHONDONTWRITEBYTECODE='0')
  run=subprocess.run(cmd,capture_output=True,text=True,cwd=d,env=env,timeout=40)
  require(run.returncode==0,'relocated hostile run failed: '+run.stderr)
  require(not (d/'executed-marker').exists(),'hostile module executed')
  require(not any(x.name=='__pycache__' for x in d.rglob('*')),'bytecode was written')
  out=json.loads(run.stdout)
  require(out['optimize']==(2 if flags==['-OO'] else 1 if flags else 0),'environment overrode optimization')
  receipt['relocated_hostile_successes'].append({'optimize':out['optimize'],'uid':out['uid'],'read_only':True,'cwd_and_pythonpath_hijack_blocked':True})
 finally:
  # Only this temporary relocation copy is made writable for cleanup.
  for folder in ['packet','freeze']:(d/folder).chmod(0o755)
  shutil.rmtree(d)
require(before==snapshot(),'frozen files changed')
receipt.update({'frozen_files_unchanged':True,'hostile_case_count':len(receipt['hostile_tests'])//3,'hostile_run_count':len(receipt['hostile_tests']),'manifest_sha256':PINS['manifest_sha256'],'bootstrap_sha256':PINS['bootstrap_sha256'],'verifier_sha256':PINS['verifier_sha256']})
print(json.dumps(receipt,indent=2))

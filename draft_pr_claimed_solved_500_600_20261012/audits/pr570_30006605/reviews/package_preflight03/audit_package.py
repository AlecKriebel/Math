#!/usr/bin/env python3
"""Independent inventory/Git-blob and actual OS-network-denied replay audit."""
from pathlib import Path,PurePosixPath
import datetime,errno,hashlib,json,os,stat,subprocess,sys,zipfile
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent.parent
REPO=AUDIT.parents[2]
CACHE=HERE/'.cache'
OUT=CACHE/'extract'
ROOT=OUT/'weighted_centers_verification'
sha=lambda b:hashlib.sha256(b).hexdigest()
def dump(name,obj): (HERE/name).write_text(json.dumps(obj,indent=2)+'\n')
def inventory(): return {p.relative_to(ROOT).as_posix():sha(p.read_bytes()) for p in ROOT.rglob('*') if p.is_file()}
assert sys.version_info>=(3,11) and __debug__
assert subprocess.check_output(['git','branch','--show-current'],cwd=REPO,text=True).strip()=='main'
with zipfile.ZipFile(AUDIT/'publication/verification_package.zip') as z:
 names=z.namelist(); assert len(names)==len(set(names))==93
 for x in z.infolist():
  p=PurePosixPath(x.filename)
  assert not p.is_absolute() and '..' not in p.parts and p.as_posix()==x.filename and '\\' not in x.filename
  assert p.parts[0]=='weighted_centers_verification' and not stat.S_ISLNK(x.external_attr>>16)
  assert not any(y in ('.cache','scratch','sources','qa','.secrets') for y in p.parts)
  assert '.private' not in p.name
 z.extractall(OUT)
payload={p.relative_to(ROOT).as_posix():p.read_bytes() for p in ROOT.rglob('*') if p.is_file()}
m=json.loads(payload['MANIFEST.json']); assert set(payload)==set(m['files'])|{'MANIFEST.json'}
for n,r in m['files'].items(): assert len(payload[n])==r['bytes'] and sha(payload[n])==r['sha256']
seals=json.loads(payload['SEALS.json']); assert seals==m['nested_seals'] and len(seals)==6
nested=0
for n in seals:
 seen=set()
 for line in payload[n].decode().splitlines():
  h,rel=line.split('  ',1); t=(PurePosixPath(n).parent/rel).as_posix(); assert t not in seen; seen.add(t)
  assert sha(payload[t])==h; nested+=1
assert nested==54
snap=json.loads(payload['ORIGINAL_SNAPSHOT.json']); assert len(snap['files'])==16
blob_rows=[]
for r in snap['files']:
 n=r['path']; actual=subprocess.check_output(['git','show','417ca52e83cf06b07c388d89c756cfd86473d5b0:'+n],cwd=REPO)
 assert actual==payload['original/'+n] and sha(actual)==r['sha256'] and len(actual)==r['size']
 blob_rows.append({'path':n,'sha256':sha(actual),'bytes':len(actual),'exact_git_blob':True})
dump('INTEGRITY_RESULTS.json',{'status':'PASS','members':93,'outer_payloads':92,'nested_entries':nested,'ordinary_seals':6,'git_originals':blob_rows,'archive_safe':True,'branch':'main'})
before=inventory()
profile='(version 1)(allow default)(deny network*)'
probe=subprocess.run(['/usr/bin/sandbox-exec','-p',profile,sys.executable,'-c','import socket; socket.create_connection(("127.0.0.1",9),timeout=1)'],capture_output=True,text=True)
assert probe.returncode!=0 and 'Operation not permitted' in probe.stderr and 'PermissionError' in probe.stderr
proc=subprocess.Popen(['/usr/bin/sandbox-exec','-p',profile,sys.executable,str(ROOT/'run_all.py')],cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(CACHE)),stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
stdout,stderr=proc.communicate()
(HERE/'OFFLINE_REPLAY.stdout.txt').write_text(stdout); (HERE/'OFFLINE_REPLAY.stderr.txt').write_text(stderr)
rows=[json.loads(x) for x in stdout.splitlines()]
assert proc.returncode==0 and not stderr and len(rows)==6 and rows[-1]['replayed_jobs']==5 and rows[-1]['status']=='PASS'
assert before==inventory()
dump('OFFLINE_REPLAY_RESULTS.json',{'status':'PASS','python':sys.version,'assertions_enabled':__debug__,'os_profile':profile,'loopback_probe_returncode':probe.returncode,'loopback_probe_error':probe.stderr.splitlines()[-1],'network_denial_verified':True,'all_five_actual_jobs':True,'results':rows,'frozen_extraction_unchanged':True,'completed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
print('PASS: all five actual jobs under verified OS network denial')

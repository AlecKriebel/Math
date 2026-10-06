from pathlib import Path
import subprocess,json,hashlib,os,datetime
A=Path(__file__).resolve().parent;C=A.parents[2]
D=A/'remote_main_advance_reconciliation_20261006'
i=json.loads((D/'INSPECTION.json').read_text())
if i['selected_collision_paths']:raise RuntimeError('collision')
s=json.loads((A/'SOURCE_MATH_CHECKPOINT_SELECTION_20261006.json').read_text())
pins=[]
for r in s['paths']:
 b=(C/r).read_bytes();pins.append({'file':r,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
def command(args):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 p=subprocess.Popen(['git',*args],cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE);o,e=p.communicate()
 n=len(records);(D/('ff'+str(n)+'.stdout.bin')).write_bytes(o);(D/('ff'+str(n)+'.stderr.bin')).write_bytes(e)
 records.append({'argv':['git',*args],'PID':p.pid,'UTC_start':start,'UTC_end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':p.returncode,'stdout_bytes':len(o),'stderr_bytes':len(e),'stdout_sha256':hashlib.sha256(o).hexdigest(),'stderr_sha256':hashlib.sha256(e).hexdigest()})
 (D/'FAST_FORWARD_PROCESS_JOURNAL.json').write_text(json.dumps(records,indent=2)+'\n')
 if p.returncode:raise RuntimeError(e.decode())
 return o
records=[]
if command(['symbolic-ref','--short','HEAD']).strip()!=b'main':raise RuntimeError('notmain')
if command(['rev-parse','HEAD']).decode().strip()!=i['old']:raise RuntimeError('HEADchanged')
if command(['diff','--cached','--name-only','-z']):raise RuntimeError('staged')
if command(['ls-remote','https://github.com/AlecKriebel/Math.git','refs/heads/main']).decode().split()[0]!=i['new']:raise RuntimeError('remotechanged')
command(['merge','--ff-only',i['new']])
if command(['rev-parse','HEAD']).decode().strip()!=i['new']:raise RuntimeError('ff failed')
if command(['diff','--cached','--name-only','-z']):raise RuntimeError('index changed')
for r in pins:
 b=(C/r['file']).read_bytes()
 if len(b)!=r['bytes'] or hashlib.sha256(b).hexdigest()!=r['sha256']:raise RuntimeError('selected work changed')
v={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'operator_PID':os.getpid(),'old':i['old'],'new':i['new'],'preserved_remote_commits':i['commits'],'selected_full_bodies_preserved':pins,'branch':'main','index_empty':True,'no_remote_mutation':True,'no_primary_checkout_mutation':True,'next_checkpoint_expected_parent':i['new']}
(D/'FAST_FORWARD_RECEIPT.json').write_text(json.dumps(v,indent=2)+'\n')
print(json.dumps({k:x for k,x in v.items() if k!='selected_full_bodies_preserved'}))


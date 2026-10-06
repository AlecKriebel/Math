from pathlib import Path
import argparse,subprocess,json,hashlib,datetime,os
parser=argparse.ArgumentParser();parser.add_argument('label');parser.add_argument('expected');parser.add_argument('selection',type=Path);parser.add_argument('message');args=parser.parse_args()
A=Path(__file__).resolve().parent;C=A.parents[2];D=A/'actual_checkpoints'/args.label;D.mkdir(parents=True,exist_ok=False);records=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(c,m):
 if not c:raise RuntimeError(m)
def run(argv):
 start=now();p=subprocess.Popen(argv,cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate();i=len(records)
 for name,b in [('stdout',out),('stderr',err)]:(D/(str(i)+'.'+name+'.bin')).write_bytes(b)
 records.append({'argv':argv,'PID':p.pid,'UTC_start':start,'UTC_end':now(),'exit_code':p.returncode,'stdout_file':str(i)+'.stdout.bin','stderr_file':str(i)+'.stderr.bin','stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_sha256':hashlib.sha256(err).hexdigest()})
 (D/'PROCESS_JOURNAL.json').write_text(json.dumps({'actual_operator_PID':os.getpid(),'records':records},indent=2)+'\n');require(p.returncode==0,err.decode()[:1200]);return out
def git(*a):return run(['git',*a])
require(git('symbolic-ref','--short','HEAD').strip()==b'main','notmain');require(git('rev-parse','HEAD').strip().decode()==args.expected,'HEADchanged');require(git('ls-remote','https://github.com/AlecKriebel/Math.git','refs/heads/main').decode().split()[0]==args.expected,'remotechanged');require(not git('diff','--cached','--name-only','-z'),'foreignstaged')
paths=sorted(set(json.loads(args.selection.read_text())['paths']));pins=[]
for rel in paths:
 p=(C/rel).resolve();require(p.is_relative_to(C) and p.is_file() and not (C/rel).is_symlink(),'invalidpath');b=p.read_bytes();pins.append({'file':rel,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
git('add','-f','--',*paths);staged=sorted(x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x);require(staged and set(staged)<=set(paths),'stagescope')
git('commit','-m',args.message);commit=git('rev-parse','HEAD').strip().decode();require(git('rev-parse',commit+'^').strip().decode()==args.expected,'parent');changed=sorted(x.decode() for x in git('diff-tree','--no-commit-id','--name-only','-r','-z',commit).split(b'\0') if x);require(changed==staged,'commitscope')
for row in pins:
 b=git('show',commit+':'+row['file']);require(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'committedbody')
git('push','--force-with-lease=refs/heads/main:'+args.expected,'https://github.com/AlecKriebel/Math.git','HEAD:refs/heads/main');require(git('ls-remote','https://github.com/AlecKriebel/Math.git','refs/heads/main').decode().split()[0]==commit,'readback');require(not git('diff','--cached','--name-only','-z'),'stagedremainder')
r={'schema':'scoped-main-checkpoint/v1','UTC':now(),'actual_operator_PID':os.getpid(),'commit':commit,'parent':args.expected,'branch':'main','remote_verified':True,'changed_paths':changed,'pins':pins,'primary_checkout_mutated':False,'primary_synchronization_pending':True}
(D/'RECEIPT.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in ['pins','changed_paths']}))

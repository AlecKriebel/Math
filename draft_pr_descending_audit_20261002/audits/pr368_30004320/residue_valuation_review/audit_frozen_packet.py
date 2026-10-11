#!/usr/bin/env python3
"""Read-only frozen Git/manifest and complete byte-exact replay audit."""
from pathlib import Path
import json,hashlib,subprocess,sys,datetime,shutil
OWN=Path(__file__).resolve().parent
AUDIT=OWN.parent
REPO=AUDIT.parents[2]
HEAD='74617174ddfb3ea726cea343a4ba915613724bdc'
BASE='efd29c05204703acca9a0860812f54b94fae54b1'
TARGET='problems/30004320_laurent_descent'
SNAP=AUDIT/'snapshot'/TARGET
RUN=OWN/'private'/'artifact_replay'
RUN.mkdir(exist_ok=True)
CAND=RUN/'candidate'
if not CAND.exists():shutil.copytree(SNAP,CAND)
STREAM=OWN/'replay_streams';STREAM.mkdir(exist_ok=True)
checks=[]
def ck(name,ok,detail=None):
 if not ok:raise AssertionError(name)
 checks.append({'name':name,'detail':detail})
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*argv):return subprocess.check_output(['git',*argv],cwd=REPO)
def binding(name,path,row,sizekey='bytes',shakey='sha256'):
 b=path.read_bytes();ck(name,len(b)==row[sizekey] and sha(b)==row[shakey],{'bytes':len(b),'sha256':sha(b)})
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
manifest=json.loads((AUDIT/'snapshot_manifest.json').read_bytes())
ck('frozen_literal_pins',manifest['head']==HEAD and manifest['base']==BASE and manifest['target_prefix']==TARGET)
paths=[r['path'] for r in manifest['files']]
ck('frozen_unique_scope',len(paths)==54 and len(set(paths))==54 and sum(p.startswith(TARGET+'/')for p in paths)==53)
diff=git('diff','--name-only',BASE,HEAD).decode().splitlines()
ck('recursive_git_scope',set(diff)==set(paths))
for row in manifest['files']:
 b=(AUDIT/'snapshot'/row['path']).read_bytes();raw=git('show',HEAD+':'+row['path'])
 ck('frozen_blob:'+row['path'],raw==b and len(b)==row['bytes'] and sha(b)==row['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob_sha'])
 mode=git('ls-tree',HEAD,'--',row['path']).decode().split()[0]
 ck('mode:'+row['path'],mode=='100644')
ck('private_candidate_exact',all((CAND/f.relative_to(SNAP)).read_bytes()==f.read_bytes()for f in SNAP.rglob('*')if f.is_file()))
bindings=0;sources=0
for f in sorted(SNAP.rglob('*.json')):
 a=json.loads(f.read_bytes())
 # Full JSON parsing includes all existing state/result objects, not a sampled projection.
 ck('parse_complete_json:'+str(f.relative_to(SNAP)),isinstance(a,(dict,list)))
 if isinstance(a,dict) and 'files'in a and f.name!='REMOTE_BINDING.json':
  for row in a['files']:
   if 'path'in row:
    binding(str(f.relative_to(SNAP))+':'+row['path'],f.parent/row['path'],row);bindings+=1
   elif 'name'in row:
    binding(str(f.relative_to(SNAP))+':'+row['name'],OWN/'private'/row['name'],row);sources+=1
pub=json.loads((SNAP/'PUBLICATION_MANIFEST.json').read_bytes())
ck('publication_exact_scope',set(r['path']for r in pub['files'])==set(str(f.relative_to(SNAP))for f in SNAP.rglob('*')if f.is_file() and f.name!='PUBLICATION_MANIFEST.json'))
ck('eleven_fresh_sources',sources==11)
chain=['5e2eb63fd571f2f660ff9ebb436440029b5d1268','d7d898ba23e9d024e79b938e3e0e305d91bb125b','c800217d22d329d6ca397f3c18e5115c77688fb9','24ecf1f2f0ab62082f328545180e4b2ba1640ab7','b08662a16499edf37f0c0eae850cfa00b7778ed6']
prev=BASE
for turn,commit in enumerate(chain,1):
 parents=git('show','-s','--format=%P',commit).decode().strip().split();ck('author_parent:'+str(turn),parents==[prev]);prev=commit
 mf=json.loads((SNAP/f'TURN_{turn}_MANIFEST.json').read_bytes())
 ck('author_turn_manifest:'+str(turn),git('show',commit+':'+TARGET+f'/TURN_{turn}_MANIFEST.json')==(SNAP/f'TURN_{turn}_MANIFEST.json').read_bytes())
 for row in mf['files']:ck('author_anchor:'+str(turn)+':'+row['path'],git('show',commit+':'+TARGET+'/'+row['path'])==(SNAP/row['path']).read_bytes())
 if turn>1:ck('manifest_chain:'+str(turn),mf['previous_manifest_sha256']==sha((SNAP/f'TURN_{turn-1}_MANIFEST.json').read_bytes()))
ck('frozen_publication_parents',git('show','-s','--format=%P',HEAD).decode().strip().split()==[BASE,chain[-1]])
am=json.loads((SNAP/'FINAL_AUTHOR_MANIFEST.json').read_bytes())
for row in am['files']:ck('final_author_anchor:'+row['path'],git('show',chain[-1]+':'+TARGET+'/'+row['path'])==(SNAP/row['path']).read_bytes())
ck('final_author_manifest_anchor',git('show',chain[-1]+':'+TARGET+'/FINAL_AUTHOR_MANIFEST.json')==(SNAP/'FINAL_AUTHOR_MANIFEST.json').read_bytes())
old=git('show',BASE+':unsolved_math_prioritization/QUEUE.md').decode().splitlines(keepends=True)
new=git('show',HEAD+':unsolved_math_prioritization/QUEUE.md').decode().splitlines(keepends=True)
ck('queue_same_linecount',len(old)==len(new));ix=[i for i,l in enumerate(new)if len(l.split('|'))>2 and l.split('|')[2].strip().split()[:1]==['30004320']];ck('one_queue_row',len(ix)==1)
i=ix[0];oc=old[i].split('|');nc=new[i].split('|');ck('queue_scope',len(oc)==len(nc)and all(oc[j]==nc[j]for j in range(len(oc))if j not in(8,9)) and oc[8].strip()=='queued' and oc[9].strip()=='0/5' and nc[8].strip()=='unsolved' and nc[9].strip()=='5/5' and all(a==b for j,(a,b)in enumerate(zip(old,new))if j!=i))
remote=json.loads((SNAP/'review/REMOTE_BINDING.json').read_bytes())
for row in remote['files']:
 b=(SNAP/row['path']).read_bytes();ck('historical_remote_blob:'+row['path'],len(b)==row['size']and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob_sha'])
replays=[]
def run(label,argv,expected=None):
 r=subprocess.run(argv,cwd=CAND,capture_output=True)
 (STREAM/(label+'.stdout')).write_bytes(r.stdout);(STREAM/(label+'.stderr')).write_bytes(r.stderr)
 ck('replay_exit:'+label,r.returncode==0,{'returncode':r.returncode})
 if expected is not None:ck('replay_full_stdout:'+label,r.stdout==expected)
 replays.append({'label':label,'argv':argv,'returncode':r.returncode,'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'stderr_bytes':len(r.stderr),'stderr_sha256':sha(r.stderr)})
 print(label,'PASS',flush=True)
for turn in range(1,6):run('author_turn_'+str(turn),[sys.executable,str(CAND/f'check_turn_{turn}.py')],(SNAP/f'TURN_{turn}_CHECKS.json').read_bytes())
run('historical_independent',[sys.executable,str(CAND/'review/independent_checks.py')],(SNAP/'review/INDEPENDENT_CHECKS.json').read_bytes())
run('author_wrapper',[sys.executable,str(CAND/'verify_packet.py'),'--source-dir',str(OWN/'private')],(SNAP/'review/AUTHOR_REPLAY.json').read_bytes())
run('historical_review_wrapper',[sys.executable,str(CAND/'review/verify_review.py'),'--author-dir',str(CAND)],b'PASS: review hashes, frozen author/remote binding, and independent replay\n')
run('publication_with_sources',[sys.executable,str(CAND/'verify_publication.py'),'--source-dir',str(OWN/'private')])
run('publication_no_sources',[sys.executable,str(CAND/'verify_publication.py')])
# Compare every byte of both publication streams to independently assembled complete wrapper output.
author=(SNAP/'review/AUTHOR_REPLAY.json').read_bytes()
review=b'PASS: review hashes, frozen author/remote binding, and independent replay\n'
end=b'PASS: all publication bytes, frozen author proofs and independent review; original unsolved 5/5\n'
ck('publication_sources_complete_stdout',(STREAM/'publication_with_sources.stdout').read_bytes()==author+review+end)
j=json.loads(author);j['source_pdfs_checked']=0;j['source_check']='not requested; raw sources are not distributed'
ck('publication_portable_complete_stdout',(STREAM/'publication_no_sources.stdout').read_bytes()==(json.dumps(j,indent=2,sort_keys=True)+'\n').encode()+review+end)
receipt={'status':'PASS','started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':HEAD,'base':BASE,'frozen_paths':54,'target_paths':53,'nested_public_file_bindings':bindings,'fresh_primary_sources':sources,'author_checkpoints':chain,'queue_line_one_based':i+1,'checks':checks,'check_count':len(checks),'author_assertions':128694,'historical_independent_assertions':8664,'replays':replays,'limitations':'Read-only frozen Git and complete byte streams. No live remote acceptance/merge claim; finite controls do not prove source/gerbe theorems.'}
(OWN/'ARTIFACT_REPRODUCTION.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS',len(checks),'artifact checks',bindings,'public nested bindings')

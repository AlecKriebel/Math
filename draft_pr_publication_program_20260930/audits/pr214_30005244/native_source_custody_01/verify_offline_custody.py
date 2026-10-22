"""Offline identity/completeness replay only. No API, subprocess, Git or math."""
from pathlib import Path
import hashlib,json,stat,sys
HERE=Path(__file__).absolute().parent
def need(x,msg):
 if type(x)is not bool or not x:raise RuntimeError(msg)
def native(k,b):return hashlib.sha1(k.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def read(path):
 p=HERE/path;need(p.resolve()==p and stat.S_ISREG(p.lstat().st_mode),'Ordinary canonical custody file');return p.read_bytes()
def run():
 inv=json.loads(read('INVENTORY.json'));records=json.loads(read('BODY_RECORDS.json'));alltrees={}
 for name in ('AUTHENTICATED_TREES.json','BODY_ADDITIONAL_TREES.json','SOURCE_DIRECTORY_TREES.json','RELATED_CONTEXT_TREES.json'):
  for oid,entries in json.loads(read(name)).items():
   if oid in alltrees:need(alltrees[oid]==entries,'Tree cache disagreement')
   rows=sorted(entries.items(),key=lambda v:v[0].encode()+(b'/' if v[1]['type']=='tree' else b''))
   raw=b''.join(v['mode'].lstrip('0').encode()+b' '+k.encode()+b'\0'+bytes.fromhex(v['sha']) for k,v in rows)
   need(native('tree',raw)==oid,'Native tree SHA1');alltrees[oid]=entries
 def lookup(oid,path):
  for i,name in enumerate(path.split('/')):
   r=alltrees[oid][name]
   if i<len(path.split('/'))-1:oid=r['sha']
  return r
 def descend(oid,prefix):
  out={}
  for name,r in alltrees[oid].items():
   path=prefix+'/'+name
   if r['type']=='tree':out.update(descend(r['sha'],path))
   else:out[path]=r
  return out
 attempt='unsolved_math_prioritization/attempts/30005244'
 for tag,count in (('original',31),('current',41)):
  root=inv[tag]['commit']['tree'];commit=inv[tag]['commit']['sha'];raw=read('_private/native_commits/'+commit+'.commit')
  need(native('commit',raw)==commit and raw.startswith(('tree '+root+'\n').encode()),'Exact raw native commit object/root')
  parents=[s.removeprefix(b'parent ').decode() for s in raw.split(b'\n\n',1)[0].splitlines() if s.startswith(b'parent ')]
  need(parents==inv[tag]['commit']['parents'],'Exact raw native ordered parents')
  tree=lookup(root,attempt);need(tree==inv[tag]['attempt'],'Attempt native path association')
  leaves=descend(tree['sha'],attempt);need(leaves==inv[tag]['leaves'] and len(leaves)==count,'Complete recursive owned leaf inventory')
  selected=[r for r in records['records'] if r['snapshot']==tag and not r.get('kind')]
  need(len(selected)==count and {r['path'] for r in selected}==set(leaves),'Full owned body coverage')
  for r in selected:
   b=read(r['reading_copy']);need(pin(b)=={k:r[k] for k in ('bytes','sha256')} and native('blob',b)==r['sha'] and {k:r[k] for k in ('mode','type','sha')}==leaves[r['path']],'Every selected native body and mode')
  for path,r in inv[tag]['instructions'].items():
   b=read('_private/reading/'+tag+'/'+path);need(pin(b)=={k:r[k] for k in ('bytes','sha256')} and native('blob',b)==r['sha'] and lookup(root,path)=={k:r[k] for k in ('mode','type','sha')},'Applicable instruction native body')
  q=inv[tag]['queue'];b=read('_private/reading/'+tag+'/unsolved_math_prioritization/QUEUE.md');need(pin(b)=={k:q[k] for k in ('bytes','sha256')} and native('blob',b)==q['sha'],'Whole native QUEUE body')
  matches=[line for line in b.splitlines(keepends=True) if len(line.decode().split('|'))==14 and line.decode().split('|')[2].strip().split(' / ')[0]=='30005244']
  need(len(matches)==1 and pin(matches[0])==q['row_pin'] and matches[0].decode()==q['row'],'Unique exact own QUEUE row')
 for r in records['records']:
  b=read(r['reading_copy']);need(pin(b)=={k:r[k] for k in ('bytes','sha256')} and native('blob',b)==r['sha'],'Every recorded applicable body')
 original={r['path']:r for r in records['records'] if r['snapshot']=='original' and not r.get('kind')}
 current={r['path']:r for r in records['records'] if r['snapshot']=='current' and not r.get('kind')}
 for path,r in original.items():
  archive=current[attempt+'/history/original_submission_20261015/'+path.removeprefix(attempt+'/')]
  need(all(r[k]==archive[k] for k in ('mode','type','sha','bytes','sha256')),'All31 original archival copies exact')
 context=json.loads(read('RELATED_SOURCE_CONTEXT.json'))
 for tag in ('original','current'):
  r=context[tag]
  if r['node'] is not None:
   b=read(r['reading_copy']);need(pin(b)=={k:r[k] for k in ('bytes','sha256')} and native('blob',b)==r['node']['sha'],'Exact bounded related-target native body')
 ledger=json.loads(read('_private/API_LEDGER.json'))
 for r in ledger:
  b=read('_private/'+r['raw_path']);need(pin(b)==r['stdout_pin'] and r['method']=='GET' and r['hostname']=='github.com' and r['exit']==0,'Exact successful actual GET response')
 need(len(ledger)<=350 and sum(r['stdout_pin']['bytes'] for r in ledger)<=120000000,'Finite response budget')
 return {'schema':'pr214-native-custody-offline-replay-v1','status':'PASS','native_commits_verified':2,'canonical_native_trees_verified':len(alltrees),'original_attempt_files':31,'current_attempt_files':41,'original31_exact_current_archival_copies':31,'whole_QUEUE_bodies_unique_rows':2,'full_body_records_including_two_readmes':len(records['records']),'actual_GET_responses':len(ledger),'wire_bytes':sum(r['stdout_pin']['bytes'] for r in ledger),'no_API_Git_subprocess_or_scientific_program_execution':True,'mathematical_acceptance_inferred':False}
if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))


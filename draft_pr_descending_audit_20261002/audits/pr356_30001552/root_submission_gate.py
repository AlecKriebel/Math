"""Read-only exact-source, submission and closed-evidence checks for PR356."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,stat,subprocess,zipfile
A=Path(__file__).resolve().parent;P=A.parents[1];R=P.parent
Q='unsolved_math_prioritization/QUEUE.md';TARGET='problems/30001552_antimorphic_periods';PY='/opt/homebrew/bin/python3.11'
def utc():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def inventory(root):
 out={}
 for p in sorted(root.rglob('*')):
  assert not p.is_symlink() and (p.is_file() or p.is_dir())
  e={'type':'file' if p.is_file() else 'directory','mode':stat.S_IMODE(p.stat().st_mode)}
  if p.is_file():b=p.read_bytes();e.update(bytes=len(b),sha256=sha(b))
  out[p.relative_to(root).as_posix()]=e
 return out
class Capture:
 def __init__(self,purpose):
  self.directory=A/'root_replay_private'/(purpose+'_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f'))
  self.directory.mkdir(parents=True,exist_ok=False);self.entries=[]
 def run(self,label,args,cwd=R,ok=(0,),input=None):
  args=[str(x) for x in args];assert not (self.directory/(label+'.json')).exists()
  prep={'utc':utc(),'argv':args,'cwd':str(cwd),'programs':[{'path':s,'bytes':Path(s).stat().st_size,'sha256':sha(Path(s).read_bytes())} for s in args if s.endswith('.py') and Path(s).is_file()]}
  (self.directory/(label+'.preexecution.json')).write_text(json.dumps(prep,indent=2)+'\n')
  z=subprocess.run(args,cwd=cwd,input=input,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0',GIT_NO_LAZY_FETCH='1'))
  streams={}
  for name,b in [('stdout',z.stdout),('stderr',z.stderr)]:
   f=self.directory/(label+'.'+name);f.write_bytes(b);streams[name]={'path':str(f),'bytes':len(b),'sha256':sha(b)}
  e={**prep,'finished_utc':utc(),'exit_code':z.returncode,'streams':streams};self.entries.append(e)
  (self.directory/(label+'.json')).write_text(json.dumps(e,indent=2)+'\n');assert z.returncode in ok,(label,z.returncode,z.stderr.decode(errors='replace'));return z
 def git(self,*args):
  z=self.run('git_'+str(len(self.entries)),['git',*args]);assert not z.stderr;return z.stdout
def current_clearance():
 c=load(A/'PUBLISHING_CLEARANCE.json')
 assert c['status']=='READY_AFTER_TWO_SEQUENTIAL_FRESH_PREPRINT_REVIEWS' and c['second_review_mandatory_findings']==0 and len(c['fresh_reviews'])==2
 pins={e['path']:(e['bytes'],e['sha256']) for e in c['sealed_submission_files']};assert len(pins)==4
 for name,pin in pins.items():b=(A/'preprint'/name).read_bytes();assert (len(b),sha(b))==pin
 for n in (1,2):
  v=load(A/f'ROOT_PREPRINT_REVIEW0{n}_VERIFICATION.json');assert v['mandatory_findings']==0 and v['closed_namespace_unchanged'] and v['whole_verifier_output_compared'] and v['all_mandatory_submission_findings_resolved']
  assert {e['path']:(e['bytes'],e['sha256']) for e in v['sealed_submission_files']}==pins
  assert sha((A/f'preprint_review_0{n}'/v['review_seal_path']).read_bytes())==v['review_seal_sha256']
 return c
def queue_binding(capture,base,target):
 old=capture.git('show',f'{base}:{Q}').splitlines(keepends=True);new=capture.git('show',f'{target}:{Q}').splitlines(keepends=True)
 assert len(old)==len(new);changes=[i for i,(a,b) in enumerate(zip(old,new)) if a!=b];assert len(changes)==1
 i=changes[0];before,after=old[i].split(b'|'),new[i].split(b'|');assert len(before)==len(after)
 assert before[2].strip().split(b' / ')[0]==b'30001552' and [before[j].strip() for j in (8,9)]==[b'queued',b'0/5']
 assert [after[j].strip() for j in (8,9)]==[b'claimed_solved',b'1/5']
 assert [j for j,(a,b) in enumerate(zip(before,after)) if a!=b]==[8,9,11]
 receipt=load(A/'queue_repair_receipt.json');assert old[i].decode()==receipt['old_row'] and new[i].decode()==receipt['new_row']
 return {'queue_physical_line':i+1,'queue_only_pipe_cells':[8,9,11],'all_other_queue_bytes_equal':True}
def package_replay(capture):
 clear=current_clearance();original=load(A/'snapshot_manifest.json');scratch=capture.directory/'zip_scratch';scratch.mkdir()
 with zipfile.ZipFile(A/'preprint/alternating-antimorphic-verification.zip') as z:
  members=z.infolist();assert len(members)==69 and len({m.filename for m in members})==69
  for m in members:
   p=Path(m.filename);assert not m.is_dir() and not p.is_absolute() and '..' not in p.parts and p.parts[0]=='alternating-antimorphic-verification'
   assert (m.external_attr>>16)&0o170000 in (0,0o100000)
   f=scratch/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(z.read(m))
 t=scratch/'alternating-antimorphic-verification';before=inventory(t)
 for name in ['alternating-antimorphic-fine-wilf.tex','zenodo-deposit.json']:assert (t/name).read_bytes()==(A/'preprint'/name).read_bytes()
 for e in original['files']:
  if e['path']==Q:continue
  b=(t/'submitted_problem'/Path(e['path']).relative_to(TARGET)).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
 prior=load(A/'ROOT_PREPRINT_PACKAGE_VERIFICATION.json');expected=(A/'root_replay_private/preprint_draft002/integrity.stdout').read_bytes()
 z=capture.run('package_integrity',[PY,'-B',t/'verify_supplement.py'],cwd=t)
 assert z.stdout==expected and not z.stderr and inventory(t)==before
 streams=[]
 for label,relative in [('default','preprint_draft002/integrity.stdout'),('full','preprint_draft001/full.stdout')]:
  native=(A/'root_replay_private'/relative).read_bytes();pin=prior['runs']['integrity' if label=='default' else 'full']['stdout']
  assert len(native)==pin['bytes'] and sha(native)==pin['sha256']
  for n in (1,2):
   v=load(A/f'ROOT_PREPRINT_REVIEW0{n}_VERIFICATION.json');bindings=v['package_native_streams'][label]
   b=Path(bindings['stdout_path']).read_bytes();assert b==native and Path(bindings['stderr_path']).read_bytes()==b''
   assert len(b)==bindings['bytes'] and sha(b)==bindings['sha256'] and bindings['exit_code']==0
  streams.append({'mode':label,'bytes':len(native),'sha256':sha(native),'whole_output_equal_root_and_both_reviewers':True})
 current_clearance()
 return {'ordinary_zip_files':69,'payload_files':68,'fresh_native_integrity_output_equal':True,'all_original16_bindings_exact':True,
  'full_and_default_native_stream_comparisons':streams,'mathematical_programs_reexecuted_here':False,
  'scope':'Fresh complete package integrity gate; unchanged ZIP pins bind previous genuine root and both fresh reviewer full executions. No unnecessary additional finite-program rerun.'}
def closed_reviews(capture):
 maths=load(A/'ROOT_CLOSED_MATH_FAMILIES.json');names={'signed_graph':A/'signed_graph_review/proposed_namespace','word_overlap':A/'word_overlap_review','definition_counterexamples':A/'definition_counterexample_review'};specs=[]
 for e in maths['native_verifications']:
  if e['mode']!='full':continue
  n=names[e['name']];pin=maths['whole_closed_namespaces'][e['name']];actual=inventory(n)
  files={p:{k:v[k] for k in ['bytes','sha256','mode']} for p,v in actual.items() if v['type']=='file'}
  dirs={p:v['mode'] for p,v in actual.items() if v['type']=='directory'};dirs['.']=stat.S_IMODE(n.stat().st_mode)
  assert files==pin['files'] and dirs==pin['directories']
  output=A/'root_replay_private/family_closure_001'/(e['name']+'_full_closed.stdout');assert len(output.read_bytes())==e['stdout_bytes'] and sha(output.read_bytes())==e['stdout_sha256']
  specs.append((e['name'],n,e['argv'],output,actual))
 priority=load(A/'ROOT_PRIORITY_POSTCLOSURE_REPLAY.json');n=A/'priority_review';assert inventory(n)==priority['tree'];e=priority['runs']['full'];output=A/'root_replay_private/priority_postclosure_001/full.stdout'
 assert len(output.read_bytes())==e['stdout']['bytes'] and sha(output.read_bytes())==e['stdout']['sha256'];specs.append(('priority_review',n,e['argv'],output,inventory(n)))
 for k in (1,2):
  v=load(A/f'ROOT_PREPRINT_REVIEW0{k}_VERIFICATION.json');n=A/f'preprint_review_0{k}';assert inventory(n)==v['whole_namespace']
  e=next(e for e in v['native_runs'] if '--full' in e['argv'] or e.get('mode')=='full');output=Path(e['stdout_path']);assert len(output.read_bytes())==e['stdout_bytes'] and sha(output.read_bytes())==e['stdout_sha256']
  specs.append((f'preprint_review_0{k}',n,e['argv'],output,inventory(n)))
 results=[]
 for name,n,args,output,before in specs:
  z=capture.run('closed_'+name,args,cwd=A);assert z.stdout==output.read_bytes() and not z.stderr and inventory(n)==before,name
  results.append({'family':name,'whole_files':sum(e['type']=='file' for e in before.values()),'whole_output_equal':True,'closed_namespace_unchanged':True})
 return results

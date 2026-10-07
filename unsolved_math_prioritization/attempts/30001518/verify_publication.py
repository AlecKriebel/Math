#!/usr/bin/env python3
"""Externally anchored exact-inventory replay; finite controls are not proof formalization."""
import argparse, hashlib, json, os, re, subprocess, sys, tempfile, zipfile
from pathlib import Path, PurePosixPath
ANCHORS = {
 'packet': ('AUTHOR_MANIFEST.json','802e09153108d1ca826841748adfe751aec2fb2c1fe6718bca1083b0e56eb610','author_packet.zip','164e5736afdf41580386741079a6ee5b05ea5041b56036def48f379970f3042b'),
 'audit_frozen': ('AUDIT_MANIFEST.json','8e5005761c5f9c0fddd8b0bcc5c4dfb9a599cbc92c011d541d06b7da2e097e46','independent_audit.zip','9d2a975d347fe8f54301b7d31d70a365b9fa28503082cf4d52760f07a46a475c')}
TOP={'README.md','RESEARCH_LOG.md','PUBLICATION_STATUS.json','requirements.txt','verify_publication.py','mutation_tests.py','PUBLIC_MANIFEST.json','author_packet.zip','independent_audit.zip'}
def need(ok,message):
 if not ok: raise RuntimeError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):
 need(p.is_file() and not p.is_symlink(),'Nonregular file: '+str(p));return p.read_bytes()
def unique(pairs):
 d={}
 for k,v in pairs:need(k not in d,'Duplicate JSON key');d[k]=v
 return d
def parse(b):return json.loads(b,object_pairs_hook=unique)
def safe(s):
 need(isinstance(s,str) and s and not s.startswith('/') and '\\' not in s and all(x not in ('','.','..') for x in s.split('/')),'Unsafe path');return PurePosixPath(s)
def match(b,r):return r=={'bytes':len(b),'sha256':sha(b)} and type(r['bytes']) is int

def verify(root,pin,integrity_only=False):
 need(re.fullmatch('[0-9a-f]{64}',pin) is not None,'Bad external pin')
 need(root.is_dir() and not root.is_symlink(),'Invalid root')
 raw=read(root/'PUBLIC_MANIFEST.json');need(sha(raw)==pin,'External manifest pin mismatch');m=parse(raw)
 need(m['schema']=='retroreflector-source-free-publication-v1' and m['problem_id']==30001518,'Manifest identity')
 entries=m['files'];need(isinstance(entries,dict),'Bad file map');expected=set(entries)|{'PUBLIC_MANIFEST.json'};dirs=set()
 for name in expected:dirs.update(str(p) for p in safe(name).parents if str(p)!='.')
 actual=set();actual_dirs=set()
 for p in root.rglob('*'):
  need(not p.is_symlink(),'Symlink rejected');name=p.relative_to(root).as_posix()
  if p.is_dir():actual_dirs.add(name)
  else:need(p.is_file(),'Special file rejected');actual.add(name)
 need((actual,actual_dirs)==(expected,dirs),'Closed inventory mismatch')
 for name,r in entries.items():need(match(read(root/name),r),'Payload mismatch: '+name)
 closed=set(TOP)
 for role,(mf,mp,zf,zp) in ANCHORS.items():
  need(sha(read(root/role/mf))==mp,'Frozen manifest mismatch: '+role)
  fm=parse(read(root/role/mf));need(fm['problem_id']==30001518,'Frozen identity');names=set()
  for r in fm['files']:
   need(set(r)=={'path','bytes','sha256'},'Frozen record shape');name=r['path'];need(safe(name).name==name and name not in names,'Unsafe or duplicate frozen path');names.add(name)
   need(match(read(root/role/name),{'bytes':r['bytes'],'sha256':r['sha256']}),'Frozen payload mismatch')
  names|={mf,'SHA256SUMS'};need({p.name for p in (root/role).iterdir()}==names,'Frozen inventory differs')
  sums=''.join(sha(read(root/role/n))+'  '+n+'\n' for n in sorted(names-{'SHA256SUMS'}))
  need(read(root/role/'SHA256SUMS')==sums.encode(),'Frozen checksum list differs')
  need(sha(read(root/zf))==zp,'Frozen archive mismatch')
  with zipfile.ZipFile(root/zf) as z:
   zn=z.namelist();need(len(zn)==len(set(zn)) and set(zn)=={role+'/'+n for n in names},'Archive inventory differs')
   for n in names:need(z.read(role+'/'+n)==read(root/role/n),'Archive bytes differ')
  closed.update(role+'/'+n for n in names)
 need(expected==closed,'Top-level allowlist differs')
 st=parse(read(root/'PUBLICATION_STATUS.json'));acc=parse(read(root/'audit_frozen/ACCEPTANCE.json'))
 need(st['status']==acc['status']=='unsolved' and st['turns']==acc['turns']=='5/5','Disposition mismatch')
 need(st['full_problem_solved'] is False and st['novelty_claimed'] is False and acc['mathematical_correction_required'] is False,'Claim boundary')
 replay=None
 if not integrity_only:
  env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
  # Explicitly remove -O/-OO from the spawned interpreter. The frozen author
  # scripts correctly reject optimized execution; rejection is not a passed replay.
  with tempfile.TemporaryDirectory(prefix='retro-publication-') as cwd:
   probe=subprocess.run([sys.executable,'-I','-S','-B','-c','import sys; print(sys.flags.optimize)'],capture_output=True,env=env,cwd=cwd,check=True)
   need(probe.stdout==b'0\n','Normal child not established')
   cmd=[sys.executable,'-I','-S','-B',str(root/'audit_frozen/run_audit.py'),'--author',str(root/'packet'),'--archive',str(root/'author_packet.zip')]
   p=subprocess.run(cmd,capture_output=True,env=env,cwd=cwd,timeout=600)
   need(p.returncode==0 and not p.stderr,'Audit failed: '+p.stderr.decode(errors='replace')[-1000:]);got=parse(p.stdout)
  need(got['status']=='PASS_SCOPED_AUDIT_CONTROLS' and got['full_problem_solved'] is False and got['author_freeze_unchanged'] is True,'Replay status')
  need(got['author_replay']['author_assertions']==9280 and got['author_replay']['external_inputs']=={'corpora':'NOT_RUN','source_pdfs':'NOT_RUN'},'Author replay scope')
  need([x['active_optimization'] for x in got['genuine_optimization_runs']]==[0,1,2],'Actual independent modes')
  need(all(x['checks']==77613 and x['exit_code']==0 for x in got['genuine_optimization_runs']),'Independent replay counts')
  need(len(got['independent_faults_rejected'])==12 and len(got['corruptions_rejected'])==40 and len(got['author_optimization_rejections'])==4,'Negative-control counts')
  need(all(x['exit_code']!=0 for k in ('independent_faults_rejected','corruptions_rejected','author_optimization_rejections') for x in got[k]),'Negative control accepted')
  need(got['external_source_negative'] is None,'Source-free scope')
  need(got['relocated_author_replay']==got['author_replay'],'Relocated author differs')
  frozen=parse(read(root/'audit_frozen/audit_results.json'))
  # Historical source/corpus checks are retained as evidence, never mislabeled
  # as newly reproduced without those external inputs.
  for k in ('anchored_author','independent_controls','genuine_optimization_runs','independent_faults_rejected','author_optimization_rejections','corruptions_rejected','self_consistency_limitation_control'):
   need(got[k]==frozen[k],'Frozen finite-control output differs: '+k)
  replay={'normal_child_optimization':0,'author_exact_checks':9280,'independent_checks_per_mode':77613,'actual_independent_modes':[0,1,2], 'mathematical_faults_rejected':12,'anchored_corruptions_rejected':40,'author_optimized_script_rejections':4,'author_optimized_replay_passed':False,'external_inputs':got['author_replay']['external_inputs'],'source_pdf_negative_control':'NOT_RUN','relocated_author_replay':'PASS'}
 return {'status':'PASS','problem_id':30001518,'files':len(expected),'external_manifest_sha256':pin,'publication_wrapper_optimization_level':sys.flags.optimize,'integrity_only':integrity_only,'replay':replay,'full_problem_solved':False,'scope':'Package integrity and finite controls; general bounded piecewise-smooth almost-every-ray problem unresolved.'}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--expected-manifest-sha256',required=True);p.add_argument('--root',type=Path);p.add_argument('--integrity-only',action='store_true');a=p.parse_args()
 root=a.root if a.root is not None else Path(__file__).absolute().parent
 print(json.dumps(verify(root.absolute(),a.expected_manifest_sha256,a.integrity_only),indent=2,sort_keys=True))
if __name__=='__main__':main()

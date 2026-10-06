#!/usr/bin/env python3
"""Authenticate every publication byte before executing a relocated frozen packet.

Obtain the wrapper and manifest SHA-256 from an independent publication receipt.
Integrity and finite certificate replay do not certify an unrestricted theorem.
"""
from pathlib import Path
import argparse, hashlib, io, json, os, shutil, stat, subprocess, sys, tempfile, zipfile
ROOT=Path(__file__).resolve().parent
PINS={
 'OPG-605_author_packet.zip':(17362,'f3cb16cc91789f6577849ddc1091bd29f67a600b711bcd2eacf56658626100f0'),
 'OPG-605_author_packet.manifest.json':(1927,'f45a494556b383263eea83bf788ca69618194bf259f0edb7bdf258ce7b65602e'),
 'OPG-605_independent_audit.zip':(75271,'ae9607823488af2edb9f1867d58a83eb2f8b8c8d6ccd63edc2c367137e2b5e6d'),
 'OPG-605_independent_audit.manifest.json':(4860,'972aeac7a77b451ca6182ec59685a42a05d26010b6acf319010a6d78b57cc0b9'),
 'OPG-605_accepted_packet.zip':(17633,'de0c739de8c520fb0bd009bd23d36dfa8e035e83f9626c19122c0e6827cdc9ae'),
 'OPG-605_accepted_packet.manifest.json':(2701,'6d662f60ae57051101cd6da706d0ba6146ac7e8581ff16d657606efcc62e6b1f'),
}
MODES={'normal':[],'optimized':['-O'],'isolated':['-I'],'isolated_optimized':['-I','-O']}
def need(c,m):
 if not c:raise ValueError(m)
def digest(b):return hashlib.sha256(b).hexdigest()
def pin(b,p,label):need((len(b),digest(b))==tuple(p),label+': size/hash mismatch')
def safe(name):
 p=Path(name);need(not p.is_absolute() and '..' not in p.parts and p.as_posix()==name,'unsafe path: '+name);return p
def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--expect-manifest',required=True,help='Externally obtained SHA-256 of PUBLICATION_MANIFEST.json')
 parser.add_argument('--corpus-dir',type=Path);parser.add_argument('--source-dir',type=Path)
 parser.add_argument('--full-artifact-matrix',action='store_true')
 parser.add_argument('--integrity-only',action='store_true')
 a=parser.parse_args();need(bool(a.corpus_dir)==bool(a.source_dir),'Supply both input directories or neither')
 need(not a.full_artifact_matrix or a.corpus_dir,'Full matrix requires exact external inputs')
 corpus=a.corpus_dir.resolve() if a.corpus_dir else None;sources=a.source_dir.resolve() if a.source_dir else None
 mb=(ROOT/'PUBLICATION_MANIFEST.json').read_bytes();need(digest(mb)==a.expect_manifest,'external publication-manifest hash mismatch')
 m=json.loads(mb);need(m['schema']=='opg605-publication-manifest-v1','manifest schema')
 entries=m['files'];names=[e['path'] for e in entries];need(len(names)==len(set(names)),'duplicate publication entries')
 actual=[]
 for f in ROOT.rglob('*'):
  need(not f.is_symlink(),'publication symlink')
  if f.is_file():actual.append(f.relative_to(ROOT).as_posix())
 need(set(actual)==set(names)|{'PUBLICATION_MANIFEST.json'},'publication file set differs')
 verified={}
 for e in entries:
  b=(ROOT/safe(e['path'])).read_bytes();pin(b,(e['bytes'],e['sha256']),e['path']);verified[e['path']]=b
 for n,p in PINS.items():pin(verified['releases/'+n],p,n)
 packets={};members_checked=0
 for stem,directory,count in [('author_packet','original',11),('independent_audit','audit',26),('accepted_packet','audit/accepted',11)]:
  ext=json.loads(verified[f'releases/OPG-605_{stem}.manifest.json']);expected=ext['members'];members={}
  with zipfile.ZipFile(io.BytesIO(verified[f'releases/OPG-605_{stem}.zip'])) as z:
   need(len(z.infolist())==len(expected)==count and set(z.namelist())==set(expected),'ZIP member set: '+stem)
   for info in z.infolist():
    name=info.filename;safe(name);need(not info.is_dir() and not stat.S_ISLNK(info.external_attr>>16),'unsafe ZIP member')
    b=z.read(info);p=expected[name];pin(b,(p['bytes'],p['sha256']),name)
    need(verified[directory+'/'+name]==b,'extracted bytes differ: '+name);members[name]=b;members_checked+=1
  packets[stem]=members
 for stem in ['author_packet','accepted_packet']:
  for ext in ['zip','manifest.json']:
   n=f'OPG-605_{stem}.{ext}';need(packets['independent_audit'][n]==verified['releases/'+n],'nested freeze differs')
 acc=json.loads(packets['independent_audit']['ACCEPTANCE.json'])
 need(acc['decision']=='ACCEPTED_PARTIAL_WITH_LOADER_REPAIR' and acc['approaches_used']==3 and acc['approach_limit']==5,'acceptance identity')
 need(acc['status']=='unsolved_partial_stalled' and acc['original_isolated_failures_recorded']==2,'acceptance scope')
 changed=sorted(n for n in packets['author_packet'] if packets['author_packet'][n]!=packets['accepted_packet'][n])
 need(changed==acc['changed_members']==['MANIFEST.json','VERIFYING.md','verify.py'],'derivative scope')
 for key in ['accepted_archive','accepted_external_manifest','original_archive','original_external_manifest']:
  p=acc[key];pin(verified['releases/'+p['filename']],(p['bytes'],p['sha256']),key)
 for key in ['artifact_audit','audit_report','corpus_audit','frozen_acceptance','independent_results','patch','source_audit']:
  p=acc[key];pin(packets['independent_audit'][p['filename']],(p['bytes'],p['sha256']),key)
 hist=json.loads(packets['independent_audit']['ARTIFACT_AUDIT_RESULTS.json']);need(hist['result']=='PASS' and hist['checks']==len(hist['tests'])==88,'historical matrix count')
 need(sum(t['actual_exit']!=0 and 'original relocated certificate isolated' in t['test'] for t in hist['tests'])==2,'historical original failures')
 frozen=json.loads(packets['independent_audit']['FROZEN_ACCEPTANCE_RESULTS.json']);need(frozen['result']=='PASS' and len(frozen['checks'])==8,'frozen acceptance count')
 result={'result':'PASS','problem_id':3075,'rank':925,'canonical_queue_status':'unsolved','turns':'3/5','external_artifact_pins_verified':len(PINS),'archive_members_verified':members_checked,'published_files_verified':len(entries)+1,'exact_changed_derivative_members':changed,'historical_artifact_checks':88,'historical_frozen_acceptance_checks':8,'full_external_inputs_supplied':bool(corpus),'formal_proof_certification':False}
 if a.integrity_only:
  result['replay_performed']=False;print(json.dumps(result,indent=2,sort_keys=True));return
 # Execute only the frozen bytes already authenticated above, in a new unrelated directory.
 with tempfile.TemporaryDirectory(prefix='opg605 publication relocated ') as td:
  td=Path(td);env={'PATH':os.environ.get('PATH',''),'HOME':str(td/'empty_home'),'LC_ALL':'C.UTF-8','PYTHONDONTWRITEBYTECODE':'1'}
  for stem,directory in [('author_packet','original'),('accepted_packet','accepted'),('independent_audit','audit')]:
   for name,b in packets[stem].items():
    p=td/directory/safe(name);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
  # Replay the actual frozen patch, rather than merely comparing a claimed diff.
  patchdir=td/'patch replay';shutil.copytree(td/'original',patchdir)
  proc=subprocess.run(['patch','--batch','--fuzz=0','-p1','-i',str(td/'audit/ISOLATED_LOADING.patch')],cwd=patchdir,env=env,capture_output=True,text=True,timeout=30)
  need(proc.returncode==0,'patch replay failed: '+proc.stderr)
  need({p.name for p in patchdir.iterdir()}==set(packets['accepted_packet']),'patch replay member set')
  for name,b in packets['accepted_packet'].items():need((patchdir/name).read_bytes()==b,'patch replay bytes: '+name)
  checks=[]
  def run(label,flags,script,args=(),expected=0,contains='"result": "PASS"'):
   r=subprocess.run([sys.executable,'-B']+flags+[str(script)]+list(map(str,args)),cwd=td,env=env,capture_output=True,text=True,timeout=300)
   need(r.returncode==expected and contains in r.stdout+r.stderr,label+': '+r.stderr+r.stdout)
   checks.append({'test':label,'flags':flags,'actual_exit':r.returncode,'expected_exit':expected,'stdout_sha256':digest(r.stdout.encode()),'result':'PASS'})
   return r
  for label,directory in [('original','original'),('accepted','accepted')]:
   for mode,flags in MODES.items():
    expected_fail=label=='original' and '-I' in flags
    run(label+' '+mode,flags,td/directory/'verify.py',expected=1 if expected_fail else 0,contains="No module named 'arrangement'" if expected_fail else '"result": "PASS"')
  for mode,flags in MODES.items():run('independent '+mode,flags,td/'audit/independent_verifier.py',[td/'accepted/witness.json'])
  if corpus:
   for mode,flags in MODES.items():run('full corpus and six source pins '+mode,flags,td/'accepted/verify_inputs.py',[corpus/n for n in ['catalog.json','problems.json','research_results.json']]+[sources])
  if a.full_artifact_matrix:
   r=run('88-check artifact matrix',['-I','-O'],td/'audit/audit_artifacts.py',[td/'original',corpus,sources])
   fresh=json.loads((td/'audit/ARTIFACT_AUDIT_RESULTS.json').read_bytes());need(fresh['checks']==88 and fresh['expected_original_isolated_failures']==2,'fresh matrix scope')
   need(all(t['result']=='PASS' for t in fresh['tests']),'matrix failures')
   result['fresh_artifact_matrix_checks']=88;result['fresh_artifact_matrix_sha256']=digest((td/'audit/ARTIFACT_AUDIT_RESULTS.json').read_bytes())
  result.update(replay_performed=True,patch_reconstructed_accepted_members=11,expected_original_isolated_failures_reproduced=2,replay_checks=checks)
 print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':
 try:main()
 except Exception as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)

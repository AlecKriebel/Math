#!/usr/bin/env python3
from pathlib import Path
import datetime,hashlib,json,os,subprocess
R=Path(__file__).resolve().parent;root=R/'_local/extracted'
anchors=['--expected-manifest-sha256','6a3164a73be08b9c20c3b2fab5bdbcf1a4f1eb51ee1d8f7ce80184f41b8c6a22','--expected-context-sha256','6f66797c62c2b1d0c5d3e681eadf48bc80c839f7145961a3197174db1f0dd69c','--expected-snapshot-sha256','da2152816bbcd548e4db411ab57992c121009d935e2de59b3f6de93ae304a1d6']
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(R/'_local/tmp'));env.pop('PYTHONOPTIMIZE',None)
rows=[]
def run(mode,flags,label,program,args):
 r=subprocess.run(['python3','-B',*flags,str(program),*args],cwd=root,env=env,capture_output=True,text=True,timeout=60)
 if r.returncode==0:raise ValueError('False input accepted: '+label+' '+mode)
 rows.append({'mode':mode,'label':label,'returncode':r.returncode,'stdout_sha256':hashlib.sha256(r.stdout.encode()).hexdigest(),'stderr_tail':r.stderr[-600:]})
for mode,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
 wrong=list(anchors);wrong[1]='0'*64;run(mode,flags,'wrong_external_manifest_anchor',root/'verify.py',wrong)
 run(mode,flags,'anchors_are_mandatory',root/'verify.py',[])
 path=root/'current_edition/PROOF_CLASSIFICATION.md';old=path.read_bytes()
 try:path.write_bytes(old+b'\nTAMPERED');run(mode,flags,'actual_current_proof_changed',root/'verify.py',anchors)
 finally:path.write_bytes(old)
 path=root/'UNLISTED_PAYLOAD'
 try:path.write_bytes(b'unlisted');run(mode,flags,'unlisted_payload',root/'verify.py',anchors)
 finally:path.unlink()
 path=root/'current_edition/README.md';old=path.read_bytes()
 try:
  path.unlink();path.symlink_to(root/'original_submitted/README.md');run(mode,flags,'symlink_current_member',root/'verify.py',anchors)
 finally:
  path.unlink();path.write_bytes(old)
 for raw,args in [('root_intersection_family_check.py',['--inject-failure']),('reviews/candidate_adversary/verify_algebra.py',['--inject-failure','wrong-second-branch']),('reviews/candidate_adversary/verify_algebra.py',['--inject-failure','reverse-order']),('reviews/portable_quotient_diagnostics/checks.py',['--inject-failure']),('priority/structural_cross_challenge/durable_structural_checks.py',['--inject-failure'])]:run(mode,flags,'registered_program_false_control:'+raw+':'+str(args),root/raw,args)
 code="import runpy; m=runpy.run_path("+repr(str(root/'reviews/blind_source_reconstruction/checks.py'))+"); m['require'](False,'independent direct false predicate')"
 r=subprocess.run(['python3','-B',*flags,'-c',code],cwd=root,env=env,capture_output=True,text=True)
 if r.returncode==0:raise ValueError('Source reconstruction false predicate accepted')
 rows.append({'mode':mode,'label':'source_reconstruction_explicit_false_predicate','returncode':r.returncode,'stderr_tail':r.stderr[-500:]})
(R/'ARCHIVE_NEGATIVE_CONTROLS.json').write_text(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_rejected':True,'count':len(rows),'runs':rows,'scope':'Mutations were only to independently extracted own-folder copies and restored; source package untouched.'},indent=2)+'\n');print('all rejected',len(rows))

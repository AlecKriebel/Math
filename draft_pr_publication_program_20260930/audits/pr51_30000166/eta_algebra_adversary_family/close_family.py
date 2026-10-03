#!/usr/bin/env python3
"""ROOT-invoked self-only family closer. Does not grant acceptance authority."""
from pathlib import Path
import argparse,hashlib,json,stat,os
from datetime import datetime,timezone
F=Path(__file__).resolve().parent
MANIFEST='SELF_MANIFEST.json'
FILES=('INITIAL_INPUTS.json','RESEARCH_LOG.md','independent_exact_checks.py','capture_checks.py','independent_results.json','exact_checks_capture/SOURCE_PRELAUNCH.py','exact_checks_capture/PRELAUNCH.json','exact_checks_capture/CAPTURE.json','exact_checks_capture/stdout.bin','exact_checks_capture/stderr.bin','check_original_helper.py','original_helper_capture/PRELAUNCH.json','original_helper_capture/CAPTURE.json','original_helper_capture/stdout.bin','original_helper_capture/stderr.bin','FULL_INPUT_BINDINGS.json','PRIMARY_SOURCE_SCOPE.md','PROOF_AUDIT.md','REPORT.md','VERDICT.json','close_family.py','verify_closed_family.py','READY.md')
DIRS=('', 'exact_checks_capture', 'original_helper_capture')
def strict(p):
 def pairs(xs):
  d={}
  for k,v in xs:
   if k in d:raise ValueError('duplicate key: '+k)
   d[k]=v
  return d
 return json.loads(p.read_bytes(),object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def sha(b):return hashlib.sha256(b).hexdigest()
def verify_inputs():
 r=Path('/Users/alec/Documents/Math');rows=strict(F/'FULL_INPUT_BINDINGS.json')['files'];assert len(rows)==15
 for row in rows:
  p=r/row['path'];assert p.is_file() and not p.is_symlink();b=p.read_bytes()
  assert len(b)==row['bytes'] and sha(b)==row['sha256'] and oct(stat.S_IMODE(p.stat().st_mode))==row['mode']=='0o444'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--expected-report-sha256',required=True);a=ap.parse_args()
 assert not (F/MANIFEST).exists()
 actualfiles=[];actualdirs=[]
 for p in F.rglob('*'):
  assert not p.is_symlink()
  if p.is_file():actualfiles.append(str(p.relative_to(F)))
  elif p.is_dir():actualdirs.append(str(p.relative_to(F)))
  else:raise AssertionError('nonregular family member')
 assert set(actualfiles)==set(FILES) and set(actualdirs)==set(DIRS)-{''}
 assert sha((F/'REPORT.md').read_bytes())==a.expected_report_sha256
 v=strict(F/'VERDICT.json');assert v['status']=='PASS_ALREADY_SOLVED_EXACT_ETA_PRODUCT' and v['mandatory_corrections']==[] and v['root_acceptance_or_merge_authority'] is False
 r=strict(F/'independent_results.json');assert r['status']=='PASS' and type(r['assertions']) is int and r['assertions']==324186 and sum(r['by_family'].values())==r['assertions']
 for name,pid in [('exact_checks_capture',36555),('original_helper_capture',38799)]:
  cap=strict(F/name/'CAPTURE.json');assert cap['status']=='PASS' and type(cap['child_pid']) is int and cap['child_pid']==pid and type(cap['exit_code']) is int and cap['exit_code']==0 and cap['source_unchanged'] is True
  for channel in ('stdout','stderr'):
   p=F/name/(channel+'.bin');b=p.read_bytes();row=cap[channel]
   assert row['path']==str(p) and len(b)==row['bytes'] and sha(b)==row['sha256']
 verify_inputs()
 files=[]
 for n in sorted(FILES):
  p=F/n;b=p.read_bytes();p.chmod(0o444);files.append({'path':n,'bytes':len(b),'sha256':sha(b),'mode':'0o444'})
 record={'schema':'pr51-eta-algebra-adversary-self-only-closure/v1','created_utc':datetime.now(timezone.utc).isoformat(),'creator_pid':os.getpid(),'original_head':'8006dd5f134ad0a2fa930e7278d3cb17945f4201','files_count':len(files),'files':files,'directories':[{'path':d,'mode':'0o555'} for d in DIRS],'self_excluded':[{'path':MANIFEST,'mode':'0o444'}],'original_input_count':15,'no_original_or_native_changes':True,'root_acceptance_or_merge_authority':False,'qualification':'A self-only closure of an independent mathematical review; ROOT actual launch and whole readback are separate.'}
 p=F/MANIFEST;p.write_text(json.dumps(record,indent=2)+'\n');p.chmod(0o444)
 for d in sorted(DIRS,key=lambda x:-len(x)):(F/d).chmod(0o555)
 verify_inputs();print(json.dumps({'status':'PASS','manifest':str(p),'manifest_sha256':sha(p.read_bytes()),'payload_files':len(files),'scope':'Self-only independent math family; no merge authority'},indent=2))
if __name__=='__main__':main()

#!/usr/bin/env python3
"""Strict externally anchored inventory and exact replay of the independent audit."""
import argparse,hashlib,json,pathlib,stat,subprocess,sys
NAMES={'README.md','ADVERSARIAL_AUDIT.md','EXPANDED_LEMMAS.md','SOURCE_AUDIT.json','ACCEPTANCE.json','INDEPENDENT_RESULTS.json','AUTHOR_CONTROL_RESULTS.json','independent_check.py','audit_controls.py','verify_audit.py'}
def need(x,s):
 if not x:raise RuntimeError(s)
def unique(pairs):
 d={}
 for k,v in pairs:need(k not in d,'duplicate JSON key');d[k]=v
 return d
def verify(root,manifest,author_root=None,author_manifest=None,author_archive=None):
 need(root.is_dir() and not root.is_symlink(),'ordinary root required')
 need(stat.S_ISREG(manifest.lstat().st_mode),'ordinary manifest required')
 need(root.resolve() not in manifest.resolve().parents,'manifest must be external')
 need({p.name for p in root.iterdir()}==NAMES,'strict inventory mismatch')
 for p in root.iterdir():need(stat.S_ISREG(p.lstat().st_mode),'regular files only')
 raw=manifest.read_bytes();m=json.loads(raw,object_pairs_hook=unique)
 need(set(m)=={'schema','problem_id','files'} and m['schema']=='independent-audit-v1','manifest schema')
 need(type(m['problem_id']) is int and m['problem_id']==30001702,'manifest problem')
 need(type(m['files']) is list and len(m['files'])==len(NAMES),'manifest count')
 need(all(type(r) is dict and set(r)=={'path','bytes','sha256'} for r in m['files']),'manifest records')
 need({r['path'] for r in m['files']}==NAMES,'manifest inventory')
 for r in m['files']:
  need(type(r['bytes']) is int and r['bytes']>=0,'byte count type')
  need(type(r['sha256']) is str and len(r['sha256'])==64 and all(c in '0123456789abcdef' for c in r['sha256']),'digest syntax')
  b=(root/r['path']).read_bytes();need(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],'hash or byte mismatch')
 common=[sys.executable,'-I','-B']+(['-O'] if sys.flags.optimize else [])
 p=subprocess.run(common+[str(root/'independent_check.py')],cwd='/tmp',capture_output=True,text=True,timeout=120)
 need(p.returncode==0 and not p.stderr,'independent replay failed')
 need(p.stdout==(root/'INDEPENDENT_RESULTS.json').read_text(),'independent exact replay mismatch')
 report=json.loads(p.stdout);need(report['status']=='PARTIAL_UNRESOLVED' and report['universal_factorial_bound_proved'] is False,'independent scope mismatch')
 need(report['independent_arithmetic_checks']==11475 and report['independent_product_checks']==900,'independent check counts')
 acc=json.loads((root/'ACCEPTANCE.json').read_text());need(acc['verdict']=='ACCEPTED_PARTIAL_UNRESOLVED' and acc['universal_solution_accepted'] is False,'acceptance scope')
 need(acc['original_author_payload_modified'] is False and acc['correction_required'] is False,'unexpected correction state')
 controls=json.loads((root/'AUTHOR_CONTROL_RESULTS.json').read_text())
 need(controls['executions']==78 and controls['expected_negative']==72,'control counts')
 have=[x is not None for x in [author_root,author_manifest,author_archive]]
 need(all(have) or not any(have),'supply all three author input options')
 replayed=False
 if all(have):
  cmd=common+[str(root/'audit_controls.py'),'--author-root',str(author_root),'--manifest',str(author_manifest),'--archive',str(author_archive)]
  p=subprocess.run(cmd,cwd='/tmp',capture_output=True,text=True,timeout=300)
  need(p.returncode==0 and not p.stderr,'author controls replay failed')
  need(p.stdout==(root/'AUTHOR_CONTROL_RESULTS.json').read_text(),'author controls exact replay mismatch');replayed=True
 return {'verified':True,'problem_id':30001702,'status':'ACCEPTED_PARTIAL_UNRESOLVED','optimized':bool(sys.flags.optimize),'payload_files':len(NAMES),'manifest_sha256':hashlib.sha256(raw).hexdigest(),'independent_exact_replay':True,'author_controls_replayed':replayed}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=pathlib.Path,default=pathlib.Path(__file__).absolute().parent);p.add_argument('--manifest',type=pathlib.Path,required=True)
 p.add_argument('--author-root',type=pathlib.Path);p.add_argument('--author-manifest',type=pathlib.Path);p.add_argument('--author-archive',type=pathlib.Path);a=p.parse_args()
 print(json.dumps(verify(a.root.absolute(),a.manifest.absolute(),*(x.absolute() if x else None for x in [a.author_root,a.author_manifest,a.author_archive])),indent=2,sort_keys=True))

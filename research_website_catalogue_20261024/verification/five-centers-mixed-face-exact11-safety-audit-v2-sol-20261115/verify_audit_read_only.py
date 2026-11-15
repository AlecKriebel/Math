"""Standalone pure immutable audit/source custody. No project import, runtime, network, subprocess or writes."""
from pathlib import Path,PurePosixPath
import hashlib,json,stat,sys
D=Path(__file__).resolve().parent
N=0

def need(ok,label):
 global N
 N+=1
 if not ok:raise RuntimeError(label)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):
 p=Path(p);O=D.parent/'five-centers-mixed-face-production-integration-preparation-v2-sol-20261115'
 need((D in p.parents or O in p.parents) and p.resolve()==p and stat.S_ISREG(p.lstat().st_mode),'only own or reviewed immutable regular files')
 return p.read_bytes()
def obj(p):return json.loads(read(p))
def pin(p,r):
 b=read(p);need(len(b)==r['bytes'] and sha(b)==r['SHA256'],'whole byte pin');return b
def safe(n):
 p=PurePosixPath(n);need(p.parts and str(p)==n and not p.is_absolute() and '..' not in p.parts and '\\' not in n,'exact safe path');return p
def extent(root):
 need(root.resolve()==root and stat.S_ISDIR(root.lstat().st_mode),'real ordinary root')
 files=[];dirs=[]
 for p in root.rglob('*'):
  mode=p.lstat().st_mode;need(p.resolve()==p and (stat.S_ISDIR(mode) or stat.S_ISREG(mode)),'closed regular namespace')
  (files if stat.S_ISREG(mode) else dirs).append(p.relative_to(root).as_posix())
 return sorted(files),sorted(dirs)
def main():
 need(sys.argv[1:] in [[],['--preseal']],'only bounded pure modes');preseal=bool(sys.argv[1:])
 bindings=obj(D/'INPUT_BINDINGS.json');ib=pin(D/'INITIAL_SEAL.json',bindings['initial_seal'])
 need(sha(ib)=='a492dfb546ebe2a67fca1ace39ff7d618ee83fe3505ba7fb4f00b0ac748fc50b','informed initial unchanged')
 for r in json.loads(ib)['files']:pin(r['path'],r)
 O=Path(bindings['preparation_root']);sb=pin(O/'PREPARATION_SEAL.json',bindings['preparation_final_seal']);s=json.loads(sb)
 mb=pin(O/'PREPARATION_MANIFEST.json',bindings['preparation_manifest']);m=json.loads(mb)
 need(sha(mb)==s['MANIFEST_SHA256'] and sha(read(O/'PREPARATION_CLOSURE.json'))==s['CLOSURE_SHA256'],'whole immutable source terminal controls')
 names=[]
 for r in m['files']:pin(O/safe(r['path']),r);names.append(r['path'])
 f,d=extent(O);term=['PREPARATION_CLOSURE.json','PREPARATION_MANIFEST.json','PREPARATION_SEAL.json']
 need(len(names)==len(set(names))==75 and f==sorted(names+term) and d==m['directories']==s['owned_directories'],'exact current78files6dirs')
 need(m['future_subtree_exclusions']==[] and m['exact_root_terminal_exclusions']==term,'no source future exclusions')
 for r in bindings['current_code_pins']:pin(r['path'],r)
 pin(O/'RUNTIME_CONTRACT.json',bindings['runtime_contract_pin']);pin(O/'SEALED_NAMESPACE_CONTRACT.json',bindings['source_namespace_contract_pin'])
 need(read(D/'PREPARATION_PURE_CLOSURE.json')==read(D/'PREPARATION_PURE_CLOSURE_OPTIMIZED.json'),'whole normal/O outputs identical')
 need(obj(D/'PREPARATION_PURE_CLOSURE.json')['checks']==505,'actual current pure closure')
 controls=obj(D/'CONTROL_RESULTS.json');need(controls['status']=='PASS_FRESH_INDEPENDENT_CORRECTION_NAMESPACE_RUNTIME_CONTROLS' and [len(r['negative_cases']) for r in controls['results']]==[21,20],'retained fresh own negative controls')
 need(obj(D/'WRAPPER_CONTROL_RESULTS.json')['status']=='PASS_FRESH_EXACT_CHANGED_AUDIT_WRAPPER','retained changed wrapper result')
 verdict=obj(D/'VERDICT.json');need(verdict['status']=='PASS_FOR_ROOT_REVIEW_UNDER_STATED_ASSUMPTIONS' and verdict['production_installation_authority'] is False and verdict['publication_authority'] is False,'qualified verdict grants no production authority')
 for n in ['SOURCE_CUSTODY','PREPARATION_PURE_CLOSURE','PREPARATION_PURE_CLOSURE_OPTIMIZED','HELD_PREFLIGHT','CONTROL_RESULTS','WRAPPER_CONTROL_RESULTS']:
  need(read(D/(n+'.stderr'))==b'','complete empty stderr evidence')
 if not preseal:
  seal=json.loads(read(D/'FINAL_SEAL.json'));manifest_body=read(D/'MANIFEST.json');need(sha(manifest_body)==seal['MANIFEST_SHA256'],'same owned final manifest buffer')
  manifest=json.loads(manifest_body);names=[]
  for r in manifest['files']:pin(D/safe(r['path']),r);names.append(r['path'])
  f,d=extent(D);need(len(names)==len(set(names))==seal['owned_payload_count'] and f==sorted(names+['MANIFEST.json','FINAL_SEAL.json']) and d==manifest['directories'],'complete own file/directory namespace')
  need(manifest['exact_root_terminal_exclusions']==['MANIFEST.json','FINAL_SEAL.json'] and manifest['future_subtree_exclusions']==[],'exact own root terminal exclusions only')
  need(sha(read(D/'REPORT.md'))==seal['REPORT_SHA256'] and sha(read(D/'VERDICT.json'))==seal['VERDICT_SHA256'],'full report and custom verdict')
 print(json.dumps({'status':'PASS_INFORMED_V2_AUDIT_CUSTODY','mode':'preseal' if preseal else 'final','checks':N,'review_verdict':'PASS_FOR_ROOT_REVIEW_UNDER_STATED_ASSUMPTIONS','source_final_seal_SHA256':sha(sb),'actual_sibling_runtime_live_website_Git_network_subprocess_or_writes':False,'project_or_control_campaign_imports':False,'production_authority':False},sort_keys=True))
if __name__=='__main__':main()

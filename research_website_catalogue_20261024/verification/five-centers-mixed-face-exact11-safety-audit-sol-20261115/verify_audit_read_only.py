"""Standalone read-only audit custody. No project imports, subprocess, network, controls or writes."""
from pathlib import Path,PurePosixPath
import hashlib,json,stat,sys
D=Path(__file__).resolve().parent
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
N=0

def need(ok,label):
 global N
 N+=1
 if not ok:raise ValueError(label)
def read(path):
 path=Path(path)
 need(path!=W and W not in path.parents and '.git' not in path.parts,'never live website or real Git')
 need(path.resolve()==path and stat.S_ISREG(path.lstat().st_mode),'real regular whole file')
 return path.read_bytes()
def sha(body):return hashlib.sha256(body).hexdigest()
def pin(path,row):
 body=read(path);need(len(body)==row['bytes'] and sha(body)==row['SHA256'],'whole-byte pin '+str(path));return body
def obj(path):return json.loads(read(path))
def safe(name):
 p=PurePosixPath(name)
 need(str(p)==name and not p.is_absolute() and '..' not in p.parts and '\\' not in name and p.parts,'exact safe relative name')
 return p
def namespace(root):
 need(root.resolve()==root and stat.S_ISDIR(root.lstat().st_mode),'real directory root')
 files=[];dirs=[]
 for p in root.rglob('*'):
  m=p.lstat().st_mode;n=p.relative_to(root).as_posix()
  need(p.resolve()==p and (stat.S_ISREG(m) or stat.S_ISDIR(m)),'strict regular namespace '+n)
  (files if stat.S_ISREG(m) else dirs).append(n)
 return sorted(files),sorted(dirs)
def main():
 need(sys.argv[1:] in [[],['--preseal']],'only pure custody modes')
 preseal=sys.argv[1:]==['--preseal']
 bindings=obj(D/'INPUT_BINDINGS.json')
 initial=json.loads(pin(D/'INITIAL_SEAL.json',bindings['initial_seal']))
 for key in ['initial_expectations','research_log_at_initial_checkpoint']:pin(initial[key]['path'],initial[key])
 O=Path(bindings['preparation_root'])
 source_seal=json.loads(pin(O/'PREPARATION_SEAL.json',bindings['preparation_final_seal']))
 source_manifest=json.loads(pin(O/'PREPARATION_MANIFEST.json',bindings['preparation_manifest']))
 need(source_seal['MANIFEST_SHA256']==bindings['preparation_manifest']['SHA256'],'same authenticated preparation manifest')
 need(sha(read(O/'PREPARATION_CLOSURE.json'))==source_seal['CLOSURE_SHA256'],'source closure pin')
 for row in source_manifest['files']:pin(O/safe(row['path']),row)
 for row in obj(O/'REFERENCE_BINDINGS.json')['files']:
  body=pin(row['path'],row)
  if 'copy' in row:need(body==read(O/safe(row['copy'])),'whole unnormalized reference copy')
 for row in bindings['current_code_pins']:pin(row['path'],row)
 for observation in obj(D/'CURRENT_NAMESPACE_OBSERVATIONS.json')['observations']:
  files,dirs=namespace(Path(observation['path']))
  need(files==observation['observed_complete_files'] and dirs==observation['observed_complete_directories'],'exact full current packet file and directory extent')
 need(obj(D/'CONTROL_RESULTS_V2.json')['status']=='COMPLETED_WITH_CONFIRMED_STRICT_NAMESPACE_BLOCKER','retained actual adverse control result')
 verdict=obj(D/'VERDICT.json')
 need(verdict['status']=='NO_GO_STRICT_NAMESPACE_REQUIREMENT' and verdict['production_installation_authority'] is False,'source verdict grants no production authority')
 if not preseal:
  seal_bytes=read(D/'FINAL_SEAL.json');seal=json.loads(seal_bytes)
  mb=read(D/'MANIFEST.json');need(sha(mb)==seal['MANIFEST_SHA256'],'own immutable final manifest buffer')
  manifest=json.loads(mb);paths=[]
  for row in manifest['files']:
   pin(D/safe(row['path']),row);paths.append(row['path'])
  need(len(paths)==len(set(paths))==seal['owned_payload_count'],'exact own payload count')
  files,dirs=namespace(D)
  need(files==sorted(paths+['MANIFEST.json','FINAL_SEAL.json']) and dirs==manifest['directories'],'complete own files and directories, exact root terminals only')
  need(manifest['exact_root_terminal_exclusions']==['MANIFEST.json','FINAL_SEAL.json'],'no future subtree exclusions')
  need(sha(read(D/'REPORT.md'))==seal['REPORT_SHA256'] and sha(read(D/'VERDICT.json'))==seal['VERDICT_SHA256'],'full report and literal verdict')
 print(json.dumps({'status':'PASS_AUDIT_CUSTODY_WITH_RETAINED_NO_GO','mode':'preseal' if preseal else 'final','checks':N,'review_verdict':'NO_GO_STRICT_NAMESPACE_REQUIREMENT','source_preparation_seal_SHA256':bindings['preparation_final_seal']['SHA256'],'reviewed_code_controls_or_source_campaigns_executed':False,'website_real_git_network_subprocess_or_writes':False,'production_authority':False},sort_keys=True))
if __name__=='__main__':main()

"""Standalone final audit custody; owned held data only, no live/Git/writer programme execution or writes."""
from pathlib import Path,PurePosixPath
import hashlib,json,stat,sys
D=Path(__file__).resolve().parent;S=D.parent/'supported-cycle-focal-private-stage-sol-20261115';N=0

def need(ok,label):
 global N
 N+=1
 if not ok:raise RuntimeError(label)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):
 p=Path(p);need((D in p.parents or S in p.parents) and p.resolve()==p and stat.S_ISREG(p.lstat().st_mode),'only own or sealed writer ordinary held file');return p.read_bytes()
def obj(p):return json.loads(read(p))
def pin(p,r):
 b=read(p);need(len(b)==r['bytes'] and sha(b)==r['SHA256'],'whole exact bytes');return b
def safe(n):
 p=PurePosixPath(n);need(p.parts and str(p)==n and not p.is_absolute() and '..' not in p.parts and '\\' not in n,'exact safe name');return p
def extent(root):
 need(root in [D,S],'bounded own/writer extent');need(root.resolve()==root and stat.S_ISDIR(root.lstat().st_mode),'real ordinary root');files=[];dirs=[]
 for p in root.rglob('*'):
  mode=p.lstat().st_mode;need(p.resolve()==p and (stat.S_ISREG(mode) or stat.S_ISDIR(mode)),'ordinary closed entries');(files if stat.S_ISREG(mode) else dirs).append(p.relative_to(root).as_posix())
 return sorted(files),sorted(dirs)
def earlier(manifest,seal,digest):
 sb=read(D/seal);need(sha(sb)==digest,'earlier immutable phase seal');s=json.loads(sb);mb=read(D/manifest);need(sha(mb)==s['MANIFEST_SHA256'],'earlier complete phase manifest')
 for r in json.loads(mb)['files']:pin(D/safe(r['path']),r)
def main():
 need(sys.argv[1:] in [[],['--preseal']],'only pure modes');preseal=bool(sys.argv[1:])
 earlier('INITIAL_MANIFEST.json','INITIAL_SEAL.json','709ceeaf5c386f2ffd24682a919fd100d51224b4207e43f68c361ab8e4c8b21b')
 earlier('BASELINE_MANIFEST.json','BASELINE_SEAL.json','9d319d461f8c392ff828536c6ea60898998a9320cfb630cb9d9a2cab5f1f4c2b')
 bindings=obj(D/'INPUT_BINDINGS.json');sb=pin(S/'FINAL_SEAL.json',bindings['writer_FINAL_SEAL']);need(sha(sb)=='edf8e4e64ea345e950f6d94e678b4d6c8530df37089e80ef6681a519b7fedf54','exact original writer FINAL retained')
 seal=json.loads(sb);mb=pin(S/'OWNED_MANIFEST.json',bindings['writer_OWNED_MANIFEST']);need(sha(mb)==seal['manifest']['SHA256'],'same sealed writer manifest buffer');m=json.loads(mb)
 for n,r in m['payloads'].items():pin(S/safe(n),r)
 files,dirs=extent(S);need(files==sorted(list(m['payloads'])+['OWNED_MANIFEST.json','FINAL_SEAL.json']) and dirs==m['directories'],'complete exact original writer file and directory custody')
 need(type(m['recursive_basename_or_future_subtree_exclusions']) is list and m['recursive_basename_or_future_subtree_exclusions']==[],'literal empty-list schema retained, no normalization')
 comp=obj(D/'INDEPENDENT_COMPARISON_V2.json');need(comp['status']=='COMPLETED_NO_GO_NATIVE_INTEGRATION_ADAPTER' and len(comp['findings'])==2,'retained actual independent findings')
 for e in comp['article_evidence']:pin(e['actual_HTML_pin']['path'],e['actual_HTML_pin'])
 need(obj(D/'WRITER_PURE_CLOSURE.json')['checks']==289283,'retained actual safe writer pure result')
 verdict=obj(D/'VERDICT.json');need(verdict['status']=='NO_GO_NATIVE_FRAME_AND_LOCAL_HEAD_ADAPTER' and verdict['source_or_stage_repaired_by_auditor'] is False and verdict['production_installation_authority'] is False,'narrow routine adapter verdict grants no authority')
 for name in ['INDEPENDENT_COMPARISON_V2','WRITER_PURE_CLOSURE']:need(read(D/(name+'.stderr'))==b'','complete successful review stderr')
 need(bool(read(D/'INDEPENDENT_COMPARISON.stderr')),'retained original reviewer harness failure stream')
 if not preseal:
  final=obj(D/'FINAL_SEAL.json');body=read(D/'FINAL_MANIFEST.json');need(sha(body)==final['MANIFEST_SHA256'],'same full final audit manifest buffer');m=json.loads(body);names=[]
  for r in m['files']:pin(D/safe(r['path']),r);names.append(r['path'])
  files,dirs=extent(D);need(len(names)==len(set(names))==final['owned_payload_count'] and files==sorted(names+['FINAL_MANIFEST.json','FINAL_SEAL.json']) and dirs==m['directories'],'complete final own file and directory namespace')
  need(m['exact_root_terminal_exclusions']==['FINAL_MANIFEST.json','FINAL_SEAL.json'] and m['future_subtree_exclusions']==[],'only exact final root terminals, no future directories')
  need(sha(read(D/'REPORT.md'))==final['REPORT_SHA256'] and sha(read(D/'VERDICT.json'))==final['VERDICT_SHA256'],'full report and literal custom verdict')
 print(json.dumps({'status':'PASS_FINAL_AUDIT_CUSTODY_WITH_RETAINED_ADAPTER_NO_GO','mode':'preseal' if preseal else 'final','checks':N,'integration_verdict':'NO_GO_NATIVE_FRAME_AND_LOCAL_HEAD_ADAPTER','writer_FINAL_SHA256':sha(sb),'initial_and_actual_baseline_payloads_unchanged':True,'new_source_science_renderer_controls_live_Git_network_subprocess_or_writes':False,'publication_authority':False},sort_keys=True))
if __name__=='__main__':main()

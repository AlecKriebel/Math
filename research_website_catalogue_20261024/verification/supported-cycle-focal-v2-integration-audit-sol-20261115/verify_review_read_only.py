"""Default strict final custody; owned/source/pinned packets only, no live website/Git."""
from pathlib import Path
import hashlib,json,stat,sys
D=Path(__file__).resolve().parent;checks=0
def need(ok,label):
 global checks
 checks+=1
 if not ok:raise RuntimeError(label)
def read(p):
 p=Path(p);need(p.resolve()==p and stat.S_ISREG(p.lstat().st_mode),'ordinary real file '+str(p));return p.read_bytes()
def obj(p):return json.loads(read(p))
def pin(b):return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}
def extent(root):
 need(root.resolve()==root and stat.S_ISDIR(root.lstat().st_mode),'ordinary root')
 fs=[];ds=[]
 for q in root.rglob('*'):
  rel=q.relative_to(root).as_posix();m=q.lstat().st_mode
  if stat.S_ISDIR(m):ds.append(rel)
  else:need(stat.S_ISREG(m),'ordinary namespace entry');fs.append(rel)
 need(len(fs)==len(set(fs)) and len(ds)==len(set(ds)),'duplicate actual file/directory identity')
 return sorted(fs),sorted(ds)
def exact_namespace(root,names,dirs):
 fs,ds=extent(root)
 need(len(names)==len(set(names)) and len(dirs)==len(set(dirs)),'duplicate expected file/directory identity')
 # Both full relative path lists use the same explicit Python Unicode string lexical rule.
 need(fs==sorted(names) and ds==sorted(dirs),'exact whole file/directory identity')
def payloads(root,records):
 for n,r in records.items():need(pin(read(root/n))=={k:r[k] for k in ['bytes','SHA256']},'whole pinned payload '+n)
need(sys.argv[1:] in [[],['--preseal']],'finite read-only modes')
for name in ['SOURCE_CLOSED_EXTENTS.json','PRIOR_CLOSED_EXTENTS.json']:
 for record in obj(D/name):
  root=Path(record['root']);exact_namespace(root,list(record['files']),record['directories']);payloads(root,record['files'])
bindings=obj(D/'WRITER_CURRENT_BINDINGS.json');current=Path(bindings['source_root']);names=[r['path'] for r in bindings['files']];rows={r['path']:r for r in bindings['files']}
for root in [current,D/'reviewed-writer']:
 exact_namespace(root,names,bindings['directories']);payloads(root,rows)
for b in obj(D/'INPUT_BINDINGS.json'):
 original=read(b['source']);copy=read(D/b['copy']);need(original==copy and pin(copy)=={k:b[k] for k in ['bytes','SHA256']},'whole original literal binding')
for manifest,seal in [('INITIAL_MANIFEST.json','INITIAL_SEAL.json'),('BASELINE_MANIFEST.json','BASELINE_SEAL.json')]:
 mb=read(D/manifest);s=obj(D/seal);need(pin(mb)==s['manifest'],'earlier immutable manifest')
 m=json.loads(mb);paths=[r['path'] for r in m['files']];need(len(paths)==len(set(paths)),'earlier unique records')
 payloads(D,{r['path']:r for r in m['files']})
for output in ['WRITER_DEFAULT_CLOSURE','INDEPENDENT_COMPARISON_V2']:
 need(read(D/(output+'.stderr'))==b'','actual safe successful empty stderr')
 good=obj(D/(output+'.stdout.json'));need(good['production_authority'] is False and good['canonical_url'] is None and good['AA'] is None,'actual safe private closure')
need(read(D/'INDEPENDENT_COMPARISON.stdout.json')==b'' and b'actual ten recorded process objects' in read(D/'INDEPENDENT_COMPARISON.stderr'),'original failed own execution retained')
error=obj(D/'REVIEWER_PROCESS_COUNT_ERROR.json');need(error['actual_process_exit']==1,'original actual failure exit retained')
old=read(D/'compare_integration_read_only.py');new=read(D/'compare_integration_read_only_v2.py')
need(new==old.replace(b"need(len(history)==10,'actual ten recorded process objects')",b"need(len(history)==9,'actual nine recorded process objects')"),'exact only own helper correction')
v=obj(D/'VERDICT.json');need(v['status']=='PASS_INFORMED_CORRECTIVE_V2_INTEGRATION_PENDING_ROOT_ADOPTION','literal bounded verdict')
need(v['root_adoption'] is False and v['production_installation_authority'] is False and v['canonical_url'] is None and v['AA'] is None and v['follow_up'] is None,'authority null/false boundaries')
if sys.argv[1:]:
 contract=obj(D/'PRESEAL_NAMESPACE.json');exact_namespace(D,contract['files'],contract['directories']);mode='preseal'
else:
 sb=read(D/'FINAL_SEAL.json');s=json.loads(sb);mb=read(D/'MANIFEST.json');need(pin(mb)==s['manifest'],'same-buffer final manifest authentication');m=json.loads(mb)
 need(m['exact_root_terminal_exclusions']==['MANIFEST.json','FINAL_SEAL.json'] and m['future_subtree_exclusions']==[],'only exact root terminal exclusions')
 names=[r['path'] for r in m['files']]+['MANIFEST.json','FINAL_SEAL.json'];exact_namespace(D,names,m['directories']);payloads(D,{r['path']:r for r in m['files']})
 need(s['root_adoption'] is False and s['production_installation_authority'] is False,'final authority separation');mode='final'
print(json.dumps({'status':'PASS_INFORMED_CORRECTIVE_V2_AUDIT_CUSTODY','mode':mode,'checks':checks,'original_source_editorial_files':775,'original_stage_audit_files':[1335,1352],'V2_files':107,'whole_initial_and_baseline_payloads_unchanged':True,'failed_own_count_history_preserved':True,'strict_full_path_lexical_order_and_duplicate_checks':True,'science_render_control_website_Git_network_subprocess_or_writes':False,'root_adoption':False,'production_installation_authority':False,'canonical_url':None,'AA':None,'follow_up':None},sort_keys=True))

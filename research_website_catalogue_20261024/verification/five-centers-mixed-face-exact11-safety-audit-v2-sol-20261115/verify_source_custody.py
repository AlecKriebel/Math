"""Independent v2 source/copy custody; no reviewed import, original descriptors, runtime or live paths."""
from pathlib import Path,PurePosixPath
import ast,difflib,hashlib,json,stat
D=Path(__file__).resolve().parent
O=D.parent/'five-centers-mixed-face-production-integration-preparation-v2-sol-20261115'
N=0

def need(ok,label):
 global N
 N+=1
 if not ok:raise RuntimeError(label)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):
 p=Path(p);need((p==D or D in p.parents or O in p.parents) and p.resolve()==p and stat.S_ISREG(p.lstat().st_mode),'only own or reviewed immutable ordinary file')
 return p.read_bytes()
def obj(p):return json.loads(read(p))
def pin(p,r):
 b=read(p);need(len(b)==r['bytes'] and sha(b)==r['SHA256'],'whole byte pin '+str(p));return b
def extent(root):
 files=[];dirs=[]
 for p in root.rglob('*'):
  m=p.lstat().st_mode;need(p.resolve()==p and (stat.S_ISREG(m) or stat.S_ISDIR(m)),'strict regular file/directory')
  (files if stat.S_ISREG(m) else dirs).append(p.relative_to(root).as_posix())
 return sorted(files),sorted(dirs)
def fn(tree,name):return next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
def main():
 initial=read(D/'INITIAL_SEAL.json');need(sha(initial)=='a492dfb546ebe2a67fca1ace39ff7d618ee83fe3505ba7fb4f00b0ac748fc50b','immutable informed initial')
 for r in json.loads(initial)['files']:pin(r['path'],r)
 sb=read(O/'PREPARATION_SEAL.json');need(len(sb)==2643 and sha(sb)=='ef1aa965e73ce8738dea1b969465a3bb9ba0f9291ad133cb0c989f5524fc635d','parent immutable FINAL')
 s=json.loads(sb);mb=read(O/'PREPARATION_MANIFEST.json');need(len(mb)==12804 and sha(mb)==s['MANIFEST_SHA256']=='201bed9aaf3fd0efd538f97c27388e9ca8bd29972a283f3fe33ffc16594d2e74','same manifest buffer')
 m=json.loads(mb);paths=[]
 for r in m['files']:
  p=PurePosixPath(r['path']);need(str(p)==r['path'] and not p.is_absolute() and '..' not in p.parts,'exact safe name');pin(O/r['path'],r);paths.append(r['path'])
 files,dirs=extent(O);term=['PREPARATION_CLOSURE.json','PREPARATION_MANIFEST.json','PREPARATION_SEAL.json']
 need(len(paths)==len(set(paths))==75 and files==sorted(paths+term),'exact78 file extent')
 need(dirs==m['directories']==s['owned_directories'] and m['future_subtree_exclusions']==[],'exact6 directories, no future exclusions')
 need(sha(read(O/'PREPARATION_CLOSURE.json'))==s['CLOSURE_SHA256'],'complete terminal closure')
 prior=obj(D/'prior-no-go'/'VERDICT.json');oldpins={Path(r['path']).name:r for r in prior['current_code_pins']};comparison=obj(O/'CODE_COMPARISON.json');diff=[];pins=[]
 for r in comparison['files']:
  name=r['file'];a=read(O/'history/v1'/name);b=read(O/name)
  need((len(a),sha(a),len(b),sha(b))==(r['original_bytes'],r['original_SHA256'],r['current_bytes'],r['current_SHA256']),'whole old/current executable')
  key=Path(name).name;need(sha(a)==oldpins[key]['SHA256'],'old code matches presealed exact prior pin')
  diff.extend(difflib.unified_diff(a.decode().splitlines(keepends=True),b.decode().splitlines(keepends=True),fromfile='original79dd/'+name,tofile='corrective-v2/'+name))
  pins.append({'path':str(O/name),'bytes':len(b),'SHA256':sha(b)})
 need(sum(r['bytes'] for r in pins)==76890,'all6 full bodies')
 db=read(O/'CODE_DIFF_FROM_V1.patch');need(''.join(diff).encode()==db and len(db)==55998 and sha(db)==s['CODE_DIFF_SHA256'],'whole complete diff independently recomputed')
 a=ast.parse(read(O/'history/v1/exact11_lib.py'));b=ast.parse(read(O/'exact11_lib.py'));c=ast.parse(read(O/'verify_preparation.py'))
 for name in ['owned_entry','write_complete','validate_owned_buffer','unlink_owned','publish_buffer','parse_index']:
  need(ast.dump(fn(a,name),include_attributes=False)==ast.dump(fn(b,name),include_attributes=False),'accepted complete safety/parser AST '+name)
 for name in ['extent','closed_namespace','runtime_custody']:
  need(ast.dump(fn(b,name),include_attributes=False)==ast.dump(fn(c,name),include_attributes=False),'shared complete correction AST '+name)
 for name in ['FINAL_SEAL.json','REPORT.md','VERDICT.json']:
  need(read(O/'inputs'/('safety-v1-'+name))==read(D/'prior-no-go'/name),'complete original NO GO literal copy')
 refs=read(O/'REFERENCE_BINDINGS.json');need(sha(refs)=='8e53208ab8512ef0a25a8d48adf79d90f8b538b8987167bdd0ba631ba339ea09','all84 original metadata unchanged')
 for r in json.loads(refs)['files']:
  if 'copy' in r:pin(O/r['copy'],r)
 oldmanifest=obj(D/'prior-no-go/MANIFEST.json');row=next(r for r in oldmanifest['files'] if r['path']=='CURRENT_NAMESPACE_OBSERVATIONS.json')
 obs=json.loads(pin(O/'inputs/safety-v1-CURRENT_NAMESPACE_OBSERVATIONS.json',row));contract=obj(O/'SEALED_NAMESPACE_CONTRACT.json')
 need(contract['source_observation_SHA256']==row['SHA256'],'prior whole directory observation authenticated')
 for kind,i in [('writer',1),('audit',2)]:need(contract[kind+'_directories']==obs['observations'][i]['observed_complete_directories'],'exact retained directory list '+kind)
 need('inputs' in contract['writer_directories'],'legitimate empty writer inputs declared')
 need(sha(read(O/'RUNTIME_CONTRACT.json'))==s['runtime_contract_SHA256'],'whole finite sibling runtime schema')
 print(json.dumps({'status':'PASS_INDEPENDENT_V2_STRICT_SOURCE_CUSTODY','checks':N,'files':files,'directories':dirs,'current_code_pins':pins,'whole_current_code_bytes':76890,'whole_diff_bytes':55998,'six_accepted_safety_ASTs_equal':True,'three_shared_correction_ASTs_equal':True,'prior_NO_GO_and_initial_unchanged':True,'literal_reference_descriptors_retained':84,'historical_external_descriptors_followed':False,'runtime_or_live_paths_inspected':False},indent=2))
if __name__=='__main__':main()

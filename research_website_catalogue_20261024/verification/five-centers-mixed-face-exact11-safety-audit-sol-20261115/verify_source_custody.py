"""Independent source/data custody only; no imports of reviewed code, subprocess, writes or live paths."""
from pathlib import Path, PurePosixPath
import ast,difflib,hashlib,json,stat
D=Path(__file__).resolve().parent
O=D.parent/'five-centers-mixed-face-production-integration-preparation-sol-20261115'
OLD=D.parent/'lefschetz-link-production-integration-preparation-v2-sol-20261115'
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
N=0

def need(ok,label):
 global N
 N+=1
 if not ok:raise ValueError(label)
def read(p):
 p=Path(p)
 need(p!=W and W not in p.parents and '.git' not in p.parts,'never live website or real Git')
 need(p.resolve()==p and stat.S_ISREG(p.lstat().st_mode),'real regular held file')
 return p.read_bytes()
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p,row):
 b=read(p);need(len(b)==row['bytes'] and sha(b)==row['SHA256'],'whole bytes '+str(p));return b
def obj(p):return json.loads(read(p))
def full_namespace(root):
 files=[];dirs=[]
 need(root.resolve()==root and stat.S_ISDIR(root.lstat().st_mode),'real packet root')
 for p in root.rglob('*'):
  mode=p.lstat().st_mode;n=p.relative_to(root).as_posix()
  need(p.resolve()==p and (stat.S_ISREG(mode) or stat.S_ISDIR(mode)),'regular exact namespace '+n)
  (files if stat.S_ISREG(mode) else dirs).append(n)
 return sorted(files),sorted(dirs)
def main():
 sb=read(O/'PREPARATION_SEAL.json');need(len(sb)==2434 and sha(sb)=='79dd372023c18a2c890ef7c29ec48e3c4ddcf4453ac406764aa85a12e8bab52a','parent immutable final')
 seal=json.loads(sb)
 mb=read(O/'PREPARATION_MANIFEST.json');need(len(mb)==7898 and sha(mb)==seal['MANIFEST_SHA256']=='aecec8144325bcdd278218d66b2c176700defef2f2ff5d499750bf4fe977b87f','manifest from same buffer')
 manifest=json.loads(mb);term=['PREPARATION_MANIFEST.json','PREPARATION_SEAL.json','PREPARATION_CLOSURE.json']
 need(manifest['exact_terminal_exclusions']==term,'exact root terminals')
 need(sha(read(O/term[2]))==seal['CLOSURE_SHA256'],'terminal closure pin')
 paths=[];expected_dirs=set()
 for row in manifest['files']:
  p=PurePosixPath(row['path']);need(str(p)==row['path'] and not p.is_absolute() and '..' not in p.parts,'exact safe path')
  pin(O/row['path'],row);paths.append(row['path'])
  expected_dirs|={str(q) for q in p.parents if str(q)!='.'}
 files,dirs=full_namespace(O)
 need(len(paths)==len(set(paths))==46 and files==sorted(paths+term),'all49 exact file names')
 need(dirs==sorted(expected_dirs),'all exact directories; no future carveout')
 refs=obj(O/'REFERENCE_BINDINGS.json')
 for row in refs['files']:
  b=pin(row['path'],row)
  if 'copy' in row:need(b==read(O/row['copy']),'whole literal copied metadata')
 comparison=obj(O/'CODE_COMPARISON.json');diff=[];codepins=[]
 for row in comparison['files']:
  name=row['file'];a=read(OLD/name);b=read(O/name)
  need((len(a),sha(a),len(b),sha(b))==(row['original_bytes'],row['original_SHA256'],row['current_bytes'],row['current_SHA256']),'full original/current code pin')
  diff.extend(difflib.unified_diff(a.decode().splitlines(keepends=True),b.decode().splitlines(keepends=True),fromfile='approved-v2/'+name,tofile='current130131/'+name))
  ast.parse(b.decode());codepins.append({'path':str(O/name),'bytes':len(b),'SHA256':sha(b)})
 actual=read(O/'CODE_DIFF_FROM_APPROVED_V2.patch');need(''.join(diff).encode()==actual,'independently recomputed complete six-body diff')
 need(sha(actual)=='472363ed7ddf3151a011215d11c5b8f64cbb6bd4261e46552253dcc2f33324b2','whole inert diff')
 oldtree=ast.parse(read(OLD/'exact11_lib.py'));newtree=ast.parse(read(O/'exact11_lib.py'))
 names=['owned_entry','write_complete','validate_owned_buffer','unlink_owned','publish_buffer','parse_index']
 for name in names:
  a=next(n for n in oldtree.body if isinstance(n,ast.FunctionDef) and n.name==name)
  b=next(n for n in newtree.body if isinstance(n,ast.FunctionDef) and n.name==name)
  need(ast.dump(a,include_attributes=False)==ast.dump(b,include_attributes=False),'whole reused safety AST '+name)
 initial=obj(D/'INITIAL_SEAL.json')
 need(sha(read(D/'INITIAL_SEAL.json'))=='36594ec08bcf2cc1672c36b4cd983825ff6a84ab1a8b1659950f5486aeabfacc','pre-exposure seal unchanged')
 for key in ['initial_expectations','research_log_at_initial_checkpoint']:pin(initial[key]['path'],initial[key])
 print(json.dumps({'status':'PASS_INDEPENDENT_STRICT_CURRENT_SOURCE_CUSTODY','checks':N,'preparation_files':files,'preparation_directories':dirs,'code_pins':codepins,'current_code_bytes':sum(r['bytes'] for r in codepins),'all6_safety_ASTs_equal_prior':True,'whole_diff_recomputed':True,'references_fully_pinned':len(refs['files']),'actual_website_Git_network_or_reviewed_code_execution':False},indent=2))
if __name__=='__main__':main()

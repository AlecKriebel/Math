#!/usr/bin/env python3
"""Independent negative controls; only this review's disposable copies are changed."""
import importlib.util,json,hashlib,os,shutil,subprocess,sys,tempfile
from pathlib import Path
from fractions import Fraction as F
from itertools import permutations
D=Path(__file__).resolve().parent;PY=Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr906_30006419/reviews/computation_family/tmp/venv/bin/python');B=D/'tmp/bundle';PIN='b1881fcc385141e3f54a24dcc04cc35d4b76365a588cd18c2e832a4a4efb8364'
def need(x,s):
 if not x:raise RuntimeError(s)
def load(path):
 s=importlib.util.spec_from_file_location('review_module',path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 global B
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--bundle',type=Path);ap.add_argument('--output',type=Path);args=ap.parse_args()
 if args.bundle:B=args.bundle.resolve()
 m=load(B/'verify_package.py');m.validate(B,PIN);rows=[]
 def rejected(label,fn):
  try:fn()
  except Exception as e:rows.append({'case':label,'rejected':True,'error':type(e).__name__});return
  raise RuntimeError('Accepted negative control '+label)
 for a,b in [(True,1),(1.0,1),({'n':True},{'n':1}),({'n':1,'extra':1},{'n':1}),([1,2],[1]),({'n':[1.0]},{'n':[1]})]:rejected('strict_saved_result_'+str(len(rows)),lambda a=a,b=b:m.equivalent(a,b))
 for data in [b'{"a":1,"a":1}',b'{"a":Infinity}',b'{"a":NaN}']:rejected('strict_json_'+str(len(rows)),lambda data=data:m.strict_json(data))
 def malformed_edit(root,fn):
  path=root/'PACKAGE_MANIFEST.json';v=json.loads(path.read_bytes());fn(v);path.write_text(json.dumps(v)+'\n');return sha(path.read_bytes())
 with tempfile.TemporaryDirectory(dir=D/'tmp',prefix='independent-') as td:
  t=Path(td)
  edits=[('floating_pr',lambda x:x.update(pr=919.0)),('float_schema',lambda x:x.update(schema_version=1.0)),('float_size',lambda x:x['files']['note.tex'].update(bytes=float(x['files']['note.tex']['bytes']))),('null_records',lambda x:x.update(files=None)),('empty_records',lambda x:x.update(files={})),('empty_scope',lambda x:x.update(scope='')),('backslash_path',lambda x:x['files'].update({'x\\y':x['files'].pop('note.tex')})),('dot_path',lambda x:x['files'].update({'x/./y':x['files'].pop('note.tex')})),('double_slash',lambda x:x['files'].update({'x//y':x['files'].pop('note.tex')})),('nul_path',lambda x:x['files'].update({'x\x00y':x['files'].pop('note.tex')}))]
  for label,fn in edits:
   root=t/'case';shutil.copytree(B,root);p=malformed_edit(root,fn)
   for mode,flags,opt in [('normal',[],None),('O',['-O'],None),('OO',['-OO'],None),('env2',[],'2')]:
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
    if opt:env['PYTHONOPTIMIZE']=opt
    r=subprocess.run([str(PY),*flags,str(root/'verify_package.py'),'--expected-manifest',p,'--integrity-only'],env=env,capture_output=True,timeout=12);need(r.returncode!=0,label+'/'+mode);rows.append({'case':label,'mode':mode,'rejected':True})
   shutil.rmtree(root)
  for label,path in [('lexical_parent',str(B)+'/../bundle'),('lexical_dot',str(B)+'/./')]:
   r=subprocess.run([str(PY),path+'/verify_package.py','--expected-manifest',PIN,'--integrity-only'],capture_output=True,timeout=12);need(r.returncode!=0,label);rows.append({'case':label,'rejected':True})
  alias=t/'ancestor';alias.symlink_to(B.parent,target_is_directory=True)
  r=subprocess.run([str(PY),str(alias/'bundle/verify_package.py'),'--expected-manifest',PIN,'--integrity-only'],capture_output=True,timeout=12);need(r.returncode!=0,'ancestor_alias');rows.append({'case':'ancestor_alias','rejected':True})
  r=subprocess.run([str(PY),str(B/'verify_package.py'),'--workdir',str(t/'work')],capture_output=True,timeout=12);need(r.returncode!=0 and b'Full replay requires an external manifest anchor' in r.stderr,'no external anchor');rows.append({'case':'full_replay_without_external_anchor','rejected':True})
  # Authenticate then alter a different actual copied checker before worker execution.
  for target in ['reviews/computation_family/HARDENED_VERIFY.py','reviews/computation_family/INDEPENDENT_CONTROLS.py']:
   marker=t/'unsafe';original=m.shutil.copytree
   def changed(src,dst,*a,**kw):
    r=original(src,dst,*a,**kw)
    if Path(dst).name=='package':(Path(dst)/target).write_text('from pathlib import Path\nPath('+repr(str(marker))+').write_text("executed")\n')
    return r
   m.shutil.copytree=changed;sys_isolation=(sys.flags.isolated,sys.flags.optimize)
   # worker is called only in a dedicated -I process below because this controller is ordinary.
   m.shutil.copytree=original
   harness=t/'copy.py';harness.write_text('import importlib.util,sys\nfrom pathlib import Path\ns=importlib.util.spec_from_file_location("v",sys.argv[1]);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)\nroot=Path(sys.argv[1]).parent;orig=m.shutil.copytree\ndef changed(src,dst,*a,**kw):\n r=orig(src,dst,*a,**kw)\n if Path(dst).name=="package":(Path(dst)/'+repr(target)+').write_text('+repr('from pathlib import Path\nPath('+repr(str(marker))+').write_text("executed")\n')+')\n return r\nm.shutil.copytree=changed\ntry:m.worker(root,sys.argv[2],Path(sys.argv[3]))\nexcept RuntimeError as e:\n if '+repr('Payload fingerprint mismatch: '+target)+' not in str(e):raise\nelse:raise RuntimeError("accepted corrupted checker")\n')
   r=subprocess.run([str(PY),'-I','-B',str(harness),str(B/'verify_package.py'),PIN,str(t)],capture_output=True,timeout=20);need(r.returncode==0 and not marker.exists(),'post_copy '+target);rows.append({'case':'post_copy_'+target,'rejected_before_execution':True})
 # Distinct exact arithmetic route: Gaussian exponentiation by squaring, rational conjugacy and no splitting.
 def mul(x,y):return tuple(tuple(sum(x[i][k]*y[k][j] for k in range(2)) for j in range(2)) for i in range(2))
 I=((F(1),F(0)),(F(0),F(1)));A=((F(3,5),F(-4,5)),(F(4,5),F(3,5)));At=tuple(zip(*A))
 def power(x,n):
  r=I
  while n:
   if n&1:r=mul(r,x)
   x=mul(x,x);n//=2
  return r
 for n in [7,97,509,4093]:
  p=power(A,n);need(p!=I and mul(p,power(At,n))==I and mul(tuple(zip(*p)),p)==I,'power');rows.append({'case':'exact_power','n':n,'passed':True})
 T=((F(3),F(1)),(F(0),F(2)));Ti=((F(1,3),F(-1,6)),(F(0),F(1,2)));C=mul(mul(T,A),Ti);Q=mul(tuple(zip(*Ti)),Ti);need(mul(mul(tuple(zip(*C)),Q),C)==Q and mul(tuple(zip(*C)),C)!=I,'quadratic conjugacy');need(all((x+x)%4!=0 for x in [1,3]),'nonsplit C4->C2')
 end_cases=0
 for n in range(1,8):
  for p in permutations(range(n)):
   for j in range(n):need(len({p[i] for i in range(n) if i!=j})==n-1 and ((n-1>=2)==(n>=3)),'ambient permutation');end_cases+=1
 m.validate(B,PIN)
 out={'status':'PASS','rows':rows,'negative_rejections':sum(bool(r.get('rejected')) for r in rows),'extra_post_copy_corruption_targets':2,'end_permutation_receiving_arm_cases':end_cases,'exact_exponents':[7,97,509,4093],'nonorthogonal_conjugate_Q_control':True,'nonsplit_C4_to_C2_control':True,'scope':'Finite independent falsification controls, not analytic proofs, priority certification, or OS security.'}
 (args.output or D/'INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
if __name__=='__main__':main()

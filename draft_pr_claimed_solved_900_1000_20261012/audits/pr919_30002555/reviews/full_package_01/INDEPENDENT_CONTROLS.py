#!/usr/bin/env python3
"""Additional independently authored exact and rejection controls. No mathematical sampling claim."""
import argparse,importlib.util,itertools,json,os,shutil,subprocess,sys,tempfile,zipfile
from fractions import Fraction as Q
from pathlib import Path
HERE=Path(__file__).resolve().parent; P=HERE.parent.parent/'publication/reviewed_candidates/candidate01'
PIN='e2b2f091451dddc4e69032d05ba94b46fddaf49bd9e610f61a43692cb2ffc487'
PYTHON='/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr906_30006419/reviews/computation_family/tmp/venv/bin/python'
def need(c,m):
 if not c:raise RuntimeError(m)
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def reject(f,label):
 try:f()
 except Exception as e:return {'case':label,'rejected':True,'error_class':type(e).__name__}
 raise RuntimeError('accepted '+label)
def mm(x,y):return tuple(tuple(sum(a*b for a,b in zip(row,col)) for col in zip(*y)) for row in x)
def power(x,n):
 r=((Q(1),Q(0)),(Q(0),Q(1)))
 while n:
  if n&1:r=mm(r,x)
  x=mm(x,x);n//=2
 return r
def main():
 global P
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--candidate',type=Path,default=P);args=ap.parse_args();P=args.candidate.absolute()
 (HERE/'tmp').mkdir(exist_ok=True)
 with tempfile.TemporaryDirectory(dir=HERE/'tmp',prefix='additional_') as td:
  t=Path(td);b=t/'bundle'
  with zipfile.ZipFile(P/'rotational-veech-source-verification-v1.0.zip') as z:z.extractall(b)
  V=load(b/'verify_package.py','independently_authenticated_verifier');V.validate(b,PIN)
  rows=[]
  for label,x,y in [('bool_int',True,1),('float_int',1.0,1),('extra_key',{'x':1,'z':0},{'x':1}),('missing_key',{}, {'x':1}),('array_length',[1,2],[1]),('nested_bool',{'x':[True]},{'x':[1]}),('wrong_scalar',1,2)]:rows.append(reject(lambda x=x,y=y:V.equivalent(x,y),label))
  for label,s in [('duplicate',b'{"x":1,"x":1}'),('NaN',b'{"x":NaN}'),('Infinity',b'{"x":Infinity}'),('negative_Infinity',b'{"x":-Infinity}')]:rows.append(reject(lambda s=s:V.strict_json(s),label))
  V.equivalent({'x':[1,True,'a',None]},V.strict_json(b'{"x":[1,true,"a",null]}'))
  def mutate(m,label):
   if label=='float_pr':m['pr']=919.0
   elif label=='float_schema':m['schema_version']=1.0
   elif label=='float_bytes':m['files']['note.tex']['bytes']=float(m['files']['note.tex']['bytes'])
   elif label=='null_files':m['files']=None
   elif label=='empty_files':m['files']={}
   elif label=='scope_bool':m['scope']=True
   elif label=='original_head_bool':m['original_pr_head']=True
   else:
    names={'double_slash':'sub//note.tex','dot_component':'sub/./note.tex','backslash':'sub\\note.tex','nul':'sub\0note.tex','empty_name':'','trailing_slash':'note.tex/'}
    m['files'][names[label]]=m['files'].pop('note.tex')
  labels=['float_pr','float_schema','float_bytes','null_files','empty_files','scope_bool','original_head_bool','double_slash','dot_component','backslash','nul','empty_name','trailing_slash']
  for label in labels:
   c=t/'mutated';shutil.copytree(b,c);p=c/'PACKAGE_MANIFEST.json';m=json.loads(p.read_bytes());mutate(m,label);p.write_text(json.dumps(m)+'\n')
   # Use freshly supplied outer anchor to reach schema checks; no original anchor bypass is implied.
   pin=V.digest(p.read_bytes())
   for mode,flags,opt in [('normal',[],None),('O',['-O'],None),('OO',['-OO'],None),('env2',[],'2')]:
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
    if opt:env['PYTHONOPTIMIZE']=opt
    p2=subprocess.run([PYTHON,*flags,str(c/'verify_package.py'),'--expected-manifest',pin,'--integrity-only'],env=env,text=True,capture_output=True,timeout=10)
    need(p2.returncode!=0,'accepted '+label+'/'+mode);rows.append({'case':label,'mode':mode,'rejected':True})
   shutil.rmtree(c)
  for label,raw in [('parent_alias',str(b)+'/../bundle'),('dot_alias',str(b)+'/./')]:
   p2=subprocess.run([PYTHON,raw+'/verify_package.py','--expected-manifest',PIN,'--integrity-only'],text=True,capture_output=True,timeout=10)
   need(p2.returncode!=0,'accepted '+label);rows.append({'case':label,'rejected':True})
  p2=subprocess.run([PYTHON,str(b/'verify_package.py'),'--workdir',str(t/'noanchor')],text=True,capture_output=True,timeout=10)
  need(p2.returncode!=0 and 'requires an external manifest anchor' in p2.stderr,'unanchored full replay accepted');rows.append({'case':'full_replay_requires_anchor','rejected':True})
  alias=t/'ancestor_link';alias.symlink_to(t,target_is_directory=True)
  rows.append(reject(lambda:V.validate(alias/'bundle',PIN),'symlinked_ancestor'))
  H=load(b/'reviews/computation_family/HARDENED_VERIFY.py','authenticated_historical_hardened')
  rows.append(reject(lambda:H.canonical_root('C:\\release\\packet'),'windows_path_not_supported'))
  platform={'os_name_tested':os.name,'O_NOFOLLOW_available':hasattr(os,'O_NOFOLLOW'),'canonical_absolute_roots_require_leading_slash':True,'unconditional_O_NOFOLLOW_in_historical_gate':True,'actual_Windows_run':False,'deduction':'Current full entry point is POSIX-scoped; Python3.10+ alone is not a sufficient prerequisite on Windows.'}
  V.validate(b,PIN)
 I=((Q(1),Q(0)),(Q(0),Q(1)));A=((Q(3,5),Q(-4,5)),(Q(4,5),Q(3,5)));AT=tuple(zip(*A))
 need(mm(AT,A)==I,'orthogonality')
 powers=[]
 for n in [17,113,1009,3001]:
  p=power(A,n);need(p!=I and mm(p,power(AT,n))==I,'exact fast power');powers.append(n)
 # Independent algebraic-integer certificate: if A had finite order, its two eigenvalues
 # would be roots of unity, so rational trace 6/5 would be an algebraic integer. Rational
 # algebraic integers are integers. The nonintegral exact trace rules this out for all n.
 trace=A[0][0]+A[1][1];need(trace==Q(6,5) and trace.denominator!=1,'nonintegral trace')
 finite=[]
 for r,n in [(I,1),(((-1,0),(0,-1)),2),(((0,-1),(1,0)),4)]:need(power(r,n)==I,'finite control');finite.append(n)
 # Exhaust all n=1,2,3,4,5 permutations and every receiving arm; the invariant being tested
 # is exactly cardinality of the OTHER ambient ends, never the intrinsic arm-end count.
 cases=0
 for n in range(1,6):
  for pi in itertools.permutations(range(n)):
   for i in range(n):need(len({pi[j] for j in range(n) if j!=i})==n-1,'end permutation');cases+=1
 # Nonsplit cyclic extension C4 -> C2: no element of order two maps to the nontrivial
 # target, but its full preimage still surjects. This checks why taking a section is wrong.
 need(all((2*x)%4!=0 for x in [1,3]) and {x%2 for x in range(4)}=={0,1},'nonsplit extension fixture')
 out={'status':'PASS','additional_rejections':len(rows),'rows':rows,'platform_boundary':platform,'exact_arithmetic':{'fast_power_exponents':powers,'negative_powers_via_exact_inverse':True,'trace_numerator':trace.numerator,'trace_denominator':trace.denominator,'all_exponent_argument':'Finite order implies rational trace6/5 is an algebraic integer, contradicting denominator5.','finite_rotation_order_controls':finite},'ambient_end_permutation_cases':cases,'n1_n2_n3_thresholds':[False,False,True],'nonsplit_extension_control':'C4_to_C2','limits':'Finite controls supplement the written universal proof. Platform failure is deduced from reviewed conditions; Windows was not actually run.'}
 print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()

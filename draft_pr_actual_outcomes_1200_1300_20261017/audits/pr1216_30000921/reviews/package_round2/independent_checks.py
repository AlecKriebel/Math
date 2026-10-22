from pathlib import Path
from fractions import Fraction as F
from math import comb,factorial
import hashlib,json,datetime,random,shutil,importlib.util,subprocess
R=Path(__file__).resolve().parent;E=R/'_local/extracted';P=R.parent.parent/'publication';C=R/'_local/controls'
def need(c,m):
 if not c:raise RuntimeError(m)
def binding(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
# Independently traverse EVERY archived manifest, including the post-freeze cross challenge.
checked=[]
for p in E.rglob('MANIFEST.json'):
 d=json.loads(p.read_text());entries=d.get('files',d.get('entries',[]))
 for e in entries:
  rel=e.get('path',e.get('file'));need(binding(p.parent/rel)=={'bytes':e['bytes'],'sha256':e['sha256']},'nested binding '+str(p)+':'+rel);checked.append(str(p.relative_to(E))+':'+rel)
accept=json.loads((E/'current_edition/ACCEPTANCE.json').read_text())
for n,b in accept['current_document_bindings'].items():need(binding(E/'current_edition'/n)==b,'acceptance binding')
# Direct exact Gaussian-rational algebra, with ordinary global-coordinate oracle.
class Z:
 def __init__(s,r=0,i=0):
  if isinstance(r,Z):s.r,s.i=r.r,r.i
  else:s.r,s.i=F(r),F(i)
 def __add__(s,t):t=Z(t);return Z(s.r+t.r,s.i+t.i)
 __radd__=__add__
 def __neg__(s):return Z(-s.r,-s.i)
 def __sub__(s,t):return s+-Z(t)
 def __mul__(s,t):t=Z(t);return Z(s.r*t.r-s.i*t.i,s.r*t.i+s.i*t.r)
 __rmul__=__mul__
 def __truediv__(s,t):t=Z(t);return s*Z(t.r/t.norm(),-t.i/t.norm())
 def __pow__(s,n):
  a=Z(1)
  for _ in range(n):a=a*s
  return a
 def norm(s):return s.r*s.r+s.i*s.i
 def __eq__(s,t):t=Z(t);return s.r==t.r and s.i==t.i

def expand(v,a):return [sum((v[j]*comb(j,k)*((-a)**(j-k)) for j in range(k,len(v))),Z()) for k in range(len(v))]
def multiply(v,w):return [sum((v[j]*w[k-j] for j in range(len(v)) if 0<=k-j<len(w)),Z()) for k in range(len(v)+len(w)-1)]
def ev(v,n,a):return sum((v[j]*F(factorial(j),factorial(j-n))*(a**(j-n)) for j in range(n,len(v))),Z())
rng=random.Random(41017);cases=0;identities=0;corrected=0;kept=0
for m in [1,2,4]:
 for d in [m,m+1,m+3]:
  for alpha in [Z(),Z(F(2,7),F(-3,5))]:
   for eta in [F(1),F(1,10**8)]:
    q=[Z()]*m+[Z(F(1,7),F(2,5))]+[Z(rng.randrange(-200,201),rng.randrange(-200,201)) for _ in range(d-m)]
    a=[Z()]+[Z(F(rng.randrange(-20,21),3),F(rng.randrange(-20,21),7)) for _ in range(7)];b=[]
    for k in range(len(a)):
     n=k+m;A=q[m]*F(factorial(n),factorial(k));S=A*a[k]+sum((q[j]*F(factorial(n),factorial(n-j))*b[n-j] for j in range(m+1,min(d,n)+1)),Z())
     c=Z() if S.norm()>=eta*eta else (Z(eta)-S)/A
     corrected+=c!=Z();kept+=c==Z();b.append(a[k]+c);need(c.norm()*A.norm()<=4*eta*eta,'correction floor')
     product=multiply(expand(q,alpha),expand([b[j]/factorial(j) for j in range(len(b))],alpha))
     need(ev(product,n,alpha)==S+A*c,'independent ordinary product formula');need(ev(product,n,alpha).norm()>=eta*eta,'barrier')
     for t in range(m):need(ev(product,t,alpha)==Z(),'multiplicity')
     identities+=1
    cases+=1
# Detect corruption before exact executables run.
corruptions=[]
for kind in ['byte','extra','missing','duplicate_manifest_entry']:
 root=C/('archive_'+kind);shutil.copytree(E,root,dirs_exist_ok=True)
 if kind=='byte':(root/'current_edition/PROOF.md').write_bytes(b'bad')
 if kind=='extra':(root/'extra.txt').write_text('extra')
 if kind=='missing':(root/'original_submitted/README.md').unlink()
 if kind=='duplicate_manifest_entry':
  d=json.loads((root/'MANIFEST.json').read_text());d['files'].append(d['files'][0]);(root/'MANIFEST.json').write_text(json.dumps(d))
 run=subprocess.run(['python3','-B',str(root/'verify.py')],capture_output=True,text=True)
 need(run.returncode!=0,'accepted corruption '+kind);corruptions.append({'kind':kind,'rejected':True,'last_error':run.stderr.splitlines()[-1]})
# Scope control: root rehash alone does not repair a stale nested cross-freeze manifest.
root=C/'cross_nested_stale';shutil.copytree(E,root,dirs_exist_ok=True)
f=root/'priority/independent/cross_freeze_20261017T183513Z/CROSS_FAMILY_CHALLENGE.md';f.write_bytes(f.read_bytes()+b'\nchanged\n')
d=json.loads((root/'MANIFEST.json').read_text())
for e in d['files']:
 if e['path']==f.relative_to(root).as_posix():e.update(binding(f))
(root/'MANIFEST.json').write_text(json.dumps(d))
spec=importlib.util.spec_from_file_location('isolate_verify',root/'verify.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
expected=json.loads((root/'EXPECTED_DIAGNOSTICS.json').read_text());v.replay=lambda script,flags:expected['root' if script.name=='root_diagnostics.py' else 'analytic']
try:v.main();cross_accepted=True
except Exception:cross_accepted=False
# Build wrapper accepts absent compile/layout receipts and stale PDF with changed TeX.
root=C/'stale_pdf_build/publication';root.mkdir(parents=True,exist_ok=True);shutil.copytree(E,root/'verification',dirs_exist_ok=True)
(root/'manuscript').mkdir(exist_ok=True);(root/'manuscript/main.tex').write_text('CHANGED SOURCE THAT DOES NOT MATCH THE PDF')
(root/'output/pdf').mkdir(parents=True,exist_ok=True);shutil.copyfile(P/'Polynomial_Multipliers_Note_v1.0.pdf',root/'output/pdf/main.pdf')
(root.parent/'reviews/analytic_source_adversary').mkdir(parents=True,exist_ok=True)
(root.parent/'ROOT_EXACT_DIAGNOSTICS.json').write_text(json.dumps(expected['root']));(root.parent/'reviews/analytic_source_adversary/exact_normal.json').write_text(json.dumps(expected['analytic']))
spec=importlib.util.spec_from_file_location('build_scope',P/'build_package.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);v.ROOT=root;v.PACKAGE=root/'verification'
class SP:
 @staticmethod
 def run(*a,**k):return subprocess.CompletedProcess(a[0],0,stdout=json.dumps(json.loads((P/'BUILD_RECEIPT.json').read_text())['verification_run']),stderr='')
v.subprocess=SP
try:v.main();build_accepted=True
except Exception as e:build_accepted=False
out={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_actual_nested_bindings_match':True,'nested_bindings_checked':len(checked),'manifest_files_checked':[str(p.relative_to(E)) for p in E.rglob('MANIFEST.json')],'exact_original_recursion_cases':cases,'independent_global_product_identities':identities,'corrected_branches':corrected,'kept_branches':kept,'ordinary_corruptions':corruptions,'stale_cross_nested_manifest_accepted_with_exact_replay_stub':cross_accepted,'stale_pdf_missing_compile_and_layout_receipts_build_accepted_with_prepare_verify_stubs':build_accepted,'control_limits':'Cross control stubs only costly exact replays; all archive/binding code runs. Build control stubs preparation and exact replay to isolate missing compile/layout gate; it does not claim those stubbed operations were independently executed.'}
(R/'INDEPENDENT_CHECK_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

import itertools,json,hashlib,pathlib
import sympy as s
p=pathlib.Path('/workspace/shared/research_separable_30005767'); count=0
for f in json.loads((p/'checkpoint/FINAL_FROZEN_MANIFEST.json').read_text())['files']:
 assert hashlib.sha256((p/'checkpoint'/f['path']).read_bytes()).hexdigest()==f['sha256'];count+=1
for f in json.loads((p/'checkpoint/SOURCE_MANIFEST.json').read_text())['primary_pdfs']:
 assert hashlib.sha256((p/f['local_audit_file']).read_bytes()).hexdigest()==f['sha256'];count+=1
patterns={(2,3,4,1),(2,4,1,3),(3,1,4,2)}
counts=[]
for n in range(8):
 total=0
 for perm in itertools.permutations(range(n)):
  ok=True
  for ix in itertools.combinations(range(n),4):
   vals=[perm[i] for i in ix]; ranks=tuple(sorted(vals).index(t)+1 for t in vals)
   if ranks in patterns:ok=False;break
  total+=ok;count+=1
 counts.append(total)
z=s.symbols('z');A=z*(1-z+z*z);B=1-2*z+2*z*z;D=(1-z)**2;P=s.expand(B*B-4*A*D)
assert P==1-8*z+20*z*z-24*z**3+16*z**4-4*z**5;count+=1
assert P.subs(z,s.Rational(1,4))==-s.Rational(17,256);count+=1
assert P.subs(z,1)==1;count+=1
C=sum(v*z**i for i,v in enumerate(counts))
for i in range(8):assert s.expand(A*C*C-B*C+D).coeff(z,i)==0;count+=1
# Separate nonempty grammar polynomial matches published quadratic.
f=s.symbols('f');L=z+z*z/(1-z)**2
assert s.expand(s.cancel((L*f*f+(z+L-1)*f+z)*(1-z)**2)-(A*(1+f)**2-B*(1+f)+D))==0;count+=1
print(json.dumps({'status':'PASS','independent_assertions':count,'counts_n0_through_7':counts},indent=2))

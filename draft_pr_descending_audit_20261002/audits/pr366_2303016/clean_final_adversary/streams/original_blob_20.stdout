from pathlib import Path
from fractions import Fraction as Q
import hashlib,json,subprocess,sys
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/workspace/shared/research_thinpoints_2303016/checkpoint')
m=json.loads((p/'FINAL_FROZEN_MANIFEST.json').read_text());N=0
for f in m['files']:assert hashlib.sha256((p/f['path']).read_bytes()).hexdigest()==f['sha256'];N+=1
r=subprocess.check_output([sys.executable,str(p/'verify_turn1.py')]);assert r==(p/'TURN_1_CHECKS.json').read_bytes()
# Independently check sharp dyadic scalar envelope at arbitrary rational distances,
# not only reciprocal integers, and localization constants on exact rationals.
for a in range(1,51):
 for b in range(a,61):
  x=Q(a,b);v=sum((Q(2)**(k-1) for k in range(16) if x<=Q(1,2**k)),Q(0));assert v<=1/x;N+=1
for s in range(1,41):
 eps=Q(1,4*2**s*s)
 for ratio in [Q(1,4),Q(1,5),Q(1,9)]:assert 2**s*s*eps+ratio**s<=Q(1,2);N+=1
# First variation polynomial coefficients checked symbolically.
import sympy as S
t,J,L,H=S.symbols('t J L H');poly=S.expand((1-t)**2*J+2*t*(1-t)*L+t*t*H);assert S.diff(poly,t).subs(t,0)==2*(L-J);N+=1
print(json.dumps({'status':'PASS','manifest_bound_files':len(m['files']),'independent_assertions':N,'author_assertions':json.loads(r)['assertions'],'scope':'Integrity, exact scalar bounds and variation identity. Analytical all-set proof audited separately; no finite controls certify polarity.'},indent=2))

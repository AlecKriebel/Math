#!/usr/bin/env python3
"""Direct exact check of polynomial integer-image interface; no submitted imports.
Only definitions are loaded from our sealed independent implementation, without
executing its top-level checks or rewriting any sealed artifact.
"""
import ast,json,random
from pathlib import Path
from datetime import datetime,timezone
here=Path(__file__).resolve().parent
src=ast.parse((here/'independent_controls.py').read_text())
module=ast.Module(body=[n for n in src.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef))],type_ignores=[])
globals_={};exec(compile(module,'own_sealed_definitions','exec'),globals_)
for name in ['check','solve','period','endpoint','Lmatrix','reduced','comps','sc']:
 globals()[name]=globals_[name]
def eg(a,b):
 if not b:return a,1,0
 d,u,v=eg(b,a%b);return d,v,u-(a//b)*v
def bezout(p):
 c=[1];d=p[0]
 for a in p[1:]:
  d,s,t=eg(d,a);c=[s*z for z in c]+[t]
 check(d==1 and sum(a*b for a,b in zip(c,p))==1,'primitive Bezout');return c
def poly_reduced(A,x,y):
 n=len(A);delta=[y[i]-x[i] for i in range(n)]
 if sum(delta):return None
 L=Lmatrix(A);p=period(A);c=bezout(p)
 q=[0]+solve([r[1:] for r in L[1:]],delta[1:])
 t=-sum(c[i]*q[i] for i in range(n));h=[q[i]+t*p[i] for i in range(n)]
 if any(z.denominator!=1 for z in h):return None
 h=list(map(int,h));k=min(h[i]//p[i] for i in range(n));g=tuple(h[i]-k*p[i] for i in range(n))
 check(endpoint(A,x,g)==y,'integer image output');return g
rng=random.Random(23431676);cases=0;large=[]
for _ in range(300):
 n=rng.choice([2,3,4]);A=[[0 if i==j else rng.randrange(4) for j in range(n)] for i in range(n)]
 if not sc(A):continue
 x=tuple(rng.randrange(5) for _ in range(n));y=tuple(rng.randrange(5) for _ in range(n))
 if rng.randrange(2):y=endpoint(A,x,tuple(rng.randrange(-5,6) for _ in range(n)))
 check(poly_reduced(A,x,y)==reduced(A,x,y),'direct vs residue enumerator');cases+=1
for bits in [32,256,1024]:
 A=[[0,2**bits+1,2**(bits-1)],[2**(bits-1)+3,0,7],[11,2**bits+9,0]];x=(3,5,7);h=(13,-17,19);y=endpoint(A,x,h);p=period(A);k=min(h[i]//p[i] for i in range(3));expected=tuple(h[i]-k*p[i] for i in range(3))
 check(poly_reduced(A,x,y)==expected,'large period direct integer solver')
 large.append({'adjacency_bits':bits,'period_max_bits':max(z.bit_length() for z in p),'reduced_max_bits':max(z.bit_length() for z in expected)})
result={'completed_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS finite controls; universal proof separately recorded','random_cases':cases,'seed':23431676,'large_binary_cases':large,'timing':'After submitted helper inspection; original pre-helper controls remain independently sealed and unchanged.'}
(here/'integer_image_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

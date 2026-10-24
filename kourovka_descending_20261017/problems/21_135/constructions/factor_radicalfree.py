"""Exact factorization certificates for listed radical-free degree polynomials.

Exploratory search only: factorization of a degree polynomial does not imply
that its factors are themselves realizable group degree polynomials.
"""
from pathlib import Path
import sys,json,time,hashlib,math
from collections import Counter
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P/'tools/pythonlibs'))
import sympy as S
rows=[json.loads(l) for l in (P/'artifacts/library_scan.ndjson').read_text().splitlines()]
groups={}
for n,o,d,r in rows:
 if r==1:groups.setdefault(tuple(map(tuple,d)),[]).append(n)
symbols={}
def decomp(n):return S.factorint(n)
def expr(data):
 z=0
 for n,c in data:
  a=S.Integer(c)
  for p,e in decomp(n).items():
   symbols.setdefault(p,S.Symbol('x'+str(p)));a*=symbols[p]**e
  z+=a
 return z
def encode(f):
 vs=sorted(f.free_symbols,key=lambda x:int(str(x)[1:]))
 if not vs:return [[1,int(f)]]
 return sorted([[math.prod(int(str(x)[1:])**e for x,e in zip(vs,mon)),int(co)] for mon,co in S.Poly(f,*vs).terms()])
def mult(a,b):
 z=Counter()
 for n,c in a:
  for m,d in b:z[n*m]+=c*d
 return sorted((n,c)for n,c in z.items() if c)
out=P/'artifacts/radicalfree_factors.ndjson'
with out.open('w')as h:
 for d,names in groups.items():
  t=time.monotonic();pol=expr(d);content,fac=S.factor_list(pol)
  factors=[{'terms':encode(f),'multiplicity':int(e)}for f,e in fac]
  product=[(1,int(content))]
  for f in factors:
   for _ in range(f['multiplicity']):product=mult(product,f['terms'])
  assert tuple(product)==d,(names,product,d)
  result={'names':names,'content':int(content),'factors':factors,'seconds':round(time.monotonic()-t,6)}
  h.write(json.dumps(result,separators=(',',':'))+'\n');h.flush()
print('COMPLETE',len(groups),'exact factorization certificates',hashlib.sha256(out.read_bytes()).hexdigest())

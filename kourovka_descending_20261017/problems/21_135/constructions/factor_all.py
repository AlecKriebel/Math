"""Exploratory exact factorization of all scanned degree polynomials.

This is not an irreducibility certificate; each proposed factorization is
independently checked by plain integer sparse convolution for reconstruction.
"""
from pathlib import Path
import sys,json,math,time,hashlib
from collections import Counter
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P/'tools/pythonlibs'))
import sympy as S
rows=[json.loads(l) for l in (P/'artifacts/library_scan.ndjson').read_text().splitlines()]
groups={}
for n,o,d,r in rows:
 k=tuple(map(tuple,d))
 g=groups.setdefault(k,{'names':[],'radical_free':r==1,'order':o})
 assert g['radical_free']==(r==1)
 g['names'].append(n)
symbols={}
def expr(data):
 z=0
 for n,c in data:
  a=S.Integer(c)
  for p,e in S.factorint(n).items():
   symbols.setdefault(p,S.Symbol('x'+str(p)));a*=symbols[p]**e
  z+=a
 return z
def encode(f):
 vs=sorted(f.free_symbols,key=lambda x:int(str(x)[1:]))
 if not vs:return [[1,int(f)]]
 a=sorted([[math.prod(int(str(x)[1:])**e for x,e in zip(vs,mon)),int(co)] for mon,co in S.Poly(f,*vs).terms()])
 return a
def mult(a,b):
 z=Counter()
 for n,c in a:
  for m,d in b:z[n*m]+=c*d
 return sorted((n,c)for n,c in z.items() if c)
out=P/'artifacts/all_factors.ndjson'
with out.open('w')as h:
 for d,g in groups.items():
  pol=expr(d);content,fac=S.factor_list(pol)
  factors=[{'terms':encode(f),'multiplicity':int(e)}for f,e in fac]
  product=[(1,int(content))]
  for f in factors:
   for _ in range(f['multiplicity']):product=mult(product,f['terms'])
  assert tuple(product)==d,(g['names'],product,d)
  g.update({'content':int(content),'factors':factors})
  h.write(json.dumps(g,separators=(',',':'))+'\n');h.flush()
print('COMPLETE',len(groups),'factorization reconstructions',hashlib.sha256(out.read_bytes()).hexdigest())

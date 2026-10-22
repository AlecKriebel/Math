#!/usr/bin/env python3
"""Independent PD state-sum Jones and Fox-matrix Alexander calculation.
PD convention: incoming under-edge first, then counterclockwise; edge labels
increase along the oriented knot. SymPy is used only for exact determinants.

Usage: python check_pd_k11n42.py INPUT_JSON
External input is required and is not distributed. JSON keys: PD (crossing list),
TREFOIL (calibration crossing list), table_jones (exponent-to-coefficient map).
The report pins the separately sourced input hash and public source URLs.
"""
from itertools import product
import json
import sympy as s
from pathlib import Path
import sys,hashlib
if len(sys.argv)!=2:
 raise SystemExit("Usage: python check_pd_k11n42.py INPUT_JSON; the hash-identified source input is not distributed.")
input_path=Path(sys.argv[1])
inputs=json.loads(input_path.read_text())
PD=inputs["PD"]
TREFOIL=inputs["TREFOIL"]
def require(x):
 if not x:raise RuntimeError('exact check failed')
def add(a,b):
 r=a.copy()
 for k,v in b.items():r[k]=r.get(k,0)+v
 return {k:v for k,v in r.items() if v}
def mul(a,b):
 r={}
 for i,u in a.items():
  for j,v in b.items():r[i+j]=r.get(i+j,0)+u*v
 return {k:v for k,v in r.items() if v}
def power(a,n):
 p={0:1}
 for _ in range(n):p=mul(p,a)
 return p
class DSU:
 def __init__(self,n):self.p=list(range(n+1))
 def root(self,i):
  while i!=self.p[i]:self.p[i]=self.p[self.p[i]];i=self.p[i]
  return i
 def join(self,i,j):self.p[self.root(i)]=self.root(j)
def crossing_sign(c,n):
 a,b,d,e=c
 require(d==a%(2*n)+1)
 if b==e%(2*n)+1:return 1
 require(e==b%(2*n)+1)
 return -1

def jones(pd):
 n=len(pd);w=sum(crossing_sign(c,n) for c in pd);br={}
 require(sorted(v for c in pd for v in c)==[k for k in range(1,2*n+1) for _ in range(2)])
 for state in product((0,1),repeat=n):
  u=DSU(2*n)
  for (a,b,c,d),bit in zip(pd,state):
   if bit==0:u.join(a,d);u.join(b,c)
   else:u.join(a,b);u.join(c,d)
  loops=len({u.root(i) for i in range(1,2*n+1)})
  mon=2*sum(state)-n
  br=add(br,{k+mon:v for k,v in power({2:-1,-2:-1},loops-1).items()})
 norm={k-3*w:((-1 if w%2 else 1)*v) for k,v in br.items()}
 require(all(k%4==0 for k in norm))
 return w,{-k//4:v for k,v in norm.items()}

def alexander(pd):
 n=len(pd);t=s.symbols('t');u=DSU(2*n)
 for a,b,c,d in pd:u.join(b,d)
 roots=sorted({u.root(i) for i in range(1,2*n+1)})
 require(len(roots)==n)
 idx={r:j for j,r in enumerate(roots)}
 mat=s.zeros(n,n)
 for row,(a,b,c,d) in enumerate(pd):
  incoming,outgoing,over=idx[u.root(a)],idx[u.root(c)],idx[u.root(b)]
  if crossing_sign((a,b,c,d),n)==1:
   co=(t,-1,1-t)
  else:co=(1,-t,t-1)
  for j,v in zip((incoming,outgoing,over),co):mat[row,j]+=v
 require(mat*s.ones(n,1)==s.zeros(n,1))
 minor=mat[:n-1,:n-1]
 det=s.factor(minor.det(method='domain-ge'))
 return str(det),[[str(v) for v in row] for row in mat.tolist()]
if __name__=='__main__':
 wt,jt=jones(TREFOIL)
 print('TREFOIL',wt,jt,flush=True)
 require(wt==-3)
 require(jt=={-4:-1,-3:1,-1:1})
 at,_=alexander(TREFOIL)
 require(s.simplify(s.sympify(at)-(s.Symbol('t')**2-s.Symbol('t')+1))==0)
 w,j=jones(PD);a,mat=alexander(PD)
 expected={int(k):v for k,v in inputs["table_jones"].items()}
 require(j==expected or j=={-k:v for k,v in expected.items()})
 require(j!={0:1})
 mon=s.Poly(s.sympify(a),s.Symbol('t')).terms()
 require(len(mon)==1 and abs(mon[0][1])==1)
 result={'status':'all checks passed','input_sha256':hashlib.sha256(input_path.read_bytes()).hexdigest(),'input_bytes':input_path.stat().st_size,'source':'https://katlas.org/wiki/K11n42','pd_convention_source':'https://katlas.org/wiki/Planar_Diagrams','writhe':w,'jones_exponent_coefficients':sorted(j.items()),'jones_matches_table':j==expected,'alexander_minor_determinant':a,'alexander_normalized':1,'alexander_matrix':mat,'smoothing_states':2**len(PD),'sympy_version':s.__version__,'interpretation':'Explicit PD knot has Delta=1 and V!=1. Name/mirror ambiguity irrelevant to this obstruction.'}
 print(json.dumps(result,indent=2))

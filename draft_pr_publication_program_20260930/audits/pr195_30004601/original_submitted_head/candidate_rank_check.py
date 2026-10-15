#!/usr/bin/env python3
"""Independently authored exact Macaulay-rank verification over Q."""
import sympy as sp,json
x,y,z,w=sp.symbols('x y z w');variables=[x,y,z,w]
Q=x*y*(x-y)*(x-2*y)*z*w*(x+z+w)
f=[sp.diff(Q,v) for v in variables]
g3=[sp.Poly(p.subs(w,x+2*y+3*z),x,y,z).as_expr() for p in f]
g2=[sp.Poly(p.subs(z,2*x+3*y),x,y).as_expr() for p in g3]
def exponents(n,d):
 if n==1:yield (d,);return
 for a in range(d+1):
  for tail in exponents(n-1,d-a):yield (a,)+tail

def macaulay(polys,vs,d):
 e=sp.Poly(polys[0],*vs).total_degree();cols=list(exponents(len(vs),d));mult=list(exponents(len(vs),d-e));rows=[]
 for p in polys:
  for a in mult:
   poly=sp.Poly(p*sp.prod(v**k for v,k in zip(vs,a)),*vs)
   rows.append([poly.coeff_monomial(c) for c in cols])
 M=sp.Matrix(rows);return {'degree':d,'rows':M.rows,'cols':M.cols,'rank':M.rank(),'quotient_dimension':M.cols-M.rank(),'syzygy_dimension':M.rows-M.rank()}
out={'Q':str(Q),'polars':[str(sp.expand(p)) for p in f],'three_section':'w=x+2y+3z','two_section':'z=2x+3y','three_variable':[],'two_variable':[]}
for d in [6,7,8]:
 out['three_variable'].append(macaulay(g3,[x,y,z],d));out['two_variable'].append(macaulay(g2,[x,y],d))
relation=sp.expand(11*x*g2[0]+11*y*g2[1]-73*(2*x+3*y)*g2[2]+25*(7*x+11*y)*g2[3]);assert relation==0
assert out['three_variable'][0]['quotient_dimension']==24
assert out['three_variable'][1]['quotient_dimension']==24
assert out['two_variable'][1]['quotient_dimension']==1
assert out['two_variable'][2]['quotient_dimension']==0
assert out['two_variable'][0]['quotient_dimension']==3
out['kernel_x3_degree_6_to_7']=24-24+1
out['binary_cutoff']=8
out['explicit_binary_linear_syzygy']=['11x','11y','-73(2x+3y)','25(7x+11y)']
print(json.dumps(out,indent=2))

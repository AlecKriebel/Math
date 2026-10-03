#!/usr/bin/env python3
"""Exact finite arithmetic for the SL(2,5), p=2 counterexample.

No external packages, character-table database, source PDF, or floating point.
The mathematical bridge from these finite checks to nonsemiperfectness is proved
in COUNTEREXAMPLE.md; finite checks alone do not establish that bridge.
"""
from fractions import Fraction as F
from itertools import product, permutations
from collections import Counter
from pathlib import Path
import json

# Q(phi), phi^2=phi+1. A pair is a+b*phi.
def A(x,y): return (x[0]+y[0],x[1]+y[1])
def N(x): return (-x[0],-x[1])
def M(x,y):
 a,b=x;c,d=y
 return (a*c+b*d,a*d+b*c+b*d)
def S(x,n): return (x[0]*n,x[1]*n)
zero=(F(0),F(0)); one=(F(1),F(0)); phi=(F(0),F(1))

def qmul(q,r):
 a,b,c,d=q; e,f,g,h=r
 return (A(A(M(a,e),N(M(b,f))),N(A(M(c,g),M(d,h)))),
         A(A(M(a,f),M(b,e)),A(M(c,h),N(M(d,g)))),
         A(A(M(a,g),N(M(b,h))),A(M(c,e),M(d,f))),
         A(A(M(a,h),M(b,g)),A(N(M(c,f)),M(d,e))))

def parity(p): return sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2

def icosians():
 G=set()
 for i in range(4):
  for s in [-1,1]:
   q=[zero]*4;q[i]=S(one,s);G.add(tuple(q))
 for signs in product([-1,1],repeat=4): G.add(tuple(S(one,F(s,2)) for s in signs))
 for signs in product([-1,1],repeat=3):
  q=(zero,S(one,F(signs[0],2)),S(phi,F(signs[1],2)),S(A(phi,N(one)),F(signs[2],2)))
  for p in permutations(range(4)):
   if parity(p)==0:G.add(tuple(q[i] for i in p))
 assert len(G)==120
 e=(one,zero,zero,zero); z=tuple(N(x) for x in e)
 for q in G:
  assert qmul(q,(q[0],N(q[1]),N(q[2]),N(q[3])))==e
  for r in G: assert qmul(q,r) in G
 def order(q):
  r=e
  for n in range(1,121):
   r=qmul(r,q)
   if r==e:return n
  raise AssertionError
 orders={q:order(q) for q in G}
 # Sym^3 of the natural SU(2) representation has trace x^3-2x.
 def chi(q):
  x=S(q[0],2); y=A(M(M(x,x),x),N(S(x,2)))
  assert y[1]==0 and y[0].denominator==1
  return int(y[0])
 values={q:chi(q) for q in G}
 norm=sum(x*x for x in values.values())
 fs=sum(chi(qmul(q,q)) for q in G)
 assert norm==120 and fs==-120
 assert sum(1 for q in G if all(qmul(q,r)==qmul(r,q) for r in G))==2
 rows={o:sorted({values[q] for q in G if orders[q]==o}) for o in sorted(set(orders.values()))}
 assert rows=={1:[4],2:[-4],3:[1],4:[0],5:[-1],6:[-1],10:[1]}
 return {"order":120,"closure_products_checked":14400,"center_order":2,"element_order_counts":dict(sorted(Counter(orders.values()).items())),"symmetric_cube_values_by_order":rows,"symmetric_cube_norm":str(F(norm,120)),"symmetric_cube_frobenius_schur_indicator":str(F(fs,120))}

def sl2_checks():
 p=5;G=[x for x in product(range(p),repeat=4) if (x[0]*x[3]-x[1]*x[2])%p==1];e=(1,0,0,1);z=(4,0,0,4)
 def mul(x,y):
  a,b,c,d=x;f,g,h,i=y
  return ((a*f+b*h)%p,(a*g+b*i)%p,(c*f+d*h)%p,(c*g+d*i)%p)
 def order(x):
  y=e
  for n in range(1,121):
   y=mul(y,x)
   if y==e:return n
  raise AssertionError
 orders={g:order(g) for g in G}
 chi_plus={1:4,2:4,3:1,4:0,5:-1,6:1,10:-1}
 chi_minus={1:4,2:-4,3:1,4:0,5:-1,6:-1,10:1}
 # The p-adic projective character is forced by its Brauer values and vanishing.
 psi={g:2*chi_plus[orders[g]] if orders[g]%2 else 0 for g in G}
 assert all(psi[g]==chi_plus[orders[g]]+chi_minus[orders[g]] for g in G)
 inner=sum(psi[g]*chi_minus[orders[g]] for g in G)
 assert inner==120
 assert sum(chi_minus[order(mul(g,g))] for g in G)==-120
 # On F2[G], multiplication by 1+z has one rank-one block per central coset.
 cosets={min(g,mul(z,g)) for g in G}
 assert len(cosets)==60
 return {"group_order":len(G),"element_order_counts":dict(sorted(Counter(orders.values()).items())),"central_cosets":len(cosets),"central_nilpotent_operator_rank":60,"central_nilpotent_kernel_dimension":60,"forced_projective_dimension":psi[e],"faithful_character_multiplicity":str(F(inner,120))}

def rank2(rows):
 basis={}
 for v in rows:
  while v:
   i=v.bit_length()-1
   if i in basis:v^=basis[i]
   else:basis[i]=v;break
 return len(basis)

def a5_augmentation():
 G=[p for p in permutations(range(5)) if sum(p[i]>p[j] for i in range(5) for j in range(i+1,5))%2==0]
 # Basis v_i=e_i+e_4, i=0,...,3, for the augmentation summand of F2^5.
 matrices=[]
 for g in G:
  bits=0
  for j in range(4):
   v=(1<<g[j])^(1<<g[4])
   for i in range(4):
    if (v>>i)&1:bits|=1<<(4*i+j)
  matrices.append(bits)
 span=rank2(matrices)
 assert len(G)==60 and span==16
 # V4 fixing position 4 acts regularly on 0,1,2,3; coordinates there identify
 # the augmentation module with the V4 regular representation.
 V4=[g for g in G if g[4]==4 and all(g[g[i]]==i for i in range(5))]
 assert len(V4)==4 and {g[0] for g in V4}==set(range(4))
 return {"group_order":60,"augmentation_dimension":4,"matrix_algebra_span_dimension":span,"absolutely_irreducible":True,"sylow_2_order":4,"restriction_regular":True}

def monoid_checks():
 # Coordinates (S1,T4,S4). A5 PIM/reduction data are credited in the proof.
 reductions={"V1":(1,0,0),"V5":(1,1,0),"V4":(0,0,1)}
 targets=[(8,4,0),(8,6,0),(0,0,2)]
 coeffs=[(4,4,0),(2,6,0),(0,0,2)]
 dims=(1,4,4)
 out=[]
 for target,c in zip(targets,coeffs):
  got=tuple(sum(c[i]*list(reductions.values())[i][j] for i in range(3)) for j in range(3))
  assert got==target
  out.append({"pim_composition_vector":target,"rational_witness_coefficients_V1_V5_V4":c,"dimension":sum(a*b for a,b in zip(target,dims))})
 # F2 regular G module is P1 + 2*PT + 4*PS (T has endomorphism field F4).
 assert 24+2*32+4*8==120
 return {"all_three_F2_pims":out,"regular_dimension_reconstruction":120}

def main():
 result={"icosian_character_construction":icosians(),"sl2_f5":sl2_checks(),"a5_simple_projective":a5_augmentation(),"positive_monoid":monoid_checks(),"all_assertions_passed":True}
 out=Path(__file__).with_name("counterexample_results.json")
 out.write_text(json.dumps(result,indent=2)+"\n")
 print(json.dumps(result,indent=2))
if __name__=="__main__":main()

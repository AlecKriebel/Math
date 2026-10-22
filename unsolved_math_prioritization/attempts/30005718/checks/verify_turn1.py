#!/usr/bin/env python3
"""Standard-library exact controls and symbolic boundary certificates."""
from fractions import Fraction as F
from itertools import product
from collections import Counter
import json
C=Counter()
def ck(a,k):assert a,k;C[k]+=1
def add(*ps):
 a=[0]*max(map(len,ps))
 for p in ps:
  for i,c in enumerate(p):a[i]+=c
 while len(a)>1 and not a[-1]:a.pop()
 return a
def mul(p,q):
 a=[0]*(len(p)+len(q)-1)
 for i,x in enumerate(p):
  for j,y in enumerate(q):a[i+j]+=x*y
 return a
# Polynomials in (r,w), reduced modulo w^4, with rational coefficients.
def const(a):return {(0,0):F(a)} if a else {}
def pa(*ps):
 q={}
 for p in ps:
  for ij,a in p.items():q[ij]=q.get(ij,F(0))+a
 return {ij:a for ij,a in q.items() if a}
def pm(p,q):
 r={}
 for (i,j),a in p.items():
  for (k,l),b in q.items():
   if j+l<4:r[i+k,j+l]=r.get((i+k,j+l),F(0))+a*b
 return {ij:a for ij,a in r.items() if a}
def sc(p,a):return {ij:a*b for ij,b in p.items() if a*b}
def ma(A,B):return [[pa(a,b) for a,b in zip(row,col)] for row,col in zip(A,B)]
def mm(A,B):return [[pa(*(pm(A[i][k],B[k][j]) for k in range(len(B)))) for j in range(len(B[0]))] for i in range(len(A))]
def ms(A,p):return [[pm(a,p) for a in row] for row in A]
R={(1,0):F(1)};W={(0,1):F(1)};W2=pm(W,W);W3=pm(W2,W)
I=[[const(1),{}],[{},const(1)]]
K=[[pa(const(1),sc(W,5),sc(W2,4),W3),pa(sc(W,3),sc(W2,2))],[pa(const(3),sc(W,5),sc(W2,2)),pa(const(1),sc(W,2),sc(W2,2),W3)]]
H=ma(K,ms(I,const(-1)));power=I;KR=[[{},{}],[{},{}]];choose=const(1)
for ell in range(8):
 KR=ma(KR,ms(power,choose));power=mm(power,H)
 choose=sc(pm(choose,pa(R,const(-ell))),F(1,ell+1))
ck(power==[[{},{}],[{},{}]],'symbolic_nilpotence_mod_w4')
U=[[pa(const(1),sc(W,2)),sc(W,2)]];v=[[sc(W,2)],[const(1)]]
L=[[pa(sc(W,2),W2),W],[pa(const(1),W),pa(W,W2)]]
def pr(cs):return {(i,0):F(c) for i,c in enumerate(cs) if c}
def pc(p,j):return {(i,0):a for (i,k),a in p.items() if k==j}
r1=pa(R,const(1));r2=pa(R,const(2));d_even=pr([4,3]);d_odd=pr([6,3])
top={
 'even':[d_even,sc(pm(r1,pr([8,21,9])),F(1,2)),sc(pm(pm(R,pr([2,3])),pr([142,177,102,27])),F(1,40))],
 'odd':[const(1),sc(pr([24,31,9]),F(1,2)),sc(pm(pm(r1,r2),pr([64,81,27])),F(1,8))]
}
margin_expected={
 'even':sc(pr([960,3376,7479,15039,19170,12879,4131,486]),F(1,20)),
 'odd':sc(pr([2112,6660,8201,4914,1431,162]),F(1,4))
}
for name,Mat,d in [('even',KR,d_even),('odd',mm(L,KR),d_odd)]:
 num=mm(mm(U,Mat),v)[0][0]
 ck(pc(num,0)=={},'reversal_numerator_divisible_by_w')
 for j in range(3):ck(pc(num,j+1)==top[name][j],'symbolic_top_coefficient_formula')
 a,b,c=top[name];gap=pa(pm(pa(d,const(-1)),pm(b,b)),sc(pm(pm(d,a),c),-2))
 ck(gap==margin_expected[name],'symbolic_top_ULC_margin')
 ck(all(q>0 for q in gap.values()),'positive_top_margin_coefficients')
 # Low margin at k=4, using n=2r+4 or 2r+5.
 n=pr([4 if name=='even' else 5,2]);a=const(4);b=pa(sc(n,12),const(-44));c=sc(pm(pa(n,const(-4)),pa(sc(n,4),const(-17))),4)
 gap=pa(sc(pm(pa(d,const(-4)),pm(b,b)),4),sc(pm(pm(pa(d,const(-3)),a),c),-5))
 expected=pr([0,352,1504,3072]) if name=='even' else pr([1328,5136,6624,3072])
 ck(gap==expected,'symbolic_low_ULC_margin');ck(all(q>0 for q in gap.values()),'positive_low_margin_coefficients')
def ev(p,r):return sum(a*r**i for (i,j),a in p.items())
T=[0,0,0,2,1];Q=[0,0,0,0,1];Cc=[0,0,0,2,2];D=[0,0,0,2]
for n in range(4,501):
 V=add(T,Q,Cc);d=len(V)-1
 ck(d==3*(n-1)//2,'degree')
 ck(all(V[k]>0 for k in range(3,d+1)),'no_internal_zero')
 ck(V[3]==4 and V[4]==12*n-44 and (V[5] if d>=5 else 0)==4*(n-4)*(4*n-17),'bottom_coefficients')
 name='even' if n%2==0 else 'odd';r=(n-(4 if name=='even' else 5))//2
 for j in range(3):ck(V[d-j]==ev(top[name][j],r),'top_formula_vs_original_recursion')
 ck(T==add(D,Q) and Cc==mul([1,1],D),'two_state_identity')
 for p in [T,Q,Cc,V]:
  dp=len(p)-1
  for k in range(1,dp):ck(k*(dp-k)*p[k]*p[k] >= (k+1)*(dp-k+1)*p[k-1]*p[k+1],'finite_ULC_inequality')
 # Simultaneously evolve the unreduced source recursion and reduced D recurrence.
 T,Q,Cc,D=add(mul([0,1],T),mul([1,1],Q),mul([1,1],Cc)),add(mul([1,1],Q),mul([0,1],Cc)),add(mul([0,1,1],T),mul([1,1],Cc)),add(mul([1,2],D),mul([0,1],Q))
# Explicit failure of an unrestricted componentwise ULC-preservation argument.
ck(2*2 < 1*100,'arbitrary_reduced_vector_not_LC')
ck(2*8*8 < 6*2*12,'stripped_D6_not_ULC_degree3')
print(json.dumps({'status':'PASS','assertions':sum(C.values()),'counts':dict(sorted(C.items())),'finite_range':[4,500],'proved_unbounded_scope':'ULC inequalities at k=4 and k=d_n-1; fixed-tail polynomial criterion; interior inequalities remain unresolved'},indent=2,sort_keys=True))

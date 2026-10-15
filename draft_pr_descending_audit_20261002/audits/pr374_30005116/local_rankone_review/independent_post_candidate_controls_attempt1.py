#!/usr/bin/env python3
"""Independent checks of exact candidate path/gap formulas; author code not read."""
from fractions import Fraction as F
from itertools import product
import sympy as S
from independent_controls import pattern_prob, density, CYCLE, unlabeled_prob
# All-parameter algebra, no bounded grid substitutes for these identities.
a,b,s,p=S.symbols('a b s p', positive=True)
u=a-s; e=b*s/u; v=b+e; z=s-e
assert S.factor(u*v-a*b)==0
assert S.factor(u+v+z-a-b)==0
assert S.factor(2*u*e-2*b*s)==0
assert S.factor(2*b*(e+z)-2*b*s)==0
assert S.factor(z)==s*(a-b-s)/(a-s)
assert S.factor(-3*b*(2*a+b)*(4*b*s)+12*b*b*s*(2*a+b))==0
print('all-parameter fixed-space path identities: PASS')
Rhi=3*p**4*(1-p)**2
assert S.factor(S.diff(Rhi,p)-6*p**3*(1-p)*(2-3*p))==0
assert Rhi.subs(p,S.Rational(2,3))==S.Rational(16,243)
assert Rhi.subs(p,S.Rational(1,2))==S.Rational(3,64)
assert S.diff(Rhi,p).subs(p,S.Rational(1,2))==S.Rational(3,16)
assert 3*(S.Rational(1,2)-S.Rational(3,4)**4)==S.Rational(141,256)
bracket=p*p*(1+p+p*p+p**3)-1
assert bracket.subs(p,S.Rational(3,4))==S.Rational(551,1024)
assert S.factor((1-p**4)-(1-p)/p**2-(1-p)*bracket/p**2)==0
assert 3*S.Rational(551,1024)==S.Rational(1653,1024)
print('profile junction, peak and claimed strict-gap constants: PASS')
# Direct full-step counts on the exact fixed-space path.
count=0
for r,aa in [(2,F(4,9)),(2,F(2,5)),(3,F(3,10)),(4,F(2,9))]:
    bb=1-r*aa
    assert 0<bb<aa
    for q in range(1,10):
      ss=(aa-bb)*F(q,10)
      uu=aa-ss; ee=bb*ss/uu; zz=ss-ee
      masses=[aa]*(r-1)+[uu,ee,zz,bb]
      n=len(masses); labels=list(range(r-1))+[r-1,r-1,r-1,r]
      oldmat=[[F(labels[i]!=labels[j]) for j in range(n)] for i in range(n)]
      newmat=[[F(0) for j in range(n)] for i in range(n)]
      for i in range(n):
        for j in range(n):
          if i<r-1 or j<r-1: newmat[i][j]=F(i!=j)
      U,E,Z,B=range(r-1,r+3)
      for i,j in [(U,E),(U,B)]: newmat[i][j]=newmat[j][i]=F(1)
      pp=density(masses,oldmat)
      assert density(masses,newmat)==pp
      cc=3*pattern_prob(masses,oldmat,CYCLE)
      assert 3*pattern_prob(masses,newmat,CYCLE)==cc
      diff=sum(masses[i]*masses[j]*abs(newmat[i][j]-oldmat[i][j]) for i in range(n) for j in range(n))
      assert diff==4*bb*ss
      # Independent direct 4-vertex paw count.
      paw=unlabeled_prob(masses,newmat,[1,2,2,3])
      assert paw==24*(r-1)*aa*aa*bb*zz
      count+=1
print('literal fixed-space path controls:',count,'PASS')
print('ALL POST-CANDIDATE INDEPENDENT CONTROLS PASSED')

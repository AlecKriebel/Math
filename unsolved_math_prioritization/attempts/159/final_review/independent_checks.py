from fractions import Fraction as F
import itertools,json,math
import sympy as S
count=0
# Reconstruct support incidence and forced units independently.
U={0,1,3,7};V={0,1,2,3,5,9,11,13};E={}
for u,v in itertools.product(U,V):E.setdefault(u+v,[]).append((u,v))
U1={e[0][0] for e in E.values() if len(e)==1};V1={e[0][1] for e in E.values() if len(e)==1}
assert U1=={0,7} and V1=={0,11,13};count+=1
assert all(len(E[u+v])==1 for u,v in itertools.product(U1,V1));count+=1
# Exact residual polynomial identity.
a,b,c,d,e,g=S.symbols('a b c d e g');F1=a+b-1;F2=a*b+c-1;F3=a*c+d+e-1;F8=c+g-1;F9=a*g+e-1;F11=d+a-1;F12=d+g-1
assert S.expand(2*a*F1-2*F2+F3+(2-a)*F8-F9+(1-2*a)*F11+(2*a-2)*F12)==1;count+=1
x=S.symbols('x');f=S.symbols('f');A=1+a*x+d*x**3+x**7;B=1+b*x+c*x*x+e*x**3+f*x**5+g*x**9+x**11+x**13
for k,v in zip([1,2,3,9,10,14,16],[F1,F2,F3,F8,F9,F11,F12]):assert S.expand(A*B).coeff(x,k)-1==v;count+=1
# All rational local reflection states satisfying the exact four constraints.
for den in range(1,21):
 grid=[F(i,den) for i in range(den+1)]
 for t in (0,1):
  for aa in grid:
   bb=t-aa
   if bb<0:continue
   for ar in grid:
    br=t-ar
    if br<0 or aa*br or ar*bb:continue
    assert aa==ar and bb==br and aa in(0,1) and bb in(0,1);count+=1
# Exact finite prefixes of the credited infinite formal series.
h=[F(math.comb(2*k,k),4**k) for k in range(151)]
for n in range(151):assert sum(h[k]*h[n-k] for k in range(n+1))==1;count+=1
for n in range(1,151):assert 0<h[n]*h[n]<1;count+=1
# Residue recurrence stays positive and crosses unit at first terminal coefficient.
for den in range(2,25):
 for num in range(1,den):
  a=F(num,den);q=F(1)
  for r in range(1,51):
   q=1-a*q;assert 0<q<1;assert q==(1-(-a)**(r+1))/(1+a);count+=2
print(json.dumps({'status':'PASS','assertions':count,'formal_prefix_degree':150,'reflection_denominators':20,'residue_rational_parameters':sum(range(1,24))},sort_keys=True))

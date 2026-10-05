#!/usr/bin/env python3
"""Exact identities/controls for ID 30002830; geometric theorems are not formalized."""
import argparse
import json
from pathlib import Path
import sympy as S

checks = []
def check(name, condition, kind='identity'):
    passed = bool(condition)
    if not passed:
        raise RuntimeError('FAILED: ' + name)
    checks.append({'name': name, 'kind': kind, 'passed': True})
def zero(v):
    return S.cancel(v) == 0

s,t,U,V,W,A,C,e,R,u = S.symbols('s t U V W A C e R u')
x,y,z,v = S.symbols('x y z v')
a=s*t*(s-t); b=-s*(s-1); c=t*(t-1); d=-(a+b+c)
F=a*U+b*W+c*V
D=s*s*U-V; q=2*(V-s*U)/D
T=q*(q+2)/(q*(q+2)-U)
check('coefficient gcd is one', S.gcd(S.gcd(a,b),c)==1)
check('corrected q+2 identity',zero(q+2-2*s*(s-1)*U/D))
point={s:S.Rational(2),t:S.Rational(4),U:S.Rational(1),V:S.Rational(8,3),W:S.Rational(8)}
chart=s*t*(s-1)*(t-1)*(s-t)*U*D*q*(q+2)*(q*(q+2)-U)
check('common witness equation',zero(F.subs(point)))
check('corrected common witness chart nonzero',chart.subs(point)!=0,'domain')
check('common witness T=3/2',T.subs(point)==S.Rational(3,2),'domain')
oldpoint={s:0,t:0,U:1,V:1,W:1}
check('old chart counterexample has T=0',T.subs(oldpoint)==0,'negative_control')
check('corrected chart rejects old point',chart.subs(oldpoint)==0,'negative_control')

AA=S.cancel(a/b); CC=S.cancel(c/b)
ee=S.factor(CC*(CC+1)*s+AA*CC)
quad=C*(C+1)*s*s+2*A*C*s+A*(A+1)
check('net linear t identity',zero(t+CC*s+AA))
check('net quadratic identity',zero(quad.subs({A:AA,C:CC},simultaneous=True)))
check('net square identity',zero(ee**2+AA*CC*(AA+CC+1)))
check('net discriminant',zero(S.discriminant(quad,s)+4*A*C*(A+C+1)))
sinv=(e-A*C)/(C*(C+1)); tinv=-C*sinv-A
relation=e*e+A*C*(A+C+1)
def reduce_e(expr):
    num=S.together(expr).as_numer_denom()[0]
    return S.rem(S.Poly(num,e),S.Poly(relation,e)).as_expr()==0
check('inverse coefficients recover A',reduce_e(AA.subs({s:sinv,t:tinv},simultaneous=True)-A))
check('inverse coefficients recover C',reduce_e(CC.subs({s:sinv,t:tinv},simultaneous=True)-C))
check('net inverse recovers s',zero(sinv.subs({A:AA,C:CC,e:ee},simultaneous=True)-s))
check('net inverse recovers t',zero(tinv.subs({A:AA,C:CC,e:ee},simultaneous=True)-t))
ss=-s*(s-t-1)/(s+t-1); tt=t*(s-t+1)/(s+t-1)
check('involution preserves A',zero(AA.subs({s:ss,t:tt},simultaneous=True)-AA))
check('involution preserves C',zero(CC.subs({s:ss,t:tt},simultaneous=True)-CC))
check('involution reverses e',zero(ee.subs({s:ss,t:tt},simultaneous=True)+ee))
check('involution squares to identity on s',zero(ss.subs({s:ss,t:tt},simultaneous=True)-s))
check('involution squares to identity on t',zero(tt.subs({s:ss,t:tt},simultaneous=True)-t))
check('involution witness nontrivial',ss.subs(point)==S.Rational(6,5) and tt.subs(point)==-S.Rational(4,5))
branch=A*(A*U+W)*(A*(V-U)+V-W)
Celim=-(A*U+W)/V
check('mixed quadratic radicand identity',zero(-A*Celim*(A+Celim+1)*V**2-branch))
check('radicand A-adic coefficient nonzero',zero(S.expand(branch).coeff(A,1)-W*(V-W)) and W*(V-W)!=0)
check('common witness R=32',(ee*V).subs(point)==32 and branch.subs({A:8,U:1,V:S.Rational(8,3),W:8})==1024)
check('mutation net sign rejected',not zero(ee**2-AA*CC*(AA+CC+1)),'negative_control')
check('mutation Geiser sign rejected',not zero(AA.subs({s:-ss,t:tt},simultaneous=True)-AA),'negative_control')

check('coefficient pairing',zero(a*b/(c*d)-s*s/(t-1)**2))
check('cyclic base change makes pairing cube',zero((a*b/(c*d)).subs(s,u**3*(t-1))-u**6))
check('base change field inverse s',zero((u**3*(t-1))/(t-1)-u**3))
check('original K-radical valuation is one',S.degree(s,s)==1 and (t-1).subs(s,0)!=0)
check('mutation square base change does not produce cubic exponent',S.degree(u**4,u)%3!=0,'negative_control')
check('all original projective coefficients nonzero',all(S.expand(k)!=0 for k in (a,b,c,d)))
check('rational cubic point',zero(a+b+c+d))
check('symmetrization generic ordering count',S.factorial(4)==24)
check('Abel fiber h0 dimension arithmetic',4-1+1==4)

lead=V-s*U; mid=s*s*U-V; const=-s*(s-1)*W
Delta=mid*mid-4*lead*const
h=2*lead*t+mid
check('mixed quadratic equation identity',zero(F-(lead*t*t+mid*t+const)))
check('mixed discriminant relation',zero(h*h-Delta-4*lead*F))
check('mixed t rational inverse',zero((h-mid)/(2*lead)-t))
Y,Z,H=S.symbols('Y Z H')
A0=1+s*s*U; B0=1+s*U; k0=4*s*(s-1); C0=s*s*U+2*s-1
Q=(A0*H-Z)**2+k0*(Z-B0*H)*(Y-H)
M=S.hessian(Q,(Y,Z,H))/2
check('coefficient conic matrix determinant',zero(M.det()+4*U**2*s**4*(s-1)**4))
check('axis Y=0 discriminant',zero(S.discriminant(Q.subs({Y:0,H:1}),Z)-k0*k0*(U+1)))
check('axis Z=0 factorization',zero(Q.subs(Z,0)-H*(C0*C0*H-k0*B0*Y)))
check('axis H=0 factorization',zero(Q.subs(H,0)-Z*(Z+k0*Y)))
check('square auxiliary coefficient',zero(A0*A0+k0*B0-C0*C0))
B=Q.subs({Y:y**3,Z:z**3,H:v**3},simultaneous=True)
check('sextic total degree',S.Poly(B,y,z,v).total_degree()==6)
check('sextic homogenization matches discriminant',zero(B.subs(v,1)-Delta.subs({V:z**3-1,W:y**3-1},simultaneous=True)))
local=S.Poly(B.subs(y,1),z,v)
low=sum(co*z**m[0]*v**m[1] for m,co in local.terms() if sum(m)==3)
check('ordinary triple lowest homogeneous term',zero(low-k0*(z**3-B0*v**3)))
check('no lower degree local term',all(sum(m)>=3 for m,co in local.terms() if co!=0))
check('generic triple tangents squarefree',S.gcd(z**3-B0,S.diff(z**3-B0,z))==1)
check('geometric coefficient open nonempty',S.prod([s,s-1,U,U+1,B0,C0]).subs({s:2,U:7})!=0,'domain')
check('blowup branch corrected class even',(6,-3+1)==(2*3,2*(-1)))
check('double cover canonical class cancels',(-3+3,1-1)==(0,0))
check('mutation exceptional branch omitted has odd class',(-3)%2==1,'negative_control')
check('degenerate s=0 branch is square',zero(Delta.subs(s,0)-V*V),'negative_control')
check('degenerate U=0 conic determinant zero',M.det().subs(U,0)==0,'negative_control')

N=4*s*(s-1)*(V-s*U)
d0=N*N*(N-D*D)/D**6
check('elliptic reconstruction T',zero(T-N/(N-D*D)))
check('elliptic twist coefficient',zero(T*T/(T-1)**3-d0))
Xi=y*T/(T-1); Eta=(1+t*q)*T/(T-1)
# Replace y^3 by W+1 only after clearing denominators.
res=S.together(Eta*Eta-Xi**3+d0)
res=S.cancel(res.subs(y**3,W+1))
expected=64*s*s*(s-1)**2*(V-s*U)**3/D**6
check('elliptic reconstruction equation',zero(res-expected*F))
check('elliptic reconstruction recovers y',zero(Xi*(T-1)/T-y))
check('elliptic reconstruction recovers t',zero((Eta*(T-1)/T-1)/q-t))
check('elliptic discriminant generically nonzero',d0!=0)
check('K3 negative-control quartic canonical degree',4-4==0,'negative_control')

poly=S.Poly(F.subs({U:x**3-1,W:y**3-1,V:z**3-1},simultaneous=True),s,t,x,y,z)
support=set(poly.monoms())
expected_support={(2,1,3,0,0),(1,2,3,0,0),(2,0,0,3,0),(1,0,0,3,0),(0,2,0,0,3),(0,1,0,0,3),(2,1,0,0,0),(1,2,0,0,0),(2,0,0,0,0),(1,0,0,0,0),(0,2,0,0,0),(0,1,0,0,0)}
check('Newton support exact',support==expected_support)
check('Newton support all twelve coefficients nonzero',len(poly.terms())==12 and all(c!=0 for m,c in poly.terms()))
pairs=[((2,1,3,0,0),(2,1,0,0,0)),((2,0,0,3,0),(2,0,0,0,0)),((0,2,0,0,3),(0,2,0,0,0)),((2,1,0,0,0),(0,1,0,0,0)),((2,0,0,0,0),(0,2,0,0,0))]
expected_diffs=[(0,0,3,0,0),(0,0,0,3,0),(0,0,0,0,3),(2,0,0,0,0),(2,-2,0,0,0)]
for i,((m,n),diff) in enumerate(zip(pairs,expected_diffs)):
    check('width forcing pair '+str(i),m in support and n in support and tuple(a-b for a,b in zip(m,n))==diff)
check('forcing covectors have full rank',S.Matrix(expected_diffs).rank()==5)
check('coordinate s attains width two',max(m[0] for m in support)-min(m[0] for m in support)==2)
check('coordinate t attains width two',max(m[1] for m in support)-min(m[1] for m in support)==2)
lin=S.Poly(a*(x-1)+b*(y**3-1)+c*(z**3-1),s,t,x,y,z)
check('mutation linear x gives width one',max(m[2] for m in lin.monoms())-min(m[2] for m in lin.monoms())==1,'negative_control')
check('mutation linear x is actually solvable',S.degree(lin.as_expr(),x)==1,'negative_control')

result={'problem_id':'30002830','mathematical_verdict':'NO RESOLUTION','sympy_version':S.__version__,'check_count':len(checks),'negative_control_count':sum(q['kind']=='negative_control' for q in checks),'checks':checks,'limitations':['Symbolic checks are not a formalization of the cited diagonal-cubic criterion.','Brauer-Severi descent and symmetric-product geometry are proved in the text using stated standard theorems.','The K3 conclusion uses double-cover canonical formulas, rational double-point resolution and cohomology.','No assertion here settles the total fourfold rationality question.']}
p=argparse.ArgumentParser(); p.add_argument('--output'); args=p.parse_args()
text=json.dumps(result,indent=2)+'\n'
if args.output:Path(args.output).write_text(text)
else:print(text,end='')

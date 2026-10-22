"""Exact controls for the flag-affine twisted-degree obstruction."""
import sympy as s
from collections import Counter
import json
C=Counter()
def ck(v,k):
    assert v,k
    C[k]+=1
def eq(a,b,k): ck(s.cancel(s.expand(a-b))==0,k)
x,y,z=s.symbols('x y z')
a,c,e=s.symbols('a c e',nonzero=True)
b,h,q0,q1,r0,r1=s.symbols('b h q0 q1 r0 r1')
D=x*x*y+z*z
G={x:x,z:z+x*D,y:y-2*x*y*z-D**2+6*z*z*D+6*x*z*D**2+2*x*x*D**3}
X=a*x+b; Z=e*z+q0+q1*x; Y=c*y+h*z+r0+r1*x
d={x:X,y:Y,z:Z}
ix=(x-b)/a;iz=(z-q0-q1*ix)/e
iv={x:ix,z:iz,y:(y-h*iz-r0-r1*ix)/c}
for v in (x,y,z):eq(iv[v].xreplace(d),v,'affine_inverse')
Dp=X*X*Y+Z*Z
F={x:x,z:z+X*Dp/e,y:y-2*X*Y*Z/c-Dp**2/c+6*Z*Z*Dp/c+
   6*X*Z*Dp**2/c+2*X*X*Dp**3/c-h*X*Dp/(c*e)}
for v in (x,y,z):eq(iv[v].xreplace(G).xreplace(d),F[v],'general_flag_conjugation')
for v,degree,monomial,coef in [(y,6,(0,6),2*X**2*e**6/c),(z,2,(0,2),X*e)]:
    p=s.Poly(s.expand(F[v]),y,z)
    ck(p.total_degree()==degree,'initial_fiber_degree')
    eq(p.coeff_monomial(monomial),coef,'initial_leading_coefficient')
    ck(sum(1 for m,co in p.terms() if sum(m)==degree)==1,'unique_initial_leading_monomial')
    weight=max(3*i+j for (i,j),co in p.terms())
    target=9 if v==y else 3
    ck(weight==target,'weighted_degree')
    ck(sum(1 for (i,j),co in p.terms() if 3*i+j==weight)==1,'unique_weighted_leading_monomial')
    eq(p.coeff_monomial(y**3 if v==y else y),2*X**8*c**2 if v==y else X**3*c/e,'weighted_leading_coefficient')

# Verify the telescoping identity in an abstract free group, so it uses no
# implicit commutation between the arbitrary conjugator and affine map.
def red(word):
    out=[]
    for letter in word:
        if out and out[-1]==-letter:out.pop()
        else:out.append(letter)
    return out
for n in range(1,31):
    w=[]
    for j in range(n):w += [2]*j+[1,2,-1,-2]+[-2]*j
    ck(red(w)==[1]+[2]*n+[-1]+[-2]*n,'arbitrary_conjugator_telescoping')

# The obstruction is not a subgroup-membership test: h=Q E is an exact
# two-polynomial-exponential word, yet all its translated twisted products grow.
Q={x:x,y:y+z**3,z:z};E={x:x,y:y,z:z+y}
hh={v:E[v].xreplace(Q) for v in (x,y,z)}
eq(hh[y],y+z**3,'allowed_two_flow_countercheck')
eq(hh[z],z+y+z**3,'allowed_two_flow_countercheck')
Ei={x:x,y:y,z:z-y}
for v in (x,y,z):eq(Ei[v].xreplace(hh),Q[v],'nonflag_affine_cancellation')
# Specialize the independent variable to a single indeterminate. The universal
# no-cancellation statements are proved by the weighted calculation, not sampled.
w=s.symbols('w')
for shifts in [[(0,0),(1,2),(-2,3)],[(2,-1),(0,2),(4,-3)]]:
    U,V=s.Poly(0,w),s.Poly(w,w)
    for j,(bb,cc) in enumerate(shifts,1):
        newU=U+(V+cc)**3
        newV=V+U+bb+(V+cc)**3
        U,V=newU,newV
        ck(U.degree()==3**j and V.degree()==3**j,'translated_allowed_word_degree')

print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),
 'scope':'Exact flag-affine conjugation and leading terms, formal telescoping, and an allowed-word counterexample to overinterpreting the obstruction. Full generalized-tame membership is unresolved.'},indent=2,sort_keys=True))

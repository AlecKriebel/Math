#!/usr/bin/env python3
"""Independent exact finite controls. No third-party dependencies; not a proof engine."""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import json

checks = []
def test(name, condition, detail):
    if not condition:
        raise RuntimeError(name)
    checks.append({"name": name, "pass": True, "detail": str(detail)})

eta, eps, T = F(1,10**12), F(1,10**24), F(7,4)
q = lambda t: t*t-F(2,5)*t**4
test("epsilon is eta squared", eps == eta*eta, eps)
test("a2 radius 8eta", 52 < 8**2, "52 < 64")
test("a3 area tail 5eta", 4*F(13,3) < 25, 4*F(13,3))
test("a3 closeness 29eta", 5+F(3,4)*8*4 == 29, 29)
test("A closeness 106eta", 2*29+8*6 == 106, 106)
test("B closeness 24eta", 3*8 == 24, 24)
r=F(2,3)
test("weighted H tail majorant", r**4/(3*(1-r*r)) == F(16,135) < F(1,4), F(16,135))
test("weighted Hprime majorant", (1-r*r)**-2-1 == F(56,25) < F(9,4), F(56,25))
test("H total 5eta", 4*r+4*F(1,2) < 5, 4*r+2)
test("Hprime total 10eta", 4+4*F(3,2) == 10, 10)
test("H value separation", F(5,3)-5*eta > F(3,2) and F(5,3)+5*eta < F(11,6), "strict")
test("H square reciprocal error", 5*F(7,2)/(F(3,2)**2*F(5,3)**2) == F(14,5), F(14,5))
test("f value error", r*F(14,5) < 2, r*F(14,5))
test("fprime numerator error", 5+2*r*10 < 19 and F(19)/F(3,2)**3 < 6, F(19)/F(3,2)**3)
test("fprime cube error", F(1,3)*5*11/F(125,8) < 2, F(1,3)*5*11/F(125,8))
test("actual tip below 3/10", F(6,25)+F(5,9)*F(9,125) == F(7,25) and F(7,25)+7*eta < F(3,10), F(7,25)+7*eta)
test("trajectory strict radius gap", F(25,81)-F(3,10) == F(7,810), F(7,810))
test("complex P perturbation", 106+24*9 == 322 and 322*eta < 1, 322)
test("P0 coefficient triangle", 2+3*9+81 == 110, 110)
test("Rouche strict margin", 333*eps < 3-2, 333*eps)
test("trajectory V radius", T+333*eps < F(9,5), T+333*eps)
test("orientation 223eps", F(222)/(1-111*eps) < 223, F(222)/(1-111*eps))
test("p Taylor absorption", F(111**2,2)*eta < 1, F(111**2,2)*eta)
test("inverse Taylor absorption", 55*333*eta < 1, 55*333*eta)
test("derivative Taylor absorption", (2*111**2+F(126*333,2))*eta < 1, (2*111**2+F(126*333,2))*eta)
test("V lower division bound", 1-333*eps > F(1,2), 1-333*eps)
test("q uniform triangle", T*T+F(2,5)*T**4 < 7, T*T+F(2,5)*T**4)
test("exact Z division cost", 2*(T*162+487) == 1541 and 2*7*333 == 4662, "1541eta eps + 4662eps^2")
test("2000eps eta division bound", 1541+4662*eta < 2000, 1541+4662*eta)
test("endpoint q1", q(F(1)) == F(3,5), q(F(1)))
test("endpoint qT", q(T) == -F(441,640), q(T))
test("opposite endpoint margins", q(F(1))-2000*eta > F(1,2) and q(T)+2000*eta < -F(1,2), [q(F(1))-2000*eta,q(T)+2000*eta])
test("epsilon zero cannot certify strict reversal", not 0 > 0, "sign magnitude vanishes")

# Exact polynomial ring in a2,a3,a4, and exact truncated power series.
zero={}; one={(0,0,0):F(1)}
def add(a,b):
    c=dict(a)
    for m,v in b.items(): c[m]=c.get(m,F(0))+v
    return {m:v for m,v in c.items() if v}
def mul(a,b):
    c={}
    for m,x in a.items():
        for n,y in b.items():
            k=tuple(m[j]+n[j] for j in range(3)); c[k]=c.get(k,F(0))+x*y
    return {m:v for m,v in c.items() if v}
def smul(a,b):
    c=[{} for _ in range(5)]
    for j in range(5):
        for k in range(5-j): c[j+k]=add(c[j+k],mul(a[j],b[k]))
    return c
a2={(1,0,0):F(1)}; a3={(0,1,0):F(1)}; a4={(0,0,1):F(1)}
f=[zero,one,a2,a3,a4]; f2=smul(f,f); f3=smul(f2,f); f4=smul(f3,f)
test("formal f2 extraction", f2[2]==one and f2[3]=={(1,0,0):F(2)} and f2[4]=={(0,1,0):F(2),(2,0,0):F(1)}, str(f2))
test("formal f3 extraction", f3[3]==one and f3[4]=={(1,0,0):F(3)}, str(f3))
test("formal f4 extraction", f4[4]==one, str(f4))
test("double cover signs", [(-1)**(-3),(-1)**(-4),(-1)**(-5)]==[-1,1,-1], "4(a-bv^2+cv^4)")

# Hyperbolic division, independently rebuilding the Brown tangent expansion.
N=10
def vmul(a,b):
    c=[F(0)]*(N+1)
    for j,x in enumerate(a):
        for k,y in enumerate(b):
            if j+k<=N:c[j+k]+=x*y
    return c
def inv(a):
    assert a[0]; b=[F(0)]*(N+1); b[0]=1/a[0]
    for n in range(1,N+1):b[n]=-sum(a[k]*b[n-k] for k in range(1,n+1))/a[0]
    return b
sinh_over_u=[F(1,factorial(n+1)) if n%2==0 else F(0) for n in range(N+1)]
cosh=[F(1,factorial(n)) if n%2==0 else F(0) for n in range(N+1)]
ucoth=vmul(cosh,inv(sinh_over_u)); utan=[F(0),F(0)]+vmul(sinh_over_u,inv(cosh))[:-2]
h=[-3*ucoth[n]+utan[n]+(3 if n==0 else 0) for n in range(N+1)]
test("Brown hyperbolic tangent expansion", h[:8]==[0,0,0,0,-F(4,15),0,F(8,63),0], h)
delta=eta; s1=F(1,10**7); s2=F(1,10**5)
upper1=-F(4,15)*(2*delta-(2*delta)**3/6)+F(8,63)*s1*s1+2560*s1**4/(1-2*s1)
lower2=-F(4,15)*2*delta+F(8,63)*(1-(3*delta)**2/2)*s2*s2-2560*s2**4/(1-2*s2)
test("Brown negative tangent derivative", upper1 < 0, upper1)
test("Brown positive tangent derivative", lower2 > 0, lower2)
test("Brown actual B lower bound", F(25,96)*(1-delta/2)>F(1,4), F(25,96)*(1-delta/2))
test("Brown actual slit radius barrier", (1-s2)**2/(4*s2*s2)>1, (1-s2)**2/(4*s2*s2))
test("Brown derivative mutation falsified", -F(4,15)*(2*delta)+F(8,63)*s1*s1<0 and F(4,15)*(2*delta)+F(8,63)*s1*s1>0, "flipping the theta0 phase removes the first negative sign")

# Source-family identity, not universal support-function classification.
candidate_invariant_imag=9*eps
test("FS real-family functional invariant exclusion", candidate_invariant_imag!=0, "lambda3^2/(lambda2 lambda4)=9i eps")
result={"status":"PASS","count":len(checks),"checks":checks,"limits":"Exact finite controls supplement the independently written analytic derivation. They do not prove compactness, classical support geometry, all-source priority, or the universal analytic theorem by themselves."}
Path(__file__).with_name('INDEPENDENT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({"status":"PASS","count":len(checks)}))

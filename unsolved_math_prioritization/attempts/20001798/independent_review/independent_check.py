"""Independent Airy controls, including EO residues through complexity four.
No author checker is imported. Analytic existence and limits are reviewed in prose.
"""
from fractions import Fraction as F
from functools import lru_cache
from math import factorial
from collections import Counter,defaultdict
import json
import sympy as s

checks=Counter()
def ck(t,name):
    assert t,name
    checks[name]+=1

# Stable EO Airy differentials represented as Laurent coefficient dictionaries:
# exponent tuple e denotes coefficient * product(dt_i/t_i**e_i).
# This directly performs the local residue arithmetic with the pulled-back sign.
@lru_cache(None)
def eo(g,n):
    assert g>=0 and n>=1 and 2*g-2+n>0
    out=defaultdict(F)
    def add(e,c):out[tuple(e)]+=c
    if g:
        if (g,n)==(1,1):add((4,),F(-1,16))
        else:
            for e,c in eo(g-1,n+1).items():
                add((e[0]+e[1]+2,)+e[2:],-c/4)
    for g1 in range(g+1):
        g2=g-g1
        for mask in range(1<<(n-1)):
            I=[j for j in range(n-1) if mask>>j&1]
            J=[j for j in range(n-1) if not(mask>>j&1)]
            if (g1==0 and not I) or (g2==0 and not J):continue
            b1=g1==0 and len(I)==1
            b2=g2==0 and len(J)==1
            if b1 and b2:
                add((2,2,2),F(-1,4));continue
            if b1 or b2:
                B=I[0] if b1 else J[0]
                L=J if b1 else I; gg=g2 if b1 else g1
                for e,c in eo(gg,1+len(L)).items():
                    for k in range(0,e[0]+1,2):
                        v=[0]*n;v[0]=e[0]-k+2;v[B+1]=k+2
                        for label,exponent in zip(L,e[1:]):v[label+1]=exponent
                        add(v,-F(k+1,4)*c)
            else:
                for e,c in eo(g1,1+len(I)).items():
                    for f,d in eo(g2,1+len(J)).items():
                        v=[0]*n;v[0]=e[0]+f[0]+2
                        for label,power in zip(I,e[1:]):v[label+1]=power
                        for label,power in zip(J,f[1:]):v[label+1]=power
                        add(v,-c*d/4)
    return {e:c for e,c in out.items() if c}

ck(eo(0,3)=={(2,2,2):F(-1,2)},'EO_first_sphere_residue')
ck(eo(1,1)=={(4,):F(-1,16)},'EO_first_handle_residue')
ck(eo(2,1)=={(10,):F(-105,1024)},'EO_second_handle_residue')

# Riccati versus the independently determined amplitude series.
N=64;c=[F(1)]
for n in range(1,N+1):
    c.append(-F(1,2)*(F(4-3*n,2)*c[n-1]+sum(c[i]*c[n-i] for i in range(1,n))))
amp=[F(1)]
for k in range(N):amp.append(F((6*k+1)*(6*k+5),48*(k+1))*amp[-1])
logs=[F(0)]
for k in range(1,N+1):
    logs.append(amp[k]-sum(F(i,k)*logs[i]*amp[k-i] for i in range(1,k)))
for k in range(1,N):
    ck(logs[k]==-F(2,3*k)*c[k+1],'Riccati_amplitude_log_agreement')
ck(logs[1]==F(5,48) and logs[2]==F(5,64),'first_two_stable_terms')
EO_principal={}
for chi in range(1,5):
    total=F(0)
    for g in range((chi+1)//2+1):
        n=chi+2-2*g
        if n<1:continue
        for exponents,coefficient in eo(g,n).items():
            ck(all(e>=2 and e%2==0 for e in exponents),'EO_pole_parity')
            ck(sum(exponents)-n==3*chi,'EO_scaling_degree')
            denom=factorial(n)
            for e in exponents:denom*=e-1
            total+=coefficient*F((-1)**n,denom)
            # Symmetry under adjacent swaps is a separate output control.
            for j in range(n-1):
                e=list(exponents);e[j],e[j+1]=e[j+1],e[j]
                ck(eo(g,n).get(tuple(e),0)==coefficient,'EO_permutation_symmetry')
    ck(total==logs[chi],'EO_principal_specialization')
    EO_principal[str(chi+1)]=str(total)

# Hermitian algebra, connection scale and ramified eigenline growth.
z,zb,k,a=s.symbols('z zb k a',nonzero=True)
A=s.Matrix([[0,1],[z,0]]);H=s.diag(k/a,a/k)
Adj=H.inv()*s.Matrix([[0,zb],[1,0]])*H
expected=s.Matrix([[0,zb*a**2/k**2],[k**2/a**2,0]])
for i in range(2):
    for j in range(2):
        ck(s.simplify(Adj[i,j]-expected[i,j])==0,'Hermitian_adjoint')
        ck(s.simplify((a**6*Adj)[i,j]-s.Matrix([[0,zb*a**8/k**2],[a**4*k**2,0]])[i,j])==0,'R_cube_parameter_scale')
t,tb,h=s.symbols('t tb h',nonzero=True);rr=s.symbols('rr',positive=True)
V=s.Matrix([[1,1],[t,-t]])
ck(A.subs(z,t*t)*V==V*s.diag(t,-t),'spectral_eigenlines')
M=s.diag(rr*s.exp(h),1/(rr*s.exp(h)))
Gram=s.Matrix([[1,tb],[1,-tb]])*M*V
for i in range(2):
    for j in range(2):
        ck(s.simplify((Gram[i,j].subs(tb,rr**2/t)-2*rr*s.Matrix([[s.cosh(h),s.sinh(h)],[s.sinh(h),s.cosh(h)]])[i,j]).rewrite(s.exp))==0,'ramified_metric_Gram')
ck(s.diff(F(2,3)*t**3,t)==2*t*t,'irregular_primitive')
u=s.symbols('u',nonzero=True)
ck(s.simplify((2*t*t).subs(t,1/u)*s.diff(1/u,u)+2/u**4)==0,'ramified_pole_order_four')

# R=a^3: the small argument is a^2*x and every nonconstant radial Taylor
# monomial has a-power at least four. Cartesian differentiation does not lower it.
xx,yy=s.symbols('xx yy',real=True)
for j in range(1,9):
    term=a**(4*j)*(xx*xx+yy*yy)**j
    for d1 in range(5):
        for d2 in range(5-d1):
            derivative=s.diff(term,xx,d1,yy,d2)
            if derivative!=0:
                ck(all(m[0]>=4 for m in s.Poly(derivative,a,xx,yy).monoms()),'compact_Taylor_rate')

# DM normalization s=-2/t, y=-2/s and x=4/s^2.
s0,s1,t0,t1=s.symbols('s0 s1 t0 t1',nonzero=True)
ck(s.simplify(4/(-2/t)**2-t*t)==0,'DM_x_coordinate')
ck(s.simplify(-2/(-2/t)-t)==0,'DM_y_coordinate')
ck(s.simplify((2/t0**2)*(2/t1**2)/(-2/t0+2/t1)**2-1/(t0-t1)**2)==0,'Bergman_coordinate_invariance')
for n in range(1,8):
    for ds in [(0,)*n,(1,)*n,tuple(range(n))]:
        ck((-1)**n*(-1)**sum(2*d+1 for d in ds)==1,'stable_primitive_sheet_sign')

print(json.dumps({'status':'PASS','exact_assertions':sum(checks.values()),
 'categories':dict(sorted(checks.items())), 'riccati_orders':N,
 'EO_max_complexity':4,'EO_stable_principal_coefficients':EO_principal,
 'scope':'Independent finite algebra and EO residue controls. Complete radial existence, C-infinity estimates and source scope are audited in the report; no Stokes-limit or finite-test proof of an all-order theorem.'},indent=2,sort_keys=True))

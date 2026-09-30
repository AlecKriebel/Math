#!/usr/bin/env python3
"""Exact recurrence, ODE reconstruction, and four-site root certificate."""
from pathlib import Path
from fractions import Fraction as Q
from hashlib import sha256
import json
import sympy as s

ROOT=Path(__file__).resolve().parent
counts={}


def ck(name,condition):
    if not bool(condition):
        raise AssertionError(name)
    counts[name]=counts.get(name,0)+1


u,v,t,d,A,h=s.symbols('u v t d A h',positive=True)
P=[s.S(1),u]
D=[s.S(1),1+u]
for m in range(2,11):
    P.append(s.expand(u*P[-1]+v*D[-2]))
    D.append(s.expand(D[-1]+P[-1]))
for N in range(1,11):
    pp=s.Poly(P[N],u)
    dd=s.Poly(D[N],u)
    ck('monic_P',pp.degree()==N and pp.LC()==1)
    ck('missing_subleading_P',pp.coeff_monomial(u**(N-1))==0)
    ck('monic_D',dd.degree()==N and dd.LC()==1)
    ck('subleading_D',dd.coeff_monomial(u**(N-1))==1)
    ck('positive_recurrence_coefficients',all(c>=0 for c in s.Poly(P[N],u,v).coeffs()))
    expr=s.expand(t*D[N].subs(u,d+t)-A*(h-t)*P[N-1].subs(u,d+t))
    f=s.Poly(expr,t)
    ck('scalar_degree',f.degree()==N+1 and f.LC()==1)
    ck('scalar_subleading',s.expand(f.coeff_monomial(t**N)-(N*d+1+A))==0)
    ck('scalar_constant',s.expand(f.eval(0)+A*h*P[N-1].subs(u,d))==0)
    ck('physical_right_endpoint',s.expand(f.eval(h)-h*D[N].subs(u,d+h))==0)


def recurrence(N,u,v):
    ps=[Q(1)];ds=[Q(1)]
    if N:
        ps.append(u);ds.append(1+u)
    for m in range(2,N+1):
        ps.append(u*ps[-1]+v*ds[-2])
        ds.append(ds[-1]+ps[-1])
    return ps,ds


# Construct positive parameter classes with a specified equilibrium bound total.
# sigma is not a conserved variable; the binding balance enforces its value.
parameter_sets=[
    dict(sigma=Q(1,2),freeL=Q(1,2),freeR=Q(1,2),phi=Q(1),nu=Q(1,10000),
         b=Q(1,10000),gamma=Q(1),ST=Q(20),alpha=Q(1),beta=Q(1)),
    dict(sigma=Q(2,3),freeL=Q(3,2),freeR=Q(5,4),phi=Q(3,2),nu=Q(2,7),
         b=Q(3,5),gamma=Q(7,3),ST=Q(5,2),alpha=Q(2),beta=Q(3)),
    dict(sigma=Q(3,7),freeL=Q(1,4),freeR=Q(7,5),phi=Q(2),nu=Q(3,8),
         b=Q(1,6),gamma=Q(5,4),ST=Q(7,2),alpha=Q(1,3),beta=Q(2,5)),
]
for N in range(1,11):
    for a in parameter_sets:
        sigma=a['sigma'];L=sigma+a['freeL'];R=sigma+a['freeR']
        kappa=a['nu']*sigma/(a['freeL']*a['freeR'])
        for j in (1,3,6):
            S=a['ST']*Q(j,7)
            tt=a['gamma']*S/a['phi']
            dd=(a['b']+a['nu'])/a['phi'];vv=a['nu']/a['phi']
            hh=a['gamma']*a['ST']/a['phi'];aa=a['alpha']*sigma/a['beta']
            ps,ds=recurrence(N,dd+tt,vv)
            C=[sigma*ps[N-i]/ds[N] for i in range(N+1)]
            ck('bound_total_reconstruction',sum(C)==sigma)
            ck('physical_free_pools',L-sum(C)>0 and R-sum(C)>0 and 0<S<a['ST'])
            for c in C:
                ck('positive_receptor_concentrations',c>0)
            q=a['b']+a['gamma']*S
            rhs0=kappa*(L-sum(C))*(R-sum(C))+q*C[1]-(a['phi']+a['nu'])*C[0]
            ck('original_receptor_ODE',rhs0==0)
            for i in range(1,N):
                rhs=a['phi']*C[i-1]+q*C[i+1]-(a['phi']+q+a['nu'])*C[i]
                ck('original_receptor_ODE',rhs==0)
            ck('original_receptor_ODE',a['phi']*C[N-1]-(q+a['nu'])*C[N]==0)
            ff=tt*ds[N]-aa*(hh-tt)*ps[N-1]
            rhsS=a['alpha']*C[1]*(a['ST']-S)-a['beta']*S
            ck('exact_scalar_feedback_residual',rhsS==-a['beta']*a['phi']*ff/(a['gamma']*ds[N]))

# The sharp four-site witness: no numerical root solver.
f4=s.Poly(s.expand(t*D[4].subs({u:t+s.Rational(1,5000),v:s.Rational(1,10000)})
    -s.Rational(1,2)*(20-t)*P[3].subs({u:t+s.Rational(1,5000),v:s.Rational(1,10000)})),t)
scale=625000000000000
coeff=[625000000000000,938000000000000,-5624249850000000,
       621812687520000,624093093765001,-625250050000]
q=s.Poly.from_list(coeff,t)
ck('integer_certificate',s.expand(q.as_expr()-scale*f4.as_expr())==0)
bracket_points=[s.S(0),s.Rational(1,100),s.S(1),s.S(3)]
expected=[-625250050000,s.Rational(567224734905201,100),
          -2815969318764999,83466222268925003]
for point,value in zip(bracket_points,expected):
    ck('exact_bracket_value',q.eval(point)==value)
for i in range(3):
    ck('alternating_bracket_signs',expected[i]*expected[i+1]<0)
    ck('brackets_below_ST',0<=bracket_points[i]<bracket_points[i+1]<20)
signs=[1 if c>0 else -1 for c in coeff if c]
changes=sum(a!=b for a,b in zip(signs,signs[1:]))
ck('Descartes_exact_three',changes==3)
ck('binding_total_half',Q(1,5000)*Q(1,2)**2==Q(1,10000)*Q(1,2))

out={'problem_id':30003741,'status':'PASS_SCOPED_EXACT_RESULTS',
     'artifact_sha256':sha256((ROOT/'PARTIAL.md').read_bytes()).hexdigest(),
     'verifier_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
     'exact_assertions':sum(counts.values()),'families':counts,
     'four_site_integer_coefficients_descending':coeff,
     'four_site_sign_points':[str(x) for x in bracket_points],
     'four_site_exact_values':[str(x) for x in expected],
     'sympy_version':s.__version__,
     'scope':'Written induction proves the all-N coefficient bound. Exact signs and Descartes certify three positive scalar roots at N=4; no stability or global three-root ceiling for N>=5 is certified.'}
(ROOT/'verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

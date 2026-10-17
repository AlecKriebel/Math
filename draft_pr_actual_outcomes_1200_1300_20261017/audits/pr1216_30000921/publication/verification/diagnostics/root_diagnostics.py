#!/usr/bin/env python3
"""Exact finite algebra diagnostics, subordinate to the infinite analytic proof."""
from pathlib import Path
from fractions import Fraction as Q
from dataclasses import dataclass
from math import factorial as fact, comb
import json

ROOT=Path(__file__).resolve().parent
def require(c,m):
    if not c:raise ValueError(m)
@dataclass(frozen=True)
class G:
    r:Q=Q(0)
    i:Q=Q(0)
    def __add__(s,o):
        o=as_g(o);return G(s.r+o.r,s.i+o.i)
    __radd__=__add__
    def __neg__(s):return G(-s.r,-s.i)
    def __sub__(s,o):return s+-as_g(o)
    def __rsub__(s,o):return as_g(o)+-s
    def __mul__(s,o):
        o=as_g(o);return G(s.r*o.r-s.i*o.i,s.r*o.i+s.i*o.r)
    __rmul__=__mul__
    def __truediv__(s,o):
        o=as_g(o);v=o.norm();require(v!=0,'division by zero')
        return s*G(o.r/v,-o.i/v)
    def __pow__(s,n):
        require(type(n) is int and n>=0,'nonnegative integral power')
        v=G(Q(1))
        for _ in range(n):v=v*s
        return v
    def norm(s):return s.r*s.r+s.i*s.i
def as_g(v):return v if isinstance(v,G) else G(Q(v))
ZERO=G();ONE=G(Q(1))
def translated_coefficients(centered,alpha):
    out=[ZERO for _ in centered]
    for j,v in enumerate(centered):
        for l in range(j+1):out[l]=out[l]+v*comb(j,l)*((-alpha)**(j-l))
    return out
def multiply(x,y):
    out=[ZERO for _ in range(len(x)+len(y)-1)]
    for i,a in enumerate(x):
        for j,b in enumerate(y):out[i+j]=out[i+j]+a*b
    return out
def derivative_value(coefficients,n,alpha):
    return sum((v*(fact(j)//fact(j-n))*(alpha**(j-n)) for j,v in enumerate(coefficients) if j>=n),ZERO)
def jet_product(q,b,n):
    return sum((qj*(fact(n)//fact(n-j))*b[n-j] for j,qj in enumerate(q) if j<=n and n-j<len(b)),ZERO)
def fixed_case(m,degree,alpha,eta,variant='correct'):
    q=[ZERO]*m+[G(Q(1,3),Q(-2,5))]+[G(Q((-1)**j,j+1),Q(1,j+2)) for j in range(m+1,degree+1)]
    a=[];b=[];corrections=[];prior=[];counts={'coefficients':0,'previous_values':0,'global_identities':0,'low_derivatives':0,'nonzero_corrections':0}
    targets=[ZERO,G(eta/3),G(eta),G(-eta),G(Q(0),eta),G(2*eta),G(7*eta,-3*eta)]
    for k in range(11):
        n=k+m;A=q[m]*(fact(n)//fact(k))
        cross=sum((q[j]*(fact(n)//fact(n-j))*b[n-j] for j in range(m+1,min(degree,n)+1)),ZERO)
        # Independent input jets force zero, near-boundary and exact-boundary S.
        a.append((targets[k%len(targets)]-cross)/A)
        used_A=q[m] if variant=='wrong_factorial' else A
        used_cross=ZERO if variant=='drop_cross' else cross
        S=used_A*a[k]+used_cross
        c=ZERO if S.norm()>=eta*eta or variant=='omit_correction' else (G(eta)-S)/used_A
        b.append(a[k]+c);corrections.append(c)
        actual=jet_product(q,b,n)
        require(actual.norm()>=eta*eta,'fixed-p evaluation exclusion')
        require(c.norm()*A.norm()<=4*eta*eta,'uniform correction bound')
        for j,old in enumerate(prior):
            require(jet_product(q,b,j+m)==old,'later correction changed an earlier derivative');counts['previous_values']+=1
        prior.append(actual);counts['coefficients']+=1;counts['nonzero_corrections']+=c!=ZERO
    # A second route: expand at z=0, multiply ordinary coefficients, evaluate at alpha.
    p_global=translated_coefficients(q,alpha)
    f_global=translated_coefficients([v/fact(k) for k,v in enumerate(b)],alpha)
    product=multiply(p_global,f_global)
    for n in range(len(b)+m):
        actual=derivative_value(product,n,alpha);expected=jet_product(q,b,n)
        require(actual==expected,'ordinary-coordinate product/derivative identity');counts['global_identities']+=1
        if n<m:require(actual==ZERO,'root multiplicity low derivative');counts['low_derivatives']+=1
    return counts
def main():
    zcases=0;monomials=0;tails=0
    for k in range(15):
        t=Q(1,k+1)
        for x in range(-4,5):
            for y in range(-4,5):
                a=G(Q(x,3)*t,Q(y,3)*t);b=a if a.norm()>=t*t else G(t);c=b-a
                require(b.norm()>=t*t,'z coefficient threshold');require(c.norm()<=4*t*t,'complex z correction bound');zcases+=1
    totals={k:0 for k in ['coefficients','previous_values','global_identities','low_derivatives','nonzero_corrections']}
    polynomial_cases=0
    for alpha in [ZERO,G(Q(2,3),Q(1,2))]:
        for m in [1,2,4]:
            for degree in [m,m+1,m+2]:
                for eta in [Q(1),Q(1,100)]:
                    result=fixed_case(m,degree,alpha,eta)
                    for k,v in result.items():totals[k]+=v
                    polynomial_cases+=1
    for m in range(1,10):
        for n in range(m,m+25):
            require(Q(fact(n),fact(n-m)*(n-m+1))>=1,'simultaneous monomial lower bound');monomials+=1
        for n in range(30):
            require(Q(fact(n+1),fact(n+1+m))<=Q(fact(n),fact(n+m)),'factorial-tail monotonicity');tails+=1
    rejected=[]
    for variant in ['omit_correction','wrong_factorial','drop_cross']:
        try:fixed_case(2,4,G(Q(2,3),Q(1,2)),Q(1,100),variant)
        except ValueError as e:rejected.append({'variant':variant,'reason':str(e)})
        else:raise ValueError('Algebra mutation accepted: '+variant)
    report={'mechanism':'Candidate-aware root Gaussian-rational coefficient algebra; second oracle expands ordinary global coordinates, multiplies polynomials and evaluates derivatives at alpha. No submitted/source program imported.','z_threshold_cases':zcases,'fixed_polynomial_cases':polynomial_cases,**totals,'monomial_indices':monomials,'factorial_tail_checks':tails,'real_algorithm_mutations_rejected':rejected,'limits':'Finite synthetic jets and exact identities only. Hypercyclicity, every derivative order, entire convergence, uniform null-orbit bounds and density are proved analytically, not by these diagnostics. No historical priority/current openness claim.'}
    (ROOT/'ROOT_EXACT_DIAGNOSTICS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()

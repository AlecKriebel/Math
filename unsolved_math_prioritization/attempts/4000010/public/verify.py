#!/usr/bin/env python3
"""Small exact controls and explicitly numerical regressions for AMR-039-0010.

No network, external packages, source corpus, or exhaustive search is used.
The mathematical arguments, including all infinite-state claims, are in PROOF.md.
"""
from fractions import Fraction as F
from decimal import Decimal, localcontext
from itertools import product
import json
from pathlib import Path


def show(x):
    return str(x)


def D(x):
    if isinstance(x, F):
        return Decimal(x.numerator) / Decimal(x.denominator)
    return Decimal(x)


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), F(0))


def matvec(M, f):
    return [dot(row, f) for row in M]


def rowvec(f, M):
    return [sum((f[i] * M[i][j] for i in range(len(f))), F(0))
            for j in range(len(f))]


def variance(p, f):
    return dot(p, [x*x for x in f]) - dot(p, f)**2


def lip(f):
    return max((abs(f[i+1]-f[i]) for i in range(len(f)-1)), default=F(0))


def line_w1(p, q):
    balance = F(0)
    ans = F(0)
    for x, y in zip(p[:-1], q[:-1]):
        balance += x-y
        ans += abs(balance)
    return ans


def curvature(M):
    return min(1-line_w1(M[i], M[j])/F(j-i)
               for i in range(len(M)) for j in range(i+1, len(M)))


def alpha(A, L, r):
    return r*r/(4*A) if r <= 2*A*L else L*r-A*L*L


def lazy(M, h):
    return [[h*x+(1-h if i == j else 0) for j,x in enumerate(row)]
            for i,row in enumerate(M)]


def dec_entropy(p, q):
    return sum((D(x)*(D(x)/D(y)).ln() for x,y in zip(p,q) if x), Decimal(0))


def check():
    out = {'problem_id': '4000010', 'full_resolution_claimed': False,
           'method': 'Exact Fraction controls; Decimal regressions marked separately.'}

    # Geometric-sum constants are compared as exact fractions.
    ks = [F(1), F(1,2), F(1,4), F(1,16)]
    for k in ks:
        q=1-k; a=1-k/2
        assert 1-q*q == k*(2-k)
        assert 1-a*a == k*(1-k/4)
        assert 1/(1-k/4) <= F(4,3)
        for n in (1,2,5,12):
            assert sum((q**(2*j) for j in range(n)),F(0)) == (1-q**(2*n))/(1-q*q)
            assert sum((a**(2*j) for j in range(n)),F(0)) == (1-a**(2*n))/(1-a*a)
    out['geometric_constants'] = {'passed': True, 'kappa_values': list(map(show,ks))}

    # Exact optimizer and join checks for the truncated quadratic conjugate.
    samples=0
    for A,L in ((F(1,3),F(2,3)),(F(14,15),F(1,3)),(F(2),F(3,5))):
        join=2*A*L
        assert join*join/(4*A) == L*join-A*L*L
        assert join/(2*A) == L
        for r in (F(0),join/2,join,join+F(1,4),4*join):
            opt=min(L,r/(2*A))
            val=opt*r-A*opt*opt
            assert val == alpha(A,L,r)
            for j in range(21):
                u=L*F(j,20)
                assert u*r-A*u*u <= val
                samples += 1
    out['conjugate_controls'] = {'passed': True, 'rational_comparisons': samples,
       'limitation': 'Finite regression of formula (6); analytic maximization is proved in the text.'}

    # Uniform two-state reset chain: all entries and obstruction bounds exact.
    pi2=[F(1,2),F(1,2)]; P2=[pi2[:],pi2[:]]
    eps=F(1,16); mu2=[F(1,2)+eps,F(1,2)-eps]
    assert rowvec(pi2,P2)==pi2 and curvature(P2)==1
    S=F(1,2); v=F(1,4); A=F(1,3); L=F(2,3)
    assert variance(pi2,[F(0),F(1)])==v
    cost=alpha(A,L,F(1)); transport=cost*eps
    chi2=sum(((x-y)**2/y for x,y in zip(mu2,pi2)),F(0))
    assert line_w1(mu2,pi2)==eps
    assert cost==F(14,27) and transport==F(7,216)
    assert chi2==4*eps*eps==F(1,64)
    assert transport-chi2==F(29,1728)>0
    assert alpha(A,L,eps)==F(3,1024)
    out['exact_two_point_obstruction']={
       'passed':True,'kappa':'1','A':show(A),'L':show(L),'epsilon':show(eps),
       'cost_at_unit_distance':show(cost),'transport_cost':show(transport),
       'entropy_upper_bound_chi_squared':show(chi2),
       'strict_gap_lower_bound':show(transport-chi2),
       'scalar_profile_of_W1':show(alpha(A,L,eps))}

    # Exact three-state kernel, curvature, reversible stationary law, local variance.
    P=[[F(3,4),F(1,4),F(0)], [F(1,8),F(3,4),F(1,8)],
       [F(0),F(1,4),F(3,4)]]
    pi=[F(1,4),F(1,2),F(1,4)]
    assert all(sum(row)==1 for row in P)
    assert rowvec(pi,P)==pi
    assert all(pi[i]*P[i][j]==pi[j]*P[j][i] for i in range(3) for j in range(3))
    assert curvature(P)==F(1,4)
    identity=[F(0),F(1),F(2)]
    vv=[variance(row,identity) for row in P]
    assert vv==[F(3,16),F(1,4),F(3,16)]
    extreme_fs=[[F(0),F(s),F(s+t)] for s,t in product((-1,1),repeat=2)]
    assert all(variance(row,f)<=bound for row,bound in zip(P,vv) for f in extreme_fs)
    k=F(1,4); a=1-k/2
    C=lip([x/k for x in vv]); A=dot(pi,vv)/(1-a*a); L=F(1,3)
    assert C==F(1,4) and A==F(14,15)
    recurrences=0
    for f in extreme_fs:
        fj=f[:]
        for j in range(12):
            assert lip(fj)<=a**j
            fj=[x+L*a**(2*j)*v for x,v in zip(matvec(P,fj),vv)]
            recurrences+=1
    out['exact_three_state_controls']={
       'passed':True,'kappa':show(k),'local_variance':list(map(show,vv)),
       'C':show(C),'A':show(A),'L':show(L),'lipschitz_recurrence_steps':recurrences}

    # Lazification identities retain all relevant normalizations exactly.
    hs=[F(1),F(1,2),F(1,4),F(1,16),F(1,256)]
    lazy_results=[]
    for h in hs:
        Ph=lazy(P,h); kh=h/4
        vh=[variance(row,identity) for row in Ph]
        assert rowvec(pi,Ph)==pi and curvature(Ph)==kh
        assert vh==[h/4-h*h/16,h/4,h/4-h*h/16]
        assert lip([x/kh for x in vh])==h/4
        Ah=dot(pi,vh)/(kh*(1-kh/4))
        assert Ah==(1-h/8)/(1-h/16)
        assert F(14,15)<=Ah<1
        lazy_results.append({'h':show(h),'kappa_h':show(kh),'A_h':show(Ah),
                             'L_h':'1/3','diameter_based_T1_constant':show(2/(kh*(2-kh)))})
    out['exact_lazification_controls']={'passed':True,'values':lazy_results,
       'analytic_limit': 'A_h=(1-h/8)/(1-h/16) tends to 1 as h decreases to 0.'}

    # Numerical regressions are deliberately separated from exact certificates.
    with localcontext() as ctx:
        ctx.prec=70
        actual_H=dec_entropy(mu2,pi2)
        assert actual_H < D(chi2) < D(transport)
        c=D(cost); z=c/2; ez=z.exp(); emz=(-z).exp()
        tanh=(ez-emz)/(ez+emz); eps_star=tanh/2
        p=[Decimal('0.5')+eps_star,Decimal('0.5')-eps_star]
        hstar=dec_entropy(p,[Decimal('0.5'),Decimal('0.5')])
        b=((ez+emz)/2).ln()
        assert abs(c*eps_star-hstar-b)<Decimal('1e-65')
        residuals=[]
        for f in extreme_fs:
            mean=dot(pi,f)
            for j in range(1,31):
                lam=F(j,90)
                mgf=sum((D(p)*(D(lam*(x-mean))).exp() for p,x in zip(pi,f)),Decimal(0))
                residual=D(A*lam*lam)-mgf.ln()
                assert residual>=-Decimal('1e-65')
                residuals.append(residual)
        out['decimal_regressions']={
            'passed':True,'precision_digits':70,
            'two_point_actual_entropy':str(actual_H),
            'two_point_exact_formula_minimum_defect_decimal':str(b),
            'two_point_maximizer_epsilon_decimal':str(eps_star),
            'three_state_mgf_samples':len(residuals),
            'minimum_mgf_bound_slack':str(min(residuals)),
            'limitation':'Numerical regression only. The infinite-state and universal assertions rely on the proofs.'}
    out['overall_passed']=True
    return out


if __name__=='__main__':
    result=check()
    path=Path(__file__).with_name('verification_results.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'overall_passed':result['overall_passed'],
                      'result_file':path.name,
                      'exact_obstruction_gap':result['exact_two_point_obstruction']['strict_gap_lower_bound']},indent=2))

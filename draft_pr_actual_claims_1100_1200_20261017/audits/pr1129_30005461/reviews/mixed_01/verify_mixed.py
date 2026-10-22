#!/usr/bin/env python3
"""Independent exact falsification checks for the credited mixed odd SOS claim.

Standard-library only. All guards raise explicitly, so optimization cannot remove them.
Finite checks support the separate universal derivation; they are not its proof.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from math import comb, factorial
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
COUNTS = Counter()
NEGATIVES = []


def require(condition, family, message):
    if not condition:
        raise RuntimeError(f'{family}: {message}')
    COUNTS[family] += 1


def trim(p):
    return {k: F(v) for k, v in p.items() if v}


def add(*ps):
    out = {}
    for p in ps:
        for e, c in p.items():
            out[e] = out.get(e, 0) + c
    return trim(out)


def scale(p, c):
    return trim({e: c * v for e, v in p.items()})


def mul(p, q):
    out = {}
    for e, a in p.items():
        for f, b in q.items():
            g = tuple(x + y for x, y in zip(e, f))
            out[g] = out.get(g, 0) + a * b
    return trim(out)


def power(p, k, nvars):
    if k < 0:
        raise ValueError('negative power')
    out = {(0,) * nvars: F(1)}
    while k:
        if k % 2:
            out = mul(out, p)
        p = mul(p, p)
        k //= 2
    return out


def evaluate(p, xs):
    out = F(0)
    for e, c in p.items():
        term = c
        for x, k in zip(xs, e):
            term *= x ** k
        out += term
    return out


def binform(n, m):
    return {(k, m-k): F(comb(n, k)) for k in range(m+1)}


def split(a, b, mutate=None):
    n = a+b-1
    out = {}
    stop = a-1 if mutate == 'omit_left_endpoint' else a
    for k in range(stop):
        out[(k,n-k)] = out.get((k,n-k),0)+comb(n,k)
    for k in range(b):
        exponent = (a+k,b-1-k) if mutate == 'wrong_swap' else (n-k,k)
        out[exponent] = out.get(exponent,0)+comb(n,k)
    return trim(out)


def beta_integer(a, b):
    if a < 1 or b < 1:
        raise ValueError('beta arguments must be positive integers')
    return F(factorial(a-1)*factorial(b-1),factorial(a+b-1))


def gram(n, r):
    m=2*r
    if n <= m:
        raise ValueError('moment construction requires n > 2r')
    c=(n-m)*comb(n,m)
    return [[c*comb(r,i)*comb(r,j)*beta_integer(i+j+1,n-m)
             for j in range(r+1)] for i in range(r+1)]


def ldl(q):
    n=len(q)
    ell=[[F(int(i==j)) for j in range(n)] for i in range(n)]
    diagonal=[]
    for j in range(n):
        d=q[j][j]-sum(ell[j][k]**2*diagonal[k] for k in range(j))
        require(d>0,'positive_gram_pivots',str((n,j,d)))
        diagonal.append(d)
        for i in range(j+1,n):
            ell[i][j]=(q[i][j]-sum(ell[i][k]*ell[j][k]*diagonal[k]
                                 for k in range(j)))/d
    for i in range(n):
        for j in range(n):
            reconstructed=sum(ell[i][k]*diagonal[k]*ell[j][k] for k in range(n))
            require(reconstructed==q[i][j],'gram_reconstruction',str((i,j)))
    return ell, diagonal


def sos_binform(n, r):
    ell,diagonal=ldl(gram(n,r))
    terms=[]
    for j,d in enumerate(diagonal):
        # Q=L D L^T; column j of L supplies one linear form in the monomial vector.
        terms.append((d,trim({(r-i,i):ell[i][j] for i in range(r+1)})))
    reconstructed={}
    for d,h in terms:
        reconstructed=add(reconstructed,scale(mul(h,h),d))
    require(reconstructed==binform(n,2*r),'binform_sos_reconstruction',str((n,r)))
    return terms


def substitute_binary(h,p,q,nvars):
    out={}
    for (a,b),c in h.items():
        out=add(out,scale(mul(power(p,a,nvars),power(q,b,nvars)),c))
    return out


def from_sos(terms):
    return add(*(scale(mul(h,h),d) for d,h in terms))


def sos_power(terms,k,nvars):
    out=[(F(1),{(0,)*nvars:F(1)})]
    for _ in range(k):
        out=[(d*e,mul(h,g)) for d,h in out for e,g in terms]
    return out


def homogenize(p,d):
    out={}
    for e,c in p.items():
        residual=d-sum(e)
        if residual < 0:
            raise ValueError('requested homogenization below polynomial degree')
        out[e+(residual,)]=c
    return trim(out)


def check_mixed_certificate(psos,qsos,a,b,label):
    p=from_sos(psos);q=from_sos(qsos);nvars=3;n=a+b-1
    left=power(add(p,q),n,nvars)
    pa=sos_power(psos,a,nvars);qb=sos_power(qsos,b,nvars)
    left_block=sos_binform(n,(a-1)//2)
    right_block=sos_binform(n,(b-1)//2)
    final=[]
    for c,h in qb:
        for d,g in left_block:
            final.append((c*d,mul(h,substitute_binary(g,p,q,nvars))))
    for c,h in pa:
        for d,g in right_block:
            final.append((c*d,mul(h,substitute_binary(g,q,p,nvars))))
    require(from_sos(final)==left,'multivariate_explicit_sos',label)
    for c,_ in final:
        require(c>0,'certificate_coefficient_positivity',label)
    for d in (4,6):
        pp=homogenize(p,d);qq=homogenize(q,d)
        ph=[(c,homogenize(h,a*d//2)) for c,h in pa]
        qh=[(c,homogenize(h,b*d//2)) for c,h in qb]
        require(from_sos(ph)==power(pp,a,4),'homogenized_input_sos',label)
        require(from_sos(qh)==power(qq,b,4),'homogenized_input_sos',label)
        require(homogenize(left,n*d)==power(add(pp,qq),n,4),
                'unequal_degree_homogenization',label)
        final_h=[(c,homogenize(h,n*d//2)) for c,h in final]
        require(from_sos(final_h)==power(add(pp,qq),n,4),
                'homogenized_output_sos',label)
        for _,h in final_h:
            require(all(sum(e)==n*d//2 for e in h),'output_root_degree',label)
    return len(final)


def expect_rejection(label, condition, witness):
    before=COUNTS.copy()
    try:
        require(condition,'injected_false_claim',label)
    except RuntimeError:
        NEGATIVES.append({'label':label,'witness':witness,'rejected':True})
    else:
        raise RuntimeError('negative control was not rejected: '+label)
    if COUNTS != before:
        raise RuntimeError('failed guard incorrectly changed counts')


def main():
    expected={
      'CREDITED_MIXED_EXPONENT_PROOF.md':(7385,'be068e1471372383675640c282109ae82c2c74d3856a4e6bedf046dead97473c'),
      'PROOF.md':(10963,'46af7394ebfee7b0de9861693f84ab684502da3be208c626411f24e2538c7d15'),
      'MATHEMATICAL_AUDIT.md':(13253,'f9faede12ad50034f5620f4576c621dc275a6ddbbf29bb3e13096d778a094cce')}
    for name,(size,digest) in expected.items():
        raw=(HERE.parent.parent/'inputs'/name).read_bytes()
        require(len(raw)==size and sha256(raw).hexdigest()==digest,'frozen_input_identity',name)
    for n in range(2,81):
        for m in range(1,n):
            for k in range(m):
                require((k+1)*comb(n,k+1)==n*comb(n-1,k),
                        'derivative_coefficients',str((n,m,k)))
            for k in range(m+1):
                second=comb(n-1,k-1) if k else 0
                require(comb(n,k)==comb(n-1,k)+second,
                        'pascal_coefficients',str((n,m,k)))
    for m in range(0,51,2):
        n=m+1
        require([comb(n,k) for k in range(m+1)]+[0]
                ==[comb(n,k) if k<n else 0 for k in range(n+1)],
                'base_case_exact_coefficients',str(m))
    for a in range(1,72,2):
        for b in range(1,72,2):
            n=a+b-1
            require(split(a,b)==binform(n,n),'full_mixed_binomial_split',str((a,b)))
            require(n%2==1 and a-1<n and b-1<n and (a-1)%2==0 and (b-1)%2==0,
                    'index_parity_and_ranges',str((a,b)))
    for m in range(0,21,2):
        for delta in range(1,25):
            n=m+delta;c=delta*comb(n,m)
            for k in range(m+1):
                integral_coeff=c*comb(m,k)*beta_integer(m-k+1,delta)
                require(integral_coeff==comb(n,k),'independent_integral_coefficients',str((n,m,k)))
    certificates=[]
    for r in range(0,8):
        for delta in [1,2,5,13]:
            n=2*r+delta;terms=sos_binform(n,r)
            if (n,r) in [(5,1),(9,2)]:
                certificates.append({'n':n,'m':2*r,'weighted_squares':[
                    {'positive_weight':str(d),'root_terms':[
                        {'u_degree':e[0],'v_degree':e[1],'coefficient':str(c)}
                        for e,c in sorted(h.items())]} for d,h in terms]})
    values=[F(-7),F(-3,2),F(-1),F(-1,2),F(0),F(2,7),F(1),F(3)]
    for m in range(0,23,2):
        for delta in [1,2,3,8,17]:
            n=m+delta;b=binform(n,m)
            for t in values:
                require(evaluate(b,(t,F(1)))>0,'signed_rational_positivity',str((n,m,t)))
            require(evaluate(b,(F(1),F(0)))==comb(n,m),'projective_v_zero',str((n,m)))
    x={(1,0,0):F(1)};y={(0,1,0):F(1)};z={(0,0,1):F(1)};one={(0,0,0):F(1)}
    ps=[(F(1),add(x,scale(y,-1))),(F(2),z)]
    qs=[(F(1),add(mul(x,y),one)),(F(3),add(mul(z,z),scale(x,-1)))]
    p=from_sos(ps);q=from_sos(qs)
    require(max(map(sum,p))==2 and max(map(sum,q))==4,'different_degree_fixture','degrees 2 and 4')
    cases=[(ps,qs,1,1,'i=j=0 unequal degrees'),(ps,qs,1,3,'i=0'),
           (ps,qs,3,1,'j=0'),(ps,qs,3,3,'both cubic hypotheses'),
           (ps,qs,5,3,'distinct exponents unequal degrees'),([],qs,3,3,'p=0'),
           (ps,[],3,1,'q=0'),([],[],1,1,'both zero'),
           ([(F(2),one)],qs,1,3,'positive constant p'),
           ([(F(2),one)],[(F(3),one)],3,5,'both positive constants')]
    certificate_count=0
    for case in cases:
        certificate_count+=check_mixed_certificate(*case)
    # Homogeneous/affine threshold interface; no test of the separate principal proof.
    for c in [F(-4),F(0),F(7,3),F(3),F(4)]:
        affine={(4,2):F(1),(2,4):F(1),(0,0):F(1),(2,2):-c}
        hom={(4,2,0):F(1),(2,4,0):F(1),(0,0,6):F(1),(2,2,2):-c}
        require(homogenize(affine,6)==trim(hom),'threshold_family_interface',str(c))
    expect_rejection('literal archived positivity index',evaluate(binform(3,1),(F(-1),F(1)))>0,'f_3,1(-1)=-2')
    bad_binary={(0,2):F(1),(1,1):F(3)}
    expect_rejection('literal shortened homogenization',evaluate(bad_binary,(F(-1),F(1)))>=0,'v^2+3uv=-2 at (-1,1)')
    expect_rejection('strict positivity at N=m',evaluate(binform(2,2),(F(-1),F(1)))>0,'f_2,2(-1)=0')
    expect_rejection('positivity for odd truncation',evaluate(binform(5,3),(F(-2),F(1)))>0,'f_5,3(-2)=-49')
    expect_rejection('split omits endpoint',split(3,5,'omit_left_endpoint')==binform(7,7),'coefficient of u^2 v^5 is omitted')
    expect_rejection('second binary factor arguments unswapped',split(1,3,'wrong_swap')==binform(3,3),'u^3 coefficient changes from 1 to 3')
    expect_rejection('zero-index factor erased',{}==binform(1,0),'B_1,0=1, including i=j=0')
    expect_rejection('odd padding degree preserves positivity',F(-1)**3>=0,'p=1 padded at D=3 gives P=z^3, P(-1)=-1')
    expect_rejection('even power certifies nonnegative input',F(-1)>=0,'p=-1 has p^2=1 SOS but p<0')
    expect_rejection('fractional homogeneous square-root degree accepted',(3*3)%2==0,'odd a and odd D give aD/2 noninteger')
    expect_rejection('above-endpoint odd power is nonnegative',(3-F(4))**5>=0,'f_4(1,1)^5=-1')
    if '--negative-guard' in sys.argv:
        require(False,'deliberate_unhandled_guard','must exit nonzero even with optimization')
    payload={'status':'PASS','program':'verify_mixed.py','guards':'explicit RuntimeError; no optimization-sensitive guards',
             'check_counts':dict(sorted(COUNTS.items())),'total_checks':sum(COUNTS.values()),
             'negative_controls':NEGATIVES,'negative_control_count':len(NEGATIVES),
             'coefficient_exact_mixed_pairs':36*36,'multivariate_cases':len(cases),
             'explicit_final_weighted_squares_across_cases':certificate_count,
             'scope':'Finite exact falsification and transcription checks only. Universal proof is in REPORT.md.'}
    if '--certificates' in sys.argv:
        (HERE/'EXACT_BINFORM_CERTIFICATES.json').write_text(json.dumps(certificates,indent=2)+'\n')
    print(json.dumps(payload,sort_keys=True,indent=2))

if __name__=='__main__':
    main()

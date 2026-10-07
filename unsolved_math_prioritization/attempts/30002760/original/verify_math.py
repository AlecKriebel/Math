#!/usr/bin/env python3
"""Exact finite controls; analytic proofs and conditional hypotheses remain separate."""
import argparse
from collections import Counter
from fractions import Fraction as F
import itertools
import json
from pathlib import Path
import sys

COUNTS = Counter()

def require(condition, label, group):
    if not condition:
        raise ValueError('FAILED: ' + label)
    COUNTS[group] += 1

def unique_object(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError('Duplicate JSON key: ' + key)
        out[key] = value
    return out

def frac(value):
    if not isinstance(value, str):
        raise ValueError('A claimed rational must be a string')
    return F(value)

def derivative(p):
    return [i * p[i] for i in range(1, len(p))] or [F(0)]

def multiply(p, q):
    r = [F(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            r[i+j] += a*b
    return r

def integral(p, t=F(1)):
    return sum((a*t**(i+1)/F(i+1) for i, a in enumerate(p)), F(0))

def value(p, t):
    return sum((a*t**i for i, a in enumerate(p)), F(0))

def dot(p, q):
    return sum((a*b for a, b in zip(p, q)), F(0))

def equal(actual, claimed, label, group):
    require(actual == frac(claimed), label, group)

def main(path):
    c = json.loads(Path(path).read_text(), object_pairs_hook=unique_object)
    schema = {
        'turn_1': ['phi_derivative_norm_squared','psi_derivative_norm_squared','derivative_cross','convection_cross','galerkin_coefficient_times_epsilon','amplification_coefficient'],
        'turn_2': ['isometry_factor','blind_beta_squared','blind_residual_squared','blind_error_squared','tail_factor_squared_at_delta_3_over_4'],
        'turn_3': ['catalan_10','overlay_splits_at_k_7','rate_dilation_base'],
        'turn_4': ['theta_limit_at_a_1','test_theta','test_kappa','marking_contradiction_upper','slow_complexity_at_l_10','slow_scaled_error_at_l_10'],
        'turn_5': ['backward_euler_endpoint','backward_euler_endpoint_error_squared','allocation_p_2_q_1_2_3_N_12']}
    require(set(c) == {'problem_id','status','author_approaches'} | set(schema), 'root schema', 'schema')
    require(type(c['problem_id']) is int and c['problem_id']==30002760, 'problem identity', 'schema')
    require(c['status']=='unsolved', 'no unsupported solved promotion', 'schema')
    require(type(c['author_approaches']) is int and c['author_approaches']==5, 'approach count', 'schema')
    for k, names in schema.items():
        require(isinstance(c[k],dict) and set(c[k])==set(names), k+' schema', 'schema')

    a=c['turn_1']; g='turn_1'
    phi=[F(0),F(1),F(-1)]
    psi=[F(0),F(-1,2),F(3,2),F(-1)]
    dp,dq=derivative(phi),derivative(psi)
    P=integral(multiply(dp,dp)); Q=integral(multiply(dq,dq))
    X=integral(multiply(dq,dp)); Y=integral(multiply(dq,phi))
    for actual, key in [(P,'phi_derivative_norm_squared'),(Q,'psi_derivative_norm_squared'),(X,'derivative_cross'),(Y,'convection_cross'),(Y/P,'galerkin_coefficient_times_epsilon'),((Y/P)**2*P/Q,'amplification_coefficient')]:
        equal(actual,a[key],key,g)
    for p in [phi,psi]:
        require(value(p,F(0))==0 and value(p,F(1))==0,'homogeneous boundary',g)
    require(integral(multiply(dp,phi))==0,'self convection vanishes',g)
    for m in range(1,101):
        eps=F(1,m); coefficient=Y/(eps*P)
        require(coefficient*eps*P==Y,'Galerkin equation',g)
        error_sq=eps*(Q+coefficient**2*P-2*coefficient*X)
        equal(error_sq/(eps*Q)-1, str(frac(a['amplification_coefficient'])/eps**2),'amplification identity',g)
        require(error_sq>eps*Q,'coarse Galerkin exceeds best',g)

    a=c['turn_2'];g='turn_2'
    for m in range(1,25):
        eps=F(1,m); D=1+eps**2
        for x in range(-3,4):
            for y in range(-3,4):
                residual=[eps*x-y,x+eps*y]
                require(dot(residual,residual)/D==frac(a['isometry_factor'])*(x*x+y*y),'optimal-test matrix isometry',g)
    exact=[F(0),F(1)]; approximation=[F(0),F(0)]; error=[x-y for x,y in zip(exact,approximation)]
    equal(F(1),a['blind_beta_squared'],'stable trial beta',g)
    equal(error[0]**2,a['blind_residual_squared'],'restricted residual',g)
    equal(dot(error,error),a['blind_error_squared'],'unobserved error',g)
    equal(1+F(3,4)**2,a['tail_factor_squared_at_delta_3_over_4'],'tail Pythagorean factor',g)
    for x in range(-10,11):
        for y in range(-10,11):
            require(F(x*x+y*y)==F(x*x)+F(y*y),'test-tail decomposition',g)

    a=c['turn_3'];g='turn_3'
    catalan=[1]
    for n in range(1,31):
        catalan.append(sum(catalan[j]*catalan[n-1-j] for j in range(n)))
        require(catalan[n]>=2**(n-1),'exhaustive-search lower bound',g)
    require(type(a['catalan_10']) is int and catalan[10]==a['catalan_10'],'Catalan ten',g)
    require(type(a['overlay_splits_at_k_7']) is int and sum(2**j for j in range(8))==a['overlay_splits_at_k_7'],'overlay seven',g)
    require(type(a['rate_dilation_base']) is int and a['rate_dilation_base']==2,'rate dilation',g)
    for k in range(50):
        splits=sum(2**j for j in range(k+1))
        require(splits==2**(k+1)-1,'geometric overlay sum',g)
        require(splits+1<=a['rate_dilation_base']*(2**k+1),'complexity-to-budget comparison',g)
    trees={0:[None]}
    def leaves(t,lo=F(0),hi=F(1)):
        if t is None:
            return ((lo,hi),)
        mid=(lo+hi)/2
        return leaves(t[0],lo,mid)+leaves(t[1],mid,hi)
    for n in range(1,8):
        trees[n]=[(l,r) for j in range(n) for l in trees[j] for r in trees[n-1-j]]
        partitions={leaves(t) for t in trees[n]}
        require(len(partitions)==catalan[n],'distinct dyadic partition count',g)
        for part in partitions:
            require(len(part)==n+1 and part[0][0]==0 and part[-1][1]==1,'leaf count and endpoints',g)
            require(all(x[0]<x[1] for x in part),'positive interval lengths',g)
            require(all(part[j][1]==part[j+1][0] for j in range(len(part)-1)),'gapless partition',g)

    a=c['turn_4'];g='turn_4'
    equal(1/(1+F(1)**2),a['theta_limit_at_a_1'],'marking threshold',g)
    r=F(1,4); kappa=frac(a['test_kappa'])
    equal(r*r,a['test_theta'],'test theta',g)
    upper=(kappa+r)**2+r*r
    equal(upper,a['marking_contradiction_upper'],'marking contradiction value',g)
    require(upper<1,'strict marking contradiction',g)
    for av in [F(i,4) for i in range(17)]:
        for rv in [F(i,20) for i in range(1,20)]:
            for kv in [F(i,20) for i in range(1,20)]:
                if (kv+av*rv)**2+rv*rv<1:
                    require(rv*rv<1/(1+av*av),'admissible theta range',g)
                    for rsmall in [F(0),rv/2,rv]:
                        require((kv+av*rsmall)**2+rsmall*rsmall<1,'lower r cannot meet reliability inequality',g)
    for qroot in [F(1,2),F(1,3),F(2,3),F(3,4)]:
        for ell in range(1,51):
            geom=sum((qroot**(ell-j) for j in range(ell)),F(0))
            require(geom<1/(1-qroot),'summed contraction bound',g)
    for ell in range(1,101):
        size=1+ell*(ell+1)//2
        require(F(size,ell+1)>F(ell,2),'slow-rate scaled error unbounded witness',g)
    require(type(a['slow_complexity_at_l_10']) is int and 1+10*11//2==a['slow_complexity_at_l_10'],'slow mesh complexity',g)
    equal(F(a['slow_complexity_at_l_10'],11),a['slow_scaled_error_at_l_10'],'slow scaled error',g)

    a=c['turn_5'];g='turn_5'
    endpoint=F(3,2)
    equal(endpoint,a['backward_euler_endpoint'],'Euler equation endpoint',g)
    equal((endpoint-1)**2,a['backward_euler_endpoint_error_squared'],'Euler endpoint error',g)
    require(2*endpoint==3,'backward Euler equation',g)
    e=[F(0),-endpoint,F(1)]
    r=[-endpoint,2-endpoint,F(1)]
    for j in range(101):
        t=F(j,100)
        lhs=value(e,t)**2+integral(multiply(e,e),t)
        rhs=integral(multiply(r,r),t)
        require(lhs<=rhs,'integrated parabolic energy inequality',g)
    for p in [1,2,3]:
        for q in itertools.product(range(1,4),repeat=3):
            weights=[x**(p+1) for x in q]; B=sum(q)
            for N in range(3,14):
                lower=F(B**(p+1),N**p)
                for n1 in range(1,N-1):
                    for n2 in range(1,N-n1):
                        ns=[n1,n2,N-n1-n2]
                        total=sum((F(b,ni**p) for b,ni in zip(weights,ns)),F(0))
                        require(total>=lower,'allocation global lower bound',g)
            for L in range(6,21):
                real=[F((L-3)*qi,B) for qi in q]
                rounded=[-(-x.numerator//x.denominator) for x in real]
                require(sum(rounded)<=L and min(rounded)>=1,'rounded allocation budget',g)
                total=sum((F(b,ni**p) for b,ni in zip(weights,rounded)),F(0))
                require(total<=F(2**p*B**(p+1),L**p),'rounded allocation error bound',g)
    equal(sum((F(q**3,n**2) for q,n in zip([1,2,3],[2,4,6])),F(0)),a['allocation_p_2_q_1_2_3_N_12'],'exact allocation optimum',g)
    out={'status':'PASS_FINITE_CONTROLS','problem_id':30002760,'counts':dict(sorted(COUNTS.items())),'total_checks':sum(COUNTS.values()),'scope':'Exact finite algebra and combinatorics only; not formal verification, PDE hypothesis certification, novelty, or full resolution.'}
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--claims',default=str(Path(__file__).with_name('CLAIMS.json')))
    args=parser.parse_args()
    try:
        main(args.claims)
    except Exception as exc:
        print(str(exc),file=sys.stderr)
        sys.exit(1)

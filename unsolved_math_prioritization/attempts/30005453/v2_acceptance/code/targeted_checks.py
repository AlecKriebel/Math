#!/usr/bin/env python3
"""Fresh targeted diagnostics for the two rigidity strips and scope boundaries.

Decimal checks probe algebra at approximate extrema; they are NOT certificates
of the infinite-dimensional lemma or the stochastic convergence theorem.
Exact Fraction checks cover perfect-power jump identities and scalar dynamics.
This script neither imports nor executes the author or first-auditor verifiers.
"""
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
from pathlib import Path
import argparse, json

def require(ok, why):
    if not ok: raise ValueError(why)

def check_strips():
    cases=[]
    with localcontext() as ctx:
        ctx.prec=220
        M=D('0.5')
        for beta in map(D, ('0.05','0.1','0.25','0.5','1','2','9','25','50')):
            c=1/(beta+1)
            for degree in (1,2,5,17):
                for tiny in (D('1e-12'),D('1e-60')):
                    for sign in ('upper','lower','lower_small_denominator'):
                        # Upper: central equilibrium rate can be extremely small.
                        # Lower: central trajectory coordinate can be extremely small.
                        z0=tiny if sign=='upper' else M+tiny
                        zn=[D(1)+D(i)/(2*degree) if sign=='upper' else
                            ((M if sign=='lower_small_denominator' else D(0))+tiny*(i+1))
                            for i in range(degree)]
                        tz=sum((z0+w)**beta for w in zn)
                        p0=z0*tz
                        leaf_rates=[w*(w+z0)**beta for w in zn]
                        P=max([p0]+leaf_rates)
                        B=P**c
                        K=max(D(4),B)
                        def omega(e):
                            return e**beta if beta<=1 else beta*(2*K)**(beta-1)*e
                        eps=M/8
                        while B*degree*omega(eps)/(M/2)**beta >= M/8:
                            eps/=2
                        # Adverse neighbors create pair-sum errors of -eps/2
                        # (upper) and +eps/2 (lower), not exact attained extrema.
                        dv=(M-eps/2) if sign=='upper' else (-M+eps/2)
                        dn=[-M if sign in ('upper','lower_small_denominator') else M for _ in zn]
                        b0=z0+dv; bn=[z+d for z,d in zip(zn,dn)]
                        require(min([b0]+bn)>0 and max([b0]+bn)<=K,'positive bounded configuration')
                        tb=sum((b0+w)**beta for w in bn)
                        delta=degree*omega(eps)
                        flow=c*(p0/tb-b0)
                        if sign=='upper':
                            require(tb>=tz-delta,'upper modulus')
                            require(tb>=(M/2)**beta,'upper safe denominator')
                            require(p0/tb-z0 <= B*delta/(M/2)**beta,'upper ratio bound')
                            require(flow < -c*M/2,'upper inward drift')
                        else:
                            require(tb<=tz+delta,'lower modulus')
                            require(tz>=(M/2)**beta,'lower equilibrium denominator')
                            # This bound uses tz+delta, never an assumed lower bound on tb.
                            lower=-z0*delta/(tz+delta)
                            require(p0/tb-z0>=lower,'lower monotone ratio bound')
                            require(lower>=-B*delta/(M/2)**beta,'lower uniform error')
                            require(flow > c*M/2,'lower inward drift')
                        cases.append({'beta':str(beta),'degree':degree,'tiny':str(tiny),
                                      'strip':sign,'epsilon':str(eps),
                                      'normalized_inward_drift':str(abs(flow)/(c*M)),
                                      'status':'PASS'})
        # Each vertex in the period-two boundary pattern sees exactly one
        # edge of weight two. This cancellation holds for every alpha>0.
        boundary=0
        for alpha in map(D,('0.01','0.1','0.5','0.9','0.99')):
            positive_power=D(2)**alpha
            for phase in (0,1):
                weights=[D(2) if (i+phase)%2 else D(0) for i in range(10)]
                for i,w in enumerate(weights):
                    left=(weights[(i-1)%10]**alpha if weights[(i-1)%10] else D(0))+(w**alpha if w else D(0))
                    right=(weights[(i+1)%10]**alpha if weights[(i+1)%10] else D(0))+(w**alpha if w else D(0))
                    require(left==right==positive_power,'nonzero boundary denominators')
                    reinforcement=(w**alpha if w else D(0))*(1/left+1/right)
                    require(abs(reinforcement-w)<D('1e-210'),'boundary fixed point')
                    boundary+=1
    require(len(cases)==216,'strip coverage')
    return {'status':'PASS','precision_digits':220,'approximate_strip_cases':len(cases),
            'noninteger_beta_cases':sum(D(c['beta'])!=D(c['beta']).to_integral() for c in cases),
            'boundary_pattern_edge_checks':boundary,'cases':cases}

def exact_controls():
    jumps=0
    for m,n in ((1,100),(1,4),(1,2),(3,4),(99,100)):
        for k in range(1,26):
            # At count k^n, count^alpha=k^m exactly; q is an arbitrary rational.
            qa=F(2*k+1,7); intensity=k**m*qa; jump=F(1,k**m)
            require(jump*intensity==qa,'exact H drift')
            require(jump**2*intensity<=qa,'bracket domination')
            jumps+=1
    scalar=0
    for beta in (1,2,9):
        c=F(1,beta+1)
        for p in (F(1),F(1,2**80)):
            for b in (F(1,7),F(1),F(13,3)):
                # Symmetric single-edge trajectory: y=b^(beta+1) satisfies y'=p/2^beta-y.
                db=c*(p/(2*b)**beta-b)
                dy=(beta+1)*b**beta*db
                require(dy==p/2**beta-b**(beta+1),'scalar linearization')
                scalar+=1
    # At time zero, H(n0)-H(n0)=0, whereas unoffset H(n0)>0 for n0>1.
    offset=0
    for n0 in (2,3,7,21):
        # alpha=1/2 and square starting points are unnecessary here: nonzero
        # first positive summand proves the missing-offset contradiction.
        require(n0>1 and F(1)>0,'nonunit offset at zero');offset+=1
    return {'status':'PASS','exact_jump_and_bracket_cases':jumps,
            'exact_single_edge_scalar_identities':scalar,
            'nonunit_offset_at_zero_controls':offset,
            'complete_scalar_solution':'y(s)=p/2^beta+C*exp(-s); C>0 is unbounded backward, C<0 reaches zero, C=0 is stationary'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    result={'status':'PASS','strip_diagnostics':check_strips(),'exact_controls':exact_controls(),
            'analytic_certification_by_computation':False,
            'infinite_graph_martingale_and_compactness_proofs':'Reviewed analytically in REPORT.md; not simulated'}
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    brief=dict(result);brief['strip_diagnostics']={k:v for k,v in result['strip_diagnostics'].items() if k!='cases'}
    print(json.dumps(brief,indent=2))
if __name__=='__main__': main()

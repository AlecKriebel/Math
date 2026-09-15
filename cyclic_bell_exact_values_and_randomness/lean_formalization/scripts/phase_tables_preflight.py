#!/usr/bin/env python3
"""Exact finite settings-appendix regression checks, NOT Lean proof evidence.

Only rational/cyclotomic arithmetic is used. Roots are interpreted at the
principal root exp(2*pi*i/(8*d)); equality is reduced modulo Phi_(8*d).
Order checks below compare rational folded displacements, not floating-point
approximations of algebraic probabilities. No asymptotic claim is tested by a
finite sample. No external test verdict is imported by the Lean sources.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import general_exact_preflight as e


def exp_phase(d: int, turns: F) -> e.E:
    exponent = F(8*d)*turns
    if exponent.denominator != 1:
        raise ValueError('Phase not represented in the chosen exact field')
    return e.root(8*d, exponent.numerator)


def projector(v: list[e.E]) -> list[list[e.E]]:
    # v has unit-modulus coordinates; the unit vector is v/sqrt(d).
    return [[a*b.conj()/len(v) for b in v] for a in v]


def alice(d: int, alpha: F, a: int) -> list[e.E]:
    return [exp_phase(d, -F(a+alpha)*j/d) for j in range(d)]


def bob(d: int, beta: F, b: int) -> list[e.E]:
    return [exp_phase(d, F(b+beta)*j/d) for j in range(d)]


def sine(d: int, argument_over_pi: F) -> e.E:
    return (exp_phase(d, argument_over_pi/2)-exp_phase(d, -argument_over_pi/2))/(2*e.root(8*d, 2*d))


def literal_trace_born(d: int, M, N):
    # Full joint-state indices, independent of the entangled trace shortcut.
    ans=e.elt(8*d,[0])
    for i,j,k,l in product(range(d),repeat=4):
        rho=F(int(i==j and k==l),d)
        if rho:
            ans += rho*M[k][i]*N[l][j]
    return ans


def folded_displacement(d: int, t: F) -> F:
    u=t % d
    return min(u, F(d)-u)


def dimension_checks(d: int, C: e.Checks):
    one=e.elt(8*d,[1]); zero=one*0
    ident=e.ident(d,8*d)
    alpha=(F(0), F(-1,2)); beta=(F(-1,4), F(-3,4))
    matrices={}
    for party,offsets,fn in [('A',alpha,alice),('B',beta+alpha,bob)]:
        for x,offset in enumerate(offsets):
            vectors=[fn(d,offset,a) for a in range(d)]
            pvm=[projector(v) for v in vectors]
            matrices[(party,x)]=pvm
            for a,P in enumerate(pvm):
                C.equal(f'd{d}:{party}{x}:{a}:Hermitian',e.adj(P),P)
                C.equal(f'd{d}:{party}{x}:{a}:idempotent',e.mm(P,P),P)
                C.equal(f'd{d}:{party}{x}:{a}:trace',e.tr(P),one)
                for b in range(d):
                    ip=sum((vectors[a][j].conj()*vectors[b][j] for j in range(d)),zero)/d
                    C.equal(f'd{d}:{party}{x}:basis inner {a},{b}',ip,one*int(a==b))
            total=[[sum((P[i][j] for P in pvm),zero) for j in range(d)] for i in range(d)]
            C.equal(f'd{d}:{party}{x}:complete',total,ident)
    C.equal(f'd{d}:state trace',sum((one/d for _ in range(d)),zero),one)
    C.equal(f'd{d}:delta signs',tuple(a-b for a in alpha for b in beta),
            (F(1,4),F(3,4),F(-1,4),F(1,4)))
    peak=one/(2*d**3*sine(d,F(1,4*d))**2)
    for x,y in product(range(2),repeat=2):
        table=[]
        for a in range(d):
            row=[]
            for b in range(d):
                t=F(a-b)+alpha[x]-beta[y]
                P,Q=matrices[('A',x)][a],matrices[('B',y)][b]
                p=e.phi_expect(P,Q);row.append(p)
                u,v=alice(d,alpha[x],a),bob(d,beta[y],b)
                g=sum(((u[j]*v[j]).conj() for j in range(d)),zero)
                C.equal(f'd{d}:standard{x}{y}:Born/amplitude {a},{b}',p,g.normsq()/d**3)
                if d<=4:
                    C.equal(f'd{d}:standard{x}{y}:full trace {a},{b}',p,literal_trace_born(d,P,Q))
                sden=sine(d,t/d)
                C.truth(f'd{d}:standard{x}{y}:denominator nonzero {a},{b}',sden!=zero)
                C.equal(f'd{d}:standard{x}{y}:literal sine ratio {a},{b}',p,sine(d,t)**2/(d**3*sden**2))
                C.equal(f'd{d}:standard{x}{y}:numerator half {a},{b}',sine(d,t)**2,one/2)
                C.truth(f'd{d}:standard{x}{y}:folded-distance bound {a},{b}',folded_displacement(d,t)>=F(1,4))
            table.append(row)
        C.equal(f'd{d}:standard{x}{y}:sum one',sum((sum(r,zero) for r in table),zero),one)
        for a in range(d):
            C.equal(f'd{d}:standard{x}{y}:Alice marginal {a}',sum(table[a],zero),one/d)
            C.equal(f'd{d}:standard{x}{y}:Bob marginal {a}',sum((r[a] for r in table),zero),one/d)
        a,b=(0,1) if (x,y)==(0,1) else (0,0)
        C.equal(f'd{d}:standard{x}{y}:peak attained',table[a][b],peak)
        C.truth(f'd{d}:standard{x}{y}:not uniform',any(p!=one/d**2 for r in table for p in r))
        C.negative(f'd{d}:wrong standard normalization{x}{y}',sum((sum(r,zero) for r in table),zero)*d,one)
    apeak=one/(d**3*sine(d,F(1,2*d))**2)
    for c in range(2):
        cross=[]
        for a,b in product(range(d),repeat=2):
            Q=matrices[('B',2+c)][b]
            matched=e.phi_expect(matrices[('A',c)][a],Q)
            C.equal(f'd{d}:anchor{c}:matching {a},{b}',matched,one*F(int(a==b),d))
            p=e.phi_expect(matrices[('A',1-c)][a],Q);cross.append(p)
            t=F(a-b)+alpha[1-c]-alpha[c]
            C.equal(f'd{d}:anchor{c}:cross sine ratio {a},{b}',p,one/(d**3*sine(d,t/d)**2))
            C.truth(f'd{d}:anchor{c}:folded-distance bound {a},{b}',folded_displacement(d,t)>=F(1,2))
            if d==2:
                C.equal(f'd2:anchor{c}:qubit exception {a},{b}',p,one/4)
        C.equal(f'd{d}:anchor{c}:cross peak attained',cross[0],apeak)
        C.equal(f'd{d}:anchor{c}:cross sum one',sum(cross,zero),one)
        if d>=3:
            C.truth(f'd{d}:anchor{c}:nonuniform',any(p!=one/d**2 for p in cross))
            C.negative(f'd{d}:false uniform anchor{c}',cross[0],one/d**2)
        else:
            C.negative(f'd2:reject claimed strict anchor gap {c}',any(p!=one/4 for p in cross),True)
    # Resonant identity works even when the quotient formula is undefined.
    for t in [F(0),F(d),F(-d),F(1,4),F(-7,4),F(d*3)+F(1,2)]:
        g=sum((exp_phase(d,t*j/d) for j in range(d)),zero)
        C.equal(f'd{d}:geometric telescoping {t}',(one-exp_phase(d,t/d))*g,one-exp_phase(d,t))
        C.equal(f'd{d}:division-free squared identity {t}',sine(d,t/d)**2*g.normsq(),sine(d,t)**2)
    if d>=3:
        # Same ordinary representatives, changed Fourier direction on Bob only.
        true=e.phi_expect(matrices[('A',0)][1],matrices[('B',0)][0])
        wrong=projector([exp_phase(d,-beta[0]*j/d) for j in range(d)])
        C.negative(f'd{d}:Bob Fourier-sign control',true,e.phi_expect(matrices[('A',0)][1],wrong))


def run(ds):
    start=datetime.now(timezone.utc);C=e.Checks()
    for d in ds: dimension_checks(d,C)
    if len(set(C.rows))!=len(C.rows) or len(set(C.controls))!=len(C.controls):
        raise AssertionError('duplicate check label')
    return {'status':'PASS_compiler_free_exact_regressions_only','kernel_checked':False,
        'actual_lean_invoked':False,'started_utc':start.isoformat(),
        'finished_utc':datetime.now(timezone.utc).isoformat(),'dimensions':list(ds),
        'checks':len(C.rows),'negative_controls':len(C.controls),'check_names':C.rows,
        'negative_control_names':C.controls,'arithmetic':'Fraction in Q[x]/Phi_(8d)',
        'limitations':['Finite samples are not universal proofs or Lean kernel checks.',
        'Rational folded-angle comparisons test reduction, not an ordered algebraic field engine.',
        'No finite numerical surrogate is used for the entropy limit.',
        'Same assistant, shared exact field implementation; not an independent-agent audit.']}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--min-d',type=int,default=2);p.add_argument('--max-d',type=int,default=7)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    if not 2<=a.min_d<=a.max_d<=12:
        p.error('Use 2<=min-d<=max-d<=12 for this bounded regression suite.')
    report=run(range(a.min_d,a.max_d+1))
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','dimensions','checks','negative_controls','kernel_checked']},indent=2))

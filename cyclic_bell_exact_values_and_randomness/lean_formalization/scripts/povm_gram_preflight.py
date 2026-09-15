#!/usr/bin/env python3
"""Exact Gram/dual/primal regression for a nonprojective finite-Eve optimum.

Three real trine states, equal priors, embedded into sixteen guessing labels.
This is a test of the general finite POVM interfaces, NOT a cyclic-Bell
maximizing strategy. No numeric values or certificates are imported into Lean.
"""
from datetime import datetime,timezone
from fractions import Fraction as F
from pathlib import Path
import argparse,hashlib,json
import general_exact_preflight as E


def run():
    C=E.Checks();n=24;o=E.elt(n,[1]);z=o*0
    sqrt2=E.root(n,3)+E.root(n,-3);sqrt3=E.root(n,2)+E.root(n,-2)
    C.equal('sqrt2 squared',sqrt2*sqrt2,2*o);C.equal('sqrt3 squared',sqrt3*sqrt3,3*o)
    vectors=[[o,z],[-o/2,sqrt3/2],[-o/2,-sqrt3/2]]
    I=E.ident(2,n);zero=E.ms(z,I);Q=[];sigma=[];total=zero;totalsigma=zero
    Lambda=E.ms(F(1,3),I)
    totalentrynorm=F(0)
    for g in range(16):
        if g<3:
            v=vectors[g]
            P=[[a*b.conj() for b in v] for a in v]
            C.equal(f'projector norm {g}',sum((a.normsq() for a in v),z),o)
            C.equal(f'projector square {g}',E.mm(P,P),P)
            effect=E.ms(F(2,3),P);state=E.ms(F(1,3),P)
            L=E.ms(sqrt2*sqrt3/3,P)
            D=E.ms(sqrt3/3,E.ma(I,E.ms(-1,P)))
        else:
            effect=zero;state=zero;L=zero;D=E.ms(sqrt3/3,I)
        Q.append(effect);sigma.append(state);total=E.ma(total,effect);totalsigma=E.ma(totalsigma,state)
        C.equal(f'POVM Gram identity {g}',E.mm(E.adj(L),L),effect)
        gap=E.ma(Lambda,E.ms(-1,state))
        C.equal(f'dual positive Gram identity {g}',E.mm(E.adj(D),D),gap)
        frobenius=sum((a.normsq().rat() for row in L for a in row),F(0));totalentrynorm+=frobenius
        C.equal(f'Gram Frobenius trace {g}',E.tr(effect).rat(),frobenius)
        for i in range(2):
            for j in range(2):C.truth(f'Gram entry bounded {g}/{i}{j}',L[i][j].normsq().rat()<=2)
    C.equal('POVM sum identity',total,I);C.equal('ensemble trace one',E.tr(totalsigma),o)
    C.equal('total Gram Frobenius norm',totalentrynorm,F(2))
    success=sum((E.tr(E.mm(q,s)) for q,s in zip(Q,sigma)),z)
    C.equal('primal success two thirds',success,2*o/3)
    C.equal('primal equals dual trace',success,E.tr(Lambda))
    C.negative('POVM cannot be required projective',E.mm(Q[0],Q[0]),Q[0])
    C.negative('fixed outcome is not optimal POVM',E.tr(sigma[0]),success)
    C.negative('doubled effects fail normalization',E.ms(2,total),I)
    return {'status':'exact_POVM_Gram_regression_passed_NOT_LEAN','kernel_checked':False,
            'checks':len(C.rows),'negative_controls':len(C.controls),'check_labels':C.rows,
            'negative_control_labels':C.controls,'arithmetic':'Fraction in Q[x]/Phi_24; exact Gram residuals',
            'scope':'Finite nonprojective trine ensemble certificate testing Gram parameterization, objective normalization and the dual helper. This is not a cyclic-Bell witness and does not prove compactness.'}


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();start=datetime.now(timezone.utc)
    result=run();result.update(started_utc=start.isoformat(),finished_utc=datetime.now(timezone.utc).isoformat(),script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),shared_arithmetic_sha256=hashlib.sha256(Path(__file__).with_name('general_exact_preflight.py').read_bytes()).hexdigest())
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['check_labels','negative_control_labels']},indent=2))

#!/usr/bin/env python3
"""Exact finite tests of the new ABE/POVM interfaces; NOT Lean proof evidence.

The Gaussian-rational implementation is reused from model_bridge_preflight.
These checks never certify infinite quantum domains, closure, or suprema.
"""
from __future__ import annotations
from datetime import datetime, timezone
from fractions import Fraction as F
from itertools import product, combinations, permutations
from pathlib import Path
import argparse
import hashlib
import json
from model_bridge_preflight import (G,Z,ONE,I,Checks,mm,adj,transpose,add,scale,
    ident,diag,zero,tr,kron,mv,ip,vec,me,sum_matrix,basis,pvm)


def det(A):
    n=len(A);answer=Z
    for perm in permutations(range(n)):
        term=G((-1)**sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n)))
        for i,j in enumerate(perm):term=term*A[i][j]
        answer+=term
    return answer


def exact_psd(A):
    if A!=adj(A):return False
    for k in range(1,len(A)+1):
        for ids in combinations(range(len(A)),k):
            minor=det([[A[i][j] for j in ids] for i in ids])
            if minor.im or minor.re<0:return False
    return True


def partial_e(R,nab,ne):
    if len(R)!=nab*ne:raise ValueError('Bad tensor dimension')
    return [[sum((R[i*ne+e][i*ne+f] for i in range(nab)),Z)
             for f in range(ne)] for e in range(ne)]


def lift_apply(T,v):
    """Direct index action of T tensor I on vec(S); no trace identity assumed."""
    n=len(T)
    if len(v)!=n*n:raise ValueError('Bad purification length')
    return [sum((T[i][k]*v[k*n+e] for k in range(n) if T[i][k]!=Z),Z)
            for i in range(n) for e in range(n)]


def guessing_povm(ne):
    # Positive mixture of two differently oriented projective measurements.
    # Outcome set is the full 4x4 guess alphabet; remaining effects are zero.
    one=pvm(ne,1);two=pvm(ne,6)
    return [scale(F(1,2),one[b]) if a==0 else
            scale(F(1,2),two[b]) if a==1 else zero(ne)
            for a,b in product(range(4),repeat=2)]


def case(C,na,nb,ne,roots,label):
    n=na*nb*ne;nab=na*nb
    if len(roots)!=n or sum(x*x for x in roots)!=1 or min(roots)<0:
        raise ValueError('Need normalized nonnegative root eigenvalues')
    U=basis(n,2);S=mm(mm(U,diag(roots)),adj(U));rho=mm(S,S);v=vec(S)
    C.equal(label+': root Hermitian',S,adj(S))
    C.equal(label+': density normalization',tr(rho),ONE)
    C.equal(label+': actual purification norm',ip(v,v),ONE)
    Q=guessing_povm(ne)
    C.equal(label+': Eve complete',sum_matrix(Q,ne),ident(ne))
    for g,q in enumerate(Q):
        C.truth(f'{label}: Eve {g} PSD principal minors',exact_psd(q))
    C.truth(label+': genuinely nonprojective Eve',any(mm(q,q)!=q for q in Q))
    C.reject(label+': forcing PVM idempotence',all(mm(q,q)==q for q in Q),True)
    if ne>1:
        C.truth(label+': Eve effects need not commute',any(mm(q,r)!=mm(r,q) for q in Q for r in Q))
    C.reject(label+': doubled Eve normalization',sum_matrix([scale(2,q) for q in Q],ne),ident(ne))
    C.reject(label+': doubled state amplitude',ip([2*z for z in v],[2*z for z in v]),ONE)
    A=[pvm(na,0),pvm(na,2)];B=[pvm(nb,3),pvm(nb,5)]
    LA=[[kron(kron(m,ident(nb)),ident(ne)) for m in M] for M in A]
    LB=[[kron(kron(ident(na),m),ident(ne)) for m in M] for M in B]
    LE=[kron(ident(nab),q) for q in Q]
    marginalE=partial_e(rho,nab,ne)
    for x,y in product(range(2),repeat=2):
        table=[];extended=[];sigmas=[]
        for a,b in product(range(4),repeat=2):
            P=kron(A[x][a],B[y][b]);LP=kron(P,ident(ne))
            C.equal(f'{label}: AB product {x}{y}{a}{b}',mm(LA[x][a],LB[y][b]),LP)
            C.equal(f'{label}: AB commutation {x}{y}{a}{b}',mm(LA[x][a],LB[y][b]),mm(LB[y][b],LA[x][a]))
            sigma=partial_e(mm(mm(LP,rho),adj(LP)),nab,ne);sigmas.append(sigma)
            C.truth(f'{label}: conditional PSD {x}{y}{a}{b}',exact_psd(sigma))
            bare=me(LP,rho);table.append(bare.re);rows=[]
            for g,q in enumerate(Q):
                joint=kron(P,q);r=me(joint,rho)
                C.equal(f'{label}: extended real {x}{y}{a}{b}/{g}',r.im,F(0))
                C.truth(f'{label}: extended nonnegative {x}{y}{a}{b}/{g}',r.re>=0)
                C.equal(f'{label}: sandwich pairing {x}{y}{a}{b}/{g}',tr(mm(q,sigma)),r)
                C.equal(f'{label}: Eve commutation {x}{y}{a}{b}/{g}',mm(LP,LE[g]),mm(LE[g],LP))
                # Sparse direct Hilbert action keeps exactness without storing a
                # huge tensor matrix. Both zero and nonprojective effects occur.
                lifted=lift_apply(LA[x][a],lift_apply(LB[y][b],lift_apply(LE[g],v)))
                C.equal(f'{label}: full extended embedding {x}{y}{a}{b}/{g}',ip(v,lifted),r)
                rows.append(r.re)
            extended.append(rows)
            C.equal(f'{label}: forget Eve {x}{y}{a}{b}',sum(rows),bare.re)
        C.equal(f'{label}: full conditional instrument {x}{y}',sum_matrix(sigmas,ne),marginalE)
        C.equal(f'{label}: extended total {x}{y}',sum(map(sum,extended)),F(1))
        C.equal(f'{label}: marginal total {x}{y}',sum(table),F(1))
        success=sum(extended[g][g] for g in range(16))
        C.truth(f'{label}: success interval {x}{y}',F(0)<=success<=F(1))
        for guess in (0,5,15):
            R=[[p if g==guess else F(0) for g in range(16)] for p in table]
            C.equal(f'{label}: fixed-guess success {x}{y}/{guess}',sum(R[g][g] for g in range(16)),table[guess])
    if ne>1:
        # Pairing with an arbitrary non-Hermitian matrix detects partial-trace
        # index orientation independently of probability-only (real) tests.
        T=[[G(F(i+j+1,7),F(2*i-j+1,11)) for j in range(ne)] for i in range(ne)]
        C.equal(label+': COMPLEX partial trace pairing',tr(mm(T,marginalE)),me(kron(ident(nab),T),rho))
        if tr(mm(transpose(T),marginalE))!=tr(mm(T,marginalE)):
            C.reject(label+': wrong partial trace transpose',tr(mm(transpose(T),marginalE)),tr(mm(T,marginalE)))
    return {'local_dimensions':[na,nb,ne],'mixed_state_rank':sum(x>0 for x in roots),
            'name':label,'guess_effects':16,'nonprojective_povm':True}


def most_likely_is_not_worst_adversary(C):
    # Exact classical extended behavior: uniform AB, perfectly correlated Eve.
    # This is not asserted to maximize either cyclic functional.
    r=[[F(int(g==pair),16) for g in range(16)] for pair in range(16)]
    p=[sum(row) for row in r]
    C.equal('recorded-uniform: normalized',sum(p),F(1))
    C.equal('recorded-uniform: largest AB entry',max(p),F(1,16))
    C.equal('recorded-uniform: Eve diagonal success',sum(r[g][g] for g in range(16)),F(1))
    C.reject('recorded-uniform: largest AB entry is NOT optimal Eve success',max(p),F(1))
    C.truth('d4: general floor is strictly weaker than table peak',F(1,16)<F(1,12)<F(3,32)<F(1))
    C.reject('d4: confusing general estimate with 3/32',F(1,12),F(3,32))


def run(which):
    C=Checks();cases=[]
    data={
        'tiny':(1,1,2,[F(3,5),F(4,5)]),
        'unequal':(1,2,2,[F(1,5),F(2,5),F(2,5),F(4,5)]),
        'ranktwo':(2,2,2,[F(3,5),F(4,5)]+[F(0)]*6),
        'trivialeve':(2,3,1,[F(1,10),F(1,10),F(2,10),F(2,10),F(3,10),F(9,10)])}
    for name in which:cases.append(case(C,*data[name],name))
    most_likely_is_not_worst_adversary(C)
    assert len(C.checks)==len(set(C.checks)) and len(C.controls)==len(set(C.controls))
    return {'status':'exact_adversarial_interface_tests_passed_NOT_LEAN',
            'kernel_checked':False,'closure_checked':False,'supremum_checked':False,
            'checks':len(C.checks),'negative_controls':len(C.controls),'cases':cases,
            'check_labels':C.checks,'negative_control_labels':C.controls,
            'scope':'Finite ABE, general POVM, sandwich, full extended-correlation embedding and guessing orientation only. Does not prove any universal or topological theorem.'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cases',nargs='+',choices=['tiny','unequal','ranktwo','trivialeve'],default=['tiny','unequal'])
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();started=datetime.now(timezone.utc)
    result=run(args.cases);result['started_utc']=started.isoformat();result['finished_utc']=datetime.now(timezone.utc).isoformat()
    result['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result['shared_arithmetic_sha256']=hashlib.sha256(Path(__file__).with_name('model_bridge_preflight.py').read_bytes()).hexdigest()
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['check_labels','negative_control_labels']},indent=2))

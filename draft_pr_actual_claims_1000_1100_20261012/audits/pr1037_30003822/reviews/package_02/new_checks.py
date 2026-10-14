#!/usr/bin/env python3
"""Review02 new exact incidence-minor/contraction checks. Explicit checks work under -O."""
import sys, json, time, itertools, math, hashlib, datetime, importlib.util
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parent
records=[]
def check(name,condition,**data):
    records.append({'name':name,'ok':bool(condition),**data})
    if not condition:raise RuntimeError(name)
def partitions(n):
    if n==0:return [()]
    ans=[]
    for p in partitions(n-1):
        ans.append(p+((n-1,),))
        for i in range(len(p)):ans.append(p[:i]+(p[i]+(n-1,),)+p[i+1:])
    return sorted(ans,key=lambda p:(-len(p),p))
def canon(blocks):return tuple(sorted(tuple(sorted(b)) for b in blocks))
def contracted_transfer(n,A,allow_empty=False):
    ps=partitions(n);index={p:i for i,p in enumerate(ps)};rows=[]
    for p in ps:
        states={tuple((i,) for i in range(n)):sp.Integer(1)}
        for b in p:
            weights=[sum(A[i,j] for i in b) for j in range(n)];nxt={}
            for q,v in states.items():
                compweights=[sum(weights[j] for j in c) for c in q]
                for mask in range(0 if allow_empty else 1,1<<len(q)):
                    sel=[i for i in range(len(q)) if mask>>i&1]
                    dest=canon([q[i] for i in range(len(q)) if i not in sel]+([tuple(j for i in sel for j in q[i])] if sel else []))
                    w=v*sp.prod(compweights[i] for i in sel);nxt[dest]=nxt.get(dest,0)+w
            states=nxt
        rows.append([states.get(q,0) for q in ps])
    return ps,sp.Matrix(rows)
def forest_minors(n,p,style='star'):
    m=n-1;edges=[]
    for b in p:
        edges.extend((b[0],i) for i in b[1:]) if style=='star' else edges.extend(zip(b,b[1:]))
    s=len(edges)
    if not s:return {0:sp.Integer(1)}
    incidence=sp.Matrix([[int(i==u)-int(i==v) for i in range(m)] for u,v in edges]);dets={}
    for I in itertools.combinations(range(m),s):
        d=incidence[:,list(I)].det()
        if d:dets[I]=d
    out={}
    for I,di in dets.items():
        for J,dj in dets.items():
            mask=sum(1<<(2*i) for i in I)+sum(1<<(2*j+1) for j in J)
            sign=(-1)**(s*(s-1)//2+sum(j<i for i in I for j in J));out[mask]=sign*di*dj
    return out
def columns(n,ps):
    fs=[forest_minors(n,p) for p in ps];mons=sorted(set().union(*map(set,fs)))
    return fs,sp.Matrix([[f.get(k,0) for f in fs] for k in mons])
def catalan(n):return math.comb(2*n,n)//(n+1)
def matrix_case(n,seed):return sp.Matrix(n,n,lambda i,j:((i+1)*(j+2)+seed*(i-j+2)+i*i+2*j*j)%7-3)
def main():
    started=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
    spec=importlib.util.spec_from_file_location('fresh',ROOT/'clean_extraction/evidence/fresh_20261013/transfer_01/fresh_checks.py');fresh=importlib.util.module_from_spec(spec);spec.loader.exec_module(fresh)
    # Forest products are computed from integer incidence minors, independently of wedge multiplication.
    for n in range(1,7):
        ps=partitions(n);fs,Phi=columns(n,ps);d=Phi.rank();check('incidence-minor full Bell rank',d==catalan(n),n=n,bell=len(ps),rank=d)
        for p,f in zip(ps,fs):check('incidence star/path identity',f==forest_minors(n,p,'path'),n=n,partition=p)
        if n<=4:
            # Compare to the original exterior implementation by embedding U basis into vertex pairs.
            images=[]
            for i in range(n-1):images.extend([fresh.diff(2*i,2*(n-1)),fresh.diff(2*i+1,2*(n-1)+1)])
            for p,f in zip(ps,fs):check('incidence versus wedge forest',fresh.substitute(f,images)==fresh.forest(p),n=n,partition=p)
    # New exact weighted matrices, including zero row sums and singular/zero boundaries.
    cases=[(1,sp.Matrix([[-7]]),'n1signed'),(1,sp.zeros(1),'n1zero'),(2,sp.Matrix([[4,-4],[3,2]]),'zero_row_invertible'),(2,sp.zeros(2),'zero'),(3,sp.Matrix([[1,-2,1],[2,3,1],[-1,0,2]]),'n3_zero_row'),(3,sp.Matrix([[1,2,3],[2,4,6],[1,0,-1]]),'n3_singular'),(4,matrix_case(4,3),'n4new_signed'),(5,matrix_case(5,2),'n5new_signed')]
    for n,A,label in cases:
        ps,T=contracted_transfer(n,A);fs,Phi=columns(n,ps);pivotcols=Phi.rref()[1];P=Phi[:,list(pivotcols)];rows=P.T.rref()[1];images=Phi*T.T;G=P[list(rows),:].inv()*images[list(rows),list(pivotcols)]
        check('constant quotient full reconstruction',P*G==images[:,list(pivotcols)],case=label,n=n)
        check('kernel intertwining',images==P*G*P[list(rows),:].inv()*Phi[list(rows),:],case=label,n=n)
        da=A.det();dg=G.det();check('quotient determinant +1',dg==da**catalan(n),case=label,n=n,detA=str(da),detG=str(dg),dim=G.rows)
        if n<=3:check('full determinant small n',T.det()==da**catalan(n),case=label,n=n)
        if n<=4:
            direct,_=fresh.transition(n,A.tolist());check('contraction versus edge-subset enumeration',T==direct,case=label,n=n)
        if n==4:
            perm=sum(sp.prod(A[i,p[i]] for i in range(n)) for p in itertools.permutations(range(n)))
            check('n4 full determinant consistency',T.det()==da**catalan(n)*perm,case=label,permanent=str(perm))
        if n==5:
            # Exact integer quotient inferred from full evaluated determinant; finite consistency only.
            check('n5 numerical divisibility',da!=0 and int(T.det())%int(da**catalan(n))==0,case=label,detA=str(da))
    A=sp.Matrix([[4,-1],[3,2]]);_,good=contracted_transfer(2,A);_,bad=contracted_transfer(2,A,True);check('fault: allowing X-only inputs detected',good!=bad and good.det()!=bad.det(),correct_det=str(good.det()),faulty_det=str(bad.det()))
    # Probe candidate ordered operators with new values; use explicit checks, not removable asserts.
    for n,A in [(2,sp.Matrix([[4,-1],[3,2]])),(3,sp.Matrix([[4,-1,2],[3,2,-1],[-2,1,3]]))]:
        r=list(map(sum,A.tolist()));check('nonzero rows chosen',all(r));B=sp.diag(*r).inv()*A;S=sp.diag(*[sum(A[i,j] for i in range(n)) for j in range(n)])-A.T*sp.diag(*r).inv()*A;detD=sp.prod(r);k=fresh.kernel(n,A.tolist());fs=[fresh.forest(p) for p in partitions(n)]
        direct=[fresh.integrate(fresh.mul(k,f),n) for f in fs]
        ordered=[fresh.scale(fresh.raise_S(n,fresh.rho(n,fresh.lower(n,f,r),B),S),detD) for f in fs]
        swapped=[fresh.scale(fresh.raise_S(n,fresh.lower(n,fresh.rho(n,f,B),r),S),detD) for f in fs]
        check('new ordered factor equality',ordered==direct,n=n);check('fault: swapped lowering/substitution detected',swapped!=direct,n=n);check('fault: missing normalization detected',[fresh.scale(f,detD) for f in ordered]!=direct,n=n)
    # A deliberate false predicate must fail in both normal and optimized Python.
    try:check('injected false predicate',False)
    except RuntimeError:records.pop();check('fault: checker remains active under -O',True,optimization=sys.flags.optimize)
    else:raise RuntimeError('disabled check')
    result={'start_utc':started,'elapsed_seconds':time.monotonic()-t,'python':sys.version,'sympy':sp.__version__,'optimization':sys.flags.optimize,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'records':records,'pass':all(x['ok'] for x in records),'scope':'Fresh review02 numerical/exact finite checks only; incidence-minor and block-contraction mechanisms independently authored; Gaussian probes call the copied fresh family exterior operations; no original omitted historical checker replay.'}
    p=ROOT/('NEW_CHECK_RESULTS_O.json' if sys.flags.optimize else 'NEW_CHECK_RESULTS_NORMAL.json');p.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='records'}),flush=True)
if __name__=='__main__':main()

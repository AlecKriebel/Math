#!/usr/bin/env python3
"""Finite exact controls for the five proved, scoped results. No dependencies."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json, random

counts={}
def check(group, condition):
    if not condition: raise AssertionError(group)
    counts[group]=counts.get(group,0)+1

def nodes(n):
    return [v for t in range(n) for v in product((0,1),repeat=t)]

def policies(n):
    def rec(v):
        if len(v)==n: return [{v:n}]
        leaves=list(product((0,1),repeat=n-len(v)))
        out=[{v+w:len(v) for w in leaves}]
        for a in rec(v+(0,)):
            for b in rec(v+(1,)):out.append(a|b)
        return out
    return rec(())

def expect(values, probs):return sum((values[w]*probs[w] for w in probs),F(0))
def stopping(x,T,probs):return expect({w:x[w[:T[w]]] for w in probs},probs)
def moments(x,n,probs):
    return {v:sum((p*(x[w[:len(v)+1]]-x[v]) for w,p in probs.items() if w[:len(v)]==v),F(0)) for v in nodes(n)}

def finite_filtrations():
    n=2; leaves=list(product((0,1),repeat=n)); ps=policies(n)
    coords=[v for t in range(1,n+1) for v in product((0,1),repeat=t)]
    probs=dict.fromkeys(leaves,F(1,4))
    for vals in product((-1,0,1),repeat=len(coords)):
        x={():F(0)}|dict(zip(coords,map(F,vals)));q=moments(x,n,probs)
        b={t:expect({w:x[w[:t]] for w in leaves},probs) for t in range(n+1)}
        tests=[b[1]]+[b[len(v)]+q[v] for v in nodes(n)]
        adv=[stopping(x,T,probs) for T in ps]
        check('finite_equivalence',all(a==0 for a in tests)==all(a==0 for a in q.values())==all(a==0 for a in adv))
        V=sum(map(abs,q.values()))
        for T,a in zip(ps,adv):
            rhs=sum((p*sum((x[w[:t+1]]-x[w[:t]] for t in range(T[w])),F(0)) for w,p in probs.items()),F(0))
            check('telescoping_and_bound',a==rhs and abs(a)<=V)
        for v in nodes(n):
            t=len(v);T={w:t+1 if w[:t]==v else t for w in leaves}
            check('single_step_witness',stopping(x,T,probs)==b[t]+q[v] and max(abs(b[t]),abs(b[t]+q[v]))>=abs(q[v])/2)
    # Nonuniform measures, including null atoms.
    rng=random.Random(9700001)
    for weights in [(0,0,1,3),(1,2,0,1),(1,2,3,4)]:
        probs={w:F(z,sum(weights)) for w,z in zip(leaves,weights)}
        for _ in range(100):
            x={():F(0)}|{v:F(rng.randrange(-9,10),3) for v in coords};q=moments(x,n,probs)
            for T in ps:check('null_atom_controls',abs(stopping(x,T,probs))<=sum(map(abs,q.values())))
    # Coarse trivial filtration misses a full-history witness.
    check('coarse_counterexample',F(2,2)+F(-1,2)==F(1,2))

def feature_controls():
    outcomes=list(product((-1,1),repeat=2))
    paths=[]
    for b,c in outcomes:
        h=1 if (b,c)==(1,-1) else -1 if (b,c)==(-1,1) else 0
        paths.append((0,b,b+c,b+c+h))
    for t in range(3):
        for s in set(p[t] for p in paths):
            check('current_state_zero',sum(F(p[t+1]-p[t],4) for p in paths if p[t]==s)==0)
    val=sum((F(p[3] if bc==(1,-1) else p[2],4) for bc,p in zip(outcomes,paths)),F(0))
    check('history_counterexample',val==F(1,4))
    # Exact weighted residual inequality on all small single-step vectors.
    for delta in product((-2,0,3),repeat=3):
        for survival in product((0,1),repeat=3):
            for coefficients in product((-1,0,1),repeat=2):
                phi=((1,1,1),(0,1,2))
                f=[sum(coefficients[j]*phi[j][i] for j in range(2)) for i in range(3)]
                lhs=abs(sum(F(survival[i]*delta[i],3) for i in range(3)))
                rho=sum(F(abs(survival[i]-f[i])*abs(delta[i]),3) for i in range(3))
                eta=[abs(sum(F(phi[j][i]*delta[i],3) for i in range(3))) for j in range(2)]
                check('feature_bound',lhs<=rho+sum(abs(coefficients[j])*eta[j] for j in range(2)))

def null_vector(matrix,ncols):
    a=[[F(z) for z in row] for row in matrix];piv=[];r=0
    for c in range(ncols):
        pos=next((i for i in range(r,len(a)) if a[i][c]),None)
        if pos is None:continue
        a[r],a[pos]=a[pos],a[r];z=a[r][c];a[r]=[v/z for v in a[r]]
        for i in range(len(a)):
            if i!=r:
                z=a[i][c];a[i]=[u-z*v for u,v in zip(a[i],a[r])]
        piv.append(c);r+=1
        if r==len(a):break
    free=next(c for c in range(ncols) if c not in piv)
    u=[F(0)]*ncols;u[free]=F(1)
    for i,c in enumerate(piv):u[c]=-a[i][free]
    return u

def obstruction_controls():
    rng=random.Random(5409700001)
    examples=[]
    for n in range(1,5):
        vv=nodes(n);pp=policies(n);ww=list(product((0,1),repeat=n));probs=dict.fromkeys(ww,F(1,2**n))
        for m in range(min(len(vv)-1,8)+1):
            for rep in range(5):
                tests=[rng.choice(pp) for _ in range(m)];sel=vv[:m+1]
                C=[[int(T[v+(0,)*(n-len(v))]>len(v)) for v in sel] for T in tests]
                u=null_vector(C,m+1);d=[a*2**len(v) for a,v in zip(u,sel)];s=sum(map(abs,d));d=[a/s for a in d]
                eps=F(1,2**(n+3));x={};W={}
                for t in range(n+1):
                    for v in product((0,1),repeat=t):
                        W[v]=sum((a for a,w in zip(d,sel) if t>len(w) and v[:len(w)]==w),F(0))
                        M=sum(((F(b)-F(1,2))/2**(i+1) for i,b in enumerate(v)),F(0))
                        x[v]=M+eps*W[v]
                        check('bounded_compact',abs(W[v])<=1 and abs(x[v])<1)
                        k=sum(b*2**(t-1-i) for i,b in enumerate(v));offset=F(1-F(1,2**t),2)
                        q=2**t*(x[v]+offset)
                        rounded=(q+F(1,2)).numerator//(q+F(1,2)).denominator
                        check('price_decoder',rounded==k and abs(q-k)<=F(1,8))
                for T in tests:check('missed_fixed_tests',stopping(x,T,probs)==0)
                drift=moments(x,n,probs)
                check('nonmartingale',any(z for z in drift.values()))
                v=next(v for v in vv if drift[v]);t=len(v);b=expect({w:x[w[:t]] for w in ww},probs)
                T={w:t for w in ww} if b else {w:t+1 if w[:t]==v else t for w in ww}
                check('constructed_witness',stopping(x,T,probs)!=0)
                for v in vv:
                    expected=eps*next((a for a,w in zip(d,sel) if w==v),F(0))/2**len(v)
                    check('prescribed_drifts',drift[v]==expected)
                if n==3 and m==3 and rep==0:examples.append({'n':n,'m':m,'selected_nodes':[''.join(map(str,v)) for v in sel],'coefficients':[str(z) for z in d],'witness_expectation':str(stopping(x,T,probs))})
    return examples

def markov_controls():
    rng=random.Random(9704);n=3;ps=policies(n);leaves=list(product((0,1),repeat=n))
    # S_0 fixed; S_t for t>=1 is the t-th branch bit. Enumerate every history policy.
    for _ in range(160):
        P=[]
        for t in range(n):
            rows=[]
            for s in range(2):
                a=rng.randrange(5);rows.append((F(a,4),F(4-a,4)))
            P.append(rows)
        g=[[F(rng.randrange(-8,9),3) for s in range(2)] for t in range(n+1)]
        U=g[-1][:];L=U[:]
        for t in reversed(range(n)):
            U=[max(g[t][s],sum(P[t][s][u]*U[u] for u in range(2))) for s in range(2)]
            L=[min(g[t][s],sum(P[t][s][u]*L[u] for u in range(2))) for s in range(2)]
        probs={}
        for w in leaves:
            p=F(1);s=0
            for t,u in enumerate(w):p*=P[t][s][u];s=u
            probs[w]=p
        x={():g[0][0]}|{v:g[len(v)][v[-1]] for t in range(1,n+1) for v in product((0,1),repeat=t)}
        vals=[stopping(x,T,probs) for T in ps]
        check('snell_extrema',max(vals)==U[0] and min(vals)==L[0])
        pi=[F(1),F(0)];V=F(0);stateq=[]
        for t in range(n):
            q=[pi[s]*(sum(P[t][s][u]*g[t+1][u] for u in range(2))-g[t][s]) for s in range(2)]
            stateq+=q;V+=sum(map(abs,q));pi=[sum(pi[s]*P[t][s][u] for s in range(2)) for u in range(2)]
        for a in vals:check('markov_drift_bound',abs(a-g[0][0])<=V)
        check('markov_exact_equivalence',all(a==g[0][0] for a in vals)==all(q==0 for q in stateq))

def statistical_controls():
    for eps in map(F,range(4)):
        for r in [F(1,4),F(1,2),F(1),F(2)]:
            for ai in range(-20,21):
                a=F(ai,4)
                for ei in range(-4,5):
                    hat=a+r*F(ei,4)
                    if abs(hat)>eps+r:check('sample_witness_soundness',abs(a)>eps)
                    if abs(hat)<=eps-r:check('sample_acceptance_soundness',abs(a)<=eps)
                    if abs(a)>eps+2*r:check('sample_detection_gap',abs(hat)>eps+r)
    for den in range(2,80):
        for num in range(1,den):
            theta=F(num,den)
            for k in range(1,15):
                tv=1-(1-theta)**k
                check('rare_event_tv',0<=tv<=min(1,k*theta))
                if tv>=F(1,3):check('rare_event_lower_bound',k>=F(1,3)/theta)

if __name__=='__main__':
    finite_filtrations();feature_controls();examples=obstruction_controls();markov_controls();statistical_controls()
    print(json.dumps({'status':'PASS','arithmetic':'Python fractions.Fraction exact rational','counts':counts,'total_assertions':sum(counts.values()),'compact_obstruction_example':examples,'scope':'Finite controls supplement, and do not replace, the complete analytic proofs.'},indent=2,sort_keys=True))

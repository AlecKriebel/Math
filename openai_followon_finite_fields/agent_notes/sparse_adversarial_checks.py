"""Independent adversarial checks of the proposed sparse reductions.

Small-degree Taylor expansion and dense Euclid are deliberately used as separate
oracles. Field enumeration occurs only in these finite tests. The proposed
algorithm itself is not certified by passing these tests.
"""
from __future__ import annotations
import hashlib
import itertools
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'code'))
from finite_fields import FiniteField


def trie(F, terms, alpha):
    """Explicit-stack implementation; exponents retain their full integer values."""
    weighted = [(n, F.mul(a, F.pow(alpha, n))) for n, a in terms]
    nodes = [(weighted, None)]
    answer = {}
    stack = [(0, False)]
    bins = 0
    while stack:
        i, done = stack.pop()
        ts, children = nodes[i]
        if len(ts) == 1:
            answer[i] = (0, ts[0][1])
            continue
        if not done:
            grouped = {}
            for n, a in ts:
                q, r = divmod(n, F.p)
                grouped.setdefault(r, []).append((q, a))
            children = []
            for r, childterms in sorted(grouped.items()):
                j = len(nodes)
                nodes.append((childterms, None))
                children.append((r, j))
            nodes[i] = ts, children
            stack.append((i, True))
            stack.extend((j, False) for _, j in reversed(children))
        else:
            v = min(answer[j][0] for _, j in children)
            active = [(r, answer[j][1]) for r, j in children if answer[j][0] == v]
            for k in range(len(active)):
                c = F.zero
                for r, a in active:
                    # k < len(active) <= p; no scan of p or the exponents.
                    choose = 1
                    for u in range(k):
                        choose = choose * ((r-u) % F.p) % F.p
                        choose = choose * pow(u+1, -1, F.p) % F.p
                    bins += 1
                    c = F.add(c, F.mul(a, F.element(choose)))
                if c != F.zero:
                    answer[i] = (F.p*v+k, c)
                    break
            else:
                raise AssertionError('Vandermonde bound failed')
    return answer[0], {'nodes': len(nodes), 'binomial_values': bins}


def direct_taylor(F, terms, alpha):
    """Dense Taylor oracle, used only for small maximum degree."""
    weighted = [(n, F.mul(a, F.pow(alpha, n))) for n, a in terms]
    for k in range(max(n for n, _ in terms)+1):
        c = F.zero
        for n, a in weighted:
            c = F.add(c, F.mul(a, F.element(math.comb(n, k) if k <= n else 0)))
        if c != F.zero:
            return k, c
    raise AssertionError('nonzero polynomial transformed to zero')


def trim(a, p):
    a = [x % p for x in a]
    while a and not a[-1]: a.pop()
    return a


def mul(a, b, p):
    c = [0] * max(0, len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): c[i+j] = (c[i+j]+x*y) % p
    return trim(c, p)


def divide(a, b, p):
    a, b = trim(a,p), trim(b,p)
    q = [0]*max(0,len(a)-len(b)+1)
    ib = pow(b[-1],-1,p)
    while len(a)>=len(b):
        s=len(a)-len(b); z=a[-1]*ib%p; q[s]=z
        for j,y in enumerate(b): a[s+j]=(a[s+j]-z*y)%p
        a=trim(a,p)
    return trim(q,p),a


def gcd(a,b,p):
    while b: a,b=b,divide(a,b,p)[1]
    return [x*pow(a[-1],-1,p)%p for x in a]


def derivative(a,p): return trim([i*a[i]%p for i in range(1,len(a))],p)


def solve(matrix, rhs, p):
    rows=[list(a)+[b] for a,b in zip(matrix,rhs)]
    cols=len(matrix[0]); pivot=0; pivots=[]
    for j in range(cols):
        found=next((i for i in range(pivot,len(rows)) if rows[i][j]),None)
        if found is None: continue
        rows[pivot],rows[found]=rows[found],rows[pivot]
        z=pow(rows[pivot][j],-1,p)
        rows[pivot]=[x*z%p for x in rows[pivot]]
        for i in range(len(rows)):
            if i!=pivot:
                z=rows[i][j]
                rows[i]=[(x-z*y)%p for x,y in zip(rows[i],rows[pivot])]
        pivots.append(j); pivot+=1
    if any(not any(a[:cols]) and a[cols] for a in rows): return None
    ans=[0]*cols
    for i,j in enumerate(pivots): ans[j]=rows[i][cols]
    return ans


def pade(f,p,B):
    # 2B Taylor coefficients of f'/f; only f degrees <= 2B are used here.
    fp=derivative(f,p); s=[]; f0=pow(f[0],-1,p)
    for k in range(2*B):
        z=fp[k] if k<len(fp) else 0
        for j in range(1,min(k,len(f)-1)+1): z-=f[j]*s[k-j]
        s.append(z*f0%p)
    matrix=[];rhs=[]
    for k in range(2*B):
        row=[s[k-j] if j<=k else 0 for j in range(1,B+1)]
        row += [-int(k==j)%p for j in range(B)]
        matrix.append(row);rhs.append(-s[k]%p)
    v=solve(matrix,rhs,p)
    if v is None: return None
    q=trim([1]+v[:B],p); a=trim(v[B:],p)
    exact=mul(fp,q,p)==mul(f,a,p)
    return a,q,exact


def sparse_mul(a,b,p):
    c={}
    for n,x in a.items():
        for m,y in b.items(): c[n+m]=(c.get(n+m,0)+x*y)%p
    return {n:x for n,x in c.items() if x}


def run():
    result={'scope':'finite adversarial checks; no proof or novelty certification',
            'valuation_checks':{},'pade_checks':{},'huge_exponent_checks':[]}
    for p,h,length in [(2,(0,1),9),(3,(0,1),6),(2,(1,1,1),4),(3,(1,0,1),3)]:
        F=FiniteField(p,h)
        elements=list(F.elements_for_testing())
        alphas=[a for a in elements if a != F.zero]
        cases=0
        for coeffs in itertools.product(elements,repeat=length):
            ts=[(i,a) for i,a in enumerate(coeffs) if a!=F.zero]
            if not ts: continue
            for alpha in alphas:
                got,_=trie(F,ts,alpha)
                assert got==direct_taylor(F,ts,alpha),(p,h,ts,alpha,got)
                cases+=1
        result['valuation_checks'][f'F{F.q}_length{length}']=cases
    for p,length in [(2,9),(3,7),(5,5)]:
        count=0; failures_before_success=0; zero_derivatives=0
        for ftuple in itertools.product(range(p),repeat=length):
            f=trim(ftuple,p)
            if not f: continue
            a=next(i for i,x in enumerate(f) if x)
            f=f[a:]
            fp=derivative(f,p)
            if not fp:
                trueq=[1]; zero_derivatives+=1
            else:
                trueq=divide(f,gcd(f,fp,p),p)[0]
                trueq=[x*pow(trueq[0],-1,p)%p for x in trueq]
            B=1
            while True:
                candidate=pade(f,p,B)
                if candidate and candidate[2]:
                    A,Q,_=candidate
                    common=gcd(A,Q,p) if A else Q
                    reduced=divide(Q,common,p)[0]
                    reduced=[x*pow(reduced[0],-1,p)%p for x in reduced]
                    assert reduced==trueq,(p,f,B,reduced,trueq)
                    assert B <= 2*max(1,len(trueq)-1)
                    break
                failures_before_success+=1;B*=2
                assert B<=32
            count+=1
        result['pade_checks'][f'F{p}_length{length}']={
            'cases':count,'rejected_guesses':failures_before_success,
            'zero_derivative_inputs':zero_derivatives}
    # Huge known-root multiplicities, both promise-compliant and p-divisible.
    for p,h,k,g in [(2,(0,1),2000,{0:1,1:1}),
                    (2,(1,1,1),1001,{0:1,1:1,2:1}),
                    (3,(1,0,1),700,{0:1,2:1})]:
        F=FiniteField(p,h)
        alpha=F.one if len(h)==2 else F.element((0,1))
        pk=p**k
        for plus in (0,1):
            f={n*pk:a for n,a in g.items()}
            if plus: f=sparse_mul(f,g,p)
            ts=[(n,F.element(a)) for n,a in f.items()]
            (nu,lead),stats=trie(F,ts,alpha)
            assert nu==pk+plus,(p,h,k,plus,nu)
            assert lead != F.zero
            result['huge_exponent_checks'].append({'p':p,'field_degree':F.m,
                'max_exponent_bits':max(f).bit_length(),'term_count':len(f),
                'expected_multiplicity_bits':(pk+plus).bit_length(),
                'multiplicity_not_divisible_by_p':bool(plus),**stats})
    # An early zero Padé approximation must fail the exact sparse identity.
    p=3;f=[1]+[0]*99+[1]; early=pade(f,p,1)
    assert early is not None and not early[2]
    result['early_false_zero_rejected']=True
    result['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    return result

if __name__=='__main__':
    out=run()
    target=ROOT/'agent_notes'/'sparse_adversarial_checks.json'
    target.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

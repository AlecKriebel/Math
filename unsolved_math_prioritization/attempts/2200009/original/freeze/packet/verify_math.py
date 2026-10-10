#!/usr/bin/env python3
"""Exact finite diagnostics for the independently derived operator bridge.
No sampling result is a proof of Leake--Ryder's root-mesh theorem.
"""
from fractions import Fraction as F
from math import comb, factorial
import hashlib, json, sys

class Reject(ValueError): pass

def need(ok, text):
    if not ok: raise Reject(text)

def rational(x):
    need(type(x) in (int, F), 'exact rational required')
    return F(x)

def nat(n):
    need(type(n) is int and n >= 0, 'exact nonnegative integer required')
    return n

def poly(values):
    need(type(values) is tuple, 'coefficient tuple required')
    out = tuple(rational(x) for x in values)
    while out and out[-1] == 0: out = out[:-1]
    return out

def checked(p):
    need(type(p) is tuple and all(type(x) is F for x in p), 'canonical Fraction tuple required')
    need(not p or p[-1] != 0, 'noncanonical trailing zero')
    return p

def add(p,q):
    checked(p); checked(q)
    return poly(tuple((p[i] if i<len(p) else F(0))+(q[i] if i<len(q) else F(0)) for i in range(max(len(p),len(q)))))

def scale(p,c):
    checked(p); c=rational(c)
    return poly(tuple(c*x for x in p))

def mul(p,q):
    checked(p); checked(q)
    if not p or not q: return ()
    out=[F(0)]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):out[i+j]+=a*b
    return poly(tuple(out))

def shift(p,s):
    checked(p);s=rational(s)
    out=[F(0)]*len(p)
    for i,a in enumerate(p):
        for j in range(i+1):out[j]+=a*comb(i,j)*s**(i-j)
    return poly(tuple(out))

def reflect(p):
    checked(p)
    return poly(tuple(a*(-1)**i for i,a in enumerate(p)))

def delta(p,forward=False):
    checked(p); need(type(forward) is bool,'exact boolean required')
    return add(shift(p,1),scale(p,-1)) if forward else add(p,scale(shift(p,-1),-1))

def power_delta(p,k,forward=False):
    nat(k); checked(p); need(type(forward) is bool,'exact boolean required')
    for _ in range(k):p=delta(p,forward)
    return p

def factorial_poly(m,rising=False):
    nat(m); need(type(rising) is bool,'exact boolean required')
    p=poly((1,))
    for i in range(m):p=mul(p,poly((i if rising else -i,1)))
    return p

def conv(p,q,m,forward=False):
    nat(m);checked(p);checked(q);need(type(forward) is bool,'exact boolean required')
    need(len(p)<=m+1 and len(q)<=m+1,'ambient degree exceeded')
    ps=[p];qs=[q]
    for _ in range(m):ps.append(delta(ps[-1],forward));qs.append(delta(qs[-1],forward))
    out=()
    for k in range(m+1):out=add(out,scale(ps[k],qs[m-k][0] if qs[m-k] else F(0)))
    return out

def stencil(p,a):
    checked(p);need(type(a) is tuple,'stencil tuple required');a=tuple(rational(x) for x in a)
    out=()
    for j,c in enumerate(a):out=add(out,scale(shift(p,-j),c))
    return out

def bridge(p,a,m):
    nat(m);checked(p);need(len(p)<=m+1,'ambient degree exceeded')
    h=stencil(factorial_poly(m),a)
    return scale(conv(p,shift(h,m-1),m),F(1,factorial(m)))

def encoded(p):return [[x.numerator,x.denominator] for x in p]

def check_claims(c):
    expected={'schema':'mesh-preserver-claims-v1','problem_id':2200009,'rank':1030,'disposition':'previously_solved','new_mathematical_approaches':0,'solution_credit':'Leake and Ryder','universal_theorem_dependency':'arXiv:1712.02499v1 Theorem 1.4','zero_output_allowed':True,'finite_checks_are_proof':False,'novelty_claimed':False,'independent_review':'pending'}
    need(type(c) is dict and set(c)==set(expected),'claim keys')
    for k,v in expected.items():need(type(c[k]) is type(v) and c[k]==v,'claim '+k)

def json_pairs(items):
    d={}
    for k,v in items:
        need(k not in d,'duplicate JSON key');d[k]=v
    return d

def reject_constant(x):raise Reject('nonfinite JSON')

def main():
    if len(sys.argv)>1:
        need(len(sys.argv)==3 and sys.argv[1]=='--claims','usage: verify_math.py [--claims FILE]')
        with open(sys.argv[2],encoding='utf-8') as f:check_claims(json.load(f,object_pairs_hook=json_pairs,parse_constant=reject_constant))
    counts={}; trace=hashlib.sha256()
    def eq(a,b,label):
        need(a==b,label);counts[label]=counts.get(label,0)+1
        trace.update(json.dumps([label,encoded(a) if type(a) is tuple else ([a.numerator,a.denominator] if type(a) is F else a)],sort_keys=True,separators=(',',':')).encode()+b'\n')
    def yes(x,label):eq(bool(x),True,label)
    def denied(fn,label):
        try:fn()
        except (Reject,TypeError):counts[label]=counts.get(label,0)+1;return
        raise Reject('hostile input accepted: '+label)
    from itertools import product,combinations
    stencils=list(product((-1,0,1),repeat=3))+[(),(F(1,2),F(-2,3),F(3,7)),(1,-4,6,-4,1)]
    for m in range(9):
        fall=factorial_poly(m);rise=factorial_poly(m,True)
        eq(shift(fall,m-1),rise,'falling-rising-translation')
        for k in range(m+2):
            expected=scale(factorial_poly(m-k,True),factorial(m)//factorial(m-k)) if k<=m else ()
            eq(power_delta(rise,k),expected,'rising-difference')
        inputs=[poly((0,)*d+(1,)) for d in range(m+1)]+[poly(tuple(F((-1)**i*(i+1),i+2) for i in range(m+1))),()]
        for a in stencils:
            h=stencil(fall,a);r=shift(h,m-1)
            # Coefficients of T in powers of the backward difference.
            cs=[sum((F(a[j])*(-1)**k*comb(j,k) for j in range(k,len(a))),F(0)) for k in range(m+1)]
            for k,c in enumerate(cs):
                q=power_delta(r,m-k)
                eq(q[0] if q else F(0),factorial(m)*c,'stencil-difference-coefficient')
            for p in inputs:
                out=stencil(p,a)
                eq(bridge(p,a,m),out,'operator-bridge')
                eq(scale(conv(p,h,m,True),F(1,factorial(m))),out,'forward-operator-bridge')
            if not h:
                for p in inputs:eq(stencil(p,a),(),'zero-symbol-annihilates')
        for p in inputs:
            eq(conv(p,rise,m),scale(p,factorial(m)),'convolution-unit')
            for q in inputs:
                c=conv(p,q,m)
                eq(c,conv(q,p,m),'convolution-symmetry')
                eq(conv(reflect(p),reflect(q),m),scale(reflect(conv(p,q,m,True)),(-1)**m),'reflection-forward-backward')
                d,e=len(p)-1,len(q)-1
                deg=d+e-m if p and q and d+e>=m else -1
                eq(len(c)-1,deg,'convolution-degree')
                if c:eq(c[-1],p[-1]*q[-1]*F(factorial(d)*factorial(e),factorial(deg)),'convolution-leading-coefficient')
    # Exact quadratic mesh checks, including lower-degree factors and rational boundary gaps.
    roots=[F(i,2) for i in range(-4,5)]
    inputs=[(),poly((1,)),poly((-1,))]+[poly((-r,1)) for r in roots]
    inputs += [mul(poly((-a,1)),poly((-b,1))) for a,b in combinations(roots,2) if b-a>=1]
    for p in inputs:
        for q in inputs:
            c=conv(p,q,2)
            yes(len(c)<3 or c[1]**2-4*c[2]*c[0]>=c[2]**2,'quadratic-mesh')
    # Deliberately wrong identities must actually fail on explicit witnesses.
    x=poly((0,1));f=factorial_poly(3);h=f
    yes(scale(conv(x,h,3),F(1,6))!=x,'negative-missing-translation')
    yes(conv(f,shift(h,2),3)!=f,'negative-missing-factorial')
    yes(conv(f,f,3)!=conv(f,f,3,True),'negative-difference-direction')
    # Low-degree zero conventions and degree loss are explicit.
    eq(stencil(poly((1,)),(1,-1)),(),'constant-killed-by-difference')
    eq(stencil(factorial_poly(2),(1,-1)),poly((-2,2)),'degree-drop-linear-symbol')
    eq(stencil(factorial_poly(2),(1,-2,1)),poly((2,)),'degree-drop-constant-symbol')
    eq(stencil(factorial_poly(2),(1,-3,3,-1)),(),'degree-drop-zero-symbol')
    class IntChild(int):pass
    class FractionChild(F):pass
    for v in [True,False,1.0,'1',None,IntChild(1),FractionChild(1)]:
        denied(lambda v=v:poly((v,)),'exact-coefficient-hostiles')
        denied(lambda v=v:stencil(x,(v,)),'exact-stencil-hostiles')
        denied(lambda v=v:shift(x,v),'exact-shift-hostiles')
    for v in [True,False,1.0,'1',None,-1,F(1),IntChild(1)]:
        denied(lambda v=v:conv(x,x,v),'exact-degree-hostiles')
    for v in [[],[F(1)],(1,), (F(1),F(0)),(FractionChild(1),)]:denied(lambda v=v:conv(v,x,2),'canonical-polynomial-hostiles')
    denied(lambda:conv(f,x,2),'oversize-input-hostile')
    denied(lambda:conv(x,x,2,1),'boolean-direction-hostile')
    denied(lambda:stencil(x,[1]),'stencil-container-hostile')
    # No assertion statements: optimization must not remove any test.
    return {'schema':'mesh-preserver-diagnostics-v1','status':'PASS','counts':counts,'total_checks':sum(counts.values()),'trace_sha256':trace.hexdigest(),'scope':'Finite exact algebra checks; universal root-mesh conclusion depends on the credited theorem.'}

if __name__=='__main__':
    try:print(json.dumps(main(),sort_keys=True,separators=(',',':')))
    except (Reject,OSError,ValueError,TypeError,KeyError) as e:
        print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)

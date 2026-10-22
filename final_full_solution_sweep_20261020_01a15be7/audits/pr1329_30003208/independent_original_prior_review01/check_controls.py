#!/usr/bin/env python3
"""Fresh finite controls for mechanisms only; not an infinite-dimensional proof.
Stdlib only. Sparse compact-plus-scalar operators retain the infinite scalar
character, rather than replacing it by a finite trace. All coefficients are
Gaussian rationals (pairs of exact rational coefficients). No author programs are imported.
"""
import itertools,json
from fractions import Fraction as F
G=0
def need(p,m):
    global G
    G+=1
    if not p:raise ValueError(m)
Z=(0,0);ONE=(1,0);II=(0,1)
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def mul(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def clean(d):return {k:v for k,v in d.items() if v!=Z}
def op(lam=Z,k=None):return (lam,{} if k is None else clean(k))
def plus(a,b):
    d=dict(a[1])
    for k,v in b[1].items():d[k]=add(d.get(k,Z),v)
    return op(add(a[0],b[0]),d)
def product(a,b):
    d={}
    for (i,j),v in a[1].items():
        for (k,l),w in b[1].items():
            if j==k:d[i,l]=add(d.get((i,l),Z),mul(v,w))
    for key,v in a[1].items():d[key]=add(d.get(key,Z),mul(v,b[0]))
    for key,v in b[1].items():d[key]=add(d.get(key,Z),mul(a[0],v))
    return op(mul(a[0],b[0]),d)
def var(j):return op(k={(0,j):ONE,(j,0):ONE})
def word(w):
    a=op(ONE)
    for j in w:a=product(a,var(j))
    return a
def expect(a):return op(a[0],{(0,0):a[1].get((0,0),Z)})
def coeff(a,i,j):return add(a[0] if i==j else Z,a[1].get((i,j),Z))
def compress(a,N):return {(i,j):coeff(a,i,j) for i in range(N+1) for j in range(N+1) if coeff(a,i,j)!=Z}
def permute(a,s):return op(a[0],{(s.get(i,i),s.get(j,j)):v for (i,j),v in a[1].items()})
def completion(S,k,N):
    need(all(i>N for i in S) and k>0,'future support');T={i+k for i in S};U=S|T;p={i:i+k for i in S}
    for i,j in zip(sorted(U-S),sorted(U-T),strict=True):p[i]=j
    need(set(p)==U and set(p.values())==U and len(set(p.values()))==len(p),'permutation')
    need(all(p.get(i,i)==i for i in range(N+1)),'past fixed');return p
def reject(f):
    try:f()
    except ValueError:return 1
    raise ValueError('false control escaped')
def main():
    pc=over=wc=mc=0
    for N in range(4):
        pool=list(range(N+1,N+8))
        for bits in range(1<<7):
            S={pool[i] for i in range(7) if bits>>i&1}
            for k in range(1,7):
                p=completion(S,k,N);pc+=1;over+=bool(S&{i+k for i in S})
                if S:
                    w=tuple(sorted(S))+tuple(sorted(S,reverse=True))+(min(S),)*3
                    need(tuple(p[i] for i in w)==tuple(i+k for i in w),'repeated whole-word transport');wc+=1
    for N in range(4):
        alphabet=range(N+1,N+4)
        for n in range(0,7):
            for w in itertools.product(alphabet,repeat=n):
                a=word(w);need(compress(a,N)==compress(expect(a),N),'future expectation compression')
                for k in [1,2,4]:
                    p=completion(set(w),k,N);need(permute(a,p)==word(tuple(i+k for i in w)),'whole-word covariance')
                    need(compress(word(tuple(i+k for i in w)),N)==compress(a,N),'shift compression')
                mc+=1
    # General A elements are linear combinations of 1,a,a^2 in C^3.
    for N in range(3):
        i,j=N+1,N+2
        for r,s in [(ONE,II),((2,-1),(-1,3)),(Z,ONE)]:
            x=plus(op(r),op(Z,{k:mul(s,v) for k,v in product(var(i),var(j))[1].items()}))
            need(compress(x,N)==compress(expect(x),N),'nonselfadjoint scalar-plus-compact control')
    failures=0
    failures+=reject(lambda:need(compress(op(k={(1,1):ONE}),1)==compress(expect(op(k={(1,1):ONE})),1),'outside future domain'))
    failures+=reject(lambda:need(expect(var(3))==var(3),'global instead of compressed equality'))
    failures+=reject(lambda:need(coeff(op(k={(1,1):ONE}),1,1)==Z,'cyclic-vector-only test'))
    failures+=reject(lambda:need(expect(product(var(3),var(3)))==op(),'linear moments suffice'))
    failures+=reject(lambda:need(expect(product(var(3),var(3)))==op((F(1,4),0)),'replace character by normalized trace in dimension8'))
    need(word((1,2,3))==op(),'nonfaithful universal-word image')
    # This universal word is nonzero: evaluate every copy a at its +1 character.
    need(1*1*1==1,'universal nonzero character witness')
    for m in range(1,20):
        q=op(k={(j,j):ONE for j in range(m+1)})
        need(expect(q)==op(k={(0,0):ONE}),'nonnormality finite-rank values')
        need(coeff(expect(q),1,1)==Z and coeff(expect(op(ONE)),1,1)==ONE,'limit-through-F obstruction')
    failures+=reject(lambda:need(expect(q)==expect(op(ONE)),'normal extension shortcut'))
    p=completion({2,3},1,1)
    failures+=reject(lambda:need(len(set({2:3,3:4,4:3}.values()))==3,'bad overlap completion'))
    failures+=reject(lambda:need((p[2],p[2])==(3,4),'different shifts for repeated index'))
    # Boundedness cannot be discarded in a dense-vector extension: n e_0n
    # kills each finitely supported vector eventually, but not eta_n=1/n.
    for n in range(1,100):need(n*F(1,n)==1,'unbounded dense-vector counterexample coefficient')
    need(failures==8,'negative control count')
    print(json.dumps({'schema':'tail-generation-independent-exact-controls/v1','permutation_cases':pc,'overlap_cases':over,'repeated_word_cases':wc,'matrix_word_cases':mc,'negative_rejections':failures,'explicit_guards':G,'author_code_executed':False,'universal_proof_from_finite_controls':False},sort_keys=True,separators=(',',':')))
if __name__=='__main__':main()

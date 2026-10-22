#!/usr/bin/env python3
"""Exact supplemental controls for the graded/full-algebra separation.
Not a search for full algebra isomorphisms; the universal proof is in TURN_1.md.
"""
import itertools,json
from collections import Counter
checks=Counter()
def ck(v,label):
    assert v,label
    checks[label]+=1

def case(p,exhaust=False):
    d=next(a for a in range(2,p) if pow(a,(p-1)//2,p)==p-1)
    zero=(0,0);one=(1,0)
    add=lambda a,b:((a[0]+b[0])%p,(a[1]+b[1])%p)
    neg=lambda a:((-a[0])%p,(-a[1])%p)
    sub=lambda a,b:add(a,neg(b))
    mul=lambda a,b:((a[0]*b[0]+d*a[1]*b[1])%p,(a[0]*b[1]+a[1]*b[0])%p)
    scale=lambda a,c:((a[0]*c)%p,(a[1]*c)%p)
    es=list(itertools.product(range(p),repeat=2))
    # Finite-field multiplication and absence of zero divisors; no float arithmetic.
    for a in es:
        for b in es:
            ck(mul(a,b)==mul(b,a),'field_commutativity')
            ck(a==zero or b==zero or mul(a,b)!=zero,'field_no_zero_divisors')
    r=(0,1);ri=(0,pow(d,-1,p));half=pow(2,-1,p)
    ck(mul(r,r)==(d,0) and mul(r,ri)==one,'root_and_inverse')
    # Six-dimensional Lie bracket, ordered X0,X1,Y0,Y1,Z0,Z1.
    def bracket(v,w):
        out=[zero]*6
        for i,j,z,c in [(0,2,4,1),(0,3,5,1),(1,2,5,1),(1,3,4,d)]:
            out[z]=add(out[z],scale(sub(mul(v[i],w[j]),mul(v[j],w[i])),c))
        return tuple(out)
    old=[tuple(one if i==j else zero for i in range(6)) for j in range(6)]
    new=[]
    for a,b in [(0,1),(2,3),(4,5)]:
        for sign in [1,-1]:
            v=[zero]*6;v[a]=(half,0);v[b]=scale(ri,sign*half);new.append(tuple(v))
    # new order X+,X-,Y+,Y-,Z+,Z-.
    for i in range(6):
        for j in range(6):
            target=[zero]*6
            for a,b,z in [(0,2,4),(1,3,5)]:
                if (i,j)==(a,b):target=list(new[z])
                if (j,i)==(a,b):target=[neg(x) for x in new[z]]
            ck(bracket(new[i],new[j])==tuple(target),'split_bracket_identity')
    for a,b in [(0,1),(2,3),(4,5)]:
        ck(tuple(add(x,y) for x,y in zip(new[a],new[b]))==old[a],'basis_inverse')
        ck(tuple(mul(r,sub(x,y)) for x,y in zip(new[a],new[b]))==old[b],'basis_inverse')
    # Exact contraction images; each v has p^2 central-coordinate choices.
    def comm_n(v,w):return sub(mul(v[0],w[1]),mul(w[0],v[1]))
    def comm_s(v,w):return ((v[0][0]*w[1][0]-w[0][0]*v[1][0])%p,(v[0][1]*w[1][1]-w[0][1]*v[1][1])%p)
    vs=list(itertools.product(es,repeat=2))
    distributions={}
    for name,comm in [('nonsplit',comm_n),('split',comm_s)]:
        hist=Counter()
        for v in vs:
            # For p=3,5 exhaust every contraction input; for p=7 use basis rank.
            if exhaust:
                im={comm(v,w) for w in vs}
                size=len(im)
            else:
                basis=[((1,0),zero),((0,1),zero),(zero,(1,0)),(zero,(0,1))]
                cols=[comm(v,w) for w in basis]
                rank=0 if all(c==zero for c in cols) else 1
                if any((a[0]*b[1]-a[1]*b[0])%p for a in cols for b in cols):rank=2
                size=p**rank
            expected=1 if v==(zero,zero) else (p*p if name=='nonsplit' else p**sum(v[0][i]!=0 or v[1][i]!=0 for i in range(2)))
            ck(size==expected,'contraction_image_size')
            hist[size]+=1
        count=sum(num*p*p//size for size,num in hist.items())
        expected=p**4+p*p-1 if name=='nonsplit' else (p*p+p-1)**2
        ck(count==expected,'conjugacy_count')
        distributions[name]={'image_histogram':dict(sorted(hist.items())),'conjugacy_classes':count}
    ck(distributions['split']['conjugacy_classes']-distributions['nonsplit']['conjugacy_classes']==2*(p-1)**2*(p+1),'strict_center_dimension_gap')
    # Ordered-monomial Hilbert coefficients (four weight1 and two weight2 generators).
    coeff=[1]
    for weight in [1,1,1,1,2,2]:
        nxt=[0]*(len(coeff)+weight*(p-1))
        for i,c in enumerate(coeff):
            for a in range(p):nxt[i+weight*a]+=c
        coeff=nxt
    ck(sum(coeff)==p**6 and coeff==coeff[::-1],'graded_dimension_and_symmetry')
    return {'p':p,'nonsquare_d':d,'contraction_method':'all inputs' if exhaust else 'four-basis rank','groups':distributions,'graded_dimension':sum(coeff),'top_degree':len(coeff)-1}

# Independently test the group law over F3 on all triples of elements of H(F3).
p=3
G=list(itertools.product(range(p),repeat=3))
def prod(g,h):return ((g[0]+h[0])%p,(g[1]+h[1])%p,(g[2]+h[2]+g[0]*h[1])%p)
for a,b,c in itertools.product(G,repeat=3):ck(prod(prod(a,b),c)==prod(a,prod(b,c)),'H3_associativity')
for a in G:
    v=(0,0,0)
    for _ in range(p):v=prod(v,a)
    ck(v==(0,0,0),'H3_exponent')
results=[case(p,p in (3,5)) for p in (3,5,7)]
print(json.dumps({'status':'PASS','arithmetic':'exact finite-field/integer','total_assertions':sum(checks.values()),'assertions_by_scope':dict(checks),'cases':results,'limits':'Finite controls supplement the universal proof; no full group-algebra isomorphism search or source resolution.'},indent=2,sort_keys=True))

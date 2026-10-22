#!/usr/bin/env python3
"""Independent exact controls. Finite tests do not prove generic Tate images."""
import json
from collections import Counter
from itertools import combinations, permutations, product

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def ring_tables(n):
    q=n*n
    add=[[((a%n+b%n)%n)+n*((a//n+b//n)%n) for b in range(q)] for a in range(q)]
    mul=[[((a%n*(b%n)+(a//n)*(b//n))%n)+n*((a%n*(b//n)+(a//n)*(b%n)-(a//n)*(b//n))%n) for b in range(q)] for a in range(q)]
    neg=[((-a%n)%n)+n*((-(a//n))%n) for a in range(q)]
    return add,mul,neg

def group_control(n):
    add,mul,neg=ring_tables(n)
    c=add[2%n][n]
    minus_c=neg[c]
    # Right multiplication by the two elementary generators needs only four additions.
    cmul=mul[minus_c]
    I=(1,0,0,1)
    seen={I}; queue=[I]
    for a,b,c,d in queue:
        for g in ((a,add[a][b],c,add[c][d]),(add[a][cmul[b]],b,add[c][cmul[d]],d)):
            if g not in seen:
                seen.add(g); queue.append(g)
    for a,b,c,d in seen:
        require(add[mul[a][d]][neg[mul[b][c]]]==1, ('determinant',n,a,b,c,d))
    def mm(A,B):
        a,b,c,d=A;e,f,g,h=B
        return (add[mul[a][e]][mul[b][g]],add[mul[a][f]][mul[b][h]],add[mul[c][e]][mul[d][g]],add[mul[c][f]][mul[d][h]])
    def power(A,e):
        B=I
        while e:
            if e&1:B=mm(B,A)
            A=mm(A,A);e//=2
        return B
    U=(1,1,0,1);V=(1,0,minus_c,1)
    require(power(mm(U,V),5)==(neg[1],0,0,neg[1]),('fifth power',n))
    result={'modulus':n,'order':len(seen),'determinants_checked':len(seen)}
    if n==3:
        counts=Counter()
        for g in seen:
            for e in (1,2,3,4,5,6,10):
                if power(g,e)==I:
                    counts[e]+=1;break
            else:raise RuntimeError('Unexpected order')
        result['element_order_counts']=dict(sorted(counts.items()))
        require(counts=={1:1,2:1,3:20,4:30,5:24,6:20,10:24},'Order fingerprint')
    expected={2:10,3:120,4:320,5:15000,7:117600,9:87480,11:1742400}
    require(len(seen)==expected[n],('group order',n,len(seen)))
    if n==11:
        roots=[x for x in range(11) if (x*x+x-1)%11==0]
        projections=[]
        for r in roots:
            values={tuple((x%11+(x//11)*r)%11 for x in g) for g in seen}
            projections.append(len(values))
        require(projections==[1320,1320],('split projections',projections))
        require(len(seen)==1320**2,'split product')
        result.update(split_roots=roots,projection_orders=projections,squared_infinity_traces=[r*r%11 for r in roots])
    return result

# Laurent polynomials in u with coefficients in Z[zeta_5]. The coefficient basis
# is 1,z,z^2,z^3; z^4=-1-z-z^2-z^3. No approximate algebraic roots are used.
def normalize(d):
    out={}
    for (u,z),c in d.items():
        z%=5
        for k,m in ([(z,1)] if z<4 else [(i,-1) for i in range(4)]):
            out[u,k]=out.get((u,k),0)+c*m
    return {k:v for k,v in out.items() if v}

def plus(a,b):
    d=a.copy()
    for k,v in b.items():d[k]=d.get(k,0)+v
    return normalize(d)

def scale(a,c):return normalize({k:v*c for k,v in a.items()})

def times(a,b):
    d={}
    for (u,z),c in a.items():
        for (v,w),e in b.items():d[u+v,z+w]=d.get((u+v,z+w),0)+c*e
    return normalize(d)

ONE={(0,0):1}
def powpoly(a,n):
    r=ONE
    for _ in range(n):r=times(r,a)
    return r

def matchings(items):
    if not items:
        yield []
        return
    a,*rest=items
    for i,b in enumerate(rest):
        for m in matchings(rest[:i]+rest[i+1:]):yield [(a,b)]+m

def polynomial_controls():
    u={(1,0):1};iu={(-1,0):1}; x=plus(u,iu)
    f=plus(plus(powpoly(x,5),scale(powpoly(x,3),-5)),scale(x,5))
    require(f==plus(powpoly(u,5),powpoly(iu,5)),'Chebyshev polynomial identity')
    roots=[normalize({(1,i):1,(-1,-i):1}) for i in range(5)]
    diff={}
    for i,j in combinations(range(6),2):
        d=plus(roots[i],scale(roots[j],-1)) if j<5 else ONE
        diff[i,j]=powpoly(d,2)
    def factors(edges):
        p=ONE
        for a,b in edges:p=times(p,diff[tuple(sorted((a,b)))])
        return p
    A={};B={};C={}
    am=list(matchings(list(range(6))))
    require(len(am)==15,'A matching count')
    for m in am:A=plus(A,factors(m))
    partitions=[]
    for other in combinations(range(1,6),2):
        left=(0,)+other;right=tuple(x for x in range(6) if x not in left)
        partitions.append((left,right))
    require(len(partitions)==10,'B partition count')
    for left,right in partitions:
        base=list(combinations(left,2))+list(combinations(right,2))
        B=plus(B,factors(base))
        for order in permutations(right):C=plus(C,factors(base+list(zip(left,order))))
    D=factors(list(combinations(range(6),2)))
    t=scale(plus(powpoly(u,5),powpoly(iu,5)),-1)
    t2=powpoly(t,2)
    require(A==scale(ONE,350),('Igusa A',A))
    require(B==scale(ONE,2500),('Igusa B',B))
    require(C==plus(scale(ONE,295000),scale(t2,-11250)),('Igusa C',C))
    require(D==scale(powpoly(plus(t2,scale(ONE,-4)),2),3125),('Igusa D/discriminant',D))
    return {'coefficient_ring':'Z[zeta_5][u,u^-1]','chebyshev_identity':True,'A':350,'B':2500,'C':'295000-11250*t^2','D':'3125*(t^2-4)^2','matching_counts':[15,10,60]}

def arbitrary_lift_controls(p):
    # All determinant-one lifts of I+E12 modulo p^2, over the prime field.
    # A lift has p^3 choices. The proof, not these finite tests, covers extensions.
    n=p*p;I=(1,0,0,1)
    def mm(A,B):
        a,b,c,d=A;e,f,g,h=B
        return ((a*e+b*g)%n,(a*f+b*h)%n,(c*e+d*g)%n,(c*f+d*h)%n)
    good=bad=0;example=None
    for a,b,d in product(range(p),repeat=3):
        c=(a+d)%p
        h=(1+p*a,1+p*b,p*c,1+p*d)
        require((h[0]*h[3]-h[1]*h[2])%n==1,'Lift determinant')
        hp=I
        for _ in range(p):hp=mm(hp,h)
        if hp==(1,p,0,1):good+=1
        else:
            bad+=1
            if example is None:example={'lift':h,'power':hp}
    require(bad==0 if p>=5 else bad>0,('lifting range',p,good,bad))
    return {'p':p,'lifts':p**3,'expected_power_count':good,'other_power_count':bad,'counterexample':example}

def group_actions():
    automorphisms=[(a,b,e) for a in (1,2,3,4) for b in range(5) for e in (1,-1)]
    images={tuple((e*a*i+e*b)%5 for i in range(5)) for a,b,e in automorphisms}
    kernel=[g for g in automorphisms if tuple((g[2]*g[0]*i+g[2]*g[1])%5 for i in range(5))==tuple(range(5))]
    require(len(images)==20 and kernel==[(1,0,1),(4,0,-1)],'Chebyshev permutation image/kernel')
    # Quotient F2^5/<ones>, canonical representative min(v,v xor 31).
    def act(g,v):
        out=sum(((v>>i)&1)<<g[i] for i in range(5))
        return min(out,out^31)
    vectors=sorted({min(v,v^31) for v in range(32)})
    require(len({tuple(act(g,v) for v in vectors) for g in permutations(range(5))})==120,'Faithful S5 action')
    cycle=(1,2,3,4,0)
    fixed=[v for v in vectors if act(cycle,v)==v]
    require(fixed==[0],('generic invariant space',fixed))
    special=(0,2,3,4,1)
    specialfixed=[v for v in vectors if act(special,v)==v]
    require(len(specialfixed)==2,('special invariant space',specialfixed))
    return {'automorphisms':40,'root_image':20,'kernel':kernel,'two_torsion_action_faithful':True,'generic_fixed_space_dimension':0,'C4_special_fixed_space_dimension':1}

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--split',action='store_true');args=parser.parse_args()
    result={'scope':'Exact algebraic identities and finite matrix controls; no sampled generic-image proof.','polynomial_controls':polynomial_controls(),'group_actions':group_actions(),'arbitrary_lifts':[arbitrary_lift_controls(p) for p in (3,5,7)],'matrix_groups':[group_control(n) for n in ([2,3,4,5,7,9,11] if args.split else [2,3,4,5,7,9])]}
    print(json.dumps(result,indent=2,sort_keys=True))

#!/usr/bin/env python3
"""Fresh exact adversarial controls with no candidate imports or reads."""
from fractions import Fraction as Q
from itertools import combinations,product
import json,random
from source_first_counts import matrix,subset_c4,direct,compositions

EDGES=tuple(combinations(range(4),2))
MISS=(((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2)))
def event(values):
    out=Q(0)
    for absent in MISS:
        term=Q(1)
        for e,v in zip(EDGES,values): term*=1-v if e in absent else v
        out+=term
    return out

def direct_event(w,a):
    total=Q(0)
    for indices in product(range(len(a)),repeat=4):
        values=[w[indices[i]][indices[j]] for i,j in EDGES]
        total+=event(values)*a[indices[0]]*a[indices[1]]*a[indices[2]]*a[indices[3]]
    return total

def sign_radical(c,b,D):
    if not b or not D:return (c>0)-(c<0)
    if c>=0 and b>0:return 1
    if c<=0 and b<0:return -1
    v=c*c-b*b*D
    if c>0:return (v>0)-(v<0)
    return (v<0)-(v>0)

def mul(v,w,D):return (v[0]*w[0]+v[1]*w[1]*D,v[0]*w[1]+v[1]*w[0])
def power(v,n,D):
    out=(Q(1),Q(0))
    for _ in range(n):out=mul(out,v,D)
    return out
def profile(x):
    if x==1:return (Q(0),Q(0),Q(0))
    q=1-x;r=q.denominator//q.numerator;D=((r+1)*q-1)/r
    a=(Q(1,r+1),Q(1,r+1));b=(Q(1,r+1),Q(-r,r+1))
    a4=power(a,4,D);b4=power(b,4,D)
    return (3*(q*q-r*a4[0]-b4[0]),-3*(r*a4[1]+b4[1]),D)
def bounded(x,c):
    A,B,D=profile(x)
    assert sign_radical(A-c,B,D)>=0,(x,c,A,B,D)

def node(kind,children,weights):
    assert sum(weights)==1 and all(w>=0 for w in weights)
    if kind=='union':
        p=sum(w*w*x[0] for w,x in zip(weights,children));c=sum(w**4*x[1] for w,x in zip(weights,children))
    else:
        p=1-sum(w*w*(1-x[0]) for w,x in zip(weights,children))
        c=sum(w**4*x[1] for w,x in zip(weights,children))+6*sum(weights[i]**2*weights[j]**2*(1-children[i][0])*(1-children[j][0]) for i,j in combinations(range(len(weights)),2))
    bounded(p,c)
    if kind=='union' and Q(1,2)<p<1 and max(weights)<1:
        w=max(weights);gap=Q(3,8)*(1-w)*(1-p)**2*(4-(1-p));bounded(p,c+gap)
    return p,c

def components(w,vertices,complement=False):
    todo=set(vertices);parts=[]
    while todo:
        start=min(todo);seen={start};stack=[start];todo.remove(start)
        while stack:
            v=stack.pop()
            nbr=[u for u in sorted(todo) if bool(w[v][u])!=complement]
            for u in nbr:todo.remove(u);seen.add(u);stack.append(u)
        parts.append(sorted(seen))
    return parts
def recursive_cograph(w,V):
    if len(V)<=1:return True
    parts=components(w,V)
    if len(parts)>1:return all(recursive_cograph(w,B) for B in parts)
    parts=components(w,V,True)
    return len(parts)>1 and all(recursive_cograph(w,B) for B in parts)
def p4free(w):
    for V in combinations(range(len(w)),4):
        degrees=sorted(sum(w[i][j] for j in V) for i in V)
        if degrees==[1,1,2,2]:return False
    return True
def recursive_density(w,V,a):
    if len(V)==1:return Q(0),Q(0)
    parts=components(w,V);kind='union'
    if len(parts)==1:parts=components(w,V,True);kind='join'
    assert len(parts)>1
    masses=[sum(a[v] for v in B) for B in parts];total=sum(masses)
    children=[recursive_density(w,B,a) for B in parts]
    return node(kind,children,[m/total for m in masses])

def main():
    counts={}
    # All possible four-vertex graphs distinguish matching inequality from induced counts.
    for mask in range(64):
        values=[Q((mask>>k)&1) for k in range(6)]
        present=sum(all(values[EDGES.index(e)]==1 for e in matching) for matching in MISS)
        assert event(values)<=Q(present,2)
    counts['four_vertex_matching_cases']=64
    # Conditional edge kernel is enumerated independently through the entire induced event.
    kernels=0
    for masses in compositions(7):
        a=[Q(k,7) for k in masses];q=sum(x*x for x in a)
        for i,j in product(range(len(a)),repeat=2):
            k=Q(0)
            for u,v in product(range(len(a)),repeat=2):
                idx=(i,j,u,v);vals=[Q(int(idx[e[0]]!=idx[e[1]])) for e in EDGES]
                vals[0]=Q(1);plus=event(vals);vals[0]=Q(0);minus=event(vals)
                k+=a[u]*a[v]*(plus-minus)
            expected=-(q-a[i]**2) if i==j else (a[i]+a[j])**2-q
            assert k==expected
            kernels+=1
    counts['conditional_kernel_cases']=kernels
    # Exhaustive recursive/P4 recognition plus unequal positive weights through order five.
    cographs=0;weighted=0
    for n in range(1,6):
        for mask in range(1<<(n*(n-1)//2)):
            w=matrix(n,mask);rec=recursive_cograph(w,list(range(n)))
            assert rec==p4free(w)
            if rec:
                cographs+=1;a=[Q(i+1,n*(n+1)//2) for i in range(n)]
                p,c=recursive_density(w,list(range(n)),a)
                pd,cd=direct(w,a)
                assert (p,c)==(pd,cd)
                if n<=4:assert c==direct_event(w,a)
                weighted+=1
    counts['exhaustive_cographs_and_weighted_counts']=cographs
    # Arbitrary depth, zero children and deterministic p=1 endpoint children.
    for depth in (1,2,3,8,32,128,257):
        value=(Q(0),Q(0))
        for level in range(depth):
            value=node('join' if level%2 else 'union',[(Q(0),Q(0)),value,(Q(1),Q(0))],[Q(1,3),Q(2,3),Q(0)])
    counts['maximum_cotree_depth']=257
    endpoint_cases=0
    for denom in range(2,24):
        for num in range(denom+1):
            weights=[Q(num,denom),1-Q(num,denom)]
            for kind in ('union','join'):
                node(kind,[(Q(1),Q(0)),(Q(0),Q(0))],weights);endpoint_cases+=1
    counts['endpoint_zero_child_cases']=endpoint_cases
    # Exact countable geometric part tails: merged tail and original retained moments.
    for length in (1,2,4,8,16,64):
        a=[Q(1,2**i) for i in range(1,length+1)]+[Q(1,2**length)]
        s2=sum(x*x for x in a);s4=sum(x**4 for x in a);bounded(1-s2,3*(s2*s2-s4))
    counts['countable_geometric_tail_controls']=6
    # Randomized only in corpus selection, with fixed seed and exact arithmetic.
    rng=random.Random(374003)
    joins=0
    for _ in range(32):
        masses=[Q(rng.randrange(1,7)) for _ in range(3)];total=sum(masses);masses=[x/total for x in masses]
        w=[[Q(rng.randrange(0,3),4) for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(i):w[i][j]=w[j][i]
        p,c=direct(w,[Q(1,3)]*3);assert p<=Q(1,2)
        value=node('join',[(p,c),(Q(0),Q(0)),(Q(1,2),Q(3,8))],masses)
        joins+=1
    counts['fractional_low_density_internal_join_cases']=joins
    # Fresh fixed-space tying surgeries and derivatives in rational families.
    ties=0
    for r in range(2,7):
        for denom in (2,3,5):
            ratio=Q(1,denom);a=1/(r+ratio);b=ratio*a
            for step in (Q(1,7),Q(1,3),Q(3,4)):
                s=(a-b)*step;u=a-s;e=b*s/u;z=s-e
                masses=[a]*(r-1)+[u,e,z,b]
                labels=list(range(r-1))+[r-1]*3+[r]
                base=[[Q(int(i!=j)) for j in labels] for i in labels]
                after=[row[:] for row in base];U=r-1;E=r;Z=r+1;B=r+2
                after[U][E]=after[E][U]=Q(1)
                for child in (E,Z):after[B][child]=after[child][B]=Q(0)
                p0,c0=direct(base,masses);p1,c1=direct(after,masses)
                assert (p0,c0)==(p1,c1);T=sum(masses[i]*masses[j]*abs(after[i][j]-base[i][j]) for i,j in product(range(len(masses)),repeat=2))
                assert T==4*b*s
                q=1-p0;variation=Q(0)
                for i,j in product(range(len(masses)),repeat=2):
                    K=-(q-(a if labels[i]<r else b)**2) if labels[i]==labels[j] else ((a if labels[i]<r else b)+(a if labels[j]<r else b))**2-q
                    variation+=6*masses[i]*masses[j]*(after[i][j]-base[i][j])*K
                assert variation==-3*b*(2*a+b)*T
                ties+=1
    counts['fixed_space_tie_cases']=ties
    # Nonconstant-within-original-part fractional directions, including overlapping edges.
    local=0
    for r in range(2,7):
        a=Q(5,5*r+1);b=Q(1,5*r+1)
        masses=[a/2,a/2]+[a]*(r-1)+[b]
        labels=[0,0]+list(range(1,r))+[r]
        base=[[Q(int(i!=j)) for j in labels] for i in labels]
        radius=b*(2*a+b)/114
        amplitude=radius/(2*max(Q(1),a/(4*b)))
        after=[row[:] for row in base]
        after[0][0]+=amplitude
        after[0][-1]=after[-1][0]=1-amplitude*a/(4*b)
        p0,c0=direct(base,masses);p1,c1=direct(after,masses)
        assert p0==p1
        h=[[after[i][j]-base[i][j] for j in range(len(masses))] for i in range(len(masses))]
        T=sum(masses[i]*masses[j]*abs(h[i][j]) for i,j in product(range(len(masses)),repeat=2))
        eta=max(abs(h[i][j]) for i,j in product(range(len(masses)),repeat=2))
        assert eta<=radius and c1<=c0-Q(3,2)*b*(2*a+b)*T
        variation=Q(0);q=1-p0
        for i,j in product(range(len(masses)),repeat=2):
            K=-(q-(a if labels[i]<r else b)**2) if labels[i]==labels[j] else ((a if labels[i]<r else b)+(a if labels[j]<r else b))**2-q
            variation+=6*masses[i]*masses[j]*h[i][j]*K
        assert abs(c1-c0-variation)<=171*eta*T
        assert c1==direct_event(after,masses)
        local+=1
    counts['nonconstant_small_amplitude_controls']=local
    print(json.dumps({'status':'PASS','counts':counts,'scope':'exact finite falsification controls supplement universal proof audit'},sort_keys=True))

if __name__=='__main__':main()

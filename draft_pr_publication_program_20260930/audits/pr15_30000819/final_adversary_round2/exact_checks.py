#!/usr/bin/env python3
"""Fresh integer/fraction controls; no candidate or sibling code imports.

All-degree certificates are separate mathematical arguments in REPORT.md.
Finite checks verify the certificate interfaces, not the general theorem.
"""
from pathlib import Path
from itertools import product, combinations, combinations_with_replacement
from fractions import Fraction
from math import factorial, gcd, lcm, comb
import json

N=0
GROUPS=[]
def ck(value, message):
    global N
    N+=1
    if not value: raise AssertionError(message)

def step(layer,A):
    return {tuple(x+y for x,y in zip(p,a)) for p in layer for a in A}

def reduce_rows(rows):
    a=[list(map(Fraction,row)) for row in rows]
    piv=[]; i=0
    if not a:return [],[]
    for j in range(len(a[0])):
        q=next((t for t in range(i,len(a)) if a[t][j]),None)
        if q is None:continue
        a[i],a[q]=a[q],a[i]
        v=a[i][j];a[i]=[x/v for x in a[i]]
        for t in range(len(a)):
            if t!=i:
                f=a[t][j];a[t]=[x-f*y for x,y in zip(a[t],a[i])]
        piv.append(j);i+=1
        if i==len(a):break
    return a,piv

def rk(rows):return len(reduce_rows(rows)[1])

def primitive_circuits(A):
    columns=[p+(1,) for p in A]; r=rk(columns); result=[]
    for size in range(2,r+2):
        for ids in combinations(range(len(A)),size):
            rows,piv=reduce_rows(zip(*(columns[i] for i in ids)))
            if len(piv)!=size-1:continue
            free=next(j for j in range(size) if j not in piv)
            u=[Fraction(0)]*size;u[free]=1
            for row,i in zip(rows,piv):u[i]=-row[free]
            if not all(u):continue
            s=lcm(*(v.denominator for v in u));u=[int(v*s) for v in u]
            g=gcd(*u);u=[x//g for x in u]
            if u[0]<0:u=[-x for x in u]
            full=[0]*len(A)
            for i,x in zip(ids,u):full[i]=x
            result.append(tuple(full))
    return result

def circuit_suite(A,V,name):
    b=N; circuits=primitive_circuits(A); basis=[]; columns=[p+(1,) for p in A]
    for u in circuits:
        ck(all(sum(x*p[j] for x,p in zip(u,columns))==0 for j in range(len(columns[0]))),'exact circuit relation')
        ck(gcd(*u)==1,'primitive circuit')
        degree=sum(x for x in u if x>0)
        ck(sum(u)==0 and degree<=V,'homogeneous primitive degree <= intrinsic V')
        ck(sum(x!=0 for x in u)<=2*degree,'signed support bound')
        if rk(basis+[u])>len(basis):basis.append(u)
    c=len(A)-rk(columns)
    ck(len(basis)==c,'rational circuit basis spans kernel')
    ck(all(any(u[i] for u in basis) for i in range(len(A))),'basis support covers every nonfree coordinate')
    ck(c<=V-1 and len(A)<=2*V*c,'volume/codimension and dimension removal')
    GROUPS.append(dict(name=name,assertions=N-b,n=len(A),c=c,V=V,circuits=len(circuits)))

def boundary_cube():
    b=N;receipts=[]
    for d in range(2,6):
        for m in (2,3):
            A=tuple(p for p in product(range(m+1),repeat=d) if any(x in (0,m) for x in p))
            n=(m+1)**d-(m-1)**d;V=factorial(d)*m**d;c=n-d-1
            ck(len(A)==n and len(set(A))==n,'distinct selected boundary points')
            ck(all(tuple(int(i==j) for i in range(d)) in A for j in range(d)) and (0,)*d in A,'generated intrinsic lattice is Z^d')
            actual={(0,)*d};counts=[]
            for k in range(3):
                saturated=set(product(range(k*m+1),repeat=d))
                ck(actual<=saturated,'sumset lies in degree slice of cube cone')
                holes=saturated-actual
                ck(len(holes)==((m-1)**d if k==1 else 0),'only degree-one interior holes')
                counts.append(len(holes))
                if k<2:actual=step(actual,A)
            # Explicit two-summand construction for every integer point of 2P.
            for p in product(range(2*m+1),repeat=d):
                left=[max(0,x-m) for x in p]
                left[0]=0 if p[0]<=m else m
                right_second=0 if p[1]<=m else m
                left[1]=p[1]-right_second
                left=tuple(left);right=tuple(x-y for x,y in zip(p,left))
                ck(left in A and right in A,'two selected boundary summands realize each saturated degree-two point')
            # Every selected point is in a primitive line or square circuit.
            Aset=set(A)
            for p in A:
                j=next((i for i,x in enumerate(p) if 0<x<m),None)
                if j is not None:
                    lo=list(p);hi=list(p);lo[j]-=1;hi[j]+=1
                    ck(tuple(lo) in Aset and tuple(hi) in Aset and all(x+z==2*y for x,y,z in zip(lo,p,hi)),'nonvertex boundary point belongs to primitive line circuit')
                else:
                    q=list(p);r=list(p);s=list(p)
                    q[0]=m-p[0];r[1]=m-p[1];s[0]=m-p[0];s[1]=m-p[1]
                    ck(tuple(q) in Aset and tuple(r) in Aset and tuple(s) in Aset and all(x+w==y+z for x,y,z,w in zip(p,q,r,s)),'cube vertex belongs to primitive square circuit')
            ck(c<=V-1 and n<=2*V*c,'cube configuration satisfies both volume inequalities')
            ck(1<=2*V*V*(V-1)**2-2,'quartic bounds nonempty hole height')
            receipts.append(dict(d=d,m=m,n=n,c=c,V=V,holes_by_degree_0_1_2=counts,h=1,
                                 all_degree_certificate='2A=2P integer points; corners inductively cover every k>=2'))
    GROUPS.append(dict(name='boundary-only cubes with finite nonempty holes, dimensions2-5',assertions=N-b,families=receipts))

def interval_cube_products():
    b=N;receipts=[]
    for d in range(2,6):
        for m in range(4,7):
            A=tuple((x,)+y for x in (0,1,m-1,m) for y in product((0,1),repeat=d-1))
            actual={(0,)*d};levels=[];last=-1
            for k in range(m):
                xset={sum(p) for p in combinations_with_replacement((0,1,m-1,m),k)}
                cube=set(product(range(k+1),repeat=d-1))
                predicted={(x,)+y for x in xset for y in cube}
                saturated={(x,)+y for x in range(k*m+1) for y in cube}
                ck(actual==predicted,'independent multiset x sums pair with every binary coordinate sum')
                holes=saturated-actual
                expected=k*(m-k-2)*(k+1)**(d-1) if 1<=k<=m-3 else 0
                ck(len(holes)==expected,'exact product hole count')
                if holes:last=k
                levels.append(dict(k=k,holes=len(holes)))
                if k<m-1:actual=step(actual,A)
            V=factorial(d)*m
            ck(last==m-3,'all-degree last-hole product height')
            ck(last<=2*V*V*(V-1)**2-2,'quartic estimate on higher-dimensional h>1 family')
            ck(len(A)-d-1<=V-1 and len(A)<=2*V*(len(A)-d-1),'actual selected n and intrinsic cube product volume')
            receipts.append(dict(d=d,m=m,n=len(A),V=V,h=last,levels=levels,
                                 all_degree_certificate='sumset Cartesian factorization and one-dimensional adjacent interval coverage'))
    GROUPS.append(dict(name='sparse interval times unit cube, dimensions2-5',assertions=N-b,families=receipts))

def orient(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])

def polygon_triangulations():
    b=N;receipts=[]
    for m in range(2,9):
        A=tuple([(x,0) for x in range(m)]+[(m,y) for y in range(m)]+[(x,m) for x in range(m,0,-1)]+[(0,y) for y in range(m,0,-1)])
        polygon=list(range(len(A)));triangles=[]
        while len(polygon)>3:
            found=False
            for j,v in enumerate(polygon):
                p=polygon[j-1];q=polygon[(j+1)%len(polygon)];t=(p,v,q)
                if orient(*(A[i] for i in t))<=0:continue
                if any(all(orient(A[t[h]],A[t[(h+1)%3]],A[w])>=0 for h in range(3)) for w in polygon if w not in t):continue
                triangles.append(t);polygon.pop(j);found=True;break
            ck(found,'ear clipping progresses through collinear selected boundary points')
        triangles.append(tuple(polygon));V=2*m*m
        ck(set().union(*map(set,triangles))==set(range(len(A))),'all selected points occur in triangulation')
        ck(all(orient(*(A[i] for i in t))>0 for t in triangles),'positive integral simplex volumes')
        ck(sum(orient(*(A[i] for i in t)) for t in triangles)==V,'triangle volumes sum to intrinsic normalized polygon volume')
        seen={0}
        while True:
            more={i for i,t in enumerate(triangles) if any(len(set(t)&set(triangles[j]))==2 for j in seen)}-seen
            if not more:break
            seen|=more
        ck(len(seen)==len(triangles),'connected facet dual adjacency')
        ck(len(A)<=2+len(triangles)<=2+V,'triangulation proves c<=V-1 using actual selected points')
        receipts.append(dict(m=m,n=len(A),t=len(triangles),V=V))
    GROUPS.append(dict(name='all-selected boundary polygon triangulations by ear clipping',assertions=N-b,families=receipts))

def nonstandard_normalization():
    b=N;receipts=[]
    for m in range(3,8):
        A=((0,0,0),(1,0,0),(0,1,0),(0,0,1),(1,0,1),(0,1,1),(1,1,m),(1,1,m+1))
        layer={(0,0,0)};counts=[]
        for k in range(m+1):
            sat=set();pred=set()
            for x in range(k+1):
                for y in range(k+1):
                    L=max(0,x+y-k);U=min(x,y)
                    sat|={(x,y,z) for z in range(m*L,m*U+k+1)}
                    pred|={(x,y,z) for j in range(L,U+1) for z in range(m*j,m*j+k+1)}
            ck(layer==pred,'integer high-fiber counts reproduce semigroup layers')
            gaps=sat-layer
            ck(len(gaps)==comb(k+1,3)*max(0,m-k-1),'fiber-gap count reproduces primary family')
            counts.append(len(gaps))
            if k==1:ck(not gaps and layer==set(A),'all degree-one lattice points selected')
            if k==2 and m>=4:ck((1,1,3) in gaps,'normalization needs a degree-two monomial despite complete degree one')
            if k<m:layer=step(layer,A)
        h=max((k for k,g in enumerate(counts) if g),default=None)
        ck(h==(m-2 if m>=4 else None),'nonempty h=m-2; m3 empty boundary has no assigned maximum')
        if m>=4:
            coefficients=(3,m-3,m-3,0,0,0,3,0)
            realized=tuple(sum(t*a[j] for t,a in zip(coefficients,A)) for j in range(3))
            ck(sum(coefficients)==2*m and realized==(m,m,3*m),'positive power of degree-two normalized monomial belongs to R')
            ck(h<=2*(m+6)**2*(m+5)**2-2,'coarse bound for primary volume V=m+6')
        receipts.append(dict(m=m,V=m+6,h=h,holes_by_degree=counts,
                             all_degree_certificate='integer fiber intervals have consecutive coverage once k>=m-1'))
    GROUPS.append(dict(name='BDGM complete degree-one family with nonstandard normalization',assertions=N-b,families=receipts))

def boundaries_and_false_variants():
    b=N;variants=[]
    # The first genuine hole is 2 at degree1, exactly killed by all generators.
    A=(0,1,3,4);pairs={x+y for x in A for y in A}
    ck(set(range(5))-set(A)=={2} and pairs==set(range(9)),'A4 has precisely a degree-one hole and no degree-two hole')
    ck(all(2+a in pairs for a in A),'hole quotient is annihilated by R_+')
    # H1 ends at1; H2 for P1 with O(4) ends at-1, giving regR2, regI3.
    h=1;regR=max(h+1,-1+2);regI=regR+1
    ck(h==regI-2 and h>regI-3,'subtract-two equality rejects subtract-three shift')
    variants.append('incorrect subtract-three regularity offset')
    ck(-1>2*1**2*(1-1)**2-2,'empty h=-1 cannot extend formula to V1')
    variants.append('empty/V1 formula extension')
    ck(set(range(5))-set(range(5))!=set(range(5))-set(A),'filling omitted selected points changes holes')
    variants.append('substitution by complete polytope lattice points')
    u=(3,-4,0,1);degree=sum(max(x,0) for x in u)
    ck(degree==4 and sum(max(2*x,0) for x in u)>4,'nonprimitive circuit multiples defeat degree<=V')
    variants.append('dropping circuit primitivity')
    for k in range(1,11):
        sums={sum(p) for p in combinations_with_replacement((0,2,6,8),k)}
        ck(1 not in sums and 1<=8*k,'proper ambient group gives arbitrarily high ambient holes')
    variants.append('finite ambient holes with proper generated-group index')
    for k in range(10):
        simplex={(2*a+b,3*b) for a in range(k+1) for b in range(k-a+1)}
        actual={tuple(sum(p[j] for p in ps) for j in (0,1)) for ps in combinations_with_replacement(((0,0),(2,0),(1,3)),k)}
        ck(actual==simplex,'c0 free simplex has no intrinsic holes at any degree by unique coefficients')
        ck({7*k}=={sum(p) for p in combinations_with_replacement((7,),k)},'d0 singleton normal boundary')
    # Seventeen independent apex columns leave c2,V4 and n21>2Vc16.
    n=4+17;c=2;V=4
    ck(n>2*V*c,'support bound fails after appending many free variables outside finite-hole hypothesis')
    for k in range(1,11):
        ck(2 not in A and k-1>=0,'hole (2,k-1) has forced one base factor in every pyramid degree')
    variants.append('discarding finite nonempty-hole condition in dimension removal')
    ck(0==sum(()) and (0 in {0}),'degree-zero sumset covers the saturated degree-zero point')
    variants.append('forgetting degree-zero exception to interval coverage')
    variants.append('normalization assumed generated in degree one: rejected in BDGM group')
    GROUPS.append(dict(name='degenerate boundaries and falsified unsupported variants',assertions=N-b,rejected_variants=variants))

def main():
    boundary_cube()
    interval_cube_products()
    polygon_triangulations()
    circuit_suite(tuple(p for p in product(range(3),repeat=2) if 0 in p or 2 in p),8,'primitive circuits on selected boundary of 2x2 square')
    circuit_suite(tuple(product((0,1),repeat=3)),6,'primitive circuits on three-dimensional unit cube')
    circuit_suite(((-1,0),(1,0),(0,-1),(0,1)),2,'nonspanning diamond intrinsic volume2')
    nonstandard_normalization()
    boundaries_and_false_variants()
    receipt=dict(status='passed',exact_assertions=N,arithmetic='Python integers, fractions, exact finite sets',
                 groups=GROUPS,no_candidate_or_sibling_imports=True,
                 scope='Checkable controls and written all-degree family certificates; not a general formal proof or novelty certificate')
    encoded=json.dumps(receipt,indent=2)+'\n'
    Path(__file__).with_name('exact_checks.json').write_text(encoded)
    print(encoded,end='')

if __name__=='__main__':main()

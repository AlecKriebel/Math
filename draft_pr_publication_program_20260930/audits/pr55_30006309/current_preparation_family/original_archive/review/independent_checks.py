#!/usr/bin/env python3
"""Independent exact regular-lower-hull diagnostics for the product comparison.
Unlike the author checker, triangulations are generated from exact lower
supporting hyperplanes; they are not supplied as staircase triangulations.
Standard library only. Finite diagnostics do not replace GKZ or the proof.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
from math import comb, gcd
import json
import random

counts = Counter()
rng = random.Random(30006309)
def test(condition, category):
    assert condition, category
    counts[category] += 1

def inverse(matrix):
    n=len(matrix)
    a=[[F(x) for x in row]+[F(int(i==j)) for j in range(n)]
       for i,row in enumerate(matrix)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if a[i][j]),None)
        if pivot is None: return None
        a[j],a[pivot]=a[pivot],a[j]
        c=a[j][j]
        a[j]=[x/c for x in a[j]]
        for i in range(n):
            if i!=j and a[i][j]:
                c=a[i][j]
                a[i]=[u-c*v for u,v in zip(a[i],a[j])]
    return [row[n:] for row in a]

def determinant(a):
    a=[list(row) for row in a]
    n=len(a)
    if not n:return 1
    sign,prev=1,1
    for k in range(n-1):
        pivot=next((i for i in range(k,n) if a[i][k]),None)
        if pivot is None:return 0
        if pivot!=k:
            a[k],a[pivot]=a[pivot],a[k]
            sign=-sign
        pv=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                numerator=a[i][j]*pv-a[i][k]*a[k][j]
                assert numerator%prev==0
                a[i][j]=numerator//prev
        for i in range(k+1,n):a[i][k]=0
        prev=pv
    return sign*a[-1][-1]

@lru_cache(None)
def lattice_volume(vertices):
    k=len(vertices)-1
    if k==0:return 1
    edges=[[v[j]-vertices[0][j] for j in range(len(v))]
           for v in vertices[1:]]
    answer=0
    for cols in combinations(range(len(vertices[0])),k):
        answer=gcd(answer,abs(determinant([[row[j] for j in cols] for row in edges])))
    return answer

class Hull:
    def __init__(self,A):
        self.A=tuple(A)
        self.dim=len(A[0])
        self.bases=[]
        for S in combinations(range(len(A)),self.dim+1):
            inv=inverse([[1,*A[i]] for i in S])
            if inv is None:continue
            # Rows express evaluation at each point as a linear combination
            # of values at the candidate affine simplex.
            evals=[]
            for point in A:
                row=[1,*point]
                evals.append(tuple(sum(F(row[k])*inv[k][j] for k in range(self.dim+1))
                                   for j in range(self.dim+1)))
            self.bases.append((S,tuple(evals)))
    def triangulate(self,w):
        tops=[]
        for S,ev in self.bases:
            ws=[w[i] for i in S]
            extra_equal=False
            valid=True
            for i,row in enumerate(ev):
                if i in S:continue
                gap=w[i]-sum(x*y for x,y in zip(row,ws))
                if gap<0:
                    valid=False
                    break
                if gap==0:extra_equal=True
            if valid:
                if extra_equal:return None
                tops.append(S)
        assert tops
        return tuple(tops)
    def generic(self,bias=None,scale=1):
        for _ in range(200):
            noise=[rng.randrange(-100000,100001) for _ in self.A]
            w=noise if bias is None else [scale*x+y for x,y in zip(bias,noise)]
            T=self.triangulate(w)
            if T is not None:return w,T
        raise AssertionError('generic height construction failed')

def square_face(vertices,lengths):
    return len(lengths)-sum(all(v[i]==0 for v in vertices)
                            or all(v[i]==L for v in vertices)
                            for i,L in enumerate(lengths))
def simplex_face(vertices,n,L):
    active=sum(all(v[i]==0 for v in vertices) for i in range(n))
    active+=all(sum(v)==L for v in vertices)
    return n-active
def simplex_vertices(n,L=1):
    return [(0,)*n]+[tuple(L*int(i==j) for i in range(n)) for j in range(n)]
def skeleton(tops):
    return {face for top in tops for k in range(1,len(top)+1)
            for face in combinations(top,k)}
def eta(A,T,face_dim):
    dim=len(A[0])
    out=[[0]*len(A) for _ in range(dim+1)]
    for face in skeleton(T):
        pts=tuple(A[i] for i in face)
        k=len(face)-1
        if face_dim(pts)!=k:continue
        volume=lattice_volume(pts)
        test(volume>0,'nonzero_massive_volume')
        for i in face:out[k][i]+=volume
    return out
def massive(E):
    d=len(E)-1
    return tuple(sum((-1)**(d-k)*E[k][i] for k in range(d+1))
                 for i in range(len(E[0])))
def project(v,n):
    return tuple(sum(v[i:i+n]) for i in range(0,len(v),n))
def dot(a,b):return sum(x*y for x,y in zip(a,b))

# Direct binomial finite-difference controls over larger n.
for n in range(1,31):
    for j in range(n+1):
        got=sum((-1)**(2*n-1-j-l)*comb(n,l+1)*comb(j+l+1,j+1) for l in range(n))
        test(got==(n if j==n else -1 if j==n-1 else 0),'finite_difference')

# Test the lower/minimum convention against an explicit quadratic discriminant.
A=[(0,),(1,),(2,)]
H=Hull(A)
for w,expected in [([0,1,0],(1,0,1)),([0,-1,0],(0,2,0))]:
    T=H.triangulate(w)
    m=massive(eta(A,T,lambda vs:square_face(vs,(2,))))
    test(m==expected,'explicit_discriminant_label')
    monomials=[(0,2,0),(1,0,1)] # b^2-4ac
    test(dot(w,m)==min(dot(w,v) for v in monomials),'minimum_sign')
    test(dot(w,m)!=max(dot(w,v) for v in monomials),'negative_sign_control')

summaries=[]
def run_family(name,A,n,base_face,random_samples,equal_samples):
    delta=simplex_vertices(n-1)
    B=[a+b for a in A for b in delta]
    HB,HA=Hull(B),Hull(A)
    def prod_face(vs):
        return base_face([v[:n] for v in vs])+simplex_face([v[n:] for v in vs],n-1,1)
    samples=[]
    for _ in range(random_samples):
        w,U=HB.generic()
        E=eta(B,U,prod_face)
        m=massive(E)
        test(all(x>=0 for x in m),'smooth_discriminant_nonnegative_exponents')
        samples.append((w,U,m,project(m,n)))
    equal=[]
    for _ in range(equal_samples):
        w,T=HA.generic()
        ET=eta(A,T,base_face)
        desired=tuple(n*ET[n][i]-ET[n-1][i] for i in range(len(A)))
        bias=[x for x in w for _ in delta]
        # Fix one generic perturbation direction; increase K until the
        # combinatorial refinement criterion holds. The support test below
        # is not used to select K.
        noise=[rng.randrange(-100000,100001) for _ in B]
        scale=10
        for _try in range(15):
            height=[scale*x+y for x,y in zip(bias,noise)]
            U=HB.triangulate(height)
            if U is not None and all(any(set(i//n for i in u)<=set(t) for t in T) for u in U):
                break
            scale*=10
        else:raise AssertionError('no regular refinement')
        test(all(any(set(i//n for i in u)<=set(t) for t in T) for u in U),'regular_product_refinement')
        used={i for t in T for i in t}
        test(all(i//n in used for u in U for i in u),'unused_points_stay_unused')
        EU=eta(B,U,prod_face)
        proj=[project(row,n) for row in EU]
        for k in range(2*n):
            expected=tuple(sum(comb(n,k-j+1)*comb(k+1,j+1)*ET[j][i]
                               for j in range(n+1) if 0<=k-j<n)
                           for i in range(len(A)))
            test(proj[k]==expected,'all_massive_levels')
        mu=massive(EU)
        test(project(mu,n)==desired,'projected_vector_identity')
        test(all(dot(bias,mu)<=dot(bias,m) for _,_,m,_ in samples),'equal_column_support_minimum')
        # Finite-fiber support identity against the sampled projected hull.
        test(dot(w,desired)==dot(bias,mu),'projection_pairing')
        equal.append((w,T,desired))
        samples.append((height,U,mu,project(mu,n)))
    # Independent normal-fan labels: a height's massive vector must minimize
    # the same functional over every other sampled regular massive vector.
    for w,U,m,pm in samples:
        test(all(dot(w,m)<=dot(w,other) for _,_,other,_ in samples),'generic_GKZ_minimizer')
    nonvertex=0
    if name=='unit_square':
        endpoints={(2,0,0,2),(0,2,2,0)}
        for _,_,_,pm in samples:
            test(pm[0]==pm[3] and pm[1]==pm[2] and pm[0]+pm[1]==2 and 0<=pm[0]<=2,
                 'square_projected_polytope')
            nonvertex+=pm not in endpoints
        test(nonvertex>0,'nonvertex_projections_exist')
        # An interior diagonal cannot be included in eta_{T,1}.
        T=equal[0][1]
        proper=equal[0][2]
        all_edges=eta(A,T,lambda vs:len(vs)-1)
        wrong=tuple(2*all_edges[2][i]-all_edges[1][i] for i in range(len(A)))
        test(wrong!=proper,'negative_nonmassive_edge_control')
    summaries.append({'name':name,'n':n,'A_points':len(A),'B_points':len(B),
                      'random_generic_samples':random_samples,
                      'equal_column_refinements':equal_samples,
                      'different_product_triangulations':len(set(t for _,t,_,_ in samples)),
                      'nonvertex_projections_observed':nonvertex,
                      'unused_base_points_observed':any(len(set(i for t in T for i in t))<len(A) for _,T,_ in equal)})

run_family('unit_square',list(product(range(2),repeat=2)),2,
           lambda vs:square_face(vs,(1,1)),48,12)
run_family('double_triangle',[v for v in product(range(3),repeat=2) if sum(v)<=2],2,
           lambda vs:simplex_face(vs,2,2),16,10)
run_family('rectangle_2_by_1',list(product(range(3),range(2))),2,
           lambda vs:square_face(vs,(2,1)),16,10)

# Five-dimensional product of a nonunimodular tetrahedron and Delta_2.
# Full A contains unused edge lattice points; all top simplices use the
# tetrahedron's four corners. Generic lower hulls of the 12 corner products
# produce different exact refinements without a staircase construction.
n=3
A=[v for v in product(range(3),repeat=3) if sum(v)<=2]
delta=simplex_vertices(2)
B=[a+b for a in A for b in delta]
corners=simplex_vertices(3,2)
C=[a+b for a in corners for b in delta]
C_to_B=[B.index(v) for v in C]
HC=Hull(C)
baseT=[tuple(A.index(v) for v in corners)]
ET=eta(A,baseT,lambda vs:simplex_face(vs,3,2))
wanted=tuple(n*ET[n][i]-ET[n-1][i] for i in range(len(A)))
test(sorted(wanted)==[0]*6+[12]*4,'explicit_nonunimodular_vector')
different=set()
for _ in range(10):
    heights,UT=HC.generic()
    U=tuple(tuple(sorted(C_to_B[i] for i in t)) for t in UT)
    different.add(U)
    # Extend the corner heights to all of B above every selected lower plane.
    # The resulting full configuration has exactly the same lower hull.
    full_height=[10**20]*len(B)
    for i,b in enumerate(C_to_B):full_height[b]=heights[i]
    for t in U:
        inv=inverse([[1,*B[i]] for i in t])
        coeff=[sum(inv[k][j]*full_height[t[j]] for j in range(6)) for k in range(6)]
        test(all(full_height[i]>=sum(x*y for x,y in zip([1,*v],coeff)) for i,v in enumerate(B)),
             'full_configuration_lower_support')
    EU=eta(B,U,lambda vs:simplex_face([v[:3] for v in vs],3,2)
                        +simplex_face([v[3:] for v in vs],2,1))
    projected=[project(row,3) for row in EU]
    for k in range(6):
        expected=tuple(sum(comb(3,k-j+1)*comb(k+1,j+1)*ET[j][i]
                           for j in range(4) if 0<=k-j<3) for i in range(len(A)))
        test(projected[k]==expected,'dimension_three_massive_levels')
    test(project(massive(EU),3)==wanted,'dimension_three_vector_identity')
test(len(different)>1,'different_nonunimodular_refinements')
summaries.append({'name':'double_tetrahedron_times_triangle','n':3,'A_points':len(A),
                  'B_points':len(B),'generic_refinements':10,
                  'different_product_triangulations':len(different),
                  'base_normalized_volume':8,'nonzero_projected_coordinate_value':12,
                  'unused_base_points':len(A)-4})

result={'status':'PASS','exact_assertions':sum(counts.values()),
        'checks_by_category':dict(sorted(counts.items())),'families':summaries,
        'algorithm':'Exact rational lower supporting hyperplanes, fraction-free integer determinants, saturated face volumes, independent massive-vector and support checks.',
        'limits':['Finite regular triangulations sampled by fixed-seed integer heights, not all triangulations.',
                  'No computation replaces the general centroid or GKZ proof.',
                  'Only the specified smooth complete-lattice source regime is certified.',
                  'No historical novelty claim.']}
print(json.dumps(result,indent=2,sort_keys=True))

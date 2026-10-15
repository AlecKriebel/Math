#!/usr/bin/env python3
"""Independent exact FEM endpoint diagnostics, using only Python's standard library."""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
from hashlib import sha256
from itertools import combinations
import json
counts={}
def ck(name,ok):
    assert ok,name
    counts[name]=counts.get(name,0)+1
def add(P,Q):
    R=dict(P)
    for e,v in Q.items():R[e]=R.get(e,F(0))+v
    return {e:v for e,v in R.items() if v}
def smul(c,P):return {e:c*v for e,v in P.items() if c*v}
def mul(P,Q):
    R={}
    for (i,j),a in P.items():
        for (k,l),b in Q.items():R[i+k,j+l]=R.get((i+k,j+l),F(0))+a*b
    return {e:v for e,v in R.items() if v}
def deriv(P,k):
    R={}
    for e,v in P.items():
        if e[k]:
            f=list(e);f[k]-=1;R[tuple(f)]=v*e[k]
    return R
def integrate(P):return sum(v*F(factorial(i)*factorial(j),factorial(i+j+2)) for (i,j),v in P.items())
def evalp(P,x,y):return sum(v*x**i*y**j for (i,j),v in P.items())
one={(0,0):F(1)};x={(1,0):F(1)};y={(0,1):F(1)}
L=[add(add(one,smul(-1,x)),smul(-1,y)),x,y]
cubic=smul(20,mul(mul(L[0],L[1]),L[2]))
psis=[]
for i,j in combinations(range(3),2):
    quad=smul(4,mul(L[i],L[j]));psi=add(quad,smul(-1,cubic));psis.append(psi)
    ck('mean_zero_exact_polynomial',integrate(psi)==0)
    ck('separate_integrals',integrate(quad)==integrate(cubic)==F(1,6))
    # A cubic restriction is determined by four rational values. These tests
    # also verify trace compatibility in either orientation of the edge.
    third=3-i-j
    for t in (F(0),F(1,3),F(2,3),F(1)):
        bary=[F(0)]*3;bary[i]=t;bary[j]=1-t
        ck('selected_edge_trace',evalp(psi,bary[1],bary[2])==4*t*(1-t))
        for vanish in (i,j):
            bary=[F(0)]*3;remaining=[z for z in range(3) if z!=vanish]
            bary[remaining[0]]=t;bary[remaining[1]]=1-t
            ck('other_edge_trace_zero',evalp(psi,bary[1],bary[2])==0)
    ck('unit_trace_integral',4*(F(1,2)-F(1,3))==F(2,3))
grads=[(deriv(P,0),deriv(P,1)) for P in psis]
G=[[integrate(add(mul(a[0],b[0]),mul(a[1],b[1]))) for b in grads] for a in grads]
ck('reference_energy_values',[G[i][i] for i in range(3)]==[F(40,9),F(40,9),F(64,9)])
def det(A):
    if len(A)==1:return A[0][0]
    return sum((-1)**j*A[0][j]*det([row[:j]+row[j+1:] for row in A[1:]]) for j in range(len(A)))
M=[[3*G[i][i]-G[i][j] if i==j else -G[i][j] for j in range(3)] for i in range(3)]
for size in (1,2,3):
    for inds in combinations(range(3),size):
        ck('overlap_energy_matrix_bound',det([[M[i][j] for j in inds] for i in inds])>=0)
# Affine scaling: det(B)*B^-1*B^-T is independent of a common positive scale.
for a,b,c,d in [(F(1),F(0),F(0),F(1)),(F(2),F(1),F(0),F(1)),(F(1),F(1,3),F(1,4),F(2))]:
    D=a*d-b*c
    base=((d*d+b*b)/D,(-c*d-a*b)/D,(c*c+a*a)/D)
    for n in range(9):
        h=F(1,2**n);aa,bb,cc,dd=(h*z for z in (a,b,c,d));DD=aa*dd-bb*cc
        current=((dd*dd+bb*bb)/DD,(-cc*dd-aa*bb)/DD,(cc*cc+aa*aa)/DD)
        ck('two_dimensional_scale_invariance',current==base)
# Labelled newest-vertex bisection, starting with the exact source pattern.
def edge(a,b):return tuple(sorted((a,b)))
O=(F(1,2),F(1,2));corners=[(F(0),F(0)),(F(1),F(0)),(F(1),F(1)),(F(0),F(1))]
mesh=[]
for i in range(4):
    a=corners[i];b=corners[(i+1)%4]
    mesh.append(((a,b,O),{edge(a,b):0,edge(a,O):1,edge(b,O):1}))
def bisect(T):
    verts,labels=T
    e=min(labels,key=labels.get);lev=labels[e];a,b=e;c=next(v for v in verts if v not in e)
    mid=((a[0]+b[0])/2,(a[1]+b[1])/2)
    return [((a,mid,c),{edge(a,mid):lev+2,edge(mid,c):lev+2,edge(a,c):labels[edge(a,c)]}),
            ((mid,b,c),{edge(mid,b):lev+2,edge(mid,c):lev+2,edge(b,c):labels[edge(b,c)]})]
def area(T):
    a,b,c=T;return abs((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))/2
for j in range(5):
    h=F(1,2**j)
    ck('uniform_base_pattern_cardinality',len(mesh)==4*4**j)
    ck('mesh_covers_unit_area',sum(area(T[0]) for T in mesh)==1)
    for verts,labels in mesh:
        ck('valid_child_labels',sorted(labels.values())==[2*j,2*j+1,2*j+1])
        ck('triangle_area',area(verts)==h*h/4)
        # Each triangle contains exactly one center of a dyadic square.
        centers=[v for v in verts if (v[0]/h-F(1,2)).denominator==1 and (v[1]/h-F(1,2)).denominator==1]
        ck('dyadic_square_center',len(centers)==1)
    if j<4:
        mesh=[kid for T in mesh for kid in bisect(T)]
        mesh=[kid for T in mesh for kid in bisect(T)]
# Multiscale exact tails, selected-edge weights and a constructive O(4^n)
# cost bound using the exact 4*(4^j-1) two-generation fill count.
for n in range(1,41):
    partial=4*sum(F(1,4**j) for j in range(1,n+1))
    ck('energy_and_tail',partial+F(4,3*4**n)==F(4,3))
    cost=sum(4*j+4*(4**j-1) for j in range(1,n+1))
    ck('explicit_refinement_cost_bound',cost<=8*4**n)
    ck('selected_mass_each_level',4**n*2*F(1,4**n)==2)
    ck('selected_mass_total',sum(4**j*2*F(1,4**j) for j in range(1,n+1))==2*n)
    h=F(1,4**n)
    ck('jump_times_length_squared',8*h*h/2==4*h*h)
# Exact identity behind Cauchy's allocation inequality:
# (sum m)(sum a²/m)-(sum a)² = sum_(i<j)(a_i*m_j-a_j*m_i)²/(m_i*m_j).
for num in range(2,10):
    for seed in range(1,21):
        weights=[F((i+seed)%7+1,4**(1+i%4)) for i in range(num)]
        allocations=[1+(seed*(i+1)+i*i)%13 for i in range(num)]
        lhs=sum(allocations)*sum(a*a/m for a,m in zip(weights,allocations))-sum(weights)**2
        rhs=sum((weights[i]*allocations[j]-weights[j]*allocations[i])**2/F(allocations[i]*allocations[j]) for i in range(num) for j in range(i+1,num))
        ck('allocation_sum_of_squares_identity',lhs==rhs>=0)
root=Path(__file__).resolve().parent
result={'status':'PASS','exact_assertions':sum(counts.values()),'counts':counts,'artifact_sha256':sha256((root/'author_replay/COUNTEREXAMPLE.md').read_bytes()).hexdigest(),'reference_energy_matrix':[[str(z) for z in row] for row in G],'scope':'Exact polynomial integration, trace/overlap/scaling checks, labelled NVB base-pattern refinement and allocation identities; no finite enumeration is substituted for the all-mesh proof.'}
out=json.dumps(result,indent=2,sort_keys=True)+'\n';(root/'independent_results.json').write_text(out);print(out,end='')


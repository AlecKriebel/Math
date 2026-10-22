"""Independent exact graph, extension, exponent and entropy controls."""
from itertools import combinations,product
from collections import Counter
from fractions import Fraction as F
from math import factorial,comb,prod
import json
import sympy as s
C=Counter()
def ck(v,key):
    assert v,key
    C[key]+=1

def determinant(A):
    if not A:return 1
    B=[list(map(F,row)) for row in A];ans=F(1);n=len(B)
    for j in range(n):
        pivot=next((i for i in range(j,n) if B[i][j]),None)
        if pivot is None:return 0
        if pivot!=j:B[j],B[pivot]=B[pivot],B[j];ans=-ans
        x=B[j][j];ans*=x
        for col in range(j,n):B[j][col]/=x
        for i in range(j+1,n):
            x=B[i][j]
            for col in range(j,n):B[i][col]-=x*B[j][col]
    return ans

# Kirchhoff's matrix-tree formula for contracted restricted-attachment graphs,
# independent of the author's Pruefer enumeration implementation.
for k in range(2,13):
    for V in range(1,k+1):
        for I in range(V+1):
            outside=k-V;b=V-I
            L=[[(k-I if i==j else 0)-1 for j in range(outside)] for i in range(outside)]
            exact=determinant(L)
            expected=1 if outside==0 else b*(k-I)**(outside-1)
            ck(exact==expected,'restricted_Cayley_extension_Kirchhoff')

def tree_count(labels,edge_set):
    labels=list(labels);k=len(labels)
    L=[[0]*k for _ in labels]
    for i,j in combinations(range(k),2):
        if tuple(sorted((labels[i],labels[j]))) in edge_set:
            L[i][i]+=1;L[j][j]+=1;L[i][j]-=1;L[j][i]-=1
    return determinant([row[:-1] for row in L[:-1]])
def partitions(n,lo=2):
    if n==0:yield ();return
    for a in range(lo,n+1):
        for rest in partitions(n-a,a):yield (a,)+rest
def falling(n,j):return prod(range(n-j+1,n+1))
def forest_moment(n,k,p):
    out=F(1)
    for v in range(2,k+1):
        for parts in partitions(v):
            r=len(parts);m=v-r
            term=F(falling(k,v)**2,falling(n,v)*k**(2*m))*(1/p-1)**m
            term*=prod(F(a**a,factorial(a)) for a in parts)
            term/=prod(factorial(j) for j in Counter(parts).values())
            out+=term
    return out

# Compute the actual likelihood via induced-subgraph Laplacians on every graph.
# This route does not enumerate the candidate's planted trees.
graphs=0
for n,k in [(4,2),(4,3),(4,4),(5,3),(5,5)]:
    edges=list(combinations(range(n),2));N=len(edges);p=F(1,3)
    EL=EL2=F(0)
    for mask in range(1<<N):
        present={e for i,e in enumerate(edges) if mask>>i&1}
        z=sum(tree_count(S,present) for S in combinations(range(n),k))
        ck(z>=0 and F(z).denominator==1,'Kirchhoff_tree_count_integrality')
        L=F(z,comb(n,k)*k**(k-2))*p**(-(k-1))
        w=p**len(present)*(1-p)**(N-len(present))
        EL+=w*L;EL2+=w*L*L;graphs+=1
    ck(EL==1,'Kirchhoff_likelihood_normalization')
    ck(EL2==forest_moment(n,k,p),'Kirchhoff_likelihood_forest_second_moment')

# Recount queried null pairs directly, including all root-root exclusions.
for n in range(3,17):
    for r in range(1,min(4,n)+1):
        for I in range(r,n+1):
            roots=set(range(r));internal=set(range(I))
            pairs=[(u,v) for u,v in combinations(range(n),2)
                   if (u in internal or v in internal) and not (u in roots and v in roots)]
            ck(len(pairs)==I*n-I*(I+1)//2-comb(r,2),'null_queried_pair_count')

# Exact critical powers: t=k^2/n and one component contributes k^(1/4).
ck(F(2)+F(1,4)==F(9,4),'critical_second_moment_power')
ck(1/F(9,4)==F(4,9),'critical_L2_size_power')
r=s.symbols('r',positive=True)
ratio=s.Rational(1,4)*(r/4)/((r/2)*(r/2+1))/prod(r+j for j in range(1,5))
ck(s.simplify(ratio-1/(4*(r+1)*(r+2)**2*(r+3)*(r+4)))==0,'critical_four_step_ratio')

# Independent entropy certificate, without the author's power-of-two reduction.
def exp_lower(x,order=31):
    return sum(((-x)**j/F(factorial(j)) for j in range(order+1)),F(0))
def log_bounds(x,m=128):
    u=(x-1)/(x+1)
    lo=2*sum((u**(2*j+1)/F(2*j+1) for j in range(m)),F(0))
    hi=lo+2*u**(2*m+1)/((2*m+1)*(1-u*u))
    return lo,hi
c=F(3,2);e1=exp_lower(F(1));ec=exp_lower(c)
terms=[];scale=10**12
for j in range(10):
    R=e1*F(5,3)**j
    ll,_=log_bounds(1+R/c)
    term=ec*c**j/F(factorial(j))*(c+R)*ll
    rounded=term.numerator*scale//term.denominator
    ck(F(rounded,scale)<=term,'independent_entropy_rounddown')
    terms.append(rounded)
_,upper=log_bounds(c,32)
ceil=(upper.numerator*scale+upper.denominator-1)//upper.denominator
gap=F(sum(terms)-scale-ceil,scale)
ck(gap>F(1,500),'independent_depth_two_entropy_certificate')

print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(sorted(C.items())),
 'null_graphs_with_Kirchhoff_likelihood':graphs,
 'independent_entropy_certificate':{'lower_term_numerators':terms,'scale':scale,'log_c_upper_numerator':ceil,'gap':str(gap),'exp_order':31,'direct_atanh_terms':128},
 'scope':'Independent finite Kirchhoff, queried-edge, critical-exponent and rational-entropy controls. The asymptotic and stochastic-law audit is in INDEPENDENT_REVIEW.md.'},indent=2,sort_keys=True))

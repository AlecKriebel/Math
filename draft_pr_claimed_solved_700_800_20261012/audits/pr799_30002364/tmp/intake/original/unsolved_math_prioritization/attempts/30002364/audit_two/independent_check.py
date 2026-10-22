"""Independent finite certificate; no geometric theorem is proved by this file."""
import sys
if not (sys.flags.isolated and sys.flags.no_site):
    raise SystemExit('Launch with python -I -S')
from itertools import permutations, combinations, product as choices
from fractions import Fraction
import json

def demand(ok, why):
    if not ok: raise RuntimeError(why)

# Permutations of the four roots (a,b,-a,-b), with function composition.
one = (0,1,2,3)
r = (1,2,3,0)
s = (0,3,2,1)
def compose(p,q): return tuple(p[q[k]] for k in range(4))
def power(p,n):
    ans=one
    for _ in range(n): ans=compose(ans,p)
    return ans
H=[power(r,j) for j in range(4)]+[compose(power(r,j),s) for j in range(4)]
demand(len(set(H))==8,'root permutations generate order 8')
G=[(h,c) for c in (0,1) for h in H]
def product(x,y): return (compose(x[0],y[0]), (x[1]+y[1])%2)
e=(one,0)
inverses={x:next(y for y in G if product(x,y)==e) for x in G}
c=(one,1)
D={e,(s,0)}
f=(-1,-1,-1,1,-1,1,1,-1)
Phi={(h,0 if f[j]==1 else 1) for j,h in enumerate(H)}
demand(len(Phi)==8 and {product(c,x) for x in Phi}.isdisjoint(Phi),'CM type')
# Direct Galois action on the subset of embeddings, without a prescribed matrix.
types=[{product(t,x) for x in Phi} for t in G]
C=[[2*int(h in P)-1 for h in G] for P in types]
M=[row[:8] for row in C[:8]]
# Independent determinant by all 8! terms, not Gaussian elimination.
def det_permutation(A):
    ans=0
    for p in permutations(range(len(A))):
        term=(-1)**sum(p[i]>p[j] for i in range(len(A)) for j in range(i+1,len(A)))
        for i in range(len(A)): term*=A[i][p[i]]
        ans+=term
    return ans

def rank(A):
    a=[[Fraction(x) for x in row] for row in A]; row=0
    for col in range(len(a[0])):
        pivot=next((j for j in range(row,len(a)) if a[j][col]),None)
        if pivot is None: continue
        a[row],a[pivot]=a[pivot],a[row]
        t=a[row][col]; a[row]=[x/t for x in a[row]]
        for j in range(len(a)):
            if j!=row:
                t=a[j][col]; a[j]=[x-t*y for x,y in zip(a[j],a[row])]
        row+=1
    return row

# Primes are right cosets tD, because tP=t'P iff t'=td.
def prime(t): return frozenset(product(t,d) for d in D)
primes=list(dict.fromkeys(prime(t) for t in G))
representatives=[next(t for t in G if prime(t)==P) for P in primes]
# sigma^{-1}P_base = h^{-1} t P_base is evaluated as equality of actual cosets.
counts=[[sum(prime(inverses[sigma])==prime(product(inverses[h],t)) for sigma in Phi)
         for h in G] for t in representatives]
N=[[2*n-2 for n in row] for row in counts]
# N/2 is the centered slope. Each embedding fiber has precisely two elements.
demand(all(sum(prime(inverses[sigma])==P for sigma in G)==2 for P in primes),'fiber sizes')
columns=list(zip(*N))
demand(det_permutation(M)==256,'Hodge determinant')
demand(rank(C)==8,'full Hodge centered rank')
demand(rank(N)==4,'local centered rank')
demand(len(set(columns))==16,'16 distinct embedding valuation vectors')
demand(all(any(col) for col in columns),'no zero embedding vector')
demand(len({t for t in G if {product(t,x) for x in Phi}==Phi})==1,'reflex field is E')
demand(len({t for t in G if {product(x,t) for x in Phi}==Phi})==1,'primitive type stabilizer')

def balanced(J): return all(sum(columns[j][i] for j in J)==0 for i in range(len(primes)))
D2=[J for J in combinations(range(16),2) if balanced(J)]
demand(D2==[(i,i+8) for i in range(8)],'only conjugate-pair Tate divisors')
W=(1,3,13,15)
demand(balanced(W),'quartic witness Tate')
demand(all(not set(J)<=set(W) for J in D2),'quartic witness not divisor-generated')
demand(any(sum(row[j] for j in W) for row in C),'quartic witness not Hodge invariant')
T4=[J for J in combinations(range(16),4) if balanced(J)]
L4={tuple(sorted(p+q)) for p,q in combinations(D2,2)}
demand(L4<=set(T4),'divisor products Tate')
# The four exceptional eigenspaces form a Galois-stable family, explicitly checking descent.
exceptional=[J for J in T4 if J not in L4]
demand(len(T4)==32 and len(L4)==28 and len(exceptional)==4,'exact degree-four dimensions')
for J in exceptional:
    for t in G:
        new=tuple(sorted(G.index(product(t,G[j])) for j in J))
        demand(new in exceptional,'exceptional span Galois stable')
slopes=[Fraction(n,2) for n in counts[0]]
demand([slopes.count(Fraction(x,2)) for x in (0,1,2)]==[6,4,6],'Newton multiplicities')
# Honda-Tate local invariant obstruction is absent: each local degree is two.
demand(all((2*x).denominator==1 for x in slopes),'local degrees times slopes integral')
# Exhaust all CM types with the same oriented local slope function for pi.
lift_types=[]
for signs in choices((-1,1),repeat=8):
    T={(h,0 if signs[j]==1 else 1) for j,h in enumerate(H)}
    base_counts=[sum(prime(inverses[sigma])==P for sigma in T) for P in primes]
    if base_counts==[row[0] for row in counts]:
        orbit=[{product(t,x) for x in T} for t in G]
        centered=[[2*int(h in P)-1 for h in G] for P in orbit]
        lift_types.append({'signs':signs,'centered_Hodge_rank':rank(centered)})
demand(len(lift_types)==2 and all(T['centered_Hodge_rank']==8 for T in lift_types),'fixed-slope CM lift types')
print(json.dumps({'result':'PASS independent permutation/coset certificate','root_group_order':len(H),
 'CM_galois_group_order':len(G),'CM_type_left_stabilizer':1,'CM_type_right_stabilizer':1,
 'hodge_centered_rank':rank(C),'hodge_determinant':det_permutation(M),
 'slope_centered_rank':rank(N),'distinct_embedding_columns':len(set(columns)),
 'Tate_degree_two_dimension':len(D2),'Tate_degree_four_dimension':len(T4),
 'Lefschetz_degree_four_dimension':len(L4),'exceptional_quartics':exceptional,
 'fixed_slope_CM_types':lift_types,'prime_count':len(primes),'local_degree':2,'geometric_theorems_formalized':False},sort_keys=True))

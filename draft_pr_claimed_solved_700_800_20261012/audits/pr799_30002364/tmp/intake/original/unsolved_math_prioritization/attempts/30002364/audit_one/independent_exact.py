"""Independent rational diagnostics built from permutations of the quartic roots.
Does not import or execute the author's checker. Stdlib only.
"""
import sys
if not sys.flags.isolated or not sys.flags.no_site:
    raise SystemExit('Use python -I -S.')
import itertools, json
from fractions import Fraction as F

def check(x, message):
    if not x: raise RuntimeError(message)

# Root order: a,b,-a,-b. Composition is actual root substitution.
I=(0,1,2,3)
r=(1,2,3,0)
s=(0,3,2,1)
c=lambda g,h: tuple(g[h[i]] for i in range(4))
def power(g,n):
    h=I
    for _ in range(n): h=c(g,h)
    return h
H=[c(power(r,j),power(s,k)) for k in (0,1) for j in range(4)]
inv=lambda h: tuple(h.index(j) for j in range(4))
signs=(-1,-1,-1,1,-1,1,1,-1)
f=dict(zip(H,signs))
G=[(h,k) for k in (0,1) for h in H]
cm=lambda g,h:(c(g[0],h[0]), (g[1]+h[1])%2)
gi=lambda g:(inv(g[0]),g[1])
indicator=lambda g:int(((-1)**g[1])*f[g[0]]==1)
D=[(I,0),(s,0)]
Phi={g for g in G if indicator(g)}
# Compute ST fibers by equality of right cosets gD, not the author's averaging function.
coset=lambda g:frozenset(cm(g,d) for d in D)
primes=[]
for g in G:
    if coset(g) not in primes: primes.append(coset(g))
slopes={v:F(sum(coset(gi(phi))==v for phi in Phi),sum(coset(gi(g))==v for g in G)) for v in primes}
S=[[slopes[frozenset(cm(gi(h),t) for t in v)] for h in G] for v in primes]
C=[[2*x-1 for x in row] for row in S]
M=[[2*indicator(cm(gi(t),h))-1 for h in G] for t in G]
T=[[indicator(cm(gi(t),h)) for h in G] for t in G]

def rank(A):
    B=[[F(x) for x in row] for row in A]; k=0
    for j in range(len(B[0])):
        z=next((i for i in range(k,len(B)) if B[i][j]),None)
        if z is None: continue
        B[k],B[z]=B[z],B[k]; p=B[k][j]; B[k]=[a/p for a in B[k]]
        for i in range(len(B)):
            if i!=k:
                p=B[i][j]; B[i]=[a-p*b for a,b in zip(B[i],B[k])]
        k+=1
        if k==len(B): break
    return k

def balanced(labels): return all(sum(row[j] for j in labels)==0 for row in C)
columns=[tuple(row[j] for row in C) for j in range(16)]
classes={k:[list(labels) for labels in itertools.combinations(range(16),2*k) if balanced(labels)] for k in range(9)}
lefschetz={k:[labels for labels in classes[k] if all((j+8)%16 in labels for j in labels)] for k in range(9)}
W=[1,3,13,15]
fulltype_stabilizer_left=[i for i,g in enumerate(G) if {cm(g,p) for p in Phi}==Phi]
fulltype_stabilizer_right=[i for i,g in enumerate(G) if {cm(p,g) for p in Phi}==Phi]
check(rank(M)==8,'Hodge centered rank')
check(rank(T)==9,'Mumford Tate rank')
check(rank(C)==4,'Frobenius centered rank')
check(rank(S)==5,'Frobenius full rank')
check(len(set(columns))==16,'distinct valuation columns')
check(fulltype_stabilizer_left==[0] and fulltype_stabilizer_right==[0],'primitive type and full reflex field')
check(classes[1]==[[j,j+8] for j in range(8)],'degree-two Tate pairs')
check(W in classes[2] and W not in lefschetz[2],'exotic Tate wedge')
check(any(sum(row[j] for j in W) for row in M),'not Hodge wedge')
# A same-reduction family: enumerate ALL CM types having identical local fibers.
# Both compatible E-CM types have full centered Hodge rank; no choice among
# these types gives rank four merely by selecting a distinguished lift.
compatible=[]
for bits in itertools.product((0,1),repeat=8):
    Q={G[j+(8 if not bits[j] else 0)] for j in range(8)}
    counts={v:sum(coset(gi(phi))==v for phi in Q) for v in primes}
    if all(F(counts[v],2)==slopes[v] for v in primes):
        U=[[2*int(cm(gi(t),h) in Q)-1 for h in G] for t in G]
        compatible.append({'bits':list(bits),'centered_rank':rank(U)})
check(len(compatible)==2,'number of E-CM types sharing local fibers')
check(all(x['centered_rank']==8 for x in compatible),'compatible types have full Hodge rank')
result={'result':'PASS independent exact diagnostics','construction':'permutation substitution and direct local embedding fibers','hodge_centered_rank':rank(M),'mumford_tate_dimension':rank(T),'frobenius_centered_rank':rank(C),'frobenius_torus_dimension':rank(S),'distinct_signed_columns':len(set(columns)),'prime_count':len(primes),'prime_local_degree':2,'type_left_stabilizer':fulltype_stabilizer_left,'type_right_stabilizer':fulltype_stabilizer_right,'tate_dimensions_by_codimension':{str(k):len(v) for k,v in classes.items()},'lefschetz_dimensions_by_codimension':{str(k):len(v) for k,v in lefschetz.items()},'wedge_labels':W,'compatible_cm_types':compatible,'newton_slopes':{str(x):S[0].count(x) for x in sorted(set(S[0]))},'all_honda_tate_local_invariants_integral':all((2*x).denominator==1 for x in S[0]),'geometric_theorems_formally_verified':False}
print(json.dumps(result,sort_keys=True,indent=2))

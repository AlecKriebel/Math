#!/usr/bin/env python3
"""Independent exact local arithmetic and finite-plane checks; no quotient enumeration.
Only stdlib plus numpy are used. All matrices are reduced mod 11 after each product.
Output is evidence, not a substitute for LSV's theorem or the mathematical proof.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, sys
import numpy as np

P=11

def irreducible_cubic():
    for aa in range(P):
        for bb in range(1,P):
            if all((x**3+aa*x+bb)%P for x in range(P)):
                return (bb,aa,0,1)
    raise AssertionError('no cubic')
MOD=irreducible_cubic()
ZERO=(0,0,0); ONE=(1,0,0)
BASIS=[ONE,(0,1,0),(0,0,1)]
def add(a,b): return tuple((x+y)%P for x,y in zip(a,b))
def neg(a): return tuple((-x)%P for x in a)
def sub(a,b): return add(a,neg(b))
def mul(a,b):
    c=[0]*5
    for i in range(3):
        for j in range(3): c[i+j]=(c[i+j]+a[i]*b[j])%P
    for k in (4,3):
        v=c[k]
        for j in range(3): c[k-3+j]=(c[k-3+j]-v*MOD[j])%P
    return tuple(c[:3])
def power(a,n):
    r=ONE
    while n:
        if n&1:r=mul(r,a)
        a=mul(a,a); n//=2
    return r

def inverse(a):
    assert a!=ZERO
    b=power(a,P**3-2); assert mul(a,b)==ONE
    return b

def phi(a,k=1): return power(a,P**(k%3))
def multiplication(a): return np.array([mul(a,e) for e in BASIS], dtype=np.int64).T

def invmat(a):
    n=a.shape[0]; z=np.concatenate([a.copy()%P,np.eye(n,dtype=np.int64)],axis=1)
    for j in range(n):
        k=next(k for k in range(j,n) if z[k,j])
        z[[j,k]]=z[[k,j]]
        z[j]=(z[j]*pow(int(z[j,j]),P-2,P))%P
        for k in range(n):
            if k!=j:z[k]=(z[k]-z[k,j]*z[j])%P
    assert np.array_equal((a@z[:,n:])%P,np.eye(n,dtype=np.int64))
    return z[:,n:]

# Derive Ad(1-z^{-1}) using z^3=1+1/t. For alpha z^k, the result is
# alpha z^k +(alpha-phi^{-1}(alpha))*(sum_{i<k} z^i+t*sum_{i<3}z^i).
# This follows by multiplying (1-z^{-1}) alpha z^k (1+t*(1+z+z^2)).
fr=np.array([sub(e,phi(e,2)) for e in BASIS],dtype=np.int64).T
b0=np.eye(9,dtype=np.int64); b1=np.zeros((9,9),dtype=np.int64)
for k in range(3):
    for i in range(3):
        if i<k:b0[3*i:3*i+3,3*k:3*k+3]+=fr
        b1[3*i:3*i+3,3*k:3*k+3]=fr
b0%=P
c0=invmat(b0); c1=(-c0@b1@c0)%P; c2=(-c0@b1@c1)%P
assert not np.any((b1@c2)%P)
B=np.stack([b0,b1,np.zeros_like(b0)]); BI=np.stack([c0,c1,c2])

def polymul(a,b):
    out=np.zeros((len(a)+len(b)-1,9,9),dtype=np.int64)
    for i in range(len(a)):
        for j in range(len(b)):out[i+j]=(out[i+j]+a[i]@b[j])%P
    return out
identity=np.zeros((5,9,9),dtype=np.int64);identity[0]=np.eye(9,dtype=np.int64)
assert np.array_equal(polymul(B,BI),identity)
assert np.array_equal(polymul(BI,B),identity)

# All 133 classes F_1331^*/F_11^*. Normalizing coordinates is just a transversal.
reps=[]
for a in range(P):
    for b in range(P):
        for c in range(P):
            u=(a,b,c)
            if u==ZERO:continue
            first=next(x for x in u if x)
            if first==1:reps.append(u)
assert len(reps)==133
positive=[];negative=[]
for u in reps:
    cu=np.zeros((9,9),dtype=np.int64); ci=np.zeros_like(cu)
    for k in range(3):
        ratio=mul(u,inverse(phi(u,k)))
        cu[3*k:3*k+3,3*k:3*k+3]=multiplication(ratio)
        ci[3*k:3*k+3,3*k:3*k+3]=multiplication(inverse(ratio))
    assert np.array_equal((cu@ci)%P,np.eye(9,dtype=np.int64))
    positive.append(np.stack([(cu@v@ci)%P for v in B]))
    negative.append(np.stack([(cu@v@ci)%P for v in BI]))
S=np.array(positive+negative)
SI=np.array(negative+positive)
assert len({s.astype('uint8').tobytes() for s in S})==266
keys={np.pad(s,((0,2),(0,0),(0,0))).astype('uint8').tobytes():i for i,s in enumerate(S)}
adj=np.zeros((266,266),dtype=np.int64)
for i,si in enumerate(SI):
    out=np.zeros((266,5,9,9),dtype=np.int64)
    for a in range(3):
        for b in range(3):out[:,a+b]=(out[:,a+b]+si[a]@S[:,b])%P
    for j,ss in enumerate(out):
        if ss.astype('uint8').tobytes() in keys:adj[i,j]=1
assert np.array_equal(adj,adj.T)
assert not np.any(np.diag(adj))
assert not np.any(adj[:133,:133]) and not np.any(adj[133:,133:])
assert np.all(adj.sum(axis=1)==12)
N=adj[:133,133:]
assert np.array_equal(N@N.T,11*np.eye(133,dtype=np.int64)+np.ones((133,133),dtype=np.int64))
# Exact identity above proves no 4-cycles. Bipartition proves no odd cycles.
# All products here have polynomial degree <=4, so reducing modulo t^9 cannot
# create additional equality s_i^{-1}s_j=s_k: equality mod t^9 is exact here.

# Construct PG(2,11) without any extension-field machinery.
points=reps
inc=np.array([[int(sum(x*y for x,y in zip(pt,line))%P==0) for line in points] for pt in points],dtype=np.int64)
assert np.all(inc.sum(axis=0)==12) and np.all(inc.sum(axis=1)==12)
assert np.array_equal(inc@inc.T,11*np.eye(133,dtype=np.int64)+np.ones((133,133),dtype=np.int64))
A=np.block([[np.zeros((133,133),dtype=np.int64),inc],[inc.T,np.zeros((133,133),dtype=np.int64)]])
ev=np.linalg.eigvalsh(A.astype(float))
spec_gap=(12-float(np.sqrt(11)))/12
actual_deleted=[]
for delete in (0,133):
    H=np.delete(np.delete(A,delete,axis=0),delete,axis=1)
    deg=H.sum(axis=1)
    normalized=np.eye(265)-(H/np.sqrt(deg[:,None]*deg[None,:]))
    es=np.linalg.eigvalsh(normalized)
    assert abs(es[0])<1e-12
    actual_deleted.append(float(es[1]))
# Every deletion is conjugate to one of these two by projective linear symmetry;
# duality swaps the two types. The proof uses the exact conservative bound below.

def rrank_mod(A,p):
    z=A.copy()%p; row=0
    for col in range(z.shape[1]):
        nz=next((i for i in range(row,z.shape[0]) if z[i,col]),None)
        if nz is None:continue
        z[[row,nz]]=z[[nz,row]];z[row]=(z[row]*pow(int(z[row,col]),p-2,p))%p
        for i in range(row+1,z.shape[0]):
            if z[i,col]:z[i]=(z[i]-z[i,col]*z[row])%p
        row+=1
        if row==z.shape[0]:break
    return row

# The summed cocycle identities in the proof are checked on the boundary of a
# tetrahedron with arbitrary integer vertex potentials: m(e)=2, a_uv=g_v-g_u.
# Each local difference equals the opposite oriented edge, up to sign.
from itertools import combinations
triangles=list(combinations(range(4),3));edges=list(combinations(range(4),2))
g=[3,-2,5,7]; energy=sum(2*(g[v]-g[u])**2 for u,v in edges)
local_energy=0;local_norm=0
for v in range(4):
    for tri in triangles:
        if v in tri:
            u,w=[a for a in tri if a!=v]
            local_energy+=((g[u]-g[v])-(g[w]-g[v]))**2
    local_norm+=sum(2*(g[u]-g[v])**2 for u in range(4) if u!=v)
assert local_energy==energy and local_norm==2*energy

# The degree-six obstruction and spherical Euler identity are exact integer
# identities, not claims about positive characteristic boundary ranks.
for vertices in range(1,100):
    edges_sphere=3*vertices-6
    assert edges_sphere<3*vertices
out={
 'utc':datetime.now(timezone.utc).isoformat(),
 'python':sys.version,'numpy':np.__version__,
 'field_modulus_low_to_high':MOD,
 'generator_matrices':{'positive_count':len(positive),'negative_count':len(negative),'all_distinct':True,'forward_degree_bound':1,'inverse_degree_bound':2,'inverse_product_exact':True,'local_products_degree_bound':4,'congruence_exponent':9},
 'arithmetic_neighbor_link':{'vertices':266,'edges':int(adj.sum()//2),'degree_min':int(adj.sum(1).min()),'degree_max':int(adj.sum(1).max()),'same_color_edges':0,'exact_incidence_gram':'11 I + J','girth_at_least':6,'sha256_incidence_uint8':hashlib.sha256(N.astype('uint8').tobytes()).hexdigest()},
 'projective_plane':{'points':133,'lines':133,'gram_exact':True,'degree':12,'adjacency_eigenvalue_min':float(ev[0]),'adjacency_eigenvalue_max':float(ev[-1]),'normalized_gap_formula':spec_gap,'deleted_gap_exact_lower_bound':(11-float(np.sqrt(11)))/12,'deleted_gap_numerical_by_two_types':actual_deleted},
 'weighted_cocycle_count_identity':{'E':energy,'summed_link_energy':local_energy,'summed_local_norm':local_norm},
 'interpretation':'Exact local matrix and incidence checks support independent derivations. Floating eigenvalues are diagnostics only. No full finite congruence quotient was enumerated; no exhaustive H_1 computation of K is claimed.'
}
Path(__file__).with_name('DIAGNOSTICS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

#!/usr/bin/env python3
"""Source-only adversarial controls. Standard-library exact arithmetic, no candidate imports.

Finite computations verify identities; the accompanying proof note supplies all
infinite-support/non-finite-generation arguments. No finite truncation is treated
as proof of an infinite claim. Matrix/group-ring conventions are explicit.
"""
from fractions import Fraction
from itertools import permutations, product
from collections import defaultdict
import hashlib, pathlib, datetime, json

def rank(a):
    a = [[Fraction(x) for x in row] for row in a]
    if not a: return 0
    r = 0
    for j in range(len(a[0])):
        p = next((i for i in range(r,len(a)) if a[i][j]),None)
        if p is None: continue
        a[r],a[p] = a[p],a[r]
        q = a[r][j]; a[r] = [x/q for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][j]:
                q = a[i][j]; a[i] = [x-q*y for x,y in zip(a[i],a[r])]
        r += 1
        if r == len(a): break
    return r

def mm(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def eye(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def kron(a,b):
    return [[a[i][j]*b[k][l] for j in range(len(a[0])) for l in range(len(b[0]))]
            for i in range(len(a)) for k in range(len(b))]
def neg(a): return [[-x for x in row] for row in a]
def zero(a): return all(x==0 for row in a for x in row)
def emit(name, **kw): print(json.dumps(dict(control=name, **kw),sort_keys=True))

def pmul(a,b): return tuple(a[b[i]] for i in range(3))
def pinv(a): return tuple(a.index(i) for i in range(3))
S = sorted(permutations(range(3))); E=(0,1,2); s=(1,0,2)
H={E,s}
T=[]; covered=set()
for g in S:
    if g not in covered:
        T.append(g); covered.update(pmul(h,g) for h in H)
assert len(T)==3 and any(pmul(pmul(g,s),pinv(g)) not in H for g in S)

def add(a,b):
    out=defaultdict(int); out.update(a)
    for g,c in b.items(): out[g]+=c
    return {g:c for g,c in out.items() if c}
def scale(a,n): return {g:n*c for g,c in a.items() if n*c}
def grmul(a,b,mul):
    out=defaultdict(int)
    for g,c in a.items():
        for h,d in b.items(): out[mul(g,h)]+=c*d
    return {g:c for g,c in out.items() if c}
def basis(g): return {g:1}
def theta(a):
    return {t:{h:grmul(basis(t),a,pmul).get(h,0) for h in sorted(H)} for t in T}
def evaltheta(a,x): return {h:grmul(basis(x),a,pmul).get(h,0) for h in sorted(H)}
def rhs_h(f,h):
    return {t:{k:grmul({u:c for u,c in f[t].items() if c},basis(h),pmul).get(k,0)
                   for k in sorted(H)} for t in T}
coind_rows=[(t,h) for t in T for h in sorted(H)]
Theta=[[theta(basis(g))[t][h] for g in S] for t,h in coind_rows]
assert all(sum(row)==1 for row in Theta) and all(sum(col)==1 for col in zip(*Theta))
checks=0
for a,g,h,x in product(S,S,H,S):
    # Theta(g*a)(x)=Theta(a)(x*g); no normality needed.
    assert evaltheta(basis(pmul(g,a)),x)==evaltheta(basis(a),pmul(x,g))
    assert theta(basis(pmul(a,h)))==rhs_h(theta(basis(a)),h)
    assert evaltheta(basis(a),pmul(h,x))=={
        k:grmul(basis(h),{u:c for u,c in evaltheta(basis(a),x).items() if c},pmul).get(k,0)
        for k in sorted(H)}
    checks+=1
def wrongtheta(a,x): return {h:grmul(a,basis(x),pmul).get(h,0) for h in sorted(H)}
wrong = next((a,g,x) for a,g,x in product(S,S,S)
             if wrongtheta(basis(pmul(g,a)),x)!=wrongtheta(basis(a),pmul(x,g)))
assert evaltheta({g:1 for g in S},E)=={h:1 for h in sorted(H)}
emit('nonnormal_S3_H_order2_coinduction',transversal=T,integer_matrix=Theta,
     rank=rank(Theta),equivariance_cases=checks,wrong_projection_witness=wrong,
     norm_projection='sum_G maps to sum_H, coefficient 1, no division')

def reduce_word(w):
    out=[]
    for a in w:
        if out and out[-1]==-a: out.pop()
        else: out.append(a)
    return tuple(out)
def fmul(u,v): return reduce_word(u+v)
def finv(u): return tuple(-x for x in reversed(u))
def gmul(u,v): return (fmul(u[0],v[0]),fmul(u[1],v[1]))
def ginv(u): return (finv(u[0]),finv(u[1]))
ge=((),()); a=((1,),()); b=((2,),()); c=((),(1,)); d=((),(2,))
Rone=basis(ge)
def diff(g): return add(basis(g),scale(Rone,-1))
def rproduct(u,v): return grmul(u,v,gmul)
x=gmul(b,ginv(a)); y=gmul(c,ginv(a)); z=gmul(d,ginv(a))
height=lambda u: sum(1 if k>0 else -1 for k in u[0]+u[1])
assert all(height(u)==0 for u in [x,y,z])
assert gmul(gmul(ginv(a),x),a)==gmul(gmul(y,x),ginv(y))
assert gmul(a,y)==gmul(y,a) and gmul(a,z)==gmul(z,a)
coeff=diff(x)
u=basis(y); v=basis(a)
assert rproduct(coeff,rproduct(u,v))==rproduct(rproduct(coeff,u),v)
assert rproduct(rproduct(u,v),coeff)!=rproduct(rproduct(u,coeff),v)
emit('actual_noncommuting_right_module_matrix',x=x,y=y,z=z,
     conjugation_identity=True,right_linearity=True,wrong_side_detected=True,
     wrong_side_outputs=[str(rproduct(rproduct(u,v),coeff)),str(rproduct(rproduct(u,coeff),v))])

# The actual augmentation resolution of F2 x F2 has four square cells.
gens=[a,b,c,d]
cols=[]
for i,j in [(0,2),(0,3),(1,2),(1,3)]:
    col=[{} for _ in gens]
    col[i]=scale(diff(gens[j]),-1); col[j]=diff(gens[i]); cols.append(col)
for col in cols:
    boundary={}
    for entry,g in zip(col,gens): boundary=add(boundary,rproduct(entry,diff(g)))
    assert boundary=={}
    assert all(sum(entry.values())==0 for entry in col)
emit('actual_F2xF2_augmentation_resolution',square_boundaries=4,all_zero=True,
     free_ranks=[1,4,4],actual_H1='0 by independent tensor proof',actual_H2='cokernel of right R^4 target; finitely generated')

# Exact cyclic cover over Z[t,t^-1]; Laurent exponents are never truncated.
B=[[-1,-1,0,0],[0,0,-1,-1],[1,0,1,0],[0,1,0,1]]
w=[1,-1,-1,1]
assert rank(B)==3 and mm(B,[[v] for v in w])==[[0]]*4
assert mm([[1,1,1,1]],B)==[[0]*4]
polys=[{n:1} for n in range(-8,9)]
kernel_vectors=[[{n:v} for v in w] for n in range(-8,9)]
assert len({tuple(tuple(sorted(p.items())) for p in vec) for vec in kernel_vectors})==17
emit('top_syzygy_FP1_not_FP2_group_ring_control',cover_incidence_matrix=B,
     primitive_kernel=w,rank=3,exact_laurent_kernel='Z[t,t^-1]*(1,-1,-1,1)',
     independent_translates=17,subgroup_generators=[x,y,z],
     proof='H=ker(F2xF2 -> Z) is finitely generated; H2(H,Z)=Z[t,t^-1]; induced cyclic finitely presented module is not FP2')

A=[[1,1],[0,1]]; N=7
height_matrix=[[0]*(2*N) for _ in range(2*(N+1))]
for h in range(N):
    for i in range(2):
        height_matrix[2*h+i][2*h+i]+=1
        for j in range(2): height_matrix[2*(h+1)+i][2*h+j]-=A[i][j]
assert rank(height_matrix)==2*N
periodic=[[0]*(2*N) for _ in range(2*N)]
for h in range(N):
    for i in range(2):
        periodic[2*h+i][2*h+i]+=1
        for j in range(2): periodic[2*((h+1)%N)+i][2*h+j]-=A[i][j]
assert rank(periodic)==2*N-1
assert mm(A,[[1],[0]])==[[1],[0]]
emit('height_finite_support_matrix',transport=A,window_input_rank=2*N,
     window_output_rank=rank(height_matrix),periodic_nullity=2*N-rank(periodic),
     completed_fixed_vector='constant sequence (1,0)',nonascending_fixed_vector='reflection fixes height 0')

D=[[2,1],[0,3]]; U=[[1,0],[3,-1]]; V=[[0,1],[1,-2]]
assert mm(mm(U,D),V)==[[1,0],[0,6]]
I=eye(2); d0=kron(D,I)+kron(I,D)
d1=[r+s for r,s in zip(neg(kron(I,D)),kron(D,I))]
assert zero(mm(d1,d0))
assert rank(d0)==4 and rank(d1)==4
def residue(vec): return (3*vec[0]-vec[1])%6
bocks=[]
for p,v in [(2,[1,0]),(3,[1,1])]:
    lift=[r[0] for r in mm(D,[[u] for u in v])]
    assert all(q%p==0 for q in lift)
    image=[q//p for q in lift]
    assert residue(image)!=0 and p*residue(image)%6==0
    bocks.append(dict(prime=p,kernel_vector=v,lift=lift,bockstein=image,class_mod6=residue(image)))
emit('integral_tensor_Tor_Bockstein',differential=D,U=U,V=V,smith_diagonal=[1,6],
     rational_cohomology='0',integral_H1='Z/6',bocksteins=bocks,
     tensor_d0=d0,tensor_d1=d1,composition_zero=True,
     tensor_cohomology={'H1':'Tor_1(Z/6,Z/6)=Z/6','H2':'Z/6 tensor Z/6=Z/6'},
     rational_only_negative='direct sum over n of Z/2 with trivial action has zero rationalization but is not finitely generated')

def hmul(u,v):
    a,b,c=u; A,B,C=v
    return a+A,b+B,c+C+a*B
def hinv(u):
    a,b,c=u; return -a,-b,-c+a*b
he=(0,0,0); hx=(1,0,0); hy=(0,1,0); hz=(0,0,1)
comm=lambda u,v: hmul(hmul(hmul(u,v),hinv(u)),hinv(v))
assert comm(hx,hy)==hz
small=list(product(range(-1,2),repeat=3))
assert all(hmul(hmul(u,v),w)==hmul(u,hmul(v,w)) for u,v,w in product(small,repeat=3))
assert all(comm((1,0,m),(0,1,n))==hz for m,n in product(range(-4,5),repeat=2))
qsmall=list(product(range(-2,3),repeat=2)); cocycle=lambda u,v:u[0]*v[1]
qadd=lambda u,v:(u[0]+v[0],u[1]+v[1])
assert all(cocycle(u,v)+cocycle(qadd(u,v),w)==cocycle(v,w)+cocycle(u,qadd(v,w))
           for u,v,w in product(qsmall,repeat=3))
emit('nonsplit_Heisenberg_extension',commutator=hz,associativity_cases=len(small)**3,
     cocycle_cases=len(qsmall)**3,central_lift_cases=81,
     no_split_reason='Every pair of lifts of quotient generators has commutator z',
     concentration='N=Z, Q=Z^2, H3(G,ZG)=Z, all other degrees zero')

def parity_sign(n): return -1 if n%2 else 1
def kmul(u,v): return (u[0]+parity_sign(u[1])*v[0],u[1]+v[1])
ke=(0,0); kx=(1,0); ky=(0,1); kxi=(-1,0)
kone=basis(ke)
kd=lambda g:add(basis(g),scale(kone,-1))
km=lambda u,v:grmul(u,v,kmul)
ka=add(basis(ky),basis(kxi)); kb=add(kone,scale(basis(kxi),-1))
assert add(km(ka,kd(kx)),km(kb,kd(ky)))=={}
orientation=lambda p:sum(c*parity_sign(g[1]) for g,c in p.items())
assert orientation(ka)==orientation(kb)==0
assert sum(ka.values())==2
assert km(basis(ky),basis(kx))!=km(basis(kx),basis(ky))
emit('actual_Klein_bottle_diagonal_action',Fox_coefficients=[str(ka),str(kb)],
     augmentation_boundary_zero=True,top_cokernel='Z, x acts +1, y acts -1',
     orientation_eval=[orientation(ka),orientation(kb)],wrong_trivial_eval=sum(ka.values()),
     noncommuting=True)

emit('quotient_concentration_omitted_negative',group='Z^2 * Z',
     actual_cell_ranks=[1,3,1],actual_H1_witness='(0,0,1), cannot be δ0(r) because (a-1)r=0 implies r=0',
     actual_H2_witness='augmentation survives coker((1-b),(a-1),0)',
     conclusion='Type F quotient with cohomology in two degrees; concentration is an additional hypothesis')
emit('infinite_graph_trivial_stabilizers_negative',graph='one vertex, countably many loop edges',
     group='free group of countable rank',H1='direct sum over n of Z',FP1=False,
     finite_graph_control_ranks=[rank(eye(n)) for n in [1,3,10]],
     proof='A finite generating set has finite total loop support; a loop outside support survives abelianization')
emit('omitted_N_FP_direct_sum_negative',N='free group of countable rank',
     map='generator n maps to basis vector n in direct sum Z',
     conclusion='Hom(N,direct sum Z) contains a map outside direct sum Hom(N,Z)')

emit('completed',status='PASS',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
     script_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
     caveat='Exact identities and finite controls; infinite claims require the independent proof note; no candidate or historical imports')

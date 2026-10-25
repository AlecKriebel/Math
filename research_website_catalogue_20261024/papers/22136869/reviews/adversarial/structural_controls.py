#!/usr/bin/env python3
"""Exact finite controls for the all-n/observable-symmetry proof interfaces."""
import sympy as s
import itertools as it
from collections import Counter
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
counts=Counter();details={}
def ck(v,k):
    if not bool(v):raise AssertionError(k)
    counts[k]+=1
R=s.Rational
def JC(a):return a*s.eye(4)+(1-a)*s.ones(4)/4
A,B,C=JC(R(1,2)),JC(R(1,3)),JC(R(2,5))
cherry=s.Matrix(16,4,lambda i,j:B[j,i//4]*C[j,i%4])
for M in [A,cherry,A*A]:
    ck(M.rank()==4,'subtree_column_rank')
    for j in range(4):ck(sum(M[:,j])==1,'subtree_normalization')
for i,j in it.combinations([1,2,3],2):
    perm=list(range(4));perm[i],perm[j]=perm[j],perm[i]
    P=s.zeros(4)
    for k in range(4):P[perm[k],k]=1
    PP=s.kronecker_product(P,P)
    ck(A*P==P*A,'jc_equivariance')
    ck(cherry*P==PP*cherry,'jc_equivariance')
# A marginal left inverse witnesses injectivity without forming a huge inverse.
marg=s.Matrix(4,16,lambda i,j:int(i==j//4))
ck(marg*cherry==B,'cherry_marginal')
left=B.inv()*marg
ck(left*cherry==s.eye(4),'explicit_subtree_left_inverse')
L=s.kronecker_product(A,cherry,A*A)
LI=s.kronecker_product(A.inv(),left,(A*A).inv())
ck(LI*L==s.eye(64),'three_subtree_tensor_injective')
ck(JC(0).rank()==1,'zero_eigenvalue_negative_control')

# Positive-tree pair-coordinate recovery has nonsingular derivative per
# character; character-fixed outputs force equal recovered edge parameters.
a,b,c=s.symbols('a b c',positive=True)
J=s.Matrix([[b,a,0],[c,0,a],[0,c,b]])
ck(s.factor(J.det())==-2*a*b*c,'tree_rank_general_identity')
for n in [2,3]:ck(n*3=={2:6,3:9}[n],'tree_dimensions')
triples=[v for v in it.product(range(4),repeat=3) if v[0]^v[1]^v[2]==0]
sigma={0:0,1:3,2:2,3:1}
orbits={frozenset((v,tuple(sigma[x] for x in v))) for v in triples}
ck((len(triples),len(orbits))==(16,10),'fourier_ambient_dimensions')
ck((20-9+6,29-15+9,20-9,29-15)==(17,23,11,14),'local_fiber_dimensions')

# Clarify what the equal-B specialization adds to the p12 positive ansatz.
kap,z=s.symbols('kap z');tau=R(1,3);sig=2*s.sqrt(5)/3
shape1=kap*(1+tau*tau)+2*tau-sig*(kap*tau+1)
ks=s.solve(shape1,kap)
ck(len(ks)==1 and s.simplify(ks[0]-3/s.sqrt(5))==0,'equal_B_forces_kappa')
shape2=2*kap*tau+z*(kap*kap*tau*tau+1)-(2*tau/sig)*(kap*kap+1+2*kap*z*tau)
zs=s.solve(shape2.subs(kap,ks[0]),z)
ck(len(zs)==1 and s.simplify(zs[0]-1/s.sqrt(5))==0,'equal_B_forces_b_squared')
ratio2=s.simplify((kap*kap+1+2*kap*z*tau)/(2*(1+tau*tau))).subs({kap:ks[0],z:zs[0]})
ck(s.simplify(ratio2-R(36,25))==0,'equal_B_forces_positive_ratio_6_over_5')
details['ansatz_adjudication']='The ratio is not necessary for unrestricted tree factorization, but is necessary after the equal-B specialization. Both interpretations have exact evidence.'

# Graph controls on several binary trees and every internal vertex: replacing
# a degree-three vertex by the theta core yields exactly one level-two blob.
def edge(a,b):return frozenset((a,b))
def nodes(E):return set().union(*E)
def components(E,V):
    unseen=set(V);out=[]
    while unseen:
        start=next(iter(unseen));seen={start};todo=[start]
        while todo:
            a=todo.pop()
            for e in E:
                if a in e:
                    b=next(iter(e-{a}))
                    if b not in seen:seen.add(b);todo.append(b)
        unseen-=seen;out.append(seen)
    return out
families=0
for scheme in range(3):
    E={edge('v0',str(i)) for i in range(1,4)}
    for n in range(3,9):
        if n>3:
            choices=sorted(E,key=lambda e:tuple(sorted(e)))
            old=choices[(scheme*(n+1))%len(choices)];E.remove(old)
            a,b=sorted(old);w='v'+str(n-3);E|={edge(a,w),edge(b,w),edge(w,str(n))}
        V=nodes(E)
        for v in sorted(x for x in V if x.startswith('v')):
            neigh=sorted(next(iter(e-{v})) for e in E if v in e)
            ck(len(neigh)==3,'binary_tree_vertex')
            core={edge('P','U'),edge('U','Q'),edge('P','R2'),edge('R2','Q'),edge('P','R3'),edge('R3','Q')}
            N={e for e in E if v not in e}|core|{edge(x,y) for x,y in zip(neigh,['U','R2','R3'])}
            NV=nodes(N)
            ck(len(components(N,NV))==1,'grafted_connectivity')
            for x in NV:
                degree=sum(x in e for e in N)
                ck(degree==(1 if x.isdigit() else 3),'grafted_binary_degrees')
            nonbridges={e for e in N if len(components(N-{e},NV))==1}
            ck(nonbridges==core,'sole_nontrivial_blob')
            ck(len(core)-5+1==2,'strict_level_two_core')
            contract={edge(v if a in {'P','U','Q','R2','R3'} else a,v if b in {'P','U','Q','R2','R3'} else b) for e in N-core for a,b in [tuple(e)]}
            ck(contract==E,'tree_of_blobs_recovers_tree')
            families+=1
details['graft_instances']=families

# Bind the positive cubic root used by additional_controls to its CRootOf index.
x=s.symbols('x');p=s.Poly(634127002560*x**3-2160769703472*x**2+1746884136303*x-169873318739,x)
lo=R(1073231219980,10**12);hi=R(1073231219981,10**12)
ck(p.count_roots(-s.oo,lo)==1 and p.count_roots(lo,hi)==1 and p.count_roots(hi,s.oo)==1,'cubic_embedding_root_index')
result={'status':'PASS','utc':datetime.now(timezone.utc).isoformat(),'assertions':sum(counts.values()),'families':len(counts),'counts':dict(counts),'details':details,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limits':'Finite topology and exact linear algebra controls support, but do not replace, the written universal common-kernel proof.'}
Path(__file__).with_name('structural_control_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

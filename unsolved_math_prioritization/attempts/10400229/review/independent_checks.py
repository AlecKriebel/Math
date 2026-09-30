#!/usr/bin/env python3
"""Independent exact symbolic and continuant controls, not a knot classifier."""
from itertools import product
from pathlib import Path
from math import gcd,isqrt
import hashlib,json
import sympy as S
counts={}
def ck(name,cond):
    assert cond,name
    counts[name]=counts.get(name,0)+1

t=S.symbols('t', nonzero=True)
a,b,c,d,e=S.symbols('a b c d e')
V=S.Matrix([[a,b],[c,d]])
Vp=V+S.diag(e,0)
ck('symbolic_rank_two_difference',S.expand((Vp-t*Vp.T).det()-(V-t*V.T).det()-e*d*(1-t)**2)==0)
ck('symbolic_metabolic_norm',S.expand((V-t*V.T).det().subs(d,0)/t-(b-c*t)*(b-c/t))==0)
for sign in (-1,1):
    ck('rank_two_normalization',S.expand((V-V.T).det().subs(c,b-sign))==1)
    ck('determinant_square',S.expand(((b-c*t)*(b-c/t)).subs({t:-1,c:b-sign})-(2*b-sign)**2)==0)
V0=S.Matrix([[1,0],[-1,-1]]);P=S.Matrix([[1,1],[1,0]])
ck('anti_isometry',P.T*V0*P==-V0 and P.det()==-1)
Graph=S.eye(2).col_join(P)
ck('graph_isotropic',Graph.T*S.diag(V0,V0)*Graph==S.zeros(2))
# A left inverse to the graph inclusion certifies primitivity without a search.
ck('graph_primitive',S.eye(2).row_join(S.zeros(2))*Graph==S.eye(2))
ck('nonmetabolic_discriminant',isqrt(5)**2!=5)
ck('normalized_order_two_polynomial',S.expand((V0-t*V0.T).det()/t)==3-t-1/t)
H=S.Matrix([[e,1],[0,0]])
ck('metabolic_block',S.expand((H-t*H.T).det()/t)==1 and H[1,1]==0)
for z in (-2,-1,0,1,2):
    W=S.diag(V0,H.subs(e,z))
    ck('stable_polynomial',S.expand((W-t*W.T).det()/t**2)==3-t-1/t)
# Hermitian conjugation fixes every symmetric rational Alexander polynomial.
u,v=S.symbols('u v')
D=1+u*(t+1/t-2)+v*(t*t+1/(t*t)-2)
ck('symmetric_D',S.simplify(D.subs(t,1/t)-D)==0)
Change=S.diag(1/D,1)
ck('witt_hyperbolic_congruence',S.simplify(Change.T.subs(t,1/t)*S.diag(D**2,-1)*Change)==S.diag(1,-1))
C=S.Matrix([[0,1-t],[1-1/t,-(1-t)*(1-1/t)]])
ck('crossing_block_hermitian',S.simplify(C.T.subs(t,1/t)-C)==S.zeros(2))
ck('crossing_block_isotropic',C[0,0]==0 and S.simplify(C.det())!=0)

# Independent continuant recursion, rather than matrix products, for every
# signed word of length <=5 with coefficients -2..2, at every genuine crossing.
def cf(word):
    p,q=1,0
    for z in reversed(word):p,q=z*p+q,p
    return p,q

def prefix_matrix(word):
    a,c=cf(word)
    b,d=cf(word[:-1]) if word else (0,1)
    return a,b,c,d

cases=0;preserved=0;branches={'same':0,'opposite':0,'zero_prefix':0,'zero_suffix':0,'nontrivial_ribbon':0}
for length in range(1,6):
    for word in product(range(-2,3),repeat=length):
        p,q=cf(word)
        for i,x in enumerate(word):
            if x==0:continue
            eps=1 if x>0 else -1
            changed=word[:i]+(x-2*eps,)+word[i+1:]
            pp,qq=cf(changed)
            a,b,c,d=prefix_matrix(word[:i]);u,w=cf(word[i+1:]);delta=a*d-b*c
            cases+=1
            ck('continuant_update',(pp,qq)==(p-2*eps*a*u,q-2*eps*c*u))
            ck('continuant_primitive',abs(delta)==1 and gcd(p,q)==gcd(pp,qq)==gcd(u,w)==1)
            if p==0 or p%2==0 or abs(p)!=abs(pp):continue
            preserved+=1
            if p==pp:
                branches['same']+=1
                branches['zero_prefix']+=int(a==0);branches['zero_suffix']+=int(u==0)
                ck('degenerate_preserving_case',a*u==0 and (qq-q)%abs(p)==0)
            else:
                branches['opposite']+=1
                ck('opposite_divisibility',a*u!=0 and u in (a,-a) and abs(p)==a*a)
                eta=u//a
                ck('signed_denominator_formula',q==eta*(eps*a*c+delta))
                qn=(1 if p>0 else -1)*q
                qpn=(1 if pp>0 else -1)*qq
                ck('normalized_denominators',qn==a*c+eps*delta and qpn==a*c-eps*delta)
                ck('mirror_inverse_residue',(qn*qpn+1)%abs(p)==0)
                m=abs(a)
                if m>1:
                    branches['nontrivial_ribbon']+=1
                    k=((1 if a>0 else -1)*c)%m
                    target=m*k+eps*delta
                    ck('ribbon_parameters',m%2==1 and 0<k<m and gcd(k,m)==1)
                    ck('ribbon_residue',qn%(m*m)==target and 0<target<m*m and gcd(target,m*m)==1)
# The equality-of-determinants branches used above are genuinely exercised.
for name in branches:ck('branch_coverage_'+name,branches[name]>0)
ck('explicit_example',cf((3,-1,-3))==(9,4) and cf((3,1,-3))==(-9,-2))

# Direct, independent matrix proof of the symmetric-union numerator identity.
m,k,b,d,eps=S.symbols('m k b d eps')
Q=S.Matrix([[m,b],[k,d]]);J=S.diag(1,-1);Middle=S.Matrix([[eps,1],[1,0]])
column=S.expand(Q*Middle*J*Q.T*J)[:,0]
ck('symmetric_union_general_column',column==S.Matrix([eps*m*m,eps*m*k+m*d-b*k]))
for n in range(1,5):
    for w in product((-2,-1,1,2),repeat=n):
        m,k=cf(w);delta=(-1)**n
        for ep in (-1,1):
            p,q=cf(w+(ep,)+tuple(-z for z in reversed(w)))
            ck('symmetric_union_signed_identity',(p,q)==(ep*delta*m*m,ep*delta*m*k+1))

root=Path(__file__).parent
out={'problem_id':10400229,'status':'PASS_INDEPENDENT_EXACT_CONTROLS','assertions':sum(counts.values()),'groups':counts,
     'continued_fraction_crossings':cases,'odd_determinant_preserving_crossings':preserved,'branches':branches,
     'artifact_sha256':hashlib.sha256((root/'author_replay/PARTIAL.md').read_bytes()).hexdigest(),
     'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     'scope':'Symbolic Seifert/Witt calculations and exact signed continuants only. No prime-knot recognition, arbitrary crossing conversion, or complete geometric ribbon theorem is certified computationally.'}
print(json.dumps(out,indent=2,sort_keys=True))

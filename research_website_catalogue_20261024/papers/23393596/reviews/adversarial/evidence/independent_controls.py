#!/usr/bin/env python3
"""Fresh source-free braid controls: only primary mathematical definitions are used.
No submitted helper is imported or opened. Exact arithmetic throughout.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
from itertools import combinations
from datetime import datetime, timezone
import json, hashlib
import sympy as S
OUT=Path(__file__).resolve().parent

def inv(w): return [-i for i in w[::-1]]
def red(w):
    r=[]
    for x in w:
        if r and r[-1]==-x:r.pop()
        else:r.append(x)
    return r
def mul(*w):return red(sum(w,[]))
def comm(a,b):return mul(a,b,inv(a),inv(b))
a,b=[1,1],[2,2]
c=comm(a,b);d=mul(inv(a),c,a);e=mul(inv(b),c,b)
u,v=comm(c,d),comm(d,e);beta=comm(u,v)

def labelled_crossings(w,m=3):
    p=list(range(1,m+1));signed=defaultdict(int,{pair:0 for pair in combinations(p,2)})
    for t in w:
        i=abs(t)-1; pair=tuple(sorted((p[i],p[i+1])))
        signed[pair]+=1 if t>0 else -1
        p[i],p[i+1]=p[i+1],p[i]
    return p,{str(k):v for k,v in sorted(signed.items())}

def blocks(w):
    out=[]
    for x in w:
        if out and abs(out[-1][0])==abs(x):out[-1][1]+=1 if x>0 else -1
        else:out.append([abs(x),1 if x>0 else -1])
    assert all(t[1] for t in out)
    assert all(t[0]==(1 if i%2==0 else 2) for i,t in enumerate(out))
    assert len(out)%2==0
    return [t[1] for t in out[::2]],[t[1] for t in out[1::2]]

def goeritz(A,B,wrong_previous=False):
    n=sum(map(abs,B));G=S.zeros(n);start=0
    for j,(aa,bb) in enumerate(zip(A,B)):
        G[start,start]+=aa
        # Incidence vector of every actual sigma_2 crossing; coincident regions cancel.
        sign=1 if (B[j-1] if wrong_previous else bb)>0 else -1
        for k in range(abs(bb)):
            edge=S.zeros(n,1);edge[(start+k)%n]+=1;edge[(start+k+1)%n]-=1
            G-=sign*(edge*edge.T)
        start+=abs(bb)
    return G

def variation(seq):
    signs=[S.sign(x) for x in seq if x]
    return sum(x!=y for x,y in zip(signs,signs[1:]))

def characteristic_inertia(G):
    # Symmetry makes all roots real; Descartes sign variations are exact here.
    coeff=list(G.charpoly().all_coeffs());zeros=0
    while len(coeff)>1 and coeff[-1]==0:coeff.pop();zeros+=1
    n=len(coeff)-1
    pos=variation(coeff);neg=variation([x*((-1)**(n-i)) for i,x in enumerate(coeff)])
    assert pos+neg+zeros==G.rows
    return (pos,neg,zeros),coeff

I=S.eye(2);X=S.Matrix([[1,0],[-1,1]]);Y=S.Matrix([[1,1],[0,1]])
def matletter(t):return (X if abs(t)==1 else Y)**(1 if t>0 else -1)
def burau(w):
    P=I
    for t in w:P=P*matletter(t)
    return P

def meyer(A,B):
    U=A.inv()-I;V=I-B
    common=[]
    for z in U.row_join(-V).nullspace():
        w=U*z[:2,0]
        if w!=S.zeros(2,1):common.append(w)
    E=S.Matrix.hstack(*common).columnspace() if common else []
    if not E:return 0
    lifts=[]
    for w in E:
        lift=[]
        for C in (U,V):
            solution,params=C.gauss_jordan_solve(w)
            lift.append(solution.subs({t:0 for t in params}))
        lifts.append(lift[0]+lift[1])
    Q=S.Matrix(len(E),len(E),lambda i,j:S.det(S.Matrix.hstack(lifts[i],E[j])))
    Q=(Q+Q.T)/2
    inert,_=characteristic_inertia(Q)
    return inert[0]-inert[1]

def signature(w):
    P=I;s=0;steps=[]
    for t in w:
        B=matletter(t);m=meyer(P,B);s-=m;P=P*B;steps.append(m)
    return s,P,steps

# Faithful free-group Artin action, used only on short identities to avoid exponential words.
def substitute(w,imgs):return mul(*[imgs[t-1] if t>0 else inv(imgs[-t-1]) for t in w])
def artin(w):
    imgs=[[1],[2],[3]]
    for t in w:
        i=abs(t)-1;T=[[1],[2],[3]]
        if t>0:T[i]=[i+1,i+2,-i-1];T[i+1]=[i+1]
        else:T[i]=[i+2];T[i+1]=[-i-2,i+1,i+2]
        imgs=[substitute(z,T) for z in imgs]
    return imgs

A,B=blocks(beta);G=goeritz(A,B)
inertia,poly=characteristic_inertia(G)
sig,P,steps=signature(beta)
assert len(beta)==104 and len(A)==23 and G.rows==48
assert inertia==(23,25,0) and sum(A)==0 and sig==-2
assert int(G.det())==-7154819319988224
assert P==S.Matrix([[-1401703009468415,3686720931790848],[2187353096552448,-5753116310519807]])
assert labelled_crossings(beta)==([1,2,3],{'(1, 2)':0,'(1, 3)':0,'(2, 3)':0})
assert all(i==0 for i in labelled_crossings(beta,6)[1].values())
assert artin([1,2,1])==artin([2,1,2])
h=mul([2],a,[-2]);z=[1,2]*3
assert artin(mul(a,h,b))==artin(z)

controls=[]
for word,name,expected in [([], 'identity',0),([1]*3,'positive trefoil with split unknot',-2),([-1]*3,'negative trefoil with split unknot',2),([1,2]*6,'Delta_3^4',-8),(inv(beta),'inverse witness',2),([-t for t in beta],'mirror witness',2)]:
    s,_,_=signature(word);assert s==expected;controls.append({'name':name,'signature':s})
for ell in range(1,9):
    assert signature([1]*ell)[0]==1-ell
for r in range(1,5):assert signature(z*(2*r))[0]==-8*r
for r in range(1,4):assert abs(F(signature(beta*r)[0],r)-F(sig))<=6
# Goeritz calibration includes the small N=1,2 region-coincidence cases.
for aa,bb in [(1,1),(3,1),(2,2),(1,3),(-2,3),(2,-3),(-1,-1)]:
    word=([1]*aa if aa>0 else [-1]*(-aa))+([2]*bb if bb>0 else [-2]*(-bb))
    H=goeritz([aa],[bb]);inert,_=characteristic_inertia(H)
    assert inert[0]-inert[1]-aa==signature(word)[0]
# Selected short Artin words and an eight-letter prefix check braid relations,
# inverse signatures, cancellation, and conjugacy, with no submitted outputs.
short_checks=0
for w in [[],[1],[2],[-1],[1,2],[1,-2],[2,2],[-1,2,1],[1,1,2,2],beta[:8]]:
    s=signature(w)[0]
    assert signature(inv(w))[0]==-s
    assert signature([1]+w+[-1])[0]==s
    assert signature(w+[1,-1])[0]==s
    assert signature(w+[1,2,1])[0]==signature(w+[2,1,2])[0]
    short_checks+=4
wrong=goeritz(A,B,wrong_previous=True);wi,_=characteristic_inertia(wrong)
# A deliberately uncorrected previous-block off-diagonal transcription is not the diagram.
wrong_off=G.copy();start=0
for j,bb in enumerate(B):
    old=1 if bb>0 else -1;prev=1 if B[j-1]>0 else -1
    for k in range(abs(bb)):
        i=(start+k)%48;q=(i+1)%48
        wrong_off[i,q]+=prev-old;wrong_off[q,i]+=prev-old
    start+=abs(bb)
woi,_=characteristic_inertia(wrong_off)
assert wrong_off!=G
# A changed generator loses purity/linking/derived input, even if signature survives.
mut=beta.copy();mut[0]=-mut[0]
assert any(labelled_crossings(mut)[1].values())
# UCT boundary control: C2 --2--> C1 has integral H2=0 and H1=Z/2,
# but mod2 H2=F2. Dropping torsion-freeness invalidates the 2r upper bound.
uct={'boundary_matrix':[[2]],'rank_Q':1,'rank_F2':0,'H2_Z_rank':0,'H2_F2_dimension':1,'H1_Z':'Z/2'}
# A single hyperbolic local pair is independent despite negative dual coefficient.
assert S.Matrix([[0,-1],[-1,0]]).det()==-1
# Reducible / zero-dimensional controls establish no acyclicity requirement.
assert characteristic_inertia(S.zeros(0))[0]==(0,0,0)
result={'utc':datetime.now(timezone.utc).isoformat(),'helper_sources_read':False,'sympy_version':S.__version__,
'word':beta,'length':len(beta),'A':A,'B':B,'derived_expression_levels':{'a':0,'b':0,'c':1,'d':1,'e':1,'u':2,'v':2,'beta':3},
'purity_linking':labelled_crossings(beta),'added_strands':labelled_crossings(beta,6),
'goeritz':{'dimension':48,'inertia':inertia,'determinant':str(G.det()),'correction':sum(A),'characteristic_coefficients':[str(t) for t in poly]},
'meyer':{'signature':sig,'burau_matrix':[[str(P[i,j]) for j in range(2)] for i in range(2)],'increments':steps},
'controls':controls,'relation_inverse_conjugacy_cancellation_checks':short_checks,
'previous_block_all_edges_mutant':{'inertia':wi,'same_matrix':wrong==G},
'printed_off_diagonal_index_mutant':{'inertia':woi,'determinant':str(wrong_off.det())},
'one_crossing_sign_mutant_linking':labelled_crossings(mut),
'UCT_torsion_boundary_control':uct,
'limits':'Finite algebraic checks are not proofs of all-depth persistence or universal topology. Those are reconstructed analytically in the review.'}
(OUT/'independent-controls.json').write_text(json.dumps(result,indent=2)+'\n')
(OUT/'goeritz-matrix.json').write_text(json.dumps([[int(t) for t in G.row(i)] for i in range(48)],indent=2)+'\n')
print(json.dumps({k:result[k] for k in ('utc','length','purity_linking','controls','relation_inverse_conjugacy_cancellation_checks','printed_off_diagonal_index_mutant')},indent=2))
print('PASS independent exact controls; no submitted helper source read')

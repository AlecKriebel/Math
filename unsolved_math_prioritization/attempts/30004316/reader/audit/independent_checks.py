"""Independent audit from original X-basis and finite-field Fourier bases.
No imported source archive or candidate program. Python stdlib + SymPy.
"""
from itertools import product
from collections import defaultdict, deque
from fractions import Fraction
from pathlib import Path
import argparse
import json, hashlib
import sympy as sp


def require(condition, detail):
    """Keep each finite check active under normal Python, -O, and -OO."""
    if not condition:
        raise AssertionError(detail)
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path, help='optional JSON output path; default: stdout only')
args = parser.parse_args()

def words(n): return list(product(range(4),repeat=n))
def cross(w,j):
    v=list(w); v[j],v[j+1]=v[j+1],(v[j]+1)%4; return tuple(v)
def matrix(n,terms):
    ws=words(n); pos={w:j for j,w in enumerate(ws)}
    M=sp.zeros(len(ws))
    for j,w in enumerate(ws):
        for s,path in terms:
            v=w
            for a in path: v=cross(v,a)
            M[pos[v],j]+=s
    return M
q2=matrix(2,[(1,()),(-1,(0,))])
q3=matrix(3,[(1,()),(-1,(0,)),(-1,(1,)),(1,(0,1)),(1,(1,0)),(-1,(0,1,0))])
# Pair orbit relation basis, without symmetrizer image calculations.
ws2=words(2); p2={w:j for j,w in enumerate(ws2)}
unseen=set(ws2); orbits=[]
while unseen:
    root=min(unseen); orb=[]; w=root
    while w not in orb: orb.append(w); w=cross(w,0)
    unseen.difference_update(orb); orbits.append(sorted(orb))
oc={w:j for j,o in enumerate(orbits) for w in o}
R=[]
for o in orbits:
    for w in o[1:]:
        v=sp.zeros(16,1); v[p2[w]]=1; v[p2[o[0]]]=-1; R.append(v)
R=sp.Matrix.hstack(*R)
# Adjacent product constraints for K3.
ws3=words(3); constraints=sp.zeros(16,64)
for j,(a,b,c) in enumerate(ws3):
    constraints[oc[a,b]*4+c,j]=1
    constraints[8+a*2+oc[b,c],j]=1
# Weight-3 d2, using independent orbit-difference bases of R.
d2=sp.zeros(80,112)
for a in range(4):
    for ri in range(14):
        col=a*14+ri
        for (b,c),coef in zip(ws2,R[:,ri]):
            if coef:
                d2[oc[a,b]*4+c,col]+=coef
                d2[8+a*16+b*4+c,col]+=coef
for ri in range(14):
    for c in range(4):
        col=56+ri*4+c
        for (a,b),coef in zip(ws2,R[:,ri]):
            if coef:
                d2[8+a*16+b*4+c,col]+=coef
                d2[72+a*2+oc[b,c],col]+=coef
# Explicit rational witnesses, built by tensor products.
t=sp.ones(4,1); a=sp.Matrix([1,0,-1,0]); b=sp.Matrix([0,1,0,-1])
v_re=sp.kronecker_product(t,sp.kronecker_product(a,a)-sp.kronecker_product(b,b))
v_im=-sp.kronecker_product(t,sp.kronecker_product(a,b)+sp.kronecker_product(b,a))
require(constraints*q3==sp.zeros(16,64), 'check failed at original line 64')
require(constraints*v_re==sp.zeros(16,1) and constraints*v_im==sp.zeros(16,1), 'check failed at original line 65')

def modrank(M,p):
    rows=[[int(x)%p for x in row] for row in M.tolist()]
    rank=0; ncols=len(rows[0]) if rows else 0
    for col in range(ncols):
        pivot=next((j for j in range(rank,len(rows)) if rows[j][col]),None)
        if pivot is None: continue
        rows[rank],rows[pivot]=rows[pivot],rows[rank]
        fac=pow(rows[rank][col],-1,p)
        rows[rank]=[(x*fac)%p for x in rows[rank]]
        for j in range(rank+1,len(rows)):
            if rows[j][col]:
                fac=rows[j][col]
                rows[j]=[(x-fac*y)%p for x,y in zip(rows[j],rows[rank])]
        rank+=1
        if rank==len(rows): break
    return rank

# Original X-basis faces, using explicit repeated braid operations.
def dX(w):
    out=defaultdict(int); n=len(w)
    for j in range(n):
        left=w
        for s in range(j-1,-1,-1): left=cross(left,s)
        right=w
        for s in range(j,n-1): right=cross(right,s)
        out[left[1:]]+=(-1)**j; out[right[:-1]]-=(-1)**j
    return {w:c for w,c in out.items() if c}
def dX_simplified(w):
    out=defaultdict(int)
    for j in range(len(w)):
        left=tuple((v+1)%4 for v in w[:j])+w[j+1:]
        right=w[:j]+w[j+1:]
        out[left]+=(-1)**j; out[right]-=(-1)**j
    return {w:c for w,c in out.items() if c}
for n in range(7):
    for w in words(n): require(dX(w)==dX_simplified(w), 'check failed at original line 102')

# Fourier checks in every selected odd finite field containing i, independent
# of the Q(i) implementation in the candidate. Repeated crossings define faces.
def finite_field_fourier_check(p,I,max_n=7):
    lam=[pow(I,j,p) for j in range(4)]
    def add(out,w,c):
        out[w]=(out.get(w,0)+c)%p
        if not out[w]: del out[w]
    def faceD(w):
        out={}
        for j in range(len(w)):
            sign=(-1)**j
            left=list(w); cl=1
            for s in range(j-1,-1,-1):
                cl=cl*lam[left[s]]%p; left[s],left[s+1]=left[s+1],left[s]
            if left[0]==0: add(out,tuple(left[1:]),sign*4*cl)
            right=list(w); cr=1
            for s in range(j,len(w)-1):
                cr=cr*lam[right[s]]%p; right[s],right[s+1]=right[s+1],right[s]
            if right[-1]==0: add(out,tuple(right[:-1]),-sign*4*cr)
        return out
    def formulaD(w):
        out={}; prefix=1
        for j,x in enumerate(w):
            if x==0: add(out,w[:j]+w[j+1:],(-1)**j*4*(prefix-1))
            prefix=prefix*lam[x]%p
        return out
    def H(w):
        nz=next((j for j,x in enumerate(w) if x),None)
        if nz is None: return {}
        gap=0
        while nz+1+gap<len(w) and w[nz+1+gap]==0: gap+=1
        if gap%2: return {}
        c=((-1)**(nz+1)*pow(4*(lam[w[nz]]-1)%p,-1,p))%p
        return {w[:nz+1]+(0,)+w[nz+1:]:c}
    def extend(f,v):
        out={}
        for w,c in v.items():
            for u,d in f(w).items(): add(out,u,c*d)
        return out
    count=0
    for n in range(max_n+1):
        for w in words(n):
            dd=faceD(w); require(dd==formulaD(w), (p,w,dd,formulaD(w)))
            require(extend(faceD,dd)=={}, (p,w,'d2'))
            dh=extend(faceD,H(w)); hd=extend(H,dd)
            for u,c in hd.items(): add(dh,u,c)
            want={} if all(x==0 for x in w) else {w:1}
            require(dh==want, (p,w,dh,want))
            count+=1
    return {'prime':p,'i':I,'max_word_degree':max_n,'words_checked':count,'face_formula_d_squared_and_dh_plus_hd':True}

# Fourier degree-3 block recovered from original X-basis matrix.
I=sp.I
us=[sp.Matrix([I**(-j*x) for x in range(4)]) for j in range(4)]
W=sp.Matrix.hstack(*(sp.kronecker_product(us[x],us[y],us[z]) for x,y,z in [(1,1,0),(1,0,1),(0,1,1)]))
FW=(W.conjugate().T*W).inv()*W.conjugate().T*q3*W
FW=FW.applyfunc(sp.simplify)
require((q3*W-W*FW).applyfunc(sp.simplify)==sp.zeros(64,3), 'check failed at original line 161')
ell=sp.Matrix([[I,1+I,1]])
require((ell*FW).applyfunc(sp.simplify)==sp.zeros(1,3), 'check failed at original line 163')
minor=sp.simplify(FW[:2,:2].det()); require(minor==-2*I, 'check failed at original line 164')

results={
 'independent_method':'Original X-basis relation orbits, signed six-term braid sum, and original-basis braided faces. No source ZIP or candidate program execution.',
 'rational':{'pair_orbit_sizes':list(map(len,orbits)),'QS2_rank':q2.rank(),'QS3_rank':q3.rank(),'K3_dimension':64-constraints.rank(),'QS3_with_two_witnesses_rank':q3.row_join(v_re).row_join(v_im).rank(),'C2_weight3_dimension':112,'d2_weight3_rank':d2.rank(),'H2_weight3_dimension':112-d2.rank()-q3.rank()},
 'Fourier_Q3_matrix':[[str(x) for x in row] for row in FW.tolist()],
 'Fourier_annihilator':['i','1+i','1'],'Fourier_2by2_minor':str(minor),
 'odd_prime_rank_checks':[{'p':p,'Q3_rank':modrank(q3,p),'K3_dimension':64-modrank(constraints,p),'Q3_plus_witnesses_rank':modrank(q3.row_join(v_re).row_join(v_im),p),'d2_rank':modrank(d2,p)} for p in [3,5,7,11,13,17,19]],
 'original_X_faces_checked_words':sum(4**n for n in range(7)),
 'finite_field_contraction':[finite_field_fourier_check(p,I) for p,I in [(5,2),(13,5),(17,4)]],
 'limits':'Finite checks supplement the all-degree proof. No census, global-dimension theorem, source archive program, exhaustive literature, characteristic-two, or constrained algebra-ideal quotient certification.'
}
payload = json.dumps(results, indent=2) + '\n'
if args.output is not None:
    args.output.write_text(payload, encoding='utf-8')
print(payload, end='')

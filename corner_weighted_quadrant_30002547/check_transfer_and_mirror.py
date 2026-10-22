"""Exact, finite sanity checks for Attempts 1 and 4; not asymptotic evidence."""
from itertools import product
from collections import defaultdict
import json

D = 'ENWS'
V = {'E':(1,0), 'N':(0,1), 'W':(-1,0), 'S':(0,-1)}
NEG = dict(zip('ENWS','WSEN'))
CORNERS = {('N','W'),('E','S')}

def corners(w):
    return sum((x,y) in CORNERS for x,y in zip(w,w[1:]))
def revneg(w):
    return ''.join(NEG[d] for d in reversed(w))
def vertices(w):
    x=y=0
    result=[(x,y)]
    for d in w:
        dx,dy=V[d]; x+=dx; y+=dy
        result.append((x,y))
    return result

checks={}
# Every local pair is reverse-negation invariant.
assert all(((i,j) in CORNERS)==((NEG[j],NEG[i]) in CORNERS) for i in D for j in D)
checks['reverse_negation_pairs']=16
# Check mirrors exhaustively through n=4, grouped as in the proof.
count=0
for n in range(1,5):
    H=n
    classes=defaultdict(list)
    for ds in product(D,repeat=n):
        w=''.join(ds)
        classes[(vertices(w)[-1],w[0],w[-1])].append(w)
    for (_,f,_),words in classes.items():
        A=('N'*H+'E'*H) if f=='W' else ('E'*H+'N'*H)
        images=set()
        for p in words:
            for q in words:
                w=A+p+revneg(q)+revneg(A)
                vs=vertices(w)
                assert vs[-1]==(0,0)
                assert all(x>=0 and y>=0 for x,y in vs)
                assert len(w)==2*n+4*H
                assert corners(w)==corners(p)+corners(q)
                assert w not in images
                images.add(w); count+=1
checks['mirror_ordered_pairs_through_length_4']=count
# Check exact displacement coefficients by exponent-count polynomials.
for L in range(1,9):
    coeff=defaultdict(int)
    for ds in product(D,repeat=L):
        w=''.join(ds)
        if vertices(w)[-1]==(-1,L-1):
            coeff[corners('N'+w)]+=1
    assert dict(coeff)=={1:L}
checks['negative_block_identity_lengths']=list(range(1,9))
# Exact quadrant polynomials through half-length 8.
state={(0,0,''): [1]}
polys={0:[1]}
for length in range(1,17):
    new={}
    for (x,y,last),p in state.items():
        for d in D:
            dx,dy=V[d]; xx,yy=x+dx,y+dy
            if xx<0 or yy<0: continue
            shift=int((last,d) in CORNERS)
            key=(xx,yy,d)
            q=new.setdefault(key,[0]*(len(p)+shift))
            if len(q)<len(p)+shift:q.extend([0]*(len(p)+shift-len(q)))
            for k,c in enumerate(p):q[k+shift]+=c
    state=new
    if length%2==0:
        q=[]
        for (x,y,_),p in state.items():
            if x or y:continue
            if len(q)<len(p):q.extend([0]*(len(p)-len(q)))
            for k,c in enumerate(p):q[k]+=c
        while q and q[-1]==0:q.pop()
        polys[length//2]=q
checks['Q_n_coefficients_ascending_a']=polys
print(json.dumps(checks,indent=2))

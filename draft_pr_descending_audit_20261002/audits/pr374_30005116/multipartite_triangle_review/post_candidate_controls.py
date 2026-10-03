"""Own supplemental controls after candidate prose, before author-code replay."""
from fractions import Fraction as Q
from itertools import combinations, product
from independent_controls import densities

edges4=list(combinations(range(4),2))
for bits in product([0,1],repeat=6):
    selected={e for e,b in zip(edges4,bits) if b}
    degrees=[sum(i in e for e in selected) for i in range(4)]
    c4=int(sorted(degrees)==[2,2,2,2])
    match=sum(all(e in selected for e in matching) for matching in [((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))])
    assert 2*c4<=match
print('Matching inequality: all 64 four-vertex graphs PASS')

def mul(u,v,d): return (u[0]*v[0]+u[1]*v[1]*d,u[0]*v[1]+u[1]*v[0])
def fourth(u,d): return mul(mul(u,u,d),mul(u,u,d),d)
radicals=0
for denom in range(2,70):
    for num in range(1,denom+1):
        q=Q(num,denom); r=int(1/q); d=((r+1)*q-1)/r
        a=(Q(1,r+1),Q(1,r+1)); b=(Q(1,r+1),Q(-r,r+1))
        aa=fourth(a,d); bb=fourth(b,d)
        A=(1+6*r*d+r*(r*r-r+1)*d*d)/(r+1)**3
        B=4*r*(r-1)*d/(r+1)**3
        assert (r*aa[0]+bb[0],r*aa[1]+bb[1])==(A,-B)
        radicals+=1
print('Exact quadratic-field expansion cases:',radicals)

def partitions(n,minimum=1):
    if n==0: yield ()
    for z in range(minimum,n+1):
        for rest in partitions(n-z,z): yield (z,)+rest
finite=0
for n in range(4,13):
    for part in partitions(n):
        labels=[i for i,size in enumerate(part) for _ in range(size)]
        direct=sum(sorted([sum(labels[s]!=labels[t] for t in verts if t!=s) for s in verts])==[2,2,2,2] for verts in combinations(range(n),4))
        q=sum(Q(z,n)**2 for z in part); p3=sum(Q(z,n)**3 for z in part); p4=sum(Q(z,n)**4 for z in part)
        assert Q(24*direct,n**4)==3*(q*q-p4)+6*(p3-q)/n+3*(1-q)/n**2
        finite+=1
print('Exact finite-size identity direct induced-subset cases:',finite)

multijoin=0
templates=[[],[(0,1)],[(0,1),(1,2)]]
w=[Q(2,5),Q(3,5)]
local=[Q(1,4),Q(1,4),Q(1,2)]
for e1,e2 in product(templates,repeat=2):
    d1=densities(local,e1);d2=densities(local,e2)
    allw=[w[0]*a for a in local]+[w[1]*a for a in local]
    edges=list(e1)+[(a+3,b+3) for a,b in e2]+list(product(range(3),range(3,6)))
    actual=densities(allw,edges)
    p=1-sum(ww*ww*(1*1-dd['edge']) for ww,dd in zip(w,[d1,d2]))
    c=w[0]**4*d1['C4']+w[1]**4*d2['C4']+6*w[0]**2*w[1]**2*(1-d1['edge'])*(1-d2['edge'])
    assert actual['edge']==p and actual['C4']==c
    multijoin+=1
print('Multiple low-density block complete-join cases:',multijoin)
author_example=densities([Q(4,9),Q(2,9),Q(2,9),Q(1,9)],[(0,1),(0,2),(0,3),(1,2)])
assert author_example['edge']==Q(16,27)
assert author_example['C4']==Q(64,243)
assert author_example['triangle']==Q(32,243)
print('Author rational tie values independently PASS')
print('Candidate verifier imports: 0; PDF reads: 0')

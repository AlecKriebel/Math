"""Independent, exact matrix/witness checks for the structural referee report.
Standard library only; does not import the submitted verifiers or certificates.
"""
from collections import deque, Counter
import json
from pathlib import Path

P = 29
I = (1,0,0,1)
Z = (28,0,0,28)
A = (0,28,1,0)
B = (2,7,12,28)
def mul(a,b,p=P):
    x,y,z,w = a
    q,r,s,t = b
    return ((x*q+y*s)%p,(x*r+y*t)%p,(z*q+w*s)%p,(z*r+w*t)%p)
def power(a,n,p=P):
    out=I
    for _ in range(n): out=mul(out,a,p)
    return out
def closure(gs,p=P):
    result={I}; todo=deque([I])
    while todo:
        a=todo.popleft()
        for b in gs:
            c=mul(a,b,p)
            if c not in result:
                result.add(c); todo.append(c)
    return result
def order(a):
    n=1; c=a
    while c!=I:
        n+=1; c=mul(c,a)
    return n
def act(a,v):
    return ((a[0]*v[0]+a[1]*v[1])%P,(a[2]*v[0]+a[3]*v[1])%P)
H=closure([A,B]); assert len(H)==120
assert all((a[0]*a[3]-a[1]*a[2])%P==1 for a in H)
assert power(A,2)==power(B,3)==power(mul(A,B),5)==Z
assert [a for a in H if a!=I and power(a,2)==I]==[Z]
R=[A,(12,24,0,17),(25,3,4,4)]
assert R[1]==mul(mul(B,A),power(B,2))
assert R[2]==mul(mul(A,R[1]),power(mul(A,B),2))
assert all(a in H and power(a,2)==Z for a in R)
Q=[closure([R[j] for j in range(3) if j!=i]) for i in range(3)]
assert [len(q) for q in Q]==[8,12,20]
assert [order(mul(R[1],R[2])), order(mul(R[0],R[2])),order(mul(R[0],R[1]))]==[4,3,10]
assert len(closure(R))==120
assert Q[0]&Q[1]==closure([R[2]])
assert Q[0]&Q[1]&Q[2]=={I,Z}
assert all(R[i] not in Q[i] for i in range(3))
lines=[{(a,a*t%P) for a in range(P)} for t in range(P)]+[{(0,a) for a in range(P)}]
stabilizers=[]
for w in lines:
    v=next(v for v in w if v!=(0,0))
    hw={a for a in H if act(a,v) in w}
    assert len(hw)==4 and any(order(a)==4 for a in hw)
    stabilizers.append(len(hw))
assert {a for a in H if act(a,(1,0))==(1,0)}=={I}
# Independent paired Cayley traversal checks the claimed SL_2(5) isomorphism.
A5=(0,4,1,0); B5=(0,4,1,1)
paired={(I,I)}; todo=deque(paired)
while todo:
    x,y=todo.popleft()
    for s,t in [(A5,A),(B5,B)]:
        u=(mul(x,s,5),mul(y,t))
        if u not in paired:
            paired.add(u); todo.append(u)
SL5={(a,b,c,d) for a in range(5) for b in range(5) for c in range(5) for d in range(5) if (a*d-b*c)%5==1}
assert len(paired)==120
assert {x for x,y in paired}==SL5 and {y for x,y in paired}==H
# Faithful three-family: enumerate the translation and involution cosets.
def affine_line(w,c):
    return {((a*w[0]%P,a*w[1]%P),I) for a in range(P)}|{(((a*w[0]+c[0])%P,(a*w[1]+c[1])%P),Z) for a in range(P)}
L=[affine_line((1,0),(0,0)),affine_line((0,1),(0,0)),affine_line((1,1),(2,0))]
e=((0,0),I)
assert [len(x) for x in L]==[58]*3
assert L[0]&L[1]=={e,((0,0),Z)}
assert L[0]&L[2]=={e,((2,0),Z)}
assert L[1]&L[2]=={e,((0,27),Z)}
assert L[0]&L[1]&L[2]=={e}
# Characteristic-11 boundary example.
p=11; aa=(0,10,1,0); bb=(0,2,5,1); cc=(6,10,0,2)
h11=closure([aa,bb],p)
assert len(h11)==120 and cc in h11
assert power(cc,10,p)==I and all(power(cc,d,p)!=I for d in [1,2,5])
def act11(a,v): return ((a[0]*v[0]+a[1]*v[1])%11,(a[2]*v[0]+a[3]*v[1])%11)
w1={(a,0) for a in range(11)}; w2={(a,4*a%11) for a in range(11)}
assert {act11(cc,v) for v in w1}==w1 and {act11(cc,v) for v in w2}==w2
v11={(a,b) for a in range(11) for b in range(11)}
l11=[{(v,h) for v in w for h in k} for w,k in [(w1,closure([cc],11)),(w2,closure([cc],11)),(v11,closure([power(cc,5,11)],11)),(v11,closure([power(cc,2,11)],11))]]
assert set.intersection(*l11)=={e}
assert [len(set.intersection(*(l11[j] for j in range(4) if j!=i))) for i in range(4)]==[11,11,5,2]
result={'complement_order':len(H),'element_order_distribution':dict(sorted(Counter(map(order,H)).items())),'pair_orders':[len(q) for q in Q],'pair_product_orders':[order(mul(R[1],R[2])),order(mul(R[0],R[2])),order(mul(R[0],R[1]))],'line_stabilizer_orders':dict(Counter(stabilizers)),'faithful_family_orders':[len(x) for x in L],'sl2_5_isomorphism_checked':True,'characteristic_11_deletion_orders':[11,11,5,2],'assertions':'all passed'}
print(json.dumps(result,indent=2))
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')

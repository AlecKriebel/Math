"""Independent exact source-word and quaternion controls. No author code imported."""
from fractions import Fraction as F
from collections import Counter
import json
Cts=Counter()
def ck(value,name):
    assert value,name
    Cts[name]+=1

def red(w):
    a=[]
    for x in w:
        if a and a[-1]==-x:a.pop()
        else:a.append(x)
    return tuple(a)
def inv(w):return tuple(-x for x in w[::-1])
def sub(w,G):return red(sum((G[abs(x)-1] if x>0 else inv(G[-x-1]) for x in w),()))
def compose(F,G):return tuple(sub(w,F) for w in G)
Id=((1,),(2,),(3,),(4,))
A=((3,1),(2,),(3,),(4,));B=((1,),(2,),(-2,-1,3),(4,));C=((1,),(2,3,4),(3,),(4,));D=((1,),(2,),(3,),(4,-2));E=((1,-4),(4,2),(3,),(4,))
Ai=((-3,1),(2,),(3,),(4,));Bi=((1,),(2,),(1,2,3),(4,));Ci=((1,),(2,-4,-3),(3,),(4,));Di=((1,),(2,),(3,),(4,2));Ei=((1,4),(-4,2),(3,),(4,))
r=(-1,-3,1,2,3,4,-2,-4)
rels=tuple(w[i:]+w[:i] for w in (r,inv(r)) for i in range(8))
# Only positive relation proofs are used. No completeness of this reducer is assumed.
def shorten(w):
    w=red(w);steps=[]
    while True:
        changed=False
        for l in range(8,4,-1):
            for i in range(len(w)-l+1):
                for rel in rels:
                    if w[i:i+l]==rel[:l]:
                        old=w;w=red(w[:i]+inv(rel[l:])+w[i+l:]);steps.append([list(old),i,l,list(rel),list(w)])
                        changed=True;break
                if changed:break
            if changed:break
        if not changed:return w,steps
for G,Gi in zip((A,B,C,D,E),(Ai,Bi,Ci,Di,Ei)):
    ck(compose(G,Gi)==Id and compose(Gi,G)==Id,'free_inverse_source_lifts')
    ck(shorten(sub(r,G))[0]==(),'surface_relator_source_lifts')
ABC=compose(compose(A,B),C);Q=Id
for _ in range(4):Q=compose(Q,ABC)
E2=compose(E,E);Ad=tuple((-4,)+w+(4,) for w in Id);rhs=compose(Ad,E2)
traces=[]
for j in range(4):
    residual=red(Q[j]+inv(rhs[j]));out,steps=shorten(residual)
    ck(out==(),'based_chain_identity_each_generator');traces.append({'generator':j+1,'residual':residual,'steps':steps})
# The actual twist image, rather than an abelian primitive-word test.
ck(inv(sub((1,),compose(Ai,Ai)))==(-1,3,3),'simple_curve_exact_twist_word')
# Infinite dihedral multiplication; verifies all n at once by integral normal forms.
def dm(a,b):return (a[0]+(-1)**a[1]*b[0],(a[1]+b[1])%2)
def di(a):return (-(-1)**a[1]*a[0],a[1])
def ph(pair):
    a,b=pair;return dm(a,b),dm(dm(b,a),b)
pair=((1,0),(0,1));initial=pair
for _ in range(3):pair=ph(pair)
ck(pair==initial,'dihedral_monodromy_cube_all_periods')
ck(dm(dm(dm(initial[0],initial[1]),di(initial[0])),di(initial[1]))==(2,0),'dihedral_boundary_monodromy')

# Generic four-square gluing, independent of the author's vertex enumerator.
h=(0,2,1,3);v=(1,0,3,2)
parent=list(range(16))
def find(i):
    while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
    return i
def union(a,b):parent[find(a)]=find(b)
# corners: bottom left, bottom right, top right, top left.
for s in range(4):
    union(4*s+1,4*h[s]);union(4*s+2,4*h[s]+3)
    union(4*s+3,4*v[s]);union(4*s+2,4*v[s]+1)
V=len({find(i) for i in range(16)})
ck(V==2 and V-8+4==-2,'origami_genus_two')
ck(find(0)!=find(3) and {find(0),find(3)}=={find(12),find(15)},'two_edge_embedded_circle_endpoints')

one=(F(1),F(0),F(0),F(0));ii=(F(0),F(1),F(0),F(0));jj=(F(0),F(0),F(1),F(0));kk=(F(0),F(0),F(0),F(1))
def qm(q,p):
    a,b,c,d=q;e,f,g,h=p
    return (a*e-b*f-c*g-d*h,a*f+b*e+c*h-d*g,a*g-b*h+c*e+d*f,a*h+b*g-c*f+d*e)
def qi(q):return (q[0],-q[1],-q[2],-q[3])
def qs(a,b):return tuple(x-y for x,y in zip(a,b))
def qdot(a,b):return sum(x*y for x,y in zip(a,b))
def conj(q,p):return qm(qm(q,p),qi(q))
def assess(data):
    a1,a2,a3,a4,b1,b2,b3,b4=data
    for q in data:ck(qdot(q,q)==1,'unit_quaternion_input')
    for u,w in ((qm(a1,b2),qm(b1,a1)),(qm(a2,b1),qm(b2,a3)),(qm(a3,b3),qm(b4,a2)),(qm(a4,b4),qm(b3,a4))):ck(u==w,'four_square_relation')
    delta=qs(a2,a3);V=qm(a4,delta);P=qm(a1,delta);W=conj(qi(b1),P);S=qdot(delta,delta)
    ck(S>0 and V[0]==0 and P[0]==0,'angle_nonzero_imaginary')
    aa=qm(a1,qi(a4));q=qm(qi(aa),qm(b1,b1));dot=qdot(V,W)
    ck(dot==S*q[0],'unsquared_numerator_identity')
    ck(dot*dot/(qdot(V,V)*qdot(P,P))==q[0]**2,'angle_trace_square_identity')
    return q[0]**2

def family(a,b,which):
    if which==1:return ((a,b,0,0),kk,qi(kk),one,ii,ii,jj,jj)
    a1=(a,0,b,0);a2=(F(1,2),)*4;a3=conj(jj,a2);b1=qm(qm(a1,a2),jj);b2=conj(qi(a1),b1)
    return (a1,a2,a3,one,b1,b2,jj,jj)
def gauge(data,u):
    a1,a2,a3,a4,b1,b2,b3,b4=data
    return qm(a1,qi(u)),qm(u,a2),qm(u,a3),qm(a4,qi(u)),b1,conj(u,b2),b3,conj(u,b4)
for k in range(1,21):
    a=F(1-k*k,1+k*k);b=F(2*k,1+k*k)
    for which in (1,2):
        data=family(a,b,which);val=assess(data)
        for u in ((F(3,5),F(0),F(4,5),F(0)),(F(1,2),)*4):ck(assess(gauge(data,u))==val,'nongauged_source_identity')
ck(assess(family(F(3,5),F(4,5),1))==F(9,25),'first_nonconstant_witness')
ck(assess(family(F(5,13),F(12,13),1))==F(25,169),'second_nonconstant_witness')
ck(qm(ii,jj)!=qm(jj,ii),'irreducibility_witness')
ck(assess(family(F(3,5),F(4,5),2))==F(1,100),'second_family_source_value')
print(json.dumps({'status':'PASS','exact_controls':sum(Cts.values()),'groups':dict(sorted(Cts.items())), 'chain_identity_reduction_traces':traces,'scope':'Exact based-word relation proofs and quaternion/cover controls; geometric, measure and KAM theorems are audited in the written review.'},sort_keys=True,indent=2))

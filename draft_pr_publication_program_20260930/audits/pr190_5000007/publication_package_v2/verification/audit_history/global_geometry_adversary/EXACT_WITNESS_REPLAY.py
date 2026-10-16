"""Independent exact replay of the public 16-face geometry; no imported checker.
Main global theorem in GEOMETRIC_DERIVATION.md does not depend on this script.
Ring Q(r), r^4+r^3+r^2+r+1=0, embedded r=exp(2*pi*i/5).
Numerical arguments are printed only after all legality and length checks are exact.
"""
from fractions import Fraction as F
from math import cos, sin, pi, atan2, degrees
import json

class K:
    def __init__(self, x=0):
        self.c = tuple(map(F,x)) if isinstance(x,(list,tuple)) else (F(x),F(0),F(0),F(0))
    def __add__(a,b):
        b=coerce(b);return K(tuple(x+y for x,y in zip(a.c,b.c)))
    __radd__=__add__
    def __neg__(a):return K(tuple(-x for x in a.c))
    def __sub__(a,b):return a+-coerce(b)
    def __rsub__(a,b):return coerce(b)+-a
    def __mul__(a,b):
        b=coerce(b);c=[F(0)]*7
        for i,x in enumerate(a.c):
            for j,y in enumerate(b.c):c[i+j]+=x*y
        for j in range(6,3,-1):
            for k in range(4):c[j-4+k]-=c[j]
        return K(c[:4])
    __rmul__=__mul__
    def __eq__(a,b):return a.c==coerce(b).c
    def inv(a):
        assert a!=0
        cols=[(a*K(tuple(int(i==j) for i in range(4)))).c for j in range(4)]
        m=[[cols[j][i] for j in range(4)]+[F(i==0)] for i in range(4)]
        for j in range(4):
            pivot=next(i for i in range(j,4) if m[i][j])
            m[j],m[pivot]=m[pivot],m[j]
            v=m[j][j];m[j]=[x/v for x in m[j]]
            for i in range(4):
                if i!=j:
                    v=m[i][j];m[i]=[x-v*y for x,y in zip(m[i],m[j])]
        return K(tuple(m[i][4] for i in range(4)))
    def __truediv__(a,b):return a*coerce(b).inv()
    def conj(a):return sum((x*RP[(-j)%5] for j,x in enumerate(a.c)),K())
    def real_pair(a):
        assert a==a.conj(),a.c
        assert a.c[1]==0 and a.c[2]==a.c[3],a.c
        b=-a.c[2]/2;return a.c[0]+b,b
    def sign(a):
        x,y=a.real_pair()
        if not y:return (x>0)-(x<0)
        if not x:return (y>0)-(y<0)
        if x>0 and y>0:return 1
        if x<0 and y<0:return -1
        z=x*x-5*y*y
        assert z!=0
        return ((z>0)-(z<0))*((x>0)-(x<0))
    def approx(a):
        r=complex(cos(2*pi/5),sin(2*pi/5))
        return sum(float(x)*r**j for j,x in enumerate(a.c))
def coerce(x):return x if isinstance(x,K) else K(x)
R=K((0,1,0,0));RP=[K(1)]
for _ in range(4):RP.append(RP[-1]*R)
assert RP[-1]*R==1
def det(a,b):return a.conj()*b-a*b.conj()
def inside01(x,strict=True):
    return x.sign()>=(1 if strict else 0) and (1-x).sign()>=(1 if strict else 0)
def real_repr(x):return [str(z) for z in x.real_pair()]
def direction36(x):
    for j in range(5):
        if x==RP[j]:return (2*j)%10
        if x==-RP[j]:return (2*j+5)%10
    raise AssertionError(x.c)

faces=[
 [6,18,4,8,10],[10,8,0,16,2],[17,16,0,12,1],
 [3,13,2,16,17],[5,9,1,12,14],[14,12,0,8,4],
 [5,14,4,18,19],[3,17,1,9,11],[11,9,5,19,7],
 [6,10,2,13,15],[19,18,6,15,7],[15,13,3,11,7]]
itinerary=[1,3,11,8,6,5,1,3,11,10,8,6,4,5,2,1]
expected=[(2,16),(3,13),(7,11),(5,19),(4,14),(0,8),(2,16),
          (3,13),(7,15),(7,19),(5,19),(5,14),(12,14),(0,12),(0,16)]
# The physical outward boundary lists develop counterclockwise; shared sides reverse.
def place(face, first, z, edgevector):
    j=face.index(first);d={first:z}
    for k in range(4):
        z=z+edgevector*RP[k];d[face[(j+k+1)%5]]=z
    assert z+edgevector*RP[4]==d[first]
    return d
occ=[place(faces[itinerary[0]],0,K(),K(1))]
for i in range(1,len(itinerary)):
    old,new=faces[itinerary[i-1]],faces[itinerary[i]]
    common=set(old)&set(new);assert len(common)==2
    j=next(j for j in range(5) if new[j] in common and new[(j+1)%5] in common)
    u,v=new[j],new[(j+1)%5]
    d=place(new,u,occ[-1][u],occ[-1][v]-occ[-1][u])
    assert all(d[x]==occ[-1][x] for x in common)
    occ.append(d)
Z=occ[-1][2]
length2=Z*Z.conj()
assert length2==K((85,0,-137,-137)) # (307+137*sqrt(5))/2.
crossings=[]
for i,(u,v) in enumerate(expected):
    assert {u,v}==set(faces[itinerary[i]])&set(faces[itinerary[i+1]])
    aa=occ[i][u];ee=occ[i][v]-aa;dd=det(Z,ee)
    assert dd!=0
    t=det(aa,ee)/dd;s=det(aa,Z)/dd
    assert inside01(t) and inside01(s)
    assert not crossings or (t-crossings[-1][0]).sign()>0
    crossings.append((t,s))
# Every face is convex. Its full boundary intersections must be precisely its
# prescribed entry/exit points; testing every edge rejects an unlisted crossing.
for i,(face,d) in enumerate(zip((faces[x] for x in itinerary),occ)):
    contacts=[]
    for j,u in enumerate(face):
        v=face[(j+1)%5];aa=d[u];ee=d[v]-aa;dd=det(Z,ee)
        assert dd!=0
        t=det(aa,ee)/dd;s=det(aa,Z)/dd
        if inside01(t,False) and inside01(s,False):contacts.append(t)
    unique=[]
    for t in contacts:
        if t not in unique:unique.append(t)
    wanted=[K(0) if i==0 else crossings[i-1][0],
            K(1) if i==len(occ)-1 else crossings[i][0]]
    assert len(unique)==2 and all(t in unique for t in wanted)
    for u,z in d.items():
        if det(z,Z)==0:
            t=(z/Z)
            assert (i,u,t.c) in [(0,0,K(0).c),(15,2,K(1).c)]
# Graph-distance statement independently follows from the same face data.
edges={tuple(sorted((f[j],f[(j+1)%5]))) for f in faces for j in range(5)}
assert len(edges)==30 and (0,2) not in edges
assert tuple(sorted((0,16))) in edges and tuple(sorted((16,2))) in edges
terminal_outward=occ[-1][10]-occ[-1][2]
terminal_transport=occ[-1][16]-occ[-1][2]
assert direction36(terminal_outward)==3  # 108 degrees.
assert direction36(terminal_transport)==6 # 216 degrees, Q outgoing corner q2.
assert direction36(occ[0][16]-occ[0][0])==0
assert (det(K(1),Z)/(R-R.conj())).sign()>0
assert (det(Z,-RP[3])/(R-R.conj())).sign()>0 # 0<alpha<pi/5 exactly.
za=Z.approx()
result={
 "status":"all exact assertions passed",
 "itinerary_occurrences":len(occ),
 "crossings_checked":len(crossings),
 "interior_vertex_hits":0,
 "endpoint_graph_distance":2,
 "length_squared_A_plus_B_sqrt5":real_repr(length2),
 "endpoint_coefficients_Q_r":[str(c) for c in Z.c],
 "initial_alpha_degrees_approx":degrees(atan2(za.imag,za.real)),
 "terminal_outward_ray_degrees_exact":36*direction36(terminal_outward),
 "terminal_transported_ray_degrees_exact":36*direction36(terminal_transport),
 "even_N_beta_minus_alpha_degrees_exact":144,
 "proper_parity_class":"A1",
 "initial_sector_0_lt_alpha_lt_pi_over_5_exact":True,
 "exact_crossing_parameters_A_plus_B_sqrt5":[[real_repr(t),real_repr(s)] for t,s in crossings]}
print(json.dumps(result,indent=2))

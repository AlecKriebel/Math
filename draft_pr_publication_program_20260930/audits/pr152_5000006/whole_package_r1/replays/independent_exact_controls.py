"""Original R1 exact controls; no imports of the publication's verifier."""
from fractions import Fraction as F
from pathlib import Path
from math import gcd
import json
counts={}
def check(name, condition):
    if not condition: raise RuntimeError(name)
    counts[name]=counts.get(name,0)+1

# The literal source definition is evaluated over entire exact linear partitions,
# rather than using the five alpha samples in the packaged diagnostic.
def literal(n,a,b,odd):
    h=n//2; result=set()
    for k in range(n-1):
        if n%2:
            if odd:
                yes=((k<=h-1 and a>=F(n-2*k-2,n)) or
                     (k>=h and a<=F(2*(n-k-2),n))) and b+a==F(2*(n-k-1),n)
            else:
                yes=((k<=h+1 and a<=F(n-2*k-2,n) and b-a==F(2*(k+1),n)) or
                     (k>=h and a>=F(2*(n-k-2),n) and b-a==F(2*(k+3-n),n)))
        else:
            if odd:
                yes=((k<=h-1 and a>=F(h-k-1,h)) or
                     (k>=h-1 and a<=F(n-k-2,h))) and b+a==F(n-k-1,h)
            else:
                yes=((k<=h-1 and a<=F(h-k-1,h) and b-a==F(k+1,h)) or
                     (k>=h-1 and a>=F(n-k-2,h) and b-a==F(k+3-n,h)))
        if yes: result.add(k%(n-2))
    return result

for n in range(3,81):
    delta=F(n-2,n)
    # All possible linear inequality breaks from Definition 2.1.
    breaks={F(0),delta}
    for k in range(n-1):
        if n%2: breaks.update([F(n-2*k-2,n),F(2*(n-k-2),n)])
        else: breaks.update([F(n//2-k-1,n//2),F(n-k-2,n//2)])
    for odd in [True,False]:
        for s in range(-n,n+1):
            if odd: lo=max(F(0),F(2*s,n)-1); hi=min(delta,F(2*s-2,n))
            else: lo=max(F(0),F(2-2*s,n)); hi=min(delta,1-F(2*s,n))
            if lo>hi: continue
            edges=sorted({lo,hi}|{x for x in breaks if lo<=x<=hi})
            samples=edges+[(x+y)/2 for x,y in zip(edges,edges[1:])]
            label=(n-1-s if odd else s-1)%(n-2)
            for a in samples:
                b=F(2*s,n)-a if odd else F(2*s,n)+a
                check('literal_partition',literal(n,a,b,odd)=={label})
                check('physical_reverse',literal(n,1-b,1-a,odd)=={(-label if odd else label)%(n-2)})
                check('polygon_reflection',literal(n,delta-a,1+F(2,n)-b,odd)=={(-label)%(n-2)})
            # Full-cone lift changes vanish modulo n-2.
            r=n-2 if n%2 else (n-2)//2
            for lift in range(-3,4):
                check('whole_cone_lift',lift*n*r%(n-2)==0)
    for m in range(n-2 if n%2 else (n-2)//2):
        for e in ([0] if n%2 else [0,1]):
            K=(2*m+1-e)%(n-2)
            mr=-m-1 if e==0 else -m
            check('intrinsic_reversal',(2*mr+1-e)%(n-2)==(-K)%(n-2))

# Independent quadratic-field reflection and first-hit validation of O-A-B-A-O.
Z=(F(0),F(0)); ONE=(F(1),F(0))
def q(a,b=0):return (F(a),F(b))
def add(x,y):return (x[0]+y[0],x[1]+y[1])
def neg(x):return (-x[0],-x[1])
def sub(x,y):return add(x,neg(y))
def mul(x,y):return (x[0]*y[0]+5*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def inv(x):
    d=x[0]*x[0]-5*x[1]*x[1]
    return (x[0]/d,-x[1]/d)
def sign(x):
    a,b=x
    if not b:return (a>0)-(a<0)
    if a>=0 and b>0:return 1
    if a<=0 and b<0:return -1
    v=5*b*b-a*a
    return ((v>0)-(v<0)) if b>0 else ((v<0)-(v>0))
def vsub(x,y):return (sub(x[0],y[0]),sub(x[1],y[1]))
def vmul(x,a):return (mul(x[0],a),mul(x[1],a))
def cross(x,y):return sub(mul(x[0],y[1]),mul(x[1],y[0]))
c=q(F(1,4),F(1,4)); u=q(F(-1,4),F(1,4)); s2=sub(ONE,mul(c,c))
def dot(x,y):return add(mul(x[0],y[0]),mul(s2,mul(x[1],y[1])))
def reflect(d,t):return vsub(vmul(t,mul(q(2),mul(dot(d,t),inv(dot(t,t))))),d)
poly=[(Z,Z),(neg(u),mul(q(2),c)),(q(F(1,2)),add(mul(q(2),c),ONE)),
      (add(ONE,u),mul(q(2),c)),(ONE,Z)]
A=(Z,q(2));B=(q(F(5,4)),mul(q(2),mul(c,c)))
path=[poly[0],A,B,A,poly[0]]
for j in range(4):
    midpoint=tuple(mul(add(path[j][d],path[j+1][d]),q(F(1,2))) for d in [0,1])
    # Clockwise convex polygon: every segment's midpoint lies strictly inside.
    for k in range(5):
        check('open_segment_inside',sign(cross(vsub(poly[(k+1)%5],poly[k]),vsub(midpoint,poly[k])))<0)
for j,side in [(1,1),(2,3),(3,1)]:
    incoming=vsub(path[j],path[j-1]);outgoing=vsub(path[j+1],path[j])
    tangent=vsub(poly[(side+1)%5],poly[side]);bounced=reflect(incoming,tangent)
    check('reflection_cross_zero',cross(bounced,outgoing)==Z)
    check('reflection_positive_scale',sign(dot(bounced,outgoing))>0)
    check('collision_on_side',cross(tangent,vsub(path[j],poly[side]))==Z)
    along=mul(dot(vsub(path[j],poly[side]),tangent),inv(dot(tangent,tangent)))
    check('collision_strict_side',sign(along)>0 and sign(sub(ONE,along))>0)
check('pentagon_exact_type',literal(5,F(1,2),F(1,2),False)=={2})

# Expanded lattice check, with all twelve triangular dihedral images.
def rot(p,q):return p-q,p
def mirror(p,q):return q,p
def norm(p,q):return p*p-p*q+q*q
def quotient(p,q):
    a=2 if (p+q)%3==2 else 1
    weight={0:F(3,4),1:F(1,4),2:F(1)}[(p+q)%3]
    return F(a*a*norm(p,q))/weight
for p in range(-20,21):
    for q0 in range(-20,21):
        if gcd(p,q0)!=1:continue
        for reflected in [False,True]:
            w=mirror(p,q0) if reflected else (p,q0)
            for _ in range(6):
                check('all_hex_dihedral',quotient(*w)==quotient(p,q0))
                w=rot(*w)

receipt={'status':'PASS','counts':counts,'checks':sum(counts.values()),
 'scope':'Entire alpha partitions for n=3..80, exact first-hit/reflection witness, full dihedral lattice box; finite controls, not universal theorem.',
 'witness':'O-A-B-A-O; both first and final reflection checked by full scaled-field vector equations.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))

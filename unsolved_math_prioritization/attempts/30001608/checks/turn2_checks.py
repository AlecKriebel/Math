"""Exact finite controls for the nonlinear drift identity and its stated range."""
import json
from fractions import Fraction as F
from itertools import product
from collections import Counter
C=Counter()
def ck(v,k):
    assert v,k
    C[k]+=1
def direct(s,la,c,K):
    a,b,x,y=s;D=x+y+1
    def V(t):
        aa,bb,xx,yy=t
        return (aa+xx-bb-yy)**2+c*(aa*aa+bb*bb)+K*(2*aa+2*bb+xx+yy)
    jumps=[((1,0,0,0),la/2),((0,1,0,0),la/2),((-1,0,1,0),F(a*(x+1),D)),((0,-1,0,1),F(b*(y+1),D)),((0,0,-1,0),F(x*(y+1),D)),((0,0,0,-1),F(y*(x+1),D))]
    return sum(rate*(V(tuple(i+j for i,j in zip(s,v)))-V(s)) for v,rate in jumps if rate)
for la in [F(1,4),F(1,2),F(1),F(3,2),F(19,10),F(2),F(10)]:
    c=2/la;K=3+c
    for a,b,x,y in product(range(5),repeat=4):
        D=x+y+1;S=a+b+x+y
        P3=-2*c*(a*a*x+b*b*y)
        P2=-2*c*(a*a+b*b)-2*(x*x+y*y)+4*(a*y+b*x)-3*(a*x+b*y)-2*c*x*y
        P1=-(a+b)+(7*la+4-c)*(x+y);P0=7*la+6
        ck(D*direct((a,b,x,y),la,c,K)==P3+P2+P1+P0,'full_nonlinear_generator_identity')
        ck(P3<=0,'nonpositive_cubic_drift')
        if la<2:
            de=2*(c-1)/(c+1)
            ck(P2<=-de*(a*a+b*b+x*x+y*y),'negative_quadratic_form')
            B=max(7*la+4-c,0);CC=7*la+6
            ck(P3+P2+P1+P0<=-de*F(S*S,4)+B*S+CC,'global_drift_envelope')
for la in [F(1,4),F(1),F(3,2),F(19,10),F(199,100)]:
    c=2/la;de=2*(c-1)/(c+1);B=max(7*la+4-c,0);CC=7*la+6
    R=int(4*(B+CC+2)/de)+2
    for S in [R,R+1,2*R,10*R]:ck(-de*F(S*S,4)+B*S+CC<=-(S+1),'finite_set_threshold')
for la,c in product([F(2),F(3),F(10)],[F(1,4),F(1),F(2),F(10)]):
    t=(la*c+2)/(4*c);val=-2*c*t*t+(la*c+2)*t-2
    ck(val==(la*c+2)**2/(8*c)-2,'quadratic_family_maximum')
    ck(val>=la-2,'high_load_obstruction_bound')
    if la>2 or c!=1:ck(val>0,'positive_ray_obstruction')
for K in [F(1,4),F(1),F(4),F(100)]:
    for m in range(101):
        ck(direct((m,0,0,m),F(2),F(1),K)==F((8+2*K)*m+4+4*K,m+1),'critical_ray_exact_identity')
        ck(direct((m,0,0,m),F(2),F(1),K)>0,'critical_ray_positive')
print(json.dumps({'status':'PASS','assertions':sum(C.values()),'counts':dict(sorted(C.items())),'scope':'Exact finite controls only; global drift inequalities and positive recurrence are proved in TURN_2.md.'},sort_keys=True,indent=2))

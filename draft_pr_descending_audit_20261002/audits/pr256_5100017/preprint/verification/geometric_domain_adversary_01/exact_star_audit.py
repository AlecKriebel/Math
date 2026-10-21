"""Exact star regenerated from a tangent slope and physical reflection.
Independent direct Cartesian projections and polynomial shoelace moments.
"""
import sympy as s
import json
from pathlib import Path
A=s.Rational(221,96);B=s.Rational(27625,20736);L=s.Rational(125,96)
a=s.sqrt(A);b=s.sqrt(B)
def simp(x):return s.factor(s.radsimp(s.simplify(x)))
def dot(p,q):return sum(p[j]*q[j] for j in (0,1))
def cross(p,q):return p[0]*q[1]-p[1]*q[0]
def scaled(c,p):return [simp(c*x) for x in p]
def sub(p,q):return [simp(p[j]-q[j]) for j in (0,1)]
def add(p,q):return [simp(p[j]+q[j]) for j in (0,1)]
# Inner semiaxes (1,25/144); line from (0,b) tangent to it has slope
# sqrt(b^2-(25/144)^2) = sqrt(L). A down-left direction is (-1,-sqrt(L)).
p=[s.Integer(0),b];v=[-s.Integer(1),-s.sqrt(L)];P=[];V=[]
for i in range(8):
    P.append(p);V.append(v)
    step=simp(-2*(p[0]*v[0]/A+p[1]*v[1]/B)/(v[0]*v[0]/A+v[1]*v[1]/B))
    assert step>0
    q=add(p,scaled(step,v));n=[q[0]/A,q[1]/B]
    v=sub(v,scaled(simp(2*dot(v,n)/dot(n,n)),n));p=q
assert all(simp(p[j]-P[0][j])==0 and simp(v[j]-V[0][j])==0 for j in (0,1))
normalized=[[simp(p[0]/a),simp(p[1]/b)] for p in P]
assert len({tuple(p) for p in normalized})==8
for i,p in enumerate(P):
    q=P[(i+1)%8];u=P[(i-1)%8];edge=sub(q,p);normal=[p[0]/A,p[1]/B]
    assert simp(p[0]**2/A+p[1]**2/B-1)==0
    ni=[-edge[1],edge[0]];c=dot(ni,p)
    assert simp(c*c-(A-L)*ni[0]**2-(B-L)*ni[1]**2)==0
    vin=sub(p,u);vout=sub(q,p)
    # Unit incoming/outgoing verify physically, independent of propagated V.
    vin=scaled(1/s.sqrt(dot(vin,vin)),vin);vout=scaled(1/s.sqrt(dot(vout,vout)),vout)
    refl=sub(vin,scaled(simp(2*dot(vin,normal)/dot(normal,normal)),normal))
    assert all(simp(refl[j]-vout[j])==0 for j in (0,1))
    assert simp(cross(p,q))>0
    assert all(simp(p[j]+P[(i+4)%8][j])==0 for j in (0,1))
# Rays wind counterclockwise and all edges turn through <pi about O.
# Count positive crossings of the ray y=0,x>0 using usual oriented winding.
winding=0
for i,p in enumerate(P):
    q=P[(i+1)%8]
    if p[1]<=0<q[1] and cross(p,q)>0:winding+=1
    elif q[1]<=0<p[1] and cross(p,q)<0:winding-=1
assert winding==3
X,Y=s.symbols('X Y',real=True);Q=[]
for p in P:
    n=[p[0]/A,p[1]/B];r=dot(n,n)
    Q.append([s.expand(([X,Y][j])+(1-n[0]*X-n[1]*Y)*n[j]/r) for j in (0,1)])
S=s.Integer(0);T=[s.Integer(0),s.Integer(0)]
for i,q in enumerate(Q):
    r=Q[(i+1)%8];c=s.expand(cross(q,r));S+=c/2
    for j in (0,1):T[j]+=s.expand(c*(q[j]+r[j]))
S=s.factor(S);T=[s.factor(t) for t in T];S0=s.factor(S.subs({X:0,Y:0}))
H=(A+B)/2;e=(A-B)/2;d=s.factor(1-L*(1/A+1/B));F=s.factor(H*d+2*L);v=s.factor(-4*e*L*d/(F*F-e*e*d*d));rho2=s.factor(-2*F/d)
assert d==-s.Rational(120,221) and F==s.Rational(2795,1728) and v==s.Rational(7,13)
assert rho2==s.Rational(123539,20736)
assert s.factor(S-S0*(1+d*(X*X+Y*Y)/(2*F)))==0
expected_x=S0*((3-(F+2*H*d+e*v*d+2*F*v+3*e*d)/F)*X+d*(3-v)*X*(X*X+Y*Y)/(2*F))
expected_y=S0*((3-(F+2*H*d+e*v*d-2*F*v-3*e*d)/F)*Y+d*(3+v)*Y*(X*X+Y*Y)/(2*F))
assert all(s.factor(T[j]-[expected_x,expected_y][j])==0 for j in (0,1))
zero_moment=[s.factor(t.subs({X:s.sqrt(rho2),Y:0})) for t in T]
assert S.subs({X:s.sqrt(rho2),Y:0}).simplify()==0
assert zero_moment[0]!=0
result={'status':'PASS','construction':'(0,b), initial tangent slope sqrt(lambda), ray intersection, physical specular reflection','normalized_vertices':[[str(v) for v in p] for p in normalized],'least_period':8,'winding':winding,'a_squared':str(A),'b_squared':str(B),'lambda':str(L),'d':str(d),'F':str(F),'v':str(v),'exceptional_radius_squared':str(rho2),'S0':str(S0),'signed_area_polynomial':str(S),'first_moment_polynomials':[str(t) for t in T],'zero_circle_point':['sqrt('+str(rho2)+')','0'],'first_moment_on_zero_circle':[str(t) for t in zero_moment],'zero_circle_moment_nonzero':True,'limitations':'Exact single-family verification and domain obstruction; all-N conclusions require general deductions.'}
Path('EXACT_STAR_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

"""Author controls for k905. Own code; standard library, SymPy, mpmath.
Finite exact algebra and separately labeled actual-billiard diagnostics.
"""
import sympy as s
import mpmath as mp
from fractions import Fraction as F
from math import gcd
from collections import Counter
import json
ct=Counter()
def ck(x,kind):
    assert x,kind
    ct[kind]+=1
def cross(x,y):return x[0]*y[1]-x[1]*y[0]
def dot(x,y):return x[0]*y[0]+x[1]*y[1]
def inv(x,f):
    d=(x[0]-f[0],x[1]-f[1]);z=dot(d,d)
    return (f[0]+d[0]/z,f[1]+d[1]/z)
def area(q):return sum(cross(q[i],q[(i+1)%len(q)]) for i in range(len(q)))/2
cases=0
for m in range(2,24):
    for alpha,beta,c in [(F(5,4),F(3,4),F(1)),(F(5),F(4),F(3)),(F(13),F(12),F(5))]:
        ck(alpha*alpha-beta*beta==c*c,'confocal_rational_axes')
        half=[]
        for j in range(m):
            t=F(j,m-j)
            half.append((alpha*(1-t*t)/(1+t*t),beta*2*t/(1+t*t)))
        T=half+[(-x,-y) for x,y in half]
        for tau in range(1,m):
            if gcd(tau,2*m)!=1:continue
            ck(tau%2==1,'primitive_even_rotation')
            ordered=[T[i*tau%(2*m)] for i in range(2*m)]
            U=[inv(x,(c,0)) for x in ordered];V=[inv(x,(-c,0)) for x in ordered]
            for i in range(2*m):
                ck(ordered[i]!= (c,0) and ordered[i]!=(-c,0),'inversion_centers_avoided')
                ck(V[(i+m)%(2*m)]==tuple(-x for x in U[i]),'exact_central_equivariance')
                ck(inv(U[i],(c,0))==ordered[i],'inversion_involution')
            ck(len(set(U))==2*m,'distinct_inverse_vertices')
            ck(area(U)==area(V),'exact_signed_area_equality')
            if area(V):ck(area(U)/area(V)==1,'ratio_on_natural_domain')
            cases+=1
# Exact axis orbit and contact construction.
a=s.sqrt(2);b=s.Integer(1);alpha2=s.Rational(4,3);beta2=s.Rational(1,3)
P=[(a,0),(0,b),(-a,0),(0,-b)]
T=[(2*a/3,b/3),(-2*a/3,b/3),(-2*a/3,-b/3),(2*a/3,-b/3)]
for i in range(4):
    A=P[i];B=P[(i+1)%4];d=(B[0]-A[0],B[1]-A[1]);t=T[i]
    ck(s.simplify(dot(d,d)-3)==0,'exact_orbit_side_length')
    ck(s.simplify(t[0]**2/alpha2+t[1]**2/beta2-1)==0,'contact_on_caustic')
    ck(s.simplify(cross((t[0]-A[0],t[1]-A[1]),d))==0,'contact_on_chord')
    ck(s.simplify(t[0]*d[0]/alpha2+t[1]*d[1]/beta2)==0,'caustic_tangent_direction')
    frac=s.simplify(dot((t[0]-A[0],t[1]-A[1]),d)/dot(d,d))
    ck(0<frac<1,'contact_inside_segment')
    prev=P[(i-1)%4];inc=((A[0]-prev[0])/s.sqrt(3),(A[1]-prev[1])/s.sqrt(3));out=(d[0]/s.sqrt(3),d[1]/s.sqrt(3))
    ck(s.simplify(cross((inc[0]-out[0],inc[1]-out[1]),(A[0]/2,A[1])))==0,'exact_specular_normal')
    ck(s.simplify(t[0]**2+t[1]**2-1)==0,'contact_on_focus_circle')
for sign in [-1,1]:
    V=[tuple(s.simplify(z) for z in inv(x,(s.Integer(sign),0))) for x in T]
    ck(len(set(V))==4,'zero_example_distinct_vertices')
    for x,y in V:ck(x==s.Rational(sign,2),'zero_example_line')
    ck(s.simplify(area(V))==0,'exact_zero_area')
# Independent direct rectangle formula, then physical axis-family substitution.
u,v,c=s.symbols('u v c',positive=True)
rect=[(u,v),(-u,v),(-u,-v),(u,-v)]
Ainv=s.factor(area([inv(x,(c,0)) for x in rect]));r2=u*u+v*v
expected=4*u*v*(r2-c*c)*(r2+c*c)/((r2+c*c)**2-4*c*c*u*u)**2
ck(s.cancel(Ainv-expected)==0,'rectangle_inversion_formula')
aa,bb=s.symbols('a b',positive=True)
expr=expected.subs({u:aa**3/(aa*aa+bb*bb),v:bb**3/(aa*aa+bb*bb),c*c:aa*aa-bb*bb})
ck(s.cancel(expr-4*(2*bb*bb-aa*aa)*(2*aa*aa-bb*bb)/(aa**3*bb**3))==0,'axis_four_orbit_area_formula')
exact=sum(ct.values())
# Diagnostic actual primitive billiards; contact computed from chord covectors.
mp.mp.dps=80;num=0;maxerr=mp.mpf(0);ncases=0

def near(x,scale=1):
    global num,maxerr
    err=abs(x)/(1+abs(scale));maxerr=max(maxerr,err)
    assert err<mp.mpf('1e-60');num+=1
for N in range(4,26,2):
    for tau in range(1,N//2):
        if gcd(N,tau)!=1:continue
        for kval in ['0.2','0.7','0.98']:
            k=mp.mpf(kval);K=mp.ellipk(k*k);v=2*K*tau/N
            sn=lambda u:mp.ellipfun('sn',u,k*k)
            cn=lambda u:mp.ellipfun('cn',u,k*k)
            dn=lambda u:mp.ellipfun('dn',u,k*k)
            a=dn(v)/cn(v);b=mp.sqrt(1-k*k)/cn(v)
            for ph in ['0.137','0.519']:
                P=[(-a*sn(mp.mpf(ph)*K+2*i*v),b*cn(mp.mpf(ph)*K+2*i*v)) for i in range(N)]
                T=[]
                for i in range(N):
                    x,y=P[i];xx,yy=P[(i+1)%N];n=(yy-y,x-xx);h=n[0]*x+n[1]*y
                    T.append((n[0]/h,(1-k*k)*n[1]/h))
                U=[inv(x,(k,0)) for x in T];V=[inv(x,(-k,0)) for x in T]
                size=max(abs(z) for x in U+V for z in x)
                for i in range(N):
                    near(T[i][0]**2+T[i][1]**2/(1-k*k)-1)
                    for d in range(2):
                        near(T[(i+N//2)%N][d]+T[i][d]);near(V[(i+N//2)%N][d]+U[i][d],size)
                near(area(U)-area(V),N*size*size)
                ncases+=1
print(json.dumps({'status':'PASS','exact_assertions':exact,'exact_families':dict(sorted(ct.items())),'generic_rational_polygon_cases':cases,'actual_billiard_diagnostic_cases':ncases,'diagnostic_assertions':num,'decimal_precision':80,'relative_residual_threshold':'1e-60','maximum_relative_residual':mp.nstr(maxerr,8),'scope':'Exact finite geometry/algebra controls and a symbolic genuine four-orbit zero certificate, plus separate high-precision actual-billiard diagnostics. Generic rational contact polygons are not claimed billiard orbits; the universal argument is in PROOF.md.'},indent=2,sort_keys=True))

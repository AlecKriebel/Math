"""Independent high-precision Euclidean diagnostics; not interval certificates."""
import sys
sys.path.insert(0, '/Users/alec/Library/Python/3.11/lib/python/site-packages')
import mpmath as mp
import math, json
from pathlib import Path
mp.mp.dps = 240

def normerr(lhs,rhs):
    return abs(lhs-rhs)/max(mp.mpf(1),abs(lhs),abs(rhs))
def det(p,q):
    return p[0]*q[1]-p[1]*q[0]
def area(p):
    return mp.fsum(det(p[j],p[(j+1)%len(p)]) for j in range(len(p)))/2
def inversion(p,c):
    # Compute actual squared Euclidean distance, not a Jacobi surrogate.
    xx,yy = p[0]-c,p[1]
    rr = xx*xx+yy*yy
    return (xx/rr,yy/rr)
max_errors = {}
def observe(name,lhs,rhs):
    ee=normerr(lhs,rhs)
    max_errors[name]=max(max_errors.get(name,mp.mpf(0)),ee)
    if ee > mp.mpf('1e-55'):
        raise AssertionError((name,mp.nstr(ee,15)))

def run(ktext,N,tau):
    k=mp.mpf(ktext); par=k*k; kp=mp.sqrt(1-par)
    K=mp.ellipk(par); v=2*K*tau/N; delta=2*v; m=N//2
    sn=lambda u:mp.ellipfun('sn',u,par)
    cn=lambda u:mp.ellipfun('cn',u,par)
    dn=lambda u:mp.ellipfun('dn',u,par)
    h=sn(v); cv=cn(v); dv=dn(v); t=h*h; q=cv*cv
    # Deliberately use a non-unit caustic scale.
    alpha=mp.mpf('2.37'); beta=alpha*kp; c=alpha*k
    a=alpha*dv/cv; b=beta/cv
    U=1-2*par*t+par*t*t; V=1-2*t+par*t*t; W=1-par*t*t
    C=b*h*dv*q*q/alpha**3; CA=a*b*h*cv/dv
    Lam=U*(par*par*t**3+par*par*t*t-5*par*t+par+2)/(2*kp**4*W**3)
    a0=q/(U-V)**2; a1=(Lam-a0)/2
    a2=(V*V-U*U*t)/(4*h*cv*dv*(U*U-par*V*V)*(U-V))
    nome=mp.exp(-mp.pi*mp.ellipk(1-par)/K); Q=nome**m
    theta3=mp.jtheta(3,0,Q); theta4=mp.jtheta(4,0,Q)
    kap=mp.jtheta(2,0,Q)**2/theta3**2
    KM=mp.pi*theta3**2/2; lam=m*KM/K
    const=(4*CA*C*Lam/kp)*lam*lam*theta4**2/theta3**2
    ell=2*K/m
    S=lambda w:mp.fsum(dn(w+j*delta) for j in range(m))
    P=lambda w:(-a*sn(w),b*cn(w))
    F=lambda w:1/dn(w)
    Fprime=lambda w:par*sn(w)*cn(w)/(dn(w)**2)
    products=[]
    for phase in [mp.mpf(0),mp.mpf('0.013'),mp.mpf('0.271'),mp.mpf('0.539'),mp.mpf('0.999999999999')]:
        w=4*K*phase
        vertices=[P(w+j*delta) for j in range(N)]
        AA=area(vertices)
        plus=area([inversion(p,c) for p in vertices])
        minus=area([inversion(p,-c) for p in vertices])
        observe('ordinary_area',AA,2*CA*S(w))
        observe('inverse_area',plus,2*C*Lam/kp*S(w+v+K))
        observe('either_focus',plus,minus)
        observe('reversal',area(vertices[::-1])*area([inversion(p,c) for p in vertices[::-1]]),AA*plus)
        observe('explicit_product',AA*plus,const)
        observe('filtered_dn',S(w),lam*mp.ellipfun('dn',lam*w,kap*kap))
        observe('half_grid_product',S(w)*S(w+ell/2),lam*lam*theta4**2/theta3**2)
        observe('half_shift_congruence',S(w+K+v),S(w+ell/2))
        u=w+v
        e1=det(inversion(P(u-v),c),inversion(P(u+v),c))/2
        e2=det(inversion(P(u-v+2*K),c),inversion(P(u+v+2*K),c))/2
        rhs=a0*F(u)+a1*(F(u+delta)+F(u-delta))+a2*(Fprime(u+delta)-Fprime(u-delta))
        observe('pointwise_telescoping_identity',(e1+e2)/(2*C),rhs)
        # A line through successive vertices is tangent to the caustic:
        # in normalized caustic coordinates its support equals its normal norm.
        p1,p2=vertices[0],vertices[1]
        nx=p2[1]-p1[1]; ny=p1[0]-p2[0]; support=nx*p1[0]+ny*p1[1]
        observe('confocal_caustic_tangency',support*support,alpha**2*nx*nx+beta**2*ny*ny)
        # Reflection in the outer normal: unit incident/outgoing tangent parts agree.
        prev,pnow,nxt=vertices[-1],vertices[0],vertices[1]
        inc=(pnow[0]-prev[0],pnow[1]-prev[1]); out=(nxt[0]-pnow[0],nxt[1]-pnow[1])
        ni=mp.sqrt(det(inc,(inc[1],-inc[0]))*-1)
        no=mp.sqrt(out[0]**2+out[1]**2)
        tangent=(-pnow[1]/(b*b),pnow[0]/(a*a))
        observe('reflection_law',(inc[0]*tangent[0]+inc[1]*tangent[1])/ni,(out[0]*tangent[0]+out[1]*tangent[1])/no)
        products.append(AA*plus)
    observe('phase_independence',min(products),max(products))
    if N==4:
        observe('N4_constant',const,4)
    return {'k':ktext,'N':N,'tau':tau,'phases':len(products),'product':mp.nstr(const,25)}

cases=[]
for kk in ['0.001','0.2','0.7','0.95','0.999999999999999']:
    for NN in [4,8,12,16,20,28]:
        for tt in range(1,NN//2):
            if math.gcd(NN,tt)==1:
                cases.append(run(kk,NN,tt))
for NN,tt in [(64,1),(64,31),(128,1),(128,63),(4,1),(12,5)]:
    cases.append(run('0.9999999999999999999999999999999999999999',NN,tt))

# Negative controls deliberately violate the period-divisible-by-four or least
# period hypothesis, and should show phase variation.
negative=[]
for NN,tt in [(6,1),(10,1),(12,2)]:
    k=mp.mpf('.99'); par=k*k; K=mp.ellipk(par); v=2*K*tt/NN
    alpha=mp.mpf(1); a=mp.ellipfun('dn',v,par)/mp.ellipfun('cn',v,par)
    b=mp.sqrt(1-par)/mp.ellipfun('cn',v,par)
    values=[]
    for frac in [mp.mpf(0),mp.mpf('.213'),mp.mpf('.529')]:
        vs=[(-a*mp.ellipfun('sn',4*K*frac+2*j*v,par),b*mp.ellipfun('cn',4*K*frac+2*j*v,par)) for j in range(NN)]
        values.append(area(vs)*area([inversion(p,k) for p in vs]))
    spread=(max(values)-min(values))/max(abs(v) for v in values)
    assert spread>mp.mpf('1e-7')
    negative.append({'N_label':NN,'tau':tt,'least_period':NN//math.gcd(NN,tt),'relative_spread':mp.nstr(spread,20)})

out={'all_passed':True,'dps':mp.mp.dps,'mpmath_version':mp.__version__,
     'case_count':len(cases),'phase_case_count':sum(c['phases'] for c in cases),
     'max_normalized_errors':{n:mp.nstr(e,15) for n,e in max_errors.items()},
     'cases':cases,'negative_controls':negative,'caveat':'Diagnostic arithmetic, not interval-certified evidence.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='cases'},indent=2))

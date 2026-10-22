"""Fresh review02 controls. No archived checker imports; numerical outputs uncertified."""
from pathlib import Path
from datetime import datetime, timezone
from fractions import Fraction
from math import gcd
import json, hashlib
import sympy as s
import mpmath as mp
OUT=Path(__file__).resolve().parent/'FRESH_INDEPENDENT_RESULTS.json'

def exact_general_even():
    a,b,c=s.symbols('a b c',positive=True); S=a*a+b*b; h=s.sqrt(S)
    det=lambda u,v:s.det(s.Matrix([u,v])); dot=lambda u,v:sum(x*y for x,y in zip(u,v))
    area=lambda q:s.simplify(sum(det(q[j],q[(j+1)%4]) for j in range(4))/2)
    lam=a*a*b*b/S; alpha2=a*a-lam;beta2=b*b-lam
    cases={'diamond':[(a,0),(0,b),(-a,0),(0,-b)],'rectangle':[(a*a/h,b*b/h),(-a*a/h,b*b/h),(-a*a/h,-b*b/h),(a*a/h,-b*b/h)]}
    rows=[]; residuals=[]
    for name,P in cases.items():
        Q={}
        for e in [-1,1]:
            q=[]
            for j,(x,y) in enumerate(P):
                n=(x/a**2,y/b**2); f=(e*c,0); nn=dot(n,n)
                q.append(tuple(s.simplify(f[i]+(1-dot(n,f))*n[i]/nn) for i in range(2)))
            Q[e]=area(q)
        for j,X in enumerate(P):
            Y=P[(j+1)%4]; prev=P[(j-1)%4]
            residuals.append(s.simplify(X[0]**2/a**2+X[1]**2/b**2-1))
            lx=Y[1]-X[1];ly=X[0]-Y[0]; d=lx*X[0]+ly*X[1]
            residuals.append(s.simplify(alpha2*lx**2+beta2*ly**2-d*d))
            inc=tuple(s.simplify(X[i]-prev[i]) for i in range(2)); vel=tuple(s.simplify(Y[i]-X[i]) for i in range(2))
            incnorm=s.sqrt(dot(inc,inc));outnorm=s.sqrt(dot(vel,vel)); normal=(X[0]/a**2,X[1]/b**2)
            for i in range(2):residuals.append(s.simplify(inc[i]/incnorm-2*dot(inc,normal)*normal[i]/(incnorm*dot(normal,normal))-vel[i]/outnorm))
        rows.append({'case':name,'Bminus':str(Q[-1]),'Bplus':str(Q[1]),'product':str(s.simplify(Q[-1]*Q[1]))})
    assert all(x==0 for x in residuals)
    assert rows[0]['Bplus']=='2*a*b' and s.simplify(s.sympify(rows[1]['Bplus'],locals={'a':a,'b':b})-S)==0
    return {'assumptions':'a>b>0, c^2=a^2-b^2; lambda=a^2*b^2/(a^2+b^2)','zero_residuals':len(residuals),'all_zero':True,'phases':rows,'product_difference':'(a^2-b^2)^2 > 0','primitive':4}

def combinatorics():
    count=0;phase_count=0;cut=0;n3=0
    for N in range(3,200):
        for t in range(1,(N+1)//2):
            if gcd(N,t)>1:continue
            delta=Fraction(t,N);roots=[-delta/2,delta/2]
            for j0 in range(N):
                w=roots[0]-j0*delta
                singular=[j for j in range(N) if any((w+j*delta-r).denominator==1 for r in roots)]
                assert sorted(singular)==sorted([j0,(j0+1)%N])
                if j0==N-1:cut+=1
                if N==3:n3+=1
                phase_count+=1
            assert (Fraction(N,2)%1==Fraction(1,2))==bool(N%2)
            count+=1
    return {'primitive_N3_through199_cases':count,'all_pole_phases':phase_count,'cyclic_cut_cases':cut,'N3_pole_phases':n3,'all_pass':True}

mp.mp.dps=120
mf=lambda x:mp.mpf(str(x))
serialize=lambda x:mp.nstr(x,32)
def det(u,v):return u[0]*v[1]-u[1]*v[0]
def dot(u,v):return sum(x*y for x,y in zip(u,v))
def add(u,v):return tuple(x+y for x,y in zip(u,v))
def sub(u,v):return tuple(x-y for x,y in zip(u,v))
def scale(q,x):return tuple(x*y for y in q)
def norm(u):return mp.sqrt(dot(u,u))
def area(P):return sum(det(P[j],P[(j+1)%len(P)]) for j in range(len(P)))/2
def unit(u):return scale(u,1/norm(u))
def maxvec(u):return max(abs(x) for x in u)

def one_family(N,t,ktext):
    k=mf(ktext);m=k*k;K=mp.ellipk(m);Kp=mp.ellipk(1-m);p=1j*Kp;v=2*K*t/N;delta=2*v;L=4*K/N
    sn=lambda w:mp.ellipfun('sn',w,m);cn=lambda w:mp.ellipfun('cn',w,m);dn=lambda w:mp.ellipfun('dn',w,m)
    alpha=mp.mpf(1);beta=mp.sqrt(1-m);c=k;a=dn(v)/cn(v);b=beta/cn(v);lam=b*b-beta*beta
    P=lambda w:(-a*sn(w),b*cn(w))
    Q=lambda w:(a*(c-a*sn(w))/(a-c*sn(w)),a*b*cn(w)/(a-c*sn(w)))
    T=lambda w:area([Q(w+j*delta) for j in range(N)])
    inv=lambda w,e:scale(sub(P(w),(e*c,0)),1/(a+e*c*sn(w))**2)
    D=lambda w,e:area([inv(w+j*delta,e) for j in range(N)])
    mb=4*k/(1+k)**2;Kb=(1+k)*K;Kbp=(1+k)*Kp/2
    db=-c*lam/beta**2;Rb=b*b/beta**2;r=a;tM=mp.sqrt((Rb+abs(db))**2-r*r)
    qnew=mp.exp(-mp.pi*Kbp/Kb)**N
    th2=mp.jtheta(2,0,qnew);th3=mp.jtheta(3,0,qnew);mN=(th2/th3)**4;KN=mp.pi*th3**2/2;C=N*KN/Kb
    errors={key:mp.mpf(0) for key in ['boundary','confocal_tangency','unit_reflection','foot_from_actual_outer_side','focal_circle','polarity_circle','bicentric_contact_ratio','dn_area_trace','arbitrary_order_dn_sum','focus_phase_dn','inverse_ratio_constancy','real_reduced_period','reflection_character','imaginary_antiperiod','quarter_sn','quarter_cn','quarter_dn','complement_zero','row_residue','simple_pole_order']}
    update=lambda key,x:errors.__setitem__(key,max(errors[key],abs(x)))
    phases=[mf('0.173')*K,mf('0.619')*K,mf('1.307')*K]
    products=[];ratios=[];Bvals=[];minedge=mp.inf
    for w in phases:
        points=[P(w+j*delta) for j in range(N)];qs=[Q(w+j*delta) for j in range(N)]
        outer=[]
        for j,X in enumerate(points):
            Y=points[(j+1)%N];n=(X[0]/a**2,X[1]/b**2);nn=(Y[0]/a**2,Y[1]/b**2);h=det(n,nn)
            outer.append(((nn[1]-n[1])/h,(n[0]-nn[0])/h))
        for j,X in enumerate(points):
            Y=points[(j+1)%N];prev=points[(j-1)%N]
            update('boundary',X[0]**2/a**2+X[1]**2/b**2-1)
            z=sub(Y,X);normal=(z[1],-z[0]);ell=dot(normal,X)
            update('confocal_tangency',(alpha**2*normal[0]**2+beta**2*normal[1]**2-ell**2)/a**2)
            ni=(X[0]/a**2,X[1]/b**2);vi=unit(sub(X,prev));vo=unit(z)
            update('unit_reflection',maxvec(sub(sub(vi,scale(ni,2*dot(vi,ni)/dot(ni,ni))),vo)))
            # Independent foot from the actual outer side endpoints, no tangent formula.
            U=outer[(j-1)%N];V=outer[j];direction=sub(V,U);f=(c,0)
            foot=add(U,scale(direction,dot(sub(f,U),direction)/dot(direction,direction)))
            update('foot_from_actual_outer_side',maxvec(sub(foot,qs[j]))/a)
            update('focal_circle',(dot(qs[j],qs[j])-a*a)/(a*a));minedge=min(minedge,det(qs[j],qs[(j+1)%N])/(a*a))
        R=[]
        for V in outer:R.append((a*a*(V[0]+c)/(a*a+c*V[0]),a*a*V[1]/(a*a+c*V[0])))
        for X in R:update('polarity_circle',(dot(sub(X,(db,0)),sub(X,(db,0)))-Rb**2)/Rb**2)
        B=area(qs);Bminus=T(w+2*K);products.append(B*Bminus/a**4);Bvals.append(B/a**2)
        update('bicentric_contact_ratio',B/area(R)-r*r/(Rb*Rb-db*db))
        u=(1+k)*(w+v-K)/2
        Sdn=sum(mp.ellipfun('dn',u+2*j*Kb*t/N,mb) for j in range(N))
        update('dn_area_trace',(B-r**3*tM/(Rb*Rb-db*db)*Sdn)/a**2)
        update('arbitrary_order_dn_sum',Sdn-C*mp.ellipfun('dn',C*u,mN))
        Sswitch=sum(mp.ellipfun('dn',u+Kb+2*j*Kb*t/N,mb) for j in range(N))
        update('focus_phase_dn',(Bminus-r**3*tM/(Rb*Rb-db*db)*Sswitch)/a**2)
        ratios.append(B/D(w,-1)/a**4)
        update('real_reduced_period',(T(w+L)-B)/a**2)
        update('reflection_character',(T(2*K-w)-B)/a**2)
        update('imaginary_antiperiod',(T(w+2*p)+B)/a**2)
        z=w/3+mp.mpf('.07')*p
        update('quarter_sn',sn(K+p+z)-dn(z)/(k*cn(z)))
        update('quarter_cn',cn(K+p+z)+1j*beta/(k*cn(z)))
        update('quarter_dn',dn(K+p+z)-1j*beta*sn(z)/cn(z))
    update('inverse_ratio_constancy',max(ratios)-min(ratios))
    for row in [1,3]:
        update('complement_zero',T(K-v+row*p+L/2)/a**2)
        # Symmetric sampling cancels constant terms; eps is finite, not certified.
        eps=mp.mpf('1e-28');w0=K-v+row*p
        r1=scale(sub(Q(w0+eps),Q(w0-eps)),eps/2)
        r2=scale(sub(Q(w0+delta+eps),Q(w0+delta-eps)),eps/2)
        update('row_residue',maxvec(add(r1,r2))/a)
        update('simple_pole_order',eps**2*abs(T(w0+eps))/a**2)
    assert minedge>0
    for name,val in errors.items():assert val<mp.mpf('1e-23') if name in {'row_residue','simple_pole_order'} else val<mp.mpf('1e-75'),(N,t,ktext,name,serialize(val))
    spread=max(products)-min(products)
    if N%2:assert abs(spread)<mp.mpf('1e-75')
    else:assert abs(spread)>mp.mpf('1e-12')
    return {'N':N,'tau':t,'k':ktext,'phase_count':len(phases),'normalized_products':list(map(serialize,products)),'normalized_product_spread':serialize(spread),'minimum_forward_contact_det_over_a2':serialize(minedge),'errors':{x:serialize(y) for x,y in errors.items()},'no_interval_certification':True}

if __name__=='__main__':
    start=datetime.now(timezone.utc).isoformat()
    exact=exact_general_even();finite=combinatorics();rows=[]
    for case in [(3,1,'0.317'),(5,2,'0.813'),(9,4,'0.9731'),(15,4,'0.02003'),(33,16,'0.4807'),(65,29,'0.99871'),(7,3,'0.00000000123'),(10,3,'0.6591')]:
        rows.append(one_family(*case));print('PASS fresh family',case,flush=True)
    result={'utc_start':start,'utc_end':datetime.now(timezone.utc).isoformat(),'program_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'sympy':s.__version__,'mpmath':mp.__version__,'dps':mp.mp.dps,'exact_general_even':exact,'finite_combinatorics':finite,'families':rows,'all_pass':True,'universal_theorem_proved_by_written_derivation_not_finite_tests':True}
    OUT.write_text(json.dumps(result,indent=2)+'\n');print('WROTE',OUT)

#!/usr/bin/env python3
"""Fresh, deterministic PR210 classical/general-equivalence controls.
Run with the scientific Python specified in the audit instruction.
No network, external files, or inherited verification code is used.
Exact SymPy identities are certificates; mpmath values are diagnostics, not interval proofs.
"""
from pathlib import Path
import json, hashlib, sys
import sympy as s
import mpmath as mp

BASE=Path(__file__).resolve().parent
mp.mp.dps=70

def simp(x): return s.factor(s.cancel(x))
def astr(x): return str(s.simplify(x))
def area(points):
    return sum(points[j][0]*points[(j+1)%len(points)][1]-points[j][1]*points[(j+1)%len(points)][0] for j in range(len(points)))/2

def exact_certificates():
    u,v,lam=s.symbols('u v lam',positive=True)
    c=s.sqrt(u-v);a2=u+lam;b2=v+lam
    A=a2*a2/u-(u-v);B=b2*b2/v;D=c*a2*lam/u;C=a2*a2*((u-v)/u-1)
    h=D/A;rad=D*D/A-C
    d=a2*D/C;R2=a2*a2*(D*D-A*C)/(C*C)
    identities={
      'noncircle_coefficient_difference':simp(A-B+(u-v)*lam**2/(u*v)),
      'focus_at_origin_relation':simp(D*D+C*(B-A)),
      'focus_distance_equals_center_distance_squared':simp(rad*(B-A)/(A*B)-h*h),
      'polar_dual_equal_quadratic_coefficients':simp(A*C-D*D-B*C),
      'bicentric_outer_center':simp(d+c*lam/v),
      'bicentric_outer_radius_squared':simp(R2-u*b2*b2/(v*v)),
    }
    X,Y=s.symbols('X Y')
    ox=a2*(X-c)/(a2-c*X);oy=b2*Y/(a2-c*X)
    image=A*X*X+B*Y*Y-2*D*X+C
    identities['inverse_caustic_equation']=simp((ox*ox/u+oy*oy/v-1)*(a2-c*X)**2-image)
    # Exact auxiliary-circle, focal-foot, and opposite-foot Mobius identities.
    t=s.symbols('t',real=True);aa=s.Integer(5);bb=s.Integer(3);cc=s.Integer(4)
    x=aa*(1-t*t)/(1+t*t);y=2*bb*t/(1+t*t)
    nx=x/(aa*aa);ny=y/(bb*bb)
    qx=cc+(1-cc*nx)*nx/(nx*nx+ny*ny);qy=(1-cc*nx)*ny/(nx*nx+ny*ny)
    px=aa*aa*(x+cc)/(aa*aa+cc*x);py=aa*aa*y/(aa*aa+cc*x)
    identities['direct_projection_equals_projectivity_x']=simp(qx-px)
    identities['direct_projection_equals_projectivity_y']=simp(qy-py)
    identities['auxiliary_circle']=simp(px*px+py*py-aa*aa)
    w=(px+s.I*py)/aa;e=cc/aa
    mx=aa*aa*(x-cc)/(aa*aa-cc*x);my=aa*aa*y/(aa*aa-cc*x)
    identities['focus_switch_mobius']=s.simplify((w-e)/(1-e*w)-(mx+s.I*my)/aa)
    # An exact ODE certificate for the shifted ascending Gauss identity.
    kk,ss=s.symbols('kk ss',positive=True)
    rho=(1-kk)/(1+kk);mb=4*kk/(1+kk)**2
    f2=rho*(1+kk*ss)/(1-kk*ss)
    identities['shifted_gauss_dn_ODE']=simp(kk*(kk-ss)/(1-kk*ss)-(1+kk)**2/s.Integer(4)*((2-mb)-2*f2))
    # Bicentric modulus and maximum tangent length, using alpha and c.
    al,cc2,ll=s.symbols('al cc2 ll',positive=True)
    be2=al**2-cc2**2;aa2=al**2+ll;bb2=be2+ll
    RR=al*bb2/be2;DD=cc2*ll/be2;TM2=(RR+DD)**2-aa2
    identities['bicentric_tangent_maximum_squared']=simp(TM2-ll*bb2*(al+cc2)**2/be2**2)
    identities['bicentric_modulus_is_ascending_Gauss']=simp(4*RR*DD/TM2-4*al*cc2/(al+cc2)**2)
    # Unit-circle polarity sign check at an exact offset ellipse.
    MM=s.Matrix([[3,0,-3],[0,4,0],[-3,0,-9]])
    xx0,yy0=s.symbols('xx0 yy0');lin=s.Matrix([xx0,yy0,-1])
    identities['offset_ellipse_polar_sign']=simp((lin.T*MM.inv()*lin)[0]*4-(xx0**2+yy0**2+s.Rational(2,3)*xx0-s.Rational(1,3)))
    assert all(x==0 for x in identities.values()),identities
    # Confocal conics intersect transversally: the x²,y² solution and determinant.
    xx=simp(u*a2/(u-v));yy=simp(-v*b2/(u-v))
    eq1=simp(xx/a2+yy/b2-1);eq2=simp(xx/u+yy/v-1)
    assert eq1==eq2==0
    grad_determinant=simp(4*(1/(a2*v)-1/(b2*u)))
    # Under u>v>0, lam>0 all four intersections are finite and transverse.
    assert simp(grad_determinant-4*lam*(u-v)/(a2*b2*u*v))==0
    # Homothetic 3-Poncelet family is an exact control against a universal
    # circle/conic or arbitrary Möbius area-product theorem.
    sq=s.sqrt(3);values=[]
    for co,si in [(s.Integer(1),s.Integer(0)),(s.Integer(0),s.Integer(1))]:
        P=[(aa*(co*cu-si*su),bb*(si*cu+co*su)) for cu,su in [(1,0),(-s.Rational(1,2),sq/2),(-s.Rational(1,2),-sq/2)]]
        project=lambda p,sgn:(aa*aa*(p[0]+sgn*cc)/(aa*aa+sgn*cc*p[0]),aa*aa*p[1]/(aa*aa+sgn*cc*p[0]))
        Qp=[project(p,1) for p in P];Qm=[project(p,-1) for p in P]
        # Successive tangents of the homothetic equilateral-affine triangles
        # intersect at the antipodal twice-scaled third vertex, cyclically.
        T=[(-2*p[0],-2*p[1]) for p in P]
        PT=[project(p,1) for p in T]
        values.append({'cos_phase':astr(co),'sin_phase':astr(si),'plus_area':astr(area(Qp)),'minus_area':astr(area(Qm)),
          'product':astr(area(Qp)*area(Qm)),'original_tangent_area_ratio':astr(area(T)/area(P)),
          'projected_tangent_area_ratio':astr(area(PT)/area(Qp))})
    assert values[0]['product']!=values[1]['product']
    assert values[0]['projected_tangent_area_ratio']!=values[1]['projected_tangent_area_ratio']
    return {'zero_identities':{k:astr(vv) for k,vv in identities.items()},
      'symbolic_assumptions':'u=alpha²>v=beta²>0, lam=a²-alpha²=b²-beta²>0; c=sqrt(u-v)',
      'image_conic_coefficients':{k:astr(val) for k,val in [('A',A),('B',B),('D',D),('C',C),('h',h)]},
      'noncircle_coefficient_difference':astr(A-B),
      'bicentric_polar_circle':{'incircle_radius_squared':astr(a2),'outer_center_x':astr(d),'outer_radius_squared':astr(R2),
         'limiting_point_product':astr(a2),'origin_is_limiting_point':False},
      'transverse_intersection':{'x_squared':astr(xx),'y_squared':astr(yy),'gradient_determinant_over_xy':astr(grad_determinant)},
      'nonconfocal_homothetic_N3_counterexample':{'ellipse':'x²/25+y²/9=1','caustic':'x²/(25/4)+y²/(9/4)=1','foci':['(4,0)','(-4,0)'],'phases':values,
         'product_difference':astr(s.sympify(values[0]['product'])-s.sympify(values[1]['product']))}}

def cross(p,q):return p[0]*q[1]-p[1]*q[0]
def norm(p):return mp.sqrt(p[0]*p[0]+p[1]*p[1])
def intersect(n1,n2,rhs):
    de=cross(n1,n2)
    return (rhs*(n2[1]-n1[1])/de,rhs*(n1[0]-n2[0])/de)
def project_line(p,x,y):
    d=(y[0]-x[0],y[1]-x[1]);dot=lambda a,b:a[0]*b[0]+a[1]*b[1]
    t=dot((p[0]-x[0],p[1]-x[1]),d)/dot(d,d)
    return (x[0]+t*d[0],x[1]+t*d[1])
def nstr(x):return mp.nstr(x,45)
def relrange(xs):
    return (max(xs)-min(xs))/max([mp.mpf(1)]+[abs(x) for x in xs])
def case(N,tau,kstring):
    k=mp.mpf(kstring);m=k*k;K=mp.ellipk(m);Kp=mp.ellipk(1-m);v=2*K*tau/N;alpha=mp.mpf(1);beta=mp.sqrt(1-m)
    a=mp.ellipfun('dn',v,m)/mp.ellipfun('cn',v,m);b=beta/mp.ellipfun('cn',v,m);c=k;L=4*K/N;center=K-v
    lam=a*a-alpha*alpha;bc_d=-c*lam/(beta*beta);bc_R=alpha*b*b/(beta*beta)
    def qplus(w):
        sn=mp.ellipfun('sn',w,m);cn=mp.ellipfun('cn',w,m)
        return (a*(c-a*sn)/(a-c*sn),a*b*cn/(a-c*sn))
    def trace(w):return area([qplus(w+4*K*tau*j/N) for j in range(N)])
    nome=mp.exp(-mp.pi*Kp/K);mred=mp.mfrom(q=nome**(mp.mpf(N)/2));Kr=mp.ellipk(mred);scale=2*Kr/L;amplitude=trace(center)
    mb=4*k/(1+k)**2;Kb=mp.ellipk(mb);Kbprime=mp.ellipk(1-mb);d0=-bc_d
    tM=mp.sqrt((bc_R+d0)**2-a*a);gamma=a**3*tM/(bc_R**2-d0**2)
    phases=[mp.mpf(j)/19*L for j in [1,3,7,11,16]]
    raw_products=[];raw_areas=[];raw_ratios=[];wrong_phase_products=[];data=[];err={'direct_outer_side_projection':mp.mpf(0),'mobius_focus_switch':mp.mpf(0),'bicentric_circle_residual':mp.mpf(0),'polar_equals_projective_outer':mp.mpf(0),'dn_model':mp.mpf(0),'halfperiod_product':mp.mpf(0),'focus_phase_relation':mp.mpf(0),'midpoint_outer_formula':mp.mpf(0),'gauss_circle_coordinates':mp.mpf(0),'positive_tangent_dn':mp.mpf(0),'contact_area_ratio':mp.mpf(0),'area_equals_dn_trace':mp.mpf(0),'generalized_Landen':mp.mpf(0),'Gauss_complete_periods':mp.mpf(0)}
    for w in phases:
        P=[(-a*mp.ellipfun('sn',w+4*K*tau*j/N,m),b*mp.ellipfun('cn',w+4*K*tau*j/N,m)) for j in range(N)]
        normals=[(p[0]/(a*a),p[1]/(b*b)) for p in P]
        T=[intersect(normals[j],normals[(j+1)%N],1) for j in range(N)]
        Qp=[project_line((c,0),T[j-1],T[j]) for j in range(N)]
        Qm=[project_line((-c,0),T[j-1],T[j]) for j in range(N)]
        Q=[qplus(w+4*K*tau*j/N) for j in range(N)]
        for p,q,other in zip(Qp,Q,Qm):
            err['direct_outer_side_projection']=max(err['direct_outer_side_projection'],norm((p[0]-q[0],p[1]-q[1])))
            zz=mp.mpc(*q)/a;e=c/a;zzm=(zz-e)/(1-e*zz)
            err['mobius_focus_switch']=max(err['mobius_focus_switch'],abs(zzm-mp.mpc(*other)/a))
        R=[intersect(Q[j],Q[(j+1)%N],a*a) for j in range(N)]
        PT=[(a*a*(p[0]+c)/(a*a+c*p[0]),a*a*p[1]/(a*a+c*p[0])) for p in T]
        for r,pt in zip(R,PT):
            err['polar_equals_projective_outer']=max(err['polar_equals_projective_outer'],norm((r[0]-pt[0],r[1]-pt[1])))
            err['bicentric_circle_residual']=max(err['bicentric_circle_residual'],abs((r[0]-bc_d)**2+r[1]**2-bc_R**2)/max(1,bc_R**2))
        Ap=area(Qp);Am=area(Qm);AR=area(R)
        ust=(1+k)*(w+v-K)/2;sigma=2*Kb*tau/N
        dtrace=mp.fsum(mp.ellipfun('dn',ust+j*sigma,mb) for j in range(N))
        err['Gauss_complete_periods']=max(err['Gauss_complete_periods'],abs(Kb-(1+k)*K),abs(Kbprime-(1+k)*Kp/2))
        for j in range(N):
            z=w+v+j*4*K*tau/N
            vmid=(-a*a/alpha*mp.ellipfun('sn',z,m),b*b/beta*mp.ellipfun('cn',z,m))
            err['midpoint_outer_formula']=max(err['midpoint_outer_formula'],norm((T[j][0]-vmid[0],T[j][1]-vmid[1]))/max(1,norm(T[j])))
            uj=ust+j*sigma;su=mp.ellipfun('sn',uj,mb);cu=mp.ellipfun('cn',uj,mb)
            normalized=(mp.mpc(R[j][0]-bc_d,R[j][1]))/bc_R
            err['gauss_circle_coordinates']=max(err['gauss_circle_coordinates'],abs(normalized+(1-2*su*su+2j*su*cu)))
            real_t=mp.sqrt(R[j][0]**2+R[j][1]**2-a*a)
            err['positive_tangent_dn']=max(err['positive_tangent_dn'],abs(real_t-tM*mp.ellipfun('dn',uj,mb))/max(1,real_t))
            assert cross(Q[j],Q[(j+1)%N])>0
        err['contact_area_ratio']=max(err['contact_area_ratio'],abs(Ap/AR-a*a/(bc_R**2-d0**2)))
        err['area_equals_dn_trace']=max(err['area_equals_dn_trace'],abs(Ap-gamma*dtrace)/max(1,abs(Ap)))
        old_identity_rhs=N*Kr/Kb*mp.ellipfun('dn',N*Kr/Kb*ust,mred)
        err['generalized_Landen']=max(err['generalized_Landen'],abs(dtrace-old_identity_rhs)/max(1,abs(dtrace)))
        err['focus_phase_relation']=max(err['focus_phase_relation'],abs(Am-trace(w+2*K)))
        err['dn_model']=max(err['dn_model'],abs(Ap-amplitude*mp.ellipfun('dn',scale*(w-center),mred))/max(1,abs(Ap)))
        expected=amplitude**2*mp.sqrt(1-mred)
        err['halfperiod_product']=max(err['halfperiod_product'],abs(trace(w)*trace(w+L/2)-expected)/max(1,abs(expected)))
        raw_products.append(Ap*Am);raw_areas.append(Ap);raw_ratios.append(Ap/AR);wrong_phase_products.append(Ap*trace(w+K))
        assert abs(area(list(reversed(Qp)))*area(list(reversed(Qm)))-Ap*Am)<mp.mpf('1e-45')
        data.append({'phase_over_L':nstr(w/L),'Bplus':nstr(Ap),'Bminus':nstr(Am),'product':nstr(Ap*Am),'bicentric_area':nstr(AR),'contact_to_bicentric_area_ratio':nstr(Ap/AR)})
    products=raw_products;aps=raw_areas;ratios=raw_ratios
    assert max(err.values())<mp.mpf('1e-45'),err
    if N%2:assert relrange(products)<mp.mpf('1e-40')
    else:assert relrange(products)>mp.mpf('1e-10')
    if N==3:assert relrange(wrong_phase_products)>mp.mpf('1e-4')
    return {'N':N,'turning_number':tau,'k':kstring,'precision_digits':mp.mp.dps,'a':nstr(a),'b':nstr(b),'elliptic_caustic_alpha':'1','elliptic_caustic_beta':nstr(beta),
      'reduced_model':{'mred':nstr(mred),'nome':'q^(N/2)','amplitude':nstr(amplitude),'scale':nstr(scale),'halfperiod_product':nstr(expected)},
      'max_errors':{k:nstr(vv) for k,vv in err.items()},'relative_product_range':nstr(relrange(products)),'relative_plus_area_range':nstr(relrange(aps)),'wrong_original_K_shift_product_range':nstr(relrange(wrong_phase_products)),
      'contact_ratio_observation_range':nstr(relrange(ratios)),'contact_ratio_status':'fresh exact audit derivation in EXACT_BICENTRIC_DN_BRIDGE.md; numerical values corroborate, no historical-priority inference' ,'samples':data}

def main():
    exact=exact_certificates()
    specs=[(3,1,'.7'),(5,1,'.7'),(5,2,'.7'),(7,1,'.9'),(7,2,'.7'),(7,3,'.7'),(9,2,'.55'),(11,4,'.7'),(4,1,'.7'),(6,1,'.7'),(8,3,'.7')]
    numerical=[case(*args) for args in specs]
    out={'format':'PR210 classical/general controls v1','deterministic':True,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'python':sys.version,
      'sympy_version':s.__version__,'mpmath_version':mp.__version__,'exact':exact,'numerical':numerical,
      'interpretation':'Exact identities establish object bridges and exact counterexamples to overbroad extensions. High-precision computations diagnose the target and conditional classical dn model; they do not certify priority or replace the proof.'}
    (BASE/'CONTROL_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'exact_zero_identities':len(exact['zero_identities']),'numerical_cases':len(numerical),'all_assertions_passed':True,'odd_cases':[x['N'] for x in numerical if x['N']%2],'even_negative_controls':[x['N'] for x in numerical if not x['N']%2]},indent=2))
if __name__=='__main__':main()

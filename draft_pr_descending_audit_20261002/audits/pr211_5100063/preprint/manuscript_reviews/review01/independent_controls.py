"""Fresh whole-manuscript checks; no import of candidate or inherited programs."""
import hashlib,json,math
from pathlib import Path
import mpmath as mp
import sympy as sp

mp.mp.dps=100
HERE=Path(__file__).resolve().parent
maxerr={}
def check(name,a,b,tol=mp.mpf('1e-70')):
    error=abs(a-b)/max(mp.mpf(1),abs(a),abs(b))
    maxerr[name]=max(maxerr.get(name,mp.mpf(0)),error)
    assert error<tol,(name,mp.nstr(error,10))
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def area(points):return sum(det(points[i],points[(i+1)%len(points)]) for i in range(len(points)))/2
def inv(q,f,rho=1):
    dx,dy=q[0]-f,q[1]
    den=dx*dx+dy*dy
    return (f+rho*rho*dx/den,rho*rho*dy/den)

# Independent polynomial certificate of the factor numerators before division.
k,t,x,C,d=sp.symbols('k t x C d')
q=1-t;m=k*k;D=1-m*t*x*x
U=1-2*m*t+m*t*t;V=1-2*t+m*t*t
def reduce(poly):
    poly=sp.Poly(sp.expand(poly),C,d)
    out=0
    for (i,j),coeff in poly.terms():
        out+=coeff*C**(i%2)*d**(j%2)*q**(i//2)*(1-m*t)**(j//2)
    return sp.factor(out)
certificates={
 'factor1_numerator':reduce((D+k*x*C*d)**2-m*t*(1-x*x)*(1-m*x*x)-D*(d+k*C*x)**2),
 'factor2_after_Cd_multiplication':reduce(C*d*((U*D+k*V*x*C*d)**2-m*V*V*t*(1-x*x)*(1-m*x*x))-D*(d+k*C*x)*(C*(U*U-m*V*V*t)+k*d*(V*V-U*U*t)*x)),
 'triple_D_numerator':sp.factor(U*U-m*V*V*t-(1-m*t)*(U*(1-m*t*t)-2*m*t*q*V)),
 'triple_C_numerator':sp.factor(V*V-U*U*t-q*(V*(1-m*t*t)-2*t*(1-m*t)*U)),
 'outer_original_focal_difference':sp.factor((1-m*t)**2-(1-m)-m*q*q+m*(1-m)*t*t),
}
assert all(v==0 for v in certificates.values()),certificates

counts={'families':0,'direct_phase_pairs':0,'complex_edge_points':0,'pole_neighborhoods':0,'scaling_radius_repetition_checks':0}
pole_diagnostics=[]
for ks in ['0.01','0.3','0.83','0.999']:
    kval=mp.mpf(ks);mval=kval*kval;K=mp.ellipk(mval);H=mp.ellipk(1-mval)
    sn=lambda z:mp.ellipfun('sn',z,mval)
    cn=lambda z:mp.ellipfun('cn',z,mval)
    dn=lambda z:mp.ellipfun('dn',z,mval)
    for N in [3,5,7,9,11,15]:
      for tau in range(1,(N+1)//2):
        if math.gcd(tau,N)!=1:continue
        v=2*K*tau/N;step=2*v;L=4*K/N;p=1j*H;r0=3*K+p;R=r0+v
        h,Cv,dv=sn(v),cn(v),dn(v);tv=h*h;qv=Cv*Cv
        al=mp.mpf('1.7');be=al*mp.sqrt(1-mval);focus=al*kval
        a=al*dv/Cv;b=be/Cv;Ao=al*dv*dv/qv;Bo=be/qv
        Uv=1-2*mval*tv+mval*tv*tv;Vv=1-2*tv+mval*tv*tv
        L0=(Uv*Uv-mval*Vv*Vv*tv)/dv;L1=(Vv*Vv-Uv*Uv*tv)/Cv
        C0=Bo*h*dv*qv**4/(al**3*Cv)
        def Q(z):
            # Solve the two tangent line equations independently, not outer formula.
            sm,cm=sn(z-v),cn(z-v);sp_,cp=sn(z+v),cn(z+v)
            A1,B1=-sm/a,cm/b;A2,B2=-sp_/a,cp/b
            den=A1*B2-B1*A2
            return ((B2-B1)/den,(A1-A2)/den)
        def e_direct(z):
            left=inv(Q(z-v),focus);right=inv(Q(z+v),focus)
            # Remove the same constant focal translation before a single edge.
            return det((left[0]-focus,left[1]),(right[0]-focus,right[1]))/2
        def e(z):
            s=sn(z)
            return C0*dn(z)*(1-mval*tv*s*s)/((dv+kval*Cv*s)**2*(L0+kval*L1*s))
        def F(z):return sum(e(z+j*step) for j in range(N))
        product0=None
        for phase in [mp.mpf('0.071')*K,mp.mpf('0.347')*K,mp.mpf('1.213')*K]:
            qs=[Q(phase+j*step) for j in range(N)]
            for j,z in enumerate([phase+j*step for j in range(N)]):
                check('outer_x',qs[j][0],-Ao*sn(z));check('outer_y',qs[j][1],Bo*cn(z))
            plus=area([inv(qp,focus) for qp in qs]);minus=area([inv(qp,-focus) for qp in qs])
            check('direct_area_cyclic_edge',plus,F(phase+v))
            assert plus>0 and minus>0
            product=plus*minus
            if product0 is None:product0=product
            check('direct_phase_invariance',product,product0)
            check('focus_halfperiod',minus,F(phase+v+L/2))
            for z in [phase+mp.mpf('0.17')*p]:
                check('direct_complex_edge',e_direct(z),e(z));counts['complex_edge_points']+=1
            counts['direct_phase_pairs']+=1
        # Probe the leading double parts at their actual two complex fibers.
        eps=mp.mpf('1e-22')*K
        aplus=(e(r0+v+eps)+e(r0+v-eps))*eps**2/2
        aminus=(e(r0-v+eps)+e(r0-v-eps))*eps**2/2
        check('opposite_double_principal_parts',aplus,-aminus,tol=mp.mpf('1e-35'))
        if ks in ['0.3','0.83'] and N in [3,5,7]:
            # Small-circle samples independently recover Laurent coefficients by DFT.
            eps=mp.mpf('1e-9')*K
            for center,kind in [(R,'trace_simple'),(r0+3*v,'second_fiber'),(p,'jacobi_pole')]:
                vals=[e(center+eps*mp.exp(2j*mp.pi*j/32)) for j in range(32)]
                c2=sum(vals[j]*(eps*mp.exp(2j*mp.pi*j/32))**2 for j in range(32))/32
                if kind!='trace_simple':assert abs(c2)<mp.mpf('1e-60'),(N,tau,kind,c2)
                if kind=='jacobi_pole':
                    c1=sum(vals[j]*(eps*mp.exp(2j*mp.pi*j/32)) for j in range(32))/32
                    assert abs(c1)<mp.mpf('1e-60'),(N,tau,kind,c1)
                counts['pole_neighborhoods']+=1
            vals=[F(R+eps*mp.exp(2j*mp.pi*j/32)) for j in range(32)]
            c2=sum(vals[j]*(eps*mp.exp(2j*mp.pi*j/32))**2 for j in range(32))/32
            c1=sum(vals[j]*(eps*mp.exp(2j*mp.pi*j/32)) for j in range(32))/32
            assert abs(c2)<mp.mpf('1e-60') and abs(c1)>mp.mpf('1e-8')
            zero=F(R+L/2)
            assert abs(zero)<mp.mpf('1e-75'),(N,tau,zero)
            pole_diagnostics.append({'k':ks,'N':N,'tau':tau,'double_trace_dft_abs':mp.nstr(abs(c2),8),'simple_trace_residue_abs':mp.nstr(abs(c1),8),'complementary_zero_abs':mp.nstr(abs(zero),8)})
        if N==3 and ks=='0.3':
            qs=[Q(mp.mpf('.37')+j*step) for j in range(N)]
            for scale,rho,repeat in [(mp.mpf('2.7'),mp.mpf('1.3'),3),(mp.mpf('.4'),mp.mpf('2.1'),4)]:
                scaled=[(scale*x,scale*y) for x,y in qs]*repeat
                got=area([inv(z,scale*focus,rho) for z in scaled])*area([inv(z,-scale*focus,rho) for z in scaled])
                original=area([inv(z,focus) for z in qs])*area([inv(z,-focus) for z in qs])
                check('scale_radius_repeat',got,original*repeat**2*rho**8/scale**4)
                check('reversal',area(list(reversed(qs))),-area(qs))
                counts['scaling_radius_repetition_checks']+=1
        counts['families']+=1

result={'status':'PASS','precision_digits':mp.mp.dps,'exact_polynomial_certificates':{k:str(v) for k,v in certificates.items()},'counts':counts,'largest_relative_errors':{k:mp.nstr(v,9) for k,v in maxerr.items()},'pole_diagnostics':pole_diagnostics,'limitations':'Numerical contour extraction and phase samples are diagnostics, not proof or interval certification. Exact identities are symbolic. Independent analytic reconstruction is in REPORT.md.'}
(HERE/'INDEPENDENT_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

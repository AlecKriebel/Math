#!/usr/bin/env python3
"""Fresh adversarial controls for the C1 characteristic existence audit.

Formal identities are universal within the displayed finite-dimensional polynomial
families only. Numeric observations are finite diagnostics. Neither establishes the
general Banach-space theorem, which is proved in the written reconstruction.
"""
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
import hashlib,json,math,sys
import sympy as s

HERE=Path(__file__).resolve().parent
counts=Counter(); failures=[]; evidence={}
def check(name,condition):
    if not bool(condition):
        failures.append(name)
        raise AssertionError(name)
    counts[name]+=1
def zero(name,expression): check(name,s.factor(expression)==0)

# Length one is a harmless normalization for this algebraic coordinate family.
x,a,b,d,v0,g=s.symbols('x a b d v0 g',real=True)
X=x+a*x*(1-x); jac=s.diff(X,x)
V=v0+b*x*(1-x)+d*x*(1-x)*(2*x-1)
mean=s.integrate(V*jac,(x,0,1))
K=s.integrate((V-mean)*jac,(x,0,x))
weighted_constant=s.integrate(K*jac,(x,0,1))
H=K-weighted_constant
zero('parametric_degree_one_lift',X.subs(x,1)-X.subs(x,0)-1)
zero('parametric_velocity_endpoint_values',V.subs(x,1)-V.subs(x,0))
zero('parametric_primitive_endpoint_values',H.subs(x,1)-H.subs(x,0))
zero('parametric_zero_physical_primitive_mean',s.integrate(H*jac,(x,0,1)))
zero('parametric_primitive_derivative',s.diff(H,x)-(V-mean)*jac)
zero('parametric_physical_mean_conservation',s.integrate(H*jac+V*s.diff(V,x),(x,0,1)))
physical_slope=s.diff(V,x)/jac
slope_acceleration=(s.diff(H,x)*jac-s.diff(V,x)**2)/jac**2
zero('parametric_corrected_Riccati',slope_acceleration-(V-mean-physical_slope**2))

# Relabeling changes the interval coordinate and is allowed to have different
# endpoint derivatives. For |a|,|g|<1 both original and relabeled lifts are positive.
r=x+g*x*(1-x)
Xr=s.expand(X.subs(x,r)); Vr=s.expand(V.subs(x,r)); ar=s.diff(Xr,x)
mr=s.integrate(Vr*ar,(x,0,1))
Kr=s.integrate((Vr-mr)*ar,(x,0,x))
Hr=Kr-s.integrate(Kr*ar,(x,0,1))
zero('parametric_relabel_mean_naturality',mr-mean)
zero('parametric_relabel_K_naturality',Kr-K.subs(x,r))
zero('parametric_relabel_H_naturality',Hr-H.subs(x,r))

# An integration-by-parts control needs equal endpoint values, not endpoint slopes.
test=1+x*x*(1-x)**2
zero('parametric_weak_flux_corner_boundary_cancellation',
     s.integrate(V*s.diff(V,x)*test+V*V*s.diff(test,x)/2,(x,0,1)))

# Exact negative controls intentionally implement incorrect or inadmissible choices.
point={a:s.Rational(1,2),b:s.Rational(2,3),d:s.Rational(3,5),v0:s.Rational(7,11)}
unweighted_mean=s.integrate(V,(x,0,1))
wrong_mean_K=s.integrate((V-unweighted_mean)*jac,(x,0,x))
wrong_mean_endpoint=s.factor(wrong_mean_K.subs(x,1))
check('negative_unweighted_label_mean_breaks_periodicity',wrong_mean_endpoint.subs(point)!=0)
wrong_H=K-s.integrate(K,(x,0,1))
wrong_H_physical_mean=s.factor(s.integrate(wrong_H*jac,(x,0,1)))
check('negative_unweighted_primitive_constant_changes_mean',wrong_H_physical_mean.subs(point)!=0)
K_no_mean=s.integrate(V*jac,(x,0,x))
check('negative_no_mean_subtraction_breaks_periodicity',K_no_mean.subs(x,1).subs(point)!=0)
nonperiodic_velocity=1+x
check('negative_nonperiodic_velocity_breaks_mean_conservation',
      s.integrate(nonperiodic_velocity*s.diff(nonperiodic_velocity,x),(x,0,1))==s.Rational(3,2))
folded=X.subs(a,2)
check('negative_degree_one_without_injectivity',folded.subs(x,s.Rational(1,2))==folded.subs(x,1))
check('negative_folded_jacobian',s.diff(folded,x).subs(x,1)==-1)
evidence['wrong_mean_endpoint_residual']=str(wrong_mean_endpoint)
evidence['wrong_primitive_physical_mean_residual']=str(wrong_H_physical_mean)
evidence['folded_map']='X=x+2x(1-x): X(1/2)=X(1)=1, Xprime(1)=-1'

# Independently derive the exact background characteristic: z_t=z(z-L)/6.
P,R,theta=s.symbols('P R theta',positive=True)
L=2*P; kap=P/3; speed=kap**2
z=L*x/(x+(L-x)*R)
phi=lambda q:(q-P)**2/6-P**2/18
primitive=lambda q:((q-P)**3-P**2*(q-P))/18
zero('background_logistic_characteristic',kap*R*s.diff(z,R)-(phi(z)-speed))
zero('background_characteristic_acceleration',kap*R*s.diff(phi(z),R)-primitive(z))
zero('background_right_jacobian',s.diff(z,x).subs(x,0)-1/R)
zero('background_left_jacobian',s.diff(z,x).subs(x,L)-R)
check('negative_forced_matching_endpoint_derivatives',
      s.diff(phi(x),x).subs(x,0)!=s.diff(phi(x),x).subs(x,L))
zero('background_right_physical_slope',
     (s.diff(phi(z),x)/s.diff(z,x)).subs(x,0)+kap)
zero('background_left_physical_slope',
     (s.diff(phi(z),x)/s.diff(z,x)).subs(x,L)-kap)
wm,wp,f=s.symbols('wm wp f',real=True)
zero('general_corner_jump_identity',
     (f-wm**2)-(f-wp**2)+(wm+wp)*(wm-wp))
# A literal-v1 Section 4 domain falsifier: adding e*sin(x) gives the same
# smooth perturbation slope e on both sides and hence a nonconstant jump.
e=s.symbols('e',nonzero=True,real=True)
v1_wm=kap+e; v1_wp=-kap+e; v1_J=v1_wm-v1_wp
v1_Jt=-(v1_wm+v1_wp)*v1_J
zero('v1_fixed_peak_smooth_perturbation_jump_derivative',v1_Jt+4*kap*e)
check('negative_v1_smooth_perturbation_class_not_invariant',v1_Jt!=0)
evidence['v1_smooth_perturbation_domain_control']='u0=phi+e*sin(x): J(0)=2*kappa, Jprime(0)=-4*kappa*e. A fixed translated phi plus a smooth periodic perturbation would force J(t)=2*kappa.'
# On 0<x<theta, derivatives of phi(x) and phi(x-theta+L) differ by this quantity.
zero('negative_periodic_W1infinity_translation_continuity',
     s.diff(phi(x),x)-s.diff(phi(x-theta+L),x)-(-2*kap+theta/3))

# A fixed C1 cutoff proxy checks scaling only; it is not the C-infinity cutoff
# used in the theorem and is deliberately labeled as such.
y,delta=s.symbols('y delta',positive=True)
rho=(1-y)**4*(1+4*y)
raw=-delta*x*rho.subs(y,x/delta**2)
zero('cutoff_proxy_amplitude_scaling',raw.subs(x,y*delta**2)/delta**3+y*rho)
zero('cutoff_proxy_slope_scaling',s.diff(raw,x).subs(x,y*delta**2)/delta+rho+y*s.diff(rho,y))
zero('cutoff_proxy_second_derivative_scaling',
     delta*s.diff(raw,x,2).subs(x,y*delta**2)+2*s.diff(rho,y)+y*s.diff(rho,y,2))
second_coefficient=s.factor((delta*s.diff(raw,x,2)).subs(x,delta**2/4))
check('negative_C2_lifespan_control_would_not_be_uniform',second_coefficient!=0 and not second_coefficient.has(delta))
evidence['proxy_second_derivative_at_quarter_width']=str(second_coefficient)+'/delta'

numeric_scaling=[]
for dd in [0.1,0.01,0.0001]:
    amp=float((-y*rho).subs(y,s.Rational(1,4)))*dd**3
    slope=float((-(rho+y*s.diff(rho,y))).subs(y,s.Rational(1,4)))*dd
    second=float(second_coefficient)/dd
    check('finite_float_proxy_small_C1_large_C2',abs(amp)<dd**3 and abs(slope)<2*dd and abs(second)>1/dd)
    numeric_scaling.append({'delta':dd,'amplitude_at_quarter_width':amp,'slope_at_quarter_width':slope,'second_derivative_at_quarter_width':second})
evidence['finite_numeric_scaling']=numeric_scaling
numeric_background=[]
for tt in [0.,1.,5.,10.]:
    kk=math.pi/3; ll=2*math.pi; rr=math.exp(kk*tt)
    vals=[]
    for xx in [0.,ll/4,ll/2,3*ll/4,ll]:
        denom=xx+(ll-xx)*rr
        zz=ll*xx/denom
        aa=ll*ll*rr/(denom*denom)
        slope=(zz-math.pi)/3
        check('finite_float_background_invertibility_and_slope',aa>0 and abs(slope)<=kk*(1+1e-14))
        vals.append({'label':xx,'relative_position':zz,'jacobian':aa,'physical_slope':slope})
    numeric_background.append({'time':tt,'samples':vals})
evidence['finite_numeric_background']=numeric_background

receipt={'status':'PASS','utc':datetime.now(timezone.utc).isoformat(),
         'python':sys.version,'executable':sys.executable,'sympy_version':s.__version__,
         'checks':dict(counts),'assertions':sum(counts.values()),'failures':failures,
         'control_scope':{'parametric_exact':'Universal algebra within explicitly displayed polynomial/rational families, not general functions or a PDE existence proof.',
                          'negative_exact':'Exact counterexamples to deliberately wrong mean/primitive, nonperiodic endpoint values, folded map, forced matching derivatives, false translation continuity, and second-derivative lifetime dependence.',
                          'numeric':'23 finite floating-point observations only; no validated PDE simulation or universal inference.',
                          'general_theorem':'Written independent reconstruction supplies Banach bounds, Picard, weak formulation, continuation and smoothness arguments.'},
         'evidence':evidence,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(HERE/'CONTROL_RESULTS.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='evidence'},indent=2))

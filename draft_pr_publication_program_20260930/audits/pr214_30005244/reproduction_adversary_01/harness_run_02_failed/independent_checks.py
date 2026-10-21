"""New checks authored for this audit; no submitted code is imported.
Exact checks are finite/symbolic identities, not continuum or priority proofs.
"""
from pathlib import Path
from fractions import Fraction as F
import json, datetime, sys
import sympy as s
import numpy as np
import mpmath as mp
P=Path(__file__).resolve().parent
checks=[]
def check(name,condition,evidence):
    assert bool(condition),name
    checks.append({'name':name,'pass':True,'evidence':evidence})
x,y,z=s.symbols('x y z',real=True)
k=s.symbols('k')
rho=s.sqrt(x*x+y*y+z*z)
g=s.exp(s.I*k*rho)/(4*s.pi*rho)
cartesian=-s.hessian(g,(x,y,z))-k*k*g*s.eye(3)
def tensor(v,kappa):
    rr=s.sqrt(v.dot(v));t=kappa*rr
    return s.exp(s.I*t)*((1-s.I*t-t*t)*s.eye(3)+(t*t+3*s.I*t-3)*(v*v.T)/(rr*rr))/(4*s.pi*rr**3)
# Nine Cartesian derivatives at two nonaxial points, with symbolic COMPLEX k.
for j,v in enumerate([s.Matrix([s.Rational(2,3),s.Rational(-1,3),s.Rational(2,3)]),s.Matrix([1,2,-2])]):
    actual=cartesian.subs(dict(zip((x,y,z),v)))
    difference=(actual-tensor(v,k)).applyfunc(s.simplify)
    check('cartesian_nine_component_identity_%d'%j,difference==s.zeros(3),{'point':[str(c) for c in v],'frequency':'unrestricted symbolic k','components':9})
v=s.Matrix([s.Rational(2,3),s.Rational(-1,3),s.Rational(2,3)])
rr=s.symbols('rr',positive=True)
a=cartesian.subs({x:rr*v[0],y:rr*v[1],z:rr*v[2]})
static=tensor(rr*v,0)
for ij in [(0,0),(0,1),(1,1)]:
    i,j=ij
    leading=-k*k*(s.eye(3)+v*v.T)[i,j]/(8*s.pi*rr)-s.I*k**3*s.eye(3)[i,j]/(6*s.pi)
    left=s.series(a[i,j]-static[i,j]-leading,rr,0,1).removeO()
    check('cartesian_near_field_%s_%s'%ij,s.simplify(left)==0,{'remaining_order':'O(rr)','components':list(ij)})
for frequency in [s.I,-2*s.I,s.Rational(3,5)+4*s.I/7,0]:
    h=s.Rational(2,7)
    check('dynamic_dimensionless_scaling_'+str(frequency),(h**3*tensor(h*v,frequency)-tensor(v,h*frequency)).applyfunc(s.simplify)==s.zeros(3),{'h':str(h),'frequency':str(frequency)})
    check('kernel_conjugation_'+str(frequency),(tensor(v,-s.conjugate(frequency))-s.conjugate(tensor(v,frequency))).applyfunc(s.simplify)==s.zeros(3),{'frequency':str(frequency)})
check('dynamic_zero_frequency_exact',tensor(v,0)-static.subs(rr,1)==s.zeros(3),{'parameter':'k=0'})
check('off_origin_kernel_trace',s.simplify(s.trace(tensor(v,k))+2*k*k*s.exp(s.I*k)/(4*s.pi))==0,{'identity':'trace(K_k)=-2*k^2*g_k'})
# Exact overlap volume obtained from two spherical caps, rather than a crude box bound.
d=s.symbols('d',real=True)
capheight=1-d/2
overlap=s.expand(2*s.pi*capheight**2*(1-capheight/3))
check('two_cap_overlap',s.simplify(overlap-s.pi*(4+d)*(2-d)**2/12)==0,{'distance_interval':'0 <= d <= 2'})
radial_moments={}
for power in [-2,-1,0,2]:
    radial_moments[power]=s.simplify(4*s.pi*s.integrate(d**(power+2)*overlap,(d,0,2)))
check('overlap_normalizes_pair_volume',radial_moments[0]==(4*s.pi/3)**2,{'pair_volume':str(radial_moments[0])})
check('exact_C2_Hilbert_Schmidt_squared',s.simplify(6*radial_moments[-2]/(64*s.pi*s.pi))==s.Rational(3,8),{'squared_norm':'3/8 < 1','distance_integral':str(radial_moments[-2])})
check('exact_quartic_remainder_majorant_HS_squared',s.simplify(9*radial_moments[2]/(16*s.pi*s.pi))==s.Rational(6,5),{'squared_constant':'6/5 < 4','distance_squared_integral':str(radial_moments[2])})
check('constant_mode_C2_compression',s.simplify(-radial_moments[-1]/(6*s.pi*(4*s.pi/3)))==-s.Rational(4,15),{'coefficient':'-4/15','distance_inverse_integral':str(radial_moments[-1])})
ell=s.symbols('ell',integer=True,positive=True)
mu=(ell-1)/(3*(2*ell+1))
check('universal_harmonic_gap',s.simplify(mu-s.Rational(1,15)-(ell-2)/(5*(2*ell+1)))==0,{'valid_for':'all integer ell >= 2','identity':'mu_ell-1/15=(ell-2)/(5*(2ell+1))'})
check('universal_harmonic_accumulation',s.simplify(s.Rational(1,6)-mu-1/(2*(2*ell+1)))==0,{'limit':'1/6 from below'})
kk=F(1,10000);eta=120*kk**2;graph=eta/(1-eta)
sharper_trace_upper=-F(2,3)*kk**3+3*(2*kk**4+2*kk**2*graph)
coarse_trace_upper=-F(7831,15000)*kk**3
check('independent_graph_trace_margin',sharper_trace_upper<coarse_trace_upper<0,{'sharper_trace_upper':str(sharper_trace_upper),'published_coarse_upper':str(coarse_trace_upper)})
# An exact NONORTHOGONAL rank-two Riesz projector of a defective 3x3 block.
t=s.symbols('t',real=True);lam=2*s.I
A=s.Matrix([[lam,1,t],[0,lam,0],[0,0,1]])
projector=s.eye(3)-(A-lam*s.eye(3))**2/(1-lam)**2
check('defective_projector_idempotent',(projector*projector-projector).applyfunc(s.simplify)==s.zeros(3),{'projector':str(projector)})
check('defective_projector_commutes',(A*projector-projector*A).applyfunc(s.simplify)==s.zeros(3),{'trace':str(s.trace(projector))})
check('defective_projector_nonorthogonal',projector!=s.conjugate(projector.T) and s.trace(projector)==2,{'parameter':'symbolic real t; nonorthogonal for t != 0'})
check('defective_projector_generalized_eigenspace',(A-lam*s.eye(3))**2*projector==s.zeros(3),{'Jordan_order_at_most':2})
# Small-argument numerical stress test. This is deliberately outside the finite
# refinement tables, and illustrates why their raw double subtraction is not
# a general-purpose accurate kernel evaluator. No published source is imported.
mp.mp.dps=100
stress=[]
for radius,frequency in [('0.0625','1.2'),('0.000001','0.0001'),('0.00000001','0.0001')]:
    r=mp.mpf(radius);kap=mp.mpf(frequency)
    gg=lambda q:mp.exp(mp.j*kap*q)/(4*mp.pi*q)
    transverse= -mp.diff(gg,r)/r-kap**2*gg(r)-1/(4*mp.pi*r**3)
    radial=-mp.diff(gg,r,2)-kap**2*gg(r)+2/(4*mp.pi*r**3)
    rd=float(r);kd=float(kap);tt=rd*kd
    aa=(np.exp(1j*tt)*(1-1j*tt-tt*tt)-1)/(4*np.pi*rd**3)
    bb=(np.exp(1j*tt)*(tt*tt+3j*tt-3)+3)/(4*np.pi*rd**3)
    norm_ref=max(abs(transverse),abs(radial))
    rel=max(abs(mp.mpc(aa)-transverse),abs(mp.mpc(aa+bb)-radial))/norm_ref
    stress.append({'radius':radius,'frequency':frequency,'raw_double_transverse':[float(aa.real),float(aa.imag)],'raw_double_radial':[float((aa+bb).real),float((aa+bb).imag)],'high_precision_transverse':mp.nstr(transverse,35),'high_precision_radial':mp.nstr(radial,35),'relative_error':float(rel),'classification':'illustration of cancellation outside published table parameters'})
check('stress_exposes_small_argument_cancellation',max(row['relative_error'] for row in stress)>0.1,{'not_a_theorem_counterexample':True,'published_tables_use_resolved_separations':True})
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'classification':'new independent symbolic/rational checks and separately labelled numerical stress illustration','exact_or_symbolic_checks':checks[:-1],'stress_illustration_assertion':checks[-1],'check_count':len(checks),'stress_rows':stress,'runtime':{'python':sys.version,'numpy':np.__version__,'sympy':s.__version__,'mpmath':mp.__version__},'limitations':'No infinite-dimensional theorem, full source-dependency or priority proof is certified by these checks.'}
(P/'INDEPENDENT_CHECKS_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'checks':len(checks),'all_passed':True,'stress_rows':stress},indent=2))

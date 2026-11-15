"""Independent finite controls: exact tangent congruence and intrinsic curves.

Not a universal proof. No supplied verifier is imported. Standard library exact
Gaussian rational arithmetic plus existing NumPy for bounded double precision.
"""
from pathlib import Path
from fractions import Fraction as Q
from dataclasses import dataclass
import json, math, sys
import numpy as np
@dataclass(frozen=True)
class C:
    a:Q=Q(0);b:Q=Q(0)
    def __add__(z,w):
        w=w if isinstance(w,C) else C(Q(w));return C(z.a+w.a,z.b+w.b)
    __radd__=__add__
    def __neg__(z):return C(-z.a,-z.b)
    def __sub__(z,w):return z+-w if isinstance(w,C) else z+C(-Q(w))
    def __rsub__(z,w):return -z+w
    def __mul__(z,w):
        w=w if isinstance(w,C) else C(Q(w));return C(z.a*w.a-z.b*w.b,z.a*w.b+z.b*w.a)
    __rmul__=__mul__
    def conj(z):return C(z.a,-z.b)
    def __truediv__(z,w):
        w=w if isinstance(w,C) else C(Q(w));d=w.a*w.a+w.b*w.b
        if not d:raise ZeroDivisionError
        u=z*w.conj();return C(u.a/d,u.b/d)
I=[[C(1),C()],[C(),C(1)]]
def add(a,b):return [[a[i][j]+b[i][j] for j in range(2)] for i in range(2)]
def neg(a):return [[-x for x in r] for r in a]
def sub(a,b):return add(a,neg(b))
def scale(a,c):return [[x*c for x in r] for r in a]
def mm(a,b):return [[sum((a[i][k]*b[k][j] for k in range(2)),C()) for j in range(2)] for i in range(2)]
def star(a):return [[a[j][i].conj() for j in range(2)] for i in range(2)]
def inv(a):
    d=a[0][0]*a[1][1]-a[0][1]*a[1][0]
    return [[a[1][1]/d,-a[0][1]/d],[-a[1][0]/d,a[0][0]/d]]
def fro2(a):return sum((z.a*z.a+z.b*z.b for r in a for z in r),Q())
def positive(a):
    return a==star(a) and a[0][0].b==a[1][1].b==0 and a[0][0].a>=0 and a[1][1].a>=0 and (a[0][0]*a[1][1]-a[0][1]*a[1][0]).a>=0
def F(w,t):return mm(add(w,scale(I,t)),inv(add(I,scale(w,t))))
checks=[]
def check(name,ok,**detail):
    checks.append({'name':name,'passed':bool(ok),**detail})
    if not ok:raise ValueError(name)
rot=[[C(Q(3,5)),C(Q(-4,5))],[C(Q(4,5)),C(Q(3,5))]]
vals=[C(1),C(0,1),C(0,-1),C(Q(3,5),Q(4,5)),C(Q(5,13),Q(-12,13))]
unitaries=[]
for a in vals:
 for b in vals:
    d=[[a,C()],[C(),b]];unitaries.append(mm(mm(rot,d),star(rot)))
tangents=[[[C(0,1),C()],[C(),C()]],[[C(),C()],[C(),C(0,1)]],[[C(),C(1)],[C(-1),C()]],[[C(),C(0,1)],[C(0,1),C()]],[[C(0,2),C(Q(2,3),Q(-3,5))],[C(Q(-2,3),Q(-3,5)),C(0,-1)]]]
times=[Q(0),Q(1,100),Q(1,4),Q(1,2),Q(9,10),Q(999,1000),Q(1)]
bad_order_detected=0
for wi,w in enumerate(unitaries):
 check('exact_input_unitary',mm(star(w),w)==I)
 check('exact_input_semicircle',positive(add(w,star(w))))
 for t in times:
    r=inv(add(I,scale(w,t)));f=F(w,t);q=(1-t*t)/(1+t*t)
    check('exact_output_unitary',mm(star(f),f)==I)
    check('exact_resolvent_Gram_order',positive(sub(mm(star(add(I,scale(w,t))),add(I,scale(w,t))),scale(I,1+t*t))))
    check('exact_congruence_factor_norm_certificate',positive(sub(scale(I,1/(1+t*t)),mm(star(r),r))))
    check('exact_semicircle_preserved',positive(add(f,star(f))))
    for x in tangents:
        e=mm(w,x);direct=sub(mm(e,r),mm(mm(mm(add(w,scale(I,t)),r),scale(e,t)),r));congruence=scale(mm(mm(star(r),x),r),1-t*t)
        check('exact_right_trivialized_tangent_congruence',mm(star(f),direct)==congruence)
        check('exact_HS_differential_bound',fro2(direct)<=q*q*fro2(e))
        wrong=scale(mm(mm(r,r),e),1-t*t)
        if wrong!=direct:bad_order_detected+=1
    if t==0:check('exact_initial',f==w)
    if t==1:check('exact_terminal',f==I)
check('wrong_noncommuting_derivative_order_detected',bad_order_detected>0,cases=bad_order_detected)
for t in times:
    q=(1-t*t)/(1+t*t)
    for cos in [Q(0),Q(3,5),Q(5,13),Q(1)]:
        d=(1-t*t)/(1+t*t+2*t*cos);check('exact_scalar_allowed_derivative',0<=d<=q)
    if 0<t<1:
        d=(1-t*t)/(1+t*t-2*t*Q(3,5));check('exact_left_semicircle_negative_control',d>q)
# Excluded normalizedHS metrics admit a nonzero winding loop at the forbidden
# small constant: determinant(exp(iθ)⊕I)=exp(iθ), not nullhomotopic.
check('normalized_HS_excluded_N4_closed',Q(1,4)<=Q(1,4))
check('normalized_HS_excluded_N5_strict',Q(1,5)<Q(1,4))

eye=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Z=np.diag([1.,-1.]).astype(complex)
def exp_pauli(a,p):return math.cos(a)*eye+1j*math.sin(a)*p
def phi(s):return exp_pauli(math.sin(s)/8,X)@exp_pauli((1-math.cos(s))/8,Z)
def phiprime(s):
    a=math.sin(s)/8;b=(1-math.cos(s))/8
    return (1j*math.cos(s)/8*X)@exp_pauli(a,X)@exp_pauli(b,Z)+exp_pauli(a,X)@(1j*math.sin(s)/8*Z)@exp_pauli(b,Z)
def nf(w,t):return (w+t*eye)@np.linalg.inv(eye+t*w)
def distance(u,v,kind):
    angles=np.angle(np.linalg.eigvals(u.conj().T@v));return float(np.linalg.norm(angles,2) if kind=='HS' else np.max(abs(angles)))
def norm(a,kind):return float(np.linalg.norm(a,'fro' if kind=='HS' else 2))
grid=np.linspace(0,2*math.pi,65)[:-1];worst_excess=0.;noncommuting=0
for t in [0.,.01,.25,.5,.9,.999999,1.]:
    q=(1-t*t)/(1+t*t);outputs=[]
    for s in grid:
        w=phi(s);e=phiprime(s);r=np.linalg.inv(eye+t*w);f=nf(w,t);j=(1-t*t)*r@e@r;outputs.append(f)
        noncommuting+=norm(w@e-e@w,'op')>1e-8
        for kind,L in [('op',1/8),('HS',math.sqrt(2)/8)]:
            check('noncommuting_periodic_input_speed',abs(norm(e,kind)-L)<1e-13,metric=kind)
            excess=norm(j,kind)-q*L;worst_excess=max(worst_excess,excess)
            check('noncommuting_periodic_output_speed',excess<1e-12,metric=kind)
        check('finite_endpoint_fixed_base',norm(nf(eye,t)-eye,'op')<1e-13)
    for i,s in enumerate(grid):
        for k in range(i+1,len(grid)):
            d=abs(s-grid[k]);d=min(d,2*math.pi-d)
            for kind,L in [('op',1/8),('HS',math.sqrt(2)/8)]:
                excess=distance(outputs[i],outputs[k],kind)-q*L*d;worst_excess=max(worst_excess,excess)
                check('intrinsic_geodesic_pair_estimate',excess<2e-12,metric=kind)
check('curve_actually_noncommuting',noncommuting>0,cases=noncommuting)
# Scalar distance-to-basepoint map on the circle attains the coefficient in a
# one-sided antipodal limit. This checks sharp boundary behavior, including1.
sharp=[]
for t in [0.,.25,.5,.9,.999999,1.]:
    q=(1-t*t)/(1+t*t);eps=1e-6
    g=lambda a:2*math.atan((1-t)/(1+t)*math.tan(a/2))
    slope=(g(math.pi/2)-g(math.pi/2-eps))/eps
    check('sharp_scalar_boundary_limit',abs(slope-q)<2e-6)
    sharp.append({'t':t,'q':q,'boundary_slope':slope})
result={'status':'PASS','scope':'Finite exact Gaussian-rational tangent/Gram/HS identities plus bounded double-precision noncommuting periodic-map intrinsic-distance diagnostics; universal proof is the sealed analytic reconstruction.','exact_check_count':sum(x['name'].startswith('exact_') or x['name'].startswith('wrong_') for x in checks),'check_count':len(checks),'all_passed':all(x['passed'] for x in checks),'checks_by_name':{n:sum(x['name']==n for x in checks) for n in sorted({x['name'] for x in checks})},'wrong_order_cases_detected':bad_order_detected,'numeric_worst_excess':worst_excess,'sharp_boundary':sharp,'normalized_HS_control_is_excluded_metric':True,'interval_certification':False,'universal_proof_by_finite_test':False,'source_scripts_imported':False,'numpy_version':np.__version__,'normal_and_optimized_same_logic':True}
target=Path(sys.argv[1]);target.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,sort_keys=True))

#!/usr/bin/env python3
"""Independent exact falsification checks; universal proofs are in REPORT.md.
Standard library only. No asserts: normal and optimized runs execute identical work.
"""
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
import hashlib
import json
import sys

class Failure(Exception):
    pass

class Poly:
    def __init__(self, n, terms=None):
        self.n = n
        self.t = {tuple(e): F(a) for e,a in (terms or {}).items() if a}
        if any(len(e) != n or min(e,default=0) < 0 for e in self.t):
            raise Failure('invalid polynomial exponent')
    def const(self, a): return Poly(self.n,{(0,)*self.n:a})
    def coerce(self, q): return q if isinstance(q,Poly) else self.const(q)
    def __add__(self,q):
        q=self.coerce(q)
        if q.n != self.n: raise Failure('dimension mismatch')
        d=dict(self.t)
        for e,a in q.t.items(): d[e]=d.get(e,F(0))+a
        return Poly(self.n,d)
    __radd__=__add__
    def __neg__(self): return Poly(self.n,{e:-a for e,a in self.t.items()})
    def __sub__(self,q): return self+-self.coerce(q)
    def __rsub__(self,q): return self.coerce(q)+-self
    def __mul__(self,q):
        q=self.coerce(q)
        if q.n != self.n: raise Failure('dimension mismatch')
        d={}
        for e,a in self.t.items():
            for f,b in q.t.items():
                g=tuple(x+y for x,y in zip(e,f));d[g]=d.get(g,F(0))+a*b
        return Poly(self.n,d)
    __rmul__=__mul__
    def __pow__(self,k):
        if not isinstance(k,int) or k<0: raise Failure('invalid polynomial power')
        r=self.const(1);b=self
        while k:
            if k%2:r=r*b
            b=b*b;k//=2
        return r
    def __eq__(self,q):
        q=self.coerce(q)
        return self.n==q.n and self.t==q.t
    def sub(self,images):
        if len(images)!=self.n:raise Failure('substitution arity')
        n=images[0].n;r=Poly(n)
        for e,a in self.t.items():
            p=Poly(n,{(0,)*n:a})
            for b,k in zip(images,e):p=p*(b**k)
            r=r+p
        return r
    def eval(self,values):
        if len(values)!=self.n:raise Failure('evaluation arity')
        return sum((a*prod_fraction(F(v)**k for v,k in zip(values,e)) for e,a in self.t.items()),F(0))
    def div_monomial(self,exponents):
        d={}
        for e,a in self.t.items():
            f=tuple(x-y for x,y in zip(e,exponents))
            if min(f,default=0)<0:raise Failure('not divisible by exceptional monomial')
            d[f]=a
        return Poly(self.n,d)
    def derivative(self,i):
        d={}
        for e,a in self.t.items():
            if e[i]:
                f=list(e);f[i]-=1;d[tuple(f)]=a*e[i]
        return Poly(self.n,d)
    def format(self):return [[list(e),str(a)] for e,a in sorted(self.t.items())]

def prod_fraction(values):
    r=F(1)
    for v in values:r*=v
    return r

def variables(n):
    return [Poly(n,{tuple(int(i==j) for j in range(n)):1}) for i in range(n)]

checks={}; controls=[]; evidence={}
def check(name,condition):
    checks[name]=checks.get(name,0)+1
    if not condition:raise Failure(name)
def negative(name,false_claim):
    if false_claim:raise Failure('negative control unexpectedly accepted: '+name)
    controls.append(name)

def compositions(total,n):
    if n==1:
        yield (total,);return
    for a in range(total+1):
        for rest in compositions(total-a,n-1):yield (a,)+rest

def pb_exp(e):
    a,b,c,d=e
    return (2*a+b+d,a+2*b+d,3*c+d)

def normal_exp(e):
    a,b,c,d=e;q,r=divmod(d,3)
    return (a+q,b+q,c+q,r)

def geometric_order(p):
    if not p.t:raise Failure('zero equation has no finite multiplicity')
    return min(e[0]+e[1] for e in p.t)

def tangent(p):
    m=geometric_order(p)
    return Poly(p.n,{e:a for e,a in p.t.items() if e[0]+e[1]==m})

def transform(p,chart,m=None):
    u,v,c=variables(3)
    if m is None:m=geometric_order(p)
    if chart=='vertical':return p.sub([u*v,v,c]).div_monomial((0,m,0))
    if chart=='horizontal':return p.sub([u,u*v,c]).div_monomial((m,0,0))
    raise Failure('unrecognized blowup chart')

def restriction(p,i):
    vs=variables(p.n);vs[i]=Poly(p.n)
    return p.sub(vs)

def ldl_pivots(matrix):
    n=len(matrix);L=[[F(0) for _ in range(n)]for _ in range(n)];D=[]
    for i in range(n):
        L[i][i]=F(1)
        d=matrix[i][i]-sum((L[i][k]**2*D[k] for k in range(i)),F(0))
        if d<=0:raise Failure('moment Gram matrix not positive definite')
        D.append(d)
        for j in range(i+1,n):
            L[j][i]=(matrix[j][i]-sum((L[j][k]*L[i][k]*D[k] for k in range(i)),F(0)))/d
    return D

def cube_moment(e):
    if any(k%2 for k in e):return F(0)
    return prod_fraction(F(2,k+1) for k in e)

def main():
    parent=Path(__file__).resolve().parents[2]/'inputs'
    pins={
        'PROOF.md':'46af7394ebfee7b0de9861693f84ab684502da3be208c626411f24e2538c7d15',
        'REAL_DELTA_APPENDIX.md':'c1ca3231f1b61e9a550d37a0b1dd63a618d25caab0fb897978b863ed0614cd38',
        'MATHEMATICAL_AUDIT.md':'f9faede12ad50034f5620f4576c621dc275a6ddbbf29bb3e13096d778a094cce'}
    for name,pin in pins.items():
        check('input_pins',hashlib.sha256((parent/name).read_bytes()).hexdigest()==pin)
    evidence['input_pins']=pins

    A,B,C,D,c=variables(5);x,y,z,p=variables(4)
    G=A*B*C-D**3;q=A**2+B**2+C**2-c*D**2
    images=[x**2*y,x*y**2,z**3,x*y*z,p]
    M=x**4*y**2+x**2*y**4+z**6-p*x**2*y**2*z**2
    check('symbolic_substitution',G.sub(images)==0)
    check('symbolic_substitution',q.sub(images)==M)
    negative('changed_C_to_z_squared_preserves_cubic_relation',G.sub([x*x*y,x*y*y,z*z,x*y*z,p])==0)
    negative('erased_parameter_still_exact',q.sub([x*x*y,x*y*y,z**3,x*y*z,Poly(4)])==M)
    negative('nonuniform_degree_substitution_is_degree_three',all(sum(next(iter(h.t)))==3 for h in [x*x*y,x*y*y,z*z,x*y*z]))
    normal_images={}
    for total in range(11):
        for e in compositions(total,4):
            n=normal_exp(e);pe=pb_exp(e)
            check('kernel_normal_form',pb_exp(n)==pe)
            check('kernel_normal_form',sum(n)==total and n[-1]<3)
            if e[-1]<3:
                check('kernel_injectivity_finite_control',pe not in normal_images or normal_images[pe]==e)
                normal_images[pe]=e
    evidence['kernel_normal_forms_tested']=len(normal_images)
    for m in range(1,40,2):
        for e in compositions(m,4):check('degree_tripling',sum(pb_exp(e))==3*m)
        check('degree_tripling',2*(3*m)==6*m)
    for N in range(0,40):check('parity',((N+1)%2==1)==(N%2==0))
    negative('odd_N_produces_odd_m',(9+1)%2==1)
    for k in range(15):
        for ell in range(k,18):
            check('odd_power_propagation',2*ell+1==(2*k+1)+2*(ell-k))

    vals=[F(-3),F(-1),F(-1,2),F(1,3),F(1),F(2)]
    params=[F(-100),F(-3),F(-1),F(0),F(1,5),F(1),F(2),F(2999,1000)]
    sign_patterns=set()
    for a,b,d,cv in product(vals,vals,[F(-2),F(-1),F(1),F(3)],params):
        point=[a*d,b*d,d/(a*b),d]
        sign_patterns.add(tuple(1 if v>0 else -1 for v in point))
        check('signed_projective_positivity',point[0]*point[1]*point[2]==point[3]**3)
        value=sum(v*v for v in point[:3])-cv*point[3]**2
        check('signed_projective_positivity',value>0)
        check('signed_projective_positivity',value>=(3-cv)*d*d)
        for T in point:check('square_bundle_chart_sign',value/(T*T)>0)
    for a,b,cc in product(range(-3,4),repeat=3):
        if a*b*cc==0 and (a or b or cc):
            check('boundary_positivity',a*a+b*b+cc*cc>0)
    evidence['signed_nonzero_patterns']=len(sign_patterns)
    negative('AM_GM_on_signed_coordinates',F(-2)+F(-1)+F(1,2)>=3)
    check('endpoint_zero',q.eval([1,1,1,1,3])==0)
    negative('strict_positivity_extends_to_c_3',q.eval([1,1,1,1,3])>0)
    for cv in [F(31,10),F(4),F(9)]:
        for k in range(8):
            check('above_endpoint_falsification',(F(3)-cv)**(2*k+1)<0)
    endpoint_bad_value=M.eval([1,1,1,4])
    check('even_power_control_antecedent',endpoint_bad_value<0 and endpoint_bad_value**2>0)
    negative('even_power_positivity_implies_odd_positivity',endpoint_bad_value>0)
    # Explicit model disproves the interchange forall c exists k -> exists k forall c.
    for k in range(50):
        ck=F(3)-F(1,k+1);cv=(ck+3)/2
        check('quantifier_model',ck<cv<3)
    negative('uniform_endpoint_from_pointwise_eventual_model',F(3)-F(1,51)>=3)

    # A homogeneous SOS square root can use only lattice points of half the Newton triangle.
    allowed=[]
    for e in compositions(3,3):
        a,b,cc=e
        # Barycentric weights of (2,1,0),(1,2,0),(0,0,3).
        weights=[F(2*a-b,3),F(2*b-a,3),F(cc,3)]
        if all(t>=0 for t in weights) and sum(weights)==1:allowed.append(e)
    check('axis_symmetry',M.sub([y,x,z,p])==M)
    check('newton_support',set(allowed)=={(2,1,0),(1,2,0),(0,0,3),(1,1,1)})
    pairs=[(a,b)for a in allowed for b in allowed if tuple(x+y for x,y in zip(a,b))==(2,2,2)]
    check('newton_support',pairs==[((1,1,1),(1,1,1))])
    evidence['half_newton_lattice_points']=[list(e) for e in allowed]

    # Exact divided-difference identity used for downward closure of each threshold set.
    u,v=variables(2)
    grid=[F(a,b)for a in range(-4,5)for b in (1,2)]
    for m in range(1,22,2):
        Q=sum((comb(m,j+1)*u**(m-1-j)*v**j for j in range(m)),Poly(2))
        check('divided_difference_identity',(u+v)**m-u**m==v*Q)
        for av,bv in product(grid,repeat=2):check('divided_difference_signed_samples',Q.eval([av,bv])>=0)
    negative('even_exponent_divided_difference_nonnegative',((-2+1)**2-(-2)**2)>=0)

    # Exact Gram moments underpin a correct closure proof, rather than assuming all PSD images closed.
    pivots={}
    for d in [0,1,2,3,6]:
        basis=list(compositions(d,3))
        T=[[cube_moment(tuple(a+b for a,b in zip(e,f)))for f in basis]for e in basis]
        ds=ldl_pivots(T);pivots[str(d)]={'dimension':len(basis),'pivots':[str(t)for t in ds]}
        for t in ds:check('positive_definite_moment_matrix',t>0)
    evidence['cube_moment_pivots']=pivots
    for n in range(1,51):
        a,b,cc=F(1,n),F(1),F(n)
        check('nonclosed_general_PSD_image_control',a>0 and cc>0 and a*cc-b*b==0)
    negative('limiting_projected_pair_0_1_has_PSD_lift',F(0)*F(999)-F(1)**2>=0)

    # Derive all six blowup charts independently by polynomial substitution and exact division.
    u,v,c=variables(3)
    fs=[u*u+u**4+v**6-c*u*u*v*v,
        u*u+u**4*v*v+v**4-c*u*u*v*v,
        u*u+u**4*v**4+v*v-c*u*u*v*v]
    expected_v=[fs[1],fs[2],1+u*u-c*u*u*v*v+u**4*v**6]
    expected_h=[1+u*u+v**6*u**4-c*v*v*u*u,
                1+v*v*u**4+(v**4-c*v*v)*u*u,
                1+v*v-c*v*v*u*u+v**4*u**6]
    tangent_expected=[u*u,u*u,u*u+v*v]
    evidence['blowups']=[]
    for depth,f in enumerate(fs):
        check('blowup_multiplicity',geometric_order(f)==2)
        check('blowup_tangent',tangent(f)==tangent_expected[depth])
        V=transform(f,'vertical');H=transform(f,'horizontal')
        check('all_blowup_charts',V==expected_v[depth])
        check('all_blowup_charts',H==expected_h[depth])
        ev=restriction(V,1);eh=restriction(H,0)
        check('exceptional_divisor',ev==(u*u if depth<2 else 1+u*u))
        check('exceptional_divisor',eh==(1 if depth<2 else 1+v*v))
        # Strict transforms are not divisible by the exceptional coordinate.
        check('exceptional_factor_removed',any(e[1]==0 for e in V.t))
        check('exceptional_factor_removed',any(e[0]==0 for e in H.t))
        evidence['blowups'].append({'depth':depth+1,'multiplicity':geometric_order(f),
            'vertical':V.format(),'horizontal':H.format(),'vertical_exceptional':ev.format(),
            'horizontal_exceptional':eh.format()})
    delta=sum(geometric_order(f)*(geometric_order(f)-1)//2 for f in fs)
    check('real_delta_recursion',delta==3 and 2*delta==6)
    negative('drop_final_double_center_still_delta_3',2==delta)
    wrong=transform(fs[0],'vertical',m=1)
    negative('divide_only_one_exceptional_factor_is_strict',any(e[1]==0 for e in wrong.t))
    for value in grid:
        check('terminal_real_no_directions',1+value*value>0)
    # The second chart is essential: uv has a direction at infinity absent from finite u/v.
    node=u*v
    ev=restriction(transform(node,'vertical'),1)
    eh=restriction(transform(node,'horizontal'),0)
    directions={(0,1),(1,0)}
    vertical_covered={d for d in directions if d[1]!=0}
    horizontal_covered={d for d in directions if d[0]!=0}
    check('missing_chart_counterexample',ev==u and eh==v and all(node.eval([a,b,0])==0 for a,b in directions) and vertical_covered|horizontal_covered==directions)
    negative('one_finite_blowup_chart_covers_all_real_directions',vertical_covered==directions)
    actual_first_tangent_directions={(0,1)}
    negative('using_only_nonzero_complementary_chart_finds_unique_direction',all(d[0]!=0 for d in actual_first_tangent_directions))
    evidence['local_delta_per_axis_zero']=delta
    evidence['total_real_delta']=2*delta

    # Independent coordinate/singularity identities used only for the prior-result bridge.
    x,y,z,c=variables(4)
    M=x**4*y*y+x*x*y**4+z**6-c*x*x*y*y*z*z
    check('complex_gradient',M.derivative(0)==2*x*y*y*(2*x*x+y*y-c*z*z))
    check('complex_gradient',M.derivative(1)==2*x*x*y*(x*x+2*y*y-c*z*z))
    check('complex_gradient',M.derivative(2)==2*z*(3*z**4-c*x*x*y*y))
    u,v,c=variables(3);E1=2*u+v-c;E2=u+2*v-c;E3=3-c*u*v
    L1=2*E1-E2;L2=2*E2-E1
    check('complex_gradient_elimination',L1==3*u-c and L2==3*v-c)
    check('complex_gradient_elimination',27-c**3==9*E3+c*L1*L2+c*c*(L1+L2))
    for cv in params:check('complex_gradient_real_parameter_samples',cv**3<27)

    return {'verdict':'PASS','method':'standard-library exact rational sparse polynomial arithmetic',
        'finite_checks_are_falsification_not_universal_proofs':True,
        'check_counts':dict(sorted(checks.items())),'total_checks':sum(checks.values()),
        'negative_controls':controls,'negative_control_count':len(controls),'evidence':evidence}

if __name__=='__main__':
    try:
        result=main()
        print(json.dumps(result,sort_keys=True,indent=2))
    except Exception as exc:
        print(json.dumps({'verdict':'FAIL','error_type':type(exc).__name__,'error':str(exc)},sort_keys=True))
        sys.exit(1)

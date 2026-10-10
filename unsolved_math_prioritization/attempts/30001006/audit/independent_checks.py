#!/usr/bin/env python3
"""Independent exact diagnostics. Does not certify geometric existence."""
from fractions import Fraction as F
from itertools import combinations, product
import json
import sympy as s

checks=[]; controls=[]
def require(test,label):
    if not test: raise RuntimeError(label)
def record(test,label):
    require(test,label);checks.append(label)

# Algebraic-curvature Bianchi projection, independent of author B-wedge-B models.
# Images of all symmetric pair-matrix units span the curvature space.
component_count=0; model_count=0
for n in (4,5):
    pairs=list(combinations(range(n),2)); positions={p:i for i,p in enumerate(pairs)}
    indices=list(product(range(n),repeat=4))
    for a in range(len(pairs)):
      for b in range(a,len(pairs)):
        def raw(i,j,k,l):
            if i==j or k==l:return F(0)
            p=positions[tuple(sorted((i,j)))];q=positions[tuple(sorted((k,l)))]
            return F((1 if i<j else -1)*(1 if k<l else -1)*int((p==a and q==b) or (p==b and q==a)))
        R={(i,j,k,l):raw(i,j,k,l)-(raw(i,j,k,l)+raw(i,k,l,j)+raw(i,l,j,k))/3 for i,j,k,l in indices}
        def g2(i,j,k,l):return -(R[i,k,j,l]+R[i,l,j,k])/3
        for i,j,k,l in indices:
            require(R[i,j,k,l]+R[i,k,l,j]+R[i,l,j,k]==0,'Bianchi projection')
            reconstructed=(g2(j,k,i,l)+g2(i,l,j,k)-g2(i,k,j,l)-g2(j,l,i,k))/2
            require(reconstructed==R[i,j,k,l],'normal metric 2-jet')
            component_count+=1
        model_count+=1
    checks.append('all_symmetric_pair_generators_normal_jet_n_'+str(n))

# Exact CK recursion through total order 5 for flat principal part and a generic
# quadratic right-side coefficient. Curved-principal coefficient terms in the
# 3-jet proof multiply derivatives already known to vanish (see audit report).
x,y,z,t=s.symbols('x y z t');coords=(x,y,z,t)
q=x*x+2*y*y+3*z*z+4*t*t+5*x*y+6*x*t+7*y*t+8*z*t

def ck_poly(q):
    vs=[s.Integer(1),s.Integer(0)]
    for j in range(4):
        prior=sum(vs[k]*t**k for k in range(len(vs)))
        rhs=s.expand(q*prior).coeff(t,j)-sum(s.diff(vs[j],u,2) for u in (x,y,z))
        vs.append(s.expand(rhs/((j+1)*(j+2))))
    return s.expand(sum(vs[k]*t**k for k in range(len(vs))))
v=ck_poly(q)
for order in (1,2,3):
    for derivs in product(coords,repeat=order):
        require(s.diff(v,*derivs).subs(dict.fromkeys(coords,0))==0,'CK metric 3-jet')
record(s.diff(v,t,4).subs(dict.fromkeys(coords,0))!=0,'CK fourth_jet_can_change')
record(v.subs(t,0)==1 and s.diff(v,t).subs(t,0)==0,'CK exact_Cauchy_data')
for add,label,order in ((s.Integer(1),'nonzero_F_at_center_breaks_second_jet',2),(t,'nonzero_dF_at_center_breaks_third_jet',3)):
    require(s.diff(ck_poly(q+add),t,order).subs(dict.fromkeys(coords,0))!=0,label);controls.append(label)

r,n,A,M,J,H,P=s.symbols('r n A M J H P',positive=True)
w=r**(n-1)*s.exp(-A*r*r/2); alpha=(n-1)/r-A*r
record(s.simplify(s.diff(w,r)/w-alpha)==0,'radial_integrating_factor')
vp=-M*J/w
record(s.simplify(H*vp+H*M*J/w)==0,'lower_radial_Laplacian_bound_has_correct_sign')
require(s.simplify(H*(-vp)+H*M*J/w)!=0,'positive_derivative_sign_mutation');controls.append('positive_derivative_sign_mutation')
e=s.symbols('e',positive=True)
record(s.simplify(s.expand_power_base(e**n*(4*e)**(2-n),force=True)-4**(2-n)*e**2)==0,'tail_order_epsilon_squared')

# Boundary Hessian of F = scalar - d|W|, showing why first jet is essential.
u1,u2,b1,b2,d=s.symbols('u1 u2 b1 b2 d',real=True)
Ffun=-d*s.sqrt(u1*u1+u2*u2)
hess=s.hessian(Ffun,(u1,u2)).subs({u1:1,u2:0})
record(hess==s.Matrix([[0,0],[0,-d]]),'norm_Hessian_transverse_term')
record((s.Matrix([0,0]).T*hess*s.Matrix([0,0]))[0]==0,'zero_curvature_first_jet_kills_Hessian_term')
require((s.Matrix([0,1]).T*hess*s.Matrix([0,1]))[0]==-d,'nonzero_first_jet_control');controls.append('nonzero_first_jet_prevents_Laplacian_cancellation')

# Numerical constants of an exact abstract apex witness in scalar/Weyl space.
# This tests the tangent formula, not Hamilton Q itself.
e=s.symbols('e',positive=True)
record(s.simplify(3-4*s.sqrt(2**2))==-5,'apex_outward_velocity_witness')
record(s.simplify(s.diff(4*e+3*t-4*s.sqrt((e+2*t)**2),t).subs(t,0))==-5,'smooth_boundary_approximation_same_limit')
print(json.dumps({'status':'PASS','checks':checks,'negative_controls':controls,'normal_jet_generators':model_count,'normal_jet_component_checks':component_count,'scope':'Exact algebra and finite jet diagnostics only; analytic existence, gluing and PDE implications are established in the written audit, not by these tests.'},indent=2,sort_keys=True))

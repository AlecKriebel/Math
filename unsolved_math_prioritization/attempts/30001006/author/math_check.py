#!/usr/bin/env python3
"""Exact identities supporting, not proving, the geometric existence argument."""
import json
import sympy as s

checks = []
negatives = []

def require(ok, label):
    if not bool(ok):
        raise RuntimeError(label)

def zero(expr, label):
    require(s.simplify(expr) == 0, label)
    checks.append(label)

def reject(expr, label):
    require(s.simplify(expr) != 0, label)
    negatives.append(label)

n, d, a, c, mu, beta = s.symbols('n d a c mu beta', positive=True)
N = n * (n - 1) / 2
c_of_d = 2 * n * (n - 1) / d**2
zero(c_of_d * N * a**2 - (n*(n-1)*a/d)**2, 'closed_cone_parameter_conversion')
zero(c_of_d.subs(d**2, 2*(n-2)*(n-1)) - n/(n-2), 'central_parameter_conversion')
reject(n*(n-1)/d**2*N*a**2 - (n*(n-1)*a/d)**2, 'missing_factor_two_detected')
L = 4*N*mu**2/(n-2)**2
U = (n-1)**2/(N*beta**2)
zero(2*n*(n-1)/U - n**2*beta**2, 'lower_d_squared_endpoint')
zero(2*n*(n-1)/L - (n-2)**2/mu**2, 'upper_d_squared_endpoint')

v, lapv, gradv2 = s.symbols('v lapv gradv2', positive=True)
k = 2/(n-2)
an = 4*(n-1)/(n-2)
conformal_correction = -2*(n-1)*k*(lapv/v-gradv2/v**2)-(n-1)*(n-2)*k**2*gradv2/v**2
zero(conformal_correction + an*lapv/v, 'conformal_gradient_terms_cancel')
zero((n+2)/(n-2)-1-4/(n-2), 'weyl_conformal_weight')
wrong = -2*(n-1)*k*(lapv/v-gradv2/v**2)-(n-1)*(n-1)*k**2*gradv2/v**2
reject(wrong+an*lapv/v, 'wrong_conformal_coefficient_detected')

r, A, M = s.symbols('r A M', positive=True)
w = r**(n-1)*s.exp(-A*r*r/2)
alpha = (n-1)/r-A*r
zero(s.diff(w,r)/w-alpha, 'radial_integrating_factor')
J=s.Function('J')(r)
phi=s.symbols('phi')
z=-M*J/w
zero((s.diff(z,r)+alpha*z).subs(s.diff(J,r),w*phi)+M*phi, 'radial_barrier_ode')
H=s.symbols('H', positive=True)
# Actual Delta r = alpha + H; z <= 0. Difference must be negative.
zero((alpha+H)*z-alpha*z+M*J*H/w, 'laplacian_comparison_sign_identity')
reject((alpha-H)*z-alpha*z+M*J*H/w, 'reversed_laplacian_bound_detected')

# Exact all-n antiderivative, with n != 2 understood in the proof.
zero(s.diff(r**(2-n)/(2-n),r)-r**(1-n), 'radial_tail_antiderivative')
eps=s.symbols('eps', positive=True)
zero(s.powsimp(s.expand_power_base(eps**n*(4*eps)**(2-n), force=True))-4**(2-n)*eps**2, 'radial_tail_epsilon_squared')
zero(n**2*beta**2-2*n*(n-1)/U, 'ode_pde_endpoint_bridge')
zero((n**2*beta**2).subs({n:12,beta**2:s.Rational(55,36)})-220, 'dimension_twelve_target_unchanged')

# Verify the normal-coordinate second-jet reconstruction on three exact
# algebraic curvature models, including genuinely non-diagonal ones.
D=4
models=[s.eye(D), s.Matrix([[2,1,0,0],[1,-1,2,0],[0,2,3,1],[0,0,1,-2]]),
        s.Matrix([[0,1,2,3],[1,1,-1,0],[2,-1,2,1],[3,0,1,4]])]
for idx,B in enumerate(models):
    def R(i,j,k,l):
        return B[i,k]*B[j,l]-B[i,l]*B[j,k]
    def g2(i,j,k,l):
        return -(R(i,k,j,l)+R(i,l,j,k))/3
    for i in range(D):
        for j in range(D):
            for k0 in range(D):
                for l in range(D):
                    recovered=(g2(j,k0,i,l)+g2(i,l,j,k0)-g2(i,k0,j,l)-g2(j,l,i,k0))/2
                    require(s.simplify(recovered-R(i,j,k0,l))==0, 'normal_jet_component')
    checks.append('normal_metric_jet_model_'+str(idx+1))

require(len(checks)==16, 'named_check_count_changed')
require(len(negatives)==3, 'negative_control_count_changed')
print(json.dumps({'status':'PASS','named_exact_checks':checks,'named_exact_check_count':len(checks),
                  'negative_controls':negatives,'normal_jet_component_checks':768,
                  'scope':'Identities and finite model diagnostics only; no computation certifies analytic existence, compact gluing, or the missing universal Weyl bound.'},indent=2,sort_keys=True))

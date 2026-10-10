#!/usr/bin/env python3
"""Read-only exact algebra checks. This is not a proof of the full PDE target."""
import argparse
import json
import sys
import sympy as s


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inject-failure', action='store_true')
    args = parser.parse_args()
    checks = []

    def eq(name, left, right):
        residual = s.simplify(left - right)
        require(residual == 0, name + ': nonzero exact residual ' + str(residual))
        checks.append({'name': name, 'result': 'pass', 'arithmetic': 'exact_symbolic'})

    n = s.symbols('n', integer=True, positive=True)
    k = s.symbols('k', integer=True, positive=True)
    r = s.symbols('r', positive=True)
    t = s.symbols('t', real=True)
    eq('annulus_average_constant', (2**n-1)/(1-2**(-n)), 2**n)
    eq('thickness_radius_factor', (s.Rational(1,4))**(n-2)/(s.Rational(1,4))**n, 16)
    rk, rho, ak = 2**(-k), 2**(-3*k-4), 2**(-k)
    eq('spike_height_scaling', rk**2*ak/rho**2, 2**(3*k+8))
    eq('spike_relative_radius', rho/rk, 2**(-2*k-4))
    eq('adjacent_support_ratio', (rho+2**(-3*(k+1)-4))/(rk-2**(-k-1)), 9*2**(-2*k-6))
    require(s.Rational(9,256) < 1, 'adjacent support inequality failed')
    checks.append({'name':'adjacent_support_inequality_k_ge_1','result':'pass','arithmetic':'exact_rational_plus_monotonicity'})
    eq('curvature_ratio_exponent', 2**(k*k-k+4)*2**k/2**(2*k+2), 2**(k*k-2*k+2))
    f = s.exp(t)*(1+s.Rational(2,5)*s.sin(t))
    eq('oscillatory_f_first_derivative', s.diff(f,t), s.exp(t)*(1+s.Rational(2,5)*(s.sin(t)+s.cos(t))))
    eq('oscillatory_f_second_derivative', s.diff(f,t,2), s.exp(t)*(1+s.Rational(4,5)*s.cos(t)))
    eq('oscillatory_f_third_derivative', s.diff(f,t,3), s.exp(t)*(1+s.Rational(4,5)*(s.cos(t)-s.sin(t))))
    eq('negative_third_derivative_value', (s.diff(f,t,3)/s.exp(t)).subs(t,3*s.pi/4), 1-s.Rational(4,5)*s.sqrt(2))
    require(s.Rational(4,25)*2<1 and s.Rational(16,25)*2>1, 'exact derivative-sign comparisons failed')
    checks.append({'name':'oscillatory_derivative_signs','result':'pass','arithmetic':'exact_rational_squared_comparisons'})
    w = -s.log(1+r*r)
    G = 2*(n-2)*s.exp(t)+4*s.exp(2*t)
    laplacian = s.diff(w,r,2)+(n-1)*s.diff(w,r)/r
    eq('entire_solution_PDE', -laplacian, G.subs(t,w))
    V = s.diff(G,t).subs(t,w)
    eq('entire_stability_potential', V, 2*(n-2)/(1+r*r)+8/(1+r*r)**2)
    eq('entire_potential_Hardy_comparison', 2*(n-2)-r*r*V, (2*(n-2)+2*(n-6)*r*r)/(1+r*r)**2)
    H = (n-2)**2/4
    eq('Hardy_dimension_threshold', H-2*(n-2), (n-2)*(n-10)/4)
    a = n/(n+2)
    g = G.subs(t,a*t)/(2*n)
    eq('normalized_g_value', g.subs(t,0), 1)
    eq('normalized_g_derivative', s.diff(g,t).subs(t,0), 1)
    v = -s.log(1+r*r/(2*n+4))/a
    eq('normalized_entire_PDE', -(s.diff(v,r,2)+(n-1)*s.diff(v,r)/r), g.subs(t,v))
    ut, utt, wt, wtt = s.symbols('ut utt wt wtt')
    ur, urr = -ut/r, (utt+ut)/r**2
    eq('cylindrical_radial_operator', (-r*r*(urr+(n-1)*ur/r)).subs({ut:2+wt,utt:wtt}), -wtt+(n-2)*wt+2*(n-2))
    beta = (n-2)/2
    z, zt = s.symbols('z zt')
    eq('cylinder_measure_exponent', n-1-2*beta-2, -1)
    eq('cylinder_energy_cross_term', (zt+beta*z)**2-zt**2-H*z*z, 2*beta*z*zt)
    # The general chain rule uses independent jets; it is not a numerical PDE test.
    F, Fpp, Fppp, grad2 = s.symbols('F Fpp Fppp grad2')
    eq('potential_chain_rule_jets', -(-Fpp*F+Fppp*grad2), Fpp*F-Fppp*grad2)
    if args.inject_failure:
        require(False, 'intentional explicit failure: optimization must not disable checks')
    print(json.dumps({'status':'pass','checks':checks,'count':len(checks),
        'numerical_evidence':False,'full_target_proved':False,
        'scope':'Exact identities and finite arithmetic checks only. Analytic arguments require mathematical review.'},indent=2))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(json.dumps({'status':'fail','error':str(exc)}), file=sys.stderr)
        sys.exit(1)

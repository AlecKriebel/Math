"""Reproducible checks of this audit's theorem dictionaries, not a proof by samples.

Requires mpmath. No network, repository state, or submitted verification imports.
"""
import json
from math import gcd
from pathlib import Path
import mpmath as mp

mp.mp.dps = 80


def check_case(k_string, n, tau):
    k = mp.mpf(k_string)
    param = k*k
    kp = mp.sqrt(1-param)
    K = mp.ellipk(param)
    Kp = mp.ellipk(1-param)
    nome = mp.exp(-mp.pi*Kp/K)
    sn = lambda u: mp.ellipfun('sn', u, param)
    cn = lambda u: mp.ellipfun('cn', u, param)
    dn = lambda u: mp.ellipfun('dn', u, param)
    theta = lambda u: mp.jtheta(4, mp.pi*u/(2*K), nome)
    alpha = mp.mpf(2)
    beta = alpha*kp
    c = alpha*k
    v = 2*K*tau/n
    delta = 2*v
    a = alpha*dn(v)/cn(v)
    b = beta/cn(v)
    A = a*a/alpha
    B = b*b/beta
    lam = a*a-alpha*alpha
    t = sn(v)**2
    Cv = alpha**4*(1-param*t*t)**2/(1-t)**4
    half = n//2
    w = K-delta
    max_factor_residual = mp.mpf(0)
    max_theta_residual = mp.mpf(0)
    products = []
    focus_products = []
    for phase in [mp.mpf('0.071'), mp.mpf('0.233'), mp.mpf('0.571')]:
        initial = phase*K
        pplus = pminus = mp.mpf(1)
        for j in range(n):
            x0, y0 = -a*sn(initial+j*delta), b*cn(initial+j*delta)
            x1, y1 = -a*sn(initial+(j+1)*delta), b*cn(initial+(j+1)*delta)
            # Solve the actual two tangent equations x*xj/a² + y*yj/b² = 1.
            n0x, n0y, n1x, n1y = x0/a**2, y0/b**2, x1/a**2, y1/b**2
            determinant = n0x*n1y-n0y*n1x
            qx = (n1y-n0y)/determinant
            qy = (n0x-n1x)/determinant
            u = initial+v+j*delta
            dp2, dm2 = (qx-c)**2+qy*qy, (qx+c)**2+qy*qy
            H = Cv*dn(u)**2*(dn(delta)**2-param*cn(delta)**2*sn(u)**2)
            max_factor_residual = max(max_factor_residual, abs(dp2*dm2/H-1))
            theta_rhs = theta(u+w)*theta(u-w)*theta(0)**2/(theta(u)**2*theta(w)**2)
            theta_lhs = 1-param*sn(u)**2*sn(w)**2
            max_theta_residual = max(max_theta_residual, abs(theta_lhs/theta_rhs-1))
            pplus *= mp.sqrt(dp2)
            pminus *= mp.sqrt(dm2)
        products.append(pplus)
        focus_products.append(pminus)
    data = {
        'k': k_string, 'N': n, 'tau': tau,
        'factor_relative_residual': str(max_factor_residual),
        'theta_relative_residual': str(max_theta_residual),
        'phase_product_relative_spread': str(max(products)/min(products)-1),
        'focus_relative_difference': str(max(abs(x/y-1) for x,y in zip(products,focus_products))),
        'Q_squared_axis_difference_residual': str(abs(A*A-B*B-c*c*(1-lam*lam/(alpha*alpha*beta*beta)))),
        'Q_major_axis': 'x' if A > B else 'y',
    }
    assert max_factor_residual < mp.mpf('1e-65')
    assert max_theta_residual < mp.mpf('1e-65')
    assert mp.mpf(data['Q_squared_axis_difference_residual']) < mp.mpf('1e-60')
    if n % 4 == 0:
        norm_prediction = Cv**half*kp**half*dn(delta)**(2*half)*(theta(0)/theta(w))**(2*half)
        data['theta_constant_relative_residual'] = str(max(abs(x*x/norm_prediction-1) for x in products))
        assert mp.mpf(data['theta_constant_relative_residual']) < mp.mpf('1e-60')
        assert mp.mpf(data['phase_product_relative_spread']) < mp.mpf('1e-60')
        assert mp.mpf(data['focus_relative_difference']) < mp.mpf('1e-60')
    else:
        assert mp.mpf(data['phase_product_relative_spread']) > mp.mpf('1e-12')
    return data


cases = [check_case(k, n, tau)
         for k in ['0.35', '0.8', '0.97']
         for n in [4, 8, 12, 16, 20, 24]
         for tau in range(1, n//2) if gcd(n,tau) == 1]
negative_controls = [check_case('0.8', n, 1) for n in [6,10,14]]

# Exact counterexample to the literal point version of BT v2 Theorem 4.3(1).
# Caustic (alpha,beta)=(2,1), outer (a²,b²)=(6,3), orbit rectangle (±2,±1).
# Center feet R are (±2,0),(0,±1), c²=3:
# product |F-R| = |alpha²-c²|*(beta²+c²) = 4, whereas beta**4 = 1.
exact_counterbridge = {
    'alpha': 2, 'beta': 1, 'c_squared': 3,
    'outer_a_squared': 6, 'outer_b_squared': 3,
    'center_feet_focal_distance_product': 4,
    'literal_BT_rhs': 1,
    'focus_to_side_distance_product': 1,
    'target_Q_focal_product': 72,
}
assert exact_counterbridge['center_feet_focal_distance_product'] != exact_counterbridge['literal_BT_rhs']
out = {'mpmath_version': mp.__version__, 'precision_digits': mp.mp.dps, 'admissible_case_count': len(cases), 'cases': cases,
       'negative_controls': negative_controls, 'exact_counterbridge': exact_counterbridge,
       'conclusion': 'All sampled bridge identities passed; parity controls varied. Samples do not prove the theorem or historical priority.'}
Path(__file__).with_name('bridge_check_results.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps({'precision_digits': mp.mp.dps, 'admissible_case_count': len(cases),
                  'negative_control_count': len(negative_controls), 'all_checks_passed': True}))

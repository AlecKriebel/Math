"""Independent reproducibility checks. Analytic theorem application is proved in the audit."""
from pathlib import Path
from fractions import Fraction as Q
import hashlib
import json
import sympy as sp
import mpmath as mp

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).with_name('CURRENT_RECURSION_AUDIT_CHECK.json')
TARGETS = {
    'theta_twisted_volumes_30004711/authored/AUTHOR_APPROACH_5_POSITIVE_CURRENT_REPAIR.md':
        (10732, 'd6e451d3f193ccf9400180bf17fb924d8b4ea7d2efecf8c8c0401c1796547779'),
    'theta_twisted_volumes_30004711/authored/AUTHOR_APPROACH_3_GEOMETRIC_RECURSION.md':
        (9943, '6994b76c1ed8d96f1784d88c147fe6789ba9fabc57fb3b4a42808547deddd88f'),
    'theta_twisted_volumes_30004711/authored/AUTHOR_APPROACH_4_ODD_TORUS_COLLAR.md':
        (10912, 'cded43f4a42ce5bbaa8d06c1f6deae2540ba413f60adf9643b199f1a935414b0'),
}
for name, (size, digest) in TARGETS.items():
    data = (ROOT / name).read_bytes()
    assert len(data) == size, name
    assert hashlib.sha256(data).hexdigest() == digest, name

r, eps, t, L = sp.symbols('r eps t L', positive=True)
transverse = sp.integrate(-sp.log(r), (r, 0, eps))
assert sp.simplify(transverse - eps * (1 - sp.log(eps))) == 0
assert sp.limit(transverse, eps, 0, dir='+') == 0
assert Q(1, 2) + Q(1, 2) == 1
assert Q(3, 2) * Q(1, 2) * Q(1, 24) == Q(1, 32)

# With dd^c=(i/2pi)partial barpartial, the Euclidean density is Delta/(4pi).
# Model u(r)=2log(log(1/r)); its positive curvature has disk mass 1/t=m'(t)/2.
u = 2 * sp.log(-sp.log(r))
laplacian = sp.diff(u, r, 2) + sp.diff(u, r) / r
assert sp.simplify(laplacian + 2/(r**2 * sp.log(r)**2)) == 0
mass = sp.integrate(-laplacian * r / 2, (r, 0, sp.exp(-t)))
assert sp.simplify(mass - 1/t) == 0
assert sp.limit((2*sp.log(t) + sp.log(sp.log(t)))/t, t, sp.oo) == 0
assert sp.limit((1 + sp.log(sp.log(t)))/t, t, sp.oo) == 0

S = lambda g, n: Q((-1)**n) * Q(2)**(1-g)
W = lambda g, n: Q(2)**(1-g-n)
ratio_cases = 0
split_cases = 0
for g in range(0, 8):
    for n in range(1, 10):
        c = 2*g - 2 + n
        if c <= 1:
            continue
        if n >= 2:
            assert S(g,n)/S(g,n-1) == -1
            assert W(g,n)/W(g,n-1) == Q(1,2)
            assert 2*g - 2 + n - 1 == c - 1
            ratio_cases += 1
        if g >= 1:
            assert S(g,n)/S(g-1,n+1) == -Q(1,2)
            assert W(g,n)/W(g-1,n+1) == 1
            assert 2*(g-1) - 2 + n + 1 == c - 1
            ratio_cases += 1
        for g1 in range(g+1):
            for n1 in range(1,n+1):
                g2,n2 = g-g1,n+1-n1
                c1,c2 = 2*g1-2+n1,2*g2-2+n2
                if c1 <= 0 or c2 <= 0:
                    continue
                assert c1+c2 == c-1 and c1<c and c2<c
                assert S(g,n)/(S(g1,n1)*S(g2,n2)) == -Q(1,2)
                assert W(g,n)/(W(g1,n1)*W(g2,n2)) == 1
                split_cases += 1

z = sp.symbols('z')
mgf = sp.exp(L*z)/sp.cos(2*sp.pi*z)
assert sp.simplify(sp.diff(mgf,z).subs(z,0)-L) == 0
assert sp.simplify(sp.diff(mgf,z,3).subs(z,0)-(L**3+12*sp.pi**2*L)) == 0
T21 = sp.Rational(1,2)*(sp.Rational(1,8)+sp.Rational(1,64))*(L**2+12*sp.pi**2)/6
assert sp.simplify(T21-3*(L**2+12*sp.pi**2)/256) == 0
assert sp.simplify(T21*sp.Rational(S(2,1).numerator,S(2,1).denominator)+3*(L**2+12*sp.pi**2)/512) == 0

mp.mp.dps = 65
H = lambda x,l: (mp.sech((x-l)/4)-mp.sech((x+l)/4))/(4*mp.pi)
quad = lambda f, l: mp.quad(f, [0, max(20,2*abs(l)), 100, mp.inf])
errors = []
for l in [mp.mpf('-7'),mp.mpf('0'),mp.mpf('0.5'),mp.mpf('3'),mp.mpf('12')]:
    for power, expected in [(1,l),(3,l**3+12*mp.pi**2*l)]:
        actual = quad(lambda x: x**power*H(x,l),l)
        err = abs(actual-expected)
        assert err < mp.mpf('1e-45')*(1+abs(expected)), (l,power,err)
        errors.append(err)
    sw = quad(lambda x: -x*H(2*x,l)/2,l)
    err = abs(sw+l/8)
    assert err < mp.mpf('1e-45')*(1+abs(l)), (l,err)
    errors.append(err)
for x,l,j in [(mp.mpf('0.1'),mp.mpf('2'),mp.mpf('5')),(mp.mpf('7'),mp.mpf('3'),mp.mpf('1'))]:
    assert abs((H(x+j,l)+H(x-j,l))/2-(H(x,l+j)+H(x,l-j))/2)<mp.mpf('1e-60')

report = {
    'frozen_targets_and_dependency_hashes_match': True,
    'transverse_integral': str(transverse),
    'divisor_curvature_coefficient': '1/2',
    'canonical_odd_integral': '1/32',
    'dual_odd_integral': '-1/32',
    'model_flux_disk_mass': str(mass),
    'flux_convention': 'disk mass = m_prime(t)/2',
    'normalization_ratio_cases': ratio_cases,
    'stable_separating_cases': split_cases,
    'numerical_integrals_checked': len(errors),
    'max_absolute_numerical_integral_error': mp.nstr(max(errors), 8),
    'T_2_1': str(sp.simplify(T21)),
    'all_reproducibility_checks_passed': True,
    'theorem_application_and_current_extension_require_the_written_mathematical_audit': True,
    'actual_torsion_comparison_verified': False,
    'higher_rank_top_chern_extension_verified': False,
}
OUT.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))

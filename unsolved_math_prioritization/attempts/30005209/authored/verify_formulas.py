"""Numerical sanity checks for proved formulas; these are not proof certificates."""
import json
import math
from pathlib import Path
from scipy.integrate import quad


def side_average_difference(A, B, cosine, alpha):
    D = A * B * math.sqrt(1 - cosine * cosine)
    def H(s, t):
        q = A*A*s*s + B*B*t*t
        cross = 2*A*B*cosine*s*t
        return (q + cross)**(-alpha/2) + (q-cross)**(-alpha/2)
    val, err = quad(lambda u: (1-u)*(H(1,u)-H(u,1)), 0, 1,
                    epsabs=2e-12, epsrel=2e-12)
    return D*val/(3-alpha), D*err/(3-alpha)


def square_hessian(alpha):
    val, err = quad(lambda u: (1-u)**2*(1+u)/(1+u*u)**(1+alpha/2),
                    0, 1, epsabs=2e-12, epsrel=2e-12)
    return -8*alpha*val/(3-alpha), 8*alpha*err/(3-alpha)


def convolution_energy(alpha):
    # The singular integral on (0,1) is integrated exactly term by term.
    part1 = (2/3)/(1-alpha) - 1/(3-alpha) + 0.5/(4-alpha)
    part2, err = quad(lambda u: u**(-alpha)*(2-u)**3/6,
                      1, 2, epsabs=2e-12, epsrel=2e-12)
    numerical = 2*(part1+part2)
    exact_formula = 2*(2**(4-alpha)-4)/math.prod(k-alpha for k in [1,2,3,4])
    J = 2/((1-alpha)*(2-alpha))
    gap = J-(4-alpha)*exact_formula/4
    return dict(alpha=alpha, convolution=numerical, closed_form=exact_formula,
                absolute_difference=abs(numerical-exact_formula),
                vertex_minus_side_limit=gap, quadrature_error_estimate=2*err)


def main():
    rows = []
    for alpha in [0.1, 0.5, 1.0, 1.9]:
        for cosine in [-0.75, 0.0, 0.75]:
            d, err = side_average_difference(2.0, 0.5, cosine, alpha)
            reverse, _ = side_average_difference(0.5, 2.0, cosine, alpha)
            rhombus, _ = side_average_difference(1.0, 1.0, cosine, alpha)
            assert d < 0 and reverse > 0 and rhombus == 0
            assert abs(d+reverse) < 1e-11
            rows.append(dict(alpha=alpha, cosine=cosine, difference=d,
                             swapped_difference=reverse, rhombus_difference=rhombus,
                             quadrature_error_estimate=err))
    hessians = []
    for alpha in [0.1, 0.5, 1.0, 1.9]:
        h, err = square_hessian(alpha)
        eps = 1e-5
        d, _ = side_average_difference(math.exp(eps), math.exp(-eps), 0.0, alpha)
        finite_difference = 2*d/eps
        assert h < 0 and abs(h-finite_difference) < 1e-7
        hessians.append(dict(alpha=alpha, exact_integral_evaluation=h,
                             first_derivative_difference_quotient=finite_difference,
                             absolute_difference=abs(h-finite_difference),
                             quadrature_error_estimate=err))
    convolution = [convolution_energy(alpha) for alpha in [0.1, 0.5, 0.9]]
    assert all(r['absolute_difference'] < 1e-11 and r['vertex_minus_side_limit'] > 0
               for r in convolution)
    out = dict(status='all sanity checks passed',
               proof_status='Floating-point checks only. The proofs are in the mathematical notes.',
               parallelogram_checks=rows, square_hessian_checks=hessians,
               thin_triangle_checks=convolution)
    Path(__file__).with_name('verification_results.json').write_text(
        json.dumps(out, indent=2)+'\n')
    print(json.dumps(dict(status=out['status'], parallelogram_cases=len(rows),
                         square_hessian_cases=len(hessians),
                         convolution_cases=len(convolution))))


if __name__ == '__main__':
    main()

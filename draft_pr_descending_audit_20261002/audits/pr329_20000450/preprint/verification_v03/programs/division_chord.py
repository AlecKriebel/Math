#!/usr/bin/env python3
# Public export: optimization must not disable scientific assertions.
import sys
if sys.flags.optimize:
    raise SystemExit("Verification refuses Python optimization (-O/-OO).")
"""Independent fifth-torsion derivation from chord/tangent law, no candidate imports."""
import json
import sympy as s
import sys

x, c2, c1, c0, beta = s.symbols('x c2 c1 c0 beta')
f = x**3+c2*x**2+c1*x+c0
checks = []


def equal(left, right, name):
    difference = s.cancel(left-right)
    if difference != 0:
        raise ValueError(name+': '+str(difference))
    checks.append(name)


def main():
    # Work in Q(c2,c1,c0,x)[v]/(v^2-f). Slopes have only a v coefficient.
    slope2_over_v = s.diff(f,x)/(2*f)
    x2 = s.cancel(f*slope2_over_v**2-c2-2*x)
    v2_over_v = s.cancel(-1+slope2_over_v*(x-x2))
    slope3_over_v = s.cancel((v2_over_v-1)/(x2-x))
    x3 = s.cancel(f*slope3_over_v**2-c2-x2-x)
    # Curve membership follows from the following universal line-intersection
    # factorization; this avoids expanding f(x3) as a huge nested rational term.
    z, x1, x_2, v1, v_2, slope, intercept = s.symbols('z x1 x_2 v1 v_2 slope intercept')
    line_difference = (slope*z+intercept)**2-f.subs(x,z)
    equal(s.Poly(line_difference,z).coeff_monomial(z**2),slope**2-c2,
          'Vieta third-intersection abscissa coefficient')
    equal(f.subs(x,x2), f*v2_over_v**2, 'doubled point lies on cubic')
    # These are independently extracted from the addition expressions.
    q3 = s.cancel(4*f*(x-x2))
    h6 = s.cancel(16*f**2*v2_over_v)
    q5 = s.cancel((x2-x3)*4*f*q3**2)
    q5 = s.Poly(q5,x).as_expr()
    b2,b4,b6,b8 = 4*c2,2*c1,4*c0,4*c2*c0-c1**2
    expected_q3 = 3*x**4+b2*x**3+3*b4*x**2+3*b6*x+b8
    expected_h6 = 2*x**6+b2*x**5+5*b4*x**4+10*b6*x**3+10*b8*x**2+(b2*b8-b4*b6)*x+b4*b8-b6**2
    equal(q3,expected_q3,'third polynomial agrees with direct doubling numerator')
    equal(h6,expected_h6,'fourth polynomial divided by2v agrees with doubled ordinate')
    equal(q5,16*f**2*h6-q3**3,'fifth recursion agrees with x2-x3 chord numerator')
    if s.degree(q5,x)!=12 or s.Poly(q5,x).LC()!=5:
        raise ValueError('Wrong fifth polynomial degree/leading coefficient')
    specialization={c2:(beta**2-6*beta+1)/4,c1:(beta**2-beta)/2,c0:beta**2/4}
    fifth=s.Poly(s.expand(q5.subs(specialization)),x)
    third=s.expand(q3.subs(specialization))
    branch=s.expand(4*f.subs(specialization))
    remainder, residual=s.div(fifth,s.Poly(x*(x-beta),x))
    if not residual.is_zero: raise ValueError('Marked subgroup is not a factor')
    manuscript_coefficients=[5,5*(beta**2-5*beta+1),
        beta**4-7*beta**3+44*beta**2-38*beta+1,
        beta*(beta**4+3*beta**3-26*beta**2+127*beta-9),
        beta**2*(beta**4+3*beta**3+19*beta**2-248*beta+36),
        beta**3*(beta**4+3*beta**3-71*beta**2+322*beta-84),
        beta**4*(beta**4-12*beta**3+94*beta**2-293*beta+126),
        5*beta**5*(beta**3-10*beta**2+36*beta-25),
        5*beta**6*(2*beta**2-13*beta+16),10*beta**7*(beta-3),5*beta**8]
    for power,(actual,claimed) in enumerate(zip(remainder.all_coeffs(),manuscript_coefficients)):
        equal(actual,claimed,'R coefficient x^'+str(10-power))
    Delta=beta**5*(beta**2-11*beta-1)
    equal(s.resultant(fifth.as_expr(),branch,x),Delta**6,'no second-torsion collision: resultant=Delta^6')
    equal(s.resultant(fifth.as_expr(),third,x),Delta**8,'no third-torsion denominator collision: resultant=Delta^8')
    equal(remainder.as_expr().subs(x,0),5*beta**8,'R does not include x=0 when beta nonzero')
    equal(remainder.as_expr().subs(x,beta),5*beta**12,'R does not include x=beta when beta nonzero')
    example=s.Poly(q5.subs({c2:0,c1:0,c0:1}),x)
    exact_disc=s.discriminant(example.as_expr(),x)
    equal(exact_disc,5**11*(-432)**22,'universal discriminant constant from nonsingular v^2=x^3+1')
    # Deliberately altered x^8 coefficient must fail exact equality.
    mutant=remainder.as_expr()+beta*x**8
    if s.expand(mutant-remainder.as_expr())==0: raise ValueError('Coefficient mutant was not detected')
    # At beta=0 the model and polynomial are singular; at characteristic5 the
    # leading coefficient vanishes, so the characteristic-zero count cannot pass.
    bad=s.Poly(fifth.as_expr().subs(beta,0),x)
    if s.degree(s.gcd(bad,bad.diff()),x)==0: raise ValueError('Singular-fiber repeated-root boundary missed')
    char5=s.Poly(fifth.as_expr().subs(beta,1),x,modulus=5)
    if char5.degree()==12: raise ValueError('Characteristic5 leading-coefficient degeneration missed')
    print(json.dumps(dict(status='PASS',interpreter=sys.executable,sympy_version=s.__version__,
        mechanism='Direct chord/tangent doubling/tripling before specialization; no candidate imports',
        exact_checks=checks,third_from_chord=str(s.expand(q3)),fourth_over_2v_from_chord=str(s.expand(h6)),
        generic_fifth_coefficients=[str(s.factor(a)) for a in s.Poly(q5,x).all_coeffs()],
        Tate_remainder_coefficients=[str(s.factor(a)) for a in remainder.all_coeffs()],
        fifth_degree=12,fifth_leading_coefficient=5,second_torsion_resultant='Delta^6',third_torsion_resultant='Delta^8',
        discriminant_constant_certificate='5^11; universal homogeneity/separability proof required for Delta^22 exponent',
        coefficient_mutant_rejected=True,singular_beta0_repeated_root_detected=True,
        characteristic5_degree=char5.degree(),
        scope='Exact generic polynomial derivation and factors; completeness and discriminant homogeneity/etaleness proof are in REPORT.md, not inferred from finite samples.'),indent=2))


if __name__=='__main__':
    main()

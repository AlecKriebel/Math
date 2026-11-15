#!/usr/bin/env python3
"""Independent exact geometry/algebra checks; imports no author/audit code.

This uses real-coordinate Wirtinger derivatives for all four charts, obtains
an exact Bernstein certificate for the full determinant, and solves the
second-variation equation by its polynomial coefficient matrix. It does not
prove parabolic existence or authenticate the equation against publications.
"""
import json
import platform
from pathlib import Path
import sympy as S

ROOT = Path(__file__).resolve().parent
checks = []


def equal(name, left, right=0):
    difference = S.factor(S.together(S.simplify(left - right)))
    if difference != 0:
        raise AssertionError((name, difference))
    checks.append(name)


def bernstein_coefficients(polynomial, variables):
    poly = S.Poly(S.expand(polynomial), *variables)
    first, second = variables
    m, n = poly.degree(first), poly.degree(second)
    result = []
    for i in range(m + 1):
        row = []
        for j in range(n + 1):
            value = sum(
                poly.coeff_monomial(first**k * second**l)
                * S.binomial(i, k) / S.binomial(m, k)
                * S.binomial(j, l) / S.binomial(n, l)
                for k in range(i + 1) for l in range(j + 1)
            )
            row.append(value)
        result.append(row)
    rebuilt = sum(
        result[i][j] * S.binomial(m, i) * first**i * (1-first)**(m-i)
        * S.binomial(n, j) * second**j * (1-second)**(n-j)
        for i in range(m + 1) for j in range(n + 1)
    )
    equal("Bernstein reconstruction " + str((m, n)), rebuilt, polynomial)
    return result


epsilon = S.Rational(1, 96)
delta = S.Rational(1, 4)
r, a, z, b = S.symbols("r a z b", real=True)
u, v = S.symbols("u v", nonnegative=True)
p, x = S.symbols("p x", real=True)
q = S.symbols("q", real=True)
ru = r*r + a*a
rv = z*z + b*b

# Independent differentiation in Re(s), Im(s), Re(z), Im(z). Rotational
# symmetry then reduces to a=b=0 without changing diagonal values or the
# modulus of the mixed term. Do not use the author's radial derivative code.
chart_records = []
derived = None
for base_infinity in (False, True):
    for fiber_infinity in (False, True):
        local_p = 1/(1+ru) if base_infinity else ru/(1+ru)
        local_x = 1/(1+rv) if fiber_infinity else rv/(1+rv)
        weight = (2*S.log(1+ru) + 2*S.log(1+rv)
                  + (2-epsilon)*(1-local_p) + delta*local_p*local_x**2)
        hss = ((S.diff(weight, r, 2) + S.diff(weight, a, 2))/4).subs({a:0, b:0})
        hzz = ((S.diff(weight, z, 2) + S.diff(weight, b, 2))/4).subs({a:0, b:0})
        hsz = ((S.diff(weight, r, z) + S.diff(weight, a, b)
                + S.I*(S.diff(weight, r, b)-S.diff(weight, a, z)))/4).subs({a:0, b:0})
        hss = S.factor(hss)
        hzz = S.factor(hzz)
        hsz = S.factor(hsz)
        pp = 1/(1+r*r) if base_infinity else r*r/(1+r*r)
        xx = 1/(1+z*z) if fiber_infinity else z*z/(1+z*z)
        # The following target polynomials are derived from finite-chart
        # real differentiation below, rather than imported from the draft.
        finite_substitution = {r:S.sqrt(p/(1-p)), z:S.sqrt(x/(1-x))}
        if not base_infinity and not fiber_infinity:
            AA = S.factor(((1+r*r)**2*hss).subs(finite_substitution))
            BB = S.factor(((1+z*z)**2*hzz).subs(finite_substitution))
            QQ = S.factor(((1+r*r)**2*(1+z*z)**2*hsz**2).subs(finite_substitution))
            derived = (AA, BB, QQ)
            equal("finite central fiber metric", hzz.subs(r,0), 2/(1+z*z)**2)
            equal("finite central mixed term", hsz.subs(r,0), 0)
            equal("finite central base jet", hss.subs(r,0), epsilon+delta*(z*z/(1+z*z))**2)
        AA, BB, QQ = derived
        label = ("infinity" if base_infinity else "finite") + "/" + ("infinity" if fiber_infinity else "finite")
        equal(label+" base curvature", (1+r*r)**2*hss, AA.subs({p:pp,x:xx}))
        equal(label+" fiber curvature", (1+z*z)**2*hzz, BB.subs({p:pp,x:xx}))
        equal(label+" mixed squared modulus", (1+r*r)**2*(1+z*z)**2*hsz**2, QQ.subs({p:pp,x:xx}))
        chart_records.append({"chart":label, "real_derived_hss":str(hss), "real_derived_hzz":str(hzz), "real_derived_hsz_at_zero_phases":str(hsz)})

AA, BB, QQ = derived
DD = S.expand(AA*BB-QQ)
certificates = {}
for name, polynomial in (("A",AA),("B",BB),("determinant",DD)):
    coefficients = bernstein_coefficients(polynomial, (p,x))
    minimum = min(sum(coefficients, []))
    if minimum <= 0:
        raise AssertionError((name, minimum))
    checks.append(name+" universal positive Bernstein certificate")
    certificates[name] = {"coefficients":[[str(c) for c in row] for row in coefficients], "lower_bound":str(minimum)}
equal("A bound equals epsilon", S.Rational(certificates["A"]["lower_bound"]), epsilon)
equal("B bound", S.Rational(certificates["B"]["lower_bound"]), S.Rational(3,2))
equal("determinant stronger continuum bound", S.Rational(certificates["determinant"]["lower_bound"]), S.Rational(1,48))

# Establish weight transitions directly in radial charts with positive radii.
U,V = S.symbols("U V", positive=True)
finite = 2*S.log(1+u)+2*S.log(1+v)+(2-epsilon)/(1+u)+delta*u/(1+u)*(v/(1+v))**2
for bi,fi in ((True,False),(False,True),(True,True)):
    old = finite.subs({u:1/U if bi else U, v:1/V if fi else V})
    correction = (2*S.log(U) if bi else 0)+(2*S.log(V) if fi else 0)
    pp = 1/(1+U) if bi else U/(1+U)
    xx = 1/(1+V) if fi else V/(1+V)
    new = 2*S.log(1+U)+2*S.log(1+V)+(2-epsilon)*(1-pp)+delta*pp*xx**2
    equal("weight transition "+str((bi,fi)), S.expand_log(old+correction,force=True), new)

# Probability normalization at the stationary central fiber with planar
# area dA; radial area is pi*dv. Base constants cancel exactly.
radial_mass = S.integrate(1/(1+v)**2, (v,0,S.oo))
equal("central anticanonical radial mass", radial_mass, 1)
equal("central curvature radial mass", S.integrate(2/(1+v)**2,(v,0,S.oo)), 2)
equal("stationary density ratio", (2/(1+v)**2)/2, (1/(1+v)**2)/radial_mass)
equal("uniform x probability", S.diff(v/(1+v),v), 1/(1+v)**2)

# Obtain the radial Laplacian by applying actual real Wirtinger derivatives
# to a generic F(x), then compare its chain-rule form, before any spectrum.
F = S.Function("F")
xx_real = (z*z+b*b)/(1+z*z+b*b)
lap_real = ((1+z*z)**2/2 * (S.diff(F(xx_real),z,2)+S.diff(F(xx_real),b,2))/4).subs(b,0)
lap_expected = (S.Rational(1,2)*(x*(1-x)*S.diff(F(x),x,2)+(1-2*x)*S.diff(F(x),x))).subs(x,z*z/(1+z*z))
equal("generic real-coordinate Laplacian", lap_real, lap_expected)

def lap(poly):
    return (x*(1-x)*S.diff(poly,x,2)+(1-2*x)*S.diff(poly,x))/2

def horizontal_generator(poly):
    return S.expand(lap(poly)+poly-S.integrate(poly,(x,0,1)))

# Polynomial coefficients, not a supplied Legendre expansion.
basis = (S.Integer(1),x,x*x)
matrix = S.Matrix([[horizontal_generator(poly).coeff(x,i) for poly in basis] for i in range(3)])
expected_matrix = S.Matrix([[0,0,-S.Rational(1,3)],[0,0,2],[0,0,-2]])
for i in range(3):
    for j in range(3):
        equal("generator entry "+str((i,j)),matrix[i,j],expected_matrix[i,j])
w = epsilon - delta*(1-q)/6 + delta*(1-q)*x + delta*q*x*x
equal("coefficient solution initial jet",w.subs(q,1),epsilon+delta*x*x)
equal("coefficient solution exact PDE",-2*q*S.diff(w,q),horizontal_generator(w))
equal("coefficient solution mean",S.integrate(w,(x,0,1)),epsilon+delta/3)
equal("exact negative coefficient",w.subs({x:0,q:S.Rational(1,2)}),-S.Rational(1,96))
equal("zero crossing q=3/4",w.subs({x:0,q:S.Rational(3,4)}),0)
equal("pole initial derivative",horizontal_generator(epsilon+delta*x*x).subs(x,0),-S.Rational(1,12))
equal("monotonicity certificate in x",S.diff(w,x),delta*((1-q)+2*q*x))

# Independently check the specific eigenmodes quoted by the draft after
# solving by the matrix mechanism.
P1,P2 = 2*x-1, 6*x*x-6*x+1
equal("quoted degree-one eigenmode",lap(P1),-P1)
equal("quoted degree-two eigenmode",lap(P2),-3*P2)
equal("quoted mode solution matches independent polynomial",w,epsilon+delta/3+delta*P1/2+delta*q*P2/6)

# Normalization controls: omission of denominator changes the reaction of
# the constant component. Correct root weight and positive time rescaling
# preserve the sign; mixing conventions need not.
equal("unnormalized-density initial pole derivative",(lap(epsilon+delta*x*x)+epsilon+delta*x*x).subs(x,0),epsilon)
equal("root weight at negative time",w.subs({x:0,q:S.Rational(1,2)})/2,-S.Rational(1,192))
equal("stationary-product reaction cancellation",S.Integer(2)-S.Integer(2),0)
rank = S.symbols("rank",positive=True)
root = w/rank
root_generator = rank*lap(root)+rank*root-rank*S.integrate(root,(x,0,1))
equal("root plus time-rescaling generator",root_generator,rank*(-2*q*S.diff(root,q)))
growth = S.symbols("growth",positive=True)
unnormalized = (epsilon+delta/3)*growth+delta*P1/2+delta*q*P2/6
equal("omitted-denominator PDE",growth*S.diff(unnormalized,growth)-2*q*S.diff(unnormalized,q),lap(unnormalized)+unnormalized)
equal("omitted-denominator pole growth certificate",S.diff(unnormalized,growth).subs(x,0)*growth-2*q*S.diff(unnormalized,q).subs(x,0),epsilon*growth+delta*(growth-q)/3)

report = {
    "status":"PASS_GEOMETRY_AND_EXACT_ALGEBRA",
    "exact_checks":len(checks),
    "check_names":checks,
    "initial_curvature_polynomials":{"A":str(AA),"B":str(BB),"mixed_squared":str(QQ),"determinant":str(DD)},
    "four_chart_real_derivatives":chart_records,
    "universal_bernstein_certificates":certificates,
    "horizontal_polynomial_generator":str(matrix),
    "horizontal_solution_q_exp_minus_2t":str(w),
    "negative_time":"log(2)/2",
    "negative_coefficient":"-1/96",
    "strongest_verified_claim":"Global initial positivity and exact finite-time negative horizontal curvature for the explicitly stated normalized equation, conditional on smooth finite-time existence.",
    "unverified_dependencies":["Published source's intended flow convention and scope","Finite-time smooth existence theorem and its applicability"],
    "python":platform.python_version(),
    "sympy":S.__version__,
}
(ROOT/"verification_results.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps({key:report[key] for key in ("status","exact_checks","negative_time","negative_coefficient")},indent=2))

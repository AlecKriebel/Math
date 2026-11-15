#!/usr/bin/env python3
"""Read-only exact diagnostics for the independent sealed reconstruction.

No archive imports, network, file creation, or supplied-result reads. Run with
the stated Python/SymPy environment; stdout is the only output.
Analytic smooth existence and the mathematical parameter differentiation are
documented separately, not certified by these identities.
"""
import json
import platform
import sympy as S

checks = []
controls = []


def same(name, a, b=0):
    residual = S.factor(S.together(a-b))
    if residual != 0:
        raise AssertionError((name, str(residual)))
    checks.append(name)


def reject(name, residual):
    residual = S.factor(S.together(residual))
    if residual == 0:
        raise AssertionError(("negative control survived", name))
    controls.append({"mutation": name, "nonzero_residual": str(residual)})


u, v = S.symbols("u v", nonnegative=True)
p, x, y = S.symbols("p x y", real=True)
e, d = S.Rational(1, 96), S.Rational(1, 4)


def radial(q, z):
    return S.diff(q, z)+z*S.diff(q, z, 2)


# An arbitrary radial function: independently establish the Wirtinger rule
# from real coordinates before specializing to the stated initial weight.
a, b, c, h = S.symbols("a b c h", real=True)
F = S.Function("F")
real_q = F(a*a+b*b, c*c+h*h)
same("generic base radial Wirtinger rule",
     (S.diff(real_q, a, 2)+S.diff(real_q, b, 2))/4,
     radial(F(u, v), u).subs({u:a*a+b*b, v:c*c+h*h}))
same("generic fiber radial Wirtinger rule",
     (S.diff(real_q, c, 2)+S.diff(real_q, h, 2))/4,
     radial(F(u, v), v).subs({u:a*a+b*b, v:c*c+h*h}))

A = 4*p+(e+d*x*x)*(1-2*p)
B = 2+2*d*p*x*(2-3*x)
Q = 4*d*d*p*(1-p)*x**3*(1-x)
finite = 2*S.log(1+u)+2*S.log(1+v)+(2-e)/(1+u)+d*u/(1+u)*(v/(1+v))**2
for invert_s in (False, True):
    for invert_z in (False, True):
        pp = 1/(1+u) if invert_s else u/(1+u)
        xx = 1/(1+v) if invert_z else v/(1+v)
        local = 2*S.log(1+u)+2*S.log(1+v)+(2-e)*(1-pp)+d*pp*xx**2
        label = "chart "+str((invert_s, invert_z))
        same(label+" horizontal", (1+u)**2*radial(local, u), A.subs({p:pp, x:xx}))
        same(label+" vertical", (1+v)**2*radial(local, v), B.subs({p:pp, x:xx}))
        same(label+" mixed squared", (1+u)**2*(1+v)**2*u*v*S.diff(local, u, v)**2, Q.subs({p:pp, x:xx}))
        old = finite.subs({u:1/u if invert_s else u, v:1/v if invert_z else v}, simultaneous=True)
        transition = (2*S.log(u) if invert_s else 0)+(2*S.log(v) if invert_z else 0)
        # Transition overlaps have strictly positive radii. Factor log
        # arguments before applying real log laws; nonnegative symbols alone
        # do not make the CAS expand log(1+1/u).
        difference = old+transition-local
        difference = difference.replace(lambda z: z.func == S.log,
                                        lambda z: S.log(S.factor(z.args[0])))
        same(label+" bundle transition", S.expand_log(difference, force=True))

# These identities have explicitly nonnegative factors on the CLOSED square.
# Hence they prove continuum positivity, including both projective infinities.
a0, b0, q0 = e+S.Rational(167, 48)*p, S.Rational(3, 2), p/4
ra = d*(x*x+2*p*(1-x*x))
rb = 2*d*((1-p)+p*(1-x)*(1+3*x))
rq = 4*d*d*p*(p+(1-p)*((1-x)*(1+x+x*x)+x**4))
same("A certificate", A-a0, ra)
same("B certificate", B-b0, rb)
same("Q certificate", q0-Q, rq)
same("strict determinant baseline", a0*b0-q0, S.Rational(1, 64)+S.Rational(159, 32)*p)
same("whole determinant certificate", A*B-Q, a0*b0-q0+ra*B+a0*rb+rq)
same("strict weakest initial horizontal endpoint", A.subs({p:0, x:0}), e)
same("strict vertical infinity endpoint", B.subs({p:1, x:1}), S.Rational(3, 2))

same("central fiber curvature", radial(finite, v).subs(u, 0), 2/(1+v)**2)
same("central horizontal initial jet", radial(finite, u).subs(u, 0), e+d*(v/(1+v))**2)
same("central mixed vanishing", (u*v*S.diff(finite, u, v)**2).subs(u, 0))
same("stationary normalized density", (2/(1+v)**2)/2, 1/(1+v)**2)
same("probability normalization", S.integrate(1/(1+v)**2, (v, 0, S.oo)), 1)
same("pushforward uniform probability", S.diff(v/(1+v), v), 1/(1+v)**2)


def lap(q):
    return (x*(1-x)*S.diff(q, x, 2)+(1-2*x)*S.diff(q, x))/2


# Generic chain rule, not a fit to finitely many powers.
fx = F(x)
same("generic radial Laplacian coordinate rule",
     (1+v)**2*radial(fx.subs(x, v/(1+v)), v)/2,
     lap(fx).subs(x, v/(1+v)))
P1, P2 = 2*x-1, 6*x*x-6*x+1
for name, mode, eigen in (("one", P1, -1), ("two", P2, -3)):
    same("mode "+name+" eigenvalue", lap(mode), eigen*mode)
    same("mode "+name+" zero mean", S.integrate(mode, (x, 0, 1)))
same("quadratic decomposition", x*x, S.Rational(1, 3)+P1/2+P2/6)
w = e+d/3+d*P1/2+d*y*P2/6
mean = S.integrate(w, (x, 0, 1))
dt = -2*y*S.diff(w, y)
same("closed actual jet PDE", dt, lap(w)+w-mean)
same("initial jet", w.subs(y, 1), e+d*x*x)
same("conserved mean", mean, e+d/3)
same("exact pole formula", w.subs(x, 0), e-d*(1-y)/6)
same("exact finite negative value y=1/2", w.subs({x:0, y:S.Rational(1, 2)}), -e)
same("exact zero threshold y=3/4", w.subs({x:0, y:S.Rational(3, 4)}))
same("initial pole derivative", dt.subs({x:0, y:1}), -S.Rational(1, 12))
same("increasing in x for all finite t", S.diff(w, x), d*((1-y)+2*y*x))
same("constant-mode generator vanishes", lap(S.Integer(1))+S.Integer(1)-S.integrate(S.Integer(1), (x, 0, 1)))

# The product is exactly stationary for the DEFINITION of the probability
# flow. A literal +r*c in the SAME weight/time gives a falsifiable residual.
cprod = radial(2*S.log(1+u), u)
li = radial(-2*S.log(1+u), u)
same("stationary product coefficient-one calibration", cprod+li)
same("product coefficient at s=0", cprod.subs(u, 0), 2)
reject("same-weight/time rank-two reaction in printed evolution", (2*cprod+li).subs(u, 0))
reject("omit evolving integral normalization", dt-(lap(w)+w))
reject("reverse normalization-mean sign", dt-(lap(w)+w+mean))
reject("reverse Laplacian sign", dt-(-lap(w)+w-mean))
reject("insert rank-two reaction without conversion", dt-(lap(w)+2*w-mean))
reject("wrong rate exp(-t)", -y*S.diff(w, y)-(lap(w)+w-mean))
reject("negative value already at time zero", w.subs({x:0, y:1})+e)

r = S.symbols("r", positive=True)
root = w/r
same("consistent root-weight and time conversion", r*lap(root)+r*root-r*S.integrate(root, (x, 0, 1)), r*(-2*y*S.diff(root, y)))

print(json.dumps({
    "status":"PASS_EXACT_DIAGNOSTICS_WITH_EXPLICIT_ANALYTIC_INPUT",
    "record_id":23331080,
    "exact_checks":len(checks), "check_names":checks,
    "negative_controls_rejected":len(controls), "negative_controls":controls,
    "initial_positivity":"A*B-Q >= 1/64+(159/32)*p > 0 on entire closed unit square",
    "actual_jet":"epsilon+delta/3+delta*P1/2+delta*exp(-2*t)*P2/6",
    "negative_coefficient":"-1/96", "finite_time":"log(2)/2",
    "import_limit":"Actual smooth finite-time nonlinear flow existence and parameter regularity remain cited analytic mathematics, not computer-proved.",
    "sampling_used_as_proof":False, "supplied_code_or_result_imported":False,
    "python":platform.python_version(), "sympy":S.__version__
}, indent=2))

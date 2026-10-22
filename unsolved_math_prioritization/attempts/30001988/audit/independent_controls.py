#!/usr/bin/env python3
"""Independent exact controls, not a proof of an infinite mathematical claim.
Requires Python 3 and SymPy 1.14.0. Writes only JSON to stdout.
"""
import json
import random
import sympy as s

def require(p, msg):
    if not p:
        raise RuntimeError(msg)

def main():
    t = s.Symbol('t')
    z = s.symbols('z0:6')
    vars = (t,) + z
    def delta(p):
        return s.diff(p, t) + sum(s.diff(p, z[i])*z[i+1] for i in range(5))
    def zero(p):
        return s.Poly(s.expand(p), *vars).is_zero
    rng = random.Random(30001988)
    def poly():
        v = (t,) + z[:5]
        p = s.Integer(rng.randrange(-3,4))
        for _ in range(8):
            p += rng.randrange(-3,4)*rng.choice(v)*rng.choice((s.Integer(1),)+v)
        return s.expand(p)
    coeffs = [(s.Integer(1),s.Integer(1)), (-s.Integer(1),s.Integer(1)),
              (t,s.Integer(1)), (t*t+1,s.Integer(1)), (s.Integer(1),t+1)]
    nonprimitive = 0
    highest_jet = 0
    for k in range(100):
        n,d = poly(),poly()
        if zero(d): d=s.Integer(1)
        numerator=s.expand(delta(n)*d-n*delta(d))
        for an,ad in coeffs:
            require(not zero(ad*numerator-an*z[0]*d*d), 'unexpected rational primitive')
            nonprimitive += 1
        # Independent quotient-rule coefficient identity: no cancellation is hidden.
        require(zero(s.diff(numerator,z[5])-(s.diff(n,z[4])*d-n*s.diff(d,z[4]))),
                'highest-jet coefficient mismatch')
        highest_jet += 1
    # A finite polynomial-ansatz search. Includes nonconstant coefficients in Q(t).
    basis = sorted(s.polys.monomials.itermonomials((t,)+z[:4],2), key=str)
    c = s.symbols('c0:'+str(len(basis)))
    ansatz = sum(ci*mi for ci,mi in zip(c,basis))
    for a in (s.Integer(1),t,t*t+1):
        eqs=s.Poly(s.expand(delta(ansatz)-a*z[0]),*vars).coeffs()
        require(s.linsolve(eqs,c) is s.EmptySet, 'polynomial ansatz unexpectedly solvable')
    # Positive controls ensure the derivative engine can find actual primitives.
    positive = 0
    for r in (s.Integer(0),s.Integer(1),t,z[0],t*z[0],z[0]**2,z[2],1/(z[0]+1)):
        n,d=s.fraction(r)
        b=delta(r)
        require(s.cancel((delta(n)*d-n*delta(d))/d**2-b)==0, 'positive derivative control')
        positive += 1
    # Leibniz terms must not disappear for nonconstant a.
    require(zero(delta(t*z[0])-(z[0]+t*z[1])), 'nonconstant coefficient lost')
    require(zero(delta(delta(t*z[0]))-(2*z[1]+t*z[2])), 'second Leibniz term lost')
    # Scope counterexample: a may not be promoted from K to F.
    require(s.cancel((z[1]/z[0])*z[0]-delta(z[0]))==0, 'coefficient-scope counterexample')
    # Scope counterexample: an algebraically transcendental constant is not a
    # differential indeterminate. Over K=Q(t), t'=1, adjoin a transcendental
    # constant c: delta(t*c)=c. Evaluating positive c-jets at zero checks this.
    constant_jets = {zi:0 for zi in z[1:]}
    require(zero(delta(t*z[0]).subs(constant_jets)-z[0]), 'transcendence-promise counterexample')
    # For a base-field primitive r, r and r+1 solve the same equation and Y-r
    # separates them. This exercises the unconstrained branch and specialization.
    specializations = 0
    for r in (s.Integer(0),t,t*t/2,t**3/3):
        require(s.cancel(delta(r+1)-delta(r))==0, 'translation control')
        require(s.expand((r+1)-r)==1, 'separation control')
        specializations += 1
    # Characteristic-p boundary: y^p=u, u'=0 admits the prescribed y'=z0,
    # and (y+1)^p-u has remainder 1. These are finite algebraic consistency
    # controls; the field construction and irreducibility are proved in AUDIT.md.
    Y,U,Z=s.symbols('Y U Z')
    positive_characteristics=0
    for p in (2,3,5,7):
        require(s.Poly(s.diff(Y**p-U,Y)*Z,Y,U,Z, modulus=p).is_zero,
                'inseparable relation incompatible with derivation')
        rem=s.rem(s.Poly((Y+1)**p-U,Y,U,modulus=p),s.Poly(Y**p-U,Y,U,modulus=p))
        require(rem.as_expr()==1, 'characteristic-p separating polynomial')
        positive_characteristics += 1
    print(json.dumps({
        'passed':True,'engine':'SymPy exact polynomial/rational arithmetic',
        'sympy_version':s.__version__,'seed':30001988,
        'rational_nonprimitive_controls':nonprimitive,
        'highest_jet_coefficient_controls':highest_jet,
        'polynomial_ansatz_unsatisfiability_controls':3,
        'polynomial_ansatz_basis_size':len(basis),
        'positive_derivative_controls':positive,
        'nonconstant_coefficient_Leibniz_controls':2,
        'scope_counterexample_controls':2,
        'specialization_root_separation_controls':specializations,
        'positive_characteristic_boundary_controls':positive_characteristics,
        'limitations':'Finite exact controls only; no DCF decision procedure, full-target reduction, or theorem-prover claim.'
    },indent=2))

if __name__=='__main__': main()

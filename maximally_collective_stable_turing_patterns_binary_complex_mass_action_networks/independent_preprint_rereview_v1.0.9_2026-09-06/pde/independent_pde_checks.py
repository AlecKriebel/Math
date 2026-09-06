#!/usr/bin/env python3
"""Independent exact checks: no imports from the paper's implementation.

Uses explicit polynomial reaction fields and their derivatives. Near-threshold
interval signs use Bernstein coefficients on epsilon in [0,1/1000], rather
than the production verifier's reciprocal orthant substitution. A finite
dimensional check is identified as such and never promoted to an all-m proof.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import sympy as S

results = {"target_commit": "94d5177485b9680be8b77f13448abf1f923963e8",
           "started_utc": datetime.now(timezone.utc).isoformat(), "checks": []}


def require(truth, detail):
    if not truth:
        raise RuntimeError(detail)


def zero(expression, detail):
    entries = list(expression) if isinstance(expression, S.MatrixBase) else [expression]
    require(all(S.cancel(z) == 0 for z in entries), detail)


def record(name, **details):
    results["checks"].append(dict(name=name, **details))
    print(name, flush=True)


def field(m):
    x = S.Matrix(S.symbols(f"x1:{m+2}"))
    f = S.zeros(m+1, 1)
    # Empty source -> X1.
    f[0] += 1
    # X1 + Xi -> X1 + X(i+1), i=2,...,m-2.
    for i in range(1, m-2):
        f[i] -= x[0]*x[i]
        f[i+1] += x[0]*x[i]
    # X1 + X(m-1) -> 2Xm, then 2Xm -> X2.
    q = x[0]*x[m-2]
    f[0] -= q
    f[m-2] -= q
    f[m-1] += 2*q
    f[m-1] -= 2*x[m-1]**2
    f[1] += x[m-1]**2
    # 2Z <-> X1 + Xm.
    net = x[m]**2-x[0]*x[m-1]
    f[0] += net
    f[m-1] += net
    f[m] -= 2*net
    c = S.Matrix([0]+[4]*(m-2)+[2, 1])
    unit = dict.fromkeys(x, S.Integer(1))
    zero(f.subs(unit), "unit state is not equilibrium")
    zero((c.T*f)[0], "reaction field does not conserve mass")
    A = f.jacobian(x).subs(unit)
    tensors = [S.hessian(fi, x) for fi in f]
    def B(u, v):
        return S.Matrix([(u.T*Q*v)[0] for Q in tensors])
    return A, c, B


def corrections(A, c, B, r, D, mass=None):
    mass = c if mass is None else mass
    forcing = -B(r, r)/4
    w0 = A.col_join(mass.T).gauss_jordan_solve(
        forcing.col_join(S.zeros(1, 1)))[0]
    w2 = (A-4*D).inv()*forcing
    zero(A*w0-forcing, "zero-mode correction fails")
    zero((mass.T*w0)[0], "zero-mode gauge fails")
    zero((A-4*D)*w2-forcing, "second-mode correction fails")
    return w0, w2


e, s, lam, t = S.symbols("epsilon s lambda t", real=True)


def bernstein_orthant_sign(expression, name):
    """Strict positivity for 0<epsilon<=1/1000, s>=0.

    Cancel a rational expression, extract powers of epsilon from numerator and
    denominator, and expand the remaining numerator/denominator by powers of s.
    Each coefficient polynomial in epsilon is converted to a Bernstein basis
    on [0,1/1000]. Nonnegative Bernstein coefficients prove nonnegativity.
    Strictly positive s^0 Bernstein coefficients prove strict positivity even
    at s=0; extracted epsilon factors are positive on the open interval.
    """
    num, den = S.fraction(S.cancel(expression))
    if den.subs({e: S.Rational(1, 2000), s: 0}) < 0:
        num, den = -num, -den
    diagnostics = []
    for namepart, part in (("numerator", num), ("denominator", den)):
        poly = S.Poly(part, e, s)
        power_e = min(monomial[0] for monomial, _ in poly.terms())
        reduced = S.cancel(part/e**power_e)
        blocks = S.Poly(reduced, s)
        require(blocks.coeff_monomial(1) != 0, f"{name}: no strict constant block")
        total = 0
        zeros = 0
        for (spower,), polynomial_e in blocks.terms():
            epoly = S.Poly(polynomial_e, e)
            degree = epoly.degree()
            power_coefficients = [epoly.nth(j)/S.Integer(1000)**j for j in range(degree+1)]
            bern = [S.factor(sum(power_coefficients[j]*S.binomial(k,j)/S.binomial(degree,j)
                                for j in range(k+1))) for k in range(degree+1)]
            require(all(v >= 0 for v in bern), f"{name} {namepart}: negative Bernstein coefficient")
            if spower == 0:
                require(all(v > 0 for v in bern), f"{name} {namepart}: non-strict constant block")
            total += len(bern)
            zeros += sum(v == 0 for v in bern)
        diagnostics.append(dict(part=namepart, extracted_epsilon_power=power_e,
                                s_blocks=len(blocks.terms()), bernstein_coefficients=total,
                                zero_coefficients=zeros))
    return dict(name=name, certificate=diagnostics)


def near_threshold():
    A, c, B = field(3)
    r = S.Matrix([1, -1-S.Rational(16,9)*e-e**2/2, -e,
                  S.Rational(1,2)-S.Rational(13,18)*e])
    D = S.diag(*[S.factor(v/r[i]) for i,v in enumerate(A*r)])
    M = A-D
    zero(M*r, "prescribed critical eigenvector fails")
    ell = M.T.nullspace()[0]
    ell = ell/ell[-1]
    w0, w2 = corrections(A,c,B,r,D)
    cubic = S.factor((ell.T*(B(r,w0)+B(r,w2)/2))[0]/(ell.T*r)[0])
    zero(S.limit(cubic,e,0)-S.Rational(6,1379), "incorrect cubic limit")
    zero(S.limit(S.diff(cubic,e),e,0)-S.Rational(421985,11409846), "incorrect cubic slope")
    eta = S.factor((ell.T*D*r)[0]/(ell.T*r)[0])
    cp = S.Poly((lam*S.eye(4)-A+t*D).det(method="domain-ge"),lam)
    require(cp.LC() == 1, "characteristic is not monic")
    a1,a2,a3,a4 = [S.factor(v) for v in cp.all_coeffs()[1:]]
    H2 = S.factor(a1*a2-a3)
    H3 = S.factor(a3*H2-a1*a1*a4)
    zero(a4.subs(t,1), "onset constant coefficient is nonzero")
    zero(eta-S.diff(a4,t).subs(t,1)/a3.subs(t,1), "crossing identity fails")
    zero((lam*S.eye(4)-A).det()/lam-(lam+7)*(lam**2+5*lam+2), "homogeneous complement wrong")
    certificates = [bernstein_orthant_sign(D[i,i], f"diffusion_{i+1}") for i in range(4)]
    certificates += [bernstein_orthant_sign(cubic,"positive_cubic"),
                     bernstein_orthant_sign(eta,"positive_crossing"),
                     bernstein_orthant_sign(-(ell.T*r)[0],"negative_pairing")]
    for name, expression in (("a1",a1),("a2",a2),("a3",a3),
                             ("a4_div_t_minus_1",S.cancel(a4/(t-1))),
                             ("H2",H2),("H3",H3)):
        certificates.append(bernstein_orthant_sign(expression.subs(t,1+s),name))
    record("near_threshold_reaction_derivation_and_independent_interval_signs",
           interval="0<epsilon<=1/1000, t>=1", cubic=str(cubic),
           eta=str(eta), certificates=certificates)


def finite_normal_forms():
    L = S.symbols("L", positive=True)
    rows = []
    for m in (3,4,6,9):
        A,c,B = field(m)
        nu = m-2
        K = lambda i: S.Integer(91*m-181-i)
        r = S.Matrix([1]+[-K(i)/(63*nu) for i in range(2,m)]+[-S.Rational(2,9),S.Rational(5,14)])
        D = S.diag(S.Rational(23,63),*[1/K(i) for i in range(2,m)],S.Rational(1,7),S.Rational(16,45))
        ell = S.Matrix([-S.Rational(266,815)]+[S.Rational(78260*nu,163)/K(i-1) for i in range(2,m)]+[S.Rational(18368,7335),1])
        zero((A-D)*r,"unit critical vector fails")
        zero(ell.T*(A-D),"unit left vector fails")
        w0,w2 = corrections(A,c,B,r,D)
        N = S.factor((ell.T*(B(r,w0)+B(r,w2)/2))[0])
        h = sum(1/K(i) for i in range(1,m-1))
        Q = 589180301*m**3-3500015940*m**2+6930529579*m-4574434500
        PR = 68605040480814208768*m**4-550882186169626030957*m**3+1658612632937449670852*m**2-2219226476204103501323*m+1113379274975809565700
        PC = 652054120726848*m**4-5151971981328467*m**3+15265080924982572*m**2-20102347725659113*m+9927281930180400
        target = S.Rational(PR,286118780220*(8*m-17)*Q)-S.Rational(215*PC,11645046*(8*m-17)*Q)*h
        zero(N-target,"unit numerator disagrees with printed closed form")
        require(N>0 and (ell.T*r)[0]<0,"unit cubic signs fail")
        H = S.diag(1,*[K(i)/(L*K(i-1)) for i in range(2,m)],1,1)
        q = H.inv()*c
        scaledw0,_ = corrections(A,c,B,r,D,q)
        rho = A.nullspace()[0]
        tau = S.factor(-((q.T*w0)[0])/((q.T*rho)[0]))
        zero(scaledw0-w0-tau*rho,"scaled gauge relation fails")
        scaledN = S.factor((ell.T*(B(r,scaledw0)+B(r,w2)/2))[0])
        den = S.factor((ell.T*H.inv()*r)[0])
        zero(den+S.Rational(485873,924210)+S.Rational(11180,1467)*L*nu,"scaled pairing fails")
        # Test the entire symbolic L gauge, then assess the exact algebraic endpoints.
        endpoints = (1/S.sqrt(3) if m==3 else S.sqrt(5)/(2*S.sqrt(nu)), S.Rational(90*nu,90*nu+1))
        endpoint_rows=[]
        for value in endpoints:
            num_value = S.simplify(scaledN.subs(L,value))
            cub_value = S.simplify((scaledN/den).subs(L,value))
            require(bool(num_value>S.Rational(1,200)),"scaled numerator margin fails")
            require(bool(cub_value<0),"scaled endpoint cubic not negative")
            endpoint_rows.append(dict(L=str(value),cubic=str(cub_value),numerator=str(num_value)))
        rows.append(dict(m=m,unit_cubic=str(S.factor(N/(ell.T*r)[0])),endpoints=endpoint_rows))
    record("finite_exact_reaction_contractions_and_symbolic_L_gauges",dimensions=rows,
           scope="Finite regression checks, not the proof of the all-dimensional claim")


def modulus_certificates():
    x,y,z,sd,U,Ap = S.symbols("x y z sd U A", nonnegative=True)
    la = x+S.I*y
    damp=1+sd
    g1=la+2+S.Rational(23,63)*damp
    gm=la+5+S.Rational(1,7)*damp
    gz=la+4+S.Rational(16,45)*damp
    F=g1*gm*gz-4*g1-4*gm+gz
    G=gz*(4*g1+gm)-36
    F0=la**3+11*la**2+31*la+16
    P=la**4+12*la**3+42*la**2+47*la+16
    R=5*la**2+33*la+16
    modulus=lambda q: S.expand(q*S.conjugate(q)).subs(y**2,z)
    certificates=(("E35",modulus((1+la)*P)-modulus(R),(x,z),35),
                  ("E77",(S.Rational(91,90)**2+z)*modulus(F)-modulus(G),(x,z,sd),77),
                  ("E84",S.Rational(91,90)**2*(1+Ap*x+z/3)*modulus(F)-modulus(G),(x,z,sd),84),
                  ("E22",(1+(U+S.Rational(1,4))*x+S.Rational(5,4)*z)*modulus(F0)-modulus(R),(x,z),22))
    summaries=[]
    for name,expression,variables,count in certificates:
        poly=S.Poly(S.expand(expression),*variables)
        require(len(poly.terms())==count,f"{name} term count mismatch")
        require(poly.coeff_monomial(1)==0,f"{name} nonzero constant")
        for monomial,coefficient in poly.terms():
            coeffpoly=S.Poly(coefficient,Ap,U)
            require(all(v>=0 for v in coeffpoly.coeffs()),f"{name} negative coefficient")
        # Strictly positive pure-axis coefficients force origin-only equality.
        witnesses=[]
        for index in range(len(variables)):
            valid=[]
            for monomial,coefficient in poly.terms():
                if monomial[index]>0 and sum(monomial)==monomial[index]:
                    if coefficient.subs({Ap:0,U:0})>0:
                        valid.append((monomial,coefficient))
            require(bool(valid),f"{name} missing strict axis witness")
            witnesses.append(dict(variable=str(variables[index]),power=valid[-1][0][index],coefficient=str(valid[-1][1])))
        summaries.append(dict(name=name,terms=count,equality_witnesses=witnesses))
    record("independent_all_dimensional_modulus_expansions",certificates=summaries)


def generic_gauge_and_margin():
    nu,L,h,v,y=S.symbols("nu L h v y",positive=True)
    m=nu+2
    K=lambda i:91*m-181-i
    sigma=1/(126*nu)
    w02=(1008*m**2-20459*m+37138)/(31752*nu*(8*m-17))
    w0m=-S.Rational(1,81)
    w0z=(16861*m-34044)/(7938*(8*m-17))
    # Reindex the formal harmonic sum from K1,...,K(m-2) to K2,...,K(m-1).
    shifted_h=h-1/K(1)+1/K(m-1)
    # Sum (i-2)/K_i = K2 sum(1/K_i)-nu; no unevaluated large sum remains.
    mass_w0=4*L*(nu*w02-sigma*nu*(nu-1)/2+w02*shifted_h-sigma*(K(2)*shifted_h-nu))+2*w0m+w0z
    mass_rho=1-8*L*(nu+shifted_h)
    actual_tau=S.factor(-mass_w0/mass_rho)
    top=1494249120*h*L*nu**2-69786990*h*L*nu+108738630*L*nu**2+1214388*L*nu-8521*L-125249670*nu**2+1031940*nu
    bt=32760*h*L*nu+32760*L*nu**2+4*L-4095*nu
    target_tau=-top/(15876*(8*nu-1)*bt)
    zero(actual_tau-target_tau,"all-dimensional gauge bridge wrong")
    dH=-4225*L*nu**2*(182448*L*nu+1008*L-7513)/(2*bt**2)
    dL=-65*nu*(-61531470*h*nu+125249670*nu**2+1031940*nu-7513)/(252*bt**2)
    zero(S.diff(actual_tau,h)-dH,"harmonic derivative wrong")
    zero(S.diff(actual_tau,L)-dL,"L derivative wrong")
    Q=589180301*m**3-3500015940*m**2+6930529579*m-4574434500
    PR=68605040480814208768*m**4-550882186169626030957*m**3+1658612632937449670852*m**2-2219226476204103501323*m+1113379274975809565700
    PC=652054120726848*m**4-5151971981328467*m**3+15265080924982572*m**2-20102347725659113*m+9927281930180400
    R=PR/(286118780220*(8*m-17)*Q)
    C=-215*PC/(11645046*(8*m-17)*Q)
    margin=S.factor(R+C*nu/(90*nu+1)-S.Rational(1,100))
    pnum,pden=S.fraction(margin)
    shifted_coeffs=[]
    for label,polynomial in (("reference_margin_num",pnum),("reference_margin_den",pden),("minus_C_num",PC)):
        coeffs=S.Poly(S.expand(polynomial.subs(nu,v+1)),v).all_coeffs()
        require(all(c>0 for c in coeffs),f"{label} shifted signs wrong")
        shifted_coeffs.append(dict(name=label,coefficients=[str(c) for c in coeffs]))
    pt=-1040195520*nu**3+756272790*nu**2*y-507201030*nu**2-21412755*nu*y-935658*nu+58481
    dt=-32760*nu**2+4095*nu*y-360*nu-4
    zero(actual_tau.subs({h:S.Rational(1,91),L:1/y})-S.Rational(1,20)+pt/(79380*(8*nu-1)*dt),"endpoint gauge bridge wrong")
    upper=-S.Rational(189709065,2)*nu**3-507201030*nu**2-935658*nu+58481
    require(pt.subs({nu:1,y:S.Rational(7,4)})<0,"nu=1 endpoint bound wrong")
    require(upper.subs(nu,2)<0,"nu>=2 upper bound wrong")
    require(all(c<0 for c in S.Poly(S.diff(upper,nu),nu).all_coeffs()),"upper bound monotonicity wrong")
    record("generic_conservation_gauge_and_cubic_margin_bridges",formal_harmonic_domain="1/91<=h<1/90, h<=nu/(90nu+1)",
           broader_cubic_domain="integer nu>=1, L>=1/sqrt(3nu)",shifted_coefficients=shifted_coeffs)


near_threshold()
finite_normal_forms()
modulus_certificates()
generic_gauge_and_margin()
results["finished_utc"]=datetime.now(timezone.utc).isoformat()
results["status"]="PASS"
Path(__file__).with_name("INDEPENDENT_RESULTS.json").write_text(json.dumps(results,indent=2)+"\n")
print("INDEPENDENT_PDE_CHECKS_PASS",flush=True)

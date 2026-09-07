#!/usr/bin/env python3
"""Independent referee calculations, with no imports from the submitted code.

Network construction uses the published reactions. Symbolic identities verify
the all-parameter modulus/sign arguments; selected rational dimensions test
the reaction-to-cubic chain and do not purport to prove an all-dimension result.
"""
from pathlib import Path
import json
import math
import time
import sympy as S

OUT = Path(__file__).resolve().parent
R = S.Rational
results = {"sympy": S.__version__, "checks": [], "dimensions": []}


def check(condition, label):
    if not condition:
        raise RuntimeError(label)
    results["checks"].append(label)


def zero(expr):
    if isinstance(expr, S.MatrixBase):
        return all(S.cancel(e) == 0 for e in expr)
    return S.cancel(expr) == 0


def network(m):
    n = m + 1
    x = S.symbols("x1:" + str(n + 1))
    reactions = []

    def add(src, dst):
        y = S.zeros(n, 1)
        yp = S.zeros(n, 1)
        for i, count in src.items():
            y[i] = count
        for i, count in dst.items():
            yp[i] = count
        reactions.append((y, yp))

    add({}, {0: 1})
    for i in range(1, m - 2):
        add({0: 1, i: 1}, {0: 1, i + 1: 1})
    add({0: 1, m - 2: 1}, {m - 1: 2})
    add({m - 1: 2}, {1: 1})
    add({m: 2}, {0: 1, m - 1: 1})
    add({0: 1, m - 1: 1}, {m: 2})
    f = S.zeros(n, 1)
    for y, yp in reactions:
        monomial = S.prod(x[j] ** int(y[j]) for j in range(n))
        f += (yp - y) * monomial
    one = dict.fromkeys(x, 1)
    A = f.jacobian(x).subs(one)
    hessians = [S.hessian(fi, x) for fi in f]

    def B(u, v):
        return S.Matrix([(u.T * h * v)[0] for h in hessians])

    c = S.Matrix([0] + [4] * (m - 2) + [2, 1])
    rho = S.Matrix([2] + [-2] * (m - 2) + [0, 1])
    check(zero(f.subs(one)), f"m={m}: unit reaction flux balances")
    check(zero((c.T * f)[0]), f"m={m}: nonlinear mass conservation")
    check(zero(A * rho), f"m={m}: conservation kernel")
    return A, B, c, rho


def profile(m):
    K = lambda i: 91 * m - 181 - i
    r = S.Matrix([1] + [-R(K(i), 63 * (m - 2)) for i in range(2, m)] + [-R(2, 9), R(5, 14)])
    ell = S.Matrix([-R(266, 815)] + [R(78260 * (m - 2), 163 * (K(i) + 1)) for i in range(2, m)] + [R(18368, 7335), 1])
    d = [R(23, 63)] + [R(1, K(i)) for i in range(2, m)] + [R(1, 7), R(16, 45)]
    return K, r, ell, S.diag(*d)


def gauge_solve(A, rhs, g):
    matrix = A.copy()
    forcing = rhs.copy()
    matrix[-1, :] = g.T
    forcing[-1] = 0
    solution = matrix.inv(method="DM") * forcing
    solution = solution.applyfunc(S.cancel)
    check(zero(A * solution - rhs) and zero(g.dot(solution)), "compatible homogeneous correction")
    return solution


def reference_numerator(m, harmonic):
    q = 589180301*m**3 - 3500015940*m**2 + 6930529579*m - 4574434500
    pr = 68605040480814208768*m**4 - 550882186169626030957*m**3 + 1658612632937449670852*m**2 - 2219226476204103501323*m + 1113379274975809565700
    pc = 652054120726848*m**4 - 5151971981328467*m**3 + 15265080924982572*m**2 - 20102347725659113*m + 9927281930180400
    return pr / (S.Integer(286118780220)*(8*m-17)*q) - 215*pc*harmonic/(S.Integer(11645046)*(8*m-17)*q)


def reaction_cubics():
    for m in [3, 4, 5, 7, 12, 25]:
        A, B, c, rho = network(m)
        K, r, ell, D = profile(m)
        harmonic = sum((R(1, K(j)) for j in range(1, m-1)), S.Integer(0))
        check(zero((A-D)*r) and zero((A-D).T*ell), f"m={m}: critical vectors")
        ip = ell.dot(r)
        cross = ell.dot(D*r)
        check(ip < 0 and cross < 0, f"m={m}: algebraic simplicity and crossing")
        check(zero(ip + (7043400*m-13600927-7043400*harmonic)/S.Integer(924210)), f"m={m}: exact projection denominator")
        rhs = -B(r, r)/4
        w0 = gauge_solve(A, rhs, c)
        w2 = (A-4*D).inv(method="DM")*rhs
        check(zero((A-4*D)*w2-rhs), f"m={m}: second harmonic solve")
        numerator = ell.dot(B(r,w0)+B(r,w2)/2)
        check(zero(numerator-reference_numerator(m,harmonic)), f"m={m}: independently reconstructed reference numerator")
        check(numerator > R(1,100), f"m={m}: reference positive margin")
        sigma = R(1,126*(m-2))
        for i in range(2,m):
            Ti = R(S.prod(K(j) for j in range(i-3,i+1)), S.prod(K(j) for j in range(-1,3)))
            check(zero(w2[i-1]-(Ti*(w2[1]+sigma*K(2)/3)-sigma*K(i)/3)), f"m={m},i={i}: second harmonic telescoping recurrence")
        slopes = ell.dot(B(r,rho))
        check(zero(slopes + 4*(1760850*harmonic-10253)/S.Integer(462105)), f"m={m}: kernel gauge slope")
        nu = m-2
        upper = R(90*nu,90*nu+1)
        # The two rational points lie in the certified interval. Irrational
        # lower endpoints are addressed by all-parameter inequalities below.
        low_rational = R(3,5) if nu == 1 else R(math.isqrt(1250000//nu)+1,1000)
        Ls = [low_rational, upper]
        for L in Ls:
            check((3*nu*L**2 >= 1 if nu == 1 else 4*nu*L**2 >= 5) and L<=upper, f"m={m},L={L}: test point is certified")
            H = S.diag(1,*[R(K(i),K(i-1))/L for i in range(2,m)],1,1)
            g = H.inv()*c
            direct_w0 = gauge_solve(A,rhs,g)
            tau = -g.dot(w0)/g.dot(rho)
            check(zero(direct_w0-w0-tau*rho), f"m={m},L={L}: physical mass gauge")
            tilde = H.inv()*ell
            check(zero((H*(A-D)).T*tilde), f"m={m},L={L}: scaled left vector")
            ip_scaled = tilde.dot(r)
            check(zero(ip_scaled+R(485873,924210)+R(11180,1467)*L*nu), f"m={m},L={L}: scaled denominator")
            Nscaled = tilde.dot(H*(B(r,direct_w0)+B(r,w2)/2))
            check(zero(Nscaled-numerator-tau*slopes), f"m={m},L={L}: dynamic scaled cubic identity")
            check(Nscaled > R(1,200) and ip_scaled < 0, f"m={m},L={L}: scaled supercritical sign")
        results["dimensions"].append({"m":m,"cubic":str(S.cancel(numerator/ip)),"eta":str(S.cancel(cross/ip)),"gauge_points":[str(x) for x in Ls]})


def modulus_checks():
    x,y,z,s,alpha,U = S.symbols("x y z s alpha U", real=True)
    lam=x+S.I*y
    t=1+s
    g1=lam+2+R(23,63)*t
    gm=lam+5+t/7
    gz=lam+4+R(16,45)*t
    F=g1*gm*gz-4*g1-4*gm+gz
    G=gz*(4*g1+gm)-36
    F0=lam**3+11*lam**2+31*lam+16
    R0=5*lam**2+33*lam+16
    P=lam**4+12*lam**3+42*lam**2+47*lam+16

    def modulus(e):
        e=S.Poly(S.expand(e*S.conjugate(e)),y)
        check(all(k[0]%2==0 for k in e.monoms()),"modulus has even imaginary powers")
        return S.expand(sum(coeff*z**(power[0]//2) for power,coeff in e.terms()))

    cases = [
        (35, ((1+x)**2+z)*modulus(P)-modulus(R0), (x,z), None),
        (77, (R(91,90)**2+z)*modulus(F)-modulus(G), (x,z,s), None),
        (84, R(91,90)**2*(1+alpha*x+z/3)*modulus(F)-modulus(G), (x,z,s), alpha),
        (22, (1+(U+R(1,4))*x+R(5,4)*z)*modulus(F0)-modulus(R0), (x,z), U),
    ]
    results["modulus_certificates"] = []
    for count,expr,variables,parameter in cases:
        polynomial=S.Poly(expr,*variables)
        check(len(polynomial.terms()) == count, f"E{count}: independent support count")
        check(polynomial.coeff_monomial((0,)*len(variables)) == 0,f"E{count}: equality at origin")
        for coefficient in polynomial.coeffs():
            values=S.Poly(coefficient,parameter).all_coeffs() if parameter else [coefficient]
            check(all(v>=0 for v in values) and any(v>0 for v in values),f"E{count}: coefficient positivity")
        # Each positive coordinate axis contains a strictly positive monomial.
        for index in range(len(variables)):
            witnesses=[]
            for powers,coefficient in polynomial.terms():
                if powers[index]>0 and sum(powers)==powers[index]:
                    at_boundary=coefficient.subs(parameter,0 if parameter==U else 1) if parameter else coefficient
                    if at_boundary>0:
                        witnesses.append(list(powers))
            check(bool(witnesses),f"E{count}: strictness on coordinate axis {index}")
        results["modulus_certificates"].append({"name":f"E{count}","terms":count,"strict_zero_set":"origin"})


def general_scalar_checks():
    m,u,nu,v,L,h=S.symbols("m u nu v L h", real=True)
    q=589180301*m**3-3500015940*m**2+6930529579*m-4574434500
    N=reference_numerator(m,h)
    numerator,denominator=S.fraction(S.cancel(N.subs(h,(m-2)/(90*m-179))-R(1,100)))
    for label,p in [("Q",q),("Nref-1/100 numerator",numerator),("Nref-1/100 denominator",denominator)]:
        coeffs=S.Poly(S.expand(p.subs(m,u+3)),u).all_coeffs()
        check(all(x>0 for x in coeffs),f"all m>=3: {label} shifted coefficients positive")
    At=1494249120*h*L*nu**2-69786990*h*L*nu+108738630*L*nu**2+1214388*L*nu-8521*L-125249670*nu**2+1031940*nu
    Bt=32760*h*L*nu+32760*L*nu**2+4*L-4095*nu
    tau=-At/(15876*(8*nu-1)*Bt)
    dh=-4225*L*nu**2*(182448*L*nu+1008*L-7513)/(2*Bt**2)
    dL=-65*nu*(-61531470*h*nu+125249670*nu**2+1031940*nu-7513)/(252*Bt**2)
    check(zero(S.diff(tau,h)-dh),"all-parameter gauge derivative in harmonic sum")
    check(zero(S.diff(tau,L)-dL),"all-parameter gauge derivative in L")
    y=S.symbols("y",positive=True)
    Pt=-1040195520*nu**3+756272790*nu**2*y-507201030*nu**2-21412755*nu*y-935658*nu+58481
    Dt=-32760*nu**2+4095*nu*y-360*nu-4
    check(zero(tau.subs({h:R(1,91),L:1/y})-R(1,20)+Pt/(79380*(8*nu-1)*Dt)),"gauge endpoint clearing identity")
    check(Pt.subs({nu:1,y:R(7,4)})==-R(1049074663,4),"exceptional endpoint rational upper bound")
    upper=-R(189709065,2)*nu**3-507201030*nu**2-935658*nu+58481
    # Dropping -21412755*nu*y and using y<=5nu/4 gives this upper bound.
    check(zero((Pt+21412755*nu*y).subs(y,5*nu/4)-upper),"generic endpoint polynomial upper bound")
    check(upper.subs(nu,2)==-2789453215 and all(c<0 for c in S.Poly(S.diff(upper,nu),nu).all_coeffs()),"generic endpoint upper bound negative")
    # Harmonic bound S_m in (-1/10,0) is global and does not require samples.
    Sm=-4*(1760850*h-10253)/S.Integer(462105)
    check(Sm.subs(h,R(1,91))<0 and Sm.subs(h,R(1,90))>-R(1,10),"all-dimensional gauge slope bounds")


def generic_recurrence_checks():
    m,i=S.symbols("m i",integer=True)
    K=lambda j:91*m-181-j
    ri=lambda j:-K(j)/(63*(m-2))
    r1,rm,rz=1,-R(2,9),R(5,14)
    w1=(182448*m-373417)/(31752*(8*m-17))
    wbase=(1008*m**2-20459*m+37138)/(31752*(m-2)*(8*m-17))
    wi=lambda j:wbase-(j-2)/(126*(m-2))
    wm,wz=-R(1,81),(16861*m-34044)/(7938*(8*m-17))
    b1=-2*r1*ri(m-1)+2*rz**2-2*r1*rm
    b2=-2*r1*ri(2)+2*rm**2
    bm=4*r1*ri(m-1)-4*rm**2+2*rz**2-2*r1*rm
    bz=-4*rz**2+4*r1*rm
    residuals=[-2*w1-wi(m-1)-wm+2*wz+b1/4,
               -w1-wi(2)+2*wm+b2/4,
               wi(i-1)-wi(i)+(2*r1*ri(i-1)-2*r1*ri(i))/4,
               w1+2*wi(m-1)-5*wm+2*wz+bm/4,
               2*w1+2*wm-4*wz+bz/4]
    check(all(zero(x) for x in residuals),"all-dimensional homogeneous correction row identities")
    check(zero(4*((m-2)*wbase-(m-3)*(m-2)/(252*(m-2)))+2*wm+wz),"all-dimensional homogeneous correction mass gauge")
    W=S.symbols("W")
    sigma=1/(126*(m-2))
    Ti=lambda j:S.prod(K(k) for k in [j-3,j-2,j-1,j])/S.prod(K(k) for k in [-1,0,1,2])
    vi=lambda j:Ti(j)*(W+sigma*K(2)/3)-sigma*K(j)/3
    check(zero(vi(2)-W),"generic recurrence has correct initial value")
    check(zero(vi(i-1)-(1+4/K(i))*vi(i)-sigma),"all-dimensional second harmonic interior identity")
    terminal=S.cancel(Ti(m-1))
    matrix=S.Matrix([[-R(218,63),-terminal,-1,2],[-1,-(1+4/K(2)),2,0],
                     [1,2*terminal,-R(39,7),2],[2,0,2,-R(244,45)]])
    q=589180301*m**3-3500015940*m**2+6930529579*m-4574434500
    expected=64*q/(6615*(91*m-183)*(91*m-181)*(91*m-180))
    check(zero(matrix.det(method="domain-ge")-expected),"all-dimensional second harmonic boundary determinant")


if __name__ == "__main__":
    started=time.time()
    modulus_checks()
    general_scalar_checks()
    generic_recurrence_checks()
    reaction_cubics()
    results["elapsed_seconds"]=round(time.time()-started,3)
    results["check_count"]=len(results["checks"])
    results["status"]="PASS"
    (OUT/"INDEPENDENT_NONLINEAR_RESULTS.json").write_text(json.dumps(results,indent=2)+"\n")
    print(f"PASS: {results['check_count']} exact checks in {results['elapsed_seconds']} seconds")

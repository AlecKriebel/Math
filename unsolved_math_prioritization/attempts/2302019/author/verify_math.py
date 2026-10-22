#!/usr/bin/env python3
"""Deterministic, standard-library formula checks; not a proof oracle."""
import cmath
from fractions import Fraction as Q
import json
import math
from pathlib import Path
import sys


def integrated_sinc(a, z):
    """Integral of sinc(a*t)^2 from 0 to z, by its entire power series."""
    term = complex(z)
    result = term
    for n in range(100):
        term *= -4*a*a*z*z*(2*n+1)/((2*n+4)*(2*n+3)**2)
        result += term
    return result


def simpson(func, left, right, steps=2048):
    h = (right-left)/steps
    result = func(left)+func(right)
    for j in range(1, steps):
        result += (4 if j % 2 else 2)*func(left+j*h)
    return result*h/3


def run():
    exact = 0
    smoke = 0

    def exact_check(condition):
        nonlocal exact
        assert condition
        exact += 1

    def smoke_check(condition):
        nonlocal smoke
        assert condition
        smoke += 1

    # Exact Taylor coefficients: convolution versus (1-cos(2z))/(2z^2).
    for n in range(19):
        convolution = sum((Q((-1)**n,
                             math.factorial(2*j+1)*math.factorial(2*(n-j)+1))
                           for j in range(n+1)), Q(0))
        closed = Q((-1)**n*2**(2*n+1), math.factorial(2*n+2))
        exact_check(convolution == closed)
        primitive = closed / (2*n+1)
        exact_check(primitive*(2*n+1) == convolution)
        if n < 18:
            following = Q((-1)**(n+1)*2**(2*n+3),
                          math.factorial(2*n+4)*(2*n+3))
            exact_check(following/primitive ==
                        Q(-4*(2*n+1), (2*n+4)*(2*n+3)**2))

    exact_check(Q(1)-Q(1,4)**2/6 == Q(95,96))
    exact_check(Q(1,8)*Q(95,96)**2 == Q(9025,73728))

    examples = []
    for ratio in (Q(1,3), Q(1,2), Q(2,3)):
        for Bq in (Q(1,2), Q(1), Q(3)):
            for Kq in (Q(1,2), Q(1), Q(2)):
                Aq = ratio*Bq
                Lq = (Bq-Aq)/(Kq*Bq)
                deltaq = min(Aq, Bq-Aq)
                exact_check(Lq > 0)
                exact_check(Aq+Kq*Bq*Lq == Bq)
                exact_check(Aq+Kq*Bq*Lq/2 == (Aq+Bq)/2)
                exact_check(0 < deltaq <= Aq)
                exact_check(Aq+deltaq <= Bq)
                for j in range(17):
                    tq = Lq*j/32
                    exact_check(Aq <= Aq+Kq*Bq*tq <= (Aq+Bq)/2)
                A,B,K,L,delta = map(float,(Aq,Bq,Kq,Lq,deltaq))
                a=K/4
                def witness(z):
                    return A+(2*a*delta/math.pi)*integrated_sinc(a,z)
                gap = witness(1/K).real-A
                smoke_check(gap > float(Q(9025,73728))*delta)
                smoke_check(abs(witness(0)-A) < 1e-12)
                for t in (-8,-2,-0.25,0.25,2,8):
                    value=witness(t/K)
                    smoke_check(abs(value.imag) < 1e-12)
                    smoke_check((A-delta-1e-12 <= value.real <= A+1e-12)
                                if t<0 else
                                (A-1e-12 <= value.real <= A+delta+1e-12))
                for xs in (-2,-0.25,0,0.5,3):
                    for ys in (0.1,0.75,2):
                        x,y=xs/K,ys/K
                        theta=math.atan2(y,x)
                        step=math.exp(K*y+(theta/math.pi)*math.log(A)
                                      +(1-theta/math.pi)*math.log(B))
                        integrand=lambda t: (y/((t-x)**2+y*y)
                                             *math.log(B/(A+K*B*t))/math.pi)
                        D=simpson(integrand,0,L)
                        d=L*y*math.log(2*B/(A+B))/(2*math.pi*((abs(x)+L/2)**2+y*y))
                        ramp=step*math.exp(-D)
                        smoke_check(D+1e-10 >= d > 0)
                        smoke_check(0 < ramp < step)
                        smoke_check(A*math.exp(K*y) <= ramp+1e-10)
                        smoke_check(abs(witness(complex(x,y))) <= ramp+1e-10)
                        smoke_check(abs(witness(complex(x,-y))-
                                        witness(complex(x,y)).conjugate()) < 1e-10)
                if Bq==1 and Kq==1:
                    examples.append({"A":str(Aq),"B":str(Bq),"K":str(Kq),
                                     "witness_gap_at_1_over_K":format(gap,".10f"),
                                     "proved_rational_gap_lower_bound":str(Q(9025,73728)*deltaq)})

    # Exact common periods for sample rational frequencies; coefficients
    # need not be real and the proof in PROOFS.md covers irrational ones.
    for denominator in range(1,13):
        for numerator in range(-7,8):
            exact_check(Q(numerator,denominator)*math.factorial(12)
                        == int(Q(numerator,denominator)*math.factorial(12)))
    frequencies=[Q(1,2),Q(-2,3),Q(4,5)]
    coefficients=[1+2j,-0.5j,0.25-0.75j]
    period=60*math.pi
    def p(t):
        return sum(c*cmath.exp(1j*float(lam)*t)
                   for c,lam in zip(coefficients,frequencies))
    for t in (-10,-1,0,0.2,3):
        smoke_check(abs(p(t+period)-p(t)) < 1e-11)
        smoke_check(abs(p(t-period)-p(t)) < 1e-11)

    return {"packet_id":"2302019-reconstruction-20261005-v1",
            "exact_rational_controls":exact,
            "floating_point_smoke_controls":smoke,
            "parameter_triples":27,
            "complex_upper_half_plane_points":405,
            "examples":examples,
            "scope":"Finite formula and example checks only; no certified quadrature, optimality proof, or full resolution."}


def main():
    if not __debug__:
        raise SystemExit("Run without Python optimization: assertions are required.")
    result=run()
    data=json.dumps(result,indent=2,sort_keys=True)+"\n"
    if sys.argv[1:]==["--emit"]:
        print(data,end="")
        return
    if sys.argv[1:]:
        raise SystemExit("Usage: python3 verify_math.py [--emit]")
    expected=Path(__file__).with_name("EXPECTED_CHECKS.json").read_text()
    if data != expected:
        raise SystemExit("FAIL: mathematical replay output differs from EXPECTED_CHECKS.json")
    print(data,end="")


if __name__=="__main__":
    main()

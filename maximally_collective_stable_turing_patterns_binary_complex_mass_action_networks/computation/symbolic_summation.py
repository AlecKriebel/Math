#!/usr/bin/env python3
"""Closed all-m formulas for the rational seed's adjoint contractions."""
from __future__ import annotations
import sympy as sp


def H_exact(m: int) -> sp.Rational:
    if m < 3:
        raise ValueError
    return sp.Add(*(sp.Rational(1, 227*m-451-3*j) for j in range(2,m-1)), evaluate=True)


def Qpoly(m):
    return (sp.Integer(1910521667596003)*m**3
            -sp.Integer(11322779437089660)*m**2
            +sp.Integer(22368031913707929)*m
            -sp.Integer(14729097938020928))


def ell_dot_r(m, H):
    return (-(sp.Integer(892802400)*m**2-sp.Integer(3400424303)*m+sp.Integer(3217891606))
            /(sp.Integer(7377120)*(m-2))
            +sp.Rational(1860005,5123)*H)


def ell_dot_Dr(m, H):
    return (-(sp.Integer(99148487)*m-sp.Integer(186549574))
            /(sp.Integer(7377120)*(m-2))
            -sp.Rational(1860005,5123)*H)


def cubic_numerator(m, H):
    A=(sp.Integer(86392373709756938206702324880)*m**5
       -sp.Integer(878316832027584429913234554493)*m**4
       +sp.Integer(3570576759617470240582317330966)*m**3
       -sp.Integer(7255203323904441261456947317999)*m**2
       +sp.Integer(7368642295819384535817788489606)*m
       -sp.Integer(2992572008943165191299483794816))
    B=(sp.Integer(892292533383541579520)*m**4
       -sp.Integer(7159841249775619992477)*m**3
       +sp.Integer(21539344009097108736900)*m**2
       -sp.Integer(28792766432259158176231)*m
       +sp.Integer(14430205416389750108352))
    R=A/(sp.Integer(566562816000)*(m-2)*(8*m-17)*Qpoly(m))
    C=-sp.Integer(372001)*B/(sp.Integer(78689280)*(8*m-17)*Qpoly(m))
    return sp.factor(R+C*H)


def eta_closed(m: int):
    H=H_exact(m)
    return sp.factor(ell_dot_Dr(m,H)/ell_dot_r(m,H))


def cubic_closed(m: int):
    H=H_exact(m)
    return sp.factor(cubic_numerator(m,H)/ell_dot_r(m,H))


def lower_bound_cubic_numerator(m):
    G=(sp.Integer(16961968965064836030215580229120)*m**6
       -sp.Integer(204060992591161140189804029423632)*m**5
       +sp.Integer(1022744662082541440031646436769769)*m**4
       -sp.Integer(2733435957152538936565966048042046)*m**3
       +sp.Integer(4108750818252419615808760310850899)*m**2
       -sp.Integer(3293419603698721148657010487662254)*m
       +sp.Integer(1099794747471284681949805627086720))
    return G/(sp.Integer(566562816000)*(m-2)*(8*m-17)*(224*m-445)*Qpoly(m))


def upper_bound_ell_dot_r(m):
    G=(sp.Integer(199987737600)*m**3-sp.Integer(1161670519072)*m**2
       +sp.Integer(2247388570579)*m-sp.Integer(1448032207870))
    return -G/(sp.Integer(7377120)*(m-2)*(224*m-445))


if __name__ == "__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument('m',type=int)
    a=p.parse_args()
    H=H_exact(a.m)
    print('H =',H)
    print('ell.r =',ell_dot_r(a.m,H))
    print('ell.Dr =',ell_dot_Dr(a.m,H))
    print('eta =',eta_closed(a.m))
    print('N =',cubic_numerator(a.m,H))
    print('c =',cubic_closed(a.m))
    print('N lower bound =',lower_bound_cubic_numerator(a.m))
    print('ell.r upper bound =',upper_bound_ell_dot_r(a.m))

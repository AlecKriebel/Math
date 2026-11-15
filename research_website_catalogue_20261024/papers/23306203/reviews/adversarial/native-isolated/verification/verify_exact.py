#!/usr/bin/env python3
"""Finite exact controls; standard library only; no writes or network access."""
from collections import Counter
from fractions import Fraction as F
from math import gcd
import json

CHECKS = 0

def require(condition, label):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise ArithmeticError(label)

def divisor(n, tau, focus):
    step = F(tau, n)
    zeros, poles = Counter(), Counter()
    for j in range(n):
        poles.update([(-j*step)%1, (F(1,2)-j*step)%1])
        zeros.update([(-F(focus,4)+step/2-j*step)%1,
                      (-F(focus,4)-step/2-j*step)%1])
    return zeros, poles

def classification_checks():
    counts = {"odd_nonconstant":0, "n_2_mod_4_constant":0,
              "n_0_mod_4_nonconstant":0}
    for n in range(3,102):
        for tau in range(1,(n+1)//2):
            if gcd(tau,n) != 1:
                continue
            key = ("odd_nonconstant" if n%2 else
                   "n_2_mod_4_constant" if n%4==2 else
                   "n_0_mod_4_nonconstant")
            for focus in (1,-1):
                zeros,poles = divisor(n,tau,focus)
                require(sum(zeros.values()) == sum(poles.values()) == 2*n,
                        "complete zero and pole degree")
                require(len(zeros)==n and set(zeros.values())=={2},
                        "coincident double zero coset")
                if n%2:
                    require(len(poles)==2*n and set(poles.values())=={1},
                            "odd two disjoint simple pole cosets")
                    require(not (zeros.keys() & poles.keys()), "odd no cancellation")
                elif n%4==2:
                    require(zeros==poles, "complete double divisor cancellation")
                else:
                    require(len(poles)==n and set(poles.values())=={2},
                            "even coincident double pole coset")
                    require(not (zeros.keys() & poles.keys()), "four class no cancellation")
                for r in (2,3,4):
                    orders = [r*(zeros[x]-poles[x])
                              for x in zeros.keys() | poles.keys()]
                    require(all(v==0 for v in orders)==(n%4==2),
                            "repetition preserves divisor criterion")
            counts[key] += 1
    return counts

RHO2 = F(8,15)

def multiply(x,y):
    return (x[0]*y[0]+RHO2*x[1]*y[1], x[0]*y[1]+x[1]*y[0])

def product(factors):
    value = (F(1),F(0))
    for factor in factors:
        value = multiply(value,factor)
    return value

def triangle_checks():
    a2,b2,c2 = F(15),F(7),F(8)
    A2,B2 = F(135,16),F(7,16)
    require(a2-b2==A2-B2==c2, "triangle confocality")
    require(0<B2<b2 and 0<A2<a2, "strict nested nondegenerate caustic")
    require(a2>c2>0, "positive real focal factors")
    # X is x/a; y is the ordinary y coordinate.
    vertices = [(F(1),F(0)),(-F(3,4),F(7,4)),(-F(3,4),-F(7,4))]
    for X,y in vertices:
        require(X*X+y*y/b2==1, "vertex on outer ellipse")
    require(A2==a2*F(9,16), "vertical tangent x=-A")
    require(A2+a2*B2==a2, "sloping tangents x +/- ay=a")
    require(vertices[1][0]+vertices[1][1]==1 and
            vertices[2][0]-vertices[2][1]==1, "sloping side incidence")
    require(a2/16+F(1,16)==1, "off-axis inward ray is unit")
    require(F(1,4)==5*F(1,20) and -F(1,4)-1==-5*F(1,4),
            "off-axis reflected rays sum to inward normal multiple")
    require((-F(1,4),F(1,4))[0]+(-F(1,4),-F(1,4))[0]==-F(1,2),
            "axis reflected rays sum horizontally")
    plus = product([(F(1),-X) for X,_ in vertices])
    minus = product([(F(1),X) for X,_ in vertices])
    require(plus==(F(1,2),F(1,5)), "normalized product of T")
    require(minus==(F(1,2),-F(1,5)), "normalized product of -T")
    p2,m2 = multiply(plus,plus),multiply(minus,minus)
    difference = (p2[0]-m2[0],p2[1]-m2[1])
    require(difference==(F(0),F(2,5)), "normalized doubled product difference")
    coefficient = a2**3*difference[1]
    require(coefficient==1350 and coefficient>0, "positive actual difference 1350 rho")
    require(coefficient**2*RHO2==F(180)**2*30, "positive difference 180 sqrt(30)")
    return {"least_period":3, "listed_return_length":6,
            "primitive_products":"15 sqrt(15)/2 +/- 3 sqrt(8)",
            "doubled_six_event_difference":"180 sqrt(30)"}

def four_period_checks():
    a2,b2 = F(4),F(1)
    c2,S = a2-b2,a2+b2
    A2,B2 = a2**2/S,b2**2/S
    require(A2-B2==c2, "four period confocality")
    require(0<A2<a2 and 0<B2<b2, "four period strict nesting")
    require(A2/a2+B2/b2==1, "rectangle boundary and diamond tangency")
    require(A2/a2**2==B2/b2**2, "rectangle normal bisects perpendicular rays")
    rectangle,diamond = (a2-(c2/a2)*A2)**2,a2*b2
    require(rectangle==4*a2**2*b2**2/S**2, "rectangle focal product")
    require(S**2-4*a2*b2==c2**2>0, "distinct noncircular products")
    require(diamond==4 and rectangle==F(64,25) and diamond!=rectangle,
            "exact physical four period nonconstancy")
    return {"a_squared":"4", "b_squared":"1",
            "caustic_A_squared":"16/5", "caustic_B_squared":"1/5",
            "diamond_product":"4", "rectangle_product":"64/25"}

def main():
    counts = classification_checks()
    triangle,four = triangle_checks(),four_period_checks()
    print(json.dumps({
        "status":"PASS", "arithmetic":"exact fractions and Q(sqrt(8/15))",
        "least_period_range":[3,101], "both_foci_checked":True,
        "primitive_rotation_counts":counts, "checks":CHECKS,
        "repetition_counts_checked":[2,3,4],
        "doubled_triangle":triangle, "four_period_control":four,
        "limit":"Finite controls support the written all-period proof. The Jacobi analytic identities and geometric parametrization are proof inputs, not conclusions of this checker."
    },indent=2))

if __name__ == "__main__":
    main()

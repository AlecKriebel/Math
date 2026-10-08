#!/usr/bin/env python3
"""Finite exact algebra checks, not a stochastic proof or a simulation."""
from fractions import Fraction as Q
from math import comb
import json
import os


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def sub(x, y):
    return (x[0] - y[0], x[1] - y[1])


def mul(x, y):
    return (x[0]*y[0] - x[1]*y[1], x[0]*y[1] + x[1]*y[0])


def scale(a, x):
    return (a*x[0], a*x[1])


def dot(x, y):
    return x[0]*y[0] + x[1]*y[1]


def norm2(x):
    return dot(x, x)


def inverse(x):
    n = norm2(x)
    if n == 0:
        raise ValueError('complex inverse requires a nonzero point')
    return (x[0]/n, -x[1]/n)


def circle_point(R, t):
    if R <= 0:
        raise ValueError('radius must be positive')
    return (R*(1-t*t)/(1+t*t), R*2*t/(1+t*t))


def boundary_coefficient(R, x, y, a):
    if R <= 0:
        raise ValueError('radius must be positive')
    if norm2(x) != R*R:
        raise ValueError('x must be on the reflecting circle')
    if norm2(y) < R*R:
        raise ValueError('y must be in the closed exterior')
    d2 = norm2(sub(x, y))
    if d2 == 0:
        raise ValueError('logarithmic formula excludes the diagonal')
    return dot(sub(x, y), x)/(R*d2) - a/R


def expect_rejection(call, message):
    try:
        call()
    except ValueError:
        return
    raise RuntimeError('guard did not reject: ' + message)


def in_two_hole_closure(z):
    return (norm2(z) <= 100 and norm2(z) >= 1
            and norm2(sub(z, (Q(4), Q(4)))) >= Q(1, 4))


def main():
    counts = {'boundary_identities': 0, 'inversion_identities': 0,
              'threshold_witnesses': 0, 'controlled_path_checks': 0,
              'even_power_integrals': 0, 'neumann_boundary_checks': 0,
              'guard_rejections': 0}
    for R in (Q(1,2), Q(1), Q(3,2), Q(2)):
        xs = [circle_point(R, Q(k,3)) for k in range(-6,7)]
        xs.append((-R,Q(0)))
        ys = [(R*Q(i,2), R*Q(j,2)) for i in range(-6,7)
              for j in range(-6,7) if i*i+j*j >= 4]
        for x in xs:
            for y in ys:
                d2=norm2(sub(x,y))
                if d2 == 0:
                    continue
                for a in (Q(1,2),Q(1),Q(2)):
                    actual=boundary_coefficient(R,x,y,a)
                    expected=((1-2*a)*d2+R*R-norm2(y))/(2*R*d2)
                    require(actual == expected, 'boundary coefficient identity')
                    require(actual <= 0, 'boundary sign for a >= 1/2')
                    counts['boundary_identities'] += 1
                require(dot(sub(x,y),x)/R <= d2/(2*R), 'exterior ball inequality')
                h=scale(R*R,sub(mul(inverse(y),inverse(y)),
                                 mul(inverse(x),inverse(x))))
                expected=R**4*d2*norm2(add(x,y))/(norm2(x)**2*norm2(y)**2)
                require(norm2(h) == expected, 'inversion factorization')
                counts['inversion_identities'] += 1
        for a in (Q(0),Q(1,4),Q(49,100)):
            c=boundary_coefficient(R,(R,Q(0)),(-R,Q(0)),a)
            require(c == (1-2*a)/(2*R) and c > 0, 'sharp threshold witness')
            counts['threshold_witnesses'] += 1
    c=boundary_coefficient(Q(1),(Q(1),Q(0)),(Q(-2),Q(0)),Q(0))
    require(c == Q(1,3), 'expanding reflection witness')
    c=boundary_coefficient(Q(1),(Q(1),Q(0)),(Q(3,2),Q(0)),Q(0))
    require(c == -2, 'contracting reflection witness')
    for k in range(21):
        t=Q(k,20); b=(-t,Q(0)); n=(Q(1),Q(0))
        X=(Q(1),Q(0)); Y=(-2-t,Q(0))
        require(add(add((Q(1),Q(0)),b),scale(t,n)) == X, 'controlled X equation')
        require(add((Q(-2),Q(0)),b) == Y, 'controlled expanding Y equation')
        require(norm2(sub(X,Y)) == (3+t)**2, 'controlled expansion distance')
        require(in_two_hole_closure(X) and in_two_hole_closure(Y), 'expansion domain membership')
        require(norm2(Y) > 1 and norm2(Y) < 100, 'expanding Y has no circle hit')
        L_y=max(Q(0),t-Q(1,2)); Y=(max(Q(1),Q(3,2)-t),Q(0))
        require(add(add((Q(3,2),Q(0)),b),scale(L_y,n)) == Y, 'controlled contracting Y equation')
        require(norm2(sub(X,Y)) == max(Q(0),Q(1,2)-t)**2, 'controlled contraction distance')
        require(in_two_hole_closure(Y), 'contraction domain membership')
        require(L_y == 0 or norm2(Y) == 1, 'regulator support')
        counts['controlled_path_checks'] += 1
    for m in range(1,65):
        polynomial_integral=-sum((Q(comb(2*j,j),4**j) for j in range(m)),Q(0))
        integration_by_parts=-Q(2*m*comb(2*m,m),4**m)
        require(polynomial_integral == integration_by_parts, 'even-power circular integral')
        counts['even_power_integrals'] += 1
    for k in range(-30,31):
        x,y=circle_point(Q(1),Q(k,7))
        gradient=(3-3*x*x-y*y,-2*x*y)
        require(dot((x,y),gradient) == 0, 'unit-disk Neumann polynomial')
        counts['neumann_boundary_checks'] += 1
    mean_dx=3-3*Q(1,4)-Q(1,4)
    require(mean_dx == 2 and mean_dx**2 == 4, 'product-uniform generator witness')
    guards=[
        (lambda: circle_point(Q(0),Q(1)), 'zero circle radius'),
        (lambda: circle_point(Q(-1),Q(1)), 'negative circle radius'),
        (lambda: inverse((Q(0),Q(0))), 'zero complex inverse'),
        (lambda: boundary_coefficient(Q(0),(Q(0),Q(0)),(Q(1),Q(0)),Q(1)), 'zero exterior radius'),
        (lambda: boundary_coefficient(Q(1),(Q(2),Q(0)),(Q(3),Q(0)),Q(1)), 'nonboundary x'),
        (lambda: boundary_coefficient(Q(1),(Q(1),Q(0)),(Q(0),Q(0)),Q(1)), 'interior obstacle y'),
        (lambda: boundary_coefficient(Q(1),(Q(1),Q(0)),(Q(1),Q(0)),Q(1)), 'diagonal logarithm')]
    for call,label in guards:
        expect_rejection(call,label)
        counts['guard_rejections'] += 1
    print(json.dumps({'result':'PASS','uid':os.getuid(),'counts':counts,
                     'arithmetic':'exact fractions only',
                     'scope':'finite algebra checks; no Brownian simulation or asymptotic proof'},sort_keys=True))


if __name__ == '__main__':
    main()

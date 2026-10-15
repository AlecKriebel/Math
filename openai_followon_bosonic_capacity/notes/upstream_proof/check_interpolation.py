#!/usr/bin/env python3
"""Deterministic exploratory falsification checks, not proof certificates.
Pure Python standard library; no upstream source mutation or third-party dependencies.
"""
import cmath
import hashlib
import json
import math
import random
from pathlib import Path

SEED = 27320261006
TRIALS = 50000
rng = random.Random(SEED)

def f(x):
    return x / math.sinh(x) if x else 1.0

def weights(m, x, y):
    return [m * f(x) * math.exp(x), m * f(x) * math.exp(-x),
            m * f(y) * math.exp(y), m * f(y) * math.exp(-y),
            m * f(x) * f(y) / f(x + y)]

def lambda_max(a, b, c):
    # symmetric matrix [[a,b],[b,c]]
    return (a + c + math.hypot(a-c, 2*b))/2

def comparison_norm(source, target, L):
    a = sum(target[k]*L[k][0]**2 for k in range(2)) / source[0]
    c = sum(target[k]*L[k][1]**2 for k in range(2)) / source[1]
    b = sum(target[k]*L[k][0]*L[k][1] for k in range(2)) / math.sqrt(source[0]*source[1])
    return lambda_max(a,b,c)

max_ratio = 0.0
for trial in range(TRIALS):
    source = [weights(10**rng.uniform(-2,2), rng.uniform(-8,8), rng.uniform(-8,8)) for _ in range(2)]
    target = [weights(10**rng.uniform(-2,2), rng.uniform(-8,8), rng.uniform(-8,8)) for _ in range(2)]
    L = [[rng.uniform(-1,1) for _ in range(2)] for _ in range(2)]
    four = [comparison_norm([s[j] for s in source], [t[j] for t in target], L) for j in range(4)]
    target_norm = comparison_norm([s[4] for s in source], [t[4] for t in target], L)
    ratio = target_norm/max(four)
    max_ratio = max(max_ratio,ratio)
    if ratio>1+1e-9:
        raise AssertionError(('four-weight falsification', trial, ratio,source,target,L))

max_derivative_imag = -math.inf
max_B_imag = -math.inf
for trial in range(TRIALS):
    q = 10**rng.uniform(-3,2)
    lo,hi = math.pi/2+1e-14,math.pi-1e-14
    for step in range(60):
        p = (lo+hi)/2
        if p*math.tan(p) < -q*math.tanh(q): lo=p
        else: hi=p
    p = rng.uniform(0.000001,1-0.000001)*(lo+hi)/2
    u = p + 1j*q
    s = (u/cmath.sin(u))**2
    B = u/cmath.tan(u)
    minus_Bprime = (B-s)/(2*s*(B-1))
    max_B_imag=max(max_B_imag,B.imag)
    max_derivative_imag=max(max_derivative_imag,minus_Bprime.imag)
    if s.imag<=0 or B.imag>=0 or minus_Bprime.imag>1e-7:
        raise AssertionError(('Stieltjes sign falsification', trial,u,s,B,minus_Bprime))

result = {'seed':SEED,'trials_per_family':TRIALS,'four_weight_2x2_max_target_to_hypothesis_ratio':max_ratio,
          'upper_half_plane_max_B_imag':max_B_imag,'upper_half_plane_max_minus_Bprime_imag':max_derivative_imag,
          'status':'no sampled falsification; this is numerical evidence, not a theorem or interval certificate'}
print(json.dumps(result,indent=2))
Path(__file__).with_name('check_interpolation_results.json').write_text(json.dumps(result,indent=2)+'\n')

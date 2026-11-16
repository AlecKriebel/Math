#!/usr/bin/env python3
"""New independent exact analytic controls; inert unless --run is explicit."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations
from math import comb
import json
import sys

A = Path(__file__).resolve().parent
COUNT = 0


def need(value, reason):
    global COUNT
    COUNT += 1
    if not value:
        raise RuntimeError(reason)


def matrix(rows):
    return tuple(tuple(F(x) for x in row) for row in rows)


def outer(z):
    return matrix([[x*y for y in z] for x in z])


def scale(k, a):
    return matrix([[k*x for x in row] for row in a])


def add(a, b):
    return matrix([[a[i][j]+b[i][j] for j in range(len(a))] for i in range(len(a))])


def mul(a, b):
    return matrix([[sum(a[i][k]*b[k][j] for k in range(len(a))) for j in range(len(a))] for i in range(len(a))])


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def pairing(a, b):
    return trace(mul(a, b))


def determinant(a):
    if len(a) == 1:
        return a[0][0]
    return sum((-1)**j*a[0][j]*determinant(tuple(tuple(row[k] for k in range(len(a)) if k != j) for row in a[1:])) for j in range(len(a)))


def psd(a):
    if any(a[i][j] != a[j][i] for i in range(len(a)) for j in range(len(a))):
        return False
    return all(determinant(tuple(tuple(a[i][j] for j in indices) for i in indices)) >= 0 for size in range(1,len(a)+1) for indices in combinations(range(len(a)),size))


def block(a, value):
    return matrix([list(row)+[0] for row in a] + [[0]*len(a)+[value]])


def run():
    need(not (A / "OWN_ANALYTIC_RESULTS.json").exists(), "do not overwrite actual own results")
    I = matrix([[1,0,0],[0,1,0],[0,0,1]])
    n = (1,-1,-1)
    B0, B1 = outer((1,0,1)), outer((1,1,0))
    J = add(B0,B1)
    P = add(I,scale(F(-1,3),outer(n)))
    need(mul(P,P) == P, "rational support projector")
    need(mul(mul(P,B0),P) == B0 and mul(mul(P,B1),P) == B1, "common support")
    need(add(J,scale(-1,P)) == scale(F(1,3),outer((2,1,1))), "exact coercivity Gram factor")
    need(mul(B0,B1) != mul(B1,B0), "noncommuting fixture")
    samples = 0
    for den in [1,2]:
        for integers in product(range(-2,3), repeat=3):
            z = tuple(F(x,den) for x in integers)
            w = (z[1],-z[2],z[0])
            X = add(outer(z),outer(w))
            C = mul(mul(P,X),P)
            need(psd(X) and psd(C), "exact Gram/compressed PSD")
            for B in [B0,B1]:
                need(pairing(X,B) == pairing(C,B), "whole compression evaluations")
            need(pairing(C,J) >= trace(C), "lambda1 trace coercivity")
            need(trace(C)**2 >= pairing(C,C), "PSD Frobenius trace bound")
            for mass in [1,10,1000000]:
                Y = add(X,scale(mass,outer(n)))
                need(mul(mul(P,Y),P) == C, "kernel mass vanishes on compression")
                need(pairing(Y,B0) == pairing(X,B0) and pairing(Y,B1) == pairing(X,B1), "kernel mass invisible in all evaluations")
            for rho in [F(0),F(1,3),F(1,2),F(2,3),F(1)]:
                Y = add(B0,scale(2,B1))
                need(pairing(block(X,rho),block(Y,1)) == pairing(X,Y)+rho, "exact scalar shift trace")
            samples += 1
    rowx = matrix([[0,0,0],[0,1,0],[0,0,0]])
    rowone = matrix([[0,0,0],[0,0,0],[0,0,1]])
    singular_samples = 0
    for den in range(1,13):
        for numerator in range(den+1):
            x = F(numerator,den)
            B = add(scale(1-x,B0),scale(x,B1))
            need(psd(B) and determinant(B) == 0, "singular no-Slater segment")
            need(pairing(rowx,B) == x and pairing(rowone,B) == 1-x, "exact tight slack certificates")
            singular_samples += 1
    B2 = scale(F(1,2),J)
    signed = 0
    for c0,c1,c2 in product(range(-3,4),repeat=3):
        Z = add(add(scale(c0,B0),scale(c1,B1)),scale(c2,B2))
        good = F(c0)+F(c2,2) >= 0 and F(c1)+F(c2,2) >= 0
        need(psd(Z) == good, "exact dual-cone membership")
        if not good:
            continue
        s = c0+c1+c2
        t = abs(s)+1
        q = s+t
        need(q > 0, "strict affine witness denominator")
        X = scale(F(1,q),add(Z,scale(t,B0)))
        need(psd(X), "positive affine witness")
        need(q*pairing(rowx,X) == c1+F(c2,2) >= 0, "dual slack pairing with negative coefficients allowed")
        need(F(c0+t+c1+c2,q) == 1, "affine coefficients sum1")
        signed += 1
    s = -3+2
    t = abs(s)+1
    q = s+t
    need(q == 1 and add(scale(-3,I),scale(2,scale(2,I))) == I, "negative-total-sum redundant-point algebra fixture")
    nonclosed = []
    for k in range(1,33):
        X = matrix([[F(1,k),1],[1,k]])
        need(psd(X) and determinant(X) == 0, "nonclosed generic PSD image sequence")
        need(X[0][0] == F(1,k) and X[0][1] == 1, "nonclosed image coordinates")
        nonclosed.append({"k":k,"x":str(X[0][0]),"y":"1","trace":str(trace(X))})
    for z in [0,1,100,1000000]:
        need(determinant(matrix([[0,1],[1,z]])) == -1, "unattainable limit determinant independent of z")
    need(pairing(matrix([[1]]),matrix([[0]])) == 0 != 1, "non-tight point slack cannot have zero-lift certificate")
    for k in range(1,129):
        need(2**(2*k)-1 >= 2**k, "safe exact exponent-halving loss")
    need(not (2**0-1 >= 2**0), "small-threshold negative control")
    for N in range(12,4097):
        n_even = 2*(N//4)
        need(n_even % 2 == 0 and 2*n_even <= N and 3*n_even >= N, "every residue class city exponent arithmetic")
    for n1 in range(2,66,2):
        N0 = max(12,2*n1+4)
        need(2*(N0//4) >= n1, "explicit even threshold")
    for q in range(2,41):
        need(sum(s*comb(q,s) for s in range(1,q+1)) == q*2**(q-1), "distinguished state count identity")
        need(sum(s*(q-s)*comb(q,s) for s in range(1,q+1)) == q*(q-1)*2**(q-2), "distinguished ordered transition identity")
    result = {"status":"PASS_BOUNDED_OWN_ANALYTIC_CONTROLS_NOT_EXTERNAL_RANK_PROOF", "checks":COUNT, "rational_noncommuting_compression_samples":samples, "singular_affine_segment_samples":singular_samples, "admissible_signed_dual_samples":signed, "nonclosed_image_exact_sequence":nonclosed, "mechanisms":["common support and exact Gram coercivity", "noncommuting PSD trace and scalar-block shift", "no-Slater singular affine slack section", "signed dual witness and negative-sum normalization", "nonclosed arbitrary cone image and non-tight slack negative controls", "uniform residue/exponent and binomial identities"], "native_source_or_scientific_imports_or_executions":[], "graph_matching_tour_enumeration":False, "external_asymptotic_exponential_PSD_rank_established_by_controls":False, "root139_gate":"CLOSED"}
    (A / "OWN_ANALYTIC_RESULTS.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":result["status"],"checks":COUNT,"analytic_samples":samples,"singular_samples":singular_samples,"signed_samples":signed,"root139_gate":"CLOSED"}))


if __name__ == "__main__":
    if sys.argv[1:] != ["--run"]:
        raise SystemExit("Inert by default; --run performs only newly authored bounded own analytic controls")
    run()

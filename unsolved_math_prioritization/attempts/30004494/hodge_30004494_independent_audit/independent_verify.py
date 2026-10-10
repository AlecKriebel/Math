#!/usr/bin/env python3
"""Independent exact controls and frozen-input integrity. No geometry is formalized.

The arithmetic implementation does not import or invoke the author's verifier.
Only the separate integrity/replay section invokes it as an additional check.
"""
from fractions import Fraction as Q
from itertools import product, permutations
from pathlib import Path
from hashlib import sha256
from math import lcm
import argparse
import json
import subprocess
import zipfile

p = argparse.ArgumentParser()
p.add_argument('--author', type=Path, default=Path(__file__).resolve().parent.parent / 'hodge_30004494')
p.add_argument('--archive', type=Path)
a = p.parse_args()
root = a.author.resolve()
archive = a.archive or root.parent / 'HODGE_30004494_AUTHOR_SAFE_FREEZE.zip'
expected_archive = '2880eb1f6345f6326c5b4ed8ab05801aa3c5db71d07e5a383472c74d69bcddbe'
expected_manifest = '1b384c58531496829886e4a0a96820dad434ea796a3c36b96f532e5b6c6a8571'
checks = 0

def require(truth):
    global checks
    checks += 1
    if not truth:
        raise AssertionError('Independent check failed: ' + str(checks))

def determinant(M):
    # Leibniz formula, deliberately distinct from author's elimination routine.
    n = len(M)
    out = Q(0)
    for perm in permutations(range(n)):
        inversions = sum(perm[i] > perm[j] for i in range(n) for j in range(i+1,n))
        term = Q(-1 if inversions % 2 else 1)
        for i,j in enumerate(perm):
            term *= M[i][j]
        out += term
    return out

def cramer_ones(M):
    den = determinant(M)
    return [determinant([[1 if j == col else M[i][j] for j in range(len(M))]
                         for i in range(len(M))]) / den for col in range(len(M))]

def mult(M,v):
    return [sum(Q(t)*u for t,u in zip(row,v)) for row in M]

# Exhaust all symmetric 3x3 integral Z-matrices with diagonal 1..6 and
# upper off-diagonal 0..-3; retain exactly positive-definite ones by Sylvester.
matrices = 0
candidates = 0
for diagonal in product(range(1,7), repeat=3):
    for neg in product(range(4), repeat=3):
        candidates += 1
        x,y,z = neg
        P = [[diagonal[0],-x,-y],[-x,diagonal[1],-z],[-y,-z,diagonal[2]]]
        if not all(determinant([r[:k] for r in P[:k]]) > 0 for k in (1,2,3)):
            continue
        v = cramer_ones(P)
        require(all(t > 0 for t in v))
        require(mult(P,v) == [1,1,1])
        scale = lcm(*(t.denominator for t in v))
        integral = [scale*t for t in v]
        require(all(t.denominator == 1 and t > 0 for t in integral))
        require(mult(P,integral) == [scale]*3)
        matrices += 1
require(cramer_ones([[5,-2],[-2,1]]) == [3,7])
require(cramer_ones([[1,0],[0,2]]) == [1,Q(1,2)])

# An exact interval arrangement decides all real strict primal and weak dual
# feasibility in two variables, normalized by a_1+a_2=1 or y_1+y_2=1.
def candidates_on_simplex(rows):
    breaks = {Q(0),Q(1)}
    for r,s in rows:
        if r != s:
            t = Q(-s, r-s)
            if 0 <= t <= 1:
                breaks.add(t)
    seq = sorted(breaks)
    return seq + [(u+v)/2 for u,v in zip(seq,seq[1:])]

alternatives = 0
primal_count = 0
for vals in product(range(-3,4), repeat=4):
    B = [list(vals[:2]),list(vals[2:])]
    primal = next(([t,1-t] for t in candidates_on_simplex(B)
                   if all(v < 0 for v in mult(B,[t,1-t]))),None)
    Bt = [list(col) for col in zip(*B)]
    dual = next(([t,1-t] for t in candidates_on_simplex(Bt)
                 if all(v >= 0 for v in mult(Bt,[t,1-t]))),None)
    require((primal is None) != (dual is None))
    if primal is not None:
        denominator = lcm(*(t.denominator for t in primal))
        require(all(v < 0 for v in mult(B,[t*denominator for t in primal])))
        primal_count += 1
    alternatives += 1

# Independent determinant bookkeeping in the associated-graded basis.
# Polarization identifies det(E^{n-q}) with det(E^q)^{-1}, modulo torsion.
def filtration_vector(n,p):
    vec = [0]*(n+1)
    for q in range(p,n+1):
        if 2*q > n:
            vec[q] += 1
        elif 2*q < n:
            vec[n-q] -= 1
        # middle graded determinant is torsion when n is even.
    return vec

weights = 96
for n in range(1,weights+1):
    start = (n+2)//2
    G = [sum(filtration_vector(n,p)[q] for p in range(1,n+1)) for q in range(n+1)]
    L = [sum(filtration_vector(n,p)[q] for p in range(start,n+1)) for q in range(n+1)]
    correction = filtration_vector(n,start) if n%2 else [0]*(n+1)
    require(G == [2*x-y for x,y in zip(L,correction)])
    if n == 1:
        require(G == L)
    if n >= 3 and n%2:
        require(G != L and G != [2*x for x in L])

# Closed cone control: boundary strictness is essential, even when every
# actual positive-x test ray separately acquires a curve-dependent threshold.
for m in range(1,513):
    t = Q(1,2*m)
    require(m*t*t-t == -Q(1,4*m))
    x,y,z = t*t,t,Q(1)
    require(y*y == x*z and x >= 0 and z >= 0)

# Genuine ruled-surface numerical control: X=F_e, S^2=-e, S.F=1, F^2=0.
# L=S+eF is nef/big, E=S; mL-E is ample exactly when m>=2 for e>=1.
ruled_checks = 0
for e in range(1,33):
    for m in range(1,65):
        alpha,beta = m-1,m*e
        degree_F = alpha
        degree_S = -e*alpha+beta
        square = -e*alpha*alpha+2*alpha*beta
        require(degree_S == e)
        require((degree_F > 0 and degree_S > 0 and square > 0) == (m >= 2))
        ruled_checks += 1

# Frozen author files and safe archive: no import of author arithmetic above.
manifest_bytes = (root/'MANIFEST.json').read_bytes()
require(sha256(manifest_bytes).hexdigest() == expected_manifest)
manifest = json.loads(manifest_bytes)
for item in manifest['files']:
    blob = (root/item['path']).read_bytes()
    require(len(blob) == item['bytes'])
    require(sha256(blob).hexdigest() == item['sha256'])
require(sha256(archive.read_bytes()).hexdigest() == expected_archive)
expected_names = {'hodge_30004494/'+f['path'] for f in manifest['files']} | {'hodge_30004494/MANIFEST.json'}
with zipfile.ZipFile(archive) as z:
    require(set(z.namelist()) == expected_names)
    require(len(z.namelist()) == len(expected_names))
    for name in z.namelist():
        require(z.read(name) == (root/Path(name).name).read_bytes())
run = subprocess.run(['python3','verify.py'],cwd=root,capture_output=True,check=True)
require(run.stdout == (root/'VERIFICATION.json').read_bytes())
require(not run.stderr)
print(json.dumps({
    'problem_id':'30004494',
    'verdict':'PASS_INDEPENDENT_FINITE_CONTROLS_AND_INTEGRITY',
    'checks':checks,
    'positive_definite_matrices_checked':matrices,
    'candidate_sign_matrices':candidates,
    'exact_2x2_linear_alternatives':alternatives,
    'strict_primal_feasible_cases':primal_count,
    'dual_certificate_cases':alternatives-primal_count,
    'determinant_weights_checked':[1,weights],
    'curved_cone_threshold_countercontrols':512,
    'hirzebruch_surface_numerical_cases':ruled_checks,
    'author_replay':'byte_identical',
    'author_assertions':json.loads(run.stdout)['checks'],
    'author_manifest_sha256':expected_manifest,
    'author_archive_sha256':expected_archive,
    'scope':'Finite exact controls and integrity only; not formal verification of geometry or a solution of the original conjecture.'
},indent=2,sort_keys=True))

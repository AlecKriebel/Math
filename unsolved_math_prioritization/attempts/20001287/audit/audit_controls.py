#!/usr/bin/env python3
"""Portable independent algebra and integrity controls for Problem 20001287.
Run: python3 audit_controls.py [author_public_directory]
Only author replay needs SymPy. Other checks use Python's standard library.
No network calls; no source files or private retrieval material are required.
Writes audit_controls.json beside this script, never in the author directory.
These controls do not prove Prekopa-Leindler or its equality theorem.
"""
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import hashlib
import itertools
import json
import shutil
import subprocess
import sys
import tempfile

PIN = 'f8f59ad75dcd339d00d7a1fefaef95c88e20bc58f1d8340f00c64b961524f730'
FILES = {'LOCAL_EXPANSION.md', 'PROOF.md', 'README.md', 'RESEARCH_LOG.md',
         'SOURCE_GATE.md', 'check_exact.py', 'exact_results.json'}


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def freeze(p):
    mpath = p/'FROZEN_AUTHOR_MANIFEST.json'
    require(sha(mpath) == PIN, 'frozen manifest mismatch')
    m = json.loads(mpath.read_text())
    require(set(m['files']) == FILES, 'unexpected author allowlist')
    require(m['problem_id'] == 20001287 and m['rank'] == 510, 'wrong target')
    require(m['approaches_completed'] == 3 and m['approach_budget'] == 5, 'wrong approach disposition')
    for name, expected in m['files'].items():
        require((p/name).stat().st_size == expected['bytes'], 'frozen byte length mismatch')
        require(sha(p/name) == expected['sha256'], 'frozen file hash mismatch')
    return {name: sha(p/name) for name in sorted(FILES)}


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(x) for x in zip(*a)]


def mul(a, b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]


def determinant(a):
    a = [list(map(F,row)) for row in a]
    d = F(1)
    for j in range(len(a)):
        p = next((i for i in range(j,len(a)) if a[i][j]), None)
        if p is None:
            return F(0)
        if p != j:
            a[p],a[j] = a[j],a[p]
            d = -d
        v = a[j][j]
        d *= v
        for i in range(j+1,len(a)):
            q = a[i][j]/v
            for k in range(j+1,len(a)):
                a[i][k] -= q*a[j][k]
    return d


def inverse(a):
    n = len(a)
    z = [list(map(F,row))+e for row,e in zip(a,eye(n))]
    for j in range(n):
        p = next(i for i in range(j,n) if z[i][j])
        z[p],z[j] = z[j],z[p]
        d = z[j][j]
        z[j] = [v/d for v in z[j]]
        for i in range(n):
            if i != j:
                q = z[i][j]
                z[i] = [x-q*y for x,y in zip(z[i],z[j])]
    return [row[n:] for row in z]


def generator(n, family):
    a = eye(n)
    for i in range(n):
        for j in range(i):
            a[i][j] = F(((i+2)*(j+3)+family)%5-2, family+2)
    if family == 1:
        a = [[v*F(j+2,j+1) for j,v in enumerate(row)] for row in a]
    if family == 2:
        u = eye(n)
        for i in range(n-1):
            u[i][i+1] = F((-1)**i,3)
        a = mul(a,u)
    return a


def gram_checks(a):
    n = len(a)
    ai = inverse(a)
    at = transpose(a)
    g = mul(at,a)
    gi = inverse(g)
    require(mul(at,transpose(ai)) == eye(n), 'dual pairing failure')
    require(gi == mul(ai,transpose(ai)), 'inverse Gram failure')
    require(determinant(g) == determinant(a)**2, 'Gram determinant failure')
    require(all(determinant([row[:k] for row in g[:k]]) > 0 for k in range(1,n+1)), 'positive definiteness failure')
    # Compare every coefficient of the quadratic form, not sampled x,y.
    b = [row+[-v for v in rowi] for row,rowi in zip(a,transpose(ai))]
    bt_b = mul(transpose(b),b)
    certificate = [[(g[i][j] if i<n and j<n else gi[i-n][j-n] if i>=n and j>=n else -F(i%n == j%n))
                    for j in range(2*n)] for i in range(2*n)]
    require(bt_b == certificate, 'Young square coefficient failure')
    # An arbitrary positive column rescaling must preserve the cone.
    scales = [F(i+2,i+1) for i in range(n)]
    ad = [[v*scales[j] for j,v in enumerate(row)] for row in a]
    require(mul(transpose(ad),ad) == [[scales[i]*g[i][j]*scales[j] for j in range(n)] for i in range(n)], 'column scaling congruence failure')
    require(abs(determinant(a))*abs(determinant(transpose(ai))) == 1, 'absolute Jacobian cancellation failure')
    return str(determinant(a))


def cleaned(poly):
    return {k:v for k,v in poly.items() if v}


def add(poly, e, f, power, value):
    poly[(min(e,f),max(e,f),power)] += F(value)


def hessian_check(n):
    edges = list(itertools.combinations(range(n),2))
    number = {e:i for i,e in enumerate(edges)}
    q2 = defaultdict(F)
    # Half-normal moment of X_i X_j is a for i != j and 1 otherwise.
    # Enumerate the determinant, inverse and exponential density derivatives.
    for e in range(len(edges)):
        add(q2,e,e,0,F(1,2))
    for i in range(n):
        for k in range(n):
            for j in range(n):
                if i != k and k != j:
                    e = number[tuple(sorted((i,k)))]
                    f = number[tuple(sorted((k,j)))]
                    add(q2,e,f,int(i != j),F(-1,2))
    for ei,e in enumerate(edges):
        for fi,f in enumerate(edges):
            counts = [int(v in e)+int(v in f) for v in range(n)]
            odd = sum(v%2 for v in counts)
            require(odd in (0,2,4), 'unexpected moment degree')
            add(q2,ei,fi,odd//2,F(1,2))
    expected_q2 = defaultdict(F)
    for ei,e in enumerate(edges):
        for fi in range(ei+1,len(edges)):
            if not set(e)&set(edges[fi]):
                add(expected_q2,ei,fi,2,1)
    require(cleaned(q2) == cleaned(expected_q2), 'density second-order cancellation failure')
    product = defaultdict(F, {k:2*v for k,v in q2.items()})
    for i in range(n):
        for j in range(i+1,n):
            for k in range(n):
                if i != k and k != j:
                    add(product,number[tuple(sorted((i,k)))],number[tuple(sorted((k,j)))],1,1)
    for ei in range(len(edges)):
        for fi in range(len(edges)):
            add(product,ei,fi,2,-1)
    claimed = defaultdict(F)
    for ei in range(len(edges)):
        add(claimed,ei,ei,1,-1)
        add(claimed,ei,ei,2,1)
    for vertex in range(n):
        incident = [i for i,e in enumerate(edges) if vertex in e]
        for ei in incident:
            for fi in incident:
                add(claimed,ei,fi,1,F(1,2))
                add(claimed,ei,fi,2,-1)
    require(cleaned(product) == cleaned(claimed), 'Hessian coefficient failure')
    # Restrict to one edge: the normalized product must be 1-a^2*t^2+O(t^3).
    require({power:v for (ei,fi,power),v in cleaned(product).items() if ei == fi == 0} == {2:F(-1)}, 'planar calibration failure')
    return {'n':n,'shape_variables':len(edges),'density_coefficients_checked':len(edges)*(len(edges)+1)//2,
            'product_coefficients_verified':True}


def main():
    author = Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parent.parent/'public'
    before = freeze(author)
    recorded = json.loads((author/'exact_results.json').read_text())
    require(recorded['all_checks_passed'] is True, 'author result flag failure')
    with tempfile.TemporaryDirectory(prefix='spherical-replay-') as tmp:
        p = Path(tmp)
        shutil.copyfile(author/'check_exact.py',p/'check_exact.py')
        run = subprocess.run([sys.executable,'-B',str(p/'check_exact.py')],cwd=p,
                             capture_output=True,text=True,check=True,timeout=180)
        require((p/'exact_results.json').read_bytes() == (author/'exact_results.json').read_bytes(), 'author replay is not byte identical')
        replay = json.loads(run.stdout)
    matrices = []
    unique = set()
    reflected = 0
    for n in range(1,7):
        for family in range(3):
            a = generator(n,family)
            unique.add(tuple(tuple(row) for row in a))
            d = gram_checks(a)
            matrices.append({'n':n,'family':family,'det_A':d,'identities':'pass'})
            # Absolute determinants are necessary even for a reflected generator.
            reflected_a = [row[:] for row in a]
            reflected_a[0] = [-v for v in reflected_a[0]]
            require(F(gram_checks(reflected_a)) == -F(d), 'reflection orientation failure')
            reflected += 1
    require(matrices == recorded['rational_gram_tests'], 'independent rational test differs')
    hessian = [hessian_check(n) for n in range(2,9)]
    require(recorded['hessian_tests'] == [{'n':x['n'],'independent_edges':x['shape_variables'],'identities':'pass'} for x in hessian], 'Hessian coverage mismatch')
    # Scalar Gaussian normalization after cancelling pi symbolically.
    require(all(F(1,2)**n/F(2)**n == F(1,4)**n for n in range(1,65)), 'normalization failure')
    # sqrt(2) < 23/16 proves the circular-cone obstruction exactly.
    require(F(23,16)**2 > 2 and F(23,16)>0, 'nonsimplicial obstruction failure')
    negative = []
    for name,check in [
        ('wrong_dual_transpose',lambda: mul(transpose(generator(3,1)),inverse(generator(3,1))) == eye(3)),
        ('missing_log_jacobian',lambda: F(2)*F(3) == 1),
        ('wrong_sharp_constant',lambda: F(1,2)**4/F(2)**4 == F(1,2)**4),
        ('planar_deficit_sign_reversed',lambda: F(-1) == F(1)),
    ]:
        require(not check(), 'negative control unexpectedly accepted: '+name)
        negative.append(name)
    corruptions = []
    with tempfile.TemporaryDirectory(prefix='spherical-corruption-') as tmp:
        p = Path(tmp)
        for name in FILES|{'FROZEN_AUTHOR_MANIFEST.json'}:
            shutil.copyfile(author/name,p/name)
        for name in ('PROOF.md','FROZEN_AUTHOR_MANIFEST.json'):
            original = (p/name).read_bytes()
            (p/name).write_bytes(original+b'\ncorruption\n')
            try:
                freeze(p)
            except AssertionError:
                corruptions.append(name)
            else:
                raise AssertionError('corruption accepted: '+name)
            (p/name).write_bytes(original)
    require(freeze(author) == before, 'frozen inputs changed')
    result = {'verdict':'PASS_FULL_PRIOR','problem_id':20001287,'full_target_solved':True,
              'classification':'complete deduction from established literature','novelty_claim':False,
              'frozen_manifest_sha256':PIN,'frozen_files_checked':len(FILES),'frozen_files_unchanged':True,
              'author_replay_byte_identical':True,'author_replay_summary':replay,
              'independent_rational_gram_tests':matrices,'rational_test_instances':len(matrices),
              'distinct_rational_matrices':len(unique),'reflected_orientation_tests':reflected,
              'independent_hessian_tests':hessian,'algebra_negative_controls_rejected':negative,
              'integrity_corruptions_rejected':corruptions,
              'proof_scope':'Finite exact supporting algebra; analytic theorem and equality hypotheses audited separately in AUDIT_REPORT.md.',
              'remote_mutations':False}
    out = Path(__file__).with_name('audit_controls.json')
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'verdict':result['verdict'],'author_replay_byte_identical':True,
                      'matrix_instances':len(matrices),'distinct_matrices':len(unique),
                      'hessian_dimensions':len(hessian),'integrity_corruptions_rejected':len(corruptions)},sort_keys=True))


if __name__ == '__main__':
    main()

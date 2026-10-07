#!/usr/bin/env python3
"""Source-free independent replay, optimizer-safety, and adversarial controls.

Run from any directory with the frozen ../public packet intact. Only the audit
report beside this script is written; author verifier runs use temporary copies.
All audit checks use explicit exceptions and remain active under -O and -OO.
"""
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, product
from math import isqrt
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
PUBLIC = HERE.parent / 'public'
EXPECTED_MANIFEST = '58932d752e971ec0789b637ceab3ae3f0246927befb6bece2dcb1188ae034100'
checks = Counter()

def need(condition, label):
    if not condition:
        raise RuntimeError('AUDIT FAILURE: ' + label)
    checks[label.split(':', 1)[0]] += 1

def digest(data):
    return hashlib.sha256(data).hexdigest()

manifest_bytes = (PUBLIC / 'FROZEN_MANIFEST.json').read_bytes()
need(digest(manifest_bytes) == EXPECTED_MANIFEST, 'manifest: pinned digest')
manifest = json.loads(manifest_bytes)
for row in manifest['files']:
    b = (PUBLIC / row['path']).read_bytes()
    need(len(b) == row['bytes'], 'manifest: bytes ' + row['path'])
    need(digest(b) == row['sha256'], 'manifest: digest ' + row['path'])

# Independently specified geometry, matrix, witness, radical expressions, table.
points = [(9, 9), (-3, 0), (6, 3), (7, -4), (2, 10), (8, 0)]
expected_matrix = [
 [0,225,45,173,50,82], [225,0,90,116,125,121],
 [45,90,0,50,65,13], [173,116,50,0,221,17],
 [50,125,65,221,0,136], [82,121,13,17,136,0]]
matrix = [[(a[0]-b[0])**2+(a[1]-b[1])**2 for b in points] for a in points]
need(matrix == expected_matrix, 'geometry: matrix')
openings = [Q(0),Q(1,2),Q(1,2),Q(0),Q(1,2),Q(1,2)]
supports = [(2,4),(1,2),(2,5),(2,5),(2,4),(2,5)]
assignments = [[Q(1,2) if i in supports[j] else Q(0) for j in range(6)] for i in range(6)]
need(sum(openings) == 2, 'geometry: opening mass')
for j in range(6):
    need(sum(assignments[i][j] for i in range(6)) == 1, 'geometry: column mass')
    for i in range(6):
        need(0 <= assignments[i][j] <= openings[i] <= 1, 'geometry: feasibility')
need(sum(assignments[i][j] for i in range(6) for j in range(6) if i != j) == 4,
     'geometry: off-diagonal mass')
radicals = Counter()
for i in range(6):
    for j in range(6):
        if matrix[i][j] and assignments[i][j]:
            radicals[matrix[i][j]] += assignments[i][j]
need(radicals == {45:Q(1,2),50:Q(1),90:Q(1,2),13:Q(1),17:Q(1,2),65:Q(1,2)},
     'geometry: symbolic fractional expression')

def bracket(m, scale):
    v = isqrt(m * scale**2)
    need(v*v <= m*scale**2 < (v+1)**2, 'radicals: floor enclosure')
    return Q(v,scale), Q(v + (v*v < m*scale**2),scale)

def brackets(scale):
    return {v:bracket(v,scale) for row in matrix for v in row}

bounds = brackets(10**12)
frac_lo = sum(w*bounds[m][0] for m,w in radicals.items())
frac_hi = sum(w*bounds[m][1] for m,w in radicals.items())
all_centers = list(combinations(range(6),2))
cost_intervals = {}
for centers in all_centers:
    nearest_squared = [min(matrix[i][j] for i in centers) for j in range(6)]
    cost_intervals[centers] = tuple(sum(bounds[m][e] for m in nearest_squared) for e in (0,1))
    need(cost_intervals[centers][0] > frac_hi, 'geometry: every integral competitor')
    # Every assignment to a fixed pair is no cheaper, checked in squared space.
    for chosen in product(centers, repeat=6):
        need(all(matrix[chosen[j]][j] >= nearest_squared[j] for j in range(6)),
             'geometry: exhaustive integral assignment')
need(all(cost_intervals[c][0] > cost_intervals[(1,2)][1]
         for c in all_centers if c != (1,2)), 'geometry: unique optimal center pair')
integer_radicals = Counter(min(matrix[i][j] for i in (1,2)) for j in range(6))
del integer_radicals[0]
need(integer_radicals == {45:1,50:1,65:1,13:1}, 'geometry: symbolic integral expression')
b6 = brackets(10**6)
expected_lower_numerators = [33604984,27234517,28672704,40096873,25799723,
25447078,35527457,36903653,27964380,27862843,26871653,28380397,29035568,35093168,25799723]
for centers, expected in zip(all_centers, expected_lower_numerators):
    v = sum(b6[min(matrix[i][j] for i in centers)][0] for j in range(6))
    need(v == Q(expected,10**6), 'geometry: printed table')
lo6 = sum(b6[min(matrix[i][j] for i in (1,2))][0] for j in range(6))
hi6 = sum(w*b6[m][1] for m,w in radicals.items())
need(lo6-hi6 == Q(232103,400000), 'geometry: printed gap')
need(lo6-hi6 > Q(29,50), 'geometry: strict gap margin')
need(lo6-hi6-4*6*Q(1,100) > Q(17,50), 'geometry: perturbation margin')
need((lo6-hi6)/10 - Q(8,1000) > Q(1,20), 'geometry: CLT open box margin')

# Recover covariance by integrating Gaussian polynomials, rather than
# assuming the claimed entries or calling a numerical linear algebra package.
def gaussian_moment(exponents):
    value = 1
    for e in exponents:
        if e % 2:
            return 0
        for t in range(1,e,2):
            value *= t
    return value

def edge_polynomial(edge):
    i,j = edge
    zero = (0,)*6
    ei = list(zero); ei[i] = 2
    ej = list(zero); ej[j] = 2
    cross = list(zero); cross[i] = cross[j] = 1
    return {zero:-2,tuple(ei):1,tuple(ej):1,tuple(cross):-2}

covariance = []
for a in all_centers:
    row = []
    pa = edge_polynomial(a)
    need(sum(c*gaussian_moment(e) for e,c in pa.items()) == 0, 'CLT: centered summand')
    for b in all_centers:
        pb = edge_polynomial(b)
        value = Q(sum(c*d*gaussian_moment(tuple(x+y for x,y in zip(e,f)))
                      for e,c in pa.items() for f,d in pb.items()),8)
        expected = Q(1) if a == b else Q(1,4) if set(a)&set(b) else Q(0)
        need(value == expected, 'CLT: covariance from Gaussian moments')
        need(value == Q(int(a==b),2) + Q(len(set(a)&set(b)),4),
             'CLT: positive noise plus incidence Gram')
        row.append(value)
    covariance.append(row)
# With K6 incidence B, B^T B = 4 Id + J. Covariance is 1/2 Id + BB^T/4.
for i in range(6):
    for j in range(6):
        need(sum(int(i in edge)*int(j in edge) for edge in all_centers) == 4*int(i==j)+1,
             'CLT: incidence spectrum certificate')

# Distinct small-grid tests of line rounding, including zero openings,
# saturated openings, coincident facilities, and clients outside their span.
line_vectors = 0
line_client_tests = 0
for denominator,max_n in [(3,5),(5,4),(7,3)]:
    for n in range(2,max_n+1):
        locations = [0,0,2,5,5][:n]
        for weights in product(range(denominator+1), repeat=n):
            total = sum(weights)
            if total % denominator or not 0 < total//denominator < n:
                continue
            k = total//denominator
            cumulative = [0]
            for w in weights:
                cumulative.append(cumulative[-1]+w)
            selected = []
            for h in range(denominator):
                phase = Q(2*h+1,2)
                s = [i for i in range(n) if any(cumulative[i] <= phase+denominator*t < cumulative[i+1] for t in range(k))]
                need(len(s) == k and len(set(s)) == k, 'line: distinct k selections')
                selected.append(s)
            for start in range(n):
                for end in range(start,n):
                    missed = sum(not any(start<=i<=end for i in s) for s in selected)
                    need(Q(missed,denominator) == max(Q(0),1-Q(sum(weights[start:end+1]),denominator)),
                         'line: every interval miss probability')
            for client in [-2,0,1,2,3,5,7]:
                distances = [abs(t-client) for t in locations]
                expected_cost = Q(sum(min(distances[i] for i in s) for s in selected),denominator)
                remaining = Q(1); frac_cost = Q(0)
                for i in sorted(range(n),key=lambda i:distances[i]):
                    mass = min(remaining,Q(weights[i],denominator))
                    frac_cost += mass*distances[i]
                    remaining -= mass
                need(remaining == 0, 'line: fractional greedy feasibility')
                need(expected_cost == frac_cost, 'line: layer-cake objective equality')
                line_client_tests += 1
            line_vectors += 1

# Reconstruct the duplicated geometry for additional r values, including
# different labels at the same site. Witness feasibility uses representative labels.
replicated_pairs = 0
for r in [1,2,3,9,11]:
    locations = [base for base in range(6) for _ in range(r)]
    for first,second in combinations(range(6*r),2):
        lo = sum(bounds[min(matrix[locations[first]][j],matrix[locations[second]][j])][0]
                 for j in locations)
        need(lo - r*frac_hi > Q(29*r,50), 'replication: labelled center-pair gap')
        replicated_pairs += 1
    need(r*(lo6-hi6)-4*(6*r)*Q(1,100) > Q(17*r,50), 'replication: perturbation margin')

# Original and one-line hardened verifier must have identical baseline output.
original = (PUBLIC / 'verify.py').read_text()
hardened = (HERE / 'verify_hardened.py').read_text()
need(hardened == original.replace(' assert b\n', " if not b:\n  raise AssertionError('certificate check failed')\n"),
     'patch: exact minimal change')
expected_output = (PUBLIC / 'verification.json').read_bytes()

def run_script(source, flag):
    with tempfile.TemporaryDirectory(prefix='kmedian-audit-') as temp:
        script = Path(temp)/'verify.py'
        script.write_text(source)
        env = dict(os.environ)
        env.pop('PYTHONOPTIMIZE',None)
        command = [sys.executable] + ([flag] if flag else []) + [str(script)]
        result = subprocess.run(command, capture_output=True, text=True, env=env, timeout=60)
        out = script.with_name('verification.json')
        payload = out.read_bytes() if out.exists() else None
        return {'exit': result.returncode,'wrote_report':payload is not None,
                'report_sha256':digest(payload) if payload else None,
                'assertion_rejected':result.returncode != 0 and 'AssertionError' in result.stderr},payload

baseline_results = []
for name,source in [('original',original),('hardened',hardened)]:
    for flag in ['', '-O','-OO']:
        result,payload = run_script(source,flag)
        need(result['exit'] == 0 and payload == expected_output, 'execution: baseline '+name+' '+flag)
        baseline_results.append({'variant':name,'mode':flag or 'normal',**result})

mutations = [
 ('explicit_false_check','check(sum(y)==2)','check(False)'),
 ('invalid_opening_mass','[0,1,1,0,1,1]','[0,0,0,0,0,0]'),
 ('invalid_column_mass','Q(int(i in support[j]),2)','Q(int(i in support[j]),3)'),
 ('unsupported_facility','support=[(2,4)','support=[(0,4)'),
 ('invalid_radical_enclosure','lo=[[Q(isqrt(v*scale*scale),scale)','lo=[[Q(isqrt(v*scale*scale)+1,scale)'),
 ('false_gap_threshold','check(L-FU>Q(29,50))','check(L-FU>Q(1000))'),
 ('false_replication_threshold','check(lower-r*FU>Q(29*r,50))','check(lower-r*FU>Q(1000*r))'),
 ('negative_covariance_diagonal','Q(1)if a==b','Q(-100)if a==b'),
 ('repeated_rounding_phase','[Q(1,2),Q(3,2),Q(5,2),Q(7,2)]','[Q(1,2),Q(1,2),Q(1,2),Q(1,2)]'),
 ('false_off_diagonal_mass','if i!=j)==4)','if i!=j)==5)'),
]
mutation_results = []
for mutation,before,after in mutations:
    for name,source in [('original',original),('hardened',hardened)]:
        need(source.count(before) == 1, 'mutation: unique anchor '+mutation)
        changed = source.replace(before,after,1)
        for flag in ['', '-O','-OO']:
            result,_ = run_script(changed,flag)
            expected_reject = name == 'hardened' or not flag
            need(result['assertion_rejected'] == expected_reject,
                 'mutation: detection '+mutation+' '+name+' '+flag)
            need(result['wrote_report'] != expected_reject,
                 'mutation: report gate '+mutation+' '+name+' '+flag)
            mutation_results.append({'mutation':mutation,'variant':name,'mode':flag or 'normal',**result})

# The original corpus is unchanged, including its saved JSON output.
for row in manifest['files']:
    need(digest((PUBLIC/row['path']).read_bytes()) == row['sha256'], 'preservation: '+row['path'])
report = {
 'problem_id':2800903,'rank':989,'frozen_manifest_sha256':EXPECTED_MANIFEST,
 'python_version':sys.version.split()[0],
 'mathematical_verdict':'all five scoped proof routes accepted; original joint probability question unresolved',
 'verifier_verdict':'original fails optimized-Python negative controls; minimal hardening passes all modes',
 'checks_by_category':dict(sorted(checks.items())),
 'exact_independent_checks':sum(checks.values()),
 'independent_fractional_interval_1e12':list(map(str,[frac_lo,frac_hi])),
 'independent_integer_interval_1e12':list(map(str,cost_intervals[(1,2)])),
 'frozen_gap_lower':'232103/400000',
 'independent_line_vectors':line_vectors,'independent_line_client_tests':line_client_tests,
 'independent_replicated_pairs':replicated_pairs,
 'covariance_spectrum':[{'value':'3','multiplicity':1},{'value':'3/2','multiplicity':5},{'value':'1/2','multiplicity':9}],
 'baseline_results':baseline_results,'mutation_results':mutation_results,
 'limitations':['Finite controls do not replace universal written proofs.',
                'No LP-optimum computation or probability simulation.',
                'No new joint growing-n/d theorem or novelty certification.',
                'Mutation suite samples common corruptions; not a proof against arbitrary code tampering.'],
}
(HERE/'AUDIT_CHECKS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['baseline_results','mutation_results']},indent=2))

#!/usr/bin/env python3
"""Exact controls and inventory checking; NOT a proof of the full PDE claim."""
import sys
sys.dont_write_bytecode = True
import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
import sympy as s

FILES = {
    'README.md', 'PROOF.md', 'APPROACHES.md', 'SOURCE_AUDIT.md',
    'PUBLIC_METADATA.json', 'claims.json', 'verify.py',
    'test_fail_closed.py', 'requirements.txt', 'AUTHOR_TEST_RESULTS.json',
}
ROOT = Path(__file__).resolve().parent
EXPECTED_CLAIMS = {
    'problem_id': 30000801,
    'verdict': 'PARTIAL_ONLY_FULL_PROBLEM_UNRESOLVED',
    'full_resolution': False,
    'novelty_claim': False,
    'dimension': 4,
    'operator': 'Delta^2',
    'laplacian_sign': 'sum_second_derivatives',
    'nonlinearity': 'lambda*u*exp(2*u^2)',
    'boundary': ['u=0', 'Delta_u=0'],
    'lambda': 'positive_spatial_constant_tending_to_zero',
    'bubble_rhs_coefficient': 96,
    'energy_quantum_pi_squared_coefficient': 16,
    'fundamental_log_pi_squared_denominator': 8,
    'pohozaev_mass_pi_squared_denominator': 16,
    'extra_hypotheses_proved_from_target': False,
    'criterion_hypotheses': [
        'interior_point', 'C3_exterior_logarithmic_profile_with_C3_regular_part',
        'finite_primitive_mass_limit', 'all_height_ratios_positive_and_finite',
        'both_weighted_masses_exhausted_by_finitely_many_bubbles',
    ],
    'ordinary_energy_tightness_suffices': False,
    'checks_prove_global_PDE_claim': False,
    'substantive_approaches': 5,
}
PINS = {
    'catalog': (21735099, '891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566', 15458),
    'problems': (68931837, '04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf', 15458),
    'reports': (80334822, '8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b', 6701),
}
REVIEW_SHA = '6c5a284146c34349fd290aa03fea676c2fcd00352dec31988d7a5376d638fe3e'
STATEMENT_SHA = 'e240b1b64786f66238f5efc7e10d42b166b7de5c2962733213161c6ba79c7c36'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(b):
    return hashlib.sha256(b).hexdigest()


def read_json(path):
    def unique_pairs(pairs):
        out = {}
        for key, value in pairs:
            require(key not in out, 'duplicate JSON key')
            out[key] = value
        return out
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_pairs)


def inventory():
    require(not any(p.is_symlink() for p in ROOT.iterdir()), 'symlink payload member')
    actual = {p.name for p in ROOT.iterdir()}
    require(actual == FILES | {'MANIFEST.json'}, 'missing or extra payload file')
    require(all(p.is_file() for p in ROOT.iterdir()), 'non-file payload member')
    manifest = read_json(ROOT / 'MANIFEST.json')
    require(set(manifest) == {'schema', 'files'}, 'manifest schema keys')
    require(manifest['schema'] == 'sha256-byte-inventory-v1', 'manifest schema')
    require(set(manifest['files']) == FILES, 'manifest members')
    for name in sorted(FILES):
        b = (ROOT / name).read_bytes()
        expected = {'bytes': len(b), 'sha256': digest(b)}
        require(manifest['files'][name] == expected, 'integrity mismatch: ' + name)


def metadata():
    claims = read_json(ROOT / 'claims.json')
    # Canonical serialization distinguishes false from 0 and true from 1.
    require(json.dumps(claims, sort_keys=True) == json.dumps(EXPECTED_CLAIMS, sort_keys=True),
            'claim scope/normalization mismatch')
    md = read_json(ROOT / 'PUBLIC_METADATA.json')
    require(md['problem_id'] == 30000801 and md['problem_number'] == 'OWR-1591-003', 'target metadata')
    require(md['full_resolution'] is False, 'metadata full-resolution overclaim')
    for key, (size, sha, count) in PINS.items():
        d = md['corpora'][key]
        require(d == {'bytes': size, 'sha256': sha, 'record_count': count}, 'corpus metadata pin: ' + key)
    review = md['review']
    require(review['review_sha256'] == REVIEW_SHA, 'review hash pin')
    require(review['statement_sha256'] == STATEMENT_SHA, 'statement hash pin')
    require(review['serialized_bytes'] == 4537, 'review byte count')
    require(review['serialization'] == 'json.dumps([record, reports.get(problem_number, {})], sort_keys=True).encode(utf-8)', 'serialization')
    require(review['report_present'] is False and review['missing_report_representation'] == '{}', 'missing report treatment')
    require(review['review_hash_matches_catalog'] is True and review['statement_hash_matches_catalog'] is True, 'catalog match')
    for entry in md['inspected_pdfs']:
        require(set(entry) == {'title', 'url', 'version', 'bytes', 'sha256', 'inspection'}, 'PDF metadata fields')
        require(entry['url'].startswith('https://') and entry['bytes'] > 0, 'PDF metadata types')
        require(len(entry['sha256']) == 64 and all(c in '0123456789abcdef' for c in entry['sha256']), 'PDF hash form')
    return md


def verify_sources(paths, md):
    if paths is None:
        return 'not_requested; offline metadata pins only'
    parsed = {}
    for key, path in zip(('catalog', 'problems', 'reports'), paths):
        raw = Path(path).read_bytes()
        size, sha, count = PINS[key]
        require(len(raw) == size and digest(raw) == sha, 'supplied corpus bytes/hash: ' + key)
        parsed[key] = json.loads(raw)
        require(len(parsed[key]) == count, 'supplied corpus count: ' + key)
    matches = [r for r in parsed['problems'] if str(r['id']) == '30000801']
    cats = [r for r in parsed['catalog'] if str(r['id']) == '30000801']
    require(len(matches) == 1 and len(cats) == 1, 'unique target rows')
    record, cat = matches[0], cats[0]
    require(record['problem_number'] == 'OWR-1591-003', 'problem number')
    reports = parsed['reports']
    require(record['problem_number'] not in reports, 'report absence changed')
    combined = json.dumps([record, reports.get(record['problem_number'], {})], sort_keys=True).encode('utf-8')
    require(len(combined) == 4537 and digest(combined) == REVIEW_SHA == cat['review_hash'], 'complete review replay')
    require(digest(record['statement'].encode('utf-8')) == STATEMENT_SHA == cat['statement_hash'], 'statement replay')
    require(cat['rank'] == 816, 'rank replay')
    return 'PASS: all three full corpus hashes/counts and complete default-sorted review replay'


def exact_controls():
    require(s.__version__ == '1.14.0', 'requires pinned SymPy 1.14.0')
    names = []
    def zero(expr, name):
        require(s.simplify(s.expand(expr)) == 0, 'exact identity failed: ' + name)
        names.append(name)
    r = s.symbols('r', positive=True)
    A, B, C = s.symbols('A B C', real=True)
    lap = lambda v: s.diff(v, r, 2) + 3 * s.diff(v, r) / r
    eta = -s.log(1 + r*r)
    zero(lap(eta) + 4*(r*r+2)/(1+r*r)**2, 'bubble Laplacian')
    zero(lap(lap(eta)) - 96/(1+r*r)**4, 'bubble bilaplacian')
    t = s.symbols('t', nonnegative=True)
    antiderivative = -1/(2*(1+t)**2) + 1/(3*(1+t)**3)
    zero(s.diff(antiderivative, t) - t/(1+t)**4, 'mass rational antiderivative')
    mass = 96*(s.limit(antiderivative, t, s.oo)-antiderivative.subs(t, 0))
    zero(mass - 16, 'mass coefficient in pi squared')
    w = A*s.log(1/r) + B + C*r*r
    v = lap(w)
    flux = 2*r**3*((r*s.diff(w,r))*s.diff(v,r)-v*s.diff(r*s.diff(w,r),r)+r*v*v/2)
    zero(s.limit(flux, r, 0) + 4*A*A, 'Pohozaev log flux with smooth radial perturbation')
    zero(2*r**3*s.diff(lap(-s.log(r)),r) - 8, 'fundamental log flux')
    z, lam = s.symbols('z lam', real=True)
    F = lam*(s.exp(2*z*z)-1)/4
    zero(s.diff(F,z)-lam*z*s.exp(2*z*z), 'primitive derivative')
    xs = s.symbols('x0:4', real=True)
    u = s.Function('u')(*xs)
    D = lambda f: sum(s.diff(f,x,2) for x in xs)
    du = D(u)
    square_rhs = u*D(du) + du*du + 4*sum(s.diff(u,x)*s.diff(du,x) for x in xs) + 2*sum(s.diff(u,x,y)**2 for x in xs for y in xs)
    zero(D(D(u*u/2))-square_rhs, 'formal arbitrary-function square-chain identity')
    xu = sum(x*s.diff(u,x) for x in xs)
    J = [xu*s.diff(du,x)-du*s.diff(xu,x)+x*du*du/2 for x in xs]
    zero(sum(s.diff(Jj,x) for Jj,x in zip(J,xs))-xu*D(du), 'formal arbitrary-function Pohozaev divergence in dimension four')
    aa, bb, cc, d1, d2 = s.symbols('a b c d1 d2', real=True)
    S1, S2 = aa+bb+cc, aa*aa+bb*bb+cc*cc
    zero((S1+d1)**2-(S2+d2) - (2*(aa*bb+aa*cc+bb*cc)+2*S1*d1+d1*d1-d2), 'weighted defect expansion')
    c, M, h = s.symbols('c M h', positive=True)
    zero(2*(M+h/M)**2-2*M*M-4*h-2*h*h/(M*M), 'exact bubble exponent expansion')
    def gap(weights):
        return sum(weights)**2-sum(x*x for x in weights)
    require(gap([Q(1)]) == 0, 'one positive weight')
    require(gap([Q(1),Q(1,2)]) == 1, 'two positive weights')
    require(gap([Q(1),Q(0)]) == 0, 'zero-weight guard')
    require(gap([Q(1),Q(1),Q(-1,2)]) == 0, 'signed-weight guard')
    require((Q(1)+Q(1,2))**2 == Q(1)+Q(1,4)+Q(1), 'primitive defect control')
    names += ['one-weight control','positive-pair obstruction','zero-weight countercontrol','signed-weight countercontrol','positive primitive-defect countercontrol']
    for n in (2,3,7,19,101):
        energy, weight = Q(1,n*n), Q(n)
        require(energy*weight == Q(1,n), 'vanishing first-moment model')
        require(energy*weight*weight == 1, 'nonvanishing second-moment model')
    names.append('exact measure-level weighted-neck controls')
    # Strict positivity provides the general proof; these finite controls are diagnostics only.
    return names


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs', nargs=3, metavar=('CATALOG','PROBLEMS','REPORTS'))
    args = parser.parse_args()
    inventory()
    md = metadata()
    replay = verify_sources(args.inputs, md)
    controls = exact_controls()
    print(json.dumps({'status':'PASS', 'verdict':EXPECTED_CLAIMS['verdict'],
                      'source_replay':replay, 'exact_control_count':len(controls),
                      'controls':controls, 'proves_full_target':False}, indent=2))

if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(json.dumps({'status':'FAIL','error':str(exc)}), file=sys.stderr)
        sys.exit(1)

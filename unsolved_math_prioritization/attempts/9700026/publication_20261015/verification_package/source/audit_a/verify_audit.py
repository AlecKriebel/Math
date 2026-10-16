#!/usr/bin/env python3
"""Pinned author artifact replay and independently written rational checks."""
import copy
import hashlib
import io
import json
import pathlib
import sys
import zipfile
from fractions import Fraction as F

ZIP_PIN = (11844, 'adc58ab6c2b52963f303582261ee603470dbf2728eee8b4546c04ba7cf9b201d')
MANIFEST_PIN = (1878, '1e2c8f73e3d7d0bb127773a089901d11d70f3f44445f08f128c399ee71c68fe9')
AUTHOR_FILES = {'README.md', 'PROOF.md', 'SOURCE_AUDIT.md', 'certificate.json',
                'verify.py', 'verification_results.json', 'PUBLIC_METADATA.json', 'MANIFEST.json'}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def pin(data):
    return len(data), hashlib.sha256(data).hexdigest()

def rational(s):
    require(type(s) is str, 'Expected a rational string')
    return F(s)

def witness(c):
    require(type(c) is dict and set(c) == {'schema', 'problem_id', 'alpha', 'beta', 'cities',
            'initial_weights', 'square_halfwidth', 'claimed_p', 'claimed_K',
            'claimed_lower_bound', 'claimed_upper_bound'}, 'Wrong certificate schema')
    require(c['schema'] == 'city-persistence-certificate-v1' and c['problem_id'] == '9700026', 'Wrong identity')
    a, b = rational(c['alpha']), rational(c['beta'])
    require(a > 1 and b > 2*a and a/b == F(1,4), 'Wrong parameter region')
    require(type(c['cities']) is list and len(c['cities']) == 3, 'Expected three sites')
    sites = []
    for row in c['cities']:
        require(type(row) is list and len(row) == 2, 'Wrong site shape')
        sites.append(tuple(map(rational, row)))
    require(type(c['initial_weights']) is list and len(c['initial_weights']) == 3, 'Wrong weight shape')
    weights = list(map(rational, c['initial_weights']))
    require(sum(weights) == 1 and min(weights) > 0, 'Wrong positive simplex')
    h = rational(c['square_halfwidth'])
    require(h > 0, 'Halfwidth must be positive')
    require(all(h < u < 1-h for site in sites for u in site), 'Strict interior-square margin failed')
    ds = [sum((sites[j][k]-sites[i][k])**2 for k in (0,1)) for i,j in [(0,1),(0,2),(1,2)]]
    require(min(ds) > 8*h*h, 'Strict separation failed')
    det = (sites[1][0]-sites[0][0])*(sites[2][1]-sites[0][1])-(sites[1][1]-sites[0][1])*(sites[2][0]-sites[0][0])
    require(det != 0 and len(set(ds)) == 3, 'Triangle genericity checks failed')
    p, k = 2*a/b, 4*h*h
    lower, upper = k*k, 1-2*k*k
    require(rational(c['claimed_p']) == p == F(1,2), 'Wrong p')
    require(rational(c['claimed_K']) == k, 'Wrong K')
    require(rational(c['claimed_lower_bound']) == lower > 0, 'Wrong lower bound')
    require(rational(c['claimed_upper_bound']) == upper < 1, 'Wrong upper bound')
    require(min(weights) >= lower, 'Initial weights below uniform bound')
    # Independent cross-multiplied influence checks at exact fourth-power states.
    count = 0
    for i in range(3):
        for s in [F(1,2),F(1,7),F(1,11),F(1,101)]:
            z = [F(0)]*3
            z[i] = s**4
            others = [j for j in range(3) if j != i]
            z[others[0]], z[others[1]] = (1-z[i])*F(2,5), (1-z[i])*F(3,5)
            for dx in [F(-1),F(-1,3),F(0),F(2,5),F(1)]:
                for dy in [F(-1),F(-1,3),F(0),F(2,5),F(1)]:
                    y = (sites[i][0]+dx*h*s, sites[i][1]+dy*h*s)
                    distance = [sum((y[t]-x[t])**2 for t in (0,1)) for x in sites]
                    for j in others:
                        require(z[i]**2*distance[j]**4 >= z[j]**2*distance[i]**4, 'Influence sample failed')
                        count += 1
    # Independent polynomial expansion of b(t)=(K+A exp(-t/2))^2.
    algebra = 0
    for u0 in [F(1,10000), k, F(1,64), F(1,3), F(3,4)]:
        v = u0-k
        require((F(0),-k*v,-v*v) == (k*k-k*k,k*v-2*k*v,-v*v), 'Scalar comparison identity failed')
        algebra += 1
    # Identity behind the audit's uniform strip estimate for local Lipschitzness.
    gradient_checks = 0
    for i,j in [(0,1),(0,2),(1,2)]:
        d2 = sum((sites[i][t]-sites[j][t])**2 for t in (0,1))
        for lam in [F(1,5),F(1),F(7,3)]:
            for y in [(F(0),F(0)),(F(1,3),F(2,3)),(F(1),F(1))]:
                f = sum((y[t]-sites[i][t])**2-lam*(y[t]-sites[j][t])**2 for t in (0,1))
                g2 = sum((2*((1-lam)*y[t]-sites[i][t]+lam*sites[j][t]))**2 for t in (0,1))
                require(g2 == 4*((1-lam)*f+lam*d2), 'Gradient identity failed')
                gradient_checks += 1
    return {'status':'PASS', 'independent_influence_checks':count, 'comparison_algebra_checks':algebra,
            'gradient_identity_checks':gradient_checks, 'squared_distances':list(map(str,ds)),
            'triangle_determinant':str(det), 'K':str(k), 'p':str(p),
            'lower':str(lower), 'upper':str(upper)}

def verify(root):
    raw = (root/'AUTHOR_SAFE_FREEZE.zip').read_bytes()
    mraw = (root/'AUTHOR_EXTERNAL_MANIFEST.json').read_bytes()
    require(pin(raw) == ZIP_PIN, 'Author archive pin mismatch')
    require(pin(mraw) == MANIFEST_PIN, 'Author external manifest pin mismatch')
    external = json.loads(mraw)
    require(external['problem_id'] == '9700026', 'Manifest identity mismatch')
    require((external['zip']['bytes'], external['zip']['sha256']) == ZIP_PIN, 'Manifest archive pin mismatch')
    require({r['path'] for r in external['files']} == AUTHOR_FILES and len(external['files']) == 8, 'Wrong manifest inventory')
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        require(set(z.namelist()) == AUTHOR_FILES and len(z.namelist()) == 8, 'Wrong archive inventory')
        require(z.testzip() is None, 'ZIP CRC failure')
        for row in external['files']:
            path = row['path']
            data = z.read(path)
            require(pin(data) == (row['bytes'], row['sha256']), 'Archive member pin mismatch: '+path)
            require((root/'author'/path).read_bytes() == data, 'Expanded author member mismatch: '+path)
    c = json.loads((root/'author'/'certificate.json').read_bytes())
    result = witness(c)
    result.update({'author_zip_bytes': ZIP_PIN[0], 'author_zip_sha256': ZIP_PIN[1],
                   'author_external_manifest_bytes': MANIFEST_PIN[0],
                   'author_external_manifest_sha256': MANIFEST_PIN[1], 'author_files_verified':8})
    if (root/'MANIFEST.json').exists():
        manifest = json.loads((root/'MANIFEST.json').read_bytes())
        paths = {r['path'] for r in manifest['files']}
        found = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.name != 'MANIFEST.json'}
        # The nested author manifest is an ordinary pinned member.
        found.add('author/MANIFEST.json')
        require(paths == found and len(paths) == len(manifest['files']), 'Audit inventory mismatch')
        for row in manifest['files']:
            require(pin((root/row['path']).read_bytes()) == (row['bytes'],row['sha256']), 'Audit member mismatch: '+row['path'])
        result['audit_manifest_verified'] = True
    return result

def self_test(root):
    base=json.loads((root/'author'/'certificate.json').read_bytes())
    mutations=[]
    for key,value in [('alpha','1'),('beta','4'),('claimed_K','1/63'),('claimed_p','1'),
                      ('claimed_lower_bound','1/4095'),('claimed_upper_bound','1'),
                      ('problem_id','9700027'),('square_halfwidth','0'),('initial_weights',{'1/6':0,'1/3':0,'1/2':0})]:
        c=copy.deepcopy(base);c[key]=value;mutations.append((key,c))
    c=copy.deepcopy(base);c['cities'][0]=c['cities'][1];mutations.append(('coincident',c))
    c=copy.deepcopy(base);c['cities'][0][0]='0';mutations.append(('boundary',c))
    c=copy.deepcopy(base);c['initial_weights'][0]='0';mutations.append(('zero weight',c))
    c=copy.deepcopy(base);c['extra']='x';mutations.append(('extra field',c))
    rejected=[]
    for label,c in mutations:
        try:witness(c)
        except (ValueError,TypeError,KeyError,ZeroDivisionError):rejected.append(label)
        else:raise ValueError('Accepted invalid mutation: '+label)
    good=copy.deepcopy(base);good['alpha']='5';good['beta']='20';witness(good)
    good=copy.deepcopy(base);good['cities'][0][0]='201/1000';witness(good)
    return {'status':'PASS','negative_controls':rejected,'positive_controls':['exponents 5,20','nearby position']}

if __name__ == '__main__':
    root=pathlib.Path(__file__).resolve().parent
    require(sys.argv[1:] in ([],['--self-test']), 'Usage: verify_audit.py [--self-test]')
    print(json.dumps(self_test(root) if sys.argv[1:] else verify(root), indent=2, sort_keys=True))

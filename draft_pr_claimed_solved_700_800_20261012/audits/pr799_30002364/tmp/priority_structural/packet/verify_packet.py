#!/usr/bin/env python3
"""Authenticated closed authored inventory plus exact finite arithmetic; no geometry formalization."""
import hashlib
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path
import sys

def need(ok, message):
    if not ok:
        raise ValueError(message)

def unique(pairs):
    result = {}
    for k, v in pairs:
        need(k not in result, 'duplicate JSON key')
        result[k] = v
    return result

def read_json(p):
    return json.loads(p.read_text(), object_pairs_hook=unique)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def trim(a):
    a = list(a)
    while len(a) > 1 and not a[-1]:
        a.pop()
    return a

def mul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i+j] += x*y
    return trim(r)

def add(a, b):
    return trim([(a[i] if i < len(a) else 0)+(b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b)))])

def rem(a, b, p):
    a = trim([x % p for x in a])
    while len(a) >= len(b) and any(a):
        z = a[-1] * pow(b[-1], -1, p) % p
        d = len(a)-len(b)
        for i, x in enumerate(b):
            a[d+i] = (a[d+i]-z*x) % p
        a = trim(a)
    return a

def qm(a, b):
    return (a[0]*b[0]-2*a[1]*b[1], a[0]*b[1]+a[1]*b[0])

def qa(a, b):
    return (a[0]+b[0], a[1]+b[1])

def qs(n, a):
    return (n*a[0], n*a[1])

def qp(a, n):
    r = (1, 0)
    for unused in range(n):
        r = qm(r, a)
    return r

def qpoly(a, b):
    r = [(0, 0)] * (len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i+j] = qa(r[i+j], qm(x, y))
    return r

def evalp(a, x):
    r = Q(0)
    for c in reversed(a):
        r = r*x+c
    return r

def rank(rows):
    a = [[Q(x) for x in r] for r in rows]
    n = 0
    for j in range(len(a[0])):
        k = next((k for k in range(n, len(a)) if a[k][j]), None)
        if k is None:
            continue
        a[n], a[k] = a[k], a[n]
        z = a[n][j]
        a[n] = [x/z for x in a[n]]
        for k in range(len(a)):
            if k != n:
                z = a[k][j]
                a[k] = [x-z*y for x,y in zip(a[k],a[n])]
        n += 1
    return n

def hull(points):
    h = []
    for x, y in points:
        while len(h) > 1:
            a,b = h[-2:]
            if (b[1]-a[1])*(x-b[0]) < (y-b[1])*(b[0]-a[0]):
                break
            h.pop()
        h.append((Q(x),Q(y)))
    return h

def arithmetic(d):
    need(d['target'] == 30002364 and d['pr'] == 799, 'wrong target')
    need(d['conclusion'] == 'prior_ingredients_supply_full_forward_negation', 'scope drift')
    for k in ['explicit_published_answer_located','historical_firstness_certified',
              'current_worldwide_open_status_certified']:
        need(d[k] is False, 'unjustified historical scope')
    need(d['predecessor_chain_available_by'] == '2024-12-04', 'date drift')
    need(d['controls_do_not_formalize_geometry'] is True, 'geometry overclaim')
    need(set(d['necessary_sources']) == {'ribet1980','milne2001','afv2024'}, 'source-chain drift')
    need(len(d['geometric_dependencies']) == 6, 'missing geometric dependencies')
    p = d['polynomial_ascending']
    need(p == [8,-8,2,0,1,-2,1], 'wrong predecessor polynomial')
    need(d['quadratic_field_w_square'] == -2, 'wrong quadratic field')
    f = [tuple(x) for x in d['cubic_over_quadratic_ascending']]
    fc = [(a,-b) for a,b in f]
    need(qpoly(f,fc) == [(x,0) for x in p], 'quadratic factorization')
    # T^3 conjugate(F)(2/T) = -2w F(T).
    lhs = [qs(2**(3-i),fc[3-i]) for i in range(4)]
    need(lhs == [qm((0,-2),x) for x in f], 'reciprocity identity')
    c,b,a,one = f
    need(one == (1,0), 'nonmonic cubic')
    disc = (0,0)
    for x in [qm(qp(a,2),qp(b,2)), qs(-4,qp(b,3)),
              qs(-4,qm(qp(a,3),c)), qs(-27,qp(c,2)), qs(18,qm(qm(a,b),c))]:
        disc = qa(disc,x)
    need(disc == (142,0), 'cubic discriminant')
    need(11**2 < 142 < 12**2, 'nonsquare check')
    prime = d['irreducibility_prime']
    need(prime == 7, 'irreducibility-prime drift')
    divisions = 0
    for degree in (1,2,3):
        for cs in itertools.product(range(prime), repeat=degree):
            divisions += 1
            need(any(rem(p,list(cs)+[1],prime)), 'reducible modulo 7')
    r = d['trace_polynomial_ascending']
    need(r == [8,-5,-2,1], 'trace cubic drift')
    # Expand T^3 R(T+2/T) using Laurent exponents.
    laurent = {}
    for n,cn in enumerate(r):
        from math import comb
        for k in range(n+1):
            power = 3+n-2*k
            laurent[power] = laurent.get(power,0)+cn*comb(n,k)*2**k
    need(all(v == (p[k] if 0 <= k < len(p) else 0) for k,v in laurent.items()), 'Weil trace identity')
    intervals = [(Q(-141,50),Q(-2)),(Q(1),Q(2)),(Q(2),Q(141,50))]
    need(all(evalp(r,a)*evalp(r,b) < 0 for a,b in intervals), 'trace root intervals')
    need(Q(141,50)**2 < 8, 'trace root absolute bound')
    nh = hull([(0,Q(3,2)),(1,Q(1,2)),(2,0),(3,0)])
    need(nh == [(Q(0),Q(3,2)),(Q(1),Q(1,2)),(Q(2),Q(0)),(Q(3),Q(0))], 'Newton polygon')
    rows = sorted(set(itertools.permutations((-1,0,1))))
    cols = [tuple(row[i] for row in rows) for i in range(3)]
    signed = cols+[tuple(-x for x in c) for c in cols]
    # S3 and global conjugation; distinct rows form the S3 orbit.
    permutations = list(itertools.permutations(range(3)))
    group = {(perm,sign) for perm in permutations for sign in (-1,1)}
    norm = qs(-1,c)
    eigen = qs(Q(1,8),qp(norm,2))
    computed = {'irreducibility_divisions':divisions,'cubic_discriminant':list(disc),
                'P_at_2':int(evalp(p,Q(2))),'centered_rank':rank(rows),
                'signed_distinct_columns':len(set(signed)), 'group_order':len(group),
                'root_of_unity_eigenvalue':[int(x) for x in eigen]}
    need(computed == d['expected'], 'arithmetic result drift')
    need(all(sum(row)==0 for row in rows), 'norm relation valuation')
    need(rank(rows)==2 and len(set(signed))==6, 'all-powers obstruction premises')
    return computed

def main():
    need(len(sys.argv)==4, 'usage: verify_packet.py ROOT MANIFEST_SHA256 CHECKER_SHA256')
    root = Path(sys.argv[1]).absolute()
    for x in [root,*root.parents]:
        need(not x.is_symlink(), 'symlink in root path')
    me = Path(__file__).absolute()
    need(me == root/'verify_packet.py', 'checker location mismatch')
    need(not me.is_symlink() and sha(me)==sys.argv[3], 'checker SHA mismatch')
    mp = root/'MANIFEST.json'
    need(not mp.is_symlink() and sha(mp)==sys.argv[2], 'manifest SHA mismatch')
    manifest = read_json(mp)
    need(manifest['schema']=='pr799-structural-authored-v1', 'manifest schema')
    files = manifest['files']
    need(isinstance(files,dict), 'manifest inventory')
    actual = set()
    for q in root.rglob('*'):
        need(not q.is_symlink(), 'symlink member')
        need(q.is_file(), 'unexpected directory or special file')
        actual.add(q.name)
    need(actual==set(files)|{'MANIFEST.json'}, 'closed inventory mismatch')
    for name,digest in files.items():
        need(Path(name).name==name and name not in ('.','..'), 'unsafe member name')
        need(sha(root/name)==digest, 'member SHA mismatch: '+name)
    freeze = read_json(root/'INITIAL_FREEZE.json')
    need(freeze['no_candidate_or_other_audit_read'] is True, 'independence record')
    for name,digest in freeze['files'].items():
        need(sha(root/name)==digest, 'initial freeze mismatch')
    retrievals=read_json(root/'RETRIEVAL_LEDGER.json')
    success={r['id'] for r in retrievals if r['status']=='retrieved'}
    data=read_json(root/'ARITHMETIC_DATA.json')
    need(set(data['necessary_sources']) <= success, 'unretrieved necessary primary')
    scopes={s['source']:s for s in read_json(root/'READING_SCOPES.json')}
    need(set(data['necessary_sources']) <= set(scopes), 'uninspected necessary primary')
    need('p22' in scopes['afv2024']['read_scope'], 'missing predecessor table scope')
    results=arithmetic(data)
    print(json.dumps({'status':'PASS','finite_arithmetic':results,
                      'geometry_formalized':False,'historical_firstness_certified':False},sort_keys=True))

if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        print('FAIL: '+str(exc),file=sys.stderr)
        sys.exit(1)

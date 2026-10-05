#!/usr/bin/env python3
"""Independent exact regression and binding audit for the frozen EP-655 packet.

Uses integer Ramanujan trace norms, not the author's cyclotomic remainder code.
Finite controls supplement the separately reviewed all-n proof. No network.
"""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from math import gcd
from pathlib import Path
import argparse
import json
import subprocess
import sys
import tempfile
import zipfile

PIN_ARCHIVE = 'e5d6e7b26638daf7cedcc4e20456bb3bef3af3e5df3686ffa312164c3e072615'
PIN_MANIFEST = '8c709f826b2646098379f87aa3b1a56a54f1486fb1839a6283f7159a12c07b56'
EXPECTED_FILES = {'PROOF.md','REPORT.md','RESEARCH_LOG.md','SOURCES.json','STATUS.json',
 'VERIFICATION.json','VERIFICATION_METADATA.json','verify.py','verify_manifest.py','MANIFEST.json'}
checks = Counter()

def check(condition, label):
    checks[label] += 1
    if not condition:
        raise RuntimeError('Failed: ' + label)

@lru_cache(None)
def divisors(n):
    return tuple(d for d in range(1, n+1) if n % d == 0)

@lru_cache(None)
def mu(n):
    # Independent factorization definition of the Mobius function.
    result, p = 1, 2
    while p*p <= n:
        if n % p == 0:
            n //= p
            result = -result
            if n % p == 0:
                return 0
        while n % p == 0:
            n //= p
        p += 1
    return -result if n > 1 else result

@lru_cache(None)
def ramanujan(n, k):
    return sum(d*mu(n//d) for d in divisors(gcd(n,k)))

def trace_norm(coefficients, n, sums):
    # Sum |q(zeta^u)|^2 over units u modulo n. This nonnegative integer
    # vanishes iff q vanishes at a primitive nth root. No approximations.
    return sum(a*b*sums[(i-j) % n]
               for i,a in coefficients.items() for j,b in coefficients.items())

def chord_poly(n,k):
    c = Counter({0:2})
    c[k] -= 1
    c[(-k) % n] -= 1
    return {i:a for i,a in c.items() if a}

def squared_fibers(points):
    result=[]
    for i,(x,y) in enumerate(points):
        result.append(Counter((x-u)**2+(y-v)**2
            for j,(u,v) in enumerate(points) if i != j))
    return result

def admissible(points):
    if len(set(points)) != len(points):
        raise ValueError('Repeated points are outside the finite-set model')
    return all(all(d>0 and multiplicity <= 2 for d,multiplicity in f.items())
               for f in squared_fibers(points))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--author-dir',type=Path,required=True)
    ap.add_argument('--archive',type=Path,required=True)
    args=ap.parse_args()
    root=args.author_dir.resolve()
    archive=args.archive.read_bytes()
    check(len(archive)==15683,'archive_byte_count')
    check(sha256(archive).hexdigest()==PIN_ARCHIVE,'archive_sha256')
    manifest=(root/'MANIFEST.json').read_bytes()
    check(sha256(manifest).hexdigest()==PIN_MANIFEST,'manifest_sha256')
    m=json.loads(manifest)
    check({p.name for p in root.iterdir()}==EXPECTED_FILES,'author_inventory')
    check(len(m['files'])==9,'author_payload_count')
    for item in m['files']:
        p=root/item['path']
        check(not p.is_symlink() and p.is_file(),'author_regular_file')
        b=p.read_bytes()
        check(len(b)==item['bytes'] and sha256(b).hexdigest()==item['sha256'],
              'author_payload_binding')
    with zipfile.ZipFile(args.archive) as z:
        names=z.namelist()
        check(len(names)==len(set(names))==10,'archive_unique_inventory')
        check(set(names)==EXPECTED_FILES,'archive_inventory')
        for name in names:
            check(z.read(name)==(root/name).read_bytes(),'archive_matches_directory')
    # Replays inspect the author code but do not count as independent arithmetic.
    expected=(root/'VERIFICATION.json').read_bytes()
    for flags in ([],['-O']):
        r=subprocess.run([sys.executable,'-B',*flags,str(root/'verify.py')],
                         capture_output=True,check=True)
        check(r.stdout==expected and not r.stderr,'author_replay_byte_identical')
    v=json.loads(expected)
    check(v['total_checks']==sum(v['counts'].values())==711511,'author_total_accounting')
    check(v['counts']['exact_chord_equality']==sum(k*k for k in range(1,128)),
          'author_equality_count_accounting')
    check(v['counts']['distance_graph_regularity']==sum(n//2 for n in range(2,65)),
          'author_graph_count_accounting')
    # A complete second algorithm for equal-chord detection.
    for n in range(2,129):
        sums=[ramanujan(n,k) for k in range(n)]
        phi=sum(gcd(u,n)==1 for u in range(n))
        check(sums[0]==phi,'ramanujan_zero_is_totient')
        polys={k:chord_poly(n,k) for k in range(1,n)}
        for a in range(1,n):
            check(trace_norm(polys[a],n,sums)>0,'independent_positive_chord')
            for b in range(1,n):
                q=dict(polys[a])
                for i,c in polys[b].items():
                    q[i]=q.get(i,0)-c
                q={i:c for i,c in q.items() if c}
                norm=trace_norm(q,n,sums)
                check(norm>=0 and (norm==0)==(a==b or a+b==n),
                      'ramanujan_chord_equality')
        fibers=Counter(min(k,n-k) for k in range(1,n))
        check(len(fibers)==n//2 and max(fibers.values())<=2,
              'independent_cardinality_and_admissibility')
        check(sorted(fibers.values())==sorted([2]*((n-1)//2)+([1] if n%2==0 else [])),
              'independent_parity_multiplicities')
        for c in [Fraction(1,1),Fraction(1,100),Fraction(1,10**12)]:
            check(Fraction(n//2)<(1+c)*n/2,'rational_strict_counterexample')
        if n<=64:
            for k in range(1,n//2+1):
                edges={tuple(sorted((i,(i+k)%n))) for i in range(n)}
                degree=Counter(t for edge in edges for t in edge)
                expected_degree=1 if 2*k==n else 2
                check(set(degree.values())=={expected_degree} and len(degree)==n,
                      'independent_graph_degrees')
                check(len(edges)==(n//2 if 2*k==n else n),
                      'independent_graph_edge_counts')
    for n in range(1,10001):
        # Unlike integer-division rewriting, search for the least integer d
        # whose double can accommodate n-1 points.
        d=n//2
        check(2*d>=n-1 and (d==0 or 2*(d-1)<n-1),'integral_lower_bound')
    square=[(1,0),(0,1),(-1,0),(0,-1)]
    check(admissible(square),'square_admissible')
    check(not admissible(square+[(0,0)]),'circumcenter_invalidates')
    check(set().union(*(set(f) for f in squared_fibers(square)))=={2,4},'square_two_lengths')
    check(admissible([(0,0)]) and squared_fibers([(0,0)])==[Counter()], 'singleton')
    # Convexity alone does not imply the centered-circle condition.
    convex_invalid=[(Fraction(0),Fraction(0)),(Fraction(3,5),Fraction(-4,5)),
                    (Fraction(1),Fraction(0)),(Fraction(3,5),Fraction(4,5))]
    crosses=[]
    for i in range(4):
        a,b,c=[convex_invalid[(i+j)%4] for j in range(3)]
        crosses.append((b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-b[0]))
    check(all(x>0 for x in crosses),'convex_invalid_control_is_convex')
    check(not admissible(convex_invalid),'convexity_not_admissibility')
    line=[(i,0) for i in range(5)]
    check(admissible(line),'nonminimal_admissible_line')
    check(len(set().union(*(set(f) for f in squared_fibers(line))))==4>5//2,
          'minimum_is_not_every_set')
    # Test the author's integrity rejection using disposable archive copies.
    for mutation in ['modified','missing','extra','symlink']:
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)
            with zipfile.ZipFile(args.archive) as z:
                z.extractall(folder)
            if mutation=='modified':
                with (folder/'PROOF.md').open('a') as f: f.write('\nALTERED\n')
            elif mutation=='missing':
                (folder/'PROOF.md').unlink()
            elif mutation=='extra':
                (folder/'UNEXPECTED.txt').write_text('extra')
            elif mutation=='symlink':
                (folder/'PROOF.md').unlink()
                (folder/'PROOF.md').symlink_to(folder/'REPORT.md')
            r=subprocess.run([sys.executable,'-B',str(folder/'verify_manifest.py')],
                             capture_output=True)
            check(r.returncode!=0,'negative_integrity_'+mutation)
    print(json.dumps({'status':'PASS','author_archive_sha256':PIN_ARCHIVE,
        'author_manifest_sha256':PIN_MANIFEST,'author_replay_checks_each':711511,
        'independent_method':'Integer Ramanujan trace norms plus rational and graph controls',
        'independent_chord_n_range':[2,128],
        'counts':dict(sorted(checks.items())),'total_checks':sum(checks.values()),
        'limits':'Finite exact controls, not an all-n proof or proof-assistant certificate.'},
        indent=2,sort_keys=True))

if __name__=='__main__': main()

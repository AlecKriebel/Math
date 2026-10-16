#!/usr/bin/env python3
"""Bounded exact checks for crossing/halving partial results, not a solver."""
import argparse
import ast
from fractions import Fraction
import hashlib
from itertools import combinations
import json
from math import comb
import os
from pathlib import Path
from random import Random
import sys
sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def reject(fn, fragment):
    try:
        fn()
    except (RuntimeError, ValueError) as exc:
        require(fragment in str(exc), 'wrong negative-control rejection')
        return
    raise RuntimeError('negative control was accepted')


def orient(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])


def validate(points):
    require(type(points) in (list, tuple), 'point list required')
    require(3 <= len(points) <= 16, 'bounded size: require 3 through 16')
    require(all(type(p) in (list, tuple) and len(p) == 2 for p in points), 'two coordinates required')
    require(all(type(v) in (int, Fraction) for p in points for v in p), 'exact coordinates required')
    require(all(abs(v) <= 10**9 for p in points for v in p), 'coordinate size guard')
    require(len(set(map(tuple, points))) == len(points), 'repeated point')
    require(all(orient(*triple) != 0 for triple in combinations(points, 3)), 'collinear triple')


def hull_size(points):
    points = sorted(map(tuple, points))
    def half(seq):
        out = []
        for p in seq:
            while len(out) >= 2 and orient(out[-2], out[-1], p) <= 0:
                out.pop()
            out.append(p)
        return out
    return len(half(points)[:-1] + half(points[::-1])[:-1])


def edges(points):
    n = len(points)
    e = [0]*((n-2)//2+1)
    for i, j in combinations(range(n), 2):
        left = sum(orient(points[i], points[j], points[k]) > 0 for k in range(n) if k not in (i,j))
        e[min(left, n-2-left)] += 1
    return e


def crossing(a,b,c,d):
    return orient(a,b,c)*orient(a,b,d) < 0 and orient(c,d,a)*orient(c,d,b) < 0


def crossing_counts(points):
    segment_pairs = convex_sets = 0
    for a,b,c,d in combinations(points, 4):
        pairs = sum((crossing(a,b,c,d), crossing(a,c,b,d), crossing(a,d,b,c)))
        require(pairs in (0,1), 'a quadruple has invalid crossing multiplicity')
        segment_pairs += pairs
        convex_sets += hull_size((a,b,c,d)) == 4
    require(segment_pairs == convex_sets, 'independent crossing methods disagree')
    return segment_pairs


def metrics(points):
    validate(points)
    n = len(points); e = edges(points); c = crossing_counts(points)
    m = len(e)-1; N = comb(n,2); w = [j*(n-2-j) for j in range(m+1)]
    require(sum(e) == N and e[0] == hull_size(points), 'edge partition or hull count failed')
    require(c + sum(a*b for a,b in zip(w,e)) == 3*comb(n,4), 'quadrilateral identity failed')
    E = [sum(e[:k+1]) for k in range(m)]
    weights = [n-3-2*k for k in range(m)]
    require(all(x>0 for x in weights), 'nonpositive cumulative coefficient')
    require(c == 3*comb(n,4)-w[m]*N+sum(a*b for a,b in zip(weights,E)), 'summation by parts failed')
    if m:
        require(e[-1] == N-E[-1], 'halving complement failed')
        require(weights[-1] == (1 if n%2==0 else 2), 'last coefficient parity failed')
    if n==3:require(c==0 and e[-1]==3,'triangle identity failed')
    if n==4:require(c+e[-1]==3,'four-point identity failed')
    if n==5:require(c+2*e[-1]==15,'five-point identity failed')
    if e[0]==3 and n==6:require(c+e[-1]==9,'triangular six-point identity failed')
    if e[0]==3 and n==7:require(c+2*e[-1]==33,'triangular seven-point identity failed')
    if e[0]==3 and n==8:require(c==-15+4*e[1]+e[2] and e[-1]==10-c+3*e[1], 'triangular eight-point identity failed')
    return dict(n=n,crossings=c,halving=e[-1],edges=e)


OUTER = [(0,0),(1000,0),(0,1000)]
WITNESSES = [
    ('P', OUTER+[(578,36),(72,693),(201,510),(52,473),(56,41)], [3,6,13,6],22,6),
    ('Q', OUTER+[(171,780),(189,153),(17,28),(421,229),(171,510)], [3,7,9,9],22,9),
    ('R', OUTER+[(81,398),(957,30),(78,650),(288,498),(77,202)], [3,6,10,9],19,9)
]


def deletion_check(points):
    n = len(points); require(n>=4,'deletion size too small')
    z = metrics(points); sub = [metrics(points[:i]+points[i+1:]) for i in range(n)]
    require(sum(q['crossings'] for q in sub)==(n-4)*z['crossings'], 'crossing deletion identity failed')
    if n%2:
        expected = (n-1)//2*z['halving']
    else:
        expected = (n-2)*z['halving'] + n//2*z['edges'][n//2-2]
    require(sum(q['halving'] for q in sub)==expected, 'halving deletion identity failed')
    return n


def auxiliary_fixtures():
    rng = Random(195377)
    out = []
    for n in range(3,11):
        for sample in range(12):
            for attempt in range(100):
                p = [(rng.randrange(-99,100),rng.randrange(-99,100)) for _ in range(n)]
                if len(set(p))==n and all(orient(*t)!=0 for t in combinations(p,3)):
                    out.append(p);break
            else:raise RuntimeError('fixture generation bound exceeded')
    return out


def mutation_checks():
    rng = Random(61561); count = 0; changes = []
    for n in range(3,13):
        for k in range(n-2):
            for attempt in range(100):
                rest = [(rng.randrange(-100,101),rng.randrange(20,201)*(1 if j<k else -1)) for j in range(n-3)]
                a = [(Fraction(0),Fraction(1,10**6)),(-10,0),(10,0)]+rest
                b = [(Fraction(0),-Fraction(1,10**6)),(-10,0),(10,0)]+rest
                triples = list(combinations(range(n),3))
                signs_a = [orient(*(a[i] for i in t)) for t in triples]
                signs_b = [orient(*(b[i] for i in t)) for t in triples]
                if 0 in signs_a or 0 in signs_b:continue
                changed = [t for t,x,y in zip(triples,signs_a,signs_b) if x*y<0]
                if changed==[(0,1,2)]:break
            else:raise RuntimeError('mutation fixture generation bound exceeded')
            x = metrics(a);y = metrics(b); dc = y['crossings']-x['crossings']; dh = y['halving']-x['halving']
            require(dc==2*k-n+3,'single mutation crossing formula failed')
            critical = 1 if n%2==0 else 2
            expected_h = (1 if dc<0 else -1) if abs(dc)==critical else 0
            require(dh==expected_h,'single mutation halving formula failed')
            if dc<0:require(dh>=0,'decreasing crossing reduced halving')
            if dc==0:require(n%2==1 and y['edges']==x['edges'],'zero-cost mutation changed profile')
            count += 1;changes.append((n,k,dc,dh))
    return dict(fixtures=count,orders=list(range(3,13)),changes=changes)


def algebra_checks():
    # Finite arithmetic regression for general identities proven in the report.
    checks = 0
    for n in range(4,101):
        m=(n-2)//2; w=[j*(n-2-j) for j in range(m+1)]
        for k in range(m):
            require(w[k+1]-w[k]==n-3-2*k>0,'weight-difference identity failed')
            checks += 1
    # Regression for the audit correction: E is integral, E-L need not be.
    # n=4, a triangular-hull configuration: C=0, E_0=3, A_4=-3, a_0=1.
    lower = Fraction(5, 2)
    slack = Fraction(3)-lower
    budget = Fraction(0)-(-3)-lower
    require(slack > budget//1, 'rational lower-bound counterexample lost')
    require(slack <= (lower+budget)//1-lower, 'corrected real-bound rounding failed')
    # Integer-profile exchange is realized by P and Q above.
    delta=[0,1,-4,3]
    require(sum(delta)==0 and sum(j*(6-j)*v for j,v in enumerate(delta))==0,'profile exchange not crossing neutral')
    require(delta[-1]==3,'profile exchange halving change failed')
    return checks


def mathematics():
    witnesses = []
    for name,p,e,c,h in WITNESSES:
        z=metrics(p)
        require(z['edges']==e and z['crossings']==c and z['halving']==h,'witness count mismatch '+name)
        require(all(x>0 and y>0 and x+y<1000 for x,y in p[3:]),'inner point outside triangle')
        deletion_check(p);witnesses.append(dict(name=name,**z))
    require(witnesses[0]['crossings']==witnesses[1]['crossings']>witnesses[2]['crossings'],'nonoptimality certificate failed')
    require(witnesses[0]['halving']<witnesses[1]['halving'],'unequal-halving certificate failed')
    fixtures=auxiliary_fixtures();deletions=0
    for p in fixtures:
        metrics(p)
        if len(p)>=4:deletions+=deletion_check(p)
    reject(lambda:validate([(0,0),(1,1),(2,2)]),'collinear triple')
    reject(lambda:validate([(0,0),(1,0),(1,0)]),'repeated point')
    reject(lambda:validate([(0.,0),(1,0),(0,1)]),'exact coordinates')
    reject(lambda:validate([(False,0),(1,0),(0,1)]),'exact coordinates')
    reject(lambda:validate([(i,i*i) for i in range(17)]),'bounded size')
    reject(lambda:validate([(0,0),(10**10,0),(0,1)]),'coordinate size')
    reject(lambda:validate([(0,0),(1,1)]),'bounded size')
    return dict(witnesses=witnesses,auxiliary_fixtures=len(fixtures),auxiliary_vertex_deletions=deletions,
                witness_vertex_deletions=24,mutation=mutation_checks(),weight_identities=algebra_checks(),negative_input_controls=7)


def verify_pins():
    pins=json.loads((BASE/'PAYLOAD_PINS.json').read_text())
    require(pins.get('schema')==1,'unknown pin schema')
    files=pins.get('files');require(isinstance(files,list) and files,'empty pin list')
    require(len({x['path'] for x in files})==len(files),'duplicate pinned file')
    require({p.name for p in BASE.iterdir() if p.name!='PAYLOAD_PINS.json'}=={x['path'] for x in files},'payload file set changed')
    for x in files:
        p=BASE/x['path'];require(p.parent==BASE and p.is_file() and not p.is_symlink(),'invalid pinned file')
        data=p.read_bytes();require(len(data)==x['bytes'],'pinned byte count mismatch: '+x['path'])
        require(hashlib.sha256(data).hexdigest()==x['sha256'],'pinned hash mismatch: '+x['path'])
    status=json.loads((BASE/'STATUS.json').read_text())
    require(status['problem_id']==7200057 and status['outcome']=='exhausted' and status['substantive_proof_search_approaches']==5,'research status drift')
    require(status['full_target_resolved'] is False,'false resolution status')
    manifest=json.loads((BASE/'SOURCE_MANIFEST.json').read_text())
    require(manifest['source_bodies_in_payload'] is False,'source bodies forbidden')
    require(not any(isinstance(x,ast.Assert) for x in ast.walk(ast.parse(Path(__file__).read_text()))),'checker contains assert')
    return dict(pinned_files=len(files),all_hashes_matched=True,no_assert_nodes=True)


def readonly_probes():
    require(os.geteuid()==1000,'read-only verification requires UID 1000')
    require(not os.access(BASE,os.W_OK),'packet directory is writable')
    probe=BASE/('.write_probe_'+str(os.getpid()));require(not probe.exists(),'write probe collision')
    try:fd=os.open(probe,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
    except PermissionError:pass
    else:
        os.close(fd);probe.unlink();raise RuntimeError('packet create unexpectedly succeeded')
    denied=0
    for p in BASE.iterdir():
        require(p.is_file() and not p.is_symlink(),'unexpected probe entry')
        require(not os.access(p,os.W_OK),'packet file is writable')
        try:fd=os.open(p,os.O_WRONLY)
        except PermissionError:denied+=1
        else:os.close(fd);raise RuntimeError('file write-open unexpectedly succeeded')
    return dict(directory_create_denied=True,existing_file_write_open_denials=denied,actual_write_probes=True)


def output_destination(value):
    p=Path(value).expanduser().resolve()
    require(p!=BASE and BASE not in p.parents,'output must be external to the packet')
    require(not p.exists(),'output already exists')
    return p


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-readonly',action='store_true');parser.add_argument('--output')
    args=parser.parse_args();out=output_destination(args.output) if args.output else None
    ro=readonly_probes() if args.require_readonly else dict(actual_write_probes=False)
    result=dict(status='passed',uid=os.geteuid(),python_optimization=sys.flags.optimize,readonly_required=args.require_readonly,
                readonly=ro,checks=dict(integrity=verify_pins(),mathematics=mathematics()),
                limits='Exact bounded checks of supplied lemmas and witnesses; no exhaustive order-type search or global extremum certificate.')
    data=json.dumps(result,sort_keys=True,indent=2)+'\n'
    if out:
        with out.open('x') as f:f.write(data)
    else:sys.stdout.write(data)


if __name__=='__main__':
    try:main()
    except Exception as exc:
        sys.stderr.write(type(exc).__name__+': '+str(exc)+'\n');sys.exit(1)

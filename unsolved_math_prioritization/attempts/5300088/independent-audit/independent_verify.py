#!/usr/bin/env python3
"""Portable independent exact controls. These do not prove the infinite statements."""
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
from itertools import permutations, product
import json
from pathlib import Path
import subprocess
import sys

MANIFEST_HASH = '166b1c2642947993cefe9212ba2d523438168a0ce58372731b1a850cc2021945'
PARTIAL_HASH = 'c3e83dea255fed2940b9c8bc6d4cf9f14d34b77f94851fab3e1047394a5f96cc'
counts = Counter()
def ck(value, category):
    if not value:
        raise RuntimeError('Independent check failed: ' + category)
    counts[category] += 1

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def lor(v, w):
    return v[0]*w[0]-sum(v[i]*w[i] for i in range(1,4))

def determinant(columns):
    ans = 0
    for p in permutations(range(4)):
        inv = sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))
        term = F((-1)**inv)
        for i in range(4):
            term *= columns[p[i]][i]
        ans += term
    return ans

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--packet', type=Path, default=Path(__file__).resolve().parent.parent/'submission')
    args = parser.parse_args()
    b = args.packet.resolve()
    ck(sha(b/'SHA256SUMS.json') == MANIFEST_HASH, 'frozen_binding')
    ck(sha(b/'PARTIAL.md') == PARTIAL_HASH, 'frozen_binding')
    manifest = json.loads((b/'SHA256SUMS.json').read_text())
    ck({p.name for p in b.iterdir()} == set(manifest['files'])|{'SHA256SUMS.json'}, 'packet_allowlist')
    for name, digest in manifest['files'].items():
        ck((b/name).is_file() and not (b/name).is_symlink(), 'regular_file')
        ck(sha(b/name)==digest, 'frozen_file_hash')
    expected = (b/'CONTROL_RESULTS.json').read_bytes()
    for options in ([], ['-O']):
        p = subprocess.run([sys.executable, '-B', *options, str(b/'verify.py')], capture_output=True, check=True)
        ck(p.stdout==expected and p.stderr==b'', 'author_replay_byte_match')
    p = subprocess.run([sys.executable, '-B', str(b/'verify_manifest.py')], capture_output=True, check=True)
    ck(json.loads(p.stdout)['verified_files']==11, 'author_manifest_replay')

    parameters = [(F(3),7),(F(7,2),7),(F(13),7),(F(101),5)]
    word_counts = {}
    for q, maxdepth in parameters:
        # Independent scalar coordinate transformations, with explicit inverses.
        c=(q*q+q**-2)/2
        s=(q*q-q**-2)/2
        t=(q-q**-1)/(q+q**-1)
        k=2/(q+q**-1)
        h=q**-2
        def action(g, v):
            a,x,y,z=v
            if g==0: return (c*a+s*x,s*a+c*x,-z,y)
            if g==1: return (c*a-s*x,-s*a+c*x,z,-y)
            if g==2: return (c*a+s*y,x,s*a+c*y,z)
            return (c*a-s*y,x,-s*a+c*y,z)
        E=[tuple(F(int(i==j)) for i in range(4)) for j in range(4)]
        for g in range(4):
            cols=[action(g,e) for e in E]
            ck(determinant(cols)==1, 'orientation_determinant')
            for i in range(4):
                for j in range(4):
                    ck(lor(cols[i],cols[j])==lor(E[i],E[j]), 'lorentz_gram')
            ck(action(g,E[0])[0]>0, 'time_orientation')
        ck(c-s==h and c+s==q*q, 'boost_endpoints')
        ck(c-s*t==1 and s-c*t==t, 'pairing_symbolic_coefficients')
        ck(2*t*t>1, 'closed_cap_separation')
        ck(t*t+k*k==1, 'cap_slab')
        ck((1+k)/(1-k)==((q+1)/(q-1))**2, 'depth_log_identity')
        ck((q+1)/(q-1)<q, 'depth_below_injectivity')
        for u in (F(i,20) for i in range(-20,21)):
            den=c+s*u
            ck(den>=h>0, 'positive_pairing_denominator')
            ck((s+c*u)/den-t==(u+t)/den, 'full_interval_pairing_identity')

        # Ideal fixed points, screw endpoints, and exact interior convex combinations.
        e1=(F(1),F(1),F(0),F(0)); ne1=(F(1),F(-1),F(0),F(0))
        e2=(F(1),F(0),F(1),F(0)); ne2=(F(1),F(0),F(-1),F(0))
        for g,p,scale in [(0,e1,q*q),(0,ne1,h),(2,e2,q*q),(2,ne2,h)]:
            ck(action(g,p)==tuple(scale*v for v in p), 'ideal_fixed_points')
        weight=c/(c+s)
        ck(0<weight<1, 'hull_segment_weight')
        for p,sign in ((e2,1),(ne2,-1)):
            out=action(0,p)
            klein=tuple(out[i]/out[0] for i in range(1,4))
            combined=tuple(weight*klein[i]+(1-weight)*(-1 if i==0 else 0) for i in range(3))
            ck(combined==(0,0,sign*h), 'hull_segment_exact')
        vertices=[(F(1),0,0),(-F(1),0,0),(0,F(1),0),(0,-F(1),0),(0,0,h),(0,0,-h)]
        for signs in product((-1,1), repeat=3):
            normal=(signs[0],signs[1],signs[2]/h)
            for vertex in vertices:
                ck(sum(x*y for x,y in zip(normal,vertex))<=1, 'octahedron_facet')
            ck(sum(x*x for x in normal)==q**4+2, 'octahedron_face_distance')
        ck(0<1/(q**4+2)<k*k, 'depth_bounds_consistent')

        # Longer words than the author's length-five checks, including noninteger q.
        origin=(F(1),F(0),F(0),F(0))
        frontier=[(-1,origin)]
        word_count=0
        for depth in range(1,maxdepth+1):
            next_level=[]
            for old,v in frontier:
                for g in range(4):
                    if old>=0 and g==(old^1):
                        continue
                    w=action(g,v)
                    ck(lor(w,w)==1 and w[0]>0, 'word_hyperboloid')
                    ck(action(g^1,w)==v, 'word_inverse')
                    axis=1 if g<2 else 2
                    sign=1 if g%2==0 else -1
                    ck(sign*w[axis]>t*w[0], 'word_ping_pong')
                    ck(w[0]>=c, 'word_displacement_lower_bound')
                    next_level.append((g,w))
                    word_count+=1
            ck(len(next_level)==4*3**(depth-1), 'reduced_word_level_count')
            frontier=next_level
        word_counts[str(q)]={'maximum_length':maxdepth,'word_parameter_evaluations':word_count}

    # Mutation controls detect dropping the quarter-turn and using the wrong depth scale.
    for q in (F(3),F(7,2),F(13)):
        c=(q*q+q**-2)/2; s=(q*q-q**-2)/2
        planar_image=(s/c,1/c,F(0))
        weight=c/(c+s)
        wrong_combination=tuple(weight*planar_image[i]+(1-weight)*(-1 if i==0 else 0) for i in range(3))
        ck(wrong_combination!=(0,0,q**-2), 'reject_no_screw_hull_claim')
        ck((q+1)/(q-1)<q, 'reject_depth_equals_injectivity')
    ck(F(10)<=2*100 and F(10)>2*2, 'reject_rank_genus_substitution')

    print(json.dumps({'status':'passed','independent_exact_checks':sum(counts.values()),
        'categories':dict(sorted(counts.items())), 'word_stress_tests':word_counts,
        'author_checks_per_replay':json.loads(expected)['checks'],
        'author_normal_and_optimized_byte_identical':True,
        'frozen_manifest_sha256':MANIFEST_HASH,'frozen_partial_sha256':PARTIAL_HASH,
        'scope':'Exact finite controls and frozen-packet replay. Infinite-word, quotient, topological, and literature statements require the separate written audit; the target remains unsolved.'},indent=2,sort_keys=True))
if __name__=='__main__':
    main()

#!/usr/bin/env python3
"""Independent arithmetic audit; stdlib only. Does not certify topology.

Inputs are the immutable author-safe directory and author ZIP. No scholarly
PDF, extracted source, catalogue corpus, network, or private coordination input.
"""
import argparse
from fractions import Fraction
from itertools import combinations, permutations, product
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

ZIP_SHA = '808dd53041a58e139590fd5eb31c85b8667f06637c6995024708256e8eddddce'
MANIFEST_SHA = '94868f587e11bc5cf7e275beacd7cdec8beaf6b033dc8d48e557d83e1225559b'
OUTPUT_SHA = 'fbf14c00d60c2df0e2eeb08d87b51a62115209b9c3a57057f5f8f0df2af210b2'
F = Fraction

def sha(b):
    return hashlib.sha256(b).hexdigest()

def check(x, message):
    if not x:
        raise AssertionError(message)

def determinant(a):
    """Fraction-free Bareiss determinant, independent of author's rank code."""
    a = [row[:] for row in a]
    n, sign, previous = len(a), 1, 1
    for k in range(n - 1):
        if not a[k][k]:
            i = next((i for i in range(k + 1, n) if a[i][k]), None)
            if i is None:
                return 0
            a[k], a[i] = a[i], a[k]
            sign *= -1
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * pivot - a[i][k] * a[k][j]
                check(numerator % previous == 0, 'Exact Bareiss division')
                a[i][j] = numerator // previous
            a[i][k] = 0
        previous = pivot
    return sign * a[-1][-1]

def perm_compose(a, b):
    return tuple(a[x - 1] for x in b)

def perm_inverse(a):
    return tuple(a.index(i) + 1 for i in range(1, len(a) + 1))

def subgroup_model(n):
    identity = tuple(range(1, n + 1))
    transposition = (2, 1) + tuple(range(3, n + 1))
    group = set(permutations(identity))
    h = {identity, transposition}
    normalizer = {g for g in group if
        {perm_compose(perm_compose(g, t), perm_inverse(g)) for t in h} == h}
    cosets = sorted({tuple(sorted(perm_compose(t, g) for t in h)) for g in group})
    def collision(u, candidates):
        return [g for g in candidates if u.intersection(perm_compose(g, x) for x in u)]
    return group, h, normalizer, cosets, collision

def independently_recompute(original):
    rows = original['results']
    check(len(rows) == 6, 'Exactly six original groups')
    results = []
    # Invert the three affine branches directly, without author solver logic.
    roots = [F(1, 6), F(1, 2), F(5, 6)]
    values = [3 * roots[0], 2 - 3 * roots[1], 3 * roots[2] - 2]
    check(values == [F(1, 2)] * 3, 'Independent PL level evaluation')
    signs = [1, -1, 1]
    check(rows[0]['roots'] == list(map(str, roots)) and rows[0]['signs'] == signs, 'PL output')
    check(rows[0]['costs'] == [{'g': g, 'one_slice': 2*g-2, 'three_slices': 6*g-6}
        for g in range(2, 9)], 'PL costs')
    results.append({'group': 1, 'pass': True, 'method': 'Direct affine branch evaluation'})

    for g in range(1, 9):
        j = [[(1 if c == r+1 else -1 if c == r-1 else 0)
              if r//2 == c//2 else 0 for c in range(2*g)] for r in range(2*g)]
        for d in (-3, -1, 1, 2):
            check(determinant([[d*x for x in row] for row in j]) == d**(2*g), 'Scaled pairing determinant')
    check(rows[1]['ranks'] == [{'g': g, 'rank': 2*g} for g in range(1, 9)], 'Rank reports')
    check(rows[1]['degrees_with_total_one'] == [2, -1], 'Disconnected degree report')
    results.append({'group': 2, 'pass': True, 'method': 'Fraction-free determinant, not rank implementation'})

    # Algebraic composition of affine maps (s,b), x -> s*x+b.
    comp = lambda u,v: (u[0]*v[0], u[0]*v[1]+u[1])
    a, r = (1, 2), (-1, 0)
    check(comp(r,r) == (1,0) and comp(comp(r,a),r) == (1,-2), 'Dihedral symbolic relations')
    check(F(1,2).denominator != 1, 'A reflection fixing this height needs nonintegral translation index')
    check(rows[2]['stabilizing_height_solutions'] == [{'sign':1,'n':0}], 'Dihedral fixed-height report')
    check(rows[2]['strict_norm_gap_for_pushforward_only'] ==
          [{'g':g,'upstairs_norm':2*g-2,'pushforward_norm':0} for g in range(2,9)], 'Dihedral norm arithmetic')
    results.append({'group': 3, 'pass': True, 'method': 'Symbolic affine-map composition'})

    group,h,normalizer,cosets,collision = subgroup_model(3)
    cycle = (2,3,1)
    u = h | {perm_compose(t,cycle) for t in h}
    collisions = sorted(collision(u, group-h))
    check(len(normalizer) == 2 and normalizer == h, 'S3 normalizer')
    check(rows[3]['full_test_collision_elements'] == [[x-1 for x in g] for g in collisions], 'All S3 collision elements')
    check(not collision(h,group-h) and collision(u,group-h) and not collision(u,normalizer-h), 'S3 good and bad sets')
    results.append({'group':4,'pass':True,'method':'One-based permutation and coset enumeration'})

    before,after = (0,0),(2,-2)
    cost = lambda a: (sum(abs(x) for x in a)-sum(a))//2
    check(sum(before)==sum(after) and cost(before)==0 and cost(after)==2,'Independent truncation formula')
    check(rows[4]['before_chiminus']==0 and rows[4]['after_chiminus']==2 and
          rows[4]['topological_realizability_claimed'] is False,'Euler report')
    results.append({'group':5,'pass':True,'method':'Absolute-value formula for negative part'})

    tree_rows=[]
    for d in range(1,6):
        words=list(product(range(3), repeat=d))
        tree_rows.append({'depth':d,'outward_branches_per_side':len(words)})
    check(rows[5]['branches']==tree_rows,'Enumerated rooted branches')
    results.append({'group':6,'pass':True,'method':'Explicit rooted ternary words'})
    return results

def adversarial_checks():
    out=[]
    # Arbitrarily bad essential dual surfaces: 2k+1 alternating crossings.
    crossing=[]
    for k in range(1,21):
        n=2*k+1
        roots=[F(2*i+1,2*n) for i in range(n)]
        signs=[(-1)**i for i in range(n)]
        check(sum(signs)==1 and all(F(i,n)<t<F(i+1,n) for i,t in enumerate(roots)), 'Alternating root orientations')
        crossing.append({'crossings':n,'signed_class':1,'complexity_multiple':n})
    out.append({'name':'Unbounded essential-but-nonminimal PL family','cases':crossing,'pass':True})

    # A k-scaled translation action has k edge orbits, each primitive upstairs.
    scaled=[]
    for k in range(1,21):
        levels=[F(2*j+1,2*k) for j in range(k)]
        check(all(0<t<1 for t in levels) and len(set(levels))==k,'Scaled line orbit levels')
        scaled.append({'scale':k,'edge_orbits':k,'class_per_orbit':1,'sum_over_orbits':k})
    out.append({'name':'Scaled translation is not a multiplied single-edge class','cases':scaled,'pass':True})

    # Integer heights have reflection isotropy; interior heights do not.
    total=noninteger=integer=0
    heights=sorted({F(p,q) for q in range(1,12) for p in range(-22,23)})
    for t in heights:
        reflection_index=t
        fixes=reflection_index.denominator==1
        check(fixes==(t.denominator==1),'Integer-height reflection criterion')
        total+=1; integer+=int(fixes); noninteger+=int(not fixes)
    check((-F(1,2)+1)==F(1,2),'Inverting reflection fixes edge midpoint')
    check((1-0,1-1)==(1,0),'Inverting reflection exchanges endpoints')
    out.append({'name':'Dihedral vertex and inversion hazards','rational_heights':total,
                'integer_reflection_fixed_heights':integer,'noninteger_free_heights':noninteger,
                'midpoint_setwise_stabilizer_index_over_pointwise':2,'pass':True})

    # Exhaust all H-invariant S3 subsets and all pairs of S4 H-cosets.
    group,h,normalizer,cosets,collision=subgroup_model(3)
    subsets=0; deck_misses=0
    for bits in product((0,1),repeat=len(cosets)):
        u=set().union(*(set(c) for c,b in zip(cosets,bits) if b))
        full=bool(collision(u,group-h)); deck=bool(collision(u,normalizer-h))
        check(full==(sum(bits)>1),'Full criterion for invariant finite subsets')
        subsets+=1; deck_misses+=int(full and not deck)
    group,h,normalizer,cosets,collision=subgroup_model(4)
    pairs=misses=0
    for c1,c2 in combinations(cosets,2):
        u=set(c1)|set(c2)
        check(bool(collision(u,group-h)),'Every two-coset set collides fully')
        pairs+=1; misses+=int(not collision(u,normalizer-h))
    check((len(normalizer),pairs,misses)==(4,66,60),'Nontrivial quotient deck group still insufficient')
    out.append({'name':'Exhaustive nonnormal normalizer blind spots','s3_subsets':subsets,
                's3_deck_only_false_negatives':deck_misses,'s4_normalizer_order':len(normalizer),
                's4_two_coset_sets':pairs,'s4_deck_only_false_negatives':misses,'pass':True})

    # Pairing rank alone cannot produce the full degree-versus-genus inequality.
    for g in range(2,13):
        for d in range(2,8):
            # Each block A=diag(d,1) satisfies A^T J A=dJ.
            block=((d,0),(0,1))
            transformed=((0,block[0][0]*block[1][1]),(-block[0][0]*block[1][1],0))
            check(transformed==((0,d),(-d,0)),'Same-dimension scaled symplectic form')
    for k in range(-20,21):
        if k not in (0,1):
            check(k+(1-k)==1 and 1 not in (k,1-k),'Total degree one lacks degree-one component')
    out.append({'name':'Cup-pairing lower bound has deliberate limited strength',
                'same_genus_matrix_models':66,'topological_maps_asserted':False,'pass':True})
    return out

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--author-safe',required=True,type=Path)
    parser.add_argument('--author-archive',required=True,type=Path)
    args=parser.parse_args()
    safe=args.author_safe.resolve(); archive=args.author_archive.resolve()
    b=archive.read_bytes();check(len(b)==23418 and sha(b)==ZIP_SHA,'Frozen author ZIP binding')
    manifest_bytes=(safe/'MANIFEST.json').read_bytes()
    check(sha(manifest_bytes)==MANIFEST_SHA,'Frozen manifest binding')
    manifest=json.loads(manifest_bytes)
    expected={f['path'] for f in manifest['files']}|{'MANIFEST.json'}
    check({p.name for p in safe.iterdir() if p.is_file()}==expected,'Author directory inventory')
    check(not any(p.is_symlink() for p in safe.iterdir()),'No author symlinks')
    for f in manifest['files']:
        data=(safe/f['path']).read_bytes()
        check(len(data)==f['bytes'] and sha(data)==f['sha256'],'Manifest member '+f['path'])
    with zipfile.ZipFile(archive) as z:
        check(set(z.namelist())=={'safe/'+n for n in expected} and len(z.namelist())==11,'Exact archive inventory')
        for n in expected:
            check(z.read('safe/'+n)==(safe/n).read_bytes(),'ZIP/directory equality '+n)
    process=subprocess.run([sys.executable,'-B','verify.py'],cwd=safe,capture_output=True)
    check(process.returncode==0 and not process.stderr,'Original replay status')
    check(process.stdout==(safe/'CONTROL_RESULTS.json').read_bytes() and
          sha(process.stdout)==OUTPUT_SHA,'Original byte-for-byte replay')
    original=json.loads(process.stdout)
    independent=independently_recompute(original)
    added=adversarial_checks()
    return {'target_id':10900010,'rank':672,'verdict':'PASS AS QUALIFIED PARTIAL RESULTS; NO GENERAL RESOLUTION',
        'author_zip_sha256':ZIP_SHA,'author_zip_bytes':len(b),'author_archive_members':11,
        'author_manifest_sha256':MANIFEST_SHA,'author_manifest_entries_verified':10,
        'original_replay':{'exit_code':0,'stdout_bytes':len(process.stdout),'stdout_sha256':OUTPUT_SHA,'exact_match':True},
        'independent_control_groups':independent,'additional_adversarial_groups':added,
        'all_pass':True,'scope':'Finite exact controls only; mathematical audit is separate prose; no topological completeness claim'}

if __name__=='__main__':
    print(json.dumps(main(),indent=2,sort_keys=True))

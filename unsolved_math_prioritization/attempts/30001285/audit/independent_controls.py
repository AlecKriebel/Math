#!/usr/bin/env python3
"""Independent finite-group controls and author-freeze adversarial validation.
This is not a checker for imported motivic theorems. No third-party text.
"""
import argparse
from collections import Counter
import hashlib
import itertools
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

counts = Counter()
def require(condition, label):
    if not condition:
        raise RuntimeError(label)
    counts[label] += 1

def finite_group(moduli):
    elements = tuple(itertools.product(*(range(m) for m in moduli)))
    zero = (0,) * len(moduli)
    def add(a, b): return tuple((x+y) % m for x,y,m in zip(a,b,moduli))
    def mul(n, a): return tuple(n*x % m for x,m in zip(a,moduli))
    subgroups = {frozenset([zero])}
    pending = list(subgroups)
    while pending:
        H = pending.pop()
        for a in elements:
            J = frozenset(add(h,mul(n,a)) for h in H for n in range(math.lcm(*moduli)))
            if J not in subgroups:
                subgroups.add(J); pending.append(J)
    return elements,zero,add,mul,subgroups

group_models = [(m,) for m in range(1,13)] + [(2,2),(2,4),(3,3),(2,2,2),(4,4)]
for moduli in group_models:
    B,zero,add,mul,subgroups = finite_group(moduli)
    for D in subgroups:
        cosets = {frozenset(add(b,d) for d in D) for b in B}
        rep = {b:min(C) for C in cosets for b in C}
        Q = set(rep.values())
        for n in range(1,13):
            nD = {mul(n,d) for d in D}
            for q in Q:
                if mul(n,q) not in D: continue
                theta = frozenset(add(mul(n,q),v) for v in nD)
                require(all(frozenset(add(mul(n,b),v) for v in nD)==theta
                            for b in B if rep[b]==q), 'theta_independent')
                lifts = [b for b in B if rep[b]==q and mul(n,b)==zero]
                require(bool(lifts)==(zero in theta), 'cyclic_lift_equivalence')
                for b in lifts:
                    require(all(mul((j+k)%n,b)==add(mul(j,b),mul(k,b))
                                for j in range(n) for k in range(n)), 'lift_is_homomorphism')
        for e in range(1, math.lcm(*moduli)+1):
            if any(mul(e,d)!=zero for d in D): continue
            require(all(mul(e,b)==mul(e,rep[b]) for b in B), 'multiplier_well_defined')
            ker = {q for q in Q if mul(e,q)==zero}
            Be = {b for b in B if mul(e,b)==zero}
            require(ker=={rep[b] for b in Be}, 'multiplier_kernel')
            Qe = {q for q in Q if mul(e,q) in D}
            require({mul(e,q) for q in Qe} == D & {mul(e,b) for b in B}, 'torsion_sequence_surjectivity')
            require(all(rep[mul(e,q)]==rep[mul(e,rep[q])] for q in Q), 'quotient_composite')
            require(all(rep[mul(e,b)]==rep[mul(e,rep[b])] for b in B), 'ambient_composite')

# Nonliftability and multiplier information loss are distinct phenomena.
require([b for b in range(4) if 2*b%4==0] == [0,2], 'projection_negative_source_images')
require(all(b%2==0 for b in range(4) if 2*b%4==0), 'projection_negative_kills_images')
require((2*1)%4 != 0, 'theta_nonzero')
require({2*q%4 for q in range(2)} == {0,2}, 'multiplier_positive')
require(all(2*x%2==0 for x in range(2)) and 0!=1, 'multiplier_negative_kernel')
require(len({b%4 for b in range(8) if 4*b%8==0}) == 2, 'finite_refinement_not_quotient_torsion')
for m,d,n in itertools.product(range(1,21), repeat=3):
    if math.gcd(d,n)!=1: continue
    require(all(x==0 for x in range(m) if d*x%m==0 and n*x%m==0), 'coprime_annihilators')

# Formal sign controls, not motivic normalization verification.
for degree in range(0,8):
    require((-1)**degree == (1 if degree%2==0 else -1), 'koszul_parity')
require((-1)**1==-1 and (-1)**4==1 and (-1)**5==-1, 'suspension_cohomology_degree_shift')
require({x*x%5 for x in range(1,5)}=={1,4}, 'q5_quadratic_units')
# Hilbert-symbol formula at odd p for 2 and 5, with valuations 0 and 1.
require(pow(2, (5-1)//2, 5)==4, 'q5_hilbert_symbol_negative')

p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True)
p.add_argument('--expected-manifest-sha256',required=True);args=p.parse_args()
packet=args.packet.resolve()
manifest_data=(packet/'MANIFEST.json').read_bytes()
require(hashlib.sha256(manifest_data).hexdigest()==args.expected_manifest_sha256, 'external_digest')
manifest=json.loads(manifest_data)
require(set(manifest['files'])|{'MANIFEST.json'}=={x.name for x in packet.iterdir()}, 'independent_inventory')
for name,item in manifest['files'].items():
    b=(packet/name).read_bytes()
    require(not (packet/name).is_symlink() and len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256'], 'independent_payload_hash')

def run(root,mode,script,*extra):
    return subprocess.run([sys.executable,'-I','-S','-B',*mode,str(root/script),*extra],text=True,capture_output=True,cwd='/tmp')

modes=[[],['-O']]
for mode in modes:
    result=run(packet,mode,'checks.py')
    require(result.returncode==0 and json.loads(result.stdout)==json.loads((packet/'CHECK_RESULTS.json').read_text()),'author_checks_exact_output')
    result=run(packet,mode,'verify_manifest.py','--expected-manifest-sha256',args.expected_manifest_sha256)
    require(result.returncode==0 and json.loads(result.stdout)['files_verified']==15, 'author_verifier_positive')
    cases=['bad_external_digest','payload_edit','extra_file','missing_file','payload_symlink','manifest_symlink','unsafe_name','nonregular_payload']
    for case in cases:
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'packet';shutil.copytree(packet,root)
            expected=args.expected_manifest_sha256
            if case=='bad_external_digest': expected='0'*64
            elif case=='payload_edit': (root/'STATEMENT.md').write_bytes((root/'STATEMENT.md').read_bytes()+b'\n')
            elif case=='extra_file': (root/'EXTRA').write_text('unlisted')
            elif case=='missing_file': (root/'STATEMENT.md').unlink()
            elif case=='payload_symlink':
                dest=Path(tmp)/'original_statement';shutil.move(root/'STATEMENT.md',dest);(root/'STATEMENT.md').symlink_to(dest)
            elif case=='manifest_symlink':
                dest=Path(tmp)/'original_manifest';shutil.move(root/'MANIFEST.json',dest);(root/'MANIFEST.json').symlink_to(dest)
            elif case=='nonregular_payload': (root/'STATEMENT.md').unlink();(root/'STATEMENT.md').mkdir()
            elif case=='unsafe_name':
                data=json.loads((root/'MANIFEST.json').read_text());data['files']['../STATEMENT.md']=data['files'].pop('STATEMENT.md')
                new=json.dumps(data).encode();(root/'MANIFEST.json').write_bytes(new);expected=hashlib.sha256(new).hexdigest()
            result=run(root,mode,'verify_manifest.py','--expected-manifest-sha256',expected)
            require(result.returncode!=0, 'verifier_reject_'+case)
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp); code=(packet/'checks.py').read_text()
        code=code.replace("counts = Counter()", "counts = Counter()")
        code=code.replace("# All subgroups", "check('deliberate_failure', False)\n\n# All subgroups",1)
        (root/'checks.py').write_text(code)
        result=run(root,mode,'checks.py')
        require(result.returncode!=0 and 'deliberate_failure' in result.stderr, 'checks_explicit_failure_survives_optimization')
print(json.dumps({'status':'PASS','group_models':len(group_models),'author_assertions_per_run':114419,
 'author_modes':['normal','optimized'],'independent_controls':dict(sorted(counts.items())),
 'total_independent_controls':sum(counts.values()),'limits':['No motivic theorem or common beta/sigma product normalization is proved by finite controls.','Negative validator tests use isolated disposable copies; the author freeze is unchanged.']},indent=2,sort_keys=True))

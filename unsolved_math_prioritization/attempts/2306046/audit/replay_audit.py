#!/usr/bin/env python3
"""Small independent exact controls and destructive tests on disposable copies only.

No source text, source PDFs, network access, or theorem-proof claim is needed.
"""
from pathlib import Path
from fractions import Fraction as Q
from math import isqrt
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
from verify_frozen_author import verify

def load_source(path):
    namespace = {'__name__': 'audit_loaded', '__file__': str(path)}
    exec(compile(path.read_text(), str(path), 'exec'), namespace)
    return namespace

def main(root):
    root = root.absolute()
    binding = verify(root)
    author = load_source(root / 'verify.py')
    expected = json.loads((root / 'EXPECTED_CHECKS.json').read_text())
    result = author['run']()
    assert result == expected and result['total_assertions'] == 23516
    baseline = subprocess.run([sys.executable, str(root / 'verify_integrity.py')], capture_output=True, text=True)
    assert baseline.returncode == 0

    counts = {}
    def check(label, condition):
        if not condition:
            raise AssertionError(label)
        counts[label] = counts.get(label, 0) + 1
    def squared(v):
        return v[0]*v[0] + v[1]*v[1]
    def gap_squared(A, B):
        # An independent ordered-norm derivation: sqrt(H) <= sqrt(L) + 1.
        H, L = max(A, B), min(A, B)
        delta = H-L-1
        return delta <= 0 or delta*delta <= 4*L
    def product(z, w):
        return (z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0])
    def plus(z, w):
        return (z[0]+w[0], z[1]+w[1])

    # Norms of these rational Pythagorean vectors are exact rationals.
    directions = [(Q(1),Q(0)),(Q(0),Q(1)),(Q(3,5),Q(4,5)),
                  (Q(-3,5),Q(4,5)),(Q(5,13),Q(-12,13)),(Q(-1),Q(0))]
    radii = [Q(0),Q(1,3),Q(1,2),Q(1),Q(1001,1000),Q(3,2),Q(2),Q(3)]
    vectors = [(tuple(r*v for v in u), r) for u in directions for r in radii]
    for (a, ra) in vectors:
        check('rational_norm', squared(a) == ra*ra)
        for b, rb in vectors:
            truth = abs(ra-rb) <= 1
            check('author_predicate_rational_oracle', author['modulus_gap_le_one'](a,b) == truth)
            check('independent_predicate_rational_oracle', gap_squared(squared(a),squared(b)) == truth)
            check('predicate_swap_symmetry', author['modulus_gap_le_one'](a,b) == author['modulus_gap_le_one'](b,a))

    # Coefficients from direct convolution, independent of the author's recurrence.
    for gamma in directions:
        for zeta in directions:
            gp, zp = [(Q(1),Q(0))], [(Q(1),Q(0))]
            for _ in range(24):
                gp.append(product(gp[-1],gamma)); zp.append(product(zp[-1],zeta))
            coeff = []
            for n in range(1,26):
                value = (Q(0),Q(0))
                for j in range(n): value = plus(value,product(gp[j],zp[n-1-j]))
                coeff.append(value)
            for a,b in zip(coeff,coeff[1:]):
                check('independent_convolution_gap', gap_squared(squared(a),squared(b)))

    # Test arithmetic mutants against the independent oracle, including both orders.
    mutants = {
        'one_sided_upper_only': lambda a,b: squared(a) <= squared(b) or gap_squared(squared(a),squared(b)),
        'raw_coefficient_difference': lambda a,b: squared((a[0]-b[0],a[1]-b[1])) <= 1,
        'remove_nonpositive_T_branch': lambda a,b: (squared(a)+squared(b)-1)**2 <= 4*squared(a)*squared(b),
        'replace_or_with_and': lambda a,b: squared(a)+squared(b)-1 <= 0 and (squared(a)+squared(b)-1)**2 <= 4*squared(a)*squared(b),
        'make_boundary_strict': lambda a,b: squared(a)+squared(b)-1 < 0 or (squared(a)+squared(b)-1)**2 < 4*squared(a)*squared(b),
        'enlarge_bound_to_two': lambda a,b: gap_squared(squared(a)/4,squared(b)/4),
        'accept_everything': lambda a,b: True,
    }
    math_mutations=[]
    original = author['modulus_gap_le_one']
    for name, predicate in mutants.items():
        witnesses=[]
        for a,ra in vectors:
            for b,rb in vectors:
                if predicate(a,b) != (abs(ra-rb)<=1):
                    witnesses.append({'a':[str(v) for v in a], 'b':[str(v) for v in b],
                                      'expected':abs(ra-rb)<=1,'mutant':predicate(a,b)})
                    break
            if witnesses: break
        check('mathematical_mutant_killed', bool(witnesses))
        author['modulus_gap_le_one'] = predicate
        try:
            survived = author['run']() == expected
        except AssertionError:
            survived = False
        math_mutations.append({'mutation':name,'independent_oracle_rejected':True,
                               'author_suite_survived':survived,'witness':witnesses[0]})
    author['modulus_gap_le_one']=original

    integrity_mutations=[]
    cases=['unmodified','extra_file','missing_file','modified_file','payload_symlink',
           'manifest_symlink','modified_manifest','coordinated_payload_and_manifest','extra_empty_directory']
    with tempfile.TemporaryDirectory(prefix='starlike-audit-') as temp:
        tmp=Path(temp)
        for name in cases:
            copy=tmp/name
            shutil.copytree(root,copy)
            if name=='extra_file': (copy/'EXTRA').write_text('test\n')
            elif name=='missing_file': (copy/'README.md').unlink()
            elif name=='modified_file': (copy/'README.md').write_bytes((copy/'README.md').read_bytes()+b'\n')
            elif name in ('payload_symlink','manifest_symlink'):
                filename='README.md' if name=='payload_symlink' else 'AUTHOR_MANIFEST.json'
                external=tmp/(name+'.external')
                external.write_bytes((copy/filename).read_bytes())
                (copy/filename).unlink(); (copy/filename).symlink_to(external)
            elif name=='modified_manifest':
                (copy/'AUTHOR_MANIFEST.json').write_bytes((copy/'AUTHOR_MANIFEST.json').read_bytes()+b'\n')
            elif name=='coordinated_payload_and_manifest':
                payload=(copy/'README.md').read_bytes()+b'\n'
                (copy/'README.md').write_bytes(payload)
                m=json.loads((copy/'AUTHOR_MANIFEST.json').read_text())
                row=next(r for r in m['files'] if r['path']=='README.md')
                row.update(bytes=len(payload),sha256=hashlib.sha256(payload).hexdigest())
                (copy/'AUTHOR_MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
            elif name=='extra_empty_directory': (copy/'extra_empty').mkdir()
            try: verify(copy); strict_accepted=True
            except (ValueError, OSError): strict_accepted=False
            original_accepted=subprocess.run([sys.executable,str(copy/'verify_integrity.py')],capture_output=True).returncode==0
            check('pinned_integrity_control',strict_accepted==(name=='unmodified'))
            integrity_mutations.append({'mutation':name,'pinned_verifier_accepts':strict_accepted,
                                        'author_verifier_accepts':original_accepted})
    assert verify(root)==binding
    return {'all_passed':True,'target_id':'2306046','author_manifest_sha256':binding['author_manifest_sha256'],
            'author_controls_replayed':result['total_assertions'],'independent_control_counts':counts,
            'independent_control_total':sum(counts.values()),'mathematical_mutations':math_mutations,
            'integrity_mutations':integrity_mutations,'original_frozen_tree_unchanged':True,
            'scope':'Exact finite controls, mutation coverage and freeze authentication; not a proof of the general theorem.'}

if __name__=='__main__':
    root=Path(sys.argv[1]) if len(sys.argv)==2 else Path(__file__).parent.parent/'author'
    print(json.dumps(main(root),indent=2,sort_keys=True))

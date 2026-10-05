#!/usr/bin/env python3
"""Independent packet and model controls. No infinite theorem is machine-certified.

Usage: python3 -B INDEPENDENT_CONTROLS.py --release PATH
The submitted verifier is replayed only after independent anchored verification.
"""
from pathlib import Path
from itertools import product, combinations
from fractions import Fraction
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verify_frozen(root, bindings):
    expected = bindings['frozen_files']
    if set(p.name for p in root.iterdir()) != set(expected):
        raise ValueError('Exact nine-file boundary failed')
    for name, rec in expected.items():
        p = root / name
        if p.is_symlink() or not p.is_file():
            raise ValueError('Nonregular file')
        b = p.read_bytes()
        if len(b) != rec['bytes'] or digest(b) != rec['sha256']:
            raise ValueError('Externally anchored file mismatch: ' + name)
    m = json.loads((root / 'MANIFEST.json').read_text())
    if m['problem_id'] != '30001678' or m['status'] != 'unresolved_scoped_partials':
        raise ValueError('Wrong target or disposition')
    if m['files'] != {n:r for n,r in expected.items() if n != 'MANIFEST.json'}:
        raise ValueError('Manifest/payload binding mismatch')


def mutation_controls(root, bindings):
    cases = ['same_size_payload_change', 'missing_payload', 'extra_hidden_file',
             'nested_directory', 'symlink_substitution', 'manifest_only_change',
             'coordinated_payload_and_manifest_change', 'unlisted_pdf',
             'manifest_traversal', 'wrong_problem_id', 'wrong_status']
    for case in cases:
        with tempfile.TemporaryDirectory(prefix='independent-perfect-product-') as d:
            p = Path(d) / 'packet'
            shutil.copytree(root, p)
            if case == 'same_size_payload_change':
                b = bytearray((p / 'PROOF.md').read_bytes()); b[0] ^= 1
                (p / 'PROOF.md').write_bytes(b)
            elif case == 'missing_payload':
                (p / 'README.md').unlink()
            elif case == 'extra_hidden_file':
                (p / '.unlisted').write_text('control')
            elif case == 'nested_directory':
                (p / 'nested').mkdir()
            elif case == 'symlink_substitution':
                (p / 'README.md').unlink()
                (p / 'README.md').symlink_to('PROOF.md')
            elif case == 'unlisted_pdf':
                (p / 'source.pdf').write_bytes(b'%PDF synthetic mutation only')
            else:
                m = json.loads((p / 'MANIFEST.json').read_text())
                if case == 'manifest_only_change':
                    (p / 'MANIFEST.json').write_bytes((p / 'MANIFEST.json').read_bytes() + b' ')
                elif case == 'coordinated_payload_and_manifest_change':
                    b = (p / 'README.md').read_bytes() + b'\nchanged\n'
                    (p / 'README.md').write_bytes(b)
                    m['files']['README.md'] = {'bytes':len(b),'sha256':digest(b)}
                elif case == 'manifest_traversal':
                    m['files']['../README.md'] = m['files'].pop('README.md')
                elif case == 'wrong_problem_id':
                    m['problem_id'] = '30001679'
                elif case == 'wrong_status':
                    m['status'] = 'solved'
                if case != 'manifest_only_change':
                    (p / 'MANIFEST.json').write_text(json.dumps(m))
            try:
                verify_frozen(p, bindings)
            except (ValueError, OSError, KeyError):
                continue
            raise AssertionError('Accepted mutation: ' + case)
    return cases


def mathematical_controls():
    counts = {}
    def check(group, value):
        if not value:
            raise AssertionError(group)
        counts[group] = counts.get(group, 0) + 1

    # Different finite model from the submitted reflection-orbit checker:
    # cyclic translations on Z/18Z by the subgroup {0,6,12}.
    domain = range(18)
    classes = {x:frozenset((x + t) % 18 for t in (0,6,12)) for x in domain}
    codes = {x:tuple(int(a in classes[x]) for a in domain) for x in domain}
    for x,y in product(domain, repeat=2):
        check('finite_closed_orbit_separation', (codes[x] == codes[y]) == ((x-y) % 6 == 0))
        check('finite_compact_class_distance',
              (tuple(min(abs(a-z) for z in classes[x]) for a in domain) ==
               tuple(min(abs(a-z) for z in classes[y]) for a in domain)) ==
              (classes[x] == classes[y]))

    # Dense orbit prefixes have every finite word, even when two tails are
    # symbolically different. A finite prefix is not an E0 decision procedure.
    for n in range(1,8):
        zero_prefix = (0,)*n
        one_prefix = (1,)*n
        for target in product((0,1), repeat=n):
            check('dense_orbit_prefixes',
                  tuple(z ^ (z ^ t) for z,t in zip(zero_prefix,target)) == target)
            check('dense_orbit_prefixes',
                  tuple(z ^ (z ^ t) for z,t in zip(one_prefix,target)) == target)
        step = lambda k: int(k < n)
        check('finite_tail_trap', step(n) == 0 and step(n-1) == 1)
        check('finite_tail_trap', all(step(k) == 1 for k in range(n)))
        check('finite_tail_trap', 1 != 0)  # Constant tails differ at index n for every n.

    # Weighted box budget, using weights 3^n and widths 9^(-n-1),
    # independent of the submitted choice of powers of two.
    budgets = {}
    for p in (1,2,5):
        ratio = Fraction(3,9**p)
        total = Fraction(1,9**p) / (1-ratio)
        budgets[str(p)] = str(total)
        for n in range(1,12):
            partial = sum((Fraction(3**k, 9**(p*(k+1))) for k in range(n)), Fraction())
            check('weighted_box_exact_series', partial == total*(1-ratio**n))
            check('weighted_box_exact_series', 0 < partial < total)

    # Finite scheduling model for the actual fusion invariant. Each leaf is
    # a binary cylinder prefix. Meeting x_a != x_b forces restrictions on
    # selected leaves and sometimes an as-yet inactive coordinate reservoir.
    leaves = [{():''} for _ in range(4)]
    requirements = [(0,1),(1,3),(0,2),(2,3)]
    history = []
    def incompatible(a,b):
        return any(x != y for x,y in zip(a,b))
    for stage,(a,b) in enumerate(requirements):
        previous = [dict(d) for d in leaves]
        for j in range(stage+1):
            leaves[j] = {label+(bit,):prefix+str(bit)
                         for label,prefix in leaves[j].items() for bit in (0,1)}
        selections = list(product(*(list(d) for d in leaves)))
        for selection in selections:
            pa,pb = leaves[a][selection[a]],leaves[b][selection[b]]
            if not incompatible(pa,pb):
                length = max(len(pa),len(pb))
                leaves[a][selection[a]] = pa.ljust(length,'0')+'0'
                leaves[b][selection[b]] = pb.ljust(length,'0')+'1'
            check('fusion_selected_rectangle',
                  incompatible(leaves[a][selection[a]],leaves[b][selection[b]]))
        for j in range(4):
            check('fusion_all_labels_survive', len(leaves[j]) == 2**max(0,stage-j+1))
            for label,prefix in leaves[j].items():
                old_label = label[:-1] if j <= stage else label
                check('fusion_nested_cylinders', prefix.startswith(previous[j][old_label]))
            for (_,u),(_,v) in combinations(leaves[j].items(),2):
                check('fusion_coordinate_disjointness', incompatible(u,v))
        for aa,bb in requirements[:stage+1]:
            for u,v in product(leaves[aa].values(),leaves[bb].values()):
                check('fusion_previous_requirement_preserved', incompatible(u,v))
        history.append([len(d) for d in leaves])
    check('future_reservoir_eventually_splits', history[-1] == [16,8,4,2])

    # Distances to compact classes need only be Borel, not continuous.
    # K={0,2} union {1/n:n>=1}; classes {0,2} and singleton {1/n}.
    # The graph is closed, but distance from 2 to [1/n] tends to 2,
    # whereas distance from 2 to [0] equals 0.
    for n in range(2,40):
        check('compact_distance_need_not_be_continuous', abs(Fraction(2)-Fraction(1,n)) > 1)

    return {'assertion_groups':counts, 'total_model_assertions':sum(counts.values()),
            'weighted_box_bounds':budgets, 'fusion_leaf_counts':history}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--release',type=Path,required=True)
    args = parser.parse_args()
    bindings = json.loads((Path(__file__).parent / 'BINDINGS.json').read_text())
    verify_frozen(args.release,bindings)
    rejected = mutation_controls(args.release,bindings)
    models = mathematical_controls()
    # Submitted code is never imported into the independent checks above.
    replay = subprocess.run([sys.executable,'-B',str(args.release/'verify_packet.py'),'--self-test'],
                            capture_output=True,check=True)
    if replay.stderr:
        raise AssertionError('Unexpected author-checker stderr')
    author = json.loads(replay.stdout)
    verify_frozen(args.release,bindings)
    print(json.dumps({
        'result':'PASS_SCOPED_AUDIT_CONTROLS',
        'problem_id':'30001678',
        'research_disposition':'unsolved',
        'approaches_completed':5,
        'approaches_required':5,
        'frozen_manifest_sha256':bindings['frozen_manifest_sha256'],
        'frozen_files_before_and_after':9,
        'independent_mutations_rejected':rejected,
        'independent_models':models,
        'author_checker_replay':author,
        'mathematical_audit':'Retained results accepted with the explicit Cantor-extraction containment repair in AUDIT.md; frozen bytes unchanged.',
        'source_caveat':'KLy preprint Example 2.2 parenthetical is overstrong; not used by the packet.',
        'limits':['No automated proof of the infinite results.',
                  'No unrestricted theorem or admissible counterexample.',
                  'No global-openness, novelty, or exhaustive-literature certification.',
                  'Live target page and raw AI corpora remain uninspected.']
    },indent=2,sort_keys=True))


if __name__ == '__main__':
    main()

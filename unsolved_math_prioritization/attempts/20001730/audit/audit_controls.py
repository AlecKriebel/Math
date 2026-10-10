#!/usr/bin/env python3
"""Independent exact checks for the frozen conditional Gibbs compatibility note.

Usage: python audit_controls.py RELEASE_DIRECTORY [RELEASE_ARCHIVE]
No external dependencies. All integrity gates remain active under python -O.
Finite controls are not a formal proof of the continuous theorem.
"""
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

EXPECTED_MANIFEST = '13c0d3e846ff254a8d526574f12446517e56b4d6c6e8c27b1cd8c866af34a193'
EXPECTED_PROOF = '77354e318baf41c5afc0d062b041fb7ca1a41b2380e2d8da78d058cfd342a93c'
EXPECTED_ARCHIVE = 'b982ce65c18016451e63bf1520662590a14106731a7150149ed237ec3847ef73'
counts = {}

def check(group, condition):
    if not condition:
        raise RuntimeError('Independent check failed: ' + group)
    counts[group] = counts.get(group, 0) + 1

def sha(data):
    return hashlib.sha256(data).hexdigest()

def verify_bytes(root):
    if sha((root / 'MANIFEST.json').read_bytes()) != EXPECTED_MANIFEST:
        raise RuntimeError('Pinned manifest mismatch')
    if sha((root / 'CORRECTED_THEOREM.md').read_bytes()) != EXPECTED_PROOF:
        raise RuntimeError('Pinned proof mismatch')
    manifest = json.loads((root / 'MANIFEST.json').read_text())
    required = {'MANIFEST.json', 'MANIFEST.sha256'}
    for entry in manifest['files']:
        path = root / entry['path']
        if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(root.resolve()):
            raise RuntimeError('Unsafe or missing payload')
        data = path.read_bytes()
        if len(data) != entry['bytes'] or sha(data) != entry['sha256']:
            raise RuntimeError('Payload size/hash mismatch')
        required.add(entry['path'])
    actual = {str(path.relative_to(root)) for path in root.rglob('*') if path.is_file() or path.is_symlink()}
    if actual != required:
        raise RuntimeError('Payload inventory mismatch')
    if (root / 'MANIFEST.sha256').read_text().split()[0] != EXPECTED_MANIFEST:
        raise RuntimeError('Manifest sidecar mismatch')
    return manifest

def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)) for i in range(2))

I = ((1, 0), (0, 1))
B = ((2, 1), (1, 1))
BI = ((1, -1), (-1, 2))

def matrix_power(n):
    factor = B if n >= 0 else BI
    out = I
    for _ in range(abs(n)):
        out = mm(out, factor)
    return out

def qadd(x, y):
    return (x[0] + y[0], x[1] + y[1])

def qmul(x, y):
    return (x[0] * y[0] + 5 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])

def exp_sample(k):
    return Q(2) ** k

def run_release(root, optimized=False):
    # -E makes the baseline independent of an inherited PYTHONOPTIMIZE value.
    command = [sys.executable, '-E'] + (['-O'] if optimized else []) + [str(root / 'verify_release.py')]
    return subprocess.run(command, capture_output=True, text=True)

def main():
    if len(sys.argv) not in (2, 3):
        raise SystemExit(__doc__)
    root = Path(sys.argv[1]).resolve()
    manifest = verify_bytes(root)
    check('pinned_release_integrity', len(manifest['files']) == 9)
    replay = run_release(root)
    check('normal_release_replay', replay.returncode == 0)
    replay_json = json.loads(replay.stdout)
    check('normal_release_replay', replay_json['finite_control_assertions'] == 4177)

    archive_checked = False
    if len(sys.argv) == 3:
        archive = Path(sys.argv[2])
        check('archive_integrity', sha(archive.read_bytes()) == EXPECTED_ARCHIVE)
        with zipfile.ZipFile(archive) as z:
            prefix = 'Gibbs_Leaf_Conull_Correction/'
            expected = {prefix + p.name for p in root.iterdir() if p.is_file()}
            check('archive_inventory', len(z.namelist()) == len(set(z.namelist())) and set(z.namelist()) == expected)
            for name in z.namelist():
                check('archive_payload_equality', z.read(name) == (root / name.removeprefix(prefix)).read_bytes())
        archive_checked = True

    mutation_results = {}
    with tempfile.TemporaryDirectory(prefix='gibbs-independent-audit-') as temp:
        temp = Path(temp)
        for mutation in ['proof_append', 'proof_same_size', 'unlisted_file', 'missing_payload', 'manifest_edit', 'receipt_edit', 'payload_symlink']:
            copy = temp / mutation
            shutil.copytree(root, copy)
            proof = copy / 'CORRECTED_THEOREM.md'
            if mutation == 'proof_append':
                proof.write_bytes(proof.read_bytes() + b'\nAudit mutation.\n')
            elif mutation == 'proof_same_size':
                data = bytearray(proof.read_bytes()); data[0] ^= 1; proof.write_bytes(data)
            elif mutation == 'unlisted_file':
                (copy / 'extra.txt').write_text('audit mutation')
            elif mutation == 'missing_payload':
                (copy / 'README.md').unlink()
            elif mutation == 'manifest_edit':
                p = copy / 'MANIFEST.json'; p.write_bytes(p.read_bytes() + b'\n')
            elif mutation == 'receipt_edit':
                p = copy / 'REPLAY_EXPECTED.json'; p.write_bytes(p.read_bytes() + b'\n')
            elif mutation == 'payload_symlink':
                p = copy / 'README.md'; p.unlink(); p.symlink_to(root / 'README.md')
            rejected = run_release(copy).returncode != 0
            check('normal_mutations_rejected', rejected)
            try:
                verify_bytes(copy)
            except (RuntimeError, FileNotFoundError):
                independent_rejected = True
            else:
                independent_rejected = False
            check('independent_mutations_rejected', independent_rejected)
            mutation_results[mutation] = {'release_normal_rejected': rejected, 'independent_rejected': independent_rejected}

        optimized = run_release(temp / 'proof_append', optimized=True)
        optimized_accepts_mutation = optimized.returncode == 0
        check('documented_optimizer_caveat_reproduced', optimized_accepts_mutation)

    # Independent exact field controls for the exceptional leaf argument.
    lam = (Q(3, 2), Q(1, 2))
    slope = (Q(-1, 2), Q(1, 2))
    v = ((Q(1), Q(0)), slope)
    bv = (qadd((Q(2), Q(0)), slope), qadd((Q(1), Q(0)), slope))
    check('quadratic_eigenvector', bv == tuple(qmul(lam, x) for x in v))
    for k in range(-80, 81):
        if not k:
            continue
        p = matrix_power(k)
        w = (p[0][0] - 1, p[1][0])
        determinant = (p[0][0] - 1) * (p[1][1] - 1) - p[0][1] * p[1][0]
        check('nontrivial_power_no_fixed_direction', determinant != 0)
        # ell(u,v)=v-((sqrt(5)-1)/2)u; ell(w) cannot vanish.
        ell_w = (Q(w[1]) + Q(w[0], 2), -Q(w[0], 2))
        check('exceptional_leaf_annihilator', ell_w != (0, 0))

    # Finite atomic measure models test cancellation, not joint measurability.
    tau = (Q(2), Q(3), Q(5))
    numerator = (Q(7), Q(11), Q(13))
    wrong_sign_detected = False
    for bx in range(-3, 4):
        for by in range(-3, 4):
            for cexp in range(-3, 4):
                ebx, eby, c = exp_sample(bx), exp_sample(by), exp_sample(cexp)
                cg = ebx * c / eby
                sigma_x = tuple(n / ebx for n in numerator)
                sigma_y = tuple(c * n / eby for n in numerator)
                tau_y = tuple(cg * n for n in tau)
                check('normalized_rebasing_atomic', sigma_y == tuple(cg * n for n in sigma_x))
                check('basepoint_independent_rn_atomic', tuple(s / t for s, t in zip(sigma_x, tau)) == tuple(s / t for s, t in zip(sigma_y, tau_y)))
                wrong_cg = eby * c / ebx
                if sigma_y != tuple(wrong_cg * n for n in sigma_x):
                    wrong_sign_detected = True
    check('wrong_rebasing_sign_detected', wrong_sign_detected)

    # Independent finite partition-ratio model, including a zero-mass atom.
    denominator = (Q(1), Q(2), Q(3), Q(0))
    measure = (Q(3), Q(5), Q(7), Q(0))
    partitions = [((0, 1, 2, 3),), ((0, 1), (2, 3)), ((0,), (1,), (2,), (3,))]
    for partition in partitions:
        density = [Q(0)] * 4
        for atom in partition:
            d = sum(denominator[i] for i in atom)
            ratio = sum(measure[i] for i in atom) / d if d else Q(1)
            for i in atom:
                density[i] = ratio
            check('partition_ratio_mass', sum(density[i] * denominator[i] for i in atom) == sum(measure[i] for i in atom))
    check('partition_ratio_terminal_density', all(density[i] * denominator[i] == measure[i] for i in range(4)))

    # Check exact covariance coefficient separately from the frozen replay.
    for aa in range(-3, 4):
        for bx in range(-3, 4):
            for bfx in range(-3, 4):
                afgx = aa + bfx - bx
                check('transport_scalar_cancellation', exp_sample(aa) * exp_sample(bfx) / exp_sample(bx) == exp_sample(afgx))

    # Finite exact samples of the contraction inequality used analytically.
    for theta in (Q(1, 2), Q(2, 3), Q(3, 4)):
        for C in (Q(1), Q(2), Q(5)):
            for R in (Q(1), Q(5), Q(20)):
                for delta in (Q(1, 2), Q(1, 5)):
                    n = 0
                    while C * theta ** n * R >= delta:
                        n += 1
                    check('compact_capture_bound', all(C * theta ** m * R < delta for m in range(n, n + 8)))

    # All original files are still identical after adversarial copies/tests.
    verify_bytes(root)
    result = {
        'status': 'PASS_INDEPENDENT_FINITE_CONTROLS_WITH_VERIFIER_CAVEAT',
        'manifest_sha256': EXPECTED_MANIFEST,
        'proof_sha256': EXPECTED_PROOF,
        'archive_sha256': EXPECTED_ARCHIVE if archive_checked else None,
        'original_finite_control_assertions': 4177,
        'independent_check_count': sum(counts.values()),
        'independent_groups': counts,
        'normal_mutation_results': mutation_results,
        'release_verifier_accepts_modified_proof_under_python_O': optimized_accepts_mutation,
        'independent_integrity_checks_use_runtime_exceptions': True,
        'original_freeze_unchanged': True,
        'mathematical_scope': 'Conditional theorem reviewed separately; finite checks do not prove its continuous measure-theoretic steps.',
        'original_problem_status': 'unsolved',
    }
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()

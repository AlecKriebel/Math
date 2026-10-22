#!/usr/bin/env python3
"""Mutation tests execute the trusted verifier, never a mutated target's code."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def need(test, message):
    if not test:
        raise ValueError(message)


def writable_copy(source, target):
    shutil.copytree(source, target)
    target.chmod(0o700)
    for f in target.iterdir():
        f.chmod(0o600)


def rehash(root, name):
    p = root/'MANIFEST.json'
    m = json.loads(p.read_text())
    b = (root/name).read_bytes()
    for e in m['files']:
        if e['name'] == name:
            e['bytes'] = len(b)
            e['sha256'] = hashlib.sha256(b).hexdigest()
    p.write_text(json.dumps(m, indent=2)+'\n')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--author-root', type=Path, required=True)
    p.add_argument('--expected-audit-manifest', required=True)
    args = p.parse_args()
    root = Path(__file__).resolve().parent
    verifier = root/'verify_audit.py'
    author = args.author_root.resolve()
    base = json.loads((root/'CLAIMS.json').read_text())
    semantic = [
        ('claim_full_proof', 'full_conjecture_proved', True, False),
        ('claim_counterexample', 'conjecture_disproved', True, False),
        ('claim_han_false', 'han_theorem_disproved', True, False),
        ('claim_prior_resolution', 'han_v5_verified_as_resolution', True, False),
        ('claim_affine_v1_zero', 'affine_example_has_v1_zero', True, False),
        ('claim_formal_proof', 'finite_checks_are_formal_voa_proof', True, False),
        ('change_status', 'status', 'already_solved', False),
        ('change_routes', 'author_approaches_completed', 4, False),
        ('bool_as_problem_id', 'problem_id', True, False),
        ('skip_patch', 'read_only_runner_patch_required', False, False),
        ('zero_tail', 'tail_action', 0, True),
        ('wrong_lift_sign', 'hat_sign', 1, True),
        ('wrong_spectral_sign', 'spectral_sign', 1, True),
        ('wrong_charge', 'cartan_charge', 1, True),
        ('coordinate_not_rigid', 'coordinate_dimensions', [1, 0, 0, 0, 0], True),
        ('spin_rigid', 'spin_dimensions', [0, 0, 0, 0], True),
        ('permute_unequal_factors', 'permutation_order', 6, True),
        ('float_as_coefficient', 'hat_sign', -1.0, True),
    ]
    integrity = ['report_changed', 'report_missing', 'extra_file', 'report_symlink',
                 'root_symlink', 'rehashed_report', 'rehashed_claims', 'rehashed_code',
                 'duplicate_manifest_key', 'duplicate_manifest_entry', 'source_pdf_added',
                 'audit_report_changed', 'audit_rehashed_acceptance']
    details = []
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    with tempfile.TemporaryDirectory(prefix='voa-independent-') as temp:
        temp = Path(temp)
        for mode in [[], ['-O'], ['-OO']]:
            label = 'normal' if not mode else mode[0]
            def run(*extra):
                return subprocess.run([sys.executable, *mode, str(verifier), *map(str, extra)],
                                      capture_output=True, text=True, env=env)
            def verify(aroot, uroot):
                return run('--author-root', aroot, '--audit-root', uroot,
                           '--expected-audit-manifest', args.expected_audit_manifest)
            def rejected(result, name):
                need(result.returncode == 3 and result.stderr.startswith('AUDIT_REJECTED:'),
                     'Wrong failure or unexpected acceptance: '+label+' '+name+' '+result.stderr)
                details.append({'mode': label, 'fixture': name, 'rejected': True})
            r = verify(author, root)
            need(r.returncode == 0 and json.loads(r.stdout)['ok'] is True,
                 'Positive baseline failed: '+r.stderr)
            details.append({'mode': label, 'fixture': 'positive_baseline', 'accepted': True})
            for name, key, value, nested in semantic:
                c = copy.deepcopy(base)
                (c['arithmetic'] if nested else c)[key] = value
                f = temp/'claims.json'
                f.write_text(json.dumps(c))
                rejected(run('--claims', f), name)
            for name, payload in [
                ('duplicate_claim_key', (root/'CLAIMS.json').read_text().replace('"problem_id": 30002842', '"problem_id": 30002842, "problem_id": 30002842')),
                ('nonfinite_claim', (root/'CLAIMS.json').read_text().replace('"cartan_charge": 2', '"cartan_charge": NaN')),
            ]:
                f = temp/'claims.json'
                f.write_text(payload)
                rejected(run('--claims', f), name)
            for name in integrity:
                target = temp/(label.replace('-', '')+'_'+name)
                is_audit = name.startswith('audit_')
                source = root if is_audit else author
                if name == 'root_symlink':
                    target.symlink_to(author, target_is_directory=True)
                else:
                    writable_copy(source, target)
                    if name in ['report_changed', 'rehashed_report', 'audit_report_changed']:
                        f = target/('AUDIT.md' if is_audit else 'REPORT.md')
                        f.write_bytes(f.read_bytes()+b'\nMUTATION\n')
                        if name == 'rehashed_report':
                            rehash(target, f.name)
                    elif name == 'report_missing':
                        (target/'REPORT.md').unlink()
                    elif name == 'extra_file':
                        (target/'UNLISTED').write_text('unexpected')
                    elif name == 'report_symlink':
                        (target/'REPORT.md').unlink()
                        (target/'REPORT.md').symlink_to(author/'REPORT.md')
                    elif name == 'rehashed_claims':
                        f = target/'CLAIMS.json'
                        c = json.loads(f.read_text()); c['full_conjecture_proved'] = True
                        f.write_text(json.dumps(c)); rehash(target, f.name)
                    elif name == 'rehashed_code':
                        f = target/'verify_math.py'; f.write_text('raise RuntimeError("untrusted target code")\n')
                        rehash(target, f.name)
                    elif name == 'duplicate_manifest_key':
                        f = target/'MANIFEST.json'
                        f.write_text(f.read_text().replace('"problem_id": 30002842', '"problem_id": 30002842, "problem_id": 30002842'))
                    elif name == 'duplicate_manifest_entry':
                        f = target/'MANIFEST.json'; m = json.loads(f.read_text())
                        m['files'].append(m['files'][0]); f.write_text(json.dumps(m))
                    elif name == 'source_pdf_added':
                        (target/'source.pdf').write_bytes(b'%PDF-1.4\n')
                    elif name == 'audit_rehashed_acceptance':
                        f = target/'ACCEPTANCE.json'; a = json.loads(f.read_text())
                        a['conjecture_status'] = 'already_solved'
                        f.write_text(json.dumps(a)); rehash(target, f.name)
                    else:
                        raise ValueError('unimplemented mutation '+name)
                rejected(verify(author if is_audit else target, target if is_audit else root), name)
    output = {'ok': True, 'positive_baselines': 3,
              'semantic_rejections': 3*(len(semantic)+2), 'integrity_rejections': 3*len(integrity),
              'modes': ['normal', '-O', '-OO'], 'details': details}
    need(len(details) == 3*(1+len(semantic)+2+len(integrity)), 'fixture count mismatch')
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()

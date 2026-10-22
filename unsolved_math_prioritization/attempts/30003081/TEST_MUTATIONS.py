#!/usr/bin/env python3
"""Disposable fail-closed integrity controls; requires trusted external hashes."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

BOOTSTRAP = '''import hashlib,pathlib,sys
p=pathlib.Path(sys.argv[1]); expected=sys.argv[2]; data=p.read_bytes() if not p.is_symlink() and p.is_file() else b""
if hashlib.sha256(data).hexdigest()!=expected: raise SystemExit("Verifier bootstrap hash mismatch")
sys.argv=[str(p),*sys.argv[3:]]
exec(compile(data,str(p),"exec"),{"__name__":"__main__","__file__":str(p)})
'''


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def edit_manifest(root, change):
    path = root / 'PUBLICATION_MANIFEST.json'
    value = json.loads(path.read_bytes())
    change(value)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def rebind_outer(root, relative):
    def update(value):
        for item in value['files']:
            if item['path'] == relative:
                data = (root / relative).read_bytes()
                item.update(bytes=len(data), sha256=sha(data))
    edit_manifest(root, update)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--packet', type=Path, default=Path(__file__).absolute().parent)
    parser.add_argument('--expected-manifest', required=True)
    parser.add_argument('--expected-verifier', required=True)
    args = parser.parse_args()
    source = args.packet.absolute()
    verifier = source / 'VERIFY_PUBLICATION.py'
    need(sha(verifier.read_bytes()) == args.expected_verifier, 'Trusted verifier mismatch')
    original = {p.relative_to(source).as_posix(): p.read_bytes() for p in source.rglob('*') if p.is_file()}
    need(sha(original['PUBLICATION_MANIFEST.json']) == args.expected_manifest, 'Trusted manifest mismatch')
    env = {k: v for k, v in os.environ.items() if not k.startswith('PYTHON')}
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    results = []
    cases = ['wrong_anchor', 'proof_byte', 'missing_file', 'extra_file', 'extra_directory',
             'file_symlink', 'manifest_symlink', 'directory_symlink', 'root_symlink', 'fifo',
             'duplicate_json_key', 'duplicate_member', 'traversal_path', 'absolute_path',
             'boolean_size', 'negative_size', 'bad_digest', 'wrong_schema', 'wrong_problem',
             'frozen_anchor_change', 'rebound_checker', 'verifier_substitution', 'verifier_symlink',
             'corrected_checker_byte', 'patch_byte', 'extra_entry_field', 'manifest_self_entry',
             'nonlist_files', 'nondict_manifest', 'boolean_problem', 'wrong_status', 'wrong_turns', 'nonfinite_json', 'source_pdf', 'audit_checker_byte', 'canonical_patch_byte', 'canonical_header_rebound']
    modes = [('ordinary', []), ('optimized', ['-O']), ('double_optimized', ['-OO'])]
    def run(root, anchor, flags, code=verifier):
        return subprocess.run([sys.executable, '-I', '-B', *flags, '-c', BOOTSTRAP,
                               str(code), args.expected_verifier, '--packet', str(root),
                               '--expected-manifest', anchor, '--check-only'],
                              env=env, capture_output=True, timeout=30)
    for mode, flags in modes:
        result = run(source, args.expected_manifest, flags)
        need(result.returncode == 0 and json.loads(result.stdout)['status'] == 'PASS', 'Baseline failed: ' + mode)
        for case in cases:
            with tempfile.TemporaryDirectory(prefix='log-deletion-publication-test-') as temporary:
                parent = Path(temporary)
                root = parent / 'packet'
                shutil.copytree(source, root)
                root.chmod(0o700)
                for fixture in root.rglob('*'):
                    fixture.chmod(0o700 if fixture.is_dir() else 0o600)
                target = root
                anchor = args.expected_manifest
                code = verifier
                reanchor = False
                if case == 'wrong_anchor': anchor = '0' * 64
                elif case == 'proof_byte':
                    path = root / 'original/RESULT.md'; path.write_bytes(path.read_bytes() + b'x')
                elif case == 'missing_file': (root / 'original/README.md').unlink()
                elif case == 'extra_file': (root / 'SURPRISE').write_text('fault\n')
                elif case == 'extra_directory': (root / 'SURPRISE').mkdir()
                elif case == 'file_symlink':
                    path = root / 'original/README.md'; path.unlink(); path.symlink_to(source / 'original/README.md')
                elif case == 'manifest_symlink':
                    path = root / 'PUBLICATION_MANIFEST.json'; path.unlink(); path.symlink_to(source / path.name)
                elif case == 'directory_symlink':
                    shutil.rmtree(root / 'original'); (root / 'original').symlink_to(source / 'original', target_is_directory=True)
                elif case == 'root_symlink':
                    target = parent / 'linked'; target.symlink_to(root, target_is_directory=True)
                elif case == 'fifo': os.mkfifo(root / 'PIPE')
                elif case == 'duplicate_json_key':
                    path = root / 'PUBLICATION_MANIFEST.json'; path.write_bytes(b'{"schema":"duplicate",' + path.read_bytes().lstrip()[1:]); reanchor = True
                elif case == 'duplicate_member':
                    edit_manifest(root, lambda m: m['files'].append(m['files'][0].copy())); reanchor = True
                elif case in ('traversal_path', 'absolute_path'):
                    name = '../escape' if case == 'traversal_path' else '/tmp/escape'
                    edit_manifest(root, lambda m: m['files'][0].update(path=name)); reanchor = True
                elif case in ('boolean_size', 'negative_size'):
                    value = True if case == 'boolean_size' else -1
                    edit_manifest(root, lambda m: m['files'][0].update(bytes=value)); reanchor = True
                elif case == 'bad_digest':
                    edit_manifest(root, lambda m: m['files'][0].update(sha256='bad')); reanchor = True
                elif case == 'wrong_schema':
                    edit_manifest(root, lambda m: m.update(schema='different')); reanchor = True
                elif case == 'wrong_problem':
                    edit_manifest(root, lambda m: m.update(problem_id=1)); reanchor = True
                elif case == 'frozen_anchor_change':
                    edit_manifest(root, lambda m: m['frozen_manifest_anchors'].update({'original/MANIFEST.json': '0' * 64})); reanchor = True
                elif case == 'rebound_checker':
                    relative = 'original/check_math.py'; path = root / relative
                    path.write_text('raise RuntimeError("must not execute altered checker")\n')
                    inner_path = root / 'original/MANIFEST.json'; inner = json.loads(inner_path.read_bytes())
                    for item in inner['files']:
                        if item['path'] == 'check_math.py': item.update(bytes=path.stat().st_size, sha256=sha(path.read_bytes()))
                    inner_path.write_text(json.dumps(inner, indent=2, sort_keys=True) + '\n')
                    rebind_outer(root, relative); rebind_outer(root, 'original/MANIFEST.json'); reanchor = True
                elif case == 'corrected_checker_byte':
                    path = root / 'corrected/verify_packet.py'; path.write_bytes(path.read_bytes()+b'x')
                elif case == 'patch_byte':
                    path = root / 'independent_audit/HARDENING.patch'; path.write_bytes(path.read_bytes()+b'x')
                elif case == 'extra_entry_field':
                    edit_manifest(root, lambda m: m['files'][0].update(extra=True)); reanchor = True
                elif case == 'manifest_self_entry':
                    edit_manifest(root, lambda m: m['files'][0].update(path='PUBLICATION_MANIFEST.json')); reanchor = True
                elif case == 'nonlist_files':
                    edit_manifest(root, lambda m: m.update(files={})); reanchor = True
                elif case == 'nondict_manifest':
                    (root / 'PUBLICATION_MANIFEST.json').write_text('[]'); reanchor = True
                elif case == 'boolean_problem':
                    edit_manifest(root, lambda m: m.update(problem_id=True)); reanchor = True
                elif case == 'wrong_status':
                    edit_manifest(root, lambda m: m.update(status='claimed_solved')); reanchor = True
                elif case == 'wrong_turns':
                    edit_manifest(root, lambda m: m.update(turns='0/5')); reanchor = True
                elif case == 'nonfinite_json':
                    edit_manifest(root, lambda m: m.update(problem_id=float('nan'))); reanchor = True
                elif case == 'source_pdf':
                    (root / 'source.pdf').write_bytes(b'%PDF-1.4\n')
                elif case == 'canonical_patch_byte':
                    path = root / 'HARDENING_REPLAY.patch'; path.write_bytes(path.read_bytes()+b'x')
                elif case == 'canonical_header_rebound':
                    path = root / 'HARDENING_REPLAY.patch'; path.write_bytes(path.read_bytes().replace(b'@@ -76,7 +76,7 @@', b'@@ -77,7 +77,7 @@'))
                    rebind_outer(root, 'HARDENING_REPLAY.patch'); reanchor = True
                elif case == 'audit_checker_byte':
                    path = root / 'independent_audit/verify_audit.py'; path.write_bytes(path.read_bytes()+b'x')
                elif case == 'verifier_symlink':
                    code = root / 'VERIFY_PUBLICATION.py'; code.unlink(); code.symlink_to(verifier)
                elif case == 'verifier_substitution':
                    code = root / 'VERIFY_PUBLICATION.py'; code.write_text('print("PASS")\n')
                if reanchor: anchor = sha((root / 'PUBLICATION_MANIFEST.json').read_bytes())
                result = run(target, anchor, flags, code)
                need(result.returncode != 0, 'Accepted mutation: ' + case + ': ' + mode)
                if case == 'rebound_checker':
                    need(b'Frozen manifest anchor mismatch' in result.stderr, 'Rebound checker reached execution')
                if case in ('verifier_substitution', 'verifier_symlink'):
                    need(b'Verifier bootstrap hash mismatch' in result.stderr, 'Substituted verifier reached execution')
                results.append({'case': case, 'mode': mode, 'rejected': True})
    # Explicit environment controls: a fresh ordinary child is not optimized,
    # even when the caller has a conflicting PYTHONOPTIMIZE value.
    for value in ('1', '2'):
        poisoned = dict(env, PYTHONOPTIMIZE=value)
        result = subprocess.run([sys.executable, '-I', '-B', '-c', 'import sys; print(sys.flags.optimize); assert False, \"ASSERTION_RETENTION_CONTROL\"'], env=poisoned, capture_output=True)
        need(result.returncode != 0 and result.stdout == b'0\n' and b'AssertionError: ASSERTION_RETENTION_CONTROL' in result.stderr, 'Ordinary child assertions not retained')
        result = subprocess.run([sys.executable, '-I', '-B', '-c', BOOTSTRAP,
                                 str(verifier), args.expected_verifier, '--packet', str(source),
                                 '--expected-manifest', args.expected_manifest, '--check-only'],
                                env=poisoned, capture_output=True, timeout=30)
        need(result.returncode == 0 and json.loads(result.stdout)['status'] == 'PASS', 'Poisoned-environment wrapper failed')
    current = {p.relative_to(source).as_posix(): p.read_bytes() for p in source.rglob('*') if p.is_file()}
    need(current == original, 'Source packet changed')
    print(json.dumps({'status': 'PASS', 'mutation_classes': len(cases), 'rejections': len(results),
                      'positive_baselines': 3, 'ordinary_child_environment_controls': 2,
                      'cases': results, 'source_packet_unchanged': True,
                      'limits': 'Integrity fault controls with an externally pinned verifier; not proof-assistant certification or an executable sandbox.'}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

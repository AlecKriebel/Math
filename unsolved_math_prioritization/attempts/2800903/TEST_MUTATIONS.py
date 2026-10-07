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
p=pathlib.Path(sys.argv[1]); expected=sys.argv[2]; data=p.read_bytes()
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
             'frozen_anchor_change', 'rebound_checker', 'verifier_substitution', 'substitution_rebound_outer', 'corrected_rebind', 'audit_patch_change', 'nonfinite_json']
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
            with tempfile.TemporaryDirectory(prefix='kmedian-publication-test-') as temporary:
                parent = Path(temporary)
                root = parent / 'packet'
                shutil.copytree(source, root)
                target = root
                anchor = args.expected_manifest
                code = verifier
                reanchor = False
                if case == 'wrong_anchor': anchor = '0' * 64
                elif case == 'proof_byte':
                    path = root / 'public/RESULT.md'; path.write_bytes(path.read_bytes() + b'x')
                elif case == 'missing_file': (root / 'public/README.md').unlink()
                elif case == 'extra_file': (root / 'SURPRISE').write_text('fault\n')
                elif case == 'extra_directory': (root / 'SURPRISE').mkdir()
                elif case == 'file_symlink':
                    path = root / 'public/README.md'; path.unlink(); path.symlink_to(source / 'public/README.md')
                elif case == 'manifest_symlink':
                    path = root / 'PUBLICATION_MANIFEST.json'; path.unlink(); path.symlink_to(source / path.name)
                elif case == 'directory_symlink':
                    shutil.rmtree(root / 'public'); (root / 'public').symlink_to(source / 'public', target_is_directory=True)
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
                    edit_manifest(root, lambda m: m['frozen_manifest_anchors'].update({'public/FROZEN_MANIFEST.json': '0' * 64})); reanchor = True
                elif case == 'rebound_checker':
                    relative = 'public/verify.py'; path = root / relative
                    path.write_text('raise RuntimeError("must not execute altered checker")\n')
                    inner_path = root / 'public/FROZEN_MANIFEST.json'; inner = json.loads(inner_path.read_bytes())
                    for item in inner['files']:
                        if item['path'] == 'verify.py': item.update(bytes=path.stat().st_size, sha256=sha(path.read_bytes()))
                    inner_path.write_text(json.dumps(inner, indent=2, sort_keys=True) + '\n')
                    rebind_outer(root, relative); rebind_outer(root, 'public/FROZEN_MANIFEST.json'); reanchor = True
                elif case == 'nonfinite_json':
                    path = root / 'PUBLICATION_MANIFEST.json'
                    path.write_bytes(path.read_bytes().replace(b'"problem_id": 2800903', b'"problem_id": NaN'))
                    reanchor = True
                elif case == 'audit_patch_change':
                    relative = 'independent_audit/VERIFY_HARDENING.patch'
                    path = root / relative; path.write_bytes(path.read_bytes() + b'x')
                    rebind_outer(root, relative); reanchor = True
                elif case == 'corrected_rebind':
                    relative = 'corrected/verify.py'; path = root / relative
                    path.write_text('raise RuntimeError("must not execute changed correction")\n')
                    inner_path = root / 'corrected/CORRECTED_MANIFEST.json'; inner = json.loads(inner_path.read_bytes())
                    for item in inner['files']:
                        if item['path'] == 'verify.py': item.update(bytes=path.stat().st_size, sha256=sha(path.read_bytes()))
                    inner_path.write_text(json.dumps(inner, indent=2, sort_keys=True) + '\n')
                    rebind_outer(root, relative); rebind_outer(root, 'corrected/CORRECTED_MANIFEST.json'); reanchor = True
                elif case == 'substitution_rebound_outer':
                    code = root / 'VERIFY_PUBLICATION.py'; code.write_text('print("PASS")\n')
                    rebind_outer(root, 'VERIFY_PUBLICATION.py'); reanchor = True
                elif case in ('verifier_substitution', 'substitution_rebound_outer'):
                    code = root / 'VERIFY_PUBLICATION.py'; code.write_text('print("PASS")\n')
                if reanchor: anchor = sha((root / 'PUBLICATION_MANIFEST.json').read_bytes())
                result = run(target, anchor, flags, code)
                need(result.returncode != 0, 'Accepted mutation: ' + case + ': ' + mode)
                if case == 'rebound_checker':
                    need(b'Frozen manifest anchor mismatch' in result.stderr, 'Rebound checker reached execution')
                if case in ('verifier_substitution', 'substitution_rebound_outer'):
                    need(b'Verifier bootstrap hash mismatch' in result.stderr, 'Substituted verifier reached execution')
                results.append({'case': case, 'mode': mode, 'rejected': True})
    # Explicit environment controls: a fresh ordinary child is not optimized,
    # even when the caller has a conflicting PYTHONOPTIMIZE value.
    for value in ('1', '2'):
        poisoned = dict(env, PYTHONOPTIMIZE=value)
        result = subprocess.run([sys.executable, '-I', '-B', '-c', 'import sys; print(sys.flags.optimize)'], env=poisoned, capture_output=True)
        need(result.returncode == 0 and result.stdout == b'0\n', 'Ordinary child not pinned')
    current = {p.relative_to(source).as_posix(): p.read_bytes() for p in source.rglob('*') if p.is_file()}
    need(current == original, 'Source packet changed')
    print(json.dumps({'status': 'PASS', 'mutation_classes': len(cases), 'rejections': len(results),
                      'positive_baselines': 3, 'ordinary_child_environment_controls': 2,
                      'cases': results, 'source_packet_unchanged': True,
                      'limits': 'Integrity fault controls with an externally pinned verifier; not proof-assistant certification or an executable sandbox.'}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

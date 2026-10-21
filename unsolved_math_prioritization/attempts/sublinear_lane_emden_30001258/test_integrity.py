"""Mutations test integrity rejection, not the mathematical theorem. No sockets."""
import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def main(root, receipt):
    trusted = root / 'verify.py'
    results = []
    cases = ['baseline', 'modified_report', 'modified_audit', 'missing_file', 'extra_file',
             'extra_directory', 'symlink_payload', 'symlink_root', 'fifo_entry', 'manifest_tamper',
             'receipt_pin_tamper', 'symlink_receipt', 'internal_receipt', 'validator_tamper',
             'ast_tamper', 'duplicate_manifest_key', 'resigned_false_proof_claim',
             'resigned_ast_omission', 'resigned_original_tamper', 'resigned_wrong_identity']
    with tempfile.TemporaryDirectory(prefix='sublinear_integrity_') as temp:
        base = Path(temp)
        for case in cases:
            candidate = base / case
            shutil.copytree(root, candidate)
            pin = base / (case + '_receipt.json')
            shutil.copyfile(receipt, pin)
            target = candidate
            if case == 'modified_report':
                with (candidate / 'RESONANT_NODAL_ANALYSIS.md').open('ab') as f: f.write(b'\nchanged\n')
            elif case == 'modified_audit':
                with (candidate / 'INDEPENDENT_AUDIT.md').open('ab') as f: f.write(b'changed')
            elif case == 'missing_file': (candidate / 'README.md').unlink()
            elif case == 'extra_file': (candidate / 'extra').write_text('x')
            elif case == 'extra_directory': (candidate / 'extra').mkdir()
            elif case == 'symlink_payload':
                (candidate / 'README.md').unlink()
                (candidate / 'README.md').symlink_to(root / 'README.md')
            elif case == 'symlink_root':
                target = base / 'linked_root'
                target.symlink_to(candidate, target_is_directory=True)
            elif case == 'fifo_entry': os.mkfifo(candidate / 'pipe')
            elif case == 'manifest_tamper':
                with (candidate / 'MANIFEST.json').open('ab') as f: f.write(b' ')
            elif case == 'receipt_pin_tamper':
                obj = json.loads(pin.read_text()); obj['manifest_sha256'] = '0' * 64
                pin.write_text(json.dumps(obj))
            elif case == 'symlink_receipt':
                pin.unlink(); pin.symlink_to(receipt)
            elif case == 'internal_receipt':
                shutil.copyfile(pin, candidate / 'receipt.json'); pin = candidate / 'receipt.json'
            elif case == 'validator_tamper': (candidate / 'verify.py').write_text('print("forged PASS")\n')
            elif case == 'ast_tamper': (candidate / 'AST_PROVENANCE.json').write_text('{}')
            elif case == 'duplicate_manifest_key':
                data = (candidate / 'MANIFEST.json').read_text()
                (candidate / 'MANIFEST.json').write_text('{"README.md": {},' + data[1:])
                obj = json.loads(pin.read_text())
                obj['manifest_sha256'] = hashlib.sha256((candidate / 'MANIFEST.json').read_bytes()).hexdigest()
                pin.write_text(json.dumps(obj))
            elif case.startswith('resigned_'):
                if case == 'resigned_false_proof_claim':
                    obj = json.loads((candidate / 'PROVENANCE.json').read_text())
                    obj['mathematical_certificate'] = True
                    (candidate / 'PROVENANCE.json').write_text(json.dumps(obj))
                elif case == 'resigned_ast_omission': (candidate / 'AST_PROVENANCE.json').write_text('{}')
                elif case == 'resigned_original_tamper': (candidate / 'RESONANT_NODAL_ANALYSIS.md').write_text('altered original')
                elif case == 'resigned_wrong_identity':
                    obj = json.loads((candidate / 'PUBLIC_METADATA.json').read_text()); obj['problem_id'] = 0
                    (candidate / 'PUBLIC_METADATA.json').write_text(json.dumps(obj))
                manifest = json.loads((candidate / 'MANIFEST.json').read_text())
                for name in manifest:
                    data = (candidate / name).read_bytes()
                    manifest[name] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
                (candidate / 'MANIFEST.json').write_text(json.dumps(manifest))
                obj = json.loads(pin.read_text()); obj['manifest_sha256'] = hashlib.sha256((candidate / 'MANIFEST.json').read_bytes()).hexdigest()
                pin.write_text(json.dumps(obj))
            for flags in ([], ['-O']):
                run = subprocess.run([sys.executable, *flags, '-B', str(trusted), str(target), str(pin)],
                                     capture_output=True, text=True, timeout=10)
                result = json.loads(run.stdout)
                expected = 'PASS' if case == 'baseline' else 'FAIL'
                require(result['status'] == expected and run.returncode == (0 if case == 'baseline' else 1)
                        and not run.stderr, 'unexpected result: ' + case + repr(flags) + run.stdout + run.stderr)
                results.append({'case': case, 'optimized': bool(flags), 'status': result['status'],
                                'error': result.get('error')})
    return {'status': 'PASS', 'mathematical_certificate': False, 'runs': len(results),
            'negative_mutations_per_mode': len(cases) - 1, 'results': results}


if __name__ == '__main__':
    require(len(sys.argv) == 3, 'usage: test_integrity.py PACKAGE EXTERNAL_RECEIPT')
    print(json.dumps(main(Path(sys.argv[1]).absolute(), Path(sys.argv[2]).absolute()), indent=2))

#!/usr/bin/env python3
"""Check rejection of corrupt copies; keep every original input unchanged."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--expected-manifest', required=True)
    a = p.parse_args()
    root = Path(__file__).resolve().parent
    result = {'relocated_positive_modes': [], 'rejected_controls': [], 'original_inputs_preserved': True}
    with tempfile.TemporaryDirectory(prefix='blaschke publication controls ') as temporary:
        parent = Path(temporary)
        for mode in [[], ['-O'], ['-OO']]:
            label = mode[0] if mode else 'normal'
            controls = ['positive', 'payload-tamper', 'extra-file', 'extra-directory', 'missing-file', 'manifest-rewrite', 'wrong-external-pin', 'symlink-payload', 'symlink-manifest', 'symlink-directory', 'author-zip-tamper', 'audit-zip-tamper', 'nested-author-zip-tamper']
            for control in controls:
                dest = parent / (label + ' ' + control)
                shutil.copytree(root, dest)
                target = dest / 'CORRECTIONS.md'
                manifest = dest / 'PUBLICATION_MANIFEST.json'
                pin = a.expected_manifest
                if control == 'payload-tamper':
                    target.write_bytes(target.read_bytes() + b'\nCORRUPTED\n')
                elif control == 'extra-file':
                    (dest / 'unexpected.txt').write_text('unexpected')
                elif control == 'extra-directory':
                    (dest / 'unexpected directory').mkdir()
                elif control == 'missing-file':
                    target.unlink()
                elif control == 'manifest-rewrite':
                    manifest.write_bytes(manifest.read_bytes() + b'\n')
                elif control == 'wrong-external-pin':
                    pin = '0' * 64
                elif control in {'symlink-payload', 'symlink-manifest'}:
                    item = target if control == 'symlink-payload' else manifest
                    external = parent / (label + ' ' + control + ' external')
                    external.write_bytes(item.read_bytes())
                    item.unlink()
                    item.symlink_to(external)
                elif control == 'symlink-directory':
                    (dest / 'unexpected directory link').symlink_to(dest / 'archives', target_is_directory=True)
                elif control.endswith('zip-tamper'):
                    names = {'author-zip-tamper': 'archives/BLASCHKE_COMPACTIFICATIONS_5300014_AUTHOR_SAFE_FREEZE.zip', 'audit-zip-tamper': 'archives/BLASCHKE_COMPACTIFICATIONS_5300014_INDEPENDENT_AUDIT_SAFE.zip', 'nested-author-zip-tamper': 'independent_audit/AUTHOR_SAFE_FREEZE.zip'}
                    item = dest / names[control]
                    item.write_bytes(item.read_bytes() + b'corrupt')
                run = subprocess.run([sys.executable, '-B'] + mode + [str(dest / 'verify_publication.py'), '--expected-manifest', pin], cwd=parent, capture_output=True)
                if control == 'positive':
                    require(run.returncode == 0, 'relocated positive failed: ' + run.stderr.decode())
                    result['relocated_positive_modes'].append(label)
                else:
                    require(run.returncode != 0, 'negative accepted: ' + label + ':' + control)
                    result['rejected_controls'].append(label + ':' + control)
    result['negative_control_count'] = len(result['rejected_controls'])
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

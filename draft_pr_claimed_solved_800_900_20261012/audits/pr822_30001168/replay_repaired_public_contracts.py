#!/usr/bin/env python3
"""Replay exact published entry points in a relocated tree without sealed writes."""
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent


def need(ok, reason):
    if not ok:
        raise RuntimeError(reason)


def main():
    assembly = json.loads((HERE / 'LOCAL_PR_ASSEMBLY_R2.json').read_bytes())
    build = json.loads((HERE / 'preprint/BUILD_RECEIPT.json').read_bytes())
    source = Path(assembly['tree'])
    before = {p.relative_to(source).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in source.rglob('*') if p.is_file()}
    receipt = {'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'status': 'RUNNING', 'review_round': 'R2', 'cases': [],
               'relocated_with_spaces': True, 'advertised_relative_builder_command': True}
    output = HERE / 'ROOT_REPAIRS_AND_ASSEMBLY_REPLAY_R2.json'
    with tempfile.TemporaryDirectory(prefix='repaired yamabe published contracts ') as td:
        td = Path(td)
        tree = td / 'published tree with spaces'
        shutil.copytree(source, tree)
        pre = tree / 'publication_20261013/preprint'
        for optimized in (False, True):
            flags = ['-I', '-B'] + (['-O'] if optimized else [])
            commands = [
                ('outer_full', tree, ['verify_publication.py', assembly['outer_manifest_sha256'], '--full']),
                ('current_outer_controls', tree, ['package_controls.py', assembly['outer_manifest_sha256']]),
                ('public_builder', pre, ['build_verification.py', '--from-package', '../verification_package',
                                        '--trusted-index-sha256', build['index_sha256'], '--output-root',
                                        str(td / ('fresh rebuild ' + str(optimized)))])]
            for label, cwd, args in commands:
                process = subprocess.run([sys.executable, *flags, *args], cwd=cwd,
                                         capture_output=True, text=True, timeout=900)
                row = {'case': label, 'optimized': optimized, 'exit': process.returncode}
                if process.returncode:
                    row['stderr'] = process.stderr
                    receipt.update(status='INTERRUPTED_OR_FAILED')
                    receipt['cases'].append(row)
                    output.write_text(json.dumps(receipt, indent=2) + '\n')
                    raise RuntimeError(label + ': ' + process.stderr)
                data = json.loads(process.stdout)
                if label == 'outer_full':
                    need(data['regular_files'] == 163 and data['archive_members_verified'] == 110, 'outer counts')
                if label == 'current_outer_controls':
                    need(data['total'] == 22 and data['expected_rejections'] == 20, 'control counts')
                if label == 'public_builder':
                    rebuilt = td / ('fresh rebuild ' + str(optimized))
                    need(all((rebuilt / name).read_bytes() == (pre / name).read_bytes()
                             for name in ['package_index.json', 'verification.zip']), 'exact public rebuild')
                row['result'] = data
                receipt['cases'].append(row)
                output.write_text(json.dumps(receipt, indent=2) + '\n')
    after = {p.relative_to(source).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
             for p in source.rglob('*') if p.is_file()}
    need(before == after, 'sealed assembly changed')
    receipt.update(status='PASS', sealed_assembly_unchanged=True,
                   public_rebuilds_byte_identical=True, contract_replays=len(receipt['cases']))
    output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'status': 'PASS', 'contract_replays': len(receipt['cases']),
                      'public_rebuilds_byte_identical': True, 'sealed_assembly_unchanged': True}))


if __name__ == '__main__':
    main()

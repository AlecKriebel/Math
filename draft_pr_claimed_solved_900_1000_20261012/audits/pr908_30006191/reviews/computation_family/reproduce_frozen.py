#!/usr/bin/env python3
"""Replay unchanged original scripts in disposable copies, with mode receipts."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
MODES = {'normal': ([], None), 'O': (['-O'], None), 'OO': (['-OO'], None),
         'env_2': ([], '2')}


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--packet', type=Path, required=True)
    parser.add_argument('--python', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    (HERE / 'tmp').mkdir(exist_ok=True)
    require((HERE / 'tmp').is_dir() and not (HERE / 'tmp').is_symlink(), 'unsafe disposable work directory')
    sys.path.insert(0, str(HERE))
    import verify_frozen_packet
    before = verify_frozen_packet.verify(str(args.packet))
    environment_probe = subprocess.run([str(args.python), '-c',
        'import sys,numpy,scipy,sympy,mpmath,json; print(json.dumps({"python":sys.version.split()[0],"numpy":numpy.__version__,"scipy":scipy.__version__,"sympy":sympy.__version__,"mpmath":mpmath.__version__}))'],
        capture_output=True, text=True, check=True)
    commands = {'wrapper_integrity': ['verify_package.py', '--integrity-only'],
                'wrapper_full': ['verify_package.py'],
                'author': ['author/verify.py'],
                'audit_a': ['audit_a/independent_checks.py', '--proof', 'author/BOUNDED_REGION_PROOF.md'],
                'audit_b': ['audit_b/independent_checks.py', '--author-dir', 'author']}
    receipts = []
    with tempfile.TemporaryDirectory(dir=HERE / 'tmp', prefix='unchanged_replay_') as temp:
        for mode, (flags, optimize) in MODES.items():
            for label, tail in commands.items():
                work = Path(temp) / (mode + '_' + label)
                shutil.copytree(args.packet, work)
                env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(HERE / 'tmp'))
                env.pop('PYTHONOPTIMIZE', None)
                if optimize is not None:
                    env['PYTHONOPTIMIZE'] = optimize
                command = [str(args.python)] + flags + [str(HERE / 'frozen_runner.py')] + tail
                process = subprocess.run(command, cwd=work, env=env, capture_output=True, text=True, timeout=900)
                record = {'label': label, 'mode': mode, 'exit_code': process.returncode,
                          'stdout_sha256': digest(process.stdout.encode()), 'stdout_bytes': len(process.stdout.encode()),
                          'stderr_sha256': digest(process.stderr.encode()),
                          'optimization_observations': [], 'saved_packet_script_bytes_unchanged': True}
                for line in process.stderr.splitlines():
                    try:
                        observation = json.loads(line)
                        if type(observation) is dict and 'observation' in observation:
                            record['optimization_observations'].append(observation)
                    except json.JSONDecodeError:
                        pass
                require(process.returncode == 0, label + ' replay failed in ' + mode + ': ' + process.stderr[-2000:])
                result = json.loads(process.stdout)
                (HERE / 'tmp' / ('replay_' + label + '_' + mode + '.json')).write_text(process.stdout)
                if label in {'author', 'audit_b'}:
                    saved_name = 'author/CHECK_RESULTS.json' if label == 'author' else 'audit_b/INDEPENDENT_RESULTS.json'
                    saved_data = (args.packet / saved_name).read_bytes()
                    saved = json.loads(saved_data)
                    record['historical_result_stdout_byte_identical'] = process.stdout.encode() == saved_data
                    record['historical_result_json_identical'] = result == saved
                    record['historical_result_sha256'] = digest(saved_data)
                    record['observed_summary'] = result
                elif label == 'audit_a':
                    saved_data = (args.packet / 'audit_a/INDEPENDENT_CHECK_RESULTS.json').read_bytes()
                    current_data = (work / 'audit_a/INDEPENDENT_CHECK_RESULTS.json').read_bytes()
                    record['historical_detailed_result_byte_identical'] = current_data == saved_data
                    record['historical_detailed_result_json_identical'] = json.loads(current_data) == json.loads(saved_data)
                    record['detailed_result_sha256'] = digest(current_data)
                    record['detailed_result_bytes'] = len(current_data)
                    record['observed_summary'] = result
                elif label == 'wrapper_full':
                    record['finite_status'] = {key: value.get('status', value.get('manifest', value.get('input_integrity', {}).get('status')))
                                              for key, value in result['finite_controls'].items()}
                else:
                    record['observed_summary'] = result
                for name in ('verify_package.py', 'author/verify.py', 'audit_a/independent_checks.py', 'audit_b/independent_checks.py'):
                    require((work / name).read_bytes() == (args.packet / name).read_bytes(), 'frozen code unexpectedly changed')
                receipts.append(record)
    after = verify_frozen_packet.verify(str(args.packet))
    require(before['files'] == after['files'], 'original changed')
    output = {'status': 'PASS', 'utc': datetime.now(timezone.utc).isoformat(),
              'environment': json.loads(environment_probe.stdout), 'runs': receipts,
              'original_26_unchanged': True, 'original_fingerprint_receipt_before': before['files'],
              'original_fingerprint_receipt_after': after['files'],
              'source_bytes_check': 'not requested; no retained PDF inputs; no fresh-source-byte claim',
              'nested_wrapper_temporary_directory': 'TMPDIR explicitly confined to this review tmp folder',
              'warning': 'Optimized runs are execution observations, not evidence for assertions that Python removes. Historical output bytes can differ with Python/numerical libraries.'}
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'status': output['status'], 'runs': len(receipts), 'environment': output['environment'],
                      'original_26_unchanged': True}))


if __name__ == '__main__':
    main()

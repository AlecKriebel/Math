#!/usr/bin/env python3
"""Root independent relocated replay of the proposed supported verifier."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
REPAIR = HERE / 'verification_repair'


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def binding(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def save(path, obj):
    path.write_text(json.dumps(obj, indent=2) + '\n')


def main():
    output = HERE / 'ROOT_REPAIR_REPLAY.json'
    need(not output.exists(), 'Refuse overwriting root raw evidence')
    names = ['verify.py', 'controls_exact.py', 'controls_deterministic.py', 'SOURCE_MANIFEST.json']
    pins = {n: binding(REPAIR / n) for n in names}
    private = HERE / 'private_cases'
    private.mkdir(exist_ok=True)
    records = []
    with tempfile.TemporaryDirectory(prefix='root repaired path with spaces ', dir=private) as directory:
        temp = Path(directory)
        package = temp / 'package with spaces'
        package.mkdir()
        for name in names:
            shutil.copyfile(REPAIR / name, package / name)
        shutil.copytree(REPAIR / 'frozen_history', package / 'frozen_history')
        manifest = json.loads((package / 'SOURCE_MANIFEST.json').read_text())
        need(len(manifest['files']) == 12, 'Frozen inventory count')
        for row in manifest['files']:
            need(binding(package / 'frozen_history' / row['path']) == {k: row[k] for k in ['bytes', 'sha256']}, 'Copied history differs')
        cwd = temp / 'unrelated working directory'
        cwd.mkdir()
        trap = temp / 'PATH trap'
        trap.mkdir()
        (trap / 'python3').write_text('#!/bin/sh\nexit 93\n')
        (trap / 'python3').chmod(0o755)
        corrupted = temp / 'same length wrong history'
        shutil.copytree(package, corrupted)
        file = corrupted / 'frozen_history/author/attempts/turn_01.md'
        raw = file.read_bytes()
        file.write_bytes(b'X' + raw[1:])
        resealed = temp / 'fully resealed wrong saved result'
        shutil.copytree(package, resealed)
        history = resealed / 'frozen_history'
        saved = history / 'author/checks/verification_results.json'
        obj = json.loads(saved.read_text())
        obj['density'] = '300'
        save(saved, obj)
        author = history / 'author/MANIFEST.json'
        obj = json.loads(author.read_text())
        for name, row in obj['files'].items():
            row.update(binding(history / 'author' / name))
        save(author, obj)
        release = history / 'RELEASE_MANIFEST.json'
        obj = json.loads(release.read_text())
        for row in obj['files']:
            row.update(binding(history / row['path']))
        save(release, obj)
        source_manifest = resealed / 'SOURCE_MANIFEST.json'
        obj = json.loads(source_manifest.read_text())
        for row in obj['files']:
            row.update(binding(history / row['path']))
        save(source_manifest, obj)
        cases = [('baseline', [], None), ('marker', ['--diagnostic-fault', 'marker'], 'Marker is ambiguous'),
                 ('source_corruption', ['--inputs', str(corrupted)], 'Frozen source hash mismatch'),
                 ('resealed_saved_result', ['--inputs', str(resealed)], 'Canonical source manifest literal hash mismatch')]
        for case, args, reason in cases:
            for optimized in [False, True]:
                env = os.environ.copy()
                env.pop('PYTHONOPTIMIZE', None)
                if optimized:
                    env['PYTHONOPTIMIZE'] = '1'
                env['PATH'] = str(trap) + os.pathsep + env.get('PATH', '')
                cmd = [sys.executable, str(package / 'verify.py'), *args]
                run = subprocess.run(cmd, cwd=cwd, env=env, text=True, capture_output=True, timeout=120)
                record = {'case': case, 'optimized': optimized, 'command': cmd, 'cwd': str(cwd),
                          'returncode': run.returncode, 'stdout': run.stdout, 'stderr': run.stderr,
                          'expected_error': reason, 'copied_verifier_sha256': pins['verify.py']['sha256']}
                records.append(record)
                # Preserve raw evidence before judging any outcome.
                save(output, {'status': 'IN_PROGRESS', 'code_bindings': pins, 'records': records})
                if reason is None:
                    result = json.loads(run.stdout)
                    need(run.returncode == 0 and run.stderr == '' and result['status'] == 'PASS', 'Root baseline failed')
                    need(result['runtime']['executable'] == sys.executable and result['runtime']['optimization'] == int(optimized), 'Root child/mode')
                    need(result['original_scripts_safe_under_optimization'] is False and result['saved_results']['saved_result_files_checked'] == 2, 'Historical scope/result guards')
                else:
                    need(run.returncode == 1 and run.stdout == '' and reason in run.stderr, 'Root negative failed/wrong guard')
                print(case, optimized, run.returncode, flush=True)
    need(pins == {n: binding(REPAIR / n) for n in names}, 'Reviewed proposal changed during root replay')
    baselines = [json.loads(r['stdout']) for r in records if r['case'] == 'baseline']
    for r in baselines:
        del r['runtime']
    need(baselines[0] == baselines[1], 'Baseline mathematical values differ')
    result = {'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'pr': 445, 'problem_id': '30002737',
              'frozen_head': '3242c84e06db7e99012c7fe581adde5c3f89fc89', 'status': 'ROOT_REPLAY_EXPECTATIONS_MET',
              'code_bindings': pins, 'actual_baselines': 2, 'actual_negatives': 6, 'records': records,
              'scope': 'Independent relocated subprocess replay of this exact proposed repair; whole-package and priority acceptance remain separate; original 1/1/0 history unchanged.'}
    save(output, result)
    print(json.dumps({k: v for k, v in result.items() if k not in ['records', 'code_bindings']}, indent=2))


if __name__ == '__main__':
    main()

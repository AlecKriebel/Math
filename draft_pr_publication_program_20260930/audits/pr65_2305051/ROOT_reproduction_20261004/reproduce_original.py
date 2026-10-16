"""ROOT custody revalidation and isolated execution of unchanged PR65 checkers."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import stat
import subprocess
import sys

HERE = Path(__file__).resolve().parent
A = HERE.parent / 'original_source_authentication_20261004'
T = A / 'original/unsolved_math_prioritization/attempts/2305051'

def digest(body):
    return hashlib.sha256(body).hexdigest()

def save(name, obj):
    with (HERE / name).open('x') as f:
        json.dump(obj, f, indent=2)
        f.write('\n')

def pin(path):
    body = path.read_bytes()
    return {'path': str(path), 'bytes': len(body), 'sha256': digest(body)}

def main():
    assert not sys.flags.optimize
    assert digest((A / 'SELF_MANIFEST.json').read_bytes()) == '95ee403195eeddd052fdddd2c6c6ce0a29792166e08e89bfc95a1ab84e5c1bb1'
    manifest = json.loads((A / 'SELF_MANIFEST.json').read_text())
    for row in manifest['files']:
        path = A / row['path']
        assert stat.S_ISREG(path.lstat().st_mode)
        body = path.read_bytes()
        assert len(body) == row['bytes'] and digest(body) == row['sha256'], path
    blobs = json.loads((A / 'ORIGINAL_BLOB_MANIFEST.json').read_text())
    for row in blobs['artifacts']:
        body = (A / row['retained_path']).read_bytes()
        assert len(body) == row['bytes'] and digest(body) == row['sha256']
        assert hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest() == row['git_blob_SHA1']
        assert row['mode'] == '100644'
    commands = [json.loads(x) for x in (A / 'ACTUAL_COMMANDS.jsonl').read_text().splitlines()]
    previous_finish = None
    for row in commands:
        assert type(row['actual_pid']) is int and row['actual_pid'] > 0
        assert row['exit_code'] == 0
        start = dt.datetime.fromisoformat(row['started_UTC'])
        finish = dt.datetime.fromisoformat(row['finished_UTC'])
        assert start <= finish and (previous_finish is None or previous_finish <= start)
        previous_finish = finish
        for stream in ('stdout', 'stderr'):
            body = (A / row[stream + '_path']).read_bytes()
            assert len(body) == row[stream + '_bytes'] and digest(body) == row[stream + '_sha256']
    wrapper = json.loads((T / 'source_record.json').read_text())
    current = json.loads((HERE.parent / 'ROOT_selected_source_20261004/CURRENT_SQL_SELECTED_PAIR.json').read_text())
    assert type(wrapper['upstream_report']) is dict and wrapper['upstream_report']
    assert current['SQL_report_text_is_null'] is False
    assert wrapper['problem'] == current['problem'] and wrapper['upstream_report'] == current['report']
    assert (A / 'original/unsolved_math_prioritization/state.json').read_bytes() == b'{}\n'
    assert (A / 'original/unsolved_math_prioritization/history.jsonl').read_bytes() == b''
    input_paths = [Path(__file__), A / 'SELF_MANIFEST.json', A / 'ORIGINAL_BLOB_MANIFEST.json',
                   T / 'CANDIDATE.md', T / 'verify_recursion.py', T / 'verification.json',
                   T / 'review/independent_checks.py', T / 'review/independent_results.json']
    prelaunch = [pin(p) for p in input_paths]
    save('SOURCE_PRELAUNCH.json', {'UTC': dt.datetime.now(dt.timezone.utc).isoformat(), 'inputs': prelaunch,
                                  'self_manifest_members_verified': len(manifest['files']),
                                  'original_bodies_verified': len(blobs['artifacts']),
                                  'original_serial_commands_verified': len(commands),
                                  'typed_current_SQL_matches_original_source_pair': True})
    results = []
    for label, script, expected_name in [
            ('author', T / 'verify_recursion.py', T / 'verification.json'),
            ('old_independent', T / 'review/independent_checks.py', T / 'review/independent_results.json')]:
        work = HERE / label
        work.mkdir()
        (work / script.name).write_bytes(script.read_bytes())
        (work / 'CANDIDATE.md').write_bytes((T / 'CANDIDATE.md').read_bytes())
        argv = [sys.executable, '-E', '-B', str(work / script.name)]
        started = dt.datetime.now(dt.timezone.utc).isoformat()
        child = subprocess.Popen(argv, cwd=work, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = child.communicate()
        finished = dt.datetime.now(dt.timezone.utc).isoformat()
        (work / 'stdout.bin').write_bytes(out)
        (work / 'stderr.bin').write_bytes(err)
        rec = {'label': label, 'argv': argv, 'cwd': str(work), 'actual_pid': child.pid,
               'started_UTC': started, 'finished_UTC': finished, 'exit_code': child.returncode,
               'stdout': pin(work / 'stdout.bin'), 'stderr': pin(work / 'stderr.bin'),
               'code': pin(work / script.name), 'original_code': pin(script),
               'assertions_enabled': True, 'actual_execution': True}
        assert child.returncode == 0 and err == b'', rec
        assert (work / script.name).read_bytes() == script.read_bytes()
        assert out == expected_name.read_bytes(), 'Exact original receipt differs: ' + label
        rec['stdout_byte_identical_to_original_receipt'] = True
        receipt = json.loads(out)
        rec['exact_assertions'] = receipt.get('exact_assertions', receipt.get('assertions_passed'))
        if label == 'old_independent':
            assert (work / 'independent_results.json').read_bytes() == out
            rec['written_result_byte_identical_to_stdout'] = True
        results.append(rec)
    assert [pin(p) for p in input_paths] == prelaunch
    save('REPRODUCTION.json', {'schema': 'PR65-ROOT-actual-reproduction/v1',
                             'UTC': dt.datetime.now(dt.timezone.utc).isoformat(),
                             'controller_pid': os.getpid(), 'status': 'PASS',
                             'unchanged_input_pins': prelaunch, 'actual_commands': results,
                             'finite_diagnostics_only': True, 'new_proof_attempts': 0,
                             'proof_scope': 'Finite diagnostics do not prove the analytic all-stage or boundary conclusions.',
                             'frozen_original_evidence_unchanged': True})
    print(json.dumps({'status': 'PASS', 'self_manifest_members': len(manifest['files']),
                      'original_bodies': len(blobs['artifacts']), 'original_actual_commands': len(commands),
                      'author_assertions': results[0]['exact_assertions'],
                      'old_independent_assertions': results[1]['exact_assertions'],
                      'exact_original_receipts_reproduced': True}))

if __name__ == '__main__':
    main()

"""Verify completed independent-family custody and reproduce new bounded checks."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import stat
import subprocess
import sys

HERE = Path(__file__).resolve().parent
A = HERE.parent

def sha(body):
    return hashlib.sha256(body).hexdigest()

def pin(path):
    body = path.read_bytes()
    return {'path': str(path), 'bytes': len(body), 'sha256': sha(body)}

def save(name, obj):
    with (HERE / name).open('x') as f:
        json.dump(obj, f, indent=2)
        f.write('\n')

def main():
    assert not sys.flags.optimize
    families = [
        ('analytic', A / 'universal_bloch_analytic_adversary_20261004', 'ARTIFACT_MANIFEST.json',
         'diagnostics.py', 'DIAGNOSTIC_RESULTS.json'),
        ('factorization', A / 'blaschke_factorization_scope_adversary_20261004', 'SELF_MANIFEST.json',
         'exact_factorization_controls.py', 'EXACT_CONTROL_RESULTS.json')]
    pins = [pin(Path(__file__))]
    verified = []
    for name, base, manifest_name, script_name, result_name in families:
        manifest = json.loads((base / manifest_name).read_text())
        rows = manifest['artifacts']
        for row in rows:
            p = base / row['path']
            assert stat.S_ISREG(p.lstat().st_mode)
            body = p.read_bytes()
            assert len(body) == row['bytes'] and sha(body) == row['sha256'], p
        commands = [json.loads(line) for line in (base / 'ACTUAL_COMMANDS.jsonl').read_text().splitlines()]
        for row in commands:
            assert row.get('exit_code', row.get('returncode')) == 0, row
        pins.extend([pin(base / manifest_name), pin(base / 'ACTUAL_COMMANDS.jsonl'),
                     pin(base / script_name), pin(base / result_name)])
        verified.append({'family': name, 'manifest_members_verified': len(rows),
                         'actual_commands': len(commands)})
    save('NEW_FAMILIES_SOURCE_PRELAUNCH.json', {'UTC': dt.datetime.now(dt.timezone.utc).isoformat(), 'pins': pins})
    executions = []
    for name, base, manifest_name, script_name, result_name in families:
        work = HERE / ('new_' + name)
        work.mkdir()
        script = work / script_name
        script.write_bytes((base / script_name).read_bytes())
        argv = [sys.executable, '-E', '-B', str(script)]
        start = dt.datetime.now(dt.timezone.utc).isoformat()
        child = subprocess.Popen(argv, cwd=work, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = child.communicate()
        end = dt.datetime.now(dt.timezone.utc).isoformat()
        (work / 'stdout.bin').write_bytes(out)
        (work / 'stderr.bin').write_bytes(err)
        assert child.returncode == 0 and not err
        expected = (base / result_name).read_bytes()
        assert out == expected and (work / result_name).read_bytes() == expected
        result = json.loads(out)
        if name == 'analytic':
            assert all(row['less_than_24'] is True for row in result['sampled_Zygmund_Hn'])
        executions.append({'family': name, 'argv': argv, 'cwd': str(work),
                           'actual_pid': child.pid, 'started_UTC': start, 'finished_UTC': end,
                           'exit_code': child.returncode, 'stdout': pin(work / 'stdout.bin'),
                           'stderr': pin(work / 'stderr.bin'), 'original_code': pin(base / script_name),
                           'executed_code': pin(script), 'exact_prior_receipt_reproduced': True,
                           'finite_controls_are_proof': False})
    assert [pin(Path(p['path'])) for p in pins] == pins
    final = {'schema': 'PR65-ROOT-new-family-readback/v1',
             'UTC': dt.datetime.now(dt.timezone.utc).isoformat(), 'controller_pid': os.getpid(),
             'status': 'PASS', 'families': verified, 'executions': executions,
             'unchanged_input_pins': pins, 'new_proof_attempts': 0}
    save('NEW_FAMILIES_READBACK.json', final)
    print(json.dumps({'status': 'PASS', 'families': verified,
                      'unchanged_checks_reproduced': True, 'analytic_sampled_bounds_all_true': True}))

if __name__ == '__main__':
    main()

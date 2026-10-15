"""New all-guard and malformed-package controls, without altering the candidate."""
import ast
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
PUB = HERE.parent.parent / 'publication'
WORK = HERE / 'control_work'


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def command(path, mode):
    return [sys.executable, '-I', '-S', '-B', *(['-' + 'O' * mode] if mode else []), str(path)]


def run(path, mode):
    p = subprocess.run(command(path, mode), cwd=path.parent, capture_output=True, timeout=30)
    return {'exit_code': p.returncode, 'stdout': p.stdout.decode(), 'stderr': p.stderr.decode(),
            'stdout_sha256': hashlib.sha256(p.stdout).hexdigest(),
            'stderr_sha256': hashlib.sha256(p.stderr).hexdigest()}


def main():
    WORK.mkdir(exist_ok=True)
    guard_rows = []
    source = (PUB / 'checks/verify_functor_identities_explicit_guards.py').read_text()
    tree = ast.parse(source)
    guards = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and
              isinstance(n.func, ast.Name) and n.func.id == 'require']
    for index in range(11):
        mutant = ast.parse(source)
        calls = [n for n in ast.walk(mutant) if isinstance(n, ast.Call) and
                 isinstance(n.func, ast.Name) and n.func.id == 'require']
        calls[index].args[0] = ast.Constant(False)
        ast.fix_missing_locations(mutant)
        path = WORK / ('false_guard_' + str(index) + '.py')
        path.write_text(ast.unparse(mutant) + '\n')
        label = guards[index].args[1].value
        for mode in (0, 1, 2):
            result = run(path, mode)
            need(result['exit_code'] == 1 and result['stdout'] == '' and
                 result['stderr'].splitlines()[-1] == 'RuntimeError: ' + label,
                 'guard must remain active in every optimization mode')
            guard_rows.append({'guard': index + 1, 'label': label, 'mode': mode,
                               'intended_rejection': True, **result})

    scenarios = [
        ('missing_mathematical_source', 'unexpected exit for none'),
        ('invalid_reference_json', 'JSONDecodeError'),
        ('wrong_recursive_boolean_type', 'complete stdout mismatch for none'),
        ('trailing_stdout', 'complete stdout mismatch for none'),
        ('unexpected_stderr', 'complete stderr mismatch for none'),
        ('unrelated_runtime_error', 'unexpected exit for none'),
        ('wrong_intended_failure_reason', 'complete stdout mismatch for missing_parameter_shift'),
        ('syntax_error', 'unexpected exit for none'),
        ('unknown_contract_program', 'unexpected contract program')]
    malformed_rows = []
    for scenario, reason in scenarios:
        for mode in (0, 1, 2):
            package = WORK / 'package'
            if package.exists():
                shutil.rmtree(package)
            package.mkdir()
            shutil.copyfile(PUB / 'run_checks.py', package / 'run_checks.py')
            shutil.copytree(PUB / 'checks', package / 'checks')
            shutil.copytree(PUB / 'expected', package / 'expected')
            checker = package / 'checks/current/check_conjugacy.py'
            if scenario == 'missing_mathematical_source':
                checker.unlink()
            elif scenario == 'invalid_reference_json':
                (package / 'expected/FINITE_CONTRACT.json').write_text('{')
            elif scenario == 'wrong_recursive_boolean_type':
                p = package / 'expected/verify_functor_identities.json'
                d = json.loads(p.read_text()); d['conjugacy_matrix'] = 1
                p.write_text(json.dumps(d))
            elif scenario == 'trailing_stdout':
                checker.write_text(checker.read_text() + '\nprint("extra")\n')
            elif scenario == 'unexpected_stderr':
                checker.write_text(checker.read_text() + '\nimport sys\nprint("extra",file=sys.stderr)\n')
            elif scenario == 'unrelated_runtime_error':
                p = package / 'checks/verify_functor_identities_explicit_guards.py'
                p.write_text('raise RuntimeError("unrelated exception")\n')
            elif scenario == 'wrong_intended_failure_reason':
                p = package / 'expected/INDEPENDENT_CONTROLS.json'
                d = json.loads(p.read_text());d['missing_parameter_shift'] = 'unrelated exception'
                p.write_text(json.dumps(d))
            elif scenario == 'syntax_error':
                checker.write_text('def invalid(:\n')
            elif scenario == 'unknown_contract_program':
                p = package / 'expected/FINITE_CONTRACT.json'
                d = json.loads(p.read_text());d['modes']['0'][0]['program'] = 'unrelated.py'
                p.write_text(json.dumps(d))
            result = run(package / 'run_checks.py', mode)
            need(result['exit_code'] != 0 and '"status": "PASS"' not in result['stdout'] and
                 reason in result['stderr'], scenario + ' must fail for intended contract reason')
            malformed_rows.append({'scenario': scenario, 'outer_optimization_mode': mode,
                                   'expected_reason': reason, 'intended_rejection': True, **result})
    shutil.rmtree(WORK)
    result = {'status': 'PASS', 'all_eleven_guard_false_controls': guard_rows,
              'malformed_package_controls': malformed_rows,
              'extra_executions': len(guard_rows) + len(malformed_rows),
              'interpretation': 'Every guard independently rejects in normal/-O/-OO. Nine malformed package families fail, never earn the published runner PASS. This is a selected-control contract audit, not a general security or source-intent certificate.'}
    (HERE / 'receipts/EXTRA_CONTROLS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'guard_rejections': len(guard_rows),
                      'malformed_package_rejections': len(malformed_rows)}, indent=2))


if __name__ == '__main__':
    main()

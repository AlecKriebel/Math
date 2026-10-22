"""Replay the submitted symbolic coordinate validator, without old UID harness.

Only the preserved pure mutation function and literal reference data are
extracted by AST from the historical runner. Its module is not imported and
its environmental harness is not executed. All inputs remain unchanged.
"""
import ast
from copy import deepcopy
from fractions import Fraction
import hashlib
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
SUBMITTED = HERE.parent / 'submitted'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def main():
    tree = ast.parse((SUBMITTED / 'run_finite_checks.py').read_text())
    data = {}
    functions = []
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id in ('POSITIVES', 'EXPECTED_MUTATIONS'):
                data[node.targets[0].id] = ast.literal_eval(node.value)
        if isinstance(node, ast.FunctionDef) and node.name == 'mutations':
            functions.append(node)
    require(len(functions) == 1 and set(data) == {'POSITIVES', 'EXPECTED_MUTATIONS'},
            'exact reviewed pure function and literals required')
    module = ast.Module(body=functions, type_ignores=[])
    namespace = {'deepcopy': deepcopy, 'Fraction': Fraction}
    exec(compile(module, '<reviewed-pure-certificate-mutations>', 'exec'), namespace)
    original = json.loads((SUBMITTED / 'current/EMBEDDING_CERTIFICATE.json').read_text())
    mutations = namespace['mutations'](original)
    require(len(mutations) == 15, '15 intended certificate fault families required')
    rows = []
    import tempfile
    checker = SUBMITTED / 'current/audit_exact_embedding.py'
    inputs = {p: p.read_bytes() for p in (checker, SUBMITTED / 'current/EMBEDDING_CERTIFICATE.json')}
    with tempfile.TemporaryDirectory(prefix='grassmann-math-only-') as tmp:
        for mode in (0, 1, 2):
            cases = [('baseline', SUBMITTED / 'current/EMBEDDING_CERTIFICATE.json', 0,
                      {**data['POSITIVES'], 'python_optimization': mode})]
            for (label, value, prefix), (expected_label, reason) in zip(mutations, data['EXPECTED_MUTATIONS']):
                require(label == expected_label and reason.startswith(prefix), 'fault label/reason differs')
                require(value != original, 'fault does not change certificate')
                path = pathlib.Path(tmp) / (label + '.json')
                path.write_text(json.dumps(value, sort_keys=True) + '\n')
                cases.append((label, path, 1, {'status': 'FAIL', 'error': reason}))
            for label, certificate, expected_exit, expected in cases:
                command = [sys.executable, '-I', '-S', '-B']
                if mode:
                    command.append('-' + 'O' * mode)
                command.extend([str(checker), '--certificate', str(certificate)])
                result = subprocess.run(command, capture_output=True, timeout=120, check=False)
                wanted = (json.dumps(expected, sort_keys=True) + '\n').encode()
                require(result.returncode == expected_exit and result.stdout == wanted and result.stderr == b'',
                        label + ': full stdout/stderr/exit contract differs')
                rows.append({'mode': mode, 'case': label, 'exit_code': result.returncode,
                             'stdout': result.stdout.decode(), 'stderr': result.stderr.decode(),
                             'certificate_sha256': hashlib.sha256(certificate.read_bytes()).hexdigest(),
                             'complete_reference_match': True})
    require(all(p.read_bytes() == value for p, value in inputs.items()), 'original input bytes changed')
    result = {'status': 'PASS', 'baseline_runs': 3, 'certificate_fault_runs': 45,
              'submitted_validator_sha256': hashlib.sha256(checker.read_bytes()).hexdigest(),
              'original_inputs_unchanged': True,
              'historical_uid1000_permission_harness_replayed': False,
              'historical_module_imported_or_run': False,
              'interpreter': sys.version,
              'scope': 'Exact symbolic coordinate identities and specified certificate faults; not Fawzi reproof, source scope or priority certificate.',
              'runs': rows}
    (HERE / 'FINITE_REPRODUCTION.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'runs'}, indent=2))


if __name__ == '__main__':
    main()

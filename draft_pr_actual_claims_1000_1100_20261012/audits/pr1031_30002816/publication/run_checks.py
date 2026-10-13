"""Portable exact coordinate/certificate replay; no historical environment harness."""
import argparse
import ast
from copy import deepcopy
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent


def require(test, message):
    if not test:
        raise RuntimeError(message)


def exact_types(actual, expected):
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, dict):
        return actual.keys() == expected.keys() and all(
            exact_types(actual[k], expected[k]) for k in expected)
    if isinstance(expected, list):
        return len(actual) == len(expected) and all(
            exact_types(a, b) for a, b in zip(actual, expected))
    return actual == expected


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    source = HERE / 'evidence/submitted/run_finite_checks.py'
    checker = HERE / 'checks/audit_exact_embedding.py'
    certificate = HERE / 'checks/EMBEDDING_CERTIFICATE.json'
    pins = json.loads((HERE / 'evidence/SUBMITTED_PINS.json').read_text())
    pinned = {item['relative']: item for item in pins['files']}
    for path, relative in [(source, 'run_finite_checks.py'),
                           (checker, 'current/audit_exact_embedding.py'),
                           (certificate, 'current/EMBEDDING_CERTIFICATE.json')]:
        require(digest(path) == pinned[relative]['sha256'] and
                path.stat().st_size == pinned[relative]['bytes'],
                relative + ': original source bytes differ')
    references = json.loads((HERE / 'expected/ROOT_FINITE_REPRODUCTION.json').read_text())
    require(references['status'] == 'PASS' and references['baseline_runs'] == 3 and
            references['certificate_fault_runs'] == 45, 'Reference scope differs')
    reference_map = {(r['mode'], r['case']): r for r in references['runs']}
    require(len(reference_map) == len(references['runs']) == 48,
            'References must contain exactly 48 unique executed cases')
    tree = ast.parse(source.read_text())
    values = {}
    functions = []
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id in ('POSITIVES', 'EXPECTED_MUTATIONS'):
                values[node.targets[0].id] = ast.literal_eval(node.value)
        if isinstance(node, ast.FunctionDef) and node.name == 'mutations':
            functions.append(node)
    require(len(functions) == 1 and set(values) == {'POSITIVES', 'EXPECTED_MUTATIONS'},
            'Exactly the reviewed pure mutation function and literals required')
    namespace = {'deepcopy': deepcopy, 'Fraction': Fraction}
    exec(compile(ast.Module(body=functions, type_ignores=[]),
                 '<reviewed-pure-certificate-mutations>', 'exec'), namespace)
    original = json.loads(certificate.read_text())
    faults = namespace['mutations'](original)
    require(len(faults) == len(values['EXPECTED_MUTATIONS']) == 15,
            'Exactly 15 actual certificate fault families required')
    input_bytes = {path: path.read_bytes() for path in (source, checker, certificate)}
    rows = []
    with tempfile.TemporaryDirectory(prefix='grassmann-coordinate-replay-') as temporary:
        for mode in (0, 1, 2):
            cases = [('baseline', certificate)]
            for (label, value, reason_prefix), (expected_label, reason) in zip(
                    faults, values['EXPECTED_MUTATIONS']):
                require(label == expected_label and reason.startswith(reason_prefix),
                        'Fault label/reason differs')
                require(not exact_types(value, original), 'Fault changes no certificate value')
                path = Path(temporary) / (label + '.json')
                path.write_text(json.dumps(value, sort_keys=True) + '\n')
                cases.append((label, path))
            for label, path in cases:
                reference = reference_map[(mode, label)]
                require(digest(path) == reference['certificate_sha256'],
                        label + ': actual fault bytes differ from reviewed fault')
                command = [sys.executable, '-I', '-S', '-B']
                if mode:
                    command.append('-' + 'O' * mode)
                command.extend([str(checker), '--certificate', str(path)])
                result = subprocess.run(command, capture_output=True, timeout=120, check=False)
                require(result.returncode == reference['exit_code'], label + ': exit differs')
                require(result.stdout == reference['stdout'].encode('utf-8'), label + ': stdout differs')
                require(result.stderr == reference['stderr'].encode('utf-8'), label + ': stderr differs')
                require(exact_types(json.loads(result.stdout), json.loads(reference['stdout'])),
                        label + ': recursive JSON identity/types differ')
                if label == 'baseline':
                    require(result.returncode == 0, 'Baseline must succeed')
                else:
                    require(result.returncode == 1, 'Actual faulty certificate must be rejected')
                rows.append({'mode': mode, 'case': label, 'exit_code': result.returncode,
                             'stdout': result.stdout.decode('utf-8'),
                             'stderr': result.stderr.decode('utf-8'),
                             'certificate_sha256': digest(path),
                             'complete_reference_match': True})
    require(all(path.read_bytes() == data for path, data in input_bytes.items()),
            'Input files changed')
    receipt = {'status': 'PASS', 'baseline_runs': 3, 'certificate_fault_runs': 45,
               'original_inputs_unchanged': True,
               'historical_module_imported_or_run': False,
               'historical_uid1000_permission_harness_replayed': False,
               'arithmetic_source_sha256': digest(checker),
               'interpreter': sys.version, 'platform': platform.platform(),
               'finite_scope': 'Symbolic coordinate identities and intended certificate faults; not Fawzi reproof, explicit calibration, universal proof or priority certificate.',
               'runs': rows}
    if args.output:
        args.output.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({k: v for k, v in receipt.items() if k != 'runs'}, indent=2))


if __name__ == '__main__':
    main()

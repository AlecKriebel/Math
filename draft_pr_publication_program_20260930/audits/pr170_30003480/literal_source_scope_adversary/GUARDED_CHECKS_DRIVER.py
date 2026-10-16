"""Run explicit guards ordinarily and with -O, including five false controls."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import stat


class DriverFailure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise DriverFailure(message)


def execute(checker, optimized, variant):
    command = [sys.executable]+(['-O'] if optimized else [])+[str(checker), '--variant', variant]
    result = subprocess.run(command, capture_output=True)
    return result


def main():
    directory = Path(__file__).resolve().parent
    checker = directory/'GUARDED_EXACT_CHECKS.py'
    variants = {
        'q2_coefficient': 'Q2 coefficient/full-product value changed',
        'witness_roots': 'Witness roots do not square to coordinates',
        'witness_coordinates': 'Witness must remain strictly inside cube',
        'parity_weights': 'Parity weights do not realize requested marginal eigenvalues',
        'ghz_discrepancy': 'Literal GHZ discrepancy is not reproduced',
    }
    baseline_runs = []
    for optimized in [False, True]:
        result = execute(checker, optimized, 'baseline')
        require(result.returncode == 0, 'Baseline failed in '+str(optimized)+' mode')
        require(result.stderr == b'', 'Baseline wrote an unexpected diagnostic')
        payload = json.loads(result.stdout)
        require(payload['status'] == 'verified_finite_controls', 'Baseline success status missing')
        require(payload['universal_theorem_proved_by_finite_checks'] is False,
                'Finite controls must not claim the universal theorem')
        baseline_runs.append(result)
    require(baseline_runs[0].stdout == baseline_runs[1].stdout,
            'Ordinary and -O baseline outputs disagree')

    negative_results = []
    for variant, expected_error in variants.items():
        mode_results = []
        for optimized in [False, True]:
            result = execute(checker, optimized, variant)
            require(result.returncode == 2, 'False control not explicitly rejected: '+variant)
            require(result.stdout == b'', 'Rejected control emitted a success payload: '+variant)
            payload = json.loads(result.stderr)
            require(payload['status'] == 'verification_failed', 'Explicit rejection status missing')
            require(payload['variant'] == variant, 'Rejected variant identity mismatch')
            require(payload['error'] == expected_error, 'Unexpected rejection mechanism: '+variant)
            mode_results.append(result)
        require(mode_results[0].stderr == mode_results[1].stderr,
                'Ordinary and -O rejection diagnostics disagree: '+variant)
        negative_results.append({'variant': variant, 'ordinary_returncode': 2,
                                 'optimized_returncode': 2, 'rejection': expected_error,
                                 'identical_diagnostics_in_both_modes': True,
                                 'diagnostic_sha256': hashlib.sha256(mode_results[0].stderr).hexdigest()})

    receipt = {'status': 'guarded_control_repair_passed',
               'python_executable': sys.executable,
               'python_version': sys.version,
               'python_executable_identity': {
                   'resolved_path': str(Path(sys.executable).resolve()),
                   'bytes': len(Path(sys.executable).read_bytes()),
                   'sha256': hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest(),
                   'mode': format(stat.S_IMODE(Path(sys.executable).stat().st_mode), '04o')},
               'checker_sha256': hashlib.sha256(checker.read_bytes()).hexdigest(),
               'driver_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               'baseline_ordinary_and_optimized_agree_byte_for_byte': True,
               'baseline_modes': [
                   {'mode': 'ordinary', 'returncode': baseline_runs[0].returncode,
                    'stdout_sha256': hashlib.sha256(baseline_runs[0].stdout).hexdigest()},
                   {'mode': '-O', 'returncode': baseline_runs[1].returncode,
                    'stdout_sha256': hashlib.sha256(baseline_runs[1].stdout).hexdigest()}],
               'baseline_stdout_sha256': hashlib.sha256(baseline_runs[0].stdout).hexdigest(),
               'baseline_payload': json.loads(baseline_runs[0].stdout),
               'false_variants_rejected_in_both_modes': negative_results,
               'checker_runs': 12,
               'negative_runs_rejected': 10,
               'uses_removable_assertions': False,
               'universal_theorem_proved_by_finite_checks': False}
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (DriverFailure, ValueError, KeyError) as exc:
        print('Guarded driver failed: '+str(exc), file=sys.stderr)
        sys.exit(2)

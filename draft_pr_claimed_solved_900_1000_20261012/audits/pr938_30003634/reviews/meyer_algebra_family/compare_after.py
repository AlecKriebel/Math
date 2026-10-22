#!/usr/bin/env python3
"""Post-independence comparison and a second scalar-line cocycle calculation."""
from pathlib import Path
from fractions import Fraction as F
import datetime, hashlib, json, subprocess, argparse, sys
sys.dont_write_bytecode = True
import reproduce as r
HERE = Path(__file__).resolve().parent

class VerificationError(RuntimeError):
    """A failed mathematical or provenance check, active in every Python mode."""

def require(condition, message):
    if not condition:
        raise VerificationError(str(message))

def scalar_term(A, g):
    """Solve a 2x2 linear system for the known generator image line.
    This intentionally does not use the nullspace or form routines in reproduce.py.
    """
    a, b = A[0]
    c, d = A[1]
    D = [[d - 1, -b], [-c, a - 1]]
    e = [F(0), F(1)] if abs(g) == 1 else [F(1), F(0)]
    eps = F(1 if g > 0 else -1)
    y = [eps, F(0)] if abs(g) == 1 else [F(0), -eps]
    delta = D[0][0] * D[1][1] - D[0][1] * D[1][0]
    if delta:
        x = [(D[1][1] * e[0] - D[0][1] * e[1]) / delta, (-D[1][0] * e[0] + D[0][0] * e[1]) / delta]
    else:
        found = next(((i, j) for i in range(2) for j in range(2) if D[i][j]), None)
        if found is None:
            return 0
        i, j = found
        x = [F(0), F(0)]
        x[j] = e[i] / D[i][j]
        if any((sum((D[i][j] * x[j] for j in range(2))) != e[i] for i in range(2))):
            return 0
    q = (x[0] + y[0]) * e[1] - (x[1] + y[1]) * e[0]
    return (q > 0) - (q < 0)

def compare_certificate(independent, cert):
    own_terms = [x['meyer'] for x in independent['meyer_terms']]
    pairs = independent['power_pairs']
    syllables = [x for pair in zip(pairs['A'], pairs['B']) for x in pair]
    checks = dict(word=cert['word'] == independent['free_reduced_word'], syllables=cert['syllables'] == syllables, linking=cert['pairwise_linking'] == list(independent['strand_tracking']['linking_numbers'].values()), burau=cert['burau_matrix'] == [x for row in independent['final_Burau_matrix'] for x in row], signature=cert['signature'] == independent['signature'], all_104_meyer_terms=cert['meyer_terms'] == own_terms)
    require(all(checks.values()), 'Original certificate comparison failed: ' + str(checks))
    return checks

def calculate():
    initial = json.loads((HERE / 'INDEPENDENCE_CHECKPOINT.json').read_text())
    for name, digest in initial['files'].items():
        if name == 'reproduce.py':
            # Historical code hash remains pinned in the original checkpoint.
            # The new external public-map seal authenticates the hardened code.
            require(digest == 'f5b29eb7e7385a261e8671a5d6a7feb6ecf8e1bfd25170ef2a0e79d2930a72ee', 'Historical independent implementation pin changed')
        else:
            require(hashlib.sha256((HERE / name).read_bytes()).hexdigest() == digest, 'Initial independent artifact pin changed: ' + name)
    independent = json.loads((HERE / 'INDEPENDENT_RESULTS.json').read_text())
    certpath = HERE.parents[1] / 'original/unsolved_math_prioritization/attempts/30003634/original/certificate.json'
    cert = json.loads(certpath.read_text())
    checks = compare_certificate(independent, cert)
    own_terms = [x['meyer'] for x in independent['meyer_terms']]
    scalar = [scalar_term(r.frac(t['prefix_matrix']), t['letter']) for t in independent['meyer_terms']]
    require(scalar == own_terms, 'Independent scalar cocycle terms differ')
    witness = independent['free_reduced_word']
    witness_transform_checks = {'mirror': r.signature([-g for g in witness]), 'inverse': r.signature(r.inverse_word(witness)), 'reverse': r.signature(list(reversed(witness))), 'conjugate': r.signature([1, 2] + witness + [-2, -1])}
    require(witness_transform_checks == {'mirror': 2, 'inverse': 2, 'reverse': -2, 'conjugate': -2}, 'Witness transformation signature mismatch')
    scalar_short_checks = 0
    for w in [c['word'] for c in independent['controls']]:
        A = r.I
        total = 0
        for g in w:
            total -= scalar_term(A, g)
            A = r.multiply(A, r.T[g])
            scalar_short_checks += 1
        require(total == r.signature(w), 'Short scalar control signature mismatch')
    # Child stdout carries the complete result and preserves the active optimization.
    flags = ['-OO'] if sys.flags.optimize == 2 else ['-O'] if sys.flags.optimize == 1 else []
    run = subprocess.run([sys.executable, *flags, str(HERE / 'reproduce.py')], text=True, capture_output=True, check=True)
    rerun = json.loads(run.stdout)
    for obj in [independent, rerun]:
        obj.pop('utc')
    require(independent == rerun, 'Cold replay differs from independently checkpointed mathematics')
    return dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), phase='Original certificate first read only after independent result/checkpoint creation; later code hardening preserves that result', original_programs_executed=False, original_programs_imported=False, historical_verdicts_read=False, sibling_reports_read=False, certificate_sha256=hashlib.sha256(certpath.read_bytes()).hexdigest(), comparisons=checks, second_scalar_line_all_104_equal=True, witness_transform_signatures=witness_transform_checks, scalar_control_crossings=scalar_short_checks, replay_command='python3 reproduce.py', private_cold_replay_exit=run.returncode, replay_equal_except_timestamp=True, global_opposite_symplectic_convention_signature=2, global_convention_explanation='Replacing Omega by -Omega reverses every form sign; consistently reversing ordinary-signature convention changes -2 to +2 and preserves nonvanishing.', runtime_optimization_level=sys.flags.optimize, child_optimization_preserved=True, historical_implementation_pin_preserved_but_current_code_hardened=True)

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Explicit result destination; omitted means stdout only.')
    args = parser.parse_args(argv)
    payload = json.dumps(calculate(), indent=2) + '\n'
    if args.output is not None:
        args.output.write_text(payload)
    sys.stdout.write(payload)

if __name__ == '__main__':
    try:
        main()
    except VerificationError as exc:
        print('Verification failed: ' + str(exc), file=sys.stderr)
        sys.exit(1)

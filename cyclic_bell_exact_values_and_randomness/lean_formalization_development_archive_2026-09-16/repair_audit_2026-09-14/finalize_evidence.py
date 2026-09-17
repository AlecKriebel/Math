"""Consolidate a successful frozen run; never substitute for check.py."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RUN_ID = '20260915T041758190218Z'
sys.path.insert(0, str(ROOT / 'scripts'))
from check import protected_fingerprints, parse_axioms


def main():
    run_dir = ROOT / 'logs' / 'runs' / RUN_ID
    report = json.loads((run_dir / 'run.json').read_text())
    assert report['run_id'] == RUN_ID
    assert report['status'] == 'candidate_kernel_checks_passed_statement_review_required'
    assert report['kernel_checked'] is True
    assert report['protected_source_hashes'] == protected_fingerprints()
    expected = json.loads((ROOT / 'reference' / 'expected_theorems.json').read_text())
    assert len(expected) == len(report['axioms']) == 1852
    assert set(expected) == set(report['axioms'])
    assert {a for values in report['axioms'].values() for a in values} <= {
        'propext', 'Classical.choice', 'Quot.sound'}
    commands = report['commands']
    for command in commands:
        assert command['exit_code'] == (1 if command['expected_failure'] else 0)
        path = run_dir / command['log']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == command['log_sha256']
    controls = [c for c in commands if any(a.startswith('validation/') for a in c['command'])]
    assert len(controls) == 25
    assert sum(c['expected_failure'] for c in controls) == 20
    build = next(c for c in commands if c['command'] == ['lake', 'build'])
    build_axioms = parse_axioms((run_dir / build['log']).read_text(), expected)
    assert build_axioms == report['axioms']
    tests = (HERE / 'runner_tests.log').read_text()
    assert 'Ran 63 tests' in tests and tests.rstrip().endswith('OK')
    assert json.loads((HERE / 'FINAL_INPUT_INTEGRITY.json').read_text())['all_received_files_preserved']
    assert json.loads((HERE / 'FINAL_DECLARATION_PRESERVATION.json').read_text())['all_original_named_declarations_retained']
    assert hashlib.sha256((ROOT.parent / 'main.tex').read_bytes()).hexdigest() == report['manuscript']['sha256']

    saved = HERE / 'final_clean_run'
    if saved.exists():
        assert json.loads((saved / 'run.json').read_text())['run_id'] == RUN_ID
    shutil.copytree(run_dir, saved, dirs_exist_ok=True)
    reviews = [
        'FINAL_STATEMENT_RECONCILIATION.md', 'SOURCE_POLAR_FINAL_ADDENDUM.md',
        'CLOSURE_SEMANTIC_AUDIT.md', 'SEMANTIC_AUDIT.md',
        'ADVERSARIAL_SEMANTIC_AUDIT.md', 'VALIDATION_REPAIRS.md',
        'RUNNER_FINAL_REVIEW.md']
    result = {
        'status': 'verified_mathematical_claims_with_documented_proof_boundaries',
        'completed_utc': datetime.now(timezone.utc).isoformat(),
        'frozen_implementation_commit': '6648fbca6',
        'kernel_checked': True,
        'clean_run_id': RUN_ID,
        'clean_run_receipt': 'final_clean_run/run.json',
        'source_files': 106,
        'named_theorems': 1387,
        'audited_named_declarations': 1852,
        'original_named_declarations_retained': 1538,
        'expanded_statement_examples': 100,
        'lean_acceptance_controls_passed': 5,
        'lean_rejection_controls_passed': 20,
        'runner_tests_passed': 63,
        'axiom_union': sorted({a for v in report['axioms'].values() for a in v}),
        'standalone_axioms_equal_clean_build_axioms': True,
        'all_command_logs_hash_checked': True,
        'protected_sources_still_match_clean_run': True,
        'manuscript': report['manuscript'],
        'semantic_review': 'Independent source/model/statement audits found no remaining gap in mapped mathematical result statements.',
        'review_sha256': {p: hashlib.sha256((HERE / p).read_bytes()).hexdigest() for p in reviews},
        'boundaries': [
            'Result formalization, not a line-by-line prose-proof translation.',
            'General polar identity uses supplied defining polar properties; arbitrary polar existence/strong-limit representations not separately formalized.',
            'MUB result has an alternative stronger positivity proof; Toeplitz/SVD intermediate calculation not separately translated.',
            'External self-testing, literature novelty/priority and open questions are outside scope.',
            'Qqa/Qqc closure inclusion is for finite input alphabets, without finite Hilbert dimension restriction.'
        ]
    }
    (HERE / 'RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
    evaluation = HERE / 'FINAL_EVALUATION.md'
    text = evaluation.read_text()
    text = text.replace(
        '**Final verification status: in progress. Do not treat this draft as a completed certificate.**',
        '**Final verification: passed.** The repaired companion passes the complete frozen clean build, '
        'all controls, every-declaration axiom checks, and source/dependency integrity checks. '
        'Independent reviews found no remaining gap in the mapped mathematical result statements. '
        'The proof-method and external-result boundaries below remain explicit.')
    text = text.replace(
        'The final clean-run result, command/log hashes, compiler and dependency identities,\n'
        'axiom list, control results and unchanged-source checks will be recorded here\n'
        'after the run completes.',
        f'''The final clean run `{RUN_ID}` completed successfully in
{report['elapsed_seconds']:.1f} seconds using `{report['lean_version']}`. All
{len(commands)} recorded commands had the required exit status. Both the clean
build and the standalone collection produced exactly the same 1,852 axiom
reports, with only `propext`, `Classical.choice`, and `Quot.sound`. No admissions,
custom axioms or native proof-evaluation axioms are present in the audited dependencies.

All five acceptance controls and twenty intended proof rejections passed again
against the clean build. The 100 expanded statement examples elaborated. Compiler
commit, all nine locked dependency revisions, manuscript identity, command-log
hashes and protected source fingerprints passed the final checks.

See [the complete command/log receipt](final_clean_run/run.json),
[the consolidated result](RESULT.json), and [the actual clean build log](final_clean_run/{build['log']}).
Historical root handoff reports and `SOURCE_HASHES.sha256` describe the received
snapshot; use this receipt and `reference/source_inventory.json` for the repaired
snapshot.''')
    evaluation.write_text(text)
    with (HERE / 'RESEARCH_LOG.md').open('a') as log:
        log.write('\n' + result['completed_utc'] +
            ' — Full frozen clean verification completed successfully: 106 source files, 1,387 theorems, '
            '1,852 identical standard-axiom reports in both collections, 100 expanded statement examples, '
            '5 acceptance controls, 20 strict rejection controls, 63 runner tests, and all protected '
            'source/manuscript/dependency checks. Final independent reconciliation found no dropped '
            'original declaration or weakened model/endpoint and no remaining mapped-result coverage gap. '
            'Completion estimate 100% for repair, mathematical-claim coverage and evaluation, with '
            'documented alternative-proof and external-literature boundaries. Evidence retained in '
            'final_clean_run and FINAL_EVALUATION.md; publication checkpoint follows.\n')
    print(json.dumps({k: result[k] for k in ['status', 'audited_named_declarations', 'axiom_union']}, indent=2))


if __name__ == '__main__':
    main()

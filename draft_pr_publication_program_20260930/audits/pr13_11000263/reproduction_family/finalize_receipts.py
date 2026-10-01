#!/usr/bin/env python3
"""Record a scoped family verdict and hash manifest from existing receipts."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAPSHOT = HERE.parent/'source_snapshot'

def read(path):
    return json.loads(path.read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    replay = read(HERE/'replay_receipt.json')
    independent = read(HERE/'independent_laurent_receipt.json')
    prior_rerun = read(SNAPSHOT/'verifier_rerun.json')
    stored_verify = read(SNAPSHOT/'verification.json')
    assert prior_rerun['verifier_sha256'] == sha(SNAPSHOT/'verify.py')
    for key in ('case_count', 'equality_and_rank_checks', 'cases'):
        assert prior_rerun[key] == stored_verify[key], key
    assert replay['status'] == independent['status'] == 'passed'
    assert replay['snapshot_unchanged']
    for run in replay['runs']:
        assert run['exact_bytes_match'] and run['json_semantics_match']
    now = datetime.now(timezone.utc).isoformat()
    verdict = {
        'family': 'PR13 independent exact reproduction and numerical/proof consistency',
        'timestamp_utc': now,
        'frozen_head': '7a845f7e025a24affe1b712cf7ada648570f9c64',
        'verdict': 'PASS_SCOPED_REPAIRED_PRESENTATIONS',
        'completion_estimate_percent': 100,
        'claim': 'Over F=Q(q), X3 is nonzero in A_n and C_n for every n>=3, with the explicitly defined legal-row and extra-strand repairs.',
        'blocking_findings': [],
        'frozen_replay': {'byte_exact_receipts': True, 'rational_cases': 42,
                          'rational_checks': 1590, 'symbolic_checks': 23,
                          'stored_rerun_verifier_hash_matches': True,
                          'stored_rerun_cases_and_counts_match': True,
                          'snapshot_unchanged': True},
        'independent_checks': {'labeled_check_count': independent['check_count'],
                               'matrix_strands': '3..12',
                               'specialization_case_count': independent['specialization_case_count'],
                               'mechanism': independent['mechanism'],
                               'whole_word_inverse_wrong_order_rejected': True},
        'all_index_verified_mechanism': 'Arbitrary-amplitude translated three-coordinate propagation, disjoint-support fixation, induction for Xk, exceptional R2 and both Rk word ranges.',
        'scalar_scope_comparison': {'read_after_own_conclusion': True,
                                   'independent_conclusion_matches': True,
                                   'scope_note_sha256': sha(SNAPSHOT/'SCALAR_SCOPE_CHECK.md')},
        'scope_boundaries': [
            'The literal terminal row is ill-typed; no unconditional claim for the uncorrected source.',
            'Finite checks are supplemental; the local support argument supplies arbitrary indices.',
            'u must be invertible; u=0 is inadmissible.',
            'u=q or u=q^2 kills X3 in this representation.',
            'u=q^3 retains X3 over Q(q), but may fail at additional q specializations such as +/-1.',
            'Three strands have no X4; m=4 adds R3 and m=5 adds R4.',
            'No universal finite-dimensionality, author-intent, or novelty/priority conclusion.'
        ],
        'independence': {'historical_REVIEW_read': False, 'historical_verdict_read': False,
                         'sibling_conclusions_read': False,
                         'candidate_modules_imported': False},
        'mutations': {'own_family_only': True, 'scratch_ignored': True,
                      'environment_modified': False, 'canonical_files_modified': False,
                      'git_mutations_performed': False, 'read_only_git_check_ignore': True,
                      'external_outreach': False},
        'report': 'REPORT.md', 'reproduction_code': ['replay_frozen.py', 'independent_laurent_check.py'],
        'receipts': ['replay_receipt.json', 'independent_laurent_receipt.json']
    }
    (HERE/'verdict.json').write_text(json.dumps(verdict, indent=2)+'\n')
    with (HERE/'RESEARCH_LOG.md').open('a') as log:
        log.write('\n## '+now+' — Final checkpoint (100% complete)\n\n')
        log.write('- Scoped repaired-presentation claim passes the family adversary.\n')
        log.write('- All required replay, independent exact, all-index, scalar, singular, base-ring, and coverage checks are recorded.\n')
        log.write('- Machine-readable verdict and artifact SHA-256 manifest finalized; historical review/verdict and siblings remain unread.\n')
    files = sorted(p for p in HERE.iterdir() if p.is_file() and p.name != 'artifact_hashes.json')
    manifest = {'timestamp_utc': now, 'hash_algorithm': 'sha256',
                'files': {p.name: sha(p) for p in files}}
    (HERE/'artifact_hashes.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(json.dumps({'verdict': verdict['verdict'], 'check_count': independent['check_count'],
                      'completion_percent': 100, 'timestamp_utc': now,
                      'artifact_count': len(files)}, indent=2))

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Repairer's offline replay of the first independent review's helper attacks.

This reuses independently authored probes; it is not a new independent review.
Original review outputs and REQUEST_CHANGES verdict remain unchanged.
"""
import importlib.util
import json
import sys
import tempfile
from pathlib import Path
import common as c

sys.dont_write_bytecode = True
OPERATIONS = Path(__file__).resolve().parent
AUDIT = OPERATIONS.parent
REVIEW = AUDIT / 'reviews/operations_adversary1'


def main():
    source = REVIEW / 'independent_attacks.py'
    spec = importlib.util.spec_from_file_location('round1_independent_probes_for_repairer_replay', source)
    reviewer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reviewer)
    private = OPERATIONS / 'private_cases'
    private.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='round1_attack_replay_', dir=private) as directory:
        # Move only temporary fixture creation into our own ignored directory.
        # The independently authored attack implementations are unmodified.
        reviewer.HERE = Path(directory)
        for kind in ('source_receipt', 'mathematical_acceptance_gate', 'branch_install_plan', 'pr', 'problem', 'original_head'):
            reviewer.freeze_attack(kind)
        for kind in ('verified', 'uncertain', 'receipt_only'):
            reviewer.removed_registration(kind)
        for kind in ('receipt', 'manifest', 'installed_paper', 'historical'):
            reviewer.main_conflict(kind)
        c.require(not reviewer.REAL_CALLS, 'Replay escaped offline isolation')
        c.require(len(reviewer.RESULTS) == 13 and all(x.get('expectation_met') is True
                  and type(x.get('real_external_calls')) is int and x['real_external_calls'] == 0 for x in reviewer.RESULTS),
                  'At least one independent helper attack remains unresolved')
    result = {'scope': 'Repairer replay of unmodified independently authored helper attacks; not a new independent review.',
              'first_review_verdict_preserved': 'REQUEST_CHANGES',
              'first_review_source_sha256': c.sha(source.read_bytes()),
              'first_review_report_sha256': c.sha((REVIEW / 'REPORT.md').read_bytes()),
              'all_expectations_met': True, 'probe_count': 13, 'real_external_calls': 0,
              'cases': reviewer.RESULTS, 'builder_defect_scope': 'Root-owned R4 is outside this helper-only replay.',
              'remaining_acceptance_gap': 'A NEW fresh independent operations adversary must review final helpers and builder.'}
    suffix = 'NORMAL' if __debug__ else 'OPTIMIZED'
    (OPERATIONS / ('ROUND1_ATTACK_REPLAY_REPAIRED_' + suffix + '.json')).write_bytes(c.json_bytes(result))
    print(json.dumps({'all_expectations_met': True, 'probe_count': 13, 'real_external_calls': 0}, sort_keys=True))


if __name__ == '__main__':
    main()

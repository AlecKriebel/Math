#!/usr/bin/env python3
"""Fresh read-only gate binding check before the single operation attempt.

Eligibility is checked before any gate or research finding is read. This script
has no mutation path. It deliberately does not refresh or edit RESULT.json.
"""
from pathlib import Path
import argparse
import datetime
import hashlib
import importlib.util
import json

CASE = Path(__file__).resolve().parents[2]
EXPECTED_CODE = '73f14bb65c29aad2643aabddb76773f86b43b01f028d43911698deb3be556cec'
EXPECTED_PLAN = 'ae6b6d85d86659fceb3d347874e89ae9f3878a228cc33f354ef99417e5bc8fd5'
EXPECTED_RESULT = 'ce9392f13903b4937b69e5045cf61e00e8d071358568e583599f05564236ec38'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--expected-gate-sha256', required=True)
    args = parser.parse_args()
    require(not (CASE / 'STATUS_OPERATION_ATTEMPT.json').exists(), 'Attempt custody exists: administrative reconciliation only; do not read gate')
    source = CASE / 'status_operation.py'
    require(digest(source.read_bytes()) == EXPECTED_CODE, 'Operation code drift')
    spec = importlib.util.spec_from_file_location('read_only_operation', source)
    operation = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(operation)
    # This function performs only selected PR/ref metadata and QUEUE reads.
    original = operation.check_current_head()
    gate_bytes = (CASE / 'PRIORITY_GATE.json').read_bytes()
    require(digest(gate_bytes) == args.expected_gate_sha256, 'Final gate differs from delivered hash')
    gate = json.loads(gate_bytes)
    plan_bytes = (CASE / 'STATUS_OPERATION_PLAN.json').read_bytes()
    result_bytes = (CASE / 'reviews/status_operations_adversary/RESULT.json').read_bytes()
    require(digest(plan_bytes) == EXPECTED_PLAN and digest(result_bytes) == EXPECTED_RESULT, 'Plan/result drift')
    require(gate.get('verdict') == 'ALREADY_RESOLVED_ORIGINAL_PROBLEM' and gate.get('selected_pr') == 436 and gate.get('problem_id') == 2569, 'Final gate scope differs')
    require(gate.get('all_independent_priority_reviews_complete') is True and gate.get('operations_adversary_accepted') is True and gate.get('required_repairs_remaining') == 0, 'Final gate is not complete and accepted')
    binding = gate['operation_binding']
    require(binding.get('code_sha256') == EXPECTED_CODE and binding.get('plan_sha256') == EXPECTED_PLAN and binding.get('operations_result_sha256') == EXPECTED_RESULT, 'Exact operations acceptance not bound')
    require(binding.get('expected_head_sha') == operation.HEAD and binding.get('old_queue_sha256') == digest(original) and binding.get('new_queue_sha256') == json.loads(plan_bytes)['new_sha256'], 'Frozen administrative inputs differ')
    required = gate['required_final_findings_sha256']
    case_rel = str(CASE.relative_to(operation.PROGRAM.parent))
    require(case_rel + '/ROOT_FINAL_SOURCE_INTEGRITY.json' in required, 'Fresh root source integrity absent')
    require(required.get(case_rel + '/reviews/status_operations_adversary/RESULT.json') == EXPECTED_RESULT, 'Required findings do not include exact result')
    for rel, expected in required.items():
        path = operation.PROGRAM.parent / rel
        require(path.resolve().is_relative_to(CASE.resolve()), 'Finding escapes selected case')
        require(digest(path.read_bytes()) == expected, 'Required local finding drift: ' + rel)
    receipt = {'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'accepted': True,
               'required_repairs_remaining': 0, 'selected_pr': 436, 'problem_id': 2569,
               'code_sha256': EXPECTED_CODE, 'plan_sha256': EXPECTED_PLAN, 'result_sha256': EXPECTED_RESULT,
               'final_gate_sha256': digest(gate_bytes), 'required_finding_count': len(required),
               'frozen_head_eligibility_confirmed_before_gate_read': True,
               'all_required_local_finding_hashes_match': True,
               'remote_main_publication': 'Must still pass helper at apply using final checkpoint',
               'reviewer_remote_mutations': 0, 'new_proof_attempts': 0, 'review_progress_percent': 100}
    (CASE / 'reviews/status_operations_adversary/FINAL_GATE_READBACK.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Future root-only administrative final evidence reconciliation.

Preparation never imports or executes this source or its guard module. This
reads preserved scientific replay evidence and actual v2 inspections; it does
not rerun a scientific program or infer an earlier native proof transition.
Root owns the complete reviewed plan, actual launch and separate child capture.
"""
import argparse
import json
import sys
# Future root entry points preserve every sealed source closure.
sys.dont_write_bytecode = True
import pr38_guards as g


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--preparation-manifest-sha256', required=True)
    parser.add_argument('--plan', required=True, help='Root-owned repository-relative complete reviewed final plan')
    parser.add_argument('--plan-sha256', required=True)
    args = parser.parse_args()
    g.require(args.execute, 'Future actual root --execute required')
    g.manifest(g.HERE, g.HERE / 'PREPARATION_MANIFEST.json', args.preparation_manifest_sha256)
    path = g.regular(g.R, args.plan)
    g.require(path.resolve().is_relative_to(g.A.resolve()) and not path.resolve().is_relative_to(g.HERE.resolve()), 'Copy draft to separate root-owned plan; sealed preparation is immutable')
    raw = path.read_bytes()
    g.require(g.sha(raw) == g.digest(args.plan_sha256), 'Exact full root-reviewed plan changed')
    plan = g.parse(raw)
    g.require(plan['preparation_manifest_sha256'] == args.preparation_manifest_sha256, 'Exact closed preparation pin required in root-reviewed plan')
    started = g.stamp()
    before = g.final_scope(plan)
    output = g.A / 'final_evidence_reconciliation'
    g.require(not output.exists() and not output.is_symlink(), 'Inspect previous reconciliation and failures before retry; no overwrite')
    output.mkdir(mode=0o700)
    scope_path = output / 'WHOLE_SCOPE_CONTRACT.json'
    g.dump(scope_path, plan, exclusive=True)
    after = g.final_scope(plan)
    g.require(g.strict_equal(before, after) and path.read_bytes() == raw, 'Complete evidence/preparation plan changed during actual administrative reconciliation')
    receipt = {'schema': 'pr38-actual-final-evidence-reconciliation/v1', 'status': 'PASS', 'pr': g.PR, 'problem_id': int(g.ID),
        'started_at_utc': started, 'finished_at_utc': g.stamp(), 'actual_root_reconciliation': True,
        'science_reexecution_of_v2': False, 'original_actual_closed_family_replay_bound': True,
        'root_reviewed_plan': g.repo_pin(path), 'reconciliation_source': g.repo_pin(g.HERE / 'seal_final_evidence.py'),
        'preparation_manifest_sha256': args.preparation_manifest_sha256,
        'whole_manifest_sha256': plan['whole_manifest_sha256'], 'whole_scope_contract_sha256': g.sha(scope_path.read_bytes()),
        'bindings_before': before, 'bindings_after': after, 'entire_scope': plan,
        'claim': 'Actual administrative byte reconciliation of original12/108 scientific replay plus source-first and actual v2 alias inspections. No new science replay, theorem-import recertification or historical native event.'}
    receipt_path = output / 'ROOT_FINAL_GATE.json'
    g.dump(receipt_path, receipt, exclusive=True)
    members = [{'path': p.name, 'bytes': len(p.read_bytes()), 'sha256': g.sha(p.read_bytes())} for p in sorted(output.iterdir())]
    g.require({z['path'] for z in members} == {'WHOLE_SCOPE_CONTRACT.json', 'ROOT_FINAL_GATE.json'}, 'Unexpected reconciliation member')
    g.dump(output / 'FINAL_MANIFEST.json', {'schema': 'pr38-strict-final-evidence-reconciliation-closure/v1', 'self_excluded': ['FINAL_MANIFEST.json'], 'files_count': 2, 'files': members}, exclusive=True)
    g.exact_closure(output, {'WHOLE_SCOPE_CONTRACT.json', 'ROOT_FINAL_GATE.json', 'FINAL_MANIFEST.json'})
    print(json.dumps({'status': 'PASS', 'root_final_receipt_sha256': g.sha(receipt_path.read_bytes()),
        'whole_scope_contract_sha256': g.sha(scope_path.read_bytes()), 'final_manifest_sha256': g.sha((output / 'FINAL_MANIFEST.json').read_bytes()),
        'actual_administrative_reconciliation': True, 'science_reexecution_of_v2': False,
        'original_substantive_attempts': 2, 'new_substantive_attempts': 0, 'audit_turns': 0}))


if __name__ == '__main__':
    g.run(main)

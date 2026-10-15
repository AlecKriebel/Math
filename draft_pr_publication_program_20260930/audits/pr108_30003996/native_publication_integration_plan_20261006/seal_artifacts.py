"""Seal the planning deliverable; read-only Git/gh, writes only beside this file."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess
D = Path(__file__).resolve().parent
A = D.parent
C = A.parents[2]
K = '30003996'
P = 'unsolved_math_prioritization/'
N = P + 'attempts/' + K + '/'
def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(data):
    return hashlib.sha256(data).hexdigest()
def pin(path):
    data = path.read_bytes()
    return {'path': str(path.relative_to(D)), 'bytes': len(data), 'sha256': sha(data)}
def dump(name, obj):
    (D / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')
def main():
    records = []
    receipts = D / 'seal_receipts'
    receipts.mkdir(exist_ok=False)
    def run(argv):
        start = now()
        process = subprocess.Popen(argv, cwd=C, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        index = len(records)
        (receipts / (str(index) + '.stdout.bin')).write_bytes(out)
        (receipts / (str(index) + '.stderr.bin')).write_bytes(err)
        records.append({'argv': argv, 'cwd': str(C), 'PID': process.pid, 'UTC_start': start,
                        'UTC_end': now(), 'exit_code': process.returncode, 'stdout_bytes': len(out),
                        'stdout_sha256': sha(out), 'stderr_bytes': len(err), 'stderr_sha256': sha(err),
                        'stdout_file': 'seal_receipts/' + str(index) + '.stdout.bin',
                        'stderr_file': 'seal_receipts/' + str(index) + '.stderr.bin'})
        dump('SEAL_PROCESS_JOURNAL.json', {'actual_operator_PID': os.getpid(), 'records': records})
        if process.returncode:
            raise RuntimeError(err.decode())
        return out
    head = run(['/usr/bin/git', 'rev-parse', 'HEAD']).decode().strip()
    branch = run(['/usr/bin/git', 'symbolic-ref', '--short', 'HEAD']).decode().strip()
    diff = run(['/usr/bin/git', 'diff', '--name-only', '--', N]).decode()
    tree = run(['/usr/bin/git', 'ls-tree', '-r', '--name-only', head, '--', N]).decode()
    live = json.loads(run(['gh', 'pr', 'view', '108', '--repo', 'AlecKriebel/Math', '--json',
                          'number,state,isDraft,headRefName,headRefOid,baseRefName,url']))
    auth = json.loads((A / 'original_source_authentication_20261006/ORIGINAL_BLOB_MANIFEST.json').read_text())
    template = json.loads((D / 'CONFIG_TEMPLATE_DO_NOT_RUN.json').read_text())
    original = [N + 'historical_original/' + item['relative_path'] for item in auth['files']]
    effective = []
    for item in template['effective_diagnostics_pins']:
        name = str(Path(item['path']).relative_to(Path('draft_pr_publication_program_20260930/audits/pr108_30003996/repaired_diagnostics_v1')))
        effective.append(N + ('EFFECTIVE_DIAGNOSTICS_README.md' if name == 'README.md' else name))
    fixed = [N + name for name in ['README.md', 'RESEARCH_LOG.md', 'PUBLICATION_EVIDENCE.json',
                                   'IMPORT_BASELINE.json', 'HISTORICAL_DESK_ASSESSMENT.json', 'assessment.json',
                                   'source_record.json', 'prior_imported_report.json']]
    gates = [N + 'publication/gates/' + role + '.json' for role in
             ['mathematics', 'priority', 'package', 'pre_execution_adversary', 'final']]
    publication = [N + 'publication/' + name for name in ['PACKAGE_MANIFEST.json', 'ACTUAL_PUBLICATION_RECEIPT.json',
                                                         'DOI_METADATA_RESPONSE.json', 'ACTUAL_TRACKER_READBACK.json']]
    rules = {'schema': 'pr108-native-affected-path-selection/v1', 'UTC': now(),
             'review_bundle_only': True, 'native_export_executed': False,
             'global_candidate_allowlist': [P + name for name in ['assessments.json', 'state.json', 'history.jsonl',
                 'assessment_history.jsonl', 'catalog.json', 'ranking.csv', 'summary.json', 'SHORTLIST.md', 'QUEUE.md']],
             'global_selection_rule': 'Offer only bytes differing from the pinned main parent; no foreign row mutation.',
             'fixed_native_destinations': sorted(original + effective + fixed + gates + publication),
             'package_destinations': 'Exact manifest relative_path -> ' + N + 'publication/package/<relative_path>',
             'payload_receipt_destinations': N + 'publication/payload_readbacks/<0..package-file-count-minus-one>.json',
             'native_destination_precondition': 'Entire target attempt absent on main and in worktree before and after prepare.',
             'protected_paths': ['.git/**', P + 'cache/**', P + 'queue.py', P + 'policy.json', P + 'manifest.json',
                                 P + 'review_v2/**', 'all sibling attempt paths', 'all global tracker paths', 'all foreign audit paths'],
             'unrelated_catalog_preservation': 'Full baseline row including rank and list position; 48 is a dated observation, not a future assumed count.',
             'original_status': 'claimed_solved', 'original_budget': '2/5',
             'original_structured_ledger_present': False, 'new_central_proof_search_turns': 0}
    dump('AFFECTED_PATH_RULES.json', rules)
    tests = json.loads((D / 'OFFLINE_FIXTURE_RESULTS.json').read_text())
    if not tests['normal_and_optimized_passed'] or tests['fixture_tests_per_mode'] != 13:
        raise RuntimeError('Final fixture results incomplete')
    stamp = now()
    (D / 'RESEARCH_LOG.md').write_text(
        '# PR108 native publication integration planning log\n\n'
        'Scope: nonexecuted plan/helper in this dedicated folder. No shared Git, native, remote, service or outreach mutation authority.\n\n'
        '- 2026-10-06T05:17:53+00:00 — Planning subtask 0%. Read supplied scope and applicable repository instructions. Existing mathematical gate reports 100%; priority clearance pending; author effort2/5, new proof-search turns0.\n'
        '- 2026-10-06T05:21:27.266625+00:00 — Planning subtask 30%. Actual bounded context collector authenticated 15 incoming files with no structured ledger, raw/SQL/submitted source equality, imported report{}, main94cb59e6, original OPEN/draft head, no native target, and48 existing unrelated stale catalog projections. Source cache read and hashed in place; no backend copy/download.\n'
        '- 2026-10-06T05:27:31.963174+00:00 — Planning subtask 70%. First helper draft and10 pure fixtures passed normally and under-O. Native CLI lacks claimed_solved choice; explicit dated baseline import plus source-pinned assess function selected. No real prepare/assess execution.\n'
        '- 2026-10-06T05:30:55.324486+00:00 — Planning subtask 80%. Unusable config/gate templates written with no commissioning, package or DOI. Exact source/diagnostic pins retained.\n'
        '- 2026-10-06T05:34:02.489503+00:00 — Planning subtask 90%. Eleven fixtures passed after multiline CSV coverage and actual published payload checks. Original and unrelated native rows/history/campaign scores remain proposed invariants, not runtime successes.\n'
        '- ' + tests['UTC'] + ' — Planning subtask 95%. Final13 pure fixtures and syntax checks passed normally and under-O, including ZIP member validation without filesystem extraction. Fixtures establish only their named helper behaviors; the real native pipeline remains unexecuted.\n'
        '- ' + stamp + ' — Planning deliverable 100%; execution readiness remains conditional. Plan, explicit affected-path rules, inert templates, helper, logs, input/output manifests and actual read/test receipts sealed. Current mathematical clearance is the existing root report; no new novelty, publication or integration success claimed. Native integration/publication/merge executed0%; original effort2/5 preserved in the proposed dated import interpretation; audit proof-search turns0. Parent must commission a fresh independent pre-execution adversary and renew actual gates/parent/DIFF/readbacks.\n\n'
        'An early read-only global Git status was inadvertently unscoped and returned truncated sparse-checkout output. Failed/truncated preliminary reads are retained separately and excluded from evidence. Later authoritative Git/gh reads are bounded and have actual receipts. No other PR body was processed.\n')
    completion = {'schema': 'pr108-native-plan-deliverable-completion/v1', 'UTC': stamp,
                  'actual_operator_PID': os.getpid(), 'planning_subtask_percent': 100,
                  'native_integration_executed': False, 'native_assess_executed': False,
                  'publication_executed': False, 'merge_executed': False, 'outreach_prepared_or_sent': False,
                  'shared_Git_index_branch_remote_mutated': False, 'original_budget': '2/5',
                  'original_structured_ledger_present': False, 'new_central_proof_search_turns': 0,
                  'mathematical_clearance_is_existing_root_report': True, 'priority_clearance_asserted': False,
                  'pre_execution_adversary_still_required': True, 'future_commissioning_still_required': True,
                  'fixture_tests_per_mode': 13, 'normal_and_optimized_passed': True,
                  'final_read_only_main_parent': head, 'final_read_only_branch': branch,
                  'final_read_only_native_target_diff': diff, 'final_read_only_native_target_tree': tree,
                  'native_target_directory_present_at_seal': (C / N).exists(), 'final_read_only_PR_metadata': live,
                  'helper_pin': pin(D / 'prepare_review_bundle.py'), 'plan_pin': pin(D / 'PLAN.md')}
    dump('TASK_COMPLETION.json', completion)
    excluded = {'OUTPUT_MANIFEST.json', 'SEAL_RECEIPT.json'}
    files = [pin(path) for path in sorted(D.rglob('*')) if path.is_file() and path.name not in excluded]
    dump('OUTPUT_MANIFEST.json', {'schema': 'pr108-native-plan-output-byte-manifest/v1', 'UTC': now(),
                                 'self_exclusions': sorted(excluded), 'files': files,
                                 'total_bytes': sum(item['bytes'] for item in files)})
    seal = {'schema': 'pr108-native-plan-seal/v1', 'UTC': now(), 'actual_operator_PID': os.getpid(),
            'output_manifest_pin': pin(D / 'OUTPUT_MANIFEST.json'),
            'context_input_manifest_pin': pin(D / 'CONTEXT_INPUT_MANIFEST.json'),
            'helper_pin': pin(D / 'prepare_review_bundle.py'), 'file_count': len(files),
            'planning_subtask_percent': 100, 'real_native_prepare_executed': False,
            'real_native_assess_executed': False, 'publication_or_merge_executed': False}
    dump('SEAL_RECEIPT.json', seal)
    print(json.dumps({'UTC': seal['UTC'], 'files': len(files), 'total_manifested_bytes': sum(x['bytes'] for x in files),
                      'helper_sha256': seal['helper_pin']['sha256'], 'seal_receipt_pin': pin(D / 'SEAL_RECEIPT.json'),
                      'real_native_prepare_executed': False}))
if __name__ == '__main__':
    main()

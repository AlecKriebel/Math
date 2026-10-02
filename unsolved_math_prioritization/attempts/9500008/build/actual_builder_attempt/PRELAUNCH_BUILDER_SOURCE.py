#!/usr/bin/env python3
"""Static PR39 administrative builder; root executes only after actual evidence.

Adapted from closed PR38 current_execution_revision's administrative contract.
No research-code import, verifier execution, mathematical search, network,
Git mutation or canonical/shared native write. A NEW whole-current gate remains
pending. All copied outputs are read-only; old writers must use fresh private
directories with no copied saved result before any separately reviewed replay.
"""
from __future__ import annotations

import argparse
import ctypes
import datetime as dt
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import traceback

HEAD = '652b8115080e5e97b2274cb602de3faf8c551f20'
BASE = 'c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
SNAPSHOT_SHA = 'debd6fd2621f401ec927c441da3b54a13ca60ee917698898299ad24faf67616e'
SCOPE_SHA = 'bb498651cba86e9e06922b3d598c737ced8ddd2cf656a0346db9ec6c2abc1c52'
READ_SHA = '98300bb8122e86203fd87276ad87a2865d671fce3f22becc6608b52ababfc868'
ADDENDUM_SHA = 'c36d6ae8fd8d6d0fa04e2ee37b211cbc2b653ff61c35c9d9f05279f0c9ecf21f'
QUALIFICATION_SHA = 'bc236c9118d066589f6c16bfa246996af5ba05a6f42b1247a2b74d0fdc7b1ade'
STATEMENT_SHA = '8657a696b6f2139cdc191ebb854db37bdbc5e175b1725499e14ca7aea50beb52'
PAIR_SHA = 'ee839ad6359f75822db9ac6a2ad1e1b8069895d6bccab37fd3b055441a626f32'
PR_URL = 'https://github.com/AlecKriebel/Math/pull/39'
GATE = 'pending_NEW_whole_current_packet_source_first_adversary'
HEADER = ['Rank', 'ID / code', 'Problem', 'EV', 'Impact (/10)', 'Difficulty', 'Proposed', 'Status', 'Turns', 'Chat', 'Findings', 'DOI']
FORBIDDEN = {'.git', '__pycache__'}
CLOCK_KEYS = {'utc', 'time_utc', 'at', 'started_utc', 'ended_utc'}
HISTORICAL_TOP = ['PARTIAL.md', 'verify.py', 'verification.json', 'source_record.json', 'prior_report.json', 'source_checksums.json', 'turns.json',
                  'review/submitted_verify.py', 'review/submitted_results.json', 'review/independent_checks.py', 'review/independent_results.json']
SOURCE_NAMES = {'prepare_current_packet.py', 'INPUT_PINS.json', 'ADAPTATION_BASIS.json', 'CURRENT_REFLECTION_REPAIR.md', 'README.md', 'ROOT_GUARD_CONTRACT.md', 'RESEARCH_LOG.md'}


def require(condition, message):
    if not condition: raise ValueError(message)


def sha(data): return hashlib.sha256(data).hexdigest()


def encoded(value): return (json.dumps(value, indent=2, ensure_ascii=False)+'\n').encode()


def relative(value):
    require(isinstance(value, str) and value and '\\' not in value, 'Invalid relative path')
    path = PurePosixPath(value)
    require(not path.is_absolute() and str(path) == value and not {'.', '..'}.intersection(path.parts), 'Noncanonical/unsafe path: '+value)
    require(not FORBIDDEN.intersection(path.parts) and path.suffix not in {'.pdf', '.pyc', '.tmp', '.html', '.sqlite'}, 'Scratch/foreign path prohibited: '+value)
    return value


def regular_inventory(root, excluded_files=(), cache_prefix=None):
    found = set()
    for path in root.rglob('*'):
        name = path.relative_to(root).as_posix()
        if name in excluded_files or (cache_prefix and PurePosixPath(name).parts[0] == cache_prefix): continue
        require(not path.is_symlink(), 'Symlink in strict inventory: '+name)
        if path.is_file(): found.add(relative(name))
        else: require(path.is_dir(), 'Nonregular inventory member: '+name)
    return found


def publish_absent(stage, destination):
    require(sys.platform == 'darwin', 'Exclusive atomic rename requires the reviewed macOS host')
    libc = ctypes.CDLL(None, use_errno=True); rename = libc.renamex_np
    rename.argtypes, rename.restype = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint], ctypes.c_int
    if rename(os.fsencode(stage), os.fsencode(destination), 0x00000004) != 0:
        number = ctypes.get_errno(); raise OSError(number, os.strerror(number), str(destination))


def arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--root-receipt', required=True)
    parser.add_argument('--root-receipt-sha256', required=True)
    parser.add_argument('--root-replay-script', required=True)
    parser.add_argument('--root-replay-script-sha256', required=True)
    parser.add_argument('--root-executed-collector', required=True)
    parser.add_argument('--root-executed-collector-sha256', required=True)
    parser.add_argument('--root-scope-certificate-sha256', required=True)
    parser.add_argument('--root-read-ledger-sha256', required=True)
    parser.add_argument('--root-retention-manifest', required=True)
    parser.add_argument('--root-retention-manifest-sha256', required=True)
    parser.add_argument('--root-current-input-manifest', required=True)
    parser.add_argument('--root-current-input-manifest-sha256', required=True)
    parser.add_argument('--root-science-card', required=True)
    parser.add_argument('--root-science-card-sha256', required=True)
    parser.add_argument('--root-replay-read-attestation', required=True)
    parser.add_argument('--root-replay-read-attestation-sha256', required=True)
    return parser.parse_args()


def execute(args, script, audit, repo, attempt):
    require(not sys.flags.optimize, 'Assertions must be enabled')
    destination = audit/'reviewed_candidate'
    require(not destination.exists() and not destination.is_symlink(), 'Never overwrite an existing candidate')
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    dependencies, retained, git_records = {}, {}, []

    def git(*arguments):
        require(arguments and arguments[0] in {'branch', 'show', 'ls-tree', 'diff', 'rev-parse'}, 'Read-only Git capability only')
        require(arguments[0] != 'branch' or arguments[1:] == ('--show-current',), 'Read-only branch query only')
        index = len(git_records); command = ['git', *arguments]
        row = {'argv': command, 'cwd': str(repo), 'started_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
               'launch_attempted': False, 'actual_execution': False, 'completed': False, 'exit_code': None, 'stdin_supplied': False,
               'retention_errors': []}
        git_records.append(row)
        directory = attempt/'git'
        error = original_traceback = process = None
        popen_called = False
        def retain(channel,data,available=True):
            path = directory/(str(index)+'.'+channel)
            try:path.write_bytes(data)
            except OSError as caught:
                row['retention_errors'].append({'stage':'primary_stream_retention','type':type(caught).__name__,'message':str(caught)})
                path = attempt/'retention_fallback'/(str(index)+'.'+channel)
                try:path.parent.mkdir(exist_ok=True);path.write_bytes(data)
                except BaseException as secondary:
                    row['retention_errors'].append({'stage':'fallback_stream_retention','type':type(secondary).__name__,'message':str(secondary)})
                    print('Available readonly Git '+channel+' bytes follow; filesystem retention failed:',file=sys.stderr)
                    sys.stderr.buffer.write(data);raise
            row[channel] = {'path':path.relative_to(attempt).as_posix(),'size':len(data),'sha256':sha(data),'available':available}
        def save(): (attempt/'GIT_COMMANDS.json').write_bytes(encoded(git_records))
        try:
            directory.mkdir(exist_ok=True)
            for channel in ['stdout','stderr']: retain(channel,b'',False)
            row['stdio_kind']='prelaunch_empty_placeholder';save()
            require(not row['retention_errors'],'Prelaunch retention failed; no command may run')
            row['launch_attempted']=True;save()
            try:
                popen_called=True
                process=subprocess.run(command,cwd=repo,capture_output=True,timeout=180,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
                row.update(actual_execution=True,completed=True,exit_code=process.returncode,stdio_kind='complete_child_streams')
                values={'stdout':process.stdout,'stderr':process.stderr}
            except subprocess.TimeoutExpired as caught:
                error,original_traceback=caught,caught.__traceback__
                row.update(actual_execution=True,completed=False,stdio_kind='partial_timeout')
                values={'stdout':caught.stdout,'stderr':caught.stderr}
            except OSError as caught:
                error,original_traceback=caught,caught.__traceback__
                row.update(actual_execution=False,completed=False,stdio_kind='no_child_launched')
                values={'stdout':None,'stderr':None}
            if error:row['failure']={'type':type(error).__name__,'message':str(error),'errno':getattr(error,'errno',None)}
            for channel,value in values.items():
                data=value.encode() if isinstance(value,str) else value or b''
                retain(channel,data,value is not None)
        except BaseException as caught:
            if not popen_called:row['launch_attempted']=False;row['failure_stage']='prelaunch_retention'
            if error is None:
                error,original_traceback=caught,caught.__traceback__
                row['failure']={'type':type(caught).__name__,'message':str(caught)}
            else:row['retention_errors'].append({'stage':'stream_retention','type':type(caught).__name__,'message':str(caught)})
        finally:
            row['ended_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
            try:save()
            except BaseException as caught:
                row['retention_errors'].append({'stage':'ledger_retention','type':type(caught).__name__,'message':str(caught)})
                print(json.dumps(row),file=sys.stderr)
        if error:raise error.with_traceback(original_traceback)
        require(not row['retention_errors'],'Readonly Git retention failed; available evidence preserved')
        require(process.returncode==0,'Readonly Git command failed; real full streams preserved')
        return process.stdout

    require(git('branch', '--show-current').strip() == b'main', 'Stay on main')

    def bind(name, role, expected=None):
        name = relative(name); path = audit/name
        require(path.is_file() and not path.is_symlink(), 'Missing/nonregular input: '+name)
        require(all(not parent.is_symlink() for parent in path.parents if parent != audit.parent), 'Symlink ancestor: '+name)
        data = path.read_bytes(); record = {'path': name, 'bytes': len(data), 'sha256': sha(data), 'role': role}
        require(expected is None or record['sha256'] == expected, 'Explicit input pin changed: '+name)
        require(name not in dependencies or dependencies[name]['sha256'] == record['sha256'], 'Input changed during build: '+name)
        dependencies[name] = record; return data

    revision = json.loads(bind('current_execution_revision/REVISION_MANIFEST.json', 'reviewed_execution_source_revision_manifest'))
    require(revision['excluded'] == ['REVISION_MANIFEST.json'] and len(revision['files']) == 4 and len({x['path'] for x in revision['files']}) == 4, 'Exact revision source closure required')
    require(regular_inventory(script.parent) == {x['path'] for x in revision['files']}|{'REVISION_MANIFEST.json'}, 'Exact adjacent revision membership required')
    for row in revision['files']:
        raw = bind('current_execution_revision/'+relative(row['path']), 'root_reviewed_exact_administrative_revision', row['sha256'])
        require(type(row['size']) is int and len(raw) == row['size'], 'Exact revised source size')
    exception = json.loads(bind('current_execution_revision/RETAINED_CAPABILITY_EXCEPTIONS.json', 'exact_historical_run1_capability_rows'))
    require(exception['root_support_manifest_sha256'] == args.root_retention_manifest_sha256 and len(exception['files']) == 8, 'Only exact reviewed support exceptions')
    exception_rows = {x['path']:x for x in exception['files']}
    require(len(exception_rows) == 8 and all(x.endswith('.run1') for x in exception_rows), 'Distinct exact historical exception rows')
    preparation = json.loads(bind('current_preparation_family/PREPARATION_MANIFEST.json', 'exact_static_builder_manifest'))
    require(preparation['excluded'] == ['PREPARATION_MANIFEST.json'] and {x['path'] for x in preparation['files']} == SOURCE_NAMES, 'Exact prepared source closure required')
    require(regular_inventory(audit/'current_preparation_family') == SOURCE_NAMES|{'PREPARATION_MANIFEST.json'}, 'Exact root preparation inventory required')
    for row in preparation['files']:
        raw = bind('current_preparation_family/'+relative(row['path']), 'reviewed_static_builder_source', row['sha256'])
        require(len(raw) == row['size'], 'Prepared source size differs')
    pins = json.loads(bind('current_preparation_family/INPUT_PINS.json', 'original_and_closed_input_pins'))
    for name in [args.root_receipt,args.root_replay_script,args.root_current_input_manifest,args.root_science_card,args.root_replay_read_attestation]:
        require(PurePosixPath(relative(name)).parent.as_posix()=='.','Root prerequisite must be directly at the audit root, never private scratch')
    root_raw = bind(args.root_receipt, 'actual_root_complete_reproduction_receipt', args.root_receipt_sha256); root = json.loads(root_raw)
    require(root.get('status') == 'PASS' and root.get('head') == HEAD and root.get('base') == BASE, 'Actual PASS for exact PR39 head/base required')
    require(root.get('exact_original_file_count') == 16 and root.get('changed_diff_path_count') == 17 and root.get('closed_family_count') == 3, 'Actual original16/17 and three families required')
    require(root.get('authored_members_verified_before_and_after') == 732, 'All732 first-party members before/after required')
    require(root.get('original_substantive_turns') == 2 and root.get('turn_limit') == 5 and root.get('new_substantive_attempts') == root.get('audit_turns') == 0, 'Preserve original2/5, new0/audit0')
    require(root.get('full_problem_solved') is False and root.get('retention_errors') == [], 'Unsolved complete retained actual attempt required')
    wrapper = bind(args.root_replay_script, 'actual_root_entrypoint_source', args.root_replay_script_sha256)
    collector = bind(args.root_executed_collector, 'actual_root_collector_source', args.root_executed_collector_sha256)
    require(root['root_script_path'] == args.root_replay_script and root['root_script_sha256'] == args.root_replay_script_sha256, 'Actual root wrapper pin required')
    require(root['executed_collector_path'] == args.root_executed_collector and root['executed_collector_sha256'] == args.root_executed_collector_sha256, 'Actual executed collector pin required')
    scope = bind('ROOT_PARTIAL_SCOPE_CERTIFICATE.md', 'root_scientific_scope_certificate', args.root_scope_certificate_sha256)
    require(args.root_scope_certificate_sha256 == SCOPE_SHA, 'Exact root scope certificate required')
    ledger_raw = bind('ROOT_PRIMARY_READ_LEDGER.json', 'direct_root_primary_reading_ledger', args.root_read_ledger_sha256); ledger = json.loads(ledger_raw)
    require(args.root_read_ledger_sha256 == READ_SHA and ledger['scope_certificate_sha256'] == SCOPE_SHA and ledger['reading_completed'] is True and ledger['new_substantive_attempts'] == 0, 'Exact genuine root reading ledger required')
    addendum_raw = bind('ROOT_PRIMARY_READ_ADDENDUM.json', 'root_primary_reading_addendum', ADDENDUM_SHA); addendum = json.loads(addendum_raw)
    qualification = bind('ROOT_PRIMARY_PROOF_QUALIFICATIONS.md', 'root_imported_primary_proof_qualifications', QUALIFICATION_SHA)
    require(addendum['prior_read_ledger_sha256'] == READ_SHA and addendum['primary_proof_qualification_sha256'] == QUALIFICATION_SHA and addendum['new_substantive_attempts'] == addendum['audit_attempts_added'] == 0, 'Read addendum/qualification chain required')
    require(root['root_primary_read_ledger'] == {'path':'ROOT_PRIMARY_READ_LEDGER.json','size':len(ledger_raw),'sha256':READ_SHA}, 'Actual replay must bind exact reading input')
    card_raw = bind(args.root_science_card, 'genuine_future_root_science_card', args.root_science_card_sha256); card = json.loads(card_raw)
    require(card.get('status') == 'UNSOLVED' and card.get('full_problem_solved') is False and card.get('partial_valid') is True, 'Genuine scoped UNSOLVED science card required')
    require(card.get('scope_certificate_sha256') == SCOPE_SHA and card.get('read_ledger_sha256') == READ_SHA and card.get('read_addendum_sha256') == ADDENDUM_SHA and card.get('proof_qualifications_sha256') == QUALIFICATION_SHA, 'Science card must bind actual complete primary/science chain')
    require(card.get('original_substantive_attempts') == 2 and card.get('turn_limit') == 5 and card.get('new_substantive_attempts') == card.get('audit_attempts_added') == 0, 'Science accounting required')
    require(card.get('current_model') is None and card.get('current_reasoning_effort') is None and card.get('current_deadline_utc') is None, 'Unavailable current exposure/deadline must be null')
    require(card.get('novelty_claimed') is False and card.get('new_whole_current_gate') == 'PENDING', 'No transferred current verdict/novelty claim')
    require(card.get('actual_replay_receipt_sha256') == args.root_receipt_sha256 and card.get('actual_replay_read_attestation_sha256') == args.root_replay_read_attestation_sha256,'Science card must bind actual receipt and separate new reading')
    attestation_raw=bind(args.root_replay_read_attestation,'genuine_new_root_replay_and_source_reading_attestation',args.root_replay_read_attestation_sha256);attestation=json.loads(attestation_raw)
    require(attestation.get('reading_completed') is True and attestation.get('root_receipt_sha256')==args.root_receipt_sha256,'Genuine separate root reading of actual evidence required')
    require(attestation.get('scope_certificate_sha256')==SCOPE_SHA and attestation.get('primary_read_ledger_sha256')==READ_SHA and attestation.get('read_addendum_sha256')==ADDENDUM_SHA and attestation.get('proof_qualifications_sha256')==QUALIFICATION_SHA,'Separate root attestation must preserve complete primary chain')
    require(attestation.get('root_entrypoint_sha256')==args.root_replay_script_sha256 and attestation.get('executed_collector_sha256')==args.root_executed_collector_sha256 and attestation.get('primary_read_ledger_modified') is False,'Actual source/read-ledger provenance required')
    require(attestation.get('original_substantive_attempts')==2 and attestation.get('new_substantive_attempts')==attestation.get('audit_attempts_added')==0,'Reading attestation changes no original research budget')
    current_raw = bind(args.root_current_input_manifest, 'genuine_root_current_complete_preimages', args.root_current_input_manifest_sha256); current = json.loads(current_raw)
    require(current.get('approved_by_root') is True and current.get('reason') and current.get('current_head'), 'Explicit genuine root current preimages required')
    require(root['current_input_manifest'] == {'path':args.root_current_input_manifest,'size':len(current_raw),'sha256':args.root_current_input_manifest_sha256}, 'Actual root must bind current preimage manifest')
    require(root['native_full_file_preimages_before_and_after'] == current['files'] and root['current_head_unchanged'] == current['current_head'] == git('rev-parse','HEAD').decode().strip(), 'Actual complete native preimages/HEAD must remain unchanged')
    native_names = {'unsolved_math_prioritization/'+name for name in ['QUEUE.md','state.json','history.jsonl','catalog.json','assessments.json','queue.py','policy.json','manifest.json','cache/problems.json','cache/research_results.json','cache/catalog.sqlite','review_v2/related_target_groups.json']}|{'draft_pr_publication_program_20260930/inventory.json'}
    require(len(current['files']) == 13 and {x['path'] for x in current['files']} == native_names, 'Exact thirteen complete current preimages required')
    def validate_native_preimages():
        for row in current['files']:
            name = PurePosixPath(row['path']); require(not name.is_absolute() and '..' not in name.parts and name.as_posix() == row['path'], 'Unsafe native preimage')
            path = repo/name; require(path.is_file() and not path.is_symlink() and all(not x.is_symlink() for x in path.parents if x != repo.parent), 'Nonregular native preimage')
            data = path.read_bytes(); require(len(data) == row['size'] and sha(data) == row['sha256'], 'Native preimage changed after actual replay')
    validate_native_preimages()

    snapshot_raw = bind('snapshot_manifest.json', 'exact_original16_manifest', SNAPSHOT_SHA); snapshot = json.loads(snapshot_raw)
    require(snapshot['head'] == HEAD and snapshot['base'] == BASE and snapshot['pr'] == 39 and str(snapshot['problem']) == '9500008', 'Wrong original source')
    require(len(snapshot['files']) == 16 and len(snapshot['changed_paths']) == 17, 'Exact original16/17 required')
    original = {}
    for row in snapshot['files']:
        name = relative(row['path']); require(name not in original and row['mode'] == '100644', 'Unique original100644 members required')
        data = bind('source_snapshot/'+name, 'immutable_original16_source', row['sha256']); require(len(data) == row['size'], 'Original size differs')
        target = 'unsolved_math_prioritization/attempts/9500008/'+name
        require(git('show', HEAD+':'+target) == data and git('ls-tree', HEAD,'--',target).decode().strip() == row['mode']+' blob '+row['git_blob']+'\t'+target, 'Exact original native Git bytes/mode/blob required')
        original[name] = data
    require(regular_inventory(audit/'source_snapshot') == set(original), 'Exactly16 original archive files required')
    diff = bind('pr_input/diff.patch', 'full_original49891_byte17_path_diff', snapshot['diff_sha256'])
    require(len(diff) == snapshot['diff_bytes'] == 49891 and git('diff', BASE,HEAD) == diff and git('diff','--name-only',BASE,HEAD).decode().splitlines() == snapshot['changed_paths'], 'Exact full original diff required')
    metadata_raw = bind('pr_input/metadata.json', 'frozen_original_draft_metadata', pins['auxiliary'][0]['sha256']); metadata = json.loads(metadata_raw)
    require(metadata['number'] == 39 and metadata['headRefOid'] == HEAD and metadata['isDraft'] is True, 'Frozen original draft metadata differs')
    problem, prior, readiness, turns, verdict = [json.loads(original[name]) for name in ['source_record.json','prior_report.json','readiness.json','turns.json','review/verdict.json']]
    require(problem['id'] == 9500008 and problem['problem_number'] == 'AMR-094-0008' and 'problem' not in problem and prior, 'Entire flat source and actual nonempty prior required')
    require(sha(problem['statement'].encode()) == STATEMENT_SHA and sha(json.dumps([problem,prior],sort_keys=True).encode()) == PAIR_SHA, 'Exact whole statement/source-prior pair required')
    require(turns['count'] == len(turns['attempts']) == readiness['budget']['used'] == 2 and readiness['budget']['maximum_substantive_attempts'] == 5 and [x['number'] for x in turns['attempts']] == [1,2], 'Exact authored local2/5 ledger required')
    require([x['outcome'] for x in turns['attempts']] == ['unresolved','partial'] and readiness['outcome'] == 'unresolved' and verdict['full_problem_solved'] is False, 'Unresolved plus scoped partial required')
    require(sha(original['PARTIAL.md']) == turns['attempts'][1]['sha256'] == readiness['reviewed_artifact_sha256'] == verdict['artifact_sha256'], 'Original PARTIAL seal must remain exact')
    provenance = root['provenance']
    require(provenance['status'] == 'PASS_READONLY_PROVENANCE_REPRODUCTION' and provenance['complete_flat_problem'] == problem and provenance['complete_actual_prior_report'] == prior, 'Actual full source and PRESENT prior required')
    require(provenance['prior_raw_key_present'] is True and provenance['prior_fallback_used'] is False and provenance['raw_and_SQL_full_pair_equal_snapshot_and_root_pins'] is True, 'No null/missing-report fallback for PR39')
    require(provenance['raw_corpus_bytes'] == 149266659 and provenance['problem_count'] == 15458 and provenance['research_report_count'] == 6701 and provenance['full_raw_and_SQL_importer_join_checked'] is True and provenance['SQL_mode'] == 'ro, immutable, query_only', 'Full149MB/allSQL provenance required')
    require(provenance['pure_queue_score'] == pins['pure_queue_score'] and provenance['pure_queue_score']['review_hash'] == PAIR_SHA, 'Exact pure score full pair required')
    expected_git = [{'path':'unsolved_math_prioritization/attempts/9500008/'+x['path'],'mode':x['mode'],'git_blob':x['git_blob'],'size':x['size'],'sha256':x['sha256']} for x in snapshot['files']]
    require(provenance['original_git_files'] == expected_git and provenance['changed_diff_paths'] == snapshot['changed_paths'] and provenance['full_diff_bytes'] == 49891 and provenance['full_diff_sha256'] == sha(diff), 'Complete actual Git/diff provenance required')
    native = provenance['current_native_target']; require(native['state'] is None and native['history_events'] == [] and native['catalog']['local_status'] == 'queued' and native['catalog']['turns_used'] == 0, 'Canonical absence/queued0 distinct from local2/5 required')
    require(provenance['target_attempt_absent_at_base_current_HEAD_and_private_native'] is True, 'No fabricated original native events/attempt tree')
    closure = root['strict_root_closure_before_and_after']; require(root['strict_root_exact_recursive_closure_verified'] is True and closure['equal'] is True and closure['before'] == closure['after'], 'Exact live before/after closed coverage required')
    require(root['nested_manifest_and_foreign_component_extras_rejected_by_original_and_strict_root_guards'] is True, 'Actual exact-root negative controls required')
    packet_controls, manifest_controls = root['real_packet_controls'], root['real_manifest_controls']
    require(len(packet_controls) == 6 and all(x['observed_expected'] for x in packet_controls), 'Six actual source/prior/budget/code controls required')
    require({x['label'] for x in packet_controls} == {'packet_baseline','packet_source_statement_narrowed','packet_source_actual_report_erased','packet_budget_six_attempts','packet_actual_corrupt_rotation','packet_code_rotation_corrupted'}, 'Complete distinct actual packet mechanisms required')
    require(len(manifest_controls) == 28 and all(x['observed_expected'] and x['strict_root_guard_pass'] == (x['case']=='baseline') for x in manifest_controls), 'Twenty-eight actual strict manifest controls required')
    manifest_cases = {'baseline','missing','extra','same_size_hash','exclusion_cheat','unsafe_path','symlink','nested_manifest_extra','nested_foreign_component_extra'}
    require(len({(x['family'],x['case']) for x in manifest_controls}) == 28, 'Manifest controls must be distinct')
    for family in pins['families']:
        required_cases = manifest_cases|({'foreign_pdf_corrupted'} if family=='primary_scope_family' else set())
        require({x['case'] for x in manifest_controls if x['family']==family} == required_cases, 'All actual family manifest mechanisms required')
    require(root['real_uniform_prose_and_code_control_count'] == 10, 'Actual eight prose/two code controls required')

    copied_families = {}
    for family, info in pins['families'].items():
        name = family+'/'+info['manifest_name']; data = bind(name,'exact_closed_first_party_manifest',info['manifest']['sha256']); pin = root['family_manifests'][family]
        require(pin == closure['before'][family] and pin['manifest_path'] == name and pin['manifest_sha256'] == info['manifest']['sha256'] and pin['member_count'] == info['member_count'] and pin['strict_recursive_coverage'] is True, 'Actual family closure differs')
        copied_families['family_evidence/'+name] = data
        names = set()
        for row in info['members']:
            path = relative(row['path']); require(path not in names, 'Duplicate family member'); names.add(path)
            raw = bind(family+'/'+path,'closed_first_party_member',row['sha256']); require(len(raw) == row['size'], 'Closed member size differs')
            copied_families['family_evidence/'+family+'/'+path] = raw
        foreign = {x['path'] for x in info['foreign_members']}
        require(regular_inventory(audit/family, foreign, info['cache_prefix']) == names|{info['manifest_name']}, 'Exact family recursive first-party coverage differs')
    require(set(root['family_manifests']) == set(pins['families']) and sum(x['member_count'] for x in pins['families'].values()) == 732, 'Exactly closed522/48/162 required')

    retention_raw = bind(args.root_retention_manifest,'actual_root_strict_retention_manifest',args.root_retention_manifest_sha256); retention = json.loads(retention_raw)
    support = relative(retention['support_directory']); require(args.root_retention_manifest == support+'/ROOT_SUPPORT_MANIFEST.json', 'Exact support anchor required')
    require(retention['status'] == 'PASS' and retention['path_base'] == 'support_directory' and retention['self_excluding'] is True and retention['excluded'] == ['ROOT_SUPPORT_MANIFEST.json'] and retention['foreign_corpus_SQL_PDF_OCR_cache_or_private_scratch_retained'] is False, 'Exact successful first-party support closure required')
    require(retention['root_reproduction_receipt'] == {'path':args.root_receipt,'size':len(root_raw),'sha256':args.root_receipt_sha256} and retention['root_reproduction_receipt_sha256'] == args.root_receipt_sha256, 'Support must bind actual complete root receipt')
    retained_rows = {}
    for row in retention['files']:
        name = relative(row['path']); require(name not in retained_rows and name != 'ROOT_SUPPORT_MANIFEST.json', 'Unique exact nonself support members required')
        pp = PurePosixPath(name); require(pp.suffix in {'.py','.json','.jsonl','.stdin','.stdout','.stderr','.patch','.md','.txt'} or pp.name == '.gitignore' or (name in exception_rows and json.dumps(row,sort_keys=True) == json.dumps(exception_rows[name],sort_keys=True)), 'Unreviewed retained capability')
        raw = bind(support+'/'+name,'retained_actual_first_party_evidence',row['sha256']); require(len(raw) == row['size'],'Retained whole evidence size differs')
        retained_rows[support+'/'+name] = row; retained['root_verification/evidence/'+support+'/'+name] = raw
    require(regular_inventory(audit/support) == {x['path'] for x in retention['files']}|{'ROOT_SUPPORT_MANIFEST.json'}, 'Exact recursive actual retained membership required')
    retained['root_verification/evidence/'+args.root_retention_manifest] = retention_raw

    def artifact(row, must_be_retained=True):
        path = Path(row['path']); name = path.relative_to(audit).as_posix() if path.is_absolute() else relative(row['path'])
        require(not must_be_retained or name in retained_rows, 'Whole referenced actual artifact not retained: '+name)
        raw = bind(name,'complete_actual_or_saved_evidence_reference',row['sha256']); require(len(raw) == row.get('size',row.get('bytes')), 'Referenced whole evidence size differs'); return raw

    hashes = {x['sha256'] for x in retained_rows.values()}; require({sha(wrapper),sha(collector)} <= hashes, 'Actual wrapper/collector source must survive retention')
    require(root['actual_outer_program_runs'] and root['actual_nested_program_runs'] and root['full_structured_receipt_comparisons'], 'Complete actual program and comparison lists required')
    default_rows = [x for x in root['actual_outer_program_runs'] if x['label']=='root_default_python314_missing_sympy']; require(len(default_rows)==1,'Exactly genuine default failure required')
    for row in root['actual_outer_program_runs']:
        require(row['script_sha256'] in hashes and row['launch_attempted'] and row['actual_execution'] and row['completed'], 'Every actual outer source/completed launch retained')
        require(row['exit_code'] == (1 if row['label']=='root_default_python314_missing_sympy' else 0),'Only actual expected default outer failure allowed')
        artifact(row['stdout']); artifact(row['stderr'])
    for row in root['actual_nested_program_runs']:
        require(row['launch_attempted'] and row['actual_execution'] and row['completed'], 'Actual nested launch/completion required')
        if row.get('script'): require(row['script']['sha256'] in hashes,'Every nested actual source must be retained')
        require(row['exit_code'] in {0,1} and (row['exit_code']==0 or row['outer_label'] in {'root_reconstructed_packet_and_manifest_controls','uniform_actual_eight_prose_and_two_code_controls'}), 'Only documented actual negative nested failures allowed')
        artifact(row['stdout']); artifact(row['stderr'])
        if 'stdin' in row:
            value = artifact(row['stdin'])
            require(row['argv']==['git','hash-object','--stdin'] and row['exit_code']==0,'Unreviewed stdin producer; separate reviewed revision required')
            matched = [x for x in snapshot['files'] if original[x['path']]==value]
            require(matched and artifact(row['stdout']).strip() in {x['git_blob'].encode() for x in matched}, 'Actual stdin must equal whole original and return its blob')
    # PR39's reviewed producers currently supply no stdin. Do not import PR38's
    # forced all16 stdin coverage; any actual supplied bytes are still retained.
    policy = root['comparison_exclusion_policy']; require(set(policy['clock_keys'])==CLOCK_KEYS and policy['qualified_differences_remain_in_full_JSON'] and not policy['broad_runtime_or_native_ignoring'],'Only exact comparison exclusions allowed')
    prefixes = policy['single_private_path_prefix']; require(prefixes['saved']==str(repo) and Path(prefixes['actual']).is_relative_to(audit/'tmp'),'Exact private prefix provenance required')
    def normalize(value):
        if isinstance(value,dict): return {k:normalize(v) for k,v in value.items() if k not in CLOCK_KEYS}
        if isinstance(value,list): return [normalize(v) for v in value]
        return value.replace(prefixes['actual'],prefixes['saved']) if isinstance(value,str) else value
    def differences(a,b,path='$'):
        if type(a)!=type(b): return [{'path':path,'actual':a,'saved':b}]
        if isinstance(a,dict):
            if set(a)!=set(b): return [{'path':path,'actual_keys':sorted(a),'saved_keys':sorted(b)}]
            return [v for k in a for v in differences(a[k],b[k],path+'/'+k)]
        if isinstance(a,list):
            if len(a)!=len(b): return [{'path':path,'actual_length':len(a),'saved_length':len(b)}]
            return [v for i in range(len(a)) for v in differences(a[i],b[i],path+'/'+str(i))]
        return [] if a==b else [{'path':path,'actual':a,'saved':b}]
    for row in root['full_structured_receipt_comparisons']:
        actual,saved = artifact(row['actual']),artifact(row['saved'],False)
        delta = differences(normalize(json.loads(actual)),normalize(json.loads(saved))); qualifiers = row['precise_qualifications']
        require(delta==row['full_JSON_differences'] and row['all_remaining_fields_equal'] is True and row['equal_after_explicit_clock_and_private_path_exclusions']==(not delta) and row['complete_JSON_BYTE_equal']==(actual==saved),'Whole comparison bodies/flags must independently agree')
        for item in delta:
            q = qualifiers.get(item['path']); require(q and q['difference']==item and q['reason'],'Exact whole-difference qualification required')
            require('actual_complete_stream' in q and 'saved_complete_stream' in q,'Only full stream prefix-qualified differences allowed')
            require(normalize(artifact(q['actual_complete_stream']).decode())==normalize(artifact(q['saved_complete_stream'],False).decode()),'Whole qualified stream bodies must agree')
    require({x['label'] for x in root['full_structured_receipt_comparisons']} == {'primary_source_qualifications_whole_JSON','rotation_exact_falsification_controls_whole_JSON','uniform_exact_controls_whole_JSON','uniform_full_actual_adversarial_receipt'}, 'All exact source/rotation/uniform whole results required')
    require(json.loads(artifact(root['source_native_inspection_receipt']))==provenance,'Actual retained full provenance must equal inline object')
    specs=[('author','verify.py','verification.json',520),('old_submitted','review/submitted_verify.py','review/submitted_results.json',520),('old_independent','review/independent_checks.py','review/independent_results.json',899)]
    require(len(root['original_replays'])==3,'Three actual original FILE-writing programs required')
    for row,(label,program,receipt,count) in zip(root['original_replays'],specs):
        require(row['label']==label and row['program']==program and row['program_sha256']==sha(original[program]) and row['exit_code']==0 and row['stdout_bytes']==count,'Original actual program/source/count differs')
        generated,stdout,stderr=artifact(row['generated_receipt']),artifact(row['actual_stdout']),artifact(row['actual_stderr'])
        require(generated==stdout==original[receipt] and len(stdout)==count and not stderr and json.loads(generated)==json.loads(original[receipt])==row['complete_actual_result'],'Whole actual generated FILE/STDOUT BYTE and full JSON equality required')
        require(all(row[k] is True for k in ['whole_stdout_BYTE_equal','whole_stdout_JSON_equal','generated_complete_receipt_BYTE_equal','generated_complete_receipt_JSON_equal']),'Whole result flags must agree')
        require('program itself writes' in row['generated_receipt_behavior'] and row['generated_receipt_sha256']==sha(generated),'Do not mislabel materialized stdout as actual file output')
    require(root['original_runtime_python']=='/usr/bin/python3' and root['original_runtime_sympy_version']=='1.14.0','Actual supplied diagnostic runtime required')
    failed=root['default_python314_actual_failure']; require(failed['exit_code']==1 and failed['generated_result_absent'] is True and not artifact(failed['actual_stdout']) and b"ModuleNotFoundError: No module named 'sympy'" in artifact(failed['actual_stderr']),'Real default missing-SymPy failure retained')
    require(root['default_python314_runtime']['version_info'][:2]==[3,14] and root['default_python314_missing_sympy_failure_retained'] is True,'Actual default3.14 runtime required')

    historical_states = {revision:git('show',revision+':unsolved_math_prioritization/state.json') for revision in [BASE,HEAD]}
    require(all('9500008' not in json.loads(x) for x in historical_states.values()),'Never fabricate historical canonical events')
    old_sentence = b'Brownian symmetry therefore preserves each stopped Brownian-pair law.'
    replacement = b'Deterministic sign reflection preserves the Brownian property in the same filtration, so each reflected stopped pair remains admissible; its joint stopped-pair law need not equal the original law.'
    old_review = original['review/REVIEW.md']; require(old_review.count(old_sentence)==1 and old_sentence in old_review.splitlines()[21],'Exact historical false sentence at line22 required')
    repair = bind('current_preparation_family/CURRENT_REFLECTION_REPAIR.md','checkable_current_reflection_and_imported_source_qualification')
    notice = b'# Current precision-corrected review; NEW whole-current gate pending\n\nThe embedded dated author/reviewer identities, PASS/none labels and original checksum below are archival context. They do not supply a current verdict. Only the historical line22 joint-law sentence is corrected in the preserved body. See the appended current precision correction and root qualifications. PARTIAL.md, all code and original16 are unchanged.\n\n'
    current_review = notice+old_review.replace(old_sentence,replacement,1)+b'\n\n'+repair
    queue_path=repo/'unsolved_math_prioritization/QUEUE.md';queue_raw=queue_path.read_bytes();lines=queue_raw.decode().splitlines(keepends=True)
    header=[x.strip() for x in next(x for x in lines if x.startswith('| Rank |')).split('|')[1:-1]];require(header==HEADER,'Exact twelve named queue columns required')
    matches=[x for x in lines if len(x.split('|'))==14 and x.split('|')[2].strip()=='9500008 / AMR-094-0008'];require(len(matches)==1,'Unique target row required')
    before=matches[0];fields=before.split('|');indexes={name:i+1 for i,name in enumerate(header)}
    require(fields[indexes['Status']].strip()=='queued' and fields[indexes['Turns']].strip()=='0/5','Current queued0/5 row required; changes need a fresh reviewed rebase')
    changed=list(fields);findings='2026-10-02: Scoped bounded independent-piece coupling and weak diffusive scaling partial valid; exact finite random Brownian origin remains UNSOLVED. Current stopped-pair reflection wording corrected; imported Th5.3 sign/initial-level qualifications retained. Original2/5,new0/audit0; actual original three FILE-writing diagnostics and closed522/48/162 bound; NEW whole-current gate pending. '+PR_URL+'.'
    for name,value in {'Status':'unsolved','Turns':'2/5','Findings':findings}.items():changed[indexes[name]]=' '+value+' '
    require(all(fields[i]==changed[i] for i in range(14) if i not in {indexes[x] for x in ['Status','Turns','Findings']}),'Only named Status/Turns/Findings changes allowed')
    after='|'.join(changed);require(queue_raw.count(before.encode())==1,'Unique full row preimage required');prospective=b''.join(after.encode() if x==before.encode() else x for x in queue_raw.splitlines(keepends=True))
    common={'id':'9500008','problem_number':'AMR-094-0008','status':'unsolved_scoped_partial_pending_NEW_whole_gate','original_head':HEAD,'original_base':BASE,'original_substantive_attempts':2,'substantive_attempt_limit':5,'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved':False,'novelty_claimed':False,'current_gate':GATE,'current_model':None,'current_reasoning_effort':None,'current_deadline_utc':None,'historical_model_reasoning_deadline_archival_only':True,'canonical_historical_events_inferred':False,'historical_worker_transcript':'not_verified','current_workflow_completion_estimate_percent':75,'full_target_partial_progress_estimate_percent':15,'estimate_is_heuristic_not_solution_probability':True,'closed_first_party_members':732,'root_receipt_sha256':args.root_receipt_sha256,'exact_remaining_gap':readiness['exact_claim'],'remaining_gap_qualification':'Need exact finite random origin or admissible bounded counterexample excluding every such origin; coupling/scaling does not settle it.'}
    summary='''# PR39 / 9500008 / Burdzy Problem8: scoped partial; full target UNSOLVED

The target permits an a.s. finite random real origin S, not necessarily stopping
or a junction, with independent centered standard Brownian halves. Input stopped
pairs are independent and may be nonidentical or zero length; one deterministic
finite strict duration bound and divergence of both duration sums are required.
The original PARTIAL gives a fixed-origin two-sided Brownian comparison with
uniform expanding-window O(sqrt(log(2+R))) a.s. error and weak diffusive scaling.
It modifies infinitely many piece interiors and constructs no exact finite
random shift. Full random-origin status remains UNSOLVED. No novelty is claimed;
piece rotation and iid finite-mean results are credited to Burdzy-Scheutzow.

The historical review's stopped-pair joint-law equality is corrected only in
current review material. Sign reflection preserves Brownian admissibility and
the unchanged stopping filtration, and deterministic transforms preserve mark
independence; the asymmetric capped negative-hit example shows pair laws differ.
Root's imported Th5.3 proof is retained with whole-backward-path reflection and
the vanishing Gaussian initial-above-level term. These are source presentation
qualifications, not a new target attempt. PARTIAL, original16, code, receipts,
source/prior and two authored turns stay exact in original_archive. The primary
author definition governs the abbreviated corpus, and Problem7.7 differs in
bound and conclusion. This bounded source audit is not exhaustive novelty proof.

The actual nonempty AMR-094-0008 prior is PRESENT, equal as a whole object to
original/root/raw/SQL pins. It is neither null nor {} fallback. Actual root read
all149MB, all15458 records/allSQL importer joins and pure score/full pair hashes.
Actual unchanged author/submitted FILE writers reproduce complete520-byte files
and stdout with12288 configurations/48 prefix checks; the old independent FILE
writer reproduces899 bytes/12 groups/144 configurations/2256 equalities/16 prefix
laws with SymPy1.14. The real default3.14 missing-SymPy failure is retained.
Finite diagnostics supplement the proof audit; they are no Brownian-law proof.

Closed522/48/162 first-party members, real source/budget/code and28 manifest
controls, exact qualification/rotation/uniform results, and eight prose/two code
failures are bound to actual root support. Foreign PDF/HTML/OCR/raw/SQL/cache and
private clone bodies are excluded. Each actual supplied stdin is retained in
full; PR39 does not borrow PR38's different all16-stdin coverage convention.

The authored local ledger is2/5; canonical base/head/current state/history remain
absent for the target and current queue is0/5 before a prospective patch. New
substantive attempts0 and audit attempts0. No hidden historical worker events
are inferred. Historical model/reasoning/deadline are archival; current exposures
are unavailable/null, deadline null. The new current whole-source-first gate is
PENDING; historical PASS labels do not transfer. No paper/new DOI/tracker,
release, external contact or live queue/state/history/Git/remote write occurs.
'''
    context='''
CURRENT_PROOF_DEPENDENCIES resolves audit-relative paths against repository_root/
draft_pr_publication_program_20260930/audits/pr39_9500008 even after canonical
copy. It does not relocate original helpers' dependencies to family_evidence.
Copied historical drivers/code/results are read-only. Replaying a file writer
requires a separately reviewed fresh private directory with only original code
and no copied saved JSON output; direct execution cannot overwrite CLOSED files.
The strict current MANIFEST excludes only its exact root self. The twelve-column
queue proposal changes only Status/Turns/Findings, preserving all unrelated
bytes, Chat and DOI; it makes no live mutation. Root and a NEW whole-current
source-first adversary must review this entire current packet before promotion.
'''
    outputs={'original_archive/'+name:data for name,data in original.items()};outputs.update({name:original[name] for name in HISTORICAL_TOP});outputs.update(copied_families);outputs.update(retained)
    outputs.update({'README.md':(summary+context).encode(),'CURRENT_CONTEXT.md':(summary+context).encode(),'SOURCE_AUDIT.md':(summary+'\n'+repair.decode()).encode(),'pr_body.md':(summary+'\nLocal proposed body only; current gate pending.\n').encode(),'CURRENT_AUDIT_SCOPE.md':('NEW whole-current source-first review PENDING.\n\n'+summary+'\n'+context).encode(),'CURRENT_REFLECTION_REPAIR.md':repair,'review/REVIEW.md':current_review,'CURRENT_PARTIAL_SCOPE_CERTIFICATE.md':scope,'primary_evidence/ROOT_PRIMARY_READ_LEDGER.json':ledger_raw,'primary_evidence/ROOT_PRIMARY_READ_ADDENDUM.json':addendum_raw,'primary_evidence/ROOT_PRIMARY_PROOF_QUALIFICATIONS.md':qualification,'root_verification/ROOT_SCIENCE_CARD.json':card_raw,'root_verification/ROOT_REPLAY_READ_ATTESTATION.json':attestation_raw,'root_verification/ROOT_CURRENT_INPUT_PREIMAGES.json':current_raw,'root_verification/ROOT_CLOSED_FAMILIES_ACTUAL_REPRODUCTION.json':root_raw,'original_diff.patch':diff,'original_pr_metadata.json':metadata_raw,'original_snapshot_manifest.json':snapshot_raw,'queue_proposal/QUEUE_PREIMAGE.md':queue_raw,'queue_proposal/QUEUE_PROSPECTIVE.md':prospective})
    for name in ['attempt.json','status.json','readiness.json']:outputs[name]=encoded(common)
    outputs['review/verdict.json']=encoded({**common,'current_verdict':None,'historical_verdict_transferred':False,'current_precision_correction_recorded':True,'PARTIAL_theorem_changed':False})
    outputs['CURRENT_REVIEW_CORRECTION_RECEIPT.json']=encoded({'original_review_sha256':sha(old_review),'historical_line':22,'exact_old_sentence':old_sentence.decode(),'exact_current_sentence':replacement.decode(),'current_review_sha256':sha(current_review),'only_body_sentence_replaced':True,'archival_notice_and_appendix_added':True,'original_review_preserved':True,'PARTIAL_code_source_receipts_turns_unchanged':True,'source_credited_presentation_repair_not_new_attempt':True})
    outputs['HISTORICAL_ORIGINAL_NOTICE.md']=('Historical original sixteen-file packet is exact in original_archive. All embedded historical PASS/none/model/reasoning/deadline fields there are archival; no current verdict is inferred.\n\n'+context).encode()
    outputs['CURRENT_SOURCE_SERIALIZATION_RECEIPT.json']=encoded({'entire_flat_source_equal':provenance['complete_flat_problem']==problem,'entire_actual_prior_equal':provenance['complete_actual_prior_report']==prior,'prior_raw_key_present':True,'fallback_used':False,'original_source_sha256':sha(original['source_record.json']),'original_prior_sha256':sha(original['prior_report.json']),'statement_hash':STATEMENT_SHA,'pair_hash':PAIR_SHA,'original_bytes_preserved':True,'comparison_rule':'Whole object equality for content; independent exact bytes preserved without forced reserialization.'})
    outputs['CURRENT_QUEUE_PATCH.json']=encoded({'phase':'Prospective named-only patch; no shared write','id':9500008,'header_names':header,'column_count':12,'whole_queue_preimage_sha256':sha(queue_raw),'whole_queue_prospective_sha256':sha(prospective),'row_before':before,'row_prospective':after,'allowed_named_changes':['Status','Turns','Findings'],'all_unrelated_bytes_Chat_DOI_preserved':True,'integration_guard':'Recheck complete preimage; intervening changes need a fresh reviewed named-row rebase. Never replay the original full diff.'})
    for revision,data in historical_states.items():outputs['historical_native_state/'+revision+'.json']=data
    for name in regular_inventory(script.parent):outputs['build/'+name]=(script.parent/name).read_bytes()
    outputs['RESEARCH_LOG.md']=(now+' — administrative current freeze75%; full-target heuristic partial progress15%, not solution probability. Valid partial and exact finite-origin gap as root science chain; original2/5,new0/audit0. Only current review wording/imported source qualifications repaired; no mathematical search. Whole three actual FILE/stdout results, fullrawSQL provenance, closed732, real controls, failure/stdio/source and exact audit anchor retained. NEW whole-current review pending.\n').encode()
    outputs['CURRENT_PROOF_DEPENDENCIES.json']=encoded({'utc':now,'dependency_anchor_repository_relative':audit.relative_to(repo).as_posix(),'resolution_rule':'Resolve files.path against repository_root/dependency_anchor_repository_relative, including canonical copies; scratch is never an anchor.','closed_family_member_counts':{k:v['member_count'] for k,v in pins['families'].items()},'closed_first_party_member_count':732,'root_retention_manifest':args.root_retention_manifest,'root_retention_manifest_sha256':args.root_retention_manifest_sha256,'files':sorted(dependencies.values(),key=lambda x:x['path'])})
    outputs['CURRENT_BUILD_RECEIPT.json']=encoded({'utc':now,'kind':'Actual administrative exact-input freeze; no research helper import/execution','original_archive_count':16,'original_diff_path_count':17,'PARTIAL_and_all_code_whole_receipts_source_prior_two_turns_BYTE_exact':True,'current_review_precision_repair_only':True,'actual_builder_path':script.relative_to(audit).as_posix(),'actual_builder_sha256':sha(script.read_bytes()),'root_receipt_sha256':args.root_receipt_sha256,'root_science_card_sha256':args.root_science_card_sha256,'root_current_input_manifest_sha256':args.root_current_input_manifest_sha256,'root_wrapper_sha256':sha(wrapper),'root_collector_sha256':sha(collector),'root_scope_sha256':SCOPE_SHA,'root_read_ledger_sha256':READ_SHA,'root_read_addendum_sha256':ADDENDUM_SHA,'root_proof_qualifications_sha256':QUALIFICATION_SHA,'closed_first_party_members':732,'original_actual_FILE_writing_programs':3,'current_gate':GATE,'new_substantive_attempts':0,'audit_turns':0,'shared_git_remote_inventory_canonical_writes':0,'copied_outputs_readonly':True})
    for row in dependencies.values():
        data=(audit/row['path']).read_bytes();require(len(data)==row['bytes'] and sha(data)==row['sha256'],'Input changed before freeze')
    require(queue_path.read_bytes()==queue_raw,'Live queue changed; preserve attempt and require fresh reviewed preimage')
    validate_native_preimages()
    require(git('rev-parse','HEAD').decode().strip()==current['current_head'],'Current HEAD changed before freeze; preserve attempt')
    for name in regular_inventory(attempt):outputs['build/actual_builder_attempt/'+name]=(attempt/name).read_bytes()
    stage=audit/('reviewed_candidate.preparation_'+dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ'));stage.mkdir(exist_ok=False)
    try:
        for name,data in sorted(outputs.items()):
            path=stage/relative(name);path.parent.mkdir(parents=True,exist_ok=True)
            with path.open('xb') as handle:handle.write(data)
            path.chmod(0o444)
        require(regular_inventory(stage/'original_archive')==set(original),'Exact archived16 required')
        for name,data in original.items():require((stage/'original_archive'/name).read_bytes()==data,'Archive bytes differ')
        for name in HISTORICAL_TOP:require((stage/name).read_bytes()==original[name],'Current immutable PARTIAL/code/source/receipts/ledger differs')
        rows=[{'path':name,'bytes':len((stage/name).read_bytes()),'sha256':sha((stage/name).read_bytes()),'mode':'0444'} for name in sorted(regular_inventory(stage))]
        manifest={'utc':now,'schema':'strict_self_excluded_recursive_current_packet_v1','self_excluded':['MANIFEST.json'],'files_count':len(rows),'files':rows,'current_gate':GATE}
        with (stage/'MANIFEST.json').open('xb') as handle:handle.write(encoded(manifest))
        (stage/'MANIFEST.json').chmod(0o444)
        require(regular_inventory(stage)=={x['path'] for x in rows}|{'MANIFEST.json'},'Exact current recursive self exclusion required')
        for row in rows:
            data=(stage/row['path']).read_bytes();require(len(data)==row['bytes'] and sha(data)==row['sha256'] and (stage/row['path']).stat().st_mode&0o777==0o444,'Staged immutable member differs')
        require(not destination.exists() and not destination.is_symlink(),'Destination appeared; preserve stage')
        publish_absent(stage,destination)
    except BaseException:
        try:(stage/'BUILD_FAILURE.json').write_bytes(encoded({'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'status':'FAILED_BUILD_PRESERVED','traceback':traceback.format_exc(),'new_substantive_attempts':0}))
        except BaseException:print('Secondary staged-failure retention failed; original error preserved',file=sys.stderr)
        raise
    print(json.dumps({'status':'CURRENT_PACKET_FROZEN_NEW_WHOLE_GATE_PENDING','destination':str(destination),'members':len(rows),'manifest_sha256':sha((destination/'MANIFEST.json').read_bytes()),'proposed_status':'unsolved','attempts':'2/5','new_substantive_attempts':0,'audit_turns':0,'shared_writes':0},indent=2))


def main():
    args=arguments();require(args.execute,'Static preparation only; root must explicitly execute after actual evidence')
    for name,value in vars(args).items():
        if name.endswith('sha256'):require(re.fullmatch(r'[0-9a-f]{64}',value) is not None,'Explicit SHA256 required: '+name)
    script=Path(__file__).resolve();require(script.parent.name=='current_execution_revision' and script.parent.parent.name=='pr39_9500008','Exact dedicated PR39 audit anchor required')
    audit,repo=script.parent.parent,script.parent.parent.parents[2]
    (audit/'tmp').mkdir(exist_ok=True);attempt=audit/'tmp'/('root_pr39_current_build_'+dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ'));attempt.mkdir(exist_ok=False)
    try:
        (attempt/'BUILDER_INVOCATION.json').write_bytes(encoded({'argv':sys.argv,'cwd':str(Path.cwd()),'source_path':script.relative_to(audit).as_posix(),'source_sha256':sha(script.read_bytes()),'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'root_explicit_execute':True,'private_locator_administrative_only':attempt.name}))
        (attempt/'PRELAUNCH_BUILDER_SOURCE.py').write_bytes(script.read_bytes())
        execute(args,script,audit,repo,attempt)
    except BaseException:
        error=traceback.format_exc()
        try:(attempt/'BUILD_ATTEMPT_FAILURE.json').write_bytes(encoded({'status':'FAILED_BUILD_PRESERVED','traceback':error,'new_substantive_attempts':0,'scratch_is_dependency_anchor':False}))
        except BaseException:print('Secondary attempt-failure retention failed; original error preserved',file=sys.stderr)
        print(error,file=sys.stderr);raise


if __name__=='__main__':main()

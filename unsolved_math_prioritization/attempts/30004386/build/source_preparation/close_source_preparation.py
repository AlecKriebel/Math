#!/usr/bin/env python3
"""Own exact source-only closure. Never import/run/compile builder/operator/math.

This actual operation hashes complete own and pinned inputs, checks all JSON
duplicate/finite numbers and actual own-capture streams, preserves transparent
after-edit reconstructions, and writes only this source family's final records.
"""
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import stat

P = Path(__file__).absolute().parent
A = P.parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'Duplicate JSON key')
            result[key] = value
        return result
    def constant(value):
        raise ValueError('Nonfinite JSON constant: ' + value)
    def floating(value):
        number = float(value)
        require(math.isfinite(number), 'Nonfinite JSON float')
        return number
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant, parse_float=floating)


def regular(path):
    require(not path.is_symlink() and all(not parent.is_symlink() for parent in path.parents)
            and stat.S_ISREG(path.stat().st_mode), 'Regular nonsymlink file required')
    raw = path.read_bytes()
    if path.name.endswith('.json'):
        load(raw)
    if path.name.endswith('.jsonl'):
        for line in raw.splitlines():
            require(line.strip(), 'Blank JSONL row')
            load(line)
    return raw


def row(path, root):
    raw = regular(path)
    require(len(raw) < 100 * 1024 * 1024, 'Own/retained single-file limit')
    return dict(path=path.relative_to(root).as_posix(), bytes=len(raw), sha256=sha(raw))


def inventory(root):
    files, directories = set(), set()
    require(root.is_dir() and not root.is_symlink(), 'Regular root required')
    for path in root.rglob('*'):
        require(not path.is_symlink(), 'Symlink member rejected')
        name = path.relative_to(root).as_posix()
        mode = path.stat().st_mode
        if stat.S_ISREG(mode):
            files.add(name)
        else:
            require(stat.S_ISDIR(mode), 'Special member rejected')
            directories.add(name)
    require(directories == {parent.as_posix() for name in files for parent in
            PurePosixPath(name).parents if parent.as_posix() != '.'}, 'Extra/empty directory rejected')
    return files


def bound(root, item):
    require(type(item) is dict and set(item) == {'path', 'bytes', 'sha256'} and
            type(item['bytes']) is int and item['bytes'] >= 0, 'Typed exact hash row')
    require(row(root / item['path'], root) == item, 'Pinned member changed: ' + item['path'])


def write(name, body):
    with (P / name).open('xb') as out:
        out.write(body)


def encode(value):
    return (json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode()


def clock(value):
    number = dt.datetime.fromisoformat(value)
    require(number.tzinfo is not None and number.utcoffset() == dt.timedelta(0), 'Actual aware UTC')
    return number


require(P.name == 'current_preparation_family' and A.name == 'pr43_30004386', 'Exact own anchor')
require(not (P / 'PREPARATION_MANIFEST.json').exists() and not (P / 'SOURCE_STATUS.json').exists(),
        'Never overwrite a source closure')
require(not (A / 'reviewed_candidate').exists(), 'No candidate created in source preparation')
pins = load(regular(P / 'INPUT_PINS.json'))
bound(A, pins['snapshot_manifest'])
for item in pins['auxiliary']:
    bound(A, item)
for info in pins['retained_closures']:
    root = A / info['directory']
    require(inventory(root) == {item['path'] for item in info['files']}, 'Retained root membership')
    for item in info['files']:
        bound(root, item)
require(inventory(A / 'foreign_primary') == {item['path'] for item in pins['root_foreign_members']},
        'Root foreign exact membership')
for item in pins['root_foreign_members']:
    bound(A / 'foreign_primary', item)
for family, info in pins['families'].items():
    root = A / family
    bound(root, info['manifest'])
    wanted = {item['path'] for item in info['copied_members'] + info['foreign_members']}
    require(len(wanted) == len(info['copied_members']) + len(info['foreign_members']) and
            inventory(root) == wanted | {info['manifest']['path']}, 'Original disjoint family closure')
    for item in info['copied_members'] + info['foreign_members']:
        bound(root, item)
require(sha(regular(P / 'SOURCE_PRECISION_QUALIFICATIONS.md')) == pins['qualification_sha256'], 'Qualification unchanged')
require(regular(A / 'source_snapshot/turns.jsonl') == b'', 'Original ledger still0bytes')
captures = {}
for name, source, expected_pid in [
    ('AUTHORING_ACTUAL_CAPTURE', 'author_source_documents.py', 45774),
    ('PRIVATE_CONTROLS_ACTUAL_CAPTURE', 'private_contract_controls.py', 45784)]:
    root = P / name
    actual = load(regular(root / 'CAPTURE.json'))
    require(actual['actual_execution'] is True and actual['completed'] is True and
            type(actual['pid']) is int and actual['pid'] == expected_pid and
            type(actual['exit_code']) is int and actual['exit_code'] == 0 and
            actual['stdin_supplied'] is False and actual['source_unchanged'] is True and
            actual['operator_unchanged'] is True and
            actual['builder_future_ROOT_operator_or_scientific_helpers_imported_compiled_executed'] is False and
            clock(actual['started_utc']) <= clock(actual['finished_utc']), 'Genuine scoped own capture')
    require(regular(root / 'PRELAUNCH_SOURCE.py') == regular(P / source) and
            sha(regular(root / 'PRELAUNCH_SOURCE.py')) == actual['source_sha256'] and
            sha(regular(root / 'PRELAUNCH_OPERATOR.py')) == actual['operator_sha256'], 'Actual prelaunch source pins')
    for channel in ['stdout', 'stderr']:
        bound(root, actual[channel])
    require(not regular(root / 'stderr.bin'), 'Own actual operation stderr retained but not empty')
    captures[name] = actual
controls = load(regular(P / 'PRIVATE_CONTRACT_CONTROL_RESULTS.json'))
require(controls['all_passed'] is True and len(controls['checks']) == 28 and
        all(item['passed'] is True for item in controls['checks']) and
        controls['tested_builder_import_compile_execution'] is False and
        controls['tested_future_ROOT_operator_execution'] is False and
        controls['scientific_helpers_run'] is False and controls['new_whole_current_gate'] == 'PENDING' and
        controls['current_whole_verdict'] is None, 'Own finite contract scope')
for probe in controls['permission_probes']:
    path = P / probe['path']
    require(format(stat.S_IMODE(path.stat().st_mode), '05o') == probe['actual_full_mode'] and
            len(regular(path)) == probe['bytes'] and sha(regular(path)) == probe['sha256'], 'Actual private mode still preserved')
require(regular(P / 'private_controls/rename_absent/member') == b'own source retained after failure\n' and
        regular(P / 'private_controls/rename_existing/sentinel') == b'own destination retained\n', 'Actual absent/existing rename evidence')

# The actual document-authoring stdout pinned a then-current drafting snapshot.
# Preserve exact after-edit reconstructions without claiming prelaunch storage
# of the builder/operator or any execution of them at that drafting point.
author_receipt = load(regular(P / 'AUTHORING_ACTUAL_CAPTURE/stdout.bin'))
builder = regular(P / 'prepare_current_packet.py')
inner_line = b"        'audit_relative_inner_attempt': attempt.relative_to(audit).as_posix(),\n"
require(builder.count(inner_line) == 1, 'Exact final one-line builder clarification')
old_builder = builder.replace(inner_line, b'', 1)
require(sha(old_builder) == author_receipt['builder_source']['sha256'] and
        len(old_builder) == author_receipt['builder_source']['bytes'], 'Exact earlier builder reconstruction')
write('builder_before_final_tool_edit_RECONSTRUCTED_AFTER.py', old_builder)
operator = regular(P / 'capture_root_builder_operation.py')
new = b"""        for key, path, prior in [('builder_unchanged_after_child', builder, source),
                                 ('operator_unchanged_after_child', script, operator)]:
            try:
                record[key] = regular(path) == prior
            except BaseException:
                record[key] = False
                record[key + '_read_failure'] = traceback.format_exc()
"""
old = b"""        record['builder_unchanged_after_child'] = regular(builder) == source
        record['operator_unchanged_after_child'] = regular(script) == operator
"""
require(operator.count(new) == 1, 'Exact final ROOT operator failure-preservation clarification')
old_operator = operator.replace(new, old, 1)
require(sha(old_operator) == author_receipt['future_ROOT_operator_source']['sha256'] and
        len(old_operator) == author_receipt['future_ROOT_operator_source']['bytes'], 'Exact earlier operator reconstruction')
write('operator_before_final_tool_edit_RECONSTRUCTED_AFTER.py', old_operator)
now = dt.datetime.now(dt.timezone.utc).isoformat()
write('SOURCE_TOOL_EDIT_NOTES.md', (
    '# Source tool-edit provenance\n\n' + now +
    ' — Actual document/pin authoring PID45774 and private contract predicates PID45784 '
    'completed earlier with full prelaunch source/operator and streams. These operations '
    'never ran/imported/compiled the proposed builder or future ROOT operator.\n\n'
    'After their actual capture, tool edits added the explicit inner-attempt path to the '
    'future execution reference and made the future ROOT operator retain a final failure '
    'receipt even if source re-reading fails. Contract/draft text now explicitly states '
    'the exact separate certificate heading/marker and the copied-private-probe permission '
    'scope. The ownership note also corrects the number of empty primary extraction/render '
    'streams from twenty to eighteen; this did not change a family classification or pin. '
    'One attempted tool patch was rejected for absent context; a subsequent read '
    'confirmed none of its new source tokens existed before the accepted patch. No '
    'builder execution or candidate creation occurred.\n\n'
    'The two RECONSTRUCTED_AFTER source files are created by this closure after those '
    'tool edits by exact inverse substitution. They match the earlier actual authoring '
    'receipt byte counts and SHA pins. They are explicitly after-edit reconstructions, '
    'not old prelaunch saves or executed builder sources. The source-preparation manifest '
    'pins the final source now; a future genuine ROOT prelaunch capture remains separate '
    'and PENDING. No old/current version or historical runtime is silently substituted.\n').encode())
status = dict(schema='PR43_CLOSED_SOURCE_ONLY_CURRENT_PREPARATION_STATUS_v1', utc=now,
    closure_actual_pid=os.getpid(), own_static_whole_source_contract_draft_read_completed=True,
    builder=row(P / 'prepare_current_packet.py', P), future_ROOT_operator=row(P / 'capture_root_builder_operation.py', P),
    source_tools_edited_builder_and_operator_without_executing=True,
    genuine_own_document_authoring_pid=45774, genuine_own_private_predicate_pid=45784,
    own_finite_contract_checks=28, own_ordinary0444_accepted=True,
    own_full01444_02444_04444_rejected=True,
    builder_imported_executed_compiled=False, future_ROOT_operator_executed=False,
    candidate_or_family_scientific_helpers_imported_executed_compiled=False,
    candidate_created=False, ROOT_reading_or_approval_attested_by_preparer=False,
    ROOT_mechanical_inspection='Genuine separate ROOT evidence pinned; no future flags inferred',
    original_family_closures_unchanged=True, individual_foreign_full_bodies_copied=False,
    new_different_source_adversary='PENDING', genuine_ROOT_prerequisites_and_fresh13='PENDING',
    future_administrative_freeze='PENDING', NEW_whole_current_gate='PENDING',
    future_whole_current_verdict=None, current_model=None, current_reasoning_effort=None,
    current_deadline_utc=None, original_source_status='already_solved',
    full_problem_solved_by_project=False, novelty_claimed=False,
    original_substantive_attempts=0, turn_limit=5, new_substantive_attempts=0, audit_turns=0,
    source_preparation_completion_percent=100, publication_workflow_percent=65,
    new_project_discovery_percent=0, native_canonical_git_index_remote_writes=False,
    external_human_contact=False, paper_created=False, new_DOI_created=False, tracker_row_created=False)
write('SOURCE_STATUS.json', encode(status))
write('SOURCE_PREPARATION_RESEARCH_LOG.md', (
    '# PR43 source preparation research log\n\n'
    '2026-10-02T23:52:52.844452+00:00 — actual own document/pin authoring started; '
    'PID45774 exited0 at23:52:53.028667+00:00. Original16/family18+8/probability43+23 '
    'and only relevant ROOT closures pinned. Source preparation75%; publication65%; '
    'new project discovery0%. Original0/5,new0/audit0.\n\n'
    '2026-10-02T23:52:56.593876+00:00 — actual own private predicates started; '
    'PID45784 exited0 at23:52:56.669741+00:00. All28 finite controls passed, '
    'including full special permission rejection and actual macOS exclusive rename '
    'existing-target preservation. Proposed builder/operator/math sources were not '
    'imported/compiled/executed. Source preparation90%; publication65%; discovery0%.\n\n'
    + now + ' — final source/contracts/drafts statically read; all source input '
    'hashes, exact topology, genuine own captures, source reconstruction distinctions '
    'and28 control results checked by actual closure PID' + str(os.getpid()) + '. '
    'Source preparation100%; publication65%; new project discovery0%. All4 genuine '
    'ROOT prerequisites/fresh13, NEW different source review, future freeze and NEW '
    'whole-current review remain PENDING. No ROOT approval or future PASS fabricated. '
    'Original0/5,new0/audit0; no paper/new DOI/tracker/native/canonical/Git/remote write '
    'or outside human contact.\n').encode())
top = {
    'prepare_current_packet.py', 'capture_root_builder_operation.py', 'author_source_documents.py',
    'private_contract_controls.py', 'capture_preparation_operation.py', 'close_source_preparation.py',
    'SOURCE_PRECISION_QUALIFICATIONS.md', 'CURRENT_OVERVIEW.md', 'EXECUTION_CONTRACT.md',
    'ROOT_READ_EXPECTATIONS.md', 'OWNERSHIP_CLASSIFICATION_NOTES.md', 'INPUT_PINS.json',
    'DRAFT_ROOT_READ_LEDGER.json', 'DRAFT_ROOT_SCIENCE_CARD.json',
    'DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json', 'DRAFT_ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md',
    'PRIVATE_CONTRACT_CONTROL_RESULTS.json', 'SOURCE_STATUS.json',
    'SOURCE_PREPARATION_RESEARCH_LOG.md', 'SOURCE_TOOL_EDIT_NOTES.md',
    'builder_before_final_tool_edit_RECONSTRUCTED_AFTER.py',
    'operator_before_final_tool_edit_RECONSTRUCTED_AFTER.py'}
expected = top | {capture + '/' + name for capture in captures for name in
                 ['PRELAUNCH_SOURCE.py', 'PRELAUNCH_OPERATOR.py', 'CAPTURE.json', 'stdout.bin', 'stderr.bin']}
expected |= {'private_controls/mode_' + value for value in ['00444', '01444', '02444', '04444']}
expected |= {'private_controls/rename_absent/member', 'private_controls/rename_existing/sentinel'}
require(inventory(P) == expected, 'Exact declared own first-party membership required')
files = [row(P / name, P) for name in sorted(expected)]
manifest = dict(schema='PR43_CLOSED_SOURCE_ONLY_PREPARATION_MANIFEST_v1',
    status='CLOSED_SOURCE_ONLY_CURRENT_PREPARATION', utc=now,
    self_excluded=['PREPARATION_MANIFEST.json'], files_count=len(files), files=files,
    first_party_member_scope='This preparer own source/docs/drafts/private controls/captures only; no parent/sibling/foreign full body copied',
    foreign_body_members=[], builder_imported_executed_compiled=False,
    future_ROOT_operator_executed=False, future_current_freeze_or_whole_PASS_claimed=False,
    original_substantive_attempts=0, new_substantive_attempts=0, audit_turns=0,
    source_preparation_completion_percent=100, publication_workflow_percent=65,
    new_project_discovery_percent=0,
    private_permission_observations_at_original_audit_path=controls['permission_probes'])
write('PREPARATION_MANIFEST.json', encode(manifest))
require(inventory(P) == expected | {'PREPARATION_MANIFEST.json'}, 'Exact self-only own source closure')
for item in files:
    bound(P, item)
print(json.dumps(dict(status=manifest['status'], actual_closure_pid=os.getpid(),
    manifest_sha256=sha(regular(P / 'PREPARATION_MANIFEST.json')),
    builder_sha256=status['builder']['sha256'], future_ROOT_operator_sha256=status['future_ROOT_operator']['sha256'],
    qualification_sha256=pins['qualification_sha256'], input_pins_sha256=sha(regular(P / 'INPUT_PINS.json')),
    files_count=len(files), candidate_created=False,
    builder_future_ROOT_operator_or_scientific_helpers_imported_compiled_executed=False,
    NEW_whole_current_gate='PENDING'), indent=2))

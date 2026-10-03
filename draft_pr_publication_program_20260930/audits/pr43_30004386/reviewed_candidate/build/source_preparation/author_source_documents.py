#!/usr/bin/env python3
"""Own source-only document/pin authoring; no proposed builder/operator/math execution.

The builder and Markdown sources are edited by the preparer's file tools. This
actual operation authors the input contract and four false/null ROOT drafts,
checks source byte identities and inspects exact manifest rows. It never
imports or compiles those source files, contacts people or mutates Git/native.
"""
import datetime as dt
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import re
import stat

P = Path(__file__).absolute().parent
A = P.parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def load(raw):
    def pairs(items):
        out = {}
        for key, value in items:
            require(key not in out, 'Duplicate JSON key')
            out[key] = value
        return out
    def constant(value):
        raise ValueError('Nonfinite JSON constant: ' + value)
    def floating(value):
        number = float(value)
        require(math.isfinite(number), 'Nonfinite JSON float')
        return number
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant, parse_float=floating)


def regular(path):
    require(not path.is_symlink() and all(not p.is_symlink() for p in path.parents)
            and stat.S_ISREG(path.stat().st_mode), 'Regular nonsymlink file required')
    return path.read_bytes()


def row(path, root):
    raw = regular(path)
    return dict(path=path.relative_to(root).as_posix(), bytes=len(raw), sha256=digest(raw))


def members(root):
    require(root.is_dir() and not root.is_symlink(), 'Regular root required')
    files, directories = [], set()
    for path in sorted(root.rglob('*')):
        require(not path.is_symlink(), 'Symlink member rejected')
        mode = path.stat().st_mode
        if stat.S_ISREG(mode):
            files.append(row(path, root))
        else:
            require(stat.S_ISDIR(mode), 'Special member rejected')
            directories.add(path.relative_to(root).as_posix())
    require(directories == {parent.as_posix() for entry in files for parent in
                           PurePosixPath(entry['path']).parents if parent.as_posix() != '.'},
            'Unexpected empty directory')
    return files


def write_json(name, obj):
    with (P / name).open('x') as out:
        json.dump(obj, out, indent=2, ensure_ascii=False, allow_nan=False)
        out.write('\n')


require(P.name == 'current_preparation_family' and A.name == 'pr43_30004386', 'Exact own source root')
require(not (A / 'reviewed_candidate').exists(), 'Source-only preparation requires absent candidate')
require(not (P / 'INPUT_PINS.json').exists(), 'Never overwrite a source authoring operation')
snapshot = load(regular(A / 'snapshot_manifest.json'))
require(snapshot['head'] == '86be0f85c7a37a5cad8d24abd16a32d8d1f27e62' and
        snapshot['base'] == '60292bed09f59236aa192cb17aa138f7b4750e1a' and len(snapshot['files']) == 16,
        'PR43 original identities required')
for item in snapshot['files']:
    actual = row(A / 'source_snapshot' / item['path'], A / 'source_snapshot')
    require(actual == dict(path=item['path'], bytes=item['size'], sha256=item['sha256']), 'Original pin mismatch')
require(regular(A / 'source_snapshot/turns.jsonl') == b'', 'Zero-byte ledger required')
expected_family_seals = {
    'compactness_source_family': ('OWNERSHIP_MANIFEST.json', '9abc7c0dba6d4167201eec93608772be0bb26f31faf03e21805650e7d8ebc2b9'),
    'probability_source_family': ('SELF_MANIFEST.json', 'de68537cda5407bf5b0c1a4dcd28de7ae51c96932d4b3af84aca389d82607e7c')}
families = {}
for family, (name, expected) in expected_family_seals.items():
    root = A / family
    manifest_row = row(root / name, root)
    require(manifest_row['sha256'] == expected, 'Original independent seal changed')
    manifest = load(regular(root / name))
    if family == 'compactness_source_family':
        authored = manifest['first_party_files']
        foreign = [{key: item[key] for key in ['path', 'bytes', 'sha256']}
                   for item in manifest['foreign_individually_excluded']]
        require(len(authored) == 18 and len(foreign) == 8, 'Compactness18/8 required')
    else:
        authored = [{key: item[key] for key in ['path', 'bytes', 'sha256']}
                    for item in manifest['files'] if item['classification'] == 'first_party_audit_artifact']
        foreign = [{key: item[key] for key in ['path', 'bytes', 'sha256']}
                   for item in manifest['files'] if item['classification'] == 'foreign_primary_or_access_evidence']
        require(len(authored) == 43 and len(foreign) == 23 and len(manifest['files']) == 66, 'Probability43/23 required')
        for item in authored:
            if item['path'].startswith('captures/') and ('.extract.' in item['path'] or
                    re.fullmatch(r'captures/(jkp_v2_p(4|7|10)|owr_p412)\.(stdout|stderr)\.txt', item['path']) or
                    item['path'].startswith('captures/original_report_extract.') or
                    item['path'].startswith('captures/kpt_arxiv_v1.pdf.')):
                require(item['bytes'] == 0 and regular(root / item['path']) == b'', 'Primary-derived stream not empty')
    wanted = sorted(authored + foreign + [manifest_row], key=lambda item: item['path'])
    require(members(root) == wanted, 'Exact original family membership/hashes changed')
    families[family] = dict(manifest=manifest_row, copied_members=authored, foreign_members=foreign)
root_closures = [
    'original_git_commands', 'root_original_actual_reproduction',
    'root_original_branch_fetch_actual_capture', 'root_original_export_actual_capture',
    'root_original_reproduction_actual_capture', 'root_primary_jkp_download_actual_capture',
    'root_primary_owr_download_actual_capture', 'root_closed_evidence_inspection_actual_capture']
retained = [dict(directory=name, files=members(A / name)) for name in root_closures]
auxiliary_names = ['ORIGINAL_GIT_COMMANDS.json', 'capture_root_command.py', 'export_original_snapshot.py',
                   'reproduce_original_checks.py', 'pinned_problem.json', 'pinned_prior_report.json',
                   'ROOT_SOURCE_MATCH_AND_PROOF_NOTES.md', 'inspect_closed_evidence.py',
                   'ROOT_CLOSED_EVIDENCE_INSPECTION.json']
actual_manifest = row(A / 'root_original_actual_reproduction/MANIFEST.json', A)
family_hashes = {family: info['manifest']['sha256'] for family, info in families.items()}
qualification = digest(regular(P / 'SOURCE_PRECISION_QUALIFICATIONS.md'))
root_notes = digest(regular(A / 'ROOT_SOURCE_MATCH_AND_PROOF_NOTES.md'))
pins = dict(schema='PR43_SOURCE_ONLY_FIXED_INPUT_CONTRACT_v1',
    status='SOURCE_ONLY_FIXED_INPUTS_FUTURE_ROOT_PREREQUISITES_PENDING',
    utc=dt.datetime.now(dt.timezone.utc).isoformat(), snapshot_manifest=row(A / 'snapshot_manifest.json', A),
    retained_closures=retained, auxiliary=[row(A / name, A) for name in auxiliary_names],
    root_foreign_members=members(A / 'foreign_primary'), families=families,
    qualification_sha256=qualification, root_proof_notes_sha256=root_notes,
    actual_reproduction_manifest_sha256=actual_manifest['sha256'], family_manifest_sha256=family_hashes,
    source_preparation_approval=False, genuine_ROOT_prerequisites='PENDING',
    original_substantive_attempts=0, new_substantive_attempts=0, audit_turns=0,
    ROOT_first_party_mechanical_inspection='actual evidence pinned; genuine ROOT ledger still PENDING',
    unrelated_ROOT_PR41_capture_siblings='excluded by explicit relevant-only membership',
    excluded_foreign_body_copying=False, scientific_helper_execution=False)
write_json('INPUT_PINS.json', pins)
flags = {name: False for name in [
    'original_mathematical_body_and_complete_original_diff_fully_read',
    'operative_primary_definitions_target_and_full_JKP_v2_proof_fully_read',
    'printed_source_proof_repairs_and_historical_qualifications_fully_read_and_accepted',
    'whole_raw_SQL_and_absent_prior_actual_evidence_fully_read',
    'unchanged_original_helper_actual_reproductions_and_all_results_fully_read',
    'both_closed_independent_families_fully_read',
    'all_first_party_closures_and_individual_foreign_exclusions_mechanically_checked',
    'exact_prior_published_source_match_and_scoped_partial_acceptance_accepted']}
common = dict(schema='PR43_DRAFT_NOT_ROOT_APPROVAL_v1', created_utc=None, reading_completed=False,
    root_flags=flags, reading_notes=None, scope_certificate_sha256=None,
    preparation_manifest_sha256=None, source_qualification_sha256=qualification,
    root_proof_notes_sha256=root_notes, actual_reproduction_manifest_sha256=actual_manifest['sha256'],
    family_manifest_sha256=family_hashes, original_substantive_attempts=0,
    new_substantive_attempts=0, audit_turns=0,
    instruction='ROOT must separately author a genuine external record after full reading; this false/null draft is never approval.')
write_json('DRAFT_ROOT_READ_LEDGER.json', common)
science = dict(common, status='PENDING_ROOT_READING_AND_APPROVAL', partial_valid=False,
    full_target_resolved_in_prior_published_literature=False, full_problem_solved_by_project=False,
    novelty_claimed=False, turn_limit=5, prior_publication_doi='10.4064/sm210413-16-9',
    read_ledger_sha256=None, current_input_manifest_sha256=None, new_whole_current_gate='PENDING',
    current_model=None, current_reasoning_effort=None, current_deadline_utc=None,
    current_verdict=None, paper_created=False, new_DOI_created=False, tracker_row_created=False)
write_json('DRAFT_ROOT_SCIENCE_CARD.json', science)
native = ['draft_pr_publication_program_20260930/inventory.json'] + [
    'unsolved_math_prioritization/' + name for name in [
        'QUEUE.md', 'assessments.json', 'cache/catalog.sqlite', 'cache/problems.json',
        'cache/research_results.json', 'catalog.json', 'history.jsonl', 'manifest.json',
        'policy.json', 'queue.py', 'review_v2/related_target_groups.json', 'state.json']]
write_json('DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json', dict(schema='PR43_DRAFT_FRESH13_NOT_APPROVAL_v1',
    approved_by_root=False, reason=None, created_utc=None, current_head=None, files=[], required_paths=native,
    instruction='ROOT must genuinely inspect and bind actual main HEAD/all13 whole inputs after source closure; no preparation observation is a current approval.'))
draft = '''# DRAFT — not ROOT approval

DRAFT_SCOPE_PENDING_ROOT_READING
PR43 / 30004386 / OWR-17469-011
Original head: 86be0f85c7a37a5cad8d24abd16a32d8d1f27e62
Original base: 60292bed09f59236aa192cb17aa138f7b4750e1a
Proposed status after genuine approval: already_solved
Prior publication: 10.4064/sm210413-16-9
NEW whole-current review: PENDING
Original turns: 0/5; new: 0; audit: 0
Project discovery: false
Paper/new DOI/tracker: false

ROOT must separately author ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md after
full scientific/source/provenance reading and mechanical closure inspection.
Use marker ROOT_SCOPE_ACCEPTED_SOURCE_MATCH_ONLY and literal line
Status: already_solved only after genuine scoped acceptance. Record proof
assumptions, all printed-source repairs, actual/historical receipt distinction,
raw-key ABSENT/SQL{} fallback and publication limits. This pending draft has
no ROOT approval, no future freeze and no current whole verdict.
'''
with (P / 'DRAFT_ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md').open('x') as out:
    out.write(draft)
print(json.dumps(dict(status='OWN_ACTUAL_SOURCE_DOCUMENT_AND_PIN_AUTHORING_COMPLETE',
    input_pins_sha256=digest(regular(P / 'INPUT_PINS.json')),
    qualification_sha256=qualification,
    builder_source=row(P / 'prepare_current_packet.py', P),
    future_ROOT_operator_source=row(P / 'capture_root_builder_operation.py', P),
    families_unchanged=True, candidate_created=False,
    proposed_builder_operator_or_scientific_helpers_imported_compiled_executed=False), indent=2))

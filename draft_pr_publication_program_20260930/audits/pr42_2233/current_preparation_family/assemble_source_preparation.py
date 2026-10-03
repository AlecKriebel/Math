"""Authoring-only inspection and pin generation. Does not load/run/compile builder.

All writes stay in this source-preparation folder. No native, Git, remote,
canonical, scientific-helper or external-human operation is available here.
"""
import datetime as dt
import hashlib
import json
from pathlib import Path

P = Path(__file__).resolve().parent
A = P.parent
R = A.parents[2]
def H(raw):
    return hashlib.sha256(raw).hexdigest()
def J(path):
    return json.loads(path.read_bytes())
def row(path, anchor=A):
    assert path.is_file() and not path.is_symlink() and all(not p.is_symlink() for p in path.parents)
    raw = path.read_bytes()
    return dict(path=path.relative_to(anchor).as_posix(), bytes=len(raw), sha256=H(raw))
def inventory(root):
    files = []
    directories = set()
    assert root.is_dir() and not root.is_symlink()
    for path in sorted(root.rglob('*')):
        assert not path.is_symlink()
        if path.is_file():
            files.append(row(path, root))
        else:
            assert path.is_dir()
            directories.add(path.relative_to(root).as_posix())
    expected = {p.as_posix() for item in files for p in Path(item['path']).parents if p.as_posix() != '.'}
    assert directories == expected
    return files
def write(name, value):
    path = P / name
    assert not path.exists()
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
now = dt.datetime.now(dt.timezone.utc).isoformat()
literal = J(A / 'literal_geometry_family/final_seal.json')
exact = J(A / 'exact_spectrum_family/OWN_CLOSED_MANIFEST.json')
derivative_name = 'controls/primary_pdf_extract.stdout.txt'
first = [item for item in literal['first_party_closed_files'] if item['path'] != derivative_name]
derivative = [item for item in literal['first_party_closed_files'] if item['path'] == derivative_name]
assert len(derivative) == 1
foreign = literal['foreign_primary_excluded_files'] + derivative
exact_first = [dict(path=item['relative_path'], bytes=item['bytes'], sha256=item['sha256']) for item in exact['own_files_including_self'] if item['relative_path'] != 'OWN_CLOSED_MANIFEST.json']
exact_foreign = [dict(path=item['relative_path'], bytes=item['bytes'], sha256=item['sha256']) for item in exact['foreign_files_inside_root_individually_excluded']]
families = {}
for name, manifest, copied, foreign_rows in [('literal_geometry_family', 'final_seal.json', first, foreign), ('exact_spectrum_family', 'OWN_CLOSED_MANIFEST.json', exact_first, exact_foreign)]:
    actual = inventory(A / name)
    expected = copied + foreign_rows + [row(A / name / manifest, A / name)]
    assert sorted(actual, key=lambda item: item['path']) == sorted(expected, key=lambda item: item['path'])
    families[name] = dict(manifest=row(A / name / manifest, A / name), copied_members=copied, foreign_members=foreign_rows, copied_count=len(copied), foreign_count=len(foreign_rows))
closures = ['root_original_actual_reproduction_v2', 'root_original_actual_reproduction',
            'original_git_commands', 'original_git_commands_v2',
            'root_original_branch_fetch_actual_capture', 'root_original_export_actual_capture',
            'root_original_export_v2_actual_capture', 'root_original_reproduction_outer_actual_capture',
            'root_original_reproduction_v2_outer_actual_capture']
retained = [dict(directory=name, files=inventory(A / name)) for name in closures]
auxiliary = ['ORIGINAL_GIT_COMMANDS.json', 'ORIGINAL_GIT_COMMANDS_V2.json',
             'ROOT_EXPORT_BASE_CORRECTION.json', 'ROOT_INITIAL_SOURCE_PIN.json',
             'pinned_problem.json', 'pinned_prior_report.json', 'snapshot_manifest_v2.json',
             'original_diff_v2.patch', 'capture_root_command.py', 'export_original_snapshot.py',
             'export_original_snapshot_v2.py', 'reproduce_original_checks.py',
             'reproduce_original_checks_v2.py', 'RESEARCH_LOG.md']
snapshot = J(A / 'snapshot_manifest_v2.json')
assert H((A / 'snapshot_manifest_v2.json').read_bytes()) == 'fb02fd7824cbe28845f88a404f59420ccb5c794c6e7e95338e8b6d29bdb61c0f'
actual_original = inventory(A / 'source_snapshot_v2')
expected_original = [dict(path=item['path'], bytes=item['size'], sha256=item['sha256']) for item in snapshot['files']]
assert actual_original == expected_original and len(actual_original) == 17
assert inventory(A / 'source_snapshot') == []
assert H((A / 'literal_geometry_family/final_seal.json').read_bytes()) == 'ad900516fdf42696ecfdc29f4e8c775fffa13ae7f49239e2127d8c46e381daae'
assert H((A / 'exact_spectrum_family/OWN_CLOSED_MANIFEST.json').read_bytes()) == '8817acbf2645b271cf9e28e553de30344648eb4192bbbe075e569a93e1bf387a'
result = J(A / 'root_original_actual_reproduction_v2/RESULT.json')
assert result['status'] == 'PASS_ROOT_GENUINE_ORIGINAL_REPRODUCTION'
assert result['original_prior_raw_key_present'] is False
assert result['author_assertions'] == 18306 and result['independent_assertions'] == 1263
assert result['reviewed_author_and_independent_saved_files_byte_exact'] is True
native_names = ['unsolved_math_prioritization/' + name for name in ['QUEUE.md', 'state.json', 'history.jsonl', 'catalog.json', 'assessments.json', 'queue.py', 'policy.json', 'manifest.json', 'cache/problems.json', 'cache/research_results.json', 'cache/catalog.sqlite', 'review_v2/related_target_groups.json']] + ['draft_pr_publication_program_20260930/inventory.json']
native_rows = [row(R / name, R) for name in sorted(native_names)]
pins = dict(schema='PR42_SOURCE_ONLY_INPUT_PINS_v1', status='SOURCE_ONLY_FIXED_INPUTS_FUTURE_ROOT_PREREQUISITES_PENDING', utc=now,
            original_head=snapshot['head'], original_base=snapshot['base'], original_manifest=row(A / 'snapshot_manifest_v2.json'), original17=actual_original,
            retained_closures=retained, auxiliary=[row(A / name) for name in auxiliary], families=families,
            family_manifest_sha256={name: info['manifest']['sha256'] for name, info in families.items()},
            actual_reproduction_manifest_sha256=H((A / 'root_original_actual_reproduction_v2/MANIFEST.json').read_bytes()),
            qualification_sha256=H((P / 'SOURCE_PRECISION_QUALIFICATIONS.md').read_bytes()),
            native13_at_preparation=native_rows, preparation_native13_is_dated_not_future_approval=True,
            expected_empty_failed_export_directory='source_snapshot', current_or_future_root_verdict_claimed=False)
write('INPUT_PINS.json', pins)
flags = ['original_mathematical_body_fully_read', 'operative_primary_definitions_and_target_fully_read',
         'source_precision_and_historical_qualifications_fully_read_and_accepted',
         'whole_raw_SQL_and_absent_prior_actual_evidence_fully_read',
         'unchanged_original_helper_actual_reproductions_fully_read',
         'both_closed_independent_families_fully_read',
         'closed_input_manifests_and_retained_evidence_exactly_checked', 'scoped_scientific_conclusions_accepted']
draft = dict(schema='PR42_DRAFT_NOT_ROOT_APPROVAL_v1', utc=now, reading_completed=False,
             root_flags={flag: False for flag in flags}, scope_certificate_sha256=None,
             preparation_manifest_sha256=None, source_qualification_sha256=pins['qualification_sha256'],
             actual_reproduction_manifest_sha256=pins['actual_reproduction_manifest_sha256'],
             family_manifest_sha256=pins['family_manifest_sha256'], original_substantive_attempts=2,
             new_substantive_attempts=0, audit_turns=0,
             instruction='ROOT must author a separate genuine external record after full reading. This false/null draft is never approval.')
write('DRAFT_ROOT_READ_LEDGER.json', draft)
science = dict(draft, status='PENDING_ROOT_READING_AND_APPROVAL', partial_valid=False,
               full_problem_solved=False, novelty_claimed=False, turn_limit=5,
               read_ledger_sha256=None, current_input_manifest_sha256=None,
               current_model=None, current_reasoning_effort=None, current_deadline_utc=None,
               current_verdict=None, new_whole_current_gate='PENDING')
write('DRAFT_ROOT_SCIENCE_CARD.json', science)
write('DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json', dict(schema='PR42_DRAFT_FRESH13_NOT_APPROVAL_v1', approved_by_root=False, reason=None, created_utc=None, current_head=None, files=[], required_paths=sorted(native_names), instruction='ROOT must genuinely inspect and pin current main HEAD and all13 whole live files; preparation-time pins are only dated evidence.'))
write('STATIC_INPUT_INSPECTION.json', dict(schema='PR42_AUTHORING_ONLY_STATIC_INPUT_INSPECTION_v1', utc=now,
          builder_imported_executed_compiled=False, candidate_created=False, original17_complete_bytes_verified=True,
          actual_result_whole_JSON_parsed=True, actual_root_PID89127_exit0_receipt_retained=True,
          raw_prior_key_absent_not_null=True, scoped_science_review_owner='ROOT; not attested by preparer',
          family_counts={name: dict(copied=info['copied_count'], foreign=info['foreign_count'], manifest_self=1) for name, info in families.items()},
          literal_derivative_exclusion=derivative, retained_closure_counts={info['directory']:len(info['files']) for info in retained},
          original2_new0_audit0=True, current_model=None, current_reasoning_effort=None, current_deadline_utc=None,
          native_canonical_git_index_remote_writes=False, external_human_contact=False))
print(json.dumps(dict(status='SOURCE_ONLY_AUTHORING_INPUTS_INSPECTED', utc=now, original17=17,
                     families={name: dict(copied=info['copied_count'], foreign=info['foreign_count']) for name,info in families.items()},
                     retained_files=sum(len(info['files']) for info in retained), builder_imported_executed_compiled=False)))

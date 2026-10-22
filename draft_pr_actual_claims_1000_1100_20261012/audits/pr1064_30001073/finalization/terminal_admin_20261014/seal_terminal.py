#!/usr/bin/env python3
"""Seal the completed terminal administrative records without changing the package."""
from pathlib import Path
import datetime, hashlib, json

HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parent.parent / 'preprint_v1_0'

def require(condition, message):
    if not condition:
        raise ValueError(message)

def load(path):
    return json.loads(path.read_text())

def rec(path, root):
    data = path.read_bytes()
    return {'path': path.relative_to(root).as_posix(), 'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest()}

def write_new(path, obj):
    require(not path.exists(), 'preserve existing seal: ' + str(path))
    path.write_text(json.dumps(obj, indent=2) + chr(10))

def main():
    require(not (HERE / 'tmp').exists() and not (HERE / 'tmp_resume').exists(), 'scratch remains')
    final = load(HERE / 'RESUME_FINAL_CUSTODY_RECEIPT.json')
    require(final['pass'] and final['immediate_boundary'] == 494 and
            final['whole03_prior_input_records_retained'] == 467 and
            final['current_package_files'] == 204 and
            final['historical_record_resolutions'] == 1510, 'custody gate differs')
    for name in ('REPRODUCTION_RECEIPTS.json', 'RESUME_REPRODUCTION_RECEIPTS.json'):
        data = load(HERE / name)
        require(data['pass'] and data['actual_commands'] == 481 and
                data['successes'] == 13 and data['expected_nonzero_rejections'] == 468,
                'actual reproduction gate differs')
    for name in ('GUARD_CONTROL_RECEIPTS.json', 'RESUME_GUARD_CONTROL_RECEIPTS.json'):
        data = load(HERE / name)
        require(data['pass'] and data['protected_inputs'] == 203 and
                data['hardlink_rejections'] == 406 and data['all_sentinels_unchanged'],
                'guard gate differs')
    for row in load(HERE / 'FINAL_CURRENT_PINS.json')['records']:
        require(rec(PACKAGE / row['path'], PACKAGE) == row, 'current package differs')
    for name in ('EXECUTIONS.jsonl', 'RESUME_EXECUTIONS.jsonl'):
        commands = [json.loads(line) for line in (HERE / name).read_text().splitlines()]
        require(len(commands) == 481 and all((r['returncode'] == 0) == r['expected_success']
                                           for r in commands), 'actual command ledger differs')
    files = sorted(p for p in HERE.rglob('*') if p.is_file() and
                   not {'tmp', 'tmp_resume', '__pycache__'}.intersection(p.relative_to(HERE).parts)
                   and p.name not in ('OUTPUT_PINS.json', 'SEAL.json'))
    records = [rec(p, HERE) for p in files]
    require(all(not p.is_symlink() for p in files), 'unexpected output symlink')
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    write_new(HERE / 'OUTPUT_PINS.json', {
        'utc': now,
        'scope': 'All local terminal administrative files, including exact saved-before snapshots and preserved failed resumption helpers; excludes this self-seal and separate SEAL.json. No candidate or historical seal rebound.',
        'entries': records,
    })
    write_new(HERE / 'SEAL.json', {
        'utc': now,
        'status': 'TERMINAL_ADMIN_RECONCILIATION_COMPLETE_ROOT_ADOPTION_REQUIRED',
        'stage': 'READY_FOR_SUBMISSION_UNPUBLISHED_HELD_AFTER_1032',
        'pr': 1064,
        'head': 'bdefe31b9d226c8f27008d13f57775d5de8df3d7',
        'whole_package_reviews_completed': 3,
        'whole_package_reviews_required': 2,
        'latest_complete_whole_review_actionable_P0_P1_P2_P3': 0,
        'this_is_another_whole_review': False,
        'root_terminal_adoption_required': True,
        'ready_for_submission_after_root_adoption': True,
        'publication_ready': False,
        'published': False,
        'issues_updated': False,
        'ascending_publication_hold_after_pr': 1032,
        'accepted_math_source_TeX_PDF_and_existing_bibliographic_bytes_unchanged': True,
        'metadata_objects_equal': True,
        'native_repository_check_local_only': True,
        'prior_original_commands': 481,
        'separate_resumed_clean_commands': 481,
        'separate_readonly_commands': 3,
        'initial_boundary_records': 422,
        'expanded_boundary_records': 494,
        'whole03_input_boundary_records': 467,
        'authorized_admin_changes': 9,
        'unchanged_boundary_records': 485,
        'current_package_files': 204,
        'historical_resolutions': 1510,
        'old_copy_records_preserved': 122,
        'new_exact_copies': 41,
        'current_source_equal_copies': 163,
        'individual_omissions': 29,
        'archive_members': 193,
        'paper_pdf': rec(PACKAGE / 'paper.pdf', PACKAGE),
        'paper_tex': rec(PACKAGE / 'paper.tex', PACKAGE),
        'support_zip': rec(PACKAGE / 'support.zip', PACKAGE),
        'native_manifest': rec(PACKAGE / 'publication/zenodo-deposit.json', PACKAGE),
        'output_pins': rec(HERE / 'OUTPUT_PINS.json', HERE),
        'report': rec(HERE / 'FINALIZATION_REPORT.md', HERE),
        'current_package_pins': rec(HERE / 'FINAL_CURRENT_PINS.json', HERE),
        'final_resumed_custody': rec(HERE / 'RESUME_FINAL_CUSTODY_RECEIPT.json', HERE),
        'full_code_prose_diff': rec(HERE / 'COMPLETE_CODE_PROSE_DIFF.patch', HERE),
    })
    for row in load(HERE / 'OUTPUT_PINS.json')['entries']:
        require(rec(HERE / row['path'], HERE) == row, 'finalization output changed during seal')
    print(json.dumps({'pass': True, 'sealed_outputs': len(records),
                      'output_pins': rec(HERE / 'OUTPUT_PINS.json', HERE),
                      'terminal_seal': rec(HERE / 'SEAL.json', HERE)}, indent=2))

if __name__ == '__main__':
    main()

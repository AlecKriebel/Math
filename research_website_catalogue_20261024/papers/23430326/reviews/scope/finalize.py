#!/usr/bin/env python3
"""Seal this source/scope handoff; never execute submitted support programs."""
from pathlib import Path
import datetime
import hashlib
import json
import re
import stat
import zipfile

O = Path(__file__).resolve().parent
P = O.parents[1]
S = P / 'sources'

def read(p):
    return json.loads(p.read_text())

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def save(p, value):
    with p.open('x') as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def binding(p):
    return {'path': str(p.relative_to(P)), 'bytes': p.stat().st_size, 'sha256': sha(p)}

now = datetime.datetime.now(datetime.timezone.utc).isoformat()
baseline = read(O / 'source-baseline.json')
custody = []
for old in baseline['files']:
    after = binding(P / old['path'])
    assert after == old, old['path']
    custody.append({'before': old, 'after': after, 'unchanged': True})
for old in read(O / 'initial-seal-bindings.json')['files']:
    assert binding(P / old['path']) == old, old['path']

raw = read(S / 'record-raw.json')
record = read(S / 'record.json')
assert raw == record
assert str(record['id']) == '23430326'
assert record['metadata']['version'] == '1.1'
assert record['metadata']['publication_date'] == '2026-10-16'
expected = {
    'paper.pdf': (106606, 'b5eac802fb40161d2a129b0f9898d348', '1144eb3999212084bef013e7984bfc54bf43a9f931d959b63ba2743d814cf0a9'),
    'pr1032_supportkit_v1.1.zip': (394529, 'c23fde2093aa0627daa36ba61d6bca1f', '1f1a66d7e67b1434e4c17af96c9461b1d2f6bd7f4197de4ef88f95aad8105dc1'),
}
for name, (size, md5, digest) in expected.items():
    payload = (S / name).read_bytes()
    assert len(payload) == size and hashlib.md5(payload).hexdigest() == md5
    assert hashlib.sha256(payload).hexdigest() == digest
    api = next(row for row in record['files'] if row['key'] == name)
    assert api['size'] == size and api['checksum'].lower() == 'md5:' + md5
    receipt = next(row for row in read(S / 'receipt.json')['files'] if row['name'] == name)
    assert receipt['bytes'] == size and receipt['md5'] == md5 and receipt['sha256'] == digest

members = []
with zipfile.ZipFile(S / 'pr1032_supportkit_v1.1.zip') as archive:
    assert len(archive.infolist()) == 37
    for item in archive.infolist():
        path = Path(item.filename)
        mode = item.external_attr >> 16
        assert not path.is_absolute() and '..' not in path.parts
        assert not item.flag_bits & 1
        assert not stat.S_ISLNK(mode) and not item.is_dir()
        assert not path.suffix.lower() in {'.zip', '.tar', '.gz', '.7z', '.rar'}
        payload = archive.read(item)
        assert payload == (S / 'support' / item.filename).read_bytes()
        members.append({'member': item.filename, 'bytes': len(payload), 'sha256': hashlib.sha256(payload).hexdigest(), 'unchanged': True})
assert (S / 'support/paper.pdf').read_bytes() == (S / 'paper.pdf').read_bytes()
assert set(read(S / 'support/ALLOWLIST.json')['files']) == {row['member'] for row in members}
manifest = read(S / 'support/MANIFEST.json')['files']
assert len(manifest) == 36
for row in manifest:
    assert (S / 'support' / row['path']).stat().st_size == row['bytes']
    assert sha(S / 'support' / row['path']) == row['sha256']

primary = []
for filename in ['primary-acquisition-receipt.json', 'primary-additional-acquisition-receipt.json']:
    for row in read(S / filename)['sources']:
        if row.get('raw_path') and row.get('sha256'):
            assert sha(P / row['raw_path']) == row['sha256'], row['name']
        if row.get('text_path') and row.get('text_sha256'):
            assert sha(P / row['text_path']) == row['text_sha256'], row['name']
        primary.append(row['name'])
for row in read(O / 'primary-read-ledger.json')['sources']:
    assert row['name'] in primary
    if row.get('raw_path') and row.get('sha256'):
        assert sha(P / row['raw_path']) == row['sha256']
    if row.get('text_path') and row.get('text_sha256'):
        assert sha(P / row['text_path']) == row['text_sha256']

tex = (S / 'support/paper.tex').read_text()
abstract = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex, re.S).group(1).strip()
check = read(O / 'abstract-check.json')
candidate = read(O / 'content.json')
assert abstract == (O / 'abstract-source.tex').read_text().strip()
assert hashlib.sha256(abstract.encode()).hexdigest() == check['source_abstract_sha256']
assert sha(S / 'support/paper.tex') == check['source_tex_sha256']
assert candidate['abstract_original_tex'] == abstract
assert candidate['abstract'] == check['normalized_abstract']
assert candidate['abstract_paragraphs'] == [check['normalized_abstract']]
assert candidate['abstract_heading'] == 'Original abstract'
assert candidate['mathematical_verdict'] is None
for flag in ['mathematical_clearance', 'publication_clearance', 'page_promotion_permission']:
    assert candidate[flag] is False
assert candidate['follow_up'] is None
assert candidate['canonical_url'] is None

save(O / 'custody-before-after.json', {
    'record_id': '23430326', 'utc': now,
    'initial_source_baseline_sha256': sha(O / 'source-baseline.json'),
    'initial_scope_seal_sha256': sha(O / 'independent-scope-seal.json'),
    'all_initial_source_files_unchanged': True,
    'source_before_after': custody,
    'all_archive_member_bytes_unchanged': True, 'archive_members': members,
    'raw_and_normalized_api_parsed_equal': True,
    'source_helpers_executed': False,
    'note': 'Primary-source cache files and own review derivatives are additional acquisitions, never replacements for original authorities.'
})
save(O / 'verdict.json', {
    'record_id': '23430326', 'sheet_row': 85, 'utc': now,
    'task_status': 'COMPLETE', 'completion_estimate_percent_of_assigned_source_scope_task': 100,
    'scope_verdict': 'LITERAL_FULL_TARGET_CONVENTIONS_AND_CREDIT_SCOPE_COMPLETE',
    'scope_mismatch': None, 'original_claim_weakened': False,
    'source_authenticated': True, 'source_originals_preserved': True,
    'full_actual_manuscript_read': True, 'full_original_abstract_preserved': True,
    'independent_initial_seal_before_historical_opinion_bodies': True,
    'current_sibling_review_bodies_read': False,
    'mathematical_verdict': None, 'mathematical_clearance': False,
    'publication_clearance': False, 'page_promotion_permission': False,
    'candidate_held': True, 'candidate': 'reviews/scope/content.json',
    'report': 'reviews/scope/REVIEW.md',
    'strongest_verified_scope_finding': 'The authenticated full target and inspected primary interfaces admit the stated literal scope and credit boundaries; no literal target/convention mismatch was found. This is not an independent complete mathematical verdict.',
    'remaining_gaps': [
        'Separate independent complete mathematical lanes and root adjudication of all analytic and noninduction steps.',
        'Complete Luo–Zha body not inspected; all substantive parameter/mechanism/period-consequence overlap and historical priority remain UNKNOWN.',
        'No exhaustive worldwide novelty or current open-status conclusion.'
    ],
    'source_helpers_executed': False, 'fresh_mathematical_program_results_claimed': False,
    'follow_up': None, 'external_contact_or_outreach': False,
    'publication_configuration_created': False, 'promotion_configuration_created': False,
    'public_page_rendered': False, 'live_action': False, 'browser_ui_used': False, 'web_primary_sources_retrieved': True,
    'native_sheet_mutated': False, 'native_AA': None,
    'overall_programme_completion_claimed': False
})
save(O / 'validation.json', {
    'record_id': '23430326', 'utc': now, 'validation_kind': 'SOURCE_SCOPE_CUSTODY_AND_SCHEMA_ONLY',
    'baseline_files_rehashed': len(custody), 'all_baseline_files_unchanged': True,
    'archive_regular_member_bytes_verified': len(members), 'manifest_entries_verified': len(manifest),
    'primary_acquisition_rows_bound': len(primary),
    'raw_normalized_metadata_equal': True, 'api_receipt_expected_asset_hashes_match': True,
    'standalone_embedded_pdf_equal': True, 'complete_original_abstract_equal': True,
    'candidate_held_flags_consistent': True, 'source_programs_executed': False,
    'mathematical_clearance': False, 'publication_clearance': False,
    'write_scope': ['sources/', 'reviews/scope/'],
    'separate_current_lanes_not_read': True
})
with (O / 'RESEARCH_LOG.md').open('a') as stream:
    stream.write(f'\n{now} — Complete scope report and held content candidate finalized. All initial authority files, all37 archive members, internal manifest, primary receipts and complete abstract rehashed successfully. Completion estimate: **100% of assigned source/scope task**. Separate mathematical/root gates remain pending; full Luo–Zha comparison remains UNKNOWN. No submitted helper execution, current sibling-lane reading, publication configuration, native mutation, Git action or external communication.\n')

excluded = {'SEAL.json', 'SEAL.sha256', 'SHA256SUMS'}
files = sorted(p for directory in [S, O] for p in directory.rglob('*') if p.is_file() and not (p.parent == O and p.name in excluded))
seal = {
    'record_id': '23430326', 'utc': now, 'seal_kind': 'SOURCE_SCOPE_HANDOFF_ONLY',
    'scope_task_complete': True, 'mathematical_clearance': False, 'publication_clearance': False,
    'files': [binding(path) for path in files],
    'source_initial_seal_sha256': sha(O / 'independent-scope-seal.json'),
    'follow_up': None, 'excludes_self_and_sha_manifests': True
}
save(O / 'SEAL.json', seal)
with (O / 'SHA256SUMS').open('x') as stream:
    for row in seal['files']:
        stream.write(row['sha256'] + '  ' + row['path'] + '\n')
    stream.write(sha(O / 'SEAL.json') + '  reviews/scope/SEAL.json\n')
with (O / 'SEAL.sha256').open('x') as stream:
    stream.write(sha(O / 'SEAL.json') + '  SEAL.json\n')
print(json.dumps({'record_id': '23430326', 'scope_status': 'COMPLETE', 'seal_sha256': sha(O / 'SEAL.json'), 'sealed_files': len(seal['files']), 'mathematical_clearance': False, 'publication_clearance': False}))

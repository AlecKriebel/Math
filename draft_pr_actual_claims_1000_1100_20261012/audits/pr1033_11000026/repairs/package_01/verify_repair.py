"""Reproducible integrity checks for PKG-01; not a new adversarial review.

Run with PYTHONDONTWRITEBYTECODE=1 python3 -B. Receipt/pins live outside the
archive, avoiding a circular hash of the archive inside itself. No services,
Git state, source bodies, or mathematical conclusions are changed.
"""
import datetime
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import runpy
import stat
from urllib.parse import unquote, urlsplit
import zipfile

ROOT = Path(__file__).resolve().parents[2]
PUB = ROOT / 'publication'
REPAIR = Path(__file__).resolve().parent
PREFIX = 'teichmuller_original_ball_paths_v1/'
RAW = 'publication/evidence/metric_01/sources/farb_printed_24_25.txt'
ALLOWED_CHANGED = {
    'CANDIDATE_INTEGRITY.json', 'RESEARCH_LOG.md', 'prepare_package.py',
    'publication/PACKAGE_MANIFEST.json', 'publication/README.md',
    'publication/SUPPLEMENT.md', 'publication/evidence/AUDIT_COPY_MANIFEST.json',
    'publication/evidence/CURRENT_REVIEW_STATE.json', 'publication/evidence/INDEX.md',
    'publication/teichmuller_original_ball_paths_source_audits_v1.zip',
}


def pin(path):
    return {'bytes': path.stat().st_size,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def row(path):
    return {'path': path.relative_to(ROOT).as_posix(), **pin(path)}


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def main():
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    before = json.loads((REPAIR / 'BASELINE_FILE_PINS.json').read_text())
    baseline = {item['path']: item for item in before['files']}
    protected = []
    changed_before = []
    for name, item in baseline.items():
        p = ROOT / name
        if name == RAW:
            assert not p.exists()
            continue
        if name in ALLOWED_CHANGED:
            if pin(p) != {k: item[k] for k in ('bytes', 'sha256')}:
                changed_before.append(name)
            continue
        assert pin(p) == {k: item[k] for k in ('bytes', 'sha256')}, name
        protected.append(name)
    raw_private = ROOT / 'reviews/metric_01/sources/farb_printed_24_25.txt'
    assert pin(raw_private) == {k: baseline[RAW][k] for k in ('bytes', 'sha256')}

    original = json.loads((ROOT / 'SUBMITTED_PINS.json').read_text())
    assert len(original['files']) == 8
    original_checks = []
    for item in original['files']:
        source = ROOT / item['snapshot_path']
        target = PUB / 'evidence' / item['snapshot_path']
        assert source.read_bytes() == target.read_bytes()
        assert pin(source) == {k: item[k] for k in ('bytes', 'sha256')}
        original_checks.append({'snapshot_path': item['snapshot_path'], **pin(target),
                                'snapshot_and_distribution_identical': True})
    original_inventory = json.loads((ROOT / 'submitted/MANIFEST.json').read_text())
    assert sorted(original_inventory['files_exactly']) == sorted(p.name for p in (ROOT / 'submitted').iterdir() if p.is_file())
    for item in original_inventory['files']:
        assert pin(ROOT / 'submitted' / item['path']) == {k: item[k] for k in ('bytes', 'sha256')}

    copies = json.loads((PUB / 'evidence/AUDIT_COPY_MANIFEST.json').read_text())
    old_copies = json.loads((REPAIR / 'before/publication/evidence/AUDIT_COPY_MANIFEST.json').read_text())
    retained = [item for item in old_copies['files'] if item['path'] != RAW.removeprefix('publication/')]
    assert copies['files'][:39] == retained and len(copies['files']) == 54
    assert len({item['path'] for item in copies['files']}) == 54
    copy_checks = []
    for item in copies['files']:
        source, target = ROOT / item['audit_source_path'], PUB / item['path']
        assert source.read_bytes() == target.read_bytes()
        assert pin(target) == {k: item[k] for k in ('bytes', 'sha256')}
        copy_checks.append({**item, 'source_and_copy_identical': True})
    authored = ROOT / 'reviews/package_01'
    output = json.loads((authored / 'OUTPUT_PINS.json').read_text())
    assert len(output['files']) == 14
    for item in output['files']:
        assert pin(authored / item['path']) == {k: item[k] for k in ('bytes', 'sha256')}
    assert {item['path'].removeprefix('evidence/package_01/') for item in copies['files'][39:]} == {
        p.name for p in authored.iterdir() if p.is_file()}
    old_input = json.loads((authored / 'INPUT_PINS_FINAL.json').read_text())
    assert old_input['all_initial_bytes_unchanged'] is True
    assert old_input['tree_unchanged'] is True
    stage = json.loads((PUB / 'evidence/PACKAGE_01_REPAIR_STAGE_MAPPING.json').read_text())
    assert stage['historical_stage']['reviewed_archive'] == baseline['publication/teichmuller_original_ball_paths_source_audits_v1.zip']
    assert stage['historical_stage']['reviewed_package_manifest'] == baseline['publication/PACKAGE_MANIFEST.json']
    assert stage['appended_authored_records'] == copies['files'][39:]
    root_pins = json.loads((ROOT / 'ROOT_MATH_ACCEPTANCE.json').read_text())['authored_output_pins']
    for item in root_pins:
        assert pin(ROOT / item['path']) == {k: item[k] for k in ('bytes', 'sha256')}
    assert 'authored_output_pins' in stage['intentionally_omitted_raw_body']['root_historical_output_pin']

    select = runpy.run_path(str(ROOT / 'prepare_package.py'))['is_authored_review_record']
    filter_checks = []
    for family in ('metric_01', 'teich_source_01', 'priority_01', 'package_01'):
        d = ROOT / 'reviews' / family
        selected = {p.relative_to(d).as_posix() for p in d.rglob('*') if p.is_file() and select(p, d)}
        included = {item['audit_source_path'].removeprefix('reviews/' + family + '/')
                    for item in copies['files'] if item['audit_source_path'].startswith('reviews/' + family + '/')}
        assert selected == included, family
        filter_checks.append({'family': family, 'selected_records': len(selected),
                              'selected_set_equals_distribution': True})
    assert not select(raw_private, ROOT / 'reviews/metric_01')
    probes = ['extracted/review.md', 'candidate_render/report.json', 'render/a.md',
              'renders/a.json', 'sources/raw/a.json', 'sources/rawprivate/a.md',
              'sources/raw_private/a.md', '.cache/a.json', 'cache/a.json',
              '__pycache__/a.json', '.venv/a.md', 'tmp/a.json', 'sources/a.txt',
              'sources/a.html', 'sources/a.pdf', 'sources/a.png', 'a.zip', 'a.pyc']
    assert all(not select(authored / name, authored) for name in probes)

    manifest_path = PUB / 'PACKAGE_MANIFEST.json'
    manifest = json.loads(manifest_path.read_text())
    files = [PUB / name for name in ('research_note.tex', 'research_note.pdf', 'README.md', 'SUPPLEMENT.md', 'metadata.json')]
    files.extend(p for p in (PUB / 'evidence').rglob('*') if p.is_file())
    files.sort(key=lambda p: p.relative_to(PUB).as_posix())
    expected = [{'path': p.relative_to(PUB).as_posix(), **pin(p)} for p in files]
    assert manifest['files'] == expected and len(expected) == 72
    assert manifest['third_party_papers_redistributed'] is False
    assert manifest['executable_verification_claimed'] is False
    assert manifest['manifest_self_hash_excluded'] is True
    forbidden = {'raw', 'rawprivate', 'raw_private', 'extracted', 'render', 'renders',
                 'candidate_render', 'cache', '.cache', '__pycache__', '.venv', 'tmp'}
    assert all(not (forbidden & {part.casefold() for part in PurePosixPath(item['path']).parts}) for item in expected)
    assert all(Path(item['path']).suffix.casefold() not in {'.txt', '.html', '.png', '.pyc', '.zip'} for item in expected)
    assert [item['path'] for item in expected if Path(item['path']).suffix.casefold() == '.pdf'] == ['research_note.pdf']
    assert all(item['sha256'] != baseline[RAW]['sha256'] for item in expected)

    archive = PUB / 'teichmuller_original_ball_paths_source_audits_v1.zip'
    entries = sorted(files + [manifest_path], key=lambda p: p.relative_to(PUB).as_posix())
    rebuilt = io.BytesIO()
    with zipfile.ZipFile(rebuilt, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in entries:
            info = zipfile.ZipInfo(PREFIX + p.relative_to(PUB).as_posix(), date_time=(2026, 10, 13, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, p.read_bytes())
    assert rebuilt.getvalue() == archive.read_bytes()
    with zipfile.ZipFile(archive) as z:
        infos = z.infolist()
        names = [item.filename for item in infos]
        assert z.testzip() is None
        assert len(names) == len(set(names)) == len({name.casefold() for name in names}) == 73
        assert names == [PREFIX + p.relative_to(PUB).as_posix() for p in entries]
        for item, p in zip(infos, entries):
            name = item.filename
            pure = PurePosixPath(name)
            assert name.isascii() and name.startswith(PREFIX)
            assert not pure.is_absolute() and '..' not in pure.parts and '\\' not in name
            assert name == pure.as_posix() and len(pure.parts) >= 2
            assert item.date_time == (2026, 10, 13, 0, 0, 0)
            assert stat.S_IFMT(item.external_attr >> 16) == stat.S_IFREG
            assert stat.S_IMODE(item.external_attr >> 16) == 0o644
            assert item.create_system == 3 and item.compress_type == zipfile.ZIP_DEFLATED
            assert z.read(name) == p.read_bytes()
        assert PREFIX + RAW.removeprefix('publication/') not in names

    parsed = [p.relative_to(PUB).as_posix() for p in sorted(PUB.rglob('*.json'))]
    for name in parsed:
        json.loads((PUB / name).read_text())
    metadata = json.loads((PUB / 'metadata.json').read_text())
    wrapper = json.loads((PUB / 'zenodo-deposit.json').read_text())
    assert wrapper['metadata'] == metadata
    assert pin(PUB / 'metadata.json') == {k: baseline['publication/metadata.json'][k] for k in ('bytes', 'sha256')}
    assert pin(PUB / 'zenodo-deposit.json') == {k: baseline['publication/zenodo-deposit.json'][k] for k in ('bytes', 'sha256')}
    assert all((PUB / item['path']).is_file() for item in wrapper['files'])
    navigation = []
    for name in ('README.md', 'SUPPLEMENT.md', 'evidence/INDEX.md'):
        p = PUB / name
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', p.read_text()):
            parsed_target = urlsplit(target)
            if parsed_target.scheme or not parsed_target.path:
                continue
            resolved = (p.parent / unquote(parsed_target.path)).resolve()
            assert resolved.is_relative_to(PUB) and resolved.is_file(), (name, target)
            navigation.append({'from': name, 'target': target, 'resolves': True})
    state = json.loads((PUB / 'evidence/CURRENT_REVIEW_STATE.json').read_text())
    assert state['next_gate'] == 'NEW independent whole-package review 02'
    assert state['fresh_package_reviews'][0]['status'] == 'ISSUES_FOUND'
    assert state['fresh_package_reviews'][1]['status'] == 'PENDING'
    assert state['all_actionable_issues_resolved'] is False
    assert state['preprint_ready_for_immutable_publication'] is False
    assert state['published'] is False

    receipt = {
        'utc': now, 'status': 'PASS', 'scope': 'PKG-01 repair integrity only; not independent review clearance',
        'repair_id': 'PKG-01', 'repair_completion_percent': 100,
        'archive_entries': 73, 'manifest_rows': 72,
        'archive_bytes': archive.stat().st_size,
        'archive_sha256': pin(archive)['sha256'],
        'package_manifest': pin(manifest_path),
        'authored_copy_manifest': pin(PUB / 'evidence/AUDIT_COPY_MANIFEST.json'),
        'paper_pages': 3, 'paper_pdf_bytes': (PUB / 'research_note.pdf').stat().st_size,
        'paper_pdf_sha256': pin(PUB / 'research_note.pdf')['sha256'],
        'tex_sha256': pin(PUB / 'research_note.tex')['sha256'],
        'metadata_sha256': pin(PUB / 'metadata.json')['sha256'],
        'original_copies_match': 8, 'retained_prior_authored_copies_match': 39,
        'appended_package_01_authored_copies_match': 15, 'authored_copies_match': 54,
        'baseline_protected_files_unchanged': len(protected),
        'private_review_files_unchanged': len([name for name in protected if name.startswith('reviews/')]),
        'frozen_root_output_pins_match_private_sources': len(root_pins),
        'raw_farb_extract_absent_from_distribution': True,
        'private_original_raw_extract_preserved': pin(raw_private),
        'zip_safe_names_crc_inventory_bytes_and_deterministic_reconstruction_pass': True,
        'navigation_manifest_metadata_wrapper_pass': True,
        'all_candidate_json_parses': True, 'candidate_json_files': len(parsed),
        'navigation_links_checked': len(navigation),
        'preprint_ready_for_immutable_publication': False,
        'new_whole_package_review_pending': True, 'next_gate': state['next_gate'],
        'verification_details': 'repairs/package_01/REPAIR_VERIFICATION.json'}
    save(ROOT / 'CANDIDATE_INTEGRITY.json', receipt)
    save(REPAIR / 'REPAIR_VERIFICATION.json', {
        'utc': now, 'receipt': receipt, 'baseline_changed_control_paths': changed_before,
        'baseline_deleted_paths': [RAW], 'protected_unchanged_paths': protected,
        'original_checks': original_checks, 'copy_checks': copy_checks,
        'filter_checks': filter_checks, 'additional_rejected_filter_probes': probes,
        'navigation_checks': navigation, 'current_manifest_checks': expected,
        'zip_reconstruction_sha256': hashlib.sha256(rebuilt.getvalue()).hexdigest()})
    candidate_files = sorted([p for p in PUB.rglob('*') if p.is_file()] + [ROOT / 'prepare_package.py', ROOT / 'build_package.py'])
    save(REPAIR / 'REPAIRED_CANDIDATE_PINS.json', {
        'utc': now, 'scope': 'Entire repaired publication tree plus preparation/build scripts; private own-PDF renders are pinned but excluded from ZIP',
        'review_status': 'package_02 PENDING', 'original_head': original['head_oid'],
        'files': [row(p) for p in candidate_files]})
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
